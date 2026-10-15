# RL Filters

> An inductor is a capacitor turned inside out: it passes slow signals and blocks fast ones. Put it in series and you get a low-pass that wastes no DC power.

**Type:** Learn
**Prerequisites:** Phase 10 (Filters and Resonance), Lessons 02 (RC Low-Pass and High-Pass) and 03 (Decibels and Bode Plots); Phase 08 (Magnetism and Inductors), Lessons 04 (The Inductor) and 05 (RL Transients); Phase 09 (Alternating Current), Lesson 06 (Impedance)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Inductive reactance (X_L) | An inductor's opposition to AC: 2 pi f L ohms, growing with frequency | A heavy door: easy to push slowly, hard to swing fast |
| RL low-pass | Inductor in series, resistor to ground: passes low frequencies | A heavy door in the doorway lets people stroll through but stops a stampede |
| RL high-pass | Resistor in series, inductor to ground: passes high frequencies | The inductor shorts the slow stuff to ground |
| Crossover | A pair of filters that splits audio between a woofer and a tweeter | A traffic officer sending trucks one way and motorbikes the other |
| Woofer / tweeter | Loudspeakers built for low / high frequencies | A big drum / a small bell |
| DCR | The inductor's wire resistance, from Phase 08 | The friction in the door's hinges |
| Choke | An inductor used to block high-frequency noise on a power line | A speed bump for ripple |
| Ripple | A small unwanted AC wiggle on top of a DC supply | Waves on the surface of a calm lake |
| Duality | The fact that swapping L for C (and series for parallel) gives mirror-image circuits | A photo and its negative |

## Learning Objectives

- Derive the RL low-pass and high-pass transfer functions from impedances and find fc = R / (2 pi L)
- Show with the simulator that an RL and an RC filter with the same cutoff have identical responses
- Design a first-order speaker crossover and check that the two halves share the power
- Predict how an inductor's DCR changes the pass-band gain and the cutoff
- Explain why inductors, not resistors, are used to filter power lines

## The Problem

An RC low-pass is cheap and simple. But it has a weakness: its resistor sits in series with the signal. For a small signal going into a high-resistance input, that is fine. For **power**, it is a disaster. A loudspeaker is about 8 ohm; a series resistor large enough to make a useful filter would eat most of the amplifier's power as heat. A 5 V supply feeding a 1 A load cannot afford a series resistor that drops half a volt and wastes half a watt just to remove some ripple.

The inductor solves this. At DC its impedance is (ideally) zero, so it passes the full DC current with no loss, while its impedance grows with frequency and blocks high-frequency signals. Every loudspeaker crossover, every power-supply ripple filter and every EMI filter on a mains cable uses inductors for this reason. This lesson builds RL filters and compares them with their RC cousins.

## The Physics

### The inductor's impedance

From Phase 08, an inductor obeys v = L di/dt: its voltage is proportional to how fast its current changes. For a sine current of frequency f, the faster the wiggle, the larger the voltage needed for the same current. Phase 09 packed this into the inductor's impedance:

```
Z_L = j * 2 pi f * L = j omega L
```

"the impedance of an inductor is j times two pi f times L". Its size, the **inductive reactance** X_L = 2 pi f L, *grows* with frequency: zero at DC, very large at high frequency. The j says the inductor's voltage *leads* its current by 90 degrees. Compare the capacitor, whose reactance 1 / (2 pi f C) *falls* with frequency and whose voltage *lags*.

Some numbers for L = 10 mH:

| f | X_L = 2 pi f L |
|---|---|
| 0 (DC) | 0 ohm (a wire) |
| 159 Hz | 10 ohm |
| 1592 Hz | 100 ohm |
| 15.9 kHz | 1000 ohm |
| 1 MHz | 62.8 k ohm (nearly open) |

### The RL low-pass

```
   V_in ---[ L ]---+--- V_out
                   |
                  [ R ]
                   |
   0 V ------------+

H = R / (R + j omega L) = 1 / (1 + j omega L / R)
```

This has exactly the form of the RC low-pass, 1 / (1 + j f/fc), with

```
fc = R / (2 pi L)
```

Read it: "the cutoff of an RL filter is the resistance divided by two pi times the inductance". It is where the inductor's reactance equals R. The time constant is tau = L / R (Phase 08, Lesson 05), and fc = 1 / (2 pi tau) as for RC.

**Worked example.** R = 100 ohm, L = 10 mH: fc = 100 / (2 x 3.1416 x 0.01) = 100 / 0.06283 = 1591.5 Hz. At fc/10 = 159 Hz, X_L = 10 ohm: H = 100 / (100 + 10j); |H| = 100 / sqrt(10,000 + 100) = 0.995. At 10 fc, X_L = 1000 ohm: |H| = 100 / sqrt(10,000 + 1,000,000) = 0.0995. The same numbers as the RC low-pass with the same fc in Lesson 02.

**Physically.** At low frequency the inductor is almost a wire and all the input reaches R. At high frequency the inductor's reactance is huge, almost no current flows, and the output is almost zero. The inductor "refuses" fast changes of current, which is precisely what we want to block.

### The RL high-pass

Swap them: resistor in series, inductor to ground.

```
   V_in ---[ R ]---+--- V_out
                   |
                  [ L ]
                   |
   0 V ------------+

H = j omega L / (R + j omega L)
```

At low frequency the inductor shorts the output to ground (output near 0); at high frequency the inductor is nearly open and the output follows the input. Same cutoff fc = R / (2 pi L), phase +45° at fc.

### Duality: RC and RL are mirror images

| | RC | RL |
|---|---|---|
| Low-pass | R in series, C to ground | L in series, R to ground |
| High-pass | C in series, R to ground | R in series, L to ground |
| Cutoff | 1 / (2 pi R C) | R / (2 pi L) |
| Time constant | R C | L / R |

For the same fc, the frequency responses are **identical**. What differs is practical: component size and cost, how much DC flows through the series part, and how the filter behaves with the real source and load.

### When to choose L over C

- **Low impedances and power.** At 8 ohm (speakers) or 1 to 10 ohm (power supplies), an RC filter would need a large series resistor that wastes power. An RL filter puts an inductor in series instead: no DC drop (apart from its DCR) and no DC loss.
- **High impedances and small signals.** For a 10 k ohm signal path at 1 kHz, an RL low-pass would need L = 10,000 / (2 pi x 1000) = 1.6 H: a large, heavy, expensive part. An RC with R = 10 k and C = 16 nF costs a cent. So small-signal filters use RC (or the active filters of Phase 13).
- **Real inductors are less ideal than real capacitors.** They have DCR, they can saturate, they pick up and radiate magnetic fields, and their value changes with current. Use them where their strengths matter.

## The Concept

### A first-order speaker crossover

A two-way speaker has a **woofer** (big cone, good at bass, poor at treble) and a **tweeter** (small dome, good at treble, damaged by bass). A **crossover** splits the amplifier output between them:

```
                 +---[ L ]---+---(woofer 8 ohm)---+
  amplifier o----+           |                    |
                 +---[ C ]---+---(tweeter 8 ohm)--+
                                                  |
  ground    o-------------------------------------+
```

The woofer branch is an RL low-pass (L in series with the 8 ohm woofer); the tweeter branch is an RC high-pass (C in series with the 8 ohm tweeter). For a crossover frequency of 2 kHz:

```
L = R / (2 pi fc) = 8 / (2 x 3.1416 x 2000) = 0.637 mH
C = 1 / (2 pi fc R) = 1 / (2 x 3.1416 x 2000 x 8) = 9.95 µF
```

At 2 kHz both speakers get -3 dB, which is half power each. At every frequency the two powers add up to the full power:

```
|H_woofer|^2 + |H_tweeter|^2 = 1 / (1 + x^2) + x^2 / (1 + x^2) = 1,      x = f / fc
```

```
 gain (dB)
   0 |-----------__              __-----------
     |  woofer     \__      __/    tweeter
  -3 |                 \  /             <- both -3 dB at 2 kHz
     |                 /  \
 -20 |          __/          \__
     +-----+------+------+------+-----> f (log)
         200 Hz  1 kHz  2 kHz  4 kHz  20 kHz
```

So the total sound power stays flat (in an ideal world where both speakers are 8 ohm resistors; real speakers are not, which is why real crossovers are more elaborate).

**Worked example at 1 kHz.** x = 0.5: woofer power share 1 / 1.25 = 0.8 (-0.97 dB), tweeter 0.25 / 1.25 = 0.2 (-6.99 dB). Total 1.0.

### What DCR does

A real 0.637 mH air-core coil wound from thin wire might have 0.3 to 1 ohm of DCR. That resistance is in series with the woofer, so:

- At low frequency the woofer gets 8 / (8 + DCR) of the voltage: with 1 ohm, 8/9 = 0.889 = -1.02 dB. A permanent loss of loudness and efficiency.
- The cutoff becomes (8 + DCR) / (2 pi L): with 1 ohm, 9 / (2 pi x 0.637e-3) = 2250 Hz instead of 2000.

Speaker builders buy thick-wire coils (low DCR) for woofer crossovers for exactly this reason.

### Cleaning a power line

A 5 V supply feeds a 5 ohm load (1 A) and carries ripple at 100 kHz from a switching converter. A 100 µH inductor in series with the load is an RL low-pass with fc = 5 / (2 pi x 100e-6) = 7958 Hz. The ripple at 100 kHz is 12.6 times above fc, so it is cut by about 20 log10(12.6) = 22 dB, to less than a tenth. At DC the inductor is a wire: the load still gets the full 5 V. An RC filter would need a series resistor; even 0.5 ohm would drop 0.45 V and waste 0.41 W. (In practice a capacitor is added across the load too, forming an LC filter with a steeper -40 dB per decade slope. Lessons 05 and 06 show what happens when L and C meet.)

### Designing an RL filter, step by step

A worked design from start to finish. A USB-powered audio board takes 5 V at 0.25 A, so it looks like a 20 ohm load. The USB supply carries noise at 1 MHz from the computer's switching regulators, and you want it at least 30 dB lower at the board.

1. **How far above fc must 1 MHz be?** A first-order filter falls at 20 dB per decade, so 30 dB needs 1.5 decades: a factor of 10^1.5 = 31.6. So fc must be at most 1,000,000 / 31.6 = 31.6 kHz.
2. **Which inductor?** With R = 20 ohm: L = R / (2 pi fc) = 20 / (2 x 3.1416 x 31,600) = 101 µH. Choose a standard 100 µH (fc = 31.8 kHz).
3. **Check the gain at 1 MHz.** f/fc = 31.4; |H| = 1 / sqrt(1 + 31.4²) = 0.0318 = -29.9 dB. A hair short of the target, because standard values rarely land exactly; a 150 µH part (fc = 21.2 kHz, -33.5 dB at 1 MHz) gives margin.
4. **Check DC.** The inductor must carry 0.25 A without saturating, so pick one with I_sat of at least 0.5 A. Its DCR, say 0.4 ohm, drops 0.25 x 0.4 = 0.1 V and wastes 0.25² x 0.4 = 25 mW: acceptable.
5. **Check the load is really resistive.** If the board itself has a big capacitor at its input (it usually does), the filter is really an LC filter, with a resonance (Lesson 05). That is usually good (steeper roll-off) but can ring; Lesson 07 shows how to judge it.

```
   USB 5 V ---[ 100 uH, DCR 0.4 ohm ]---+--- board (about 20 ohm)
                                        |
   0 V ---------------------------------+
```

The same five steps (find the needed attenuation, convert to a cutoff, compute L, check the DC current and loss, check the real load) work for any RL filter.

## Build It

### Step 1: The RL low-pass by hand

```python
def rl_low_pass_response(freq, resistance, inductance):
    z_l = 1j * 2 * math.pi * freq * inductance
    return resistance / (resistance + z_l)


def rl_cutoff(resistance, inductance):
    return resistance / (2 * math.pi * inductance)
```

Output for R = 100 ohm, L = 10 mH: fc = 1591.5 Hz, tau = 100 µs; |Z_L| = 10, 100 and 1000 ohm at fc/10, fc and 10 fc, with |H| = 0.9950, 0.7071, 0.0995 and phases -5.7°, -45.0°, -84.3°.

### Step 2: RL against RC in the simulator

```python
PART = {"R": "resistor", "L": "inductor", "C": "capacitor"}


def series_then_shunt(series, shunt, dcr=0.0):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    start = "in"
    if dcr:
        c.resistor("Rdcr", "in", "w", dcr)
        start = "w"
    getattr(c, PART[series[0]])("Xseries", start, "out", series[1])
    getattr(c, PART[shunt[0]])("Xshunt", "out", "0", shunt[1])
    return c
```

One helper builds any "series part, then part to ground" filter. `getattr(c, "inductor")` is just a way of calling `c.inductor(...)` when the part name is stored in a variable. We compare the RL low-pass (10 mH, 100 ohm) with an RC low-pass with the same cutoff (1 k ohm, 100 nF):

```
  cutoffs: RL 1591.5 Hz, RC 1591.5 Hz
  largest gain difference: 8.69e-09 dB
  RL high-pass (R in series, L to ground): cutoff 1591.6 Hz, gain at fc/10 -20.04 dB, at 10 fc -0.04 dB
```

The two low-pass curves are identical to within rounding: the circuit's "shape" only depends on fc.

### Step 3: The crossover

```
     200 Hz: woofer   -0.04 dB, tweeter  -20.04 dB, total power share 1.000
    1000 Hz: woofer   -0.97 dB, tweeter   -6.99 dB, total power share 1.000
    2000 Hz: woofer   -3.01 dB, tweeter   -3.01 dB, total power share 1.000
   20000 Hz: woofer  -20.04 dB, tweeter   -0.04 dB, total power share 1.000
```

`10 ** (w / 10)` turns each dB gain back into a *power* ratio (10 log10 for power, Lesson 03), and the two always add to 1.000.

### Step 4: DCR

```
  DCR 0.0 ohm: woofer gain at 100 Hz -0.01 dB, cutoff  2000.0 Hz
  DCR 0.3 ohm: woofer gain at 100 Hz -0.33 dB, cutoff  2074.9 Hz
  DCR 1.0 ohm: woofer gain at 100 Hz -1.03 dB, cutoff  2249.9 Hz
```

Check the 1 ohm line by hand: 20 log10(8/9) = -1.02 dB (the extra 0.01 dB is the inductor's small reactance at 100 Hz), and 9 / (2 pi x 0.637e-3) = 2250 Hz.

### Step 5: The supply-line filter

The script shows the ripple at 100 kHz cut to -22.0 dB, then runs a DC analysis of the same circuit to show the load gets the full 5.000 V and 1.00 A, and compares with the loss a series resistor would cause.

## Use It

- **Speaker crossovers.** Commercial crossover coils are specified by inductance, DCR and wire gauge: for example "0.68 mH, 0.32 ohm, 18 AWG air core". Air cores are used because iron cores saturate at high audio power and distort.
- **Power-line EMI filters.** The IEC mains inlet on a computer or lab instrument often contains a "common-mode choke" plus capacitors, keeping the device's high-frequency switching noise out of the mains wiring. Datasheets specify the *insertion loss* in dB versus frequency: a Bode plot.
- **Ferrite beads** (Phase 08) are tiny lossy inductors used as RL low-passes on power pins: they pass DC and cut noise above tens of megahertz.
- **Switching regulator outputs** use an inductor and a capacitor as an LC low-pass that turns a chopped square wave into smooth DC (Phase 18).
- **Guitar pickups are RL low-passes.** A pickup's coil (a few henries, several kilo-ohms of DCR) driving the guitar cable and amplifier input forms a filter whose corner, with the cable's capacitance, sets much of the "tone" of the instrument. Long cables sound duller for exactly this reason.
- **Current sensing and ripple.** In motor drives the motor's own winding inductance, with its resistance, forms an RL low-pass that smooths the PWM current (Phase 18).

## Try It in the Lab

Open **"Keep the treble out of the woofer"**. The woofer is an 8 ohm resistor, and you choose the coil in series with it. The goals: a cutoff between 1.5 and 2.5 kHz, and at least 12 dB of cut at 20 kHz. Compute fc = R / (2 pi L) for each coil in the drawer (they are a factor of 10 apart). Then, using -20 dB per decade above fc, estimate the gain at 20 kHz for each. Which coil fails the cutoff but would still protect the woofer from treble very well?

## Common Mistakes

- **Writing fc = 1 / (2 pi R L).** For RL it is R / (2 pi L). Check the units: ohm / henry = 1/s.
- **Thinking a bigger inductor raises the cutoff.** A bigger L lowers fc (the reactance reaches R at a lower frequency), just as a bigger C does in an RC filter.
- **Forgetting the source and load resistance.** In an RL low-pass, R is the *total* resistance in the loop: the load, plus the DCR, plus the source's output resistance.
- **Using an RL filter at high impedance.** A 10 k ohm, 1 kHz RL filter needs over a henry. Use RC there.
- **Assuming the load is a pure resistor.** Real loads have input capacitance (and sometimes inductance). An RL filter feeding a capacitive load is really an LC filter with a resonance, which can boost noise near its resonant frequency instead of cutting it.
- **Expecting a ferrite bead to work at audio frequencies.** Beads are designed to be lossy above about 10 MHz; at 1 kHz they are just a few milliohms of wire.
- **Ignoring saturation.** A power inductor carrying more DC than its saturation current loses most of its inductance (Phase 08), and the filter stops filtering exactly when the load is heaviest.

## Exercises

1. **Easy.** Find the cutoff of an RL low-pass with L = 2.2 mH and R = 47 ohm.
2. **Easy.** Which inductor gives a 300 Hz cutoff with a 4 ohm speaker?
3. **Medium.** Design a first-order crossover at 3 kHz for a 6 ohm woofer and a 6 ohm tweeter. Give L and C, and the power share of each speaker at 1.5 kHz.
4. **Medium.** A supply filter uses 47 µH in series with a 2 ohm load. By how many dB does it cut ripple at 250 kHz? Check with `series_then_shunt(("L", 47e-6), ("R", 2.0))`.
5. **Hard.** The source (amplifier) has an output resistance of 0.2 ohm and the coil has 0.5 ohm DCR. Modify `series_then_shunt` to include both, and find the new woofer cutoff and low-frequency gain in the 2 kHz crossover. How would you compensate the coil value so that the cutoff returns to 2 kHz?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Inductive reactance | "The coil's AC resistance" | X_L = 2 pi f L, the size of Z_L = j omega L, growing with frequency |
| RL low-pass | "Series coil filter" | L in series, R to ground; H = 1 / (1 + j f/fc), fc = R / (2 pi L) |
| RL high-pass | "Shunt coil filter" | R in series, L to ground; passes above fc |
| Crossover | "The speaker filter" | Complementary low-pass and high-pass filters splitting a signal between drivers |
| DCR | "Coil resistance" | The winding's DC resistance, which adds loss and moves the cutoff |
| Duality | "L and C swap roles" | Exchanging inductors with capacitors and series with parallel gives circuits with mirror-image behaviour |

## Further Reading

- [All About Circuits, Volume II, Chapter 8: Filters (inductive low-pass and high-pass)](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-8/low-pass-filters/) — RL filters alongside RC ones
- [The Art of Electronics (Horowitz & Hill), 3rd edition, chapter 1, inductors and LC filters](https://artofelectronics.net/) — when to choose inductors in practice
- [Elliott Sound Products: "Passive Crossover Network Design"](https://sound-au.com/lr-passive.htm) — a detailed, practical guide to speaker crossovers
- Würth Elektronik, *Trilogy of Magnetics* (design guide), chapters on EMI filtering — real inductors and chokes in power-line filters
