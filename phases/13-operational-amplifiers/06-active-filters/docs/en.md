# Active Filters

> Passive RC filters sag, droop and load each other. Put an op-amp in the loop and you can stack poles without loading, add gain, and choose exactly how sharply the response bends at the cutoff.

**Type:** Build
**Prerequisites:** 13-03 (Inverting and Non-Inverting Amplifiers), 13-05 (Integrators and Differentiators); Phase 10 (Filters and Resonance), lessons 02-rc-low-pass-and-high-pass, 03-decibels-and-bode-plots, 05-rlc-resonance, 07-quality-factor and 08-ac-analysis-in-our-simulator
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Active filter | A filter that uses an op-amp (which needs power) together with R and C | A water filter with a pump, versus one that relies on gravity |
| Passive filter | A filter made only of R, L and C | The gravity filter |
| Order | How many capacitors (energy-storing parts) shape the response; each adds 20 dB/decade of roll-off | The number of sieves in a stack |
| Pole | A frequency at which one RC "corner" starts to cut; a first-order filter has one pole | One sieve's mesh size |
| Roll-off | How fast the gain falls beyond the cutoff, in dB per decade | How steep the slope beyond the cliff edge is |
| Cutoff frequency (f_c) | The frequency where the gain has fallen 3 dB from the pass band | The edge of the cliff |
| Natural frequency (f₀) | The characteristic frequency of a second-order filter, 1/(2π√(R₁R₂C₁C₂)) | The pitch a bell rings at |
| Quality factor (Q) | How "resonant" a second-order filter is: low Q droops early, high Q peaks before cutting (Phase 10) | How long a bell rings after being struck |
| Butterworth | The response with Q = 0.707: as flat as possible in the pass band, no peak | A road that stays perfectly level until the cliff |
| Sallen-Key | A popular second-order active filter using one op-amp as a follower, two resistors and two capacitors | A standard recipe that every cook knows |
| Anti-aliasing filter | A low-pass filter before an analogue-to-digital converter that removes frequencies the converter would misread (Phase 19) | Sunglasses that stop the glare before your eyes |

## Learning Objectives

- Build a first-order active low-pass filter with gain, and compute its cutoff.
- Explain why cascading passive RC sections works poorly, and how a buffer fixes it.
- Design a unity-gain Sallen-Key low-pass filter for a given f₀ and Q, including the Butterworth Q = 0.707.
- See the effect of Q on the response (droop, flat, peak) with AC analysis.
- Turn a low-pass Sallen-Key into a high-pass by swapping R and C.

## The Problem

A sensor signal of interest lives below 200 Hz, but it arrives with 5 kHz interference from a nearby switching power supply. An audio system must separate bass for the woofer from treble for the tweeter. A 10 kHz-sampling ADC must not see anything above 5 kHz (Phase 19 explains why).

Phase 10 filtered with R, L and C. One RC section falls only 20 dB per decade: at 5 kHz, a 1 kHz RC filter still passes 20 % of the interference. Two RC sections in a row should fall 40 dB per decade, but the second one loads the first, and the result droops long before the cutoff. Inductors would help (RLC circuits can be sharp) but at audio frequencies they are large, heavy and pick up hum. Op-amps let us build sharp filters from resistors and capacitors only.

## The Physics

Two ideas from earlier lessons combine.

**Buffering removes loading.** A voltage follower (lesson 01) has infinite input resistance and zero output resistance. Put one between two RC stages and each stage behaves exactly as it would alone.

**Feedback creates resonance without inductors.** A second-order filter's character is set by Q (Phase 10). In an RLC circuit, Q comes from energy sloshing between L and C. In a Sallen-Key filter, the op-amp's output feeds back through a capacitor to the middle of the filter; near f₀ this feedback pushes the signal up, acting like the "spring" an inductor would provide. The amount of feedback, set by the capacitor ratio, sets Q.

What the pump analogy gets wrong: the op-amp does not add energy *to the filtered signal* at all frequencies; at most it adds a fixed gain. What it adds is the *ability to shape* the response without the parts loading each other.

## The Concept

### First order, with gain

Put a capacitor across the feedback resistor of an inverting amplifier:

```
               C_F 15.9 nF
           +-----| |-------+
           |               |
           +----[R_F 10 k]--+
           |               |
 V_in --[R_I 1 k]--+--|- \  |
                      |    >-+---- V_out
           ground ----|+ /
```

At low frequency C_F is an open circuit: gain −R_F/R_I = −10 (20 dB). At high frequency C_F shorts R_F and the gain falls. The corner is where C_F's impedance equals R_F:

```
f_c = 1 / (2π R_F C_F) = 1 / (2π × 10 k × 15.9 nF) = 1001 Hz
```

Simulated: pass band **20.00 dB**, cutoff **1001 Hz**, then 20 dB lower per decade (−0.03 dB at 10 kHz, −19.99 dB at 100 kHz). Gain and filtering in one stage.

### Second order: passive versus Sallen-Key

Aim for 1 kHz with R = 10 kΩ.

**Passive RC-RC** (two sections of 10 kΩ and 15.9 nF, each with a 1 kHz corner alone):

```
 V_in --[R]--+--[R]--+--- V_out
             |       |
            [C]     [C]
             |       |
           ground  ground
```

**Unity-gain Sallen-Key low-pass**:

```
                      C1 (to output)
              +---------| |--------------+
              |                          |
 V_in --[R1]--+--[R2]--+--- p ---|+ \    |
              a        |         |    >--+---- V_out
                      [C2]    +--|- /    |
                       |      |          |
                     ground   +----------+   (op-amp as a follower)
```

For R1 = R2 = R, the standard results are

```
f₀ = 1 / (2π R √(C1 C2))          Q = √(C1 / C2) / 2
```

Read: "the natural frequency is one over two pi R times the square root of the two capacitors multiplied", and "Q is half the square root of the capacitor ratio". For a flat (Butterworth) response, Q = 0.707, so √(C1/C2) = 1.414: **C1 = 2 C2**. Then √(C1 C2) = C2√2, and for f₀ = 1 kHz with R = 10 kΩ: C2 = 1/(2π × 10⁴ × 1000 × √2) = 11.25 nF, C1 = 22.5 nF.

Simulated gains:

| Design | 100 Hz | 500 Hz | 1 kHz | 2 kHz | 10 kHz | Cutoff (−3 dB) |
|---|---|---|---|---|---|---|
| Passive RC-RC, 15.9 nF | −0.29 dB | −4.49 dB | −9.53 dB | −16.52 dB | −40.28 dB | 375 Hz |
| Sallen-Key, Q = 0.707 | 0.00 dB | −0.26 dB | −3.01 dB | −12.30 dB | −39.99 dB | 1000 Hz |
| Sallen-Key, Q = 2.0 | +0.08 dB | +2.04 dB | +6.02 dB | −10.01 dB | −39.93 dB | 1165 Hz |

Read the rows:

- The **passive** filter loses 4.5 dB already at 500 Hz and its −3 dB point is at 375 Hz, far below the intended 1 kHz. Its Q is only about 0.33: the second section draws current from the first and blurs both corners.
- The **Butterworth** Sallen-Key is flat (−0.26 dB at half the cutoff), exactly −3.01 dB at 1 kHz, then falls 40 dB per decade.
- The **Q = 2** design (C1 = 63.7 nF, C2 = 3.98 nF, same f₀) peaks: +6 dB at f₀ (a gain of Q = 2), then falls even more steeply. Its "cutoff" measured 3 dB below the peak is 1165 Hz. High-Q filters are useful when you need a steep edge, or to pick out one frequency, but they ring in the time domain (Phase 10).

All three end up near −40 dB at 10 kHz: far above the corner, every second-order low-pass falls at 40 dB per decade. The differences, which matter, are all near the corner. `code/out.png` shows the three curves.

### Why Q depends on the capacitor ratio

At low frequencies C1 does nothing (open) and the circuit is just two RC sections buffered at the end. Near f₀, the output is in phase with node `a` (the follower copies p, which lags a only a little), and C1 feeds output current *back into* node `a`. That positive push near f₀ partly cancels the loss in R1 and R2, lifting the response: more C1 relative to C2 means more push, more Q. At high frequencies C2 shorts p to ground and the output dies.

### Checking it in time

Feed the Butterworth filter 1 V at 200 Hz plus 1 V at 5 kHz (the "signal" and the "whine"), and run a transient. Measuring each frequency component of the output:

```
output: 0.999 V at 200 Hz, 0.0398 V at 5 kHz  (5 kHz is attenuated -28.0 dB)
```

Predicted from the Bode plot: 5 kHz is log₁₀(5) = 0.70 decades above f₀, so a second-order filter is down about 40 × 0.70 = 28 dB. ✓

### High-pass: swap R and C

Exchange every resistor with a capacitor and vice versa. With C1 = C2 = C:

```
                       R1 (to output)
              +--------/\/\/-----------+
              |                        |
 V_in --| |---+---| |--+--- p ---|+ \  |
         C1   a   C2   |         |   >-+---- V_out
                      [R2]    +--|- /  |
                       |      |        |
                     ground   +--------+
```

f₀ = 1/(2π C √(R1 R2)), Q = √(R2/R1)/2, so for Butterworth **R2 = 2 R1**. With C = 10 nF, R1 = 11.25 kΩ, R2 = 22.5 kΩ: f₀ = 1000 Hz, and the simulator gives −40.0 dB at 100 Hz, −12.3 dB at 500 Hz, −3.01 dB at 1 kHz and 0.00 dB at 10 kHz: the mirror image of the low-pass.

### Higher orders

For 60, 80, 100 dB per decade, cascade sections: a fourth-order Butterworth filter is two Sallen-Key stages with Q = 0.541 and Q = 1.307 (not two Q = 0.707 stages!). Tables of these Q values for Butterworth, Bessel (best pulse shape) and Chebyshev (steepest, with ripple) are in every filter handbook, and tools like TI's Filter Designer compute the parts.

## Build It

### Step 1: First-order active low-pass

```python
def inverting_low_pass():
    circuit = Circuit()
    circuit.sine_source("VIN", "in", "0", amplitude=1.0, freq=1000.0)
    circuit.resistor("RI", "in", "n", 1e3)
    circuit.resistor("RF", "n", "out", 10e3)
    circuit.capacitor("CF", "n", "out", 15.9e-9)
    circuit.opamp("U1", plus="0", minus="n", out="out", gain=1e5)
    return circuit
```

### Step 2: Sallen-Key low-pass

```python
def sallen_key_low_pass(r, c_feedback, c_ground):
    circuit = Circuit()
    circuit.sine_source("VIN", "in", "0", amplitude=1.0, freq=1000.0)
    circuit.resistor("R1", "in", "a", r)
    circuit.resistor("R2", "a", "p", r)
    circuit.capacitor("C1", "a", "out", c_feedback)
    circuit.capacitor("C2", "p", "0", c_ground)
    circuit.opamp("U1", plus="p", minus="out", out="out", gain=1e5)
    return circuit
```

`minus="out", out="out"` makes the follower. `result = circuit.ac(FREQS, source="VIN")` then gives `result.gain_db_at(f, "out")` and `result.cutoff("out")` (the frequency 3 dB below the largest gain).

### Step 3: Compare, check in time, plot

`show_second_order` tabulates the three designs, `show_high_pass` the swapped version, `show_transient_check` extracts the 200 Hz and 5 kHz components of a transient output with a complex-exponential average (as in Phase 12 lesson 07), and `plot` saves the Bode curves.

```
uv run python phases/13-operational-amplifiers/06-active-filters/code/main.py
```

## Use It

- **Anti-aliasing before ADCs**: a second- or fourth-order Sallen-Key low-pass in front of a microcontroller's ADC is standard practice in sensor and audio designs.
- **Audio crossovers and tone controls**: active crossovers split the signal into bass/mid/treble with Linkwitz-Riley filters (two Butterworth stages); equalisers use band-pass sections.
- **Design tools**: TI Filter Designer, Analog Devices' Analog Filter Wizard and the FilterPro tool compute R and C for a chosen response, order and op-amp.
- **Part choice**: use C0G/NP0 ceramic or film capacitors in filters (their value doesn't change with voltage or temperature), 1 % resistors, and an op-amp whose gain-bandwidth is at least 100 × f₀ × Q (lesson 07) so the op-amp itself doesn't distort the response.
- **Switched-capacitor filters** (MAX7400, LTC1069) make filters whose cutoff is set by a clock frequency: easily tunable, used in instruments.

## Try It in the Lab

A Sallen-Key low-pass with two 10 kΩ resistors, a 10 nF capacitor from the + input to ground and the op-amp as a follower. Choose the feedback capacitor so the response is flat to about 1 kHz (no bump), and cuts 10 kHz whine by at least 35 dB.

Think about: f₀ = 1/(2π R √(C1 C2)) and Q = √(C1/C2)/2, the Butterworth condition, and which available capacitor comes closest. After passing, try the others: which one makes a resonant bump, and which one sags too early?

## Common Mistakes

- **Cascading passive RC sections and expecting a sharp corner.** They load each other; buffer between them or use an active topology.
- **Swapping C1 and C2 in a Sallen-Key low-pass.** The feedback capacitor (to the output) must be the larger one for Q = 0.707; swapped, Q drops to 0.35 and the response droops.
- **Cascading two Butterworth second-order sections for a fourth-order Butterworth.** The overall response would droop; each section needs its own tabulated Q.
- **Ignoring the op-amp's bandwidth.** A 1 MHz op-amp in a 50 kHz high-Q filter shifts the response (lesson 07).
- **Using cheap high-k ceramic capacitors** (X7R, Y5V) whose capacitance changes with voltage: the filter's corner moves with the signal and distorts it.
- **Forgetting that "cutoff" means −3 dB.** At the cutoff the signal is already 29 % smaller; put the cutoff comfortably above the band you want to keep.

## Exercises

1. Design a first-order active low-pass with a gain of −5 and a cutoff of 300 Hz, using R_I = 2 kΩ. What R_F and C_F?
2. Design a Butterworth Sallen-Key low-pass at 5 kHz with R = 4.7 kΩ. What C1 and C2?
3. A Sallen-Key low-pass has R = 10 kΩ, C1 = 47 nF, C2 = 10 nF. Compute f₀ and Q. Will it peak?
4. By how many dB does a Butterworth second-order low-pass at 1 kHz attenuate 50 Hz? 20 kHz? (Use the Bode slopes.)
5. Change the script to cascade two Sallen-Key stages with Q = 0.541 and Q = 1.307 (same f₀ = 1 kHz). Check that the result is a flat fourth-order response with −3 dB at 1 kHz and −80 dB/decade.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Active filter | "Op-amp filter" | Filter built from R, C and an op-amp; no inductors, no loading between stages |
| Order | "Poles" | Number of reactive elements; roll-off of 20 dB/decade per order |
| f₀ | "Corner", "natural frequency" | 1/(2π√(R1R2C1C2)) for a Sallen-Key section |
| Q | "Quality factor" | Shape near the corner: 0.5 droops, 0.707 flat (Butterworth), > 0.707 peaks |
| Butterworth | "Maximally flat" | Response with no ripple in the pass band; Q = 0.707 per second-order section |
| Sallen-Key | "Unity-gain VCVS filter" | Second-order section with a follower and positive feedback through a capacitor |
| Roll-off | "Slope" | Rate of attenuation beyond the corner, in dB/decade |

## Further Reading

- R. Mancini (ed.), *Op Amps For Everyone* (Texas Instruments, 2002; Newnes), chapter 16 "Active Filter Design Techniques" (T. Kugelstadt): Sallen-Key and multiple-feedback design tables.
- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., section 6.3 "Active filters" (Sallen-Key, Butterworth, Bessel and Chebyshev responses).
- Analog Devices, *Linear Circuit Design Handbook*, chapter 8 "Analog Filters" (H. Zumbahlen). https://www.analog.com/en/resources/technical-books/linear-circuit-design-handbook.html
- R. P. Sallen and E. L. Key, "A Practical Method of Designing RC Active Filters", *IRE Transactions on Circuit Theory*, 1955: the original paper.
