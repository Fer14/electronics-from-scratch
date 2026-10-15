# Dependent Sources

> A dependent source is a source with a remote control: its output is set by a voltage somewhere else in the circuit. It is how we model every transistor and every amplifier.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 05 Lesson 04 (Modified Nodal Analysis from Scratch), Lesson 05 (Superposition) and Lesson 06 (Thevenin and Norton)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Independent source | A source whose value is fixed by itself: a battery, a current source, a signal generator | A tap you set by hand |
| Dependent (controlled) source | A source whose value is set by a voltage or current elsewhere in the circuit | A tap whose opening is controlled by a sensor in another room |
| Controlling quantity | The voltage or current that sets a dependent source's value | The sensor reading |
| VCVS | Voltage-controlled voltage source: output voltage = gain × a controlling voltage | A loudspeaker volume that follows a knob somewhere else |
| VCCS | Voltage-controlled current source: output current = gm × a controlling voltage | A pump whose flow follows a pressure gauge |
| CCVS, CCCS | Current-controlled voltage source and current-controlled current source | The same, with a flow meter as the sensor |
| Gain | How many times bigger the output is than the controlling input (no unit for VCVS) | A lever's mechanical advantage |
| Transconductance (gm) | Gain of a VCCS: output amps per input volt, measured in siemens | Litres per second of pump flow per bar of pressure |
| Amplifier | A circuit whose output signal is a larger copy of its input signal | A megaphone |
| Model | A simplified circuit that behaves like a real device in the situations we care about | A paper map of a real city |
| Input / output resistance | The resistance an amplifier presents at its input, and the Thevenin resistance of its output | How hard it is to push into the input, and how much the output sags under load |
| Feedback | Feeding part of the output back to the input, so the circuit corrects itself | A thermostat |
| Test source | A source you connect to a port to measure its resistance when other methods fail | Pushing on a door to feel how stiff it is |

## Learning Objectives

- Name the four kinds of dependent sources and draw their symbols.
- Explain why dependent sources are not real parts but models of transistors and amplifiers, and where their energy comes from.
- Analyse amplifier models built from a VCVS or a VCCS, with input and output resistances, by hand and with `sim`.
- Explain why dependent sources must stay on during superposition and Thevenin analysis, and use a test source to find the Thevenin resistance of a circuit with feedback.
- Write the MNA stamps of a VCVS and a VCCS and recognise them in `sim/elements.py`.

## The Problem

Everything so far was passive resistors and fixed sources. That is not enough to describe the most important parts in electronics: transistors and amplifiers.

Take a microphone. It produces about 10 mV. A loudspeaker needs volts. Something in between must take a small voltage and produce a large one, a *copy* whose size follows the input. No arrangement of resistors and batteries can do that: a resistor network always gives an output *smaller* than its sources (dividers only divide).

What you need is a source whose output follows a voltage somewhere else, multiplied by a gain. In Phase 12 you will see that a transistor behaves, for small signals, exactly like a VCCS: a current at its collector set by the voltage at its base. In Phase 13 an op-amp behaves like a VCVS with a gain of a hundred thousand. Before you meet the real devices, you need the circuit element that models them. That is the **dependent source**. And since it changes how superposition and Thevenin work, you need to learn the new rules now.

## The Physics

There is no part in a shop called "dependent source". It is a **model**: a piece of circuit that behaves like a real active device for the purposes of analysis.

Where does its energy come from? From a power supply, always. A transistor amplifier is connected to a battery or a supply rail. The small input signal does not provide the output's energy; it *controls* how much of the supply's energy is let through to the output, the way a small hand on a tap controls a large flow of water from the mains. The dependent source in the model hides this: it is drawn as if it created power by itself, and the supply is often left out of small-signal drawings.

That is why dependent sources can deliver more power to a load than their controlling input receives, which is the definition of **power gain**. And it is why a circuit with dependent sources can show behaviour no resistor network can: gain, negative resistance, oscillation.

What the model gets wrong: a real amplifier cannot produce more voltage than its supply (it "clips" at the rails, Phase 13), it has limited speed (Phase 13), and a transistor is only approximately linear for small signals (Phase 12). The dependent source is perfectly linear and infinitely strong. As long as signals stay small and slow, it is an excellent model.

## The Concept

### The four kinds

Dependent sources are drawn as diamonds, to tell them apart from the circles of independent sources:

```
     VCVS                 VCCS                 CCVS                 CCCS
      +                     ↑
     ◇ v = A × vx          ◇ i = gm × vx       ◇ v = rm × ix        ◇ i = β × ix
      -
  (gain A, no unit)    (gm in siemens)      (rm in ohms)         (β, no unit)
```

- `vx` is a controlling voltage between two nodes somewhere in the circuit.
- `ix` is a controlling current through some branch.

Our simulator provides the two voltage-controlled kinds directly:

```python
circuit.vcvs("E1", "out", "0", "p", "n", gain)   # v(out) - v(0) = gain × (v(p) - v(n))
circuit.vccs("G1", "out", "0", "p", "n", gm)     # current gm × (v(p) - v(n)) flows from out, through G1, to 0
```

(The letters E and G come from SPICE, where E is a VCVS and G a VCCS. F and H are the current-controlled ones.) Current-controlled sources can always be built from these: send the controlling current through a small sensing resistor `Rs`, and control a voltage-controlled source with the voltage across it, scaling the gain by `1/Rs`.

### Example 1: a voltage amplifier model (VCVS)

A practical model of any voltage amplifier has three parts: an input resistance (what the input looks like to the source driving it), a VCVS that multiplies the input voltage, and an output resistance (the Thevenin resistance of the output).

```
        signal source                   amplifier                       load
   ┌──[Rs = 1 kΩ]──● in ──────┐       ┌──[Rout = 100 Ω]──● out ──┐
   │               │          │       │                  │        │
 [vs = 100 mV]   [Rin = 9 kΩ] │      ◇ A × v(in)          [RL = 900 Ω]
   │               │          │       │  A = 50          │        │
   └───────────────┴──────────┘       └──────────────────┴────────┘
                        all bottoms are ground
```

Step by step, by hand:

1. **Input divider.** The signal source (100 mV behind 1 kΩ, a Thevenin source) drives the 9 kΩ input:
   `v(in) = 100 mV × 9 / (1 + 9) = 90 mV`. We lost 10 % because the input resistance is not infinite.
2. **The VCVS.** It produces `A × v(in) = 50 × 90 mV = 4.5 V`. Notice that the VCVS does not load the input at all: it only *looks at* `v(in)`, it draws no current from it.
3. **Output divider.** 4.5 V behind `Rout = 100 Ω` drives `RL = 900 Ω`:
   `v(out) = 4.5 × 900 / (100 + 900) = 4.05 V`. Another 10 % lost.

Overall voltage gain: `4.05 V / 0.1 V = 40.5`, less than the "50" printed on the box, because of the two dividers. This is the most important practical lesson about amplifiers: **the gain you get depends on what is connected on both sides.**

Power: the input takes `v(in)² / Rin = (0.09)² / 9000 = 0.9 µW`. The load receives `4.05² / 900 = 18.2 mW`. A power gain of about 20 000. That energy, in a real amplifier, comes from its power supply.

### Example 2: a transistor-like model (VCCS)

A transistor amplifier stage, for small signals, behaves like a VCCS: an input voltage `v(in)` sets an output current `gm × v(in)` that is pulled through a resistor `RC` from a supply. (Phase 12 builds this from the real transistor; here it is just the model.)

```
           VCC = 10 V
              │
            [RC]
              │
              ● out
              │
             ◇  G1: pulls gm × v(in) from out to ground
              │
             gnd
```

With `gm = 40 mS` (a typical transistor value at 1 mA, which you will derive in Phase 12) and `RC = 2 kΩ`:

```
v(in) = 0       →  current 0         →  v(out) = 10 V
v(in) = 10 mV   →  current 0.4 mA    →  v(out) = 10 - 2 kΩ × 0.4 mA = 9.2 V
v(in) = 20 mV   →  current 0.8 mA    →  v(out) = 8.4 V
```

Every extra 10 mV in gives 0.8 V less out. The voltage gain is `Δv(out) / Δv(in) = -0.8 V / 10 mV = -80`, which is `-gm × RC = -0.04 × 2000`. The minus sign means the output moves *opposite* to the input: this stage is an **inverting amplifier**.

### Example 3: feedback tames a huge gain

An op-amp (Phase 13) is, to a first approximation, a VCVS with an enormous gain, say `A = 100 000`, controlled by the difference between its two inputs: `v(out) = A × (v(+) - v(-))`. Such a gain is useless on its own: 1 mV of input would ask for 100 V of output. But wrapped in **feedback** it becomes precise:

```
              R2 = 10 kΩ
          ┌──/\/\/\/\──────────┐
          │                    │
 vin ──[R1 = 1 kΩ]──● n ───────┤
                    │          │
                  (−)  E1      │
                  (+) ◇ A × (v(+) - v(n)) ── ● out
                    │
                   gnd
```

Node n sits between R1 and R2. By the divider rule with two sources (superposition, Lesson 05):

```
v(n) = vin × R2/(R1 + R2) + v(out) × R1/(R1 + R2)
```

and the VCVS says `v(out) = A × (0 - v(n)) = -A × v(n)`. Substitute and solve for the gain:

```
v(out) / vin = - [A × R2/(R1+R2)] / [1 + A × R1/(R1+R2)]
```

With `A = 100 000`, `R1 = 1 kΩ`, `R2 = 10 kΩ`: `R2/(R1+R2) = 10/11 = 0.9091`, `R1/(R1+R2) = 1/11 = 0.0909`.

```
gain = - (100 000 × 0.9091) / (1 + 100 000 × 0.0909)
     = - 90 909 / 9 092
     = - 9.9989
```

Almost exactly `-R2/R1 = -10`. The huge, imprecise gain has disappeared from the answer; only the two resistors matter. If A were 50 000 instead, the gain would be -9.9978. This is why op-amp circuits are designed with feedback: the result depends on resistors you can buy at 0.1 % accuracy, not on a gain that varies by a factor of two between chips.

### Rule change 1: superposition keeps dependent sources ON

In superposition (Lesson 05) you turn off independent sources one at a time. **Dependent sources are never turned off**: they are part of the circuit's structure, like resistors. Their value is not an input; it is decided by the circuit. If you zero them, you analyse a different circuit.

### Rule change 2: Thevenin needs a test source

The dead-source method for `Rth` (Lesson 06, Method 2) breaks: you cannot kill a dependent source, and you cannot combine it with resistors by series-parallel rules. Use a **test source** instead:

1. Turn off the independent sources only.
2. Connect a test current source `It` into the port.
3. Solve the circuit (the dependent sources react to the test current) and measure the port voltage `Vt`.
4. `Rth = Vt / It`.

### A striking example: feedback shrinks output resistance

Take a VCVS with gain `A = 100 000` and output resistance `Rout = 100 Ω`, and wire it as a **voltage follower**: its controlling voltage is `v(in) - v(out)`, so it constantly corrects its own output.

```
 vin ──── (+)
              ◇ E1 = A × (v(in) - v(out)) ── x ──[Rout = 100 Ω]──● out
 out ──── (−)                                                    │
           (feedback wire from out back to the minus input)    port
```

What is the Thevenin resistance at `out`?

- **Wrong way:** "turn off" E1 (make it 0 V), and see 100 Ω. That would be correct only if E1 did not react.
- **Right way:** test source. With `vin = 0`, push `It` into `out`. E1 sees `v(in) - v(out) = -v(out)` and produces `v(x) = -A × v(out)`. The test current flows through `Rout` into x, so `v(out) = v(x) + It × Rout = -A × v(out) + It × Rout`. Solve:

```
v(out) × (1 + A) = It × Rout
Rth = v(out) / It = Rout / (1 + A) = 100 / 100 001 ≈ 0.001 Ω
```

Feedback made the output a hundred thousand times stiffer. This is why an op-amp follower can drive a load as if it were an ideal voltage source.

### The MNA stamps (how `sim` does it)

From Lesson 04, a voltage source with branch index k added row k: `v_p - v_m = V`. A VCVS is the same, except the right side is not a fixed number but `A × (v_cp - v_cm)`. Moving that to the left side:

```
row k:   +1 at column p,  -1 at column m,  -A at column cp,  +A at column cm,   z[k] = 0
plus the usual ±1 in column k of rows p and m (its current in KCL).
```

A VCCS adds no row. Its current `gm × (v_cp - v_cm)` leaves node p and enters node m, so in KCL:

```
row p:   +gm at column cp,  -gm at column cm
row m:   -gm at column cp,  +gm at column cm
```

Open `sim/elements.py` and find the `VCVS` and `VCCS` classes: their `stamp` methods are exactly these lines. Notice one new thing: these stamps make the matrix **non-symmetric** (row p gets entries in columns cp and cm, but rows cp and cm get nothing back). Resistor-only matrices are always symmetric; active devices break the symmetry.

## Build It

`code/main.py` simulates the three amplifier examples and the follower, compares every number with the hand formulas, and shows the test-source method.

### Step 1: the voltage amplifier model

```python
def voltage_amplifier(signal_volts, load_ohms=900):
    circuit = Circuit()
    circuit.voltage_source("VS", "s", "0", signal_volts)
    circuit.resistor("RS", "s", "in", 1000)
    circuit.resistor("RIN", "in", "0", 9000)
    circuit.vcvs("E1", "x", "0", "in", "0", 50.0)
    circuit.resistor("ROUT", "x", "out", 100)
    circuit.resistor("RL", "out", "0", load_ohms)
    return circuit
```

The code prints `v(in)`, `v(out)`, the overall gain (40.5), and the input and load powers with their ratio. It also repeats the run with lighter and heavier loads to show the gain changing.

### Step 2: the VCCS stage

```python
def transconductance_stage(input_volts, rc_ohms=2000, gm=0.04):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", 10.0)
    circuit.voltage_source("VIN", "in", "0", input_volts)
    circuit.resistor("RC", "vcc", "out", rc_ohms)
    circuit.vccs("G1", "out", "0", "in", "0", gm)
    return circuit
```

Running it with 0, 10 and 20 mV gives 10, 9.2 and 8.4 V; the code computes the gain from two runs and compares it with `-gm × RC`.

### Step 3: feedback

The inverting amplifier with `A = 10⁵` gives a gain of -9.9989, and the code repeats it for A from 10 to 10⁶ to show the gain converging to -10.

### Step 4: Thevenin resistance with a test source

```python
def follower_output_resistance(gain, rout=100.0, test_amps=1e-3):
    circuit = Circuit()
    circuit.voltage_source("VIN", "in", "0", 0.0)
    circuit.vcvs("E1", "x", "0", "in", "out", gain)
    circuit.resistor("ROUT", "x", "out", rout)
    circuit.current_source("ITEST", "0", "out", test_amps)
    return circuit.dc().v("out") / test_amps
```

The code prints the result next to `Rout / (1 + A)`, and next to the wrong "kill the dependent source" answer of 100 Ω.

Run it:

```
uv run python phases/05-circuit-analysis-and-our-simulator/08-dependent-sources/code/main.py
```

## Use It

- **Transistor small-signal models.** The "hybrid-pi" model of a BJT, used in every analog design textbook, is a resistor `rπ` at the input and a VCCS `gm × vbe` at the output. A MOSFET's model is a VCCS with an infinite input resistance. You will build both in Phase 12.
- **Op-amp datasheets.** Datasheets of op-amps such as the TL072 or LM358 quote an "open-loop voltage gain" (often 100 dB, which is 100 000) and an "output resistance": the A and Rout of the VCVS model you used here.
- **SPICE macromodels.** Manufacturers ship SPICE models of their op-amps made largely from E and G elements (VCVS and VCCS) plus resistors and capacitors, because they simulate fast and capture the important behaviour.
- **Sensors and transducers.** A Hall-effect sensor produces a voltage proportional to magnetic field; a current-sense amplifier produces a voltage proportional to a current. Both are dependent sources in a system diagram.

## Try It in the Lab

The lab board is the transistor-like stage: a 10 V supply, a 50 mV input, and a VCCS with `gm = 40 mS` that pulls current from the output node. The resistor from the supply to the output (the slot) is missing. Choose it so the output rests between 4.5 V and 5.5 V: the middle of the supply, where an amplifier has the most room to swing up and down.

Think first:

- How much current does the VCCS pull with 50 mV at its input?
- The output is the supply minus the drop across the slot resistor. Which resistor puts it near 5 V?
- Why would an amplifier designer want the output near the middle of the supply? (Phase 12 will answer in detail.)

## Common Mistakes

- **Turning dependent sources off for superposition.** Only independent sources are switched off. Dependent ones stay.
- **Using the dead-source method for Rth.** With dependent sources, use a test source (or `Voc / Isc`).
- **Forgetting the controlling quantity's polarity.** `A × (v(p) - v(n))` is not `A × (v(n) - v(p))`. One flips the sign of the gain.
- **Thinking the VCVS draws current from its control nodes.** It only senses them. Input loading comes from input resistances you draw explicitly.
- **Believing the model beyond its limits.** A model VCVS happily outputs 1000 V. A real amplifier stops at its supply rails.
- **Treating gain as fixed.** The voltage gain of an amplifier model depends on the source resistance and the load (Example 1).

## Exercises

1. In Example 1, replace the 900 Ω load by 100 Ω. What is the overall gain now? (Answer: 22.5.)
2. In Example 2, what `RC` gives a gain of -100 with `gm = 40 mS`? What is the output with 0 V input? With 50 mV?
3. In Example 3, what gain results with `R1 = 2 kΩ`, `R2 = 20 kΩ` and `A = 1000`? Compare with `-R2/R1`.
4. Build a current-controlled current source from a 1 Ω sensing resistor and a VCCS, with current gain β = 100, in `sim`. Feed 10 µA through the sensing resistor and check the output current.
5. Harder: find the Thevenin equivalent (Vth and Rth) of Example 1's amplifier output, as seen by the load, using `Voc`, `Isc` and a test source. Explain why Rth is just Rout here, while in the follower it was much smaller.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Dependent source | "Controlled source" | A source whose value is a fixed multiple of a voltage or current elsewhere in the circuit |
| VCVS (E) | "Ideal amplifier" | `v_out = A × v_control`, draws nothing from the control nodes |
| VCCS (G) | "Transconductor" | `i_out = gm × v_control`, the core of transistor models |
| Gain | "How much it amplifies" | Output divided by input; for a VCVS a pure number, for a VCCS in siemens |
| Feedback | "Closing the loop" | Feeding the output back to the input so the result depends on stable parts (resistors) instead of the raw gain |
| Test source | "Push and measure" | A current (or voltage) applied to a port, with independent sources off, to find Rth when dependent sources are present |
| Model | "The equivalent circuit" | Ideal elements arranged to mimic a real device in a limited range of conditions |

## Further Reading

- *The Art of Electronics*, Horowitz and Hill, 3rd edition, Chapter 2 (transistors as transconductance devices) and Chapter 4 (op-amps and feedback).
- Agarwal and Lang, *Foundations of Analog and Digital Electronic Circuits* (MIT 6.002 textbook), Chapter 7 "The MOSFET Amplifier", which builds an amplifier from a dependent source.
- [MIT OpenCourseWare 6.002 Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/): the lectures on dependent sources, amplifiers and small-signal models.
- [Texas Instruments TL072 datasheet](https://www.ti.com/lit/ds/symlink/tl072.pdf): look up the open-loop gain and the typical application circuits that use feedback.
