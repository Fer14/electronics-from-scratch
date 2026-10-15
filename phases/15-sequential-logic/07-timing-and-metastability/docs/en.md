# Timing and Metastability

> A flip-flop needs its input to sit still for a moment around the clock edge. Respect that window and the design runs at a known speed; violate it and the flip-flop can balance on a knife edge for an unpredictable time.

**Type:** Learn
**Prerequisites:** Phase 14 (Digital Logic), Lesson 05 (CMOS Gates from Transistors) and Lesson 07 (Adders), Phase 15 (Sequential Logic), Lessons 01 and 03 (Memory from Feedback, Flip-Flops and the Clock)
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Clock-to-Q delay (tcq) | Time from the clock edge until the flip-flop's output shows the new value | The moment between the starter's pistol and the runner moving |
| Propagation delay (tpd) | Time for a change to travel through combinational logic | The time a message takes to cross town |
| Setup time (tsu) | How long before the clock edge the input must already be stable | Being on the platform before the train's doors close |
| Hold time (th) | How long after the clock edge the input must stay stable | Not pulling your bag out until the doors have shut |
| Critical path | The slowest register-to-register path | The slowest leg of a relay race |
| Maximum clock frequency (fmax) | The fastest clock at which every path still meets setup | The fastest tempo the slowest musician can follow |
| Slack | How much time is left over on a path; negative slack means a violation | Arriving 5 minutes early (positive) or late (negative) |
| Clock skew | Difference in arrival time of the same clock edge at different flip-flops | Two clocks in a house that disagree by a few seconds |
| Metastability | A flip-flop stuck temporarily between 0 and 1 because its input changed inside the setup/hold window | A coin landing on its edge and wobbling before it falls |
| Resolution time | How long a metastable flip-flop takes to fall to a clean 0 or 1 | How long the wobbling coin takes to fall |
| Synchronizer | Two (or more) flip-flops in a row that give a metastable value time to resolve before anyone uses it | A waiting room where the coin can finish falling |
| MTBF | Mean time between failures: the average time between two synchronizer failures | How often, on average, the coin is still wobbling when you look |
| Clock domain | The set of flip-flops driven by one clock | Everyone living by one town's church bell |

## Learning Objectives

- Write the setup constraint `T >= tcq + tlogic + tsu` and compute the maximum clock frequency of a path.
- Use the logic depth from the simulator to estimate the critical path of an adder between two registers.
- Explain the hold constraint and how clock skew helps setup but hurts hold.
- Explain metastability physically, and measure the resolution time constant `tau` of a CMOS latch in the circuit simulator.
- Compute the MTBF of a single flip-flop and of a two-flip-flop synchronizer, and explain why the second is so much safer.

## The Problem

Lesson 03 promised that synchronous design hides all the messy timing: "as long as the logic settles before the next edge, nothing else matters". This lesson turns "as long as" into numbers. How fast can a clock go before the logic fails to settle? What happens if a signal arrives too late, or too early? And what about signals that come from outside the clocked world (a push button, a sensor, another chip with its own clock), which can change at any instant, including exactly at a clock edge?

The first question decides the speed of every processor: when a datasheet says 3.2 GHz, it means the slowest path between any two registers fits in 312 ps. The last question is behind some of the nastiest, rarest bugs in electronics: a system that fails once a week for no apparent reason. Both have quantitative answers.

## The Physics

### Why a flip-flop has a setup time

A flip-flop is two latches (Lesson 03). At the rising edge, the master closes and its feedback loop must lock onto the value `d` had just before. Locking takes time: the master's internal nodes must have charged to the new value (through transistor resistances and capacitances, Phase 07) before the loop closes. If `d` changed too recently, the internal node is still on its way, partway between 0 and 1, when the loop closes. That is the **setup time**: the minimum time `d` must have been stable before the edge. Similarly, closing the master's input switch is not instantaneous, so `d` must stay stable briefly after the edge: the **hold time**.

### Why violating it causes metastability

What happens if the loop closes while its node is exactly at, or very near, the switching point? Lesson 01 showed that a bistable loop has an **unstable equilibrium** in the middle, like a ball on a hilltop. The loop does not choose immediately. It amplifies the small difference between where it is and the exact balance point, and that difference grows **exponentially**:

```
v(t) = v(0) x e^(t / tau)
```

Read it: "the distance from balance multiplies by e (2.718) every tau seconds". Here `v(0)` is the small initial imbalance and `tau` (the Greek letter tau) is the loop's time constant, roughly the node capacitance divided by the transistors' combined transconductance `gm` (how much current changes per volt, Phase 12, Lesson 07):

```
tau ≈ C / (gm_n + gm_p)
```

The time to resolve to a full logic level is the time for `v` to grow from `v(0)` to about half the supply:

```
t_resolve = tau x ln(V_half / v(0))
```

`ln` is the natural logarithm (the inverse of `e^x`). This formula says: the closer to balance it starts, the longer it takes, but only **logarithmically** longer. Ten times closer adds just `tau x ln(10) = 2.3 tau`. And it can, in principle, take arbitrarily long if `v(0)` is arbitrarily small. While it is undecided, its output sits at an intermediate voltage, or rises late, and the logic it drives may read 0 in one place and 1 in another. That state is **metastability**.

Our circuit simulator measures this directly. Two CMOS inverters (`k = 1 mA/V^2`, 1 pF per node) are released from 2.5 V plus or minus a small imbalance:

```
  start   100 mV away from balance -> resolves in 944.6 ps
  start    10 mV away from balance -> resolves in 1.686 ns
  start     1 mV away from balance -> resolves in 2.427 ns
  start   100 uV away from balance -> resolves in 3.169 ns
  start    10 uV away from balance -> resolves in 3.91 ns
  start     1 uV away from balance -> resolves in 4.651 ns
```

Every factor of 10 closer adds the same 741 ps, so `tau = 741 ps / ln(10) = 322 ps`. The hand estimate: at 2.5 V each transistor has `gm = k (VGS - Vth) = 0.001 x 1.5 = 1.5 mS`, so `tau ≈ 1 pF / 3 mS = 333 ps`. They agree within 4 %. Real flip-flops in modern processes have `tau` of 10-50 ps; old 74HC parts have a few nanoseconds.

## The Concept

### The setup constraint

Consider the basic synchronous path: a flip-flop launches data at a clock edge, the data passes through combinational logic, and another flip-flop captures it at the **next** edge.

```
   launch                                         capture
  +------+        +---------------------+        +------+
  | DFF  |--Q---->| combinational logic |---D--->| DFF  |
  +--^---+        +---------------------+        +--^---+
     |                                              |
    clk ------------------------------------------- clk

 time:  edge 1           ...                        edge 2
        |<- tcq ->|<----- tlogic ----->|<- tsu ->|
        |<------------------ T ----------------->|
```

After edge 1, the launching flip-flop's output changes after `tcq`. The change takes `tlogic` (the critical path) to reach the capture flip-flop's input. And it must arrive `tsu` before edge 2. Say it as a sentence: "the clock period must be at least the clock-to-Q delay plus the logic delay plus the setup time".

```
T >= tcq + tlogic + tsu
fmax = 1 / (tcq + tlogic + tsu)
```

Worked example: an 8-bit ripple-carry adder between two registers. The simulator's `ripple_adder(8)` has a logic depth of 17 gate delays.

With 74HC-like parts at 5 V (gate 8 ns, tcq 15 ns, setup 5 ns, illustrative values close to those of a 74HC74 flip-flop):

```
T = 15 ns + 17 x 8 ns + 5 ns = 15 + 136 + 5 = 156 ns
fmax = 1 / 156 ns = 6.4 MHz
```

With a modern chip (gate 15 ps, tcq 40 ps, setup 25 ps):

```
T = 40 ps + 17 x 15 ps + 25 ps = 40 + 255 + 25 = 320 ps
fmax = 1 / 320 ps = 3.1 GHz
```

Same circuit, same depth; the technology changes the gate delay by a factor of 500. Notice that most of the period is the adder: to go faster, shorten the critical path (a lookahead adder, Phase 14, Lesson 07) or cut it in two with a register in the middle, which is **pipelining** (Phase 20, Lesson 05).

The **slack** of a path is how much time is left: `slack = T - (tcq + tlogic + tsu)`. Timing analysis tools compute the slack of every one of the millions of paths in a chip and report the worst. Negative slack means the chip will not work at that clock.

### The hold constraint

The setup constraint protects against data arriving **too late**. The hold constraint protects against data arriving **too early**. At edge 1, the capture flip-flop is grabbing the **old** value from its input. At the same edge, the launching flip-flop starts sending the **new** value. If the new value races through a very short path and reaches the capture flip-flop before its hold time is over, it corrupts the capture:

```
tcq + tlogic_min >= th
```

where `tlogic_min` is the **shortest** path. Note: this constraint does not involve the clock period at all. A hold violation cannot be fixed by slowing the clock; the only cure is to add delay to the short path (tools insert buffers).

### Clock skew

The clock edge does not arrive at every flip-flop at exactly the same instant: wires have different lengths and the buffer tree is not perfectly balanced. Let **skew** be how much later the edge arrives at the capture flip-flop than at the launching one.

- **Setup gets easier:** the capture edge is later, so the data has `T + skew` to arrive: `T >= tcq + tlogic + tsu - skew`.
- **Hold gets harder:** the capture flip-flop holds the old value until later, giving the new data more time to sneak in: `tcq + tlogic_min >= th + skew`.

Numbers (path `tcq = 40 ps`, `tlogic = 270 ps`, `tsu = 25 ps`, `th = 15 ps`, shortest logic 10 ps):

```
skew    0 ps: T >= 335 ps (2.99 GHz);  hold slack 40 + 10 - 15 = +35 ps   ok
skew  +20 ps: T >= 315 ps (3.17 GHz)
skew  -20 ps: T >= 355 ps (2.82 GHz)
skew  +60 ps: hold slack 40 + 10 - (15 + 60) = -25 ps                     HOLD VIOLATION
```

That last line is why the "gate the clock with an AND" trick of Lesson 04 is dangerous: it adds skew to one register. Clock trees are designed to keep skew to a few picoseconds, and timing tools check both constraints on every path.

### Signals from outside: why metastability cannot be avoided

Inside one clock domain, the setup and hold constraints can be met by design. But a signal from a push button, a sensor or another clock domain is **asynchronous**: it can change at any moment. Sooner or later it will change inside some flip-flop's setup/hold window. There is no circuit that always resolves in bounded time (a deep result, sometimes called Buridan's principle after the donkey that starved between two equal bales of hay). We cannot prevent metastability; we can only make it **rare enough**.

### How rare? The MTBF formula

Model it with the physics above. A flip-flop goes metastable when the data edge falls inside a small window `W` around the clock edge (a fraction of a nanosecond). If the data changes `f_data` times per second, and each change lands at a random time within a clock period `1 / f_clk`, the chance that one change lands in the window is `W x f_clk`. So metastable events happen at a rate of `f_data x f_clk x W` per second.

Most of those resolve quickly. Only those that started very close to balance take longer than the time `t_r` we allow before using the output, and the exponential law says that fraction is `e^(-t_r / tau)`. The rate of **failures** is the product, and the mean time between failures is its inverse:

```
MTBF = e^(t_r / tau) / (W x f_clk x f_data)
```

Read it: "the mean time between failures grows exponentially with the time you allow for resolution, and shrinks in proportion to how often the clock ticks and the data changes".

The script checks this reasoning with a Monte Carlo experiment: 2 million data edges at random times within a 10 ns clock period, each one starting from an imbalance proportional to how close it fell to the clock edge. The number that fail to resolve within 0.5, 1.0 and 1.5 ns matches the formula's prediction (8497 against 8465, 1844 against 1791, 357 against 379; the small differences are random sampling).

### One flip-flop versus a synchronizer

Take `f_clk = 100 MHz`, data changing a million times per second, `W = 0.2 ns`, and our simulated `tau = 322 ps`.

**One flip-flop**, whose output feeds logic that leaves it 5 ns to resolve:

```
MTBF = e^(5 ns / 0.322 ns) / (0.2e-9 x 1e8 x 1e6)
     = e^15.5 / 2e4
     = 5.6e6 / 2e4
     ≈ 280 s
```

A failure every 4.6 minutes. Unusable.

**Two flip-flops in a row (a synchronizer).** The first one may go metastable, but nobody looks at its output except the second flip-flop, one full clock period (10 ns) later. Now `t_r = 5 + 10 = 15 ns`:

```
MTBF = e^(15 / 0.322) / 2e4 = e^46.6 / 2e4 ≈ 8.6e15 s ≈ 270 million years
```

Ten extra nanoseconds multiplied the MTBF by `e^(10 / 0.322) = e^31 ≈ 3 x 10^13`. That exponential is why the two-flip-flop synchronizer is the universal rule:

```
 async_in --->[DFF]--- meta --->[DFF]--- sync_out ---> (safe to use)
               ^                  ^
              clk                clk
```

**Every asynchronous input passes through at least two flip-flops before any logic uses it.** Very fast or very critical systems use three. The cost is one or two cycles of extra latency.

### Crossing between clock domains

A synchronizer handles one bit. A multi-bit value (a counter, an address) crossing from one clock domain to another cannot simply go through one synchronizer per bit: the bits may resolve on different cycles and the receiver sees a mixture of old and new. Standard solutions: send the value in **Gray code** (only one bit changes per step, so a mixture is always either the old or the new value), use a handshake (a synchronized "data valid" flag while the data bus is held stable), or use an asynchronous FIFO, which combines both ideas.

## Build It

The script `code/main.py` computes timing budgets, measures metastability in the circuit simulator and evaluates the MTBF formula.

### Step 1: The setup budget

```python
def fmax(tcq, tlogic, tsetup, skew=0.0):
    period = tcq + tlogic + tsetup - skew
    return period, 1 / period

depth = ripple_adder(8).depth()
```

`ripple_adder(8)` is a ready-made gate-level 8-bit adder in `sim.logic`, built from the same full adders as Phase 14, Lesson 07. Its `depth()` is the critical path in gate delays (17). The script multiplies by a gate delay for each technology.

### Step 2: Skew and hold

The same function with a skew argument, and the hold slack `tcq + t_min - (t_hold + skew)` for two skews. The output shows setup improving and hold breaking as skew grows.

### Step 3: Metastability in the analog simulator

```python
def latch_resolution(imbalance, vdd=5.0, load=1e-12):
    c = Circuit("cross-coupled inverters")
    c.voltage_source("VDD", "vdd", "0", vdd)
    for i, (node, other) in enumerate([("q", "qb"), ("qb", "q")]):
        c.pmos(f"MP{i}", d=node, g=other, s="vdd", vth=1.0, k=1e-3, lam=0.02)
        c.nmos(f"MN{i}", d=node, g=other, s="0", vth=1.0, k=1e-3, lam=0.02)
    c.capacitor("C0", "q", "0", load, v0=vdd / 2 + imbalance)
    c.capacitor("C1", "qb", "0", load, v0=vdd / 2 - imbalance)
    t = c.transient(t_stop=40e-9, dt=0.02e-9)
    return t.time_to_cross("q", 0.8 * vdd)
```

Two inverters, each driving the other's input, with capacitors that start just off the balance point. `time_to_cross` reports when `q` reaches 4 V, a clean logic 1. (`lam=0.02` gives the transistors a little output conductance, as real ones have, so the balance point is well defined.)

### Step 4: Fit tau

The resolution time is a straight line against `ln(imbalance)`, with slope `-tau`. `np.polyfit` fits that line:

```python
slope = np.polyfit(np.log(imbalances), times, 1)[0]
tau = -slope
```

### Step 5: Monte Carlo and MTBF

```python
offsets = rng.uniform(-5e-9, 5e-9, 2_000_000)
needed = tau * np.log((window / 2) / np.maximum(np.abs(offsets), 1e-30))
fails = int(np.sum(needed > t_res))

def mtbf(t_resolve, tau, window, f_clk, f_data):
    return math.exp(t_resolve / tau) / (window * f_clk * f_data)
```

`offsets` are the times between data edges and the clock edge. An edge that lands at distance `|offset|` from the clock edge starts with an imbalance proportional to it, and so needs `tau x ln((W/2) / |offset|)` to resolve (zero or negative means "resolves at once"). Counting those that need more than the allowed time reproduces the formula.

Run it:

```bash
uv run python phases/15-sequential-logic/07-timing-and-metastability/code/main.py
```

## Use It

- **Datasheets** give setup, hold and clock-to-Q times for every flip-flop. The 74HC74 datasheet lists them at 2, 4.5 and 6 V supply; FPGA datasheets give them per speed grade.
- **Static timing analysis.** Chip and FPGA tools (for example the timing analyzers in Vivado and Quartus, or PrimeTime for ASICs) compute the slack of every path for setup and hold, at several temperature and voltage corners, and refuse to sign off a design with negative slack.
- **Overclocking** raises the clock until the critical path's slack goes negative; raising the core voltage speeds up the gates (smaller `tpd`) to buy it back, at the cost of power.
- **Synchronizers everywhere.** Every button, every UART receive pin and every interrupt line of a microcontroller goes through a synchronizer inside the chip. FPGA vendors provide synchronizer cells and constraint attributes (such as `ASYNC_REG` in AMD/Xilinx tools) so the two flip-flops are placed close together.
- **Famous failures.** Metastability was understood in the 1970s after unexplained crashes in early multiprocessor systems; Chaney and Molnar's 1973 measurements showed flip-flop outputs hovering for long, unbounded times.

## Try It in the Lab

This lesson has no lab task. The ideas here are numerical: use the script and the exercises.

## Common Mistakes

- **Forgetting tcq and tsu.** The clock period is not just the logic delay. On fast chips tcq + tsu can be a third of the period.
- **Trying to fix hold violations by slowing the clock.** Hold does not depend on the period. Add delay to the short path instead.
- **One flip-flop for an asynchronous input.** It will go metastable sooner or later, and the logic it feeds will misbehave. Always use at least two flip-flops.
- **Synchronizing a multi-bit bus bit by bit.** The bits can resolve on different cycles. Use Gray code, a handshake or an asynchronous FIFO.
- **Assuming metastability means a wrong value.** It means an **undecided** value for an unpredictable time. A late but correct decision is fine; trouble comes when different parts of the logic see different decisions.

## Exercises

1. A path has `tcq = 0.3 ns`, logic of 12 gates at 0.12 ns each and `tsu = 0.2 ns`. What is the maximum clock frequency? If you could split the logic in half with a register (adding another `tcq + tsu`), what would the new fmax be?
2. The same path has a shortest logic path of 0.05 ns and the flip-flop's hold time is 0.25 ns. Is there a hold violation with zero skew? With 0.1 ns of skew? How much delay must be added to the short path?
3. A flip-flop has `tau = 50 ps` and `W = 20 ps`. A 200 MHz clock samples a signal that changes 10 million times per second. Compute the MTBF with `t_r = 2 ns` and with `t_r = 2 + 5 = 7 ns` (one more flip-flop).
4. From the simulated table, how long would the latch need to resolve from an imbalance of 1 nV? Use `t = t(1 uV) + tau x ln(1000)`.
5. Explain why a 4-bit counter value crossing to another clock domain is safe in Gray code (0000, 0001, 0011, 0010, 0110, ...) but not in binary. Give an example of a wrong value the receiver could see with binary when the count goes from 0111 to 1000.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| tcq | "Clock-to-out" | Delay from the clock edge to a valid flip-flop output |
| Setup time | "tsu" | Input must be stable this long before the edge |
| Hold time | "th" | Input must stay stable this long after the edge |
| Critical path | "The slow path" | The register-to-register path with the least slack; it sets fmax |
| Setup constraint | "Max delay check" | `T >= tcq + tlogic + tsu - skew` |
| Hold constraint | "Min delay check" | `tcq + tlogic_min >= th + skew`, independent of the clock period |
| Clock skew | "Skew" | Arrival-time difference of one clock edge at two flip-flops |
| Metastability | "Going meta" | A flip-flop near its balance point, resolving with time constant tau, possibly taking arbitrarily long |
| Synchronizer | "Two-flop sync" | Flip-flops in series so a metastable value has a full cycle to resolve before use |
| MTBF | "Mean time between failures" | `e^(t_r/tau) / (W f_clk f_data)` for a synchronizer |

## Further Reading

- David Harris and Sarah Harris, *Digital Design and Computer Architecture*, Chapter 3, sections on timing of sequential logic, clock skew, metastability and synchronizers.
- Thomas J. Chaney and Charles E. Molnar, "Anomalous Behavior of Synchronizer and Arbiter Circuits", *IEEE Transactions on Computers*, 1973.
- Clifford E. Cummings, "Clock Domain Crossing (CDC) Design & Verification Techniques Using SystemVerilog" (SNUG 2008), a widely used practical guide to synchronizers and Gray-code crossings.
- Texas Instruments datasheet *SN74HC74* (setup, hold and propagation delay specifications) and TI application report SDYA006, *Metastable Response in 5-V Logic Circuits*.
