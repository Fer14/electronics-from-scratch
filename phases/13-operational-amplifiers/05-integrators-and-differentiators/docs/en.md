# Integrators and Differentiators

> Replace the feedback resistor with a capacitor and the virtual ground pours a current proportional to the input into it: the output becomes the running total of the input. Swap them, and the output becomes the input's rate of change.

**Type:** Build
**Prerequisites:** 13-03 (Inverting and Non-Inverting Amplifiers); Phase 07 (Capacitors), lessons 02-capacitance, 03-charging-and-discharging and 08-transient-simulation-from-scratch; Phase 10 (Filters and Resonance), lesson 03-decibels-and-bode-plots
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Integrate | Add up a quantity continuously over time: the running total | Filling a bucket: the water level is the total of everything the tap has poured |
| Differentiate | Find how fast a quantity is changing at each instant | A car's speedometer: how fast the distance travelled is changing |
| Integrator | An op-amp circuit whose output is (minus) the integral of its input | A bucket whose level you read as a voltage |
| Differentiator | An op-amp circuit whose output is (minus) the derivative of its input | A speedometer for voltages |
| Ramp | A voltage that rises (or falls) at a constant rate | A ruler held at a slant |
| Triangle wave | A wave made of rising and falling ramps | The teeth of a saw blade, symmetrical |
| Square wave | A wave that jumps between two levels | A light flashing on and off |
| Slope | Rate of change, in volts per second | The steepness of a hill |
| Drift | Slow, unwanted wandering of an integrator's output due to tiny DC errors | A bucket under a slowly dripping tap that will eventually overflow |
| Offset voltage | A tiny DC error at an op-amp's input (lesson 07) | The drip |
| Reset / leak resistor | A resistor across the integrating capacitor that limits drift | A small hole in the bucket that stops it overflowing |
| Noise gain | How much an amplifier boosts random fast fluctuations | A microphone that exaggerates every rustle |

## Learning Objectives

- Derive the integrator's output from the virtual ground and the capacitor law I = C dV/dt.
- Compute ramp rates and triangle amplitudes, and design an integrator for a given ramp.
- Explain integrator drift and fix it with a parallel resistor, accepting the trade-off.
- Derive the differentiator and explain why the pure version amplifies noise; add a series resistor to tame it.
- Read both circuits in the frequency domain: −20 dB/decade and +20 dB/decade.

## The Problem

Many quantities in the world are totals or rates. A car's position is the total of its speed over time; a battery's charge is the total of its current; the sweep of an oscilloscope's beam is a steadily rising voltage. Conversely, a speedometer, a heart-rate monitor's edge detector, and a motor controller's "derivative" term all need rates of change.

In Phase 07 a capacitor charged through a resistor gave a curve that was only approximately straight at the start, and bent over as the capacitor filled (the exponential). With an op-amp we can force the charging current to stay constant, so the capacitor's voltage rises in a perfectly straight line. That one trick gives precise ramps, triangle waves and analogue computers that solve differential equations.

## The Physics

A capacitor's law (Phase 07) in words: **the current into a capacitor equals its capacitance times how fast its voltage is changing**:

```
I = C × dV/dt
```

Read it both ways:

- If you push a **constant** current I into it, its voltage changes at a constant rate I/C (volts per second): a straight ramp.
- If you **force** its voltage to change, the current that flows is proportional to how fast you change it.

In a plain RC circuit, the current is (V_in − V_C)/R, which shrinks as V_C rises: the ramp bends. Put the capacitor in an op-amp's feedback path and its left plate sits at the virtual ground (0 V), so the current is V_in/R regardless of the capacitor's voltage. That constant current is the whole secret.

What the bucket analogy gets wrong: a bucket only fills. A capacitor in an integrator "fills" in either direction: positive input current raises one plate and lowers the other, and the output voltage can go negative as easily as positive (within the rails).

## The Concept

### The integrator

```
                 R                 C
   V_in -------/\/\/----+--------| |--------+
                        |                   |
                        +----|- \           |
                             |    >---------+---- V_out
                  ground ----|+ /
```

1. Virtual ground: V− = 0 V.
2. Current through R: I = V_in / R. No current enters the op-amp, so all of it flows into the capacitor.
3. The capacitor's left plate is at 0 V and its right plate is the output, so its voltage is −V_out. Using I = C dV/dt with V = −V_out:

```
dV_out/dt = −V_in / (R C)
```

Read: "the output changes at a rate equal to minus the input divided by RC". For a constant input, that is a straight ramp. Over time, the output is minus the running total (integral) of the input, scaled by 1/(RC):

```
V_out(t) = V_out(0) − (1 / RC) × ∫ V_in dt
```

**Worked example.** V_in = −1 V, R = 10 kΩ, C = 100 nF. RC = 10⁴ × 10⁻⁷ = 1 ms. Rate = −(−1)/0.001 = **+1000 V/s**, i.e. 1 V per millisecond. The simulator:

| t | V_out | Ideal |
|---|---|---|
| 0 ms | 0.0000 V | 0.00 V |
| 1 ms | 1.0000 V | 1.00 V |
| 2 ms | 2.0000 V | 2.00 V |
| 3 ms | 2.9999 V | 3.00 V |
| 5 ms | 4.9998 V | 5.00 V |

The current through R and C is a constant −100 µA (−1 V / 10 kΩ; the minus sign just says it flows from the virtual ground back toward the −1 V source). The ramp would continue until the output reaches the +12 V rail at 12 ms.

### Square in, triangle out

Feed a ±1 V square wave at 1 kHz into an integrator with R = 10 kΩ and C = 10 nF (RC = 0.1 ms). During each half period (0.5 ms) the input is constant, so the output ramps at 1 V / 0.1 ms = 10,000 V/s, for 0.5 ms: a change of 5 V. Then the input flips and the ramp reverses. The output is a **triangle wave of 5 V peak-to-peak**. Simulated: 4.992 V peak-to-peak, from −2.552 V to +2.440 V.

(A 1 MΩ resistor across C, explained next, slightly rounds the ramps and centres the triangle around 0 V; without it, the triangle would sit wherever the first half-cycle left it.)

### The drift problem

An integrator integrates *everything*, including errors. A real op-amp has an input offset voltage of perhaps 1 mV (lesson 07). With no input signal at all, that 1 mV acts like an input: it drives 1 mV / 10 kΩ = 0.1 µA into the capacitor forever.

| Time | Plain integrator | With 1 MΩ across C |
|---|---|---|
| 0.05 s | 0.051 V | 0.040 V |
| 0.10 s | 0.101 V | 0.064 V |
| 0.20 s | 0.201 V | 0.087 V |
| 0.50 s | 0.500 V | 0.100 V |

The plain integrator climbs at 1 V/s and would hit the 12 V rail after 12 s, with no input at all. A **leak resistor** R_L across C gives DC a path. At DC the capacitor is an open circuit, so for the offset (which sits at the + input, lesson 07) the circuit is a non-inverting amplifier with gain 1 + R_L/R = 1 + 1 MΩ/10 kΩ = 101. The output settles at 101 × 1 mV ≈ 0.1 V instead of running away.

The price: the circuit only integrates well at frequencies where C's impedance is much smaller than R_L, i.e. above f = 1/(2π R_L C). Below it, it behaves like an ordinary amplifier with gain −R_L/R. Other practical fixes: a switch that resets C periodically (as in oscilloscope sweeps and in the integrating ADCs of multimeters), or a feedback loop that keeps the output centred.

### The differentiator

Swap R and C:

```
                 C                 R_F
   V_in --------| |------+--------/\/\/------+
                         |                   |
                         +----|- \           |
                              |    >---------+---- V_out
                   ground ----|+ /
```

The capacitor's right plate sits at the virtual ground, so its voltage equals V_in, and its current is C dV_in/dt. All of it flows through R_F:

```
V_out = −R_F C × dV_in/dt
```

Read: "the output is minus R_F C times the rate of change of the input". Feed it a triangle with slopes of ±10,000 V/s and R_F C = 10 kΩ × 10 nF = 0.1 ms: V_out = ∓0.1 ms × 10,000 V/s = ∓1 V. **A triangle in, a square out.** The script chains the two: square → integrator → triangle → differentiator → square again. The recovered square goes from −1.018 V to +1.017 V: the original ±1 V, with a small overshoot at each corner.

### Frequency-domain view

For a sine of frequency f, the capacitor's impedance is Z_C = 1/(j 2π f C) (Phase 09). The inverting gain formula −Z_F/Z_I gives:

- Integrator: −Z_C/R → |gain| = 1/(2π f R C). It halves every time the frequency doubles: **−20 dB per decade**, a perfect low-pass. 0 dB (unity gain) at f = 1/(2π RC).
- Differentiator: −R/Z_C → |gain| = 2π f R C: **+20 dB per decade**, rising forever.

With R = 10 kΩ and C = 10 nF, unity gain falls at f = 1/(2π × 10⁻⁴) = 1592 Hz:

| Frequency | Integrator | 1/(2πfRC) | Pure differentiator | 2πfRC | Differentiator with 1 kΩ in series |
|---|---|---|---|---|---|
| 10 Hz | 84.6 | 159.2 | 0.006 | 0.006 | 0.006 |
| 100 Hz | 15.72 | 15.92 | 0.063 | 0.063 | 0.063 |
| 1592 Hz | 1.000 | 1.000 | 1.000 | 1.000 | 0.995 |
| 10 kHz | 0.159 | 0.159 | 6.28 | 6.28 | 5.32 |
| 100 kHz | 0.016 | 0.016 | 62.8 | 62.8 | 9.88 |

The integrator falls short at 10 Hz because of its 1 MΩ leak resistor (corner at 1/(2π × 1 MΩ × 10 nF) = 15.9 Hz, below which the gain flattens toward 100).

### Why pure differentiators are trouble

The pure differentiator's gain keeps climbing: ×63 at 100 kHz, ×630 at 1 MHz. Any high-frequency noise (and every real signal has some) is amplified enormously. Worse, a real op-amp's own gain falls with frequency (lesson 07), and the combination tends to ring or oscillate. The practical fix is a small resistor R_S in series with C: above f = 1/(2π R_S C) the input looks like a plain resistor and the gain levels off at R_F/R_S (= 10 here). That is the right-hand column: 9.88 instead of 62.8 at 100 kHz. In practice, true differentiators are rare; integrators are everywhere.

## Build It

### Step 1: A ramp with optional errors

```python
def ramp(input_volts, ohms, farads, stop, offset_volts=0.0, leak_ohms=None):
    circuit = Circuit()
    circuit.voltage_source("VIN", "in", "0", input_volts)
    circuit.resistor("R", "in", "n", ohms)
    circuit.capacitor("C", "n", "out", farads, v0=0.0)
    if leak_ohms:
        circuit.resistor("RLEAK", "n", "out", leak_ohms)
    circuit.voltage_source("VOS", "p", "0", offset_volts)
    circuit.opamp("U1", plus="p", minus="n", out="out", gain=1e5, rails=RAILS)
    return circuit.transient(t_stop=stop, dt=stop / 2000)
```

`VOS` holds the + input at the offset voltage, our stand-in for the op-amp's internal error. With `offset_volts=0.0` it is just a ground.

### Step 2: The square-triangle-square chain

```python
circuit.pulse_source("VSQ", "sq", "0", low=-1.0, high=1.0, period=1e-3, duty=0.5)
circuit.resistor("RI", "sq", "n1", 10e3)
circuit.capacitor("CI", "n1", "tri", 10e-9, v0=0.0)
circuit.resistor("RLEAK", "n1", "tri", 1e6)
circuit.opamp("U1", plus="0", minus="n1", out="tri", gain=1e5, rails=RAILS)
circuit.capacitor("CD", "tri", "x", 10e-9, v0=0.0)
circuit.resistor("RD", "x", "n2", 1e3)
circuit.resistor("RF", "n2", "back", 10e3)
circuit.opamp("U2", plus="0", minus="n2", out="back", gain=1e5, rails=RAILS)
```

We run 40 ms and measure the last 2 ms, after the leak resistor has centred the triangle.

### Step 3: AC sweeps

`show_frequency_response` builds an integrator, a pure differentiator and a differentiator with a 1 kΩ series resistor, and compares their AC gains with the formulas.

```
uv run python phases/13-operational-amplifiers/05-integrators-and-differentiators/code/main.py
```

## Use It

- **Function generators**: a Schmitt trigger (lesson 02) and an integrator in a loop make a triangle and a square wave at the same time; classic chips like the XR2206 work this way.
- **Dual-slope ADCs**: the analogue-to-digital converter in most handheld multimeters integrates the input for a fixed time, then integrates a reference back down to zero and counts how long that takes. Errors in R and C cancel out, which is why cheap meters are so accurate.
- **PID controllers**: the "I" (integral) term of a motor or temperature controller removes steady errors; the "D" (derivative) term reacts to fast changes, always with a limited high-frequency gain.
- **Charge amplifiers**: piezoelectric sensors and microphones produce charge; an integrator turns charge into voltage (V = Q/C).
- **Analogue computers**: before digital computers, chains of integrators solved differential equations (trajectories, chemical reactions) in real time. Electronic music synthesizers still use the same blocks.
- **Choosing the capacitor**: for integrators use film capacitors (polypropylene, polystyrene) or C0G ceramics, which have little leakage and little "memory"; electrolytics leak too much.

## Try It in the Lab

An inverting integrator: −1 V input, a 10 kΩ input resistor, and an empty slot for the feedback capacitor (starting empty). A downstream timer fires when the ramp crosses 5 V, and it must fire about 1 ms after the start. A second goal checks the ramp is straight (about half way at 0.5 ms).

Think about: the current the virtual ground forces through the resistor, the ramp rate I/C, and the capacitance that gives 5 V in 1 ms. Which standard value is closest? What does a ten-times-smaller or larger capacitor do to the timing?

## Common Mistakes

- **Forgetting the minus sign.** A positive input makes the inverting integrator's output ramp *down*.
- **No DC path across C.** A pure integrator drifts to a rail because of offsets and bias currents; use a leak resistor or a reset switch.
- **Leak resistor too small.** Then the circuit only integrates at high frequencies and is just an amplifier below 1/(2π R_L C).
- **Using a pure differentiator.** It amplifies noise without limit; add a series resistor (and often a small capacitor across R_F).
- **Ignoring the rails.** An integrator's output stops ramping when it hits a rail, and takes time to recover.
- **Electrolytic capacitors in integrators.** Their leakage current acts like an extra input.

## Exercises

1. An integrator has R = 47 kΩ and C = 220 nF. A constant 0.5 V input is applied. What is the ramp rate, and how long until the output reaches −10 V?
2. A ±2 V, 500 Hz square wave drives an integrator with R = 10 kΩ, C = 47 nF. What is the triangle's peak-to-peak amplitude?
3. With a 2 mV offset, R = 100 kΩ, C = 1 µF and no leak resistor, how long until a ±15 V op-amp saturates?
4. A differentiator has C = 100 nF and R_F = 10 kΩ. The input is a ramp rising at 50 V/s. What is the output? What is it if the input is a 1 V-amplitude sine at 1 kHz?
5. In the script, change the leak resistor in `square_chain` to 100 kΩ. How do the triangle's shape and amplitude change? Explain with the corner frequency 1/(2π R_L C).

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Integrator | "Miller integrator" | Capacitor in feedback: dV_out/dt = −V_in/(RC) |
| Differentiator | "Differentiating amp" | Capacitor at the input: V_out = −R C dV_in/dt |
| RC (time constant) | "Integration time" | Sets the scale: 1/(RC) volts per second per volt of input |
| Drift | "Integrator runaway" | Output wandering to a rail by integrating tiny DC errors |
| Leak resistor | "DC feedback resistor" | Resistor across C that limits DC gain to R_L/R |
| Unity-gain frequency | "Crossover" | f = 1/(2π RC), where an ideal integrator or differentiator has gain 1 |
| Noise gain (of a differentiator) | "High-frequency gain" | Rises at +20 dB/decade unless limited by a series resistor |

## Further Reading

- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., sections 4.2.6 (integrators) and 4.5.7 (differentiators).
- *All About Circuits*, Volume III, chapter 8, "Differentiator and integrator circuits". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-8/differentiator-integrator-circuits/
- W. Jung (ed.), *Op Amp Applications Handbook* (Analog Devices), chapter H "Op amp history", which traces the op amp back to the integrators of analogue computers. https://www.analog.com/en/resources/technical-books/op-amp-applications-handbook.html
- Texas Instruments, "Integrator Circuit" analog engineer's circuit (SBOA275). https://www.ti.com/lit/pdf/sboa275
