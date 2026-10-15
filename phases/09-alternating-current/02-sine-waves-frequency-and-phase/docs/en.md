# Sine Waves, Frequency and Phase

> A sine wave is the shadow of a spinning arrow. Three numbers describe it completely: how long the arrow is, how fast it spins, and where it started.

**Type:** Learn
**Prerequisites:** Phase 06 (Sources, Batteries and Measurement), Lesson 06 (The Oscilloscope); Phase 07 (Capacitors), Lesson 04 (The Time Constant); Phase 09, Lesson 01 (Why Alternating Current)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Sine wave | The smooth, endlessly repeating up-and-down curve that AC voltages follow | The height of a seat on a Ferris wheel as the wheel turns |
| Instantaneous value | The value of the voltage at one exact instant | One single frame of a video |
| Amplitude (peak) | The biggest value the wave reaches, measured from the middle line | How high the Ferris wheel seat gets above the hub |
| Peak-to-peak | Distance from the lowest point to the highest point: twice the amplitude | Top of the wheel to the bottom of the wheel |
| Offset | A constant value added to the whole wave, shifting it up or down | Building the whole Ferris wheel on a hill |
| Angle | How far round the circle you have turned | The hour hand's position on a clock face |
| Degree | 1/360 of a full turn | One of 360 equal slices of a pizza |
| Radian | The angle at which the arc you walked equals the radius; a full turn is 2 pi radians (about 6.283) | Walking round a circular track and measuring the distance in "track radii" |
| Angular frequency (omega, ω) | How fast the angle grows, in radians per second: 2 x pi x f | Revolutions per minute of an engine, but in radians per second |
| Phase | Where in its cycle a wave is at time zero, as an angle | Which seat of the Ferris wheel was at the bottom when you started the stopwatch |
| Phase shift | The difference in phase between two waves of the same frequency | Two runners on the same circular track, one a quarter-lap ahead |
| Lead / lag | The wave that reaches its peak first "leads"; the other "lags" | The runner ahead leads, the one behind lags |
| In phase | Two waves that peak at exactly the same moments | Two soldiers marching in step |

## Learning Objectives

- Describe a sine wave with its amplitude, frequency (or period) and phase, and write it as v(t) = A sin(2 pi f t + phi).
- Convert between degrees and radians, and between frequency, period and angular frequency.
- Compute the instantaneous value of a sine wave at a given time, by hand.
- Measure frequency and phase difference from sampled data using zero crossings.
- Explain why a resistor-capacitor circuit driven by a sine wave produces a sine wave of the same frequency but smaller and delayed.

## The Problem

You connect an oscilloscope (Phase 06, Lesson 06) to the output of a small 12 V AC transformer and to the voltage across a capacitor somewhere in the circuit. Two wavy lines appear on the screen. Your colleague asks: "what's the amplitude, what's the frequency, and how far is the second one behind the first?" To answer, you need a precise vocabulary for waves, and a formula you can plug numbers into.

That formula is also the foundation of the rest of this phase. RMS values (Lesson 03), phasors (Lesson 05), impedance (Lesson 06) and AC power (Lesson 07) are all built on the description of a sine wave by three numbers. Get those three numbers solid and the rest falls into place.

## The Physics

### Where the sine shape comes from

In Phase 08, Lesson 07, you met the generator: a coil spinning at a steady speed in a magnetic field. Look at one side of the coil from the end of the shaft. It goes round in a circle. The voltage it produces depends on how fast it cuts across the field, and that turns out to be proportional to the **height** of a point going round a circle, measured at each instant.

Draw a circle of radius A. Put an arrow from the centre to the edge and let it spin anticlockwise at a constant speed. At every moment, write down the height of the arrow's tip above the horizontal line through the centre. Plot that height against time. You get a sine wave:

```
        spinning arrow                    height of the tip vs time
             . . .                   +A |    _.--._
          .    ^    .                   |  /        \
         .    /      .                  | /          \
        .    / angle  .               0 |/------------\------------/---  time
        .   o-------- .                 |              \          /
         .            .                 |               \        /
          .          .               -A |                '-.__.-'
             . . .                      0      T/4    T/2    3T/4    T
```

- When the arrow points right (angle 0), the height is 0.
- A quarter turn later (90 degrees), it points straight up: height +A, the peak.
- Half a turn (180 degrees): pointing left, height 0 again.
- Three quarters (270 degrees): pointing down, height -A.
- A full turn (360 degrees): back where it started.

The function that turns "angle" into "height of the tip on a circle of radius 1" is called **sine**, written sin. So the height is A x sin(angle).

### Why sine waves matter so much

Many things in nature oscillate as sines: a mass on a spring, a pendulum (for small swings), a guitar string's basic note, and, as you will see in Phase 10, a capacitor and an inductor trading energy. But the real reason engineers love sine waves is this:

**When a sine wave passes through resistors, capacitors and inductors, what comes out is still a sine wave of the same frequency.** Only its size and its timing (phase) change.

No other wave shape has this property. Send a square wave through a resistor-capacitor circuit and you get rounded "shark fins" (Phase 07, Lesson 03): the shape changes. Send a sine wave and you get a sine wave. That means, for sine waves, a whole circuit can be described by two numbers per frequency: "how much smaller" and "how much later". That is exactly what impedance (Lesson 06) and filters (Phase 10) are about. (And thanks to a result by Joseph Fourier, any repeating waveform can be built from sine waves, so understanding sines is enough to understand everything.)

## The Concept

### Angle in degrees and in radians

You already know **degrees**: a full turn is 360 degrees. Engineers and the maths inside Python prefer **radians**. Here is the idea. Walk around a circle of radius 1 metre. When you have walked 1 metre along the edge, the angle you have turned is 1 radian. A full circle has a circumference of 2 x pi x radius, with pi (written π) the famous number 3.14159..., so a full turn is 2 x pi = 6.2832 radians.

```
360 degrees = 2 pi radians
1 radian    = 360 / (2 pi) = 57.2958 degrees
90 degrees  = 2 pi / 4     = pi / 2 = 1.5708 radians
```

To convert degrees to radians multiply by pi / 180; radians to degrees, multiply by 180 / pi. Python's `math.sin` and `numpy.sin` expect radians, so `math.radians(90)` gives 1.5708 and `math.sin(math.radians(90))` gives 1.0.

### Frequency, period and angular frequency

From Lesson 01: the **frequency** f is the number of full cycles per second (hertz, Hz), and the **period** T = 1 / f is the time for one cycle.

If the arrow makes f full turns each second, and each turn is 2 pi radians, then the angle grows by 2 x pi x f radians every second. That rate has its own name, **angular frequency**, written with the Greek letter omega (ω):

```
omega = 2 x pi x f      (read: "omega equals two pi times the frequency")
```

Its unit is radians per second (rad/s). Worked examples:

| f | T = 1 / f | omega = 2 pi f |
|---|---|---|
| 50 Hz (mains, Europe) | 20 ms | 2 x 3.14159 x 50 = 314.16 rad/s |
| 60 Hz (mains, America) | 16.667 ms | 376.99 rad/s |
| 440 Hz (the note A) | 2.273 ms | 2,764.6 rad/s |
| 1,000 Hz | 1 ms | 6,283.2 rad/s |

Frequency and omega describe the same thing in different units, like km/h and m/s. Formulas look neater with omega, so you will see it a lot.

### The formula for a sine wave

After time t, the arrow has turned through omega x t radians. If at t = 0 it already pointed at an angle phi (the Greek letter phi, φ, the **phase**), its angle is omega x t + phi. The voltage is the height of the tip:

```
v(t) = A x sin(omega x t + phi) = A x sin(2 pi f t + phi)
```

Read it aloud: "the voltage at time t equals the amplitude times the sine of: two pi times the frequency times the time, plus the phase". Three numbers fully describe the wave:

- **A**, the amplitude (peak value), in volts;
- **f**, the frequency, in hertz (or omega in rad/s);
- **phi**, the phase, in radians or degrees.

Sometimes there is a fourth, a constant **offset** added on top: v(t) = offset + A sin(...). A sine riding on 2.5 V, for example, swings between 2.5 - A and 2.5 + A.

### Worked example: evaluating a sine by hand

Take A = 10 V, f = 50 Hz, phi = 0. Where is the voltage at t = 2.5 ms?

1. omega = 2 x 3.14159 x 50 = 314.16 rad/s.
2. Angle = omega x t = 314.16 x 0.0025 = 0.7854 rad. In degrees: 0.7854 x 180 / 3.14159 = 45 degrees. (Simpler: 2.5 ms is one eighth of the 20 ms period, and one eighth of 360 degrees is 45 degrees.)
3. sin(45 degrees) = 0.7071.
4. v = 10 x 0.7071 = 7.071 V.

The full table over one period (each step is one eighth of a cycle):

| t (ms) | angle (deg) | sin(angle) | v (V) |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 2.5 | 45 | 0.7071 | 7.071 |
| 5 | 90 | 1 | 10 |
| 7.5 | 135 | 0.7071 | 7.071 |
| 10 | 180 | 0 | 0 |
| 12.5 | 225 | -0.7071 | -7.071 |
| 15 | 270 | -1 | -10 |
| 17.5 | 315 | -0.7071 | -7.071 |
| 20 | 360 | 0 | 0 |

Amplitude 10 V, peak-to-peak 20 V. Notice that half the time the voltage is negative: the polarity is reversed.

### Phase: who is ahead?

Take two waves of the **same frequency**:

```
v1(t) = 5 sin(omega t)               phase 0
v2(t) = 5 sin(omega t - 60 degrees)  phase -60 degrees
```

At any moment, v2's arrow points 60 degrees "behind" v1's arrow. So v2 reaches each peak a bit later: v2 **lags** v1 by 60 degrees, or equivalently v1 **leads** v2 by 60 degrees.

How much later, in time? A full 360 degrees takes one period T. So 60 degrees takes 60/360 of a period:

```
time shift = (phase difference / 360 degrees) x T
           = (60 / 360) x 20 ms = 3.333 ms      (at 50 Hz)
```

And the other way round: if you see on the oscilloscope that one wave crosses zero (going up) 3.333 ms after the other, and the period is 20 ms, the phase difference is 360 x 3.333 / 20 = 60 degrees.

```
     v1 leads                v2 lags by 60 degrees
  |   _               _
  |  / \     .-.     / \
  | /   \   /   \   /   \
  |/-----\-/-----\-/-----\----- t
  |       \       \
  |  ^ v1 crosses up    ^ v2 crosses up 3.33 ms later
```

Some special phase differences have names:

- **0 degrees**: in phase, peaks line up.
- **90 degrees**: in quadrature: one wave is at its peak when the other crosses zero. You will see this between a capacitor's voltage and its current (Lesson 05).
- **180 degrees**: antiphase: one is at its peak when the other is at its lowest. Each is the negative of the other.

Phase only makes sense between waves of the same frequency. Two waves of different frequencies drift relative to each other, so "how far ahead" keeps changing.

### Measuring frequency and phase from data

An oscilloscope or a computer has only samples: values at many evenly spaced instants. A robust way to measure is with **zero crossings**: the moments when the wave passes through zero going upwards.

- The time between consecutive upward crossings is one period, so frequency = 1 / (average spacing).
- The time between v1's upward crossing and the next upward crossing of v2 is the lag; convert it to degrees with 360 x lag / T.

The sample just before a crossing is negative and the one after is positive or zero. The exact crossing lies between them; we estimate it by drawing a straight line between the two samples (**linear interpolation**): if the values are y0 < 0 and y1 >= 0 at times t0 and t1, the crossing is at

```
t_cross = t0 + (-y0 / (y1 - y0)) x (t1 - t0)
```

### Preview: a capacitor makes the wave late

In Phase 07 you saw that a capacitor charges through a resistor with time constant tau = R x C. Drive the same resistor-capacitor circuit with a sine wave instead of a step:

```
         R = 1 kohm
 in o-----/\/\/\-----o out
   (~)               |
  1 V, 1 kHz       ===  C = 159.15 nF
   |                 |
 0 o-----------------o
```

The capacitor never quite "catches up" with the input: by the time it has charged towards the peak, the input is already going down. The result is a sine wave at the same 1 kHz, but **smaller** and **later**. With these values, R x C x omega = 1000 x 159.15e-9 x 6283.2 = 1.000, and the simulator shows an output amplitude of about 0.707 V that lags the input by about 45 degrees (125 microseconds, one eighth of the 1 ms period). By the end of Lesson 06 you will predict those two numbers in one line of arithmetic.

## Build It

### Step 1: A sine wave function

```python
def sine(t, amplitude, freq, phase_deg=0.0):
    return amplitude * np.sin(2 * np.pi * freq * t + np.radians(phase_deg))
```

This is the formula word for word. `np.radians` converts the phase from degrees to radians. The script prints the eight-step table above; check that it matches your hand calculation.

### Step 2: Frequency, period, omega

```python
for f in (50.0, 60.0, 440.0, 1000.0):
    omega = 2 * math.pi * f
    print(f"  f = {f:7.1f} Hz   T = {1000 / f:7.3f} ms   omega = 2 pi f = {omega:9.2f} rad/s")
```

### Step 3: Zero crossings and frequency

```python
def rising_zero_crossings(time, signal):
    below = signal[:-1] < 0
    above = signal[1:] >= 0
    hits = np.where(below & above)[0]
    fraction = -signal[hits] / (signal[hits + 1] - signal[hits])
    return time[hits] + fraction * (time[hits + 1] - time[hits])


def measure_frequency(time, signal):
    crossings = rising_zero_crossings(time, signal)
    periods = np.diff(crossings)
    return 1.0 / periods.mean()
```

`below & above` is true at index k when sample k is negative and sample k+1 is not: an upward crossing. `fraction` is the interpolation from the formula above. We feed it a "mystery" 137 Hz wave with a 20 degree phase, sampled every microsecond for 0.1 s, and it returns 137.000 Hz.

### Step 4: Phase difference

```python
def measure_lag_deg(time, reference, delayed, freq):
    t_ref = rising_zero_crossings(time, reference)
    t_del = rising_zero_crossings(time, delayed)
    lag_s = t_del[-1] - t_ref[t_ref <= t_del[-1]][-1]
    return 360.0 * lag_s * freq, lag_s
```

Take the last upward crossing of the delayed wave and the reference's most recent crossing before it; their difference is the lag in seconds, and 360 x lag x f converts it to degrees (multiplying by f is the same as dividing by T). For the two 50 Hz waves, it prints a shift of 3.3333 ms and a phase of 60.00 degrees.

### Step 5: The simulated RC circuit

```python
c = Circuit()
c.sine_source("V1", "in", "0", amplitude=1.0, freq=f_test)
c.resistor("R1", "in", "out", r_ohms)
c.capacitor("C1", "out", "0", c_farads)
t = c.transient(t_stop=10e-3, dt=1e-6)
settled = t.time >= 6e-3
```

We simulate 10 ms (ten cycles) in 1 microsecond steps (Phase 07, Lesson 08 showed how such a simulation works). The first cycles contain a start-up "transient" while the capacitor charges from 0 V, so we keep only the last 4 ms, when the circuit has settled into its steady rhythm. The amplitude is half the peak-to-peak value, and the lag comes from Step 4. Expected output:

```
  output amplitude = 0.7071 V
  output lags the input by 125.0 us = 45.0 deg
```

The script also saves `out.png` with the two 50 Hz waves (top) and the RC input and output (bottom).

## Use It

- **Oscilloscope measurements.** Every scope has automatic "Freq", "Period", "Amplitude", "Pk-Pk" and "Phase" measurements. Internally they do something very close to Step 3 and Step 4.
- **Musical notes.** Concert A is 440 Hz; each octave up doubles the frequency. A pure tuning-fork tone is very close to a sine wave.
- **Signal generators.** A function generator lets you set exactly the three numbers of this lesson (amplitude, frequency, phase) plus an offset.
- **Three-phase power.** The grid carries three sine waves of the same frequency, each shifted by 120 degrees from the next. Large motors and the high-voltage grid use it because the total power flows smoothly.
- **Grid frequency as a health signal.** Grid operators watch the frequency closely: if consumption exceeds generation, the generators slow down slightly and the frequency drops below 50.000 Hz by a few hundredths of a hertz.

## Common Mistakes

- **Feeding degrees to `sin`.** `math.sin(90)` is 0.894, not 1, because 90 is taken as radians. Convert with `math.radians`.
- **Mixing up f and omega.** omega = 2 pi f. Forgetting the 2 pi gives answers about 6.28 times too small.
- **Confusing amplitude and peak-to-peak.** A sine from -10 V to +10 V has amplitude 10 V and peak-to-peak 20 V. Oscilloscopes show both: read the label.
- **Comparing phases of different frequencies.** Phase difference only means something when the frequencies are equal.
- **Getting lead and lag backwards.** The wave that reaches a given point (peak, upward zero crossing) **first** is leading. On a time axis going right, the leading wave is the one further **left**.
- **Measuring during the start-up transient.** Right after switching on, a circuit with capacitors or inductors has not yet settled. Wait several time constants before measuring amplitude and phase.

## Exercises

1. **By hand.** A 60 Hz wave has amplitude 170 V and phase 0. What is its value at t = 1 ms? (Hint: find the angle in degrees first.)
2. **Conversions.** Convert 30 degrees, 120 degrees and 270 degrees into radians, and 0.5 rad and 3 rad into degrees.
3. **Time shift.** At 1 kHz, a signal lags another by 90 degrees. How many microseconds is that? And at 50 Hz?
4. **Read the wave.** v(t) = 2.5 + 1.2 sin(1,256.6 t + 0.5236). Give the offset, the amplitude, the peak-to-peak value, the frequency in Hz and the phase in degrees. What are the highest and lowest voltages?
5. **Simulator.** In Step 5, change the frequency to 100 Hz, then to 10 kHz. Before running, guess: does the output amplitude grow or shrink, and does the lag grow or shrink? Run it and explain what you see using the idea "the capacitor needs about R x C seconds to catch up".

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Amplitude | "How big the wave is" | The peak value measured from the centre line, A in v(t) = A sin(omega t + phi) |
| Peak-to-peak | "Top to bottom" | Highest minus lowest value; 2 x A for a sine without distortion |
| Frequency | "How fast it wiggles" | Full cycles per second, in Hz |
| Angular frequency | "Omega" | 2 x pi x f, in radians per second: how fast the phase angle grows |
| Radian | "The other angle unit" | Angle whose arc length equals the radius; 2 pi rad = 360 degrees |
| Phase | "Where the wave starts" | The angle of the wave at t = 0 |
| Phase shift | "How far behind" | Difference in phase between two equal-frequency waves; time shift = (shift / 360) x T |
| Lead / lag | "Ahead / behind" | The leading wave reaches the same point of its cycle earlier |

## Further Reading

- [All About Circuits, Vol. II (AC), Chapter 1: AC Waveforms and Phase](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-1/ac-waveforms/) — waveforms, frequency and phase with clear diagrams.
- [Khan Academy: Unit circle definition of sine and cosine](https://www.khanacademy.org/math/trigonometry/unit-circle-trig-func) — if the "height of a spinning arrow" idea is new, this is the gentle maths behind it.
- *Practical Electronics for Inventors*, Scherz & Monk, 4th ed., Chapter 2 (sections on AC and sine waves) — an inventor-friendly treatment with many practical numbers.
- [Feynman Lectures on Physics, Vol. I, Chapter 21: The Harmonic Oscillator](https://www.feynmanlectures.caltech.edu/I_21.html) — why so many physical systems oscillate as sine waves.
