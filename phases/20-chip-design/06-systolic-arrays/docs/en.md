# Systolic Arrays

> Put the weights in a grid and let the data march through it. Each number is fetched once, used by a whole row of MACs, and the edges of the grid do all the talking.

**Type:** Build
**Prerequisites:** Phase 20 (Chip Design), Lessons 03 (The MAC), 04 (Moving Data Costs More) and 05 (Clocks, Critical Paths and Pipelining)
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Systolic array | A grid of identical cells that pass data to their neighbours in step with a clock | A bucket brigade in two directions at once |
| Systolic | From "systole", the beat of the heart: data is pumped through in rhythm | A heartbeat pushing blood along |
| Processing element (PE) | One cell of the grid: here, one MAC plus a few registers | One worker on the line |
| Weight-stationary | A dataflow where each PE holds one weight that stays put while inputs flow past | A stall at a market that stays while customers walk by |
| Partial sum | An incomplete dot product being built up as it passes down a column | A collection tin passed down a row of people |
| Skew | Feeding the rows one cycle apart so that data meets at the right PE at the right time | Runners starting a staggered race |
| Batch | A group of input vectors processed together with the same weights | A tray of cookies baked together |
| Utilization | The fraction of MAC slots that do useful work | How many seats on a bus are filled |
| Fill and drain | The cycles at the start and end when the array is only partly busy | A queue forming and emptying at a ticket office |
| Edge (perimeter) vs area | The array's border grows like N, its number of cells like N^2 | A square field's fence vs its grass |

## Learning Objectives

- Explain how a weight-stationary systolic array computes a matrix product by passing inputs right and partial sums down.
- Simulate such an array cycle by cycle and check its output against `numpy`.
- Compute the number of cycles, the utilization, and how they depend on the batch size (fill and drain).
- Show that the arithmetic grows with the area (N^2) while the data entering and leaving grows only with the edge (2N), so bigger arrays reuse each value more.
- Compare the area of a systolic array with the alternative of feeding every MAC from a shared register file.

## The Problem

Lesson 04 left us with a hard problem. A MAC costs about 0.3 pJ, but fetching its two operands from a large memory costs tens to hundreds of picojoules. And if every MAC fetched its own operands from a shared register file, the file would need two read ports per MAC: for a thousand MACs, two thousand ports, an absurd amount of multiplexers.

We need an arrangement where each number is fetched once and then used by many MACs, without a big multiplexer in between. In 1978, H. T. Kung and Charles Leiserson proposed an elegant answer: the **systolic array**. Instead of bringing every operand to every MAC through a central switchboard, line the MACs up in a grid and let each one hand its data to its neighbour. Data enters at the edges and flows through the grid like blood through the heart's rhythm, getting reused at every step. Forty years later, Google built its first Tensor Processing Unit around a 256 x 256 systolic array of 8-bit MACs.

## The Physics

The physics is the data-movement physics of Lesson 04, turned to our advantage. In a systolic array:

- every wire goes from one PE to its **immediate neighbour**, a few tens of micrometres away. Moving a byte 50 µm costs about `8 * 0.2 pF/mm * 0.05 mm * 0.81 V^2 = 0.065 pJ`, much less than the 0.2 pJ multiply;
- there are **no long buses and no big multiplexers** inside the array: each PE reads its inputs from the registers of its neighbours;
- the only long-distance traffic is at the **edges**: inputs entering on one side, results leaving on another, weights loaded once.

Short wires also help timing: each register-to-register path is just one MAC plus a neighbour hop, so the clock is set by the MAC's own critical path (Lesson 05), not by long cross-chip wires.

## The Concept

### What we compute

A layer applies a weight matrix `W` of size `K x N` (K inputs, N outputs) to a batch of `B` input vectors, stored as the rows of `X` (size `B x K`):

```
Y = X @ W         Y[b][j] = sum over k of X[b][k] * W[k][j]
```

That is `B * K * N` MACs.

### The weight-stationary array

Build a grid of `K` rows and `N` columns of PEs. PE `(k, j)` permanently holds the weight `W[k][j]`. Each cycle, it:

1. receives an input value `x` from its left neighbour (or from the left edge, for column 0),
2. receives a partial sum `p` from the PE above it (or 0, for row 0),
3. computes `p + W[k][j] * x` and passes it down,
4. passes `x` on to its right neighbour.

```
               column 0       column 1       column 2
                  |              |              |
   x[.][0] -->[ W00 ]  -->   [ W01 ]  -->   [ W02 ]  -->     row 0
                  |  p           |  p           |  p
   x[.][1] -->[ W10 ]  -->   [ W11 ]  -->   [ W12 ]  -->     row 1
                  |              |              |
   x[.][2] -->[ W20 ]  -->   [ W21 ]  -->   [ W22 ]  -->     row 2
                  |              |              |
                Y[.][0]        Y[.][1]        Y[.][2]        (results leave at the bottom)
```

An input `X[b][k]` enters row `k` and travels right, meeting every weight of that row, `W[k][0]`, `W[k][1]`, ...: it is **reused N times**, once per column, without being fetched again. A partial sum travels down column `j`, picking up `W[0][j] * X[b][0]`, then `W[1][j] * X[b][1]`, and so on: when it falls out of the bottom, it is the complete dot product `Y[b][j]`.

### Skew: arriving at the right moment

For the partial sum of `(b, j)` to meet `X[b][k]` at PE `(k, j)`, the timing must line up. The partial sum reaches row `k` one cycle later than row `k - 1`. So the inputs of row `k` must enter one cycle later than those of row `k - 1`: the input matrix is fed in **skewed**, like a staircase. With that skew, `X[b][k]` sits at PE `(k, j)` at cycle

```
t = b + k + j
```

"input vector b, entering row k, after travelling j columns". Here is the trace of a 3 x 3 array with a batch of 4 (`xbk` means `X[b][k]`, `.` means the PE is idle), printed row by row:

```
cycle 0: x00  .   .   |   .   .   .   |   .   .   .
cycle 1: x10 x00  .   |  x01  .   .   |   .   .   .
cycle 2: x20 x10 x00  |  x11 x01  .   |  x02  .   .
cycle 3: x30 x20 x10  |  x21 x11 x01  |  x12 x02  .
cycle 4:  .  x30 x20  |  x31 x21 x11  |  x22 x12 x02
cycle 5:  .   .  x30  |   .  x31 x21  |  x32 x22 x12
```

You can see the diagonal wave: at cycle 2, PE `(0, 2)` works on input 0 while PE `(0, 0)` already works on input 2. Result `Y[b][j]` leaves the bottom of column `j` at cycle `b + (K - 1) + j`. The last one, `Y[B-1][N-1]`, leaves at cycle `B + K + N - 3`, so the whole product takes

```
cycles = B + K + N - 2
```

### Utilization: fill and drain

The array has `K * N` MACs, so in `cycles` it could do `cycles * K * N` MACs. It actually does `B * K * N` useful ones. The **utilization** is

```
utilization = B * K * N / ((B + K + N - 2) * K * N) = B / (B + K + N - 2)
```

For a 16 x 16 array:

| Batch B | Cycles | Utilization |
|---|---|---|
| 1 | 31 | 3.2% |
| 16 | 46 | 34.8% |
| 64 | 94 | 68.1% |
| 256 | 286 | 89.5% |
| 1024 | 1054 | 97.2% |

With a single input vector the array is almost entirely idle: the wave of data passes through it once and most PEs only ever see it for one cycle. With a large batch the fill and drain cycles are shared by many inputs. This is our first hardware reason why batching matters; Lesson 08 gives the memory reason.

(Loading the weights also takes time: shifting `K` rows of weights in takes about `K` cycles, which a real array hides by loading the next weights while computing with the current ones.)

### Area grows like N^2, edges like N

An `N x N` array does `N^2` MACs per cycle. How many values cross its border per cycle? `N` inputs enter on the left and `N` results leave at the bottom: `2N`. So the number of MACs per value moved is

```
N^2 / (2N) = N / 2
```

| N | MACs per cycle | Values in + out per cycle | MACs per value moved |
|---|---|---|---|
| 4 | 16 | 8 | 2 |
| 16 | 256 | 32 | 8 |
| 64 | 4,096 | 128 | 32 |
| 256 | 65,536 | 512 | 128 |

A bigger array is not only more arithmetic; it is **more reuse** of every value that crosses its border. That is exactly what Lesson 04 asked for. It is the same geometry as a square field: double the side and you get four times the grass but only twice the fence.

### Area and throughput in the cost model

Each PE is an 8-bit MAC (608 gates in `sim.cost`), so an `N x N` array is `608 N^2` gates. Its clock is set by one MAC's path, 91 gate delays (549 MHz) if the MAC is not pipelined:

| Array | Area | MACs per cycle | Peak at 549 MHz |
|---|---|---|---|
| 8 x 8 | 0.04 M gates | 64 | 0.04 TMAC/s |
| 32 x 32 | 0.62 M gates | 1,024 | 0.56 TMAC/s |
| 128 x 128 | 9.96 M gates | 16,384 | 9.0 TMAC/s |
| 256 x 256 | 39.85 M gates | 65,536 | 36 TMAC/s |

Compare with feeding 1,024 MACs from one shared register file of 256 entries: 2,048 read ports of 255 2:1 multiplexers of 8 bits each is about 12.5 million gates, **twenty times the whole 32 x 32 systolic array**, before counting the impossible wiring. The systolic array avoids the switchboard entirely.

### Other dataflows

Weight-stationary is one choice. In an **output-stationary** array each PE keeps its own accumulator `Y[b][j]` and both inputs and weights flow past it; in **input-stationary** arrays the inputs stay. Which is best depends on which operand is reused most and is most expensive to move. Accelerator papers spend a lot of effort on this choice.

## Build It

Run:

```
uv run python phases/20-chip-design/06-systolic-arrays/code/main.py
```

### Step 1: The cycle-by-cycle simulator

```python
def systolic_matmul(x, w, trace_cycles=0):
    batch, k_dim = x.shape
    _, n_dim = w.shape
    x_reg = np.zeros((k_dim, n_dim), dtype=np.int64)
    p_reg = np.zeros((k_dim, n_dim), dtype=np.int64)
    y = np.zeros((batch, n_dim), dtype=np.int64)
    cycles = batch + k_dim + n_dim - 2
    ...
    for t in range(cycles):
        new_x = np.zeros_like(x_reg)
        new_p = np.zeros_like(p_reg)
        for k in range(k_dim):
            for j in range(n_dim):
                if j == 0:
                    b = t - k
                    x_in = x[b, k] if 0 <= b < batch else 0
                else:
                    x_in = x_reg[k, j - 1]
                p_in = p_reg[k - 1, j] if k > 0 else 0
                new_x[k, j] = x_in
                new_p[k, j] = p_in + w[k, j] * x_in
        x_reg, p_reg = new_x, new_p
        for j in range(n_dim):
            b = t - (k_dim - 1) - j
            if 0 <= b < batch:
                y[b, j] = p_reg[k_dim - 1, j]
```

`x_reg` and `p_reg` are the registers inside every PE. Each cycle computes all the new register values from the old ones (`new_x`, `new_p`) and then swaps them in, which is exactly how a clock edge updates every register at once. Column 0 takes its input from the skewed left edge (`b = t - k`); other columns take it from their left neighbour's register. The bottom row's partial sums are the outputs. For the 3 x 3 example the result equals `x @ w`, in 8 cycles (`4 + 3 + 3 - 2`).

### Step 2: A bigger check

A 16 x 16 array, batch 64, random 8-bit numbers: equal to numpy, 94 cycles, 16,384 useful MACs and 68.1% utilization, matching `B / (B + K + N - 2) = 64 / 94`.

### Step 3: Utilization versus batch

The formula for 1 to 1024 inputs (the table above).

### Step 4: Area versus edge

`N^2` against `2N` for N from 4 to 256.

### Step 5: sim.cost

```python
array = cost.systolic_array(n, n, 8)
d = cost.Design(f"{n}x{n}")
d.add("ARRAY", array, "in", "out")
peak = d.throughput() * d.max_clock_mhz() * 1e6
```

`throughput()` is the number of MACs per cycle (`rows * cols`); times the clock it gives MACs per second.

### Step 6: The shared register file alternative

A 256-entry register file with two read ports per MAC: 0.80 M gates for 64 MACs, 12.55 M gates for 1,024 MACs, against 0.04 and 0.62 M gates for the corresponding systolic arrays.

## Use It

- **Google TPU v1 (2015).** A 256 x 256 weight-stationary systolic array of 8-bit MACs with 32-bit accumulators at 700 MHz: `65,536 * 0.7e9 * 2 = 92` trillion operations per second, fed by a 24 MB on-chip buffer. Later TPUs use several 128 x 128 arrays with floating-point formats.
- **GPU tensor cores** are small matrix engines (each multiplies small tiles per cycle) inside each streaming multiprocessor; not systolic in the classic sense, but built on the same principle of reusing operands across many MACs with short wires.
- **Apple, Tesla, Amazon and many startups** build neural engines around 2-D MAC arrays with local buffers, choosing different dataflows (weight-, output- or row-stationary).
- **Beyond AI.** Kung and Leiserson originally proposed systolic arrays for matrix operations and signal processing; similar structures appear in error-correction decoders and DNA sequence alignment hardware.

## Common Mistakes

- **Expecting full speed for one input.** A big array processing one vector at a time is mostly idle (3.2% for 16 x 16). Systolic arrays need batches, or long sequences, to be efficient.
- **Forgetting the skew.** If all rows are fed at the same time, partial sums meet the wrong inputs and the result is wrong.
- **Ignoring weight loading.** Weights must be shifted in before use; if they change for every small batch, loading time and energy eat the benefit.
- **Thinking the edges are free.** The edge bandwidth still has to come from somewhere (an on-chip buffer, Lesson 07). A huge array with a starved edge is idle.
- **Assuming one shape fits every matrix.** A 256 x 256 array multiplying a 100 x 100 matrix wastes most of its cells; real compilers tile and pad matrices to the array's shape.

## Exercises

1. A 32 x 32 array processes a batch of 96 inputs with a 32 x 32 weight matrix. How many cycles does it take, and what is the utilization?
2. What batch size gives a 128 x 128 array a utilization of at least 90%?
3. At cycle 7 in a 4 x 4 array, which input `X[b][k]` sits in PE `(2, 3)`? (Use `t = b + k + j`.)
4. In the script, run `systolic_matmul` with a weight matrix that is not square (for example `K = 8`, `N = 4`) and check it against numpy. Does the cycle formula still hold?
5. Harder: modify the simulator into an output-stationary array, where PE `(b, j)` keeps an accumulator for `Y[b][j]`, inputs `X[b][k]` flow right along row `b` and weights `W[k][j]` flow down column `j`, both skewed. Verify it against numpy and compare how many values enter the array per cycle with the weight-stationary version.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Systolic array | "a MAC grid" | A grid of PEs passing data only to neighbours in lockstep with the clock |
| Weight-stationary | "weights stay put" | Each PE holds a weight; inputs flow across rows, partial sums down columns |
| Skew | "staggered inputs" | Delaying row k by k cycles so data and partial sums meet in the right PE |
| Utilization | "how busy it is" | Useful MACs divided by available MAC slots; `B / (B + K + N - 2)` here |
| Fill and drain | "pipeline bubbles" | The partly idle cycles while the data wave enters and leaves the array |
| Reuse per value | "arithmetic per byte at the edge" | `N^2 / 2N = N / 2` MACs for every value that crosses the border |

## Further Reading

- H. T. Kung, "Why Systolic Architectures?", *IEEE Computer*, 1982 — the classic, readable introduction.
- Norman P. Jouppi et al., "In-Datacenter Performance Analysis of a Tensor Processing Unit", *ISCA 2017*.
- Vivienne Sze, Yu-Hsin Chen, Tien-Ju Yang and Joel Emer, *Efficient Processing of Deep Neural Networks* (Morgan & Claypool, 2020), chapter on dataflows (weight-, output- and row-stationary).
- John L. Hennessy and David A. Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed., chapter 7, "Domain-Specific Architectures".
