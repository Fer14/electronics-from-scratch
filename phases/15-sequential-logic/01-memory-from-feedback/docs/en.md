# Memory from Feedback

> Feed a gate's output back into its own input and the circuit starts to remember, or starts to oscillate, depending on how many inversions sit in the loop.

**Type:** Learn
**Prerequisites:** Phase 14 (Digital Logic), Lessons 04-06 (Logic Gates, CMOS Gates from Transistors, Combinational Circuits), Phase 07 (Capacitors), Lesson 04 (The Time Constant)
**Time:** ~65 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Feedback | Connecting an output back to an input of the same circuit | A microphone hearing its own loudspeaker |
| Sequential circuit | A circuit whose output depends on the past as well as the present inputs | A ticket machine that remembers how many coins you already put in |
| State | The information a circuit is holding right now | The position of a light switch: up or down, it stays until moved |
| Bistable | Having exactly two stable states | A light switch that clicks up or down but never rests halfway |
| Stable state | A condition the circuit stays in by itself | A ball at the bottom of a valley |
| Unstable equilibrium | A balance point where the slightest push sends the circuit away | A ball balanced on the top of a hill |
| Positive feedback | Feedback that reinforces a change | A rumour that spreads faster the more people hear it |
| Negative feedback | Feedback that opposes a change | A thermostat turning the heater off when it gets warm |
| Ring oscillator | An odd number of inverters in a loop, which never settles | A game of "pass the opposite" around a table that never ends |
| Latch | A feedback loop with inputs to write a new value | A light switch with "on" and "off" buttons |
| Set / reset | Make the stored bit 1 / make it 0 | Pressing "on" / pressing "off" |

## Learning Objectives

- Explain the difference between combinational and sequential circuits.
- Show why two inverters in a loop hold either value forever, and why the middle point is unstable.
- Show why an odd number of inverters in a loop oscillates and compute its frequency from the gate delay.
- Simulate a CMOS ring oscillator with real transistors and estimate one gate's delay from it.
- Build a cross-coupled NOR latch and use it to set, reset and hold a bit.
- Explain why simulating feedback needs a notion of time.

## The Problem

Every circuit in Phase 14 was combinational: its outputs were a function of the inputs right now. Remove the input and the answer vanishes. That is fine for an adder, but useless for a calculator that has to remember the first number while you type the second, for a counter that has to know where it is, or for a computer that must keep a program and its variables.

To build anything that remembers, we need a circuit that keeps its output after the input that caused it has gone. No new component is needed. The trick is a wire: connect a gate's output back to its own input. Depending on how that loop is built, it can hold a bit forever or tick like a clock. This lesson explores both, because memory (Lessons 02-04) and clocks (Lesson 03) both come from this one idea.

## The Physics

### Positive feedback in two inverters

A CMOS inverter (Phase 14, Lesson 05) has high gain around its switching point: near 2.5 V, a small change at its input becomes a large, opposite change at its output. Now chain two inverters. Two inversions make a non-inversion, so the pair together has large **positive** gain: a small rise at the first input becomes a large rise at the second output.

Connect that second output back to the first input. Suppose the loop starts exactly at 2.5 V everywhere. Any tiny noise (Phase 14, Lesson 01), say the first input drifts up by 1 mV, comes back around the loop amplified, pushes the input up further, and so on. The voltage runs away until it hits a supply rail: the first node ends at 5 V, the second at 0 V. Pushed the other way, it ends at 0 V and 5 V. So:

- There are **two stable states**: (5 V, 0 V) and (0 V, 5 V). In each one, every inverter is fully on or fully off, its output sits on a rail, and the loop agrees with itself.
- There is **one unstable equilibrium** in the middle, where both nodes sit at the switching point. It is like a ball on a hilltop: it can balance there in theory, but the slightest disturbance rolls it into one of the two valleys.

```
   energy-like picture of a bistable loop

        unstable
           *
          / \
         /   \
   _____/     \_____
   state 0   state 1
   (valley)  (valley)
```

How fast does the loop leave the hilltop? Each node is a capacitor (the gate and wire capacitance, Phase 07) charged by the transistors' current. Near the middle, the extra current is proportional to how far the voltage has moved, and a current proportional to voltage charging a capacitor gives **exponential growth**: the disturbance is multiplied by e (about 2.718) every time constant `τ`, where `τ` is roughly the node capacitance divided by the transistors' transconductance. We will measure this in Lesson 07; it is the physics of metastability.

### Negative feedback in an odd ring

Now put **three** inverters in a loop. Three inversions make an inversion: the loop has negative feedback. Every time a node decides to be 1, the decision travels around the loop and arrives back at its input as "be 0". It can never agree with itself, so it never settles. Each node keeps flipping, and the flips chase each other around the ring. This is a **ring oscillator**, the simplest clock generator there is.

How fast? A change must travel around the whole ring twice before a node returns to where it started: once to flip it, once to flip it back. With `N` inverters each taking `tpd`:

```
period T = 2 x N x tpd
frequency f = 1 / (2 x N x tpd)
```

Read it: "the ring's frequency is one over twice the number of stages times the delay per stage". With 3 stages of 0.6 ns, `T = 2 x 3 x 0.6 ns = 3.6 ns`, so `f = 278 MHz`.

Ring oscillators are on almost every chip: as on-chip clocks, as temperature and process monitors (the frequency tells you how fast that chip's transistors are), and as random-number sources (the exact phase jitters with noise).

## The Concept

### Combinational versus sequential

```
combinational:   inputs ---> [ gates ] ---> outputs
                 output = f(inputs now)

sequential:      inputs ---> [ gates ] ---> outputs
                     +------>[       ]---+
                     |                   |
                     +----- state <------+
                 output = f(inputs now, state)
                 new state = g(inputs now, state)
```

A **sequential** circuit has a loop that carries **state**: information about the past. Everything with memory, from a single stored bit to a processor, is sequential.

### Two inverters: one bit of memory

```
      +-------[>o]--------+
      |        n1 -> n0   |
      |                   |
     n1                  n0
      |                   |
      +--------[o<]-------+
               n0 -> n1
```

Two consistent states:

```
 n0 = 1, n1 = 0:   NOT(n1) = NOT 0 = 1 = n0   and   NOT(n0) = 0 = n1    consistent
 n0 = 0, n1 = 1:   NOT(n1) = 0 = n0           and   NOT(n0) = 1 = n1    consistent
```

Both rows satisfy every gate. Which one the circuit is in depends on its history: whatever pushed it last. That is exactly what one bit of memory means. This loop, with two extra transistors to write into it, is the cell of the static RAM inside every processor (Phase 16, Lesson 03): six transistors per bit, called a 6T SRAM cell.

What happens at power-up? Nobody has pushed it yet, so the tiny random differences between the two inverters and noise decide. A real SRAM wakes up with random contents, which is why programs must initialise memory before using it. Our logic simulator is deterministic: all wires start at 0, the gates are evaluated in order, and it always wakes up the same way.

### How a simulator handles a loop

For combinational circuits, a simulator can evaluate gates in order from inputs to outputs, and one pass is enough. With a loop there is no "first" gate: `n0` depends on `n1`, which depends on `n0`. Our `sim.logic` solves this by **repeated evaluation**: it keeps re-evaluating every gate, using the latest values, until nothing changes. A stored bit is simply a set of values that no longer changes. If the values never stop changing, it gives up and reports that the loop oscillates.

For a ring oscillator, "never stops changing" is the correct answer, but it tells us nothing about the rhythm. For that we need **time**: assume each gate takes one time unit, and update all gates at once from the previous time step's values. Then the ring of three, starting from `n0 n1 n2 = 1 1 0`, goes:

```
t = 0: 1 1 0
t = 1: 1 0 0     n1 = NOT n0(t=0) = 0
t = 2: 1 0 1     n2 = NOT n1(t=1) = 1
t = 3: 0 0 1     n0 = NOT n2(t=2) = 0
t = 4: 0 1 1
t = 5: 0 1 0
t = 6: 1 1 0     back to the start
```

Exactly one node changes per time step, and the pattern repeats every 6 = 2 x 3 steps, as the formula predicts.

### Writing into the loop: the NOR latch

Two inverters remember, but you cannot easily tell them what to remember. Replace each inverter with a 2-input NOR. A NOR with one input at 0 behaves like an inverter of its other input (`NOR(x, 0) = x'`), so with both extra inputs at 0 the loop is the same bistable pair. The extra inputs let us overrule it:

```
            +-------+
   r ------>|       |
            |  NOR  |o-----+------> q
      +---->|       |      |
      |     +-------+      |
      |                    |
      qb                   q        each output feeds the other gate
      |                    |
      |     +-------+      |
      +----o|       |<-----+
            |  NOR  |
   s ------>|       |
            +-------+
```

The bottom gate's output is `qb` (drawn with its bubble on the left because the gate faces the other way). As equations: `q = NOR(r, qb)` and `qb = NOR(s, q)`.

- **s = 1, r = 0 (set).** A NOR with any input at 1 outputs 0, so `qb = 0`. Then `q = NOR(0, 0) = 1`. The bit is set.
- **s = 0, r = 0 (hold).** Both NORs act as inverters of each other: the bistable loop keeps whatever it had.
- **s = 0, r = 1 (reset).** `q = 0`, then `qb = NOR(0, 0) = 1`. The bit is cleared.

```
 action   s r | q qb
 set      1 0 | 1 0
 hold     0 0 | 1 0     remembers the set
 reset    0 1 | 0 1
 hold     0 0 | 0 1     remembers the reset
```

The same inputs `s = 0, r = 0` give different outputs depending on what happened before. No combinational circuit can do that. Lesson 02 studies this latch properly, including the input `s = r = 1` that you should never use.

### The ring oscillator with real transistors

Our circuit simulator can build the ring from actual MOSFETs: three CMOS inverters (PMOS and NMOS with `Vth = 1 V`, `k = 1 mA/V^2`) and a 1 pF capacitor on each node to represent the wiring and the next gate. A transient simulation (Phase 07, Lesson 08) shows it oscillating between about 0.1 V and 4.9 V at 284 MHz. Solve the formula for the delay:

```
tpd = 1 / (2 x N x f) = 1 / (2 x 3 x 284e6 Hz) = 0.59 ns
```

Compare with a back-of-envelope RC estimate: the on-resistance of each transistor is about `1 / (k x (VGS - Vth)) = 1 / (0.001 x 4) = 250 Ω` (Phase 14, Lesson 05), and `250 Ω x 1 pF = 0.25 ns`. The real delay is a couple of time constants because the transistor is not a fixed resistor during the whole swing and the input edge itself is slow. Same order of magnitude: the physics checks out.

## Build It

The script `code/main.py` builds each loop in `sim.logic` (and the ring oscillator also in `sim.Circuit`).

### Step 1: A ring of inverters

```python
def inverter_ring(stages):
    lc = LogicCircuit(f"ring of {stages} inverters")
    names = [f"n{i}" for i in range(stages)]
    for i, name in enumerate(names):
        lc.not_(name, names[i - 1])
    lc.outputs(*names)
    return lc
```

`names[i - 1]` for `i = 0` is `names[-1]`, the last wire, which closes the loop.

### Step 2: Two inverters remember

`settle(values)` writes the given values onto wires, then re-evaluates every gate until nothing changes. Writing a value onto `n1` and letting go is a "kick": a short push from outside.

```python
pair = inverter_ring(2)
first = pair.settle()
kicked = pair.settle({"n1": 1})
again = pair.settle()
```

```
  after power-up:          n0 = 1, n1 = 0
  kick n1 to 1, let go:    n0 = 0, n1 = 1
  nothing touched:         n0 = 0, n1 = 1  (it remembers)
  kick n1 to 0, let go:    n0 = 1, n1 = 0
```

### Step 3: Three inverters never settle

`settle()` raises `LogicSettleError` for the 3-ring. To see the rhythm, we update all gates at once per time step:

```python
def unit_delay_run(lc, start, steps):
    values = dict(start)
    history = [dict(values)]
    for _ in range(steps):
        values = {**values, **{gate.output: gate.evaluate(values) for gate in lc.gates}}
        history.append(dict(values))
    return history
```

Every gate reads the values of the previous step (the dictionary comprehension computes all new outputs before any is stored), which is what "each gate takes one time unit" means. The script prints the 13 steps shown above and finds a period of 6 gate delays.

### Step 4: The CMOS ring in the circuit simulator

```python
def cmos_ring(stages=3, load=1e-12):
    c = Circuit(f"{stages}-stage CMOS ring oscillator")
    c.voltage_source("VDD", "vdd", "0", 5.0)
    names = [f"n{i}" for i in range(stages)]
    for i, name in enumerate(names):
        c.pmos(f"MP{i}", d=name, g=names[i - 1], s="vdd", vth=1.0, k=1e-3)
        c.nmos(f"MN{i}", d=name, g=names[i - 1], s="0", vth=1.0, k=1e-3)
        c.capacitor(f"C{i}", name, "0", load, v0=5.0 if i % 2 == 0 else 0.0)
    return c

t = cmos_ring().transient(t_stop=100e-9, dt=0.05e-9)
f = t.frequency("n0")
```

The capacitors start at 5 V, 0 V, 5 V, an inconsistent pattern for three inverters, so the ring starts moving at once. `t.frequency` measures the oscillation from the rising crossings of the middle level.

```
  oscillation frequency: 284 MHz
  implied delay per inverter: tpd = 1 / (2 x 3 x f) = 0.59 ns
```

### Step 5: The NOR latch

```python
def nor_latch():
    lc = LogicCircuit("cross-coupled NOR latch")
    lc.inputs("s", "r")
    lc.nor("q", "r", "qb")
    lc.nor("qb", "s", "q")
    lc.outputs("q", "qb")
    return lc
```

Calling `latch.evaluate({"s": 1, "r": 0})` then `latch.evaluate({"s": 0, "r": 0})` shows the bit staying at 1: the circuit object keeps its wire values between calls, just as the real latch keeps its voltages.

Run it:

```bash
uv run python phases/15-sequential-logic/01-memory-from-feedback/code/main.py
```

## Use It

- **SRAM.** Every processor cache and register file is built from cross-coupled inverter pairs (6T cells). A 32 MB cache holds about 268 million of them.
- **Ring oscillators** are used as on-chip process monitors: a foundry measures a ring's frequency on each wafer to know how fast that batch of transistors is. A slower ring means slower chips.
- **Random numbers.** Free-running ring oscillators sampled by a clock produce jittery, unpredictable bits; many hardware random-number generators start from them.
- **Switch debouncing.** A mechanical switch bounces for milliseconds when pressed. An SR latch driven by a two-way switch (one contact sets, the other resets) gives a single clean transition.
- **Power-on state.** Because a latch wakes up in a random state, real systems have a reset signal that forces every important bit to a known value at start-up.

## Try It in the Lab

This lesson has no lab task. The first sequential lab is in Lesson 02, where you build a latch that can be written.

## Common Mistakes

- **Thinking memory needs a special part.** A bit of static memory is just two inverters in a loop. Capacitors (DRAM) and trapped charge (flash) are other ways, but the logic kind is pure feedback.
- **Counting the gates instead of the inversions.** Whether a loop remembers or oscillates depends on the number of inversions: even means bistable, odd means oscillation. Two NANDs used as inverters are an even loop; three are odd.
- **Expecting a deterministic power-up.** Real latches wake up randomly; only the simulator is deterministic.
- **Using a ring oscillator as a precise clock.** Its frequency changes with supply voltage and temperature by tens of percent. Precise clocks use a quartz crystal (Phase 17).
- **Simulating feedback without time.** A simulator that only evaluates gates in order cannot handle loops. It needs repeated evaluation (for memory) or explicit time steps (for oscillation).

## Exercises

1. A ring oscillator has 5 inverters, each with a delay of 40 ps. What is its frequency? How many inverters would you need for about 1 GHz?
2. Four inverters are connected in a loop. Is it bistable or oscillating? List the stable states as patterns of `n0 n1 n2 n3`.
3. Trace the NOR latch by hand for this input sequence: (s, r) = (0, 1), (0, 0), (1, 0), (0, 0), (0, 1). Write q after each step.
4. Build a latch from two cross-coupled NAND gates, `q = NAND(a, qb)` and `qb = NAND(b, q)`. Which input values hold the state? Which ones set and reset it? (Hint: NAND with one input at 1 is an inverter.)
5. In the script, change the ring capacitors from 1 pF to 2 pF and rerun. By what factor does the frequency change? Explain with `tpd ∝ R x C`.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Sequential circuit | "Logic with memory" | A circuit with feedback whose outputs depend on stored state as well as current inputs |
| State | "What it remembers" | The values held in the feedback loops right now |
| Bistable | "Flip-flop-like" | Having two stable operating points, as an even-inversion loop does |
| Unstable equilibrium | "The balance point" | The middle point of a bistable loop, where any disturbance grows exponentially |
| Ring oscillator | "A ring" | An odd number of inverters in a loop; `f = 1 / (2 N tpd)` |
| SR latch | "Set-reset latch" | Two cross-coupled NOR (or NAND) gates with inputs to set, reset or hold one bit |
| Positive feedback | "Regenerative feedback" | Feedback with loop gain above 1 that drives the circuit to a rail and holds it there |

## Further Reading

- David Harris and Sarah Harris, *Digital Design and Computer Architecture*, Chapter 3 (Sequential Logic Design), sections on bistable circuits and latches.
- Neil H. E. Weste and David Money Harris, *CMOS VLSI Design*, the sections on ring oscillators and the 6T SRAM cell.
- Charles Petzold, *Code*, chapter "Feedback and Flip-Flops", for a relay-level history of memory from feedback.
- All About Circuits, *Digital* textbook (Vol. IV), chapter "Multivibrators", sections on the S-R latch.
