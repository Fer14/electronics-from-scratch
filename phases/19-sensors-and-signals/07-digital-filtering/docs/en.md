# Digital Filtering

> Once a signal is a list of numbers, a filter is just arithmetic: a weighted sum of recent samples. The moving average, the exponential average (an RC in one line of code) and the windowed-sinc FIR cover most of what a sensor ever needs.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 19 (Sensors and Signals), Lessons 04-06; Phase 10 (Filters and Resonance), Lessons 01-03 (What a Filter Does, RC Low-Pass and High-Pass, Decibels and Bode Plots); Phase 07 (Capacitors), Lesson 08 (Transient Simulation from Scratch)
**Time:** ~90 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Digital filter | A calculation that turns one list of samples into another, keeping some frequencies and removing others. | A recipe that turns raw ingredients into a smoother sauce. |
| Moving average | Each output is the plain average of the last N inputs. | The average of your last N exam marks. |
| Exponential moving average (EMA) | Each output moves a fixed fraction alpha of the way from the previous output towards the new input. | A mood that shifts a little towards each new piece of news. |
| Smoothing factor (alpha) | The fraction, between 0 and 1, used by an EMA; small alpha means heavy smoothing. | How easily swayed you are. |
| FIR filter | Finite impulse response: the output is a weighted sum of a fixed number of recent inputs. Moving averages are FIR. | A committee with a fixed number of members, each with its own vote weight. |
| IIR filter | Infinite impulse response: the output also depends on previous outputs (feedback), so it remembers forever, fading. The EMA is IIR. | A rumour that keeps echoing, more faintly each time. |
| Taps / kernel | The list of weights of an FIR filter. | The committee's vote weights. |
| Impulse response | The output when the input is a single 1 followed by zeros; for an FIR it is the kernel itself. | How a bell rings after one tap. |
| Convolution | Sliding the kernel along the signal and computing the weighted sum at each position. | Moving a magnifying glass along a line of text. |
| Frequency response | How much a filter passes each frequency: gain (and phase) versus frequency. | A graphic equaliser's curve. |
| Windowed-sinc | An FIR low-pass made from the ideal sinc shape, tapered by a window so it can be finite. | A carefully trimmed ideal recipe. |
| Delay (group delay) | How long the filter makes the signal late; (N - 1) / 2 samples for a symmetric FIR. | The time a committee needs to reach a decision. |
| Median filter | Each output is the middle value of the last few inputs; removes isolated spikes. | Ignoring the one wildly wrong witness. |

## Learning Objectives

- Implement a moving average, an exponential moving average and a windowed-sinc FIR in a few lines each
- Compute a filter's gain at any frequency from its kernel, and the moving average's gain from its sinc-like formula; place its nulls on interference (a 20-sample average at 1 kHz kills 50 Hz)
- Show that the EMA with `alpha = dt / (RC + dt)` follows the RC circuit simulated by `sim` almost exactly
- Design a windowed-sinc low-pass and check it against `scipy.signal.firwin`
- Compare filters on a realistic noisy record: noise removed, delay added, and robustness to spikes

## The Problem

The previous lessons ended with a list of samples that contains the signal plus white noise, mains hum and the occasional spike from a motor switching. Lesson 06 showed that averaging helps; Lesson 04 showed that filtering before the ADC is essential against aliasing. Now that the signal is safely sampled, the rest of the cleaning can be done in firmware: no extra parts, adjustable at any time, and as sharp as you can afford to compute.

But every filter is a trade-off. Heavier smoothing means more delay: a thermostat that reacts a second late is fine, a motor controller that reacts a second late is a disaster. Some filters remove 50 Hz perfectly but smear spikes; others remove spikes but are not linear. This lesson builds the four standard tools and measures exactly what each one does to the same record.

## The Physics

There is no new physics: a digital filter is arithmetic. But there is a direct bridge to the physics you know. An RC low-pass (Phase 07) obeys `RC dv/dt = v_in - v`. Replace the derivative by a difference over one sample time `dt` (exactly what you did in Phase 07, Lesson 08, to build transient simulation by hand):

```
RC x (y[n] - y[n-1]) / dt = x[n] - y[n]
```

Solve for the new output:

```
y[n] (RC + dt) = RC y[n-1] + dt x[n]
y[n] = y[n-1] + dt / (RC + dt) x (x[n] - y[n-1])
```

That is the exponential moving average, with `alpha = dt / (RC + dt)`. One line of code is a capacitor.

## The Concept

### The moving average

```
y[n] = (x[n] + x[n-1] + ... + x[n-N+1]) / N
```

Its frequency response comes from summing N equally weighted phasors (Phase 09):

```
gain(f) = | sin(pi f N / fs) / (N x sin(pi f / fs)) |
```

Read it as: "a sinc-like curve that is 1 at DC and is exactly zero wherever `f N / fs` is a whole number". So an N-sample average at rate fs has **nulls** at `fs / N, 2 fs / N, ...`. With fs = 1000 and N = 20, the nulls are at 50, 100, 150 Hz...: it removes mains hum and all its harmonics completely, which is the "average over whole mains periods" trick of Lesson 06 in filter language. The simulation prints gain 0.000 at 50 and 100 Hz for N = 20, matching the formula.

Its weaknesses: between the nulls the response bounces back up (the "sidelobes"; at 25 Hz the N = 20 average still passes 64%), and it delays the signal by `(N - 1) / 2` samples.

### The exponential moving average

```
y[n] = y[n-1] + alpha x (x[n] - y[n-1])
```

It needs one stored number and one multiplication per sample, which is why it is everywhere in firmware. As derived above, it behaves like an RC with time constant:

```
tau = RC  =  dt x (1 - alpha) / alpha        (approximately dt / alpha for small alpha)
```

With `RC = 100 ms` at 1 kHz, `alpha = 0.001 / 0.101 = 0.0099`. The simulation compares a step through the EMA with the same step through a real RC circuit in our simulator: after 100 ms the RC gives 0.6321 (the famous 63%) and the EMA 0.6303. The small difference is the cost of the crude time step; at 10 samples per time constant it would be bigger, at 1000 smaller.

The EMA is an IIR filter: in principle its output depends on every input ever seen, with exponentially fading weight. It has no nulls; like the RC, it falls 20 dB per decade above its cutoff `1 / (2 pi tau)`.

### The windowed-sinc FIR

What would the *ideal* low-pass look like? It would pass everything below a cutoff `fc` with gain 1 and nothing above. Its impulse response, worked out by the Fourier transform, is a sinc:

```
h[n] = 2 fc / fs x sinc(2 fc / fs x n),       sinc(u) = sin(pi u) / (pi u)
```

It goes on forever in both directions, so we cut it to N taps (centred on the middle) and multiply by a smooth **window** that tapers the ends to zero; without the taper, the sudden cut causes ripples in the frequency response. The Hamming window:

```
w[n] = 0.54 - 0.46 x cos(2 pi n / (N - 1))
```

Finally divide by the sum of the taps so that the DC gain is exactly 1. With 201 taps and `fc = 10 Hz`:

```
  1 Hz:   -0.0 dB
  5 Hz:   -0.7 dB
 10 Hz:   -6.1 dB    (a windowed-sinc's cutoff is its half-amplitude point)
 20 Hz:  -50 dB
 50 Hz:  -71 dB
100 Hz:  -82 dB
```

That is a far sharper filter than any RC: it goes from passing to -50 dB within one octave. The cost: 201 multiplications per sample, and a delay of `(201 - 1) / 2 = 100` samples = 100 ms. Our kernel matches `scipy.signal.firwin(201, 10, window="hamming", fs=1000)` to within 1e-17.

### Spikes: the median filter

All of the above are **linear**: a 5 V spike becomes a smaller but wider bump, spread over the filter's length. A **median filter** sorts the last few samples and takes the middle one. One wild sample out of five never reaches the middle, so a single spike vanishes completely, while slow changes pass. It is not linear (it has no frequency response in the usual sense), so it is used *before* a linear filter, not instead of one.

### Comparing them on real data

A 1 Hz signal plus 0.2 RMS white noise, 0.3 amplitude 50 Hz hum and one spike of 5, sampled at 1 kHz (raw RMS error 0.300):

| Filter | Delay | RMS error | Largest error |
|--------|-------|-----------|---------------|
| moving average N = 20 | 9.5 ms | 0.049 | 0.30 |
| moving average N = 100 | 49.5 ms | 0.030 | 0.11 |
| exponential, tau = 20 ms | ~20 ms | 0.050 | 0.22 |
| windowed-sinc FIR, 10 Hz | 100 ms | 0.032 | 0.14 |
| median of 5, then FIR | 100 ms | 0.030 | 0.071 |

(Errors are measured after compensating each filter's delay, away from the start-up.) The N = 20 average removes the hum perfectly but lets through more noise and the spike; longer filters remove more noise but add delay. The median-plus-FIR combination halves the worst error, because the spike never gets in.

### Worked example: filters by hand

**A 4-point moving average** of the list `1, 1, 1, 5, 1, 1, 1` (a spike in the middle). Each output averages the current and three previous samples (we start at the fourth sample, once there are four):

```
samples 1,1,1,5  ->  8 / 4 = 2.0
samples 1,1,5,1  ->  8 / 4 = 2.0
samples 1,5,1,1  ->  8 / 4 = 2.0
samples 5,1,1,1  ->  8 / 4 = 2.0
samples 1,1,1,1  ->  4 / 4 = 1.0
```

The spike of height 4 above the baseline became a plateau of height 1 lasting 4 samples: smaller, but four times wider. That is what every linear filter does to spikes. A 3-point **median** of the same list gives `1, 1, 1, 1, 1`: the spike is gone.

**An EMA with alpha = 0.5** following a step `0, 1, 1, 1, 1, 1`:

```
y0 = 0
y1 = 0 + 0.5 x (1 - 0)    = 0.5
y2 = 0.5 + 0.5 x (1 - 0.5) = 0.75
y3 = 0.75 + 0.5 x 0.25    = 0.875
y4 = 0.875 + 0.5 x 0.125  = 0.9375
```

Each step closes half the remaining gap: the discrete version of an RC charging curve. With alpha = 0.5 the "time constant" is about `dt x (1 - 0.5) / 0.5 = 1` sample.

**Why the 20-sample average kills 50 Hz at 1 kHz.** Twenty samples of a 50 Hz sine at 1000 samples/s cover exactly one period (20 ms). The samples of a full period come in pairs of opposite sign (the sample at phase `theta` and the one at `theta + 180 degrees`), so their sum is zero, whatever the starting phase. The average is zero: a perfect null.

### Worked example: choosing between filters

A battery-voltage reading updated once a second: an EMA with a time constant of a few seconds is ideal (one variable, no buffer, delay irrelevant). A 50 Hz-polluted thermocouple reading: a moving average over exactly 20 ms (or 100 ms to also cancel 60 Hz). A vibration signal where 5-50 Hz must be kept and 100 Hz and above rejected sharply: a windowed-sinc FIR (or an IIR design from `scipy.signal`). A motor current with occasional switching spikes: a short median first, then whichever linear filter fits.

### Worked example: how many taps for a sharp FIR?

A useful rule of thumb for a Hamming-windowed sinc: the transition from "passing" to "well attenuated" takes about `3.3 x fs / N` hertz. For N = 201 at 1000 samples/s:

```
transition width ~ 3.3 x 1000 / 201 = 16 Hz
```

That matches the table: -6 dB at 10 Hz, already -50 dB by 20 Hz. To make the transition five times sharper (3 Hz wide) you need five times the taps, about 1100, and the delay grows to 550 ms. Sharpness costs both computation and delay; that trade-off is why IIR designs (which reach a given sharpness with far fewer operations, at the cost of a non-constant delay) are popular in firmware.

### Worked example: an EMA in integer arithmetic

On a small microcontroller without floating point, choose `alpha = 1 / 16` and keep the state scaled by 16 to preserve fractions:

```
state = state + reading - (state >> 4)      (state holds 16 x the filtered value)
filtered = state >> 4
```

`>> 4` is a shift right by 4 bits, a division by 16 that costs one instruction. With 1000 readings per second, `tau = dt x (1 - 1/16) / (1/16) = 15 ms`. If you skipped the scaling and wrote `y = y + (x - y) >> 4` on integers, any difference smaller than 16 would round to zero and the output would stop short of the input: a classic firmware bug.

## Build It

### Step 1: Moving average and EMA

```python
def moving_average(x, taps):
    kernel = np.ones(taps) / taps
    return np.convolve(x, kernel, mode="full")[:len(x)]


def exponential_average(x, alpha):
    y = np.empty_like(x)
    state = x[0]
    for index, value in enumerate(x):
        state = state + alpha * (value - state)
        y[index] = state
    return y
```

`np.convolve` slides the kernel along the signal; keeping the first `len(x)` outputs gives a **causal** filter (each output only uses past and present inputs, as a real-time firmware filter must).

### Step 2: Gain from a kernel

```python
def gain_at(kernel, frequency, rate=RATE):
    n = np.arange(len(kernel))
    return abs(np.sum(kernel * np.exp(-2j * np.pi * frequency * n / rate)))
```

Feed in a complex sinusoid of the chosen frequency: each tap multiplies a sample that is one step older, rotated by `-2 pi f / fs`. The size of the sum is the gain.

### Step 3: The EMA against the simulator's RC

`rc_step_from_sim` drives a 10 kohm, 10 uF RC with a 0-to-1 V step (a pulse source with a long period) and samples its output every millisecond; the EMA gets the same step.

### Step 4: The windowed-sinc kernel

```python
def windowed_sinc(cutoff_hz, taps, rate=RATE):
    n = np.arange(taps) - (taps - 1) / 2
    ideal = 2 * cutoff_hz / rate * np.sinc(2 * cutoff_hz / rate * n)
    window = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(taps) / (taps - 1))
    kernel = ideal * window
    return kernel / kernel.sum()
```

(`np.sinc` already includes the pi: `np.sinc(u) = sin(pi u) / (pi u)`.)

### Step 5: Clean the record

The script builds the noisy record with a fixed random seed, runs every filter, shifts each output back by its delay and measures the errors. It saves `filtering.png` with the raw samples, the FIR output and the true signal.

Run it:

```
uv run python phases/19-sensors-and-signals/07-digital-filtering/code/main.py
```

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
A 1 Hz sensor signal sampled at 1000 samples/s, with white noise (0.2 RMS), 50 Hz hum (0.3) and one spike
  RMS error of the raw samples: 0.300

Moving average: gain at a few frequencies (formula |sin(pi f N / fs) / (N sin(pi f / fs))|)
  N =  5:   1 Hz 1.000 (1.000),  25 Hz 0.975 (0.975),  50 Hz 0.904 (0.904), 100 Hz 0.647 (0.647)
  N = 20:   1 Hz 0.999 (0.999),  25 Hz 0.637 (0.637),  50 Hz 0.000 (0.000), 100 Hz 0.000 (0.000)
  N = 50:   1 Hz 0.996 (0.996),  25 Hz 0.180 (0.180),  50 Hz 0.128 (0.128), 100 Hz 0.000 (0.000)
  N = 20 spans exactly one 50 Hz period, so it has a perfect null at 50 Hz and every multiple

Exponential average y += alpha (x - y) as the digital twin of an RC (tau = 100 ms)
  alpha = dt / (tau + dt) = 0.00990
  t =   10 ms: RC in sim 0.0951, EMA 0.0947, exact 1 - e^(-t/RC) = 0.0952
  t =  100 ms: RC in sim 0.6321, EMA 0.6303, exact 1 - e^(-t/RC) = 0.6321
  t =  200 ms: RC in sim 0.8647, EMA 0.8633, exact 1 - e^(-t/RC) = 0.8647
  t =  500 ms: RC in sim 0.9933, EMA 0.9931, exact 1 - e^(-t/RC) = 0.9933

Windowed-sinc FIR low-pass: 201 taps, cutoff 10 Hz, Hamming window (largest difference from scipy.signal.firwin: 4.34e-18)
     1 Hz: gain 0.9985 (   -0.0 dB)
     5 Hz: gain 0.9195 (   -0.7 dB)
    10 Hz: gain 0.4968 (   -6.1 dB)
...
```

## Use It

- **Firmware:** the EMA is the default smoothing filter in embedded code (often with alpha a power of two, like 1/16, so the multiplication becomes a bit shift). Moving averages over a whole mains period are the standard way to read slow sensors near mains wiring.
- **Arduino and MicroPython libraries** for "smoothing" and "running average" are moving averages or EMAs.
- **DSP chips and audio processors** run FIR filters with hundreds of taps at audio rates; ARM Cortex-M4 and M7 microcontrollers have instructions (multiply-accumulate, the MAC of Phase 20) designed for exactly this.
- **Design tools:** `scipy.signal.firwin`, `scipy.signal.butter` (IIR designs), and online tools generate coefficients; you then run them in firmware with a loop of multiply-adds.
- **Sigma-delta ADCs** contain digital "sinc" filters (cascaded moving averages) whose nulls are placed on 50 and 60 Hz.
- **Decimation:** after oversampling (Lesson 04), a digital low-pass followed by keeping every k-th sample lowers the data rate while keeping the gained resolution.

## Common Mistakes

- **Forgetting the delay.** A 201-tap FIR at 1 kHz delays everything by 100 ms. In a control loop, delay can cause oscillation (Phase 13's feedback lessons).
- **Filtering to remove aliases.** Digital filters cannot separate an alias from a real signal at the same frequency (Lesson 04). Filter before the ADC.
- **Using a moving average with the wrong length near mains.** At 1 kHz, 20 or 100 samples null 50 Hz; 15 samples does not.
- **An EMA with alpha too small for the number type.** In integer firmware, `alpha x (x - y)` can round to zero for small differences and the output gets stuck; keep extra fractional bits.
- **Not normalising the kernel.** If the taps do not sum to 1, the DC gain is wrong and every reading is scaled.
- **Using a linear filter on spikes.** It smears them into wide bumps. Remove outliers first (median), then filter.

## Exercises

1. At fs = 500 samples/s, which moving-average lengths put a null at 50 Hz? (N = 10, 20, 30...: any multiple of 500 / 50 = 10.)
2. An EMA runs at 100 samples/s with alpha = 0.05. What is its approximate time constant and cutoff frequency? (tau = 0.01 x 0.95 / 0.05 = 0.19 s; f_c = 1 / (2 pi 0.19) = 0.84 Hz.)
3. What is the delay of a 51-tap symmetric FIR at 2000 samples/s? (25 samples = 12.5 ms.)
4. In `main.py`, change the FIR cutoff to 3 Hz and the taps to 401. Predict and then check: does the RMS error fall? What happens to the delay?
5. Harder: build a high-pass filter by subtracting the windowed-sinc low-pass from an "all-pass" kernel (a single 1 at the centre tap, zeros elsewhere). Use it to remove the slow 1 Hz signal and keep only the hum and noise, then check its gain at 1, 10 and 50 Hz with `gain_at`.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Moving average | "Smoothing" | Mean of the last N samples; FIR with equal taps and nulls at multiples of fs / N |
| EMA | "Low-pass in software" | y += alpha (x - y); the digital twin of an RC with tau about dt / alpha |
| FIR | "Convolution filter" | Output is a weighted sum of a fixed number of inputs |
| IIR | "Recursive filter" | Output also depends on past outputs |
| Windowed-sinc | "Sharp FIR low-pass" | A truncated, windowed ideal sinc kernel, normalised to unit DC gain |
| Group delay | "Lag" | (N - 1) / 2 samples for a symmetric FIR |
| Median filter | "Spike killer" | Middle value of a sliding window; non-linear |

## Further Reading

- [Steven W. Smith, *The Scientist and Engineer's Guide to Digital Signal Processing*, Chapters 15 (Moving Average Filters), 16 (Windowed-Sinc Filters) and 19 (Recursive Filters)](https://www.dspguide.com/ch15.htm) — free online, with exactly these filters
- Richard G. Lyons, *Understanding Digital Signal Processing*, 3rd ed. (Prentice Hall) — FIR and IIR filters explained with very little maths
- [SciPy documentation, `scipy.signal.firwin` and `scipy.signal.freqz`](https://docs.scipy.org/doc/scipy/reference/signal.html) — the library tools used here only as a check
- [MIT OpenCourseWare 6.003 "Signals and Systems"](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/) — discrete-time systems, convolution and frequency response
