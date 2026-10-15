# Kirchhoff's Voltage Law

> Walk any closed path in a circuit and add up every rise and every drop: you always get exactly zero, because you are back at the height you started from.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 01 (The Physics Underneath), especially Lesson 04 (Energy, Potential and Voltage); Phase 03 (Resistance and Ohm's Law), especially Lesson 03 (Ohm's Law); Phase 04 Lessons 01 (Nodes, Branches and Loops) and 02 (Kirchhoff's Current Law)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Kirchhoff's voltage law (KVL) | Around any closed loop, the voltage rises add up to exactly the voltage drops | Walking around a hilly park and returning to your car: total uphill equals total downhill |
| Potential (electric potential) | The voltage of a point measured from ground; energy per coulomb a charge has there | The height of a spot above sea level |
| Voltage rise | Going from a lower-potential point to a higher one (for example, from a battery's minus to its plus) | Climbing stairs |
| Voltage drop | Going from a higher-potential point to a lower one (for example, through a resistor in the direction the current flows) | Walking down a slope |
| Conservative | A quantity where only the start and end matter, not the path in between | Your height change on a hike depends only on where you start and stop, not on the trail |
| Series resistor | A resistor placed in the same single path as something else, so the same current flows through both | A narrow section of pipe before a tap |
| Polarity | Which end of an element is at the higher voltage, often marked + and - | Which end of a ramp is up |
| Loop walk | The method of going around a loop element by element, writing down each rise and drop with its sign | Counting steps up and down as you circle a building |

## Learning Objectives

- State Kirchhoff's voltage law in words and as an equation, and explain why it follows from voltage being energy per charge.
- Walk a loop, writing each element's voltage with the correct sign, in either direction.
- Use KVL to find a missing voltage in a loop.
- Combine KVL with Ohm's law to choose a series resistor that gives a part a target voltage.
- Explain why describing a circuit with node voltages makes KVL automatic.

## The Problem

A 9 V battery powers a small sensor that only wants 3 V. Connect it straight across the battery and the sensor gets 9 V and may be damaged. A standard fix is to put a resistor in series, in the same path as the sensor, so that the resistor "uses up" the extra 6 V. But how big should the resistor be? And how do you know the 9 V will really split as 6 + 3, and not some other way?

Kirchhoff's voltage law answers this. It says the voltages around any closed loop must add up to zero, so the battery's 9 V must be shared exactly among everything else in the loop. With Kirchhoff's current law from Lesson 02 and Ohm's law from Phase 03, you will then have the complete toolkit to solve any resistor circuit, which is precisely what Phase 05 automates.

## The Physics

Go back to Phase 01, Lesson 04. **Voltage** between two points is the energy that one coulomb of charge gains or loses when it moves from one to the other. One volt (V) means one joule (J) of energy per coulomb (C). As a sentence: energy equals charge times voltage.

```
E = Q × V        E in joules, Q in coulombs, V in volts
```

Pick the ground node and give every other point a **potential**: the energy per coulomb a charge would have there, measured from ground. This is exactly like height above sea level. A charge at a point with potential 7.2 V has 7.2 J per coulomb more energy than at ground, just as a ball at 7.2 m has more energy than at sea level.

Now follow one coulomb around a simple loop: a 12 V battery with two resistors, R1 and R2, after it.

```
              R1 (4.8 V)
    vcc ─────[////]───── a
     |                   |
    [+]                  [/]
  B1 12 V                [/] R2 (7.2 V)
    [-]                  [/]
     |                   |
    gnd ─────────────────┘
```

- Inside the battery, chemistry pushes the coulomb from the minus terminal (0 V) up to the plus terminal (12 V). It gains 12 J. That is a **rise**.
- Through R1 it bumps into atoms and gives up 4.8 J as heat. Its potential falls by 4.8 V. That is a **drop**.
- Through R2 it gives up 7.2 J and falls by 7.2 V. Another drop.
- It is back at gnd, at 0 V, exactly where it started.

Gain 12 J, lose 4.8 + 7.2 = 12 J. Net change: zero. It cannot be anything else, because the coulomb is back at the same point, and a point has only one potential. If you walked a hilly park and came back to your car, your total climbing equals your total descending, regardless of the route. Physicists say the electric potential is **conservative**: only the start and end points matter.

What the height analogy gets right: potential is a "level" that every point has, and differences of level are what matter. What it gets wrong: in a hill, the ball rolls down by itself and never climbs on its own. In a circuit, a battery is an "escalator" that lifts charge up, using chemical energy. Also, the escalator analogy suggests charges are lifted one at a time and fall freely; really, all charges in the loop move together, slowly, like a bicycle chain (Phase 02, Lesson 05).

One more honest caveat: KVL holds in every circuit in this course up to Phase 08. When magnetic fields change quickly through a loop (transformers, Phase 08), a voltage can appear "around" the loop without any element causing it. Engineers handle that by drawing it as an element (an inductor or a transformer winding) so KVL keeps working.

## The Concept

### The law in words and symbols

In words: **around any closed loop, the sum of the voltage rises equals the sum of the voltage drops.**

Or, counting rises as positive and drops as negative: **the signed sum of the voltages around any loop is zero.**

```
sum of voltage changes around a closed loop = 0
```

Read it aloud: "walk around a loop, add up every change in potential with its sign, and the total is zero."

### How to walk a loop

1. Pick a starting node and a direction (clockwise or anticlockwise, it does not matter).
2. Step across each element in turn. Write the change in potential: **+** if you go up (from - to + of a battery, or against the current in a resistor), **-** if you go down (from + to - of a battery, or with the current through a resistor).
3. When you are back at the start, set the total equal to zero.

Why "with the current through a resistor is a drop"? Because current in a resistor flows from higher to lower potential, like water flowing downhill. Ohm's law gives the size of the drop: the voltage across a resistor equals the current through it times its resistance, V = I × R.

### Worked example: the ladder

Here is the circuit used in the code. It has two windows (meshes), as in Lesson 01.

```
   vcc ──[ R1 1 kΩ ]── a ──[ R3 1 kΩ ]── b
    |                  |                 |
  [B1 12 V]         [R2 3 kΩ]        [R4 2 kΩ]
    |                  |                 |
   gnd ─────────────── gnd ───────────── gnd
```

The node voltages turn out to be v(vcc) = 12 V, v(a) = 7.2 V, v(b) = 4.8 V (you will be able to find these yourself after Lesson 04, and Phase 05 does it systematically). So each element's voltage is a difference of node voltages:

```
B1: 12 - 0   = 12.0 V      R1: 12 - 7.2 = 4.8 V
R2: 7.2 - 0  = 7.2 V       R3: 7.2 - 4.8 = 2.4 V
R4: 4.8 - 0  = 4.8 V
```

**Left window**, starting at gnd and going clockwise (up through B1, right through R1, down through R2):

```
+12.0 (up through B1)  - 4.8 (down through R1)  - 7.2 (down through R2)  = 0   ✓
```

**Right window**, starting at a: right through R3, down through R4, back up through R2:

```
- 2.4 (R3)  - 4.8 (R4)  + 7.2 (up through R2, against its current)  = 0   ✓
```

**Outer loop**, starting at gnd: B1, R1, R3, R4.

```
+12.0 - 4.8 - 2.4 - 4.8 = 0   ✓
```

And notice: the outer loop's equation is just the left window plus the right window. The R2 terms (-7.2 and +7.2) cancel. This is the redundancy you saw in Lesson 01: L = B - N + 1 = 5 - 4 + 1 = 2 independent loop equations.

**Direction does not matter.** Walk the right window the other way, starting at a: down R2 (-7.2), up R4 (+4.8), back left through R3 (+2.4). Total: 0. Every term just flips sign.

### Consequence 1: parallel elements share one voltage

Look at R2 and the R3-R4 chain. Both go from node a to gnd. The right-window KVL said 7.2 = 2.4 + 4.8: the voltage across R2 equals the total voltage across R3 and R4. In general, **anything connected between the same two nodes has the same voltage across it**. You used this intuitively in Phase 02 (Lesson 04); KVL is the reason.

### Consequence 2: finding a missing voltage

A 9 V battery drives a lamp, a resistor and a small motor, all in one loop. A meter says the lamp drops 3.2 V and the resistor 4.1 V. Without measuring the motor:

```
9.0 = 3.2 + 4.1 + V_motor   →   V_motor = 9.0 - 7.3 = 1.7 V
```

### Consequence 3: catching a wrong reading

A student measures the right window with a voltmeter: R3 reads 2.4 V, R4 reads 5.3 V, R2 reads 7.2 V. Walk the loop: -2.4 - 5.3 + 7.2 = **-0.5 V**. Not zero. So at least one reading is wrong (R4 is really 4.8 V; perhaps the meter was on the wrong range). KVL is a free sanity check every time you measure.

### Why node voltages make KVL automatic

Here is a subtle and very useful point. If you describe a circuit by giving each node a voltage, then each element's voltage is "v(end) minus v(start)". Walk any loop and add them:

```
(v(b) - v(a)) + (v(gnd) - v(b)) + (v(a) - v(gnd)) = 0
```

Every node voltage appears once with + and once with -, so they cancel, *whatever the numbers are*. Even made-up nonsense voltages pass KVL. The code demonstrates this with v(vcc) = 3, v(a) = -1.7, v(b) = 8.25: the loop still sums to zero.

So when you use node voltages, KVL is "built in", and the job of finding the *right* node voltages falls to KCL plus Ohm's law. That is exactly how Lesson 02 found v(a) = 5.4 V, and it is the idea behind nodal analysis in Phase 05. The other way round also works: if you choose loop currents instead, KCL becomes automatic and KVL does the work (mesh analysis, also Phase 05).

### Choosing a series resistor

Back to the sensor from The Problem. Treat the sensor as a 1 kΩ resistor that should get 3 V from a 9 V battery.

```
   vcc ──[ R_series ? ]── a
    |                     |
  [B1 9 V]           [sensor 1 kΩ]
    |                     |
   gnd ───────────────────┘
```

Step 1, KVL around the loop: 9 V = V(R_series) + V(sensor). We want V(sensor) = 3 V, so the series resistor must drop 9 - 3 = **6 V**.

Step 2, Ohm's law on the sensor: the current through it is 3 V / 1000 Ω = **3 mA** (0.003 A).

Step 3, this is a single loop, so (by KCL at node a) the same 3 mA flows through R_series. Ohm's law on it: R = 6 V / 0.003 A = **2000 Ω**.

Step 4, real resistors come in standard values (Phase 03, Lesson 04). The E12 series near 2000 Ω has 1.8 kΩ and 2.2 kΩ. With each, the current is 9 V divided by the total resistance:

```
1.8 kΩ: I = 9 / 2800 = 3.21 mA → sensor 3.21 V, resistor 5.79 V   (sum 9.00 V)
2.2 kΩ: I = 9 / 3200 = 2.81 mA → sensor 2.81 V, resistor 6.19 V   (sum 9.00 V)
```

Notice in every row the two voltages add to exactly 9 V. KVL, every time. Whether 3.21 V or 2.81 V is better depends on what the sensor tolerates (check its datasheet's "maximum supply voltage").

Notice the general pattern: in a series loop, the voltage splits *in proportion to resistance*. The 2 kΩ resistor gets twice the voltage of the 1 kΩ sensor because it has twice the resistance and the same current. Lesson 05 (The Voltage Divider) turns this into a formula.

## Build It

Run the program:

```
uv run python phases/04-kirchhoffs-laws/03-kirchhoffs-voltage-law/code/main.py
```

### Step 1: Describe the circuit

```python
node_voltages = {"gnd": 0.0, "vcc": 12.0, "a": 7.2, "b": 4.8}
branches = {
    "B1": ("battery", "vcc", "gnd", None),
    "R1": ("resistor", "vcc", "a", 1000.0),
    "R2": ("resistor", "a", "gnd", 3000.0),
    "R3": ("resistor", "a", "b", 1000.0),
    "R4": ("resistor", "b", "gnd", 2000.0),
}
```

Part 1 of the output follows one coulomb: +12 J from the battery, -4.8 J in R1, -7.2 J in R2, 0 J left.

Part 2 prints each element's voltage and the current from Ohm's law. Notice R3 and R4 carry the same 2.40 mA (they are in series), and R2 also carries 2.40 mA, while R1 carries 4.80 mA = 2.40 + 2.40 (KCL at a).

### Step 2: Walk a loop

```python
def walk_loop(start, steps, voltages):
    position = start
    total_change = 0.0
    lines = []
    for name in steps:
        kind, end_a, end_b, ohms = branches[name]
        next_position = end_b if position == end_a else end_a
        change = voltages[next_position] - voltages[position]
        total_change += change
        ...
        position = next_position
    return position, total_change, lines
```

For each element, we step from the node we are on to the element's other end, and the change is "potential where we arrive minus potential where we were". Positive is a rise, negative a drop. The program walks the left window, the right window, the outer loop, and the right window backwards. All four end with `total change = +0.000 V`.

### Step 3: Catch a bad reading, and see why node voltages always pass

```python
readings = {"R3": 2.4, "R4": 5.3, "R2": 7.2}
loop_sum = -readings["R3"] - readings["R4"] + readings["R2"]
```

The result, -0.5 V, flags the bad reading. Then the program feeds `walk_loop` some random node voltages and shows the sum is still zero, which is the cancellation explained in The Concept.

### Step 4: The missing drop

```python
missing = battery - sum(known_drops.values())
```

9.0 - 3.2 - 4.1 = 1.7 V for the motor.

### Step 5: Choose the series resistor

```python
needed_drop = battery - target_load_volts
current = target_load_volts / load_ohms
ideal_series = needed_drop / current
```

The program prints 2000 Ω, then tries every nearby E12 value, printing the load voltage, the series voltage, and their sum (always 9.00 V).

## Use It

- **LED resistors.** The most common calculation in hobby electronics: an LED keeps roughly 2 V across itself (red) and wants about 10 mA. From 5 V, KVL says the resistor drops 5 - 2 = 3 V, so R = 3 V / 0.010 A = 300 Ω; people pick 330 Ω. You will do this properly with the LED's real behaviour in Phase 11.
- **Battery packs.** Four AA cells in series give 4 × 1.5 = 6 V: walking through the pack, each cell is a rise of 1.5 V. Put one in backwards and the walk gives 1.5 + 1.5 + 1.5 - 1.5 = 3 V. KVL explains why a single reversed cell ruins the pack.
- **Voltage drop in long cables.** A 12 V supply feeding LED strips through 10 m of thin cable: if the cable has 0.5 Ω out and 0.5 Ω back and carries 2 A, each wire drops 1 V, so KVL leaves only 12 - 1 - 1 = 10 V for the strip. That is why the far end of a long LED strip looks dimmer.
- **Debugging with a voltmeter.** Measuring every element in a loop and checking the sum is a standard troubleshooting move. If a "closed switch" shows 9 V across it, KVL tells you the rest of the loop is getting nothing: the switch is actually open or broken.

## Try It in the Lab

Open the lab task for this lesson. A 9 V battery and a sensor that behaves like a 1 kΩ resistor are already on the board. Put one resistor in the slot between the battery's plus terminal and the sensor so that the sensor gets between 2.5 and 3.2 V, your resistor drops between 5.8 and 6.5 V, and your resistor dissipates less than 1/4 W.

Think about: how should the 9 V be shared? Since the same current flows through both parts, how does the ratio of their voltages relate to the ratio of their resistances? When you run it, check that the two measured voltages add to 9 V.

## Common Mistakes

- **Getting the sign of a resistor wrong.** A resistor is a drop only when you walk through it *in the direction of its current*. Walking against the current, it is a rise. If you do not yet know the current's direction, pick one, keep it consistent, and let the algebra give a negative number if needed.
- **Mixing two conventions in one equation.** Either write "rises = drops" or "signed sum = 0". Do not mix them halfway around a loop.
- **Forgetting an element.** Every element on the loop's path counts, including the battery and any wire you chose to model as a resistor.
- **Thinking a resistor "uses up" current.** It uses up voltage (energy per charge). The current is the same on both sides of a series resistor (KCL).
- **Expecting a series resistor to give the same voltage for any load.** The 2.2 kΩ resistor gives the sensor about 2.8 V only because the sensor is 1 kΩ. If the sensor draws more or less current, the split changes. That fragility is a big theme in Lesson 05 and in Phase 06.
- **Writing KVL for every loop you can see.** Only L = B - N + 1 of them are independent; the rest are sums of those.

## Exercises

1. A loop has a 12 V battery and three resistors. Two of them drop 2.5 V and 6.0 V. What does the third drop?
2. In the ladder of this lesson, walk the outer loop anticlockwise starting at node b. Write each term with its sign and check the sum.
3. A 5 V supply must give a 220 Ω load exactly 2 V. Using KVL and Ohm's law, find the series resistor. Then pick the nearest E12 value and compute the load voltage you actually get.
4. A 6 V pack is made of four 1.5 V cells, but one is inserted backwards. A 100 Ω resistor is connected across the pack. What voltage does the resistor get, and what current flows?
5. (Harder) Two batteries, 9 V and 3 V, are connected plus to plus through a 100 Ω resistor (their minus terminals are joined by a wire). Walk the loop to find the voltage across the resistor and the current. Which battery is being charged? Then flip the 3 V battery and repeat.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| KVL | "Voltages add up in series" | Around any closed loop the signed sum of voltages is zero, because potential is a level each point has |
| Voltage drop | "Voltage lost" | The decrease in potential going through an element; the energy per coulomb handed to that element |
| Voltage rise | "Where the voltage comes from" | An increase in potential, such as going from - to + through a battery |
| Potential | "Voltage at a point" | Energy per coulomb at a point, measured from the chosen ground |
| Series resistor | "A resistor that limits current" | A resistor in the same single path as a load; it takes its share of the voltage in proportion to its resistance |
| Conservative | "Energy is saved" | The change in potential between two points does not depend on the path taken |

## Further Reading

- *All About Circuits*, Volume I (DC), chapter "Divider Circuits and Kirchhoff's Laws", section on Kirchhoff's voltage law: practical loop-walking examples.
- Charles Platt, *Make: Electronics*, 3rd ed.: hands-on experiments measuring voltages around real loops with a multimeter.
- Khan Academy, Electrical Engineering, "Kirchhoff's voltage law": short visual explanation.
- Richard Feynman, *The Feynman Lectures on Physics*, Vol. II, chapters 4 and 22: why the electric field gives a potential at all, and how AC circuits stretch the idea.
