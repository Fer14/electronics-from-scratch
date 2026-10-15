# Logic Gates

> A gate is a tiny decision machine with one job, and one kind of gate, NAND, is enough to build all the others.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lesson 01 (Analog vs Digital), Lesson 03 (Boolean Algebra)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Logic gate | A small circuit whose output is a Boolean function of its inputs | A turnstile that opens only under the right conditions |
| Inverter | The NOT gate | A seesaw: one side up means the other side down |
| NAND | "Not AND": AND followed by NOT | A smoke alarm test: it stays quiet only when every sensor reports "all clear" |
| NOR | "Not OR": OR followed by NOT | A "room empty" light that is on only when no motion sensor fires |
| XOR | "Exclusive OR": 1 when the inputs differ | A staircase light with a switch at the bottom and top: flip either one and the light changes |
| XNOR | "Exclusive NOR": 1 when the inputs are equal | An equality checker |
| Universal gate | A gate type from which every other gate can be built | A single Lego brick shape that can build any model |
| Bubble | The small circle on a gate symbol that means "invert here" | A "not" sign stamped on a wire |
| Propagation delay | The time between an input change and the resulting output change | The time between pressing a doorbell and hearing it |
| Logic depth | The number of gates a signal crosses on the longest path | The number of hand-offs in a relay race |
| Fan-out | How many gate inputs one output can drive reliably | How many people one speaker can address without a microphone |
| 74HC series | A family of standard logic chips, each with a few gates inside | Off-the-shelf Lego sets with a few bricks each |

## Learning Objectives

- Draw (in ASCII) and recognise the symbols of NOT, AND, OR, NAND, NOR, XOR and XNOR, and write their truth tables.
- Explain why NAND and NOR are called universal and build NOT, AND and OR from NAND alone.
- Build XOR from four NAND gates and check it with the simulator.
- Measure logic depth and estimate the total delay of a small circuit.
- Read the basics of a 74HC logic chip: gates per package, pins, propagation delay and fan-out.

## The Problem

Lesson 03 gave you a language for decisions: expressions like `b·(a + c)`. An expression on paper does not switch a fan on. You need physical parts that compute AND, OR and NOT on real wires, parts you can buy, solder and connect.

Those parts are **logic gates**. In the 1960s and 70s engineers built whole computers (including the guidance computer that flew to the Moon) out of chips that each contained a handful of gates. Today a phone processor contains billions of them. Interestingly, the Apollo Guidance Computer used only one kind of gate: a 3-input NOR. Its designers did not do that to be clever; it made manufacturing and testing simpler. This lesson shows why one gate type is enough, and how to build the others from it.

## The Physics

A gate is built from transistor switches (Lesson 05 opens one up). From the outside, a gate behaves like this:

- Its inputs draw almost no current (a CMOS input is the gate of a MOSFET, which is insulated: Phase 12, Lesson 04). So one output can drive many inputs.
- Its output connects to either the supply or ground through a transistor that is switched on. That is how it regenerates clean levels (Lesson 01).
- Changing the output takes time, because the output must charge or discharge the small capacitance of the wires and of the inputs it drives (Phase 07: a capacitor charged through a resistance takes about one time constant RC). That time is the **propagation delay**, typically a few nanoseconds for a 74HC chip and a few picoseconds for a gate inside a modern processor.
- Each extra input it drives adds capacitance, which slows it down. That is what limits **fan-out**.

So a gate is a fast, regenerating, almost-zero-input-current decision machine. The rest of this lesson treats it as ideal and only counts gate delays.

## The Concept

### The seven gates

Here are the gates you will use for the rest of the course. Rows of each truth table are in binary counting order (ab = 00, 01, 10, 11).

```
NOT (inverter)            a  | y
                          ---+---
      a --|>o-- y         0  | 1
                          1  | 0
```

The triangle means "amplifier/buffer"; the small circle, called a **bubble**, means "invert". A triangle without a bubble is a **buffer** (output = input), which we used in Lesson 01.

```
AND                       OR                        XOR
  a --+---\                 a --\\---\                a --\\\---\
      |    )-- y                ||    >-- y               |||    >-- y
  b --+---/                 b --//---/                b --///---/

 a b | y                   a b | y                   a b | y
 0 0 | 0                   0 0 | 0                   0 0 | 0
 0 1 | 0                   0 1 | 1                   0 1 | 1
 1 0 | 0                   1 0 | 1                   1 0 | 1
 1 1 | 1                   1 1 | 1                   1 1 | 0
```

ASCII cannot draw the real curves, so remember the shapes in words: AND has a flat back and a round "D" front; OR has a curved back and a pointed front; XOR is an OR with an extra curved line behind it.

The inverted versions add a bubble at the output:

```
NAND = AND + bubble       NOR = OR + bubble         XNOR = XOR + bubble
  a ---\                    a ---\                    a ---\
        )o-- y                    >o-- y                    >o-- y
  b ---/                    b ---/                    b ---/

 a b | y                   a b | y                   a b | y
 0 0 | 1                   0 0 | 1                   0 0 | 1
 0 1 | 1                   0 1 | 0                   0 1 | 0
 1 0 | 1                   1 0 | 0                   1 0 | 0
 1 1 | 0                   1 1 | 0                   1 1 | 1
```

A compact way to remember all of them by their column of outputs:

```
gate  : output for ab = 00 01 10 11
AND   :                  0  0  0  1     "all"
OR    :                  0  1  1  1     "any"
NAND  :                  1  1  1  0     "not all"
NOR   :                  1  0  0  0     "none"
XOR   :                  0  1  1  0     "different" (odd number of 1s)
XNOR  :                  1  0  0  1     "equal"
```

### XOR in words and in algebra

XOR deserves a closer look, because it is the heart of the adder (Lesson 07) and appears all over computing. In Boolean algebra, using the symbol `⊕`:

```
a ⊕ b = a·b' + a'·b
```

Read it: "a and not b, or not a and b", which is "exactly one of them". Two everyday pictures: the staircase light (each switch flips the light, so the light is on when the switches disagree), and a "controlled inverter": if `b = 0`, `a ⊕ b = a`; if `b = 1`, `a ⊕ b = a'`. So XOR lets one bit decide whether another bit is flipped. That second picture is how the ALU in Phase 16 turns an adder into a subtractor.

XOR of more than two inputs is 1 when an **odd** number of inputs are 1. That is called **parity**, and it is the simplest error-detecting code: send 7 data bits plus their XOR, and the receiver can tell if any single bit was flipped by noise.

### Universality: one gate to build them all

A set of gates is **universal** (engineers say "functionally complete") if every Boolean function can be built from it. Lesson 03 showed that AND, OR and NOT are enough, because any truth table can be written as a sum of products. So to prove NAND is universal, we only have to build NOT, AND and OR from NANDs.

**NOT from NAND.** Tie both inputs together: `NAND(a, a) = (a·a)' = a'` (idempotent law, `a·a = a`).

```
  a --+--\
      |   )o-- a'
      +--/
```

**AND from NAND.** A NAND followed by a NOT (made from another NAND): `NAND(NAND(a,b), NAND(a,b)) = ((a·b)')' = a·b`. Two gates.

**OR from NAND.** By De Morgan, `a + b = (a'·b')' = NAND(a', b')`. Invert each input with a NAND, then NAND them. Three gates.

```
  a --[NAND a,a]-- a' --\
                         )o-- a + b
  b --[NAND b,b]-- b' --/
```

Check OR from NAND on the row a=1, b=0: a' = 0, b' = 1, NAND(0, 1) = (0·1)' = 0' = 1. Correct.

NOR is universal by the mirror-image argument: `NOR(a, a) = a'`, `NOR(NOR(a,b), NOR(a,b)) = a + b`, and `NOR(a', b') = (a' + b')' = a·b`.

Why does anyone care, if AND and OR exist as chips? Two reasons. On a chip, NAND and NOR are the natural gates of CMOS (Lesson 05): an AND gate is actually built as a NAND plus an inverter, so it is bigger and slower. And with a single gate type, a factory, a test procedure or a spare-parts box handles only one design.

### XOR from four NANDs

Building XOR directly from the universality recipes would cost many gates: `a·b' + a'·b` needs 2 NOTs, 2 ANDs and an OR, which become 2 + 4 + 3 = 9 NANDs. There is a famous trick that needs only 4:

```
             +----------[NAND]-- n2 --+
  a ---------+          /             |
             |         /              +--[NAND]-- y
             +--[NAND]-- n1           |
             |         \              |
  b ---------+          \             |
             +----------[NAND]-- n3 --+

  n1 = NAND(a, b)      n2 = NAND(a, n1)      n3 = NAND(b, n1)      y = NAND(n2, n3)
```

Work through all four rows by hand. This is exactly what the simulator prints:

```
 a b | n1 = (ab)' | n2 = (a·n1)' | n3 = (b·n1)' | y = (n2·n3)'
 0 0 |     1      |      1       |      1       |      0
 0 1 |     1      |      1       |      0       |      1
 1 0 |     1      |      0       |      1       |      1
 1 1 |     0      |      1       |      1       |      0
```

Why it works, in algebra. Start with `n2 = (a·n1)' = (a·(a·b)')'`. Simplify the inside first, using De Morgan and the complement law:

```
a·(a·b)' = a·(a' + b') = a·a' + a·b' = 0 + a·b' = a·b'
```

So `n2 = (a·b')'`, and by the same steps `n3 = (a'·b)'`. The last gate is a NAND of two inverted terms, and De Morgan turns a NAND of inverted terms into an OR:

```
y = (n2·n3)' = n2' + n3' = a·b' + a'·b = a ⊕ b
```

The shared gate n1 does double duty as "not both" for both branches.

### Gates with more inputs

AND, OR, NAND and NOR extend naturally to 3, 4 or 8 inputs: AND is 1 if **all** inputs are 1, OR if **any** is. A 3-input AND can also be made from two 2-input ANDs, `(a·b)·c`, thanks to the associative law. Careful: this is **not** true for NAND. `NAND(NAND(a,b), c)` is not a 3-input NAND, because the inner NAND inverts. Check the row a=b=c=1: the inner NAND gives 0, the outer NAND(0, 1) gives 1, but a true 3-input NAND gives 0.

### Delay and logic depth

Every gate takes a little time to respond. For a 74HC00 at 5 V the datasheet gives a typical propagation delay of about 8 ns (and a maximum of around 20 ns over temperature). If a signal must pass through 3 gates in a row, the output can take up to 3 delays to settle.

The **logic depth** of a circuit is the largest number of gates on any path from an input to an output. The XOR from four NANDs has depth 3 (a -> n1 -> n2 -> y). Our simulator computes it with `lc.depth()`. Estimated worst-case delay:

```
delay = depth x delay per gate = 3 x 8 ns = 24 ns
```

Not every input change uses the longest path. If `b = 0` and `a` rises, `n1` stays at 1, so the change travels only `a -> n2 -> y`, two gate delays. The simulator's `events()` method shows this, step by step. In Lesson 06 we see that differences between path lengths can create short false pulses called glitches, and in Phase 15 that the longest path sets how fast a clock can tick.

### Fan-out

One gate output can feed several inputs. Each input adds a few picofarads of capacitance (about 3.5 pF for a 74HC input), which slows the output down. For CMOS, the practical limit is speed, not a fixed number: the datasheet states delays at a test load (often 50 pF), so an output driving ten 74HC inputs (35 pF) plus some board wiring stays near the datasheet delay. Older TTL chips had a hard fan-out limit of about 10 because each input really drew current.

### Real chips: the 74HC family

The 7400 series started in the 1960s with TTL chips from Texas Instruments; the 74HC (high-speed CMOS) versions are what you can still buy in a 14-pin package for a few cents:

| Part | Contents | Function |
|---|---|---|
| 74HC00 | 4 x 2-input NAND | `(a·b)'` |
| 74HC02 | 4 x 2-input NOR | `(a+b)'` |
| 74HC04 | 6 x NOT | `a'` |
| 74HC08 | 4 x 2-input AND | `a·b` |
| 74HC32 | 4 x 2-input OR | `a+b` |
| 74HC86 | 4 x 2-input XOR | `a ⊕ b` |

A 14-pin chip has 2 power pins (VCC and GND) and 12 signal pins: 4 gates times (2 inputs + 1 output) = 12. That is why there are four 2-input gates or six inverters per chip.

## Build It

The script `code/main.py` builds every gate in `sim.logic`, proves NAND and NOR universal, builds XOR from four NANDs and watches a change ripple through it.

### Step 1: All gates at once

`lc.gate(op, inputs, output)` adds a gate of any type by name. We put the six 2-input gates on the same two inputs and read each column.

```python
TWO_INPUT_GATES = ["and", "or", "nand", "nor", "xor", "xnor"]

def all_gates():
    lc = LogicCircuit("the basic gates")
    lc.inputs("a", "b")
    lc.not_("not_a", "a")
    for op in TWO_INPUT_GATES:
        lc.gate(op, ["a", "b"], op)
    lc.outputs("not_a", *TWO_INPUT_GATES)
    return lc

def column(lc, output):
    return [row[output] for row in lc.truth_table(outputs=[output])]
```

Output (rows ab = 00, 01, 10, 11):

```
  not_a  [1, 1, 0, 0]
  and    [0, 0, 0, 1]
  or     [0, 1, 1, 1]
  nand   [1, 1, 1, 0]
  nor    [1, 0, 0, 0]
  xor    [0, 1, 1, 0]
  xnor   [1, 0, 0, 1]
```

### Step 2: NOT, AND and OR from NAND only

```python
def from_nand_only():
    lc = LogicCircuit("NOT, AND, OR from NAND")
    lc.inputs("a", "b")
    lc.nand("not_a", "a", "a")
    lc.nand("t", "a", "b")
    lc.nand("and_ab", "t", "t")
    lc.nand("na", "a", "a")
    lc.nand("nb", "b", "b")
    lc.nand("or_ab", "na", "nb")
    lc.outputs("not_a", "and_ab", "or_ab")
    return lc
```

The script compares each column with the real gate and prints the expected columns side by side. A mirror-image function `from_nor_only` does the same with NOR.

### Step 3: XOR from four NANDs

```python
def xor_from_nands():
    lc = LogicCircuit("XOR from four NANDs")
    lc.inputs("a", "b")
    lc.nand("n1", "a", "b")
    lc.nand("n2", "a", "n1")
    lc.nand("n3", "b", "n1")
    lc.nand("y", "n2", "n3")
    lc.outputs("y")
    return lc
```

`format_truth_table` prints the inner wires too, so you can compare with the hand-worked table above:

```
   a    b   n1   n2   n3    y
   0    0    1    1    1    0
   0    1    1    1    0    1
   1    0    1    0    1    1
   1    1    0    1    1    0
  matches XOR: True
  logic depth: 3 gate delays (a single XOR gate: 1)
```

### Step 4: Watching the change travel

`lc.events(before, after)` settles the circuit with the `before` inputs, applies the `after` change and then lets every gate react one time unit after its inputs change.

```python
changes = xor4.events(before={"a": 0, "b": 0}, after={"a": 1})
for time, wire, value in changes:
    print(f"t = {time}: {wire} -> {value}")
```

```
  t = 0: a -> 1
  t = 1: n2 -> 0
  t = 2: y -> 1
  with a 74HC00 at 5 V (about 8 ns per gate), y settles after about 24 ns in the worst case
```

With b = 0, n1 does not move, so this change needs only two gate delays. Try `before={"a": 0, "b": 1}, after={"a": 1}` in the script: now n1 also changes and you will see the three-step path.

Run it:

```bash
uv run python phases/14-digital-logic/04-logic-gates/code/main.py
```

## Use It

- **74HC chips on breadboards.** The classic way to learn digital electronics hands-on is a breadboard, a 5 V supply and a few 74HC00, 74HC04 and 74HC86 chips with LEDs on the outputs. Every circuit in this phase can be built that way.
- **Single-gate chips.** Modern boards use tiny one-gate packages such as the 74LVC1G00 (one NAND in a 5-pin SOT-23) to fix a logic mismatch between two bigger chips.
- **Inside processors.** A standard-cell library (Phase 20) offers NAND2, NOR2, INV, AOI ("AND-OR-invert") and dozens more cells; synthesis tools favour NAND and NOR forms for the reasons above.
- **Parity and checksums.** XOR trees compute parity bits in memory chips with error checking (ECC RAM) and in serial links (UART parity, Phase 17).
- **Simple cryptography.** XOR with a secret key stream hides data and XOR with the same key reveals it again, because `(m ⊕ k) ⊕ k = m`. Stream ciphers are built on this.

## Try It in the Lab

The lab task "Build XOR from four NAND gates" fixes the first NAND (`n1 = NAND(a, b)`) and leaves three slots: one combining `a` with `n1`, one combining `b` with `n1`, and the output gate combining the two. Your drawer has NAND, NOR and AND gates. Fill the slots so `y` is 1 exactly when `a` and `b` differ.

Think about: what is `n1` in each of the four rows? For which single row should the slot fed by `a` and `n1` output 0?

## Common Mistakes

- **Forgetting the bubble.** NAND and AND differ only by a small circle on the symbol, and the output is the exact opposite. Read every symbol carefully.
- **Chaining NANDs to make a wider NAND.** `NAND(NAND(a, b), c)` is not `(a·b·c)'`. Wider AND and OR can be chained; their inverted versions cannot.
- **Treating XOR as OR.** They differ only in the row 1, 1: OR gives 1, XOR gives 0. "Either one, but not both".
- **Leaving unused inputs floating on a real chip.** An unused gate on a 74HC00 should have its inputs tied to VCC or GND. A floating CMOS input can drift into the forbidden zone and make the gate oscillate and draw current (Lesson 01).
- **Ignoring delay.** Logic depth adds up. A circuit with 20 gates in a row is 20 times slower than one gate, and this sets the clock speed of everything built on it.

## Exercises

1. Write the truth table of a 3-input XOR. How many of its 8 rows are 1? Why is it called a parity gate?
2. Build NOT, OR and AND from NOR gates only, on paper. How many NORs does each need? Check one row of each by hand.
3. Show with the row a = b = c = 1 that `NAND(NAND(a, b), c)` is not a 3-input NAND. What 2-gate circuit made only of NANDs is a 3-input NAND? (Hint: you need an AND first.)
4. The XOR from four NANDs has depth 3. With 74HC00 gates at a worst-case 20 ns each, what is the worst-case delay? A 74HC86 XOR is listed at about 25 ns maximum at 4.5 V. Which is faster in the worst case?
5. Using only XOR gates, build a circuit that outputs 1 when an odd number of 4 inputs `a, b, c, d` are 1. How many 2-input XOR gates do you need, and what is the logic depth if you arrange them as a chain? As a tree?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Logic gate | "A gate" | A transistor circuit that computes a fixed Boolean function of its inputs and outputs a regenerated level |
| NAND / NOR | "Not-and / not-or" | AND / OR followed by inversion; the natural, cheapest gates in CMOS |
| XOR | "Exclusive or" | 1 when the inputs differ; a controllable inverter and a parity checker |
| Universal gate | "You can build anything from NAND" | A gate from which NOT, AND and OR, hence every Boolean function, can be built |
| Propagation delay | "Gate delay", "tpd" | Time from an input change to the output change, set by charging the load capacitance |
| Logic depth | "Levels of logic" | The largest number of gates on any input-to-output path; multiply by the gate delay to estimate speed |
| Fan-out | "How many it can drive" | The number of inputs one output drives; more fan-out means more capacitance and more delay |

## Further Reading

- Texas Instruments datasheets: *SN74HC00* (NAND), *SN74HC02* (NOR), *SN74HC86* (XOR), for pinouts, delays and input capacitance.
- Noam Nisan and Shimon Schocken, *The Elements of Computing Systems* (Nand2Tetris), Chapter 1 (Boolean Logic), where every gate is built from NAND.
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 10 (Digital Logic), on gates, families and practical wiring.
- Eldon C. Hall, *Journey to the Moon: The History of the Apollo Guidance Computer* (1996), for the all-NOR design of the AGC.
