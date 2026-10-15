# RC Low-Pass and High-Pass

> Write the RC voltage divider with impedances and the whole filter falls out in one line: H = 1 / (1 + j f / fc).

**Type:** Build
**Prerequisites:** Phase 10 (Filters and Resonance), Lesson 01 (What a Filter Does); Phase 09 (Alternating Current), Lessons 04 (Complex Numbers for Circuits), 05 (Phasors) and 06 (Impedance); Phase 07 (Capacitors), Lesson 04 (The Time Constant)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Transfer function H(f) | The complex number that says what a circuit does to a sine at frequency f: its size is the gain, its angle the phase shift | A recipe card: "at 1 kHz, multiply by 0.85 and delay by 32 degrees" |
| Magnitude \|H\| | The size of H: output amplitude over input amplitude | How loud the note comes out |
| Phase shift | The angle of H: how far the output sine is shifted relative to the input, in degrees | How late the echo arrives, as a fraction of a cycle |
| First-order filter | A filter with one energy-storing part (one capacitor or one inductor) | The simplest possible filter: one RC |
| -3 dB point | Another name for the cutoff: the frequency where \|H\| = 0.707 (Lesson 03 explains the name) | The edge of the pass band |
| Roll-off | How fast the gain falls past the cutoff | How steep the slope of a hill is |
| E12 series | The standard set of 12 resistor values per decade (1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2) | Shoe sizes: you buy the nearest size, not the exact length of your foot |
| Loading | Changing a circuit's behaviour by connecting something to its output | Opening a second tap lowers the pressure at the first |
| Rise time | How long a step takes to go from 10 % to 90 % of its final value | How long a lamp on a dimmer takes to brighten |

## Learning Objectives

- Derive the transfer functions of the RC low-pass and high-pass from the voltage divider and complex impedances
- Calculate the magnitude and phase at any frequency, and explain why the phase is -45° (low-pass) or +45° (high-pass) at the cutoff
- Design an RC filter for a target cutoff with standard component values, and check it with our simulator
- Predict how a load resistor moves the cutoff, using Thevenin's theorem
- Connect the frequency view (fc) and the time view (tau, rise time) of the same RC circuit

## The Problem

In Lesson 01 you saw that an RC divider passes low frequencies and blocks high ones, and you used a formula for its gain that we promised to derive. That is not enough to design with. Real questions are: "I need a cutoff of 1 kHz and I have a 10 nF capacitor; which resistor?"; "my filter works on the bench but the cutoff moved when I connected the next stage, why?"; "this filter delays my signal; by how much?"; "my oscilloscope probe shows a slow rising edge; what is the bandwidth of the circuit?"

All of these are answered by treating the RC circuit with **complex impedances**, the tool you built in Phase 09. The derivation is short, and once you have it, you can analyse every first-order filter in electronics.

## The Physics

### What the capacitor does, in plain words

A capacitor's current is i = C dv/dt (Phase 07): it lets current through only while its voltage is changing, and the faster the change, the more current. For a sine of frequency f, the voltage changes faster the higher f is (the same amplitude in less time). So at high frequency, a small voltage across the capacitor is enough to pass a large current: the capacitor behaves like a small resistance. At low frequency it barely passes any current: a large resistance. At DC, after charging, none at all.

Phase 09 packed this into the capacitor's **impedance**:

```
Z_C = 1 / (j * 2 pi f * C) = -j / (2 pi f C)
```

Read it: "the impedance of a capacitor is one over j times two pi f times C". The size, 1 / (2 pi f C), is the opposition in ohms. The **j** (the square root of -1, Phase 09, Lesson 04) says that the capacitor's voltage lags its current by a quarter cycle (90 degrees). We often write omega = 2 pi f (the angular frequency, radians per second), so Z_C = 1 / (j omega C).

A resistor's impedance is just Z_R = R: no j, no frequency dependence, voltage and current in step.

### The low-pass as a divider of impedances

The voltage divider rule (Phase 04) works for impedances exactly as for resistances, because Kirchhoff's laws hold for phasors:

```
   V_in ---[ Z_R = R ]---+--- V_out
                         |
                     [ Z_C = 1/(j w C) ]
                         |
   0 V ------------------+

   V_out / V_in = Z_C / (Z_R + Z_C)
```

Put the impedances in and simplify (multiply top and bottom by j omega C):

```
H = (1 / (j w C)) / (R + 1 / (j w C)) = 1 / (1 + j w R C)
```

This is the **transfer function** of the RC low-pass. Using fc = 1 / (2 pi R C), the product omega R C = 2 pi f R C = f / fc, so

```
H(f) = 1 / (1 + j f / fc)
```

Read it: "H equals one over one plus j times f over fc". Everything about the filter is in this line.

### Magnitude and phase

A complex number a + jb has size sqrt(a² + b²) and angle atan(b / a) (Phase 09, Lesson 04). The denominator 1 + j f/fc has size sqrt(1 + (f/fc)²) and angle atan(f/fc). Dividing by a complex number divides by its size and *subtracts* its angle, so:

```
|H| = 1 / sqrt(1 + (f/fc)^2)         phase = -atan(f/fc)
```

| f | f/fc | \|H\| | Phase |
|---|---|---|---|
| fc / 10 | 0.1 | 0.995 | -5.7° |
| fc / 2 | 0.5 | 0.894 | -26.6° |
| fc | 1 | 0.707 | -45.0° |
| 2 fc | 2 | 0.447 | -63.4° |
| 10 fc | 10 | 0.0995 | -84.3° |

**Worked example at f = fc / 2.** H = 1 / (1 + 0.5j). Multiply top and bottom by the conjugate (1 - 0.5j): H = (1 - 0.5j) / (1 + 0.25) = 0.8 - 0.4j. Size: sqrt(0.64 + 0.16) = sqrt(0.8) = 0.894. Angle: atan(-0.4 / 0.8) = atan(-0.5) = -26.6°. You can check every line of the table this way; the code prints the real and imaginary parts too.

Three regions:

- **Far below fc**: |H| is about 1, phase about 0. The capacitor is nearly open; the output follows the input.
- **At fc**: |H| = 0.707 and the phase is exactly -45°. The resistor and the capacitor have equal-sized impedances, so the output is the capacitor's half of a right-angled triangle.
- **Far above fc**: |H| is about fc / f: double the frequency, half the output. The phase approaches -90°: the output lags by a quarter cycle. In Lesson 03 this "halves per octave, tenth per decade" behaviour becomes a straight line on a Bode plot.

**What the negative phase means physically.** The capacitor's voltage can only change by charging through R, which takes time; it lags behind the input. At low frequency the lag is a negligible fraction of a slow cycle; at high frequency the capacitor is still catching up when the input reverses, so the lag approaches a quarter of a cycle (and the amplitude it reaches shrinks).

### The high-pass

Swap the parts: capacitor in series, resistor to ground.

```
   V_in ---[ C ]---+--- V_out
                   |
                  [ R ]
                   |
   0 V ------------+

H = R / (R + 1/(j w C)) = j w R C / (1 + j w R C) = (j f/fc) / (1 + j f/fc)
```

```
|H| = (f/fc) / sqrt(1 + (f/fc)^2)       phase = 90° - atan(f/fc)
```

Now |H| is near 0 at low frequency (the capacitor blocks), 0.707 at fc with a phase of **+45°** (the output *leads* the input), and near 1 at high frequency with phase near 0. The cutoff is the same fc = 1 / (2 pi R C). Notice that low-pass H plus high-pass H equals exactly 1: the two outputs always add up to the input, because the resistor's and capacitor's voltages always add up to V_in (Kirchhoff's voltage law).

## The Concept

### Designing for a cutoff

Rearrange fc = 1 / (2 pi R C):

```
R = 1 / (2 pi fc C)          C = 1 / (2 pi fc R)
```

**Worked example.** Target fc = 1 kHz with C = 10 nF: R = 1 / (2 x 3.1416 x 1000 x 1e-8) = 1 / 6.283e-5 = 15,915 ohm. Resistors are sold in standard values; the nearest in the E12 series (Phase 03) is 15 k ohm, giving fc = 1 / (2 pi x 15,000 x 1e-8) = 1061 Hz. That is 6 % high, usually fine: the capacitor's own tolerance is often ±10 % (Phase 07, Lesson 07).

**How to choose the pair.** Many (R, C) pairs give the same fc. Practical rules:

- Keep R between about 1 k ohm and 100 k ohm. Smaller R draws a lot of current from the source; larger R picks up noise and is sensitive to loading.
- Prefer capacitor values that come in good, stable types (C0G/NP0 ceramics up to a few nF, film capacitors for larger values in audio).

### Loading: the next stage is part of the filter

Connect a load resistor R_L across the low-pass output. Now the capacitor has R_L in parallel. Use Thevenin's theorem (Phase 05, Lesson 06) on the source plus R plus R_L, seen from the capacitor:

- Thevenin voltage: V_in x R_L / (R + R_L), so the gain at DC drops from 1 to R_L / (R + R_L).
- Thevenin resistance: R in parallel with R_L = R R_L / (R + R_L), smaller than R.
- The capacitor now charges through that smaller resistance, so the **cutoff moves up**: fc = 1 / (2 pi (R || R_L) C).

**Worked example.** R = 1 k, C = 100 nF, R_L = 1 k. DC gain = 1000 / 2000 = 0.5. R || R_L = 500 ohm. fc = 1 / (2 pi x 500 x 1e-7) = 3183 Hz, twice the unloaded value. With R_L = 100 k the effect is only 1 %: a rule of thumb is that **the load should be at least 10 times larger than R** (preferably 100). When it cannot be, put a buffer (an op-amp follower, Phase 13) between stages.

### Time view and frequency view

The same RC circuit has a time constant tau = R C (Phase 07) and a cutoff fc = 1 / (2 pi tau). They are two descriptions of the same thing:

- A circuit that takes a long time to respond (big tau) cannot follow fast wiggles (low fc).
- When you feed it a step, the output rises along 1 - e^(-t/tau). It reaches 10 % when e^(-t/tau) = 0.9, at t = 0.105 tau, and 90 % when e^(-t/tau) = 0.1, at t = 2.303 tau. The 10-90 % **rise time** is the difference, t_r = tau x ln(9) = 2.2 tau, which in frequency terms is

```
t_r = 2.2 tau = 2.2 / (2 pi fc) = 0.35 / fc
```

"rise time is about 0.35 divided by the bandwidth". This rule appears on every oscilloscope datasheet: a 100 MHz scope cannot show edges faster than about 3.5 ns.

**Worked example.** R = 1 k, C = 100 nF: tau = 100 µs, fc = 1592 Hz, rise time 220 µs.

## Build It

### Step 1: The transfer function from impedances

```python
def low_pass_response(freq, resistance, capacitance):
    z_c = 1 / (1j * 2 * math.pi * freq * capacitance)
    return z_c / (resistance + z_c)


def high_pass_response(freq, resistance, capacitance):
    z_c = 1 / (1j * 2 * math.pi * freq * capacitance)
    return resistance / (resistance + z_c)
```

These are literally the voltage divider with Python's complex numbers (`1j` is j). `cmath.polar(h)` gives the size and angle. Output for R = 1 k, C = 100 nF:

```
  f =    795.8 Hz: H = +0.8000 -0.4000j, |H| = 0.8944, phase =  -26.6 deg
  f =   1591.5 Hz: H = +0.5000 -0.5000j, |H| = 0.7071, phase =  -45.0 deg
  f =  15915.5 Hz: H = +0.0099 -0.0990j, |H| = 0.0995, phase =  -84.3 deg
```

At fc, H = 0.5 - 0.5j exactly: equal real and imaginary parts, an angle of -45°.

### Step 2: Compare with the simulator

```python
def rc_circuit(kind, resistance, capacitance, load=None):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    if kind == "low":
        c.resistor("R1", "in", "out", resistance)
        c.capacitor("C1", "out", "0", capacitance)
    else:
        c.capacitor("C1", "in", "out", capacitance)
        c.resistor("R1", "out", "0", resistance)
    if load:
        c.resistor("Rload", "out", "0", load)
    return c


freqs = np.logspace(1, 6, 501)
sweep = rc_circuit("low", r, cap).ac(freqs, source="V1")
```

`np.logspace(1, 6, 501)` makes 501 frequencies spread evenly on a logarithmic scale from 10^1 = 10 Hz to 10^6 = 1 MHz (100 points per factor of ten). The simulator solves the circuit at each one. Its AC analysis always drives the chosen source with a 1 V sine, so the output voltage *is* H. `sweep.cutoff("out")` searches for the frequency where the gain has fallen 3 dB (to 0.707) below its maximum:

```
  largest difference in |H| over 10 Hz .. 1 MHz: 1.00e-09
  cutoff found by the simulator: 1591.5 Hz (formula 1591.5 Hz)
  phase at fc: -45.0 deg
```

### Step 3: The high-pass

The same check for the swapped circuit: |H| = 0.0995 at fc/10 with +84.3°, 0.7071 at fc with +45.0°, 0.9950 at 10 fc with +5.7°, and the simulator's cutoff at 1591.6 Hz (the tiny difference is the search interpolating between sweep points).

### Step 4: Design with standard values

```python
def nearest_e12(value):
    decade = 10 ** math.floor(math.log10(value))
    candidates = [m * decade for m in E12] + [10 * decade]
    return min(candidates, key=lambda r: abs(math.log(r / value)))
```

It picks the E12 value with the smallest *ratio* error (comparing logarithms, so 10 % high and 10 % low count the same). Output: exact 15,915 ohm, nearest 15,000 ohm, fc = 1061 Hz, confirmed by the simulator.

### Step 5: Loading

```
  no load   : DC gain 1.000, cutoff  1591.5 Hz
  100 k load: DC gain 0.990, cutoff  1607.4 Hz
  10 k load : DC gain 0.909, cutoff  1750.7 Hz
  1 k load  : DC gain 0.500, cutoff  3183.0 Hz
```

Check the 10 k line: DC gain 10 / 11 = 0.909; R || R_L = 1000 x 10000 / 11000 = 909 ohm; fc = 1 / (2 pi x 909 x 1e-7) = 1751 Hz.

### Step 6: Rise time

We drive the low-pass with a 0 to 1 V step (a pulse source with a long period) and measure the time between 10 % and 90 %:

```python
def rise_time_10_90(t, v, final):
    t10 = t[np.argmax(v >= 0.1 * final)]
    t90 = t[np.argmax(v >= 0.9 * final)]
    return t90 - t10
```

`np.argmax` on a true/false array returns the index of the first `True`: the first sample at or above the level. Output: 219.7 µs, against 2.2 tau = 220.0 µs and 0.35 / fc = 219.9 µs.

## Use It

- **Anti-aliasing before an ADC.** A microcontroller sampling at 10 kHz needs frequencies above 5 kHz removed. A first-order RC with fc = 1 to 2 kHz is often the first line of defence, with R = 1 k to 10 k and a C0G capacitor (Phase 19).
- **PWM to analog.** A PWM pin (Phase 17) switching at 20 kHz, followed by an RC low-pass with fc = 200 Hz, gives a smooth voltage proportional to the duty cycle, with the 20 kHz ripple cut by a factor of 100.
- **Audio coupling capacitors** form high-pass filters with the next stage's input resistance. A guitar pedal with 1 M ohm input and a 22 nF coupling capacitor: fc = 7 Hz.
- **Oscilloscope bandwidth.** A scope's front end behaves roughly like a low-pass; datasheets quote bandwidth and rise time related by t_r ≈ 0.35 / BW (Phase 06).
- **Debouncing buttons.** A 10 k resistor and 100 nF capacitor (tau = 1 ms, fc = 159 Hz) filter the fast bouncing of a mechanical switch before a logic input.

## Try It in the Lab

Open **"Put the cutoff near 1 kHz"**. A 10 nF capacitor goes from the output to ground; choose the series resistor so that the cutoff lands between 900 Hz and 1.2 kHz and 100 Hz still passes almost untouched. Compute the exact R first, then look at the drawer: four standard values, each roughly a factor of 3 apart. Which is closest in *ratio*? Predict the cutoff for each before running, and notice that the biggest resistor fails both goals.

## Common Mistakes

- **Forgetting the 2 pi.** fc = 1 / (2 pi R C), not 1 / (R C). The second is the angular cutoff in rad/s, 6.28 times bigger.
- **Treating impedances as plain numbers.** R + Z_C is not R + 1/(2 pi f C): the capacitor's part is imaginary. At fc, |R + Z_C| is sqrt(2) x R, not 2R.
- **Ignoring the load.** A filter measured with nothing connected changes as soon as it drives the next stage.
- **Expecting the phase to be zero in the pass band near fc.** Already at fc/2 the low-pass delays the signal by 26.6°. In control loops and audio crossovers, that phase matters.
- **Mixing up which side leads.** Low-pass output *lags* (negative phase), high-pass output *leads* (positive phase).

## Exercises

1. **Easy.** A low-pass has R = 2.2 k and C = 47 nF. Find fc, and |H| and the phase at 500 Hz and 5 kHz.
2. **Easy.** Design a high-pass with fc = 20 Hz using C = 1 µF. Which E12 resistor would you pick, and what is the real cutoff?
3. **Medium.** Show by hand that at f = 2 fc the low-pass gives H = 0.2 - 0.4j. (Multiply by the conjugate.)
4. **Medium.** A low-pass (R = 10 k, C = 10 nF) feeds an amplifier input of 47 k ohm. Find the DC gain and the new cutoff. Check with `rc_circuit("low", 10e3, 10e-9, 47e3)`.
5. **Hard.** Add the low-pass and high-pass H at the same frequency and show the sum is exactly 1 for every f. Then explain this result using Kirchhoff's voltage law around the loop, without any algebra.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Transfer function | "The filter's formula" | H(f) = V_out / V_in as a complex number at each frequency |
| RC low-pass | "Simple filter" | H = 1 / (1 + j f/fc); \|H\| = 1/sqrt(1 + (f/fc)²), phase -atan(f/fc) |
| RC high-pass | "Blocking capacitor" | H = (j f/fc) / (1 + j f/fc); passes above fc, phase +90° to 0 |
| Cutoff frequency | "Corner frequency", "-3 dB point" | fc = 1 / (2 pi R C), where \|H\| = 0.707 and the phase is ∓45° |
| Loading | "The next stage pulls it down" | A load in parallel with the output lowers the gain and changes fc to 1 / (2 pi (R \|\| R_L) C) |
| Rise time | "How fast the edge is" | 10 % to 90 % time of a step response; t_r = 2.2 RC = 0.35 / fc |

## Further Reading

- [All About Circuits, Volume II, Chapter 8: Low-pass and high-pass filters](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-8/low-pass-filters/) — RC filters with worked numbers
- [The Art of Electronics (Horowitz & Hill), 3rd edition, sections 1.7 (impedance and reactance) and RC filters](https://artofelectronics.net/) — impedance-based design of first-order filters
- [MIT OpenCourseWare 6.002, lectures on sinusoidal steady state and filters](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) — the impedance method and frequency response
- [Tektronix: "ABCs of Probes" primer](https://www.tek.com/en/documents/whitepaper/abcs-probes-primer) — where the 0.35 / bandwidth rise-time rule is used every day
