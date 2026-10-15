# Amplifiers and Biasing

> An amplifier is a transistor parked half-on, in the middle of its range, so a small wiggle at the input becomes a large wiggle at the output. Biasing is the art of parking it in the same spot no matter which transistor you happen to have.

**Type:** Build
**Prerequisites:** 12-02 (The BJT); Phase 04 (Kirchhoff's Laws), lesson 05-the-voltage-divider; Phase 05 (Circuit Analysis and Our Simulator), lesson 06-thevenin-and-norton; Phase 10 (Filters and Resonance), lessons 03-decibels-and-bode-plots and 08-ac-analysis-in-our-simulator
**Time:** ~85 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Bias / operating point (Q point) | The steady DC voltages and currents of the transistor with no signal | Where a swing hangs at rest, so it can swing both ways |
| Biasing network | The resistors that set the operating point | The ropes holding the swing at the right height |
| Common-emitter amplifier | The basic BJT amplifier: input at the base, output at the collector, emitter shared (common) with ground | A see-saw: push one end down a little, the other end goes up a lot |
| Coupling capacitor | A capacitor that passes the AC signal but blocks the DC bias from the source | A pane of glass that lets light through but not wind |
| Bypass capacitor | A capacitor that short-circuits a resistor for AC signals only | A shortcut that is only open during the day |
| Emitter degeneration | An unbypassed emitter resistor, which lowers and stabilises the gain | A shock absorber that makes the ride less wild but more predictable |
| Voltage gain (A_v) | Output signal amplitude divided by input signal amplitude | The see-saw's arm ratio |
| Decibel (dB) | 20 × log₁₀ of a voltage ratio: ×10 is 20 dB, ×100 is 40 dB | A logarithmic ruler for ratios |
| Headroom / clipping | How far the output can swing before it hits a rail; beyond that, the waveform is cut flat | A swing hitting the ground or the bar above |
| Thevenin equivalent | A complex network reduced to one voltage source and one resistor (Phase 05) | Replacing a messy plumbing system by "one tank at this height through one pipe" |
| Inverting | The output moves opposite to the input (180° phase shift) | The see-saw again |
| Negative feedback | Part of the output is fed back to oppose the input, trading gain for stability | A thermostat that turns the heater down as the room warms up |

## Learning Objectives

- Explain why an amplifier needs a DC operating point in the middle of its range.
- Show why "fixed bias" (one base resistor) is unreliable, and why a divider plus an emitter resistor is stable.
- Compute the operating point of a divider-biased common-emitter stage by hand, using a Thevenin equivalent.
- Estimate the voltage gain, |A_v| ≈ R_C / (R_E + r_e), and the bypassed gain R_C / r_e; check both with AC analysis.
- Recognise clipping and the trade-off between gain, stability and headroom.

## The Problem

A microphone delivers a few millivolts. A guitar pickup, about 100 mV. A loudspeaker needs volts. Somewhere in between, a transistor must multiply the signal by 10, 100 or 1000, faithfully: the output must be an enlarged *copy* of the input, not a distorted one.

Lesson 01 showed the idea: park a transistor half-on and wiggle its control. Lesson 02 showed the trouble: the collector current depends on β, which varies from part to part by a factor of 2-3, and on temperature. If you build an amplifier with one base resistor, one transistor might sit nicely at mid-supply, the next one saturated at the bottom, and the amplifier stops working the moment you swap parts. This lesson builds the standard solution, the divider-biased common-emitter stage, and measures it in three ways: by hand, with the simulator's DC and AC analyses, and in the time domain.

## The Physics

### Why the operating point must sit in the middle

The output of an amplifier swings around its DC operating point. It can rise until the transistor turns off (output at the supply) and fall until the transistor saturates (output near the emitter voltage). For the largest undistorted swing, the collector should rest roughly in the middle.

```
   12 V  ------------------------------------  top rail (transistor cut off)
                /\        /\        /\
   ~8.8 V ---- /  \------/  \------/  \------  operating point (no signal)
                    \  /      \  /
   ~0.3 V ----------\/--------\/-------------  bottom (transistor saturated)
```

### Why β is the enemy, and negative feedback the cure

In a **fixed-bias** circuit, a resistor R_B from the supply sets I_B, so I_C = β I_B depends directly on β. Double β, double the current, and the collector voltage moves by volts.

Put a resistor R_E in the emitter, and set the *base voltage* instead of the base current (with a divider). Now:

- The emitter sits one V_BE (about 0.65 V) below the base: V_E ≈ V_B − 0.65.
- The emitter current is then V_E / R_E, which does not depend on β at all.

If the transistor tries to carry more current (higher β, or warmer), V_E rises, which reduces V_BE, which reduces the current. That self-correction is **negative feedback**, the most important idea in analogue electronics, and the core of Phase 13.

What the analogy gets wrong: a thermostat measures and acts; nothing in this circuit "measures". The feedback is physical and instant: the same current that flows through the transistor flows through R_E, and its voltage automatically subtracts from the drive.

## The Concept

### The circuit

```
          +12 V ------+------------+
                      |            |
                    [R1] 100 kΩ  [R_C] 2.2 kΩ
                      |            |
   v_in --||---+------+--- b       +------ c  (output)
         C_IN  |           \       |
        10 µF  |            |Q1 (β = 100)
             [R2] 10 kΩ    /
               |           e
               |           |
               |         [R_E] 200 Ω   (optionally bypassed by C_E = 470 µF)
               |           |
   ground -----+-----------+
```

The coupling capacitor C_IN lets the AC input through while keeping the source from disturbing the DC bias at the base.

### Step 1: The DC operating point, by hand

**Replace the divider by its Thevenin equivalent** (Phase 05). Seen from the base, R1 and R2 are a source of

```
V_TH = 12 × 10 k / (100 k + 10 k) = 1.091 V      through      R_TH = 100 k ∥ 10 k = 9091 Ω
```

**Write KVL around the base-emitter loop**: V_TH = I_B × R_TH + V_BE + I_E × R_E. With I_B = I_E / (β + 1):

```
I_E = (V_TH − V_BE) / ( R_E + R_TH / (β + 1) )
    = (1.091 − 0.66) / (200 + 9091/101)
    = 0.431 / (200 + 90)
    = 1.486 mA
```

Read the denominator: R_E is "the emitter's own resistor"; R_TH/(β+1) is the divider's resistance as seen through the transistor, divided by β + 1. When R_E is much bigger than R_TH/(β+1), β drops out. Here 200 Ω versus 90 Ω: β still matters a bit (we'll see by how much).

**Collector voltage**: V_C = 12 − I_C × R_C ≈ 12 − 0.99 × 1.486 mA × 2200 = 8.76 V.

### Step 2: The simulator's operating point

```
V_B = 0.9586 V   V_E = 0.2941 V   V_BE = 0.6645 V
I_C = 1.4558 mA   V_C = 8.797 V   V_CE = 8.503 V
```

Our hand result was within 2 %. (The base sits below V_TH because the base current, 14.6 µA, flows through R_TH: 1.091 − 0.0146 mA × 9.091 kΩ = 0.958 V ✓.) The collector rests at 8.8 V, leaving 3.2 V of room upward and about 8.2 V downward. For maximum symmetric swing we'd lower it to about 6 V; this design favours a stable bias over maximum swing.

### Step 3: Stability against β

The script compares fixed bias (750 kΩ from 12 V to the base, chosen to give the same current at β = 100) with our divider-plus-R_E design:

| β | Fixed bias: I_C | V_C | Divider + R_E: I_C | V_C |
|---|---|---|---|---|
| 50 | 0.757 mA | 10.33 V | 1.123 mA | 9.53 V |
| 100 | 1.511 mA | 8.68 V | 1.456 mA | 8.80 V |
| 200 | 3.018 mA | 5.36 V | 1.713 mA | 8.23 V |
| 300 | 4.522 mA | 2.05 V | 1.821 mA | 7.99 V |

Fixed bias: current proportional to β, collector all over the place, nearly saturated at β = 300. Divider + R_E: a six-fold change in β moves the current by only 60 % and the collector by 1.5 V. With a larger R_E (or a stiffer divider) it would be better still; the textbook rule is R_TH ≤ 0.1 × β_min × R_E.

### Step 4: The voltage gain

A small input wiggle v_in moves the base, and (because the emitter follows the base) the emitter by nearly the same amount. The extra emitter current is v_in / (R_E + r_e), where **r_e** is the transistor's own small emitter resistance:

```
r_e = V_T / I_C = 25.85 mV / 1.456 mA = 17.76 Ω
```

(Lesson 07 derives r_e from the diode equation's slope. Think of it as "the base-emitter junction's dynamic resistance", the same g_d of lesson 11-05.) That current also flows through R_C, so the collector moves by −R_C times it:

```
|A_v| = R_C / (R_E + r_e) = 2200 / (200 + 17.76) = 10.10   →  20 log10(10.10) = 20.09 dB
```

The simulator's AC analysis at 1 kHz: **|A_v| = 10.01 (20.01 dB), phase −179.9°** (inverting). Our estimate is within 1 %.

Notice that **the gain depends almost only on the ratio of two resistors**, R_C / R_E. That is the reward of degeneration: predictable gain.

### Bypassing R_E for more gain

Put a large capacitor C_E (470 µF) across R_E. For DC it is open, so the bias is unchanged (still stable). For a 1 kHz signal its impedance is 1/(2π × 1000 × 470 µF) = 0.34 Ω, which shorts R_E. The gain becomes

```
|A_v| = R_C / r_e = 2200 / 17.76 = 123.9
```

The simulator: **123.8**. Twelve times more gain, but now it depends on r_e = V_T / I_C, i.e. on the current, on temperature, and on β through the bias:

| β | Degenerated gain | Bypassed gain |
|---|---|---|
| 50 | 9.69 | 95.5 |
| 100 | 10.01 | 123.8 |
| 300 | 10.24 | 154.9 |

That is the fundamental trade-off: **gain versus predictability**. Phase 13's op-amps resolve it by starting with an enormous, unpredictable gain and using negative feedback to set a small, precise one.

### Step 5: Watching it in time

Feed a 1 kHz sine and look at the collector:

| Input (peak) | Collector min | Collector max | Swing (peak-to-peak) | Ratio |
|---|---|---|---|---|
| 50 mV | 8.295 V | 9.296 V | 1.000 V | 10.00 |
| 200 mV | 6.763 V | 10.722 V | 3.959 V | 9.90 |
| 500 mV | 3.641 V | 11.999 V | 8.358 V | 8.36 |

At 50 mV the output is a clean ×10 copy. At 500 mV it would need to swing ±5 V around 8.8 V, i.e. up to 13.8 V; the top flattens at 12 V where the transistor cuts off: **clipping**. The bias point decided where the clipping starts.

### Design recipe (degenerated common-emitter)

1. Choose I_C (0.5-5 mA for small-signal stages).
2. Choose V_E ≈ 1-2 V for good stability (we used 0.3 V to get gain 10 from a 12 V supply; more V_E would be more stable). Then R_E = V_E / I_E.
3. Choose R_C for the desired gain, R_C ≈ A_v × (R_E + r_e), and check V_C sits well between V_E + 0.3 V and the supply.
4. Set V_B = V_E + 0.65 V with a divider whose Thevenin resistance is small compared with β × R_E.
5. Pick C_IN so its impedance at the lowest frequency of interest is small compared with the amplifier's input resistance (lesson 07).

## Build It

### Step 1: The amplifier

```python
def common_emitter(beta=100.0, collector_ohms=COLLECTOR_OHMS, bypass=None, amplitude=0.0, freq=1000.0):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", SUPPLY)
    circuit.sine_source("VIN", "in", "0", amplitude=amplitude, freq=freq, offset=0.0)
    circuit.capacitor("CIN", "in", "b", 10e-6)
    circuit.resistor("R1", "vcc", "b", TOP_OHMS)
    circuit.resistor("R2", "b", "0", BOTTOM_OHMS)
    circuit.resistor("RC", "vcc", "c", collector_ohms)
    circuit.resistor("RE", "e", "0", EMITTER_OHMS)
    if bypass:
        circuit.capacitor("CE", "e", "0", bypass)
    circuit.npn("Q1", c="c", b="b", e="e", beta=beta)
    return circuit
```

The same circuit object answers three questions: `.dc()` for the operating point, `.ac([1000.0], source="VIN")` for the small-signal gain, `.transient(..., initial="dc")` for waveforms.

### Step 2: AC analysis

```python
ac = common_emitter(amplitude=1.0).ac([1000.0], source="VIN")
gain = abs(ac.v("c")[0])
```

The simulator first finds the DC operating point, then replaces each transistor by its straight-line (linearised) model at that point and solves the circuit with phasors (Phase 09-10). With a 1 V source, the complex voltage at the collector *is* the gain.

### Step 3: Transient

```python
result = common_emitter(amplitude=amplitude).transient(t_stop=5e-3, dt=5e-6, initial="dc")
```

`initial="dc"` starts from the DC operating point (capacitors already charged to their bias voltages). Without it, the 10 µF coupling capacitor would start empty and take about R_TH × C = 91 ms to charge, much longer than our 5 ms window.

```
uv run python phases/12-transistors/06-amplifiers-and-biasing/code/main.py
```

## Use It

- **Discrete preamps**: guitar pedals (fuzz, boost), microphone preamps and vintage radios are full of common-emitter stages exactly like this one, often with a bypassed emitter for gain and a small unbypassed part for stability.
- **Typical parts**: BC547/BC549 (low noise), 2N3904, 2N5089 (high β, used in pedals). Electrolytic capacitors for C_E; film or ceramic for C_IN.
- **Inside op-amps and chips**: the same stage, with a current source instead of R_C (lesson 08), gives gains of thousands per stage.
- **The decibel**: datasheets and audio specs quote gain in dB. Our ×10 stage is 20 dB; ×124 is 41.9 dB. Two ×10 stages in series multiply to ×100, which in dB *adds*: 20 + 20 = 40 dB.
- **Why amplifiers are now mostly op-amps**: a discrete stage needs five resistors, two capacitors and some care for 20 dB of moderately accurate gain. An op-amp (Phase 13) gives precise gain with two resistors.

## Try It in the Lab

The lab is the amplifier of this lesson, already biased (100k/10k divider, 200 Ω emitter resistor, β = 100) with a coupling capacitor at the input. The collector resistor is missing. Pick it so the gain at 1 kHz is between 18 and 22 dB (about ×10).

Think about: r_e at this bias current, the formula R_C / (R_E + r_e), and what 20 dB means as a ratio. After passing, try the other parts. One gives too little gain. What would the other do to the DC collector voltage, and to the headroom for a large signal?

## Common Mistakes

- **Designing with fixed bias.** It works on the bench with one transistor and fails in production.
- **Forgetting the emitter follows the base.** V_E = V_B − 0.65 V: this is the key to quick hand analysis.
- **Ignoring the base current in the divider.** If R_TH is not small compared with β R_E, the base voltage sags (here by 0.13 V).
- **Biasing too close to a rail.** A collector at 11 V cannot swing up more than 1 V.
- **Expecting the bypassed gain to be precise.** R_C / r_e depends on current and temperature; use partial bypass or feedback for predictable gain.
- **Using too small a coupling capacitor.** It forms a high-pass filter with the input resistance; low frequencies are lost (lesson 07 computes this).
- **Forgetting the phase inversion.** A common-emitter stage inverts. Two in cascade don't.

## Exercises

1. With R_E = 470 Ω (unbypassed) and the same divider, recompute I_E and V_C by hand. What is the gain?
2. Design a degenerated stage for a gain of 5 from a 9 V supply with I_C = 1 mA and V_E = 1 V. Find R_E, R_C, and a divider (use R_TH ≈ 10 kΩ).
3. The fixed-bias design uses 750 kΩ. Explain, with the formula I_C = β (V_CC − 0.65)/R_B, why it gives 1.51 mA at β = 100 and 4.52 mA at β = 300.
4. Express gains of ×2, ×31.6, ×1000 and ×0.5 in dB.
5. In the script, raise the input amplitude for the *bypassed* amplifier until the output clips. At what input amplitude does it start, and is it the top or the bottom that clips first?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Operating point | "Q point", "bias" | DC voltages and currents with no signal |
| Fixed bias | "Base-resistor bias" | I_B set by one resistor; I_C proportional to β; unstable |
| Divider bias | "Voltage-divider bias" | Base voltage set by a divider, current set by R_E; stable |
| Emitter degeneration | "Local feedback" | Unbypassed R_E: gain ≈ R_C/(R_E + r_e), stable and linear |
| Bypass capacitor | "C_E" | Shorts R_E for AC: gain ≈ R_C / r_e, large but less predictable |
| r_e | "Intrinsic emitter resistance" | V_T / I_C, about 26 Ω at 1 mA |
| Clipping | "Overdrive", "distortion" | Output flattened when it reaches a rail or saturation |
| dB | "Decibels" | 20 log₁₀(V_out/V_in) for voltage ratios |

## Further Reading

- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., section 2.2.7 (the common-emitter amplifier) and 2.3 (Ebers-Moll and r_e).
- *All About Circuits*, Volume III, chapter 4, "The common-emitter amplifier" and "Biasing techniques". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-4/common-emitter-amplifier/
- MIT OpenCourseWare 6.002, lectures on the MOSFET/BJT amplifier and biasing (incremental analysis). https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/
- ElectroSmash, "Fuzz Face analysis": a detailed real-world walk-through of a two-transistor common-emitter guitar circuit. https://www.electrosmash.com/fuzz-face
