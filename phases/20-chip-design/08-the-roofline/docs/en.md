# The Roofline

> A chip has two speed limits, one for arithmetic and one for memory. Which one you hit depends on how many operations you do per byte you fetch.

**Type:** Build
**Prerequisites:** Phase 20 (Chip Design), Lessons 03 (The MAC), 04 (Moving Data Costs More), 06 (Systolic Arrays) and 07 (Memory on the Chip)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| FLOP/s | Floating-point operations per second; TFLOP/s = 10^12 per second | Dishes a kitchen can cook per hour |
| Peak compute | The most operations per second the chip's arithmetic can do | The kitchen's cooking speed with every stove on |
| Memory bandwidth | The most bytes per second the memory can deliver (TB/s = 10^12 bytes per second) | How fast the delivery van brings ingredients |
| Arithmetic intensity | Operations done per byte moved from memory (FLOP per byte) | Dishes cooked per kilogram of ingredients delivered |
| Roofline | A graph of attainable speed versus intensity: a slanted line (memory limit) meeting a flat line (compute limit) | A road that climbs a hill and then runs along a flat ridge |
| Ridge point | The intensity where the two limits meet: `peak / bandwidth` | The top of the climb |
| Memory-bound | Too few operations per byte: the memory limits the speed | Cooks waiting for the van |
| Compute-bound | Enough operations per byte: the arithmetic limits the speed | The van waits while cooks are busy |
| Batch | Several inputs processed together with the same weights | Cooking for a whole table at once |
| bf16 | A 16-bit floating-point format (2 bytes per number) common in AI | A shorthand that takes half the space |
| KV cache | The stored keys and values of earlier tokens that a language model rereads for every new token | A notebook of everything said so far, reread before each new sentence |
| Prefill / decode | Processing a whole prompt at once / generating one token at a time | Reading a letter / writing the reply word by word |

## Learning Objectives

- Draw the roofline of a chip from its peak compute and its memory bandwidth, and compute its ridge point.
- Compute the arithmetic intensity of vector operations, matrix-vector products and matrix-matrix products.
- Show that a layer's intensity grows with the batch size, and find the batch that makes it compute-bound.
- Explain why a bigger batch raises throughput but also raises the time per step (latency), and choose a batch under a latency cap.
- Explain why generating text one token at a time is memory-bound, and why attention over a KV cache does not benefit from batching in the same way.

## The Problem

A vendor sells you a chip that "does 400 TFLOP/s". You run a language model on it and measure 2 TFLOP/s: one two-hundredth of the advertised number. Is the chip broken? Is your code bad?

Probably neither. The 400 is the speed of the chip's arithmetic when it has all the numbers it needs. To get those numbers, it reads memory at 2 TB/s. If your computation does only one operation for each byte it reads, the memory can feed only `2e12 bytes/s * 1 FLOP/byte = 2e12 FLOP/s`. The arithmetic spends 99.5% of its time waiting.

The **roofline model** (Samuel Williams, Andrew Waterman and David Patterson, 2009) turns this into a picture: one graph that tells you, for any computation, which speed limit applies and how fast you can possibly go. It is the most useful single tool for reasoning about AI hardware, and it explains why AI serving systems work so hard to batch requests together.

## The Physics

The two limits are physical. **Peak compute** is the number of MACs on the chip times the clock frequency times 2 (each MAC is two operations): it is set by area and by how fast the critical path allows the clock to tick (Lessons 03-06). **Memory bandwidth** is set by how many wires leave the chip towards DRAM or HBM, how fast each wire can toggle, and how much energy we are willing to spend per bit (Lessons 04 and 07). An HBM stack connects through about a thousand wires on a silicon interposer, each running at several gigabits per second, giving hundreds of GB/s to over 1 TB/s per stack.

Crucially, the two limits grow differently with technology. Adding MACs costs area, which shrinks every process generation. Adding bandwidth costs wires leaving the chip, which are limited by the chip's edge and package and by energy per bit. Over decades, compute has grown much faster than memory bandwidth (sometimes called the "memory wall"), so ridge points keep moving to the right: chips need ever more operations per byte to reach their peak.

## The Concept

### Our chip: THOTH-1

We invent a chip with round numbers:

```
peak compute     P = 400 TFLOP/s  = 400e12 FLOP/s     (bf16)
bandwidth        W = 2 TB/s       = 2e12 bytes/s
```

### Intensity

For a computation, count the floating-point operations `F` and the bytes `Q` it must move from memory. Its **arithmetic intensity** is

```
I = F / Q        (FLOP per byte)
```

### The roofline

The speed you can reach is limited both by the arithmetic and by the memory:

```
attainable = min( P , W * I )
```

"the attainable speed is the smaller of the peak compute and the bandwidth times the intensity". Plotted on log-log axes, `W * I` is a slanted line and `P` a flat roof:

```
 TFLOP/s
   400 |                    ________________________  compute roof (P)
       |                  /
   100 |                /
       |              /    <- memory slope (W * I)
    10 |            /
       |          /
     1 |        /
       +------+--------+---------+---------+------->  intensity (FLOP/byte, log scale)
             1        10       100   200  1000
                                      ^
                                 ridge point
```

They meet at the **ridge point**:

```
I_ridge = P / W = 400e12 / 2e12 = 200 FLOP per byte
```

Left of the ridge: memory-bound. Right of it: compute-bound. Worked values:

| Intensity | W * I | Attainable |
|---|---|---|
| 1 | 2 TFLOP/s | 2 TFLOP/s |
| 10 | 20 | 20 |
| 100 | 200 | 200 |
| 200 | 400 | 400 (the ridge) |
| 1000 | 2000 | 400 (the roof) |

### Intensities of real operations

**Adding two vectors** of `n` bf16 numbers: `n` additions; read `2n` values and write `n`, each 2 bytes: `6n` bytes. `I = n / 6n = 0.17`. Deeply memory-bound: 0.3 TFLOP/s on THOTH-1.

**A layer applied to one input** (matrix-vector, `d x d` weights, `d = 8192`): `2 d^2` FLOPs (a MAC per weight), and the weights alone are `2 d^2` bytes. `I ≈ 1`. Every weight is read from memory to be used exactly once. 2 TFLOP/s.

**A layer applied to a batch of `B` inputs** (matrix-matrix):

```
F = 2 * B * d^2                       (B MACs per weight, 2 FLOPs per MAC)
Q = 2 * (d^2 + B*d + B*d)             (weights, inputs, outputs, 2 bytes each)
I = B * d^2 / (d^2 + 2 B d) = B * d / (d + 2B)
```

For `B` much smaller than `d`, `I ≈ B`: **the intensity is about the batch size**, because each weight fetched is reused once per input (Lesson 04's reuse, now with a name).

### Sweeping the batch

For our 8192 x 8192 layer on THOTH-1, the time of one step is the larger of the compute time `F / P` and the memory time `Q / W` (an accelerator overlaps them, Lesson 07):

| Batch | FLOP/byte | Compute | Memory | Step | Inputs per second | Bound |
|---|---|---|---|---|---|---|
| 1 | 1.0 | 0.3 µs | 67.1 µs | 67.1 µs | 14,898 | memory |
| 32 | 31.8 | 10.7 µs | 67.6 µs | 67.6 µs | 473,141 | memory |
| 128 | 124.1 | 42.9 µs | 69.2 µs | 69.2 µs | 1,849,550 | memory |
| 256 | 240.9 | 85.9 µs | 71.3 µs | 85.9 µs | 2,980,232 | compute |
| 1024 | 819.2 | 343.6 µs | 83.9 µs | 343.6 µs | 2,980,232 | compute |

Read it carefully, because this table is the economics of AI serving:

- **From batch 1 to batch 128, the step time barely changes** (67 to 69 µs): the chip is waiting for the weights anyway, so extra inputs ride along almost for free. Throughput rises 124 times.
- **Past the ridge** (batch about 211 here, where `I` reaches 200), the step time grows in proportion to the batch: throughput stops rising and stays at the roof, about 3 million inputs per second.
- **Latency** is the step time. A user waiting for an answer waits through every step. Batch 1024 gives no more throughput than batch 256 but makes everyone wait four times longer.

So the sweet spot is just past the ridge: compute-bound (no wasted arithmetic) but no further (no wasted latency). For THOTH-1 and this layer, a batch of about 210-256.

### Why generating text is memory-bound

A language model generates one token at a time (**decode**). For each new token, every layer's weights are read once. With one user, the batch is 1 and the intensity is 1: the chip runs at 0.5% of its peak. Serving many users at once, with their tokens batched together, multiplies the reuse of every weight fetched. That is why serving systems batch requests and why the cost per token falls so steeply with the number of simultaneous users.

There is a catch: **attention**. To generate a token, each sequence also reads its own **KV cache**, the stored keys and values of all its earlier tokens. For a context of 4,096 tokens and 8,192 values per token (keys and values, 2 bytes each), that is `2 * 4096 * 8192 * 2 = 134 MB` per sequence, used for about `4 * 4096 * 8192` FLOPs: intensity about 1, no matter how many sequences are batched, because each sequence's cache is different and is used by only that sequence. Batching helps the weight matrices but not the attention reads. This is one reason long contexts are expensive to serve, and why techniques that shrink the KV cache (sharing keys and values across heads, compressing or quantizing the cache) matter so much.

During **prefill** (processing the user's whole prompt at once), the many prompt tokens act like a batch: intensity is high and the chip is compute-bound. Decode is the memory-bound phase.

## Build It

Run:

```
uv run python phases/20-chip-design/08-the-roofline/code/main.py
```

### Step 1: The roofline function

```python
def attainable(intensity):
    return np.minimum(PEAK_FLOPS, BANDWIDTH * np.asarray(intensity, dtype=float))
```

One line: the smaller of the two limits. The script prints the ridge point (200 FLOP/byte) and the attainable speed at a few intensities.

### Step 2: Intensities

```python
def matmul_counts(batch, d_in, d_out):
    flops = 2 * batch * d_in * d_out
    moved = BYTES_PER_VALUE * (d_in * d_out + batch * d_in + batch * d_out)
    return flops, moved
```

The script prints six operations: vector add (0.2), matrix-vector (1.0), batch 64 (63.0), batch 1024 (819), a square 8192^3 matrix product (2,731) and attention decode for one sequence (1.0), each with its attainable speed and its bound.

### Step 3: The batch sweep

```python
def layer_step(batch, d=8192):
    flops, moved = matmul_counts(batch, d, d)
    compute_s = flops / PEAK_FLOPS
    memory_s = moved / BANDWIDTH
    return flops / moved, compute_s, memory_s, max(compute_s, memory_s)
```

The table above, from batch 1 to 1024.

### Step 4: The ridge batch

A small loop increases the batch until the compute time reaches the memory time: batch 211, intensity 200.7, step 70.8 µs.

### Step 5: The plot

The script draws the roofline on log-log axes with the six operations as points and saves it as `out.png` next to the script.

### Step 6: The lab

In the lab, the step time is modelled as a design with two parallel branches from `in` to `out`: a fixed "memory" branch 67 units long and a "compute" branch whose length depends on the batch. `sim.cost`'s critical path is the longer of the two branches, which is exactly `max(compute, memory)`: the roofline in one line of the cost model. The script evaluates each batch.

## Use It

- **Real chips.** Recent AI accelerators and GPUs have ridge points of a few hundred FLOP per byte in 16-bit formats (for example around 1,000 TFLOP/s of dense bf16 compute over 3-4 TB/s of HBM gives roughly 250-300). The exact number depends on the format: lower precision raises peak compute but not bandwidth, so the ridge moves right.
- **Profilers.** NVIDIA Nsight Compute and Intel Advisor draw roofline plots for your kernels, placing each one by its measured intensity and speed.
- **Serving systems.** Inference servers use continuous batching to keep many requests in flight, raising intensity for the weight matrices, and cap batch sizes to meet latency targets: the exact trade-off of the table.
- **Model design.** Architectural choices such as grouped-query attention (fewer key/value heads), mixture-of-experts (more weights, but each token touches few) and quantized weights (fewer bytes per weight, so higher intensity) can all be read as moves on the roofline.

## Try It in the Lab

Open "Pick the batch that makes the layer compute-bound". Reading the 8192 x 8192 bf16 layer takes 67 µs on THOTH-1 whatever the batch; computing it takes 0.336 µs per input. One step lasts as long as the slower of the two. Choose a batch that is compute-bound (the step lasts longer than 67 µs) while keeping each step within 120 µs. Before running, compute the compute time for each batch and compare it with 67 µs. Why does the lab make batch 128 fail even though its throughput is already high?

## Common Mistakes

- **Comparing chips by peak FLOP/s alone.** A chip with twice the peak but the same bandwidth is no faster for memory-bound work.
- **Counting FLOPs but not bytes.** Intensity needs both. The same matrix product can have very different intensities depending on tiling and on what fits in on-chip memory.
- **Assuming bigger batches are always better.** Past the ridge, throughput stays flat and latency keeps growing.
- **Forgetting the KV cache.** Batching raises the intensity of weight reads, not of each sequence's own attention reads.
- **Mixing formats.** Peak compute in 8-bit is about twice the 16-bit peak, and data in 8-bit takes half the bytes; recompute the ridge for the format you actually use.

## Exercises

1. A chip has a peak of 1,000 TFLOP/s and 4 TB/s of bandwidth. What is its ridge point? How fast can it run a matrix-vector product with intensity 1?
2. Using `I = B d / (d + 2B)` with `d = 4096`, what batch gives an intensity of 100? Of 200?
3. On THOTH-1, an elementwise operation reads 2 arrays and writes 1, doing 4 FLOPs per element in bf16. What is its intensity and attainable speed?
4. Store the weights in an 8-bit format (1 byte each) but keep the inputs and outputs in bf16. Modify `matmul_counts` and find the new compute-bound batch on THOTH-1. Why does it drop?
5. Harder: a model has 40 layers of 8192 x 8192, and each user sequence has a 4,096-token KV cache of 134 MB per layer. For a batch of 64 users decoding one token each, compute the total bytes read (weights plus KV caches) and FLOPs per step, and place the step on the roofline. What dominates?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Roofline | "the roofline plot" | `attainable = min(peak, bandwidth * intensity)`, drawn on log-log axes |
| Arithmetic intensity | "FLOPs per byte" | Operations performed per byte moved from memory |
| Ridge point | "the knee" | `peak / bandwidth`: the intensity needed to reach peak compute |
| Memory-bound | "bandwidth-limited" | Intensity below the ridge; speed is `bandwidth * intensity` |
| Compute-bound | "FLOP-limited" | Intensity above the ridge; speed is the peak |
| Batching | "more users per step" | Reusing each fetched weight for B inputs, making intensity about B |
| KV cache | "the attention cache" | Per-sequence keys and values reread every decode step; its intensity stays near 1 |

## Further Reading

- Samuel Williams, Andrew Waterman and David Patterson, "Roofline: An Insightful Visual Performance Model for Multicore Architectures", *Communications of the ACM*, 52(4), 2009.
- John L. Hennessy and David A. Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed., chapter 4 and chapter 7 (rooflines of GPUs and domain-specific architectures).
- Dwarkesh Patel's interview with Reiner Pope (MatX) on chip design and the economics of AI inference ([dwarkesh.com](https://www.dwarkesh.com/p/reiner-pope-2)) — a practitioner's view of batching, memory and compute.
- Norman P. Jouppi et al., "In-Datacenter Performance Analysis of a Tensor Processing Unit", *ISCA 2017* — rooflines of a TPU, a GPU and a CPU side by side.
