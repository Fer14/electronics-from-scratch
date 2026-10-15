# The Ideal Op-Amp

> An op-amp is an amplifier with a ridiculous gain and two inputs. Alone it is useless for amplifying. Wrap it in negative feedback and it does exactly what its resistors tell it to, regardless of its own imperfections.

**Type:** Learn
**Prerequisites:** Phase 12 (Transistors), especially 06-amplifiers-and-biasing (negative feedback) and 08-current-mirrors; Phase 04 (Kirchhoff's Laws), lesson 05-the-voltage-divider; Phase 05 (Circuit Analysis and Our Simulator), lesson 08-dependent-sources
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Op-amp (operational amplifier) | A chip with two inputs and one output that amplifies the *difference* between its inputs by a huge factor | A super-sensitive referee who reacts to the tiniest difference between two teams |
| Non-inverting input (+, V+) | The input whose rise makes the output rise | The accelerator pedal |
| Inverting input (−, V−) | The input whose rise makes the output fall | The brake pedal |
| Open-loop gain (A) | How much the op-amp multiplies V+ − V− with nothing connected around it, typically 100,000 to 10,000,000 | A lever so long that a hair's movement at one end swings the other end wildly |
| Supply rails | The positive and negative supply voltages; the output can never go beyond them | The floor and ceiling of a room |
| Saturation (op-amp) | The output stuck at (or near) a rail because the input difference is too large | A needle pinned against the end of its scale |
| Feedback | Connecting the output back to an input | Watching where your hand is while reaching for a cup |
| Negative feedback | Feedback to the inverting input, so that the output counteracts its own changes | A thermostat |
| Closed-loop gain | The gain of the whole circuit with feedback, set by the feedback network | The thermostat setting, not the heater's raw power |
| Voltage follower (buffer) | An op-amp whose output is connected straight to its minus input: output = input, but with strength | A strong assistant who copies exactly what you point at |
| Golden rules | Two shortcuts for analysing op-amp circuits with negative feedback: no input current, and V+ = V− | The two rules of thumb a pilot learns before the full theory |
| Loading | When connecting a load changes the voltage of the circuit feeding it | A tap that loses pressure when you open a second tap |

## Learning Objectives

- Describe the op-amp's inputs, output and open-loop behaviour: V_out = A (V+ − V−), clipped at the rails.
- Explain why, open loop, an op-amp is a comparator and not a useful amplifier.
- Derive the voltage follower's gain A/(1 + A) and see that it approaches exactly 1.
- State the two golden rules and explain why the second one is a *result* of negative feedback, not a property of the chip.
- Use a follower to buffer a voltage divider so a load cannot disturb it.

## The Problem

Phase 12 built an amplifier from one transistor and five resistors. Its gain depended on β, on temperature, on the bias current; getting a precise gain of 10 took care, and a precise gain of 100 was harder still. Its input pulled current from the source, its output sagged under load.

The operational amplifier, born in analogue computers of the 1940s and on a chip since the 1960s (Bob Widlar's μA702 and LM101, then the famous μA741 of 1968), changes the game. Inside are 20 or so transistors arranged in the stages of Phase 12: a differential input pair, mirror loads, a gain stage, an output stage. From outside, it looks almost like a mathematical ideal: enormous gain, practically no input current, an output that can drive loads. With two resistors you get a gain that is exact to the tolerance of the resistors. This phase is about using that ideal, and lesson 07 about where it breaks.

## The Physics

### What's inside, in one paragraph

An op-amp's input is a **differential pair**: two matched transistors sharing a current source, whose currents split according to the difference of their base (or gate) voltages. A current mirror (Phase 12 lesson 08) turns that split into a single output current and gives a gain of thousands. A second stage, with a capacitor that sets its frequency response (lesson 07), adds more gain. An output stage (a push-pull pair of emitter followers) provides current without losing voltage. Overall: about 100 dB (×100,000) of gain from DC to a few hertz.

### The symbol and the equation

```
              V+ ---|+ \
                    |    >---- V_out
              V- ---|- /
          (supply pins +V_S and -V_S usually not drawn)
```

```
V_out = A × (V+ − V−)      clipped between the supply rails
```

Read: "the output equals the open-loop gain times the difference between the plus and minus inputs". `A` is the **open-loop gain**, 10⁵ for our simulator's op-amp. There is no "ground" input: only the *difference* between the two inputs matters (as long as both stay within the supply range).

What the referee analogy gets wrong: a referee decides once. An op-amp reacts continuously, and its reaction (the output) can feed back into what it sees. That loop is what this phase is about.

## The Concept

### Open loop: an over-eager amplifier

Our op-amp with ±12 V rails, minus input grounded, plus input driven directly:

| V+ − V− | Output |
|---|---|
| −200 µV | −11.17 V |
| −50 µV | −4.73 V |
| 0 | 0.00 V |
| +10 µV | +1.00 V |
| +50 µV | +4.73 V |
| +100 µV | +8.19 V |
| +1000 µV | +12.00 V |

10 µV in, 1 V out: a gain of 100,000 (100 dB). But the output is pinned at a rail for any input bigger than about ±100-200 µV. (Our simulator rounds the corner at the rails smoothly, which is why 100 µV gives 8.2 V rather than exactly 10 V; real op-amps behave similarly near their limits.) The noise in any real signal is larger than 100 µV. So **open loop, an op-amp only tells you which input is higher**. That is a **comparator**, the subject of lesson 02. To amplify, we need feedback.

### Closing the loop: the voltage follower

Connect the output straight back to the minus input, and feed the signal into the plus input:

```
   V_in ---|+ \
           |    >----+---- V_out
        +--|- /      |
        |            |
        +------------+
```

Now V− = V_out. Put that into the op-amp's equation:

```
V_out = A × (V_in − V_out)
V_out + A V_out = A V_in
V_out = V_in × A / (1 + A)
```

Read the last line: "the output equals the input times A over one plus A". For A = 10⁵, A/(1 + A) = 0.99999: the output equals the input to five decimal places. The simulator, with 2.000 V in:

| A | Output | A/(1 + A) × 2 V | V+ − V− |
|---|---|---|---|
| 10 | 1.818182 V | 1.818182 V | 181,818 µV |
| 100 | 1.980198 V | 1.980198 V | 19,802 µV |
| 1,000 | 1.998002 V | 1.998002 V | 1998 µV |
| 100,000 | 1.999980 V | 1.999980 V | 20 µV |
| 10,000,000 | 2.000000 V | 2.000000 V | 0.2 µV |

**How negative feedback works, step by step.** Suppose the output were too low, below V_in. Then V+ − V− = V_in − V_out is positive, and the huge gain drives the output up. If it overshoots above V_in, the difference turns negative and drives it down. The only stable place is where the difference is just big enough, V_out / A, to hold the output there: 20 µV for 2 V of output. The op-amp chases its own output until its inputs are (almost) equal.

### The two golden rules

For any op-amp circuit with **negative feedback** (and the output not stuck at a rail):

1. **No current flows into the inputs.** Real op-amps draw picoamps to nanoamps; we treat it as zero.
2. **The output does whatever is needed to make V+ = V−.** Because A is enormous, the difference needed is microvolts; we treat it as zero.

Rule 1 is a property of the chip (its input transistors, Phase 12). Rule 2 is **not** a property of the chip: it is what negative feedback does with a large gain. Without negative feedback (open loop, or positive feedback as in lesson 02), rule 2 is false. Every circuit in lessons 03-06 is analysed with these two rules and Ohm's law.

Rule 1 in the simulator: a 3 V source behind 1 MΩ into a follower gives an output of 2.99997 V and only 0.003 nA through the 1 MΩ resistor. (That residual comes from the tiny leak conductance the simulator adds for numerical safety; the op-amp model itself takes no input current.)

### Why bother with a gain of 1?

A follower outputs the same voltage it is given. Why is that useful? Because of **loading**. Take a 10 kΩ / 10 kΩ divider making 5 V from 10 V, and connect loads to it:

| Load | Directly on the divider | Through a follower | Current from the divider |
|---|---|---|---|
| 1 MΩ | 4.975 V | 4.9999 V | 0.500 mA |
| 100 kΩ | 4.762 V | 4.9999 V | 0.500 mA |
| 10 kΩ | 3.333 V | 4.9999 V | 0.500 mA |
| 1 kΩ | 0.833 V | 4.9999 V | 0.500 mA |

Directly, the load sits in parallel with the bottom resistor and drags the voltage down: 1 kΩ ∥ 10 kΩ = 909 Ω, and 10 × 909/(10,000 + 909) = 0.833 V (Phase 04). Through the follower, the divider sees the op-amp's input (no current, rule 1) and stays at 5 V; the 5 mA the 1 kΩ load needs comes from the op-amp's own supply via its output. The follower is a **buffer**: high input resistance, low output resistance, gain 1. It separates a delicate source from a demanding load.

### Thinking about power

Op-amps need power supply pins, usually not drawn in schematics. All the output current comes from them. A typical op-amp can supply 10-40 mA from its output; beyond that you need a transistor stage after it (Phase 12). And the output range is limited to the rails (minus some headroom, lesson 07).

## Build It

### Step 1: Open loop

```python
def open_loop(differential_volts, gain=1e5):
    circuit = Circuit()
    circuit.voltage_source("VP", "p", "0", differential_volts)
    circuit.opamp("U1", plus="p", minus="0", out="out", gain=gain, rails=RAILS)
    return circuit.dc().v("out")
```

`opamp(name, plus, minus, out, gain, rails)` is our simulator's op-amp: an output voltage source equal to gain × (V+ − V−), squeezed smoothly between the rails when `rails` is given. Its inputs draw no current.

### Step 2: The follower with different gains

```python
circuit.opamp("U1", plus="in", minus="out", out="out", gain=gain)
```

Tying `minus` to `out` is the whole feedback network. Without `rails` the model is linear, so we can compare it with A/(1 + A) exactly.

### Step 3: Buffering a divider

`divider_with_load` builds the 10 k / 10 k divider and either connects the load directly or through a follower, and reports the voltage and the divider's current.

```
uv run python phases/13-operational-amplifiers/01-the-ideal-op-amp/code/main.py
```

## Use It

- **Classic parts**: μA741 (1968; gain about 200,000, needs ±5 V or more, input bias currents around 80 nA), LM358 / LM324 (dual/quad, single supply from 3 V, cheap and everywhere), TL071/TL072 (JFET inputs, picoamp input currents, used in audio), OPA2134 (audio), MCP6002 (rail-to-rail, 1.8-6 V, for 3.3 V microcontroller systems).
- **Buffers everywhere**: between a potentiometer and an analogue-to-digital converter input, after a voltage reference, before a long cable, after a high-impedance sensor (pH probes are about 100 MΩ!).
- **Datasheet terms for the golden rules**: "large-signal voltage gain" (A, often in V/mV: 200 V/mV = 200,000), "input bias current" (rule 1's reality), "input offset voltage" (rule 2's reality: the inputs are equal only to within a millivolt or so). Lesson 07 covers them.
- **Packages**: 8-pin DIP or SOIC with two op-amps is the most common, pinout: 1 out A, 2 −in A, 3 +in A, 4 V−, 5 +in B, 6 −in B, 7 out B, 8 V+.

## Try It in the Lab

The lab is the buffered divider: a 10 V source, a 10 k / 10 k divider, an op-amp powered from 0 and 12 V with its plus input on the divider, and a 1 kΩ load on its output. A 1 MΩ resistor ties the minus input to ground so it is never floating. The connection from the output back to the minus input is up to you.

Think about: what the op-amp does with no feedback (it amplifies V+ − V− by 100,000), what "inputs equal" means when the output is wired straight to the minus input, and what a 1 MΩ feedback resistor would do together with the 1 MΩ to ground (a divider in the feedback path: lesson 03 calls it a gain of 2).

## Common Mistakes

- **Using the golden rules without negative feedback.** Open loop, V+ ≠ V−, and the output sits at a rail.
- **Forgetting the supply pins.** An op-amp's output current comes from its supply; with no supply connected, nothing works.
- **Expecting the output to go beyond the rails.** A follower on a 0-12 V supply cannot output 15 V or −1 V.
- **Leaving an input floating.** An unconnected input picks up noise and drives the output wildly. Every input needs a DC path.
- **Thinking the op-amp "copies" the input by magic.** It copies because the feedback loop forces V− to follow V+; break the loop and it stops.
- **Overloading the output.** 1 kΩ at 5 V is 5 mA, fine; 10 Ω would ask for 500 mA, which no small op-amp can provide.

## Exercises

1. An op-amp with A = 200,000 and ±15 V rails has V+ = 1.000050 V and V− = 1.000000 V, open loop. What does the output try to be, and what is it really?
2. A follower uses an op-amp with A = 50,000. What is the output for 3.3 V in? How many microvolts apart are the inputs?
3. A 5 V reference has an output resistance of 50 Ω. A 100 Ω load is connected. What does the load see directly, and through an ideal follower?
4. A follower has a voltage gain of 1. Does it have a power gain? In the 1 kΩ example, compare the current the divider supplies to the op-amp's input with the current the load receives, and compute the power delivered to the load.
5. In the script, change the divider to 100 kΩ / 100 kΩ and repeat the loading table. Which loads hurt the direct connection now?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Op-amp | "Operational amplifier" | Differential amplifier with very high gain, high input resistance, low output resistance |
| Open-loop gain A | "The op-amp's gain" | V_out / (V+ − V−) with no feedback; 10⁵-10⁷ at DC |
| Rails | "Supply", "headroom" | The supply voltages that bound the output |
| Negative feedback | "Closing the loop" | Output fed to the inverting input; forces V+ ≈ V− |
| Closed-loop gain | "The circuit's gain" | Gain set by the feedback network, e.g. A/(1+A) ≈ 1 for a follower |
| Golden rules | "Virtual short" | With negative feedback: no input current, V+ = V− |
| Buffer | "Follower", "unity-gain amp" | Gain-1 stage with high input and low output resistance; prevents loading |

## Further Reading

- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., chapter 4 "Operational Amplifiers", sections 4.1-4.2 (the golden rules).
- *All About Circuits*, Volume III, chapter 8 "Operational Amplifiers": "Single-ended and differential amplifiers", "The operational amplifier", "Negative feedback". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-8/single-ended-differential-amplifiers/
- R. Mancini (ed.), *Op Amps For Everyone* (Texas Instruments, 2002; Newnes), the chapters "Review of Circuit Theory" and "Development of the Ideal Op Amp Equations": practical and thorough.
- W. Jung (ed.), *Op Amp Applications Handbook* (Analog Devices), chapter H "Op amp history". https://www.analog.com/en/resources/technical-books/op-amp-applications-handbook.html
