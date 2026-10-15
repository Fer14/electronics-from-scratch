# The MAC

> Multiply, add, remember, repeat. Almost every AI computation is this one tiny loop, run trillions of times.

**Type:** Build
**Prerequisites:** Phase 20 (Chip Design), Lessons 01 (From Gates to Adders) and 02 (Multiplying in Hardware); Phase 15 (Sequential Logic), Lessons 03 (Flip-Flops and the Clock) and 04 (Registers)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| MAC (multiply-accumulate) | One step that multiplies two numbers and adds the result to a running total | Adding one item's price x quantity to the bill |
| Accumulator | The register that holds the running total between steps | The running total on a till |
| Dot product | Multiply two lists of numbers pair by pair and add everything up | Total cost = sum of price x quantity over all items |
| Matrix | A rectangular table of numbers | A spreadsheet |
| Matrix-vector product | A dot product of every row of a matrix with the same list | Pricing the same shopping list in every shop |
| Weight | A number stored in a neural network that multiplies an input | How much each ingredient counts in a recipe |
| Activation | A number flowing through a network (an input to a layer, or its output) | The ingredients actually put in |
| Overflow | A result too big for the bits that hold it, so it wraps around to a small number | A car odometer rolling from 99999 back to 00000 |
| Wrap-around | What binary counters do on overflow: keep only the lowest bits | A clock going from 12 back to 1 |
| FLOP | One floating-point operation; a MAC counts as two (one multiply, one add) | Counting a "sale" as two actions: scan and add |
| Feedback loop | A circuit whose output comes back as one of its own inputs | A thermostat that reacts to the temperature it caused |

## Learning Objectives

- Explain why a matrix product, and therefore a neural network layer, is made of MAC operations, and count how many MACs a layer needs.
- Work out how many bits an accumulator needs so a dot product can never overflow, and see what goes wrong when it is too narrow.
- Build a clocked MAC from gates (multiplier, adder and accumulator register) with `sim.logic` and run a dot product through it cycle by cycle.
- Break down the area of an 8-bit MAC with `sim.cost` and see how the accumulator width changes it.
- Explain why the MAC contains a feedback loop, and why that matters for clock speed (preparing Lesson 05).

## The Problem

A neural network layer takes a list of numbers (the activations), and for each output it computes a weighted sum: each input times a weight, all added up. That is a dot product. A layer with 4,096 inputs and 4,096 outputs does 4,096 dot products of length 4,096: almost 17 million multiplications and 17 million additions, for a single input. A large language model has dozens of such layers, and it does them for every word it generates.

All of that work is the same small step repeated: multiply two numbers and add the product to a running total. Chip designers call this step a **MAC**, for multiply-accumulate. If you want to know why an AI chip looks the way it does, you need to understand this one block: what it is made of, how big it is, how many bits its total needs, and why it has a loop inside that makes it hard to speed up.

## The Physics

A MAC is three blocks we already know: a multiplier (Lesson 02), an adder (Lesson 01) and a register (Phase 15, Lesson 04). The register is made of D flip-flops, each of which copies its input to its output at the rising edge of the clock and holds it until the next edge.

The physical consequence of a register is **time**. Between two clock edges, the signals must travel from the register's output, through the multiplier's result and the adder, and back to the register's input, and settle there before the next edge (with a small setup margin). If the clock ticks too early, the register captures a half-computed, wrong value. So the time the multiplier plus the adder take sets the fastest clock this MAC can run at. We will spend all of Lesson 05 on this; here we only note that the path exists.

The second physical consequence is **energy**. Each step switches a few hundred gates. With Horowitz's 45 nm numbers, an 8-bit multiply costs about 0.2 pJ and a 32-bit add about 0.1 pJ, so one 8-bit MAC with a 32-bit accumulator is about 0.3 pJ. A chip doing 10^15 such MACs per second (a "petaop" accelerator) would burn 300 W just in arithmetic. That is a real number for today's large accelerators, and it is before we count moving the data, which Lesson 04 shows is even more expensive.

## The Concept

### From a matrix to MACs

A dot product of two lists `w` and `x` of length `K`:

```
y = w[0] * x[0] + w[1] * x[1] + ... + w[K-1] * x[K-1]
```

computed one step at a time:

```
acc = 0
for k in 0 .. K-1:
    acc = acc + w[k] * x[k]        <- one MAC
y = acc
```

Worked example with eight 4-bit numbers (0 to 15). With `w = [15, 10, 10, 14, 9, 12, 13, 3]` and `x = [0, 4, 4, 13, 14, 0, 7, 13]`:

```
acc =   0 + 15 *  0 =   0
acc =   0 + 10 *  4 =  40
acc =  40 + 10 *  4 =  80
acc =  80 + 14 * 13 = 262
acc = 262 +  9 * 14 = 388
acc = 388 + 12 *  0 = 388
acc = 388 + 13 *  7 = 479
acc = 479 +  3 * 13 = 518
```

A matrix-vector product with an `R x K` matrix is `R` dot products of length `K`, so `R * K` MACs. A matrix-matrix product of `R x K` by `K x B` (a batch of `B` input vectors) is `R * K * B` MACs:

| Layer | MACs |
|---|---|
| 512 x 512, one input | 262,144 |
| 4096 x 4096, one input | 16,777,216 |
| 4096 x 4096, batch of 64 inputs | 1,073,741,824 |

People who count in FLOPs count each MAC as 2 (one multiply, one add), so the last line is about 2.1 GFLOP.

### The MAC as hardware

```
         w (8 bits)   x (8 bits)
             |            |
             +---[ 8 x 8 multiplier ]---+  product (16 bits)
                                        |
                                    [ adder ] <------------+
                                        |                  |
                                 sum (24 bits)             |
                                        |                  |
                               [ accumulator register ]    |
                                        |   (24 flip-flops)|
                                        +------------------+  acc (24 bits)
```

Every clock cycle, a new pair `(w, x)` arrives, the multiplier produces their product, the adder adds it to the current `acc`, and at the clock edge the register captures the new total. After `K` cycles, the register holds the dot product.

Notice the arrow going back up: the register's output is one of the adder's inputs. That **feedback loop** is what makes it an accumulator. It is also why you cannot simply chop the adder in half with another register to make the clock faster: the next addition needs the result of this one (Lesson 05).

### How wide must the accumulator be?

Each product of two unsigned 8-bit numbers is at most `255 * 255 = 65,025`, which needs 16 bits. Add `K` of them and the worst case is `K * 65,025`. The number of bits needed to hold a value `V` is `ceil(log2(V + 1))`, "the number of times you can halve it before it drops below 1, rounded up". So:

```
K = 1:      65,025          -> 16 bits
K = 16:     1,040,400       -> 20 bits
K = 256:    16,646,400      -> 24 bits
K = 4096:   266,342,400     -> 28 bits
```

The rule of thumb: **accumulator bits = product bits + log2(number of terms)**. Each doubling of the number of terms needs one more bit. For signed numbers (two's complement, from -128 to 127) the products are at most `128 * 128 = 16,384` in size, and the same rule holds with one sign bit.

This is why accumulators in AI chips are much wider than their inputs: 8-bit multipliers commonly feed 32-bit accumulators, and 16-bit floating-point multipliers feed 32-bit floating-point accumulators. The `sim.cost.mac` builder uses `2 * bits + 8` as its default accumulator width: 24 bits for 8-bit inputs, enough for 256 terms.

### What overflow does

If the accumulator is too narrow, the sum wraps around: only the lowest bits survive. It is like an odometer that rolls over: a 16-bit accumulator can count up to 65,535, and `65,536` reads as `0`. For a length-256 dot product of random 8-bit numbers, the exact answer in our script is 4,352,998:

```
16-bit accumulator:     27,622   (wrong by 4,325,376 = 66 * 65,536)
20-bit accumulator:    158,694   (wrong by 4,194,304 =  4 * 1,048,576)
24-bit accumulator:  4,352,998   (correct)
```

The wrong answers differ from the right one by an exact multiple of `2^bits`: the lost high part. There is no warning; the result is just silently, badly wrong. Some designs instead **saturate** (stick at the maximum value), which is less wrong but still wrong.

### Where the area goes

With `sim.cost`, an 8-bit MAC with a 24-bit accumulator costs

```
multiplier 8 x 8:          8^2 + 5 * 8 * 7 = 344 gates
adder 24 bits:             5 * 24           = 120 gates
accumulator 24 flip-flops: 6 * 24           = 144 gates
total                                       = 608 gates
```

The multiplier is 57% of it. With a 16-bit accumulator the MAC shrinks to 520 gates but overflows after a handful of terms; with 32 bits it grows to 696 gates. The critical path is the multiplier's 42 gate delays plus the adder's `2 * 24 + 1 = 49`: 91 gate delays, 1.82 ns at 20 ps per gate, so at most about 550 MHz for this unpipelined MAC.

Per million gates, you fit about 3,968 four-bit MACs, 1,644 eight-bit MACs or 527 sixteen-bit MACs. The ratio between 8-bit and 4-bit MACs (2.4x) is smaller than between the bare multipliers (4.5x, Lesson 02), because the accumulator does not shrink as much: it still needs 16 bits for 4-bit inputs.

## Build It

Run:

```
uv run python phases/20-chip-design/03-the-mac/code/main.py
```

### Step 1: The loop

The script runs the dot product of eight random 4-bit pairs one MAC at a time and checks it against `np.dot`: both give 518 (the same example as in The Concept).

### Step 2: Counting MACs

Rows x columns x batch, printed for three layers.

### Step 3: Accumulator width

```python
def accumulator_bits(value_bits, terms):
    largest = terms * (2 ** value_bits - 1) ** 2
    return math.ceil(math.log2(largest + 1))
```

The table matches the rule "product bits + log2(terms)": 24 bits for 256 terms of 8-bit inputs.

### Step 4: Overflow

```python
def wrapping_dot(w, x, acc_bits):
    acc = 0
    for wi, xi in zip(w, x):
        acc = (acc + int(wi) * int(xi)) % (2 ** acc_bits)
    return acc
```

`% (2 ** acc_bits)` keeps only the lowest `acc_bits` bits, exactly what a hardware register does when a carry falls off the top.

### Step 5: A real clocked MAC from gates

`build_mac(bits, acc_bits)` builds, inside one `LogicCircuit`, the 4 x 4 array multiplier, a ripple adder as wide as the accumulator, and a register:

```python
    acc_q = [f"acc{k}" for k in range(acc_bits)]
    acc_d = [f"sum{k}" for k in range(acc_bits)]
    carry = "zero"
    for k in range(acc_bits):
        addend = product[k] if k < len(product) else "zero"
        out = f"ac{k + 1}"
        full_adder(lc, acc_q[k], addend, carry, acc_d[k], out, tag=f"acc_fa{k}")
        carry = out
    lc.register("ACC", acc_d, acc_q)
```

The adder adds the register's outputs `acc_q` to the product and feeds `acc_d`, the register's inputs: there is the feedback loop. `run_mac` resets the register to 0 and calls `lc.step(inputs)` once per pair, which is one rising clock edge. After 12 pairs of 4-bit numbers, the 12-bit version holds 787, the exact dot product. The 8-bit version shows 19: 787 wrapped around 256 three times (`787 - 3 * 256 = 19`).

### Step 6: Area breakdown

`sim.cost.mac(8, acc_bits)` for 16, 24 and 32 bits, with the multiplier's share and the critical path (75, 91 and 107 gate delays).

### Step 7: MACs per million gates

`sim.cost.mac(bits)` with its default accumulator for 4, 8 and 16 bits.

### Step 8: The lab

The script tries each MAC in the lab and prints both goals.

## Use It

- **GPUs and "tensor cores".** Modern GPUs contain units that perform a small matrix multiply-accumulate (for example a 4 x 4 x 4 block) per clock: dozens of MACs wired together, with low-precision inputs and higher-precision accumulators.
- **TPUs and systolic arrays.** Google's first TPU had a 256 x 256 grid of 8-bit MACs (65,536 of them) with 32-bit accumulators (Lesson 06).
- **DSP chips** for audio and radio have offered single-cycle MAC instructions since the 1980s, with accumulators that include extra "guard bits" for exactly the overflow reason above (for example 40-bit accumulators for 16 x 16 products).
- **Microcontrollers.** ARM Cortex-M4 cores have MAC instructions (`SMLAL`, 32 x 32 + 64) for filters and control loops (Phase 19, Lesson 07).
- **Fused multiply-add (FMA)** in floating point does `a * b + c` with a single rounding at the end, which is both faster and more accurate than a separate multiply and add; every modern CPU and GPU has it.

## Try It in the Lab

Open "Size the accumulator". Your MAC multiplies unsigned 8-bit numbers and sums 256 of them. Three MACs are offered, with 16-, 24- and 32-bit accumulators. The accumulator must never overflow, and the MAC must fit in 640 gates. Before running, compute the required width with "product bits + log2(terms)" and the area of each MAC with `344 + 5 * acc_bits + 6 * acc_bits`.

## Common Mistakes

- **Making the accumulator as wide as the inputs.** An 8-bit accumulator for 8-bit inputs overflows on the very first product larger than 255.
- **Sizing for the average instead of the worst case.** Random data may fit in fewer bits most of the time; a hardware accumulator must handle the worst case, or saturate deliberately.
- **Forgetting the loop.** Treating the MAC as a straight pipeline of multiplier then adder misses the feedback from the register to the adder, which limits how it can be pipelined.
- **Counting FLOPs and MACs inconsistently.** A MAC is two operations. Datasheets that quote "TOPS" usually count each MAC as two operations.
- **Ignoring the accumulator in area estimates.** For low-precision inputs, the wide accumulator and its adder can be as big as the multiplier.

## Exercises

1. A dot product has 1,024 terms of unsigned 8-bit numbers. How many bits does the accumulator need?
2. A 12-bit accumulator holds the sum of 4-bit products. What is the largest number of terms that can never overflow? (Each product is at most 225.)
3. Using `sim.cost`'s formulas, compute the area and critical path of a 4-bit MAC with a 16-bit accumulator. Check with `cost.mac(4)`.
4. In the script, run the gate-level MAC with a 10-bit accumulator on the same 12 pairs. Predict the result from the exact 787 before running.
5. Harder: an accumulator could instead be split into two halves: a 12-bit low part updated every cycle and a high part that only counts the carries out of the low part. Sketch the hardware. Why does this shorten the critical path, and what happens to the area?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| MAC | "multiply-accumulate" | `acc = acc + a * b` in one clock cycle: multiplier + adder + accumulator register |
| Accumulator | "the running sum" | A register that feeds back into an adder; it must be wide enough for the worst-case total |
| Accumulator width | "guard bits" | Product bits + log2(number of terms) to never overflow |
| Overflow | "it wrapped" | The total exceeds the register, the top bits are lost and the result is wrong by a multiple of `2^bits` |
| Dot product | "a weighted sum" | Sum of products of two lists; one output of a layer |
| Feedback loop | "the accumulate path" | The register output feeding the adder input; it cannot be split by extra registers without changing the result |

## Further Reading

- David Money Harris and Sarah L. Harris, *Digital Design and Computer Architecture* (Morgan Kaufmann), chapters 3 (sequential logic) and 5 (arithmetic).
- Norman P. Jouppi et al., "In-Datacenter Performance Analysis of a Tensor Processing Unit", *ISCA 2017* — a 65,536-MAC chip.
- Mark Horowitz, "Computing's energy problem (and what we can do about it)", *ISSCC 2014* — energy per add and multiply.
- Vivienne Sze, Yu-Hsin Chen, Tien-Ju Yang and Joel Emer, *Efficient Processing of Deep Neural Networks* (Morgan & Claypool, 2020) — how accelerators are built around MACs.
