# Timers and Interrupts

> A timer is a counter that keeps time while the program does something else; an interrupt is the timer tapping the processor on the shoulder at exactly the right moment.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 17 (Microcontrollers), Lessons 01-03; Phase 15 (Sequential Logic), Lesson 05 (Counters); Phase 07 (Capacitors), Lesson 03 (Charging and Discharging)
**Time:** ~85 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Timer | A hardware counter that counts clock ticks on its own, without the program's help. | A kitchen timer that keeps counting while you cook. |
| Prescaler | A divider in front of the timer that passes on only every N-th clock tick. | A gear that turns the fast motor shaft into a slow hand on a clock. |
| Compare match | The moment the timer's count equals a value you chose. | The kitchen timer reaching zero and ringing. |
| CTC mode | "Clear timer on compare": the timer goes back to 0 at each match, so matches repeat at a fixed rate. | A metronome: tick, tick, tick, evenly. |
| Flag | A one-bit register the hardware sets to say "this event happened". | A red flag on a mailbox that pops up when post arrives. |
| Polling | The program checks the flag itself, whenever it gets round to it. | Walking to the mailbox every so often to see if the flag is up. |
| Interrupt | The hardware forces the processor to stop what it is doing and run a special function at once. | The doorbell: you stop and answer immediately. |
| ISR (interrupt service routine) | The function that runs when an interrupt happens. Also called an interrupt handler. | What you do when the doorbell rings: go to the door, sign for the parcel, come back. |
| Vector table | A list, at a fixed place in memory, of which ISR belongs to which interrupt. | The list by the door: "doorbell = parcel, phone = take a message". |
| Latency | The delay between the event and the moment it is handled. | The time from the doorbell ringing to you opening the door. |
| Jitter | How much the latency varies from one event to the next. | Sometimes you are by the door, sometimes in the shower. |
| Contact bounce | A mechanical switch's metal contacts hitting and rebounding several times when pressed. | A ball dropped on the floor bouncing a few times before it rests. |
| Debouncing | Ignoring those rebounds, in hardware or software, so one press counts once. | Waiting until the ball has stopped bouncing before you say where it landed. |

## Learning Objectives

- Compute the prescaler and compare value that make a timer fire at a given rate, and check whether they fit in the timer's register
- Explain the difference between polling and interrupts, and measure the latency and the missed events of each in a cycle-level simulation
- Describe what the processor does when an interrupt arrives (finish the instruction, save state, jump through the vector table, return)
- Debounce a button in software with a 1 ms timer interrupt
- Debounce a button in hardware with an RC filter, and compute with `t = RC ln(VDD / (VDD - VIH))` when the input crosses its threshold, checked with our simulator

## The Problem

In Lesson 01 the LED flashed for 125 ns because the program had no idea of time. The naive fix is a delay loop: "count to a million, then toggle the LED". But while the processor is counting it cannot do anything else. Worse, if you later add code (read a sensor, update a display), every delay changes, because the processor's time is shared.

Now imagine a device that must do three things at once: blink an LED every 500 ms, read a sensor every 10 ms, and react within 50 microseconds when a motor's position sensor fires. No single loop of code can keep all of those promises. What makes it possible is hardware that keeps time on its own (timers) and a way for that hardware to grab the processor's attention at exactly the right moment (interrupts).

The same two tools solve the most common beginner bug in embedded systems: a single button press that the program counts as five, because the button's contacts bounce.

## The Physics

### Counting is keeping time

A crystal oscillator on the board vibrates at a very stable frequency (a 16 MHz crystal is typically accurate to about 0.003%, that is 30 parts per million). The timer is the counter of Phase 15, Lesson 05, clocked by it. Since every tick has the same length, *the count is a measure of time*: 16 000 counts at 16 MHz is exactly 1 ms. The timer runs in its own flip-flops, so it does not care what the program is doing.

### The processor can be interrupted between instructions

The core of Lesson 01 runs fetch-decode-execute forever. An interrupt adds one check to that loop: after each instruction, the control unit looks at a few "interrupt request" lines. If one is active and enabled, instead of fetching the next instruction it:

1. pushes the program counter (and on some chips other registers) onto the stack in RAM, so it can come back;
2. clears the global interrupt enable, so the ISR is not interrupted by the same thing;
3. loads the PC from the vector table entry for that interrupt;
4. runs the ISR, which ends with a special "return from interrupt" instruction (`reti` on AVR) that restores the PC and re-enables interrupts.

On an AVR the entry takes about 4 cycles and `reti` another 4. Our simulation uses those numbers.

### Metal bounces

Inside a push-button, a springy metal strip slams onto a contact. Metal is elastic, so it rebounds, touches again, rebounds less, and settles, usually within 1 to 10 ms. To a microcontroller that samples in microseconds, that looks like a burst of presses and releases.

```
pin voltage
 3.3 V ------+  +-+   +--+ +
             |  | |   |  | |
   0 V       +--+ +---+  +-+----------------------
             ^ press      ^ settled (a few ms later)
```

## The Concept

### Choosing prescaler and compare

In CTC mode the timer counts `0, 1, ..., compare, 0, 1, ...`. That is `compare + 1` counts per match, and each count lasts `prescaler` clock cycles. So matches happen at:

```
f_interrupt = f_clock / (prescaler x (compare + 1))
```

Read it as: "the interrupt rate is the clock rate divided by the prescaler and by the number of counts per cycle". Turned around, for a wanted rate:

```
compare = f_clock / (prescaler x f_interrupt) - 1
```

Example: 1 interrupt per second from 16 MHz.

```
prescaler 1:     compare = 16 000 000 / 1 - 1     = 15 999 999   too big for 16 bits (max 65 535)
prescaler 64:    compare = 16 000 000 / 64 - 1    = 249 999      still too big
prescaler 256:   compare = 16 000 000 / 256 - 1   = 62 499       fits, and is a whole number: exact
prescaler 1024:  compare = 16 000 000 / 1024 - 1  = 15 624       fits, also exact
```

Example: 1000 interrupts per second (a 1 ms "tick").

```
prescaler 64:    compare = 16 000 000 / 64 000 - 1  = 249     exact
prescaler 256:   compare = 16 000 000 / 256 000 - 1 = 61.5    not whole: 61 or 62 gives 1008 or 992 Hz
```

The rule: pick the smallest prescaler whose compare value fits in the register and comes out as a whole number. The smaller the prescaler, the finer the time resolution.

### Polling versus interrupts

Suppose the timer sets its flag every 1 ms, and the main program is busy with chunks of work that take 2.5 ms each (updating a display, say).

**Polling:** the program checks the flag between chunks.

```
time (ms)  0    1    2    3    4    5    6    7
timer:     .    F    F    F    F    F    F    F      (flag set every 1 ms)
program:   [ work 2.5 ms ][check][ work 2.5 ms ][check]
                          ^ sees one flag, but two matches happened
```

The flag is one bit. It cannot count. If two matches happen before the program looks, it sees only one: the other tick is **lost**. And the ones it does see are handled up to 2.5 ms late.

**Interrupts:** the hardware jumps to the ISR within a few cycles of the match, in the middle of the work, and then returns to the work exactly where it left off.

```
program:   [ work ..][ISR][.. work ..][ISR][.. work ..][ISR]...
                     ^ 1 ms          ^ 2 ms           ^ 3 ms
```

No tick is lost, latency is a handful of cycles, and the work still gets done (slightly slower, because the ISR borrows some cycles).

### Keep ISRs short

While an ISR runs, other interrupts usually wait. A long ISR adds latency and jitter to everything else. The standard pattern: the ISR does the minimum (increment a counter, copy a value, set a "work to do" variable) and the main loop does the rest.

### Software debounce with a timer

Read the button once per millisecond, from the 1 ms timer interrupt. Only accept a new state when the reading has been the same for, say, 5 samples in a row:

```
reading:  1 1 1 0 1 0 0 1 0 0 0 0 0 0 0 ...
run:      . . . 1 1 1 2 1 1 2 3 4 5           <- 5 equal samples: accept "pressed"
```

Bounces shorter than 5 ms never produce 5 equal samples, so they are ignored. The cost: the press is reported about 5 ms late, which no human notices.

### Hardware debounce with an RC

Put a capacitor from the input pin to ground, next to the pull-up of Lesson 02:

```
   VDD --[ R pull-up ]--+-- pin
                        |
              button  =====  C
                |       |
               gnd     gnd
```

Pressing the button empties the capacitor quickly (the button is nearly a short). When the button is released, the capacitor charges slowly through `R`. Short bounces cannot recharge it enough to look like a 1. The voltage while charging from 0 V is (Phase 07, Lesson 03):

```
v(t) = VDD x (1 - e^(-t / RC))
```

Read it as: "the voltage rises towards VDD, covering 63% of the remaining gap every time constant RC". The pin reads 1 once `v(t)` passes VIH. Solve for the time:

```
VIH = VDD x (1 - e^(-t / RC))
e^(-t / RC) = 1 - VIH / VDD = (VDD - VIH) / VDD
t = RC x ln(VDD / (VDD - VIH))
```

With VIH = 0.6 x VDD (the ATmega figure from Lesson 02): `ln(1 / 0.4) = ln(2.5) = 0.916`, so `t = 0.916 RC`. With `R = 10 kohm`, `C = 1 uF`: `RC = 10 ms`, `t = 9.16 ms`. Longer than a typical bounce (a few ms), short enough to feel instant.

(Real designs often add a Schmitt-trigger input, Phase 13, Lesson 02, so the slowly rising voltage does not make the input flicker while crossing the undefined band. Many microcontroller inputs have a small amount of this built in.)

### Worked example: why watch crystals are 32 768 Hz

Many boards carry a second, tiny crystal at 32 768 Hz. That number is `2^15`. A 15-bit counter clocked at 32 768 Hz overflows exactly once per second:

```
32 768 counts / 32 768 Hz = 1.000 000 s
```

No compare value, no rounding, and a counter that small uses almost no power. Real-time clock peripherals (and every digital watch) count seconds this way while the main processor sleeps. A typical watch crystal is accurate to about 20 parts per million: `20e-6 x 86 400 s = 1.7 s` of drift per day.

### Worked example: a 1 kHz tick on an 8 MHz chip

At 8 MHz with a 16-bit timer in CTC mode:

```
prescaler 1:  compare = 8 000 000 / 1000 - 1 = 7999      fits, exact
prescaler 8:  compare = 8 000 000 / 8000 - 1 = 999       fits, exact
prescaler 64: compare = 8 000 000 / 64 000 - 1 = 124     fits, exact
```

All three are exact. Prefer the smallest prescaler (1): each timer count is then 125 ns, so if you later read the counter to time an event between ticks, you get the finest resolution.

### Worked example: how much latency can you afford?

A motor encoder produces a pulse every 50 us at full speed. Each pulse fires an interrupt whose ISR takes 40 cycles at 16 MHz (2.5 us), and the core needs 4 cycles (0.25 us) to enter it. If another ISR of 200 cycles (12.5 us) is running when a pulse arrives, the encoder's ISR waits:

```
worst-case latency = 12.5 us (the other ISR) + 0.25 us (entry) = 12.75 us   <  50 us    OK
```

But if the other ISR grew to 1000 cycles (62.5 us), pulses would arrive faster than they could be handled and counts would be lost, exactly like the polling case in the simulation. Keeping every ISR short protects all the others.

## Build It

### Step 1: A timer with a prescaler and a compare match

```python
class CompareTimer:
    def __init__(self, prescaler, compare):
        self.prescaler = prescaler
        self.compare = compare
        self.prescale_count = 0
        self.counter = 0
        self.flag = False
        self.flag_set_at = None
        self.matches = 0

    def clock(self, now):
        self.prescale_count += 1
        if self.prescale_count < self.prescaler:
            return
        self.prescale_count = 0
        if self.counter == self.compare:
            self.counter = 0
            self.matches += 1
            if not self.flag:
                self.flag_set_at = now
            self.flag = True
        else:
            self.counter += 1
```

`clock` is called once per processor cycle. `matches` counts every match (the truth), while `flag` is the single bit the program can see.

### Step 2: A processor that polls or takes interrupts

`Mcu.run` simulates cycle by cycle. In polling mode it burns a whole work chunk, then looks at the flag. In interrupt mode it checks the flag *between every instruction* (as the real control unit does), and if it is set, it spends 4 cycles entering the ISR, handles the tick, and spends 14 more cycles in the ISR body and `reti`. Latency is measured from the moment the flag was set to the moment the tick was handled.

### Step 3: A bouncy button and a debouncer

`bouncy_button` makes a signal that is 1 until 10 ms, then random 0s and 1s for 3 ms, then a steady 0. The random generator has a fixed seed (7), so every run is the same. `software_debounce` samples it once per millisecond and requires 5 equal samples in a row.

### Step 4: The RC debounce in the simulator

```python
def rc_debounce_time(pull_up_ohms, farads):
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", VDD)
    circuit.resistor("RPU", "vdd", "pin", pull_up_ohms)
    circuit.capacitor("C1", "pin", "0", farads, v0=0.0)
    tau = pull_up_ohms * farads
    result = circuit.transient(t_stop=4 * tau, dt=tau / 1000)
    time, volts = np.asarray(result.time), np.asarray(result.v("pin"))
    return float(np.interp(VIH, volts, time)), tau
```

The capacitor starts empty (`v0=0.0`): the button has just been released. `np.interp(VIH, volts, time)` finds the time at which the rising voltage passes VIH.

Run it:

```
uv run python phases/17-microcontrollers/05-timers-and-interrupts/code/main.py
```

You will see:

- the prescaler table: for 1 Hz only 256 and 1024 fit in 16 bits; for 1 kHz, prescaler 256 gives 61.5, which must be rounded and lands at 992 Hz;
- polling counts only 20 of the 50 ticks, with latencies near 2 ms, while interrupts count all 50 with a latency of 5 cycles (5 us at 1 MHz);
- the bouncy button produces 14 raw falling edges but one debounced press, accepted a few ms after the bouncing stops;
- the RC debounce crossing VIH at 0.916 RC: 0.92 ms, 9.16 ms and 91.6 ms for 0.1, 1 and 10 uF.

## Use It

- **Arduino `millis()`** is a timer interrupt: Timer0 overflows about every 1.024 ms and its ISR adds to a counter. `delay()` just waits for that counter. If you disable interrupts for too long, `millis()` loses time, exactly like our polling loop lost ticks.
- **`attachInterrupt()`** on Arduino connects an ISR to a pin-change interrupt, used for rotary encoders, speed sensors and wake-up buttons.
- **Real-time control** (motor drives, power converters in Phase 18) runs its control loop in a timer ISR at a fixed rate, often 10-20 kHz, because the maths of feedback assumes evenly spaced samples.
- **The ARM Cortex-M NVIC** (nested vectored interrupt controller) lets interrupts have priorities, so a high-priority ISR can interrupt a low-priority one. Latency is 12 cycles on a Cortex-M3/M4.
- **Watchdog timers** reset the chip if the program does not "pet" them in time: a safety net against firmware stuck in a loop.
- **Button debouncing** in products is usually done in software with a periodic timer, because it costs no parts. RC plus Schmitt trigger is used where there is no processor, or for reset buttons.

## Try It in the Lab

The lab is a hardware debounce. A 10 kohm pull-up charges a capacitor that you choose; the button has just been released and the capacitor starts empty. The pin must not reach the logic-1 threshold (1.98 V) before 5 ms, because the contacts may still be bouncing, but it must get there within 50 ms so the button feels responsive. Use `t = 0.916 RC` for each capacitor before you try it.

## Common Mistakes

- **Long work inside an ISR.** Printing, waiting, or reading a slow sensor inside an ISR blocks every other interrupt. Set a variable and leave.
- **Sharing variables without care.** A multi-byte variable changed in an ISR can be read half-updated by the main loop. On 8-bit chips, briefly disable interrupts while reading it, and mark it `volatile` in C so the compiler re-reads it.
- **Forgetting to clear the flag.** On many chips the flag clears automatically when the ISR runs; on others the ISR must clear it, or it runs again immediately, forever.
- **Rounding compare values silently.** 61.5 becomes 61 or 62, and the clock is 0.8% off. Over a day that is 11 minutes. Prefer settings that divide exactly.
- **Off-by-one in the compare value.** CTC counts `compare + 1` states. Compare 999 gives 1000 counts.
- **Assuming one edge per press.** Every mechanical switch bounces. Debounce in hardware or software, always.
- **Huge debounce capacitors.** 10 uF with 10 kohm takes almost 0.1 s to read a release, and the instant discharge through the button contacts can wear them.

## Exercises

1. An 8 MHz chip needs a 100 Hz interrupt with a 16-bit timer. Which prescalers (1, 8, 64, 256, 1024) give an exact whole compare value that fits? (8: 9999; 64: 1249; 256: 311.5 no; 1024: 77.1 no; 1: 79 999 does not fit.)
2. Your ISR takes 40 cycles and fires 20 000 times per second on a 16 MHz chip. What fraction of the processor's time does it use? (800 000 / 16 000 000 = 5%.)
3. In `main.py`, change the work chunk to 900 cycles. How many ticks does polling miss now, and why does the latency still differ from the interrupt case?
4. With a 4.7 kohm pull-up and VIH = 0.7 x VDD, which capacitor gives a release delay between 5 and 10 ms? (t = RC ln(1/0.3) = 1.204 RC, so RC between 4.15 and 8.3 ms: C between 0.88 and 1.77 uF, for example 1 uF or 1.5 uF.)
5. Harder: a rotary encoder produces up to 2000 pulses per second. Polling between 2.5 ms work chunks, how many pulses can you lose per chunk? Write the minimum interrupt rate you would need if you sampled the encoder from a timer instead of a pin interrupt, and explain the Nyquist-like reason (Phase 19, Lesson 04).

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Timer | "A clock" | A hardware counter clocked by the system clock through a prescaler |
| Compare match | "The timer fired" | The counter reached the value in the compare register |
| Interrupt | "An event" | Hardware forcing the core to save its place and run an ISR |
| ISR | "The callback" | The function the vector table points to for one interrupt source |
| Polling | "Checking" | The program reads a flag when it gets round to it; events can be missed |
| Latency | "Response time" | Time from the event to the start of its handling |
| Debounce | "Fixing the button" | Ignoring contact bounce by waiting for a stable level |

## Further Reading

- [ATmega328P datasheet (Microchip)](https://www.microchip.com/en-us/product/ATmega328P), chapters "Interrupts" (the vector table) and "16-bit Timer/Counter1" (CTC mode and the frequency formula)
- [Jack Ganssle, "A Guide to Debouncing"](http://www.ganssle.com/debouncing.htm) — measurements of real switch bounce and both hardware and software fixes
- [Arm, "Cortex-M3 Devices Generic User Guide", section on the NVIC and exception entry](https://developer.arm.com/documentation/dui0552/latest/) — how a 32-bit core handles interrupts and priorities
- Elecia White, *Making Embedded Systems*, 2nd ed. (O'Reilly) — chapters on timers, interrupts and doing several things at once
