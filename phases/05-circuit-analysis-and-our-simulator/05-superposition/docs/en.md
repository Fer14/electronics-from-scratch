# Superposition

> In a linear circuit, every source does its own work independently. Switch all but one off, see what it does, repeat, and add up the results.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 04 (Kirchhoff's Laws), especially Lesson 04 (Series and Parallel Resistors) and Lesson 05 (The Voltage Divider); Phase 05 Lesson 01 (Systematic Analysis) and Lesson 02 (Nodal Analysis)
**Time:** ~55 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Superposition | Adding up the separate effects of several causes to get their combined effect | Two people pushing a car: the total push is the sum of the two pushes |
| Linear (circuit) | A circuit where doubling every source doubles every voltage and current | A recipe: double the ingredients, double the cake |
| Turning a source off | Setting a source's value to zero while keeping it in place | Turning a tap to zero, without removing the pipe |
| Short circuit (short) | A plain wire: zero voltage across it, any current through it | An open archway between two rooms |
| Open circuit (open) | A gap: zero current through it, any voltage across it | A wall with no door |
| Contribution | The part of a voltage or current caused by one particular source | Each person's share of the total push |
| Transfer coefficient | The fixed number that converts one source's value into its contribution at some node | The exchange rate between a cause and its effect |
| Offset | A constant extra voltage added to a signal | The height of a table that every object on it inherits |
| Bias | The steady DC voltage or current that keeps a part in its working range, with a small signal riding on top | The tension in a guitar string before you pluck it |

## Learning Objectives

- State the superposition principle and explain why it follows from linearity.
- Turn sources off correctly: an ideal voltage source becomes a short, an ideal current source becomes an open.
- Solve a two-source circuit by solving two one-source circuits with series-parallel rules and adding the results.
- Show with numbers that power does not superpose, and explain why.
- Use our simulator to compute each source's contribution and verify the sum.

## The Problem

You have solved the workhorse circuit three times now (Lessons 01 to 04): `vb = 7 V`, `vc = 2.5 V`. Every time, you needed a full system of equations. But each source on its own would give a circuit simple enough for Phase 04's series-parallel rules: one battery with a few resistors is just dividers.

What if you could split the problem: "how much of the 7 V at node b is caused by the battery, and how much by the current source?" Then you could solve two easy circuits instead of one hard one. Better still, you would *understand* the circuit: you would know which source controls which node and how strongly.

That is not just a classroom convenience. Real circuits are full of situations where several signals add:

- a microphone signal riding on a DC bias voltage inside an amplifier;
- an audio mixer adding three instruments into one output;
- a sensor reading plus an unwanted offset plus noise.

Engineers analyse each contribution separately. The tool that makes this legitimate is **superposition**.

## The Physics

Why should effects add? Think back to the three ingredients of every equation in this phase:

- KCL: currents at a node add to zero (adding);
- KVL: voltages around a loop add to zero (adding);
- Ohm's law: `V = R × I` (multiplying by a fixed number).

Every rule is made of only two operations: adding, and multiplying by a fixed number. Rules like that are called **linear**. A linear system has a remarkable property: if solution A satisfies all the rules with source 1 alone, and solution B satisfies them with source 2 alone, then A + B satisfies them with both sources together. Check it on Ohm's law: if `V_A = R × I_A` and `V_B = R × I_B`, then `V_A + V_B = R × (I_A + I_B)`. The sum of two valid solutions is a valid solution, for every resistor, every node and every loop at once. And since the solution is unique (Lesson 01), A + B *is* the answer.

Physically, you can picture the electric field in the wires: each source sets up its own pattern of field and current, and in a linear material (like a resistor at a steady temperature) those patterns simply overlap without disturbing each other. The name "superposition" means exactly that: laying one picture on top of another.

What this gets wrong: real parts are only linear within limits. A resistor heats up and changes value; a diode, a transistor or a lamp filament is strongly non-linear. In non-linear circuits superposition fails, and you will see in Phase 12 how engineers still use it for *small* signals around a fixed bias, where the circuit looks linear enough.

## The Concept

### The rule

```
In a linear circuit with several independent sources:

1. Keep ONE source on. Turn every other independent source OFF:
     voltage source  ->  0 V  ->  replace it by a wire  (short)
     current source  ->  0 A  ->  remove it, leave a gap (open)
   Leave every resistor exactly where it is.
2. Solve that one-source circuit (often series-parallel is enough).
3. Repeat for each source.
4. Add the contributions, with their signs.
```

### Why a dead voltage source is a wire and a dead current source is a gap

A voltage source's rule is "the voltage across me is V". Set V = 0: "the voltage across me is zero, whatever current flows". That is exactly a wire.

A current source's rule is "the current through me is I". Set I = 0: "no current flows through me, whatever voltage is across me". That is exactly a gap.

Beginners often do it backwards ("remove the battery", "short the current source"). Removing a battery breaks the loop it was part of; shorting a current source steals current paths. Both give wrong answers. Ask yourself each time: "what does zero mean for *this* kind of source?"

### The workhorse, battery alone

```
        a      R1 = 1 kΩ      b      R3 = 3 kΩ      c
   ┌────●────/\/\/\/\────●────/\/\/\/\────●──────┐
   │                     │                 │      │
 [V1] 12 V             [R2] 2 kΩ         [R4] 1 kΩ   (I1 removed: open)
   │                     │                 │      
   └─────────────────────┴─────────────────┘
```

With the current source gone, R3 and R4 are in series: `3 + 1 = 4 kΩ` from b to ground. That is in parallel with R2:

```
R2 ∥ (R3 + R4) = (2 × 4) / (2 + 4) = 8/6 = 1.333 kΩ
```

Now V1, R1 and that 1.333 kΩ form a plain voltage divider:

```
vb' = 12 V × 1.333 / (1 + 1.333) = 12 × 0.5714 = 6.857 V
```

And node c sits on the R3-R4 divider below b:

```
vc' = vb' × 1 / (3 + 1) = 6.857 / 4 = 1.714 V
```

(The prime ' marks "the contribution from V1".)

### The workhorse, current source alone

```
        a      R1 = 1 kΩ      b      R3 = 3 kΩ      c
   ┌────●────/\/\/\/\────●────/\/\/\/\────●──────────┐
   │                     │                 │          │
 (wire: V1 = 0 V)      [R2] 2 kΩ         [R4] 1 kΩ  (I1) 1 mA up
   │                     │                 │          │
   └─────────────────────┴─────────────────┴──────────┘
```

The battery became a wire, so node a is now at ground and R1 goes from b to ground, in parallel with R2:

```
R1 ∥ R2 = (1 × 2) / (1 + 2) = 0.6667 kΩ
```

From node c, the current source sees two paths to ground: R4 directly (1 kΩ), and R3 followed by `R1 ∥ R2` (`3 + 0.6667 = 3.6667 kΩ`). In parallel:

```
R_seen = (1 × 3.6667) / (1 + 3.6667) = 0.7857 kΩ
vc'' = 1 mA × 0.7857 kΩ = 0.7857 V
```

Node b sits on the divider from c down through R3 and `R1 ∥ R2`:

```
vb'' = vc'' × 0.6667 / 3.6667 = 0.7857 × 0.1818 = 0.1429 V
```

(Double prime '' marks "the contribution from I1".)

### Add them

```
vb = vb' + vb'' = 6.857 + 0.143 = 7.000 V
vc = vc' + vc'' = 1.714 + 0.786 = 2.500 V
```

Exactly the answer from the full systems of Lessons 01 to 04. Two easy problems replaced one hard one, and now we also know that node b is almost entirely controlled by the battery (98 %), while node c is about two-thirds battery and one-third current source.

### A second example: two batteries

Superposition is just as handy when every source is a battery. Take the two-battery circuit of Lesson 03: a 9 V battery feeding node b through R1 = 1 kΩ, a 3 V battery feeding node b through R3 = 1 kΩ, and R2 = 2 kΩ from b to ground.

```
   ┌──[R1 1 kΩ]──● b ──[R3 1 kΩ]──┐
   │             │                 │
 [9 V]        [R2 2 kΩ]          [3 V]
   │             │                 │
   └─────────────┴─────────────────┘
```

**9 V battery alone** (the 3 V battery becomes a wire, so R3 now runs from b to ground, beside R2):

```
R2 ∥ R3 = (2 × 1) / (2 + 1) = 0.6667 kΩ
vb' = 9 × 0.6667 / (1 + 0.6667) = 9 × 0.4 = 3.6 V
```

**3 V battery alone** (the 9 V battery becomes a wire, so R1 runs from b to ground, beside R2). The circuit is the mirror image:

```
R1 ∥ R2 = 0.6667 kΩ
vb'' = 3 × 0.4 = 1.2 V
```

**Both:** `vb = 3.6 + 1.2 = 4.8 V`, exactly what mesh analysis gave in Lesson 03. Two dividers instead of a 2×2 system, and a bonus insight: each battery reaches b with the same weight (0.4), because the circuit is symmetric. A 1 V change in either battery moves b by 0.4 V.

### Transfer coefficients: superposition as a formula

Because each contribution is proportional to its source, you can write every node voltage as a weighted sum of the sources:

```
vb = (4/7)   × V1  +  (1/7 kΩ)   × I1
vc = (1/7)   × V1  +  (11/14 kΩ) × I1
```

Check: `(4/7) × 12 = 6.857` and `(1/7) × 1 = 0.143`. The numbers 4/7 and 1/7 kΩ are **transfer coefficients**: how many volts at b per volt of V1, and how many volts at b per milliamp of I1. They depend only on the resistors. If V1 drops to 9 V because the battery is old, you know immediately: `vb = (4/7) × 9 + 1/7 = 5.286 V`, no re-solving needed.

### Currents superpose too

The current through R1 from a to b:

```
battery alone:   (12 - 6.857) / 1 kΩ = 5.143 mA
source alone:    (0 - 0.143)  / 1 kΩ = -0.143 mA   (flows from b to a)
total:                                  5.000 mA
```

Each contribution can have its own sign. Keep them.

### Power does NOT superpose

Power in a resistor is `P = V² / R` (Phase 03, Lesson 05). Squaring is not linear: `(a + b)² = a² + 2ab + b²`, not `a² + b²`. For R4:

```
true power:          2.5²  / 1 kΩ = 6.25  mW
battery alone:       1.714² / 1 kΩ = 2.939 mW
source alone:        0.786² / 1 kΩ = 0.617 mW
sum of the two:                      3.556 mW   WRONG
```

The missing `2 × 1.714 × 0.786 = 2.694 mW` is the cross term `2ab`. Rule: superpose voltages and currents, then compute power from the totals.

### What counts as a source

Superposition is about *independent* sources: batteries, current sources, signal generators. In Lesson 08 you will meet *dependent* sources (whose value is set by another voltage or current in the circuit). They are part of the circuit's structure, like resistors, and must stay on during every step.

## Build It

`code/main.py` builds the workhorse with adjustable source values, so turning a source off is just setting its value to zero.

### Step 1: a circuit factory

```python
def build_workhorse(v1_volts, i1_amps):
    circuit = Circuit()
    circuit.voltage_source("V1", "a", "0", v1_volts)
    circuit.resistor("R1", "a", "b", 1000)
    circuit.resistor("R2", "b", "0", 2000)
    circuit.resistor("R3", "b", "c", 3000)
    circuit.resistor("R4", "c", "0", 1000)
    circuit.current_source("I1", "0", "c", i1_amps)
    return circuit
```

A 0 V voltage source in the simulator behaves exactly like a wire, and a 0 A current source exactly like a gap, which is the physics of "turning off".

### Step 2: solve three times

```python
both = build_workhorse(12.0, 0.001).dc()
battery_only = build_workhorse(12.0, 0.0).dc()
source_only = build_workhorse(0.0, 0.001).dc()
```

### Step 3: compare contributions, totals and the hand formulas

For each node and each resistor current, the code prints the two contributions, their sum and the true value. It also prints the hand results from this lesson (6.857, 0.143, 1.714, 0.786 V) for comparison.

### Step 4: transfer coefficients and linearity

Solving with `V1 = 1 V` alone and with `I1 = 1 mA` alone gives the transfer coefficients directly. The code then predicts `vb` for a few other combinations (an old 9 V battery, a reversed source) from the coefficients alone, and checks each prediction with a fresh simulation.

### Step 5: the power trap

Finally it compares the true power in R4 with the (wrong) sum of contribution powers, and prints the cross term.

## Use It

- **Bias plus signal.** Every transistor amplifier (Phase 12) has a DC bias from the power supply and a tiny AC signal from a microphone or sensor. Engineers analyse the DC bias with the signal off, then the signal with the DC supply off ("AC ground"), and add. That habit is superposition.
- **Audio mixers and summing amplifiers.** A mixer adds several input voltages, each through its own resistor, into one node. The output is the weighted sum of the inputs, the transfer coefficients set by the resistor values. You will build one with an op-amp in Phase 13.
- **Error budgets.** A precision voltage reference's datasheet (for example the REF5025 or LM4040) lists separate error sources: initial accuracy, temperature drift, load regulation. Each one moves the output a little; the designer estimates each contribution separately and combines them.
- **Digital-to-analog converters.** An R-2R ladder DAC (Phase 17) produces an output that is the sum of each bit's contribution, weighted by powers of two. Superposition is the reason it works.

## Try It in the Lab

The lab board has a 6 V battery feeding node b through a 2 kΩ resistor, and a 1 mA current source pushing into b from ground. The resistor from b to ground is missing. Pick it so that node b lands between 3.8 V and 4.2 V.

Use superposition before you press RUN:

- With the current source off (open), what is vb as a function of the slot resistance `Rs`? (A divider.)
- With the battery off (wire), what does the current source see from b to ground? What vb does that give?
- Add the two. Which of the offered parts gives a total near 4 V?

## Common Mistakes

- **Removing a voltage source instead of shorting it.** A dead battery is a wire, not a gap. Leaving a gap breaks every path through it.
- **Shorting a current source instead of opening it.** A dead current source is a gap. A wire across it would carry current that was never there.
- **Turning off dependent sources.** Dependent sources (Lesson 08) are not inputs; they must stay in place.
- **Adding powers.** Power is quadratic. Superpose voltages and currents first, then compute power.
- **Dropping signs.** A contribution can be negative (current flowing against your arrow). The sum is only right if you keep every sign.
- **Using superposition on non-linear circuits.** With a diode or a lamp in the circuit, contributions do not add. (Small-signal tricks come later.)

## Exercises

1. Using the transfer coefficients, find vb and vc when V1 = 6 V and I1 = 2 mA. Check with the code. (Answer to check: vb ≈ 3.71 V.)
2. What value of I1 (and in which direction) would make vc exactly 0 V while V1 stays at 12 V? Use the coefficients for vc.
3. A circuit has a 10 V battery in series with 1 kΩ feeding node x, a 5 V battery in series with 1 kΩ feeding node x, and a 1 kΩ resistor from x to ground. Find vx by superposition (two dividers) and then by nodal analysis. (Answer: 5 V.)
4. In the workhorse, compute the power in R2 correctly and with the wrong "sum of powers" method. How big is the error, in percent?
5. Harder: add a second current source of 0.5 mA pushing from ground into node b of the workhorse. Use superposition with three sources (the two you already solved plus the new one) to predict vb and vc, then check with `sim`.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Superposition | "One source at a time" | In a linear circuit, each voltage and current is the sum of the contributions of each independent source acting alone |
| Turning off a voltage source | "Short it" | Setting it to 0 V, which is the same as a wire |
| Turning off a current source | "Open it" | Setting it to 0 A, which is the same as a gap |
| Linear | "Proportional" | Built only from addition and multiplication by fixed numbers, so scaled and summed solutions stay valid |
| Transfer coefficient | "The gain from that source" | Volts (or amps) at a point per volt (or amp) of one source, set only by the resistors |
| Cross term | "Why power doesn't add" | The `2ab` in `(a + b)²`, which the sum of separate powers leaves out |

## Further Reading

- [All About Circuits, Vol. I, "Superposition Theorem"](https://www.allaboutcircuits.com/textbook/direct-current/chpt-10/superposition-theorem/): a free chapter with worked examples and the same warning about power.
- [MIT OpenCourseWare 6.002 Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/): the lecture on linearity, superposition, Thevenin and Norton.
- *The Art of Electronics*, Horowitz and Hill, 3rd edition, Chapter 1: Thevenin's theorem and superposition used as everyday design tools.
- *Feynman Lectures on Physics*, Vol. II, Chapter 22 "AC Circuits" (free at [feynmanlectures.caltech.edu](https://www.feynmanlectures.caltech.edu/II_22.html)): why linear equations make circuit effects add.
