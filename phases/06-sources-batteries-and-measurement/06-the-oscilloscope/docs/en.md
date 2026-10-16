# The Oscilloscope

> A multimeter gives you one number. An oscilloscope gives you the whole story of a voltage, drawn against time.

**Type:** Build
**Prerequisites:** Phase 01 Lesson 02 (Scientific Notation and Orders of Magnitude), Phase 06 Lesson 04 (Inside the Multimeter), Phase 06 Lesson 05 (Loading and Measurement Error)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Oscilloscope ("scope") | An instrument that draws a graph of voltage (up) against time (across), live | A heart monitor in a hospital |
| Waveform | The shape a voltage makes over time | The line on the heart monitor |
| Trace | The line the scope draws for one signal | One pen on a chart recorder |
| Channel | One input of the scope; most have 2 or 4 | One microphone on a mixing desk |
| Division (div) | One square of the grid on the screen; usually 10 across and 8 up | A square on graph paper |
| Volts per division (V/div) | How many volts one square is worth, vertically | The scale of a map |
| Time per division (s/div) | How much time one square is worth, horizontally | Frames per second in a time-lapse |
| Trigger | The rule that decides when the drawing starts, so each sweep lines up with the last | A camera that only fires when the runner crosses the line |
| Periodic signal | A signal that repeats itself exactly, again and again | The ticking of a clock |
| Period (T) | The time one repetition takes, in seconds | One full swing of a pendulum |
| Frequency (f) | How many repetitions per second, in hertz (Hz); f = 1 / T | Beats per minute, but per second |
| Amplitude | How far a wave swings from its middle | How high the waves rise above the calm sea |
| Peak-to-peak (Vpp) | The distance from the lowest to the highest point | From trough to crest |
| Offset (DC level) | A constant voltage added to the wave, shifting it up or down | The tide level the waves ride on |
| RMS | "Root mean square": the steady voltage that would heat a resistor the same amount | The equivalent steady effort of a varying workout |
| Duty cycle | The fraction of each period a pulse spends "high" | The fraction of the day a shop is open |
| Probe | The cable and tip that connect the circuit to the scope | The stethoscope's tube |
| Sampling | Measuring the voltage at regular instants and storing the numbers | Frames of a film |
| Aliasing | A fake slow wave that appears when sampling too slowly | Wagon wheels that seem to spin backwards in films |
| Bandwidth | The highest frequency a scope can show without shrinking it much | The highest note a speaker can play |

## Learning Objectives

- Read a scope screen: convert divisions into volts and seconds using the V/div and s/div settings.
- Explain what the trigger does and why the picture rolls without it.
- Measure peak-to-peak, mean, RMS, period, frequency and duty cycle from recorded samples.
- Explain why x10 probes load the circuit less, and compute the reading with each probe.
- Recognise aliasing and choose a sample rate and bandwidth that are high enough.
- Build a tiny text-mode scope on top of our simulator's transient analysis.

## The Problem

Your multimeter on "DC volts" reads 1.25 V on a pin that should switch between 0 and 5 V. Is the pin stuck halfway? Is it switching? How fast? The meter can't tell you: it shows an average. On "AC volts" it shows another number that only makes sense for clean sine waves.

Many of the interesting things in electronics happen in time: a pulse that drives a motor, the ripple on a power supply, a clock ticking millions of times per second, the instant a button bounces, the glitch that resets your microcontroller once a day. To see them, you need a picture of voltage against time. That is the oscilloscope.

## The Physics

### The old way: a beam of electrons

The first oscilloscopes were built around a cathode-ray tube, like an old television. A hot wire released electrons, a high voltage shot them toward a phosphor-coated glass screen, and the screen glowed where they hit. Two pairs of metal plates bent the beam on the way:

- the **horizontal** plates got a voltage that rose steadily (a "sweep"), dragging the dot from left to right at a fixed speed: that is the time axis;
- the **vertical** plates got the measured voltage, amplified: the dot went up and down with it.

So the dot drew the voltage against time. At the right edge the sweep jumped back and waited for the next start signal: the trigger. Because the phosphor glowed a little while, and because the sweep repeated fast, your eye saw a still line.

### The modern way: sampling

A digital scope (almost all scopes today) does the same job with numbers. Its input amplifier scales the voltage, an analog-to-digital converter **samples** it, that is, measures it at regular instants, perhaps a billion times per second, and stores the numbers in memory. A processor finds the trigger point in that memory and draws the samples around it on a screen. It can also compute measurements (frequency, RMS...) from the stored numbers, which is exactly what our script will do.

### Signals in time

A voltage that changes in time can be described by a few numbers. For a **sine wave**, the smooth wave you get from a rotating generator (Phase 09):

    v(t) = offset + amplitude * sin(2 * pi * f * t)

Read it: "the voltage at time t is the offset plus the amplitude times the sine of two pi times frequency times time." The sine goes between -1 and +1, so v goes between offset - amplitude and offset + amplitude.

Our channel 1 has offset 1 V, amplitude 2 V, f = 1000 Hz:

- maximum: 1 + 2 = 3 V; minimum: 1 - 2 = -1 V;
- peak-to-peak: 3 - (-1) = 4 V, twice the amplitude;
- period: T = 1 / f = 1 / 1000 = 0.001 s = 1 ms.

A **pulse train** (square-ish wave) jumps between a low and a high level. Our channel 2 goes from 0 to 5 V with period 1 ms and duty cycle 25 %: it is high for 0.25 ms, low for 0.75 ms.

## The Concept

### Reading the grid

The screen is a grid, usually 10 divisions across and 8 up. Two knobs set the scale:

- **V/div**: volts per vertical division. At 1 V/div, a wave that spans 4 divisions top to bottom is 4 V peak-to-peak.
- **s/div**: time per horizontal division. At 0.2 ms/div, the whole screen shows 10 * 0.2 = 2 ms.

```
  0.2 ms/div, 1 V/div
  +-----+-----+-----+-----+-----+     one cycle spans 5 divisions
  |       ***                ***      -> T = 5 * 0.2 ms = 1 ms
  |     *     *            *          -> f = 1 / 1 ms = 1000 Hz
  |----*-------*----------*------ 0 V
  | *            *     *              crest at +3 div, trough at -1 div
  |*               ***                -> Vpp = 4 div * 1 V/div = 4 V
  +-----+-----+-----+-----+-----+
```

Worked example. A wave is 3.2 divisions from trough to crest at 0.5 V/div and one cycle covers 4 divisions at 50 microseconds/div.

- Vpp = 3.2 * 0.5 = 1.6 V.
- T = 4 * 50 microseconds = 200 microseconds = 0.0002 s.
- f = 1 / 0.0002 = 5000 Hz = 5 kHz.

Choose the settings so the wave fills most of the screen vertically and shows two or three cycles horizontally: you read more precisely when the picture is big.

A **position** knob for each channel moves its trace up or down, so two signals can sit on the screen without overlapping. Our text screen does this for the pulse.

### The trigger

The scope draws one screenful, then another, then another, many times per second. If each sweep started at a random moment, each picture would show the wave shifted by a different amount and the result would be a smeared, rolling mess.

The **trigger** fixes this. You give it a **level** (say 1 V) and a **slope** (rising or falling). The scope starts each picture at the instant the signal crosses that level in that direction. For a periodic signal those instants are exactly one period apart, so every picture is identical and the trace stands still.

```
  level 1 V, rising
       ^           ^           ^         <- trigger points, 1 ms apart
  ----/--\--------/--\--------/--\----
     /    \      /    \      /    \
  __/      \____/      \____/      \__
```

Finding the crossing is easy with samples: look for two consecutive samples where the first is below the level and the second is at or above it. Then interpolate between them for a precise time.

Other trigger modes you will meet: **auto** (draw anyway if no trigger arrives, so you see something), **normal** (wait for a trigger, good for rare events), and **single** (capture once and freeze, perfect for a button press or a power-on glitch).

### Measurements from samples

A digital scope computes measurements from the stored samples v_1, v_2, ..., v_N:

- **max, min, peak-to-peak**: the largest, the smallest, and their difference.
- **mean** (DC average): add them up and divide by N. A multimeter on DC volts shows roughly this.
- **RMS**: square every sample, take the mean, then the square root. Read it: "root of the mean of the squares". It is the steady voltage that would deliver the same power to a resistor (power goes with V squared, Phase 03).
- **period and frequency**: the time between two consecutive rising crossings; f = 1 / T.
- **duty cycle**: the fraction of samples above the middle level.

For a sine with an offset there is a neat formula: RMS = square root of (offset^2 + amplitude^2 / 2). For channel 1: square root of (1 + 4 / 2) = square root of 3 = 1.732 V. For a pure sine with no offset, RMS = amplitude / square root of 2, about 0.707 times the amplitude (Phase 09 Lesson 03).

For channel 2 (0 or 5 V, 25 % of the time high):

- mean = 0.25 * 5 = 1.25 V. That is the mysterious 1.25 V the multimeter showed in The Problem: the pin was switching all along.
- RMS = square root of (0.25 * 25) = square root of 6.25 = 2.5 V.

### The probe and the input

A scope input is typically **1 Mohm** in parallel with a small capacitance (around 15 to 20 pF). So everything from Lesson 05 applies: on a soft circuit the scope loads it.

A **x10 probe** puts a 9 Mohm resistor in its tip. Together with the scope's 1 Mohm, the circuit now sees 10 Mohm, and the scope receives one tenth of the voltage (a voltage divider: 1 / (9 + 1)). The scope is told the probe is x10 and multiplies the display back by 10.

Worked example on our soft 1 M / 1 M divider from 10 V (V_th = 5 V, R_th = 500 kohm):

- **x1 probe** (scope sees 1 Mohm): 5 * 1 / (1 + 0.5) = 3.333 V. A -33 % error.
- **x10 probe** (circuit sees 10 Mohm): 5 * 10 / (10 + 0.5) = 4.762 V at the probe tip; the scope input gets 0.476 V and displays 4.762 V. A -4.8 % error.

The x10 probe has a second, bigger advantage at high frequencies: a small adjustable capacitor in the probe, set with a screw ("probe compensation") against the square-wave test output on the front of the scope, makes the divider work equally for slow and fast signals, so the probe's capacitance loads the circuit far less. You will understand capacitors properly in Phase 07; for now, the rule is: **use x10 by default**, switch to x1 only for very small signals.

### Ground clips

The probe's short ground clip is connected to the scope's chassis, which is connected to mains earth through the power cord. Clip it onto a point that is not at earth potential (for example inside mains-powered equipment that isn't isolated) and you create a short circuit through the scope's ground. This is the classic way to blow up a circuit, a probe, or worse. Clip ground only to the circuit's ground.

### Sampling and aliasing

A digital scope only sees its samples. If it samples too slowly, it can be fooled. A 1000 Hz sine sampled 1100 times per second gets one sample per cycle, each slightly later in the cycle than the last. Joined up, the samples trace a slow wave at 1100 - 1000 = 100 Hz that does not exist. This is **aliasing**: the same effect that makes car wheels seem to spin slowly backwards in films.

The rule (made precise in Phase 19 as the Nyquist criterion): you must take **more than two samples per cycle** of the fastest thing in the signal, and in practice a scope wants five or more. Scope makers quote both **sample rate** (samples per second) and **bandwidth** (the frequency where the input amplifier shrinks a sine to about 70 % of its size). A common rule: choose bandwidth at least 5 times the fastest frequency you care about.

## Build It

### Step 1: Record two signals

Our simulator's transient analysis computes voltages at every time step, just like a sampling scope fills its memory.

```python
def record_signals():
    c = Circuit()
    c.sine_source("Vsine", "ch1", "0", amplitude=2.0, freq=1000.0, offset=1.0)
    c.resistor("Rload1", "ch1", "0", 1000.0)
    c.pulse_source("Vpulse", "ch2", "0", low=0.0, high=5.0, period=1e-3, duty=0.25)
    c.resistor("Rload2", "ch2", "0", 1000.0)
    t = c.transient(t_stop=5e-3, dt=1e-6)
    return np.asarray(t.time), np.asarray(t.v("ch1")), np.asarray(t.v("ch2"))
```

5 ms at 1 microsecond per step is 5001 samples: one million samples per second, a thousand per cycle.

### Step 2: The trigger

```python
def rising_crossings(time, volts, level):
    below = volts[:-1] < level
    above = volts[1:] >= level
    indices = np.nonzero(below & above)[0]
    fractions = (level - volts[indices]) / (volts[indices + 1] - volts[indices])
    return time[indices] + fractions * (time[indices + 1] - time[indices])
```

Channel 1 crosses 1 V going up at 1, 2, 3 and 4 ms: one period apart, as expected.

### Step 3: A text screen

`ascii_screen` makes a 10 by 8 division grid, starts one division before the chosen trigger time, and for every column looks up each trace's voltage (with its own V/div and position) and puts a symbol in the matching row:

```
  |+     +     +     +     +     +     +     +     +     +     +|
  |                              :                              |
  |+     +     ****  +     +     +     +     ****  +     +     +|
  |          **    **            :         **    **             |
  |+     + **  +     **    +     +     + **  +     **    +     +|
  |       *            *         :      *            *          |
  |+     *     +     +  *  +     +     *     +     +  *  +     +|
  |     *                *       :    *                *        |
  |+--**-+-----+-----+----**-----+--**-+-----+-----+----**-----+|
  | **                      **   :**                      **    |
  |*     +     +     +     +  ****     +     +     +     +  ****|
  |      oooooooo                :     oooooooo                 |
  ...
  |oooooo+     + oooooooooooooooooooooo+     + ooooooooooooooooo|
```

Read it: the sine (`*`) peaks 3 divisions above the centre line (3 V) and dips 1 division below (-1 V); one cycle is 5 divisions (1 ms). The trigger is one division in from the left, where the sine crosses +1 V going up. The pulse (`o`) is drawn at 2 V/div with its 0 V moved to the bottom edge: it rises 2.5 divisions (5 V) and stays high for a little over one division (0.25 ms) in every five.

### Step 4: Automatic measurements

```python
def measurements(time, volts, level):
    crossings = rising_crossings(time, volts, level)
    period = float(np.mean(np.diff(crossings)))
    return {
        "max (V)": float(volts.max()),
        "min (V)": float(volts.min()),
        "peak-to-peak (V)": float(volts.max() - volts.min()),
        "mean (V)": float(volts.mean()),
        "RMS (V)": float(np.sqrt(np.mean(volts**2))),
        "period (ms)": period * 1000,
        "frequency (Hz)": 1.0 / period,
        "duty (%)": 100.0 * float(np.mean(volts > level)),
    }
```

Channel 1: max 3.000, min -1.000, Vpp 4.000, mean 1.000, RMS 1.732, period 1.000 ms. Channel 2: Vpp 5.000, mean about 1.25 V, RMS about 2.50 V, duty about 25 %, frequency about 1000 Hz. The tiny errors on channel 2 (1000.25 Hz, 25.07 %) come from the instant jumps falling between 1 microsecond samples: a real scope has exactly the same limit, set by its sample rate.

### Step 5: x1 and x10 probes

The script builds the soft divider, attaches the scope's 1 Mohm input either directly (a closed switch as the x1 probe) or through 9 Mohm (x10 probe), and prints 3.333 V versus 4.762 V.

### Step 6: Aliasing

A 1000 Hz sine sampled at 20 000 samples per second has its strongest frequency at 1000 Hz. Sampled at 1100 per second, the strongest frequency appears at 100 Hz: a ghost.

The script also saves `out.png`, a scope-style plot with a 0.2 ms by 1 V grid.

Run it:

```bash
uv run python phases/06-sources-batteries-and-measurement/06-the-oscilloscope/code/main.py
```

## Use It

- **Entry-level bench scopes** today offer 2 or 4 channels, 50 to 200 MHz bandwidth, and 1 GSa/s (a billion samples per second) sample rate, with probes rated x1/x10.
- **USB scopes and "logic analyzers"** turn a laptop into a display; cheap ones sample at a few to a few hundred MSa/s, enough for audio, PWM and slow serial buses.
- **Typical jobs:** checking that a PWM signal has the duty cycle you programmed (Phase 17); looking at ripple on a power supply (Lesson 07 and Phase 18); timing a serial bus (Phase 17); catching switch bounce with single-shot trigger; seeing a regulator oscillate.
- **Specs to read in a datasheet:** bandwidth, sample rate, memory depth (how many samples it can keep, which limits how long a capture can be at full speed), input resistance and capacitance (1 Mohm, around 15 pF), maximum input voltage, and vertical resolution (usually 8 bits, 256 levels).
- **Probe compensation:** before measuring, touch the probe to the square-wave "probe comp" terminal and adjust the probe's screw until the square wave's corners are sharp, neither rounded nor spiky.

## Common Mistakes

- **Leaving the probe on x1 while the scope thinks x10 (or vice versa).** Every reading is off by a factor of 10.
- **No trigger, or trigger on the wrong channel.** The trace rolls or never appears. Set the trigger source to the channel you look at, and its level inside the signal's range.
- **AC coupling a slow signal.** "AC coupling" removes the DC part of the signal with an input capacitor; it also distorts slow square waves. Use DC coupling unless you specifically want to zoom in on ripple.
- **Clipping the ground lead to a non-ground point.** The scope's ground is earth. See the safety note above and Phase 00 Lesson 08.
- **Reading RMS from a sine formula on a non-sine signal.** amplitude / square root of 2 only holds for pure sines. Let the scope compute RMS from samples.
- **Trusting a picture taken with too slow a sample rate.** If the wave looks suspiciously slow or smooth, change the time base and see whether the "frequency" changes in a way it shouldn't.
- **Long ground leads at high speed.** The ground wire's inductance (Phase 08) rings with fast edges and shows overshoot that isn't in the circuit. Use the short ground spring for fast signals.

## Exercises

1. A sine fills 6 divisions peak-to-peak at 200 mV/div, and 2.5 cycles fill the 10-division screen at 1 ms/div. What are Vpp, amplitude, period and frequency?
2. A pulse train switches between 0 and 3.3 V and is high for 20 microseconds out of every 100 microseconds. Compute frequency, duty cycle, mean and RMS.
3. A 50 Hz sine has amplitude 325 V. What is its RMS value? Which everyday voltage is this?
4. With a x10 probe (10 Mohm total), what does the scope show when measuring a point with V_th = 3 V and R_th = 220 kohm? With x1?
5. Change the script so channel 2 has duty 0.6 and the trigger uses channel 2's falling edge. Predict the new mean and RMS before running it. Then sample the 1000 Hz sine at 900 samples per second: where does the ghost appear?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Oscilloscope | "The scope" | Instrument that plots voltage against time from sampled (or, in old ones, directly deflected) signals |
| V/div, s/div | "The knobs" | Vertical and horizontal scale factors of the grid |
| Trigger | "Make it stop moving" | Rule (level, slope, source) that aligns each sweep to the same point of the signal |
| Peak-to-peak | "The size of the wave" | Max minus min of the signal |
| RMS | "The AC value" | Square root of the mean of the squared signal; the power-equivalent steady value |
| Duty cycle | "On time" | High time divided by period |
| x10 probe | "The normal probe" | A 9 Mohm (plus compensating capacitor) divider making the scope load the circuit 10 times less |
| Aliasing | "A weird slow wave" | A false frequency created by sampling slower than twice the real frequency |
| Bandwidth | "How fast the scope is" | Frequency at which a sine's displayed amplitude has dropped to about 70 % |

## Further Reading

- Tektronix, *XYZs of Oscilloscopes* primer (how scopes, triggers, probes and sampling work).
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., chapter on test equipment (multimeters and oscilloscopes).
- Keysight (Agilent), application note "Evaluating Oscilloscope Bandwidths for Your Application" (5989-5733EN) and their probing fundamentals notes: https://www.keysight.com/us/en/assets/7018-01455/application-notes/5989-5733.pdf
- EEVblog (Dave Jones) video tutorials on oscilloscope basics and probe compensation, on YouTube.
