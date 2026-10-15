# CPU, GPU and Accelerators

> Every chip spends the same silicon on different bets. A CPU bets on doing anything fast, a GPU on doing thousands of similar things, an accelerator on doing one thing (matrix products) as cheaply as possible.

**Type:** Build
**Prerequisites:** Phase 20 (Chip Design), Lessons 02-08; Phase 16 (A Computer from Gates); Phase 14 (Digital Logic), Lesson 02 (Binary Numbers)
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| CPU | Central processing unit: a few powerful cores that run any program, one instruction stream each, as fast as possible | A small team of brilliant generalists |
| GPU | Graphics processing unit: thousands of simple lanes running the same program on different data | A stadium crowd doing the same card trick at once |
| Accelerator | A chip specialised for one kind of work, here matrix products | A machine that only makes bottle caps, very fast |
| Out-of-order execution | A CPU running later instructions early when their inputs are ready, then putting results back in order | A chef starting the dessert while the oven heats |
| Branch prediction | Guessing which way an `if` will go so the pipeline keeps working before the answer is known | Setting the table before guests confirm they are coming |
| SIMD / SIMT | One instruction applied to many data items at once (single instruction, multiple data / threads) | One drill sergeant, a whole platoon moving |
| Floating point | Numbers stored as sign, exponent and mantissa, like scientific notation in binary | Writing 6.02 x 10^23 instead of all the digits |
| Mantissa | The significant digits of a floating-point number | The "6.02" part |
| Exponent | The power of two that scales the mantissa | The "10^23" part |
| bf16 / fp16 / fp8 / fp4 | Floating-point formats with 16, 8 or 4 bits, trading precision for size | Rounding prices to the euro, to the tenner, to the hundred |
| int8 | 8-bit integers (-128 to 127), usually with a scale factor | Counting in whole boxes of a known size |
| Quantization | Rounding numbers to a coarser format | Rounding a bill |
| Scale factor | A number that stretches values to use a format's range well before rounding | Choosing whether to measure in metres or millimetres |
| SNR (signal-to-noise ratio) | How much bigger the true signal is than the rounding error, in decibels | How much louder the voice is than the hiss |
| Outlier | A rare value much larger than the typical ones | One giant in a crowd of children |

## Learning Objectives

- Describe where a CPU core, a GPU multiprocessor and a matrix accelerator spend their area, and why.
- Count arithmetic per area for each with `sim.cost`, and see the trade between generality and efficiency.
- Explain floating-point formats (fp32, fp16, bf16, fp8 E4M3 and E5M2, fp4 E2M1) and integer formats by their bits, range and precision.
- Quantize weights to each format, measure the error, and see why scale factors and outliers matter.
- Explain why multiplier area grows with the square of the mantissa, and why accumulators stay wide.

## The Problem

Three chips can each multiply matrices. A laptop CPU does a few hundred billion multiply-adds per second. A gaming GPU does tens of trillions. A data-centre accelerator does hundreds of trillions. All three are made of the same kind of transistors in similar processes. Where does a factor of a thousand come from?

It comes from **how they spend their area**. A CPU spends most of its silicon on making one stream of arbitrary instructions run fast: caches, branch predictors, out-of-order machinery. A GPU spends it on huge register files and many simple lanes. An accelerator spends it on a grid of MACs and the memory that feeds them, and almost nothing on control. And all of them now play with **number formats**: the fewer bits per number, the more multipliers fit (Lesson 02) and the fewer bytes must be moved (Lesson 04). This lesson puts those bets side by side.

## The Physics

Two facts from earlier lessons do all the work here:

1. **Multiplier area grows with the square of the width** (Lesson 02). For floating point, the expensive part is the mantissa multiplier. Halving the mantissa width makes it about four times smaller.
2. **Moving data costs more than computing** (Lesson 04). A format with half the bits halves the bytes moved and roughly halves the energy of every memory access.

The one new piece is floating point itself. A floating-point number is

```
value = (-1)^sign * 1.mantissa * 2^(exponent - bias)
```

"a sign, times one-point-something, times a power of two". The exponent bits set the **range** (how big and how small the numbers can be); the mantissa bits set the **precision** (how finely numbers are spaced relative to their size). With `m` mantissa bits, neighbouring numbers differ by a relative step of `2^-m`: with 7 bits (bf16) about 0.8%, with 3 bits (fp8 E4M3) 12.5%, with 1 bit (fp4) 50%.

## The Concept

### Three ways to spend a chip

We sketch each chip with `sim.cost` blocks. The sizes are illustrative, chosen to show the proportions, not to describe a particular product.

**A CPU core.** Four 64-bit multipliers and adders, a big multi-ported register file (180 entries of 64 bits with 8 read ports, for out-of-order execution), 32 KB + 32 KB of L1 cache and 512 KB of L2, and a block of control (branch prediction, decode, reordering) of about 400,000 gates. Total about 5.6 million gates, of which the arithmetic is under 2%. It does 4 multiply-adds per cycle: **0.7 per million gates**. That is not waste: those caches and predictors are what let a CPU run messy, branchy, pointer-chasing code fast.

**A GPU multiprocessor.** 128 lanes of fp32 multiply-add, a 256 KB register file (so thousands of threads can each keep their values close), 128 KB of shared memory and L1, and modest control (the same instruction drives a group of 32 lanes, so the control is shared). Total about 3.8 million gates, 128 multiply-adds per cycle: **34 per million gates**, fifty times the CPU. The register file is the biggest block.

**A matrix accelerator.** A 128 x 128 array of bf16 MACs with fp32 accumulators, a 4 MB on-chip buffer, and almost no control (a sequencer and DMA engines: the compiler decided everything in advance, Lesson 07). Total about 46 million gates, 16,384 multiply-adds per cycle: **358 per million gates**, ten times the GPU and five hundred times the CPU.

```
                 arithmetic   memory (registers, caches, buffers)   control
CPU core            ~2%                    ~91%                       ~7%
GPU SM             ~12%                    ~83%                       ~5%
accelerator        ~26%                    ~73%                     ~0.2%
```

Notice that all three spend most of their area on memory: data movement is the constant. What changes is how much control logic sits between the memory and the arithmetic, and how regular the arithmetic is. Published floorplans tell the same story: in the first TPU, the matrix unit and the 24 MB unified buffer together took more than half the die, and control only about 2% (Jouppi et al., 2017).

### Number formats

| Format | Bits | Exponent | Mantissa | Largest value | Relative step |
|---|---|---|---|---|---|
| fp32 | 32 | 8 | 23 | 3.4 x 10^38 | 1.2 x 10^-7 |
| fp16 | 16 | 5 | 10 | 65,504 | 0.1% |
| bf16 | 16 | 8 | 7 | 3.4 x 10^38 | 0.8% |
| fp8 E5M2 | 8 | 5 | 2 | 57,344 | 25% |
| fp8 E4M3 | 8 | 4 | 3 | 448 | 12.5% |
| fp4 E2M1 | 4 | 2 | 1 | 6 | 50% |
| int8 | 8 | (none) | 7 + sign | 127 x scale | uniform steps |

**bf16** ("brain float", introduced by Google) keeps fp32's 8 exponent bits and cuts the mantissa to 7: the same enormous range as fp32 with coarser precision, so converting from fp32 never overflows. **fp16** has more precision but a much smaller range. The two **fp8** variants trade the other way round: E4M3 for more precision (weights and activations), E5M2 for more range (gradients in training). **fp4 E2M1** can represent only the values 0, 0.5, 1, 1.5, 2, 3, 4 and 6 (and their negatives): almost nothing, so it only works with careful scaling of small groups of values.

### Rounding weights: precision and scaling

Take 20,000 weights drawn from a bell curve with standard deviation 0.02 (typical of a trained layer) and round them to each format. The SNR in decibels is `10 * log10(signal power / error power)`: every 6 dB is about one more bit of accuracy.

| Format | SNR as is | SNR with a per-tensor scale |
|---|---|---|
| fp16 | 73.6 dB | 73.7 dB |
| bf16 | 55.7 dB | 55.6 dB |
| fp8 E5M2 | 25.6 dB | 25.6 dB |
| fp8 E4M3 | 29.6 dB | 31.5 dB |
| fp4 E2M1 | 0.0 dB | 18.4 dB |
| int8 (scaled) | | 41.2 dB |
| int4 (scaled) | | 16.0 dB |

Three lessons in this table:

- **Precision follows the mantissa.** bf16's 7 mantissa bits give about 18 dB less than fp16's 10 (3 bits times 6 dB).
- **Small formats need scale factors.** Rounded "as is", every weight of 0.02 falls below fp4's smallest step of 0.5 and becomes zero: SNR 0 dB, the layer is erased. Multiplying the weights by a scale factor first (so that the largest weight lands on the format's largest value), rounding, and dividing back recovers 18 dB. Real systems keep one scale per tensor, per row, or per small block of 16-32 values ("microscaling").
- **For bell-shaped data, integers do well.** int8 with a scale beats fp8 by 10 dB here, because its 256 levels are spread evenly over the range where the values are.

### Outliers change the picture

Activations inside large models often have rare, huge values. Make 1 in 200 values 50 times larger and quantize again:

```
fp8 E4M3, scaled:  SNR 31.5 dB overall, 32.1 dB on the ordinary values
int8, scaled:      SNR 21.0 dB overall,  9.2 dB on the ordinary values
```

With int8, the scale must stretch to fit the outliers, so the ordinary values are squeezed into a few levels near zero and lose most of their information. A floating-point format spends its bits relative to each value's size, so small and large values both keep about the same relative precision. This is why fp8 formats became popular for AI: they tolerate the messy distributions of real activations.

### Multiplier area and arithmetic per area

A floating-point multiplier multiplies the mantissas (with the hidden leading 1, so `m + 1` bits) and adds the exponents. In our model:

```
area = multiplier(m + 1) + adder(exponent bits)
fp32:     multiplier(24) + adder(8) = 3,336 + 40 = 3,376 gates
bf16:     multiplier(8)  + adder(8) =   344 + 40 =   384 gates
fp8 E4M3: multiplier(4)  + adder(4) =    76 + 20 =    96 gates
fp4 E2M1: multiplier(2)  + adder(2) =    14 + 10 =    24 gates
```

Per unit of area, you fit 8.8 times as many bf16 multipliers as fp32, 35 times as many fp8 E4M3 and 141 times as many fp4. The real ratios are smaller (normalisation, rounding and special cases add fixed costs, and the accumulators stay wide) but the direction is why each new generation of AI hardware advertises a lower-precision mode with roughly double the throughput.

### Accumulators stay wide

Low precision is for the *inputs* of a multiply. The *sum* of thousands of products needs much more precision, for the same reason as the accumulator width of Lesson 03: errors pile up. Summing 4,096 products of random numbers:

```
exact               -60.2080
fp32 accumulator    -60.2080   (error 6e-6)
bf16 accumulator    -64.5000   (error 4.3)
```

Once the running total is large, a bf16 accumulator cannot even represent the small products being added (its step at 60 is 0.25 or 0.5), so they are rounded away. That is why tensor cores and systolic arrays multiply in bf16 or fp8 but accumulate in fp32.

## Build It

Run:

```
uv run python phases/20-chip-design/10-cpu-gpu-and-accelerators/code/main.py
```

### Step 1: Three archetypes

```python
def archetype(name, blocks):
    d = cost.Design(name)
    node = "in"
    for i, (label, block) in enumerate(blocks):
        d.add(label, block, node, f"n{i}")
        node = f"n{i}"
    return d
```

Each chip is a list of `sim.cost` blocks (`cost.gates` for lumps of logic of a given area, `cost.sram` for memories). The script prints the total area, the multiply-adds per cycle and per million gates, and each block's share.

### Step 2: The formats

The dictionary `FORMATS` holds exponent bits, mantissa bits and the largest value of each format; the script prints the bit layout and the relative step `2^-m`.

### Step 3: Quantizing

```python
def quantize_float(x, exp_bits, man_bits, max_value):
    bias = 2 ** (exp_bits - 1) - 1
    min_exp = 1 - bias
    x = np.clip(np.asarray(x, dtype=np.float64), -max_value, max_value)
    mag = np.abs(x)
    exponent = np.floor(np.log2(np.where(mag > 0, mag, 1.0)))
    exponent = np.maximum(exponent, min_exp)
    step = 2.0 ** (exponent - man_bits)
    return np.clip(np.round(x / step) * step, -max_value, max_value)
```

For each value, find its power-of-two exponent (never below the format's minimum, which gives the "subnormal" numbers near zero), compute the spacing of representable numbers at that exponent, round to the nearest multiple and clip to the largest value. `quantize_int` does the same with a uniform step `max / 127`. Step 3b repeats the comparison with outliers.

### Step 4: Multiplier areas

`float_multiplier_area(e, m)` is `cost.multiplier(m + 1).area + cost.adder(e).area`.

### Step 5: Accumulators

The script sums 4,096 products with the running total rounded to bf16 after every addition, and compares with an fp32 sum.

## Use It

- **CPUs** add wide SIMD units (AVX-512, ARM SVE) and small matrix engines (Intel AMX, Apple's matrix coprocessor) to win back arithmetic density for AI without giving up generality.
- **GPUs** contain both general lanes (for graphics and arbitrary kernels) and tensor cores (for matrix multiply-accumulate in fp16, bf16, fp8 and recently fp4), whose peak throughput is many times that of the general lanes.
- **Accelerators** (TPUs, Trainium, many startups' chips) put almost all their logic into MAC arrays and on-chip SRAM, with compilers scheduling every transfer.
- **Formats in practice.** Training commonly uses bf16 with fp32 accumulation and master weights; inference often uses int8 or fp8, and increasingly 4-bit weights with per-block scale factors (the OCP "MX" microscaling formats standardise blocks of 32 values sharing one scale).
- **Phones** run neural networks on dedicated "neural engines" next to the CPU and GPU for exactly the energy reasons of Lesson 04.

## Common Mistakes

- **Comparing peak TOPS across formats.** "2,000 TOPS in fp4" and "500 TFLOP/s in bf16" may be the same hardware; always ask which format.
- **Quantizing without scaling.** Small formats have tiny ranges; values must be scaled into range first, or they vanish (fp4 as is: 0 dB).
- **Ignoring outliers.** A single huge activation can ruin an int8 tensor's precision for every other value.
- **Accumulating in low precision.** Sums of many products need a wide accumulator (fp32 or wide integers).
- **Thinking a CPU's control logic is waste.** It is what makes general code fast. Accelerators get their density by refusing to run general code.

## Exercises

1. List all positive values of fp4 E2M1 (bias 1, exponent bits 2, mantissa bit 1, including the subnormal 0.5). Check that the largest is 6.
2. What is the relative step of a format with 5 mantissa bits? Roughly how many dB of SNR should it give compared with bf16?
3. Using the formula `multiplier(m + 1) + adder(e)`, compute the area of an fp16 multiplier and of an fp8 E5M2 multiplier. How many E5M2 multipliers fit in the area of one fp16 multiplier?
4. In the script, quantize the weights to fp4 E2M1 with a separate scale for each block of 32 weights instead of one per tensor. How much SNR do you gain?
5. Harder: change Step 5 to accumulate in fp16 instead of bf16. Is the error smaller? Then accumulate in bf16 but in 64 partial sums of 64 products each (each partial sum also in bf16), adding the partial sums at the end. Explain the result using the step size at the size of the running total.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| CPU | "the processor" | Few complex cores optimised for single-stream latency, mostly caches and control |
| GPU | "the graphics card" | Many simple lanes running the same instructions, with huge register files |
| Accelerator | "an AI chip" | MAC arrays plus on-chip memory with minimal control, scheduled by a compiler |
| Mantissa / exponent | "the digits and the scale" | Precision bits and range bits of a floating-point number |
| bf16 | "brain float" | 16 bits: fp32's 8-bit exponent with a 7-bit mantissa |
| fp8 E4M3 / E5M2 | "8-bit floats" | 4 or 5 exponent bits and 3 or 2 mantissa bits; precision vs range |
| Quantization | "making the model smaller" | Rounding to a coarser format, usually with scale factors per tensor, row or block |
| Wide accumulation | "accumulate in fp32" | Summing low-precision products in a high-precision register to avoid losing small terms |

## Further Reading

- John L. Hennessy and David A. Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed., chapters 3 (CPUs), 4 (GPUs and SIMD) and 7 (domain-specific architectures).
- Norman P. Jouppi et al., "In-Datacenter Performance Analysis of a Tensor Processing Unit", *ISCA 2017* — floorplan and area breakdown of an accelerator.
- Paulius Micikevicius et al., "FP8 Formats for Deep Learning" (2022) — the E4M3 and E5M2 formats.
- Open Compute Project, *OCP Microscaling Formats (MX) Specification v1.0* (2023) — block-scaled fp8, fp6 and fp4.
