# Capacitors in Series and Parallel

> Side by side, capacitors add like extra plate area. One after another, they combine like extra gap, the same way resistors in parallel do.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 04 Lesson 04 (Series and Parallel Resistors), Phase 07 Lessons 02-04 (Capacitance, Charging and Discharging, The Time Constant)
**Time:** ~50 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Parallel | Parts connected across the same two nodes, so they share the same voltage | Several buckets standing side by side, all filled to the same height |
| Series | Parts connected one after another in a single path, so they carry the same current | Train carriages coupled in a line |
| Equivalent capacitance | The single capacitor that would behave exactly like a group | Replacing several small tanks with one big tank of the same total behaviour |
| Reciprocal | One divided by a number: the reciprocal of 4 is 1/4 = 0.25 | Turning "litres per minute" into "minutes per litre" |
| Capacitive divider | Two capacitors in series that split a voltage between them | Two springs in a row sharing a push |
| Floating node | A node connected only to capacitors, with no resistive path to anything else | An island with only drawbridges, no fixed road |
| Balancing resistor | A large resistor across each series capacitor so they share voltage evenly in the long run | A handrail that keeps people evenly spaced on a staircase |

## Learning Objectives

- Derive the parallel rule C = C1 + C2 from Q = C x V and Kirchhoff's current law.
- Derive the series rule 1/C = 1/C1 + 1/C2 from Q = C x V and Kirchhoff's voltage law.
- Compare the rules with those for resistors and explain why they are "swapped".
- Compute how two series capacitors split a voltage, and why the smaller capacitor gets the larger share.
- Measure an equivalent capacitance with the simulator by timing an RC charge.

## The Problem

Your timing circuit needs 3.2 uF. The shop sells 1, 2.2, 4.7 and 10 uF (standard E6 values), not 3.2 uF. Or you need a capacitor rated for 500 V, and the only ones in the drawer are rated 250 V. Or a circuit board has three 100 nF capacitors on one power rail, and you want to know what the rail "sees" in total.

All of these are answered by combining capacitors. The rules are short, but they are the opposite of the resistor rules you learned in Phase 04, which trips up almost everybody at first. If you derive them yourself from Q = C x V, you will never mix them up.

## The Physics

### Parallel: more plate area

Two capacitors connected across the same two nodes have the same voltage V (they are connected to the same two points, so by definition they see the same voltage difference). Each stores its own charge:

    Q1 = C1 x V        Q2 = C2 x V

The total charge the source had to deliver is the sum (Kirchhoff's current law: every coulomb that left the source landed on one or the other):

    Q = Q1 + Q2 = (C1 + C2) x V

So the pair behaves exactly like one capacitor of

> Capacitors in parallel add.

    C = C1 + C2 + C3 + ...

Physically, placing two capacitors side by side is like joining their plates into larger plates with the same gap. Larger area, more capacitance (Lesson 02).

```
        top o-----+-------+
                  |       |
                 === C1  === C2        same V across both
                  |       |
        gnd o-----+-------+
```

### Series: more gap

Now connect two capacitors one after another: C1 from `top` to `mid`, C2 from `mid` to ground.

```
        top o
            |
           === C1
            |
        mid o           <- only touches capacitors: a floating node
            |
           === C2
            |
        gnd o
```

Follow the charge. The source pulls Q off the bottom plate of C2 (through ground) and pushes Q onto the top plate of C1. The middle node, between C1's lower plate and C2's upper plate, is an isolated island of metal: nothing can flow onto it or off it from outside. It started neutral, so it must stay neutral. If C1's lower plate has gained -Q (attracted by the +Q above it), then C2's upper plate, the other half of the same island, must have +Q. So **every capacitor in a series chain carries the same charge Q**.

Each capacitor's voltage is then its charge over its capacitance, and by Kirchhoff's voltage law they add:

    V = V1 + V2 = Q / C1 + Q / C2 = Q x (1/C1 + 1/C2)

The chain behaves like a single capacitor with Q / V = C, where

> For capacitors in series, the reciprocal of the total is the sum of the reciprocals.

    1/C = 1/C1 + 1/C2 + ...

and for exactly two, the "product over sum" shortcut:

    C = (C1 x C2) / (C1 + C2)

Physically, stacking two capacitors is like making one capacitor with a gap equal to both gaps together. More gap, less capacitance. The total is always **smaller than the smallest** one in the chain.

### Why it is the other way round from resistors

| | Resistors | Capacitors |
|---|---|---|
| Series | add: R = R1 + R2 | reciprocals add: 1/C = 1/C1 + 1/C2 |
| Parallel | reciprocals add: 1/R = 1/R1 + 1/R2 | add: C = C1 + C2 |

The reason: a resistor's value measures how much it **opposes** current (volts per amp), while capacitance measures how much charge it **accepts** (coulombs per volt). Two paths side by side oppose less (resistors) but accept more (capacitors). In Phase 09 you will see that a capacitor's opposition to AC current is proportional to 1/C, which makes both tables follow one single rule.

## The Concept

### Worked example 1: making 3.2 uF

1 uF and 2.2 uF in parallel: C = 1 + 2.2 = 3.2 uF. Done.

Or 4.7 uF and 10 uF in series: C = (4.7 x 10) / (4.7 + 10) = 47 / 14.7 = 3.197 uF. Also about 3.2 uF.

### Worked example 2: three in series

Three 3.3 uF in series: 1/C = 3 x (1 / 3.3) = 0.909, so C = 1.1 uF. For n identical capacitors in series, C = C1 / n.

### Worked example 3: a mixed network

Two 1 uF in parallel (= 2 uF), all in series with a 2 uF:

    C = (2 x 2) / (2 + 2) = 1 uF

Work from the inside out, exactly as you did with resistor networks in Phase 04.

### How series capacitors share voltage

Both carry the same Q. Then V1 = Q / C1 and V2 = Q / C2, so the **smaller** capacitor gets the **larger** voltage. Using C = C1 C2 / (C1 + C2) and Q = C x V:

    V1 = V x C2 / (C1 + C2)        V2 = V x C1 / (C1 + C2)

> The voltage on each series capacitor is the total voltage times the **other** capacitor's value, over the sum.

Compare with the resistor divider from Phase 04 (V1 = V x R1 / (R1 + R2)): again the roles are swapped.

Example: 1 uF on top of 2 uF, across 9 V.

1. C = (1 x 2) / (1 + 2) = 0.667 uF.
2. Q = 0.667 uF x 9 V = 6 uC on each.
3. V1 = 6 uC / 1 uF = 6 V. V2 = 6 uC / 2 uF = 3 V. Sum 9 V.

### Series for voltage rating

Two identical 250 V capacitors in series can, ideally, take 500 V: each gets half. But real capacitors are never exactly equal and they leak (Lesson 07). Over seconds to minutes, the leakage currents, not the capacitances, decide the sharing, and one capacitor can end up with far more than half. So designers put a **balancing resistor** (for example 100 kOhm) across each one. The resistors carry much more current than the leakage and force an even split. You see this in banks of supercapacitors and in high-voltage power supplies.

### Measuring an equivalent capacitance

From Lesson 04: charging from 0 V through R, the capacitor crosses half the supply at t = 0.693 x R x C. So we can measure any combination: time the half-way crossing, divide by 0.693 x R. That is how the code checks the formulas against the simulator.

### Worked example 4: designing for voltage

You need about 50 uF that can take 400 V, but your capacitors are 100 uF / 250 V.

1. Two in series: voltage rating 2 x 250 = 500 V (with balancing resistors), capacitance 100 / 2 = 50 uF.
2. Check the share with a 20% mismatch (80 uF and 120 uF): the 80 uF gets 400 x 120 / 200 = 240 V and the 120 uF gets 160 V. 240 V is below 250 V, but the margin is thin. Designers would prefer three in series (750 V rating, 33 uF) and parallel pairs, or a single part with a proper rating.
3. Energy check (Lesson 06): the pair stores 1/2 x 50 uF x 400^2 = 4 J, exactly the same as the two capacitors would hold separately at 200 V each (2 x 1/2 x 100 uF x 200^2 = 4 J). Combining capacitors never creates energy; it only changes the voltage and capacitance it appears at.

### Stray capacitance in series

A small stray capacitance in **series** with a big capacitor dominates the combination: 1 pF in series with 1 uF is (1 x 10^-12 x 10^-6) / (10^-6 + 10^-12), essentially 1 pF. This explains why a capacitor connected through a gap, or through a poor contact that acts like a tiny capacitor, behaves as if it were almost not there. In parallel the opposite holds: 1 pF beside 1 uF changes nothing you can measure. Whenever you combine very different values, the series result is close to the **smaller** one and the parallel result close to the **larger** one.

### Charge sharing: joining two charged capacitors

What happens if you connect a charged capacitor to an empty one, in parallel? Take a 1 uF at 10 V (Q = 10 uC) and an empty 1 uF.

1. Once connected, they are in parallel and must end at the same voltage.
2. No charge can be created or destroyed, so the total is still 10 uC, now spread over 2 uF.
3. Final voltage: V = Q / C = 10 uC / 2 uF = 5 V on both.

Charge is conserved, but look at the energy (Lesson 06): before, 1/2 x 1 uF x 10^2 = 50 uJ; after, 1/2 x 2 uF x 5^2 = 25 uJ. Half the energy disappeared, as heat in the wires and a tiny spark, however low the wire resistance. This "charge sharing" happens inside chips whenever a charged node is connected to an uncharged one, and it is the same loss you will meet in Lesson 06.

### Worked example 5: a ladder of three

A 6 uF in series with the parallel pair (2 uF and 1 uF), across 12 V.

1. The parallel pair: 2 + 1 = 3 uF.
2. In series with 6 uF: C = (6 x 3) / (6 + 3) = 18 / 9 = 2 uF.
3. Total charge: Q = 2 uF x 12 V = 24 uC. The same 24 uC sits on the 6 uF and on the pair as a whole.
4. Voltages: 24 uC / 6 uF = 4 V on the 6 uF; 24 uC / 3 uF = 8 V on the pair. 4 + 8 = 12 V.
5. Inside the pair, both see 8 V: the 2 uF holds 16 uC and the 1 uF holds 8 uC, which add back up to 24 uC.

## Build It

```bash
uv run python phases/07-capacitors/05-capacitors-in-series-and-parallel/code/main.py
```

### Step 1: The rules

```python
def parallel(*capacitors):
    return sum(capacitors)


def series(*capacitors):
    return 1.0 / sum(1.0 / c for c in capacitors)
```

```
Combining capacitors (all values in uF)
  1 + 2.2 in parallel          = 3.200
  4.7 and 10 in series         = 3.197
  two 10 in series             = 5.000
  three 1 in parallel          = 3.000
  (1 || 1) in series with 2    = 1.000
```

(The symbol `||` is shorthand for "in parallel with".)

### Step 2: Two circuits for the simulator

```python
def rc_with_parallel_pair(c1, c2):
    circuit = Circuit()
    circuit.voltage_source("V1", "in", "0", SUPPLY_VOLTS)
    circuit.resistor("R1", "in", "top", RESISTOR_OHMS)
    circuit.capacitor("C1", "top", "0", c1, v0=0.0)
    circuit.capacitor("C2", "top", "0", c2, v0=0.0)
    return circuit


def rc_with_series_pair(c1, c2):
    circuit = Circuit()
    circuit.voltage_source("V1", "in", "0", SUPPLY_VOLTS)
    circuit.resistor("R1", "in", "top", RESISTOR_OHMS)
    circuit.capacitor("C1", "top", "mid", c1, v0=0.0)
    circuit.capacitor("C2", "mid", "0", c2, v0=0.0)
    return circuit
```

The series version has the floating node `mid`. Our simulator handles it because the transient starts from the capacitors' initial voltages (`v0`), which pin down `mid` at t = 0; after that the capacitor equations fix how its voltage moves.

### Step 3: Measure by timing

```python
def measured_capacitance(circuit):
    result = circuit.transient(t_stop=20e-3, dt=2e-6)
    time = np.asarray(result.time)
    volts = np.asarray(result.v("top"))
    half_time = first_crossing(time, volts, SUPPLY_VOLTS / 2)
    return half_time / math.log(2) / RESISTOR_OHMS
```

```
Measuring the combination with the simulator: time to reach half the supply = 0.693 * R * C
  1 uF || 2.2 uF : measured 3.200 uF, formula 3.200 uF
  4.7 uF + 10 uF in series: measured 3.197 uF, formula 3.197 uF
```

### Step 4: The series voltage split

```
1 uF on top of 2 uF in series, charged from 9 V
  across the 1 uF: 6.000 V (formula 9 * 2 / 3 = 6.000 V)
  across the 2 uF: 3.000 V (formula 9 * 1 / 3 = 3.000 V)
  charge on each: 6.000 uC and 6.000 uC
```

Equal charges, unequal voltages, with the smaller capacitor taking the bigger share.

## Use It

- **Decoupling banks.** A processor board may have dozens of 100 nF and 1 uF ceramics on the same rail. They are in parallel, so their capacitance adds; and spreading them out also places charge close to every power pin.
- **Supercapacitor modules.** Single supercapacitor cells are rated about 2.7 V. A "16 V" module stacks six in series (6 x 2.7 = 16.2 V) and its capacitance is one sixth of a cell's. These modules include balancing circuits.
- **Capacitive voltage dividers.** High-voltage probes and mains-powered capacitive dropper circuits use series capacitors to split a voltage; oscilloscope probes combine a resistive and a capacitive divider (Phase 06).
- **Trimming values.** A designer who needs 3.3 nF in a filter but has 2.2 nF and 1 nF on the bill of materials puts them in parallel rather than adding a new part number.
- **Hidden series capacitance.** A ceramic capacitor in a tiny package has internal stacks of layers in parallel (that is how MLCCs reach microfarads), and a capacitor connected through a long ground path can effectively be in series with stray capacitance. Knowing the rules helps you spot both.

## Try It in the Lab

The lab "Build the missing capacitor" has two capacitor pads in parallel, a 1 kOhm resistor and a 5 V supply. You need the half-way crossing between 2.0 and 2.45 ms. Convert that window to a window of total capacitance, then look for two values in the box that add up to land inside it. Ask yourself why the series version of the same problem would need a different pair.

## Common Mistakes

- **Using the resistor rules.** Parallel capacitors add; series capacitors combine by reciprocals. Derive it from Q = C x V if in doubt.
- **Expecting series capacitors to share voltage equally.** Only identical capacitors do (and only until leakage takes over). Otherwise the smaller one takes more voltage and may exceed its rating.
- **Forgetting the rating in parallel.** Paralleling a 6.3 V and a 25 V capacitor gives a 6.3 V combination: they share the same voltage.
- **Expecting more capacitance from series.** A series chain is always smaller than its smallest member. Series is used for voltage rating, not capacitance.
- **Analysing a floating node with `dc()`.** In a DC operating point, capacitors are open circuits, so a node touched only by capacitors has nothing defining its voltage, and the equations become unsolvable. Real circuits need balancing resistors for the same physical reason.

## Exercises

1. What is the equivalent of 470 nF, 220 nF and 100 nF in parallel? In series?
2. You have only 10 uF capacitors. How do you make 5 uF? 15 uF? 6.67 uF?
3. A 2.2 uF and a 4.7 uF are in series across 12 V. Find the voltage on each and the charge on each.
4. Two "identical" 100 uF, 250 V capacitors are in series across 450 V. Because of tolerance, one is actually 80 uF and the other 120 uF. What voltage does each get at first? Is either over its rating?
5. Modify the code to measure three 1 uF capacitors in series by timing the RC charge. Before running, predict the half-way time with R = 1 kOhm.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Parallel capacitors | "Just add them" | Same voltage on each, charges add, so C = C1 + C2 |
| Series capacitors | "Product over sum" | Same charge on each, voltages add, so 1/C = 1/C1 + 1/C2 |
| Equivalent capacitance | "The total" | The one capacitor that stores the same charge for the same applied voltage |
| Capacitive divider | "Caps split the voltage" | Series capacitors divide voltage inversely to their capacitance |
| Balancing resistor | "Bleeder across each cap" | A resistor that forces series capacitors to share DC voltage evenly despite unequal leakage |
| Floating node | "A node with nothing on it" | A node with no DC path to ground; its voltage is set only by stored charge |

## Further Reading

- [All About Circuits, Vol. I, Chapter 13: Series and Parallel Capacitors](https://www.allaboutcircuits.com/textbook/direct-current/chpt-13/series-and-parallel-capacitors/) - the rules with clear diagrams.
- [HyperPhysics: Capacitors in series and parallel](http://hyperphysics.phy-astr.gsu.edu/hbase/electric/capac.html) - compact derivations and calculators.
- *Practical Electronics for Inventors*, 4th ed., Scherz & Monk, section on capacitors in series and parallel and capacitive dividers.
- [Maxwell Technologies / Eaton supercapacitor module application notes on cell balancing](https://www.eaton.com/us/en-us/products/electronic-components/supercapacitors.html) - why series cells need balancing.
