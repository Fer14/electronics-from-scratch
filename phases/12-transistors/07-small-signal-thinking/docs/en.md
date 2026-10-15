# Small-Signal Thinking

> Zoom in far enough on any smooth curve and it looks straight. Bias the transistor, zoom in on its operating point, and it becomes a resistor and a controlled current source. Then every linear tool from Phases 04-10 works again.

**Type:** Build
**Prerequisites:** 12-06 (Amplifiers and Biasing); Phase 11 (Semiconductors and Diodes), lesson 05-solving-nonlinear-circuits; Phase 05 (Circuit Analysis and Our Simulator), lessons 05-superposition and 08-dependent-sources
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Large signal | The full, nonlinear behaviour of a circuit, including bias | The whole mountain |
| Small signal | A tiny variation around the operating point, small enough that the curve looks straight | The flat-looking patch of ground you stand on |
| Linearisation | Replacing a curve by its tangent at one point | Laying a ruler against a ball |
| Transconductance (g_m) | The slope of collector current versus base-emitter voltage, ΔI_C/ΔV_BE | How much the flow changes per click of the tap |
| r_π (r-pi) | The small-signal resistance seen looking into the base, β / g_m | How heavy the tap handle feels |
| r_e | The small-signal resistance looking into the emitter, about 1 / g_m | The give in the emitter side |
| Hybrid-π model | The standard small-signal BJT model: r_π from base to emitter plus a current source g_m v_be from collector to emitter | A wiring-diagram stand-in for the transistor |
| Mid-band | The frequency range where coupling and bypass capacitors act as shorts | The middle of the road, away from both kerbs |
| Input resistance (R_in) | The resistance the signal source "sees" looking into the amplifier | How hard you must push to move the see-saw |
| Distortion / harmonics | Extra frequencies (2f, 3f, …) created when a nonlinear curve bends a sine wave | A slightly squashed circle |
| Superposition | In a linear circuit, the response to two sources is the sum of the responses to each (Phase 05) | Two ripples on a pond passing through each other |

## Learning Objectives

- Explain why a nonlinear transistor behaves linearly for small enough signals.
- Derive g_m = I_C / V_T from the slope of the exponential, and compute r_π and r_e.
- Draw the hybrid-π model and use it to predict gain and input resistance by hand.
- Build the small-signal model from linear parts in the simulator and show it matches the real transistor.
- Quantify how small "small" is: distortion of about v / (4 V_T) for the second harmonic.

## The Problem

Lesson 06 used a formula, |A_v| = R_C / (R_E + r_e), with an r_e that seemed to come from nowhere. And the simulator's "AC analysis" gave us a gain without ever simulating a waveform. Both rest on the same idea, **small-signal thinking**, and it is how every engineer analyses amplifiers.

The problem it solves: transistors are wildly nonlinear (exponential!), so Kirchhoff + Ohm + phasors (Phases 04-10) should not apply. But a well-designed amplifier only ever moves a few millivolts around its operating point. Over such a small range the exponential is nearly a straight line, and straight lines are exactly what our linear tools handle. This lesson makes that precise, shows how far it can be trusted, and gives you a model you can draw on a napkin.

## The Physics

### Zooming in on the exponential

The collector current is I_C = I_S e^(V_BE / V_T). Suppose the transistor is biased at V_BE = V_Q with current I_Q. Add a small signal v_be:

```
I_C = I_S e^((V_Q + v_be)/V_T) = I_Q × e^(v_be / V_T)
```

For small x, e^x ≈ 1 + x + x²/2 + … So

```
I_C ≈ I_Q × (1 + v_be/V_T + (v_be/V_T)² / 2 + ...)
```

Keep only the first-order term, and the *change* in collector current is

```
i_c = (I_Q / V_T) × v_be = g_m × v_be
```

Read: "the small-signal collector current equals the transconductance times the small base-emitter voltage, with g_m = I_C / V_T". That is the tangent of the exponential at the operating point. It is also exactly the slope Newton-Raphson used in lesson 11-05: the simulator's "companion model" *is* the small-signal model.

**The striking fact**: g_m depends only on the bias current, not on the transistor type, size or β. At 1 mA, every silicon BJT ever made has g_m = 1 mA / 25.85 mV = 38.7 mA/V.

### What the second term tells us

The neglected term (v_be/V_T)²/2 is the **distortion**. If v_be is a sine of amplitude v, the square of a sine contains a component at twice the frequency (sin² x = (1 − cos 2x)/2). The ratio of that second harmonic to the fundamental is

```
HD2 ≈ (v / V_T) / 4 = v / (4 V_T)
```

At v = 1 mV: 1/103.4 ≈ 1 %. At 10 mV: 9.7 %. So "small" means "well below V_T ≈ 26 mV", and for hi-fi quality, below about 1 mV at the base-emitter junction (or use degeneration, which reduces the v_be part of the input).

### Base and emitter resistances

The base current is I_C / β, so its small change is i_b = g_m v_be / β. Seen from the base, the junction looks like a resistance

```
r_π = v_be / i_b = β / g_m
```

Seen from the emitter (where the current is β + 1 times the base current), it looks like

```
r_e = v_be / i_e = r_π / (β + 1) ≈ 1 / g_m
```

## The Concept

### The hybrid-π model

Replace the transistor, *for small signals only*, by:

```
        base o-----+                 +-----o collector
                   |                 |
                 [r_π]          ( g_m × v_be )   current source, pointing c → e
                   |                 |
       emitter o---+-----------------+
```

Two linear elements: a resistor r_π between base and emitter, and a voltage-controlled current source (Phase 05) from collector to emitter whose value is g_m times the base-emitter voltage. (A fuller model adds r_o, the output resistance from the Early effect, and two capacitances for high frequencies; our simulator's BJT has neither, so we leave them out.)

### The small-signal recipe

To analyse an amplifier for small signals:

1. **Find the DC operating point** (lesson 06, or `.dc()`).
2. **Compute g_m, r_π, r_e** from I_C.
3. **Draw the small-signal circuit**: replace every DC voltage source by a short (its voltage doesn't *change*), every DC current source by an open, large capacitors by shorts (mid-band), and every transistor by its hybrid-π model.
4. **Solve the linear circuit** with Ohm, Kirchhoff, Thevenin, phasors.

Step 3's first rule surprises people: the 12 V supply becomes a wire to ground. It is not "turned off"; it simply does not vary, so it contributes no signal. That is superposition (Phase 05): the total response is the DC solution plus the small-signal solution.

### Worked example: the bypassed amplifier of lesson 06

Operating point (simulator): I_C = 1.4558 mA.

```
g_m  = 1.4558 mA / 25.852 mV = 56.31 mA/V
r_π  = 100 / 0.05631 = 1776 Ω
r_e  = 1 / g_m = 17.76 Ω
```

Small-signal circuit at mid-band (C_IN, C_E short; V_CC to ground):

```
   v_in ---+--------+------------ b
           |        |             |
        [R1 100k] [R2 10k]      [r_π 1776]       c ---+
           |        |             |                   |
         ground   ground        e = ground         [R_C 2.2k] --- ground
                                (C_E shorts R_E)      |
                                               (g_m v_be) c → e
```

Since the emitter is at small-signal ground, v_be = v_in. The current source pulls g_m v_in out of the collector node through R_C, so

```
v_c = −g_m × R_C × v_in   →   A_v = −0.05631 × 2200 = −123.9
```

### Model versus transistor

The script builds the hybrid-π model from plain resistors and a `vccs`, with the bypass and coupling capacitors kept, and runs the AC analysis of both circuits:

| Frequency | Real transistor | Linear model |
|---|---|---|
| 10 Hz | 39.23 | 39.23 |
| 100 Hz | 118.68 | 118.68 |
| 1 kHz | 123.83 | 123.83 |
| 10 kHz | 123.89 | 123.89 |

They agree perfectly, and that's no coincidence: the simulator's AC analysis does exactly what we did by hand: it finds the operating point, linearises each transistor there, and solves the linear circuit. At 10 Hz the gain drops because C_E's impedance (1/(2π × 10 × 470 µF) = 34 Ω) is no longer small compared with r_e = 17.8 Ω, and C_IN starts to matter too: the amplifier is a high-pass filter at low frequency (Phase 10).

### Input resistance

From the signal source, the bias resistors and r_π are all connected from the base to (small-signal) ground, in parallel:

```
R_in = R1 ∥ R2 ∥ r_π = 9091 ∥ 1776 = 1486 Ω
```

The simulator, dividing v_in by the AC current through C_IN: **1486 Ω**. A microphone with 600 Ω output resistance would lose 600/(600+1486) = 29 % of its signal in that divider. Degeneration (unbypassed R_E) raises R_in: looking into the base you then see r_π + (β+1) R_E, about 22 kΩ for lesson 06's design.

### Low-frequency corner of the input

C_IN and R_in form a high-pass filter with corner f = 1/(2π R_in C_IN) = 1/(2π × 1486 × 10 µF) = 10.7 Hz. That is part of why the gain fell at 10 Hz. To pass bass down to 20 Hz with margin, the corner should be a few hertz.

### How small is small? Measured distortion

The script runs transient simulations with growing input amplitudes and measures the second harmonic with a discrete Fourier sum (the same "multiply by a complex sine and add up" idea as phasors):

| Input | Output (p-p) | Gain | 2nd harmonic | Estimate v / (4 V_T) |
|---|---|---|---|---|
| 1 mV | 0.248 V | 124.0 | 0.96 % | 0.97 % |
| 3 mV | 0.742 V | 123.7 | 2.90 % | 2.90 % |
| 10 mV | 2.488 V | 124.4 | 9.62 % | 9.67 % |
| 20 mV | 5.036 V | 125.9 | 18.9 % | 19.3 % |

The simple formula predicts the distortion almost exactly. A sine with 10 % second harmonic looks visibly lopsided: the negative half of the collector swing (more current) is bigger than the positive half. The "gain" even appears to rise at 20 mV, because the measured peak-to-peak swing includes the distortion.

Lesson 06's degenerated stage handles large signals much better: with R_E unbypassed, most of the input appears across R_E (a linear resistor) and only a fraction (r_e/(R_E + r_e) ≈ 8 %) across the junction. This is negative feedback reducing distortion, in exchange for gain.

### Small-signal thinking everywhere

The same recipe applies to any nonlinear device:

| Device | Bias quantity | Small-signal parameter |
|---|---|---|
| Diode | I_D | r_d = n V_T / I_D (lesson 11-05) |
| BJT | I_C | g_m = I_C / V_T, r_π = β / g_m |
| MOSFET (saturation) | I_D, V_ov | g_m = k V_ov = 2 I_D / V_ov |
| LED, zener | I | dynamic resistance from datasheet |

A MOSFET biased at 1 mA with 0.2 V of overdrive has g_m = 2 × 1 mA / 0.2 V = 10 mA/V, a quarter of a BJT's 38.7 mA/V at the same current. That is the "g_m per milliamp" advantage of BJTs mentioned in lesson 04.

## Build It

### Step 1: Operating point and parameters

```python
collector, result = operating_point()
gm = collector / THERMAL_VOLTAGE
r_pi = BETA / gm
```

### Step 2: The hybrid-π circuit

```python
def small_signal_model(gm, r_pi):
    circuit = Circuit()
    circuit.sine_source("VIN", "in", "0", amplitude=1.0, freq=FREQ, offset=0.0)
    circuit.capacitor("CIN", "in", "b", 10e-6)
    circuit.resistor("R1", "b", "0", 100e3)
    circuit.resistor("R2", "b", "0", 10e3)
    circuit.resistor("RPI", "b", "e", r_pi)
    circuit.vccs("GM", "c", "e", "b", "e", gm)
    circuit.resistor("RC", "c", "0", 2200.0)
    circuit.resistor("RE", "e", "0", 200.0)
    circuit.capacitor("CE", "e", "0", 470e-6)
    return circuit
```

R1 and R_C go to ground instead of to +12 V: the supply is a small-signal ground. No transistor, no supply, only linear parts.

### Step 3: Compare and measure

`compare_models` runs `.ac(...)` on both circuits; `show_input_resistance` divides 1 V by the AC current through C_IN.

### Step 4: Distortion

```python
def harmonic_ratio(signal, time, freq, harmonic):
    window = time >= time[-1] - 4.0 / freq
    values = signal[window] - signal[window].mean()
    t = time[window]
    fundamental = abs(np.sum(values * np.exp(-2j * np.pi * freq * t)))
    other = abs(np.sum(values * np.exp(-2j * np.pi * harmonic * freq * t)))
    return other / fundamental
```

Over a whole number of periods, multiplying by e^(−j2πft) and summing picks out the component at frequency f, just as phasors do. The ratio of the 2f component to the f component is the second-harmonic distortion.

```
uv run python phases/12-transistors/07-small-signal-thinking/code/main.py
```

## Use It

- **Datasheets list small-signal parameters**: h_fe (small-signal β), h_ie (≈ r_π), h_oe (output conductance, 1/r_o), at a stated I_C. The "h-parameters" are an older cousin of the hybrid-π model.
- **SPICE's .AC analysis** (and ours) is exactly small-signal analysis: a DC solve, a linearisation, then phasors. It never tells you about clipping or distortion; for those you need a transient (.TRAN) run.
- **Distortion specs**: audio amplifiers quote THD (total harmonic distortion) such as 0.01 %. Getting there from a junction that gives 1 % per millivolt requires lots of negative feedback, which is what op-amps provide (Phase 13).
- **Mixers in radios** exploit the nonlinearity on purpose: the squared term turns two input frequencies into their sum and difference.
- **Sensors**: a strain gauge or thermocouple produces microvolts; the first amplifier stage is designed with small-signal analysis for gain and noise.

## Common Mistakes

- **Applying small-signal results to large signals.** A gain of 124 does not mean a 100 mV input gives 12.4 V out; it clips and distorts long before.
- **Forgetting that g_m depends on bias.** Change the current and every small-signal parameter changes with it.
- **Leaving the DC supply in the small-signal circuit.** It becomes a short to ground.
- **Mixing DC and AC quantities.** Uppercase with uppercase subscripts (I_C) for DC, lowercase (i_c) for signals. Total = DC + small signal.
- **Ignoring the capacitors' frequency dependence.** "Large capacitors are shorts" is only true above the corner frequencies.
- **Thinking r_π is a physical resistor.** It is the slope of the base-emitter curve at one operating point; measure it with an ohmmeter and you get nonsense.

## Exercises

1. Compute g_m, r_π and r_e for a BJT with β = 200 at I_C = 0.25 mA.
2. In the lesson's bypassed amplifier, what would the gain be if the bias current were doubled with the same R_C? What would happen to the DC collector voltage?
3. Find the input resistance of the *degenerated* (R_E unbypassed) amplifier of lesson 06 using r_π + (β + 1) R_E in parallel with R1 ∥ R2. Then check it by modifying the script (remove CE in `small_signal_model` and `full_amplifier`).
4. A MOSFET biased at I_D = 2 mA with V_ov = 0.4 V drives R_D = 5 kΩ (common source, source grounded for AC). What is its voltage gain?
5. What input amplitude gives 0.1 % second-harmonic distortion in the bypassed stage? Verify with the script.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Small signal | "AC analysis" | Linear behaviour for variations small enough that the device curve is straight |
| g_m | "Transconductance" | ΔI_C/ΔV_BE = I_C/V_T for a BJT; 2 I_D / V_ov for a MOSFET in saturation |
| r_π | "Input resistance of the transistor" | β / g_m, between base and emitter |
| r_e | "Emitter resistance" | ≈ 1/g_m, seen looking into the emitter |
| Hybrid-π | "The small-signal model" | r_π from b to e and a current source g_m v_be from c to e (plus r_o, capacitances when needed) |
| Mid-band | "Passband" | Frequencies where coupling and bypass capacitors are effectively shorts |
| HD2 | "Second-harmonic distortion" | About v_be / (4 V_T) for a bare junction |

## Further Reading

- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., section 2.3 (the Ebers-Moll model, g_m and r_e), 2.4 (amplifier building blocks) and 2.5 (negative feedback).
- MIT OpenCourseWare 6.002 *Circuits and Electronics*, lectures "Small signal model" and "Small signal circuits" (Agarwal and Lang). https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/
- A. Sedra and K. Smith, *Microelectronic Circuits*, chapter on BJT small-signal operation and models (the standard university treatment).
- *All About Circuits*, Volume III, chapter 4, "Biasing calculations" and "Input and output coupling". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-4/input-and-output-coupling/
