# Sampling and Nyquist

> An ADC only looks at the signal at separate instants. If the signal wiggles faster than half the sampling rate, the samples cannot tell it from a slower one, and it sneaks into your data in disguise. Sample fast enough, and filter out what is too fast, before the ADC.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 19 (Sensors and Signals), Lessons 01-03; Phase 09 (Alternating Current), Lesson 02 (Sine Waves, Frequency and Phase); Phase 10 (Filters and Resonance), Lessons 02-03 (RC Low-Pass and High-Pass, Decibels and Bode Plots); Phase 17 (Microcontrollers), Lessons 04-05 (ADC and DAC, Timers and Interrupts)
**Time:** ~85 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Sampling | Measuring a signal at separate, evenly spaced instants. | A film camera taking 24 photos per second. |
| Sample | One measurement, a number. | One frame of the film. |
| Sampling rate (fs) | How many samples per second, in hertz (samples/s). | The camera's frames per second. |
| Sampling period (Ts) | The time between samples: Ts = 1 / fs. | The time between frames. |
| Continuous signal | A signal that has a value at every instant. | The real moving scene. |
| Discrete-time signal | A list of samples, with nothing in between. | The strip of film. |
| Nyquist frequency | Half the sampling rate, fs / 2. The highest frequency the samples can represent unambiguously. | The fastest rotation a film can show correctly. |
| Aliasing | A frequency above fs / 2 appearing in the samples as a different, lower frequency. | Wagon wheels in old films seeming to turn slowly backwards. |
| Alias | The false frequency that appears. | The backwards wheel. |
| Folding | The way frequencies above Nyquist reflect back into the 0 to fs / 2 range. | A paper strip folded like an accordion. |
| Anti-aliasing filter | A low-pass filter before the ADC that removes frequencies above Nyquist. | Blurring a fast-moving scene so it cannot create false patterns. |
| Reconstruction | Rebuilding the continuous signal from its samples. | Projecting the film so motion looks smooth. |
| Spectrum (FFT) | The amounts of each frequency present in a signal; the FFT (fast Fourier transform) computes it from samples. | A graphic equaliser's bars on a stereo. |
| Oversampling | Sampling much faster than strictly needed, to ease the filter and reduce noise. | Filming at 240 fps to make slow motion clean. |

## Learning Objectives

- Compute the Nyquist frequency and predict the alias of any frequency for a given sampling rate
- Show with numbers that a 900 Hz tone and a 100 Hz tone give identical samples at 1000 samples/s
- Explain the sampling theorem: a signal with no content above fs / 2 can be perfectly rebuilt from its samples
- Measure, with an FFT, where noise above Nyquist lands after sampling
- Design a first-order RC anti-aliasing filter with our simulator's AC analysis and quantify how much alias it leaves

## The Problem

Your microcontroller samples a vibration sensor at 1000 samples per second, using a timer interrupt (Phase 17, Lesson 05). The machine vibrates at 20 Hz, which is easy to measure. But a switching power supply nearby leaks 950 Hz noise onto the sensor wire. You look at the samples and see a clean 20 Hz plus a strong, mysterious 50 Hz wobble. You check for 50 Hz mains hum, add shielding, change the power supply. Nothing helps, because there *is* no 50 Hz anywhere: it is the 950 Hz noise, aliased.

Aliasing is the sneakiest error in measurement because it is invisible after the fact: once sampled, the false frequency is indistinguishable from a real one. No software can remove it. The only fixes are to sample faster or to filter before sampling. This lesson shows why, and designs the filter.

## The Physics

There is no new physics here; this is about information. A sampled signal is a list of numbers taken every `Ts = 1 / fs` seconds. Between samples the ADC knows nothing. The question is: how much of the original signal can those numbers represent?

### Two different waves, the same samples

Take a cosine at frequency `f`, sampled at instants `t = n / fs` (n = 0, 1, 2, ...):

```
x[n] = cos(2 pi f n / fs)
```

Now take a second cosine at `f + fs`:

```
cos(2 pi (f + fs) n / fs) = cos(2 pi f n / fs + 2 pi n) = cos(2 pi f n / fs)
```

Adding `2 pi n` (a whole number of full turns) changes nothing. So `f` and `f + fs` give *exactly the same samples*. The same is true for `f + 2 fs`, `f - fs`, and, because cosine is symmetric (`cos(-a) = cos(a)`), for `fs - f`. With `fs = 1000` and `f = 100`:

```
100 Hz, 900 Hz, 1100 Hz, 1900 Hz, 2100 Hz, ...  all give identical samples
```

Read it as: "frequencies that differ by a whole multiple of the sampling rate, or that mirror each other around a multiple of it, are indistinguishable after sampling".

### Where does a frequency land?

The samples can only "show" frequencies from 0 to fs / 2. Any other frequency appears as:

```
f_alias = | f - fs x round(f / fs) |
```

Read it as: "subtract the nearest multiple of the sampling rate and take the size". At 1000 samples/s:

```
 600 Hz -> |600 - 1000| = 400 Hz
 900 Hz -> |900 - 1000| = 100 Hz
1100 Hz -> |1100 - 1000| = 100 Hz
2400 Hz -> |2400 - 2000| = 400 Hz
 950 Hz -> |950 - 1000| = 50 Hz
```

Picture the frequency axis folded like an accordion at every multiple of `fs / 2`: 0 to 500 Hz is the first panel, 500 to 1000 Hz folds back over it, 1000 to 1500 Hz folds forward again, and so on.

```
   0        500       1000      1500      2000   Hz
   |---------|---------|---------|---------|
   ---------->
             <----------
                       ---------->
                                 <----------
   all of it ends up between 0 and 500 Hz
```

## The Concept

### The sampling theorem

The other side of the story is the good news, known as the Nyquist-Shannon sampling theorem: **if a signal contains no frequencies at or above fs / 2, its samples contain all of its information**, and the continuous signal can be rebuilt exactly. The rebuilding recipe ("sinc interpolation") places a `sin(x) / x` shaped pulse at each sample and adds them up:

```
x(t) = sum over n of  x[n] x sinc(fs t - n),       sinc(u) = sin(pi u) / (pi u)
```

The script rebuilds a 300 Hz tone sampled at 1000 samples/s between the sample points and gets it right to four decimal places. Then it does the same for a 700 Hz tone, and rebuilds... a perfect 300 Hz tone. The samples were honest; the signal broke the rule.

So the rule for any measurement is: **fs must be more than twice the highest frequency present**, not just the highest frequency you care about. Noise counts.

### The film camera picture

A wheel with spokes turning at 23 revolutions per second, filmed at 24 frames per second, moves `23/24` of a turn per frame, which looks exactly like moving `1/24` of a turn *backwards*. That is aliasing to `-1` revolution per second. What the picture gets wrong: film cameras also blur moving objects (each frame lasts a while), which is a crude anti-aliasing filter; an ADC's sample-and-hold is much faster and does not blur.

### Anti-aliasing filters

Since aliasing cannot be undone after sampling, we remove the offending frequencies before it: a **low-pass filter** in front of the ADC, passing the useful band and attenuating everything near and above fs / 2.

The simplest is the RC low-pass of Phase 10, Lesson 02:

```
  sensor ---[ R ]---+---> ADC
                    |
                   === C
                    |
                   gnd
```

```
f_c = 1 / (2 pi R C)
gain at frequency f = 1 / sqrt(1 + (f / f_c)^2)
```

Read it as: "the cutoff is one over two pi R C; above it, the gain falls, by about a factor of 10 (20 dB) for every factor of 10 in frequency". Decibels (Phase 10, Lesson 03): `gain_dB = 20 log10(gain)`.

For our 20 Hz signal and 950 Hz noise at 1000 samples/s:

| RC | Cutoff | Gain at 20 Hz | Gain at 950 Hz | Alias left |
|----|--------|---------------|----------------|------------|
| 1.6 k + 1 uF | 99.5 Hz | -0.17 dB | -19.6 dB | 10.4% |
| 16 k + 1 uF | 9.9 Hz | -7.0 dB | -39.6 dB | 1.0% |
| 160 k + 1 uF | 1.0 Hz | -26 dB | -59.6 dB | 0.1% |

The first-order filter is a compromise: placing the cutoff low enough to kill the noise also eats the signal. With 1.6 k and 1 uF the signal is almost untouched and the 950 Hz noise is cut to about a tenth: the false 50 Hz wobble shrinks from 0.50 to 0.05. Better than nothing, but not great.

### Doing better

- **Sample faster (oversampling).** At 10 000 samples/s, Nyquist is 5 kHz. The 950 Hz noise is now *below* Nyquist: it does not alias at all; it is just a 950 Hz component that a digital filter (Lesson 07) can remove after sampling. The analog filter only has to stop things above 5 kHz, which a single RC with its cutoff a decade above the signal does well. This is why modern designs sample much faster than "twice the signal" and then filter and decimate digitally.
- **Higher-order filters.** Two or more RC stages, or the active filters of Phase 13, Lesson 06 (a second-order Sallen-Key falls 40 dB per decade), separate pass and stop bands more sharply.
- **Remove the noise at the source**: shielding, layout, a quieter power supply (Phase 21).

### Worked example: aliasing by hand

Sample a 600 Hz cosine and a 400 Hz cosine at 1000 samples/s. The phase advances by `360 x f / fs` degrees per sample:

```
600 Hz: 360 x 600 / 1000 = 216 degrees per sample
400 Hz: 360 x 400 / 1000 = 144 degrees per sample

 n   600 Hz angle   cos      400 Hz angle   cos
 0        0        +1.000         0        +1.000
 1      216        -0.809       144        -0.809
 2      432 = 72   +0.309       288        +0.309
 3      648 = 288  +0.309       432 = 72   +0.309
 4      864 = 144  -0.809       576 = 216  -0.809
```

Identical, because 216 degrees forwards is the same as 144 degrees backwards, and a cosine does not care about direction. A frequency above Nyquist turns more than half a circle per sample, and the samples cannot tell "more than half forwards" from "less than half backwards".

### Worked example: why audio cannot use an RC

CD audio keeps up to 20 kHz and samples at 44.1 kHz: Nyquist is 22.05 kHz. To prevent audible aliases, everything above 22.05 kHz must be reduced by roughly the converter's dynamic range, about 90 dB. A first-order RC falls 20 dB per decade (6 dB per octave). From 20 kHz to 22.05 kHz is a tenth of an octave: an RC would attenuate by well under 1 dB there. Getting 90 dB in that gap needs a filter falling hundreds of dB per octave, which no simple analog circuit can do.

The solution used everywhere since the 1990s: **oversample**. Sample at, say, 64 x 44.1 kHz = 2.8 MHz. Now Nyquist is 1.4 MHz, and a gentle analog filter easily removes everything up there. A sharp *digital* filter (Lesson 07) then removes 20 kHz to 1.4 MHz, and the data is reduced back to 44.1 kHz.

### Worked example: choosing fs for a sensor

An accelerometer on a machine must capture vibrations up to 200 Hz. A first-order RC anti-aliasing filter will be placed at about 300 Hz (so 200 Hz loses only `20 log10(1 / sqrt(1 + (200/300)^2)) = -1.6 dB`). We want anything that could alias into 0-200 Hz to be at least 30 dB down. Frequencies that land in 0-200 Hz after sampling are those within 200 Hz of a multiple of fs, the first being `fs - 200`. With 20 dB per decade above 300 Hz, 30 dB needs a factor of about 31.6 above 300 Hz, that is about 9.5 kHz:

```
fs - 200 Hz >= 9.5 kHz   ->   fs >= 9.7 kHz         (choose 10 kHz)
```

Fifty times the highest frequency of interest: oversampling is the price of using a cheap one-resistor-one-capacitor filter.

### Worked example: timing jitter is a noise too

If the samples are not exactly evenly spaced, each one is taken a little early or late. For a sine of amplitude A and frequency f, the steepest slope is `2 pi f A` volts per second, so a timing error `dt` causes a voltage error up to:

```
error ~ 2 pi f A dt
```

A 1 kHz, 1 V sine sampled from a busy main loop whose timing wanders by 1 us: `2 pi x 1000 x 1 x 1e-6 = 6.3 mV`, almost 8 LSB of a 12-bit, 3.3 V ADC. Triggered by a hardware timer, the jitter falls to nanoseconds and the error to microvolts. That is the numerical reason for Phase 17's advice to sample from a timer.

## Build It

### Step 1: Sampling and the alias formula

```python
def sample(frequency, rate, seconds, phase=0.0, amplitude=1.0):
    n = np.arange(int(round(rate * seconds)))
    return amplitude * np.cos(2 * np.pi * frequency * n / rate + phase)


def alias_of(frequency, rate):
    return abs(frequency - rate * round(frequency / rate))
```

### Step 2: Let the FFT find the frequency

`strongest_frequency` multiplies one second of samples by a Hann window (to reduce leakage), takes the FFT with `np.fft.rfft`, and returns the frequency of the biggest peak. The script compares it with the alias formula for seven tones.

### Step 3: Identical samples, and rebuilding

The script prints six samples of a 900 Hz and a 100 Hz cosine side by side, then rebuilds 300 Hz and 700 Hz tones with `sinc_reconstruct`.

### Step 4: The anti-aliasing filter in the simulator

```python
def rc_lowpass_gain(ohms, farads, frequencies):
    circuit = Circuit()
    circuit.voltage_source("VIN", "in", "0", 0.0)
    circuit.resistor("R1", "in", "out", ohms)
    circuit.capacitor("C1", "out", "0", farads)
    result = circuit.ac(np.asarray(frequencies, float), source="VIN")
    return np.abs(np.asarray(result.v("out")))
```

The AC analysis of Phase 10, Lesson 08 drives VIN with a 1 V phasor at each frequency; the magnitude of `v("out")` is the gain. The script then builds one second of samples of signal plus noise, scaled by those gains, and reads the 20 Hz and 50 Hz bins of the spectrum with and without the filter.

Run it:

```
uv run python phases/19-sensors-and-signals/04-sampling-and-nyquist/code/main.py
```

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
Sampling at 1000 samples per second: the Nyquist frequency is 500 Hz
      tone  alias formula  FFT of the samples says
    100 Hz         100 Hz                  100 Hz
    400 Hz         400 Hz                  400 Hz
    600 Hz         400 Hz                  400 Hz
    900 Hz         100 Hz                  100 Hz
   1100 Hz         100 Hz                  100 Hz
   1900 Hz         100 Hz                  100 Hz
   2400 Hz         400 Hz                  400 Hz

The first samples of a 900 Hz tone and of a 100 Hz tone, both at 1000 samples/s
  n = 0: t =   0 ms   900 Hz -> +1.0000   100 Hz -> +1.0000
  n = 1: t =   1 ms   900 Hz -> +0.8090   100 Hz -> +0.8090
  n = 2: t =   2 ms   900 Hz -> +0.3090   100 Hz -> +0.3090
  n = 3: t =   3 ms   900 Hz -> -0.3090   100 Hz -> -0.3090
  n = 4: t =   4 ms   900 Hz -> -0.8090   100 Hz -> -0.8090
  n = 5: t =   5 ms   900 Hz -> -1.0000   100 Hz -> -1.0000
  identical: after sampling, nothing can tell them apart

Rebuilding a 300 Hz tone from its samples (sinc interpolation) between the sample points
  largest error over 10 ms in the middle: 0.0000 (amplitude 1)
  the same for a 700 Hz tone: the rebuilt wave matches a 300 Hz tone to within 0.0000

A 20 Hz sensor signal plus switching noise at 950 Hz, sampled at 1000 samples/s
  the noise aliases to 50 Hz, inside the band we care about (0-100 Hz)
         RC filter   cutoff  gain at 20 Hz  gain at 950 Hz  alias left
...
```

## Use It

- **Audio:** CDs sample at 44.1 kHz so that everything up to about 20 kHz (the limit of hearing) is below the 22.05 kHz Nyquist frequency, with a little room for the anti-aliasing filter. Professional audio uses 48 or 96 kHz.
- **Microcontroller ADCs** are usually triggered by a timer (Phase 17, Lesson 05) so that samples are evenly spaced; uneven spacing (jitter) adds its own errors.
- **Delta-sigma ADCs** (the 24-bit converters in scales and audio chips) sample at MHz rates and filter digitally, so their anti-aliasing filter can be a simple RC.
- **Oscilloscopes** suffer aliasing too: a scope set to a slow timebase may show a fast signal as a slow, false wave. If a waveform looks strange, change the timebase and see if it changes in a way it should not.
- **Datasheets** of ADCs recommend an RC at the input (for example 100 ohm and a few nF) both as anti-aliasing filter and as a charge reservoir for the sample-and-hold (Phase 17, Lesson 04).

## Try It in the Lab

The lab is an anti-aliasing RC with a fixed 100 nF capacitor in front of an ADC sampling at 10 000 samples per second. The useful signal is below 100 Hz. Choose the resistor so the signal at 100 Hz loses less than 1 dB but frequencies at the 5 kHz Nyquist limit are attenuated by at least 12 dB. Compute `f_c = 1 / (2 pi R C)` for each candidate, and use the gain formula at both frequencies before running it.

## Common Mistakes

- **"Twice the highest frequency I care about" is enough.** It must be twice the highest frequency *present*, including noise and interference. Filter first.
- **Filtering after the ADC to remove aliases.** Once aliased, the false frequency sits in the band with the real signal. Digital filters cannot separate them.
- **Putting the RC cutoff right at the signal frequency.** At the cutoff, the signal is already 3 dB down (70%).
- **Assuming exactly fs / 2 is fine.** At exactly Nyquist, the samples depend on the phase: a cosine might be sampled at its peaks or at its zero crossings. Stay strictly below.
- **Uneven sampling.** Taking samples in a busy main loop instead of from a timer makes the intervals vary, which smears frequencies.
- **Forgetting the source impedance.** The RC's R adds to the sensor's own output impedance; the ADC must still be able to charge its sample capacitor through it.

## Exercises

1. A signal is sampled at 8000 samples/s. What is the Nyquist frequency? Where do 3 kHz, 5 kHz, 7 kHz and 9 kHz appear? (4 kHz; 3, 3, 1 and 1 kHz.)
2. A wheel turns at 26 revolutions per second, filmed at 24 frames per second. What do you see? (2 revolutions per second forwards.)
3. An RC has R = 3.3 kohm and C = 47 nF. Find f_c and the gain in dB at 10 kHz. (1026 Hz; -19.8 dB.)
4. In `main.py`, change the sampling rate to 10 000 samples/s. Where does the 950 Hz noise appear now? Is it still an alias? (At 950 Hz: it is below the new 5 kHz Nyquist frequency, so it is a real, correctly sampled component that a digital filter can remove.)
5. Harder: add a second identical RC stage (buffered, so the stages do not load each other, or simply multiply the two gains). How much does the 950 Hz noise drop now with 1.6 k and 1 uF, and how much extra does the 20 Hz signal lose? Compare with the first-order table.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Sampling rate | "Speed of the ADC" | Samples per second, fs |
| Nyquist frequency | "The limit" | fs / 2: the highest frequency the samples can represent |
| Aliasing | "Weird low frequency" | A frequency above fs / 2 showing up as \|f - k fs\| |
| Sampling theorem | "Sample at twice" | A signal with no content at or above fs / 2 is fully described by its samples |
| Anti-aliasing filter | "Input filter" | An analog low-pass before the ADC that removes content above fs / 2 |
| Oversampling | "Sampling faster" | Sampling far above the minimum to ease the analog filter and filter digitally |
| FFT | "The spectrum" | A fast algorithm for the frequency content of a list of samples |

## Further Reading

- [Steven W. Smith, *The Scientist and Engineer's Guide to Digital Signal Processing*, Chapter 3 (ADC and DAC)](https://www.dspguide.com/ch3.htm) — sampling, aliasing and anti-aliasing filters, free online
- [Analog Devices, MT-002 "What the Nyquist Criterion Means to Your Sampled Data System Design"](https://www.analog.com/media/en/training-seminars/tutorials/MT-002.pdf) — aliasing zones and filter requirements
- [Texas Instruments, SBAA282 "Antialiasing Filter Circuit Design for Single-Ended ADC Input Using Fixed Cutoff Frequency" (Analog Engineer's Circuit)](https://www.ti.com/lit/pdf/sbaa282) — practical RC values in front of ADCs
- Claude E. Shannon, "Communication in the Presence of Noise", *Proceedings of the IRE*, 1949 — the original statement of the sampling theorem
