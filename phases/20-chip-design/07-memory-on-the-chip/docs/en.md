# Memory on the Chip

> Small memories are fast and cheap per access; big memories are dense and slow. A chip is a careful stack of both, and the order you touch data decides which one you pay for.

**Type:** Build
**Prerequisites:** Phase 20 (Chip Design), Lessons 04 (Moving Data Costs More) and 06 (Systolic Arrays); Phase 16 (A Computer from Gates), Lesson 03 (Memory); Phase 07 (Capacitors), Lesson 01 (Storing Charge)
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Memory hierarchy | Several layers of memory, from tiny and fast to huge and slow | Desk, bookshelf, library, warehouse |
| SRAM cell | A bit stored in a little loop of two inverters plus two access transistors (6 transistors) | A light switch that stays where you put it |
| DRAM cell | A bit stored as charge on a tiny capacitor behind one transistor; it leaks and must be refreshed | A leaky bucket you must top up regularly |
| Refresh | Reading and rewriting every DRAM row every few tens of milliseconds before the charge leaks away | Re-inflating a slowly leaking tyre |
| Latency | Time from asking for a value to receiving it | Waiting time at a restaurant |
| Bandwidth | How many bytes per second a memory can deliver | How many plates the kitchen sends out per minute |
| Cache | A small memory that automatically keeps copies of recently used data, managed by hardware | A desk that a helper keeps stocked with the books you used lately |
| Hit / miss | The data is (hit) or is not (miss) already in the cache | The book is on your desk, or you walk to the library |
| LRU | "Least recently used": when the cache is full, throw out what was used longest ago | Clearing the desk of the book you have not opened for longest |
| Scratchpad | A small memory that software fills and empties explicitly | A desk where you yourself decide what to bring and when |
| DMA | Direct memory access: a little engine that copies blocks of data between memories while the processor computes | A courier who fetches the next box while you work |
| Double buffering | Using two buffers: compute on one while the other is being filled | Eating from one plate while the next is being served |
| Tiling | Cutting a big matrix into blocks that fit the fast memory, and finishing all work on a block before moving on | Reading a big map one page at a time |
| Deterministic latency | Every access takes a known, fixed time | A train that always leaves at 8:00 sharp |

## Learning Objectives

- Describe the memory hierarchy of a modern chip (registers, SRAM, HBM/DRAM) with orders of magnitude for size, latency and energy per bit.
- Explain physically why SRAM is fast but bulky and DRAM is dense but slow and must be refreshed.
- Simulate a hardware-managed LRU cache on a matrix workload and see how the access order (naive or tiled) changes the hit rate from 0% to over 90%.
- Compare a cache with a software-managed scratchpad with double buffering, and explain why accelerators like deterministic latency.
- Split a fixed area budget between a MAC array and its buffer, and see why too little buffer starves a big array.

## The Problem

Lesson 06 built a beautiful systolic array: 64 MACs per cycle for an 8 x 8 grid, 65,536 for 256 x 256. But the array's edge must be fed: inputs on one side, weights loaded in, results taken away. Where do those numbers come from, and how fast can they arrive?

The weights of a big neural network take gigabytes. No chip holds that much on its silicon. They live in DRAM, which is dense and cheap but slow (about 100 ns to answer) and expensive per access (Lesson 04). Between the DRAM and the arithmetic, designers place layers of faster, smaller memory. The questions this lesson answers: what are those memories physically, how big should they be, who decides what goes in them (hardware or software), and how much of your area budget should go to memory instead of MACs?

## The Physics

### SRAM: a bit held by feedback

An SRAM cell is two inverters connected in a loop: the output of each feeds the input of the other (Phase 15, Lesson 01, memory from feedback). If one side is 1, the other is 0, and the loop holds that state as long as power is on. Two more transistors connect the two sides to a pair of **bit lines** when the cell's **word line** is raised. Six transistors per bit: fast (the loop actively drives the bit lines) and compatible with ordinary logic manufacturing, so it can sit right next to the MACs. But six transistors is a lot of area per bit.

In our cost model an SRAM bit costs 1 gate of area, against 6 for a flip-flop, which has extra transistors for clocking. So SRAM stores six times more bits per area than registers.

### DRAM: a bit as charge on a capacitor

A DRAM cell is one transistor and one tiny capacitor (about 10-20 fF). A 1 is a charged capacitor, a 0 an empty one (Phase 07, Lesson 01). That is much denser than SRAM, roughly ten times more bits per area, which is why your computer has gigabytes of DRAM and megabytes of SRAM. But:

- **Reading is slow and destructive.** The cell's charge is shared with a long bit line of much larger capacitance, producing a tiny voltage change that a sense amplifier must detect and then write back.
- **It leaks.** The charge drains away through the transistor in milliseconds, so every row must be **refreshed** (read and rewritten) about every 32-64 ms.
- **It is made in a different process.** DRAM capacitors need special manufacturing, so DRAM lives on separate dies: on the board (DDR) or stacked beside the processor (HBM).

### The hierarchy, in orders of magnitude

| Level | Typical size | Latency | Energy per bit | Cell |
|---|---|---|---|---|
| flip-flop registers | a few KB | < 1 ns | about 0.05 pJ | ~20 transistors per bit |
| small SRAM (8-64 KB) | KB | ~1 ns | about 0.2 pJ | 6 transistors |
| big on-chip SRAM | MB to 100+ MB | 5-20 ns | about 1-2 pJ | 6 transistors, longer wires |
| HBM (stacked DRAM) | 16-24 GB per stack | ~100 ns | a few pJ | 1 transistor + 1 capacitor |
| DDR DRAM | GB | ~100 ns | 20-40 pJ | 1T1C, off-package wires |

These are rounded, process-dependent numbers meant to show the shape: each step down the hierarchy is roughly ten times bigger, several times slower and several times more expensive per bit.

## The Concept

### Order matters: a cache on a matrix workload

A **cache** keeps copies of recently used data. When the processor asks for an address, the cache checks whether it has it (a **hit**, fast) or not (a **miss**: fetch from the next level, slow, and keep a copy, throwing out the least recently used line if full). The hardware does all this automatically; the program does not know the cache exists.

Our toy: a cache of 1,024 words with LRU replacement, a hit costing 1 cycle and a miss 100 cycles. The workload reads the weights of a 64 x 64 layer (4,096 words) once for each of 16 input vectors.

**Naive order:** for each input vector, read all 4,096 weights. The weights do not fit in 1,024 words. By the time we come back to weight `(0, 0)` for the next input, it was thrown out 3,072 accesses ago. With LRU this is the worst possible pattern: every single access misses.

```
naive order: 0 hits, 65,536 misses, 0.0% hit rate, 6,553,600 cycles
```

**Tiled order:** cut the weight matrix into 32 x 32 tiles (1,024 words, exactly the cache size). For each tile, process all 16 inputs before moving on. The first input brings the tile in (1,024 misses); the other 15 hit every time.

```
tiled order: 61,440 hits, 4,096 misses, 93.8% hit rate, 471,040 cycles
```

Same data, same cache, same arithmetic: **14 times faster** just by changing the loop order. This is why every high-performance matrix library tiles its loops, and why "the access pattern" is the first thing a performance engineer looks at.

### Hardware cache or software scratchpad?

A cache is convenient: programs run correctly without knowing it exists. But it has costs:

- **Tags and comparators.** For every line the cache stores which address it holds, and checks those tags on every access: extra area and energy.
- **Unpredictable timing.** Whether an access hits depends on everything that happened before. The same code can take very different times.
- **Wasted capacity.** The cache guesses what to keep; it sometimes keeps the wrong things.

Accelerators usually prefer a **scratchpad**: plain SRAM that the software (the compiler) fills explicitly. The compiler knows the whole matrix computation in advance, so it can schedule exactly which tile to load and when. With **double buffering**, a DMA engine loads tile `i + 1` into one half of the buffer while the array computes on tile `i` in the other half:

```
time -->
DMA:      [load T0] [load T1] [load T2] [load T3]
compute:            [comp T0] [comp T1] [comp T2] [comp T3]
```

If loading a tile takes less time than computing on it, the loads are completely hidden. In our toy (8 words per cycle from DRAM), a 32 x 32 tile loads in 128 cycles and takes 16,384 cycles of work, so the whole job takes `128 + 4 * 16,384 = 65,664` cycles, **the same every time**. That determinism lets a compiler predict performance exactly, which matters for chips that run the same model billions of times, and for latency guarantees in serving.

### How much area for memory?

Memory is not free: every SRAM bit costs area that could have been MACs. But MACs without memory starve. Let us split 60,000 gates between an `N x N` array (608 gates per MAC) and an SRAM buffer (1 gate per bit), with a simple model:

- DRAM delivers 2 bytes per cycle.
- The buffer holds one tile of 8-bit weights (`N^2 * 8` bits) plus a batch of input vectors (8 bits each) and their 24-bit partial results: `N * 8 + N * 24` bits per input.
- Each weight fetched from DRAM is reused once per input held, so the array gets `2 * batch` MACs' worth of new weights per cycle. It delivers `min(N^2, 2 * batch)` MACs per cycle.

| Array | Buffer | Area | Fits 60,000? | Batch held | Delivered MACs/cycle |
|---|---|---|---|---|---|
| 4 x 4 | 16 kbit | 26,112 | yes | 127 | 16 (array too small) |
| 8 x 8 | 4 kbit | 43,008 | yes | 14 | 28 (starved) |
| 8 x 8 | 16 kbit | 55,296 | yes | 62 | 64 (full speed) |
| 8 x 8 | 64 kbit | 104,448 | no | 254 | 64 |
| 16 x 16 | 16 kbit | 172,032 | no | 28 | 56 (starved and too big) |

Within the budget, the best choice is the 8 x 8 array with a 16 kbit buffer. With only 4 kbit, the same array delivers less than half its peak, because the buffer cannot hold enough inputs to reuse each weight. Notice that the 16 x 16 array with a 16 kbit buffer would deliver *less* than the 8 x 8 one at full speed: a bigger array with too little memory is a waste of silicon. This trade-off is a real design decision in every accelerator; the ratio of SRAM to MACs varies widely between chips depending on the models they target.

## Build It

Run:

```
uv run python phases/20-chip-design/07-memory-on-the-chip/code/main.py
```

### Step 1: The hierarchy table

The list `HIERARCHY` prints the orders of magnitude from The Physics.

### Step 2: Flip-flops versus SRAM

`cost.register(bits).area` (6 per bit) against `cost.sram(bits).area` (1 per bit): six times denser, for 1, 16 and 256 kbit.

### Step 3: An LRU cache

```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.lines = OrderedDict()
        self.hits = 0
        self.misses = 0

    def access(self, address):
        if address in self.lines:
            self.lines.move_to_end(address)
            self.hits += 1
            return HIT_CYCLES
        self.misses += 1
        self.lines[address] = True
        if len(self.lines) > self.capacity:
            self.lines.popitem(last=False)
        return MISS_CYCLES
```

An `OrderedDict` keeps the lines in order of use; `move_to_end` marks a line as just used, and `popitem(last=False)` throws out the oldest. Two generators produce the address streams: `weight_stream_naive` and `weight_stream_tiled`. Output: 0.0% and 93.8% hit rates.

### Step 4: The scratchpad

```python
def scratchpad_cycles(batch, k_dim, n_dim, tile, words_per_cycle):
    tiles = (k_dim // tile) * (n_dim // tile)
    load = tile * tile / words_per_cycle
    compute = batch * tile * tile
    return load + tiles * max(load, compute), load, compute
```

With double buffering, each tile costs `max(load, compute)`, plus one initial load. Our toy cache fetches one word per miss with no overlap, so it looks worse than a real cache would (real caches fetch whole lines of 64 bytes and prefetch ahead); the important difference is that the scratchpad's time is known in advance.

### Step 5: The area split

```python
def delivered_macs_per_cycle(array_n, buffer_bits, dram_bytes_per_cycle=2.0):
    weight_bits = array_n * array_n * 8
    per_input_bits = array_n * 8 + array_n * 24
    batch = max((buffer_bits - weight_bits) // per_input_bits, 0)
    peak = array_n * array_n
    if batch == 0:
        return 0, batch
    return min(peak, dram_bytes_per_cycle * batch), batch
```

The script sweeps three array sizes and three buffer sizes and prints the table above, with the area from `cost.systolic_array` and `cost.sram`.

### Step 6: The lab

The script checks the lab task's reference solution.

## Use It

- **CPUs** have a deep cache hierarchy: per core about 32-64 KB of L1 data cache (a few cycles), 1-2 MB of L2 (about a dozen cycles), and a shared L3 of tens of MB (40+ cycles), before DRAM at hundreds of cycles.
- **GPUs** combine small caches with software-managed **shared memory** (a scratchpad of up to a few hundred KB per streaming multiprocessor) that kernel writers fill explicitly, tile by tile.
- **AI accelerators** often rely mainly on scratchpads and DMA engines: the first TPU had a 24 MB "unified buffer" managed by software; Graphcore and Cerebras chips keep entire models (or large parts of them) in on-chip SRAM spread over the die.
- **HBM** stacks of DRAM dies sit beside AI processors on a silicon interposer, giving terabytes per second of bandwidth; their capacity per stack (tens of GB) often decides how big a model one chip can serve.
- **Refresh and temperature.** DRAM must refresh more often when hot, which costs bandwidth and energy; data-centre DRAM is cooled for that reason too.

## Try It in the Lab

Open "Split the area between MACs and memory". You have 60,000 gates for a systolic array of 8-bit MACs (608 gates each) and an SRAM buffer (1 gate per bit). DRAM gives 2 bytes per cycle, so a busy array needs a buffer that can hold a batch big enough to reuse each weight. Reach 64 MACs per cycle, keep the buffer at 16 kbit or more, and stay within the budget. Compute the area of each combination before running. Which goal does each wrong combination fail?

## Common Mistakes

- **Treating memory as a single flat thing.** "The data is in memory" hides a factor of 100 in latency and energy between a register and DRAM.
- **Ignoring access order.** The naive loop got 0% hits in a cache that the tiled loop used at 94%. Same hardware, 14 times slower.
- **Sizing the array without the buffer.** An array whose buffer cannot hold enough reused data runs at a fraction of its peak; the extra MACs are wasted area.
- **Forgetting DRAM refresh and latency.** DRAM bandwidth is high, but each new access takes about 100 ns; only long, predictable bursts reach the peak bandwidth.
- **Assuming caches are always better.** Caches cost tags, comparators and unpredictability; for known, regular computations software-managed scratchpads are often smaller and faster.

## Exercises

1. A cache of 2,048 words reads the 64 x 64 weights (4,096 words) in naive order for 16 inputs. Predict the hit rate with LRU, then change the capacity in the script and check.
2. With 16 x 16 tiles instead of 32 x 32 in the tiled order, what hit rate do you expect with a 1,024-word cache? Why?
3. In the scratchpad model, what DRAM bandwidth (words per cycle) would make loading a 32 x 32 tile take as long as computing on it with a batch of 1? What happens to the total time then?
4. Using `delivered_macs_per_cycle`, find the smallest buffer (in bits) that lets a 16 x 16 array reach full speed. What total area would that need?
5. Harder: add a small second level to the cache simulator (an L2 of 8,192 words with a 20-cycle hit time in front of the 100-cycle DRAM). Rerun the naive order and explain the result.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Memory hierarchy | "the caches and stuff" | Layers from registers to DRAM, each larger, slower and costlier per access than the one above |
| SRAM | "on-chip memory" | Six-transistor cells held by feedback; fast, logic-compatible, about 6x denser than flip-flops |
| DRAM | "RAM" | One transistor and one capacitor per bit; dense, slow, refreshed every few tens of ms |
| Cache | "it remembers what you used" | Hardware-managed copies of recent data with tags and a replacement policy such as LRU |
| Scratchpad | "local memory", "shared memory" | Plain SRAM filled explicitly by software, with predictable timing |
| Double buffering | "ping-pong buffers" | Loading the next block while computing on the current one, hiding transfer time |
| Tiling | "blocking" | Reordering loops so a block of data is fully reused while it sits in fast memory |

## Further Reading

- John L. Hennessy and David A. Patterson, *Computer Architecture: A Quantitative Approach* (Morgan Kaufmann), chapter 2, "Memory Hierarchy Design".
- Ulrich Drepper, "What Every Programmer Should Know About Memory" (2007) — DRAM, caches and access patterns explained in depth.
- Bruce Jacob, Spencer Ng and David Wang, *Memory Systems: Cache, DRAM, Disk* (Morgan Kaufmann, 2007).
- Norman P. Jouppi et al., "In-Datacenter Performance Analysis of a Tensor Processing Unit", *ISCA 2017* — a software-managed unified buffer feeding a systolic array.
