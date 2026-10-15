# Impedance

> Impedance is resistance that also remembers timing. With it, Ohm's law, series, parallel and the voltage divider all work for AC, one frequency at a time.

**Type:** Build
**Prerequisites:** Phase 04 (Kirchhoff's Laws), Lessons 04 (Series and Parallel Resistors) and 05 (The Voltage Divider); Phase 09, Lessons 04 (Complex Numbers for Circuits) and 05 (Phasors)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Impedance (Z) | How strongly a part opposes AC current at a given frequency, together with how much it shifts the current's timing; a complex number in ohms | The "effort" to push a swing: depends on how hard and on when in the swing you push |
| Resistance (R) | The real part of impedance: opposition that turns energy into heat, with no timing shift | Friction |
| Reactance (X) | The imaginary part of impedance: opposition that stores and returns energy, shifting timing by 90 degrees | A spring: pushes back, but gives the energy back |
| Capacitive reactance | The reactance of a capacitor, X_C = -1 / (omega C): large at low frequency, small at high | A small balloon on a pipe: a slow push fills it up and it stops the flow; a fast back-and-forth flows easily |
| Inductive reactance | The reactance of an inductor, X_L = omega L: small at low frequency, large at high | A heavy flywheel in the pipe: a steady flow is easy, fast reversals are hard |
| Generalized Ohm's law | V = Z x I with phasors | Ohm's law, upgraded to remember timing |
| Admittance (Y) | One over impedance, Y = 1 / Z, in siemens: how easily current flows | Conductance for AC: "how wide the pipe is" |
| Impedance divider | The voltage divider with impedances instead of resistances | A divider whose ratio changes with frequency: the seed of every filter |
| Corner frequency | The frequency where a reactance equals the resistance it works against | The speed at which a cyclist's air drag equals the rolling friction |

## Learning Objectives

- Define impedance as the ratio of voltage phasor to current phasor, Z = V / I, and explain what its size and its angle mean.
- Derive Z_R = R, Z_C = 1 / (j omega C) and Z_L = j omega L from the phasor laws of Lesson 05.
- Compute the reactance of capacitors and inductors at any frequency and describe their DC and high-frequency limits.
- Combine impedances in series and in parallel, and use an impedance divider to predict an output voltage.
- Confirm hand calculations with the simulator's AC analysis.

## The Problem

A speaker crossover, a mains filter in a power supply, a guitar tone knob, the tuning circuit of a radio: all are made of resistors, capacitors and inductors, and all depend on frequency. With Lesson 05 you can solve one of them by writing each part's phasor law and then Kirchhoff's laws, but you have to treat each kind of part differently.

It would be far nicer if every part, R, L or C, could be described by **one number** that plays the role of resistance, so that all the tools of Phases 04 and 05 (Ohm's law, series and parallel rules, the voltage divider, nodal analysis) worked unchanged. That number is the impedance. It is a complex number, it depends on frequency, and with it AC circuit analysis looks exactly like DC analysis, just with j's in it. This lesson builds that tool and checks it against the simulator.

## The Physics

### Why a capacitor lets fast signals through

A capacitor is two plates separated by an insulator (Phase 07). No charge ever crosses the gap. Yet AC "flows through" it: as the voltage swings up, charge piles onto one plate and leaves the other; as it swings down, the flow reverses. The current in the wires is real, even though no electron jumps the gap.

How much current? To change the voltage by some amount, a fixed amount of charge must move (q = C x v). A slow wave gives plenty of time per swing, so the same charge moves slowly: small current. A fast wave forces the same charge in and out in much less time: large current. **So the faster the wave, the more current flows for the same voltage**: the capacitor opposes high frequencies less. At DC (frequency zero) it fills up once and then no current flows at all: an open circuit.

### Why an inductor blocks fast signals

An inductor is a coil (Phase 08). Any change in its current changes its magnetic field, and Faraday's law makes the coil produce a voltage that fights the change: v = L x di/dt. A slow current change produces a small opposing voltage; a fast one produces a large one. **So the faster the wave, the more the inductor opposes it.** At DC the current is not changing at all, so the inductor is just a piece of wire: a short circuit (apart from its small wire resistance).

### Why a resistor does not care

A resistor turns energy into heat at every instant, following v = R x i at every instant. It has no memory of what happened a moment ago, so frequency makes no difference to it, and its current is always in step with its voltage.

## The Concept

### Impedance: the ratio of two phasors

For any two-terminal part in AC steady state, write the voltage across it as a phasor V and the current through it as a phasor I (Lesson 05). Define

```
Z = V / I        (read: "the impedance is the voltage phasor divided by the current phasor")
```

Z is a complex number measured in ohms. Using Lesson 04's rules for division:

- **size of Z** = (size of V) / (size of I): how many volts of amplitude per ampere of amplitude. Exactly like resistance.
- **angle of Z** = (angle of V) - (angle of I): how far the voltage is ahead of the current.

Turned around, this is the **generalized Ohm's law**:

```
V = Z x I         and         I = V / Z
```

### The three impedances

From Lesson 05:

| Part | Phasor law | Impedance Z = V / I | Size | Angle |
|---|---|---|---|---|
| Resistor | V = R I | Z_R = R | R | 0 deg (in step) |
| Capacitor | I = j omega C V | Z_C = 1 / (j omega C) = -j / (omega C) | 1 / (omega C) | -90 deg (current leads) |
| Inductor | V = j omega L I | Z_L = j omega L | omega L | +90 deg (voltage leads) |

(For the capacitor we used 1 / j = -j from Lesson 04.)

Read them aloud: "the impedance of a capacitor is one over j omega C; of an inductor, j omega L". With omega = 2 pi f, the frequency sits right there in the formula: the capacitor's impedance shrinks as frequency grows, the inductor's grows.

### Resistance and reactance

Any impedance can be written in rectangular form as

```
Z = R + jX
```

The real part R is the **resistance**: the part that dissipates energy as heat. The imaginary part X is the **reactance**: the part that stores energy and gives it back each cycle (in the capacitor's electric field, Phase 07, Lesson 06, or the inductor's magnetic field). For a pure capacitor, X_C = -1 / (omega C), negative. For a pure inductor, X_L = omega L, positive. A positive reactance is called **inductive**, a negative one **capacitive**.

### Worked numbers: how sizes change with frequency

For R = 1 kOhm, C = 1 microfarad and L = 10 mH:

| f | omega = 2 pi f | |Z_R| | |Z_C| = 1 / (omega C) | |Z_L| = omega L |
|---|---|---|---|---|
| 10 Hz | 62.83 rad/s | 1000 ohm | 1 / (62.83 x 1e-6) = 15,915 ohm | 62.83 x 0.01 = 0.628 ohm |
| 100 Hz | 628.3 | 1000 | 1,591.5 | 6.283 |
| 1 kHz | 6,283 | 1000 | 159.15 | 62.83 |
| 10 kHz | 62,832 | 1000 | 15.92 | 628.3 |
| 100 kHz | 628,319 | 1000 | 1.59 | 6,283 |

Every factor of 10 in frequency divides the capacitor's impedance by 10 and multiplies the inductor's by 10. On a log-log plot (the script's `out.png`) the resistor is a flat line, the capacitor a line sloping down, the inductor a line sloping up.

```
 |Z| (log)
   ^
   | \ capacitor                     / inductor
   |   \                           /
   |-----\----------------------/-------- resistor (flat)
   |       \                  /
   |         \              /
   +----------------------------------> f (log)
     low f: C blocks,           high f: L blocks,
            L passes                    C passes
```

The limits are worth memorising:

- **At DC (f = 0):** a capacitor is an **open circuit** (infinite impedance), an inductor is a **short** (zero impedance).
- **At very high frequency:** a capacitor acts like a short, an inductor like an open circuit.

### Worked example: Ohm's law at 1 kHz

Put a 1 V amplitude, 1 kHz source across each part alone.

- Resistor: I = 1 / 1000 = 1 mA, at 0 degrees.
- Capacitor: Z_C = -j159.15 ohm. I = 1 / (-j159.15) = j / 159.15 = j0.006283 A = 6.283 mA at +90 degrees (leading).
- Inductor: Z_L = j62.83 ohm. I = 1 / (j62.83) = -j0.01592 A = 15.92 mA at -90 degrees (lagging).

### Series and parallel: the old rules, with complex numbers

Why do the resistor rules carry over? Because they came from Kirchhoff's laws, and Lesson 05 showed that Kirchhoff's laws hold for phasors.

- **Series:** the same current I flows through each part, and the voltages add: V = Z1 I + Z2 I + ... = (Z1 + Z2 + ...) I. So **series impedances add**: Z = Z1 + Z2 + ...
- **Parallel:** the same voltage V is across each part, and the currents add: I = V/Z1 + V/Z2 + ... So **parallel impedances combine as one over the sum of the reciprocals**: 1/Z = 1/Z1 + 1/Z2 + ..., and for two parts Z = Z1 Z2 / (Z1 + Z2).

**Worked example, series RLC at 1 kHz** (R = 100 ohm, L = 10 mH, C = 1 microfarad):

```
   top o--/\/\/\--o--@@@@--o--||--o 0
         100 ohm   x 10 mH  y  1 uF
```

- Z_R = 100
- Z_L = j62.83
- Z_C = -j159.15
- Z = 100 + j62.83 - j159.15 = 100 - j96.32 ohm

Size: sqrt(100^2 + 96.32^2) = sqrt(10,000 + 9,277) = sqrt(19,277) = 138.8 ohm. Angle: atan2(-96.32, 100) = -43.9 degrees. The net reactance is negative: at 1 kHz this circuit behaves "capacitively", the capacitor's reactance beats the inductor's. The current from a 1 V source is 1 / 138.8 = 7.20 mA, at +43.9 degrees (leading the voltage). Notice that the inductor's and capacitor's reactances **cancel partly**. At one special frequency they cancel completely: that is resonance, Phase 10, Lesson 05.

**Worked example, R in parallel with C at 1 kHz** (1 kOhm and 1 microfarad):

1. 1 / Z_R = 1 / 1000 = 0.001 S (siemens: one over ohms).
2. 1 / Z_C = j omega C = j0.0062832 S.
3. Sum: 0.001 + j0.0062832.
4. Z = 1 / (0.001 + j0.0062832). Multiply by the conjugate: (0.001 - j0.0062832) / (0.001^2 + 0.0062832^2) = (0.001 - j0.0062832) / 0.000040478 = 24.70 - j155.22 ohm.

Size 157.2 ohm at -81.0 degrees: smaller than either the 1000 ohm or the 159.15 ohm alone, as parallel combinations always are, and mostly capacitive. Reciprocals of impedances have a name, **admittance**, Y = 1 / Z, and in parallel they simply add.

### The impedance divider

The voltage divider of Phase 04, Lesson 05 said V_out = V_in x R2 / (R1 + R2). Its derivation used only Ohm's law and series addition, so with impedances:

```
V_out = V_in x Z2 / (Z1 + Z2)
```

Take an inductor of 22 mH in series and a 100 ohm resistor to ground, output across the resistor:

```
 in o---@@@@@@---o out
  (~)   L 22 mH  |
   |            [R] 100 ohm
   |             |
 0 o-------------o
```

V_out / V_in = 100 / (100 + j omega 0.022).

- **50 Hz:** omega L = 314.16 x 0.022 = 6.912 ohm. Ratio = 100 / (100 + j6.912). Size = 100 / sqrt(100^2 + 6.912^2) = 100 / 100.24 = 0.9976. Nearly all the signal passes.
- **723 Hz:** omega L = 4,543 x 0.022 = 99.9 ohm, equal to R. Size = 100 / sqrt(100^2 + 100^2) = 0.707, at -45 degrees. This is the **corner frequency**, f = R / (2 pi L) = 100 / (2 x 3.14159 x 0.022) = 723 Hz.
- **10 kHz:** omega L = 62,832 x 0.022 = 1,382 ohm. Size = 100 / sqrt(100^2 + 1,382^2) = 100 / 1,386 = 0.0722. Only 7% gets through.

Low frequencies pass, high frequencies are blocked: you have just designed a **low-pass filter**. Phase 10 is all about such circuits, and it will measure these ratios in **decibels**: 20 x log10(ratio), so 0.9976 is -0.02 dB, 0.707 is -3 dB and 0.0722 is -22.8 dB.

## Build It

### Step 1: Impedance functions

```python
def z_resistor(ohms, freq):
    return complex(ohms, 0.0)


def z_capacitor(farads, freq):
    return 1 / (1j * 2 * math.pi * freq * farads)


def z_inductor(henries, freq):
    return 1j * 2 * math.pi * freq * henries


def series(*impedances):
    return sum(impedances)


def parallel(*impedances):
    return 1 / sum(1 / z for z in impedances)
```

Each function is one row of the table above. `*impedances` lets you pass any number of parts. The script prints the frequency table for 1 kOhm, 1 microfarad and 10 mH.

### Step 2: Ohm's law at 1 kHz

For each part alone, `current = 1.0 / z` gives 1 mA at 0 deg, 6.283 mA at +90 deg and 15.92 mA at -90 deg.

### Step 3: Measuring an impedance with the simulator

```python
def measured_impedance(build, freq):
    c = Circuit()
    c.sine_source("V1", "top", "0", amplitude=1.0, freq=freq)
    build(c)
    a = c.ac([freq], source="V1")
    return complex(a.v("top")[0]) / complex(a.i("V1")[0])
```

This is what an impedance meter does: apply a known AC voltage, measure the AC current, divide. `build` is a function that adds the network between node `top` and ground. The simulator's `a.i("V1")` is the complex current the source pushes out of its plus terminal. For the series RLC it returns 100 - j96.32 ohm, matching the hand result (138.8 ohm at -43.93 deg).

### Step 4: Parallel

`parallel(z_resistor(r, f), z_capacitor(cap, f))` gives 24.7 - j155.2 ohm, and the simulator agrees.

### Step 5: The divider, by hand and by simulator

```python
c = Circuit()
c.sine_source("V1", "in", "0", amplitude=1.0, freq=50.0)
c.inductor("L1", "in", "out", l_div)
c.resistor("R1", "out", "0", r_div)
freqs = np.array([50.0, 723.0, 10_000.0])
a = c.ac(freqs, source="V1")
```

`ac()` accepts a whole array of frequencies at once. For each one the script prints the hand formula Z2 / (Z1 + Z2) and the simulator's `a.gain_db("out")`: -0.02 dB, -3.01 dB and -22.83 dB both ways.

The script ends by saving `out.png`, the log-log plot of |Z| against frequency for the three parts.

## Use It

- **Decoupling capacitors.** Every chip on a board has a 100 nF capacitor next to its power pin. At 100 MHz its impedance is 1 / (2 pi x 1e8 x 1e-7) = 0.016 ohm: a near-short for fast noise, but an open circuit for the DC supply.
- **Chokes.** Inductors in series with power lines (the "ferrite beads" and coils in a laptop charger) pass the DC or 50 Hz power but block high-frequency noise.
- **Speaker impedance.** A loudspeaker labelled "8 ohm" has an impedance that varies with frequency, from about 6 ohm to 40 ohm or more; the label is a nominal value. Amplifier datasheets give power "into 8 ohm" and "into 4 ohm".
- **Cables and antennas.** Coaxial TV cable has a characteristic impedance of 75 ohm, lab and radio cable 50 ohm; matching impedances avoids reflections (Phase 21).
- **Datasheets of capacitors.** Real capacitors show an impedance curve that falls like 1 / (omega C), bottoms out, then rises again at high frequency because their leads have inductance (Phase 07, Lesson 07).

## Try It in the Lab

The lab task "Let 50 Hz through, stop 10 kHz" gives you the divider of this lesson: a slot for an inductor in series, a 100 ohm resistor to ground, and an AC source. Mains-frequency power (50 Hz) must reach the resistor almost untouched (at most 0.5 dB lost), while 10 kHz switching noise must be cut by at least 20 dB (to a tenth or less). Work out what the inductor's impedance should be at each frequency: small compared with 100 ohm at 50 Hz, large compared with 100 ohm at 10 kHz. There is a window of good values; some parts are too small to stop the noise, one is so big it starts eating the power.

## Common Mistakes

- **Adding sizes instead of complex impedances.** 100 ohm in series with j100 ohm is 141.4 ohm, not 200 ohm.
- **Forgetting the minus sign of the capacitor.** Z_C = -j / (omega C). Inductive and capacitive reactances have opposite signs and partly cancel in series.
- **Using f instead of omega.** X_L = 2 pi f L, not f L. Forgetting 2 pi makes reactances 6.28 times too small.
- **Thinking impedance is fixed.** A capacitor has no single "impedance": always ask "at what frequency?".
- **Using impedance for the start-up transient.** Impedance is a steady-state, single-frequency idea, like phasors.
- **Mixing up open and short at DC.** At DC, capacitors are open and inductors are shorts. Many beginners swap them.

## Exercises

1. **Reactances.** Compute the impedance of a 47 nF capacitor and of a 4.7 mH inductor at 50 Hz, 1 kHz and 100 kHz. At which frequency are their sizes equal?
2. **Series RL.** A 220 ohm resistor is in series with a 33 mH inductor at 1 kHz. Find Z in rectangular and polar form and the current from a 5 V amplitude source.
3. **Parallel RL.** Find the impedance of 100 ohm in parallel with 10 mH at 1 kHz. Is it more resistive or more inductive?
4. **Divider.** In a divider with R = 10 kOhm in series and C = 10 nF to ground, find V_out / V_in at 100 Hz, 1.59 kHz and 20 kHz, in size and angle. Which frequencies pass?
5. **Simulator.** Use `measured_impedance` to measure 100 ohm in series with 10 mH and 1 microfarad between 100 Hz and 10 kHz (use 50 frequencies). At what frequency is the size smallest, and what is the angle there? Compare with 1 / (2 pi sqrt(L C)).

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Impedance | "AC resistance" | Z = V / I for phasors; a complex number in ohms whose size scales amplitude and whose angle is the voltage's lead over the current |
| Resistance | "The real part" | Re(Z): dissipative opposition, no phase shift |
| Reactance | "The imaginary part" | Im(Z): energy-storing opposition; X_L = omega L > 0, X_C = -1 / (omega C) < 0 |
| Admittance | "One over Z" | Y = 1 / Z in siemens; admittances in parallel add |
| Generalized Ohm's law | "V = Z I" | Ohm's law for phasors, valid for any linear part at one frequency |
| Impedance divider | "The AC voltage divider" | V_out = V_in Z2 / (Z1 + Z2); frequency-dependent, so a filter |
| Corner frequency | "Where it starts to cut" | Frequency where |X| = R; the divider ratio is 0.707 there |

## Further Reading

- [All About Circuits, Vol. II (AC), Chapter 4: Reactance and Impedance (Capacitive)](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-4/series-resistor-capacitor-circuits/) and [Chapter 3 (Inductive)](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-3/series-resistor-inductor-circuits/) — many solved RL and RC examples.
- *The Art of Electronics*, Horowitz & Hill, 3rd ed., Section 1.7 "Impedance and reactance" — the generalized Ohm's law and the divider, compactly.
- *Practical Electronics for Inventors*, Scherz & Monk, 4th ed., Chapter 2 (sections on reactance and impedance) — practical tables and real-part examples.
- [Murata SimSurfing: impedance characteristics of real capacitors](https://ds.murata.co.jp/simsurfing/) — real capacitor impedance curves.
