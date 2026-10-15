# FPGA and ASIC

> An FPGA is a chip that can become any circuit, and pays for that freedom with area, speed and power. An ASIC is one circuit forever, and pays up front.

**Type:** Build
**Prerequisites:** Phase 20 (Chip Design), Lessons 01-05; Phase 14 (Digital Logic), Lessons 03 (Boolean Algebra), 06 (Combinational Circuits) and 08 (Multiplexers and Decoders)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| ASIC | Application-specific integrated circuit: a chip whose gates and wires are fixed when it is manufactured | A house built of brick to one plan |
| FPGA | Field-programmable gate array: a chip full of configurable logic and wiring that you program after manufacture | A huge box of LEGO that can become any house |
| LUT (lookup table) | A tiny memory with k inputs that stores the output for every one of its 2^k input combinations | A cheat sheet with the answer to every question written down |
| Configuration bits | The memory bits inside an FPGA that decide what each LUT computes and how wires connect | The instructions telling you which LEGO goes where |
| Bitstream | The file of configuration bits loaded into an FPGA when it powers up | The instruction booklet as a file |
| Programmable routing | Wires with switches at every crossing, so any block can be connected to any other | A railway network full of switch points |
| Hard block | A fixed, ASIC-style block built into an FPGA (multipliers, memories, transceivers) | Ready-made LEGO pieces like wheels and windows |
| NRE | Non-recurring engineering: the one-off cost of designing and preparing to manufacture a chip | The architect and the moulds, paid once |
| Unit cost | The cost of each additional chip once production runs | The bricks for each extra house |
| Break-even volume | The quantity at which two options cost the same in total | How many houses before the moulds pay for themselves |
| Mask set | The set of photomasks (one per layer) used to print a chip design on silicon | The stencils for every layer of a printed poster |
| Time to market | How long from idea to a product people can buy | How long until the shop opens |

## Learning Objectives

- Explain how a lookup table can implement any Boolean function of its inputs, and build one from multiplexers with `sim.logic`.
- Configure the same LUT as several different functions just by changing its configuration bits.
- Estimate the area overhead of an FPGA compared with direct gates, including configuration memory and programmable routing, and relate it to published measurements.
- Compute the break-even volume between an FPGA and an ASIC from their up-front and per-unit costs.
- Decide when each one is the right choice, considering volume, need for changes, speed, power and time to market.

## The Problem

You have designed a matrix engine in Lessons 01-08. How do you get it into silicon? You have two very different options.

You can design an **ASIC**: a chip made only for your circuit. Every gate is exactly where your design put it, nothing is wasted, and it is as fast and efficient as the process allows. But before the first chip exists you pay for months of engineering, verification and a set of photomasks: millions of dollars in a modern process. If you find a bug after manufacture, you pay again.

Or you can use an **FPGA**: an off-the-shelf chip full of small configurable logic blocks and switchable wires. You describe your circuit, a tool turns it into a configuration file, and minutes later the FPGA *is* your circuit. If it is wrong, you change the file. No masks, no waiting. But your circuit will be bigger, slower and hungrier than the ASIC version, often by an order of magnitude, and each FPGA costs more than an ASIC would in volume.

This lesson builds the heart of an FPGA (the lookup table) from gates, measures what its flexibility costs, and computes when each option wins.

## The Physics

There is no new device physics: an FPGA is built from the same CMOS transistors as any chip. The differences come from what is added to make it programmable:

- **Configuration memory.** Every LUT entry and every routing switch is controlled by a bit of SRAM (in most FPGAs) that is loaded at power-up. These bits take area and leak current even when nothing switches.
- **Pass transistors and buffers in the routing.** A signal travelling between two logic blocks passes through several programmable switches. Each switch is a transistor with some on-resistance, and each wire segment has capacitance. More resistance times more capacitance means more delay (the RC idea of Lesson 01) and more energy per transition (`C * V^2`).
- **Generality.** A LUT that can compute any 4-input function is bigger than the one gate a specific function might need.

## The Concept

### A lookup table is a memory addressed by the inputs

Any Boolean function of `k` inputs is completely described by its truth table: `2^k` rows, each with a 0 or a 1. Store those `2^k` bits in a tiny memory and use the inputs as the address: the output is the stored bit for that row. That is a **lookup table**.

For 3 inputs `a, b, c`, the row number is `4a + 2b + c`. A majority function (1 when at least two inputs are 1) has the truth table:

```
row:   0   1   2   3   4   5   6   7
a b c: 000 001 010 011 100 101 110 111
out:   0   0   0   1   0   1   1   1
```

so its configuration bits are `00010111`. An XOR of three inputs (a full adder's sum) is `01101001`. Same hardware, different 8 bits.

### Building a LUT from multiplexers

To read one of 8 stored bits, use a tree of 2:1 multiplexers (Phase 14, Lesson 08). The last input selects between neighbouring bits, the next input between those results, and so on:

```
 cfg0 --+
        [MUX c]--+
 cfg1 --+        |
                 [MUX b]--+
 cfg2 --+        |        |
        [MUX c]--+        |
 cfg3 --+                 |
                          [MUX a]--- out
 cfg4 --+                 |
        [MUX c]--+        |
 cfg5 --+        |        |
                 [MUX b]--+
 cfg6 --+        |
        [MUX c]--+
 cfg7 --+
```

A `k`-input LUT needs `2^k - 1` multiplexers. In our model each is 3 gates (two AND and one OR), plus one inverter per input to make the "not select" signals, plus `2^k` configuration bits at 6 gates each (they are stored in flip-flop-like cells):

```
LUT area = 3 * (2^k - 1) + k + 6 * 2^k
LUT3:  3 * 7  + 3 + 6 * 8   = 21 + 3 + 48   = 72 gates
LUT4:  3 * 15 + 4 + 6 * 16  = 45 + 4 + 96   = 145 gates
LUT6:  3 * 63 + 6 + 6 * 64  = 189 + 6 + 384 = 579 gates
```

Its delay is one inverter plus two gates per level: 7 gate delays for a LUT3, 13 for a LUT6. (Real FPGA LUTs are built from faster pass-transistor multiplexers, but the trend is the same.)

### What the flexibility costs

A full adder needs 5 gates. In LUTs it needs two LUT3s, one for the sum (XOR3) and one for the carry (majority): 144 gates in our model. A 4-bit ripple adder is 20 gates as direct logic but 8 LUT3s = 576 gates: about **29 times** larger, before we even connect the LUTs together.

And connecting them is the bigger cost. In an FPGA, any LUT output must be able to reach many possible LUT inputs, so every logic block sits in a grid of wire segments with programmable switches. Routing typically takes more area than the LUTs themselves; with routing at three times the logic area, our adder is about 86 times larger than direct gates.

Real FPGAs fight this overhead in several ways:

- **Bigger LUTs** (6 inputs, or one 6-input LUT that can be split into two 5-input ones) pack more logic per routing connection.
- **Dedicated carry chains**: a fast, fixed adder path between neighbouring logic blocks, so arithmetic does not use LUTs for the carries.
- **Hard blocks**: fixed multipliers ("DSP slices"), block RAMs and high-speed transceivers, built like an ASIC inside the FPGA.

Careful measurements (Ian Kuon and Jonathan Rose, 2007, on a 90 nm FPGA against standard-cell ASICs in the same process) found that for the same circuits an FPGA needed about **35 times the area** using only LUTs and about **18 times** when hard multipliers and memories could be used, was about **3 to 4 times slower** on the critical path, and used about **14 times the dynamic power**. Our toy numbers are in the same ballpark.

### The economics: up-front cost against unit cost

Say an ASIC costs \$3,000,000 in NRE (engineering, verification tools, masks) and \$4 per chip; a suitable FPGA costs \$20,000 up front (boards, tools, engineering) and \$60 per chip. The total cost of `n` units is

```
ASIC:  3,000,000 + 4 n
FPGA:     20,000 + 60 n
```

They are equal when `3,000,000 + 4n = 20,000 + 60n`, that is

```
n = (3,000,000 - 20,000) / (60 - 4) = 2,980,000 / 56 = 53,214 units
```

Below about 53 thousand units, the FPGA is cheaper overall; above, the ASIC wins, and by a lot at large volume:

| Units | ASIC per unit | FPGA per unit | Cheaper |
|---|---|---|---|
| 1,000 | \$3,004 | \$80 | FPGA |
| 10,000 | \$304 | \$62 | FPGA |
| 100,000 | \$34 | \$60.20 | ASIC |
| 1,000,000 | \$7 | \$60.02 | ASIC |

These prices are made up but realistic in shape. Mask sets alone range from tens of thousands of dollars in old processes to many millions in leading-edge ones, which pushes the break-even volume up as processes advance.

### When to choose which

- **FPGA:** prototypes and verification of future ASICs; low volumes (test equipment, scientific instruments, aerospace); products whose function must change after shipping (networking, new standards); when time to market matters more than unit cost; and latency-critical, specialised jobs where custom logic beats a CPU even with the FPGA overhead.
- **ASIC:** high volumes (phones, consumer devices, data-centre accelerators); when power or speed must be the best possible; when the function is stable.
- **In between:** structured ASICs, and FPGAs with hardened blocks for the parts that are known in advance.

AI accelerators are a famous case: both have been used. FPGAs host experimental inference engines that can change with every new model; data centres running huge volumes of stable workloads build ASICs.

## Build It

Run:

```
uv run python phases/20-chip-design/09-fpga-and-asic/code/main.py
```

### Step 1: A LUT from gates

```python
def build_lut(k):
    lc = LogicCircuit(f"LUT{k}")
    names = [f"i{n}" for n in range(k)]
    lc.inputs(*names)
    for name in names:
        lc.not_(f"n_{name}", name)
    level = [f"cfg{i}" for i in range(2 ** k)]
    for depth, sel in enumerate(reversed(names)):
        nxt = []
        for m in range(len(level) // 2):
            out = f"L{depth}_{m}" if len(level) > 2 else "out"
            add_mux(lc, f"M{depth}_{m}", level[2 * m], level[2 * m + 1], sel, out)
            nxt.append(out)
        level = nxt
    lc.outputs("out")
    return lc
```

The configuration bits `cfg0 ... cfg(2^k - 1)` are the leaves of the multiplexer tree; the last input selects at the first level, the first input at the last. `configure` sets each bit as a constant from a Python function, row by row in the same order as the truth table. The script configures one LUT3 as majority (`00010111`), XOR3 (`01101001`) and `(a AND b) OR c` (`01010111`) and checks all 8 rows each time.

### Step 2: LUT area

`lut_area(k)` adds the multiplexers, the input inverters and the configuration bits: 72, 145 and 579 gates for LUT3, LUT4 and LUT6, with depths of 7, 9 and 13 gate delays.

### Step 3: The adder in LUTs

8 LUT3s (576 gates) against a 20-gate ripple adder: 28.8 times larger before routing, about 86 times with routing at three times the logic area.

### Step 4: Measured overheads

The Kuon and Rose numbers, printed for comparison.

### Step 5: Break-even volume

```python
def break_even(nre_asic, unit_asic, nre_fpga, unit_fpga):
    return (nre_asic - nre_fpga) / (unit_fpga - unit_asic)
```

53,214 units with our prices, and the per-unit table above.

### Step 6: The lab

The script checks the lab's reference configuration.

## Use It

- **FPGA families.** AMD (formerly Xilinx) and Intel (Altera) dominate large FPGAs; Lattice and Microchip make small, low-power ones; open-source toolchains (Yosys, nextpnr) support several small families such as the Lattice iCE40, popular with hobbyists.
- **Data centres.** Microsoft's Project Catapult put FPGAs in Bing's servers to accelerate search ranking and networking; cloud providers rent FPGA instances.
- **Prototyping ASICs.** Before tape-out, chip companies run their designs on racks of large FPGAs ("emulation" and "prototyping" platforms) to boot software months before silicon exists.
- **Retro computing and hobby projects** use FPGAs to recreate old consoles and computers gate by gate.
- **AI.** Early neural-network accelerators were often prototyped on FPGAs; mass-deployed accelerators (TPUs, phone neural engines) are ASICs.

## Try It in the Lab

Open "Program the LUT as a majority vote". It is a 3-input LUT built from a multiplexer tree, with its eight configuration bits as slots. Each slot is fed from a constant 1: a `buf` passes it (the bit is 1), a `not` turns it into 0. Program the LUT so its output is 1 whenever at least two of `a`, `b`, `c` are 1. Write the truth table first, row by row; then configuration bit `i` is just the output you want in row `i`.

## Common Mistakes

- **Thinking an FPGA runs a program.** It does not execute instructions like a CPU; the configuration *is* the circuit. (Though you can configure an FPGA to be a CPU.)
- **Comparing FPGA and ASIC by LUT counts alone.** Routing usually dominates the area and the delay of an FPGA design.
- **Ignoring hard blocks.** A multiplier built from LUTs is many times worse than the FPGA's own DSP slices; good FPGA designs map arithmetic onto them.
- **Forgetting NRE grows with the process.** Leading-edge masks and verification cost far more than older nodes, raising the volume an ASIC needs to pay off.
- **Treating the choice as permanent.** Many products start on FPGAs and move to ASICs once the design and the volume are stable.

## Exercises

1. Write the configuration bits of a LUT3 that computes `a XOR b` and ignores `c`. Check them in the script by adding the function to `FUNCTIONS`.
2. How many configuration bits does a LUT5 have, and what is its area in our model?
3. Can one LUT4 compute a full adder's sum *and* carry at the same time? Why not, and how many LUT4s does an 8-bit ripple adder need?
4. With the prices of Step 5, what break-even volume do you get if the ASIC's NRE rises to \$10,000,000? If instead the FPGA price falls to \$30?
5. Harder: extend `build_lut` so that two LUT3s and one 2:1 multiplexer form a LUT4 (the fourth input selects between the two LUT3s). Compare its area with `lut_area(4)` and explain the difference.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| FPGA | "programmable hardware" | A chip of LUTs, flip-flops, hard blocks and switchable routing, configured by a bitstream |
| ASIC | "a custom chip" | A chip whose logic and wiring are fixed by its masks |
| LUT | "a logic cell" | A 2^k-bit memory addressed by k inputs, able to implement any k-input function |
| Configuration bits | "the bitstream" | The SRAM bits that set every LUT's contents and every routing switch |
| Routing overhead | "the wires eat everything" | Area, delay and power of programmable interconnect, usually larger than the logic itself |
| NRE | "the upfront cost" | One-off engineering, tools and mask costs before the first chip |
| Break-even volume | "when the ASIC pays off" | `(NRE_ASIC - NRE_FPGA) / (unit_FPGA - unit_ASIC)` |

## Further Reading

- Ian Kuon and Jonathan Rose, "Measuring the Gap Between FPGAs and ASICs", *IEEE Transactions on CAD*, 26(2), 2007.
- David Money Harris and Sarah L. Harris, *Digital Design and Computer Architecture* (Morgan Kaufmann), sections on programmable logic and FPGAs.
- Andrew Putnam et al., "A Reconfigurable Fabric for Accelerating Large-Scale Datacenter Services", *ISCA 2014* — Microsoft's Catapult FPGAs.
- [Project IceStorm and the Yosys/nextpnr open-source FPGA toolchain](https://github.com/YosysHQ) — program a real FPGA with free tools.
