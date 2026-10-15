# What a Filter Does

> Every signal is a chord of sine waves. A filter is a circuit that plays some notes of the chord louder than others.

**Type:** Learn
**Prerequisites:** Phase 09 (Alternating Current), Lessons 02 (Sine Waves, Frequency and Phase) and 06 (Impedance); Phase 04 (Kirchhoff's Laws), Lesson 05 (The Voltage Divider)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Signal | A voltage that changes over time and carries information | The wiggling voltage from a microphone |
| Frequency component | One of the pure sine waves that, added together, make up a signal | One note in a chord |
| Spectrum | The list of all frequency components of a signal and how big each one is | The bars on a music player's equalizer display |
| Filter | A circuit that lets some frequencies through and weakens others | A coffee filter that lets liquid through and keeps the grounds |
| Pass band | The range of frequencies a filter lets through | The holes that are big enough for the liquid |
| Stop band | The range of frequencies a filter blocks | The grounds that stay behind |
| Cutoff frequency (fc) | The frequency where the filter's behaviour changes from passing to blocking | The size of the holes |
| Gain | Output amplitude divided by input amplitude at one frequency (1 = untouched, 0.5 = halved) | The volume knob position for that note |
| Low-pass / high-pass | Passes low frequencies / passes high frequencies | The bass / treble knob turned fully up, the other one down |
| Band-pass / band-stop | Passes only a range / blocks only a range | A radio tuned to one station / a mute for one annoying note |
| Harmonic | A frequency component at a whole-number multiple of a basic (fundamental) frequency | The overtones that make a guitar sound different from a flute |
| Hum | Unwanted 50 Hz or 60 Hz picked up from the mains wiring | The buzz from a cheap guitar amplifier |

## Learning Objectives

- Explain that any repeating signal can be written as a sum of sine waves at different frequencies
- Describe low-pass, high-pass, band-pass and band-stop filters with their pass and stop bands
- Explain why a resistor and a capacitor form a frequency-dependent voltage divider
- Measure the frequency components of a signal before and after an RC filter with our simulator and match the formula
- See how a low-pass filter rounds the corners of a square wave by trimming its harmonics

## The Problem

You record a guitar through a cheap cable. The recording has the music, but also a steady hiss (high frequencies, from the electronics) and a low buzz at 50 Hz (from the mains wiring in the walls). You want the music and nothing else.

Or: a temperature sensor's voltage changes slowly, over seconds, but the wire to your microcontroller picks up fast spikes every time a nearby motor switches. Or: an antenna receives hundreds of radio stations at once and you want to hear one. Or: a switching power supply produces a clean 5 V plus a ripple at 500 kHz that upsets your audio amplifier.

In every case the wanted and the unwanted parts of the signal live at **different frequencies**. If you can build a circuit whose behaviour depends on frequency, you can separate them. That circuit is a **filter**, and with the impedances of Phase 09 you already have every tool needed to build one. This phase does exactly that: RC and RL filters (Lessons 02 and 04), the decibel and Bode-plot language engineers use to describe them (Lesson 03), resonance with inductors and capacitors together (Lessons 05 to 07), and finally the AC analysis inside our simulator, built from scratch (Lesson 08).

## The Physics

### A signal is a chord

In Phase 09 you met the sine wave: the smoothest possible oscillation, described by an amplitude, a frequency and a phase. Here is a surprising and powerful fact, worked out by Joseph Fourier around 1807 while studying how heat spreads:

> Any repeating waveform, however jagged, can be built by adding sine waves whose frequencies are whole-number multiples of its repetition frequency.

The lowest frequency is the **fundamental**, the multiples are **harmonics**. A **square wave** that switches between +1 V and -1 V a hundred times a second (100 Hz) is

```
square(t) = (4/pi) [ sin(2 pi 100 t) + (1/3) sin(2 pi 300 t) + (1/5) sin(2 pi 500 t) + ... ]
```

Read it: "four over pi, times the sum of the odd harmonics, each one weaker by its harmonic number". The 100 Hz fundamental has an amplitude 4/pi = 1.273 V, the 300 Hz harmonic 1.273/3 = 0.424 V, the 500 Hz harmonic 0.255 V, and so on forever. The sharp corners of the square wave are made by the high harmonics: remove them and the corners round off.

Real signals that do not repeat (speech, music) are also sums of sines, with a continuous spread of frequencies instead of neat multiples. The list of components and their sizes is the **spectrum**. A music player's equalizer display is a rough live spectrum: tall bars on the left for bass, on the right for treble.

What the "chord" picture gets wrong: the sine waves are not really "inside" the signal waiting to be found; they are one way of describing it, the way a recipe describes a cake. But it is an extraordinarily useful description for linear circuits, because of the next fact.

### Linear circuits treat each frequency separately

Resistors, capacitors and inductors are **linear**: double the input voltage and every current and voltage doubles. For linear circuits, **superposition** (Phase 05, Lesson 05) says the response to a sum of inputs is the sum of the responses to each input. So we can:

1. Split the input signal into its sine components.
2. Work out what the circuit does to each sine separately, using the impedances of Phase 09 at that frequency.
3. Add the outputs back up.

And for a single sine, a linear circuit can only do two things: change its **amplitude** (by a factor called the **gain**) and shift its **phase**. It never changes the frequency. A 200 Hz sine in gives a 200 Hz sine out, perhaps smaller and a bit delayed. A filter is a circuit whose gain depends strongly on frequency.

### The RC divider: a voltage divider that changes with frequency

From Phase 04, two resistors in series form a voltage divider: V_out = V_in x R2 / (R1 + R2), the same fraction at every frequency. Now replace the bottom resistor with a capacitor:

```
   V_in ---[ R = 1 k ]---+--- V_out
                         |
                       [ C = 100 nF ]
                         |
   0 V ------------------+
```

From Phase 09, Lesson 06, a capacitor's opposition to AC current (the size of its impedance) is

```
|Z_C| = 1 / (2 pi f C)
```

"one over two pi times frequency times capacitance". It is **huge at low frequency** (at DC, f = 0, it is infinite: an open circuit) and **tiny at high frequency** (it approaches a short circuit). Let us put numbers in for C = 100 nF:

| f | 1 / (2 pi f C) | Compared with R = 1 k |
|---|---|---|
| 10 Hz | 159 k ohm | 159 times bigger: the capacitor takes almost all the voltage |
| 200 Hz | 7.96 k ohm | much bigger: V_out is nearly V_in |
| 1592 Hz | 1.00 k ohm | equal to R: the turning point |
| 5 kHz | 318 ohm | smaller: the resistor takes most of the voltage |
| 100 kHz | 15.9 ohm | tiny: V_out is nearly 0 |

So at low frequencies the output is almost the whole input, and at high frequencies it is almost nothing. **That is a low-pass filter.** The turning point, where the capacitor's impedance equals R, is the **cutoff frequency**:

```
fc = 1 / (2 pi R C)
```

For R = 1 k and C = 100 nF: fc = 1 / (2 x 3.1416 x 1000 x 1e-7) = 1 / 6.283e-4 = 1591.5 Hz.

You might expect the gain at fc to be exactly one half (as if two equal resistors), but it is 0.707. The reason is phase: the capacitor's voltage is a quarter cycle out of step with the resistor's (Phase 09, Lesson 05), so the two voltages add like the sides of a right-angled triangle, not like two numbers in a line. With equal sizes, each is 1/sqrt(2) = 0.707 of the input. The full formula, which Lesson 02 derives, is

```
gain = 1 / sqrt(1 + (f / fc)^2)
```

Check it: at f = fc, gain = 1 / sqrt(2) = 0.707. At f = 200 Hz, f/fc = 0.1257, gain = 1 / sqrt(1.0158) = 0.992. At 5 kHz, f/fc = 3.142, gain = 1 / sqrt(10.87) = 0.303.

Swap the resistor and capacitor and the opposite happens: the capacitor blocks low frequencies and passes high ones. **That is a high-pass filter**, with the same cutoff and gain = (f/fc) / sqrt(1 + (f/fc)²).

### The four basic shapes

```
  gain                       gain
  1 |-------\                1 |            /-------
    |        \                 |           /
    |         \___             |       ___/
  0 +----------------- f     0 +----------------- f
       LOW-PASS                    HIGH-PASS
       (bass passes)               (treble passes)

  gain                       gain
  1 |       /\               1 |-------\     /-------
    |      /  \                |        \   /
    |  ___/    \___            |         \_/
  0 +----------------- f     0 +----------------- f
       BAND-PASS                   BAND-STOP (notch)
       (one station)               (kill one note, e.g. 50 Hz hum)
```

Lessons 02 to 04 build the first two with RC and RL circuits. Lessons 05 to 07 combine inductors and capacitors to build sharp band-pass and band-stop filters using **resonance**.

## The Concept

A filter is described by its **frequency response**: the gain (and phase shift) at every frequency. To use one:

1. Find the frequencies of what you want and what you do not want.
2. Choose a filter type with the wanted part in its pass band and the unwanted part in its stop band.
3. Place the cutoff between them, with as much distance on both sides as you can.

**Worked example: tone and hiss.** Our input is a 200 Hz tone of 1 V amplitude plus 5 kHz hiss of 0.5 V. Through the low-pass with fc = 1592 Hz:

- Tone: gain 0.992, output 0.992 V. Almost untouched.
- Hiss: gain 0.303, output 0.5 x 0.303 = 0.152 V.

Before, the hiss was half the size of the tone; after, it is less than a sixth. A better filter (Lesson 03 shows how to stack them) would do even more.

Through the high-pass with the same parts, the tone is cut to 0.125 V and the hiss passes at 0.476 V: the wrong filter makes things worse.

**Worked example: rounding a square wave.** A 100 Hz square wave through the same low-pass: the fundamental keeps 99.8 % (1.271 V of 1.273 V), the 3rd harmonic 98.3 %, the 11th harmonic (1100 Hz) only 82.3 %, and harmonics far above 1.6 kHz are strongly cut. The output is a square wave with rounded corners, exactly the RC charging curves of Phase 07 seen from a different angle. Same circuit, same physics: time-domain view (exponential curves) and frequency-domain view (trimmed harmonics) are two descriptions of one thing.

**Why the cutoff must sit between.** If you put fc right at the frequency you want to keep, you lose 29 % of its amplitude. If you put it right at the frequency you want to reject, you only cut it by 29 %. A single RC filter changes gradually, so the wanted and unwanted frequencies should ideally be a factor of 10 or more apart. When they are close (a 50 Hz hum next to 60 Hz music), you need the sharper filters of Lessons 05 to 07.

## Build It

### Step 1: The cutoff of our RC

```python
def cutoff_frequency(resistance, capacitance):
    return 1 / (2 * np.pi * resistance * capacitance)


def low_pass_gain(freq, fc):
    return 1 / np.sqrt(1 + (freq / fc) ** 2)


def high_pass_gain(freq, fc):
    return (freq / fc) / np.sqrt(1 + (freq / fc) ** 2)
```

Output: `fc = 1 / (2 pi R C) = 1591.5 Hz`.

### Step 2: Two tones through the filter, in the time domain

We build the input from two sine sources stacked in series (their voltages add, by Kirchhoff's voltage law), run a transient simulation for 20 ms, and keep the last 10 ms so the start-up transient has died out:

```python
def two_tone_through(kind):
    c = Circuit()
    c.sine_source("Vtone", "in", "m", amplitude=1.0, freq=TONE)
    c.sine_source("Vhiss", "m", "0", amplitude=0.5, freq=HISS)
    if kind == "low-pass":
        c.resistor("R1", "in", "out", R)
        c.capacitor("C1", "out", "0", C)
    else:
        c.capacitor("C1", "in", "out", C)
        c.resistor("R1", "out", "0", R)
    run = c.transient(t_stop=20e-3, dt=2e-6)
    t = np.asarray(run.time)
    keep = t >= 10e-3
    keep[-1] = False
    return t[keep], np.asarray(run.v("in"))[keep], np.asarray(run.v("out"))[keep]
```

Then we measure how big each component is with the **Fast Fourier Transform** (FFT), numpy's tool for splitting a sampled signal into sines:

```python
def amplitude_at(signal, t, freq):
    n = len(signal)
    spectrum = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n, t[1] - t[0])
    return 2 * np.abs(spectrum[np.argmin(np.abs(freqs - freq))]) / n
```

You do not need to understand the FFT yet (Phase 19 explains it); think of it as an automatic "how much of each frequency is in here" meter. The 10 ms window holds exactly 2 cycles of 200 Hz and 50 cycles of 5 kHz, which keeps the meter accurate. (We drop the last sample so the window is exactly 10 ms long.) Output:

```
  A 200 Hz tone plus 5000 Hz hiss through the low-pass (simulator)
     200 Hz: in 1.000 V, out 0.992 V, ratio 0.992 (formula 0.992)
    5000 Hz: in 0.500 V, out 0.152 V, ratio 0.303 (formula 0.303)
  ... through the high-pass (simulator)
     200 Hz: in 1.000 V, out 0.125 V, ratio 0.125 (formula 0.125)
    5000 Hz: in 0.500 V, out 0.476 V, ratio 0.953 (formula 0.953)
```

The simulator knows nothing about "gain formulas": it just steps the capacitor's charging equations through time, as in Phase 07. Yet each frequency comes out scaled by exactly the formula's factor. That is superposition at work.

### Step 3: The square wave's harmonics

```python
def square_wave_harmonics(fundamental, count):
    return [(n * fundamental, 4 / (np.pi * n)) for n in range(1, 2 * count, 2)]
```

The script multiplies each harmonic by the low-pass gain at its frequency: 99.8 % kept at 100 Hz down to 82.3 % at 1100 Hz. Higher harmonics (not printed) are cut further: at 15.9 kHz only 10 % is kept.

### Step 4: The frequency response directly

Instead of a time simulation, our simulator can compute the gain at any frequency directly with its **AC analysis** (Lesson 08 builds it from scratch):

```python
def ac_gain_low_pass(freqs):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    c.resistor("R1", "in", "out", R)
    c.capacitor("C1", "out", "0", C)
    return c.ac(freqs, source="V1").gain("out")
```

`c.ac(freqs, source="V1")` drives V1 with a 1 V sine at each frequency in the list, and `.gain("out")` returns the size of the output. Output:

```
       10.0 Hz: gain 1.0000 (formula 1.0000)
     1000.0 Hz: gain 0.8467 (formula 0.8467)
     1591.5 Hz: gain 0.7071 (formula 0.7071)
    10000.0 Hz: gain 0.1572 (formula 0.1572)
   100000.0 Hz: gain 0.0159 (formula 0.0159)
```

Every tenfold step in frequency well above fc divides the gain by ten. Lesson 03 turns that observation into the language of decibels and Bode plots.

## Use It

- **Audio tone controls** are adjustable low-pass and high-pass filters. A "bass" knob boosts or cuts below a few hundred hertz, a "treble" knob above a few kilohertz.
- **Loudspeaker crossovers** split music between a woofer (low-pass) and a tweeter (high-pass) so each speaker gets only what it can play (Lesson 04).
- **Anti-aliasing filters** in front of every analog-to-digital converter remove frequencies above half the sampling rate before the signal is sampled (Phase 19). A microcontroller reading a sensor at 1000 samples per second needs a low-pass well below 500 Hz.
- **Power-supply decoupling.** The 100 nF capacitor next to every chip's power pin, with the resistance and inductance of the supply traces, forms a low-pass that keeps high-frequency noise out of the chip (Phase 21).
- **Radio receivers** use band-pass filters to pick one station (Lesson 06), and **hum filters** use band-stop filters at 50 or 60 Hz.
- **Coupling capacitors** in audio amplifiers form high-pass filters with the input resistance, blocking DC while passing sound. With 10 k ohm input resistance and 1 µF, fc = 16 Hz, just below the lowest note you can hear.

## Try It in the Lab

Open **"Keep the bass, drop the hiss"**. A 1 k ohm resistor feeds the output node. Put one part from the output to ground: a capacitor, a resistor or an inductor. The goals are that 100 Hz loses less than 1 dB (about 11 % of its amplitude; Lesson 03 explains decibels) and that 10 kHz is cut by at least 15 dB (to less than about a sixth). For each part, ask: at 100 Hz and at 10 kHz, is its impedance much bigger or much smaller than 1 k ohm? Compute 1 / (2 pi f C) and 2 pi f L at both frequencies before you press RUN.

## Common Mistakes

- **Thinking a filter changes frequencies.** A linear filter only changes the amplitude and phase of each frequency component. It never creates new ones.
- **Expecting a sharp edge.** A simple RC filter changes gradually: at fc the gain is still 0.707, and a tenth of fc is not perfectly passed. Brick walls do not exist.
- **Expecting a gain of 0.5 at the cutoff.** It is 0.707, because the resistor's and capacitor's voltages are a quarter cycle apart and add like the sides of a right triangle.
- **Forgetting the load.** Connecting a low-resistance load to the output changes the filter (it is in parallel with the capacitor). Lesson 03 shows how to keep stages from loading each other.
- **Placing the cutoff on the wanted frequency.** Put it between the wanted and unwanted frequencies, as far from both as possible.

## Exercises

1. **Easy.** Find the cutoff frequency of an RC low-pass with R = 4.7 k ohm and C = 10 nF.
2. **Easy.** For the filter in this lesson (fc = 1592 Hz), compute the gain at 50 Hz, 3 kHz and 20 kHz with the formula.
3. **Medium.** You want to keep a 10 Hz heartbeat signal and remove 1 kHz interference by at least a factor of 10. With C = 1 µF, what range of R works? Keep the heartbeat's gain above 0.95. (Hint: write both conditions as limits on fc, then turn them into limits on R.)
4. **Medium.** Change `two_tone_through` so the input is the 200 Hz tone plus a 50 Hz hum of 0.5 V. Which filter, low-pass or high-pass, would help, and how much? Predict, then run.
5. **Hard.** The square wave's harmonics fall as 1/n. After the low-pass, far above fc, each harmonic is also multiplied by about fc/f. How fast do the output harmonics fall with n? Explain why the output looks like rounded corners rather than a sine.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Filter | "Removes noise" | A circuit whose gain depends on frequency, passing some components of a signal and attenuating others |
| Spectrum | "The frequencies in a signal" | The amplitude (and phase) of each sine component that sums to the signal |
| Harmonic | "Overtone" | A component at an integer multiple of a repeating signal's fundamental frequency |
| Cutoff frequency | "Where the filter starts working" | For an RC filter, fc = 1 / (2 pi R C), where the gain is 0.707 (-3 dB) |
| Gain | "How much gets through" | Output amplitude over input amplitude at one frequency |
| Low-pass / high-pass | "Bass / treble filter" | Gain near 1 below / above fc, falling on the other side |
| Frequency response | "The filter curve" | Gain and phase as functions of frequency |

## Further Reading

- [All About Circuits, Volume II, Chapter 8: Filters](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-8/what-is-a-filter/) — low-pass, high-pass, band-pass and band-stop with RC, RL and LC
- [The Art of Electronics (Horowitz & Hill), 3rd edition, chapter 1, RC filters](https://artofelectronics.net/) — the practical view of filters and their cutoffs
- [Khan Academy: Fourier series](https://www.khanacademy.org/science/electrical-engineering/ee-signals) — how a square wave is built from sines
- [3Blue1Brown: "But what is a Fourier series?"](https://www.3blue1brown.com/lessons/fourier-series) — a visual explanation of signals as sums of rotating arrows
