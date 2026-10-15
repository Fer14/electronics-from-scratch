# The Wheatstone Bridge

> Two voltage dividers side by side, compared with each other: when they agree, the meter between them reads zero, and zero is the easiest thing in the world to measure precisely.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Phase 04 lessons 01-06, especially 05 (The Voltage Divider)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Bridge | A circuit with two voltage dividers fed from the same source, and a meter connecting their midpoints | A footbridge between two staircases, joining their landings |
| Arm | One of the four resistors of the bridge | One of the four flights of stairs |
| Midpoint | The node between the two resistors of one divider | The landing of one staircase |
| Bridge output | The voltage between the two midpoints | The difference in height between the two landings |
| Balanced | The two midpoints are at the same voltage, so the output is zero | Both landings at exactly the same height: the footbridge is level |
| Null measurement | Measuring by adjusting something until a reading becomes zero | Adding weights to a balance scale until the pointer sits in the middle |
| Unknown (Rx) | The resistor whose value you want to find | The object on one side of the scale |
| Sensitivity | How much the output changes for a given change in the unknown | How far the scale's pointer moves for one extra gram |
| Strain gauge | A thin metal foil resistor glued to a part; stretching the part changes its resistance slightly | A rubber band that gets longer and thinner when pulled |
| Strain | The relative stretch of a material: change in length divided by length. A microstrain is one millionth | Stretching a 1 m rod by 1 micrometre |
| Gauge factor | How strongly a strain gauge's resistance responds to strain (about 2 for metal foil) | The gearing between stretch and resistance change |
| RTD / Pt100 | A platinum resistor whose resistance rises with temperature; 100 Ohm at 0 C | A thermometer that reports in ohms |
| Galvanometer | A very sensitive current meter, traditionally used to detect bridge balance | A feather that moves with the slightest breeze |

## Learning Objectives

- Describe the Wheatstone bridge as two voltage dividers, and compute its output from the divider formula
- Derive the balance condition R1 x R4 = R2 x R3 (equivalently R1/R2 = R3/R4) and use it to find an unknown resistor
- Explain why the balance does not depend on the supply voltage, and why null measurements are so precise
- Compute the bridge output for small changes in one arm and estimate it with the quarter-bridge rule V x dR / 4R
- Recover an unknown resistance from an unbalanced reading, and solve a bridge with a real meter using KCL at the two midpoints

## The Problem

Suppose you want to measure a resistance very precisely, to 0.01 %. Or suppose you want to detect a tiny change in resistance: a strain gauge glued to a bridge girder changes from 350.000 Ohm to 350.070 Ohm when a truck drives over. That is a change of 0.02 %.

Put the strain gauge in a simple voltage divider with another 350 Ohm resistor on 5 V and the output moves from 2.50000 V to 2.50025 V. You need to see a change of 0.25 millivolts sitting on top of 2.5 volts. Any drift in the 5 V supply (and supplies drift by more than 0.01 %) swamps the signal completely. And your meter needs a 2.5 V range with a resolution of a fraction of a millivolt, which is expensive.

What if you had a second divider, identical, sitting next to the first, and you measured the **difference** between the two midpoints? The 2.5 V cancels. You read 0 V when nothing happens and 0.25 mV when the truck drives over, on the most sensitive range of your meter. And if the supply drifts, both midpoints drift together and the difference stays put.

That is the idea of the **Wheatstone bridge**, popularized by Charles Wheatstone in 1843 (it was invented a few years earlier by Samuel Hunter Christie). It is still everywhere: in kitchen scales, pressure sensors, gas detectors and the load cells in industrial weighing machines.

## The Physics

Nothing new happens physically. Everything is the voltage divider of lesson 05, twice.

The battery holds a fixed voltage between its top terminal and ground. Two separate paths go from top to bottom: the left arm (R1 then R2) and the right arm (R3 then R4). Current flows down each path independently. Along each path, the voltage falls in proportion to the resistances (KVL plus Ohm's law), so each midpoint sits at some height between 0 V and the supply.

If the two paths divide the voltage in the **same proportion**, the two midpoints sit at the same height. Connect a meter between them and there is no voltage to push current through it: the meter reads zero. If one arm changes, its midpoint moves up or down, the midpoints are no longer at the same height, and a voltage appears across the meter.

The **balance scale** is the right picture. You put the unknown object on one pan, add known weights to the other until the pointer is centered, and read the answer from the known weights. The scale doesn't need an accurate spring, only a pointer that tells you "left heavier" or "right heavier". The bridge does the same: the meter only has to tell "zero" or "not zero", and the answer comes from the known resistors. What the picture gets wrong: a scale compares two things; a bridge compares two *ratios*.

## The Concept

### The circuit

```
                 +Vin
                  |
          +-------+-------+
          |               |
        [R1]            [R3]
          |               |
   left   +----( V )------+   right
          |    meter      |
        [R2]            [R4]
          |               |
          +-------+-------+
                  |
                ground
```

R1 and R2 form the left divider, R3 and R4 the right one. The meter is connected between the two midpoints, "left" and "right". In this lesson the meter is an ideal voltmeter: it draws no current, so the two dividers don't disturb each other (Step 7 of the code drops that assumption).

### Step 1: each midpoint from the divider formula

```
V_left  = Vin x R2 / (R1 + R2)
V_right = Vin x R4 / (R3 + R4)
```

### Step 2: the output is the difference

```
V_out = V_left - V_right = Vin x ( R2 / (R1 + R2)  -  R4 / (R3 + R4) )
```

"The bridge output is the supply times the difference of the two divider fractions."

### Worked example 1

Vin = 9 V, R1 = 1 kOhm, R2 = 2 kOhm, R3 = 1.5 kOhm, R4 = 2.2 kOhm.

```
V_left  = 9 x 2000 / 3000 = 6.0000 V
V_right = 9 x 2200 / 3700 = 5.3514 V
V_out   = 6.0000 - 5.3514 = 0.6486 V = 648.6 mV
```

### Step 3: the balance condition

The bridge is balanced when V_out = 0, which means the two fractions are equal:

```
R2 / (R1 + R2) = R4 / (R3 + R4)
```

Cross-multiply (multiply both sides by both denominators):

```
R2 x (R3 + R4) = R4 x (R1 + R2)
R2 x R3 + R2 x R4 = R4 x R1 + R4 x R2
```

The term R2 x R4 appears on both sides and cancels, leaving

```
R2 x R3 = R1 x R4        or, dividing,        R1 / R2 = R3 / R4
```

Read aloud: **"the bridge is balanced when the top-to-bottom ratio is the same on both sides"**, or equivalently **"when the products of opposite arms are equal"** (R1 and R4 are diagonally opposite, so are R2 and R3).

Two important consequences:

1. **Vin has disappeared.** Balance depends only on the resistors. A balanced bridge stays balanced if the battery is weak, fresh, or noisy. The code checks this by halving and doubling the supply.
2. **The unknown follows from three known resistors.** If R4 is unknown and you adjust R3 until the meter reads zero, then R4 = R2 x R3 / R1.

### Worked example 2: balancing

With R1 = 1 kOhm, R2 = 2 kOhm, R3 = 1.5 kOhm, what R4 balances the bridge?

```
R4 = R2 x R3 / R1 = 2000 x 1500 / 1000 = 3000 Ohm
check: V_left = 9 x 2000/3000 = 6 V,  V_right = 9 x 3000/4500 = 6 V,  V_out = 0
```

In a classic laboratory bridge, R1 and R2 are a precise "ratio arm" (for example exactly 10:1 or 1:1), R3 is a precise adjustable resistor (a decade box with knobs), and R4 is the unknown. You turn the knobs until the galvanometer shows no current and read R4 from the knobs. The accuracy is as good as the known resistors, not the meter.

### Near balance: how the output moves

Take a bridge where three arms are 1 kOhm and the fourth (R4) is near 1 kOhm, on 5 V. The code sweeps R4:

```
R4 (Ohm)    output (mV)
 900        +131.58
 950         +64.10
 990         +12.56
1000           0.00
1010         -12.44
1050         -60.98
1100        -119.05
```

The output changes sign as R4 crosses the balance value: positive means "R4 too small", negative means "R4 too big". Near balance the curve is almost a straight line: each extra 10 Ohm moves the output by about 12.5 mV. Further away it bends (900 gives +131.6, not +125).

### The quarter-bridge rule

When all four arms equal R and one of them changes by a small amount dR (dR much smaller than R), the output is close to

```
|V_out|  ~  Vin x dR / (4 x R)
```

"The output is about the supply times the fractional change, divided by four." Where does the 4 come from? Each midpoint sits at Vin/2. Changing R4 to R + dR moves the right midpoint to Vin x (R + dR)/(2R + dR). For small dR that is about Vin/2 + Vin x dR/(4R). The left midpoint doesn't move, so the difference is Vin x dR/(4R). (The sign depends on which arm changes; with R4 growing, the right midpoint rises, and V_left - V_right is negative.)

Check: 5 V, R = 1000, dR = 10: 5 x 10 / 4000 = 12.5 mV. The exact value is 12.44 mV.

### Worked example 3: the strain gauge

A metal-foil strain gauge has R = 350 Ohm and a gauge factor of 2. The gauge factor says: relative change of resistance = gauge factor x strain.

```
dR / R = GF x strain
```

At 500 microstrain (the part stretched by 500 millionths of its length, a typical working load for steel):

```
dR = 350 x 2 x 500e-6 = 0.35 Ohm
V_out ~ 5 V x 0.35 / (4 x 350) = 1.25 mV
```

The exact calculation in the code gives 1.2494 mV. The single-divider alternative reads 2.50125 V: the same 1.25 mV change, buried under 2.5 V. With the bridge, you can amplify the output by 1000 (Phase 13) and get a clean 1.25 V signal; amplify the single divider's output by 1000 and you'd ask for 2500 V.

### Worked example 4: a Pt100 thermometer

A Pt100 is a platinum resistor with 100 Ohm at 0 C, rising by about 0.385 % per degree:

```
R(T) = 100 x (1 + 0.00385 x T)        T in degrees C
```

At 25 C: 100 x (1 + 0.09625) = 109.625 Ohm. Put it as R4 in a bridge with R1 = R3 = 1 kOhm and R2 = 100 Ohm on 3.3 V. At 0 C, R1 x R4 = 1000 x 100 = R2 x R3 = 100 x 1000: balanced. At 25 C:

```
V_left  = 3.3 x 100 / 1100     = 0.30000 V
V_right = 3.3 x 109.625 / 1109.625 = 0.32602 V
V_out   = -26.0 mV
```

The bridge reads zero at 0 C and gives about -1 mV per degree, a signal that starts at zero instead of riding on a large offset.

### Finding the unknown without balancing

You don't always have to adjust anything. If you know R1, R2, R3 and Vin, a reading of V_out gives the unknown directly. Work backwards:

```
V_left  = Vin x R2 / (R1 + R2)               (known)
V_right = V_left - V_out                      (from the reading)
R4      = R3 x V_right / (Vin - V_right)      (divider formula solved for R4)
```

The last line comes from V_right = Vin x R4/(R3 + R4): multiply out, collect R4, and divide. Example with three 1 kOhm arms on 5 V and a reading of -261.86 mV: V_left = 2.5 V, V_right = 2.76186 V, R4 = 1000 x 2.76186 / 2.23814 = 1234.0 Ohm.

This is how most modern sensor bridges work: they are not balanced by hand; an amplifier and an analog-to-digital converter read the small output, and software converts it back to resistance, strain or temperature. The catch: now the result *does* depend on Vin, so designers measure Vin too and take the ratio (a "ratiometric" measurement).

### What about a real meter between the midpoints?

So far the meter drew no current. A real galvanometer has some resistance Rm, and when the bridge is unbalanced a small current flows through it from one midpoint to the other. Then the two dividers are no longer independent and the simple formulas are not exact.

You can still solve it with what you know. Write KCL at each midpoint (current in from the top resistor equals current out through the bottom resistor plus current out through the meter):

```
left:   (Vin - V_left)/R1  = V_left/R2  + (V_left - V_right)/Rm
right:  (Vin - V_right)/R3 = V_right/R4 + (V_right - V_left)/Rm
```

Two equations, two unknown voltages. Rearranged with conductances (G = 1/R, lesson 06) they become a small 2x2 system that NumPy solves in one line. The results (5 V, three 1 kOhm arms, R4 = 1050 Ohm):

```
meter resistance   V_left    V_right   meter current
1 GOhm (ideal)     2.5000 V  2.5610 V    ~0     uA
10 kOhm            2.5028 V  2.5581 V   -5.5    uA
100 Ohm            2.5274 V  2.5329 V  -54.8    uA
```

A low-resistance meter pulls the two midpoints toward each other. But at balance the two midpoints are at the same voltage, so no current flows through the meter **whatever its resistance**, and the balance condition stays exactly R1 x R4 = R2 x R3. That's another reason null measurements are so robust. Phase 05 turns this "KCL at every node" method into a general technique (nodal analysis).

## Build It

Run the script:

```
uv run python phases/04-kirchhoffs-laws/07-the-wheatstone-bridge/code/main.py
```

### Step 1: Two dividers

```python
def bridge_output(v_in, r1, r2, r3, r4):
    v_left = divider_output(v_in, r1, r2)
    v_right = divider_output(v_in, r3, r4)
    return v_left, v_right, v_left - v_right
```

That's the whole bridge, reusing the divider function from lesson 05. Worked example 1 prints 6.0000 V, 5.3514 V and 648.65 mV.

### Step 2: Balance

```python
def balancing_r4(r1, r2, r3):
    return r2 * r3 / r1
```

The script computes R4 = 3000 Ohm, shows both midpoints at 6.0000 V, then repeats on 4.5 V and 18 V to show the output stays at zero.

### Step 3: Sweep

Three 1 kOhm arms on 5 V and R4 from 900 to 1100 Ohm, printing the table above with its sign change at balance.

### Step 4: Unknown from a reading

```python
def unknown_from_reading(v_in, r1, r2, r3, v_measured):
    v_left = divider_output(v_in, r1, r2)
    v_right = v_left - v_measured
    return r3 * v_right / (v_in - v_right)
```

The script simulates a meter reading (rounded to 0.01 mV, like a real display) for 1234 Ohm and 870 Ohm and recovers both values.

### Step 5: Strain gauge

A 350 Ohm gauge with gauge factor 2 at 100, 500 and 1000 microstrain. For each, the exact bridge output, the quarter-bridge estimate and the single-divider reading are printed side by side.

### Step 6: Pt100

The bridge balanced at 0 C, read at 0, 25, 50 and 100 C: about -1 mV per degree, bending slightly at higher temperatures.

### Step 7: Real meter

```python
def bridge_with_meter(v_in, r1, r2, r3, r4, r_meter):
    g1, g2, g3, g4, gm = 1 / r1, 1 / r2, 1 / r3, 1 / r4, 1 / r_meter
    conductance_matrix = np.array([[g1 + g2 + gm, -gm], [-gm, g3 + g4 + gm]])
    injected = np.array([v_in * g1, v_in * g3])
    v_left, v_right = np.linalg.solve(conductance_matrix, injected)
    return v_left, v_right, (v_left - v_right) / r_meter
```

Each row is one KCL equation from above, moved around so the unknown voltages are on the left. For example, the left equation (Vin - V_left) G1 = V_left G2 + (V_left - V_right) Gm becomes (G1 + G2 + Gm) V_left - Gm V_right = Vin G1. `np.linalg.solve` finds the two voltages that satisfy both rows at once. The last line checks that a balanced bridge sends zero current through even a low-resistance 100 Ohm meter.

## Use It

- **Load cells and scales:** a kitchen scale's load cell is an aluminium bar with four strain gauges forming a full bridge (all four arms change, two up and two down, giving four times the quarter-bridge output). Typical datasheets quote "1 mV/V" or "2 mV/V" at full load: with a 5 V supply, a 2 mV/V cell gives 10 mV at its rated weight. A dedicated chip such as the HX711 amplifies and digitizes that output.
- **Pressure sensors:** many silicon pressure sensors (the MPX series, for instance) contain a bridge of resistors built into a thin silicon membrane.
- **Temperature:** RTDs (Pt100, Pt1000) and thermistors are often read in bridges, especially when the interesting range is near a reference temperature.
- **Gas sensors:** the old "pellistor" combustible-gas detectors compare a heated catalytic bead with an identical inactive bead in a bridge; the gas burns on one bead, heats it, and unbalances the bridge.
- **Classic instruments:** laboratory Wheatstone bridges with decade dials were the standard way to measure resistance precisely for over a century, and the same balance idea, extended to AC, measures capacitors and inductors (Phase 09).

## Try It in the Lab

Open the lab task **"Balance the bridge"**. A 9 V battery feeds a bridge. The top-left arm is 10 kOhm, the top-right arm is 1 kOhm, the lower-left arm is a sensor that currently reads 3.3 kOhm, and the lower-right arm is an empty slot. The goal: the voltage between the two midpoints must be within 10 mV of zero.

Before you try parts at random, write down the balance condition and decide which arms are "opposite". Then ask: some wrong choices put the right midpoint above the left one, others below. Can you predict the sign of the output for each part in the tray before you press RUN?

## Common Mistakes

- **Pairing the wrong arms.** The condition is R1/R2 = R3/R4 with R1, R3 on top and R2, R4 on the bottom (or products of *diagonally opposite* arms equal). Writing R1/R2 = R4/R3 balances nothing. Always label top and bottom first.
- **Thinking the supply must be precise at balance.** At balance the supply voltage drops out entirely. It only matters when you read an unbalanced output (Step 4).
- **Expecting a straight line far from balance.** The quarter-bridge rule V x dR/4R is only good for small changes. At 10 % off balance it is already off by several percent.
- **Measuring each midpoint against ground with a coarse meter.** The point of a bridge is the *difference*. Measuring 2.50125 V and 2.50000 V separately and subtracting needs a far better meter than measuring 1.25 mV directly.
- **Forgetting the meter can load the bridge.** Away from balance, a low-resistance meter changes the readings (Step 7). Use a high-resistance meter, or work at balance.
- **Ignoring self-heating.** The current through a sensor heats it a little (Phase 03, lesson 05), changing its resistance. Strain-gauge and RTD bridges run on a few volts for this reason.

## Exercises

1. Vin = 12 V, R1 = 4.7 kOhm, R2 = 2.2 kOhm, R3 = 10 kOhm, R4 = 4.7 kOhm. Compute both midpoint voltages and the bridge output. Is it balanced?
2. In a bridge with R1 = 1 kOhm and R2 = 100 Ohm (a 10:1 ratio arm), the bridge balances when the adjustable R3 is set to 4720 Ohm. What is the unknown R4?
3. Three arms are 120 Ohm and the fourth is a strain gauge of 120 Ohm with gauge factor 2.1, on a 10 V supply. Use the quarter-bridge rule to estimate the output at 800 microstrain, then compute it exactly with the divider formulas.
4. A bridge with three 1 kOhm arms on 5 V gives a reading of +40.00 mV (left minus right). Find R4. Is it bigger or smaller than 1 kOhm, and why does the sign tell you that?
5. (Harder) Using the Pt100 bridge of worked example 4, find the temperature at which the output is -75 mV. Then explain why the output in Step 6 is not exactly proportional to temperature even though the Pt100 itself is linear.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Wheatstone bridge | "A bridge circuit" | Two voltage dividers on one supply with the output taken between their midpoints |
| Balance | "The bridge reads zero" | Both dividers have the same ratio, R1/R2 = R3/R4 (equivalently R1 x R4 = R2 x R3), so the midpoints are at equal voltage |
| Null measurement | "Adjust until zero" | Find an unknown by adjusting a known quantity until a detector reads zero; accuracy comes from the known parts, not the detector |
| Quarter bridge | "One active arm" | A bridge where only one arm changes; output about Vin x dR/(4R) for small changes |
| Full bridge | "Four gauges" | All four arms change (two up, two down), giving about four times the quarter-bridge output |
| Gauge factor | "Sensitivity of the gauge" | Relative change in resistance divided by strain, about 2 for metal foil gauges |
| Ratiometric | "Measured against the supply" | A reading expressed as a fraction of the supply voltage, so supply drift cancels |

## Further Reading

- *The Art of Electronics* (Horowitz & Hill), chapter 1 (the bridge as a pair of dividers) and the chapter on precision circuits and instrumentation amplifiers, for how bridge outputs are amplified.
- All About Circuits, *Lessons in Electric Circuits*, Volume I (DC), chapter "DC Metering Circuits", section on bridge circuits.
- *Practical Electronics for Inventors* (Scherz & Monk), the sections on Wheatstone bridges and sensors.
- A load cell datasheet (any "mV/V" rated cell) and the HX711 datasheet, to see a real bridge sensor and the converter built to read it.
