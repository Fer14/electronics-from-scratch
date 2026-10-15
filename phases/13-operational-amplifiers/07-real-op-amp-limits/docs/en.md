# Real Op-Amp Limits

> The golden rules are approximations. Real op-amps have a gain that falls with frequency, an output that can only move so fast and so far, and inputs that are a millivolt off and leak nanoamps. Knowing the numbers tells you when the rules still hold.

**Type:** Build
**Prerequisites:** 13-03 (Inverting and Non-Inverting Amplifiers), 13-05 (Integrators and Differentiators), 13-06 (Active Filters); Phase 12 (Transistors), lessons 06-amplifiers-and-biasing and 07-small-signal-thinking; Phase 10 (Filters and Resonance), lesson 03-decibels-and-bode-plots
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Macro-model | A simplified circuit that behaves like a real op-amp from the outside | A flight simulator: not a plane, but it flies like one |
| Dominant pole | A deliberate low-frequency corner inside the op-amp that makes its gain fall at 20 dB/decade | A governor on an engine that limits how fast it can respond |
| GBW (gain-bandwidth product) | Open-loop gain × frequency, constant above the dominant pole; also the frequency where the open-loop gain is 1 | A fixed budget you can spend on gain or on bandwidth |
| Unity-gain frequency (f_T) | The frequency at which the open-loop gain has fallen to 1 (equal to GBW for these op-amps) | The speed at which the governor allows no amplification at all |
| Closed-loop bandwidth | The −3 dB frequency of an amplifier with feedback, about GBW / gain | How far up the scale a singer can keep full volume |
| Slew rate (SR) | The maximum rate of change of the output voltage, in V/µs | A lift's top speed: it can't climb faster, however urgently called |
| Full-power bandwidth | The highest frequency at which a full-size sine can come out without slew distortion: SR / (2π V_peak) | The fastest you can wave a heavy flag fully from side to side |
| Input offset voltage (V_OS) | A small DC error between the inputs, as if a tiny battery were in series with one input | A scale that reads 2 g with nothing on it |
| Input bias current (I_B) | The small DC current that flows into each input | A tap that drips slightly even when closed |
| Output swing | How close the output can get to each rail | How close to the wall you can park |
| Rail-to-rail | An op-amp whose output (and/or input) range reaches within millivolts of the rails | A car that can park bumper-to-wall |
| Compensation capacitor | The internal capacitor that sets the dominant pole and keeps the op-amp stable | The governor's flywheel |

## Learning Objectives

- Build an op-amp macro-model with finite DC gain, a dominant pole and slew-rate limiting from simulator parts.
- Explain the gain-bandwidth trade-off and compute closed-loop bandwidth as GBW / gain.
- Distinguish slew-rate limiting from bandwidth limiting, and compute the full-power bandwidth.
- Quantify the output error from input offset voltage and from input bias currents, and compensate the latter.
- Choose an op-amp for a job from its datasheet numbers.

## The Problem

Lesson 03's amplifier had a gain of 10 "to the accuracy of its resistors". Build it with an LM358 and feed it a 50 kHz signal: the output is smaller than expected and shifted in time. Feed it a big 30 kHz sine: the output turns into a triangle. Ground its input with a gain of 1000: the output sits at volts instead of zero. Connect a 1 MΩ sensor: another unexpected offset.

None of these are faults. They are the op-amp's real limits, printed in every datasheet. This lesson builds each limit into a simulator model, measures it, and gives the rules of thumb that tell you in advance whether an op-amp is good enough.

## The Physics

### Why the gain falls with frequency

Inside an op-amp (Phase 12): a differential input stage, a high-gain second stage and an output buffer. The second stage has a deliberately added capacitor (the **compensation** capacitor, tens of picofarads on the chip), connected around it. Together with the stage's high resistance it makes one RC corner at a very low frequency: a few hertz to tens of hertz. Above that **dominant pole**, the gain falls at 20 dB per decade, exactly like the integrator of lesson 05.

Why make an amplifier slower on purpose? Because every stage has some phase lag at high frequencies, and an amplifier with too much gain and too much lag inside a negative-feedback loop turns its feedback into positive feedback and oscillates. Rolling off the gain early, with one dominant pole, keeps every feedback configuration down to a gain of 1 stable. This is called **unity-gain compensation**.

### Why the output can only move so fast

The compensation capacitor is charged by the input stage's current. That stage is fed by a fixed current source (Phase 12 lesson 08): when the input difference is large, all of that current is steered one way, and it cannot get bigger. A fixed current into a capacitor gives a fixed rate of voltage change, I/C (lesson 05). That maximum rate, at the output, is the **slew rate**.

### Why the inputs are not perfect

The input transistors are a matched pair, but not perfectly: a few millivolts of V_BE (or V_GS) mismatch is the **offset voltage**. BJT inputs need base current (I_C/β); that is the **bias current**, tens of nanoamps for a 741 or LM358. JFET and CMOS inputs draw only picoamps.

## The Concept

### A macro-model you can see

Our simulator's `opamp` element is ideal-ish: a gain of 10⁵ at every frequency. We build a more realistic one from simulator parts:

```
   V+ --->[ input stage      ]  x  [ transconductor  ]  y  [ output   ]
          [ gain 12.57,      ]---->[ 500 µA/V pushes  ]--+->[ follower ]---> out
   V- --->[ limited to ±1 V  ]     [ current into y   ]  |  [ w/ rails ]
                                                        |
                                            node y: 15.92 MΩ and 1 nF to ground
```

- **Input stage**: an op-amp element with gain 12.57 whose output is squeezed to ±1 V (it saturates for input differences beyond about 80 mV). It plays the differential pair with its fixed tail current.
- **Integrating stage**: a transconductor (VCCS) of 500 µA/V pushes current into node y, loaded by 1 nF in parallel with 15.92 MΩ. This is the compensated second stage.
- **Output buffer**: a follower with rails.

The numbers follow from three choices: DC gain 10⁵, GBW 1 MHz, slew rate 0.5 V/µs (close to an LM358):

```
DC gain        = 12.57 × 500e-6 × 15.92e6 = 100,000   (100 dB)
dominant pole  = 1 / (2π × 15.92 MΩ × 1 nF) = 10.0 Hz
GBW            = DC gain × pole = 100,000 × 10 Hz = 1 MHz
slew rate      = g_m × (max V_x) / C = 500 µA × 1 V / 1 nF = 0.5 V/µs
```

### Open-loop gain versus frequency

| Frequency | Gain |
|---|---|
| 1 Hz | 100.0 dB (×99,501) |
| 10 Hz | 97.0 dB (×70,709) |
| 100 Hz | 80.0 dB (×9,950) |
| 1 kHz | 60.0 dB (×1,000) |
| 10 kHz | 40.0 dB (×100) |
| 100 kHz | 20.0 dB (×10) |
| 1 MHz | 0.0 dB (×1) |

Down 3 dB at the 10 Hz pole, then exactly −20 dB per decade. Above the pole, **gain × frequency is constant**: 1000 × 1 kHz = 100 × 10 kHz = 10 × 100 kHz = 1 MHz. That constant is the **gain-bandwidth product**.

### Closed-loop bandwidth = GBW / gain

With feedback, lesson 03's formula A/(1 + AB) still holds, but now A depends on frequency. At low frequencies A B ≫ 1 and the gain is 1/B. As frequency rises, A falls until A × B = 1, i.e. until A has fallen to the closed-loop gain itself. Beyond that the feedback has no spare gain to work with, and the closed-loop response follows the open-loop curve down. The corner is where the open-loop curve meets the closed-loop gain:

```
f_closed-loop ≈ GBW / (closed-loop gain)
```

Read: "the bandwidth is the gain-bandwidth product divided by the gain you asked for" (strictly, by the "noise gain" 1/B, which equals the non-inverting gain).

| Gain | Low-frequency gain | Bandwidth (simulated) | GBW / gain |
|---|---|---|---|
| 1 | 0.00 dB | 1000 kHz | 1000 kHz |
| 10 | 20.00 dB | 100.0 kHz | 100 kHz |
| 100 | 39.99 dB | 10.0 kHz | 10 kHz |
| 1000 | 59.87 dB | 1.0 kHz | 1 kHz |

A gain-of-100 stage with an LM358-class op-amp is only good to 10 kHz: not even the full audio band (20 kHz). Two stages of ×10 give ×100 with 100 kHz each (about 64 kHz together). This is the "GBW budget": **gain and bandwidth trade one for the other**.

Notice also the gain-of-1000 row: 59.87 dB instead of 60.00 dB, measured at 100 Hz. There the open-loop gain has already fallen to about 10,000, so the loop gain A × B is only about 10, and the closed-loop gain comes out 1.5 % low (985 instead of 1000): the A/(1 + AB) error of lesson 03. Accuracy, too, is spent from the same budget.

### Slew rate: a different, nonlinear limit

Ask the follower to jump from 0 to 5 V. A bandwidth limit alone would give an exponential rise with τ = 1/(2π × 1 MHz) = 0.16 µs. Instead:

```
output goes from 0.5 V to 4.5 V in 8.00 us -> 0.500 V/us
```

A straight ramp at the slew rate, 25 times slower than the bandwidth would suggest. The input stage is saturated (its ±1 V limit), the integrating capacitor is charged by the maximum current, and the output ramps at 0.5 V/µs until it catches up.

For sines, the steepest slope of V_p sin(2π f t) is 2π f V_p (at the zero crossings). The output can only follow if that is below the slew rate:

```
f_max = SR / (2π V_p)        (the full-power bandwidth)
```

For a 5 V-peak sine: 0.5 × 10⁶ / (2π × 5) = **15.9 kHz**. The simulator, follower, 5 V-peak input:

| Frequency | Output peak |
|---|---|
| 5 kHz | 5.00 V |
| 15 kHz | 5.00 V |
| 50 kHz | 2.49 V |

At 50 kHz the output becomes a triangle that can only climb 0.5 V/µs × 10 µs (half a period) = 5 V peak-to-peak: 2.5 V peak. A follower has 1 MHz of small-signal bandwidth, yet it cannot reproduce a large 50 kHz sine. **Small signals are limited by GBW, large signals by slew rate**; check both.

### Input offset voltage

Put a 2 mV source in series with the + input (that is exactly how datasheets model V_OS) and ground the input:

| Gain | Output with no signal |
|---|---|
| 1 | 2.00 mV |
| 10 | 20.00 mV |
| 100 | 199.8 mV |
| 1000 | 1980 mV |

The offset is amplified by the non-inverting gain (the noise gain, 1/B), whatever the configuration. With a gain of 1000, the "zero" output is 2 V. Fixes: a precision op-amp (OP07: 75 µV max; chopper/zero-drift parts such as the OPA387: a few µV), offset-trim pins, AC coupling where DC is not needed, or software calibration.

### Input bias current

Model 100 nA flowing into each input with two current sources. A sensor with 100 kΩ of resistance feeds a follower:

```
no compensation                 : output -10.000 mV
100 k in the feedback path too  : output   0.000 mV
```

The + input's 100 nA flows through the sensor's 100 kΩ: a 10 mV drop that the follower faithfully copies. Put an equal resistance in the feedback path (from output to − input) and the − input's bias current drops the same 10 mV there: the two errors cancel. Rule: **make the DC resistances seen by the two inputs equal**. What remains is the *difference* between the two bias currents (the "input offset current", typically 10 % of I_B). Or choose a CMOS/JFET op-amp with picoamp bias currents.

### Output swing

An older op-amp such as the LM358 on a single 5 V supply can pull its output close to 0 V but only to about 1.5 V below its positive supply, i.e. 3.5 V. A modern **rail-to-rail output** part gets within tens of millivolts of both rails:

| Input (follower) | Limited swing (0-3.5 V) | Rail-to-rail (0-5 V) |
|---|---|---|
| 1.0 V | 1.000 V | 1.000 V |
| 3.0 V | 3.000 V | 3.000 V |
| 4.0 V | 3.500 V | 4.000 V |
| 4.9 V | 3.500 V | 4.900 V |

Similarly, inputs have a **common-mode range**: many op-amps cannot accept input voltages near the positive rail. On 3.3 V systems, always choose rail-to-rail input and output (RRIO) parts.

### Other limits worth knowing

- **Output current**: typically 10-40 mA, with short-circuit protection. Heavy loads need a buffer transistor.
- **Noise**: specified in nV/√Hz; matters for microphones and sensors (Phase 19).
- **CMRR and PSRR**: how well the op-amp rejects common-mode input and supply variations (80-120 dB typical).
- **Stability with capacitive loads**: driving long cables or large capacitors adds phase lag and can cause ringing or oscillation; a small series resistor at the output helps.

## Build It

### Step 1: The macro-model

```python
def real_opamp(circuit, name, plus, minus, out, rails=(-12.0, 12.0), offset=0.0):
    inner = f"{name}_pi"
    circuit.voltage_source(f"{name}_VOS", inner, plus, offset)
    circuit.opamp(f"{name}_IN", plus=inner, minus=minus, out=f"{name}_x", gain=INPUT_GAIN, rails=(-1.0, 1.0))
    circuit.vccs(f"{name}_GM", "0", f"{name}_y", f"{name}_x", "0", STAGE_GM)
    circuit.resistor(f"{name}_R", f"{name}_y", "0", STAGE_RESISTOR)
    circuit.capacitor(f"{name}_C", f"{name}_y", "0", STAGE_CAPACITOR)
    circuit.opamp(f"{name}_OUT", plus=f"{name}_y", minus=out, out=out, gain=1e5, rails=rails)
```

The function adds the parts to an existing circuit, so it can be used like a component. The offset source sits between the outside + pin and the inner one. `vccs("..._GM", "0", y, x, "0", gm)` drives a current g_m × V_x from ground into node y.

### Step 2: Frequency responses

`open_loop_response` drives the + input with the − input grounded; `show_bandwidth` closes the loop with gains of 1 to 1000 and uses `result.cutoff("out")`.

### Step 3: Slew rate

```python
circuit.pulse_source("VIN", "in", "0", low=0.0, high=5.0, period=40e-6, duty=0.5)
real_opamp(circuit, "U1", "in", "out", "out")
result = circuit.transient(t_stop=20e-6, dt=10e-9)
```

The script finds the times the output passes 0.5 V and 4.5 V and divides 4 V by the difference. Then it runs 5 V-peak sines at three frequencies.

### Step 4: Offset, bias current, swing

`show_offset` sets `offset=2e-3`; `show_bias_current` adds two 100 nA current sources at the inputs of the simple op-amp model; `show_swing` compares rails of (0, 3.5) and (0, 5).

```
uv run python phases/13-operational-amplifiers/07-real-op-amp-limits/code/main.py
```

## Use It

Typical datasheet numbers (check the current datasheet for your exact part and grade):

| Part | GBW | Slew rate | V_OS (typ / max) | I_B | Output |
|---|---|---|---|---|---|
| LM358 | ~1 MHz | ~0.3-0.5 V/µs | 2 / 7 mV | 20-45 nA | to ~1.5 V below V+ |
| μA741 | ~1 MHz | 0.5 V/µs | 1 / 5 mV | 80 nA | ~1-2 V from each rail |
| TL072 | 3 MHz | 13 V/µs | 3 / 10 mV | 30 pA (JFET) | ~1.5 V from rails |
| MCP6002 | 1 MHz | 0.6 V/µs | ±4.5 mV max | 1 pA (CMOS) | rail-to-rail |
| OPA2134 (audio) | 8 MHz | 20 V/µs | ±0.5 mV | 5 pA | ~1 V from rails |
| OP07 (precision) | 0.6 MHz | 0.3 V/µs | 30 / 75 µV | 1-4 nA | ~1-2 V from rails |

Choosing a part, in order:

1. **Supply and swing**: single 3.3/5 V supply → rail-to-rail input/output.
2. **GBW**: at least (closed-loop gain) × (highest signal frequency) × 10 for accurate gain; for filters, 100 × f₀ × Q.
3. **Slew rate**: at least 2π f_max V_peak, with margin.
4. **DC precision**: offset × gain must be small compared with your signal; bias current × source resistance likewise.
5. Then noise, output current, power consumption and price.

## Try It in the Lab

The lab's op-amp is drawn as its insides: the same macro-model as this lesson, with a 1 MHz gain-bandwidth product. Build a non-inverting amplifier (R_G = 1 kΩ) for an ultrasonic sensor that needs at least 25 dB of gain *and* at least 30 kHz of bandwidth. Choose R_F.

Think about: what gain 25 dB is as a ratio, what bandwidth each candidate gain leaves you (GBW / gain), and therefore what range of gains satisfies both goals. One wrong part fails on gain, the other on bandwidth.

## Common Mistakes

- **Assuming the open-loop gain is 10⁵ at all frequencies.** At 10 kHz it may be only 100.
- **Confusing bandwidth and slew rate.** A large signal can be slew-limited far below the small-signal bandwidth.
- **Asking one stage for gain × bandwidth beyond its GBW.** Split the gain over two stages.
- **Ignoring offset at high gain.** A 2 mV offset at a gain of 1000 is 2 V of error.
- **Unequal resistances at the two inputs with a bipolar op-amp.** Bias currents create offset; balance them or use a FET-input part.
- **Expecting rail-to-rail behaviour from an old part.** An LM358 on 5 V cannot output 4.5 V.
- **Driving big capacitive loads directly.** The op-amp may ring or oscillate; isolate with a series resistor.

## Exercises

1. An op-amp has GBW = 3 MHz. What is the bandwidth of a non-inverting amplifier with gain 30? Of an inverting amplifier with gain −30? (Hint: the inverting one's noise gain is 1 + R_F/R_I = 31.)
2. You need a 10 V-peak sine at 20 kHz. What minimum slew rate is required? Which op-amps from the table qualify?
3. A gain-of-200 amplifier uses an op-amp with V_OS = 3 mV max. What is the worst-case output error? What V_OS would keep it below 50 mV?
4. A bipolar op-amp with I_B = 50 nA has a 470 kΩ resistor at its + input and a follower connection. What output error results? What should you add to cancel it?
5. In the script, set `SLEW_RATE = 5e6` (5 V/µs) and rerun. What happens to `INPUT_GAIN` and the input stage's saturation level? Recompute the full-power bandwidth for 5 V peak and check it with the sine runs.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| GBW | "Gain-bandwidth" | Open-loop gain × frequency above the dominant pole; closed-loop bandwidth ≈ GBW / noise gain |
| Dominant pole | "Compensation" | Deliberate low-frequency corner that makes the gain fall at 20 dB/decade, keeping the op-amp stable |
| Slew rate | "SR" | Maximum dV/dt of the output, set by the input stage's current charging the compensation capacitor |
| Full-power bandwidth | "FPBW" | SR / (2π V_peak): highest frequency for a full-amplitude sine |
| V_OS | "Offset" | DC input error voltage; appears at the output multiplied by the noise gain |
| I_B | "Bias current" | DC current into the inputs; creates errors through source and feedback resistances |
| Rail-to-rail | "RRIO" | Input and/or output range extending to within millivolts of the supplies |
| Macro-model | "SPICE model" | Simplified circuit reproducing an op-amp's terminal behaviour |

## Further Reading

- R. Mancini (ed.), *Op Amps For Everyone* (Texas Instruments, 2002; Newnes), chapters "Voltage-Feedback Op Amp Compensation" and "Understanding Op Amp Parameters".
- Analog Devices tutorials MT-033 "Voltage Feedback Op Amp Gain and Bandwidth", MT-037 "Op Amp Input Offset Voltage" and MT-038 "Op Amp Input Bias Current". https://www.analog.com/media/en/training-seminars/tutorials/MT-033.pdf
- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., section 4.4 "A detailed look at op-amp behavior" and chapter 5 "Precision Circuits".
- Texas Instruments LM358 datasheet: gain-bandwidth, slew rate, output swing on single supply. https://www.ti.com/product/LM358
