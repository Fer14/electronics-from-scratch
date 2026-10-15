# Quality Factor

> Q is one number that tells you three things at once: how narrow a resonance is, how much it magnifies, and how long it keeps ringing after you stop pushing.

**Type:** Learn
**Prerequisites:** Phase 10 (Filters and Resonance), Lessons 05 (RLC Resonance) and 06 (Band-Pass and Band-Stop)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Quality factor (Q) | A pure number describing how "good" (low-loss) a resonance is | A crystal glass (high Q) versus a cardboard box (low Q) when you tap them |
| Bandwidth (BW) | The width between the -3 dB points of a resonance, in Hz | How far off-key you can sing and still make the glass hum |
| Selectivity | How well a filter separates a wanted frequency from a nearby unwanted one | Hearing one voice in a noisy room |
| Damping | Energy loss per cycle; the opposite of Q | Friction on a swing |
| Decay envelope | The smooth curve joining the peaks of a dying oscillation | The fading loudness of a bell |
| Characteristic impedance | sqrt(L / C): the reactance of L or C at resonance, in ohms | The "size" of the sloshing |
| Loaded Q | The Q of a resonant circuit once the source and load resistances are included | A swing with a child on it, not just the empty swing |
| Settling time | How long a resonant circuit takes to reach its steady response after a change | How many pushes it takes to get a swing going |

## Learning Objectives

- Define Q three ways (f0 / BW, sqrt(L/C) / R, 2 pi x stored energy / energy lost per cycle) and show they agree
- Measure bandwidth from a simulated sweep and compute Q from it
- Relate Q to the ringing decay: each cycle the amplitude shrinks by e^(-pi/Q), so it rings for about Q cycles
- Use Q to predict how well a filter rejects a nearby frequency
- Choose R to get a Q that is neither too low (poor selectivity) nor too high (too narrow, too slow)

## The Problem

In Lessons 05 and 06 we kept meeting the same number: the voltage magnification at resonance was sqrt(L/C) / R; the centre frequency divided by the bandwidth gave the same value; and the ringing lasted longer when R was smaller. Engineers call this number **Q**, the **quality factor**, and it is the single most useful description of anything that resonates: tuned circuits, crystals, antennas, microwave cavities, guitar strings, bridges, even atoms.

Getting Q right is a design decision with a trade-off. A radio receiver with too low a Q hears two stations at once. With too high a Q, it cannot follow a station that drifts slightly, and it distorts the sound because the edges of the signal (which occupy a few kilohertz) fall outside the narrow peak. A loudspeaker with a high-Q resonance "booms" on one note. A power supply filter with high Q can ring and overshoot. This lesson ties the three faces of Q together and gives you the tools to choose it.

## The Physics

### Q as an energy ratio

The deepest definition of Q is about energy:

```
Q = 2 pi * (energy stored in the resonator) / (energy lost per cycle)
```

Read it: "Q is two pi times the energy sloshing back and forth, divided by the energy turned into heat during one cycle". A crystal glass stores the energy of its vibration and loses only a tiny fraction to the air each cycle: it has a Q of thousands and rings for seconds. A cardboard box loses most of its vibration energy in every cycle: Q of 1 or 2, a dull thud.

For a series RLC at resonance with peak current I:

- The energy sloshing between L and C is ½ L I² (when the current peaks, all the energy is in the inductor).
- The resistor turns power ½ I² R into heat (the average of a sine squared is ½, Phase 09, Lesson 03), so in one cycle of duration T = 1 / f0 it loses ½ I² R / f0.

```
Q = 2 pi * (1/2 L I^2) / (1/2 I^2 R / f0) = 2 pi f0 L / R = X_L / R
```

and since at f0 we have X_L = X_C = sqrt(L / C):

```
Q = sqrt(L / C) / R
```

**Worked example.** L = 10 mH, C = 1 µF, R = 10 ohm, 1 V drive. I = 1 / 10 = 0.1 A. Stored: ½ x 0.01 x 0.01 = 50 µJ. Lost per cycle: ½ x 0.01 x 10 / 1591.5 = 31.42 µJ. Q = 2 pi x 50 / 31.42 = 10.0.

### Q as sharpness: the bandwidth

The -3 dB edges of a series RLC band-pass are where the net reactance equals R in size, so that |Z| = sqrt(2) R. Working through the algebra gives

```
BW = f_high - f_low = R / (2 pi L) = f0 / Q
```

So the second definition is

```
Q = f0 / BW
```

"Q is the centre frequency divided by the bandwidth". A Q of 10 at 1592 Hz has a 159 Hz bandwidth; a Q of 100 only 15.9 Hz. Notice Q is a *relative* width: a Q of 10 at 1 MHz means a 100 kHz bandwidth.

### Q as ringing: the decay per cycle

Strike a resonator and let it go. Its oscillation decays exponentially, with the envelope e^(-t / tau_d). For a series RLC, tau_d = 2L / R. In one period T = 1/f0, the amplitude shrinks by the factor

```
e^(-T / tau_d) = e^(-R / (2 L f0)) = e^(-pi / Q)
```

"each peak is e to the minus pi over Q times the previous one". With Q = 10: e^(-0.314) = 0.730, a 27 % drop per cycle. With Q = 100: e^(-0.0314) = 0.969, a 3 % drop. After Q cycles the amplitude has fallen to e^(-pi) = 0.043, about 4 %. **A resonator rings for about Q cycles.** A guitar string with Q = 1000 vibrating at 110 Hz rings for about 1000 / 110 = 9 seconds.

The same time scale governs **settling**: when you switch on a sine at f0, the response takes about Q cycles to build up to its full size. High-Q filters are slow. That is the time-domain price of a narrow bandwidth, and it is a deep rule: **bandwidth times response time is roughly constant** (you met the low-pass version in Lesson 02: rise time = 0.35 / bandwidth).

### Where the "R" comes from in real circuits

In a real tuned circuit, R includes every loss: the coil's wire resistance (usually the largest), the capacitor's ESR, the source's output resistance, the load's resistance, and at radio frequencies, eddy currents, skin effect and radiation. The Q of the bare parts is the **unloaded Q**; connecting a source and load always lowers it to the **loaded Q**. For a parallel tank fed by a current source, a *large* parallel resistance means *high* Q (the opposite of the series case): Q = R_parallel / sqrt(L/C). A loading resistor across a tank therefore lowers its Q.

Typical values: coils for audio, Q of 10 to 100; RF coils, 50 to 300; ceramic resonators, about 1000; quartz crystals, 10,000 to 1,000,000.

## The Concept

The three faces of Q on one card, for a series RLC:

```
  parts      Q = sqrt(L / C) / R = 2 pi f0 L / R
  bandwidth  Q = f0 / BW            ->  BW = f0 / Q = R / (2 pi L)
  energy     Q = 2 pi * stored / lost per cycle
  ringing    each cycle the amplitude is multiplied by e^(-pi / Q)
             rings (and settles) in about Q cycles
  magnify    V_L = V_C = Q x V_source at f0
  tank       Z_tank(f0) = Q x sqrt(L / C)   (for a coil of resistance R in parallel with C)
```

### Selectivity: how Q rejects a neighbour

How much does a series RLC band-pass cut a signal at a frequency f near f0? Using the impedance:

```
|H(f)| = 1 / sqrt(1 + Q^2 (f/f0 - f0/f)^2)
```

For a neighbour 10 % above f0: f/f0 - f0/f = 1.1 - 0.909 = 0.191.

- Q = 1: |H| = 1 / sqrt(1 + 0.0365) = 0.982 (-0.16 dB). No rejection to speak of.
- Q = 10: |H| = 1 / sqrt(1 + 3.65) = 0.464 (-6.7 dB).
- Q = 100: |H| = 1 / sqrt(1 + 365) = 0.052 (-25.6 dB).

To separate close frequencies you need high Q. But the wanted signal itself has a bandwidth (a voice on AM radio occupies about ±5 kHz around the carrier), and a Q so high that BW is narrower than the signal cuts the edges of the signal off.

```
 gain (dB)
   0 |            /\            <- Q = 100: tall and needle-thin
     |           /  \
  -3 |     ____/ /\ \____       <- Q = 10: the -3 dB width is f0 / 10
     |    /     /  \     \
 -10 |___/_____/    \_____\___  <- Q = 1: a gentle hill
     +----------+----------+---> f (log)
              f0
```

### Choosing Q: the design trade

Suppose a pilot tone at 1592 Hz may drift by up to 4 % (to 1650 Hz), and an interferer sits at 2 kHz. We need:

- At 1650 Hz, gain above -6 dB: the bandwidth must be wide enough.
- At 2000 Hz, gain below -10 dB: the bandwidth must be narrow enough.

With L = 10 mH and C = 1 µF (sqrt(L/C) = 100 ohm):

| R | Q | Gain at 1650 Hz | Gain at 2000 Hz | Verdict |
|---|---|---|---|---|
| 1 ohm | 100 | -17 dB | -33 dB | too sharp: loses the drifted tone |
| 10 ohm | 10 | -1.8 dB | -13.5 dB | just right |
| 100 ohm | 1 | -0.02 dB | -0.8 dB | too blunt: passes the interferer |

Check the 10 ohm line at 1650 Hz: f/f0 - f0/f = 1.0368 - 0.9645 = 0.0723; Q² x 0.0723² = 100 x 0.00523 = 0.523; |H| = 1 / sqrt(1.523) = 0.810 = -1.8 dB. That is the lab task.

### Loaded Q: what the rest of the circuit does

The Q you compute from the parts alone is rarely the Q you get. Two worked examples.

**Series circuit with a source resistance.** Our series RLC (L = 10 mH, C = 1 µF, R = 10 ohm, Q = 10) is driven by a signal generator with a 50 ohm output resistance. The current now flows through 50 + 10 = 60 ohm, so the loaded Q is 100 / 60 = 1.67 and the bandwidth grows from 159 Hz to 955 Hz. The filter has almost stopped being selective. Low-Q sources ruin series resonators: drive them from a low resistance, or use a parallel tank instead.

**Parallel tank with a load.** A tank of 10 mH and 1 µF whose coil has 0.1 ohm of resistance has Q = 1000 and an impedance at resonance of Q x sqrt(L/C) = 1000 x 100 = 100 k ohm (Step 5 below). Connect a 100 k ohm load across it: the two 100 k ohm impedances in parallel make 50 k ohm, and the loaded Q halves to 500. Connect a 10 k ohm load and the total is 9.1 k ohm: the loaded Q falls to about 91. **For a parallel tank, Q_loaded = R_total_parallel / sqrt(L/C)**: the load must be large compared with the tank's own resonant impedance or it dominates.

### Settling time in numbers

A resonator needs about Q cycles to build up (and to die away). In seconds that is Q / f0, which is the same as 1 / BW (up to a factor near 1 / pi). Examples:

| Resonator | f0 | Q | Settles in about |
|---|---|---|---|
| Our series RLC | 1592 Hz | 10 | 10 cycles = 6.3 ms |
| An audio notch for 50 Hz hum | 50 Hz | 30 | 30 cycles = 0.6 s |
| A 455 kHz radio IF filter | 455 kHz | 50 | 50 cycles = 0.11 ms |
| A 32.768 kHz watch crystal | 32.768 kHz | 50,000 | 50,000 cycles = 1.5 s |

That last line is why a crystal oscillator takes a noticeable time to start after power-up, and why microcontrollers wait (a "start-up time" in the datasheet) before trusting their clock. The 50 Hz notch row explains why Lesson 06 had to simulate a whole second before measuring the hum.

## Build It

### Step 1: Q three ways

```python
def series_band_pass(resistance):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=F0)
    c.inductor("L1", "in", "a", L)
    c.capacitor("C1", "a", "out", C)
    c.resistor("R1", "out", "0", resistance)
    return c


def measured_bandwidth(resistance):
    g = series_band_pass(resistance).ac(FREQS, source="V1").gain_db("out")
    target = g.max() - 3.0103
    peak = int(np.argmax(g))
    logf = np.log10(FREQS)
    low = 10 ** np.interp(target, g[:peak + 1], logf[:peak + 1])
    high = 10 ** np.interp(target, g[peak:][::-1], logf[peak:][::-1])
    return low, high
```

We sweep 8001 frequencies over two decades around f0 and find where the gain crosses 3.01 dB below the peak on each side, interpolating between sweep points. (`np.interp` needs its x values increasing; on the high side the gain falls, so we reverse that half with `[::-1]`.)

```
      R    Q = sqrt(L/C)/R    f_low     f_high    BW       Q = f0 / BW
     1.0      100.00         1583.6    1599.5     15.9      100.00
    10.0       10.00         1514.0    1673.1    159.2       10.00
   100.0        1.00          983.6    2575.2   1591.5        1.00
```

The formula and the measurement agree for every R. Notice the edges are geometrically symmetric: 1514.0 x 1673.1 = 1591.5².

### Step 2: The energy definition

```
  peak current 100 mA, energy sloshing between L and C = 1/2 L I^2 = 50.0 uJ
  heat per cycle = (1/2 I^2 R) x T = 31.42 uJ
  Q = 2 pi x stored / lost = 10.00
```

### Step 3: Ringing

```python
def ring_down(resistance, cycles=40):
    c = Circuit()
    c.capacitor("C1", "top", "0", C, v0=1.0)
    c.inductor("L1", "top", "m", L)
    c.resistor("R1", "m", "0", resistance)
    period = 1 / F0
    run = c.transient(t_stop=cycles * period, dt=period / 400)
    v = np.asarray(run.v("top"))
    t = np.asarray(run.time)
    peaks = [n for n in range(1, len(v) - 1) if v[n] > v[n - 1] and v[n] >= v[n + 1] and v[n] > 0]
    return t[peaks], v[peaks]
```

We start the capacitor at 1 V and find every positive peak (a sample bigger than both neighbours). Output:

```
  R =   1.0 ohm, Q = 100.00: each peak is 0.9691 of the one before (e^(-pi/Q) = 0.9691); falls below 4.3 % after 99 cycles
  R =  10.0 ohm, Q =  10.00: each peak is 0.7301 of the one before (e^(-pi/Q) = 0.7304); falls below 4.3 % after 9 cycles
  R =  33.0 ohm, Q =   3.03: each peak is 0.3496 of the one before (e^(-pi/Q) = 0.3546); falls below 4.3 % after 2 cycles
```

"About Q cycles" is confirmed: 99 for Q = 100, 9 for Q = 10. At low Q the measured ratio drifts slightly from e^(-pi/Q) because heavy damping also slows the oscillation (Lesson 05).

### Step 4: Selectivity

```
  Q = 100.00: wanted  -0.00 dB, neighbour  -25.63 dB, rejection  25.6 dB
  Q =  10.00: wanted  -0.00 dB, neighbour   -6.67 dB, rejection   6.7 dB
  Q =   1.00: wanted  -0.00 dB, neighbour   -0.16 dB, rejection   0.2 dB
```

These match the hand calculation above.

### Step 5: Tank impedance and Q

For a parallel tank whose coil has resistance R, the impedance at resonance is Q x sqrt(L/C): 1 k ohm for a 10 ohm coil, 10 k ohm for 1 ohm, 100 k ohm for 0.1 ohm. (Lesson 05 measured the 1 ohm case: 10 k ohm.) Better coils make taller impedance peaks.

## Use It

- **Crystal oscillators.** A 16 MHz crystal with Q = 50,000 has a bandwidth of only 320 Hz: the oscillator can only run within a tiny window, which is why microcontroller clocks are accurate to about 20 parts per million. Datasheets give the "motional resistance" (ESR) and you can compute Q from it.
- **Radio front ends.** An FM receiver's input filter might have a loaded Q of about 5 to 10 (wide enough for the whole 88-108 MHz band); its IF filter has a much higher effective selectivity to pick one 200 kHz channel.
- **Loudspeaker design.** A speaker in a box has a bass resonance described by its "Qtc": about 0.7 gives the flattest response, about 1 or more sounds "boomy", about 0.5 sounds tight but thin. Same Q, different field.
- **Wireless power.** Qi chargers use coils with Q of 50 to 100 so that energy can transfer efficiently across a gap; higher Q tolerates weaker coupling.
- **Musical instruments.** A piano string has a Q of a few thousand, which is why a note sustains; the felt damper lowers its Q to almost nothing when you release the key. Electronic synthesizer filters expose a "resonance" knob that is literally a Q control.
- **Damping on purpose.** Power-supply designers add small resistors (snubbers) or choose capacitors with some ESR to lower the Q of parasitic LC resonances, so they do not ring when the load changes.
- **Measuring Q.** A network analyser sweeps the circuit and measures BW; or you strike it and count cycles on an oscilloscope until the ringing falls to 4 %.

## Try It in the Lab

Open **"Sharp enough, but not too sharp"**. A series 10 mH coil and 1 µF capacitor are fixed; the resistor sets the Q. The filter must pass 1.59 kHz within 1 dB, still pass 1.65 kHz within 6 dB (the tone may drift), and cut 2 kHz by at least 10 dB. For each resistor, compute Q and the bandwidth f0 / Q. Then estimate the gain at 1.65 kHz and 2 kHz with the selectivity formula. One resistor fails because the filter is too wide; another because it is too narrow. Before running it, decide which is which.

## Common Mistakes

- **Thinking higher Q is always better.** High Q means narrow and slow. Choose the Q the signal needs.
- **Forgetting the source and load.** The loaded Q includes every resistance in the circuit. A 50 ohm generator in series with a 10 ohm resonator ruins its Q.
- **Using Q = sqrt(L/C) / R for a parallel circuit with a parallel resistor.** For a resistor in parallel with the tank, Q = R_parallel / sqrt(L/C): bigger R means higher Q.
- **Measuring bandwidth on a linear scale and the centre as the average.** The edges are geometrically symmetric: f0 = sqrt(f_low x f_high).
- **Quoting Q without saying loaded or unloaded.** A coil's datasheet Q (for example "Q = 60 at 1 MHz") is its unloaded Q at one frequency. The circuit's Q will be lower, and the coil's Q changes with frequency.
- **Treating Q as only a filter idea.** Any resonance has a Q, including the unwanted ones: a long cable, a capacitor's parasitic inductance, a loudspeaker cabinet. High-Q parasitics are the ones that ring and cause trouble.
- **Expecting a high-Q filter to respond instantly.** It needs about Q cycles to build up and to die away.

## Exercises

1. **Easy.** A resonance at 455 kHz has a bandwidth of 9.1 kHz. What is its Q?
2. **Easy.** A series RLC has L = 4.7 mH, C = 47 nF and R = 15 ohm. Find f0, sqrt(L/C), Q and BW.
3. **Medium.** A bell ringing at 800 Hz takes 2 s for its sound to fall to about 4 % of the start. Estimate its Q.
4. **Medium.** Using the selectivity formula, find the gain of a Q = 30 filter at f0 and at 1.05 f0 and 0.95 f0. Then check with `series_band_pass` by choosing R = sqrt(L/C) / 30.
5. **Hard.** Add a 50 ohm source resistance in series with the generator in `series_band_pass` (keep R = 10 ohm as the output resistor). Compute the new loaded Q, and the new peak gain at "out". Verify both with the simulator and explain why the peak is no longer 0 dB.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Quality factor | "Q, the sharpness" | 2 pi x stored energy / energy lost per cycle; for a series RLC sqrt(L/C) / R = f0 / BW |
| Bandwidth | "BW, how wide" | Distance between the -3 dB points; BW = f0 / Q |
| Selectivity | "How well it rejects neighbours" | The gain difference between f0 and a nearby frequency, set by Q |
| Decay per cycle | "How fast it dies" | Each oscillation peak is e^(-pi/Q) of the previous; about Q cycles to fall to 4 % |
| Loaded Q | "Real-life Q" | The Q including source, load and every loss, always lower than the parts' own Q |
| Damping | "Losses" | Energy removed per cycle; low Q means heavy damping |

## Further Reading

- [All About Circuits, Volume II, Chapter 6: Q and bandwidth of a resonant circuit](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-6/q-and-bandwidth-resonant-circuit/) — Q, bandwidth and their link, with examples
- [The Feynman Lectures on Physics, Vol. I, Chapter 23 (Resonance) and Chapter 24 (Transients)](https://www.feynmanlectures.caltech.edu/I_23.html) — Q for mechanical and electrical oscillators, and the decay of ringing
- [MIT OpenCourseWare 6.002, lecture on the series RLC and quality factor](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) — the second-order circuit in depth
- [Microchip AN826, "Crystal Oscillator Basics and Crystal Selection for rfPIC and PICmicro Devices"](https://ww1.microchip.com/downloads/en/AppNotes/00826a.pdf) — Q, ESR and load capacitance in real timing parts
