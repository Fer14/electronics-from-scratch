# Combinational Circuits

> Describe what you want in words, turn the words into a table, turn the table into gates, and then check every row.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lesson 03 (Boolean Algebra) and Lesson 04 (Logic Gates)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Combinational circuit | A gate network whose outputs depend only on the inputs right now, not on the past | A calculator key press: same keys, same answer, every time |
| Specification (spec) | The precise description of what a circuit must do | The client's order form |
| Multi-bit signal | A number carried on several wires, one per bit | A row of flags held up together |
| Comparator (digital) | A circuit that tells whether two numbers are equal, or which is larger | A balance scale |
| BCD | "Binary-coded decimal": one decimal digit 0-9 stored in 4 bits | A 4-switch box that only ever shows the patterns for 0 to 9 |
| 7-segment display | Seven LED bars arranged to draw a digit | The digits on a microwave oven |
| Decoder (display) | A circuit that turns a code into the pattern that shows it | A translator from numbers to drawings |
| Don't care | An output value we are free to choose because the input never occurs | A menu item that is never ordered: any price will do |
| Critical path | The slowest path from any input to any output | The slowest runner in a relay team, which decides the team's time |
| Glitch | A brief wrong output while signals race through paths of different lengths | A flicker when you switch from one light to another |
| Hazard | A circuit structure that can produce a glitch | A road layout where two cars can briefly meet |
| Consensus term | An extra, logically redundant product term added to remove a hazard | An overlap in two shifts so the shop is never unstaffed |

## Learning Objectives

- Follow the design flow: spec, truth table, expression, simplification, gates, verification.
- Design a 2-bit equality and magnitude comparator and verify it against arithmetic for all 16 inputs.
- Design one segment of a 7-segment BCD decoder using don't-care conditions.
- Compute logic depth and the worst-case delay of a combinational circuit.
- Explain how unequal path delays cause glitches, observe one in the simulator and remove it with a consensus term.

## The Problem

You have the vocabulary (Boolean algebra) and the parts (gates). Now someone gives you a job: "the kitchen timer must show the remaining minutes on a 7-segment display" or "the vending machine must check that the code the customer typed equals the code of the slot". Nobody hands you an expression. You have to go from a description in words to a working, checked circuit, and you need to know how fast it will respond.

Circuits like these, with no memory, are called **combinational**: the output is a fixed function of the current inputs. Every digital system is made of combinational blocks (computing) and memory blocks (remembering, Phase 15). This lesson gives you a repeatable recipe for the first kind and shows the one timing trap they hide: glitches.

## The Physics

A combinational circuit is a network of CMOS gates (Lesson 05). Each gate needs a few nanoseconds to charge or discharge its output capacitance, so a change at an input spreads through the network like a wave: first the gates connected to the input, then the gates after them, and so on. Paths of different lengths deliver their changes at different times. While the wave is still travelling, the outputs can briefly show values that the Boolean equations never predict. Only after the slowest path has finished does the output equal the truth table. Physically, then, "combinational" means "the output equals the function **after it has settled**". This settling time is what limits clock speed in Phase 15.

## The Concept

### The design flow

Every combinational design follows the same steps:

```
1. Spec        say precisely what the circuit must do, with names for every input and output
2. Table       write the truth table (or a rule that generates it)
3. Expression  sum of products from the 1 rows (Lesson 03)
4. Simplify    Boolean laws or a Karnaugh map, using don't-cares
5. Gates       map the expression onto the gates you have (NAND only? XOR available?)
6. Verify      check every row against the spec, ideally with an independent model
7. Timing      find the logic depth and estimate the delay
```

Step 6 is the one beginners skip. Real chip teams spend more effort verifying than designing, because a wrong gate in a chip that has been manufactured cannot be fixed with a screwdriver.

### Example 1: a 2-bit equality comparator

**Spec.** Two 2-bit numbers `A = a1 a0` and `B = b1 b0` (Lesson 02: `a1` is the twos bit, `a0` the ones bit). Output `eq = 1` when `A = B`.

**Think before tabulating.** A table would have 2^4 = 16 rows. But the spec has structure: two numbers are equal exactly when every bit position matches. One bit position matches when `a1 = b1`, which is the XNOR (Lesson 04): `e1 = (a1 ⊕ b1)'`. So:

```
eq = e1 · e0 = (a1 ⊕ b1)' · (a0 ⊕ b0)'
```

By De Morgan, `X'·Y' = (X + Y)'`, so with XOR gates and one NOR:

```
eq = NOR( a1 ⊕ b1 , a0 ⊕ b0 )
```

```
  a1 ---\\
         ))--- d1 ---\
  b1 ---//            \
                       NOR o--- eq
  a0 ---\\            /
         ))--- d0 ---/
  b0 ---//
```

Read it out loud: "there is a difference in bit 1, or a difference in bit 0; the codes are equal when there is neither". This generalises: an 8-bit equality comparator is 8 XORs feeding an 8-input NOR. That is exactly how a cache checks whether an address is stored (Phase 20).

### Example 2: "greater than"

**Spec.** `gt = 1` when `A > B` (as unsigned numbers).

**Think like you compare numbers by hand:** look at the most significant bit first. If `a1 = 1` and `b1 = 0`, A is bigger whatever the low bits are. If the top bits are equal, the low bits decide: `a0 = 1` and `b0 = 0`.

```
gt = a1·b1'  +  e1·a0·b0'
     ^ top bit decides    ^ top bits equal, low bit decides
```

Check a few rows with a calculator: A = 2 (10), B = 1 (01): `a1·b1' = 1·1 = 1`, so gt = 1. Correct. A = 1 (01), B = 0 (00): first term `0·1 = 0`; `e1 = 1` (both top bits 0), `a0·b0' = 1·1`, second term 1, so gt = 1. Correct. A = 1, B = 2: first term `0`, `e1 = 0`, gt = 0. Correct.

The simulator checks all 16 rows against Python's `>` and `==` operators and reports 0 wrong. Using an independent model (here, ordinary arithmetic) to check a gate-level design is the most important habit of this lesson. The comparator uses 8 gates and has a logic depth of 3 (`b0 -> NOT -> AND -> OR`, or `a1 -> XNOR -> AND -> OR`).

"Less than" needs no new circuit: `A < B` is `(A > B)' · (A = B)'`, or simply swap A and B.

### Example 3: one segment of a 7-segment display

A 7-segment display has seven LED bars named `a` to `g`:

```
     aaaa
    f    b
    f    b
     gggg
    e    c
    e    c
     dddd
```

To show the digit 7 you light `a`, `b` and `c`. To show 3 you light `a, b, c, d, g`. A **BCD-to-7-segment decoder** takes a digit in 4 bits `A B C D` (A is the eights bit) and lights the right bars. It has 7 outputs; each one is its own combinational function of 4 inputs. Here is segment `a` (the top bar):

```
digit  ABCD   segments lit   a
  0    0000   a b c d e f    1
  1    0001     b c          0
  2    0010   a b   d e   g  1
  3    0011   a b c d     g  1
  4    0100     b c     f g  0
  5    0101   a   c d   f g  1
  6    0110   a   c d e f g  1
  7    0111   a b c          1
  8    1000   a b c d e f g  1
  9    1001   a b c d   f g  1
 10-15 1010-1111  never happens  X (don't care)
```

The plain sum of products has 8 minterms of 4 literals each. Now use the don't-cares. On a 4-variable Karnaugh map (rows `AB`, columns `CD`, both in Gray order 00, 01, 11, 10):

```
              CD
           00   01   11   10
        +----+----+----+----+
 AB=00  |  1 |  0 |  1 |  1 |     digits 0, 1, 3, 2
        +----+----+----+----+
 AB=01  |  0 |  1 |  1 |  1 |     digits 4, 5, 7, 6
        +----+----+----+----+
 AB=11  |  X |  X |  X |  X |     12-15 never happen
        +----+----+----+----+
 AB=10  |  1 |  1 |  X |  X |     digits 8, 9, (11, 10)
        +----+----+----+----+
```

Treat every X as a 1 where it helps and circle the largest groups:

- The two bottom rows (`A = 1`): all 1s or X. A group of 8, term `A`.
- The two right columns (`C = 1`): all 1s or X. A group of 8, term `C`.
- The middle block `B = 1, D = 1` (rows 01 and 11, columns 01 and 11): a group of 4, term `B·D`.
- The four corners (`B = 0, D = 0`): the map wraps around at its edges, so the corners are neighbours. A group of 4, term `B'·D'`.

```
a = A + C + B·D + B'·D'
```

Five gates (two NOTs, two ANDs, one 4-input OR) instead of eight 4-input ANDs plus an 8-input OR. Check digit 4 (0100): `A = 0`, `C = 0`, `B·D = 1·0 = 0`, `B'·D' = 0·1 = 0`, so `a = 0`: the top bar is dark, which is correct for a 4. The simulator checks all ten digits. (The real 74HC4511 chip contains all seven of these functions, plus a latch and blanking logic.)

Notice what the don't-cares cost: if an invalid code like 1010 did arrive, the display would show some odd pattern. That is acceptable only if the spec guarantees such codes never come. Writing down that assumption is part of the design.

### Timing: logic depth and the critical path

Lesson 04 defined logic depth: the largest number of gates on any input-to-output path. The path that achieves it is the **critical path**. For the segment decoder, the path `B -> NOT -> AND -> OR` crosses 3 gates. With a 74HC gate at about 8 ns:

```
worst-case delay = 3 x 8 ns = 24 ns
```

That means after the input changes, you must wait 24 ns before trusting the output. 24 ns sounds tiny, but it limits how often the inputs may change: no more than once every 24 ns, about 40 million times per second. Phase 15 turns this into the maximum clock frequency.

Two refinements real designers make:

- Gates with more inputs are slower (Lesson 05: more transistors in series), so "depth" counted in gates is a first estimate. Our simulator counts every gate as one delay unit.
- Different paths have different lengths. The **shortest** path matters too, because it determines how early the output starts to change. That gap between shortest and longest is what creates glitches.

### Glitches and hazards

Consider `y = a·b + a'·c`. It is a 2-to-1 selector: when `a = 1`, y follows b; when `a = 0`, y follows c (Lesson 08 calls it a multiplexer). Set `b = 1` and `c = 1`. Then whatever `a` is, y should be 1. Now let `a` fall from 1 to 0, and follow the wave with one time unit per gate:

```
t = 0   a -> 0
t = 1   p = a·b   -> 0     (the AND fed directly by a reacts first)
t = 1   na = a'   -> 1     (the inverter reacts at the same time)
t = 2   q = na·c  -> 1     (this AND had to wait for the inverter)
t = 2   y = p + q -> 0     (the OR saw p = 0 and q = 0 at t = 1!)
t = 3   y         -> 1     (now it sees q = 1)
```

For one gate delay the output was 0, a value the truth table never allows. This short false pulse is a **glitch**, and the structure that permits it is a **static-1 hazard**: two product terms hand over the job of keeping y at 1, and for a moment neither is holding it.

```
 a   ‾‾‾‾‾|_____________
 p   ‾‾‾‾‾‾‾|___________     (falls after 1 delay)
 q   _________|‾‾‾‾‾‾‾‾‾     (rises after 2 delays)
 y   ‾‾‾‾‾‾‾‾‾|_|‾‾‾‾‾‾     (one-delay glitch)
```

The fix comes from Boolean algebra. The **consensus theorem** says `a·b + a'·c = a·b + a'·c + b·c`: the extra term `b·c` never changes the truth table (when `b = c = 1`, one of the other terms is already 1). But in hardware, `b·c` stays at 1 throughout the hand-over, because it does not depend on `a` at all. The simulator shows `y` never moves once the cover term is added. On the Karnaugh map, the rule is: **a hazard exists where two adjacent 1s are covered by different groups and no single group covers both; add a group that bridges them.**

### Do glitches matter?

Often not. In a synchronous design (Phase 15), outputs are only looked at on a clock edge, long after the glitches have died out. That is the main reason digital designers use clocks. Glitches do matter when a combinational output drives something that reacts instantly: the clock input of a flip-flop, a reset line, an asynchronous interrupt, or a chip-select of a memory. They also waste power, because every false transition charges and discharges a capacitance (Lesson 05).

## Build It

The script `code/main.py` builds the comparator, the segment decoder and the hazard circuit in `sim.logic`, and checks each one against an independent model.

### Step 1: The comparator

The `and_` and `or_` methods accept any number of inputs, so `g0 = e1·a0·b0'` is one 3-input AND.

```python
def comparator():
    lc = LogicCircuit("2-bit comparator")
    lc.inputs("a1", "a0", "b1", "b0")
    lc.xnor("e1", "a1", "b1")
    lc.xnor("e0", "a0", "b0")
    lc.and_("eq", "e1", "e0")
    lc.not_("nb1", "b1")
    lc.not_("nb0", "b0")
    lc.and_("g1", "a1", "nb1")
    lc.and_("g0", "e1", "a0", "nb0")
    lc.or_("gt", "g1", "g0")
    lc.outputs("eq", "gt")
    return lc
```

### Step 2: Verify against arithmetic

For every one of the 16 input combinations, we rebuild the numbers A and B from their bits and compare the circuit with Python's own `==` and `>`:

```python
def check_comparator(lc):
    wrong = 0
    for a1, a0, b1, b0 in product((0, 1), repeat=4):
        a, b = 2 * a1 + a0, 2 * b1 + b0
        out = lc.evaluate({"a1": a1, "a0": a0, "b1": b1, "b0": b0})
        wrong += out["eq"] != int(a == b)
        wrong += out["gt"] != int(a > b)
    return wrong
```

Output (part):

```
   A  B | eq gt
   2  1 |  0  1
   2  2 |  1  0
   2  3 |  0  0
  checked against Python's == and > for all 16 rows: 0 wrong
  gates: 8, logic depth: 3
```

### Step 3: Segment `a`

```python
SEGMENTS = {
    0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg",
    5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg", 9: "abcdfg",
}

def segment_a():
    lc = LogicCircuit("segment a of a BCD display")
    lc.inputs("A", "B", "C", "D")
    lc.not_("nB", "B")
    lc.not_("nD", "D")
    lc.and_("BD", "B", "D")
    lc.and_("nBnD", "nB", "nD")
    lc.or_("a", "A", "C", "BD", "nBnD")
    lc.outputs("a")
    return lc
```

The `SEGMENTS` dictionary is the independent model: which bars each digit lights. The script loops over digits 0-9, compares, and prints `True` when all ten agree.

### Step 4: Watching a glitch

`events(before, after)` advances one gate delay at a time and reports every wire change:

```python
lc = hazard_circuit(with_cover=False)
changes = lc.events(before={"a": 1, "b": 1, "c": 1}, after={"a": 0})
```

```
  y = a·b + a'·c
    t=0: a->0, t=1: na->1, t=1: p->0, t=2: q->1, t=2: y->0, t=3: y->1
    y changed 2 times (glitch!)
  y = a·b + a'·c + b·c
    t=0: a->0, t=1: na->1, t=1: p->0, t=2: q->1
    y changed 0 times (clean)
```

### Step 5: Delay

`lc.depth()` returns the critical path in gate delays. The script multiplies it by 8 ns for a 74HC estimate.

Run it:

```bash
uv run python phases/14-digital-logic/06-combinational-circuits/code/main.py
```

## Use It

- **74HC85** is a 4-bit magnitude comparator chip with `A>B`, `A=B` and `A<B` outputs and cascading inputs so several chips compare longer numbers.
- **74HC4511** is a BCD-to-7-segment decoder/driver; **CD4543** drives LCD versions. Inside each is exactly the kind of logic built here.
- **Processors** compare constantly: every `if a == b` in a program ends up in an equality comparator; every branch "if less than" uses the subtractor's flags (Phase 16).
- **Caches** compare the tag bits of an address with the stored tags, in parallel, using wide XOR-NOR equality comparators (Phase 20, Lesson 07).
- **Glitch-free design rules.** Hardware teams have a rule: never use the output of combinational logic as a clock or asynchronous reset. Lint tools in chip design flag it automatically.

## Try It in the Lab

The lab task "Are two 2-bit numbers equal?" has three empty slots: one gate compares `a1` with `b1`, one compares `a0` with `b0`, and a third combines the two answers into `eq`. The parts are XOR, AND, OR, NOR and NAND. All 16 rows must be right.

Think about: what should each first-level gate output when its two bits differ? When should the final gate output 1, in terms of "differences"?

## Common Mistakes

- **Skipping verification.** A design that "looks right" on paper often has one wrong row. Always check every row against an independent model (arithmetic, a lookup table, a Python function).
- **Using don't-cares that do happen.** If the input can in fact take a "never happens" value (a noisy switch, a reset state), the output there is whatever your simplification made it. Make sure that is safe.
- **Forgetting map wrap-around.** On a Karnaugh map the left and right edges are neighbours, and so are the top and bottom. The four corners of a 4x4 map form one group.
- **Treating the shortest path as the delay.** The output is trustworthy only after the longest path has settled.
- **Using a combinational output as a clock.** Glitches on it will be seen as extra clock edges. Phase 15 explains how clocked design avoids this.

## Exercises

1. Extend the equality comparator to 4-bit numbers. How many XOR gates do you need, and what goes at the output? What is its logic depth if you only have 2-input gates?
2. Write `lt` (A < B) for 2-bit numbers as a sum of products in the same "top bit first" style as `gt`. Check it for A = 0, B = 3 and A = 3, B = 2.
3. Using the table in this lesson, write the column for segment `g` (the middle bar) for digits 0-9 and simplify it with a Karnaugh map using don't-cares. (One possible answer: `g = A + B·C' + B'·C + C·D'`.)
4. A circuit has three paths from input to output with 2, 4 and 5 gates. Each gate takes between 5 and 9 ns. What is the earliest the output can start to change, and the latest it is guaranteed to be settled?
5. For `y = a'·b' + a·c`, set `b = 0` and `c = 1` and let `a` rise from 0 to 1. Is there a glitch with one time unit per gate? Which consensus term removes it? Add it in the script and confirm.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Combinational circuit | "Pure logic" | Gates without feedback or memory; once settled, outputs depend only on current inputs |
| Comparator | "Equal / greater than" | Equality: XNOR per bit then AND; magnitude: decide from the most significant differing bit |
| BCD | "Binary-coded decimal" | One decimal digit in 4 bits, using only patterns 0000-1001 |
| Don't care | "X" | An output we may set freely because that input never occurs; enlarges Karnaugh groups |
| Critical path | "The slow path" | The longest input-to-output path; sets the worst-case delay |
| Glitch | "A spike" | A brief wrong output value caused by paths with unequal delays |
| Hazard | "A glitch waiting to happen" | A gate structure where a single input change can produce a glitch |
| Consensus term | "The redundant term" | `b·c` in `a·b + a'·c + b·c`: logically redundant, but it holds the output during the hand-over |

## Further Reading

- M. Morris Mano and Michael D. Ciletti, *Digital Design*, Chapter 4 (combinational logic: analysis and design procedure, magnitude comparators, decoders).
- John F. Wakerly, *Digital Design: Principles and Practices*, the chapters on combinational logic design and timing hazards.
- Texas Instruments datasheets *SN74HC85* (4-bit magnitude comparator) and *CD74HC4511* (BCD-to-7-segment latch/decoder/driver).
- All About Circuits, *Digital* textbook (Vol. IV), chapter "Combinational Logic Functions".
