# Transient Simulation from Scratch

> To simulate time, chop it into small steps and replace each capacitor, for one step, with a resistor and a current source. Then every step is just a DC circuit.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 05 Lesson 04 (Modified Nodal Analysis from Scratch), Phase 07 Lessons 02-04 (Capacitance, Charging and Discharging, The Time Constant)
**Time:** ~90 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Transient analysis | Computing how voltages and currents change over time | Filming a scene frame by frame instead of taking one photo |
| Time step (h or dt) | The small slice of time between two computed moments | The gap between two frames of a film |
| Numerical integration | Building a curve from its rate of change, one small step at a time | Walking by repeatedly looking at your compass and taking a step |
| Companion model | The resistor-plus-current-source that stands in for a capacitor during one step | A cardboard cut-out that behaves like the real actor for a single shot |
| History current | The current source in the companion model; it carries the memory of the previous step | Yesterday's balance carried forward in a bank account |
| Backward Euler | A step rule that uses the slope at the **end** of the step | Choosing your step so that you arrive pointing the way the compass will point when you land |
| Trapezoidal rule | A step rule that uses the average of the slopes at the start and end | Averaging the compass readings at both ends |
| Order of accuracy | How fast the error shrinks as the step shrinks (first order: halve the step, halve the error) | How much sharper a picture gets per extra pixel |
| Stamp | Adding one component's contribution to the matrix and right-hand side of the nodal equations | Each guest writing their own line in a shared ledger |
| Stability | Whether errors die out or blow up as the simulation runs | A bicycle that straightens itself versus one that wobbles more and more |

## Learning Objectives

- Explain why a circuit with capacitors cannot be solved with one DC calculation, and how time stepping fixes it.
- Derive the backward-Euler and trapezoidal companion models of a capacitor from I = C x dV/dt.
- Stamp the companion model into the modified nodal analysis (MNA) matrix you built in Phase 05.
- Write a complete transient simulator in about 100 lines of numpy that handles resistors, sources and capacitors.
- Measure the error of both methods against the exact RC formula and see first-order versus second-order accuracy.
- Show that your simulator and our `sim` package produce the same waveforms.

## The Problem

Every time you have called `circuit.transient(...)` in this phase, something happened behind the curtain. You have seen it agree with the exponential formulas, but you have taken it on trust. And formulas only exist for the simplest circuits. Two resistors and two capacitors in a ladder already make the hand algebra unpleasant; a real power supply with ten capacitors and a transistor has no neat formula at all.

In Phase 05 you built modified nodal analysis: write one equation per node, put them in a matrix, solve. That solves any network of resistors and sources, but only at one instant, with no history. Capacitors have history: their voltage now depends on all the current that has flowed into them before. This lesson shows the beautiful trick every circuit simulator (SPICE and its descendants included) uses to turn that history into a sequence of DC problems you already know how to solve.

## The Physics

There is no new physics in this lesson; it is all in the capacitor law from Lesson 02:

> The current into a capacitor is its capacitance times how fast its voltage is changing.

    i = C x dv/dt

What changes is how we use it. A computer cannot handle "how fast at this instant" directly. It can handle "how much did it change during a small step". Replace the instantaneous rate dv/dt by the change over one step of length h:

    dv/dt  is approximately  (v_new - v_old) / h

Here v_old is the capacitor voltage at the start of the step (known, because we computed it in the previous step) and v_new is the voltage at the end of the step (unknown, the thing we want).

The real voltage curve is smooth and bends; the straight-line approximation over a step is only exact if the curve is straight. So the answer will have an error, and the error shrinks when h shrinks. Lesson 03 already showed this by hand: big steps of RC/5 ran visibly ahead of the exact curve.

## The Concept

### Backward Euler: the slope at the end

The question is **at which moment** we evaluate the current. The backward Euler rule says: use the current at the **end** of the step.

    i_new = C x (v_new - v_old) / h

Rearrange it, separating what is unknown (v_new) from what is known (v_old):

    i_new = (C / h) x v_new  -  (C / h) x v_old

Read this as a circuit. The first term is a current proportional to the voltage, which is exactly what a resistor (conductance G = C / h) does. The second term is a fixed number for this step: a **current source** of value (C / h) x v_old. So, for the duration of one step:

> A capacitor behaves like a conductance C / h in parallel with a current source of (C / h) times its previous voltage.

```
   a o------+------------+
            |            |
           ===    =>    [ G = C/h ]     ( I_hist = G x v_old )  ^ pushes current
            |            |                                       | back into a
   b o------+------------+
```

The direction matters. The capacitor's current flows from a to b through it: i = G x v_new - G x v_old. The resistor part carries G x v_new from a to b; the source must carry G x v_old **from b to a** to subtract it. So the history source injects current into node a.

Why is this good news? Because a conductance and a current source are things MNA already knows how to stamp. Each time step becomes a plain DC problem, which we solve with the same `np.linalg.solve` as in Phase 05. Then we read off v_new for every capacitor, store it as v_old, and repeat.

### Backward Euler with numbers

Take R = 1 kOhm, C = 1 uF, V = 5 V, starting empty, step h = 0.1 ms. Then G = C / h = 1e-6 / 1e-4 = 0.01 S (equivalent to 100 Ohm).

First step: v_old = 0, so the history source is 0. The circuit for this step is a 5 V source, 1 kOhm, and a 100 Ohm "capacitor resistor". That is a voltage divider (Phase 04):

    v_new = 5 x 100 / (1000 + 100) = 0.4545 V

Second step: history source = 0.01 x 0.4545 = 4.545 mA into the capacitor node. Nodal equation at the node (currents leaving = currents entering):

    (v - 5) / 1000 + 0.01 x v = 0.004545
    0.011 x v = 0.004545 + 0.005 = 0.009545
    v = 0.8678 V

The exact values are 0.4758 V and 0.9063 V. Backward Euler is a little behind, because it uses the current at the end of each step, which is the smallest current during that step (the opposite of the hand method of Lesson 03, which used the largest and ran ahead).

### The trapezoidal rule: average both ends

A better guess: use the **average** of the currents at the start and end of the step.

    (i_new + i_old) / 2 = C x (v_new - v_old) / h

Rearranged:

    i_new = (2C / h) x v_new  -  [ (2C / h) x v_old + i_old ]

Again a conductance (now 2C / h) and a history current source (now (2C/h) x v_old + i_old). The only extra thing to remember between steps is the capacitor's current i_old as well as its voltage.

One catch: at the very first step, we often do not know i_old (the current just after switch-on may be different from the current just before). Our code, like `sim`, takes the first step with backward Euler, which needs no i_old, and then switches to the trapezoidal rule.

### How good is each method?

Errors in a step-by-step method come from treating a bending curve as straight over each step.

- **Backward Euler is first order.** Halve h and the error roughly halves. To get 10 times more accurate you need 10 times more steps.
- **The trapezoidal rule is second order.** Halve h and the error roughly quarters. 10 times more accurate needs only about 3 times more steps.

Both are **stable** for RC circuits: errors never grow, whatever the step. (A tempting alternative, forward Euler, which uses the slope at the start, becomes unstable and oscillates wildly when h is larger than 2RC.) The trapezoidal rule has one weakness: after a sudden jump, it can make the capacitor's **current** zig-zag from step to step. Backward Euler damps that. That is why practical simulators mix them.

### Putting it in MNA

Recall the MNA system from Phase 05: A x = b. The unknowns x are the node voltages followed by one current per voltage source. Each element adds ("stamps") its numbers:

- **Resistor** with conductance g between nodes a and b: add g to A[a, a] and A[b, b], subtract g from A[a, b] and A[b, a].
- **Current source** pushing I from node f to node t: subtract I from b[f], add I to b[t].
- **Voltage source** V from plus to minus, with its own row k: put +1 and -1 in row and column k at the plus and minus nodes, and V in b[k].
- **Capacitor (new)**: stamp a resistor of conductance G (C/h or 2C/h) between a and b, and a current source of I_hist from b to a.

Ground is not a row in the matrix; any stamp touching ground is simply skipped.

The full loop:

```
set every capacitor's v_old to its initial voltage, i_old to 0
for each time step k = 1, 2, ...:
    build A and b: resistors, sources (at time t_k), capacitor companions
    solve A x = b
    for each capacitor: v_new = x[a] - x[b];  compute i_new;  v_old, i_old = v_new, i_new
    store x
```

## Build It

```bash
uv run python phases/07-capacitors/08-transient-simulation-from-scratch/code/main.py
```

### Step 1: A netlist that remembers nodes

`TinyTransient` keeps lists of components and gives each node name a number. Ground ("0") is number -1, meaning "not in the matrix".

```python
class TinyTransient:
    def __init__(self):
        self.nodes = {"0": -1}
        self.resistors = []
        self.voltage_sources = []
        self.current_sources = []
        self.capacitors = []

    def node(self, name):
        if name not in self.nodes:
            self.nodes[name] = len(self.nodes) - 1
        return self.nodes[name]

    def resistor(self, a, b, ohms):
        self.resistors.append((self.node(a), self.node(b), 1.0 / ohms))

    def capacitor(self, a, b, farads, v0=0.0):
        self.capacitors.append((self.node(a), self.node(b), farads, v0))
```

Voltage and current sources are stored the same way. A source's value may be a number or a function of time, which is how we make a square wave.

### Step 2: Stamps

```python
    def stamp_conductance(self, matrix, a, b, conductance):
        if a >= 0:
            matrix[a, a] += conductance
        if b >= 0:
            matrix[b, b] += conductance
        if a >= 0 and b >= 0:
            matrix[a, b] -= conductance
            matrix[b, a] -= conductance

    def stamp_current(self, rhs, from_node, to_node, amps):
        if from_node >= 0:
            rhs[from_node] -= amps
        if to_node >= 0:
            rhs[to_node] += amps
```

### Step 3: One time step

This is the heart of the simulator. Notice the capacitor block: a conductance plus a history current, and the only difference between the two methods is the formula for those two numbers.

```python
        for index, (a, b, farads, _) in enumerate(self.capacitors):
            if method == "backward_euler":
                conductance = farads / step
                history = conductance * cap_volts[index]
            else:
                conductance = 2 * farads / step
                history = conductance * cap_volts[index] + cap_currents[index]
            self.stamp_conductance(matrix, a, b, conductance)
            self.stamp_current(rhs, b, a, history)
```

The voltage sources get their extra row, exactly as in Phase 05, and then `np.linalg.solve(matrix, rhs)` gives every node voltage at the end of the step.

### Step 4: The time loop

After each solve, we update each capacitor's memory. For backward Euler, i_new = (C/h)(v_new - v_old). For the trapezoidal rule, i_new = (2C/h)(v_new - v_old) - i_old, which is the trapezoid equation solved for i_new.

```python
        for k in range(1, steps + 1):
            step_method = "backward_euler" if k == 1 else method
            solution = self.solve_step(times[k], step, cap_volts, cap_currents, step_method)
            for index, (a, b, farads, _) in enumerate(self.capacitors):
                new_volts = self.voltage(solution, a) - self.voltage(solution, b)
                if step_method == "backward_euler":
                    cap_currents[index] = farads / step * (new_volts - cap_volts[index])
                else:
                    cap_currents[index] = 2 * farads / step * (new_volts - cap_volts[index]) - cap_currents[index]
                cap_volts[index] = new_volts
            history[k] = solution[: len(self.nodes) - 1]
```

### Step 5: Test against the exact formula

The RC charge with a deliberately coarse step, h = tau / 10:

```
RC charge, R = 1 kOhm, C = 1 uF, 5 V, step h = tau / 10 = 0.1 ms
 t (ms)  exact (V)  backward Euler  trapezoidal
    0.1     0.4758          0.4545       0.4545
    0.2     0.9063          0.8678       0.8874
    0.5     1.9673          1.8954       1.9541
    1.0     3.1606          3.0723       3.1533
    2.0     4.3233          4.2568       4.3212
    5.0     4.9663          4.9574       4.9663
```

The first two backward-Euler values are exactly the 0.4545 V and 0.8678 V we computed by hand. The first trapezoidal value is the same, because the first step is always backward Euler; after that the trapezoidal rule pulls much closer to the exact curve.

### Step 6: Error versus step size

```
Worst error over the first 5 tau as the step shrinks
      step  backward Euler (mV)  trapezoidal (mV)
     tau/5              169.991           73.0129
    tau/10               88.319           21.2675
    tau/20               45.050            5.7576
    tau/40               22.756            1.4992
    tau/80               11.437            0.3826
Halving the step roughly halves the Euler error (first order) and quarters the trapezoidal error (second order)
```

Look at the ratios down each column: backward Euler goes 170, 88, 45, 23, 11 (halving each time); trapezoidal goes 73, 21, 5.8, 1.5, 0.38 (dividing by nearly 4). With 80 steps per tau the trapezoidal error is under half a millivolt on a 5 V signal.

### Step 7: Compare with `sim`

A harder circuit: a two-stage RC ladder driven by a 5 V, 250 Hz square wave.

```
    in o--[ 1k ]--o a --[ 2.2k ]--o b
      |           |               |
   square        === 1 uF        === 470 nF
    wave          |               |
      0 ----------+---------------+
```

There is no simple formula for node b here, but we can compare our simulator with `sim`, method by method, with a 10 us step:

```
Two-stage RC ladder, 5 V 250 Hz square wave, step 10 us: ours (backward_euler) vs sim (method='be')
 t (ms)   ours a    sim a   ours b    sim b
    0.5    1.797    1.797    0.415    0.415
    1.0    2.775    2.775    1.165    1.165
    2.0    3.725    3.725    2.559    2.559
    3.0    1.487    1.487    2.326    2.326
    4.0    0.834    0.834    1.523    1.523
    6.0    4.005    4.005    3.141    3.141
    8.0    0.936    0.936    1.736    1.736
Largest difference between the two simulators: 1.1e-08 V

Two-stage RC ladder, 5 V 250 Hz square wave, step 10 us: ours (trapezoidal) vs sim (method='trap')
 t (ms)   ours a    sim a   ours b    sim b
    0.5    1.805    1.805    0.412    0.412
    1.0    2.782    2.782    1.165    1.165
    2.0    3.754    3.754    2.564    2.564
    3.0    1.490    1.490    2.339    2.339
    4.0    0.811    0.811    1.528    1.528
    6.0    4.031    4.031    3.140    3.140
    8.0    0.911    0.911    1.739    1.739
Largest difference between the two simulators: 1.1e-08 V
```

The two simulators agree to about ten billionths of a volt. The tiny leftover comes from a very small conductance (1e-12 S) that `sim` adds from every node to ground, a standard trick to keep the matrix solvable when a node would otherwise float. You have just rebuilt the engine of `sim.transient()`.

Notice also that at t = 2 ms (right at the falling edge) and t = 4 ms the two methods differ by up to 30 mV: with a 10 us step on a 1 ms time constant the methods are not yet perfectly converged, and the ladder's sharp edges are the hardest moments.

## Use It

- **SPICE.** Berkeley SPICE (1970s) and its descendants (ngspice, LTspice, Spectre, HSPICE) work this way: MNA plus companion models plus an integration rule. SPICE's default is the trapezoidal rule, with "Gear" (backward differentiation) methods as an option; LTspice adds its own modified trapezoidal method to suppress the zig-zag.
- **Variable time steps.** Real simulators do not use a fixed h. They estimate the error after each step and shrink the step near fast edges and stretch it in quiet stretches. This is why LTspice can simulate a switching power supply over 10 ms without taking billions of steps.
- **Inductors.** The same idea works for inductors (Phase 08): v = L x di/dt becomes a conductance h / L in parallel with a history current. You will add it to your simulator then.
- **Nonlinear parts.** With diodes and transistors (Phases 11-12), each time step also needs a Newton-Raphson loop, because the "DC problem" of the step is nonlinear. The time loop stays exactly the same.
- **Beyond electronics.** Thermal models of chips, building heating, and even neural network "neural ODE" solvers use the same backward-Euler and trapezoidal steps.

## Common Mistakes

- **Getting the history source backwards.** It pushes current into node a (the capacitor's first node). Reversing it makes the capacitor behave as if its voltage were negative; a simple RC test catches this immediately.
- **Forgetting to update the memory.** After every solve, both v_old and (for trapezoidal) i_old must be updated for every capacitor, before the next step.
- **Choosing h larger than the time constants.** Backward Euler stays stable but becomes very inaccurate; aim for h at most a tenth of the smallest RC you care about, and check by halving it.
- **Trapezoidal from the very first step with i_old = 0.** At switch-on the capacitor current jumps from zero to V/R; using i_old = 0 averages in a wrong value. Starting with one backward-Euler step avoids it.
- **Confusing forward and backward Euler.** Forward Euler (slope at the start) is easy to write without a matrix but becomes unstable for h > 2RC. Backward Euler needs a matrix solve, which we have anyway.
- **Trusting one run.** Always rerun with half the step. If the answer changes noticeably, the step was too big.

## Exercises

1. By hand, take one more backward-Euler step after the two worked in the text (h = 0.1 ms). What is v after 0.3 ms? Compare with the code's output (print `euler[3]`).
2. Add a method `"forward_euler"` to `TinyTransient`: during each step, treat the capacitor as a voltage source of v_old, solve, and compute v_new = v_old + h x i / C. Run the RC test with h = tau / 10, tau, and 3 x tau. What happens at 3 x tau?
3. Use your simulator to discharge a 100 uF capacitor from 9 V through 1 kOhm (set `v0=9.0` and no source). Compare with 9 x e^(-t / RC) at 0.1 s.
4. Make the ladder's step 1 us instead of 10 us. How much do the backward-Euler and trapezoidal results now differ at t = 2 ms? Explain.
5. Extend `TinyTransient` with an `inductor(a, b, henries, i0)` using the backward-Euler companion model (conductance h / L, history current equal to the previous inductor current flowing from a to b). Test it on a 10 V source, 100 Ohm and 10 mH in series: the current should approach 100 mA with tau = L / R = 0.1 ms.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Transient analysis | ".tran" | Solving the circuit at a sequence of times, each step using the previous one |
| Companion model | "The cap's equivalent circuit" | Conductance plus history current that replaces a capacitor for one time step |
| Backward Euler | "Implicit Euler" | Uses the derivative at the end of the step: first order, very stable, damps oscillation |
| Trapezoidal rule | "Trap" | Averages the derivative at both ends: second order, can ring after sharp edges |
| Time step | "dt" | The step length h; error shrinks like h (BE) or h^2 (trap) |
| Stamp | "Adding to the matrix" | Each element's fixed pattern of additions to the MNA matrix and right-hand side |
| gmin | "A tiny resistor everywhere" | Small conductance from each node to ground that simulators add to keep the matrix solvable |

## Further Reading

- L. W. Nagel, "SPICE2: A Computer Program to Simulate Semiconductor Circuits", UC Berkeley ERL Memo M520, 1975 - the thesis that defined how SPICE does transient analysis.
- [MIT OpenCourseWare 6.002 Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) - first-order circuits and their differential equations.
- [ngspice user manual, chapter on transient analysis options (METHOD, TRTOL)](https://ngspice.sourceforge.io/docs.html) - how a production simulator exposes trapezoidal and Gear integration.
- *The Art of Electronics*, 3rd ed., Horowitz & Hill, Appendix J (SPICE primer) - practical advice on using circuit simulators.
