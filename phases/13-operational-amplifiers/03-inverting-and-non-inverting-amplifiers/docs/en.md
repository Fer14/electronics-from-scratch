# Inverting and Non-Inverting Amplifiers

> Put a divider in the feedback path and the op-amp must make its output that many times bigger to keep its inputs equal. Two resistors, one precise gain.

**Type:** Build
**Prerequisites:** 13-01 (The Ideal Op-Amp); Phase 04 (Kirchhoff's Laws), lessons 02-kirchhoffs-current-law and 05-the-voltage-divider
**Time:** ~65 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Non-inverting amplifier | Signal into the + input; output = input × (1 + R_F/R_G), same polarity | A pantograph that copies a drawing, enlarged |
| Inverting amplifier | Signal into the − input through R_I; output = −input × R_F/R_I | A see-saw: one side down, the other up, by the arm ratio |
| Feedback resistor (R_F) | The resistor from the output to the − input | The rope from the output back to the controller |
| Gain resistor (R_G) | In the non-inverting amp, the resistor from the − input to ground | The anchor of the divider |
| Input resistor (R_I) | In the inverting amp, the resistor from the signal to the − input | The short arm of the see-saw |
| Feedback fraction (B, beta) | The fraction of the output fed back: R_G / (R_F + R_G) | How much of what you see reaches your brain |
| Virtual ground | In the inverting amp, the − input sits at 0 V although it is not connected to ground | A balance point kept level by a hidden hand |
| Input resistance | How much the amplifier loads its source | How heavy the door is to push |
| Loop gain (A × B) | How many times bigger the open-loop gain is than needed; the "spare" gain that makes the result accurate | Your reserve of strength beyond what the job needs |
| Gain error | The difference between the real and the ideal closed-loop gain | How far the copy's size is off |

## Learning Objectives

- Derive the gain of the non-inverting amplifier (1 + R_F/R_G) and of the inverting amplifier (−R_F/R_I) from the golden rules and Kirchhoff's current law.
- Explain the virtual ground and why the inverting amplifier's input resistance is R_I.
- Compute the exact closed-loop gain A/(1 + AB) and the gain error for a finite A.
- Recognise when the output saturates and the golden rules stop applying.
- Choose between the two configurations for a given source.

## The Problem

A thermocouple gives 41 µV per °C. An electret microphone gives 10 mV. A strain gauge bridge gives 2 mV. An analogue-to-digital converter (Phase 17) on a 3.3 V microcontroller wants signals of about 0-3 V. Every sensor needs a precise, predictable gain between it and the converter: not "about 100", but 100.0, ±1 %.

Phase 12 showed how hard that is with discrete transistors. With an op-amp it takes two resistors, and the gain is set by their ratio alone: buy 0.1 % resistors and you get a 0.1 % gain. This lesson derives the two basic configurations from the golden rules, then checks how "golden" the rules really are when the open-loop gain is finite.

## The Physics

Negative feedback is the whole story. The op-amp, with its huge gain, keeps adjusting its output until V+ = V− (golden rule 2). If the feedback path makes V− a *fraction* of the output, then to bring V− up to V+, the output must be the inverse of that fraction times V+. The resistors set the fraction; the op-amp provides whatever output voltage (within its rails) and current (within its limits) that requires.

What the "hidden hand" picture gets wrong: there is no mechanism separately watching the inputs. The op-amp's output simply responds to V+ − V− with gain A; with feedback, that response changes V−, and the loop settles where both conditions hold at once. The settling takes microseconds (lesson 07).

## The Concept

### The non-inverting amplifier

```
   V_in ------------|+ \
                    |    >----+------ V_out
              +-----|- /      |
              |               |
              +----[R_F]------+
              |
            [R_G]
              |
            ground
```

The output feeds a divider R_F / R_G, whose midpoint is the − input:

```
V− = V_out × R_G / (R_F + R_G)
```

Golden rule 2: V− = V+ = V_in. So V_in = V_out × R_G / (R_F + R_G), and

```
V_out / V_in = (R_F + R_G) / R_G = 1 + R_F / R_G
```

Read: "the gain is one plus the feedback resistor over the gain resistor". For R_F = 9 kΩ and R_G = 1 kΩ: 1 + 9 = **10**. The simulator, 0.3 V in: 2.99969 V out, V− = 0.299969 V (equal to V+ to within 31 µV), input current 0.0003 nA (rule 1).

The gain is always at least 1. With R_F = 0 (a wire) or R_G = ∞ (absent) it is exactly the follower of lesson 01. The input goes straight into the + pin, so the **input resistance is essentially infinite**: perfect for high-resistance sources.

### The inverting amplifier

```
                  R_I            R_F
   V_in ---------/\/\/---+------/\/\/------+
                         |                 |
                         +---|- \          |
                             |    >--------+---- V_out
                  ground ----|+ /
```

The + input is grounded, so golden rule 2 says V− = 0 V too. The − input is not connected to ground, but the feedback holds it at 0 V: a **virtual ground**.

Now Kirchhoff's current law at the − node. The current arriving through R_I is (V_in − 0)/R_I. No current enters the op-amp (rule 1). So all of it must leave through R_F: (0 − V_out)/R_F. Setting them equal:

```
V_in / R_I = −V_out / R_F     →     V_out / V_in = −R_F / R_I
```

Read: "the gain is minus the feedback resistor over the input resistor". For R_F = 100 kΩ, R_I = 10 kΩ: **−10**.

| R_F | R_I | Ideal gain | 0.5 V in → out | V− | Source current |
|---|---|---|---|---|---|
| 10 kΩ | 10 kΩ | −1.000 | −0.49999 V | 5.0 µV | 50.000 µA |
| 100 kΩ | 10 kΩ | −10.000 | −4.99941 V | 53.2 µV | 49.995 µA |
| 22 kΩ | 4.7 kΩ | −4.681 | −2.34029 V | 23.7 µV | 106.38 µA |

The source current is V_in / R_I whatever the gain (0.5 V / 10 kΩ = 50 µA): the source "sees" just R_I to ground. **The inverting amplifier's input resistance is R_I**, a real limitation for weak sources. The inverting configuration can have gains below 1 (an attenuator: R_F < R_I), and its virtual ground is the key to the summers of lesson 04.

### How precise? The finite-gain correction

The golden rules assume A = ∞. With a finite A, the non-inverting amplifier's exact gain follows from V_out = A (V_in − B V_out), where B = R_G / (R_F + R_G) is the **feedback fraction**:

```
V_out / V_in = A / (1 + A × B)
```

Read: "the closed-loop gain equals A over one plus A times B". When A × B (the **loop gain**) is huge, this tends to 1/B = 1 + R_F/R_G. For our gain-10 design, B = 0.1:

| A | Simulated gain | A / (1 + AB) | Error vs ideal 10 |
|---|---|---|---|
| 100 | 9.09091 | 9.09091 | 9.09 % |
| 1,000 | 9.90099 | 9.90099 | 0.99 % |
| 10,000 | 9.99001 | 9.99001 | 0.10 % |
| 100,000 | 9.99900 | 9.99900 | 0.010 % |
| 1,000,000 | 9.99990 | 9.99990 | 0.001 % |

The error is about 1/(A B): **the spare gain buys accuracy**. With A = 10⁵ and a closed-loop gain of 10, the loop gain is 10⁴ and the error 0.01 %, far below resistor tolerances. Ask for a gain of 1000 and the loop gain drops to 100, the error rises to 1 %. Lesson 07 shows that A also falls with frequency, so this error grows at high frequencies.

### The rails still rule

Gain 10 with ±12 V supplies:

| Input | Output | Ideal |
|---|---|---|
| 0.50 V | 4.9995 V | 5.00 V |
| 1.00 V | 9.9986 V | 10.00 V |
| 1.10 V | 10.9981 V | 11.00 V |
| 1.50 V | 12.0000 V | 15.00 V |
| −1.50 V | −12.0000 V | −15.00 V |

At 1.5 V in, the output would need 15 V; it saturates at 12 V. Then V− = 12 × 0.1 = 1.2 V ≠ V+ = 1.5 V: the loop is broken, and golden rule 2 no longer holds. **Always check that the output stays within the rails before trusting the golden rules.**

### Choosing between them: source resistance

A sensor producing 1 V with 100 kΩ of internal resistance:

- Into the non-inverting ×10: output **9.9986 V**. The input draws no current, so the 100 kΩ drops nothing.
- Into an inverting ×(−10) with R_I = 10 kΩ: output **−0.9091 V**, not −10 V. The sensor's 100 kΩ adds to R_I: gain = −100 k / (100 k + 10 k) = −0.909.

| | Non-inverting | Inverting |
|---|---|---|
| Gain | 1 + R_F/R_G (≥ 1) | −R_F/R_I (any size, inverted) |
| Input resistance | ~infinite | R_I |
| − input voltage | follows the input | 0 V (virtual ground) |
| Good for | high-resistance sources, precision gain | summing, attenuating, inverting, when the input may exceed the supply range |

## Build It

### Step 1: The two amplifiers

```python
def non_inverting(input_volts, feedback_ohms, ground_ohms, gain=1e5, rails=RAILS):
    circuit = Circuit()
    circuit.voltage_source("VIN", "in", "0", input_volts)
    circuit.opamp("U1", plus="in", minus="n", out="out", gain=gain, rails=rails)
    circuit.resistor("RF", "out", "n", feedback_ohms)
    circuit.resistor("RG", "n", "0", ground_ohms)
    return circuit.dc()


def inverting(input_volts, feedback_ohms, input_ohms, gain=1e5, rails=RAILS):
    circuit = Circuit()
    circuit.voltage_source("VIN", "in", "0", input_volts)
    circuit.resistor("RI", "in", "n", input_ohms)
    circuit.resistor("RF", "n", "out", feedback_ohms)
    circuit.opamp("U1", plus="0", minus="n", out="out", gain=gain, rails=rails)
    return circuit.dc()
```

### Step 2: Finite gain

`show_finite_gain` runs the gain-10 amplifier with A from 100 to 10⁶ and `rails=None` (a purely linear op-amp), so the results match A/(1 + AB) exactly.

### Step 3: Saturation and loading

`show_saturation` drives the ×10 amplifier past its rails; `show_loading` puts a 100 kΩ source resistance in front of each configuration.

```
uv run python phases/13-operational-amplifiers/03-inverting-and-non-inverting-amplifiers/code/main.py
```

## Use It

- **Microphone preamps**: a non-inverting stage with gain 20-100 (R_F = 47-100 kΩ, R_G = 1-2.2 kΩ, with a capacitor in series with R_G so the DC gain is 1 while audio gets the full gain).
- **Sensor conditioning for ADCs**: a 0-100 mV shunt-resistor signal (current sensing) amplified ×30 for a 3.3 V ADC.
- **Choosing resistor values**: keep them between about 1 kΩ and 1 MΩ. Too small and the op-amp must drive the feedback network as a load; too large and input bias currents (lesson 07) and noise create errors.
- **Single-supply systems**: with one 5 V or 3.3 V supply, signals are often referenced to mid-supply (2.5 V) instead of ground, and a rail-to-rail op-amp (MCP6002, OPA344) is used.
- **Programmable gain**: switching different R_F values with analogue switches gives a programmable-gain amplifier (PGA), common in data-acquisition systems and oscilloscopes.

## Try It in the Lab

A 0.3 V sensor, an op-amp on ±12 V with its + input on the sensor, and a 1 kΩ resistor from its − input to ground. Choose the feedback resistor so the output is about 3 V. A second goal checks that the feedback is really working: the two inputs must stay within 1 mV of each other.

Think about: the formula 1 + R_F/R_G, which part gives a gain closest to 10, and what happens to "V+ = V−" when the gain is so large that the output hits the 12 V rail.

## Common Mistakes

- **Mixing up the formulas.** Non-inverting: 1 + R_F/R_G. Inverting: −R_F/R_I. The "1 +" is not optional.
- **Expecting a non-inverting gain below 1.** It can't be done with this circuit; use a divider before it, or an inverting stage.
- **Ignoring the inverting amp's input resistance.** The source's own resistance adds to R_I and changes the gain.
- **Feedback to the wrong input.** R_F from the output to the + input makes positive feedback: a Schmitt trigger (lesson 02), not an amplifier.
- **Forgetting saturation.** Check the largest input times the gain against the rails.
- **Using huge gains in one stage.** A gain of 1000 eats the loop gain (and, lesson 07, the bandwidth); two stages of ×31.6 do better.

## Exercises

1. Design a non-inverting amplifier with a gain of 23 using E12 resistors (R_G = 1 kΩ). What is the actual gain?
2. An inverting amplifier with R_I = 4.7 kΩ and R_F = 47 kΩ is fed 0.25 V. What is the output? What current flows from the source? In which direction does current flow through R_F?
3. With A = 20,000, what is the exact gain of a non-inverting ×100 stage? What is the error in percent?
4. A 2 V sensor with 10 kΩ internal resistance drives an inverting amplifier with R_I = 10 kΩ and R_F = 20 kΩ. What is the output? What would the ideal (zero source resistance) output be?
5. In the script, use the inverting amplifier with R_F = 10 kΩ and R_I = 40 kΩ. What gain do you get? Is that a useful circuit?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Non-inverting amp | "Non-inv" | Signal at +, divider in feedback: gain 1 + R_F/R_G, very high input resistance |
| Inverting amp | "Inverter" (analogue) | Signal through R_I to −, + grounded: gain −R_F/R_I, input resistance R_I |
| Virtual ground | "Summing node" | The − input of an inverting stage held at 0 V by feedback |
| Feedback fraction B | "β" (feedback factor) | Fraction of the output returned to the − input |
| Loop gain | "A β" | A × B; large loop gain means an accurate closed-loop gain |
| Closed-loop gain | "Gain" | A/(1 + AB) ≈ 1/B |
| Gain error | "Finite-gain error" | ≈ 1/(AB) relative error |

## Further Reading

- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., sections 4.2.1-4.2.4 (inverting and non-inverting amplifiers) and 4.4 (a detailed look at op-amp behavior, including finite gain).
- R. Mancini (ed.), *Op Amps For Everyone* (Texas Instruments, 2002; Newnes), chapter "Development of the Non Ideal Op Amp Equations".
- *All About Circuits*, Volume III, chapter 8, "Divided feedback" and "An analogy for divided feedback". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-8/divided-feedback/
- Analog Devices, MT-032 tutorial "Ideal Voltage Feedback (VFB) Op Amp". https://www.analog.com/media/en/training-seminars/tutorials/MT-032.pdf
