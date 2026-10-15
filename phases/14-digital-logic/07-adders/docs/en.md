# Adders

> Adding is just school arithmetic done by XOR and AND gates, one column at a time, with the carry passed down the line.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lesson 02 (Binary Numbers), Lesson 04 (Logic Gates) and Lesson 06 (Combinational Circuits)
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Half adder | A circuit that adds two bits and gives a sum bit and a carry bit | Adding two single coins and counting "pairs" |
| Full adder | A circuit that adds three bits: two number bits plus an incoming carry | One column of school addition, including the carried 1 |
| Sum bit (s) | The bit written in the current column | The digit you write under the line |
| Carry in / carry out | The carry arriving from the column on the right / leaving to the column on the left | "Carry the one" |
| Ripple-carry adder | A chain of full adders where each carry feeds the next | A line of people passing a bucket along |
| Generate (g) | A column that creates a carry by itself (both bits are 1) | A full bucket appearing at one person in the line |
| Propagate (p) | A column that passes an incoming carry on (exactly one bit is 1) | A person who just hands the bucket along |
| Subtractor | An adder that computes a - b by adding the two's complement of b | Going backwards on an odometer |
| Carry flag | The carry out of the top column: the unsigned result did not fit | The odometer rolling over |
| Overflow flag | The signed result did not fit | A thermometer reading that wrapped from +127 to -128 |
| Carry-lookahead | A faster adder that computes carries in parallel instead of waiting for them to ripple | Shouting the result down the line instead of passing the bucket |

## Learning Objectives

- Derive the half adder and the full adder from their truth tables.
- Chain full adders into an n-bit ripple-carry adder and verify it exhaustively against arithmetic.
- Turn the adder into a subtractor with XOR gates and a carry-in, using two's complement.
- Detect unsigned overflow (carry) and signed overflow and explain the difference.
- Measure how the delay of a ripple adder grows with the number of bits and explain how carry-lookahead fixes it.

## The Problem

A computer that cannot add is not a computer. Addition is behind counting, addresses, loops, every multiplication (Phase 20), every pixel blend and every audio filter. Inside every processor there is an adder that runs billions of times per second.

Lesson 02 showed binary addition on paper. This lesson builds it from gates, the way it is built inside a chip, and finds its weakness: carries take time to travel. That weakness shaped the history of fast computers: much of the cleverness inside a modern processor's adder is about getting carries to the left end faster.

## The Physics

Physically, an adder is a combinational circuit (Lesson 06) made of CMOS gates (Lesson 05). Its special feature is a long chain: the carry out of each column is an input to the next one, so a change at the right end can travel through every column to the left end. Each column adds two gate delays. For a 64-bit adder made naively, that would be 128 gate delays, far too slow for a 3 GHz clock whose period is 0.33 ns. The engineering of adders is a fight against that chain.

## The Concept

### Adding two bits: the half adder

Adding two single bits has four cases, and the answer can be 0, 1 or 2. Two needs two bits to write (`10`), so the circuit has two outputs: the **sum** bit `s` (the ones column) and the **carry** bit `c` (the twos column).

```
 a b | a + b | c s
 ----+-------+-----
 0 0 |   0   | 0 0
 0 1 |   1   | 0 1
 1 0 |   1   | 0 1
 1 1 |   2   | 1 0
```

Look at the columns. `s` is 1 when exactly one input is 1: that is XOR (Lesson 04). `c` is 1 only when both are 1: that is AND.

```
s = a ⊕ b
c = a · b

  a ---+-----\\
       |      ))--- s
  b -+-|-----//
     | |
     | +----\
     |       )--- c
     +------/
```

It is called a **half** adder because it can do only half the job of a column: it has no input for a carry arriving from the right.

### Adding three bits: the full adder

A column in the middle of a long addition must add three bits: `a`, `b` and the carry in `cin`. The answer is 0, 1, 2 or 3, again written as two bits `cout s`:

```
 a b cin | a+b+cin | cout s
 --------+---------+-------
 0 0  0  |    0    |  0   0
 0 0  1  |    1    |  0   1
 0 1  0  |    1    |  0   1
 0 1  1  |    2    |  1   0
 1 0  0  |    1    |  0   1
 1 0  1  |    2    |  1   0
 1 1  0  |    2    |  1   0
 1 1  1  |    3    |  1   1
```

**The sum.** `s` is 1 when an odd number of inputs are 1, the parity of three bits: `s = a ⊕ b ⊕ cin`.

**The carry.** `cout` is 1 when at least two inputs are 1: the majority function from Lesson 03's exercises, `cout = a·b + a·cin + b·cin`. There is a neater form that reuses the XOR we already need. Define two helper signals:

```
g = a · b       "generate":  this column makes a carry on its own
p = a ⊕ b       "propagate": exactly one of a, b is 1, so a carry coming in will go out
```

Then the carry out happens if the column generates one, or if it propagates an incoming one:

```
cout = g + p · cin
s    = p ⊕ cin
```

Check the row `a=1, b=0, cin=1`: `g = 0`, `p = 1`, `cout = 0 + 1·1 = 1`, `s = 1 ⊕ 1 = 0`. The answer `cout s = 10` is 2, and indeed 1 + 0 + 1 = 2. Check the row `1, 1, 1`: `g = 1`, `p = 0`, `cout = 1`, `s = 0 ⊕ 1 = 1`, giving `11` = 3. Correct.

The full adder is two half adders plus an OR gate: the first half adder makes `p` and `g` from `a` and `b`; the second adds `cin` to `p`, giving `s` and `t = p·cin`; the OR combines the two possible carries.

```
         +---------- half adder 1 ---------+  +---- half adder 2 ----+
  a ---->| p = a ⊕ b ---------------------------> s = p ⊕ cin  ------------> s
  b ---->| g = a · b ---+                  |  |  t = p · cin  ---+   |
         +--------------|------------------+  +------------------|---+
                        |                         cin            |
                        +-------------> OR <---------------------+
                                         |
                                         +-----------------------------------> cout
```

Five gates: 2 XOR, 2 AND, 1 OR. Logic depth 3 (`a -> XOR -> AND -> OR`).

### The ripple-carry adder

To add two 4-bit numbers, put four full adders side by side, one per column, and connect each carry out to the carry in of the next column to the left. The rightmost carry in is 0.

```
   a3 b3        a2 b2        a1 b1        a0 b0
    | |          | |          | |          | |
  +-----+  c3  +-----+  c2  +-----+  c1  +-----+
  | FA3 |<-----| FA2 |<-----| FA1 |<-----| FA0 |<---- cin = 0
  +-----+      +-----+      +-----+      +-----+
   |   |          |            |            |
  c4   s3         s2           s1           s0
 (carry out)
```

Worked example, 6 + 7 = 13: `A = 0110`, `B = 0111`.

```
column 0: a0=0, b0=1, cin=0   -> s0 = 1, c1 = 0
column 1: a1=1, b1=1, cin=0   -> s1 = 0, c2 = 1     (generate)
column 2: a2=1, b2=1, cin=1   -> s2 = 1, c3 = 1     (generate, and propagates nothing extra)
column 3: a3=0, b3=0, cin=1   -> s3 = 1, c4 = 0
result: s3 s2 s1 s0 = 1101 = 13, carry out 0
```

Exactly the hand calculation of Lesson 02, column by column.

### Subtraction for (almost) free

Lesson 02 showed that `a - b = a + (-b)` and that `-b` in two's complement is "invert every bit, then add 1". In hardware:

- "Invert every bit of b" is one XOR per bit with a control signal `sub`: when `sub = 0`, `b ⊕ 0 = b` (unchanged); when `sub = 1`, `b ⊕ 1 = b'` (inverted). This is the "controlled inverter" from Lesson 04.
- "Add 1" is feeding `sub` into the carry in of the rightmost full adder.

```
          b3      b2      b1      b0
           |       |       |       |
  sub ---(XOR)---(XOR)---(XOR)---(XOR)
           |       |       |       |
   a3 -->[FA3]<--[FA2]<--[FA1]<--[FA0]<---- cin = sub
```

So one adder plus n XOR gates does both operations, selected by one wire. Example, 2 - 5 in 4 bits: `sub = 1`, `B = 0101` becomes `1010`, plus carry in 1:

```
    0010     (2)
  + 1010     (5 inverted)
  +    1     (carry in)
  ------
    1101     = 13 unsigned, -8 + 4 + 1 = -3 signed
```

2 - 5 = -3. Correct. For subtraction the carry out has a twist: it is 1 when **no borrow** was needed (a >= b as unsigned numbers) and 0 when a < b. Here it is 0, because 2 < 5.

### Two kinds of "it didn't fit"

The adder's bits are the same whether you think of them as unsigned or signed (that is the beauty of two's complement). What differs is how you detect a result that does not fit.

**Unsigned overflow: the carry flag.** If the true sum needs n + 1 bits, the extra bit is the carry out. 9 + 9 = 18 in 4 bits: 18 = `10010`, the 4 wires show `0010` = 2 and the carry out is 1.

**Signed overflow: the overflow flag.** In 4-bit two's complement, the range is -8 to +7. 6 + 7 = 13 is too big: the wires show `1101`, which reads as -3. The carry out is 0, so the carry flag does not notice. The rule from Lesson 02: overflow happens when two numbers with the same sign give a result with the other sign. In terms of carries there is a neat equivalent: **signed overflow happens exactly when the carry into the top column differs from the carry out of it.**

```
v = c(n-1) ⊕ c(n)
```

Check 6 + 7: column 3 receives `c3 = 1` and produces `c4 = 0`; `1 ⊕ 0 = 1`, overflow. Check 9 + 9 = `1001 + 1001`: `c3 = 0`, `c4 = 1`, overflow again, because as signed numbers this is (-7) + (-7) = -14, below -8. Check 2 - 5, column by column (`0010 + 1010` with carry in 1): column 0 is 0+0+1 = 1, `c1 = 0`; column 1 is 1+1+0 = 10, `c2 = 1`; column 2 is 0+0+1 = 1, `c3 = 0`; column 3 is 0+1+0 = 1, `c4 = 0`. So `c3 = c4 = 0` and there is no overflow, which is right: -3 fits. Doing these by hand once is the best way to trust the rule. Processors store both flags, and the program picks the one matching its meaning.

### The weakness: carries ripple

In the worst case, a carry created in column 0 must travel through every column. Take `1111 + 0001`. Column 0 makes a carry; column 1 has `p = 1` so passes it on; and so on to the end. Each column adds two gate delays (the AND for `t = p·cin` and the OR for `cout`). In the simulator, with one time unit per gate:

```
c1 at t=3, c2 at t=5, c3 at t=7, c4 at t=9
```

The carry advances 2 delays per bit. For an n-bit ripple adder the critical path is about `2n` gate delays plus a few at the ends. The simulator's depth measurements for our adder/subtractor (which has the extra XOR in front of b):

```
 bits | depth (gate delays) | 74HC estimate (8 ns per gate)
   4  |        11           |     88 ns
   8  |        19           |    152 ns
  16  |        35           |    280 ns
  32  |        67           |    536 ns
```

Depth grows in proportion to the width: double the bits, double the delay. A 64-bit ripple adder in modern transistors (about 15 ps per gate) would take about 131 delays, 2 ns, six times too slow for a 3 GHz clock.

### Carry-lookahead: computing carries in parallel

The fix is to stop waiting. Write the carries out using `g` and `p`:

```
c1 = g0 + p0·c0
c2 = g1 + p1·c1 = g1 + p1·g0 + p1·p0·c0
c3 = g2 + p2·g1 + p2·p1·g0 + p2·p1·p0·c0
```

Read `c3` out loud: "column 2 generates a carry, or column 1 generates and column 2 propagates it, or column 0 generates and columns 1 and 2 propagate it, or the carry in is propagated by all three". Every `g` and `p` is available after one gate delay, so each carry is a two-level AND-OR expression: about 3 gate delays for any carry, no waiting. The cost is more gates, and the expressions grow with width. Real designs group bits into blocks of 4, compute block-level `G` and `P`, and apply the same trick again on the blocks (a tree), so the delay grows with the **logarithm** of the width: a 64-bit adder in about 12-15 gate delays instead of 130. The 74HC283 4-bit adder chip uses lookahead internally; the classic 74182 was a separate lookahead carry generator for linking several 4-bit adders. Phase 20 (Lesson 01) measures this area-for-speed trade.

## Build It

The script `code/main.py` builds adders in `sim.logic` and checks them against Python's own arithmetic.

### Step 1: Half adder and full adder

```python
def half_adder():
    lc = LogicCircuit("half adder")
    lc.inputs("a", "b")
    lc.xor("s", "a", "b")
    lc.and_("c", "a", "b")
    lc.outputs("s", "c")
    return lc


def add_full_adder(lc, a, b, cin, s, cout, tag):
    lc.xor(f"{tag}.p", a, b)
    lc.xor(s, f"{tag}.p", cin)
    lc.and_(f"{tag}.g", a, b)
    lc.and_(f"{tag}.t", f"{tag}.p", cin)
    lc.or_(cout, f"{tag}.g", f"{tag}.t")
```

`add_full_adder` adds the five gates of one full adder to an existing circuit. The `tag` keeps the inner wire names of different columns apart (`fa0.p`, `fa1.p`, ...). The script checks the arithmetic identity `2 x cout + s = a + b + cin` on all 8 rows.

### Step 2: An n-bit adder/subtractor

```python
def add_sub(bits):
    lc = LogicCircuit(f"{bits}-bit adder/subtractor")
    a = [f"a{i}" for i in range(bits)]
    b = [f"b{i}" for i in range(bits)]
    lc.inputs(*a, *b, "sub")
    carry = "sub"
    for i in range(bits):
        lc.xor(f"bx{i}", b[i], "sub")
        add_full_adder(lc, a[i], f"bx{i}", carry, f"s{i}", f"c{i + 1}", f"fa{i}")
        carry = f"c{i + 1}"
    lc.xor("v", f"c{bits - 1}", f"c{bits}")
    lc.outputs(*[f"s{i}" for i in range(bits)], f"c{bits}", "v")
    return lc
```

The carry chain starts at `sub` (carry in = 1 for subtraction), each `b` bit passes through an XOR with `sub`, and the overflow flag `v` compares the last two carries.

### Step 3: Driving numbers in and out

Bit `i` of a number `x` is `(x >> i) & 1`: shift right by `i` places and keep the lowest bit. Reading the result back is the place-value sum of Lesson 02.

```python
def drive(bits, x, y, sub=0):
    inputs = {f"a{i}": (x >> i) & 1 for i in range(bits)}
    inputs.update({f"b{i}": (y >> i) & 1 for i in range(bits)})
    inputs["sub"] = sub
    return inputs

def read(out, bits):
    total = sum(out[f"s{i}"] << i for i in range(bits))
    return total, out[f"c{bits}"], out["v"]
```

### Step 4: Verify

All 512 4-bit cases (every `x`, every `y`, add and subtract) are compared with `(x + y) % 16` and `(x - y) % 16`; the 8-bit version is checked on 2000 random cases, including the overflow flag against the true signed result.

```
  512 cases (256 additions, 256 subtractions): 0 wrong
   3 +  4: bits 0111 =  7 unsigned /   7 signed, carry 0, overflow 0
   6 +  7: bits 1101 = 13 unsigned /  -3 signed, carry 0, overflow 1
   9 +  9: bits 0010 =  2 unsigned /   2 signed, carry 1, overflow 1
   2 -  5: bits 1101 = 13 unsigned /  -3 signed, carry 0, overflow 0
  12 -  5: bits 0111 =  7 unsigned /   7 signed, carry 1, overflow 1
```

Read the last line carefully: as unsigned numbers 12 - 5 = 7, correct, carry 1 means no borrow. As signed numbers `1100` is -4, and -4 - 5 = -9 does not fit in -8..7, so the overflow flag is set. Same bits, two meanings, two flags.

### Step 5: Watch the ripple and measure depth

```python
changes = adder4.events(before=drive(4, 15, 0), after={"b0": 1})
for bits in (4, 8, 16, 32):
    print(bits, add_sub(bits).depth())
```

Run it:

```bash
uv run python phases/14-digital-logic/07-adders/code/main.py
```

## Use It

- **74HC283** is a 4-bit binary full adder with fast carry in a 16-pin package; two of them chained make an 8-bit adder for a breadboard computer.
- **Every processor's ALU** (Phase 16, Lesson 02) contains an adder/subtractor exactly like this one, with carry and overflow flags that conditional branches test.
- **Address calculation.** Every memory access computes "base + offset" with an adder; every loop counter increments with one.
- **Multipliers** are arrays of full adders (Phase 20, Lesson 02). The simulator's `sim.logic` module has an `array_multiplier` built from the same full adder.
- **Fast adder designs** such as Kogge-Stone and Brent-Kung (named after their inventors) are carry-lookahead trees used in high-speed processors.

## Try It in the Lab

The lab task "Finish the full adder" has the generate gate `g = a·b` and the final OR already in place. Three slots remain: the gate that makes `p` from `a` and `b`, the gate that makes `s` from `p` and `cin`, and the gate that makes `t` from `p` and `cin`. The parts are XOR, AND, OR and NAND. Both `s` and `cout` must be right in all 8 rows.

Think about: which gate gives "an odd number of 1s"? When exactly should `t` be 1 so that `cout = g + t` is right?

## Common Mistakes

- **Forgetting the carry in.** A half adder in a middle column ignores the carry from the right. Every column except possibly the first needs a full adder.
- **Wrong bit order.** Bit 0 (the LSB) is where the carry chain starts. Wiring the carry chain from the MSB end adds the numbers backwards.
- **Reading the carry flag as signed overflow.** 6 + 7 in 4 bits gives carry 0 but signed overflow; 12 - 5 gives carry 1 and signed overflow. The two flags answer different questions.
- **Forgetting the +1 in subtraction.** Inverting b without setting the carry in to 1 computes `a - b - 1`.
- **Assuming a wide adder is as fast as a narrow one.** A ripple adder's delay grows with every bit added; check the critical path when you widen a design.

## Exercises

1. Add 11 + 6 in 4 bits column by column, writing `p`, `g`, `cin`, `s`, `cout` for every column. What are the carry and overflow flags?
2. Compute 3 - 7 in 4 bits with the invert-and-add-1 method. What is the result as unsigned and as signed? What is the carry out, and what does it tell you?
3. Show from the truth table that `cout = g + p·cin` equals the majority function `a·b + a·cin + b·cin` in all 8 rows.
4. A 16-bit ripple adder is built from full adders with 2 gate delays per carry stage, plus 2 delays at the ends. With 5 ns gates, what is its worst-case delay, and what is the maximum rate (additions per second) if each addition must wait for the result?
5. Write `c4` for a 4-bit carry-lookahead adder in terms of `g0..g3`, `p0..p3` and `c0`. How many product terms does it have? How many inputs does its largest AND gate need? What does this suggest about building a 32-bit lookahead adder in one level?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Half adder | "XOR and AND" | Adds two bits: `s = a ⊕ b`, `c = a·b` |
| Full adder | "One column" | Adds three bits: `s = a ⊕ b ⊕ cin`, `cout = a·b + (a ⊕ b)·cin` |
| Ripple-carry adder | "The simple adder" | n full adders with each carry out feeding the next carry in; delay grows with n |
| Generate / propagate | "g and p" | `g = a·b` makes a carry; `p = a ⊕ b` passes one on |
| Adder/subtractor | "Add or subtract with one wire" | XOR each b bit with `sub` and feed `sub` into the first carry in |
| Carry flag | "C" | Carry out of the top column: unsigned overflow on add, no-borrow on subtract |
| Overflow flag | "V" | Carry into the top column XOR carry out of it: signed overflow |
| Carry-lookahead | "Fast carry" | Computing every carry directly from g and p in parallel, at the cost of more gates |

## Further Reading

- David Harris and Sarah Harris, *Digital Design and Computer Architecture*, Chapter 5 (Digital Building Blocks: adders, ripple-carry and carry-lookahead).
- Noam Nisan and Shimon Schocken, *The Elements of Computing Systems* (Nand2Tetris), Chapter 2 (Boolean Arithmetic), where the adder is built from the gates of Chapter 1.
- Texas Instruments datasheet *SN74HC283* (4-bit binary full adder with fast carry).
- Ben Eater, "Making an 8-bit computer: ALU" videos (YouTube), for an adder/subtractor built on breadboards from 74LS283 and 74LS86 chips.
