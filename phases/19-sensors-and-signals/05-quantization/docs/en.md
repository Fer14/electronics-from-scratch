# Quantization

> An ADC rounds every sample to the nearest step. The rounding error behaves like a little noise of size LSB / sqrt(12), which is where the famous "6 dB per bit" comes from; and, strangely, a bit of real noise can help you see below one step.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 19 (Sensors and Signals), Lesson 04 (Sampling and Nyquist); Phase 17 (Microcontrollers), Lesson 04 (ADC and DAC); Phase 09 (Alternating Current), Lesson 03 (RMS Values); Phase 10 (Filters and Resonance), Lesson 03 (Decibels and Bode Plots)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Quantization | Rounding a value that could be anything to one of a fixed set of levels. | Rounding prices to the nearest 5 cents. |
| Quantization step (LSB) | The distance between two neighbouring levels: VREF / 2^N. | 5 cents. |
| Quantization error | The difference between the rounded value and the true value; between -LSB/2 and +LSB/2. | The 0-2.5 cents you gain or lose on each rounded price. |
| Quantization noise | Quantization error viewed as a random signal added to the input. | The jitter in your shopping bill from all the roundings. |
| RMS | Root mean square: the "effective" size of a varying quantity, the square root of the average of its squares (Phase 09, Lesson 03). | The typical size of the roundings. |
| Signal-to-noise ratio (SNR) | Signal power divided by noise power, usually in decibels. | How loud a voice is compared with the room's background noise. |
| SQNR | Signal-to-quantization-noise ratio: the SNR when the only noise is quantization. | The voice compared with the rounding hiss only. |
| SINAD | Signal-to-noise-and-distortion ratio: SNR counting every error of the converter. | The voice compared with all the hiss and crackle. |
| ENOB | Effective number of bits: how many bits an ideal converter would need to match a real one's SINAD. | The honest price of a "16-bit" converter that behaves like a 13-bit one. |
| Harmonic distortion | Unwanted copies of a signal at 2, 3, 4... times its frequency, created by a non-linear process. | Overtones added by an overdriven guitar amplifier. |
| Dither | Small random noise added on purpose before quantizing, so averaging can resolve values between the steps. | Shaking a sieve so small grains find their way through. |

## Learning Objectives

- Quantize a signal with N bits and show that the error is spread evenly between -LSB/2 and +LSB/2
- Derive the RMS quantization error LSB / sqrt(12) and the full-scale sine SQNR of 6.02 N + 1.76 dB, and confirm both numerically
- Convert a measured SINAD into an effective number of bits
- Explain why quantizing a very small signal produces harmonic distortion
- Use dither to measure a voltage to a fraction of an LSB by averaging, and explain why averaging alone cannot do it

## The Problem

Phase 17, Lesson 04 met the ADC as a box that outputs `floor(Vin / LSB)`. That rounding throws information away. How much? Is a 10-bit ADC good enough for audio? Why do datasheets for a "16-bit" ADC quote "13.8 effective bits"? And a puzzle: you read a constant voltage 4096 times and average the readings, hoping to get a much finer value than one step; the average is exactly the same code every time, and averaging gains nothing. Yet the same averaging works beautifully on a slightly noisy signal.

This lesson answers these with the right way of thinking about rounding: as a small, predictable noise added to every sample.

## The Physics

Nothing physical here: quantization is arithmetic. The input could be any voltage; the output can only be one of `2^N` codes. The real-world consequence is that the converter adds an error to every sample, and its size is set by N and VREF alone.

## The Concept

### The error is between -LSB/2 and +LSB/2

If we read a code back as the *middle* of its interval, `(code + 0.5) x LSB`, the error is never bigger than half a step:

```
-LSB/2  <=  error  <=  +LSB/2
```

For an 8-bit converter on 3.3 V, `LSB = 3.3 / 256 = 12.89 mV`, so every reading is within 6.4 mV of the truth (ignoring every other error).

When the input moves around by many steps (a sensor varying, an audio signal), the error at each sample is essentially unpredictable and equally likely to be anywhere in that interval. The simulation sweeps a slow ramp through the whole range and counts: the error lands in five equal sub-intervals 20% of the time each. A **uniform** distribution.

### How big is it on average: LSB / sqrt(12)

The RMS of a uniform distribution between `-a` and `+a` is found by averaging `x^2` over the interval:

```
mean of x^2 = (1 / 2a) x integral from -a to a of x^2 dx = (1 / 2a) x (2 a^3 / 3) = a^2 / 3
RMS = sqrt(a^2 / 3) = a / sqrt(3)
```

With `a = LSB / 2`:

```
RMS error = (LSB / 2) / sqrt(3) = LSB / sqrt(12) = 0.2887 x LSB
```

Read it as: "the typical size of the rounding error is about 29% of one step". For our 8-bit converter: `12.891 / 3.464 = 3.721 mV`. The simulation measures 3.720 mV.

### The 6.02 N + 1.76 dB rule

Compare that noise with the biggest sine the converter can represent: amplitude `A = VREF / 2` (from 0 to VREF). A sine's RMS is `A / sqrt(2)` (Phase 09, Lesson 03), so its power (RMS squared) is `A^2 / 2`. With `VREF = 2^N x LSB`, `A = 2^(N-1) x LSB`:

```
signal power = (2^(N-1) x LSB)^2 / 2 = 2^(2N) x LSB^2 / 8
noise power  = LSB^2 / 12
SQNR = signal power / noise power = 2^(2N) x 12 / 8 = 1.5 x 2^(2N)
```

In decibels (`10 log10` of a power ratio):

```
SQNR_dB = 10 log10(1.5) + 2N x 10 log10(2) = 1.76 + 6.02 N
```

Read it as: "each extra bit adds 6 dB of signal-to-noise ratio, plus a constant 1.76 dB". So:

| Bits | SQNR | What it is used for |
|------|------|---------------------|
| 8 | 49.9 dB | simple control, old telephone audio |
| 10 | 62.0 dB | microcontroller ADCs |
| 12 | 74.0 dB | microcontroller ADCs, oscilloscopes |
| 16 | 98.1 dB | CD audio |
| 24 | 146 dB | high-end audio and weighing (never reached in practice) |

The simulation quantizes a sine that is one LSB less than full scale (to avoid clipping) and measures the error power directly. From 8 bits up it agrees within a fraction of a dB; at 4 bits it is about 1.7 dB lower, because "one LSB less" is a noticeable part of a 16-level signal.

Two practical consequences: the formula is for a **full-scale** signal (a signal using a tenth of the range loses 20 dB), and it assumes quantization is the only noise.

### Real converters: SINAD and ENOB

A real ADC also has thermal noise, reference noise, non-linearity and clock jitter. Datasheets report the total as SINAD and turn it into **effective bits** by running the formula backwards:

```
ENOB = (SINAD - 1.76) / 6.02
```

In the simulation, a 12-bit converter whose input also carries 1 LSB RMS of extra noise has a SINAD of 62.8 dB, so `ENOB = (62.8 - 1.76) / 6.02 = 10.1`. Two of its bits are lost in the noise.

### Small signals: quantization becomes distortion

The "uniform noise" picture assumes the signal crosses many levels. A signal smaller than about one LSB only toggles between two or three codes; the output becomes a crude square-ish wave whose error is strongly tied to the signal itself. That is **distortion**: in the spectrum, new tones appear at 3, 5, 7 times the signal frequency. The simulation feeds an 8-bit quantizer a sine of 0.7 LSB amplitude: the third harmonic is only 8 dB below the fundamental. In audio, quiet passages quantized this way sound gritty.

### Dither: noise that helps

Now the averaging puzzle. A constant voltage of 127.163 LSB (from a thermistor divider in our simulator) always rounds to the same code. Average 4096 identical codes and you get that same code: an error of 0.34 LSB, no matter how many readings you take.

Add a little random noise (about half an LSB RMS) *before* the quantizer. Now the input sometimes falls below the threshold between codes and sometimes above, in proportion to where the true value sits between them. The *average* of the codes then lands close to the true value:

```
no noise:          average 127.500 LSB   error +0.337 LSB
0.5 LSB noise:     average 127.172 LSB   error +0.010 LSB
1 LSB noise:       average 127.192 LSB   error +0.029 LSB
```

This is **dither**. Each single reading got worse; the average got much better. Too much noise and you need more readings to average it away (Lesson 06 shows the averaging rule: noise falls as one over the square root of the number of readings). Dither also breaks up the small-signal distortion above, turning it back into benign noise. Many real signals already carry enough noise to dither themselves; high-resolution designs sometimes add it on purpose.

### Worked example: a toy 3-bit ADC by hand

To see every number, imagine a 3-bit converter with VREF = 8 V. Then `LSB = 8 / 2^3 = 1 V`, and there are 8 codes, 0 to 7, each covering one volt:

```
code:      0      1      2      3      4      5      6      7
covers:  0-1 V  1-2 V  2-3 V  3-4 V  4-5 V  5-6 V  6-7 V  7-8 V
read as: 0.5 V  1.5 V  2.5 V  3.5 V  4.5 V  5.5 V  6.5 V  7.5 V
```

Quantize three inputs:

```
input 2.3 V:  floor(2.3 / 1) = 2   ->  read back 2.5 V   error +0.2 V
input 5.9 V:  floor(5.9 / 1) = 5   ->  read back 5.5 V   error -0.4 V
input 7.6 V:  floor(7.6 / 1) = 7   ->  read back 7.5 V   error -0.1 V
```

Every error is between -0.5 V and +0.5 V (half an LSB). Its RMS over many varied inputs would be `1 / sqrt(12) = 0.29 V`, and a full-scale sine (4 V amplitude around 4 V) would have an SQNR of `6.02 x 3 + 1.76 = 19.8 dB`: a signal only about ten times bigger than its rounding noise. A real 12-bit converter is the same picture with 4096 much finer steps.

### Worked example: how many bits for a kitchen scale?

A scale must weigh up to 5 kg and show single grams. That is 5000 distinguishable steps, so at least:

```
2^12 = 4096   (too few)
2^13 = 8192   (enough)
```

13 bits of *effective* resolution, not nominal. Lesson 06 shows that the load cell and its amplifier add noise; if that noise is 2 LSB RMS on a 16-bit converter, the ENOB is about 14, still enough. In practice scale makers use 24-bit sigma-delta converters (like the HX711), average many readings, and display a stable 1 g.

### Worked example: SQNR of a signal that does not fill the range

A 12-bit ADC (ideal SQNR 74 dB) measures a sine of amplitude 0.33 V on a 3.3 V range. The full-scale amplitude would be 1.65 V, so the signal is 5 times smaller:

```
loss = 20 log10(1.65 / 0.33) = 20 log10(5) = 14 dB
SQNR = 74.0 - 14.0 = 60.0 dB       (like an ideal 9.7-bit converter)
```

That is the quantization argument for the conditioning of Lesson 03: amplify the signal to fill the range and you get those bits back.

### Worked example: why dither works, with probabilities

The true input is 127.163 LSB. Code 127 covers 127.0 to 128.0 LSB and is read back as 127.5; code 126 is read as 126.5, code 128 as 128.5. Add Gaussian noise of 0.5 LSB RMS. How often does each code appear? Measure the distance to each threshold in units of the noise:

```
below 127.0:  (127.0 - 127.163) / 0.5 = -0.33 noise widths   ->  probability 37.2%   (reads 126.5)
above 128.0:  (128.0 - 127.163) / 0.5 = +1.67 noise widths   ->  probability  4.7%   (reads 128.5)
in between:                                                      probability 58.1%   (reads 127.5)
```

(The probabilities come from the bell-shaped normal distribution: 37.2% of it lies more than 0.33 widths below the middle, 4.7% more than 1.67 widths above.) The expected average reading is:

```
0.372 x 126.5 + 0.581 x 127.5 + 0.047 x 128.5 = 47.06 + 74.08 + 6.04 = 127.18 LSB
```

Within 0.02 LSB of the truth. The noise turned "which code" into "how often each code", and the proportions carry the information that a single code throws away. The simulation, with 4096 real random readings, got 127.172.

### Worked example: the error is not always LSB / sqrt(12)

The "uniform error" model needs the signal to move across many codes between samples. Three cases where it fails:

- **A steady DC input:** the error is one fixed number (0.337 LSB above), not noise at all.
- **A sine whose frequency divides the sampling rate evenly:** the same few input values repeat every cycle, so the error repeats too and appears as harmonics, not as a flat noise floor. That is why the test sine in `main.py` uses 127 cycles in 8192 samples (127 is prime, so the samples never repeat exactly).
- **A tiny signal:** as shown above, the error is strongly tied to the signal.

In all three, a little noise (natural or added dither) restores the uniform-noise behaviour.

## Build It

### Step 1: A quantizer

```python
def quantize(volts, bits, vref=VREF):
    lsb = vref / 2 ** bits
    codes = np.clip(np.floor(volts / lsb), 0, 2 ** bits - 1)
    return codes, (codes + 0.5) * lsb
```

It returns the codes and the reconstructed voltages at the middle of each interval.

### Step 2: The error of a ramp

A ramp of 100 001 points through the full range gives the error's extremes, RMS and histogram.

### Step 3: SQNR of a sine

`sine_test(bits)` quantizes 8192 samples of a near-full-scale sine with 127 cycles in the record (a prime number of cycles, so the samples do not repeat and the error is spread across many levels), and computes `10 log10(signal power / error power)`. An optional extra noise turns it into a SINAD test.

### Step 4: Distortion and dither

The tiny sine's spectrum is read at the harmonics with `np.fft.rfft`. For dither, the true value comes from a divider solved by `sim`, and Gaussian noise of a chosen RMS (fixed seed) is added before quantizing.

Run it:

```
uv run python phases/19-sensors-and-signals/05-quantization/code/main.py
```

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
An 8-bit quantizer on 3.3 V: 256 codes, LSB = 12.891 mV
  error on a slow ramp: min -0.500 LSB, max +0.500 LSB
  RMS error 3.720 mV, theory LSB / sqrt(12) = 3.721 mV
  the error is spread evenly: fractions in 5 equal bins [0.199 0.2   0.2   0.2   0.2  ]

Signal-to-quantization-noise ratio of a full-scale sine
  bits   measured  6.02 N + 1.76
     4    24.12 dB       25.84 dB
     6    37.33 dB       37.88 dB
     8    49.72 dB       49.92 dB
    10    61.87 dB       61.96 dB
    12    73.98 dB       74.00 dB
    16    98.34 dB       98.08 dB

A 12-bit ADC whose input also carries 1 LSB RMS of noise
  measured SINAD 62.82 dB -> effective number of bits (SINAD - 1.76) / 6.02 = 10.14

A tiny sine (amplitude 0.7 LSB) through an 8-bit quantizer becomes a square-ish wave
  codes used: [99, 100, 101]
  harmonic 1:     0.0 dB relative to the fundamental
  harmonic 3:    -8.0 dB relative to the fundamental
  harmonic 5:   -16.2 dB relative to the fundamental
  harmonic 7:   -14.2 dB relative to the fundamental

Dither: averaging cannot beat the LSB unless there is some noise
  a thermistor divider (10 k over 9.87 k) gives 1.63920 V = 127.163 LSB
  no noise          : average of 4096 readings  127.500 LSB, error +0.337 LSB
  0.5 LSB RMS noise : average of 4096 readings  127.172 LSB, error +0.010 LSB
  1 LSB RMS noise   : average of 4096 readings  127.192 LSB, error +0.029 LSB
```

## Use It

- **Choosing an ADC:** if the signal needs 60 dB of dynamic range, a 10-bit converter is the bare minimum; leave margin for signals that do not reach full scale and for real noise.
- **Datasheets** list SNR, SINAD, THD (total harmonic distortion), SFDR (spurious-free dynamic range) and ENOB, usually measured with a full-scale sine at a stated frequency. Compare converters by ENOB, not by their nominal bits.
- **Oversampling and averaging** is how many microcontrollers get 12 or 14 useful bits from a 10-bit ADC: sample 16 times faster and average 16 readings for about 2 more bits, *provided* there is enough noise (or deliberate dither) to keep the codes moving. Microchip and Silicon Labs application notes describe exactly this.
- **Audio** is mastered at 24 bits and then dithered (with carefully shaped noise) when reduced to 16 bits for distribution, to avoid the gritty distortion of quiet passages.
- **Images** show quantization as "banding" in smooth gradients like a sky; dithering patterns hide it.

## Common Mistakes

- **Believing more bits always means more accuracy.** Bits set the quantization noise; the reference, offsets and real noise often dominate (ENOB).
- **Forgetting the signal level.** The 6.02 N + 1.76 dB is for a full-scale sine. A signal at -20 dBFS (a tenth of full scale) has 20 dB less.
- **Averaging a perfectly steady input to get more resolution.** Without noise or dither, every reading is identical; averaging gains nothing.
- **Adding too much dither.** It costs more readings to average out. About half to one LSB RMS is typical.
- **Confusing LSB/2 (the maximum error) with LSB / sqrt(12) (the RMS error).**
- **Ignoring distortion for tiny signals.** Below a few LSB, quantization error is correlated with the signal and shows up as harmonics.

## Exercises

1. A 14-bit ADC has VREF = 2.5 V. What are its LSB and its RMS quantization noise? (0.153 mV; 44 uV.)
2. What is the ideal SQNR of a 14-bit converter? Of a 20-bit one? (86.0 dB; 122.2 dB.)
3. A datasheet says SINAD = 70 dB for a "14-bit" ADC. What is its ENOB? (11.3 bits.)
4. A signal reaches only a quarter of the ADC's full scale. How many dB of SQNR does it lose? How many bits is that worth? (12 dB, about 2 bits.)
5. Harder: in `main.py`, measure how the error of the dithered average falls as you take 64, 256, 1024 and 4096 readings with 0.5 LSB of noise. Plot or print error versus number of readings and check that it roughly halves every time the number of readings is multiplied by 4.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| LSB | "One count" | VREF / 2^N, the quantization step |
| Quantization noise | "Rounding error" | The error treated as uniform noise of RMS LSB / sqrt(12) |
| SQNR | "6 dB per bit" | 6.02 N + 1.76 dB for a full-scale sine and an ideal converter |
| SINAD | "Real SNR" | Signal over all noise and distortion of a real converter |
| ENOB | "Real bits" | (SINAD - 1.76) / 6.02 |
| Dither | "Adding noise" | Small noise before quantization so that averaging can resolve below one LSB |
| Harmonic distortion | "Grit" | Tones at multiples of the signal frequency from a non-linear process |

## Further Reading

- [Analog Devices, MT-001 "Taking the Mystery out of the Infamous Formula, SNR = 6.02N + 1.76 dB"](https://www.analog.com/media/en/training-seminars/tutorials/MT-001.pdf) — the derivation and its assumptions
- [Analog Devices, MT-003 "Understand SINAD, ENOB, SNR, THD, THD + N, and SFDR"](https://www.analog.com/media/en/training-seminars/tutorials/MT-003.pdf) — the datasheet metrics explained
- [Steven W. Smith, *The Scientist and Engineer's Guide to Digital Signal Processing*, Chapter 3](https://www.dspguide.com/ch3/1.htm) — quantization and dithering, free online
- [Silicon Labs, AN118 "Improving ADC Resolution by Oversampling and Averaging"](https://www.silabs.com/documents/public/application-notes/an118.pdf) — practical oversampling with noise
