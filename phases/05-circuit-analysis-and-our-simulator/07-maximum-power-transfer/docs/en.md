# Maximum Power Transfer

> A source gives its load the most power when the load's resistance equals the source's own. And at that moment, exactly half the energy is wasted inside the source.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), especially Lesson 05 (Power and Heat); Phase 05 Lesson 06 (Thevenin and Norton)
**Time:** ~50 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Power | Energy per second, measured in watts (W); for a resistor `P = V × I = I² × R = V² / R` | How fast a kettle turns electricity into heat |
| Load power | The power that ends up in the load, where you want it | The heat in the kettle, not in the cable |
| Internal loss | Power burned inside the source's own resistance `Rth` | The heat in the cable and the plug |
| Efficiency | The fraction of the total power that reaches the load, written as a percentage | Miles per gallon for electricity |
| Matching (impedance matching) | Choosing the load resistance equal to the source resistance to get maximum power | Choosing a bicycle gear that suits your legs |
| Sweep | Repeating a simulation many times while changing one value | Trying every gear one after another |
| Maximum | The highest point of a curve | The top of a hill |
| Characteristic impedance | A standard resistance that cables and radio parts are designed around, often 50 Ω or 75 Ω | A standard pipe diameter |

## Learning Objectives

- Write the load power of a Thevenin source as a formula in the load resistance, and read it out loud.
- Show, without calculus, that load power is largest when `RL = Rth`, and find that maximum, `Vth² / (4 Rth)`.
- Compute efficiency for any load and explain why it is only 50 % at the maximum-power point.
- Decide when to match (weak signals, antennas, sensors) and when not to (power grids, batteries, chargers).
- Sweep a load with our simulator, locate the maximum, and plot power and efficiency against the load.

## The Problem

You have a source, maybe a small solar cell, an antenna, a microphone, a thermocouple or the divider from Lesson 06, and you want to get as much power as possible out of it into a load. What load resistance should you choose?

Two naive guesses, both wrong:

- "A tiny load, so lots of current flows." True, a lot of current flows, but the voltage across a tiny load is almost zero, so `P = V × I` is almost zero.
- "A huge load, so the full voltage appears across it." True, the voltage is nearly `Vth`, but almost no current flows, so `P` is again almost zero.

Somewhere in between there is a best load. Finding it is the **maximum power transfer theorem**, first stated by Moritz von Jacobi around 1840 (it is sometimes called "Jacobi's law"). It decides how antennas are connected to radios, why audio amplifiers were once wired to speakers through transformers, and what a solar charger's controller is trying to do.

And then there is a twist that surprised the early electrical industry: the best *power* is not the best *efficiency*. Thomas Edison's power stations were built the opposite way, on purpose.

## The Physics

Replace the source by its Thevenin equivalent (Lesson 06): a voltage `Vth` in series with `Rth`. The load `RL` is connected across the port. The same current `I` flows through both resistors (series), so the source's energy is shared between them:

```
   ┌──[ Rth ]──●──┐
   │           │  │
 [Vth]       [RL] │   I flows around the loop
   │           │  │
   └───────────●──┘
```

- Energy given by the source per second: `Vth × I`.
- Burned in `Rth` (wasted, inside the source): `I² × Rth`.
- Delivered to `RL` (useful): `I² × RL`.

Both are the same current squared times a resistance. So the share each one gets is in proportion to its resistance. That fact alone explains everything that follows: more `RL` means a bigger *share*, but also a smaller *current* for everyone.

What the model leaves out: real sources are not always linear (a solar cell's I-V curve is curved), and their `Rth` may change with temperature or light. The idea still holds locally, which is why solar chargers search for the best operating point continuously.

## The Concept

### Power as a formula in RL

The current in the loop is `I = Vth / (Rth + RL)`. The load power is:

```
P_L = I² × RL = Vth² × RL / (Rth + RL)²
```

Read it: "the load power is the source voltage squared, times the load resistance, divided by the square of the total resistance."

Numbers for the divider of Lesson 06, but with a 12 V battery feeding 3 kΩ over 6 kΩ (the lab board), so `Vth = 12 × 6 / 9 = 8 V` and `Rth = (3 × 6) / 9 = 2 kΩ`. In kΩ, V and mW (`V² / kΩ = mW`):

| RL | Total R | Current | P_L = I² × RL | Wasted in Rth | Efficiency |
|---|---|---|---|---|---|
| 0.5 kΩ | 2.5 kΩ | 3.2 mA | 5.12 mW | 20.48 mW | 20 % |
| 1 kΩ | 3 kΩ | 2.667 mA | 7.11 mW | 14.22 mW | 33 % |
| **2 kΩ** | 4 kΩ | 2.0 mA | **8.00 mW** | 8.00 mW | **50 %** |
| 4 kΩ | 6 kΩ | 1.333 mA | 7.11 mW | 3.56 mW | 67 % |
| 10 kΩ | 12 kΩ | 0.667 mA | 4.44 mW | 0.89 mW | 83 % |
| 100 kΩ | 102 kΩ | 0.078 mA | 0.62 mW | 0.01 mW | 98 % |

Look at the load power column: it rises, peaks at exactly 2 kΩ = `Rth`, and falls again. And notice the symmetry: 1 kΩ (half of Rth) and 4 kΩ (twice Rth) give the same 7.11 mW.

### Why the peak is exactly at RL = Rth (no calculus needed)

Divide the top and bottom of the power formula by `RL`:

```
P_L = Vth² / ( (Rth + RL)² / RL )
    = Vth² / ( Rth²/RL + 2 Rth + RL )
```

`Vth²` is fixed, so the power is largest when the bottom, `Rth²/RL + 2 Rth + RL`, is smallest. The middle `2 Rth` does not depend on `RL`, so we need the smallest value of

```
RL + Rth² / RL
```

Here is a trick from school algebra. Any number squared is zero or positive, so:

```
( √RL - Rth/√RL )² ≥ 0
RL - 2 Rth + Rth²/RL ≥ 0
RL + Rth²/RL ≥ 2 Rth
```

So `RL + Rth²/RL` can never be smaller than `2 Rth`, and it equals `2 Rth` exactly when the squared term is zero: `√RL = Rth / √RL`, which means `RL = Rth`. That is the maximum power point.

(With calculus you get the same: the derivative of `P_L` with respect to `RL` is proportional to `Rth - RL`, which is zero at `RL = Rth`.)

### How much power at the peak

Put `RL = Rth` into the formula:

```
P_max = Vth² × Rth / (2 Rth)² = Vth² / (4 Rth)
```

For our source: `8² / (4 × 2) = 64 / 8 = 8 mW`. Matches the table.

A shortcut that is easy to remember: at the match, the load gets half of `Vth` (a 50/50 divider), so `P_max = (Vth/2)² / Rth`.

### The peak is flat: you do not need a perfect match

Look at the table again: at half of `Rth` and at twice `Rth`, the load still gets 7.11 mW, which is `7.11 / 8 = 89 %` of the maximum. Put `RL = k × Rth` into the formula and simplify:

```
P_L / P_max = 4k / (1 + k)²
```

| k (RL / Rth) | Share of maximum power |
|---|---|
| 1 | 100 % |
| 0.8 or 1.25 | 99 % |
| 0.5 or 2 | 89 % |
| 0.25 or 4 | 64 % |
| 0.1 or 10 | 33 % |

So "close enough" is good enough: a load within 25 % of `Rth` already gets 99 % of the possible power. This is why engineers are relaxed about matching to within a standard resistor value, and also why a mismatch of 10 times is a serious loss.

### Any network, not only dividers

The theorem uses only `Vth` and `Rth`, so it works for any linear network. Take the workhorse seen from R4's terminals (Lesson 06): `Vth = 11.667 V`, `Rth = 3.667 kΩ`. The load that would take the most power is a 3.667 kΩ resistor in place of R4, and that power is

```
P_max = Vth² / (4 Rth) = 11.667² / (4 × 3.667) = 136.1 / 14.67 = 9.28 mW
```

The actual R4 = 1 kΩ is `k = 0.27` of `Rth`, so it gets `4 × 0.27 / 1.27² = 67 %` of that: `6.25 mW`, which is precisely the R4 power we computed in Lessons 01 and 05. Every number in this phase fits together.

### Efficiency: the price of maximum power

Efficiency is the useful fraction:

```
η = P_L / (P_L + P_wasted) = I² RL / (I² RL + I² Rth) = RL / (RL + Rth)
```

(`η` is the Greek letter "eta", the usual symbol for efficiency.) Read it: "the load's share of the total resistance". At the maximum-power point, `RL = Rth`, so `η = 1/2 = 50 %`. **Exactly as much power is wasted inside the source as is delivered.**

To be efficient you want `RL` much larger than `Rth`: 10× gives 91 %, 100× gives 99 %. But then the load gets much less than the maximum possible power.

### Two different goals

```
                 Load power                Efficiency
              ┌───────────────┐       ┌─────────────────────
   8 mW  ...  │      ●        │  100% │                ●●●●●
              │    ●   ●      │       │          ●●●●
              │  ●       ●    │   50% │      ●  (match)
              │●           ●  │       │   ●
              │              ●│       │ ●
           0  └───────────────┘    0% └─────────────────────
             0.1  1  2  10  100 kΩ    0.1  1  2  10  100 kΩ  (RL)
```

- **Want the most power from a weak, fixed source?** Match: `RL = Rth`. Accept 50 % efficiency, because the source's energy is free or tiny anyway (radio waves from a distant transmitter, a microphone's whisper, a sensor's microwatts).
- **Want to waste as little energy as possible?** Make `RL >> Rth` (or equivalently, make the source's `Rth` tiny). Power grids, batteries, phone chargers and power supplies are designed this way. A power station "matched" to the city would burn as much power in its own generators and lines as it delivers.

This is why Edison's (and every later) power plant was built with very low internal resistance: the goal was efficiency, not maximum transfer from a fixed generator. Jacobi's law had misled some early inventors into thinking motors could never exceed 50 % efficiency; they can, by not matching.

### Where the "resistance" is really an "impedance"

For AC signals (Phase 09 onwards), resistance generalises to *impedance*. Radio equipment is built around a standard of 50 Ω: transmitters, cables, antennas and receivers are all designed to look like 50 Ω so that everything is matched. Television coax uses 75 Ω. Matching there has a second reason too (avoiding reflections in long cables), which you will meet later.

## Build It

`code/main.py` sweeps the load across five decades with our simulator, finds the maximum, compares it with the formulas and plots the result.

### Step 1: the source and a load

The lab's source: 12 V, 3 kΩ on top, 6 kΩ on the bottom, the port across the 6 kΩ.

```python
def source_with_load(load_ohms):
    circuit = Circuit()
    circuit.voltage_source("V1", "a", "0", 12.0)
    circuit.resistor("R1", "a", "p", 3000)
    circuit.resistor("R2", "p", "0", 6000)
    circuit.resistor("RL", "p", "0", load_ohms)
    return circuit
```

### Step 2: sweep and record

`np.logspace(2, 6, 401)` makes 401 load values spaced evenly on a logarithmic scale from 100 Ω to 1 MΩ, so each decade gets the same number of points.

```python
loads = np.logspace(2, 6, 401)
powers = np.array([source_with_load(r).dc().p("RL") for r in loads])
best = loads[np.argmax(powers)]
```

### Step 3: efficiency, honestly

Efficiency of the *real* divider is the load power divided by the battery's power (the battery also feeds R2, which is part of the "source"). For the Thevenin equivalent, it is `RL / (RL + Rth)`. The code prints both: they differ, because the equivalent matches only at the port (Lesson 06), and the real divider wastes extra power in R2 even with no load at all.

### Step 4: the plot

The script saves `out.png` next to itself: load power and efficiency against load resistance on a logarithmic axis, with the maximum marked.

Run it:

```
uv run python phases/05-circuit-analysis-and-our-simulator/07-maximum-power-transfer/code/main.py
```

## Use It

- **Radios and antennas.** A receiving antenna is a source with a tiny `Vth` (microvolts) and an internal resistance near 50 Ω (or 73 Ω for a simple half-wave dipole in free space). Receivers present a 50 Ω input so they extract the most power from the antenna.
- **Audio, old and new.** Valve (tube) amplifiers had high output resistance and drove 8 Ω speakers through an output transformer that made the speaker "look" matched. Modern transistor amplifiers have output resistances of a fraction of an ohm and drive the speaker *un*matched (`RL >> Rth`), for efficiency and to control the speaker cone tightly.
- **Solar panels and MPPT.** A solar panel's I-V curve is curved, but at each light level there is one operating point of maximum power. Chargers include an "MPPT" (maximum power point tracking) controller that keeps adjusting the effective load to stay at that point.
- **Energy harvesting.** Tiny piezoelectric or thermoelectric harvesters (microwatts) are matched to their load because every microwatt counts and the energy source is free.
- **Batteries: do not match!** A phone battery with 0.1 Ω internal resistance "matched" to a 0.1 Ω load would deliver huge current, burn half its energy inside itself, and overheat dangerously. Battery-powered devices always present loads far larger than the battery's `Rth`.

## Try It in the Lab

The lab source is a 12 V battery with 3 kΩ on top and 6 kΩ at the bottom; the load slot sits across the 6 kΩ. Four resistors are offered. The goal: get at least 7.5 mW into the load.

Think before you try:

- What are `Vth` and `Rth` of this source?
- What is the maximum possible load power? Is 7.5 mW close to it?
- Two of the offered parts give exactly the same power. Which two, and why? (Look at the symmetry in the table above.)

## Common Mistakes

- **Thinking a smaller load always takes more power.** It takes more current, but less voltage. Power peaks in between.
- **Matching to the wrong resistance.** `RL` must equal the source's *Thevenin* resistance as seen from the port, not any single resistor inside.
- **Confusing maximum power with maximum efficiency.** At the match the efficiency is only 50 %. For power delivery systems that is terrible.
- **Changing the source instead of the load.** The theorem says: for a *fixed* source, pick the load. If you can change the source, the best is `Rth = 0`, which gives the most power *and* 100 % efficiency.
- **Forgetting power is in watts, not volts.** A matched load gets only half of `Vth`, and some people stop there. Compute `V²/R` to get power.

## Exercises

1. A source has `Vth = 10 V` and `Rth = 50 Ω`. What load gives maximum power, and how much power is it? (Answer: 50 Ω, 0.5 W.)
2. For the same source, compute the load power and efficiency for `RL = 25 Ω`, `100 Ω` and `500 Ω`.
3. A microphone has `Rth = 600 Ω` and produces `Vth = 10 mV`. What is the most power it can deliver? Express it in microwatts. (Answer: about 0.042 µW.)
4. Show from the formula that `RL = k × Rth` and `RL = Rth / k` always give the same load power, for any `k`. (Hint: substitute and simplify.)
5. Harder: a 12 V car battery has `Rth = 0.02 Ω`. Compute the "maximum power" it could deliver into a matched load, and the current. Then explain in two sentences why nobody ever does that, using efficiency and heat.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Maximum power transfer | "Match the load" | For a fixed source, load power `Vth² RL / (Rth + RL)²` peaks at `RL = Rth` |
| Maximum power | "What the source can give" | `Vth² / (4 Rth)`, delivered only into a matched load |
| Efficiency | "How much is wasted" | `RL / (RL + Rth)` for a Thevenin source; 50 % at the match |
| Matching | "50 ohms everywhere" | Making a load (or cable, or input) present the same resistance as the source |
| Load line | "The source's limits" | All the (V, I) pairs a source can produce, a straight line for a linear source |
| MPPT | "The solar thing" | A controller that keeps adjusting a solar panel's load to sit at its maximum power point |

## Further Reading

- [All About Circuits, Vol. I, "Maximum Power Transfer Theorem"](https://www.allaboutcircuits.com/textbook/direct-current/chpt-10/maximum-power-transfer-theorem/): a short free chapter with the efficiency warning.
- *The Art of Electronics*, Horowitz and Hill, 3rd edition, Chapter 1: source and load impedances, and why most electronics is deliberately *not* matched.
- *Practical Electronics for Inventors*, Scherz and Monk, 4th edition, Chapter 2: the theorem with practical examples.
- [Wikipedia, "Maximum power transfer theorem"](https://en.wikipedia.org/wiki/Maximum_power_transfer_theorem): the history (Jacobi), the efficiency debate and the AC (conjugate matching) form.
