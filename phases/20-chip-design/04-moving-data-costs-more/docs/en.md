# Moving Data Costs More

> On a modern chip, doing arithmetic is cheap. Fetching the numbers to do it on is what you really pay for.

**Type:** Build
**Prerequisites:** Phase 20 (Chip Design), Lessons 01-03; Phase 07 (Capacitors), Lesson 06 (Energy in the Electric Field); Phase 14 (Digital Logic), Lesson 08 (Multiplexers and Decoders); Phase 16 (A Computer from Gates), Lesson 03 (Memory)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Operand | A number an operation works on (the `a` and `b` in `a * b`) | An ingredient you need on the counter before cooking |
| Register file | A small set of registers inside the processor, with multiplexers to pick which one to read | The spice rack right next to the stove |
| Read port | One independent way to read a value out of a memory at the same time as others | One hand reaching into the spice rack |
| SRAM | Static RAM: fast on-chip memory, each bit a small circuit of six transistors | The pantry in the kitchen |
| DRAM | Dynamic RAM: dense memory outside the chip (or stacked next to it), each bit a tiny capacitor | The supermarket down the road |
| HBM | High Bandwidth Memory: DRAM chips stacked and placed right next to the processor | A warehouse built next door with a wide loading dock |
| Picojoule (pJ) | 10^-12 joule, the energy unit for single operations on a chip | One grain of sugar of energy |
| Wire capacitance | The capacitance of an on-chip wire, which must be charged every time its bit changes | The water needed to fill a long hose before any comes out |
| Data movement | Carrying bits from where they are stored to where they are used | Driving to the shop and back |
| Reuse | Using a number many times after fetching it once | Buying a whole bag of flour for many cakes |
| Locality | Keeping data physically close to where it is used | Keeping the knives next to the chopping board |

## Learning Objectives

- Compare the energy of arithmetic operations with the energy of reading data from registers, on-chip SRAM and DRAM, using published 45 nm figures.
- Derive the energy of moving a bit along an on-chip wire from `C * V^2`, and compare it with the energy of a multiply.
- Use `sim.cost` to show that a register file with two read ports can be larger than the MAC it feeds.
- Compute the energy per MAC for operands fetched from different memories, and show how reusing each fetched value brings it back down.
- Explain why this single fact shapes accelerators: big arrays of arithmetic surrounded by small, close memories, and algorithms that reuse data.

## The Problem

Lessons 01-03 counted the cost of computing: gates for adders and multipliers, and gate delays for their paths. If computing were all that mattered, the best AI chip would be a sea of multipliers. Real chips are not. A modern AI accelerator spends large parts of its area on memories, and most of its energy budget on moving numbers from memory to the multipliers and back.

The reason is a fact that surprises everyone the first time: **on a modern chip, fetching a number costs far more energy than doing arithmetic on it**. Multiplying two 8-bit numbers costs about 0.2 pJ. Reading those 8 bits from the computer's main memory (DRAM) costs about 250 pJ, more than a thousand times as much. A chip that fetched both operands of every multiplication from DRAM would spend 99.9% of its energy on the trip.

This lesson puts numbers on that gap, explains where it comes from physically, and shows the one trick that saves us: reuse.

## The Physics

### Every bit moved charges a wire

A wire on a chip is a thin strip of copper separated from its neighbours and from the layers below by insulator. Like any two conductors separated by an insulator, it forms a capacitor (Phase 07). A rough value for a minimum-width on-chip wire is about **0.2 pF per millimetre** (0.2 fF per micrometre).

To send a 1 down the wire, the driver charges that capacitance to the supply voltage V; later, to send a 0, it discharges it. Each full charge takes energy `C * V^2` from the supply (half is stored and later dumped, half is lost in the driver; Phase 07, Lesson 06). So moving one bit that changes value along one millimetre costs

```
E = C * V^2 = 0.2e-12 F * (0.9 V)^2 = 0.2e-12 * 0.81 = 0.162e-12 J = 0.16 pJ
```

A byte (8 bits) along 1 mm: about 1.3 pJ. Compare with an 8-bit multiply at about 0.2 pJ: **moving one byte just 0.15 mm costs as much as multiplying it**. A chip is typically 10-30 mm across, so carrying data across it costs tens of multiplies per byte.

And the gates themselves? A multiplier's gates are tiny and packed tightly: their internal wires are micrometres long. The multiplier's energy is mostly those short wires and gate inputs. A long wire is the same physics, just much more capacitance.

### Memories are mostly wires

A memory is an array of storage cells with long wires running across it: word lines (to select a row) and bit lines (to carry the stored bits out). A bigger memory has longer wires, and reading it means charging and discharging them, then amplifying the tiny signal from a cell. So:

- **A small register file** next to the arithmetic: short wires, cheap.
- **On-chip SRAM** of kilobytes to megabytes: longer bit lines and word lines, more energy per access the bigger it is. An 8 KB SRAM costs about 10 pJ per 64-bit read; a 1 MB SRAM about 100 pJ.
- **DRAM** in a separate chip: the bits must leave our chip through a pin, travel along a board trace or a silicon interposer (a few millimetres to a few centimetres of high-capacitance wire), and be read out of the DRAM's own big arrays. About 1.3-2.6 nJ per 64 bits: 20-40 pJ per bit.

### The numbers

Mark Horowitz's 2014 summary (45 nm process, rounded) is the most quoted table in computer architecture:

| Operation | Energy | Compared with an 8-bit multiply |
|---|---|---|
| 8-bit integer add | 0.03 pJ | 0.15x |
| 32-bit integer add | 0.1 pJ | 0.5x |
| 8-bit integer multiply | 0.2 pJ | 1x |
| 16-bit float multiply | 1.1 pJ | 5.5x |
| 32-bit integer multiply | 3.1 pJ | 15x |
| 32-bit float multiply | 3.7 pJ | 18x |
| 64-bit read from an 8 KB SRAM | 10 pJ | 50x |
| 64-bit read from a 1 MB SRAM | 100 pJ | 500x |
| 64-bit read from DRAM | about 2,000 pJ | 10,000x |

Newer processes shrink all of these, but arithmetic shrinks faster than wires do, so the gap has grown, not closed.

## The Concept

### The area of fetching operands

Energy is one cost; area is another. A MAC needs two operands every cycle. Suppose they come from a register file of `R` registers of 8 bits. To read any one of them you need an `R`-to-1 multiplexer for each bit (Phase 14, Lesson 08), and you need **two** such read ports, one for each operand. In our cost model:

```
storage:          6 gates per flip-flop * R * 8 bits
one read port:    3 gates per 2:1 mux * (R - 1) * 8 bits
```

For `R = 32`:

```
storage:          6 * 32 * 8   = 1,536 gates
two read ports:   2 * 3 * 31 * 8 = 1,488 gates
total:                          3,024 gates
```

The MAC it feeds is 608 gates. The register file is **five MACs' worth of area**, and its read path adds `2 * log2(32) = 10` gate delays before the MAC can even start. With 128 registers it would be 20 MACs' worth. This is why a general-purpose processor, which reads its operands from a register file for every instruction, gets so little arithmetic per square millimetre, and why accelerators try hard to avoid "fetch both operands from a big shared pool" for each operation (Lesson 06).

### Energy per MAC depends on where the operands live

Let us compute the energy of one 8-bit MAC (0.2 pJ multiply + 0.1 pJ 32-bit add = 0.3 pJ) when both 1-byte operands are fetched for it:

| Operands come from | Fetch energy per byte | Energy per MAC | Spent moving data |
|---|---|---|---|
| register file (assumed 4x cheaper than an 8 KB SRAM) | 0.31 pJ | 0.3 + 2 x 0.31 = 0.93 pJ | 68% |
| 8 KB SRAM | 1.25 pJ | 0.3 + 2.5 = 2.8 pJ | 89% |
| 1 MB SRAM | 12.5 pJ | 0.3 + 25 = 25.3 pJ | 98.8% |
| DRAM | 250 pJ | 0.3 + 500 = 500.3 pJ | 99.9% |

The register file line uses an assumption (it is not in Horowitz's table); the others come straight from it, divided by 8 bytes per 64-bit read.

So the "same" MAC costs anywhere from under 1 pJ to 500 pJ depending on where its numbers live. The arithmetic is a rounding error in the expensive cases.

### Reuse is the cure

The way out is to fetch each number once and use it many times. If each byte fetched from DRAM is used in `R` MACs, its fetch energy is shared:

```
energy per MAC = 0.3 pJ + 2 * (fetch energy per byte) / R
```

"the arithmetic, plus the cost of fetching two bytes, divided among the `R` MACs that use them". For DRAM:

```
R = 1:     0.3 + 500 / 1    = 500.3 pJ
R = 16:    0.3 + 500 / 16   =  31.6 pJ
R = 256:   0.3 + 500 / 256  =   2.25 pJ
R = 4096:  0.3 + 500 / 4096 =   0.42 pJ
```

With enough reuse, even DRAM data becomes cheap. Does such reuse exist? In a matrix product, yes, a lot:

- each **weight** of a layer is used once for every input vector in the batch (reuse = batch size);
- each **input** value is used once for every row of the weight matrix (reuse = number of outputs, often thousands).

The whole art of accelerator design (Lessons 06-08) is arranging the hardware and the order of the computation so that every number is fetched from far away as few times as possible, and reused from somewhere close as many times as possible.

### The same story in sim.cost

`sim.cost` has its own energy units to keep numbers simple: a gate switching costs 1 unit, and a quarter of a block's gates switch per cycle; a bit read from SRAM costs 10 units, from DRAM 200; a bit moved one unit of wire costs 2. Fetching two 8-bit operands (16 bits) for one MAC:

```
from SRAM:  16 * 10  =  160 units  + MAC 608 * 0.25 = 152 units  ->   312 units
from DRAM:  16 * 200 = 3200 units  + MAC 152 units               -> 3,352 units
```

The ratios are milder than the real table (DRAM is "only" 20 times SRAM here), but the conclusion is the same: the fetch dominates. DRAM also adds latency: `sim.cost.dram` takes 100 cycles to answer, against 1 for SRAM.

## Build It

Run:

```
uv run python phases/20-chip-design/04-moving-data-costs-more/code/main.py
```

### Step 1: The energy table

The list `ENERGY_PJ_45NM` holds the rounded Horowitz numbers. The script prints each one and its ratio to an 8-bit multiply: from 0.15x for an 8-bit add to 10,000x for a DRAM read.

### Step 2: Wire energy from physics

```python
def wire_energy_pj(length_mm, bits=1, cap_pf_per_mm=0.2, volts=0.9):
    return bits * cap_pf_per_mm * length_mm * volts ** 2
```

Picofarads times volts squared gives picojoules directly. One bit over 1 mm: 0.162 pJ; one byte over 10 mm: 13 pJ. An 8-bit multiply equals moving a byte about 0.15 mm.

### Step 3: Register file area

```python
mac = cost.mac(8)
for words in (8, 32, 128):
    rf = cost.register_file(words, 8)
    second_port = cost.mux(words, 8)
    total = rf.area + second_port.area
```

`cost.register_file` includes the storage and one read port, so we add a second `cost.mux` for the second operand. Output: 720, 3,024 and 12,240 gates for 8, 32 and 128 registers: 1.2, 5.0 and 20.1 MACs' worth.

### Step 4: Energy per MAC by source

```python
def energy_per_mac(source, reuse=1):
    return MAC_PJ + 2 * PER_BYTE_PJ[source] / reuse
```

The four lines of the table above.

### Step 5: Reuse

The same function with `reuse` of 1, 16, 256 and 4096, for DRAM and for a 1 MB SRAM.

### Step 6: sim.cost energy

A two-block design: a fetch block (an SRAM or a DRAM delivering 16 bits) and a MAC. `d.energy()` adds their energies; `d.latency()` counts the cycles: 2 with SRAM, 101 with DRAM.

## Use It

- **Why GPUs have huge register files.** An NVIDIA GPU streaming multiprocessor has a register file of 256 KB, larger than many CPUs' L1 cache, precisely so that thousands of threads can keep their operands close to the arithmetic.
- **Why AI chips have big SRAMs.** Accelerators from Google (TPU), Graphcore, Cerebras and others devote large parts of the die to on-chip SRAM (tens to hundreds of megabytes), so that weights and activations can be reused without going to DRAM.
- **Why HBM exists.** HBM stacks DRAM dies and places them millimetres from the processor on a silicon interposer with thousands of wires, cutting the energy and raising the bandwidth of each off-chip access compared with DRAM on a separate board.
- **Why batching helps.** Serving many users at once (a bigger batch) reuses each weight fetched from memory across more inputs, cutting energy and raising throughput per weight fetched: the roofline story of Lesson 08.
- **Why "near-memory" and "in-memory" computing are researched.** If moving data is the problem, putting simple arithmetic inside or right beside the memory arrays avoids the trip.

## Common Mistakes

- **Judging a chip by its peak arithmetic.** "1,000 TOPS" means nothing if the operands cannot be delivered; the delivered rate is usually limited by data movement.
- **Ignoring the register file.** Even the closest memory can cost more area and energy than the arithmetic it feeds, especially with many read ports.
- **Assuming the gap will close.** Process improvements make transistors cheaper faster than they make wires cheaper. Data movement has become relatively *more* expensive over time.
- **Counting reuse that the hardware cannot exploit.** A matrix product has lots of reuse in theory, but if the on-chip memory is too small to hold the reused data, it gets fetched again and the reuse is lost (Lesson 07).
- **Confusing energy and power.** Energy per operation (pJ) times operations per second gives power (W). A chip can be energy-efficient and still hot, if it does many operations.

## Exercises

1. A chip does 10^14 8-bit MACs per second, each with both operands fetched from a 1 MB SRAM (25.3 pJ per MAC). What power does that take? What if the operands come from a register file instead (0.93 pJ per MAC)?
2. Using 0.2 pF/mm and 0.9 V, how far can one byte travel on chip for the energy of a 32-bit float multiply (3.7 pJ)?
3. In our cost model, how big is a register file of 16 registers of 16 bits with two read ports? How many 8-bit MACs is that?
4. Each weight of a layer is fetched from DRAM once and used for a batch of `B` inputs. Ignoring the inputs, what batch size makes the DRAM energy per MAC equal to the arithmetic energy (0.3 pJ)? (Fetch energy for one byte: 250 pJ.)
5. Harder: a design reads its weights from DRAM (reuse = batch size B) and its inputs from an 8 KB SRAM (reuse = 4096, the number of rows). Write the energy per MAC as a function of B and find B such that data movement is half of the total.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Data movement | "memory traffic" | Bits carried from storage to arithmetic and back; usually the dominant energy cost |
| Wire energy | "interconnect power" | About `C * V^2` per bit change, roughly 0.16 pJ per bit per millimetre on chip |
| Register file | "the registers" | Small fast storage with multiplexer read ports; its area grows with entries x width x ports |
| SRAM | "on-chip memory" | Fast memory on the die; energy per access grows with its size |
| DRAM / HBM | "main memory" | Dense off-chip memory; about 10,000 times the energy of an 8-bit multiply per 64-bit read |
| Reuse | "data reuse" | Using each fetched number in many operations so its fetch cost is shared |
| Locality | "keep it close" | Placing data near the arithmetic that uses it, to shorten its trips |

## Further Reading

- Mark Horowitz, "Computing's energy problem (and what we can do about it)", *ISSCC 2014* — the energy table.
- William J. Dally, Yatish Turakhia and Song Han, "Domain-Specific Hardware Accelerators", *Communications of the ACM*, 2020 — why accelerators are organised around data movement.
- John L. Hennessy and David A. Patterson, *Computer Architecture: A Quantitative Approach* (Morgan Kaufmann), chapter on domain-specific architectures.
- Vivienne Sze, Yu-Hsin Chen, Tien-Ju Yang and Joel Emer, *Efficient Processing of Deep Neural Networks* (Morgan & Claypool, 2020), chapters on dataflows and reuse.
