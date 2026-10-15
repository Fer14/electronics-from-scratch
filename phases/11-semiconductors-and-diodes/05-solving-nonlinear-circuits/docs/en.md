# Solving Nonlinear Circuits

> When a part's law is curved, you cannot solve the circuit in one go. Guess, replace the curve by its tangent at the guess, solve the straight-line circuit, and repeat. That is Newton-Raphson, and it is how every circuit simulator handles diodes and transistors.

**Type:** Build
**Prerequisites:** 11-04 (The Diode Equation); Phase 05 (Circuit Analysis and Our Simulator), lessons 02-nodal-analysis and 04-modified-nodal-analysis-from-scratch
**Time:** ~90 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Linear | A relationship that is a straight line: double the cause, double the effect | A taxi meter with no starting fee: twice the distance, twice the price |
| Nonlinear | Anything that is not a straight line, like the diode's exponential | A phone plan where the first gigabytes are cheap and the rest very expensive |
| Operating point | The voltages and currents a circuit settles at, with nothing changing | Where a ball comes to rest at the bottom of a bowl |
| Load line | The straight line showing what current the rest of the circuit (here a resistor) would allow for each diode voltage | The menu of deals the shop is willing to offer |
| Iteration | Repeating a calculation, each time starting from the previous answer | Adjusting the shower tap again and again until the water is right |
| Fixed-point iteration | Rearranging an equation into "x = something(x)" and repeating it | Feeding the output of a machine back into its input |
| Bisection | Finding a root by repeatedly halving an interval that is known to contain it | Guessing a number between 1 and 100 by always asking "higher or lower?" |
| Newton-Raphson | Finding a root by following the tangent line from the current guess to where it hits zero | Skiing down a slope by always heading straight down the local steepest line |
| Tangent | The straight line that just touches a curve at a point and has the same steepness there | A ruler laid against a ball |
| Derivative | The steepness (slope) of a curve at a point | The gradient sign on a mountain road: "12 %" |
| Companion model | A linear stand-in for a nonlinear part: a resistor plus a current source matching the tangent | A stunt double who looks exactly like the actor from one camera angle |
| Convergence | The guesses getting closer and closer to the true answer | Zooming in on a map until you find the house |
| Residual / mismatch | How far a guess is from satisfying the equation | How much a recipe's taste still differs from what you want |

## Learning Objectives

- Write the equation of a diode-resistor circuit and see why it has no closed-form answer in elementary functions.
- Find the operating point graphically with a load line.
- Implement four ways of solving it: two kinds of fixed-point iteration, bisection and Newton-Raphson, and compare their speed and robustness.
- Explain why plain Newton crawls when the exponential overshoots, and fix it with junction "hold-back" limiting.
- Turn Newton-Raphson into a circuit method: linearise each diode into a companion model, solve with modified nodal analysis, repeat.
- Check our hand-built solver against the simulator.

## The Problem

In Phase 05 you solved any circuit of resistors and sources by writing one linear equation per node and handing the system to a linear solver. Linear equations have a wonderful property: one solve gives the exact answer.

Put a single diode in that circuit and the property is gone. Consider the simplest diode circuit there is:

```
          R = 1 kΩ
   +5 V ---/\/\/\--- a ---|>|--- ground
                     V = ?
```

Kirchhoff's current law at node `a` says the current arriving through the resistor equals the current leaving through the diode:

```
(5 − V) / 1000  =  I_S × ( e^(V / V_T) − 1 )
```

Read: "the resistor current, five minus V over a thousand, must equal the diode current from the Shockley equation". There is exactly one unknown, V. But it appears both plain and inside an exponential, and no amount of algebra with +, −, ×, ÷, powers and logs isolates it. (Mathematicians do have a special function for it, the Lambert W, but it stops helping the moment you add a second diode.)

Every circuit with diodes, LEDs, transistors or op-amps with real limits has this problem, usually with hundreds or millions of unknowns. So simulators don't solve these equations; they *close in* on the answer. This lesson builds that machinery by hand, and then shows that our simulator's answer is the same, to the last digit.

## The Physics

Nothing new physically: the diode obeys lesson 04's equation and the resistor obeys Ohm's law. The physics question is really "where does the circuit settle?".

Think of it as a negotiation. The resistor says: "if your voltage is V, I can deliver (5 − V)/1000 amps; the higher you go, the less I can push" (a straight line going down). The diode says: "if my voltage is V, I insist on I_S e^(V/V_T) amps" (an exponential going up). The circuit settles where both agree. If the diode voltage were a little too high, the diode would demand more current than the resistor can supply; the capacitance that every real node has would then discharge a little and the voltage would drop. If it were too low, the reverse would happen. The agreement point is stable, like a ball in a bowl. Our job is to calculate where it is.

## The Concept

### Step 1: The load line

Draw both laws on the same axes, current against diode voltage:

```
  I (mA)
    5 |\
      |  \  resistor: I = (5 - V)/1000          diode: I = I_S e^(V/V_T)
    4 |    \_______________________ x <-- they meet: the operating point
      |                            /\
    3 |                           /   \____
      |                          /         \____
    2 |                         /                \___
      |                        /
    1 |                      /
      |___________________ /
    0 +----+----+----+----+----+----  V (volts)
      0   0.2  0.4  0.6  0.8  ...  5 (the resistor line reaches 0 mA at 5 V)
```

The resistor line is called the **load line**: it goes from 5 mA at V = 0 (diode replaced by a short) to 0 mA at V = 5 V (diode replaced by an open circuit). Where it crosses the diode curve is the **operating point**. By eye, near 0.69 V and 4.3 mA. `code/out.png` draws it to scale. Engineers used load lines with ruler and pencil for decades, and they still are the best way to *see* a nonlinear circuit.

### Step 2: Write it as "find where something is zero"

Move everything to one side and call it the **mismatch**:

```
f(V) = (5 − V) / R  −  I_S ( e^(V/V_T) − 1 )
```

When f(V) = 0, the resistor and diode agree. If f(V) > 0 the resistor offers more than the diode takes (V is too low); if f(V) < 0 the diode demands more than the resistor can give (V is too high). Every method below is a strategy to find the V where f(V) = 0.

### Method 1: Naive guess-and-repeat (fails)

An obvious idea: guess V, compute the diode current I, then the voltage the resistor would leave: V = 5 − I × R. Repeat.

Starting at 0.6 V: the diode takes 0.12 mA, so V = 5 − 0.12 = 4.88 V. At 4.88 V the diode equation asks for about 10⁷⁰ amps, so V = 5 − 10⁷³ ≈ −10⁷³ V. The script prints the disaster:

```
step 0: V = 0.6 V
step 1: V = 4.8799 V
step 2: V = -9.52028e+70 V
```

Why? Repeating x = g(x) only settles if g is *gentle*: a small error in x must become a smaller error in g(x). Here g contains the exponential, which magnifies a 1 mV error near 0.7 V into a 4 % error in current, times R = 1000, which is huge. The error grows at each pass.

### Method 2: Rearranged guess-and-repeat (works)

Turn it around: guess V, compute the current the *resistor* allows, I = (5 − V)/R, then ask the diode what voltage it needs for that current, V = V_T ln(I/I_S + 1). The logarithm is the gentlest function there is: a 10 % error in current becomes only 2.5 mV of voltage error.

```
step 0: V = 0.000000000 V
step 1: V = 0.696397917 V
step 2: V = 0.692520491 V
step 3: V = 0.692543772 V
step 4: V = 0.692543632 V
step 5: V = 0.692543633 V
```

Five steps to nine decimal places. Lovely, but it relied on our ability to invert the diode equation and on there being only one diode in a simple chain. With a network of diodes and transistors there is no obvious way to "rearrange" anything. We need a general method.

### Method 3: Bisection (slow but unbreakable)

We know f(0) > 0 (at 0 V the resistor offers 5 mA and the diode takes nothing) and f(5) < 0 (at 5 V the diode wants an astronomical current). The answer lies between. Try the middle, 2.5 V: f < 0, so the answer is in [0, 2.5]. Try 1.25: still negative, [0, 1.25]. And so on, halving each time.

Each halving gains one binary digit. Going from a 5 V interval to 1 nV takes log₂(5 × 10⁹) ≈ 32.2, so 33 halvings. The script confirms: **33 halvings**, V = 0.692543634 V. Bisection always works in one dimension, but it is slow, and it does not generalise to a thousand unknowns (there is no "middle" of a thousand-dimensional box that tells you which half to keep).

### Method 4: Newton-Raphson

The idea, in words: at your current guess, pretend the curve is a straight line (its tangent), find where that straight line hits zero, and make that your next guess.

```
  f(V)
    |\
    | \        the curve f(V)
    |  \
    |   *  <- guess V_k: draw the tangent here
    |    \ \
    |     \  \  tangent line
    |------\---x--------------- f = 0
    |       \  ^
    |        \ next guess V_(k+1): where the tangent crosses zero
```

The slope of a curve is its **derivative**, written f'(V). A straight line through the point (V_k, f(V_k)) with slope f'(V_k) crosses zero at

```
V_(k+1) = V_k − f(V_k) / f'(V_k)
```

Read: "the next guess equals the current guess minus the mismatch divided by the slope". For our circuit the slope is

```
f'(V) = −1/R − (I_S / V_T) × e^(V/V_T)
```

The first term is the resistor's conductance, the second the diode's **small-signal conductance**, g_d = I_S e^(V/V_T) / V_T ≈ I / V_T. (At 4.3 mA, g_d = 0.0043 / 0.02585 = 0.167 siemens: the diode "looks like" a 6 Ω resistor for small changes. Remember this; Phase 12 builds amplifiers on the same idea.)

**Why Newton is so good.** Near the answer, each step roughly *squares* the error: 10⁻³ becomes 10⁻⁶, then 10⁻¹², then the limit of computer arithmetic. The digits of accuracy double every step. This is called quadratic convergence, and you can watch it in the last lines of the run:

```
step 29: V = 0.692588051998 V   current mismatch = 7.452e-06 A
step 30: V = 0.692543671092 V   current mismatch = 6.355e-09 A
step 31: V = 0.692543633181 V   current mismatch = 4.613e-15 A
```

**Why Newton can be terrible.** But look at the *first* steps from 0.6 V:

```
step   0: V = 0.600000000000 V   current mismatch = 4.280e-03 A
step   1: V = 1.358064951864 V   current mismatch = 6.524e+08 A
step   2: V = 1.332212951865 V   current mismatch = 2.400e+08 A
step   3: V = 1.306360951865 V   current mismatch = 8.829e+07 A
```

At 0.6 V the diode curve is still fairly flat (0.12 mA), so its tangent is shallow, and the tangent's zero crossing lands far away, at 1.36 V. There the diode would carry 650 million amps. From such a point, the exponential is a near-vertical wall; each Newton step on e^x from far above moves down by exactly one V_T, 25.85 mV. The script counts: **32 steps** from 0.6 V, and **173 steps** from 0 V. A real simulator also risks overflowing the computer's number range (e^710 is the largest double), which our simulator guards against with a capped exponential.

### Fixing Newton: junction hold-back

The cure, invented for the very first circuit simulators (SPICE, Berkeley, 1970s) and used in ours, is to **refuse big upward jumps in a junction voltage**. If Newton proposes to raise the diode voltage by much more than V_T, ask instead: "what current did the tangent line predict at the proposed voltage?" and move the voltage only as far as the *real* exponential needs to deliver that current. That needs a logarithm:

```
if V_new > V_base + 2 V_T:
    V_new = V_base + V_T × ln(1 + (V_new − V_base) / V_T)
```

where V_base is the larger of the old voltage and a "knee" voltage V_T ln(V_T / I_S) ≈ 0.74 V. At that voltage the diode carries about 26 mA and its slope is 1 siemens (it behaves like a 1 Ω resistor for small changes): above it the exponential is a cliff, below it big steps are harmless. A step of +0.76 V proposed from 0.6 V becomes a step to 0.82 V. Results:

| Start | Plain Newton | Newton with hold-back |
|---|---|---|
| 0.0 V | 173 steps | 13 steps |
| 0.6 V | 32 steps | 11 steps |
| 0.8 V | 9 steps | 9 steps |

From 0.8 V (just above the answer) the hold-back never triggers: Newton is already on the steep side, where it behaves well.

### From one diode to a whole circuit: companion models

Newton's step "replace the curve by its tangent" has a beautiful circuit meaning. Near the guess V_k, the diode current is approximately

```
I ≈ I(V_k) + g_d × (V − V_k)  =  g_d × V  +  I_eq,      with  I_eq = I(V_k) − g_d × V_k
```

Read: "the diode current is about a conductance g_d times V, plus a constant current I_eq". A conductance plus a constant current source in parallel: that is a **linear** circuit element! It is the diode's **companion model**:

```
         diode                       companion model at guess V_k
   a ---|>|--- 0         ==>     a ---+--- /\/\/ (1/g_d) ---+--- 0
                                      |                     |
                                      +----- ( I_eq ) ------+
```

So one Newton iteration of a whole circuit is:

1. Replace each diode by its companion model at the current guess (a resistor and a current source).
2. Build the modified nodal analysis (MNA) matrix exactly as in Phase 05 lesson 04. It is now a linear circuit.
3. Solve it. The solution is the next guess.
4. Repeat until nothing changes.

This works for any number of diodes, transistors (with a few more entries per device) and nodes. It is exactly what our simulator's `dc()` does, and what SPICE has done since 1973.

### A two-diode network

```
         R1 1k            R2 2.2k
  +5 V --/\/\/--- a ------/\/\/\---- b
                  |                  |
                 D1                 D2
                  |                  |
                 gnd                gnd
```

Unknowns: V(in), V(a), V(b) and the source current (MNA's extra unknown for a voltage source). Both diodes start at a guess of 0.6 V. Our hand-built solver prints:

```
iter     V(in)         V(a)         V(b)  largest change
   1    5.0000   1.30450425   0.63923751       5.000e+00
   2    5.0000   0.79412294   0.61718029       5.104e-01
   3    5.0000   0.76876109   0.59983191       2.536e-02
 ...
   9    5.0000   0.69223293   0.57826188       1.034e-04
  10    5.0000   0.69223272   0.57826184       2.057e-07
  11    5.0000   0.69223272   0.57826184       8.116e-13
```

Check the answer with lesson 04's rules: D2 carries (0.6922 − 0.5783) / 2200 = 51.8 µA, and V_T ln(51.8 × 10⁻⁶ / 10⁻¹⁴) = 0.02585 × 22.37 = 0.578 V. ✓. D1 carries the rest of R1's current: 4.308 − 0.052 = 4.256 mA, and V_T ln(4.256 × 10⁻³ / 10⁻¹⁴) = 0.692 V ✓.

## Build It

### Step 1: The mismatch and its slope

```python
def mismatch(volts):
    return (SOURCE_VOLTS - volts) / RESISTOR_OHMS - diode_current(volts)


def mismatch_slope(volts):
    return -1.0 / RESISTOR_OHMS - diode_slope(volts)
```

### Step 2: The two fixed-point iterations and bisection

```python
def log_fixed_point(start, tolerance=1e-9, limit=100):
    volts = start
    history = [volts]
    for _ in range(limit):
        amps = (SOURCE_VOLTS - volts) / RESISTOR_OHMS
        new_volts = THERMAL_VOLTAGE * np.log(amps / SATURATION_CURRENT + 1.0)
        history.append(new_volts)
        if abs(new_volts - volts) < tolerance:
            break
        volts = new_volts
    return history
```

`naive_fixed_point` does the opposite order (diode current first) and blows up; `bisection` keeps the half-interval where the mismatch changes sign.

### Step 3: Newton-Raphson, with optional hold-back

```python
KNEE_VOLTS = THERMAL_VOLTAGE * np.log(THERMAL_VOLTAGE / SATURATION_CURRENT)


def hold_back(new_volts, old_volts):
    base = max(old_volts, KNEE_VOLTS)
    if new_volts > base + 2 * THERMAL_VOLTAGE:
        return base + THERMAL_VOLTAGE * np.log(1 + (new_volts - base) / THERMAL_VOLTAGE)
    return new_volts


def newton(start, tolerance=1e-9, limit=300, careful=False):
    volts = start
    history = [volts]
    for _ in range(limit):
        proposal = volts - mismatch(volts) / mismatch_slope(volts)
        if careful:
            proposal = hold_back(proposal, volts)
        step = proposal - volts
        volts = proposal
        history.append(volts)
        if abs(step) < tolerance:
            break
    return history
```

### Step 4: The companion model

```python
def diode_companion(volts):
    conductance = diode_slope(volts)
    equivalent_current = diode_current(volts) - conductance * volts
    return conductance, equivalent_current
```

### Step 5: Newton + MNA for the network

Inside `solve_two_diode_network`, each iteration builds the matrix from scratch. Resistors are stamped exactly as in Phase 05: +g on the two diagonal entries, −g on the two off-diagonal ones. Each diode adds its conductance to its node's diagonal and moves its equivalent current to the right-hand side (it is a current *leaving* the node, hence the minus sign):

```python
conductance, equivalent_current = diode_companion(junction)
matrix[k, k] += conductance
right[k] -= equivalent_current
```

The voltage source adds one extra row and column (MNA), forcing V(in) = 5 V. `np.linalg.solve` gives the next guess; the loop stops when no voltage changes by more than 1 nV and no junction was held back.

### Step 6: Compare with the simulator

```python
circuit = Circuit()
circuit.voltage_source("V1", "in", "0", SOURCE_VOLTS)
circuit.resistor("R1", "in", "a", 1000.0)
circuit.diode("D1", "a", "0", Is=SATURATION_CURRENT, n=1.0)
circuit.resistor("R2", "a", "b", 2200.0)
circuit.diode("D2", "b", "0", Is=SATURATION_CURRENT, n=1.0)
result = circuit.dc()
```

The script prints both answers side by side: the single diode at V = 0.692543633 V and I = 4.307456 mA, the network at V(a) = 0.692232716 V and V(b) = 0.578261844 V, agreeing with the simulator to about a nanovolt (both stop iterating at that tolerance).

```
uv run python phases/11-semiconductors-and-diodes/05-solving-nonlinear-circuits/code/main.py
```

## Use It

- **SPICE and all its descendants** (ngspice, LTspice, Cadence Spectre, Qucs) solve DC operating points with exactly this loop: companion models, MNA, Newton-Raphson, junction limiting. When LTspice reports "convergence failed", it means this loop did not settle.
- **Simulator tricks when Newton struggles**: *gmin stepping* (put a large conductance across every junction, solve, then shrink it step by step), *source stepping* (ramp all supplies up from 0 V, re-using each answer as the next guess). Our simulator adds a tiny gmin (a very large resistor) across junctions for the same reason.
- **Transient simulation** (Phase 07 lesson 08) runs this Newton loop at every time step, using the previous instant's answer as the first guess. Because that guess is close, it usually converges in 2-4 iterations.
- **Beyond circuits**: Newton-Raphson computes square roots in your calculator, trains some machine-learning models, and finds orbits in astronomy. The "linearise, solve, repeat" pattern is everywhere.

## Try It in the Lab

This lab builds a cheap voltage reference from two diodes in series. A 9 V supply feeds them through an empty resistor slot. You must choose the resistor so the two diodes stack up to a reference voltage in the target window while carrying a sensible current: enough to be well into conduction, not so much that the resistor and diodes waste power.

Think first: what does each diode drop at about 1-5 mA? So what does the resistor see? Then try the "wrong" resistors and notice how little the reference voltage moves when the current changes ten-fold: that insensitivity is exactly why diodes are used as references.

## Common Mistakes

- **Using Ohm's law on the diode.** "The diode has 0.7 V and 4.3 mA, so it's a 163 Ω resistor": that ratio V/I changes completely at another current. Only the tangent slope (small-signal conductance) is useful, and only near one operating point.
- **Iterating in the wrong direction.** Feeding a voltage into an exponential and then into a big resistor amplifies errors (Method 1). If you iterate by hand, go through the logarithm.
- **Expecting Newton to always converge fast.** Its fast convergence is only near the answer. Far away, exponential devices make it overshoot or crawl, and it needs limiting.
- **Starting from a terrible guess.** Simulators usually start junctions near 0.6 V, not 0 V or 5 V, for good reason.
- **Stopping too early.** Stop when the change between guesses is tiny *and* the mismatch is tiny; a held-back step can look small without being converged.
- **Forgetting the sign of I_eq.** It is the companion current flowing *out of* the anode node through the diode; it goes to the right-hand side with a minus sign.

## Exercises

1. Do two iterations of the rearranged fixed-point method by hand (with a calculator) for a 3.3 V source, 330 Ω resistor and I_S = 10⁻¹⁴ A, starting from V = 0.7 V.
2. Compute the Newton step by hand from V = 0.7 V for the lesson's 5 V, 1 kΩ circuit. Is the next guess above or below the true answer? Why?
3. Count the halvings bisection needs to go from a 10 V interval to 1 µV. How many would Newton need, roughly, once it is within 1 mV?
4. Change `solve_two_diode_network` to start both diodes at 0.0 V and remove the hold-back. How many iterations now? Then restore the hold-back but keep the 0.0 V start.
5. Add a third branch to the network: R3 = 4.7 kΩ from b to a node c, with a diode D3 from c to ground. Extend the hand-built solver (one more node, one more diode stamp) and check against the simulator.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Operating point | "The DC solution", "bias point" | The steady voltages and currents where every part's law and Kirchhoff's laws hold together |
| Load line | "The resistor line" | The straight line I = (V_source − V)/R; its crossing with the device curve is the operating point |
| Newton-Raphson | "Newton's method" | Iterate V ← V − f(V)/f'(V): replace the curve by its tangent, jump to the tangent's zero |
| Quadratic convergence | "It converges really fast" | Near the root, the error is roughly squared each step: digits double |
| Companion model | "Linearised diode" | A conductance g_d = I/V_T in parallel with a current source I_eq, equal to the tangent at the guess |
| Junction limiting | "pnjlim", "hold-back" | Shrinking large upward steps of junction voltages so the exponential cannot explode |
| Small-signal conductance | "g_d", "dynamic resistance" | The slope dI/dV of the diode at its operating point, about I/V_T |

## Further Reading

- L. W. Nagel, *SPICE2: A Computer Program to Simulate Semiconductor Circuits*, University of California, Berkeley, Memo ERL-M520, 1975: the original description of companion models and junction limiting. https://www2.eecs.berkeley.edu/Pubs/TechRpts/1975/ERL-520.pdf
- MIT OpenCourseWare 6.002, lectures on nonlinear analysis and the incremental (small-signal) model. https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/
- *All About Circuits*, Volume III, chapter 3, "SPICE models". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-3/spice-models/
- G. Strang, *Calculus* (MIT OpenCourseWare free textbook), section 3.7 "Newton's Method (and Chaos)". https://ocw.mit.edu/courses/res-18-001-calculus-fall-2023/
