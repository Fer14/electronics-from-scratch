# Ohm's Law

> Voltage equals current times resistance. Know any two and the third is one multiplication or division away.

**Type:** Build
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Lessons 01 (What Resistance Is) and 02 (Resistivity and Wires); Phase 02 (Your First Circuits), Lesson 07 (Measuring with a Multimeter)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Ohm's law | The rule that the voltage across a resistor equals the current through it times its resistance | "Price = quantity × unit price" for electricity |
| Proportional | Two quantities that grow together: double one, the other doubles | Buying twice as many apples costs twice as much |
| Linear | A relation that draws a straight line on a graph | A ramp with a constant slope |
| I-V curve | A graph of current (I) against voltage (V) for a part | A fingerprint of how the part behaves |
| Slope | How steep a line is: how much it goes up for each step to the right | The steepness of a hill road |
| Ohmic | A part that obeys Ohm's law (straight-line I-V curve through zero) | A well-behaved spring |
| Voltage across | The voltage measured between the two ends of a part | The height difference between the top and bottom of a slide |
| Current through | The current flowing in one end and out of the other | The number of people going through a door per second |
| Current-limiting resistor | A resistor placed on purpose to keep the current at a safe value | A narrow gate that stops a crowd from rushing |
| Best-fit line | The straight line that passes closest to a set of measured points | Drawing the "average" line through slightly scattered dots |

## Learning Objectives

- Derive Ohm's law (V = I × R) from the drift and collision picture of Lesson 01
- Use all three forms of Ohm's law (V = I R, I = V / R, R = V / I) with correct units and prefixes
- Read an I-V graph and get the resistance from the slope of the line
- Estimate resistance from a set of noisy measurements with a best-fit line
- Choose a resistor value to get a target current from a given voltage
- Recognise the "Ohm's law triangle" as a memory aid, and know when the law applies

## The Problem

You have a 9 V battery and a sensor that should get about 9 mA. You also have a box of resistors. Which one do you use? Or: you measure 3.3 V across a resistor marked 2.2 kΩ; how much current is flowing? Or: a motor draws 2 A through a cable with 0.05 Ω of resistance; how many volts are lost in the cable?

All three questions are answered by a single relation that connects voltage, current and resistance. It is the most used equation in electronics. Every other lesson in this course, from LEDs to transistors to op-amps, uses it, usually several times per circuit. If you only remember one formula from this course, make it this one.

In Lesson 01 you defined resistance as R = V / I. That is a *definition*: any object, at any moment, has some ratio V / I. Ohm's law says something much stronger: **for many materials, that ratio is a constant**. It does not change when you change the voltage. That fact is what makes resistance useful.

## The Physics

### From drift to Ohm's law, step by step

Let us take a uniform piece of material: a wire of length *L* (meters) and cross-sectional area *A* (square meters). We connect a voltage *V* across its ends. Here is the chain of cause and effect, using only ideas from Lessons 01 and 02 and from Phase 01.

**1. The voltage creates a field.** The voltage is spread evenly along the wire. The electric field E (Phase 01, Lesson 05) is the voltage per meter:

```
E = V / L          (volts per meter)
```

For example, 0.08 V across 1 m of wire gives a field of 0.08 V/m.

**2. The field pushes each electron.** The force on a charge in a field is charge times field: F = e × E. A force on a particle of mass m gives it an acceleration a = F / m = e E / m.

**3. Collisions cap the speed.** Between collisions, which happen on average every τ seconds, the electron gains extra speed equal to acceleration × time. Averaged over the whole crowd, the drift speed is:

```
v_drift = (e × E / m) × τ
```

Read it as: "the drift speed is how fast the field accelerates an electron, times how long it gets to accelerate before it bumps into something".

**4. The drift makes a current.** From Lesson 01, current is the number of free electrons per cubic meter, times the charge of each, times the area, times the drift speed:

```
I = n × e × A × v_drift
```

**5. Put it all together.** Substitute steps 1 to 3 into step 4:

```
I = n × e × A × (e × τ / m) × (V / L)

I = [ n × e² × τ × A / (m × L) ] × V
```

Look at what is inside the square brackets: n, e, τ, m are properties of the material; A and L are the shape. **None of them depends on V.** So the current is a fixed number times the voltage. Current is proportional to voltage. The fixed number is the conductance G = 1/R. Flip it over:

```
R = m × L / (n × e² × τ × A)
```

And since Lesson 01 told us the conductivity is σ = n e² τ / m and resistivity ρ = 1/σ, this is exactly R = ρ L / A from Lesson 02. Everything fits together.

So:

```
I = V / R       or equivalently       V = I × R
```

That is **Ohm's law**. Georg Ohm found it experimentally in 1827 by measuring wires of different lengths with a very crude current meter. The explanation in terms of electrons came about seventy years later (the electron was only discovered in 1897).

### Checking it with numbers

1 m of copper wire with an area of 0.1 mm² (= 0.1 × 10⁻⁶ m²):

```
R = ρ L / A = 1.68e-8 × 1 / 1e-7 = 0.168 Ω
```

Apply 0.04 V (40 mV):

```
I = V / R = 0.04 / 0.167 = 0.24 A = 240 mA
```

Apply twice that, 80 mV: 480 mA. Twice the voltage, twice the current, and V / I is 0.167 Ω both times. The script prints exactly this table, computing the current from the drift picture (steps 1 to 4) and *not* from Ohm's law, so you can see the law appear.

### When it holds and when it does not

The derivation used one hidden assumption: **the mean free time τ does not depend on the voltage.** That is true when:

- the drift is tiny compared with the random thermal speed (always true in ordinary wires);
- the temperature stays the same (if the current heats the wire, τ shrinks and R grows; Lesson 02 showed that);
- the number of free carriers n stays the same (true for metals; very false for diodes and transistors, where the voltage itself changes how many carriers are available).

Materials and parts that obey the law are called **ohmic**. Resistors, wires and heating elements at a steady temperature are ohmic. Diodes, LEDs, lamps (filament heats up), transistors and the human body are not. Lesson 07 (When Ohm's Law Fails) explores these.

## The Concept

### The three forms

Ohm's law has three faces, all the same equation rearranged. Learn to read each one as a sentence.

> **Voltage equals current times resistance.** "How many volts does this current need to get through this resistance?"

```
V = I × R
```

> **Current equals voltage divided by resistance.** "How much current will this voltage push through this resistance?"

```
I = V / R
```

> **Resistance equals voltage divided by current.** "What resistance makes this voltage give this current?"

```
R = V / I
```

Symbols and units:

| Symbol | Quantity | Unit | Unit symbol |
|---|---|---|---|
| V | voltage across the part | volt | V |
| I | current through the part | ampere | A |
| R | resistance of the part | ohm | Ω |

Rule of thumb: **always convert to volts, amps and ohms before calculating**, then put the prefix back at the end. Or use a consistent set: volts, milliamps and kilohms also work together (1 V / 1 kΩ = 1 mA), which is very handy in electronics.

### A memory aid: the triangle

```
         /\
        /  \
       / V  \
      /------\
     / I | R  \
    /____|_____\
```

Cover the quantity you want with your finger. What is left tells you how to compute it: cover V and you see I next to R (multiply); cover I and you see V over R (divide); cover R and you see V over I (divide). It is just a reminder; understanding the sentences is better.

### Worked examples

**Example 1: find the current.** A 1 kΩ resistor is across a 9 V battery.

```
I = V / R = 9 V / 1000 Ω = 0.009 A = 9 mA
```

With the volts-milliamps-kilohms trick: 9 V / 1 kΩ = 9 mA directly.

**Example 2: find the current.** A 220 Ω resistor on a 5 V supply.

```
I = 5 / 220 = 0.02273 A = 22.7 mA
```

**Example 3: find the voltage.** 20 mA flows through a 330 Ω resistor. What voltage is across it?

```
V = I × R = 0.020 A × 330 Ω = 6.6 V
```

**Example 4: find the voltage lost in a wire.** A motor draws 2 A through a cable with 0.05 Ω of resistance (Lesson 02 showed how to compute that).

```
V = 2 × 0.05 = 0.10 V
```

The motor gets 0.1 V less than the battery provides.

**Example 5: find the resistance.** A car's 12 V heated seat draws 0.5 A.

```
R = V / I = 12 / 0.5 = 24 Ω
```

**Example 6: find the resistance.** 3.3 V across an unknown part drives 1.5 mA.

```
R = 3.3 / 0.0015 = 2200 Ω = 2.2 kΩ
```

Using the trick: 3.3 V / 1.5 mA = 2.2 kΩ.

**Example 7: design.** You want 9 mA from a 9 V battery through a single resistor (this is the lab task). R = 9 V / 9 mA = 1 kΩ. You want 2.5 mA from 12 V: R = 12 / 2.5 = 4.8 kΩ. That value does not exist in shops; Lesson 04 shows you would use 4.7 kΩ, giving 12 / 4.7 = 2.55 mA, close enough.

### The I-V graph

The best way to see Ohm's law is a graph with voltage on the horizontal axis and current on the vertical axis. For a resistor, the points lie on a **straight line through zero**:

```
   I (mA)
   20 |                      / 500 Ω
      |                    /
      |                  /         _ 1 kΩ
   10 |                /      __--
      |              /   __--          ___ 2 kΩ
      |            / __--      ____----
      |         /__-   ___-----
      |      /_--___---
    0 +---------------------------------- V (volts)
      0                 5                10
```

- **Straight** means linear: each extra volt adds the same current.
- **Through zero** means: no voltage, no current. A resistor does not make current by itself.
- **The slope** (how steep the line is) is current per volt, which is the conductance 1/R. A **steeper line means a smaller resistance**. A flat line (no current at any voltage) is an open circuit: infinite resistance. A vertical line (any current at zero voltage) is a short circuit: zero resistance.

Some books draw the axes the other way round (current horizontal, voltage vertical). Then the slope is R itself. Always check the axis labels.

### From measurements to a resistance

Real measurements are never exactly on the line. Your multimeter has a last digit that jumps around, the supply wobbles, and the resistor warms slightly. Suppose you set a bench supply to 0, 1, 2, ..., 10 V and read the current each time. You get something like:

| V (V) | I (mA) | V / I (Ω) |
|---|---|---|
| 1.0 | 0.949 | 1054 |
| 2.0 | 2.008 | 996 |
| 5.0 | 4.996 | 1001 |
| 9.0 | 9.066 | 993 |
| 10.0 | 10.005 | 1000 |

Dividing each pair gives slightly different answers, and the small-voltage ones are the worst (a tiny error in a tiny current is a big relative error). A better method: draw the **best-fit straight line** through all the points and take its slope. NumPy's `polyfit` does exactly this. It finds the line V = R × I + b that passes as close as possible to every point. The slope R comes out at about 998 Ω, much closer to the true 1000 Ω than most single readings, and the intercept b is about 0.01 V, almost zero, as Ohm's law demands.

## Build It

Run:

```
uv run python phases/03-resistance-and-ohms-law/03-ohms-law/code/main.py
```

### Step 1: Ohm's law appears from the drift picture

```python
def current_from_drift(volts, length_m, area_m2, electrons_per_m3, mean_free_time):
    field = volts / length_m
    drift = ELECTRON_CHARGE * field * mean_free_time / ELECTRON_MASS
    return electrons_per_m3 * ELECTRON_CHARGE * area_m2 * drift
```

Each line is one step of the physics: field from voltage, drift speed from field and collisions, current from drift. No resistance appears anywhere. Yet the printed V / I ratio is 0.1670 Ω for every voltage, and it matches the formula R = m L / (n e² τ A).

### Step 2: Fitting a bench measurement

```python
def fit_resistance(volts, amps):
    slope, intercept = np.polyfit(amps, volts, 1)
    return slope, intercept
```

The script fakes a bench session: a true 1 kΩ resistor, voltages from 0 to 10 V, and a little random noise (with a fixed seed, so you always get the same numbers) on each current reading. It prints the table and the best-fit slope, about 998 Ω.

### Step 3: Drawing the I-V lines

`ascii_iv_plot` draws the lines for 500 Ω, 1 kΩ and 2 kΩ in the terminal, with letters a, b, c. The 500 Ω line is the steepest: it reaches 20 mA at 10 V. The 2 kΩ line only reaches 5 mA.

### Step 4: The three forms

```python
def current(volts, ohms):
    return volts / ohms


def voltage(amps, ohms):
    return amps * ohms


def resistance(volts, amps):
    return volts / amps
```

Three one-line functions, and the six worked examples above. Compare each printed answer with your own calculator result.

### Step 5: Designing for a target current

The last step solves R = V / I for three design cases: 9 V at 9 mA (1000 Ω), 5 V at 10 mA (500 Ω), 12 V at 2.5 mA (4800 Ω). Two of these values are not ones you can buy. Lesson 04 shows which values exist and how to pick the nearest one.

## Use It

- **LED resistors.** Every LED on every gadget has a resistor next to it chosen with Ohm's law (Phase 11, Lesson 07, adds the LED's own voltage).
- **Reading datasheets.** A sensor datasheet that says "input resistance 10 kΩ" tells you that with 5 V applied it draws 5 V / 10 kΩ = 0.5 mA.
- **Measuring current without an ammeter.** Many circuits have a "shunt" resistor: a small, precise resistor (say 0.1 Ω) in the current path. Measure the voltage across it, divide by 0.1 Ω, and you have the current. Power supplies, battery monitors and motor drivers all do this.
- **Checking a fuse or wire.** If your multimeter reads 0.3 Ω for a cable, Ohm's law tells you a 5 A load will lose 1.5 V in it.
- **Electric safety.** Dry hand-to-hand skin resistance is roughly 100 kΩ. At 9 V that is 0.09 mA, harmless. At 230 V with wet hands (maybe 1 kΩ), I = 230 / 1000 = 230 mA: deadly. The same law explains both.
- **Multimeters measure resistance using Ohm's law**: they push a small known current through the part and measure the voltage (Phase 06, Lesson 04).

## Try It in the Lab

The lab task "Nine milliamps from nine volts" gives you a 9 V battery, an empty resistor slot and a box with six resistors. The goal is a current between 8 mA and 10 mA. Before trying anything, write down which resistance range satisfies the goal: what resistance gives exactly 8 mA, and what gives exactly 10 mA? Then pick from the box. Also try one of the wrong resistors on purpose and check that the current the lab shows matches what Ohm's law predicts.

## Common Mistakes

- **Forgetting unit conversions.** 9 V / 9 mA is not 1 Ω. Convert 9 mA to 0.009 A first (or use the V-mA-kΩ shortcut consistently).
- **Using the total voltage for one part.** Ohm's law relates the voltage *across that part* to the current *through that part*. In a circuit with several parts, each one has its own share of the voltage (Phase 04).
- **Believing a resistor "makes" current or voltage.** It does neither. It relates them. Without a source, there is no current.
- **Applying it to non-ohmic parts.** An LED is not a resistor. V / I for an LED changes enormously with current. You can still compute V / I at one moment, but you cannot use it to predict another point.
- **Mixing up slope directions.** On an I-vs-V plot, steep means small R. On a V-vs-I plot, steep means big R.
- **Trusting one measurement.** Repeat it, or fit several points. One noisy reading at low voltage can be several percent off.

## Exercises

1. A 4.7 kΩ resistor has 9 V across it. What current flows, in mA?
2. A 100 Ω resistor carries 35 mA. What is the voltage across it?
3. A toaster draws 4.2 A from 230 V mains. What is the resistance of its heating element (while hot)?
4. You measure 0, 2.0, 4.1, 5.9 and 8.0 mA at 0, 1, 2, 3 and 4 V. Estimate the resistance. Is the part ohmic? (Plot it or fit a line.)
5. (Harder) Using the drift picture, by what factor does the current change if you keep the voltage the same but replace a copper wire with one twice as long and twice the diameter? Check your answer with R = ρ L / A.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Ohm's law | "V equals I R" | For ohmic materials, current through a part is proportional to the voltage across it; the constant ratio V/I is the resistance |
| Ohmic | "A normal resistor" | A part whose I-V graph is a straight line through zero at a fixed temperature |
| I-V curve | "The characteristic" | Current plotted against voltage; its shape tells you how the part behaves |
| Slope of the I-V line | "How steep it is" | Current per volt, the conductance 1/R |
| Current-limiting resistor | "The resistor in front of the LED" | A resistor chosen with R = V / I to cap the current |
| Best-fit line | "Average line" | The straight line minimising the distance to measured points; its slope estimates R |
| Shunt | "Current sense resistor" | A small known resistor whose voltage tells you the current through it |

## Further Reading

- *The Art of Electronics*, 3rd edition (Horowitz & Hill), section 1.2.2: Ohm's law and the first circuits, in compact, practical form.
- *All About Circuits*, Volume I (DC), chapter "Ohm's Law": many short worked examples.
- Khan Academy, Electrical engineering, "Ohm's law" videos and practice problems.
- *Feynman Lectures on Physics*, Volume I, chapter 43 "Diffusion", sections on drift speed and ionic conductivity (the microscopic picture of currents in materials).
