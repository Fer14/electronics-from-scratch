# Thevenin and Norton

> However complicated the network, if it is linear and you only look at two of its terminals, it is a battery with a resistor in series. Nothing more.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 04 (Kirchhoff's Laws), especially Lesson 05 (The Voltage Divider); Phase 05 Lesson 02 (Nodal Analysis) and Lesson 05 (Superposition)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Terminal | A point where you can connect something from outside | A socket on the wall |
| Port | A pair of terminals used together to connect one thing | The two holes of a wall socket |
| Load | Whatever you connect to a port to use its power: a lamp, a speaker, a sensor input | The appliance you plug into the socket |
| Equivalent circuit | A simpler circuit that behaves exactly the same at the port as the real one | A stand-in actor who looks the same from the audience |
| Thevenin equivalent | One voltage source `Vth` in series with one resistor `Rth` | A battery with a little resistor glued to one end |
| Norton equivalent | One current source `In` in parallel with one resistor `Rn` | A pump with a leak pipe across it |
| Open-circuit voltage (`Voc`) | The voltage at the port when nothing is connected | The voltage of a battery sitting on a shelf |
| Short-circuit current (`Isc`) | The current that flows if you join the port's two terminals with a wire | What flows if you drop a spanner across a car battery (don't) |
| Thevenin resistance (`Rth`) | The resistance you "see" looking back into the port with all independent sources turned off | How hard it is to push current back into the socket |
| I-V line (load line) | The straight line linking port voltage and port current for every possible load | A price list: buy more current, get less voltage |
| Source transformation | Converting between Thevenin and Norton forms of the same port | Two ways of writing the same price list |

## Learning Objectives

- Explain why any linear two-terminal network has a straight-line I-V relation, and why two numbers (`Vth` and `Rth`) describe it completely.
- Find a Thevenin equivalent in three ways: from `Voc` and `Isc`, from `Voc` and the dead-source resistance, and (preview) with a test source.
- Convert between Thevenin and Norton forms with `In = Vth / Rth` and `Rn = Rth`.
- Use the equivalent to predict, in one line, the load voltage and current for any load resistor.
- Measure `Voc` and `Isc` with our simulator, build the equivalent, and show it matches the original network for many loads.

## The Problem

You are designing a sensor board. The sensor output comes out of a network of resistors and references that someone else designed, and you want to know what voltage your microcontroller's input will see. Then the next question: what if the input has 10 kΩ inside it? 100 kΩ? 1 MΩ? Each time, you would have to re-solve the whole network.

Or: you have a small solar panel with a regulator circuit inside, and you want to know how much current it can give a phone, or what its voltage drops to under load.

In both cases you do not care what happens *inside* the box. You care about two wires coming out of it, and how the box responds to whatever you connect.

Léon Charles Thévenin, a French telegraph engineer, published the answer in 1883 (Hermann von Helmholtz had found it in 1853): from the outside, any linear network is just one voltage source and one series resistor. Edward Lawry Norton at Bell Labs (and, independently, Hans Ferdinand Mayer at Siemens) gave the mirror form in 1926: one current source and one parallel resistor. With these, the load question becomes a two-resistor voltage divider, solved in your head.

## The Physics

Why can a whole network collapse into two numbers? Superposition (Lesson 05).

Connect anything to the port and call the port voltage `V` and the current flowing *out* of the port into your load `I`. Whatever the load is, from the network's point of view it draws some current `I`. So replace the load with a current source that pulls exactly that `I`. Now the network contains only linear parts and sources: its own internal sources, plus our current source pulling `I`. By superposition, the port voltage is:

```
V = (contribution of the internal sources with I = 0)  +  (contribution of I alone)
```

- The first part is the voltage with nothing drawn: the **open-circuit voltage**, `Voc`.
- The second part, with internal sources off, is the network acting as a plain resistor network with current `I` pulled out of it. A resistor network gives a voltage proportional to the current: `-Rth × I`, where `Rth` is the resistance seen looking into the port. (Minus, because pulling current out lowers the voltage.)

So:

```
V = Voc - Rth × I
```

Read it out loud: "the port voltage is the open-circuit voltage, minus a drop that grows in proportion to the current you take." That is the same equation as a battery `Voc` with a resistor `Rth` in series: every milliamp you draw loses `Rth × 1 mA` of voltage inside. The network and the little Thevenin circuit obey the same equation, so no load can tell them apart.

Physically, `Rth` is the price of drawing current: the energy per charge lost in the resistances on the way out. A real battery has one (its internal resistance, Phase 06). A voltage divider has one. A microphone, a sensor, an antenna, an amplifier output: all have one.

What the picture gets wrong: the equivalent only matches *at the port*. The power wasted *inside* the real network is generally not the power wasted in `Rth`. And it only works for linear networks; a network with a diode has a curved I-V relation that no single resistor can copy.

## The Concept

### The I-V line

Plot `V = Voc - Rth × I`:

```
  V (port voltage)
  │
Voc ●  open circuit (I = 0)
  │   ╲
  │     ╲     slope = -Rth
  │       ╲
  │         ╲
  │           ╲
  └─────────────●────── I (current out of the port)
                Isc   short circuit (V = 0)
```

A straight line is fixed by two points. The two easiest points are the ends:

- **Open circuit**: nothing connected, `I = 0`, so `V = Voc`. That gives `Vth = Voc`.
- **Short circuit**: a wire across the port, `V = 0`, so `0 = Voc - Rth × Isc`, which gives `Rth = Voc / Isc`.

Every possible load sits somewhere on this line. A 1 MΩ load sits near the top (little current, nearly full voltage); a 1 Ω load near the bottom (lots of current, almost no voltage).

### Method 1: open-circuit voltage and short-circuit current

Example: a voltage divider, 12 V battery, 6 kΩ on top, 3 kΩ on the bottom, the port across the 3 kΩ.

```
   ┌──────/\/\/\ 6 kΩ /\/\/\────●──── port +
   │                            │
 [12 V]                       [3 kΩ]
   │                            │
   └────────────────────────────●──── port -
```

**Voc**: nothing connected, so it is the plain divider: `12 × 3 / (6 + 3) = 12 × 0.3333 = 4 V`.

**Isc**: a wire across the port shorts out the 3 kΩ (no current goes through a resistor with a wire beside it: the wire has zero voltage, so the resistor has zero current). All current flows through the 6 kΩ and the wire: `12 V / 6 kΩ = 2 mA`.

**Rth** = `Voc / Isc = 4 V / 2 mA = 2 kΩ`.

So this divider, from the outside, is a 4 V battery with 2 kΩ in series.

### Method 2: open-circuit voltage and dead-source resistance

Turn every independent source off (voltage source → wire, current source → gap, as in Lesson 05), then compute the resistance between the port terminals using series-parallel rules.

For the divider: the 12 V battery becomes a wire, so the 6 kΩ now goes from the port's top terminal to the bottom wire. Looking into the port you see 6 kΩ in parallel with 3 kΩ:

```
Rth = (6 × 3) / (6 + 3) = 18 / 9 = 2 kΩ
```

Same answer, as it must be. This method is often fastest by hand. It fails only when the network contains dependent sources (Lesson 08), because those cannot be turned off.

### Method 3 (preview): test source

Turn off the independent sources, push a known test current `It` into the port, and measure the voltage `Vt` it produces. Then `Rth = Vt / It`. This always works, including with dependent sources. Lesson 08 uses it.

### Using the equivalent: one-line load calculations

With `Vth = 4 V` and `Rth = 2 kΩ`, any load `RL` forms a divider with `Rth`:

```
V_load = Vth × RL / (Rth + RL)
I_load = Vth / (Rth + RL)
```

| Load RL | V_load | I_load |
|---|---|---|
| 1 kΩ | 4 × 1/3 = 1.333 V | 1.333 mA |
| 2 kΩ | 4 × 2/4 = 2.000 V | 1.000 mA |
| 6 kΩ | 4 × 6/8 = 3.000 V | 0.500 mA |
| 20 kΩ | 4 × 20/22 = 3.636 V | 0.182 mA |
| 1 MΩ | 4 × 1000/1002 = 3.992 V | 0.004 mA |

No re-solving. This is how engineers reason about "loading" all day long: the load is only "light" when it is much bigger than `Rth`.

### The workhorse, seen from R4

Back to our workhorse. Pull R4 out and look into the two terminals where it was (node c and ground):

```
        a      R1 = 1 kΩ      b      R3 = 3 kΩ      c
   ┌────●────/\/\/\/\────●────/\/\/\/\────●────────────┐
   │                     │                 │            │
 [V1] 12 V             [R2] 2 kΩ        port +        (I1) 1 mA up
   │                     │                 │            │
   └─────────────────────┴─────────── port - ──────────┘
```

**Rth** (Method 2): V1 → wire, I1 → gap. From c, you see R3 in series with (R1 ∥ R2):

```
Rth = 3 + (1 × 2)/(1 + 2) = 3 + 0.6667 = 3.6667 kΩ
```

**Voc**: with nothing at the port, the 1 mA from I1 has only one way to go: through R3 into node b. KCL at b, nodal style (Lesson 02):

```
(vb - 12)/1 + vb/2 = 1 mA   (the 1 mA arriving through R3)
1.5 vb = 13
vb = 8.667 V
```

The 1 mA flows from c to b through R3, so c is higher than b by `3 kΩ × 1 mA = 3 V`:

```
Voc = 8.667 + 3 = 11.667 V
```

Check by putting R4 back: `V = 11.667 × 1 / (3.6667 + 1) = 11.667 / 4.6667 = 2.5 V`. The same 2.5 V we found in Lessons 01 to 05. The whole left side of the circuit, battery and current source and three resistors, behaves like an 11.67 V battery with 3.67 kΩ inside.

### Norton: the same line, written the other way

Rearrange `V = Vth - Rth × I`:

```
I = Vth/Rth - V/Rth
```

"The output current is a fixed current `Vth / Rth`, minus whatever leaks through a resistor `Rth` placed across the port." That is a current source `In = Vth / Rth` in parallel with `Rn = Rth`:

```
   Thevenin                    Norton
   ┌──[Rth]──● +               ┌────────┬────● +
   │         │                 │        │
 [Vth]     (load)            (In ↑)   [Rn]   (load)
   │         │                 │        │
   └─────────● -               └────────┴────● -

   In = Vth / Rth  = Isc       Rn = Rth
```

For the divider: `In = 4 V / 2 kΩ = 2 mA` (exactly the short-circuit current, of course), `Rn = 2 kΩ`. For the workhorse port: `In = 11.667 / 3.6667 = 3.182 mA`.

Swapping one form for the other is the **source transformation** you used in Lesson 03 (a 1 mA source with 1 kΩ in parallel became a 1 V battery with 1 kΩ in series). Now you know why it is legal: both forms have the same I-V line.

### Which form to use

- Voltage-like sources (batteries, regulator outputs, op-amp outputs) have small `Rth`: think Thevenin.
- Current-like sources (photodiodes, transistor collectors, some sensors) have huge `Rth`: think Norton.
- For combining things in parallel, Norton is handy (currents add); in series, Thevenin (voltages add).

## Build It

`code/main.py` finds the equivalents of the divider and of the workhorse with our simulator, then proves the equivalent matches the original for a range of loads.

### Step 1: networks as functions with a port

Each network is a function that adds its parts to a circuit and leaves two terminals free: `"p"` (port plus) and ground. The argument `sources_on` multiplies every independent source, so `sources_on=0.0` turns them all off (0 V is a wire, 0 A is a gap).

```python
def divider(circuit, sources_on=1.0):
    circuit.voltage_source("V1", "a", "0", 12.0 * sources_on)
    circuit.resistor("R1", "a", "p", 6000)
    circuit.resistor("R2", "p", "0", 3000)


def workhorse_without_r4(circuit, sources_on=1.0):
    circuit.voltage_source("V1", "a", "0", 12.0 * sources_on)
    circuit.resistor("R1", "a", "b", 1000)
    circuit.resistor("R2", "b", "0", 2000)
    circuit.resistor("R3", "b", "p", 3000)
    circuit.current_source("I1", "0", "p", 0.001 * sources_on)
```

### Step 2: measure Voc and Isc

Open circuit: solve with nothing attached and read `v("p")`. Short circuit: attach a 0 V voltage source across the port. That source is a perfect wire *and* an ammeter: the simulator reports the current through it.

```python
def thevenin(network):
    open_circuit = Circuit()
    network(open_circuit)
    v_open = open_circuit.dc().v("p")
    shorted = Circuit()
    network(shorted)
    shorted.voltage_source("VSHORT", "p", "0", 0.0)
    i_short = -shorted.dc().i("VSHORT")
    return v_open, v_open / i_short, i_short
```

Why the minus? `sim` reports a source's current as the current it pushes *out of its plus terminal*. The network pushes current *into* the short's plus terminal, so the reported value is negative.

### Step 3: Rth a second way, with dead sources

Method 2 in code: build the network with its sources off, push a 1 mA test current into the port, and read the voltage it produces. `Rth = V / 1 mA`.

```python
def dead_source_resistance(network, test_amps=0.001):
    dead = Circuit()
    network(dead, sources_on=0.0)
    dead.current_source("ITEST", "0", "p", test_amps)
    return dead.dc().v("p") / test_amps
```

Both methods print 2.0000 kΩ for the divider and 3.6667 kΩ for the workhorse.

### Step 4: compare original and equivalent for many loads

For each load resistor, three circuits are solved: the original network with the load, the Thevenin equivalent with the load, and the Norton equivalent with the load.

```python
def load_voltage_thevenin(v_th, r_th, load):
    equivalent = Circuit()
    equivalent.voltage_source("VTH", "t", "0", v_th)
    equivalent.resistor("RTH", "t", "p", r_th)
    equivalent.resistor("RL", "p", "0", load)
    return equivalent.dc().v("p")


def load_voltage_norton(i_n, r_n, load):
    equivalent = Circuit()
    equivalent.current_source("IN", "0", "p", i_n)
    equivalent.resistor("RN", "p", "0", r_n)
    equivalent.resistor("RL", "p", "0", load)
    return equivalent.dc().v("p")
```

The printed table shows identical load voltages, to every printed digit, for loads from 100 Ω to 1 MΩ, together with the one-line formula `Vth × RL / (Rth + RL)`. For the workhorse, the 1 kΩ row reads 2.50000 V: R4's voltage from Lessons 01 to 05.

## Use It

- **Datasheet "output impedance".** When a datasheet says a sensor or reference has an output impedance of 1 kΩ, it is giving you `Rth`. The LM35 temperature sensor, for example, quotes a low output impedance (well under an ohm at its rated current), which is why it can drive an ADC input directly; a resistive divider of 100 kΩ resistors cannot.
- **Battery health.** A car battery's open-circuit voltage (about 12.6 V when charged) is its `Vth`; its internal resistance (a few milliohms when healthy) is its `Rth`. Battery testers measure both, exactly by loading the battery and watching the voltage drop. Phase 06 does this in depth.
- **Interfacing.** Connecting a sensor (with its `Rth`) to an ADC input (a load) is a two-resistor divider. Rule of thumb: keep the load at least 10 to 100 times larger than `Rth` so less than 10 % to 1 % of the signal is lost.
- **Simplifying big circuits.** Engineers routinely replace half a schematic with its Thevenin equivalent ("the bias network looks like 2.1 V behind 8.2 kΩ") to reason about the other half, especially when biasing transistors (Phase 12).

## Try It in the Lab

The lab board is the divider of this lesson: 12 V, 6 kΩ on top, 3 kΩ on the bottom, and an empty load slot across the 3 kΩ. Pick the load that makes the port voltage between 2.9 V and 3.1 V.

Before you press RUN:

- Find `Vth` and `Rth` of the divider (the lesson already did; can you do it again without looking?).
- With the equivalent, the load voltage is `Vth × RL / (Rth + RL)`. Which RL gives 3 V?
- Why do the other loads miss? Is the miss bigger for loads smaller or larger than `Rth`?

## Common Mistakes

- **Forgetting to remove the load before finding Voc.** `Voc` is measured with *nothing* connected. If the load stays in, you get the load voltage, not `Vth`.
- **Killing sources the wrong way.** Voltage source → wire, current source → gap. The reverse gives a wrong `Rth`.
- **Killing dependent sources.** You cannot turn off a dependent source (Lesson 08). Use the test-source method.
- **Thinking the equivalent wastes the same power as the original.** It matches only at the port. The internal power is generally different.
- **Assuming Rth is the sum of all resistors.** It is the resistance *seen from the port* with sources dead: some resistors end up in parallel, some vanish (shorted by a dead voltage source), some are cut off (by a dead current source).
- **Using it for non-linear networks.** A network with a diode or LED has no single `Rth`.

## Exercises

1. A network has `Voc = 9 V` and `Isc = 30 mA`. What are `Vth`, `Rth`, `In` and `Rn`? What voltage appears across a 300 Ω load? (Answer: 4.5 V.)
2. Find the Thevenin equivalent of a divider with 10 V, 1 kΩ on top and 1 kΩ on the bottom. What is the largest current it can ever deliver?
3. Find the Thevenin equivalent of the workhorse seen from R2's terminals (node b and ground, with R2 removed). Check by putting R2 back: you should get vb = 7 V.
4. A sensor has `Rth = 4.7 kΩ`. What is the smallest ADC input resistance that keeps the error below 1 %? Below 0.1 %?
5. Harder: two networks with Thevenin equivalents (5 V, 1 kΩ) and (3 V, 2 kΩ) are connected in parallel (plus to plus, minus to minus). Find the Thevenin equivalent of the combination by converting both to Norton, adding, and converting back. Verify with `sim`.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Thevenin equivalent | "A battery and a resistor" | `Vth` in series with `Rth`, matching the network's port I-V line exactly |
| Norton equivalent | "A current source and a resistor" | `In = Vth/Rth` in parallel with `Rn = Rth`, the same line written for current |
| Open-circuit voltage | "No-load voltage" | Port voltage with nothing connected, equal to `Vth` |
| Short-circuit current | "Max current" | Current through a wire across the port, equal to `In` |
| Thevenin resistance | "Output impedance" (for DC) | Slope of the I-V line; resistance seen into the port with independent sources dead |
| Loading | "The load pulls it down" | The port voltage falling below `Voc` because current through `Rth` drops voltage inside |
| Source transformation | "Swap Thevenin for Norton" | Replacing `Vth` + series `R` by `Vth/R` + parallel `R`, or back; identical at the port |

## Further Reading

- [All About Circuits, Vol. I, "Thevenin's Theorem" and "Norton's Theorem"](https://www.allaboutcircuits.com/textbook/direct-current/chpt-10/thevenins-theorem/): free worked chapters on both forms.
- *The Art of Electronics*, Horowitz and Hill, 3rd edition, Chapter 1 (the section on Thévenin equivalent circuits): how practising engineers use the idea for every interface.
- Don H. Johnson, "Origins of the equivalent circuit concept: the voltage-source equivalent", *Proceedings of the IEEE*, vol. 91, no. 4, 2003: the history from Helmholtz to Thévenin.
- [Khan Academy, Electrical Engineering, circuit analysis](https://www.khanacademy.org/science/electrical-engineering/ee-circuit-analysis-topic): videos on Thevenin and Norton equivalents.
