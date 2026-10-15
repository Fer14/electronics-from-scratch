# What a Microcontroller Is

> A microcontroller is a whole small computer on one chip, built not to run apps but to wiggle pins: it reads the world through some legs and pushes on it through others.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 16 (A Computer from Gates), especially Lesson 06 (Instructions and Assembly) and Lesson 07 (Running a Program); Phase 11 (Semiconductors and Diodes), Lesson 07 (LEDs)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Microcontroller (MCU) | A single chip that contains a processor, memory and input/output circuits, so it can run a program and control hardware on its own. | A tiny office with a clerk, a filing cabinet and a set of doors to the street, all in one box. |
| Processor core (CPU) | The part that fetches instructions and does arithmetic and decisions. You built one from gates in Phase 16. | The clerk who reads the instruction sheet and does what it says. |
| Flash memory | Memory that keeps its contents with the power off. The program lives here. | A printed instruction manual on the shelf. |
| RAM (SRAM) | Fast memory for numbers that change while the program runs. Forgets everything when power goes off. | The clerk's whiteboard. |
| Register | A tiny, very fast storage box inside the core, usually 8, 16 or 32 bits wide. | The numbers the clerk is holding in their head right now. |
| Peripheral | A hardware block on the chip that does one job with the outside world: pins, timers, analog-to-digital converter, serial ports. | The office's specialised machines: the franking machine, the clock, the phone. |
| Pin | A metal leg of the chip that connects to the circuit board. | A door from the office to the street. |
| Memory-mapped I/O | Controlling a peripheral by writing numbers into special addresses, as if they were memory. | Pulling a numbered lever on a wall of levers: lever 5 opens door B. |
| Clock | A signal that ticks at a steady rate; each tick moves the core one step. Measured in hertz (Hz), ticks per second. | A metronome the clerk works to. |
| Clock cycle | The time between two ticks: 1 / (clock frequency). | One beat of the metronome. |
| Firmware | The program stored in a microcontroller. "Firm" because it is not changed often. | The office's standing orders. |
| Embedded system | A device with a hidden computer inside that does one job (a microwave, a thermostat). | A kitchen timer: you never think of it as a computer. |
| Fetch-decode-execute | The loop every processor runs: read the next instruction, work out what it means, do it. | Read the next line of the recipe, understand it, cook it. |
| Program counter (PC) | A register holding the address of the next instruction. | A finger on the current line of the recipe. |
| Assembly language | A human-readable version of machine instructions, one line per instruction. | The recipe written in short commands: "add 2 eggs", "stir". |

## Learning Objectives

- Describe the three ingredients of a microcontroller (core, memory, peripherals) and how they differ from a desktop computer
- Read a short assembly program and predict, step by step, what each register holds
- Convert clock cycles into time for a given clock frequency (for example 37 cycles at 16 MHz = 2.3125 microseconds)
- Explain memory-mapped I/O: why writing the number 1 into an address can make a pin go to 3.3 V
- Connect the digital world (a bit in a register) to the analog world (an LED current computed by our simulator)

## The Problem

Look around a kitchen. The microwave counts down and beeps. The washing machine opens a water valve, waits, spins the drum. The thermostat on the wall reads the temperature and switches the boiler. Each of these devices needs *decisions*: "if the door is open, stop the magnetron", "if the water level is reached, close the valve". In Phase 16 you built a computer from gates that can make such decisions. But a desktop computer is huge, power-hungry and expensive, and it has no direct way to switch a valve.

What the microwave needs is a computer that costs less than a coffee, runs from a few milliamps, starts in a millisecond and has legs it can connect directly to buttons, motors and lights. That is a microcontroller. There are more of them in the world than people: a modern car carries dozens, a TV remote has one, a USB cable sometimes has one inside the plug.

The second problem is understanding the *border* between software and hardware. Programmers write `led_on()`. Electronics engineers see a pin at 3.3 V pushing a few milliamps through a resistor and an LED. This lesson builds both views at once: a tiny processor in Python whose "write a 1 to PORTB" instruction is turned into a voltage on a pin, and our circuit simulator (`sim`) tells us how much current then flows through the LED.

## The Physics

There is no new physics in a microcontroller: everything inside is transistors switching (Phase 12), arranged into gates (Phase 14), flip-flops (Phase 15) and a datapath (Phase 16). What is worth understanding physically is the *edge* of the chip.

Inside the chip, a "1" is a node charged to the supply voltage (say 3.3 V) and a "0" is a node at 0 V. These nodes are tiny: their capacitance is a few femtofarads (1 fF = 0.000 000 000 000 001 F), so they can switch in well under a nanosecond. A pin is different. It has to drive a wire on a circuit board, an LED, maybe a long cable, which can be thousands of times more capacitance and need milliamps of current. So every output pin has a pair of much bigger transistors behind it, an "output driver": one connects the pin to the supply (to make a 1), the other connects it to ground (to make a 0). You met this pair as the CMOS inverter in Phase 14, Lesson 05.

```
          +3.3 V supply
             |
           |-'   P-channel MOSFET: ON when the register bit is 1
  bit ---o-|
         | |-.
         |   +-------- PIN ----[ 330 ohm ]----|>|---- gnd
         | |-'                                  LED
         '-|     N-channel MOSFET: ON when the register bit is 0
           |-.
             |
            gnd
```

So the chain from software to light is:

1. An instruction writes a number into a special register (PORTB).
2. One bit of that register is a flip-flop whose output drives the gates of the output transistors.
3. The upper transistor turns on, the pin is connected to 3.3 V.
4. Current flows out of the pin, through the resistor and the LED, to ground. The LED lights.

Steps 1-2 are digital and take nanoseconds. Steps 3-4 are analog: Ohm's law, the LED's forward voltage, the driver's resistance. The next lesson (GPIO) looks at step 3 in detail. Here we keep it simple: the pin is either an ideal 3.3 V or an ideal 0 V.

## The Concept

### A computer, shrunk and specialised

In Phase 16 you built a computer from separate blocks: an ALU, registers, memory, a control unit. A desktop computer keeps those blocks on separate chips: the processor, several memory sticks, a storage drive, a graphics card. A microcontroller puts a *small* version of all of them on one piece of silicon, plus the peripherals:

```
 +-------------------------------- one chip ---------------------------------+
 |                                                                            |
 |   +-----------+     +--------------+     +-------------+                   |
 |   |   CORE    |<--->|  FLASH       |     |  RAM        |                   |
 |   | registers |     |  (program,   |     |  (variables,|                   |
 |   | ALU, PC   |<--->|   keeps it   |     |   forgets   |                   |
 |   +-----------+     |   unpowered) |     |   it)       |                   |
 |        ^            +--------------+     +-------------+                   |
 |        |  address + data bus                    ^                          |
 |        +----------------------------------------+                          |
 |        |              |               |                 |                 |
 |   +---------+    +---------+    +-----------+     +-----------+            |
 |   |  GPIO   |    |  TIMER  |    |   ADC     |     |  UART /   |            |
 |   | (pins)  |    |  / PWM  |    | (analog   |     |  I2C/SPI  |            |
 |   +---------+    +---------+    |  in)      |     +-----------+            |
 |       |||             |          +-----------+          ||                 |
 +-------|||-------------|---------------|----------------||-----------------+
        pins           pin             pin              pins
```

Here are three real chips, with numbers from their datasheets, so you have a feel for the sizes:

| Chip | Core | Clock | Flash | RAM | Typical use |
|------|------|-------|-------|-----|-------------|
| ATmega328P (the Arduino Uno chip) | 8-bit AVR | 16-20 MHz | 32 KB | 2 KB | hobby boards, simple appliances |
| STM32F103 ("blue pill") | 32-bit ARM Cortex-M3 | 72 MHz | 64-128 KB | 20 KB | motor control, instruments |
| RP2040 (Raspberry Pi Pico) | two 32-bit ARM Cortex-M0+ | 133 MHz | external | 264 KB | education, USB gadgets |

Compare with a laptop: several gigahertz (thousands of megahertz) and several gigabytes of RAM (millions of kilobytes). A microcontroller is a thousand to a million times smaller, and that is exactly the point: it is cheap, it draws milliwatts, and it has no operating system to wait for. It switches on and runs your program immediately.

What the "tiny office" picture gets wrong: a real office can have many clerks working at once and rearranging the furniture. A simple microcontroller has one core doing one instruction at a time, and its "furniture" (which peripheral is on which address) is fixed when the chip is made.

### The clock, cycles and time

The core advances one step per tick of its clock. If the clock runs at 16 MHz ("megahertz", millions of ticks per second), one tick lasts:

```
cycle time = 1 / clock frequency = 1 / 16 000 000 s = 0.000 000 0625 s = 62.5 ns
```

Read it as: "the time of one cycle is one divided by the number of cycles per second". `ns` is a nanosecond, a billionth of a second.

Most simple instructions take 1 cycle; some take 2 (reading memory, jumping). So if a program needs 37 cycles, at 16 MHz it takes:

```
time = cycles / frequency = 37 / 16 000 000 s = 2.3125 microseconds  (2312.5 ns)
```

This is the most important habit of embedded work: **always turn cycles into seconds**. A loop that "only" takes 1000 cycles still takes 62.5 microseconds, and if you need to react to something every 50 microseconds, you are already too slow.

### Fetch, decode, execute

You saw this in Phase 16, Lesson 07. The core runs the same three-step loop forever:

1. **Fetch:** read the instruction at the address in the program counter (PC).
2. **Decode:** work out which operation it is and which registers it uses.
3. **Execute:** do it, update the registers and flags, and move the PC to the next instruction (or somewhere else, for a jump).

A **flag** is a one-bit register that remembers something about the last result. We use one: the **zero flag**, which is set to 1 when an arithmetic result is zero. Conditional jumps look at it: `brne` means "branch if not equal (to zero)", that is, jump if the zero flag is 0.

### Our tiny program format

We use a tiny assembly language. One instruction per line, labels end in a colon, operands are separated by commas:

| Instruction | Meaning | Cycles |
|-------------|---------|--------|
| `ldi r0, 5` | load the number 5 into register r0 | 1 |
| `dec r0` | r0 = r0 - 1; set the zero flag if the result is 0 | 1 |
| `inc r0`, `add r0, r1`, `sub r0, r1` | arithmetic, wraps around at 256 (8 bits) | 1 |
| `out PORTB, r1` | copy r1 into the I/O register PORTB | 1 |
| `in r2, PORTB` | copy an I/O register into r2 | 1 |
| `st 0x10, r3` | store r3 into RAM at address 0x10 (16) | 2 |
| `ld r4, 0x10` | load RAM address 0x10 into r4 | 2 |
| `jmp label` | jump to label | 2 |
| `brne label` | jump to label if the zero flag is 0 | 1, or 2 if it jumps |
| `halt` | stop | 1 |

`0x10` is hexadecimal (base 16) for 16, as in Phase 14, Lesson 02. Registers are 8 bits wide, so they hold 0 to 255. Adding 1 to 255 gives 0 again (it "wraps around"), exactly like the 8-bit adder of Phase 14.

Here is the program we run:

```
        ldi r0, 5          ; r0 counts down from 5
        ldi r1, 1          ; r1 holds the bit pattern "LED on"
countdown:
        out PORTB, r1      ; pin goes to 3.3 V
        ldi r2, 0
        out PORTB, r2      ; pin goes to 0 V
        dec r0
        brne countdown     ; repeat until r0 reaches 0
        ldi r3, 42
        st 0x10, r3        ; save 42 in RAM
        ld r4, 0x10        ; and read it back
        halt
```

(Text after `;` is a comment for you; our simple assembler in the code does not need them, so the program inside `main.py` has none.)

### Tracing it by hand

Let us follow the first loop, counting cycles. Each row is after the instruction finishes.

```
cycle  instruction      r0  r1  r2   what happened
  1    ldi r0, 5         5   0   0   r0 = 5
  2    ldi r1, 1         5   1   0   r1 = 1
  3    out PORTB, r1     5   1   0   PORTB = 00000001, pin high
  4    ldi r2, 0         5   1   0
  5    out PORTB, r2     5   1   0   PORTB = 00000000, pin low
  6    dec r0            4   1   0   4 is not zero: zero flag = 0
  8    brne countdown    4   1   0   jump taken: 2 cycles
```

The body of the loop is `out, ldi, out, dec, brne` = 1 + 1 + 1 + 1 + 2 = 6 cycles. It runs 5 times, but the last `brne` does not jump (r0 reached 0) and costs only 1 cycle. Total:

```
start:        2 cycles (two ldi)
loop:         5 x 6 - 1 = 29 cycles
after loop:   ldi (1) + st (2) + ld (2) + halt (1) = 6 cycles
total:        2 + 29 + 6 = 37 cycles  ->  37 x 62.5 ns = 2312.5 ns
```

The pin is high from the first `out` to the second, which is 2 cycles: 125 ns. An LED does light up in 125 ns, but your eye averages over about a hundredth of a second, so it would see nothing. That is why real blink programs waste time on purpose in delay loops or, better, use a timer (Lesson 05).

### Memory-mapped I/O: how a number becomes a voltage

Notice that `out PORTB, r1` looks just like a store to memory. That is the key trick of microcontrollers: each peripheral has a few registers that live at fixed addresses. On the ATmega328P, for instance, PORTB lives at I/O address 0x05. Writing to that address does not store into RAM; the address decoder (Phase 16, Lesson 03) routes the write to the flip-flops of port B, whose outputs drive the pins. The datasheet's "register summary" table is a map of these addresses, and reading it is half of embedded programming.

Each bit of PORTB is one pin. `00000001` means "pin PB0 high, all others low". Writing `00000101` would set PB0 and PB2 high at the same moment.

### From the bit to the LED current

When PB0 is high, the pin is (ideally) a 3.3 V source. With a 330 ohm resistor and a red LED, Kirchhoff's voltage law (Phase 04) says the 3.3 V is shared between the resistor and the LED. A red LED keeps roughly 1.8-2 V across itself (Phase 11, Lesson 07), so the resistor gets about 1.3-1.5 V and the current is about:

```
I = (3.3 V - 1.9 V) / 330 ohm = 1.4 / 330 A = 0.0042 A = 4.2 mA
```

When PB0 is low, the pin is at 0 V and no current flows. Our simulator solves the LED's exponential equation (Phase 11, Lesson 05) for the exact number.

## Build It

### Step 1: An assembler

The assembler turns text into a list of `(mnemonic, operands)` and replaces label names by addresses. A **mnemonic** is the short name of an instruction, like `ldi`.

```python
def assemble(source):
    labels = {}
    instructions = []
    for raw_line in source.strip().splitlines():
        text = raw_line.strip()
        if not text:
            continue
        if text.endswith(":"):
            labels[text[:-1]] = len(instructions)
            continue
        mnemonic, _, rest = text.partition(" ")
        operands = [part.strip() for part in rest.split(",") if part.strip()]
        instructions.append((mnemonic.lower(), operands))
    return [(mnemonic, [labels.get(operand, operand) for operand in operands])
            for mnemonic, operands in instructions]
```

A label line like `countdown:` produces no instruction; it only remembers "the next instruction's address is 2".

### Step 2: The core's state

Everything the core knows is a handful of numbers: eight registers, a RAM array, the I/O registers, the program counter, the zero flag and a cycle counter.

```python
class TinyCore:
    def __init__(self, program, ram_size=64):
        self.program = program
        self.registers = [0] * 8
        self.ram = [0] * ram_size
        self.io = {address: 0 for address in IO_ADDRESSES.values()}
        self.pc = 0
        self.zero_flag = False
        self.cycles = 0
        self.halted = False
        self.io_writes = []
```

`set_register` keeps values inside 8 bits with `& 0xFF` (the bitwise AND with 255) and updates the zero flag.

### Step 3: One step of fetch-decode-execute

`step()` fetches `self.program[self.pc]`, decodes it with a chain of `if mnemonic == ...`, executes it, adds the cycle cost and moves the PC. A taken branch costs one extra cycle, because the real core has to throw away the instruction it already started fetching.

```python
        elif mnemonic == "brne":
            if not self.zero_flag:
                next_pc = operands[0]
                cost += 1
```

`out` also records the moment and value of every write to an I/O register, so we can see the pin from outside.

### Step 4: The pin drives a circuit

For each recorded write we ask the simulator what the LED does:

```python
def led_current_for_pin(pin_volts):
    circuit = Circuit()
    circuit.voltage_source("PIN", "pin", "0", pin_volts)
    circuit.resistor("R1", "pin", "a", LED_RESISTOR_OHMS)
    circuit.led("D1", "a", "0", color="red")
    return circuit.dc().i("D1")
```

Run it:

```
uv run python phases/17-microcontrollers/01-what-a-microcontroller-is/code/main.py
```

You get the assembled program, a cycle-by-cycle trace that matches the hand trace above (37 cycles, 2.3125 us), and a list of PORTB writes with the pin voltage and the LED current computed by `sim`: a few milliamps when the bit is 1, zero when it is 0.

## Use It

- **Datasheets are the manual.** Every microcontroller comes with a datasheet of hundreds of pages. The parts you will use most: the pinout (which leg is which), the "electrical characteristics" table (voltages and currents a pin can handle), and the register descriptions of each peripheral. The ATmega328P datasheet from Microchip and the RP2040 datasheet from Raspberry Pi are both free and very readable.
- **Arduino `digitalWrite(13, HIGH)`** is a C function that, after some bookkeeping, does exactly our `out PORTB, r1`: it sets one bit of the port register that drives pin 13 (which is PB5 on the Uno).
- **MicroPython and CircuitPython** let you write Python on boards like the Raspberry Pi Pico. `Pin(25, Pin.OUT).value(1)` ends up writing a 1 into a GPIO output register, just with more layers of software in between.
- **Choosing a chip.** Engineers pick a microcontroller by asking: how many pins and which peripherals do I need, how fast must it react, how much power can it draw, and what does it cost in quantity? A 32-bit ARM Cortex-M0+ chip with 32 KB of flash costs well under one dollar in volume.
- **Cycle counting is real.** In motor control and in generating precise signals, engineers still count cycles exactly like our trace does, or read them from a timer.

## Common Mistakes

- **Thinking a microcontroller is "a small PC".** It has no operating system, no screen, often no file system. Your program is the only thing running, and if it gets stuck in a loop, nothing else happens.
- **Forgetting that cycles are time.** "It's just a loop" can mean milliseconds. Always multiply cycles by the cycle time.
- **Confusing RAM and flash.** Variables live in RAM and are lost at power-off. The program and constants live in flash. Writing to flash is slow and wears it out (typically 10 000 erase cycles).
- **Thinking writing to PORTB is "just a variable".** It is a physical action: a pin changes voltage, current flows, something heats up. A wrong value can short a pin to another pin.
- **Ignoring wrap-around.** An 8-bit register holding 255 becomes 0 when you add 1. Counters that overflow silently are a classic source of bugs (and Lesson 05 uses this deliberately for timers).
- **Expecting to see a 125 ns flash.** The eye needs tens of milliseconds. A blink program must wait on purpose.

## Exercises

1. A microcontroller runs at 8 MHz. How long is one cycle? How long does a 1000-cycle loop take? (Answer: 125 ns and 125 us.)
2. Change the program so r0 starts at 10. How many cycles does it take now? Check your count by editing `PROGRAM` in `main.py`. (Hint: 2 + 10 x 6 - 1 + 6.)
3. What value ends up in an 8-bit register after `ldi r0, 250` followed by `inc r0` six times? Is the zero flag set after the sixth `inc`? (Answer: 256 wraps to 0, so yes.)
4. Write a program that turns on pins PB0 and PB1 together with one `out`. Which number must the register hold? (Answer: binary 00000011 = 3.)
5. Harder: you want the LED to be on for 10 ms in each flash, at 16 MHz. How many cycles is that? If a delay loop body takes 4 cycles, how many times must it run? Why can this not fit in one 8-bit counter? (Answer: 160 000 cycles, 40 000 loops, more than 255, so you need nested loops or a 16-bit counter.)

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Microcontroller | "An Arduino" | A chip with core, flash, RAM and peripherals; Arduino is a board and software built around one |
| Clock speed | "How fast it is" | Cycles per second; actual speed also depends on cycles per instruction |
| Register | "A variable" | A fixed hardware storage box inside the core or a peripheral |
| I/O register | "A setting" | A register at a fixed address whose bits are wired to hardware, such as pins |
| Firmware | "The code" | The program stored in the chip's flash, run directly with no operating system |
| Flash | "Storage" | Non-volatile memory that keeps the program without power |
| Program counter | "Where the program is" | The register holding the address of the next instruction |

## Further Reading

- [ATmega328P datasheet (Microchip)](https://www.microchip.com/en-us/product/ATmega328P) — the chip of the Arduino Uno; see the "AVR CPU Core" and "I/O Ports" chapters and the instruction set summary
- [RP2040 datasheet (Raspberry Pi)](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf) — a modern microcontroller explained very clearly, including its memory map
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 15 (Microcontrollers) — how real designs use them
- [Ben Eater, "Build an 8-bit computer" and "6502 computer" video series](https://eater.net/) — the same fetch-decode-execute ideas built on breadboards
