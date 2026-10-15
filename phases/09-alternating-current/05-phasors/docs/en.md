# Phasors

> Freeze the spinning arrow. Its length is the amplitude, its angle is the phase, and every sine wave of the same frequency becomes one complex number you can add, multiply and solve for.

**Type:** Build
**Prerequisites:** Phase 07 (Capacitors), Lesson 02 (Capacitance); Phase 08 (Magnetism and Inductors), Lesson 04 (The Inductor); Phase 09, Lessons 02 (Sine Waves, Frequency and Phase) and 04 (Complex Numbers for Circuits)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Phasor | A complex number that stands for a whole sine wave of a known frequency: size = amplitude, angle = phase | A photograph of the Ferris wheel taken at time zero: it tells you where every seat will be at any later moment |
| Phasor diagram | A drawing of several phasors as arrows from the same origin | A sketch of the clock hands, all frozen at one instant |
| Time domain | Describing a signal as a value at each instant, v(t) | A video of the wave |
| Phasor domain (frequency domain) | Describing a sine wave by its phasor only | A single still photo plus the knowledge of how fast it spins |
| Derivative | How fast something is changing at an instant, in units per second | The speedometer of a car (rate of change of position) |
| Leading by 90 degrees | Reaching each peak a quarter cycle earlier | A runner a quarter-lap ahead on a circular track |
| Quadrature | Two waves 90 degrees apart | The left and right pedals of a bicycle seen from the side: one is at the top when the other is at the front |
| Steady state | The repeating behaviour a circuit settles into after start-up effects have died out | A washing machine after it reaches spin speed |
| KVL with phasors | Kirchhoff's voltage law applied to phasors: they add to zero around a loop as arrows, not as sizes | Walking round a city block: you return to the start, even though you walked in several directions |

## Learning Objectives

- Write any sine wave of a known frequency as a phasor, and recover the sine wave from the phasor.
- Add sine waves of the same frequency by adding their phasors, and explain why amplitudes do not simply add.
- Show that taking a derivative of a sine wave is the same as multiplying its phasor by j omega.
- Derive the phasor laws of the capacitor (I = j omega C V) and the inductor (V = j omega L I) from their physics.
- Solve a series RC circuit with phasors by hand and confirm it with the simulator's AC analysis.

## The Problem

Two sine waves of the same frequency arrive at a point: 3 V of amplitude in one, 4 V in the other, the second one a quarter cycle ahead. What is the amplitude of their sum? Not 7 V. Not 1 V either. You could find it by sampling both waves at a thousand instants and adding, but that would be slow, and you would have to do it again for every new case.

Things get worse with capacitors. Phase 07 told you that a capacitor's current is C times the rate of change of its voltage, i = C x dv/dt. In a circuit with resistors and capacitors driven by a sine, every Kirchhoff equation mixes values and rates of change: these are **differential equations**, the topic of whole university courses. Lesson 07-08 solved them by stepping through time.

Phasors make all of this disappear. Once each sine wave is a complex number, adding waves is adding complex numbers, and taking a rate of change is multiplying by j omega. A differential equation becomes an ordinary algebra equation, the kind you solved in Phase 05. That trick is the backbone of all AC circuit work.

## The Physics

### Every wave spins at the same speed

In Lesson 04 (Step 11) you saw that A sin(omega t + phi) is the height of an arrow of length A spinning at omega radians per second, starting at angle phi:

```
A sin(omega t + phi) = imaginary part of [ A e^(j phi) x e^(j omega t) ]
```

Read it: "the sine wave is the vertical part of the fixed complex number A e^(j phi), turned by the spinning factor e^(j omega t)".

Here is the key physical fact: in a circuit of resistors, capacitors and inductors driven at one frequency, after the start-up has died away (the **steady state**), every voltage and current is a sine wave at **that same frequency** (Lesson 02). All their arrows spin together, like the hands of a clock all glued to the same motor. Their **relative** positions never change. So we can forget about the spinning factor e^(j omega t), which is common to everyone, and keep only the fixed part, the arrow frozen at t = 0:

```
phasor V = A e^(j phi) = A at angle phi
```

That is a **phasor**. To get the real wave back, put the spinning factor back and take the vertical (imaginary) part.

A word on conventions: many textbooks use cosines and take the horizontal (real) part instead. Both work if you are consistent. We use sines, because the sources in our simulator are sines: `sine_source` with phase 0 is the phasor 1 at 0 degrees.

### Where phasors stop working

Phasors only describe **sine waves of one frequency in steady state**. They do not describe the start-up transient (use the time simulation of Phase 07, Lesson 08), and they do not directly describe square waves or two different frequencies at once (for those you break the signal into sines, one phasor calculation per frequency). Nonlinear parts like diodes (Phase 11) break the rule entirely, because they create new frequencies.

## The Concept

### From wave to phasor and back

| Sine wave | Phasor (polar) | Phasor (rectangular) |
|---|---|---|
| 10 sin(omega t) | 10 at 0 deg | 10 + 0j |
| 5 sin(omega t + 90 deg) | 5 at 90 deg | 0 + 5j |
| 2 sin(omega t - 30 deg) | 2 at -30 deg | 2 cos(-30) + 2j sin(-30) = 1.732 - 1j |
| -4 sin(omega t) | 4 at 180 deg | -4 + 0j |

Going back: the phasor 3 + 4j has size 5 and angle 53.13 degrees, so it stands for 5 sin(omega t + 53.13 deg). The phasor does not record the frequency; you have to remember it separately (it is the same for the whole circuit).

### Adding waves = adding arrows

Add v1 = 3 sin(omega t) and v2 = 4 sin(omega t + 90 deg).

1. Phasors: V1 = 3 + 0j, V2 = 0 + 4j.
2. Add: V1 + V2 = 3 + 4j.
3. Convert: size sqrt(9 + 16) = 5, angle atan2(4, 3) = 53.13 degrees.
4. Result: v1 + v2 = 5 sin(omega t + 53.13 deg).

```
 imaginary
    ^
  4 +- - - - - * V1 + V2 = 5 at 53.13 deg
    |        / |
    |  V2  /   | V2 (moved to the tip of V1)
    |    /     |
    |  /       |
  0 +--------->+----> real
    0   V1     3
```

Why does it work? Because "taking the imaginary part" and "adding" can be done in either order: the vertical part of a sum of arrows is the sum of their vertical parts. And since both arrows spin together, the sum spins with them.

Why not 7 V? The two waves peak at different times: when v2 is at its +4 V peak, v1 is crossing zero, and when v1 is at its peak, v2 is crossing zero. They never reach their peaks together, so the sum peaks at 5 V, in between. Only waves **in phase** (same angle) add their amplitudes directly; waves in antiphase (180 degrees apart) subtract.

### Rate of change = multiply by j omega

The **derivative** of a signal, written dv/dt, is how fast it changes at each instant, in volts per second. (Phase 07 used it for the capacitor: i = C dv/dt.) For a sine wave, look at the spinning arrow. The tip moves around a circle of radius A at angular speed omega, so the tip's speed is omega x A, and its direction of motion is always **at right angles** to the arrow, a quarter turn ahead (anticlockwise). The rate of change of the height is the vertical part of that velocity. So:

```
the derivative of A sin(omega t + phi)  =  omega A sin(omega t + phi + 90 deg)
```

Read it: "the rate of change of a sine wave is another sine wave, omega times bigger and 90 degrees ahead". In phasors: multiply the size by omega and add 90 degrees to the angle. From Lesson 04, multiplying by j adds 90 degrees, so:

```
phasor of dv/dt = j omega V
```

This is the central trick. Worked example: v = 10 sin(2 pi 50 t). omega = 314.16 rad/s, so dv/dt has phasor j x 314.16 x 10 = 3141.6 at 90 degrees: the wave changes at up to 3,141.6 V per second, fastest as it crosses zero (where the "a quarter ahead" cosine peaks), and has zero slope at its peaks.

```
 v(t)      _                     dv/dt        _
         /   \                              /   \
  ------/-----\-----/----       -----\----/-----\----
               \__/                   \__/
     slope is biggest at the zero crossing -> dv/dt peaks there
```

### The capacitor in phasor language

From Phase 07: the charge on a capacitor is q = C x v, and current is the rate of change of charge, so i = C x dv/dt. Read: "the current into a capacitor equals the capacitance times the rate of change of its voltage". Translate with the trick:

```
I = C x (j omega V) = j omega C V
```

Two facts drop out:

- **Size:** the current amplitude is omega x C x (voltage amplitude). For C = 1 microfarad (1e-6 F) at 50 Hz with 10 V amplitude: 314.16 x 1e-6 x 10 = 0.0031416 A = 3.1416 mA. Double the frequency and the current doubles: a capacitor passes more current at higher frequencies.
- **Phase:** the factor j means the current **leads** the voltage by 90 degrees. Physically: the current is biggest when the voltage is changing fastest (crossing zero), and zero at the voltage peak, when the capacitor is momentarily neither charging nor discharging.

### The inductor in phasor language

From Phase 08, Lesson 04: an inductor's voltage is L times the rate of change of its current, v = L x di/dt. Read: "the voltage across an inductor equals the inductance times the rate of change of its current". Translate:

```
V = j omega L I
```

- **Size:** voltage amplitude = omega x L x (current amplitude). For L = 100 mH (0.1 H) carrying 0.2 A amplitude at 50 Hz: 314.16 x 0.1 x 0.2 = 6.283 V.
- **Phase:** the voltage **leads** the current by 90 degrees (equivalently, the current lags the voltage). A mnemonic many engineers use: **ELI the ICE man**. In an inductor (L), voltage E comes before current I; in a capacitor (C), current I comes before voltage E.

### Kirchhoff's laws still hold, with arrows

At every instant, the voltages around a loop add to zero and the currents into a node add to zero (Phase 04). Since every wave is the vertical part of its spinning phasor, and that is true at every instant, the **phasors** also add to zero around loops and at nodes. Kirchhoff's laws work for phasors exactly as for DC numbers, as long as you add them as complex numbers.

### Worked example: series R and C at 1 kHz

The circuit of Lesson 02:

```
              R = 1000 ohm
   in o-------/\/\/\-------o out
     (~) 1 V at 0 deg      |
     f = 1 kHz            === C = 159.15 nF
      |                    |
    0 o--------------------o
```

Let I be the phasor of the loop current. Then:

- The resistor obeys Ohm's law at every instant, so V_R = R x I (same phase as the current).
- The capacitor: I = j omega C V_C, so V_C = I / (j omega C).
- KVL around the loop: V_source = V_R + V_C.

Numbers: omega = 2 pi x 1000 = 6,283.2 rad/s. omega C = 6,283.2 x 159.15e-9 = 0.0010000. So 1 / (j omega C) = 1 / (j x 0.001) = -1000j ohm (using 1 / j = -j from Lesson 04).

KVL: 1 = 1000 I + (-1000j) I = (1000 - 1000j) I. So

```
I = 1 / (1000 - 1000j)
  = (1000 + 1000j) / (1000^2 + 1000^2)        (multiply by the conjugate)
  = (1000 + 1000j) / 2,000,000
  = 0.0005 + 0.0005j A  =  0.7071 mA at +45 deg
```

Then:

- V_R = 1000 x I = 0.5 + 0.5j V = 0.7071 V at +45 degrees.
- V_C = -1000j x (0.0005 + 0.0005j) = -0.5j - 0.5j^2 = 0.5 - 0.5j V = 0.7071 V at -45 degrees.
- Check: V_R + V_C = 1 + 0j. KVL holds.

V_C = 0.7071 V at -45 degrees is exactly what Lesson 02 measured by simulating ten cycles: the output is 0.7071 times the input and 45 degrees late.

### The surprise: 0.7071 + 0.7071 = 1

A voltmeter across the resistor reads 0.7071 V peak (0.5 V RMS), across the capacitor also 0.7071 V peak, and across the source 1 V peak. The two parts "add up" to 1.414 V, more than the source! There is no contradiction: the two voltages are 90 degrees apart, so they never peak at the same moment. They add as the two short sides of a right triangle, and the hypotenuse is sqrt(0.7071^2 + 0.7071^2) = 1.

```
 imaginary
    ^
0.5 +     * V_R = 0.7071 at +45 deg
    |   /   \
    | /       \  (V_C drawn from the tip of V_R)
  0 +-----------* source = 1 at 0 deg ---> real
    | \       /
    |   \   /
-0.5+     * V_C = 0.7071 at -45 deg
```

This is the most common surprise for people meeting AC for the first time. Remember the picture: voltages in AC circuits add as arrows.

## Build It

### Step 1: Phasors and waves

```python
def phasor(amplitude, phase_deg):
    return cmath.rect(amplitude, math.radians(phase_deg))


def wave(p, freq, t):
    return np.imag(p * np.exp(1j * 2 * np.pi * freq * t))
```

`phasor` freezes the arrow: size `amplitude`, angle `phase_deg`. `wave` unfreezes it: multiply by the spinning factor e^(j omega t) and take the imaginary part, sample by sample. The script adds 3 sin(wt) and 4 sin(wt + 90) both ways, by phasors (5 V at 53.13 deg) and by sampling and adding, and shows they differ by less than 1e-14 V: rounding error only. The sampled sum peaks at 5.0000 V.

### Step 2: Measuring a phasor from samples

```python
def fit_phasor(time, signal, freq):
    omega = 2 * np.pi * freq
    basis = np.column_stack([np.sin(omega * time), np.cos(omega * time)])
    (a_sin, a_cos), *_ = np.linalg.lstsq(basis, signal, rcond=None)
    return complex(a_sin, a_cos)
```

Any sine of frequency f can be written as a_sin x sin(omega t) + a_cos x cos(omega t). (Because A sin(omega t + phi) = A cos(phi) sin(omega t) + A sin(phi) cos(omega t), by the angle-addition rule.) Comparing with the phasor A at phi = A cos(phi) + j A sin(phi), the phasor is a_sin + j a_cos. `np.linalg.lstsq` finds the a_sin and a_cos that best fit the samples ("least squares": the smallest total squared error). This is how a lab instrument called a lock-in amplifier measures phasors.

We use it to check the derivative rule: `np.gradient` computes the slope of 10 sin(2 pi 50 t) numerically, and its fitted phasor is about 3142 V/s at 90.00 deg, equal to j omega V.

### Step 3: The capacitor in the simulator

```python
c = Circuit()
c.sine_source("V1", "a", "0", amplitude=10.0, freq=freq)
c.capacitor("C1", "a", "0", cap)
tr = c.transient(t_stop=0.04, dt=1e-5)
keep = tr.time >= 0.02
simulated = fit_phasor(tr.time[keep], tr.i("C1")[keep], freq)
```

A 10 V, 50 Hz sine directly across 1 microfarad, simulated in time for two cycles. Fitting the second cycle's current gives about 3.1416 mA at 90 deg, matching j omega C V. The current leads by a quarter cycle.

### Step 4: The inductor

V = j omega L I for 100 mH carrying 0.2 A: the script prints 6.283 V at 90 deg.

### Step 5: The series RC circuit, by hand and by simulator

```python
source = phasor(1.0, 0.0)
cap_factor = 1 / (1j * w_rc * c_farads)
i_loop = source / (r_ohms + cap_factor)
v_r = r_ohms * i_loop
v_c = cap_factor * i_loop
```

These five lines are the worked example. They print I = 0.7071 mA at 45 deg, V_R = 0.5 + 0.5j V, V_C = 0.5 - 0.5j V, V_R + V_C = 1 + 0j V and |V_R| + |V_C| = 1.4142 V. Then we ask the simulator's AC analysis (`rc.ac([f_rc], source="V1")`), which returns V_C = V(out) and V_R = V(in) - V(out) as complex numbers. They agree to four decimals. The plot `out.png` shows the phasor diagram on the left and the three waves on the right.

## Use It

- **Power engineering.** Grid engineers draw phasor diagrams of the three phases of the grid, 120 degrees apart, and of voltage drops along lines. Devices called phasor measurement units (PMUs), synchronised by GPS, measure grid phasors across a continent many times a second.
- **Lock-in amplifiers.** Lab instruments that pull a tiny signal out of noise by fitting it to sin and cos at a known frequency, exactly like `fit_phasor`.
- **Audio.** Two speakers playing the same tone add as phasors at your ear: in phase they reinforce, in antiphase they cancel. Noise-cancelling headphones exploit the antiphase case.
- **Every AC calculation from now on.** Lesson 06 (impedance), Lesson 07 (power), and all of Phase 10 (filters) are phasor calculations.

## Try It in the Lab

The lab task "Two voltages that add to more than the source" fixes a 1 kOhm resistor in series with a capacitor slot, driven by a 1 V, 1 kHz sine. Your goal is to make the capacitor voltage about 0.71 of the source (between -3.5 dB and -2.5 dB; Phase 10 explains decibels, for now just know that -3 dB means "0.707 times"). When that happens, the resistor and the capacitor share the source equally in size, and each "has" about 0.71 V. Think about what capacitor value makes the capacitor factor 1 / (omega C) equal to the resistance at 1 kHz, and what happens with a capacitor that is too big or too small.

## Common Mistakes

- **Adding amplitudes instead of phasors.** 3 V and 4 V waves a quarter cycle apart add to 5 V, not 7 V.
- **Adding phasors of different frequencies.** A phasor makes sense only together with its frequency; a 50 Hz phasor and a 60 Hz phasor cannot be added.
- **Forgetting the j in the capacitor law.** I = omega C V gives the right size but the wrong phase; I = j omega C V gives both.
- **Using phasors for the start-up.** Phasors describe the steady state. Right after switching on, a transient is superimposed; use the time simulation.
- **Mixing conventions.** Sine-based and cosine-based phasors differ by 90 degrees in absolute angle. Pick one and stick to it; relative angles between quantities are the same either way.
- **Putting the frequency in the wrong unit.** omega is 2 pi f, in rad/s. At 1 kHz, omega = 6,283 rad/s, not 1,000.

## Exercises

1. **To phasors.** Write the phasors of 6 sin(omega t + 30 deg) and 8 sin(omega t - 60 deg) in rectangular form. Add them and give the sum as a sine wave.
2. **Antiphase.** Add 5 sin(omega t) and 3 sin(omega t + 180 deg) with phasors. Explain the answer without phasors.
3. **Capacitor current.** A 10 nF capacitor has 2 V amplitude across it at 10 kHz. Find the current amplitude and its phase relative to the voltage.
4. **Inductor voltage.** A 22 mH inductor carries 50 mA amplitude at 1 kHz. Find the voltage amplitude and its phase relative to the current.
5. **Series RL.** A 1 V, 1 kHz source drives R = 100 ohm in series with L = 15.9 mH. Using V_L = j omega L I and KVL, find I, V_R and V_L as phasors. Then build the circuit in the simulator (`c.inductor`) and check with `ac()`.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Phasor | "The complex voltage" | A complex number A e^(j phi) representing A sin(omega t + phi) at a known frequency |
| Phasor diagram | "The arrow picture" | Phasors drawn from a common origin, showing sizes and relative phases |
| j omega | "The derivative in AC" | Multiplying a phasor by j omega is the same as taking the time derivative of its wave |
| I = j omega C V | "Capacitor current leads" | Capacitor law in phasor form; current is omega C times the voltage and 90 degrees ahead |
| V = j omega L I | "Inductor voltage leads" | Inductor law in phasor form; voltage is omega L times the current and 90 degrees ahead |
| Steady state | "After it settles" | The pure sine-wave behaviour that remains once start-up transients have decayed |
| ELI the ICE man | "The mnemonic" | Voltage (E) leads current (I) in an inductor (L); current leads voltage in a capacitor (C) |

## Further Reading

- [All About Circuits, Vol. II (AC), Chapter 2: Phasors and complex numbers in AC circuits](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-2/vectors-and-ac-waveforms/) — phasors as vectors, with many diagrams.
- *The Art of Electronics*, Horowitz & Hill, 3rd ed., Chapter 1.7 (Impedance and reactance) — the compact engineer's version of the phasor method, including the "generalized Ohm's law".
- [MIT OpenCourseWare 6.002, Lecture on sinusoidal steady state](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) — how the differential equations become algebra.
- [Khan Academy: AC analysis, phasors](https://www.khanacademy.org/science/electrical-engineering/ee-circuit-analysis-topic/ee-ac-analysis/v/ee-ac-analysis-intro1) — short videos building the same idea step by step.
