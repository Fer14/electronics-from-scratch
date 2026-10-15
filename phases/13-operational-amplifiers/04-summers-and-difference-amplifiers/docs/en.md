# Summers and Difference Amplifiers

> The virtual ground is a meeting point where currents add without disturbing each other. Feed several inputs into it and the op-amp adds them. Feed one input to each side, with matched resistors, and it subtracts them.

**Type:** Build
**Prerequisites:** 13-03 (Inverting and Non-Inverting Amplifiers); Phase 04 (Kirchhoff's Laws), lessons 02-kirchhoffs-current-law and 07-the-wheatstone-bridge; Phase 05 (Circuit Analysis and Our Simulator), lesson 05-superposition
**Time:** ~65 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Summing amplifier (summer) | An inverting amplifier with several input resistors; the output is minus the weighted sum of the inputs | A mixing bowl where several ingredients are poured in together |
| Summing node | The − input of a summer, a virtual ground where all input currents meet | A town square where several streets meet |
| Weight | The factor each input is multiplied by, R_F / R_k | How many spoons of each ingredient |
| Mixer | A summer used for audio, combining several signals into one | A mixing desk in a recording studio |
| DAC (digital-to-analogue converter) | A circuit that turns a binary number into a proportional voltage | A set of weights (1, 2, 4, 8 kg) you put on a scale by switches |
| Difference amplifier | An op-amp with four resistors whose output is proportional to V1 − V2 | A balance scale that only shows the difference in weight between two pans |
| Differential signal | The difference between two voltages, the part you want | The difference in height between two people |
| Common-mode voltage | The average of the two voltages, the part they share | The height of the floor both people stand on |
| CMRR (common-mode rejection ratio) | How much better an amplifier amplifies the difference than the common part, usually in dB | How well the scale ignores the fact that it is on a moving train |
| Instrumentation amplifier | A precision difference amplifier with buffered inputs (usually three op-amps) | A balance with its pans on frictionless bearings |
| Strain gauge | A resistor that changes slightly when stretched, used to measure force | A rubber band whose length you can read electrically |

## Learning Objectives

- Derive the output of an inverting summer from KCL at the virtual ground.
- Design weighted summers, including a 4-bit binary-weighted DAC.
- Derive the difference amplifier's output and see why the four resistors must match.
- Quantify common-mode rejection and how resistor mismatch destroys it.
- Read a Wheatstone bridge with a difference amplifier, and know why instrumentation amplifiers exist.

## The Problem

A recording studio mixes ten microphones into one track. A digital music player turns numbers into voltages fifty thousand times a second. A bathroom scale measures a change of a few millivolts sitting on top of a 2.5 V bridge voltage. A current sensor reads the tiny voltage across a shunt resistor in a 12 V supply line.

The first two need *addition* of signals; the last two need *subtraction*: extracting a small difference from two voltages that share a large common part. The inverting amplifier of lesson 03 already contains the key ingredient for both: the virtual ground, a node held at 0 V where currents can meet without interfering with each other.

## The Physics

Two principles from earlier phases do all the work.

**Kirchhoff's current law** (Phase 04) at the summing node: whatever current flows in must flow out. Because the node is held at 0 V by feedback, each input's current depends only on its own voltage and resistor: I_k = V_k / R_k. The inputs don't "see" each other; there is no interaction, as there would be if you simply joined several sources with resistors.

**Superposition** (Phase 05): in a linear circuit, the response to several inputs is the sum of the responses to each one alone. A difference amplifier is analysed by working out the output due to V1 (with V2 grounded) and due to V2 (with V1 grounded), and adding them.

## The Concept

### The inverting summer

```
   V1 ---[R1]---+
                |
   V2 ---[R2]---+------[R_F]------+
                |                 |
   V3 ---[R3]---+---|- \          |
                    |    >--------+---- V_out
          ground ---|+ /
```

KCL at the − node (held at 0 V, no current into the op-amp):

```
V1/R1 + V2/R2 + V3/R3 = −V_out / R_F

V_out = −( (R_F/R1) V1 + (R_F/R2) V2 + (R_F/R3) V3 )
```

Read: "the output is minus the sum of each input times its weight, the weight being R_F over that input's resistor".

**Equal weights (a mixer).** All resistors 10 kΩ: V_out = −(V1 + V2 + V3). With 0.5 V, −0.2 V and 0.3 V: −0.600 V. The simulator: **−0.59998 V**, with the summing node at 6.0 µV (the finite-gain residue, 0.6 V / 10⁵).

**Weighted.** 1 V into 10 kΩ, 20 kΩ and 40 kΩ with R_F = 10 kΩ: weights 1, 0.5, 0.25, so V_out = −1.75 V. Simulated: **−1.7500 V**.

An audio mixer adds a volume control (potentiometer) in front of each input resistor, and often a second inverting stage to undo the minus sign.

### A 4-bit DAC

Choose resistors in the ratio 1 : 2 : 4 : 8 and feed each with a bit that is either 0 V or 5 V. With R_F = 5 kΩ and inputs into 10 k, 20 k, 40 k, 80 k:

```
V_out = −5 V × ( b3 × 5k/10k + b2 × 5k/20k + b1 × 5k/40k + b0 × 5k/80k )
      = −5 V × ( b3/2 + b2/4 + b1/8 + b0/16 )
      = −(5 V / 16) × code
```

Each step of the binary code adds 5/16 = 0.3125 V.

| Code | Bits | Output | Ideal |
|---|---|---|---|
| 0 | 0000 | 0.0000 V | 0.0000 V |
| 1 | 0001 | −0.3125 V | −0.3125 V |
| 2 | 0010 | −0.6250 V | −0.6250 V |
| 5 | 0101 | −1.5625 V | −1.5625 V |
| 8 | 1000 | −2.5000 V | −2.5000 V |
| 15 | 1111 | −4.6874 V | −4.6875 V |

That is a digital-to-analogue converter. Its limitation: the resistors must be accurate to better than one step of the smallest bit. For 4 bits the largest resistor must be right to about 1/16 = 6 %; for 16 bits, a range of 65,536:1 with accuracy far below 0.002 %, which is impossible with plain resistors. Real DACs use an R-2R ladder (only two values) or current steering (Phase 12's mirrors).

### The difference amplifier

```
                 R1                R2
   V2 ---------/\/\/---+---------/\/\/------+
                       |                    |
                       +----|- \            |
                            |    >----------+---- V_out
                       +----|+ /
                 R3    |
   V1 ---------/\/\/---+
                       |
                     [R4]
                       |
                     ground
```

By superposition:

- **V1 alone** (V2 grounded): V1 is divided by R3/R4 to give V+ = V1 × R4/(R3 + R4), and then amplified by the non-inverting gain (1 + R2/R1).
- **V2 alone** (V1 grounded, so V+ = 0): an inverting amplifier with gain −R2/R1.

```
V_out = V1 × (R4 / (R3 + R4)) × (1 + R2/R1)  −  V2 × (R2 / R1)
```

Now make the ratios match: R2/R1 = R4/R3 = G. Then R4/(R3 + R4) = G/(1 + G), and (G/(1 + G)) × (1 + G) = G:

```
V_out = G × (V1 − V2)
```

Read: "with matched ratios, the output is the gain times the difference of the inputs". Four 10 kΩ resistors give G = 1:

| V1 | V2 | Output |
|---|---|---|
| 5.2 V | 5.0 V | 0.20000 V |
| 1.0 V | 0.0 V | 0.99998 V |
| 0.0 V | 1.0 V | −0.99998 V |
| 3.0 V | 3.0 V | 0.00000 V |

The 5 V the two inputs share is ignored; only their 0.2 V difference comes out.

### Common-mode rejection and resistor matching

Write the inputs as a **differential** part V_d = V1 − V2 and a **common-mode** part V_cm = (V1 + V2)/2. An ideal difference amplifier responds only to V_d. A real one leaks a little V_cm into the output; the ratio of the differential gain to the common-mode gain is the **CMRR**, usually quoted in dB.

The leak comes from resistor mismatch. Both inputs at 5 V (pure common mode), with R4 off by a small fraction:

| R4 error | Output (should be 0) | CMRR |
|---|---|---|
| 0 % | 0.000 mV | ideal |
| 0.1 % | 2.499 mV | 66.0 dB |
| 1 % | 24.88 mV | 46.1 dB |
| 5 % | 121.9 mV | 32.5 dB |

With ordinary 1 % resistors, 5 V of common mode produces 25 mV of fake signal. If the "real" signal is the 2.5 mV of a strain gauge, it is buried ten times over. A quick rule for G = 1: common-mode gain ≈ (resistor mismatch) / 2, so a 1 % error gives 0.5 % of V_cm.

### Reading a bridge

A Wheatstone bridge (Phase 04) of 120 Ω strain gauges from 5 V: when one gauge stretches by 0.2 %, one side moves from 2.5000 V to 2.5025 V while the other stays at 2.5000 V. Difference: 2.498 mV, common mode: 2.5 V. A difference amplifier with G = 100 (1 kΩ / 100 kΩ) outputs **0.2495 V**.

Two practical problems remain. First, the 1 kΩ input resistors load the bridge (each bridge output has about 60 Ω of resistance, which adds to R1 and R3 and spoils the matching; in the script the bridge outputs are modelled as ideal sources). Second, at a gain of 100 the 1 % mismatch problem above is still there. The **instrumentation amplifier** solves both: two followers (or non-inverting stages) buffer the inputs so the bridge sees no load, and a precision difference amplifier with laser-trimmed resistors does the subtraction. One chip, one gain resistor, CMRR of 100-120 dB.

```
   three-op-amp instrumentation amplifier (block view)

   V1 --->[ buffer A1 ]---+--->[          ]
                          |    [ diff amp ]
                        [R_G]  [    A3    ]---> G x (V1 - V2)
                          |    [ matched  ]
   V2 --->[ buffer A2 ]---+--->[ resistors]

   R_G, shared by the two input stages, sets the gain G.
   the inputs only see the buffers' + pins: no current, no loading
```

## Build It

### Step 1: A general summer

```python
def inverting_summer(inputs, input_ohms, feedback_ohms):
    circuit = Circuit()
    for k, (volts, ohms) in enumerate(zip(inputs, input_ohms)):
        circuit.voltage_source(f"V{k}", f"in{k}", "0", volts)
        circuit.resistor(f"R{k}", f"in{k}", "sum", ohms)
    circuit.resistor("RF", "sum", "out", feedback_ohms)
    circuit.opamp("U1", plus="0", minus="sum", out="out", gain=1e5, rails=RAILS)
    return circuit.dc()
```

One function builds a mixer, a weighted summer or a DAC depending on the lists it is given.

### Step 2: The DAC

`show_dac` turns each code into four bits with `(code >> (3 - k)) & 1` (bit k of the binary number) and feeds 5 V × bit into the summer.

### Step 3: The difference amplifier and its mismatch

```python
def difference_amplifier(v1, v2, r1=10e3, r2=10e3, r3=10e3, r4=10e3):
    circuit = Circuit()
    circuit.voltage_source("V1", "a", "0", v1)
    circuit.voltage_source("V2", "b", "0", v2)
    circuit.resistor("R1", "b", "n", r1)
    circuit.resistor("R2", "n", "out", r2)
    circuit.resistor("R3", "a", "p", r3)
    circuit.resistor("R4", "p", "0", r4)
    circuit.opamp("U1", plus="p", minus="n", out="out", gain=1e5, rails=RAILS)
    return circuit.dc()
```

`show_mismatch` measures the output with both inputs at 5 V (common-mode gain) and with a 1 mV difference (differential gain) and divides them to get the CMRR.

```
uv run python phases/13-operational-amplifiers/04-summers-and-difference-amplifiers/code/main.py
```

## Use It

- **Audio mixers and summing buses**: the "mix bus" of a mixing desk is a virtual-ground summing node; each channel's fader feeds a resistor into it.
- **Current sensing**: high-side current-sense amplifiers (INA180, INA240) are difference amplifiers built to read millivolts across a shunt resistor while both ends sit at up to 26-80 V of common mode.
- **Instrumentation amplifiers**: INA128/INA333 and AD620/AD8421 for strain gauges, thermocouples, ECG electrodes (where the heart's 1 mV signal rides on volts of mains-induced common mode). CMRR 100-130 dB.
- **Matched resistor networks**: parts such as the LT5400 provide four resistors matched to 0.01 %, exactly for building difference amplifiers.
- **Balanced audio**: professional audio cables carry the signal and its inverse on two wires; the receiver's difference amplifier cancels hum picked up equally on both (common mode).

## Try It in the Lab

Two inputs, 5.2 V and 5.0 V, a difference amplifier with three 10 kΩ resistors in place, and an empty slot for the fourth (from the + input to ground). Get the output to read the 0.2 V difference.

Think about: the general formula for the output, and what condition makes the common 5 V cancel. Then estimate in your head what a 9.1 kΩ part would do to the output, and why a small resistor error matters so much when the inputs share a large common voltage.

## Common Mistakes

- **Joining sources directly with resistors to "add" them.** Without the virtual ground, the inputs load each other and the sum depends on all the resistors.
- **Forgetting the minus sign of the summer.** Add an inverting ×1 stage if you need a positive sum.
- **Mismatched resistors in a difference amp.** 1 % parts give only about 46 dB of CMRR at G = 1.
- **Ignoring source resistance.** In a difference amp, the source's resistance adds to R1 or R3 and unbalances the ratios.
- **Common-mode voltage outside the op-amp's input range.** V+ = V1 × R4/(R3 + R4) must stay within what the op-amp accepts.
- **Thinking a DAC built from resistors can be very precise.** Binary-weighted resistors become impractical beyond about 6-8 bits.

## Exercises

1. A summer has R_F = 20 kΩ and inputs into 10 kΩ, 20 kΩ and 40 kΩ. What is the output for 1 V, −2 V and 4 V?
2. Design a 3-bit DAC with a full-scale output of −7 V for code 7 using 5 V bits, R_F = 10 kΩ. What input resistors?
3. A difference amp has R1 = R3 = 10 kΩ, R2 = R4 = 47 kΩ. V1 = 2.03 V, V2 = 2.00 V. What is the output? What is the common-mode voltage?
4. Using "common-mode gain ≈ mismatch / 2" for G = 1, what resistor matching is needed for 80 dB of CMRR?
5. In the script, add a 60 Ω source resistance in series with each input of the bridge reading (G = 100). How much does the output change, and why?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Summer | "Summing amp", "mixer" | Inverting amp with several inputs: V_out = −Σ (R_F/R_k) V_k |
| Summing node | "Virtual ground" | The − input where the input currents add |
| DAC | "D-to-A" | Converts a binary code to a voltage, e.g. with binary-weighted resistors |
| Difference amp | "Subtractor", "diff amp" | Four-resistor stage: V_out = G (V1 − V2) when R2/R1 = R4/R3 = G |
| Common-mode voltage | "CM" | (V1 + V2)/2, the part shared by both inputs |
| CMRR | "Common-mode rejection" | Differential gain / common-mode gain, in dB |
| Instrumentation amp | "In-amp" | Buffered, precision difference amplifier with very high CMRR |

## Further Reading

- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., sections 4.2.4 (difference amplifier) and 5.14-5.15 (difference and instrumentation amplifiers).
- *All About Circuits*, Volume III, chapter 8, "Averager and summer circuits" and "Building a differential amplifier". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-8/averager-summer-circuits/
- Analog Devices, *A Designer's Guide to Instrumentation Amplifiers*, 3rd ed. (C. Kitchin and L. Counts). https://www.analog.com/media/en/training-seminars/design-handbooks/designers-guide-instrument-amps-complete.pdf
- Texas Instruments INA128 datasheet: three-op-amp topology, CMRR and gain equation. https://www.ti.com/product/INA128
