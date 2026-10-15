# Counters

> A counter is a register that adds one to itself at every clock edge. Each bit flips exactly when all the bits below it are 1.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lesson 02 (Binary Numbers) and Lesson 07 (Adders), Phase 15 (Sequential Logic), Lessons 03-04 (Flip-Flops and the Clock, Registers)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Counter | A register whose value goes up (or down) by one at each enabled clock edge | A tally clicker at a stadium gate |
| Count enable | An input that lets the counter advance or makes it pause | The thumb on the clicker |
| Toggle condition | The rule for when a bit must flip | The odometer rule: a wheel turns when every wheel to its right shows 9 |
| Synchronous counter | All flip-flops share the same clock and change together | All odometer wheels moving at the same instant |
| Ripple counter | Each flip-flop is clocked by the previous one's output | A row of dominoes, each knocking the next |
| Modulus | How many different values a counter goes through before repeating | A clock face: modulus 12 |
| Modulo-N counter | A counter that counts 0, 1, ..., N-1 and then wraps to 0 | A day counter that goes back to Monday after Sunday |
| Decade counter | A modulo-10 counter, one decimal digit | One digit of a digital clock's seconds |
| Terminal count | The last value before wrapping | 59 on a seconds display |
| Frequency divider | A counter used to make a slower clock from a fast one | Gears turning a fast motor into a slow wheel |
| Prescaler | A frequency divider in front of a timer | A gearbox in front of the speedometer |

## Learning Objectives

- Derive the next-state logic of a binary counter from the counting sequence: bit i toggles when all lower bits are 1.
- Build a synchronous n-bit counter with enable from XOR gates, AND gates and D flip-flops.
- Explain how each counter bit divides the clock frequency by two again.
- Build a modulo-10 (decade) counter with a synchronous reset at the terminal count.
- Explain how a ripple counter works and why its outputs pass through wrong values.

## The Problem

Counting is everywhere in digital systems. A microwave oven counts down seconds. A UART counts clock cycles to know when to sample the next bit. A processor's program counter steps through instructions (Phase 16). A timer in a microcontroller counts clock ticks to generate a precise 1 ms interrupt or a PWM signal (Phase 17). A screen controller counts pixels and lines.

All of these are the same circuit: a register and an adder that adds one, closed in a loop. We could use the full adder of Phase 14, Lesson 07, but adding one is so special that it needs much less logic. Deriving that logic from the pattern of binary counting is the core of this lesson, and it is our first complete example of **next-state logic**, which Lesson 06 generalises to any state machine.

## The Physics

A counter is a synchronous circuit (Lesson 03): flip-flops plus combinational logic between edges. Its speed limit is how fast the next-state logic settles. In a synchronous counter, the toggle condition of the top bit is an AND of all lower bits; built as a chain of 2-input ANDs, that chain grows with the width, just like the carry chain of an adder. A 32-bit counter needs a faster structure (lookahead, or splitting into small counters) to run at high clock rates.

Ripple counters avoid the AND chain entirely by clocking each flip-flop from the previous one, but then the flip-flops do not change at the same instant: each adds its own clock-to-output delay, so the delays pile up physically along the chain. The outputs are wrong for a short time after every edge, and wrong for longer the more bits flip.

## The Concept

### Watching binary count

Write the 4-bit counting sequence and look at each column:

```
 count  q3 q2 q1 q0
   0     0  0  0  0
   1     0  0  0  1
   2     0  0  1  0
   3     0  0  1  1
   4     0  1  0  0
   5     0  1  0  1
   6     0  1  1  0
   7     0  1  1  1
   8     1  0  0  0
   ...
  15     1  1  1  1
   0     0  0  0  0     wraps around
```

- `q0` flips at **every** step.
- `q1` flips when `q0` was 1 (from 1 to 2, from 3 to 4, ...).
- `q2` flips when `q1` and `q0` were both 1 (3 to 4, 7 to 8).
- `q3` flips when `q2`, `q1` and `q0` were all 1 (7 to 8, 15 to 0).

This is the odometer rule: a wheel advances when every wheel to its right is at its maximum. In binary the maximum is 1. It is also what the adder does when you add 1: the carry into column i is 1 exactly when all lower bits are 1.

### Next-state logic

Say the rule as an equation. Let `t_i` ("toggle i") be 1 when bit i must flip. With a count enable `en`:

```
t_0 = en
t_1 = en · q0
t_2 = en · q0 · q1
t_3 = en · q0 · q1 · q2
```

Each one is the previous one ANDed with one more bit: `t_(i+1) = t_i · q_i`. A bit that must flip gets the opposite of its value; a bit that must stay keeps it. "Flip when t is 1, keep when t is 0" is XOR (Phase 14, Lesson 04):

```
q_i+ = q_i ⊕ t_i
```

So the flip-flop input is `d_i = q_i XOR t_i`. The whole 4-bit counter:

```
 en ---+-----------+-----------+-----------+
       |           |           |           |
       v           v           v           v
     [XOR]<-q0   [AND]-t1->[XOR]<-q1   ... and so on
       |           ^           |
       d0          q0          d1
       |                       |
     [DFF]->q0               [DFF]->q1
```

In words: each stage has one XOR (to flip or not) and one AND (to pass the toggle condition up). For 4 bits: 4 XOR, 3 AND, 4 flip-flops. The simulator counts 7 gates and finds the longest path (en through the AND chain into the last XOR) has depth 4.

Check one step by hand, from 7 (0111) to 8 with `en = 1`:

```
t0 = 1               d0 = q0 ⊕ 1 = 1 ⊕ 1 = 0
t1 = 1 · q0 = 1      d1 = 1 ⊕ 1 = 0
t2 = 1 · q1 = 1      d2 = 1 ⊕ 1 = 0
t3 = 1 · q2 = 1      d3 = 0 ⊕ 1 = 1
next = 1000 = 8
```

With `en = 0`, every `t` is 0, every `d_i = q_i`, and the counter holds. The simulator's run:

```
  18 edges with en = 1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2]
  then en = 0, 0, 1, 0, 1:  [2, 2, 3, 3, 4]
```

After 15 comes 0: the counter is **modulo 16**, because 4 bits hold 16 values and the toggle of `q3` from 1 to 0 has nowhere to carry.

### Frequency division

Look at each bit as a waveform over 16 clock edges:

```
  q0 ‾_‾_‾_‾_‾_‾_‾_‾_   period  2 clock cycles
  q1 _‾‾__‾‾__‾‾__‾‾_   period  4
  q2 ___‾‾‾‾____‾‾‾‾_   period  8
  q3 _______‾‾‾‾‾‾‾‾_   period 16
```

Bit i has a period of `2^(i+1)` clock cycles, so its frequency is `f_clk / 2^(i+1)`. With a 16 MHz clock, `q0` is 8 MHz and `q3` is 1 MHz. Every bit is a square wave with 50 % duty cycle at half the frequency of the bit below: a counter is a chain of divide-by-two stages (Lesson 03's toggle flip-flop, repeated).

### Counting to something other than a power of two

A clock needs digits that go 0 to 9, or seconds that go 0 to 59. A **modulo-N** counter goes through N values and then returns to 0. The simplest way: detect the **terminal count** N-1 and make the next state 0 instead of N.

For a decade counter (N = 10), the terminal count is 9 = `1001`. Among the values 0 to 9, it is the only one with both `q3 = 1` and `q0 = 1` (8 is `1000`, and 10-15 never occur), so a single AND detects it:

```
nine = q3 · q0
```

At the edge where the counter shows 9 (and `en = 1`), we force all flip-flops to 0 with a **synchronous reset**. Our simulator's `dff` takes a `reset` wire that does exactly this. The output:

```
  [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3]
```

Two decade counters in a row, the second enabled only when the first is at 9, count 00 to 99: the `wrap` signal of one digit is the `en` of the next. That is how a digital clock or a frequency counter is built. Using the don't-cares (values 10-15 never happen) to shorten the detection logic is the same trick as the 7-segment decoder of Phase 14, Lesson 06.

There is also a tempting shortcut: let the counter reach 10 and clear it asynchronously with an immediate reset pin. It works on a breadboard, but the counter briefly shows 10 (a glitch on the outputs), and the reset pulse is only as long as it takes the flip-flops to clear, which may be too short to clear all of them. Synchronous reset at the terminal count is the safe way.

### Ripple counters

Before synchronous design was standard (and still in some low-power chips), counters were built without any AND chain. Each flip-flop is a toggle stage, and it is **clocked by the previous stage's output**: stage i+1 toggles when stage i falls from 1 to 0, which is exactly when a carry goes out of bit i.

```
 clk -->[T FF]--q0-->[T FF]--q1-->[T FF]--q2-->[T FF]--q3
          (each stage toggles on the falling edge of the one before)
```

It is very cheap (no gates at all) and each flip-flop runs at a lower frequency than the one before, which saves power. The price is timing. Each flip-flop needs a clock-to-output delay `tcq` (say 10 ns) to respond, and it only starts responding when the previous one has finished. Going from 7 (0111) to 8 (1000):

```
  t =  0 ns: clock edge
  t = 10 ns: q0 falls          count reads  6 (0110)
  t = 20 ns: q1 falls          count reads  4 (0100)
  t = 30 ns: q2 falls          count reads  0 (0000)
  t = 40 ns: q3 rises          count reads  8 (1000)
```

For 30 ns the outputs show 6, 4 and 0, values that are not the count at all. Any logic that decodes the outputs (for example "light an LED when the count is 0") would fire falsely. And the settling time grows with the number of bits: a 16-bit ripple counter needs up to 160 ns. Ripple counters are fine as simple frequency dividers, where only the last stage's frequency matters, but not where the count value is used.

## Build It

The script `code/main.py` builds the synchronous counters in `sim.logic` and simulates the ripple counter's timing in plain Python.

### Step 1: An n-bit synchronous counter

```python
def sync_counter(bits):
    lc = LogicCircuit(f"{bits}-bit synchronous counter")
    lc.inputs("en")
    toggle = "en"
    for i in range(bits):
        lc.xor(f"d{i}", f"q{i}", toggle)
        lc.dff(f"d{i}", f"q{i}", name=f"F{i}")
        if i < bits - 1:
            lc.and_(f"t{i + 1}", toggle, f"q{i}")
            toggle = f"t{i + 1}"
    lc.outputs(*[f"q{i}" for i in range(bits)])
    return lc
```

The variable `toggle` walks up the AND chain: it starts as `en`, then becomes `t1 = en·q0`, then `t2 = t1·q1`, and so on.

### Step 2: Run it

```python
def count(out, bits):
    return sum(out[f"q{i}"] << i for i in range(bits))

counter = sync_counter(4)
values = [count(counter.step({"en": 1}), 4) for _ in range(18)]
```

Each `step` is one clock edge, and `count` reads the bits back as a number (place value, Phase 14, Lesson 02).

### Step 3: The decade counter

```python
def decade_counter():
    lc = LogicCircuit("decade counter 0-9")
    lc.inputs("en")
    lc.and_("nine", "q3", "q0")
    lc.and_("wrap", "nine", "en")
    toggle = "en"
    for i in range(4):
        lc.xor(f"d{i}", f"q{i}", toggle)
        lc.dff(f"d{i}", f"q{i}", name=f"F{i}", reset="wrap")
        if i < 3:
            lc.and_(f"t{i + 1}", toggle, f"q{i}")
            toggle = f"t{i + 1}"
    lc.outputs("q3", "q2", "q1", "q0")
    return lc
```

`reset="wrap"` means: at an edge where `wrap = 1`, the flip-flop goes back to its initial value 0 instead of taking `d`.

### Step 4: The ripple counter's timing

The ripple counter is about timing, which `step()` deliberately hides, so the script models it directly: starting from a count, flip bit 0, wait `tcq`, and if it fell from 1 to 0, flip the next bit, and so on.

```python
def ripple_counter_events(start, bits=4, tcq_ns=10):
    q = [(start >> i) & 1 for i in range(bits)]
    events = []
    time = 0
    stage = 0
    while stage < bits:
        time += tcq_ns
        old = q[stage]
        q[stage] ^= 1
        events.append((time, sum(b << i for i, b in enumerate(q))))
        if old == 1:
            stage += 1
        else:
            break
    return events
```

`q[stage] ^= 1` flips one bit (`^` is Python's XOR).

Run it:

```bash
uv run python phases/15-sequential-logic/05-counters/code/main.py
```

## Use It

- **74HC161 / 74HC163** are 4-bit synchronous binary counters with parallel load; the '163 has a synchronous clear, the '161 an asynchronous one. **74HC160/162** are the decade versions.
- **74HC4040** is a 12-stage ripple counter and **CD4060** a 14-stage ripple counter with a built-in oscillator: the classic way to divide a 32,768 Hz crystal down to 2 Hz.
- **Microcontroller timers** (Phase 17, Lesson 05) are 8-, 16- or 32-bit synchronous counters with a prescaler, a compare register and an interrupt on overflow or match.
- **The program counter** of a processor (Phase 16, Lesson 04) is a counter with parallel load: it counts up through instructions and loads a new value for jumps.
- **Video timing.** A 1920 x 1080 display at 60 Hz is driven by a pixel counter and a line counter: 2200 pixel clocks per line (including blanking) and 1125 lines per frame, at a 148.5 MHz pixel clock.

## Try It in the Lab

The lab task "Next-state logic of a 2-bit counter" has two flip-flops holding `q1 q0` and the AND gate `t1 = q0·en` already wired. Slot S1 computes the next value of `q0` from `q0` and `en`; slot S2 computes the next value of `q1` from `q1` and `t1`. Parts: XOR, AND, OR, NAND. The checker applies 8 clock edges with `en` mostly 1 but sometimes 0, and checks both bits after each edge.

Think about: for each bit, when must it flip and when must it stay? Which gate flips its input exactly when a control input is 1?

## Common Mistakes

- **Using OR instead of XOR for the toggle.** `q OR t` sets a bit when it should flip it back to 0: the counter gets stuck at all ones.
- **Forgetting the enable in the toggle chain.** If `t1 = q0` instead of `en·q0`, bit 1 keeps flipping while the counter is "paused".
- **Detecting the terminal count with an asynchronous reset.** The counter shows the forbidden value briefly and some flip-flops may not clear. Use a synchronous reset at N-1.
- **Decoding ripple counter outputs.** Its outputs pass through wrong values after each edge. Only use them where that does not matter (dividing a clock), or sample them later with a synchronous register.
- **Off-by-one in modulus.** A counter that resets "when it reaches 10" counts 0-9 (modulus 10) only if the reset happens at the edge where it shows 9. Write the full sequence down and count the states.

## Exercises

1. Write the toggle conditions and XOR inputs for a 6-bit synchronous counter. How many XOR and AND gates are needed? What is the longest AND chain?
2. A 16 MHz clock drives an 8-bit counter. What are the frequencies of `q0` and `q7`? How long does the counter take to go all the way around from 0 back to 0?
3. Design a modulo-6 counter (0 to 5) from a 3-bit counter. Which count must you detect, and what is the simplest gate for it if counts 6 and 7 never occur?
4. A 12-bit ripple counter uses flip-flops with `tcq = 15 ns`. What is the worst-case settling time after a clock edge, and for which transition does it happen?
5. Build a down counter: from the pattern of counting down (15, 14, 13, ...), find when bit i must toggle. (Hint: it is the odometer rule with 0 instead of 1.) Modify `sync_counter` in the script to count down and check its output.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Synchronous counter | "Binary counter" | Flip-flops on one clock with next-state logic `q_i+ = q_i ⊕ (en·q0·...·q(i-1))` |
| Toggle condition | "When the bit flips" | Bit i flips when all lower bits are 1 (counting up) |
| Count enable | "en", "CE" | Gates the toggle chain so the counter can pause without touching the clock |
| Modulus | "Mod N" | The number of states a counter cycles through |
| Terminal count | "TC", "ripple carry out" | The last state before wrapping; often an output used to enable the next counter |
| Decade counter | "BCD counter" | A modulo-10 counter, one decimal digit |
| Ripple counter | "Asynchronous counter" | Each stage clocked by the previous output; cheap but its outputs pass through wrong values |
| Frequency divider | "Prescaler" | A counter whose top bit (or terminal count) is a slower clock |

## Further Reading

- M. Morris Mano and Michael D. Ciletti, *Digital Design*, Chapter 6 (Registers and Counters): ripple counters, synchronous counters, counters with unused states.
- Texas Instruments datasheets *SN74HC163* (synchronous 4-bit binary counter) and *CD74HC4040* (12-stage binary ripple counter).
- All About Circuits, *Digital* textbook (Vol. IV), chapter "Counters" (asynchronous and synchronous counters).
- Ben Eater, "8-bit computer: program counter" video (YouTube), a 74LS161 counter used as a program counter.
