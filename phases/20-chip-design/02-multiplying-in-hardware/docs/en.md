# Multiplying in Hardware

> Multiplication is just addition of shifted copies. But the copies grow as the square of the bits, and so does the silicon.

**Type:** Build
**Prerequisites:** Phase 20 (Chip Design), Lesson 01 (From Gates to Adders); Phase 14 (Digital Logic), Lessons 02 (Binary Numbers) and 07 (Adders)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Multiplicand / multiplier | The two numbers being multiplied (in `13 x 11`, 13 is the multiplicand and 11 the multiplier) | The price and the quantity on a receipt |
| Product | The result of a multiplication | The total on the receipt |
| Partial product | One shifted copy of the multiplicand, kept or zeroed by one bit of the multiplier | One line of a long multiplication done by hand |
| Shift | Moving all bits one place to the left (times 2) or right (divide by 2) | Adding a zero at the end of a decimal number to multiply by 10 |
| Array multiplier | A grid of AND gates and adders that adds all partial products at once | A spreadsheet that sums every row in one go |
| Half adder | An adder for two bits (XOR + AND); enough when there is no carry coming in | A full adder with one input missing |
| Column | All the bits with the same weight (same power of two) | The units, tens, hundreds columns of school arithmetic |
| Quadratic growth | Growing with the square of a size: double the size, four times the cost | Doubling the side of a tiled floor needs four times the tiles |
| Bit width (precision) | How many bits a number has; more bits mean a wider range or finer steps | How many digits a calculator can display |
| Throughput per area | How much useful work a piece of silicon does per unit of area | How many meals a kitchen serves per square metre |

## Learning Objectives

- Multiply two binary numbers by hand using partial products, and explain why each partial product is just AND gates.
- Build and verify a 4 x 4 array multiplier with `sim.logic`, and count its area and delay.
- Replace full adders by half adders where an input is always 0, and save gates without changing the result.
- Show that a multiplier's area grows with the square of its bit width, while an adder's grows linearly.
- Explain why lowering precision from 8 to 4 bits gives roughly four to five times more multipliers in the same silicon, and why that matters for AI chips.

## The Problem

A neural network spends almost all of its time multiplying numbers and adding up the results (the next lesson). A large language model generating one word multiplies billions of pairs of numbers. If you want a chip that does this fast and cheaply, the multiplier is the first block to understand.

Adders are cheap: in Lesson 01, an 8-bit adder cost 40 gates. A multiplier is different. You will see that an 8-bit multiplier costs about 344 gates in our model, a 16-bit one about 1,456, and a 32-bit one almost 6,000. Every doubling of the width costs about four times more silicon. That simple fact explains a lot of modern hardware: why AI accelerators use 8-bit and even 4-bit numbers, why graphics cards boast about "INT8 TOPS", and why number formats are a hot research topic (Lesson 10).

## The Physics

There is no new physics in a multiplier: it is made of the same AND, XOR and OR gates as an adder, each a few transistors charging and discharging tiny capacitances (Lesson 01). What is new is *how many* gates there are, and how they are wired. The amount of silicon, the delay and the energy all follow from that count. A multiplier is a good reminder that in chip design, structure (how blocks are connected) matters as much as the devices themselves.

One physical point is worth noting. Every gate that switches costs energy (`C * V^2` per switch). A multiplier has many more gates than an adder, and many of them switch on every operation. So a multiplier does not only take more area, it also burns more energy per operation: in real 45 nm silicon, an 8-bit integer multiply costs about 0.2 pJ while an 8-bit add costs about 0.03 pJ, and a 32-bit multiply about 3 pJ (Mark Horowitz's widely quoted figures, ISSCC 2014). Doubling the width roughly quadruples both.

## The Concept

### Long multiplication, in binary

Multiply 13 by 11 the school way, but in binary. 13 is `1101` and 11 is `1011`. Each digit of the multiplier selects either a copy of the multiplicand (if the digit is 1) or zero (if it is 0), shifted left by the digit's position:

```
                1 1 0 1      13  (multiplicand a)
              x 1 0 1 1      11  (multiplier b)
              ---------
                1 1 0 1      b0 = 1: 13 shifted by 0 =  13
              1 1 0 1 .      b1 = 1: 13 shifted by 1 =  26
            0 0 0 0 . .      b2 = 0: zero             =   0
          1 1 0 1 . . .      b3 = 1: 13 shifted by 3 = 104
          -------------
        1 0 0 0 1 1 1 1      13 + 26 + 0 + 104 = 143
```

Two things make this easy in hardware:

1. **Selecting a copy is an AND gate.** Bit `i` of the partial product for row `j` is `a_i AND b_j`: if `b_j` is 1 you get `a_i`, if it is 0 you get 0. For 4-bit numbers that is `4 * 4 = 16` AND gates, one per pair of bits.
2. **Shifting is free.** Shifting by `j` places just means wiring the bits into a column `j` places further left. No gates at all.

What costs real hardware is **adding** all those rows.

### The array multiplier

The straightforward way to add the rows is the way you would on paper: add row 1 to row 0, then add row 2 to that result, then row 3. Each addition is a ripple adder of 4 bits, arranged in a staircase:

```
column:    7     6     5     4     3     2     1     0
row 0:                       p03   p02   p01   p00          (a_i AND b0)
row 1:                 p13   p12   p11   p10                (a_i AND b1), shifted 1
row 2:           p23   p22   p21   p20                      shifted 2
row 3:     p33   p32   p31   p30                            shifted 3

adders:  row 1 adds into columns 1-4, row 2 into columns 2-5, row 3 into columns 3-6
```

`pji` means `a_i AND b_j`, with weight `2^(i + j)`. Each adder row has 4 full adders, and there are 3 rows (one for each row of partial products after the first): 12 full adders. The version in `sim.logic` (`array_multiplier`) builds exactly this, with every adder a full adder:

```
area = 16 AND + 12 full adders * 5 gates = 16 + 60 = 76 gates
```

In general, for `N`-bit numbers: `N^2` AND gates and `N (N - 1)` full adders, so

```
area = N^2 + 5 N (N - 1) gates
```

Read that out loud: "N squared for the partial products, plus five gates for each of N times N-minus-one full adders". The leading term is `6 N^2`: area grows with the **square** of the width.

The delay in `sim.cost` is `6 (N - 1)` gate delays (18 for 4 bits): each of the `N - 1` adder rows adds a few gate delays along the staircase. `sim.logic` measures exactly 18 for its gate-level 4 x 4 multiplier, so the model and the netlist agree.

### Trimming: half adders where an input is always zero

Look closely at the staircase. Some full adders are adding only two real bits, because their third input is a constant 0:

- the rightmost adder of each row has no carry coming in;
- the leftmost adder of the first row has no bit from row 0 above it (row 0 has only 4 bits).

A full adder whose carry-in is 0 simplifies:

```
s    = p XOR 0          = p           (the second XOR is not needed)
t    = p AND 0          = 0           (the carry-through AND is not needed)
cout = g OR 0           = g           (the OR is not needed)
```

What is left is a **half adder**: one XOR (`p = a XOR b`) and one AND (`g = a AND b`), 2 gates instead of 5. In a 4 x 4 multiplier there are four such adders, so

```
76 - 4 * 3 = 64 gates
```

That is 16% less area for exactly the same products. In general, an `N x N` array multiplier needs `N` half adders and `N (N - 2)` full adders, for `N^2 + 2N + 5N(N - 2) = 6N^2 - 8N` gates (64 for 4 bits, 320 for 8). Real synthesis tools do this kind of simplification automatically ("constant propagation"), but it pays to see it once.

The trimmed multiplier is also a little faster (16 gate delays instead of 18), because the half adders are shallower. Faster multiplier structures exist: **Wallace trees** and **Dadda trees** add all the columns in parallel with layers of full adders (each full adder takes three bits of one column and produces one bit for the same column and one for the next), reaching a delay that grows with `log N` instead of `N`, with about the same number of adders. **Booth encoding** halves the number of partial products by recoding the multiplier. All of them still have the `N^2` partial products at their heart.

### Why the square matters: precision is area

Compare adders and multipliers as the width grows (our model):

| Bits | Adder (gates) | Multiplier (gates) | Multiplier / bits^2 | Multiplier / adder |
|---|---|---|---|---|
| 4 | 20 | 76 | 4.75 | 3.8 |
| 8 | 40 | 344 | 5.38 | 8.6 |
| 16 | 80 | 1,456 | 5.69 | 18.2 |
| 32 | 160 | 5,984 | 5.84 | 37.4 |

The adder doubles when the width doubles; the multiplier roughly quadruples. Now fix a budget of 100,000 gates and ask how many multipliers fit:

```
16-bit: 100000 / 1456 =   68 multipliers
 8-bit: 100000 /  344 =  290 multipliers
 4-bit: 100000 /   76 = 1315 multipliers
```

Going from 8-bit to 4-bit numbers gives `1315 / 290 = 4.5` times more multipliers in the same silicon, and therefore (if you can keep them busy) about 4.5 times more multiplications per second per square millimetre. Going from 16-bit to 4-bit gives 19 times more. This is the hardware reason behind the push towards low-precision arithmetic in AI. Neural networks tolerate surprisingly coarse numbers, so designers happily trade precision for silicon. The catch (Lesson 10) is that very coarse numbers need care to keep a model accurate, and the accumulators that add the products must stay wide (Lesson 03).

## Build It

Run:

```
uv run python phases/20-chip-design/02-multiplying-in-hardware/code/main.py
```

### Step 1: Partial products in Python

```python
def partial_products(x, y, bits):
    return [((x if (y >> j) & 1 else 0) << j) for j in range(bits)]
```

`(y >> j) & 1` is bit `j` of the multiplier; `<< j` is the shift. For 13 x 11 the rows are 13, 26, 0 and 104, which add up to 143.

### Step 2: The full array multiplier

`array_multiplier(4)` from `sim.logic` builds the 16 AND gates and 12 full adders. The script checks it on all 256 pairs of 4-bit numbers (256 correct) and prints its cost: 76 gates and a depth of 18, the same as `sim.cost.multiplier(4)`.

### Step 3: The trimmed multiplier

```python
def trimmed_multiplier(bits):
    ...
    for j in range(1, bits):
        carry = None
        new_row = []
        for i in range(bits):
            x, y = f"pp{j}_{i}", row[i + 1]
            s, co = f"r{j}c{i}.s", f"r{j}c{i}.co"
            inputs = [n for n in (x, y, carry) if n is not None]
            if len(inputs) == 3:
                full_adder(lc, *inputs, s, co, tag=f"r{j}c{i}")
            else:
                half_adder(lc, *inputs, s, co, tag=f"r{j}c{i}")
            carry = co
            new_row.append(s)
```

Instead of feeding a constant 0 into a full adder, the builder notices when an input is missing (`None`) and uses a half adder. Output: 64 gates (36 AND, 20 XOR, 8 OR), depth 16, and 256 of 256 products correct.

### Step 4: Area versus width

The script prints the table above from `sim.cost.adder` and `sim.cost.multiplier`. The column "mult / bits^2" settles towards 6, the coefficient of the leading `6 N^2` term.

### Step 5: Multipliers per budget

For a 100,000-gate budget: 68 sixteen-bit, 290 eight-bit or 1,315 four-bit multipliers. The ratio 8-bit to 4-bit is 4.5x.

### Step 6: The lab

The script checks the lab task's reference solution with `sim.lab.evaluate`.

## Use It

- **AI accelerators.** Google's first TPU (2015-2016) used 8-bit integer multipliers precisely because they are so much smaller than floating-point ones; it packed 65,536 of them into one chip (Lesson 06). Recent GPUs and accelerators support 8-bit and 4-bit formats and quote their peak throughput separately for each width, typically doubling it each time the width halves.
- **CPUs.** A desktop CPU has a handful of 64-bit multipliers per core, built as Booth-encoded Wallace or Dadda trees, pipelined over 3-4 clock cycles (Lesson 05).
- **Microcontrollers.** Small cores such as the ARM Cortex-M0 offer either a fast single-cycle 32-bit multiplier or a small one that takes 32 cycles (one partial product per cycle, reusing one adder), selectable when the chip is designed: a classic area-for-time choice.
- **FPGAs** contain hard-wired multiplier blocks ("DSP slices", typically 18 x 18 or 27 x 18 bits) because building multipliers from the general-purpose logic would waste so much area (Lesson 09).

## Try It in the Lab

Open "Trim the 4x4 multiplier to 64 gates". It is the 76-gate array multiplier, with the last three gates of six of its adders left open as slots (for two of those adders only the first two gates are open). Each slot takes a gate (XOR, AND, OR) or a plain wire, which passes its first input straight through and costs nothing. Your goals: all 256 products right, at most 64 gates. For each slotted adder, look at its inputs: which ones really have a constant 0 coming in, and what does each equation become when you substitute 0?

## Common Mistakes

- **Thinking a multiplier is "a few adders".** For N-bit numbers it is about N adders of N bits each, plus N^2 AND gates: quadratic, not linear.
- **Forgetting the product is twice as wide.** Two N-bit numbers make a 2N-bit product (15 x 15 = 225 needs 8 bits). Dropping the top bits is an overflow.
- **Removing gates that are not really constant.** A half adder is only correct where an input is *always* 0. The lab includes adders that look similar but are not.
- **Equating "fewer bits" with "free speed".** Fewer bits give more multipliers per area, but they also lose precision, and the data still has to be moved to them (Lesson 04).
- **Ignoring signed numbers.** Two's complement multiplication needs a few extra tricks (sign extension or the Baugh-Wooley method); the unsigned array is where everyone starts.

## Exercises

1. Multiply `1011` (11) by `0110` (6) in binary with partial products. Write each row and check the sum.
2. Using `N^2 + 5N(N - 1)`, compute the area of a 6 x 6 array multiplier. How many of its full adders could become half adders, and what would the trimmed area be?
3. A design needs 1,000 multiply operations per clock cycle. How many gates do 1,000 sixteen-bit multipliers take? And 1,000 eight-bit ones? Express the difference as a ratio.
4. Modify `trimmed_multiplier` to build a 5 x 5 multiplier and check it on all 1,024 pairs. Does its gate count match `6N^2 - 8N`?
5. Harder: a multiplier that is used only once every 8 cycles can be replaced by a "shift-and-add" circuit: one N-bit adder, a few registers and a counter, adding one partial product per cycle. Estimate its area for N = 8 in our model (adder 40 gates, three 8-bit registers at 6 gates per bit, plus about 20 gates of control) and compare it with the 344-gate array multiplier. What did you pay in time?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Partial product | "one row of the multiplication" | `a AND b_j`, shifted by `j`: a copy of the multiplicand or zero |
| Array multiplier | "the simple multiplier" | N^2 AND gates and N - 1 rows of adders; area about `6N^2` gates |
| Half adder | "a cheap adder" | XOR + AND: adds two bits, used where a full adder's third input is always 0 |
| Wallace / Dadda tree | "the fast multiplier" | Adds all columns in parallel layers of full adders; delay grows with log N |
| Quadratic area | "it blows up" | Doubling the width multiplies the multiplier's area by about 4 |
| Low precision | "INT8, INT4" | Fewer bits per number: much smaller multipliers, more of them per chip |

## Further Reading

- David Money Harris and Sarah L. Harris, *Digital Design and Computer Architecture* (Morgan Kaufmann), chapter 5, "Multiplication".
- John L. Hennessy and David A. Patterson, *Computer Architecture: A Quantitative Approach* (Morgan Kaufmann), appendix J, "Computer Arithmetic" (Booth recoding, Wallace trees).
- Mark Horowitz, "Computing's energy problem (and what we can do about it)", *ISSCC 2014* — the energy-per-operation numbers used in this phase.
- Norman P. Jouppi et al., "In-Datacenter Performance Analysis of a Tensor Processing Unit", *ISCA 2017* — a chip built around tens of thousands of 8-bit multipliers.
