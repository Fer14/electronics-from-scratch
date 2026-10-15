# Systematic Analysis

> A method beats a trick: name the unknowns, write one honest equation for each, and let arithmetic finish the job.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Phase 04 (Kirchhoff's Laws), especially Lesson 01 (Nodes, Branches and Loops), Lesson 02 (Kirchhoff's Current Law) and Lesson 03 (Kirchhoff's Voltage Law)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Analysis (of a circuit) | Finding every voltage and every current in a circuit whose parts and connections you already know | Working out every family member's age from a list of clues |
| Unknown | A number you do not know yet and give a name to, like `i2` or `vb` | The blank box in a puzzle |
| Equation | A sentence that says two amounts are equal, written with symbols | A balanced kitchen scale |
| System of equations | Several equations that must all be true at the same time, sharing the same unknowns | Several clues about the same family, all true together |
| Linear | Every unknown appears only multiplied by a fixed number and added, never squared, never multiplied by another unknown | Prices at a market: twice the apples costs twice the money |
| Branch current | The current through one branch (one element) of the circuit | The flow of cars on one street |
| Branch current method | Analysis where the unknowns are the currents in every branch | Counting cars on every street of a town |
| Independent equation | An equation that says something the others do not already imply | A clue that is not just a rephrasing of an earlier clue |
| Matrix | A rectangular table of numbers, used to store the multipliers of a system of equations | A spreadsheet of coefficients |
| Vector | A single column (or row) of numbers, such as the list of all unknowns | A shopping list |
| Simulator | A program that writes and solves a circuit's equations for you | A calculator that understands drawings |
| Netlist | A text list of parts, each with the nodes it connects and its value | A seating plan: who sits between whom |

## Learning Objectives

- Explain why series-parallel simplification fails for circuits with more than one source or with bridges.
- Follow a fixed four-step recipe to analyse any resistor circuit: name, choose unknowns, write equations, solve.
- Count how many unknowns and how many independent equations a circuit needs with the branch current method.
- Solve a small system of linear equations by substitution, and write the same system as a matrix.
- Describe a circuit to our simulator (`sim`) as a netlist, run a DC analysis and check its answer with Kirchhoff's laws.

## The Problem

Here is a circuit you will meet in every lesson of this phase. It has a 12 volt battery, four resistors and a current source.

```
        a      R1 = 1 kΩ      b      R3 = 3 kΩ      c
   ┌────●────/\/\/\/\────●────/\/\/\/\────●──────────┐
   │                     │                 │          │
  +│                     │                 │          │
 [V1] 12 V             [R2] 2 kΩ         [R4] 1 kΩ  (I1) 1 mA, arrow up
  -│                     │                 │          │
   │                     │                 │          │
   └─────────────────────┴─────────────────┴──────────┘
                         gnd (0 V)
```

Symbols, so nobody gets lost:

- `V1` is a **voltage source** (a battery, here an ideal one): it keeps node `a` exactly 12 volts (V) above the bottom wire.
- `R1` to `R4` are **resistors**, measured in ohms (Ω). `1 kΩ` means 1000 Ω (k is "kilo", a thousand).
- `I1` is a **current source**: a part that pushes a fixed current, here 1 milliampere (1 mA = 0.001 A), no matter what voltage that takes. The arrow points up, so it pushes current from the bottom wire up into node `c`. You will meet real current sources in Phase 06 and Phase 12; for now think of it as a pump that always moves exactly 1 mA.
- `gnd` is **ground**, the node we agree to call 0 V. Every other node voltage is measured from it.

Question: what is the voltage at node `b`, and what current flows in each resistor?

Try your Phase 04 tools. Is R2 in series with R3? No: node `b` has three things touching it (R1, R2, R3), and series needs exactly two. Is R4 in parallel with R2? No: they do not share both ends. The voltage divider formula needs a single chain from one source; here there are two sources, V1 and I1, both pushing. No trick fits.

This is the normal situation in real electronics. The circuit inside a phone charger, a guitar pedal or a car's sensor board has dozens of nodes and several sources. Engineers do not look for clever tricks. They follow a recipe that works every time, and they hand the arithmetic to a computer. This lesson is that recipe in its plainest form, and the first time you hand a circuit to our own simulator.

## The Physics

Why should a circuit like this have one and only one answer? Three physical facts pin it down.

1. **Charge is conserved and does not pile up in wires.** Electrons are not created or destroyed, and in a steady (DC, direct current) circuit they cannot accumulate at a node, because a node is just metal and any pile of charge would push itself away immediately. So whatever current flows into a node must flow out. That is Kirchhoff's current law (KCL).
2. **Energy per charge is a property of the place.** Voltage is the energy each coulomb of charge has at a point (Phase 01, Lesson 04). If you walk a charge around a closed path and come back to the start, it is back at the same place, so it has the same energy per charge. The rises and drops along the way must cancel. That is Kirchhoff's voltage law (KVL).
3. **Each part has its own rule linking its voltage and its current.** For a resistor that rule is Ohm's law: voltage across equals current through times resistance, `V = I × R`. For an ideal battery the rule is "voltage across is fixed". For a current source it is "current through is fixed".

Each of these facts gives an equation. Put enough of them together and the unknowns have nowhere to hide. Because Ohm's law is a straight-line rule (double the current, double the voltage), all the equations are **linear**: unknowns are only multiplied by fixed numbers and added. Linear systems are the friendliest kind of mathematics there is: if they have the right number of independent equations, they have exactly one answer, and a computer can find it in microseconds even with thousands of unknowns.

What this picture leaves out: real parts are only approximately linear. A resistor heats up and its resistance changes a little (Phase 03, Lesson 07). A diode is wildly non-linear (Phase 11). For those, simulators solve a linear system over and over, nudging the answer each time. Everything you learn here is the inner step of that loop.

## The Concept

### The four-step recipe

Every analysis method in this phase is a variation of the same four steps.

```
1. NAME      Give every node a name. Pick one node as ground (0 V).
             Give every unknown a name and a direction.
2. CHOOSE    Decide which quantities are the unknowns
             (branch currents? node voltages? loop currents?).
3. WRITE     Write one independent equation per unknown,
             using KCL, KVL and each part's own rule (Ohm's law...).
4. SOLVE     Solve the system. Then check the answer with a law
             you did not use.
```

The methods differ only in step 2. This lesson uses the most direct choice, the **branch current method**: the unknowns are the currents in the resistors. Lesson 02 (nodal analysis) and Lesson 03 (mesh analysis) choose smarter unknowns so there are fewer of them.

### Step 1 for our circuit: names and directions

The circuit has four nodes: `a`, `b`, `c` and ground. Node `a` is fixed at 12 V by the battery, so it is not really unknown.

We give every resistor current a name and an arrow. The arrow is a *guess* of the direction. If the guess is wrong, the number simply comes out negative; nothing breaks.

```
   a ──R1──▶ b ──R3──▶ c
             │          │
             R2 ▼       R4 ▼
             │          │
            gnd        gnd

   i1 : through R1, from a to b
   i2 : through R2, from b down to ground
   i3 : through R3, from b to c
   i4 : through R4, from c down to ground
```

Four unknowns: `i1`, `i2`, `i3`, `i4`. So we need four independent equations.

### Step 3: where the four equations come from

**KCL at node b.** Read it as a sentence first: "the current arriving at b through R1 equals the current leaving b through R2 plus the current leaving through R3."

```
i1 = i2 + i3
```

**KCL at node c.** "What arrives at c (through R3, plus the 1 mA pushed up by the current source) equals what leaves through R4."

```
i3 + 1 mA = i4
```

Why not KCL at ground too? Try it: it says "i2 + i4 = i1 + 1 mA". Add the two equations above and you get exactly that. It brings no new information. In a circuit with N nodes, KCL gives only N - 1 independent equations; the last node's equation is always the sum of the others. (Phase 04, Lesson 02 showed why: every current that leaves one node enters another.)

**KVL around the left window (V1, R1, R2).** "The 12 V the battery gives is used up by the drop across R1 and the drop across R2." Each drop is Ohm's law, current times resistance:

```
12 V = 1 kΩ × i1 + 2 kΩ × i2
```

**KVL around the middle window (R2, R3, R4).** Node b has some voltage. Going down through R2 to ground loses all of it. Going right through R3 and then down through R4 to ground also loses all of it. Same start, same end, so the two drops are equal:

```
2 kΩ × i2 = 3 kΩ × i3 + 1 kΩ × i4
```

What about the right window, with the current source? A current source can have any voltage across it (it adjusts to push its current), so KVL around a loop containing it introduces a new unknown, its voltage. That loop would add an equation *and* an unknown, so it does not help. We skip it. This is our first hint that current sources and voltage sources need special care; Lessons 02 to 04 deal with them properly.

### A unit trick that saves your sanity

Working in kilo-ohms and milliamps is a gift: **1 kΩ × 1 mA = 1000 Ω × 0.001 A = 1 V**. So if every resistance is written in kΩ and every current in mA, Ohm's law gives volts directly with no powers of ten. Our four equations become:

```
(1)   i1 - i2 - i3        = 0
(2)             i3 - i4   = -1
(3)   i1 + 2 i2           = 12
(4)       2 i2 - 3 i3 - i4 = 0
```

(currents in mA, the right-hand numbers in mA for KCL rows and in V for KVL rows).

### Step 4: solve by substitution

The plan: use the simple equations to eliminate unknowns one by one.

From (1): `i1 = i2 + i3`. From (2): `i4 = i3 + 1`.

Put both into (3): `(i2 + i3) + 2 i2 = 12`, which tidies to

```
3 i2 + i3 = 12                      (5)
```

Put `i4 = i3 + 1` into (4): `2 i2 - 3 i3 - (i3 + 1) = 0`, which tidies to

```
2 i2 - 4 i3 = 1                     (6)
```

Now two equations, two unknowns. From (5): `i3 = 12 - 3 i2`. Put that into (6):

```
2 i2 - 4 (12 - 3 i2) = 1
2 i2 - 48 + 12 i2    = 1
14 i2                = 49
i2                   = 3.5 mA
```

Back-substitute: `i3 = 12 - 3 × 3.5 = 12 - 10.5 = 1.5 mA`, `i1 = 3.5 + 1.5 = 5 mA`, `i4 = 1.5 + 1 = 2.5 mA`.

Node voltages then follow from Ohm's law: `vb = 2 kΩ × 3.5 mA = 7 V` (R2 sits between b and ground), and `vc = 1 kΩ × 2.5 mA = 2.5 V`.

### Check with a law you did not use

Always check. Let's use KVL around the outer path a → b → c → ground → a, which we never wrote:

```
drop across R1 : 1 kΩ × 5 mA   = 5   V
drop across R3 : 3 kΩ × 1.5 mA = 4.5 V
drop across R4 : 1 kΩ × 2.5 mA = 2.5 V
total                          = 12  V    equals V1. Correct.
```

And power, as a sanity check: the resistors burn `5² × 1 + 3.5² × 2 + 1.5² × 3 + 2.5² × 1 = 25 + 24.5 + 6.75 + 6.25 = 62.5 mW` (mA² × kΩ gives mW). The battery delivers `12 V × 5 mA = 60 mW`, the current source delivers `2.5 V × 1 mA = 2.5 mW` (it pushes 1 mA up to a node at 2.5 V). Total supplied 62.5 mW, total burned 62.5 mW. Energy is conserved, so we trust the answer.

### Counting: how big does this get?

The branch current method needs one unknown per resistor. A circuit with B branches and N nodes gives N - 1 KCL equations and B - N + 1 independent KVL equations (Phase 04, Lesson 01): exactly B equations in total. Fine for 4 resistors, painful for 400.

Compare the unknowns each method needs for our circuit:

| Method | Unknowns | Count here |
|---|---|---|
| Branch currents (this lesson) | one current per resistor | 4 |
| Node voltages (Lesson 02) | one voltage per node that is not ground and not fixed by a battery | 2 (vb, vc) |
| Mesh currents (Lesson 03) | one current per window of the drawing | 2 |

Fewer unknowns means less work by hand. A computer does not care much, but it does care about one thing: the method must be *automatic*, with no human judgement like "this loop is awkward, skip it". That is what Lesson 04 builds.

### Matrices: the same equations, tidied up

Look at equations (1)-(4) again. If we write the unknowns always in the same order (i1, i2, i3, i4) and fill missing ones with 0, the equations become a table of multipliers and a column of right-hand numbers:

```
        i1   i2   i3   i4        right side
(1)  [   1   -1   -1    0 ]        [  0 ]
(2)  [   0    0    1   -1 ]        [ -1 ]
(3)  [   1    2    0    0 ]        [ 12 ]
(4)  [   0    2   -3   -1 ]        [  0 ]
```

The table on the left is a **matrix**, usually called `A`. The list of unknowns is a **vector** `x = [i1, i2, i3, i4]`, and the right side is a vector `b`. The whole system is written in three symbols:

```
A x = b
```

Read it out loud as: "for each row, multiply each number in the row by the matching unknown, add them up, and you get that row's right-hand number." Nothing more mysterious than that. The point of writing it this way is that solving `A x = b` is a solved problem: NumPy has `np.linalg.solve(A, b)`, which does the elimination we did by hand, for any size, in a fraction of a millisecond.

### Handing the circuit to a simulator

A simulator goes one step further: you do not even write the equations. You only describe the parts and what they connect, a **netlist**:

```
V1  a  0  12 V
R1  a  b  1 kΩ
R2  b  0  2 kΩ
R3  b  c  3 kΩ
R4  c  0  1 kΩ
I1  0  c  1 mA     (current flows from node 0, through the source, into c)
```

The simulator builds the equations (Lesson 04 shows exactly how) and solves them. The course's simulator lives in the `sim/` folder of this repository. You will use it from now on, but never as a black box: by the end of this phase you will have written its core yourself.

## Build It

The code in `code/main.py` does the same analysis three ways: by solving the branch-current matrix with NumPy, with our simulator, and with a final check of the laws.

### Step 1: the branch-current system as a matrix

We write the four equations exactly as above, in kΩ, mA and V.

```python
import numpy as np

branch_matrix = np.array([
    [1.0, -1.0, -1.0, 0.0],
    [0.0, 0.0, 1.0, -1.0],
    [1.0, 2.0, 0.0, 0.0],
    [0.0, 2.0, -3.0, -1.0],
])
right_side = np.array([0.0, -1.0, 12.0, 0.0])
branch_currents_ma = np.linalg.solve(branch_matrix, right_side)
```

The result is `[5.0, 3.5, 1.5, 2.5]` mA, exactly what we found by hand.

### Step 2: describe the circuit to the simulator

Each line of the netlist becomes one method call. Values are in plain SI units (ohms, volts, amperes), so 1 kΩ is `1000` and 1 mA is `0.001`.

```python
from sim import Circuit

def build_workhorse():
    circuit = Circuit()
    circuit.voltage_source("V1", "a", "0", 12.0)
    circuit.resistor("R1", "a", "b", 1000)
    circuit.resistor("R2", "b", "0", 2000)
    circuit.resistor("R3", "b", "c", 3000)
    circuit.resistor("R4", "c", "0", 1000)
    circuit.current_source("I1", "0", "c", 0.001)
    return circuit
```

### Step 3: run a DC analysis

"DC analysis" (also called the **operating point**) means: find the steady voltages and currents when nothing is changing in time.

```python
result = build_workhorse().dc()
print(result.table())
for name in ("R1", "R2", "R3", "R4"):
    print(name, result.i(name) * 1000, "mA")
```

`result.v("b")` is the voltage at node b measured from ground, and `result.i("R1")` is the current through R1 in the direction from its first node to its second (a to b). Our arrows were chosen to match the order of the nodes in the netlist, so the signs agree.

### Step 4: check Kirchhoff's laws on the simulator's answer

A result is only as good as its checks. We verify KCL at b and c and KVL around the outer loop, using only the simulator's numbers:

```python
kcl_b = result.i("R1") - result.i("R2") - result.i("R3")
kcl_c = result.i("R3") + 0.001 - result.i("R4")
kvl_outer = 12.0 - 1000 * result.i("R1") - 3000 * result.i("R3") - 1000 * result.i("R4")
```

All three print as essentially zero: a few picoamps (10⁻¹² A) for KCL and about 10⁻¹⁶ V for KVL. The picoamps come from a hidden, tiny conductance the simulator adds from every node to ground (called gmin, explained in Lesson 04); compared with milliamps, they are a billion times too small to matter.

### Step 5: the power budget

Finally we check energy conservation: power delivered by the sources equals power burned in resistors (62.5 mW each).

Run it:

```
uv run python phases/05-circuit-analysis-and-our-simulator/01-systematic-analysis/code/main.py
```

## Use It

- **Every circuit simulator works this way.** SPICE (born at UC Berkeley in the early 1970s), LTspice from Analog Devices, ngspice, Qucs, the simulators inside KiCad and every chip-design tool: you give them a netlist, they build a linear system and solve it. A modern chip simulation can have millions of unknowns; the method is the same as the 4×4 you solved by hand.
- **Design reviews.** When an engineer checks a board, they do a quick "hand analysis" of a few key nodes (exactly like our substitution) and compare it with the simulator. If the two disagree, either the model or the netlist has a mistake. Never trust one without the other.
- **Power budgets.** The power check you did is what a power engineer does for a whole product: add up what every part burns and compare it with what the battery or supply delivers. If the numbers do not match, something is miswired.
- **Sensor front ends.** A strain gauge, a thermistor or a light sensor usually sits in a network with two or more sources (a supply and a reference). Their outputs can only be predicted with a systematic method.

## Try It in the Lab

Open the lab task for this lesson. The board is our workhorse circuit, but resistor R2 between node b and ground is missing. You have three resistors to choose from. The goal is to put node b near 7 V and node c near 2.5 V at the same time.

Things to think about before you press RUN:

- How does the voltage at b change if the resistor from b to ground gets larger? Smaller? (Imagine the extremes: a short and an open.)
- Does the current source alone fix node c, or does c also depend on b?
- Can you predict the right answer without the simulator using the numbers in this lesson?

## Common Mistakes

- **Writing KCL at every node, including ground.** The last KCL equation is always the sum of the others. If you include it and drop a KVL equation instead, your system has no unique answer (NumPy will complain the matrix is "singular").
- **Writing KVL around a loop that contains a current source** without adding the source's voltage as a new unknown. A current source's voltage is not zero and not known in advance.
- **Mixing units.** Writing 1000 for one resistor and 2 for another, or amps in one equation and milliamps in another. Pick a system (SI everywhere, or kΩ-mA-V everywhere) and stick to it.
- **Thinking a negative answer is an error.** It only means the real current flows opposite to the arrow you drew. Keep the sign; the arrow and the sign together tell the truth.
- **Skipping the check.** A system with a typo in one coefficient still produces an answer, just a wrong one. A KVL or power check you did not use to build the system catches it.
- **Trusting the simulator blindly.** A simulator solves the circuit you typed, not the one you meant. A wrong node name (`"b"` vs `"B"`) silently creates a new, disconnected node.

## Exercises

1. In the workhorse circuit, compute the power burned in each resistor separately (in mW) and confirm they add up to 62.5 mW.
2. Change the current source to 2 mA (still pushing up into c). Re-solve the branch-current system by hand. What are the new i1 to i4, vb and vc? (Answer to check: vb ≈ 7.14 V.)
3. Reverse the current source (it now pulls 1 mA out of c and pushes it into ground). Predict without solving: does vc go up or down? Then edit `main.py` and confirm.
4. Count unknowns: a circuit has 7 nodes (including ground), 11 resistors and one battery from one node to ground. How many unknowns does the branch current method need? How many does a method using node voltages need?
5. Harder: replace R2 by a 6 kΩ resistor. Set up the four branch-current equations, solve them with `np.linalg.solve`, and check the result with the simulator and with a power budget.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Circuit analysis | "Working out the circuit" | Finding every node voltage and branch current from the parts and connections |
| Branch current method | "Write KCL and KVL everywhere" | Unknowns are the currents in every branch; N - 1 KCL equations plus B - N + 1 KVL equations |
| Independent equation | "Another equation" | An equation that cannot be built by adding or scaling the others |
| Linear system | "A bunch of equations" | Equations where unknowns are only scaled and added, written `A x = b`, with one solution when the rows are independent |
| Matrix | "A grid of numbers" | A table storing the multiplier of every unknown in every equation |
| Netlist | "The circuit file" | A list of parts, the nodes each one connects, and its value |
| DC analysis / operating point | "Run the sim" | Solving for steady voltages and currents when nothing changes in time |

## Further Reading

- *The Art of Electronics*, Horowitz and Hill, 3rd edition, Chapter 1 (sections 1.2 and 1.3): voltage, current, resistance and the habit of quick hand analysis that real engineers use.
- [All About Circuits, Vol. I, Chapter 10 "DC Network Analysis"](https://www.allaboutcircuits.com/textbook/direct-current/chpt-10/what-is-network-analysis/): a free textbook chapter covering branch current, mesh and nodal methods.
- [MIT OpenCourseWare 6.002 Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/), lectures 2 and 3: the "basic method" of writing KCL and KVL systematically.
- Nagel, L. W., *SPICE2: A Computer Program to Simulate Semiconductor Circuits*, UC Berkeley memo ERL-M520 (1975): the thesis behind the simulator that every modern tool descends from.
