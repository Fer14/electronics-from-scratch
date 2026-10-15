# A Virtual Microcontroller

> Put the pieces of this phase on one imaginary chip: a core that runs assembly, a timer that wakes it, an ADC that reads a light sensor, a PWM that dims an LED, and a UART that reports. Then let our circuit simulator play the outside world.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 17 (Microcontrollers), Lessons 01-06; Phase 04 (Kirchhoff's Laws), Lesson 05 (The Voltage Divider); Phase 16 (A Computer from Gates), Lesson 06 (Instructions and Assembly)
**Time:** ~100 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Virtual microcontroller | A program that imitates a microcontroller closely enough to run its firmware. Also called an emulator or instruction-set simulator. | A flight simulator: the cockpit behaves like the real plane, but nothing flies. |
| Firmware image | The assembled program, ready to be loaded into flash. | The printed recipe card handed to the cook. |
| Reset vector | The address where the core starts after power-up or reset. | Page 1 of the recipe. |
| Interrupt vector | The address the core jumps to for one interrupt. | "If the doorbell rings, go to page 12." |
| Directive | A line in an assembly file that instructs the assembler, not the processor (here `.vector`). | A note to the printer, not part of the recipe. |
| Stack | A region of memory where return addresses are pushed and popped, last in, first out. | A pile of plates: the last one put down is the first one picked up. |
| Carry flag | A one-bit result that says an unsigned subtraction needed to borrow, meaning "the first number was smaller". | The "minus" sign you would have needed. |
| Sleep mode | A state where the core stops fetching instructions to save power until an interrupt wakes it. | Napping by the door until the bell rings. |
| Event-driven simulation | A simulation that jumps straight from one interesting moment to the next, instead of stepping through every tick. | Skipping the boring parts of a film. |
| Light-dependent resistor (LDR) | A resistor whose resistance falls as more light hits it. | A sponge that lets more water through the brighter it is. |
| Duty code | The 8-bit number written to the PWM register; duty = code / 256. | The setting on a dimmer dial. |
| Duty cycle of the CPU | The fraction of time the core is awake and running code. | The fraction of the day a night guard is actually walking around. |

## Learning Objectives

- Assemble and run a complete firmware image with a reset vector, an interrupt vector, a main loop that sleeps, and an interrupt routine that does the work
- Connect five memory-mapped peripherals (GPIO, timer, ADC, PWM, UART) to a core through one I/O address map
- Use the carry and zero flags to make decisions (`cpi` then `brsh`) and trace them by hand
- Run an event-driven simulation that skips the time the core spends asleep, and compute how much of the time the core is awake
- Close the loop between firmware and circuits: a simulated LDR divider feeds the ADC, and the PWM duty that the firmware chooses drives a simulated RC filter and LED

## The Problem

Each lesson of this phase built one part of a microcontroller in isolation. Real firmware never uses one part at a time. A product as simple as an automatic night light needs all of them at once:

- a **timer** to wake up 100 times per second,
- an **ADC** to read a light sensor,
- a **decision** ("is it daytime?") in code,
- a **PWM** output to set the LED brightness,
- a **GPIO** direction setting so the PWM actually reaches the pin,
- a **UART** to print what it is doing while you debug it,
- and **sleep** in between, because it runs from a battery.

Getting these to work together is where embedded programming really happens: the timer's rate decides how fresh the readings are, the order of instructions in the ISR decides what the LED does, one forgotten DDR bit means the pin never moves. And it all has to be checked against the circuits outside the chip: will the divider put the sensor voltage in the ADC's range? What brightness does a duty of 174 give? This lesson builds that whole system in about 250 lines of Python.

## The Physics

The outside world in this lesson has two parts.

**The light sensor.** A light-dependent resistor (also called a photoresistor) is a strip of a semiconductor such as cadmium sulfide. Light frees electrons in it (photons give them enough energy to cross the band gap, Phase 11, Lesson 01), so more light means more free charge carriers and lower resistance. Over a wide range the resistance follows a power law:

```
R_LDR = R_10 x (lux / 10) ^ (-gamma)
```

Read it as: "the resistance at 10 lux, times the light level relative to 10 lux raised to minus gamma". `lux` measures how much light falls on a surface (a dark night is below 1 lux, an office about 500, daylight 10 000 or more). We use `R_10 = 10 kohm` and `gamma = 0.7`, typical of small hobby LDRs. At 1000 lux: `10 k x 100^(-0.7) = 10 k x 0.0398 = 398 ohm`. At 1 lux: `10 k x 0.1^(-0.7) = 10 k x 5.01 = 50.1 kohm`. A hundred-fold range, which is why LDRs are easy to use.

We put the LDR on top of a divider with a fixed 4.7 kohm resistor to ground:

```
  VDD 3.3 V
     |
   [ LDR ]
     |
     +------> ADC input ("sense")
     |
   [ 4.7 k ]
     |
    gnd
```

More light, smaller LDR, higher voltage at `sense`. Phase 19, Lesson 02 shows how to choose the fixed resistor for the best sensitivity.

**The LED and filter.** The PWM pin drives a red LED through 150 ohm (Lesson 02). The eye sees the average current, `duty x I_on`. For an analog view of the same signal we also feed the PWM into the 10 kohm / 1 uF filter of Lesson 03 and read its average voltage, `duty x VDD`.

## The Concept

### The chip's memory map

Our virtual chip has this I/O address map. Every peripheral register is just an address the core can `out` to or `in` from:

| Name | Address | Peripheral | Meaning |
|------|---------|------------|---------|
| PINB | 0x03 | GPIO | read pin levels |
| DDRB | 0x04 | GPIO | direction: 1 = output |
| PORTB | 0x05 | GPIO | output levels |
| TCTRL | 0x10 | Timer | bit 0 = start |
| TCOMP | 0x11 | Timer | compare value: tick every 64 x (TCOMP + 1) cycles |
| ADCSTART | 0x20 | ADC | any write starts a conversion |
| ADCH | 0x21 | ADC | 8-bit result |
| PWMDUTY | 0x30 | PWM | duty code, duty = code / 256, output on PB1 |
| UDR | 0x40 | UART | write a byte to send it |

### The program format

The same assembly as Lesson 01, plus:

| Instruction | Meaning | Cycles |
|-------------|---------|--------|
| `cpi r1, 200` | compare r1 with 200: zero flag = (r1 == 200), carry flag = (r1 < 200) | 1 |
| `brsh label` | branch if same or higher (carry clear) | 1, 2 if taken |
| `brlo label` | branch if lower (carry set) | 1, 2 if taken |
| `sei` / `cli` | enable / disable interrupts | 1 |
| `sleep` | stop until an interrupt | 1 |
| `reti` | return from interrupt: pop the PC, re-enable interrupts | 4 |

And one directive: `.vector timer, tick` tells the assembler "the timer interrupt's vector is the address of the label `tick`". Execution starts at address 0, which is our reset vector.

### The firmware, line by line

```
.vector timer, tick
reset:
        ldi r0, 0b00000010     ; PB1 is the PWM pin
        out DDRB, r0           ; make it an output
        ldi r0, 155
        out TCOMP, r0          ; tick every 64 x 156 = 9984 cycles
        ldi r0, 1
        out TCTRL, r0          ; start the timer
        sei                    ; allow interrupts
idle:
        sleep                  ; nap until the timer rings
        jmp idle
tick:
        out ADCSTART, r0       ; measure the light
        in r1, ADCH            ; r1 = light code, 0 (dark) .. 255 (bright)
        cpi r1, 200
        brsh daylight          ; bright enough: LED off
        ldi r2, 255
        sub r2, r1             ; darker -> brighter LED: duty = 255 - light
        jmp apply
daylight:
        ldi r2, 0
apply:
        out PWMDUTY, r2
        inc r3                 ; count ticks
        cpi r3, 25
        brne done              ; every 25 ticks (~0.25 s) ...
        ldi r3, 0
        out UDR, r1            ; ... report light and duty
        out UDR, r2
done:
        reti
```

(Comments after `;` are for you; the copy inside `main.py` has none.)

Two design choices are worth noticing:

1. **The main loop does nothing but sleep.** All the work happens in the ISR. This is the pattern of most battery-powered firmware: wake, do a little, sleep.
2. **The ISR uses r1, r2, r3, and the main loop only r0.** A real ISR must save (push) and restore (pop) any register the interrupted code might be using; we avoid the problem by not sharing registers. Lesson 05's warning about shared variables is the same issue.

### Timing

At 1 MHz, the timer ticks every `64 x (155 + 1) = 9984` cycles, which is `9.984 ms`, or `100.16 Hz`. The PWM counts 256 steps with a prescaler of 8: period `8 x 256 / 1 000 000 = 2.048 ms`, frequency `488.3 Hz`.

How long does one ISR take? Count the cycles of the dark path without the UART report:

```
interrupt entry          4
out ADCSTART             1
in r1, ADCH              1
cpi                      1
brsh (not taken)         1
ldi r2, 255              1
sub r2, r1               1
jmp apply                2
out PWMDUTY              1
inc r3                   1
cpi r3, 25               1
brne done (taken)        2
reti                     4
total                   21 cycles
```

21 cycles out of every 9984: the core is awake about `21 / 9984 = 0.21%` of the time (a little more on the ticks that send UART bytes). In a real chip, sleep current is a tiny fraction of run current, so the battery life is set almost entirely by the LED and by that 0.2%.

### Tracing a decision with flags

At 100 lux the sensor gives 2.317 V. The ADC code is `floor(2.317 / 3.3 x 256) = floor(179.7) = 179`.

- `cpi r1, 200` computes `179 - 200 = -21`. Not zero, so the zero flag is 0. Negative, so a borrow is needed: carry = 1.
- `brsh daylight` branches if carry is 0. Carry is 1, so it does not branch.
- `ldi r2, 255` then `sub r2, r1`: `255 - 179 = 76`. Duty code 76.

At 1000 lux the code is 236. `236 - 200 = 36`, carry 0, `brsh` branches, duty 0. The LED stays off in daylight.

### What comes out

Duty code 76 means duty `76 / 256 = 0.297`. The RC filter settles at `0.297 x 3.3 = 0.980 V`, and the LED's average current is `0.297 x I_on`. With 3.3 V, 40 ohm of driver and 150 ohm, a red LED carries about 7.7 mA when on, so on average about 2.3 mA.

### Event-driven simulation

One simulated second is a million cycles. Stepping through each one in Python would be slow and pointless, because 99.8% of them the core is asleep. So the simulator's loop is:

```
while time < stop:
    update the timer: if time has passed the next match, mark "timer" as pending
    if interrupts are enabled and something is pending: enter the ISR
    elif the core is asleep: jump time forward to the next timer match
    else: execute one instruction and add its cycles to time
```

That "jump time forward" is what makes it event-driven: the simulation moves from one event to the next. Hardware simulators and the logic simulator of `sim.logic` use the same idea.

## Build It

### Step 1: The assembler with vectors

`assemble(source)` is Lesson 01's assembler plus the `.vector` directive. It returns the program and a dictionary `{"timer": 9}`: the timer's vector points to instruction 9, where `tick:` is.

### Step 2: The world outside

```python
class LightWorld:
    def sensor_volts(self, seconds):
        lux = self.lux_at(seconds)
        if lux not in self.cache:
            circuit = Circuit()
            circuit.voltage_source("VDD", "vdd", "0", VDD)
            circuit.resistor("RLDR", "vdd", "sense", ldr_ohms(lux))
            circuit.resistor("RFIX", "sense", "0", FIXED_OHMS)
            self.cache[lux] = circuit.dc().v("sense")
        return self.cache[lux]
```

The world plays four scenes of 0.25 s each: 1000, 100, 10 and 1 lux (dusk falling quickly). Each light level's divider is solved once by `sim` and remembered.

### Step 3: The core and its peripherals

`VirtualMcu` holds sixteen 8-bit registers, the zero and carry flags, a stack, the PC and the time in cycles. `io_write` is the address decoder: writing TCOMP sets the timer's compare value, writing ADCSTART runs a conversion on the world's voltage at the current time, writing PWMDUTY logs a new duty (remembering whether DDRB bit 1 was set), writing UDR logs a byte.

`execute` is fetch-decode-execute for one instruction. The interesting new piece is the compare:

```python
        elif mnemonic == "cpi":
            difference = self.registers[self.reg(operands[0])] - self.value(operands[1])
            self.zero = difference == 0
            self.carry = difference < 0
```

### Step 4: Interrupts and sleep

```python
    def serve_interrupt(self, name):
        self.pending.discard(name)
        self.stack.append(self.pc)
        self.interrupts_enabled = False
        self.sleeping = False
        self.pc = self.vectors[name]
        self.now += INTERRUPT_ENTRY_CYCLES
```

and `run(seconds)` is the event loop above.

### Step 5: Back to the circuits

For each scene, the script takes the last duty the firmware wrote and simulates the PWM into the RC filter with `sim`'s transient analysis, then multiplies the LED's on-current (from a `sim` DC solve) by the duty.

Run it:

```
uv run python phases/17-microcontrollers/07-a-virtual-microcontroller/code/main.py
```

You will see: 25 instructions with the timer vector at 9; 100 interrupts in one second with the core awake about 0.24% of the time; a UART log with one line per scene; and a table showing, for each light level, the LDR resistance, the sensor voltage, the ADC code, the duty, the simulated RC output next to `duty x 3.3 V`, and the average LED current. Night (1 lux) gives duty 234 and about 7 mA average; daylight gives 0. A plot of light code and duty over time is saved as `night_light.png`.

## Use It

- **Real emulators:** `simavr` emulates AVR chips well enough to run Arduino firmware; QEMU emulates ARM Cortex-M boards; Renode and Wokwi simulate whole boards with sensors and displays in the browser. Teams use them to test firmware before hardware exists, exactly like this lesson.
- **Night lights, street lights and phone screens** all do this loop: read ambient light, map it to a brightness, apply with PWM. Phones use a dedicated ambient light sensor over I2C (Lesson 06) instead of an LDR.
- **Sleep is everything for batteries.** A typical small microcontroller might draw a few milliamps while running and a microamp or less in deep sleep. Waking 100 times per second for 21 cycles each is how a coin cell lasts years.
- **Hardware in the loop (HIL):** in industry, firmware running on a real chip is connected to a simulated plant (a motor, a car) so that dangerous situations can be tested safely. Our `LightWorld` is a tiny version of that.
- **Mapping is a design choice.** `duty = 255 - light` is linear; real products use a curve (often a lookup table in flash) because the eye's response is closer to logarithmic.

## Try It in the Lab

The lab looks at the analog end of this system. The night light's 488 Hz PWM at 50% duty (3.3 V high) feeds a 10 kohm resistor, and you choose the capacitor. The smoothed voltage must sit between 1.5 V and 1.8 V at 100 ms and its ripple (over the second half of the run) must stay under 0.25 V. Use `ripple = VDD x D x (1 - D) x T / RC` and the time constant to predict which capacitor is too small, which is too slow, and which is right.

## Common Mistakes

- **Forgetting `sei`.** The timer runs and sets its flag, but the core never takes the interrupt and sleeps forever. In our simulator, delete the `sei` line: the script reports that no ADC reading ever happened.
- **Forgetting DDR.** Delete the two lines that set DDRB: the firmware still computes duties, but the table shows `nan` because the PWM never reaches a pin that is an input.
- **Comparing signed and unsigned.** `cpi` plus `brsh`/`brlo` compares unsigned 0-255 values. For signed numbers (-128..127) chips have separate branches (`brge`, `brlt` on AVR).
- **Clobbering registers in an ISR.** If the main loop used r1 and the ISR overwrote it, the main loop would see values change "by magic". Save and restore, or keep registers separate.
- **Doing slow things in the ISR.** Sending many UART bytes at 9600 baud takes about 1 ms each; a real ISR would put them in a buffer for the UART interrupt to send.
- **Trusting the emulator blindly.** Our ADC converts instantly and our UART has no transmit time; a real chip has conversion times (about 100 us on the ATmega328P) and busy flags. Emulators are only as good as their models.

## Exercises

1. Which `TCOMP` would give a 50 Hz tick? (1 000 000 / (64 x 50) - 1 = 311.5, which does not fit in an 8-bit register. With our fixed prescaler of 64 the slowest tick is TCOMP = 255: 64 x 256 = 16 384 cycles, about 61 Hz. Real chips solve this with selectable prescalers or 16-bit timers, as in Lesson 05.)
2. Count the cycles of the daylight path of the ISR (with `brsh` taken), without the UART report. (4 + 1 + 1 + 1 + 2 + 1 + 1 + 1 + 1 + 2 + 4 = 19.)
3. Change the threshold from 200 to 150. Which scenes change behaviour? Predict, then run.
4. Add a fifth scene at 300 lux. What LDR resistance, sensor voltage, ADC code and duty do you expect? (R = 10 k x 30^(-0.7) = 925 ohm; V = 3.3 x 4.7 / 5.625 = 2.757 V; code 213; daylight, duty 0.)
5. Harder: add an instruction `lsr r2` (shift right by one bit) and use it to make the LED half as bright at every light level. Then make the duty follow a gentler curve by using a small lookup table: add an `ld` from RAM indexed by the top 3 bits of the light code.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Emulator | "A fake chip" | A program that executes the real firmware and models the peripherals |
| Reset vector | "Where the program starts" | The fixed address the PC is loaded with at power-up |
| Interrupt vector | "The ISR address" | The table entry the core jumps to for one interrupt source |
| Sleep | "Off" | Core clock stopped; peripherals and RAM keep running until a wake-up interrupt |
| Carry flag | "Overflow" | Set when an unsigned subtraction borrows (or an addition overflows 8 bits) |
| Event-driven simulation | "Fast simulation" | Advancing time directly to the next event instead of tick by tick |
| LDR | "Light sensor" | A resistor whose value falls roughly as a power of the light level |

## Further Reading

- [simavr, an AVR simulator (GitHub)](https://github.com/buserror/simavr) — a real emulator that runs unmodified AVR firmware with peripherals
- [Wokwi](https://wokwi.com/) — an online simulator of Arduino, ESP32 and Raspberry Pi Pico boards with sensors and LEDs
- [Microchip, "AVR Instruction Set Manual"](https://ww1.microchip.com/downloads/en/DeviceDoc/AVR-InstructionSet-Manual-DS40002198.pdf) — the real `cpi`, `brsh`, `sleep` and `reti`, with their flag rules and cycle counts
- Elecia White, *Making Embedded Systems*, 2nd ed. (O'Reilly) — designing firmware around interrupts, sleep and peripherals
