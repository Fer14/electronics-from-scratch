# Decibels and Bode Plots

> Engineers measure gain in decibels because filters multiply, and logarithms turn multiplying into adding. On a log-log plot every RC filter is two straight lines.

**Type:** Learn
**Prerequisites:** Phase 10 (Filters and Resonance), Lesson 02 (RC Low-Pass and High-Pass); Phase 01 (The Physics Underneath), Lesson 02 (Scientific Notation and Orders of Magnitude)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Logarithm (log10) | The power you must raise 10 to, to get a number: log10(1000) = 3 because 10³ = 1000 | Counting the zeros: 1000 has three |
| Decibel (dB) | A way to write a ratio as 20 x log10 (for voltages) or 10 x log10 (for powers) | The volume scale on a mixing desk |
| Bel | The original unit, log10 of a power ratio; a decibel is a tenth of a bel | Rarely used on its own |
| Decade | A factor of 10 in frequency (100 Hz to 1 kHz) | One "zero" more |
| Octave | A factor of 2 in frequency (440 Hz to 880 Hz) | The same musical note, one step higher |
| Bode plot | Two graphs of a filter: gain in dB and phase in degrees, both against frequency on a log scale | A filter's fingerprint |
| Asymptote | A straight line the curve approaches far from a special point | The road that a winding path runs alongside |
| Corner frequency | Where the two straight asymptotes of a Bode plot meet; equals fc | The corner of an L-shaped street |
| dBm / dBV | Decibels relative to a fixed reference: 1 mW, or 1 V | Height "above sea level" rather than "above the table" |
| Buffer | A stage that copies a voltage without drawing current from it | A relay runner who takes the baton without slowing the previous runner |

## Learning Objectives

- Explain logarithms from scratch and use the rule log(a x b) = log(a) + log(b)
- Convert between voltage ratios, power ratios and decibels, and remember the key values (-3, -6, -20 dB)
- Read and sketch a Bode plot of an RC filter with straight-line asymptotes: flat, then -20 dB per decade
- Show that the dB gains of stages add up when the stages are buffered, and see what loading does
- Use dBm and dBV to describe absolute levels

## The Problem

A guitar pickup produces about 0.1 V; a power amplifier delivers 20 V to the speaker; a radio antenna picks up 1 µV; a microphone 10 mV. The ratios between these span ten million to one. A filter cuts some frequency by 0.001 and another by 0.9. Two filters in a row multiply their effects. Working with these numbers directly is awkward: tiny decimals, huge ranges, and constant multiplication.

Engineers solved this a century ago, in the telephone industry, by measuring ratios on a **logarithmic** scale. On that scale, multiplying ratios becomes adding numbers, huge ranges become small numbers (a ratio of a million becomes 120), and the frequency response of an RC filter becomes two straight lines you can draw with a ruler. Every datasheet, every audio specification and every filter design uses this language. This lesson teaches it from zero.

## The Physics

There is a little physics here: human senses work logarithmically. Doubling the power of a sound does not sound "twice as loud"; it sounds a bit louder. A tenfold increase in power sounds roughly twice as loud. Our ears handle a range of sound powers of about a million million (10^12) from the quietest whisper to the threshold of pain, and the only sensible way to describe that range is by powers of ten. The *bel*, named after Alexander Graham Bell, and its tenth, the **decibel**, came from telephone engineers measuring how much signal was lost along a cable. The rest of this lesson is mathematics in service of that idea.

## The Concept

### 1. Logarithms from zero

You know powers of ten (Phase 01, Lesson 02): 10¹ = 10, 10² = 100, 10³ = 1000, and also 10⁰ = 1, 10⁻¹ = 0.1, 10⁻² = 0.01.

The **logarithm** (base 10) asks the reverse question: **"10 to what power gives this number?"**

```
log10(1000) = 3        because 10^3 = 1000
log10(0.01) = -2       because 10^-2 = 0.01
log10(1)    = 0        because 10^0 = 1
```

For whole powers of ten, the log is just "count the zeros" (negative for numbers below 1). Numbers in between have logs in between: 2 is between 1 and 10, so log10(2) is between 0 and 1. In fact log10(2) = 0.301, meaning 10^0.301 = 2.000. Similarly log10(5) = 0.699.

**The one rule you need.** Multiplying powers of ten adds their exponents: 10² x 10³ = 10⁵ (100 x 1000 = 100,000). So logs turn multiplication into addition:

```
log10(a * b) = log10(a) + log10(b)
log10(a / b) = log10(a) - log10(b)
```

Check: log10(2 x 5) = log10(10) = 1, and log10(2) + log10(5) = 0.301 + 0.699 = 1.000. That is the whole trick behind decibels.

Some handy values to remember: log10(2) = 0.301, log10(3) = 0.477, log10(5) = 0.699, log10(sqrt 2) = 0.1505.

### 2. The decibel

For a **power** ratio:

```
dB = 10 * log10(P_out / P_in)
```

For a **voltage** (or current) ratio:

```
dB = 20 * log10(V_out / V_in)
```

Why 20 for voltages? Power goes as voltage squared (P = V² / R, Phase 03), and log10(x²) = 2 log10(x). So 10 log10(V²) = 20 log10(V): the factor 20 makes the voltage dB and the power dB agree for the same signal. A voltage that doubles is +6 dB, and its power, which quadruples, is also +6 dB. Same signal, same number.

**The table to remember** (voltage ratios):

| Ratio | dB | How to see it |
|---|---|---|
| 10 | +20 | 20 x log10(10) = 20 x 1 |
| 2 | +6.02 | 20 x 0.301 |
| sqrt 2 = 1.414 | +3.01 | 20 x 0.1505 |
| 1 | 0 | no change |
| 0.707 | -3.01 | the cutoff of an RC filter |
| 0.5 | -6.02 | half |
| 0.1 | -20 | a tenth |
| 0.01 | -40 | a hundredth |
| 0.001 | -60 | a thousandth |

**Going back** from dB to a ratio:

```
ratio = 10^(dB / 20)
```

-20 dB is 10^(-1) = 0.1. -3 dB is 10^(-0.15) = 0.708. +6 dB is 10^(0.3) = 1.995.

**Why "-3 dB point".** The cutoff of an RC filter has gain 0.707, which is -3.01 dB. For power, 0.707² = 0.5: at the cutoff the output power is half. That is why fc is also called the **half-power point** or the **-3 dB point**.

**Adding instead of multiplying.** Two stages with gains 0.1 and 0.5 have a total gain of 0.05. In dB: -20 + (-6) = -26 dB, and 20 log10(0.05) = -26.0 dB. Gains multiply, dB add. A chain of a microphone preamplifier (+40 dB), a filter (-3 dB), a volume control (-20 dB) and a power amplifier (+26 dB) has a total of 40 - 3 - 20 + 26 = +43 dB. No calculator needed.

### 3. Absolute levels: dBm and dBV

A dB value is a *ratio*. To describe an absolute level, pick a reference:

- **dBm**: power relative to 1 milliwatt. 1 mW = 0 dBm, 1 W = 30 dBm, 0.1 mW = -10 dBm, 0.5 W = +27 dBm. Radio and Wi-Fi powers are always quoted this way (a phone transmits up to about +23 dBm; a received Wi-Fi signal is often -50 to -80 dBm).
- **dBV**: voltage relative to 1 V. 0.1 V = -20 dBV. Audio line levels use dBV and a cousin, dBu (relative to 0.775 V).

### 4. The Bode plot

Hendrik Bode, at Bell Labs in the 1930s, popularised a way of drawing a filter's frequency response: **two graphs**, gain in dB on top, phase in degrees below, and **frequency on a logarithmic axis** at the bottom, so that 10 Hz, 100 Hz, 1 kHz, 10 kHz are equally spaced.

Take the RC low-pass, |H| = 1 / sqrt(1 + (f/fc)²), and convert to dB:

```
gain_dB = 20 log10(|H|) = -10 * log10(1 + (f/fc)^2)
```

Look at two regions:

- **Well below fc** (f/fc much less than 1): 1 + (f/fc)² is about 1, log10(1) = 0, so the gain is about **0 dB**. A flat line.
- **Well above fc** (f/fc much more than 1): 1 + (f/fc)² is about (f/fc)², so gain_dB is about -10 log10((f/fc)²) = **-20 log10(f/fc)**. Each decade (factor 10 in f) adds -20 dB. On the log axis that is a **straight line sloping down at -20 dB per decade**, which is the same as **-6 dB per octave**.

The two lines meet at f = fc (where -20 log10(1) = 0). They are the **asymptotes** of the curve. The true curve hugs them and is furthest from them exactly at the corner, by 3 dB:

```
 gain (dB)
   0 |--------------------.____                  <- asymptote 0 dB
     |                     \   \__
  -3 |                      *     \__            * real curve at fc: -3 dB
     |                       \       \__
 -20 |                        \         \__      <- -20 dB per decade
     |                         \           \__
 -40 |                          \             \
     +-----+-------+-------+-------+-------+---- f (log scale)
         fc/100  fc/10    fc     10 fc   100 fc
```

The phase plot has its own easy sketch: 0° well below fc, -45° at fc, -90° well above fc, with the transition happening over about one decade on each side of fc (from fc/10 to 10 fc).

**Worked example.** fc = 1591.5 Hz (R = 1 k, C = 100 nF):

| f | Asymptote | True value |
|---|---|---|
| 15.9 Hz (fc/100) | 0 dB | -0.00 dB |
| 159 Hz (fc/10) | 0 dB | -0.04 dB |
| 1592 Hz (fc) | 0 dB | -3.01 dB |
| 15.9 kHz (10 fc) | -20 dB | -20.04 dB |
| 159 kHz (100 fc) | -40 dB | -40.00 dB |

One decade away from the corner, the asymptote is already within 0.04 dB.

A high-pass is the mirror image: rising at +20 dB per decade up to fc, then flat at 0 dB; phase from +90° down to 0°.

### 5. Stacking stages

If you put two identical RC low-passes in a row, and the second does not load the first, the gains multiply, so the dB values add:

- At fc: -3 + (-3) = **-6 dB**.
- Far above fc: -20 + (-20) = **-40 dB per decade**. Twice as steep.

A filter with n first-order stages rolls off at -20 n dB per decade. That is called an **n-th order** filter.

But the "does not load" condition matters a lot. The second stage's resistor and capacitor form a load on the first stage's capacitor (Lesson 02, loading). With identical R and C, the first stage is pulled down, and the combined gain at the original fc is -9.5 dB instead of -6. The fix is a **buffer** between them: a stage that copies the voltage of the first stage's output without drawing any current from it. In real circuits that is an op-amp follower (Phase 13); in our simulator we use an ideal voltage-controlled voltage source (vcvs) with gain 1 (Phase 05, Lesson 08).

## Build It

### Step 1: Logarithms

```python
for value in [1, 10, 100, 1000, 0.1, 0.01, 2, 5, 0.5]:
    print(f"  log10({value:>5}) = {math.log10(value):+.3f}   check: 10^{math.log10(value):+.3f} = {10 ** math.log10(value):.3f}")
```

Each line raises 10 back to the log to show it really returns the original number. The last line checks log10(2 x 5) = log10(2) + log10(5) = 1.000.

### Step 2: Decibel conversions

```python
def voltage_db(ratio):
    return 20 * math.log10(ratio)


def power_db(ratio):
    return 10 * math.log10(ratio)


def db_to_voltage_ratio(db):
    return 10 ** (db / 20)
```

The output reproduces the table above. Note that "-3 dB" is really 0.7079 and "-6 dB" is 0.5012: engineers round -3.01 and -6.02 for convenience.

### Step 3: dBm

```python
def dbm(watts):
    return 10 * math.log10(watts / 1e-3)
```

1 mW is 0 dBm, 1 W is +30 dBm, 0.1 mW is -10 dBm, 0.5 W is +27.0 dBm.

### Step 4: The Bode plot of our RC low-pass

```python
def single_stage():
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    low_pass(c, "in", "out", "1")
    return c


sweep = single_stage().ac(np.logspace(1, 6, 501), source="V1")
gain_db = sweep.gain_db("out")
```

`gain_db` returns 20 log10 |V(out) / V(in)| at every frequency, and `gain_db_at(f, "out")` interpolates it at one frequency. Output:

```
  f =   1591.5 Hz:   -3.01 dB, asymptote   -0.00 dB
  f =  15915.5 Hz:  -20.04 dB, asymptote  -20.00 dB
  slope far above fc: -19.96 dB per decade, -5.99 dB per octave
  largest gap between the curve and the asymptotes: 2.99 dB
```

The largest gap is 3 dB, at the corner (2.99 because the sweep points do not land exactly on fc). `save_bode` draws both curves with matplotlib's `semilogx`, which puts the horizontal axis on a log scale: open `out.png` and you see the flat line, the corner and the straight -20 dB per decade slope, plus the phase sliding from 0° to -90° through -45° at fc.

### Step 5: Two stages, buffered and loaded

```python
def two_stages(buffered):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    low_pass(c, "in", "mid", "1")
    if buffered:
        c.vcvs("E1", "buf", "0", "mid", "0", 1.0)
        low_pass(c, "buf", "out", "2")
    else:
        low_pass(c, "mid", "out", "2")
    return c
```

`c.vcvs("E1", "buf", "0", "mid", "0", 1.0)` makes node buf equal to node mid without drawing any current from mid: an ideal buffer. Output:

```
  f =    1591.5 Hz: one stage   -3.01 dB, two x one =   -6.02 dB, buffered   -6.02 dB, loaded   -9.54 dB
  f =   15915.5 Hz: one stage  -20.04 dB, two x one =  -40.09 dB, buffered  -40.09 dB, loaded  -40.29 dB
  buffered slope: -39.9 dB per decade; buffered cutoff 1024 Hz, loaded cutoff 596 Hz
```

With the buffer, the dB add exactly. Without it, the circuit is still a second-order filter (far above fc it falls at -40 dB per decade too), but near the corner the loading costs an extra 3.5 dB and drags the -3 dB point down to 596 Hz. Notice also that two stacked stages each with fc = 1592 Hz have an overall -3 dB point of 1024 Hz, not 1592: each stage already loses 3 dB at 1592 Hz, so together they lose 6 dB there.

## Use It

- **Datasheets speak dB.** An op-amp's open-loop gain "100 dB" means 100,000. A filter IC's "stop-band attenuation 80 dB" means it cuts unwanted signals by 10,000 in voltage. An ADC's "SNR 74 dB" means the signal is about 5000 times the noise.
- **Audio.** Mixing desks mark faders in dB; "0 dB" is unity gain and -inf means off. A CD's 16-bit format has about 96 dB of dynamic range (20 log10 of 2^16 = 65,536).
- **Radio.** Cable loss is quoted in dB per metre (a coaxial cable might lose 0.2 dB/m at 1 GHz), so 30 m costs 6 dB, a quarter of the power. Link budgets add transmitter power (dBm), antenna gains (dBi) and path losses (dB) to predict received power.
- **Bode plots in control and power electronics.** The stability of a feedback loop (an op-amp circuit, a power supply's regulator) is judged from its Bode plot, by looking at the phase where the gain crosses 0 dB (Phases 13 and 18).
- **Measurement.** Audio analysers and network analysers sweep a sine through a circuit and draw its Bode plot directly, just like `c.ac(...)`.

## Try It in the Lab

Open **"Attenuate by exactly 20 dB"**. A 9 k ohm resistor sits at the top of a divider; choose the bottom part so the output is exactly -20 dB below the input (within 0.5 dB) at both 100 Hz and 10 kHz. First convert -20 dB to a plain ratio. Then for each part, compute the gain in dB at both frequencies. One part makes a good attenuator at one frequency only: which one, and why does that disqualify it?

## Common Mistakes

- **Using 10 log10 for voltages.** Voltage and current ratios use 20 log10; power ratios use 10 log10.
- **Adding dB of loaded stages.** dB add exactly only when each stage is unaffected by the next. Otherwise analyse the whole circuit at once (or buffer).
- **Taking the log of a negative number or of zero.** Gains in dB use the magnitude. A gain of exactly zero is "minus infinity dB".
- **Confusing dB and dBm.** "-3 dB" is a ratio; "-3 dBm" is an absolute power of 0.5 mW.
- **Reading a log axis as linear.** On a Bode plot the distance from 100 Hz to 1 kHz is the same as from 1 kHz to 10 kHz. Halfway between 100 Hz and 1 kHz is 316 Hz, not 550 Hz.
- **Expecting the asymptote to be exact at fc.** The true curve is 3 dB below the corner of the asymptotes.

## Exercises

1. **Easy.** Convert to dB: a voltage gain of 50, a voltage ratio of 0.02, a power ratio of 1000.
2. **Easy.** Convert to plain ratios: -12 dB, +26 dB, -0.5 dB (voltage).
3. **Medium.** A chain has a +34 dB preamp, a -6 dB cable loss, a filter at -1 dB in its pass band and a +20 dB power amp. The input is 2 mV. What is the output voltage?
4. **Medium.** Sketch the asymptotic Bode plot of an RC high-pass with fc = 300 Hz from 3 Hz to 30 kHz. What are the asymptotic and true gains at 30 Hz and 300 Hz?
5. **Hard.** For three identical buffered RC low-pass stages (fc = 1 kHz each), find the overall gain in dB at 1 kHz and the frequency where the overall gain is -3 dB. (Hint: each stage must lose 1 dB there; solve 10 log10(1 + x²) = 1.) Then add a third stage to `two_stages` and check.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Decibel | "dB, how loud" | A ratio on a log scale: 20 log10 for voltages, 10 log10 for powers |
| -3 dB point | "The cutoff" | The frequency where the voltage gain is 0.707 and the power is half |
| Decade / octave | "Ten times / twice the frequency" | Steps of 10x and 2x in frequency; a first-order roll-off is -20 dB/decade = -6 dB/octave |
| Bode plot | "The frequency response graph" | Gain in dB and phase in degrees against log frequency |
| Asymptote | "The straight-line approximation" | The lines the Bode curve approaches far from the corner; within 3 dB of the true curve |
| Filter order | "How steep it is" | The number of independent energy-storing elements; each adds -20 dB/decade of roll-off |
| dBm | "Power level" | Power relative to 1 mW: 10 log10(P / 1 mW) |

## Further Reading

- [All About Circuits: Decibels, in Volume III chapter 1 ("Amplifier gain") and the dB tutorials](https://www.allaboutcircuits.com/textbook/semiconductors/chpt-1/decibels/) — a gentle introduction with tables
- [Khan Academy: Introduction to logarithms](https://www.khanacademy.org/math/algebra2/x2ec2f6f830c9fb89:logs) — logs from first principles
- [MIT OpenCourseWare 6.003 Signals and Systems, Bode plot lectures](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/) — straight-line approximations and phase sketches
- [Analog Devices, *Linear Circuit Design Handbook* (Hank Zumbahlen, editor), chapter 8 "Analog Filters"](https://www.analog.com/en/resources/technical-books/linear-circuit-design-handbook.html) — dB and Bode plots as used by working engineers
