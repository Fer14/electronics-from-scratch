# RLC Resonance

> An inductor and a capacitor push in opposite directions. At one special frequency they cancel exactly, the circuit "rings" like a bell, and a small push builds a large swing.

**Type:** Learn
**Prerequisites:** Phase 10 (Filters and Resonance), Lessons 02 (RC Low-Pass and High-Pass) and 04 (RL Filters); Phase 09 (Alternating Current), Lessons 05 (Phasors) and 06 (Impedance); Phase 07 (Capacitors), Lesson 06 (Energy in the Electric Field); Phase 08 (Magnetism and Inductors), Lesson 04 (The Inductor)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Resonance | The condition where a system responds most strongly because it is driven at its own natural rhythm | Pushing a child on a swing at exactly the right moment each time |
| Resonant frequency (f0) | The frequency at which L and C reactances are equal, f0 = 1 / (2 pi sqrt(L C)) | The swing's own rhythm, set by the length of its ropes |
| Reactance (X) | The "AC resistance" of an inductor (X_L = 2 pi f L) or capacitor (X_C = 1 / (2 pi f C)), in ohms | How hard the door or the spring pushes back |
| Series RLC | R, L and C in one loop, one after another | A swing with friction in its hinges |
| Parallel LC (tank) | L and C side by side, connected across the same two nodes | A pendulum that trades energy between height and speed |
| Ringing | The oscillation that continues by itself after a kick, slowly dying away | A bell after it is struck |
| Damping | Whatever removes energy from the oscillation, here the resistance | A hand resting on the bell |
| Quality factor (Q) | How sharp the resonance is and how long the ringing lasts (Lesson 07 goes deeper) | A crystal glass rings for seconds (high Q); a cardboard box goes "thud" (low Q) |
| Voltage magnification | At resonance the voltage across L and across C can be many times the source voltage | A small, well-timed push making a big swing |
| Tuning | Adjusting L or C to move f0 to the frequency you want | Turning a radio's dial |

## Learning Objectives

- Explain resonance as the point where the inductor's and capacitor's reactances cancel, and derive f0 = 1 / (2 pi sqrt(L C))
- Calculate the impedance and current of a series RLC circuit at, below and above resonance
- Explain and compute the voltage magnification Q across L and C at resonance
- Simulate the free ringing of an LC circuit and see how resistance damps it
- Contrast series resonance (lowest impedance) with parallel resonance (highest impedance), and choose C to tune a circuit

## The Problem

An old AM radio has a single knob that picks one station out of dozens, all arriving at the antenna at the same time on different frequencies. Inside, the knob turns a variable capacitor connected to a coil. A metal detector beeps when its coil's resonant frequency shifts slightly near a coin. A quartz watch keeps time because a tiny crystal resonates at 32,768 Hz and nowhere else. Your phone's Wi-Fi and wireless charger depend on circuits tuned to one frequency.

All of these use **resonance**: the combination of an inductor and a capacitor responding enormously at one frequency and hardly at all at others. RC and RL filters (Lessons 02 and 04) fall off gently, at 20 dB per decade. With L and C together you can build filters that pick out a narrow slice of the spectrum. Resonance can also be dangerous: it can produce voltages much larger than the supply, or make a circuit oscillate when you did not want it to. This lesson builds the idea from the two reactances you already know.

## The Physics

### Energy that sloshes back and forth

Charge a capacitor and connect it across an inductor:

1. The capacitor pushes current through the inductor. The current grows slowly (the inductor resists changes in current, Phase 08), while the capacitor's voltage falls.
2. When the capacitor is empty (zero voltage), the current is at its maximum. All the energy, which was ½ C V² in the electric field, is now ½ L I² in the magnetic field.
3. The inductor will not let the current stop suddenly. It keeps pushing charge onto the capacitor, now with the opposite polarity, until the current reaches zero and the capacitor is fully charged the other way.
4. The process reverses, and repeats.

The energy sloshes between the capacitor's electric field and the inductor's magnetic field, exactly like a pendulum trades energy between height (potential energy) and speed (kinetic energy). With no resistance, it would go on forever. Any resistance turns a little energy into heat each cycle and the oscillation slowly dies: **ringing**.

```
  capacitor voltage
   +1 |\              /\              /\
      | \            /  \            /  \        with resistance,
    0 +--\----------/----\----------/----\--> t   each swing is a
      |   \        /      \        /             little smaller
   -1 |    \______/        \______/
         energy in C -> L -> C -> L ...
```

What the pendulum picture gets wrong: a pendulum's rhythm depends on gravity and length; an LC circuit's rhythm depends on L and C. And a real pendulum loses energy to air; an LC circuit loses it to resistance and also by radiating radio waves (which is exactly what an antenna wants).

### The natural frequency

How fast does it slosh? Bigger L means the current changes more sluggishly; bigger C means more charge must move to change the voltage. Both slow the oscillation. The result (which the next section derives from reactances) is

```
f0 = 1 / (2 pi sqrt(L * C))
```

Read it: "the resonant frequency is one over two pi times the square root of L times C". For L = 10 mH and C = 1 µF: L x C = 0.01 x 0.000001 = 1e-8; sqrt(1e-8) = 1e-4; 2 pi x 1e-4 = 6.283e-4; f0 = 1 / 6.283e-4 = **1591.5 Hz**.

The square root matters: to halve f0 you must make L x C four times bigger.

### Where the formula comes from: two reactances crossing

From Phase 09, the inductor's reactance X_L = 2 pi f L grows with frequency, and the capacitor's X_C = 1 / (2 pi f C) falls. In a series circuit their impedances are j X_L and -j X_C (opposite signs, because the inductor's voltage leads its current by 90° and the capacitor's lags by 90°). They add:

```
Z_series = R + j X_L - j X_C = R + j (X_L - X_C)
```

The two reactances cancel when X_L = X_C:

```
2 pi f L = 1 / (2 pi f C)   ->   (2 pi f)^2 = 1 / (L C)   ->   f = 1 / (2 pi sqrt(L C))
```

That is f0. The table for L = 10 mH, C = 1 µF:

| f | X_L | X_C | X_L - X_C | Behaves like |
|---|---|---|---|---|
| 200 Hz | 12.6 ohm | 795.8 ohm | -783.2 ohm | a capacitor (X_C wins) |
| 800 Hz | 50.3 ohm | 198.9 ohm | -148.7 ohm | a capacitor |
| 1591.5 Hz | 100.0 ohm | 100.0 ohm | 0 | a plain resistor R |
| 3000 Hz | 188.5 ohm | 53.1 ohm | +135.4 ohm | an inductor (X_L wins) |
| 10 kHz | 628.3 ohm | 15.9 ohm | +612.4 ohm | an inductor |

Below f0 the circuit is "capacitive", above f0 it is "inductive", and at f0 the L and C together act like **a short circuit** in series: only R is left.

## The Concept

### 1. The series RLC: a current peak at f0

```
   V_in ---[ L = 10 mH ]---a---[ C = 1 uF ]---b---+
                                                  |
                                              [ R = 10 ohm ]   <- V_out across R
                                                  |
   0 V -------------------------------------------+
```

The current is I = V_in / Z, with |Z| = sqrt(R² + (X_L - X_C)²).

**At f0**: |Z| = R = 10 ohm, so a 1 V source drives I = 1 / 10 = **100 mA**, the maximum. The output across R is the whole 1 V: gain 1, 0 dB.

**At f0 / 2 = 795.8 Hz**: X_L = 50 ohm, X_C = 200 ohm, X_L - X_C = -150 ohm. |Z| = sqrt(100 + 22,500) = 150.3 ohm. I = 6.65 mA. Gain across R = 0.0665 = -23.5 dB.

**At 2 f0**: by the symmetry of the formulas (X_L doubles to 200, X_C halves to 50) the same |Z| = 150.3 ohm and the same 6.65 mA.

So the voltage across R is a **band-pass** filter: big at f0, small on both sides. On a log frequency axis the curve is symmetric around f0. Lesson 06 uses this as a band-pass filter, and Lesson 07 measures how narrow the peak is.

### 2. Voltage magnification

At f0, 100 mA flows through the inductor, whose reactance is 100 ohm. The voltage across the inductor is I x X_L = 0.1 x 100 = **10 V**. Across the capacitor: also **10 V**. From a 1 V source!

How can that be? The inductor's and capacitor's voltages are 180° out of step (one leads the current by 90°, the other lags by 90°). At every instant they are equal and opposite, so they cancel *each other* around the loop, and Kirchhoff's voltage law is satisfied: 1 V source = 10 V (L) - 10 V (C) + 1 V (R). The source only has to supply what R uses up; the 10 V is the sloshing energy, built up over many cycles like the swing.

The magnification factor is the **quality factor**:

```
Q = X_L / R = X_C / R = sqrt(L / C) / R        (at f0)
```

For our values: sqrt(0.01 / 1e-6) = sqrt(10,000) = 100 ohm; Q = 100 / 10 = 10. The voltage across L and C is Q times the source voltage. (The quantity sqrt(L/C), in ohms, is called the **characteristic impedance**: the reactance of either part at resonance.)

This is a real hazard. A series LC circuit driven at resonance from a 230 V mains can put thousands of volts across a capacitor rated for 400 V. And it is a real tool: radio receivers use it to amplify a weak station before any transistor touches it.

### 3. Ringing and damping

Charge C to 1 V and let it discharge through L and R (no source). It oscillates at nearly f0, and its amplitude decays as e^(-R t / (2L)). With R = 1 ohm (Q = 100) the oscillation barely fades over 2 ms; with 10 ohm (Q = 10) it fades to a third; with 50 ohm (Q = 2) it is almost gone after 2 ms, and it oscillates a bit slower (1541 Hz) because heavy damping slows the sloshing. Above R = 2 sqrt(L/C) = 200 ohm (Q below 0.5) it does not oscillate at all: the capacitor just drains away. That is called **overdamped**. Exactly at 200 ohm it is **critically damped**: the fastest return to zero without overshoot. Car suspensions are designed near critical damping for the same reason.

### 4. The parallel tank: an impedance peak

Put L and C in **parallel** instead:

```
   V_in ---[ Rfeed = 10 k ]---+--- tank (V_out)
                              |
                        +-----+-----+
                        |           |
                      [ C ]       [ L ]
                        |         [ R_dcr = 1 ohm ]
                        |           |
   0 V -----------------+-----------+
```

In parallel, the currents in L and C are opposite at f0 and cancel *each other*: a large current circulates around the L-C loop, but very little current needs to come from outside. So the parallel combination has its **highest** impedance at f0, the opposite of the series case. For an ideal tank the impedance at f0 would be infinite; with the inductor's wire resistance R_dcr it is about

```
Z_tank(f0) = L / (C * R_dcr)
```

For L = 10 mH, C = 1 µF, R_dcr = 1 ohm: Z = 0.01 / (1e-6 x 1) = 10,000 ohm. Fed through 10 k ohm, the output at f0 is half the input (a divider with two equal 10 k "resistances"), while away from f0 the tank's impedance is small and the output collapses (-43.5 dB at f0/2 and 2 f0). Radio receivers, oscillators and the "tank circuits" of transmitters use this.

| | Series LC | Parallel LC |
|---|---|---|
| At f0 the LC looks like | a short circuit | an open circuit |
| Current from the source at f0 | maximum | minimum |
| Voltages / currents magnified | voltages across L and C (by Q) | currents in L and C (by Q) |
| Typical use | band-pass in series with the signal; notch to ground (Lesson 06) | band-pass across the signal; oscillators |

### 5. Tuning

To set f0, solve the formula for C (or L):

```
C = 1 / ((2 pi f0)^2 * L)
```

**Worked examples.**

- f0 = 1 kHz with L = 10 mH: (2 pi x 1000)² = 3.948e7; C = 1 / (3.948e7 x 0.01) = 2.533 µF. The nearest common value is 2.2 µF, giving 1073 Hz.
- f0 = 50 Hz with L = 1 H: C = 1 / ((314.16)² x 1) = 10.13 µF. Low frequencies need big parts.
- f0 = 1 MHz (AM radio) with L = 100 µH: C = 1 / ((6.283e6)² x 1e-4) = 253 pF. An old radio's tuning capacitor swings from about 30 to 365 pF; with a coil of about 250 µH that covers roughly 530 kHz to 1.8 MHz, the whole AM band.

## Build It

### Step 1: The reactance table

```python
def resonant_frequency(inductance, capacitance):
    return 1 / (2 * math.pi * math.sqrt(inductance * capacitance))
```

The script prints X_L, X_C and their difference at five frequencies; the difference crosses zero at f0 = 1591.5 Hz.

### Step 2: The current peak

```python
def series_rlc(resistance=R):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    c.inductor("L1", "in", "a", L)
    c.capacitor("C1", "a", "b", C)
    c.resistor("R1", "b", "0", resistance)
    return c
```

We sweep 3001 frequencies from 100 Hz to 100 kHz and divide the voltage across R by R to get the current:

```
  peak current 100.00 mA at 1592.2 Hz (hand: 1 V / 10 ohm = 100 mA at 1591.5 Hz)
  f =   795.8 Hz: |Z| =   150.3 ohm, current =   6.65 mA
  f =  1591.5 Hz: |Z| =    10.0 ohm, current = 100.00 mA
  f =  3183.1 Hz: |Z| =   150.3 ohm, current =   6.65 mA
```

The peak lands on the sweep point nearest f0.

### Step 3: Voltage magnification

```python
at_f0 = series_rlc().ac([f0], source="V1")
v_l = abs(at_f0.v("in")[0] - at_f0.v("a")[0])
v_c = abs(at_f0.v("a")[0] - at_f0.v("b")[0])
```

`a.v(node)` returns the complex phasor at each frequency (here a single one), so the voltage across a part is the difference of its two node phasors. Output:

```
  source 1.000 V: V_L = 10.000 V, V_C = 10.000 V, V_R = 1.000 V
  quality factor Q = sqrt(L / C) / R = 10.0; V_L and V_C are Q times the source
  V_L and V_C are opposite: V_L + V_C = 1.00e-09 V
```

The last line measures the voltage across L and C *together* (from node in to node b): essentially zero. Ten volts each, cancelling.

### Step 4: Ringing

```python
def ringing(resistance):
    c = Circuit()
    c.capacitor("C1", "top", "0", C, v0=1.0)
    c.inductor("L1", "top", "m", L)
    c.resistor("R1", "m", "0", resistance)
    return c.transient(t_stop=10e-3, dt=1e-6)
```

No source at all: `v0=1.0` starts the capacitor charged to 1 V, and the circuit is left alone. We count the falling zero-crossings in the first 3 ms to measure the ringing frequency:

```
  R =   1.0 ohm (Q = 100.00): rings at  1591.5 Hz; largest |v| after 2 ms = 0.896 V
  R =  10.0 ohm (Q = 10.00): rings at  1589.5 Hz; largest |v| after 2 ms = 0.333 V
  R =  50.0 ohm (Q =  2.00): rings at  1541.0 Hz; largest |v| after 2 ms = 0.007 V
  R = 400.0 ohm (Q =  0.25): does not ring (overdamped); largest |v| after 2 ms = 0.005 V
```

Check the decay for R = 10 ohm: e^(-R t / 2L) = e^(-10 x 0.002 / 0.02) = e^(-1) = 0.368. The printed 0.333 is a little lower because the largest |v| after 2 ms happens slightly later than 2 ms (at the next peak of the oscillation). The 50 ohm frequency matches the damped formula f0 x sqrt(1 - 1/(4Q²)) = 1591.5 x sqrt(0.9375) = 1541 Hz.

### Step 5: The parallel tank

```
  fed through 10 k ohm: output peaks at 1592.2 Hz with gain 0.500
  so the tank looks like 9988 ohm at f0 (hand: L / (C R_dcr) = 10000 ohm)
  at   795.8 Hz the gain is only -43.5 dB
```

The tank's impedance is computed from the divider: Z = 10 k x g / (1 - g).

### Step 6: Tuning

```python
def capacitance_for(freq, inductance):
    return 1 / ((2 * math.pi * freq) ** 2 * inductance)
```

The three worked examples above: 2.533 µF, 10.13 µF and 253.3 pF.

## Use It

- **Radio tuning.** Classic AM receivers use a ferrite-rod antenna coil (about 200 to 300 µH) and a variable capacitor. FM and Wi-Fi use smaller L and C, or printed resonators on the circuit board.
- **Crystal and ceramic resonators.** A quartz crystal behaves electrically like a series RLC with an extremely high Q (10,000 to 100,000), which is why watch and microcontroller clocks are accurate to parts per million. Datasheets list the *motional* L, C and R of the equivalent circuit.
- **Wireless charging and NFC.** Both the transmitter and receiver coils are tuned with capacitors to the same frequency (around 100 to 200 kHz for Qi, 13.56 MHz for NFC), so a small coupling transfers a lot of energy.
- **Unwanted resonance.** Every real capacitor has some series inductance (ESL), so it resonates: a 100 nF ceramic with 1 nH of ESL resonates near 16 MHz and behaves like an inductor above that (Phase 07, Lesson 07). Power-supply designers place several capacitor values in parallel to cover different frequency ranges.
- **Power factor correction capacitors** on motors (Phase 09, Lesson 07) can resonate with the grid's inductance at a harmonic of 50 Hz and cause large voltages; engineers check this.

## Try It in the Lab

Open **"Tune the circuit to the 1 kHz tone"**. A 10 mH coil and a 20 ohm resistor are fixed; choose the series capacitor. The circuit must pass a 1 kHz tone within 3 dB and cut a 3 kHz tone by at least 10 dB. Compute the exact C for f0 = 1 kHz, then compute f0 for each capacitor in the drawer. None is exact: decide which is close enough, and estimate with |Z| = sqrt(R² + (X_L - X_C)²) how much the 1 kHz tone loses with it. Why does the largest capacitor pass the 3 kHz test but fail the 1 kHz one?

## Common Mistakes

- **Forgetting the square root.** f0 = 1 / (2 pi sqrt(L C)): doubling C lowers f0 by a factor of 1.414, not 2.
- **Adding reactances as plain numbers.** X_L and X_C have opposite signs in the impedance: Z = R + j(X_L - X_C). They subtract.
- **Assuming the voltages across L and C are small.** At resonance they are Q times the source voltage. Rate the parts accordingly.
- **Confusing series and parallel resonance.** Series LC is a short at f0; parallel LC is an open at f0.
- **Ignoring the inductor's resistance.** In a parallel tank the DCR sets the impedance at resonance; in a series circuit it adds to R and lowers Q.
- **Expecting the ringing frequency to equal f0 at heavy damping.** It is lower, f0 sqrt(1 - 1/(4Q²)), and disappears below Q = 0.5.

## Exercises

1. **Easy.** Find f0 for L = 47 mH and C = 220 nF.
2. **Easy.** What C resonates with a 2.2 mH inductor at 10 kHz?
3. **Medium.** A series RLC has L = 1 mH, C = 10 nF and R = 5 ohm. Find f0, the characteristic impedance sqrt(L/C), Q, and the voltage across C at resonance when the source is 2 V.
4. **Medium.** For the circuit of this lesson (L = 10 mH, C = 1 µF, R = 10 ohm), compute |Z| and the current at 1400 Hz and 1800 Hz by hand. Check with the simulator using `series_rlc().ac([1400, 1800], source="V1")`.
5. **Hard.** In `ringing`, use R = 200 ohm (critical damping) and R = 150 ohm. Plot or print v(top) over the first 1 ms. Which one returns closest to zero fastest without going negative? Explain with the idea of an overdamped, critically damped and underdamped swing.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Resonance | "The magic frequency" | The frequency where X_L = X_C, so the reactances cancel and energy sloshes freely between L and C |
| Resonant frequency | "f-zero" | f0 = 1 / (2 pi sqrt(L C)) |
| Series resonance | "LC short" | At f0 the series LC has zero net reactance: the impedance is just R |
| Parallel resonance | "Tank circuit" | At f0 the parallel LC has a very high impedance, about L / (C R) |
| Characteristic impedance | "sqrt L over C" | sqrt(L / C), the reactance of L or C at f0 |
| Quality factor | "Q, sharpness" | sqrt(L / C) / R for a series RLC; the voltage magnification at f0 and a measure of how slowly ringing dies |
| Damping | "Losses" | Energy removal by resistance; underdamped rings, critically damped returns fastest, overdamped crawls back |

## Further Reading

- [All About Circuits, Volume II, Chapter 6: Resonance](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-6/electric-pendulum/) — the "electric pendulum", series and parallel resonance
- [The Feynman Lectures on Physics, Vol. I, Chapter 23 (Resonance)](https://www.feynmanlectures.caltech.edu/I_23.html) — the same mathematics for swings, springs and circuits
- [MIT OpenCourseWare 6.002, lectures on second-order circuits](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) — RLC ringing, damping and resonance
- *Practical Electronics for Inventors* (Scherz & Monk), section on resonant circuits — tuning circuits and real-world LC parts
