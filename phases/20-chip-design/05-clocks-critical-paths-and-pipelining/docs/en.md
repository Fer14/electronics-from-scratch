# Clocks, Critical Paths and Pipelining

> The clock can only tick as fast as the slowest stretch of logic between two registers. Pipelining cuts the stretches shorter; feedback loops refuse to be cut.

**Type:** Build
**Prerequisites:** Phase 20 (Chip Design), Lessons 01-03; Phase 15 (Sequential Logic), Lessons 03 (Flip-Flops and the Clock), 04 (Registers) and 07 (Timing and Metastability)
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Clock | A signal that ticks at a fixed rate; registers update on each tick | The beat a rowing crew pulls to |
| Clock period | The time between two ticks | The time between two strokes of the oars |
| Clock frequency | Ticks per second, `1 / period` (1 GHz = a billion ticks per second, period 1 ns) | Strokes per minute |
| Register-to-register path | The logic between the output of one register and the input of the next | One leg of a relay race |
| Critical path | The slowest register-to-register path; it sets the minimum clock period | The slowest runner sets the team's pace |
| Setup time | How long before the clock edge a register's input must be stable | Being on the platform before the train doors close |
| Clock-to-output delay | How long after the edge a register's output changes | The time for the doors to open after the train stops |
| Pipelining | Inserting registers in a long path so each piece is shorter and the clock can tick faster | Splitting one long relay leg into two shorter ones |
| Pipeline stage | One piece of logic between two pipeline registers | One station on an assembly line |
| Latency | How long one piece of data takes from input to output (cycles, or time) | How long one car takes to go down the whole assembly line |
| Throughput | How many results come out per second | How many cars leave the factory per hour |
| Feedback loop | A path that comes back to where it started, through a register | A dog chasing its own tail |
| Timing closure | Getting every path of a design to fit in the clock period | Making every train connection in a timetable |

## Learning Objectives

- Explain why the clock period must be at least the delay of the slowest register-to-register path, and compute the maximum frequency from a critical path.
- Use `sim.cost.Design` to measure a datapath's critical path, area and latency, and see how a pipeline register changes all three.
- Pipeline a datapath to meet a target clock period without exceeding an area budget.
- Distinguish throughput from latency, and explain why pipelining raises the first but not (usually) the second.
- Show, with a gate-level simulation, why adding a register inside an accumulator's feedback loop changes what it computes.

## The Problem

Your 8-bit MAC from Lesson 03 works, but its critical path is 91 gate delays: 1.82 ns at 20 ps per gate. If it is the slowest thing on the chip, the clock can tick at most 549 million times per second. Your competitor's chip runs at 1 GHz with the same multipliers. How?

The answer is **pipelining**, the idea behind every assembly line: split the work into stages and let each stage work on a different item at the same time. A car factory does not wait for one car to be finished before starting the next. But pipelining has costs (more registers, more area, more latency) and one hard limit: you cannot pipeline a loop whose next step needs the result of this one, at least not without changing what it computes. The MAC has exactly such a loop.

## The Physics

### What happens between two clock edges

Consider two registers with some logic between them:

```
   [register A] --- logic (D gate delays) --- [register B]
        ^                                          ^
      clock                                      clock
```

At a rising clock edge, register A captures its input and, a moment later (the **clock-to-output delay**), its output changes. The change ripples through the logic. Each gate needs a little time to charge its output wire (Lesson 01). After the logic's delay, the result reaches register B's input. Register B needs that input to be stable a short **setup time** before the *next* clock edge, or it may capture garbage (Phase 15, Lesson 07). So:

```
clock period >= clock-to-output + logic delay + setup time
```

"The period must be long enough for the register to launch the data, the logic to compute it, and the next register to be ready to catch it." In our teaching model we fold the register overheads into the gate counts and simply say:

```
clock period >= (critical path in gate delays) * 20 ps
frequency    <= 1 / period
```

Real designs also add margin for **clock skew** (the clock edge does not reach every register at exactly the same moment) and for variations in voltage and temperature.

### Why we cannot just make the clock faster

If you raise the clock frequency beyond what the critical path allows, nothing physical breaks immediately: registers capture whatever value happens to be on their inputs at the edge, which may be half-computed. The chip computes wrong answers. Overclockers find the limit by experiment; chip designers find it by **static timing analysis**: computing the arrival time of every signal, exactly as we do with our cost model.

## The Concept

### Measuring a datapath

Our 8-bit MAC datapath, drawn as blocks between registers:

```
   in --[R_IN 16b]--> operands --[MUL 8x8: 42]--> product --[ADD 24b: 49]--> sum --[ACC 24b]--> acc
```

The only register-to-register path goes from R_IN through MUL and ADD into ACC: `42 + 49 = 91` gate delays.

```
period    = 91 * 20 ps = 1820 ps = 1.82 ns
frequency = 1 / 1.82 ns = 549 MHz
area      = 96 (R_IN) + 344 (MUL) + 120 (ADD) + 144 (ACC) = 704 gates
```

### Inserting a pipeline register

Put a 16-bit register between the multiplier and the adder:

```
   in --[R_IN]--> --[MUL: 42]--> --[R_MID 16b]--> --[ADD: 49]--> --[ACC]-->
```

Now there are two register-to-register paths: R_IN to R_MID (42) and R_MID to ACC (49). The slowest is 49:

```
period    = 49 * 20 ps = 980 ps
frequency = 1 / 0.98 ns = 1020 MHz
area      = 704 + 96 = 800 gates
latency   = 3 cycles instead of 2
```

For 14% more area, the clock is 1.86 times faster. Each MAC result now takes one more cycle to come out, but a new MAC *starts* every cycle, so the number of MACs per second (the **throughput**) almost doubles.

### Throughput versus latency

| Design | Period | MACs per second | Time for one MAC to get through |
|---|---|---|---|
| unpipelined | 1.82 ns | 0.55 billion | 2 cycles = 3.64 ns |
| 2-stage | 0.98 ns | 1.02 billion | 3 cycles = 2.94 ns |

Here even the latency improved a little in nanoseconds, because the stages are well balanced (42 and 49) and the extra cycle is shorter. In general pipelining raises throughput and leaves latency about the same or slightly worse, because each register adds its own overhead and the stages are never perfectly balanced. For an accelerator that streams billions of MACs, throughput is what matters.

### How far can you go?

Split the multiplier itself into more stages (`sim.cost.pipelined_multiplier`): with `s` stages, each stage has `ceil(42 / s)` gate delays, and each stage boundary costs a 16-bit register (96 gates).

| Stages | Stage delay | Max clock | Multiplier area |
|---|---|---|---|
| 1 | 42 | 1.19 GHz | 440 |
| 2 | 21 | 2.38 GHz | 536 |
| 3 | 14 | 3.57 GHz | 632 |
| 4 | 11 | 4.55 GHz | 728 |
| 6 | 7 | 7.14 GHz | 920 |

On paper you could go on forever. In practice three things stop you:

1. **Register overhead.** Each register's clock-to-output and setup time (in real silicon, roughly the delay of 3-4 gates) is paid once per stage. With 7 gates of logic per stage, overhead would be a third of the period.
2. **Power.** Every register bit toggles its clock input every cycle, and higher frequency means more switching per second. Clock networks alone can take a third of a chip's power.
3. **Loops.** Some paths come back to where they started, and those cannot be split.

### The loop that refuses to be cut

The accumulator computes `acc = acc + product`. Draw it:

```
             product
                |
                v
   +-----> [ ADD 24b: 49 ] ----> sum ----> [ ACC register ] ----+
   |                                                            |
   +------------------------------------------------------------+
                                acc
```

The adder's output goes into the register and comes back as the adder's input. The path from ACC through ADD back to ACC is 49 gate delays, and no matter how much you pipeline the multiplier, that loop stays 49 long. Without any register in the loop, the circuit is not even well defined (the adder would be adding its own output to itself continuously), and our cost model refuses it: "combinational loop through 'acc': put a register in the loop".

What if we put a second register in the loop, hoping to split it as we did the multiplier (for example, half of the adder before the extra register and half after)? Timing would look better, but look at what the circuit now *computes*. Even without splitting the adder, a second register in the loop changes the answer: Each sum now comes back two cycles later instead of one. Feed it the numbers 5, 3, 10, 1, 7, 2:

```
want (running sum):         5,  8, 18, 19, 26, 28
one register in the loop:   5,  8, 18, 19, 26, 28
two registers in the loop:  0,  5,  3, 15,  4, 22
```

With two registers, the loop holds two separate running sums that take turns: one adds the 1st, 3rd and 5th inputs (`5 + 10 + 7 = 22`) and the other adds the 2nd, 4th and 6th (`3 + 1 + 2 = 6`). It is a different calculation. The final answer can be recovered by adding the two sums at the end (`22 + 6 = 28`), and real designs do exactly that on purpose: they use several accumulators in parallel and combine them at the end. But that is a change of algorithm, not "just pipelining".

So the accumulator loop sets a floor on the clock period: one adder of the accumulator's width. That is one reason accumulators are designed carefully (carry-save forms, split accumulators), and why the accumulator width from Lesson 03 matters for speed, not only area.

### A pipelining recipe

To meet a target period with the fewest registers:

1. Compute the delay of every block.
2. Walk along the datapath adding delays; when the next block would push the sum over the target, put a register before it and restart the sum.
3. Check loops separately: every loop must fit in one period by itself.
4. Add up the area of the registers you inserted and check the budget.

## Build It

Run:

```
uv run python phases/20-chip-design/05-clocks-critical-paths-and-pipelining/code/main.py
```

### Step 1: The unpipelined MAC

```python
def mac_datapath(split):
    d = cost.Design("MAC datapath")
    d.add("R_IN", cost.register(16), "in", "operands")
    d.add("MUL", cost.multiplier(8), "operands", "product")
    if split:
        d.add("R_MID", cost.register(16), "product", "product_q")
        d.add("ADD", cost.adder(24), "product_q", "sum")
    else:
        d.add("ADD", cost.adder(24), "product", "sum")
    d.add("ACC", cost.register(24), "sum", "acc")
    return d
```

A `Design` is a graph: `d.add(name, block, from_node, to_node)`. Blocks with latency (registers) end a timing path and start a new one. `describe` prints area, critical path, period, `max_clock_mhz()` and `latency()`: 704 gates, 91 gate delays, 1820 ps, 549 MHz, 2 cycles.

### Step 2: One pipeline register

`mac_datapath(split=True)`: 800 gates, 49 gate delays, 980 ps, 1020 MHz, 3 cycles.

### Step 3: Pipelining the multiplier

`cost.pipelined_multiplier(8, stages)` for 1 to 6 stages; the script prints the table above.

### Step 4: The loop in the cost model

```python
loop = cost.Design("loop without a register")
loop.add("ADD", cost.adder(24), "acc", "acc")
try:
    loop.critical_path()
except ValueError as error:
    print(f"  no register in the loop: {error}")
```

An adder whose output is its own input, with no register, is a combinational loop; `critical_path` raises an error. With one or two registers in the loop, the path is 49: the adder itself.

### Step 5: The loop at gate level

`accumulator(registers_in_loop)` builds an 8-bit ripple adder whose output passes through one or two registers before returning to its input. `run_accumulator` clocks it once per input with `lc.step`. One register gives the running sum; two registers give two interleaved sums.

### Step 6: Throughput and latency

From the critical path and the latency in cycles: 0.55 versus 1.02 billion MACs per second, and 3.64 versus 2.94 ns for the first result.

### Step 7: The lab

The script tries five combinations of wires and registers in the lab's three slots and prints the critical path, the area and the verdict. Exactly two of them pass.

## Use It

- **CPU pipelines.** A modern CPU core has 10-20 pipeline stages (fetch, decode, rename, issue, execute, write back...). The Pentium 4 pushed to over 30 stages to reach high clock frequencies and paid in power and in the cost of flushing a long pipeline on a wrong branch prediction; later designs pulled back.
- **Floating-point units** are typically pipelined over 3-5 cycles: a new multiply-add can start every cycle, each takes 4 cycles to finish.
- **AI accelerators** usually run at modest clocks (around 1 GHz) with very wide arrays, because a higher clock costs power while more MACs cost only area. Their MACs are pipelined so that the accumulator loop is the only single-cycle path.
- **Timing closure** is a major phase of real chip design. Synthesis and place-and-route tools report "slack" (how much time a path has to spare) for millions of paths; engineers fix negative slack by restructuring logic, resizing gates, or adding pipeline stages (Lesson 11).
- **Retiming** is an automatic technique that moves registers across logic to balance stages without changing the function.

## Try It in the Lab

Open "Pipeline the datapath to meet the clock". A 16-bit datapath runs through two 8-bit adders (17 gate delays each), a 4 x 4 multiplier (18) and a 16-bit adder (33), between an input and an output register. The target is 1.25 GHz: 800 ps, so at most 40 gate delays per stage. Three slots sit between the blocks; each takes a wire (free) or a 16-bit register (96 gates). The total must stay within 640 gates. Use the recipe: walk along the path adding delays. How many registers are strictly necessary, and is there more than one way to place them?

## Common Mistakes

- **Taking the sum of all blocks as the critical path.** Only the logic between two consecutive registers counts.
- **Forgetting that every register costs area and power.** Pipelining is not free; the lab's area budget makes that concrete.
- **Pipelining a loop.** A register added inside a feedback loop changes the computation. Loops must fit in one cycle, or the algorithm must change (for example to several interleaved accumulators added at the end).
- **Confusing latency with throughput.** A deeper pipeline produces more results per second but each result takes as many or more cycles to emerge.
- **Unbalanced stages.** The clock is set by the slowest stage. Splitting a 42-gate path into stages of 40 and 2 gains almost nothing.

## Exercises

1. A path of 75 gate delays sits between two registers. At 20 ps per gate, what is the maximum clock? Where would you put one register to make it as fast as possible, and what is the new maximum clock?
2. A multiplier of 42 gate delays is split into 4 stages. If each register adds 3 gate delays of overhead, what is the real stage delay and maximum clock?
3. The 2-register accumulator of Step 5 is fed 1, 2, 3, 4, 5, 6, 7, 8. What two sums does it hold at the end, and how do you combine them?
4. In `mac_datapath`, change the accumulator width to 32 bits. Which path becomes critical in the pipelined version, and what is the new maximum clock?
5. Harder: design a 3-stage version of the 8-bit MAC (split the multiplier into two stages plus the adder stage). Build it with `cost.Design`, report area, critical path and latency, and explain why the clock does not improve beyond the accumulator's adder.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Clock period | "the cycle time" | Time between clock edges; must exceed the slowest register-to-register delay |
| Critical path | "the long pole" | The register-to-register path with the largest delay |
| Pipelining | "adding stages" | Inserting registers to split long paths, raising frequency and throughput at the cost of area and latency |
| Latency | "how long one takes" | Cycles (or time) from input to output for one item |
| Throughput | "how many per second" | Results per unit time; one per cycle in a full pipeline |
| Feedback loop | "a recurrence" | A path from a register back to itself; it cannot be shortened by adding registers without changing the function |
| Timing closure | "making timing" | The work of getting every path to fit the target clock period |

## Further Reading

- David Money Harris and Sarah L. Harris, *Digital Design and Computer Architecture* (Morgan Kaufmann), sections on timing of sequential logic and pipelining.
- John L. Hennessy and David A. Patterson, *Computer Organization and Design* (Morgan Kaufmann), chapter on pipelining.
- Neil Weste and David Money Harris, *CMOS VLSI Design* (Pearson), chapters on sequential circuits and timing analysis.
- Charles E. Leiserson and James B. Saxe, "Retiming Synchronous Circuitry", *Algorithmica*, 1991 — moving registers without changing the function.
