# From RTL to the Fab

> A chip starts as a text file and ends as a slab of silicon in a package. In between, software turns logic into gates, gates into geometry, and geometry into masks, and physics decides how many come out working.

**Type:** Build
**Prerequisites:** Phase 20 (Chip Design), Lessons 01-10; Phase 21 (PCB Design and Manufacturing), Lesson 05 (Fabrication) is a useful comparison; Phase 11 (Semiconductors and Diodes), Lesson 02 (Doping N and P)
**Time:** ~85 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| RTL (register-transfer level) | A description of hardware as registers and the logic that computes their next values, written in a hardware description language | A recipe that says what goes into each pot at each tick of the clock |
| HDL (Verilog, VHDL) | A programming-like language for describing circuits rather than instructions | Sheet music for a circuit instead of a story |
| Testbench | Code that feeds a design inputs and checks its outputs in simulation | An exam marked automatically |
| Verification | Proving, by simulation and by formal methods, that the design does what it should | Proofreading a book before printing a million copies |
| Synthesis | Turning RTL into a netlist of standard cells (real gates from a library) | Translating the recipe into a shopping list of exact ingredients |
| Standard cell | A pre-designed gate (NAND2, flip-flop...) of fixed height that tiles in rows | A standard brick |
| PDK (process design kit) | The foundry's package of rules, device models and cell libraries for one manufacturing process | The building code and catalogue of approved bricks |
| Floorplan | Deciding roughly where big blocks go on the die | Sketching where the kitchen and bedrooms go |
| Placement | Choosing the exact position of every cell | Placing every brick |
| Clock tree | The buffered network that delivers the clock to every flip-flop at nearly the same time | A water main branching evenly to every house |
| Routing | Drawing the metal wires that connect the cells, on many stacked metal layers | Laying pipes and cables through the walls |
| Wirelength (HPWL) | An estimate of wire needed: for each net, half the perimeter of the box around its pins | String needed to reach every pin of a net |
| Signoff | Final checks: timing, power, design rules (DRC), layout versus schematic (LVS) | The final building inspection |
| Tape-out | Sending the final layout to the foundry | Sending the manuscript to the printer |
| Mask | A plate carrying the pattern of one layer, used in lithography to print it on the wafer | A stencil for one colour of a print |
| Wafer | A thin disc of pure silicon (usually 300 mm across) on which hundreds of dies are made at once | A baking sheet of biscuits |
| Yield | The fraction of dies that work | The share of biscuits that are not burnt |
| Chiplet | A smaller die designed to be packaged together with others into one product | Building a house from prefabricated rooms |

## Learning Objectives

- Read a short piece of Verilog RTL and say which hardware it describes.
- Describe the design flow: RTL, verification, synthesis, floorplanning, placement, clock tree, routing, signoff, tape-out.
- Build a toy synthesizer that turns Boolean expressions into gates, shares common subexpressions, and checks equivalence by truth table.
- Build a toy placer that reduces total wirelength by swapping cells, and explain why placement matters for delay and power.
- Compute dies per wafer, Poisson yield and cost per good die, and explain why very large dies are so expensive and why chiplets exist.

## The Problem

Lessons 01-10 designed hardware with our cost model: adders, multipliers, MACs, arrays, memories. A real chip has billions of transistors. Nobody draws them by hand. How does a description of a MAC become a piece of silicon that does it, and what does it cost to get there?

The answer is a long chain of software tools and factory steps, each with its own physics and its own failure modes. Knowing the chain explains a lot of things you read about chips: why tape-outs are such big events, why a "respin" can delay a product by months, why the largest chips cost thousands of dollars each to make even though a wafer costs "only" tens of thousands, and why the industry is moving to chiplets.

## The Physics

### Printing transistors with light

A chip is made in layers, much like a printed circuit board (Phase 21, Lesson 05) but a thousand times finer. The bottom layers are the transistors themselves: regions of silicon doped n-type and p-type (Phase 11, Lesson 02), with gates of metal over a thin insulator. Above them come ten to fifteen layers of copper wires separated by insulators and joined by vias, from very thin local wires at the bottom to thick global wires at the top.

Each layer's pattern is printed by **lithography**: the wafer is coated with photoresist, exposed to light through a **mask** (projected and shrunk by lenses), developed, and then etched, implanted or plated. The smallest features of leading-edge chips are tens of nanometres, smaller than the wavelength of the 193 nm ultraviolet light long used; the most advanced layers are now printed with extreme ultraviolet (EUV) light at 13.5 nm. A modern chip needs dozens of masks, and a full set for a leading-edge process costs many millions of dollars.

### Why defects kill dies

A speck of dust, a crystal flaw or a small error in a pattern can short two wires or break one. Defects land at random positions on the wafer with some average density `D` per unit area. A die of area `A` works only if no fatal defect lands on it. If defects are random and independent, the number on one die follows a Poisson distribution, and the chance of zero is

```
Y = exp(-D * A)
```

"the yield is e to the minus defect density times area" (the same formula as for PCBs in Phase 21, Lesson 05). With `D = 0.1` defects per cm^2 (a mature process; new processes start much higher), a 1 cm^2 (100 mm^2) die yields `exp(-0.1) = 90.5%`, but an 8 cm^2 (800 mm^2) die yields `exp(-0.8) = 44.9%`. Big dies are punished twice: fewer fit on the wafer, and a smaller fraction of them work.

## The Concept

### Step 1: RTL

Hardware is described at the **register-transfer level**: what each register holds, and what logic computes its next value at every clock edge. Here is our MAC from Lesson 03 in Verilog:

```verilog
module mac8 (
    input  wire        clk,
    input  wire        clear,
    input  wire [7:0]  w,
    input  wire [7:0]  x,
    output reg  [23:0] acc
);
    always @(posedge clk) begin
        if (clear) acc <= 24'd0;
        else       acc <= acc + w * x;
    end
endmodule
```

Read it as hardware, not as a program: `acc` is a 24-bit register (24 flip-flops); at every rising edge of `clk` it loads either zero or `acc + w * x`. The `*` becomes a multiplier, the `+` an adder, the `if` a multiplexer in front of the register. Nothing here runs "in order": all of it exists at once, in silicon. `24'd0` means "a 24-bit decimal zero"; `<=` means "assign at the clock edge".

### Step 2: Verification

Before anything else, the design must be proven correct. Engineers write testbenches that feed millions of random and carefully chosen inputs and compare the outputs with a reference model (exactly as our scripts compared gate-level circuits with Python arithmetic), and use **formal verification** tools that prove properties for *all* inputs. Verification typically takes more effort than design itself, because a bug found after tape-out costs a new mask set and months of delay.

### Step 3: Synthesis

A **synthesis** tool reads the RTL and produces a netlist of **standard cells** from the foundry's library: NAND2, NOR2, XOR2, full-adder cells, flip-flops, each in several drive strengths. It optimises for the timing constraint (the target clock period) and the area, choosing for example a ripple or a prefix adder for `+` (Lesson 01) and a Booth-Wallace multiplier for `*` (Lesson 02).

Our toy synthesizer reads Boolean expressions with `&` (AND), `|` (OR), `^` (XOR) and `~` (NOT) and builds gates. Its one optimisation is **structural hashing**: if the same gate with the same inputs is needed twice, build it once and share it. For a full adder written as

```
sum   = a ^ b ^ c
carry = (a & b) | ((a ^ b) & c)
```

both outputs need `a ^ b`. Built separately: 6 gates. With sharing: 5 gates, the same full adder as Lesson 01. A truth-table check confirms that the gates compute exactly the expressions. Real synthesis does vastly more (Boolean minimisation, technology mapping, retiming), but sharing and checking equivalence are at its core.

### Step 4: Floorplan, placement and the clock tree

The netlist says what connects to what; it says nothing about where. **Floorplanning** puts the big blocks (memories, the MAC array, I/O) on the die. **Placement** puts every standard cell in rows. Placement matters because wires cost delay and energy (Lesson 04): two connected cells far apart need a long wire.

Placement tools minimise an estimate of total wirelength. A common one is the **half-perimeter wirelength** (HPWL): for each net, draw the smallest box containing all its pins and take half its perimeter (width plus height). For a two-pin net that is the Manhattan distance between the pins (the same idea as the ratsnest in Phase 21, Lesson 01).

Our toy placer puts the 20 gates of a 4-bit ripple adder on a 5 x 4 grid at random, then repeatedly tries swapping every pair of cells and keeps a swap if the total HPWL falls. Starting from a random placement with HPWL 63 grid units, the swaps reach 26: **59% less wire**. Real placers handle millions of cells with analytical methods and simulated annealing, but the goal is the same.

Then the **clock tree** is built: a tree of buffers that delivers the clock to every flip-flop with nearly equal delay (skew, Lesson 05), often consuming a large fraction of the chip's power.

### Step 5: Routing and signoff

**Routing** draws the actual wires on the metal layers, respecting the PDK's design rules (minimum widths and spacings, like the PCB rules of Phase 21, Lesson 04, but in nanometres). Then **signoff**: static timing analysis with the real wire delays (does every path meet the clock?), power and IR-drop analysis (does the supply network deliver enough current everywhere?), DRC (does the geometry obey every rule?), and **LVS** (does the drawn layout really implement the netlist?). Only a clean signoff gets to tape-out.

### Step 6: Tape-out, fabrication, test and packaging

**Tape-out** sends the final layout (as a GDSII or OASIS file) to the foundry. The name dates from when designs were shipped on magnetic tape. The foundry makes the masks and runs the wafers through hundreds of process steps over two to three months.

Back from the fab, each die on the wafer is tested with a probe card (**wafer sort**); the wafer is then sawn into dies; good dies are **packaged**: attached to a substrate, connected by wire bonds or by tiny solder bumps ("flip-chip"), and sealed. AI chips are often packaged next to HBM stacks on a silicon interposer. Packaged chips are tested again and sorted ("binned") by the speed and power they achieve.

### Dies per wafer and cost per good die

How many square dies of area `A` fit on a round wafer of diameter `d`? A standard approximation is

```
dies per wafer ≈ pi * (d/2)^2 / A  -  pi * d / sqrt(2 A)
```

"the wafer area divided by the die area, minus the partial dies lost around the edge". For a 300 mm wafer and a 100 mm^2 die: `pi * 150^2 / 100 = 706.9`, minus `pi * 300 / sqrt(200) = 66.6`, gives about 640 dies.

With a wafer cost of \$17,000 (an illustrative leading-edge price) and `D = 0.1` per cm^2:

| Die area | Dies per wafer | Yield | Good dies | Silicon cost per good die |
|---|---|---|---|---|
| 10 mm^2 | 6,858 | 99.0% | 6,790 | \$2.50 |
| 50 mm^2 | 1,319 | 95.1% | 1,255 | \$13.54 |
| 100 mm^2 | 640 | 90.5% | 579 | \$29.35 |
| 200 mm^2 | 306 | 81.9% | 251 | \$67.79 |
| 400 mm^2 | 143 | 67.0% | 96 | \$176.86 |
| 800 mm^2 | 65 | 44.9% | 29 | \$583.90 |

Doubling the die from 400 to 800 mm^2 more than triples the cost per good die. The largest AI chips are close to the maximum size lithography can expose in one shot (the "reticle limit", about 26 x 33 mm = 858 mm^2), which is why they are expensive even before packaging.

### Chiplets

Instead of one 800 mm^2 die, make four 200 mm^2 dies and connect them inside one package. Each small die has a much better yield and can be tested before assembly ("known good die"):

```
monolithic:     $583.90 of silicon per good chip
four chiplets:  4 x $67.79 = $271.15 of silicon + about $150 of advanced packaging = $421.15
```

Even after paying for a more complex package, the chiplet version is cheaper in this example. The price is the extra energy and latency of signals crossing between dies, and the complexity of the package. Chiplets also let a product mix dies made in different processes (logic in the newest node, I/O in an older, cheaper one).

## Build It

Run:

```
uv run python phases/20-chip-design/11-from-rtl-to-the-fab/code/main.py
```

### Step 1: The RTL

The script prints the Verilog MAC. (We do not run Verilog in this course; free simulators such as Icarus Verilog and Verilator can.)

### Step 2: The toy synthesizer

```python
class Synth:
    def __init__(self, lc):
        self.lc = lc
        self.table = {}
        self.count = 0

    def node(self, op, args):
        key = (op, tuple(sorted(args)) if op in ("and", "or", "xor") else tuple(args))
        if key in self.table:
            return self.table[key]
        self.count += 1
        name = f"n{self.count}"
        self.lc.gate(op, list(args), name)
        self.table[key] = name
        return name
```

`node` is the structural hashing: the key is the operation and its inputs (sorted for AND, OR and XOR, whose input order does not matter); an existing gate is reused. `parse_or`, `parse_xor`, `parse_and` and `parse_not` are a small recursive-descent parser: each handles one operator and calls the next tighter-binding one, so `~` binds tightest and `|` loosest. `Evaluate` reuses the same parser but computes values instead of building gates, which gives us an independent reference for `equivalent`. Output: 6 gates without sharing, 5 with, both equivalent; a 2:1 multiplexer in 4 gates.

### Step 3: The toy placer

```python
def hpwl(placement, nets):
    total = 0
    for net in nets:
        xs = [placement[c][0] for c in net]
        ys = [placement[c][1] for c in net]
        total += (max(xs) - min(xs)) + (max(ys) - min(ys))
    return total
```

`nets_of` lists, for each gate that drives other gates, the driver and all its sinks. `improve` tries every pair swap and keeps the improving ones, for up to six rounds. With the fixed random seed, HPWL goes from 63 to 26.

### Step 4: Wafer economics

`dies_per_wafer` and `poisson_yield` implement the two formulas; the script prints the table above.

### Step 5: Chiplets

The same functions for one 800 mm^2 die and four 200 mm^2 dies, plus an assumed \$150 of extra packaging.

## Use It

- **Commercial tools.** Synopsys, Cadence and Siemens EDA sell the synthesis, place-and-route and signoff tools used for almost all commercial chips.
- **Open source.** Yosys (synthesis), OpenROAD (place and route) and open PDKs such as SkyWater SKY130 and GF180MCU let anyone take a design all the way to a layout; shuttle programmes such as Tiny Tapeout share one wafer among hundreds of small student designs for a modest fee.
- **Foundries.** TSMC, Samsung and Intel make leading-edge logic; GlobalFoundries, UMC, SMIC and others make mature nodes, which still build most of the world's chips (microcontrollers, power management, sensors).
- **Packaging** has become a front line: TSMC's CoWoS puts AI dies and HBM on a silicon interposer; AMD and Intel ship processors built from several chiplets.
- **Time scales.** A large chip takes one to three years from architecture to tape-out, a few months in the fab, and months of bring-up afterwards (the chip-level cousin of Phase 21, Lesson 07).

## Common Mistakes

- **Reading Verilog as software.** Every statement describes hardware that exists all the time; `<=` in a clocked block means "this register loads this value at the edge".
- **Assuming synthesis fixes a bad architecture.** Tools optimise gates, not algorithms. A design with a long feedback loop stays slow (Lesson 05).
- **Ignoring wires.** Below about 20 nm, wire delay and energy rival gate delay; placement can make or break timing.
- **Thinking cost grows linearly with die area.** Fewer dies per wafer *and* lower yield make it grow much faster.
- **Under-verifying.** A bug after tape-out costs a new mask set and months; verification is where most of a chip team's effort goes.

## Exercises

1. In the Verilog MAC, what hardware does `if (clear) acc <= 24'd0; else acc <= acc + w * x;` become? List the blocks and their widths.
2. Synthesize `y = (a & b) | (a & c)` with the toy synthesizer. How many gates does it use? Rewrite it as `a & (b | c)` and compare. (This is the distributive law of Phase 14, Lesson 03.)
3. How many 150 mm^2 dies fit on a 300 mm wafer? With `D = 0.2` per cm^2, what is the yield and the number of good dies?
4. A new process starts at `D = 0.5` per cm^2 and improves to 0.1 over two years. For a 400 mm^2 die, how does the cost per good die change (wafer \$17,000)?
5. Harder: modify `improve` into a simple simulated annealing: accept a worse swap with probability `exp(-increase / T)` and lower `T` slowly. Use a seeded random generator so it stays deterministic. Does it beat the greedy result of 26?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| RTL | "the Verilog" | Registers plus the logic computing their next values, in an HDL |
| Synthesis | "compiling the hardware" | Mapping RTL to a netlist of standard cells under timing and area constraints |
| Place and route | "PnR", "the back end" | Positioning every cell and drawing every wire on the metal layers |
| Signoff | "closing the chip" | Final timing, power, DRC and LVS checks before tape-out |
| Tape-out | "sending it to the fab" | Delivering the final layout for mask making |
| Yield | "how many work" | Fraction of good dies; about `exp(-D * A)` for random defects |
| Reticle limit | "the biggest die you can make" | The largest area lithography can expose at once, about 858 mm^2 |
| Chiplet | "multi-die" | A smaller die combined with others in one package to improve yield and mix processes |

## Further Reading

- Neil Weste and David Money Harris, *CMOS VLSI Design: A Circuits and Systems Perspective* (Pearson) — the full flow from cells to layout and manufacturing.
- David Money Harris and Sarah L. Harris, *Digital Design and Computer Architecture* (Morgan Kaufmann), chapter 4 on hardware description languages.
- John L. Hennessy and David A. Patterson, *Computer Architecture: A Quantitative Approach*, chapter 1, the section on the cost of an integrated circuit (dies per wafer and yield).
- [The OpenROAD project](https://openroad.org/) and [Tiny Tapeout](https://tinytapeout.com/) — open-source RTL-to-GDS flows and shared shuttles for real tape-outs.
