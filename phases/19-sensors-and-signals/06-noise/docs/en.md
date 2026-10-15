# Noise

> Every resistor hisses, every current crackles, and every wire is an antenna. Noise cannot be removed, only limited: narrow the bandwidth, average many readings, and know which kinds of noise averaging can beat and which it cannot.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 19 (Sensors and Signals), Lessons 01-05; Phase 01 (The Physics Underneath), Lesson 06 (Current as Moving Charge); Phase 09 (Alternating Current), Lesson 03 (RMS Values); Phase 10 (Filters and Resonance), Lesson 03 (Decibels and Bode Plots)
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Noise | Unwanted random fluctuation added to a signal. | The hiss between radio stations. |
| Interference | Unwanted signals from somewhere specific (mains hum, a motor, a radio), not random. | A neighbour's music through the wall. |
| Thermal (Johnson) noise | The random voltage across any resistor, caused by the thermal jiggling of its electrons. | The rustle of leaves on a windless day: just from being warm. |
| Shot noise | Randomness of a current because charge comes in individual electrons. | Rain on a roof: drops arrive randomly even in steady rain. |
| 1/f (flicker, pink) noise | Noise that gets stronger at low frequencies; it causes slow drifts. | The slow wander of a person trying to stand perfectly still. |
| White noise | Noise with equal power at every frequency. | Like white light containing all colours. |
| Bandwidth (B) | The range of frequencies a circuit lets through, in hertz. | How wide the door is. |
| Noise density | Noise per square root of bandwidth, in V / sqrt(Hz) (read "volts per root hertz"). | How loud the hiss is per slice of frequency. |
| RMS noise | The effective size of the noise, the square root of the mean of the squares (it equals the standard deviation for zero-mean noise). | The typical size of the wobble. |
| SNR | Signal-to-noise ratio, usually 20 log10(signal RMS / noise RMS) in dB. | How clearly you hear the voice over the room. |
| Averaging | Adding up N readings and dividing by N. | Asking many people and taking the mean of their answers. |
| Boltzmann's constant (k) | 1.380649e-23 joules per kelvin: the link between temperature and energy per particle. | The exchange rate between "warm" and "energetic". |
| Elementary charge (q) | 1.602e-19 coulombs: the charge of one electron. | The size of one raindrop. |

## Learning Objectives

- Compute thermal noise `sqrt(4 k T R B)` and shot noise `sqrt(2 q I B)` and judge whether they matter compared with an ADC step
- Show numerically that white noise RMS grows with the square root of bandwidth, and use that to argue for filtering
- Show that averaging N readings reduces white noise by sqrt(N), and compute the SNR improvement in dB
- Explain why 1/f noise and drift are not beaten by long averages
- Reject mains interference completely by averaging over a whole number of mains periods

## The Problem

A bathroom scale's load cell gives 2 mV at full load (Lesson 03). Amplified by 400, the reading jumps around by several counts even with nothing on the scale. An ECG electrode picks up the heart's 1 mV signal under a much larger 50 Hz hum. A light sensor in a dim room gives readings that look like static.

Noise sets the ultimate limit of every measurement. Some of it is fundamental physics (you cannot build a resistor without thermal noise), some is pickup from the environment, some is drift. Each kind has a different cure. This lesson computes the fundamental kinds, then simulates the three standard weapons: limiting bandwidth, averaging, and synchronising with the interference.

## The Physics

### Thermal noise: warm electrons jiggle

In any conductor above absolute zero, the electrons bounce around randomly with thermal energy (Phase 01). At any instant slightly more might be moving left than right, so a tiny random voltage appears across the resistor's ends. Its RMS value is:

```
v_n = sqrt(4 k T R B)
```

Read it as: "the noise voltage is the square root of four, times Boltzmann's constant, times the absolute temperature, times the resistance, times the bandwidth". With `k = 1.38e-23 J/K`, `T = 300 K` (27 C), `R = 10 kohm`, `B = 10 kHz`:

```
4 x 1.38e-23 x 300 x 10 000 x 10 000 = 1.656e-12
v_n = sqrt(1.656e-12) = 1.29e-6 V = 1.29 uV RMS
```

This noise is **white**: it has the same strength at every frequency, so it grows as the square root of the bandwidth. That is why it is often given as a **density**: `sqrt(4 k T R)` = 12.9 nV per root hertz for 10 kohm. Multiply by `sqrt(B)` to get the RMS in a bandwidth.

Three ways to reduce it: lower resistance, lower temperature, or narrower bandwidth. The first is a design choice, the second is used in radio telescopes, the third is everybody's tool.

### Shot noise: charge comes in lumps

A current is a stream of individual electrons arriving at random moments, like raindrops. The number arriving in each short interval varies, so the current fluctuates:

```
i_n = sqrt(2 q I B)
```

Read it as: "the noise current is the square root of two, times the electron's charge, times the current, times the bandwidth". It matters when currents are small, as in photodiodes. For 1 nA over 10 kHz: `sqrt(2 x 1.6e-19 x 1e-9 x 1e4) = 1.8 pA`, an SNR of only 55 dB. Notice the SNR improves as `sqrt(I)`: more light, better SNR.

### 1/f noise: the slow wander

Almost every real device (transistors, op-amps, carbon resistors, sensors) also has noise that grows at low frequencies, roughly as `1 / f` in power. It shows up as slow drift over seconds and minutes. Its cause is various slow physical processes (charge trapping in materials, for instance). Its crucial property: lowering the bandwidth does *not* help much at low frequencies, and averaging longer does not keep improving the result.

### Interference

Mains wiring radiates 50 or 60 Hz electric and magnetic fields everywhere indoors. Switching power supplies radiate their switching frequency and harmonics. Radios, motors, fluorescent lights all add their own. This is not random: it has definite frequencies, which makes it easier to remove if you know them.

## The Concept

### Does thermal noise matter here?

Compare with the ADC. A 12-bit ADC on 3.3 V has an LSB of 806 uV, and quantization noise of `806 / sqrt(12) = 233 uV` RMS (Lesson 05). A 10 k / 10 k divider looks like 5 kohm to the ADC (its Thevenin resistance, which our simulator finds by injecting a test current with the supply set to zero). Its thermal noise over 1 kHz is `sqrt(4 x 1.38e-23 x 300 x 5000 x 1000) = 288 nV`. A thousand times smaller than one LSB: irrelevant.

But put a gain of 400 in front (the load cell of Lesson 03): the op-amp's input noise (often 10-20 nV / sqrt(Hz)) plus the bridge's thermal noise, over a few kHz, becomes a microvolt or so at the input and 0.4 mV or more at the output. Now it is half an LSB. That is why high-gain front ends need low-noise op-amps and narrow bandwidths.

### Bandwidth: let through only what you need

White noise power is spread evenly over frequency, so letting in four times the bandwidth lets in four times the power, which is twice the RMS voltage:

```
noise RMS in bandwidth B  =  density x sqrt(B)
```

The simulation filters one white-noise record to 1, 4, 16 and 50 kHz and finds RMS ratios of 1.00, 2.02, 4.04 and 7.15, against the square roots 1, 2, 4 and 7.07. A temperature sensor that changes over seconds needs a bandwidth of perhaps 1 Hz; every hertz beyond that lets in noise for nothing. That is what the anti-aliasing filter (Lesson 04) and the digital filters (Lesson 07) are for.

### Averaging: the square root of N

If each reading has the true value plus independent random noise of RMS `sigma`, the average of N readings has noise:

```
sigma_average = sigma / sqrt(N)
```

Why the square root? The noises add up "randomly": the sum of N independent noises has a *variance* (RMS squared) N times larger, so its RMS is `sqrt(N) x sigma`; dividing the sum by N gives `sigma x sqrt(N) / N = sigma / sqrt(N)`. Read it as: "to halve the noise, average four times as many readings".

In decibels, each factor of 4 in N gains 6 dB of SNR, each factor of 10 gains 10 dB. The simulation buries 1 mV under 10 mV RMS of white noise (SNR -20 dB, the signal invisible in any single reading):

| N | Noise left | 10 mV / sqrt(N) | SNR |
|---|-----------|-----------------|-----|
| 1 | 10.0 mV | 10.0 mV | -20 dB |
| 16 | 2.45 mV | 2.50 mV | -7.8 dB |
| 256 | 0.65 mV | 0.63 mV | +3.8 dB |
| 4096 | 0.18 mV | 0.16 mV | +15 dB |

(The last row is estimated from only 16 averages, so it is itself a little noisy.) Averaging is the same as a low-pass filter: averaging N readings taken at rate fs cuts the bandwidth to roughly `fs / (2N)`.

### Why averaging stops working: 1/f noise

The simulation makes pink (1/f) noise with the same RMS as white noise and averages blocks of increasing length:

```
block       white spread   pink spread
1           1.00           1.00
16          0.25           0.82
256         0.063          0.62
4096        0.010          0.37
```

White noise falls by 4 each time the block grows by 16. Pink noise barely moves: its power is concentrated at low frequencies, which a longer average still lets through. In practice this means every sensor has a "best" averaging time; beyond it, drift dominates. Precision instruments fight 1/f noise with **chopping** (switching the signal's polarity at a few hundred hertz so it moves up in frequency, away from the 1/f region) or with "zero-drift" op-amps that do this internally.

### Rejecting interference by synchronising

Averaging a 50 Hz hum over an arbitrary time leaves part of a cycle uncancelled. Averaging over **exactly a whole number of periods** (20 ms, 40 ms...) cancels it completely, because a full sine cycle averages to zero, whatever its phase:

```
15 ms (0.75 periods):  worst error 1497 uV
20 ms (1 period):      worst error    0 uV
50 ms (2.5 periods):   worst error  637 uV
```

Precision multimeters and many sigma-delta ADCs use integration times of exactly 20 ms or 100 ms for this reason (100 ms cancels both 50 Hz and 60 Hz, since it is 5 and 6 periods). Their datasheets call it "normal-mode rejection".

### Worked example: a noise budget for a load cell

The load cell of Lesson 03 gives 2.5 mV at full load. Its bridge looks like 350 ohm between its two outputs. The amplifier's input noise density is 10 nV per root hertz. How small a weight can we resolve?

```
bridge thermal noise density:  sqrt(4 x 1.38e-23 x 300 x 350) = 2.4 nV / sqrt(Hz)
amplifier noise density:       10 nV / sqrt(Hz)
total (add as powers):         sqrt(2.4^2 + 10^2) = 10.3 nV / sqrt(Hz)
```

The amplifier dominates. Now the bandwidth. A scale only needs to update a few times a second; filter to 10 Hz:

```
noise RMS = 10.3 nV x sqrt(10) = 32.6 nV
SNR = 20 log10(2.5 mV / 32.6 nV) = 20 log10(76 700) = 97.7 dB
```

That is about `(97.7 - 1.76) / 6.02 = 16` effective bits: one part in 65 000 of full scale. With 1 kHz of bandwidth instead, the noise would be 10 times bigger and the SNR 77.7 dB (about 12.6 bits). Narrowing the bandwidth bought more than three bits for free.

The catch is at the bottom: at 10 Hz most op-amps are deep in their 1/f region (their corner is often 10-100 Hz), so the real noise is higher than the white figure. That is why precision bridge amplifiers are chopper or zero-drift types.

### Worked example: is it worth averaging?

A 12-bit ADC reading shows a spread of 3 LSB RMS. You want 0.5 LSB. Averaging N readings divides white noise by `sqrt(N)`:

```
3 / sqrt(N) <= 0.5   ->   sqrt(N) >= 6   ->   N >= 36
```

At 10 000 samples per second, 36 readings take 3.6 ms; but to also cancel 50 Hz hum, average for 20 ms (200 readings), which brings the noise down to `3 / sqrt(200) = 0.21 LSB`.

### Worked example: the sample capacitor's own noise

The ADC's sample-and-hold capacitor (Phase 17, Lesson 04) is charged through a switch, which has resistance and therefore thermal noise. When the switch opens, the capacitor freezes whatever noise voltage it had. The result is surprisingly simple: the RMS noise frozen on a capacitor C is

```
v_n = sqrt(k T / C)
```

independent of the resistance (a bigger resistance makes more noise density, but also a narrower RC bandwidth, and the two cancel). For a 14 pF sample capacitor at 300 K:

```
sqrt(1.38e-23 x 300 / 14e-12) = sqrt(2.96e-10) = 17.2 uV RMS
```

Small compared with a 12-bit LSB (806 uV), but for a 16-bit converter on 3.3 V (50 uV LSB) it is a third of an LSB. That is one reason high-resolution ADCs use bigger sampling capacitors, which are harder to drive and need the buffers of Lesson 03.

### Worked example: SNR in decibels, both ways

Signal 1 V RMS, noise 1 mV RMS:

```
SNR = 20 log10(1 / 0.001) = 20 x 3 = 60 dB
```

Using powers instead: `10 log10(1^2 / 0.001^2) = 10 x 6 = 60 dB`: the same, which is why voltages use 20 log10 and powers 10 log10. Averaging 100 readings divides the noise by 10, which adds `20 log10(10) = 20 dB`: 80 dB. Every factor of 4 in readings adds 6 dB, roughly one bit.

## Build It

### Step 1: Fundamental noise formulas

`thermal_noise_volts(R, B)` and `shot_noise_amps(I, B)` are the two formulas. The script tabulates thermal noise from 100 ohm to 1 Mohm and shot noise from 1 nA to 1 mA.

### Step 2: The Thevenin resistance from the simulator

```python
def thevenin_resistance(top_ohms, bottom_ohms):
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", 0.0)
    circuit.resistor("RTOP", "vdd", "out", top_ohms)
    circuit.resistor("RBOT", "out", "0", bottom_ohms)
    circuit.current_source("ITEST", "0", "out", 1e-3)
    return circuit.dc().v("out") / 1e-3
```

With the supply set to 0 V, the only source is a 1 mA test current into the output; the resulting voltage divided by 1 mA is the resistance seen from the output (Phase 05, Lesson 06).

### Step 3: Bandwidth and averaging

`band_limited_rms` zeroes every FFT bin above a bandwidth and measures the RMS of what is left. `block_average_spread` cuts a record into blocks of N readings, averages each block and measures how much the averages vary.

### Step 4: Pink noise and hum

`pink_noise` takes white noise, divides its spectrum by `sqrt(f)` (so the power falls as 1/f) and normalises it. The hum test averages a 50 Hz sine plus a DC level over different windows and starting phases.

Run it:

```
uv run python phases/19-sensors-and-signals/06-noise/code/main.py
```

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
Thermal (Johnson) noise sqrt(4 k T R B) at 300 K over 10 kHz
        100 ohm:   0.129 uV RMS (  1.29 nV per root hertz)
      1,000 ohm:   0.407 uV RMS (  4.07 nV per root hertz)
     10,000 ohm:   1.287 uV RMS ( 12.87 nV per root hertz)
    100,000 ohm:   4.070 uV RMS ( 40.70 nV per root hertz)
  1,000,000 ohm:  12.872 uV RMS (128.72 nV per root hertz)

A 10 k / 10 k sensor divider looks like 5000 ohm to the ADC (found with a 1 mA test current in sim)
  its thermal noise over 1 kHz: 288 nV RMS, far below a 12-bit LSB of 806 uV

Shot noise sqrt(2 q I B) of a photodiode current over 10 kHz
  I =   1e-09 A: noise 1.790e-12 A RMS, SNR   54.9 dB
  I =   1e-06 A: noise 5.661e-11 A RMS, SNR   84.9 dB
  I =   1e-03 A: noise 1.790e-09 A RMS, SNR  114.9 dB

White noise: RMS grows with the square root of the bandwidth you let through
  bandwidth   1000 Hz: RMS 0.140  (ratio to 1 kHz 1.00, sqrt ratio 1.00)
  bandwidth   4000 Hz: RMS 0.282  (ratio to 1 kHz 2.02, sqrt ratio 2.00)
  bandwidth  16000 Hz: RMS 0.565  (ratio to 1 kHz 4.04, sqrt ratio 4.00)
  bandwidth  50000 Hz: RMS 1.000  (ratio to 1 kHz 7.15, sqrt ratio 7.07)

Averaging N readings of 1.000 mV buried in 10 mV RMS of white noise
       N  noise left  10 mV / sqrt(N)      SNR
       1   10.035 mV        10.000 mV  -20.0 dB
      16    2.447 mV         2.500 mV   -7.8 dB
     256    0.647 mV         0.625 mV    3.8 dB
    4096    0.175 mV         0.156 mV   15.1 dB

White versus 1/f (pink) noise of the same RMS: does averaging longer keep helping?
  blocks of     1: white spread 0.9971, pink spread 1.0000
  blocks of    16: white spread 0.2506, pink spread 0.8229
  blocks of   256: white spread 0.0631, pink spread 0.6185
...
```

## Use It

- **Op-amp datasheets** give input voltage noise density (for example "8 nV/sqrt(Hz) at 1 kHz") and current noise density, and a 1/f "corner frequency" below which flicker noise dominates. Zero-drift parts like the OPA388 or ADA4528 have almost no 1/f noise.
- **Resistor choice:** for low noise, keep source and feedback resistances small. Metal film resistors have little excess noise; thick-film and carbon composition resistors add more.
- **Shielding and twisted pairs** reduce interference: a grounded shield blocks electric fields; twisting the two wires of a signal makes magnetic pickup cancel. Phase 21 covers layout and grounding.
- **Differential signals** (like the bridge of Lesson 03) cancel interference that hits both wires equally: the common-mode rejection of an instrumentation amplifier does the rest.
- **Lock-in amplifiers** measure tiny signals buried in noise by modulating the signal at a known frequency and averaging in sync with it: the ultimate form of the hum trick.
- **Firmware:** taking several ADC readings and averaging them, timed to span whole mains cycles, is one of the cheapest improvements you can make to any sensor reading.

## Common Mistakes

- **Expecting averaging to fix everything.** It reduces white noise by sqrt(N), but not offsets, drift, 1/f noise or aliased interference.
- **Ignoring bandwidth.** A noise figure without a bandwidth means nothing. Always ask "over what bandwidth?"
- **Adding noise RMS values directly.** Independent noises add as powers: `total = sqrt(a^2 + b^2)`. 3 uV and 4 uV of independent noise make 5 uV, not 7 uV.
- **High-value resistors in sensitive places.** A 1 Mohm resistor makes 10 times the noise voltage of a 10 kohm one.
- **Averaging over arbitrary windows near mains equipment.** Pick windows of whole mains periods.
- **Confusing interference with noise.** Interference has a source and a frequency: find it and remove it at the source if you can.

## Exercises

1. What is the thermal noise of a 47 kohm resistor at 300 K over 20 kHz (audio)? (sqrt(4 x 1.38e-23 x 300 x 47 000 x 20 000) = 3.9 uV RMS.)
2. Two independent noise sources of 3 uV and 4 uV RMS add. What is the total? (5 uV.)
3. A reading has 2 mV RMS of white noise. How many readings must you average to get under 0.1 mV? (N >= (2 / 0.1)^2 = 400.)
4. A photodiode gives 10 nA. Over 1 kHz, what is the shot-noise SNR in dB? (i_n = 1.79 pA; SNR = 20 log10(10e-9 / 1.79e-12) = 75 dB.)
5. Harder: in `main.py`, add a 60 Hz hum as well as the 50 Hz one, and find the shortest averaging window (in whole milliseconds) that cancels both. (100 ms; check that 20 ms or 50 ms does not.)

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Thermal noise | "Resistor hiss" | sqrt(4 k T R B), white, present in every resistance |
| Shot noise | "Current noise" | sqrt(2 q I B), from the graininess of charge |
| 1/f noise | "Drift", "flicker" | Noise whose power grows at low frequencies; not reduced by long averages |
| Noise density | "nV per root hertz" | Noise RMS per sqrt(Hz); multiply by sqrt(B) |
| SNR | "Signal quality" | 20 log10(signal RMS / noise RMS) in dB |
| Averaging gain | "More samples" | Independent white noise falls by sqrt(N) |
| Normal-mode rejection | "Hum rejection" | Cancelling mains interference by integrating over whole mains periods |

## Further Reading

- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 8 (Low-Noise Techniques and Transimpedance) — thermal, shot and 1/f noise in real amplifiers
- [Analog Devices, MT-048 "Op Amp Noise Relationships: 1/f Noise, RMS Noise, and Equivalent Noise Bandwidth"](https://www.analog.com/media/en/training-seminars/tutorials/MT-048.pdf)
- [Texas Instruments, "Noise Analysis in Operational Amplifier Circuits" (SLVA043)](https://www.ti.com/lit/an/slva043b/slva043b.pdf) — how to add up noise sources in a front end
- J. B. Johnson, "Thermal Agitation of Electricity in Conductors" and H. Nyquist's companion paper, *Physical Review* 32, 1928 — the original measurements and theory of thermal noise
