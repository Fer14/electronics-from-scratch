# From Gates to Adders

> A chip designer has three currencies: area, time and energy. Counting gates is how you start keeping the books.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lessons 02 (Binary Numbers), 04 (Logic Gates), 05 (CMOS Gates from Transistors) and 07 (Adders); Phase 15 (Sequential Logic), Lesson 03 (Flip-Flops and the Clock)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Chip (integrated circuit) | A small piece of silicon with millions or billions of transistors wired together on it | A whole city printed on a fingernail |
| Die | One rectangle of silicon cut from a wafer, the chip without its package | One biscuit cut from a sheet of dough |
| Area | How much silicon a circuit takes; in this phase we count it in gates | Floor space in a building |
| Delay | How long a signal takes to get through a circuit; we count it in gate delays | Travel time across the city |
| Gate delay | The time one gate takes to react to a change at its input | One person passing a bucket in a bucket chain |
| Logic depth | The largest number of gates a signal passes through from an input to an output | The longest chain of people a bucket must pass through |
| Critical path | The particular path that has the largest delay; it limits how fast the circuit can run | The slowest road between two neighbourhoods |
| Cost model | A simple set of rules that assigns an area, a delay and an energy to every block | A price list for building materials |
| Gate equivalent (GE) | The industry's area unit: the area of one 2-input NAND gate | Measuring flats in "standard rooms" |
| Ripple-carry adder | An adder made of full adders in a row, where each carry waits for the one before | A row of dominoes |
| Carry-select adder | An adder that computes the top half twice (carry 0 and carry 1) and picks the right one when the real carry arrives | Cooking two dinners and serving whichever matches the guest |
| Trade-off | Getting more of one thing by giving up some of another | Paying for an express train to save time |

## Learning Objectives

- Explain why area, delay and energy are the three resources every chip design spends.
- Build a full adder and a ripple-carry adder from gates with `sim.logic`, and verify them on every input.
- Write your own small cost model: count gates (area) and find the longest path (delay) through a gate netlist, and check it against `sim.logic` and `sim.cost`.
- Show that a ripple adder's area and delay both grow linearly with its number of bits, and turn delay into a maximum clock frequency.
- Build a carry-select adder and measure its area-for-speed trade-off.

## The Problem

In Phase 14 you built an adder from gates and watched it add. In Phase 16 you assembled a whole little computer. Those circuits *worked*, and in a simulator that is all we asked. A chip designer asks three more questions about every circuit:

1. **How big is it?** Silicon costs money by the square millimetre (Lesson 11). A circuit twice as big costs about twice as much, and means half as many copies fit on the chip.
2. **How fast is it?** Every gate takes a little time to switch. A long chain of gates limits how often the clock can tick (Lesson 05).
3. **How much energy does it use?** Every gate that switches burns a little energy, and moving data burns much more (Lesson 04). On a phone that is battery life; in a data centre it is the electricity bill and the cooling.

Today's AI chips are, at their heart, enormous numbers of adders and multipliers, fed by memories. Why do they look the way they do? Because their designers spent their area, time and energy budgets in particular ways. To follow their reasoning we need a way to *count*. This lesson builds that habit with the simplest arithmetic circuit there is: the adder.

## The Physics

A logic gate on a chip is a handful of transistors (Phase 14, Lesson 05). A CMOS NAND gate with two inputs uses four transistors: two in parallel pulling the output up to the supply, two in series pulling it down to ground.

### Why gates take time

The output of a gate is a wire that leads to the inputs of the next gates. Those inputs are the gates of MOSFETs, and a MOSFET gate is a tiny capacitor (Phase 12, Lesson 04). To switch the output from 0 to 1, the gate's transistors must charge that capacitance through their own on-resistance. That is an RC charging process (Phase 07, Lesson 04), with a time constant `tau = R * C`. In a modern process, R is a few kilohms and C a fraction of a femtofarad per input, so `tau` is a few picoseconds, and a gate settles in roughly 10-30 ps. In this phase we use one round number for every gate:

```
1 gate delay = 20 ps (picoseconds, 20 * 10^-12 s)
```

A chain of `D` gates then takes `D * 20 ps`. Real gates differ (an XOR is slower than a NAND, a gate driving many inputs is slower than one driving a single input), but the counting idea survives.

### Why gates take area

Each transistor occupies silicon, and the wires connecting them occupy metal layers above. The industry measures logic area in **gate equivalents** (GE): the area of one 2-input NAND gate. On a modern process one GE is a fraction of a square micrometre, so a square millimetre holds a few million of them. A real XOR is about 2 GE, a D flip-flop about 4-6 GE.

### Why gates take energy

Every time a gate's output switches, its load capacitance is charged from the supply and later discharged to ground. The energy taken from the supply for one charge is `C * V^2`, half of it stored in the capacitor and half burnt as heat in the transistors (Phase 07, Lesson 06). With C around 1 fF and V around 0.8 V, that is about 0.6 fJ per switch: tiny, but a chip has billions of gates switching billions of times per second.

### Our teaching cost model

To keep numbers checkable by hand, this phase uses a deliberately simple model, the one in `sim/cost.py`:

| Thing | Area | Delay |
|---|---|---|
| any 2-input gate (AND, OR, NAND, NOR, XOR, XNOR) or NOT | 1 gate | 1 gate delay |
| D flip-flop (one bit of a register) | 6 gates | (it starts a new path) |
| a wire inside a block | free | free |

It is wrong in the details (XOR is not the same size as NAND, wires are not free) and right in the shape: bigger circuits cost proportionally more, longer chains are proportionally slower. Every conclusion in this phase survives using real numbers.

## The Concept

### The full adder, counted

A full adder adds three bits, `a`, `b` and a carry-in `cin`, and produces a sum bit `s` and a carry-out `cout` (Phase 14, Lesson 07):

```
p    = a XOR b          "propagate": exactly one of a, b is 1
s    = p XOR cin
g    = a AND b          "generate": both are 1, so a carry is born here
t    = p AND cin        "the incoming carry is passed on"
cout = g OR t
```

```
   a ---+---[XOR]--- p ---+---[XOR]--- s
   b ---+-+               |
        | |      cin -----+---+
        | |                   |
        | +---[AND]--- g ---[OR]--- cout
        |                     |
        +---------------------+--[AND]--- t  (from p and cin)
```

Its cost in our model:

- **Area:** 5 gates (2 XOR, 2 AND, 1 OR).
- **Delay:** count gates along each path from an input to an output and take the largest.
  - `a` to `s`: XOR, XOR = 2
  - `a` to `cout`: XOR (p), AND (t), OR = 3
  - `cin` to `s`: XOR = 1
  - `cin` to `cout`: AND (t), OR = 2

So the full adder's logic depth is 3, and the path from `cin` to `cout` is 2. That last number matters most, as we are about to see.

### How to find the longest path in any netlist

For any gate-level circuit, the latest time a signal can settle (its **arrival time**) follows one rule:

```
arrival(input) = 0
arrival(output of a gate) = 1 + max(arrival of each of its inputs)
```

"A gate's output is ready one gate delay after the last of its inputs is ready." Apply it to every gate, starting from the inputs, and the largest arrival time at any output is the circuit's **logic depth**. The path that produces it is the **critical path**. This rule is our whole timing model; in Build It we implement it ourselves in ten lines with recursion and memory (we remember each answer so we never compute it twice).

### The ripple-carry adder: linear in everything

Chain N full adders, each passing its carry to the next, and you add two N-bit numbers:

```
  a3 b3        a2 b2        a1 b1        a0 b0
   | |          | |          | |          | |
 +-----+      +-----+      +-----+      +-----+
 | FA3 |<-c3--| FA2 |<-c2--| FA1 |<-c1--| FA0 |<-- 0
 +-----+      +-----+      +-----+      +-----+
  |   |        |            |            |
 cout s3       s2           s1           s0
```

Area: `5 N` gates. Delay: the carry out of bit 0 is ready after 3 gate delays (from `a0, b0`); each later bit adds its `cin -> cout` delay of 2. So the last carry arrives at

```
delay = 3 + 2 * (N - 1) = 2N + 1 gate delays
```

| Bits | Area (gates) | Delay (gate delays) | Time at 20 ps | Max clock |
|---|---|---|---|---|
| 4 | 20 | 9 | 180 ps | 5.6 GHz |
| 8 | 40 | 17 | 340 ps | 2.9 GHz |
| 16 | 80 | 33 | 660 ps | 1.5 GHz |
| 32 | 160 | 65 | 1300 ps | 769 MHz |
| 64 | 320 | 129 | 2580 ps | 388 MHz |

The "max clock" column assumes the adder is the only thing between two registers: the clock period must be at least the delay, so the frequency is at most `1 / delay`. For 32 bits: `1 / (65 * 20e-12 s) = 1 / 1.3e-9 s = 769 MHz`. Double the bits, double the area and (almost) double the delay. Linear growth is good for area; for delay it is a problem, which is why fast processors do not use plain ripple adders for 64-bit numbers.

### Spending area to buy time: the carry-select adder

The top half of an 8-bit ripple adder sits idle, waiting for the carry from the bottom half. There are only two possibilities for that carry: 0 or 1. So build the top half **twice**, once assuming carry 0 and once assuming carry 1, and let both work at the same time as the bottom half. When the real carry arrives, a row of multiplexers (Phase 14, Lesson 08) picks the right answer.

```
   a7..a4, b7..b4 ---> [ 4-bit adder, carry-in 0 ] --- s7..s4 (if c4 = 0) ---+
                  \                                                         [MUX] --- s7..s4, cout
                   --> [ 4-bit adder, carry-in 1 ] --- s7..s4 (if c4 = 1) ---+
                                                                              ^
   a3..a0, b3..b0 ---> [ 4-bit adder, carry-in 0 ] --- s3..s0, c4 ------------+
```

Count it in our model:

- Bottom half: a 4-bit ripple adder, 20 gates; its carry `c4` arrives at 9 gate delays.
- Top half twice: 40 gates. Both copies finish within 9 gate delays too, since they start immediately.
- Multiplexers: 5 bits to choose (s4-s7 and cout), each made of 2 AND and 1 OR = 15 gates, plus one NOT to make "not c4": 16 gates. Through the NOT, an AND and the OR, the selection adds 3 gate delays after `c4` is ready.

Total: `20 + 40 + 16 = 76` gates and `9 + 3 = 12` gate delays, against 40 gates and 17 gate delays for the ripple adder. That is **1.9 times the area for 1.4 times the speed**. Whether that is a good deal depends on what the chip is for; the important thing is that now we can *measure* the deal. Faster adders still (carry-lookahead and parallel-prefix adders such as Kogge-Stone) push the same trade further, reaching a delay that grows with `log2 N` instead of `N`, at the price of more gates and many more wires.

## Build It

Run:

```
uv run python phases/20-chip-design/01-from-gates-to-adders/code/main.py
```

### Step 1: A full adder with sim.logic

```python
fa = LogicCircuit("full adder")
fa.inputs("a", "b", "cin")
full_adder(fa, "a", "b", "cin", "s", "cout")
fa.outputs("s", "cout")
print(fa.format_truth_table())
```

`full_adder` (from `sim.logic`) adds the five gates described above to the circuit. The truth table has 8 rows and matches binary addition: `s` is 1 when an odd number of inputs are 1, `cout` when at least two are.

### Step 2: Our own cost model

```python
def count_gates(lc):
    return sum(1 for gate in lc.gates if gate.op != "buf")


def longest_path(lc):
    driver = {gate.output: gate for gate in lc.gates}
    memo = {}

    def depth(signal):
        if signal not in driver:
            return 0
        if signal not in memo:
            gate = driver[signal]
            own = 0 if gate.op == "buf" else 1
            memo[signal] = own + max(depth(i) for i in gate.inputs)
        return memo[signal]

    return max(depth(name) for name in lc.output_names)
```

`driver` maps every wire to the gate that drives it. A wire that no gate drives (an input or a constant) arrives at time 0. A `buf` is a plain wire inside the netlist and costs nothing. The memo dictionary makes the recursion fast even for thousands of gates. For the full adder it gives 5 gates and depth 3, the same as `fa.gate_count()` and `fa.depth()`.

### Step 3: Ripple adders from 4 to 64 bits

`ripple_adder(bits)` from `sim.logic` builds the chain. For each size, the script prints our counts, the numbers of `sim.cost.adder(bits)` (which uses the formulas `5N` and `2N + 1`), and the period and maximum clock at 20 ps per gate. All three agree, which is the point: the formulas in the cost model are not magic, they are what you get by counting.

### Step 4: Exhaustive test

```python
def add_with(lc, bits, x, y):
    inputs = {f"a{i}": (x >> i) & 1 for i in range(bits)}
    inputs.update({f"b{i}": (y >> i) & 1 for i in range(bits)})
    out = lc.evaluate(inputs)
    return sum(out[f"s{i}"] << i for i in range(bits)) + (out["cout"] << bits)
```

`(x >> i) & 1` extracts bit `i` of `x`. The script adds all 16 x 16 = 256 pairs of 4-bit numbers and compares each with Python's `x + y`: 256 correct.

### Step 5: Watching the ripple

`lc.events(before, after)` replays an input change and records when each wire changes, one gate delay per gate. Changing `0111 + 0000` into `0111 + 0001` makes the carry run through all bits: `s0` settles after 2 gate delays, `s1` after 3, `s2` after 5 and `s3` after 7. Each bit waits 2 more gate delays for its carry, the `cin -> cout` delay of a full adder.

### Step 6: The carry-select adder

`carry_select_adder(8)` builds the bottom half once and the top half twice (with the constants `zero` and `one` as carry-ins), then the multiplexers. The script checks it on all 65,536 pairs and prints:

```
  ripple      :  40 gates, longest path 17 gate delays
  carry-select:  76 gates, longest path 12 gate delays
  1.90x the area for 1.42x the speed
```

### Step 7: The lab

The script loads `lab/task.json` and checks its reference solution with `sim.lab.evaluate`. For a truth-table goal the value printed is the number of wrong output bits (0 means perfect).

## Use It

- **Real adders.** A modern CPU's 64-bit integer adder finishes in a fraction of a clock cycle at 4-5 GHz; it is a parallel-prefix adder, not a ripple adder. Small, slow microcontrollers and low-power chips often use ripple adders because they are the smallest.
- **Synthesis tools choose for you.** When you write `assign s = a + b;` in Verilog (Lesson 11), the synthesis tool picks an adder architecture from a library according to your timing constraint: ripple if there is time to spare, faster and larger structures if not. Exactly our trade-off, made automatically.
- **Gate counts in the wild.** Chip area is often quoted in gate equivalents: a small 32-bit microcontroller core is a few tens of thousands of GE; a large AI accelerator has billions of transistors, hundreds of millions of GE.
- **The 20 ps assumption.** Real gate delays depend on the process, the supply voltage and the load. Designers measure in units such as FO4 (the delay of an inverter driving four copies of itself), about 10-15 ps in recent processes. Our 20 ps is a round number in that range.

## Try It in the Lab

Open "Finish the 4-bit adder". Three gates are missing from a 4-bit ripple-carry adder: the sum gate of bit 1, the gate that passes the incoming carry on in bit 2, and the generate gate of bit 3. Choose an XOR, AND or OR for each so that all 256 sums are right, with at most 20 gates and a critical path of 9 gate delays. Before running, write the five equations of a full adder and decide which equation each slot implements.

## Common Mistakes

- **Counting only area.** A tiny circuit that is too slow fails just as surely as a big circuit that is too large. Always count both.
- **Taking the shortest path instead of the longest.** A gate's output is ready only when its *last* input arrives. Delay is the *maximum* over paths.
- **Forgetting the carry-in path.** A full adder's own depth is 3, but in a chain what repeats is the 2-gate `cin -> cout` path; that is where `2N + 1` comes from.
- **Trusting the teaching model too far.** Real XOR gates are bigger and slower than NANDs, and long wires add delay. Use the model to compare designs, not to promise a frequency.
- **Thinking faster is always better.** If the adder is not on the critical path of the whole chip, making it faster wastes area.

## Exercises

1. Using `area = 5N` and `delay = 2N + 1`, compute the area and delay of a 24-bit ripple adder and its maximum clock at 20 ps per gate.
2. A half adder is one XOR and one AND. If bit 0 of a ripple adder uses a half adder (its carry-in is always 0), how many gates does an N-bit adder need? Does the delay change?
3. Build a 16-bit carry-select adder by hand on paper: 8-bit bottom half, two 8-bit top halves and multiplexers. Compute its area and delay in our model and compare with the 16-bit ripple adder.
4. Call `carry_select_adder(16)` in the script (it splits in two halves) and check your numbers from exercise 3 with `count_gates` and `longest_path`.
5. Harder: split a 16-bit adder into four 4-bit blocks, where blocks 2, 3 and 4 are each computed twice and chosen by the carry from the block before. Estimate its area and delay. Is the extra area worth it compared with the two-block version?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Area | "how big it is" | Silicon used; in this phase, the number of gates (flip-flop = 6) |
| Gate delay | "one gate's worth of time" | The time for one gate to respond, about 20 ps in our pretend process |
| Logic depth | "how many levels" | The largest number of gates between an input and an output |
| Critical path | "the slow path" | The path with the largest delay; it sets the minimum clock period |
| Ripple-carry adder | "the simple adder" | N full adders in a chain: 5N gates, 2N + 1 gate delays |
| Carry-select adder | "compute both and pick" | Duplicates the upper part for carry 0 and 1, trading area for delay |
| Cost model | "back-of-the-envelope numbers" | Rules assigning area, delay and energy to blocks so designs can be compared before they exist |

## Further Reading

- David Money Harris and Sarah L. Harris, *Digital Design and Computer Architecture* (Morgan Kaufmann), chapter 5 on arithmetic circuits: ripple, carry-lookahead and prefix adders.
- Neil Weste and David Money Harris, *CMOS VLSI Design: A Circuits and Systems Perspective* (Pearson), chapters on delay (logical effort) and datapath adders.
- John L. Hennessy and David A. Patterson, *Computer Architecture: A Quantitative Approach* (Morgan Kaufmann), appendix J on computer arithmetic.
- [Ben Eater, "Building an 8-bit breadboard computer"](https://eater.net/8bit) — an adder you can watch ripple on real chips.
