# The Boost Converter

> Charge an inductor from the input, then let go: its current has to keep flowing, and it climbs on top of the input voltage to do it. Rearrange the buck's parts and the output goes up: Vout = Vin / (1 - D).

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 18 (Power Electronics), Lessons 02-03 (Switching Converters, The Buck Converter); Phase 08 (Magnetism and Inductors), Lesson 04 (The Inductor)
**Time:** ~85 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Boost converter | A switching converter whose output is higher than its input. Also called a step-up converter. | A water ram (hydraulic ram pump): a flowing column of water, suddenly stopped, pushes some water uphill. |
| Gain (conversion ratio) | Vout / Vin. | How many times higher the water is lifted. |
| Low-side switch (boost) | The switch from the switch node to ground, which "charges" the inductor. | Opening the drain so the water column speeds up. |
| Rectifier switch / boost diode | The switch or diode from the switch node to the output, which lets the inductor's current into the output. | The one-way valve into the high tank. |
| Input current | In a boost, the inductor current is the input current; it is larger than the output current. | The big flow you need at the bottom to lift a small flow to the top. |
| Inductor resistance (DCR) | The resistance of the inductor's copper winding. | Friction in the pipe. |
| Maximum gain | The highest Vout / Vin a real boost can reach before losses win. | The tallest hill a real ram pump can lift to. |
| Right-half-plane zero | A control-theory name for the boost's habit of first moving the wrong way when D changes. Only mentioned here. | Pressing the accelerator and the car briefly slowing down first. |

## Learning Objectives

- Explain physically how a boost converter makes a voltage higher than its input
- Derive Vout = Vin / (1 - D) from volt-second balance, and the input current from energy conservation
- Compute the inductor ripple `Vin x D / (f x L)` and output ripple `I_out x D / (f x C)` and check them in the simulator
- Show, with the formula and the simulator, why inductor resistance limits the real gain to a few times the input
- Describe the boost's start-up behaviour and why it can never fully switch its output off

## The Problem

A single lithium battery gives 3.0-4.2 V. USB needs 5 V, a white LED string needs 9-30 V, an e-paper display needs 15 V, a phone's camera flash needs hundreds of volts. A linear regulator can only drop voltage; nothing in Lesson 01 can make 5 V out of 3.7 V. Neither can the buck.

The boost converter does it with the same four parts as the buck (two switches, an inductor and a capacitor), just arranged differently. It is in every power bank, every LED backlight driver, every hybrid car's battery-to-motor link. Its maths is a tidy variation of the buck's, but it has its own personality: big input currents, a ripple that hits the output capacitor hard, and limits that come from tiny resistances.

## The Physics

### Storing, then releasing

Put the inductor between the input and the switch node. Close the low-side switch: the inductor is connected straight across the input. Its current ramps up at `Vin / L`, storing energy `1/2 L I^2` in its magnetic field. The output capacitor, cut off from the input, feeds the load on its own.

Now open the low-side switch and close the high-side one. The inductor's current cannot stop (Lesson 02); it has to keep flowing, and the only path is into the output. The inductor now *adds* its own voltage to the input's to push current into a capacitor that is at a higher voltage. Its current ramps down, at `(Vout - Vin) / L`, and its stored energy goes into the output.

```
 on (S_low closed):                     off (S_high closed):

 Vin --[ L ]--+                          Vin --[ L ]--+----S_high----+-- Vout
       I up   |                                I down              |
            S_low                                                 === C, load
              |
             gnd
```

The everyday picture of a hydraulic ram pump is good: water flowing down a pipe is suddenly stopped by a valve; its momentum has to go somewhere, so it pushes a smaller amount of water up into a higher tank. What the picture gets wrong: a ram pump wastes most of its water; an ideal boost wastes nothing.

## The Concept

### The circuit

```
                L             S_high
   Vin ----+---[ L ]---+------o/ o------+-------+------ Vout
           |   I_L ->  | sw             |       |
          ===          |               === C   [ R_load ]
           |         S_low /            |       |
           |           |                |       |
   gnd ----+-----------+----------------+-------+
```

### Volt-second balance

**On (S_low closed, `D x T`):** inductor voltage = `Vin - 0 = Vin`.
**Off (S_high closed, `(1 - D) x T`):** inductor voltage = `Vin - Vout` (negative, since Vout > Vin).

Average must be zero (Lesson 03):

```
Vin x D x T + (Vin - Vout) x (1 - D) x T = 0
Vin x D + Vin - Vin x D - Vout x (1 - D) = 0
Vin = Vout x (1 - D)
Vout = Vin / (1 - D)
```

Read it as: "the output is the input divided by the fraction of time the low-side switch is open". At D = 0 (never charging) Vout = Vin. At D = 0.5, Vout = 2 Vin. As D approaches 1, the ideal formula goes to infinity.

To make 12 V from 5 V:

```
D = 1 - Vin / Vout = 1 - 5 / 12 = 7 / 12 = 0.5833
```

### Currents: the boost is a gearbox the other way

Energy conservation with ideal parts: `Vin x I_in = Vout x I_out`. For 12 V at 0.5 A (6 W) from 5 V:

```
I_in = 6 W / 5 V = 1.2 A
```

In a boost, the inductor is in the input path, so the inductor's average current *is* the input current: 1.2 A, more than twice the output current. The output only receives current during the off-time, so the average current through S_high equals I_out:

```
I_out = I_L x (1 - D)   ->   I_L = I_out / (1 - D) = 0.5 / 0.4167 = 1.2 A
```

This is why boosts need inductors and switches rated for much more current than the load takes, especially at high gain.

### Ripple

During the on-time, the inductor has Vin across it:

```
delta_I = Vin x D x T / L = Vin x D / (f x L)
```

With 5 V, D = 0.5833, 100 kHz and 100 uH:

```
delta_I = 5 x 0.5833 / (100 000 x 100e-6) = 2.917 / 10 = 0.292 A
```

The output capacitor has it harder than in a buck. During the whole on-time it alone supplies the load current, and nothing refills it:

```
delta_V = I_out x D x T / C = I_out x D / (f x C)
        = 0.5 x 0.5833 / (100 000 x 100e-6) = 0.2917 / 10 = 29.2 mV
```

Notice: no factor of 8, because the capacitor's current is a square wave (a full `-I_out` for D x T), not a gentle triangle. Boosts need more output capacitance than bucks for the same ripple.

### Why real boosts cannot reach huge gains

The inductor's winding has resistance `R_L` and carries the large input current `I_L = I_out / (1 - D)`. Its loss is `I_L^2 x R_L`, which grows like `1 / (1 - D)^2`. Working the volt-second balance with that resistance included gives:

```
Vout / Vin = 1 / (1 - D)  x  1 / (1 + R_L / (R_load x (1 - D)^2))
```

Read it as: "the ideal gain, reduced by a factor that gets worse as D approaches 1". With `R_L = 0.1 ohm` and a 24 ohm load:

| D | Ideal gain | With 0.1 ohm |
|---|------------|--------------|
| 0.50 | 2.0 | 1.97 |
| 0.75 | 4.0 | 3.75 |
| 0.90 | 10.0 | 7.06 |
| 0.95 | 20.0 | 7.50 |

Past some D, more duty *reduces* the output: the converter spends all its time charging the inductor and the losses eat everything. In practice single-stage boosts are used for gains up to about 5-10. Higher ratios use transformers or cascades.

### The boost cannot be turned off

When S_low never closes (D = 0), the path from input to output through the inductor and S_high (or the boost diode) is still there. The output sits at Vin, not 0 V. Power banks and USB boost circuits need an extra "load disconnect" switch to really turn off. The same path means that when power is first applied, the output capacitor immediately charges to about Vin through the inductor, and the inrush can be large.

### Start-up ringing

Like the buck, the boost's L and C resonate. Starting from the capacitor at Vin and jumping straight to D = 0.5833, the simulation shows the output overshooting to about 18 V and the inductor current peaking near 7.8 A, more than six times its steady value, and still ringing after 6 ms. Real boost controllers use soft start and current limiting. (Boosts are also harder to stabilise with feedback, because increasing D first *reduces* the output, since the off-time during which the output is fed gets shorter, before the extra inductor current arrives. Control engineers call it a right-half-plane zero.)

### Worked example: the power bank boost, by hand

Design a boost from one lithium cell (3.0 V empty, 3.7 V nominal, 4.2 V full) to 5 V at 1 A, switching at 1 MHz. Ignore losses for the first pass.

**Duty cycle range.** `D = 1 - Vin / Vout`:

```
Vin = 4.2 V:  D = 1 - 4.2 / 5 = 0.16
Vin = 3.7 V:  D = 1 - 3.7 / 5 = 0.26
Vin = 3.0 V:  D = 1 - 3.0 / 5 = 0.40
```

The controller's feedback loop will slide D from 0.16 to 0.40 as the cell empties.

**Input (inductor) current.** Output power is 5 W. The worst case is the lowest input:

```
I_in = 5 W / 3.0 V = 1.67 A        (with 90% efficiency: 5.56 W / 3.0 V = 1.85 A)
```

**Inductor.** Choose about 40% ripple at the worst case, `delta_I = 0.4 x 1.67 = 0.67 A`:

```
L = Vin x D / (f x delta_I) = 3.0 x 0.40 / (1 000 000 x 0.67) = 1.8 uH     -> use 2.2 uH
delta_I = 3.0 x 0.40 / (1e6 x 2.2e-6) = 0.545 A
peak current = 1.67 + 0.545 / 2 = 1.94 A
```

Pick an inductor whose saturation current is comfortably above 2 A (say 3 A), with low winding resistance, because the last section showed how much it matters.

**Output capacitor.** For 20 mV of ripple at the worst D:

```
C = I_out x D / (f x delta_V) = 1 x 0.40 / (1e6 x 0.02) = 20 uF      -> use 22 uF (or two 10 uF ceramics)
```

**Losses.** With 50 mohm of inductor resistance at 1.85 A: `1.85^2 x 0.05 = 0.17 W`. Two 40 mohm switches share the current over the cycle, adding about `1.85^2 x 0.04 = 0.14 W`. Switching losses and the controller add a few hundred milliwatts more, which is how real power banks end up near 90%.

### Worked example: why not just use D = 0.95?

Ideally, D = 0.95 gives 20 times the input. But the inductor carries `I_out / (1 - D) = 20 x I_out`. With the 0.1 ohm of the simulation and a 0.5 A load, that is 10 A through 0.1 ohm: 10 W of loss to deliver at most a few watts. The lossy gain formula gave 7.5 instead of 20. Ratios above about 5 call for a transformer-based converter.

## Build It

### Step 1: The circuit

```python
    circuit.voltage_source("VIN", "vin", "0", VIN)
    circuit.inductor("L1", coil_start, "sw", INDUCTANCE, i0=...)
    circuit.switch("SLOW", "sw", "0", closed=True, toggle_at=toggles)
    circuit.switch("SHIGH", "sw", "out", closed=False, toggle_at=toggles)
    circuit.capacitor("C1", "out", "0", CAPACITANCE, v0=...)
    circuit.resistor("RL", "out", "0", load_ohms)
```

The switch-timing helper is the one from Lesson 03, but here the low-side switch starts closed (it is the "on" switch of a boost).

### Step 2: Checking the gain and ripple

The script runs D = 0.25, 0.5, 0.5833 and 0.75 from near-steady-state initial conditions and prints the average output, the average inductor (input) current, the ripple current and the output ripple over one period.

### Step 3: Losses limit the gain

With a 0.1 ohm resistor in series with the inductor, it runs D = 0.5, 0.75 and 0.9 for 300 periods and compares the simulated gain with the lossy formula, and prints the efficiency. (D = 0.95 is only computed with the formula.)

### Step 4: Start-up

Finally it starts from the capacitor at Vin and the inductor at zero.

Run it:

```
uv run python phases/18-power-electronics/04-the-boost-converter/code/main.py
```

The ideal gains match `1 / (1 - D)` to a few millivolts; the input current at D = 0.5833 is 1.2 A; the ripples match `Vin D / (f L)` and `I_out D / (f C)`; with 0.1 ohm of winding resistance the gain at D = 0.9 is only about 7, with 67% efficiency. The start-up overshoots strongly.

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
Design: 5 V -> 12 V at 0.5 A (6 W), 100 kHz
  D = 1 - Vin / Vout = 0.5833; input current = Pout / Vin = 1.20 A
  ripple current Vin D / (f L) = 0.292 A, output ripple Iout D / (f C) = 29.2 mV

Ideal synchronous boost: simulation versus Vout = Vin / (1 - D)
       D  Vout sim  formula  I in sim  dI sim   dV sim
  0.2500   6.664 V  6.667 V   0.370 A 0.123 A    6.9 mV
  0.5000  10.000 V 10.000 V   0.828 A 0.246 A   20.5 mV
  0.5833  12.004 V 12.000 V   1.196 A 0.288 A   28.8 mV
  0.7500  19.996 V 20.000 V   3.342 A 0.371 A   62.0 mV

Power balance at D = 0.5833: in 5.980 W, out 6.004 W

With 0.1 ohm of inductor resistance the gain stops growing
      D ideal gain lossy formula lossy sim efficiency
   0.50       2.00         1.967     1.966      98.1%
   0.75       4.00         3.750     3.743      93.8%
   0.90      10.00         7.059     6.995      66.9%
   0.95      20.00         7.500         -          -

Switching on with the capacitor at Vin (as it is when power is applied): output peaks at 17.99 V, inductor current peaks at 7.80 A, after 6 ms Vout = 10.12 V
```

## Use It

- **Power banks** boost a 3.7 V lithium cell to 5 V (or 9-20 V for USB Power Delivery). At 5 V and 2 A out, the cell supplies around 3 A.
- **LED drivers** for backlights (for example the TPS61xxx family) boost to drive strings of LEDs in series, regulating current rather than voltage.
- **Single-cell gadgets** use tiny boosts to run a 3.3 V microcontroller from one 1.5 V AA cell (for example the TPS610xx series, which start up from below 1 V).
- **Electric vehicles and solar:** a boost stage raises battery or panel voltage to the hundreds of volts needed by the motor inverter or the grid-tie inverter. Solar charge controllers adjust D continuously to extract maximum power from the panel ("MPPT").
- **The flyback** converter (phone chargers) is a boost-like cousin with a transformer instead of a plain inductor, giving isolation and large voltage ratios.

## Common Mistakes

- **Underrating the inductor.** It carries the input current `I_out / (1 - D)` plus half the ripple, which can be several times the load current.
- **Too little output capacitance.** The capacitor alone feeds the load during D x T; the ripple formula has no factor of 8.
- **Expecting huge gains.** Winding and switch resistances cap real gains at a few times. Pushing D towards 1 lowers efficiency and can even lower the output.
- **Assuming the output is off when the controller is off.** It sits at Vin through the inductor and diode.
- **No diode or high-side switch.** With nowhere to go when S_low opens, the inductor's current produces the kick of Lesson 02 and destroys the switch.
- **Ignoring inrush.** At plug-in the output capacitor charges to Vin through the inductor; with a big capacitor this current spike can trip a USB port's protection.

## Exercises

1. A boost makes 9 V from a 3.6 V cell. What is D? With 0.3 A out, what is the input current (ideal)? (D = 0.6; I_in = 2.7 W / 3.6 V = 0.75 A.)
2. For that converter at 1 MHz with 4.7 uH, what is the ripple current? Peak inductor current? (3.6 x 0.6 / (1e6 x 4.7e-6) = 0.46 A; 0.75 + 0.23 = 0.98 A.)
3. How much output capacitance keeps the ripple under 20 mV? (C >= 0.3 x 0.6 / (1e6 x 0.02) = 9 uF, use 10 uF.)
4. Using the lossy formula with R_L = 0.05 ohm and a 30 ohm load, find the gain at D = 0.8 and D = 0.95. (5.0 / (1 + 0.05 / (30 x 0.04)) = 4.80; 20 / (1 + 0.05 / (30 x 0.0025)) = 12.0.)
5. Harder: modify `main.py` to replace the high-side switch by a diode (`circuit.diode("D1", "sw", "out")`). The circuit becomes nonlinear and slower to simulate, so use 50 periods. How much does the output drop, and why? (About one diode drop, because the inductor now needs Vout + 0.7 V at the switch node during the off-time.)

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Boost | "Step-up converter" | Inductor charged from the input, discharged into the output: Vout = Vin / (1 - D) |
| Input current | "What the battery gives" | Equal to the average inductor current, I_out / (1 - D) |
| Boost diode | "The output diode" | The freewheel path from the switch node to the output |
| Output ripple (boost) | "Ripple" | I_out x D / (f x C): the capacitor alone feeds the load during the on-time |
| Maximum gain | "How high it can go" | Set by resistances, not by D; typically a few times Vin |
| RHP zero | "Hard to control" | Increasing D first lowers Vout before raising it |

## Further Reading

- [Texas Instruments, SLVA372 "Basic Calculation of a Boost Converter's Power Stage"](https://www.ti.com/lit/an/slva372d/slva372d.pdf) — the standard design equations with a worked example
- Robert W. Erickson and Dragan Maksimovic, *Fundamentals of Power Electronics*, 3rd ed. (Springer), Chapters 2-3 — the boost's steady state and the effect of inductor resistance on its gain
- [TI, TPS61023 datasheet](https://www.ti.com/product/TPS61023) — real boost converter design sections
- [MIT OpenCourseWare 6.334 "Power Electronics"](https://ocw.mit.edu/courses/6-334-power-electronics-spring-2007/) — lecture notes on boost and buck-boost converters
