# Band-Pass and Band-Stop

> Combine a low-pass and a high-pass and you keep a band; put a resonant trap to ground and you delete one. That is how a radio picks a station and how an amplifier kills the mains hum.

**Type:** Learn
**Prerequisites:** Phase 10 (Filters and Resonance), Lessons 02 (RC Low-Pass and High-Pass), 03 (Decibels and Bode Plots) and 05 (RLC Resonance)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Band-pass filter | Passes a range of frequencies and blocks everything below and above it | A radio dial set to one station |
| Band-stop filter | Blocks a range of frequencies and passes everything else | Earplugs that only block one annoying whine |
| Notch filter | A very narrow band-stop filter aimed at one frequency | A sniper for a single frequency |
| Centre frequency | The middle of the pass band (or of the notch), on a log scale | The station's frequency |
| Bandwidth (BW) | The width of the pass band between its two -3 dB points, in hertz | How wide the dial's "window" is |
| Lower / upper -3 dB frequency | The two edges of the pass band | The start and end of the window |
| Geometric mean | The middle of two numbers on a log scale: sqrt(a x b) | Halfway between 100 and 10,000 on a log axis is 1,000, not 5,050 |
| Trap | A series LC placed from the signal to ground that shorts one frequency away | A drain in the floor that only opens for one size of ball |
| Twin-T | A notch made only of resistors and capacitors in two T shapes | A clever plumbing trick with two pipes that cancel |
| Hum | Unwanted 50 Hz (Europe, Asia, Africa) or 60 Hz (Americas) from the mains | The buzz of a bad guitar cable |

## Learning Objectives

- Build a wide band-pass filter from a high-pass and a low-pass, and find its -3 dB edges and centre
- Use a series RLC as a narrow band-pass and measure its bandwidth
- Build a notch filter with a series LC trap to ground and explain what limits its depth
- Build a twin-T RC notch and compare it with the LC version
- Remove 50 Hz hum from a musical note in a time-domain simulation and measure the result

## The Problem

A telephone line only needs to carry the frequencies that make speech understandable: roughly 300 Hz to 3.4 kHz. Anything outside wastes capacity and adds noise. A radio receiver's antenna picks up every station at once and must keep one band a few kilohertz wide. An ECG (heart monitor) amplifier must keep 0.5 to 40 Hz and throw away the 50 Hz picked up from the room's wiring, which can be a thousand times bigger than the heartbeat. A guitar amplifier must pass every note but kill the hum.

Low-pass and high-pass filters alone cannot do these jobs: you need to keep or remove a *band*. This lesson shows the two basic ways to build band filters: combining the RC filters you know, and using the resonance of Lesson 05.

## The Physics

### Two ways to make a band filter

**Way 1: combine two first-order filters.** A high-pass with a low cutoff f_L removes everything below f_L. A low-pass with a high cutoff f_H removes everything above f_H. Put them one after the other and only the band between survives. The slopes outside the band are the gentle -20 dB per decade of first-order filters, so this gives a **wide** band, suitable when f_H is many times f_L (speech, audio).

**Way 2: use resonance.** A series LC passes current only near f0 (Lesson 05). With the output across a resistor, you get a band-pass whose width is set by R, L and C. The narrower the better for a radio. Turn the same LC around so that it shorts the signal to ground at f0 and you get a **notch**: everything passes except a narrow slice around f0.

### Where the energy goes

In a band-pass, the energy of unwanted frequencies is mostly not *absorbed*: it is *reflected*. The filter presents a high impedance to them, so very little current flows and very little power is taken from the source. In the LC notch, the trap presents a near short at f0, so the hum current flows through the series resistor and the trap to ground; the source works hard at 50 Hz but the output node sees almost none of it. Filters redistribute where voltage appears; they do not "destroy" frequencies.

## The Concept

### 1. The wide band-pass: high-pass, buffer, low-pass

```
  V_in ---[ C1 ]---+---(buffer x1)---[ R2 ]---+--- V_out
                   |                          |
                 [ R1 ]                     [ C2 ]
                   |                          |
  0 V -------------+--------------------------+
      high-pass, fc = f_L                low-pass, fc = f_H
```

For a telephone band, f_L = 300 Hz and f_H = 3.4 kHz. With R1 = R2 = 10 k ohm:

- C1 = 1 / (2 pi x 300 x 10,000) = 53 nF
- C2 = 1 / (2 pi x 3400 x 10,000) = 4.7 nF

The buffer keeps the low-pass from loading the high-pass (Lesson 03). The **centre** of the band, on a log scale, is the geometric mean:

```
f_centre = sqrt(f_L * f_H) = sqrt(300 * 3400) = 1010 Hz
```

At the centre, each filter is a decade-ish away from its corner, so the gain is close to 0 dB (the code finds -0.73 dB, because each filter still loses a little there). At each corner the gain is about -3 dB, but the *other* filter also takes a little, so the true -3 dB edges are a bit outside: the code finds 257 Hz and 3963 Hz. Far outside, the slopes are -20 dB per decade: at 50 Hz the gain is about -15.7 dB, at 20 kHz about -15.5 dB.

This kind of band-pass only works well when f_H is much bigger than f_L. If you try to make it narrow (say f_L = 900 Hz and f_H = 1100 Hz), the two slopes overlap and the peak sinks well below 0 dB. For narrow bands, use resonance.

### 2. The narrow band-pass: series RLC

From Lesson 05:

```
  V_in ---[ L = 10 mH ]---[ C = 1 uF ]---+--- V_out
                                         |
                                     [ R = 10 ohm ]
                                         |
  0 V -----------------------------------+
```

The peak is at f0 = 1592 Hz with gain 0 dB. The two -3 dB edges are where |X_L - X_C| = R (then |Z| = sqrt(2) R and the current is 0.707 of its peak). For a series RLC the bandwidth turns out to be

```
BW = R / (2 pi L)
```

"bandwidth equals R over two pi L". Here BW = 10 / (2 pi x 0.01) = 159 Hz. The code finds edges at 1514 Hz and 1675 Hz: a bandwidth of 161 Hz (the sweep's grid spacing explains the 2 Hz difference). The ratio f0 / BW = 1592 / 159 = 10 is the Q of Lesson 05, and Lesson 07 makes this the definition of Q.

Notice the edges are not symmetric in hertz (78 Hz below, 83 Hz above): the peak is symmetric on a *log* scale, so f0 is the geometric mean of the edges: sqrt(1514 x 1675) = 1592 Hz.

### 3. The notch: an LC trap to ground

To *remove* one frequency, put the series LC from the signal to ground, after a series resistor:

```
  V_in ---[ R1 = 1 k ]---+--- V_out
                         |
                       [ C = 10 uF ]
                         |
                       [ L = 1 H ]
                         |
                       [ R_w = 10 ohm ]  (the coil's winding resistance)
                         |
  0 V -------------------+
```

This is a voltage divider: V_out / V_in = Z_trap / (R1 + Z_trap), with Z_trap = R_w + j (X_L - X_C).

- **At f0** = 1 / (2 pi sqrt(1 x 10e-6)) = 50.33 Hz, the reactances cancel and Z_trap = R_w = 10 ohm. Gain = 10 / (1000 + 10) = 0.0099 = **-40.1 dB**. The hum is cut by a factor of 100.
- **Far from f0**, |X_L - X_C| is large compared to R1 and the trap is almost open: the signal passes. At 1 kHz, X_L = 6283 ohm and X_C = 15.9 ohm; Z_trap is about 10 + j 6267 ohm; gain = |Z_trap| / |1000 + Z_trap| = 6267 / |1010 + j 6267| = 6267 / 6348 = 0.987 = -0.11 dB.
- At 100 Hz (the first harmonic of hum) the notch only gives -7.5 dB: a single notch is narrow.

**What limits the depth?** With an ideal coil (R_w = 0) the notch would be infinitely deep at exactly f0. Real coils always have resistance, and the depth is 20 log10(R_w / (R1 + R_w)). A bigger R1 makes the notch deeper, but also wider (the trap must then be much bigger than a larger R1 before the signal passes). And a 1 H coil is big and heavy. That is why practical hum filters often use the twin-T, or the active filters of Phase 13.

**Tuning precision.** At exactly 50.00 Hz (not 50.33) the gain is -39.3 dB instead of -40.1: still fine. But mains frequency drifts by ±0.2 Hz, and component tolerances of ±5 % move f0 by ±2.5 %. A very deep, very narrow notch can miss the hum entirely. Designers trade depth for width.

### 4. The twin-T: a notch without inductors

Two T-shaped networks in parallel between input and output:

```
                 R           R
  V_in ---+----[   ]---x---[   ]----+--- V_out
          |            |            |
          |          [2C]           |
          |            |            |
          |           0 V           |
          |                         |
          +----| |-----y-----| |----+
                C      |      C
                     [R/2]
                       |
                      0 V
```

The top T (two resistors with a capacitor 2C to ground) is a low-pass-like path. The bottom T (two capacitors with a resistor R/2 to ground) is a high-pass-like path. At one frequency, f_notch = 1 / (2 pi R C), the two paths deliver signals of **equal size and opposite phase** to the output, and they cancel completely. With C = 100 nF and f = 50 Hz: R = 1 / (2 pi x 50 x 1e-7) = 31,831 ohm, R/2 = 15,915 ohm, 2C = 200 nF.

The code finds -58.8 dB at 50 Hz (and in theory infinite depth exactly at f_notch), -9.1 dB at 25 and 100 Hz, and -0.17 dB at 1 kHz. A passive twin-T is wide: it already removes a lot at half and double the notch frequency. It also needs a high-impedance load (a buffer) after it, and precise components: the cancellation depends on R, R/2, C and 2C being in exact ratio.

### 5. Choosing a band filter

| Need | Choice |
|---|---|
| Wide band (f_H / f_L above about 10): speech, audio | High-pass + low-pass, buffered |
| Narrow band at high frequency (radio, kHz to GHz) | LC resonance |
| Narrow band at low frequency | Active filters (Phase 13) or digital filters (Phase 19) |
| Remove one frequency, LC practical | LC trap to ground |
| Remove one low frequency without coils | Twin-T (passive) or active notch |

## Build It

### Step 1: The telephone band-pass

```python
def voice_band_pass(f_low, f_high):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    r = 10e3
    c.capacitor("C1", "in", "hp", 1 / (2 * math.pi * f_low * r))
    c.resistor("R1", "hp", "0", r)
    c.vcvs("E1", "buf", "0", "hp", "0", 1.0)
    c.resistor("R2", "buf", "out", r)
    c.capacitor("C2", "out", "0", 1 / (2 * math.pi * f_high * r))
    return c
```

`band_edges` finds the peak of a sweep and walks outwards on both sides until the gain is 3.01 dB below it:

```python
def band_edges(freqs, gain_db, drop=3.0103):
    peak = int(np.argmax(gain_db))
    target = gain_db[peak] - drop
    below = np.where(gain_db[:peak] <= target)[0]
    above = np.where(gain_db[peak:] <= target)[0]
    low = freqs[below[-1]] if len(below) else math.nan
    high = freqs[peak + above[0]] if len(above) else math.nan
    return low, freqs[peak], high
```

Output:

```
  -3 dB edges: 257 Hz and 3963 Hz, peak near 1009 Hz, bandwidth 3706 Hz
      50 Hz:  -15.68 dB
     300 Hz:   -3.04 dB
    1000 Hz:   -0.73 dB
    3400 Hz:   -3.04 dB
   20000 Hz:  -15.52 dB
```

### Step 2: The RLC band-pass

```
  centre 1592 Hz, -3 dB edges 1514 Hz and 1675 Hz, bandwidth 161 Hz
  centre / bandwidth = 9.9 (Lesson 07 calls this Q)
```

### Step 3: The LC notch

```python
def lc_notch(capacitance=10e-6, inductance=1.0, winding=10.0):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=50.0)
    c.resistor("R1", "in", "out", 1000.0)
    c.capacitor("C1", "out", "m", capacitance)
    c.inductor("L1", "m", "w", inductance)
    c.resistor("Rw", "w", "0", winding)
    return c
```

```
    50.00 Hz:  -39.34 dB
    50.33 Hz:  -40.06 dB
   100.00 Hz:   -7.51 dB
   440.00 Hz:   -0.56 dB
  1000.00 Hz:   -0.11 dB
  deepest point of the sweep: -40.1 dB at 50.35 Hz
  depth limited by the winding: 20 log10(10 / 1010) = -40.1 dB
```

### Step 4: The twin-T

```python
def twin_t_notch(f_notch, capacitance=100e-9):
    r = 1 / (2 * math.pi * f_notch * capacitance)
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=50.0)
    c.resistor("Ra", "in", "x", r)
    c.resistor("Rb", "x", "out", r)
    c.capacitor("C2x", "x", "0", 2 * capacitance)
    c.capacitor("Ca", "in", "y", capacitance)
    c.capacitor("Cb", "y", "out", capacitance)
    c.resistor("Rhalf", "y", "0", r / 2)
    return c, r
```

The output node has nothing connected but the two Ts, which is the "high-impedance load" condition. Output: -58.8 dB at 50 Hz, -9.09 dB at 25 and 100 Hz (perfectly symmetric on the log scale), -0.17 dB at 1 kHz. The deepest sweep point is -59 dB only because no sweep frequency lands exactly on 50.00 Hz; the true notch is bottomless.

### Step 5: Hum removal in time

Two series sine sources make a 440 Hz note (the A above middle C) plus an equally loud 50 Hz hum, feeding the LC notch tuned to 50.0 Hz (C = 10.13 µF). We simulate 1 s with 20 µs steps, keep the last 0.2 s (exactly 10 cycles of 50 Hz and 88 cycles of 440 Hz) and measure each component:

```
  hum     50 Hz: before 1.000 V, after 0.0099 V (-40.1 dB)
  note   440 Hz: before 1.000 V, after 0.9379 V (-0.6 dB)
```

The hum is a hundred times smaller; the note has lost 6 %. Why simulate for a whole second? The trap is a high-Q resonant circuit: it takes many cycles to settle after switching on (Lesson 07 explains: settling time grows with Q).

## Use It

- **Telephone and voice codecs** band-limit speech to about 300 to 3400 Hz before sampling at 8 kHz.
- **Radio IF filters.** A superheterodyne receiver converts every station to a fixed "intermediate frequency" (455 kHz for AM, 10.7 MHz for FM) and uses a sharp ceramic or crystal band-pass there. Datasheets for parts such as the muRata CFWLA455 series give the centre frequency, the -6 dB bandwidth (a few kHz) and the stop-band attenuation (40 dB or more).
- **ECG and EEG front ends** combine a high-pass (to remove electrode drift), a low-pass (anti-aliasing) and often a 50/60 Hz notch, some selectable for the country.
- **Audio equalizers** are banks of band-pass filters, one per band, whose outputs are mixed with adjustable gains.
- **Wave traps** on antennas and power lines are parallel LC circuits that block one frequency from travelling along a wire, for example to keep a powerline-communication signal on one side of a transformer.
- **Digital notches.** Modern instruments often notch 50/60 Hz in software after the ADC (Phase 19), where the filter can be perfectly precise and adaptive.

## Try It in the Lab

Open **"Kill the 50 Hz hum"**. A 1 k ohm resistor feeds the output, and a trap made of a capacitor slot, a 1 H coil and the coil's 10 ohm winding resistance goes to ground. Pick the capacitor so 50 Hz is cut by at least 20 dB while notes at 1 kHz lose less than 1 dB. Compute f0 for each capacitor in the drawer. Then think about the two wrong ones: where do their notches sit, and how much do they still cut 50 Hz (use the divider formula with |X_L - X_C| at 50 Hz)? What is the deepest cut you could ever get with this coil, whatever the capacitor?

## Common Mistakes

- **Putting the centre at the arithmetic mean.** The centre of a band on a log scale is sqrt(f_L f_H), not (f_L + f_H)/2.
- **Making a narrow band-pass from RC sections.** Two first-order slopes cannot make a sharp peak; the gain at the centre collapses. Use resonance or active filters.
- **Forgetting the coil's resistance in a notch.** It sets the maximum depth.
- **Ignoring tolerance and drift.** A notch narrower than the uncertainty in f0 can miss its target.
- **Loading a twin-T.** It needs a high-impedance load; connecting it straight to a low-resistance input spoils the cancellation.
- **Forgetting harmonics.** Hum often contains 100 Hz, 150 Hz and higher harmonics (from rectifiers and transformers); one notch at 50 Hz will not remove them.

## Exercises

1. **Easy.** A band-pass has -3 dB edges at 200 Hz and 5 kHz. What are its bandwidth and centre frequency?
2. **Easy.** Which capacitor tunes an LC trap with a 470 mH coil to 60 Hz (the American mains frequency)?
3. **Medium.** For the LC notch in this lesson, compute the gain at 25 Hz by hand: find X_L, X_C, Z_trap and the divider ratio. Compare with the printed -7.35 dB.
4. **Medium.** Change `voice_band_pass` to f_L = 900 Hz and f_H = 1100 Hz. What is the peak gain, and what are the -3 dB edges? Explain why the result is a poor "narrow" filter.
5. **Hard.** Design a twin-T notch for 60 Hz with C = 47 nF. Then make one of the R/2 resistors 5 % too large in the code and see how deep the notch still is. What does this tell you about component matching?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Band-pass | "Only this range" | Gain near 1 between two edges, falling outside; built from HP + LP or from resonance |
| Band-stop / notch | "Remove this frequency" | Gain near 1 except in a band (or near one frequency) where it falls sharply |
| Bandwidth | "How wide" | Upper minus lower -3 dB frequency; for a series RLC, BW = R / (2 pi L) |
| Centre frequency | "The middle" | The geometric mean of the -3 dB edges, sqrt(f_L f_H); f0 for a resonant filter |
| LC trap | "Hum trap" | A series LC to ground that shorts the signal at f0 |
| Twin-T | "RC notch" | Two RC T-networks whose outputs cancel at f = 1 / (2 pi R C) |
| Notch depth | "How much it cuts" | The attenuation at the notch frequency, limited by losses and component mismatch |

## Further Reading

- [All About Circuits, Volume II, Chapter 8: Band-pass and band-stop filters](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-8/band-pass-filters/) — LC and RC band filters with examples
- [Analog Devices, *Linear Circuit Design Handbook* (Hank Zumbahlen, editor), chapter 8 "Analog Filters" (notch and band-pass sections)](https://www.analog.com/en/resources/technical-books/linear-circuit-design-handbook.html) — twin-T and practical notch design
- R. Mancini (ed.), *Op Amps For Everyone* (Texas Instruments, 2002; Newnes), chapter 16 "Active Filter Design Techniques" (T. Kugelstadt) — band-pass and band-rejection (twin-T) design, and how component tolerances limit them
- [The Art of Electronics (Horowitz & Hill), 3rd edition, chapter 1, LC filters and resonance](https://artofelectronics.net/) — tuned circuits in practice
