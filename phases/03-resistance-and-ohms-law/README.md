# Phase 03: Resistance and Ohm's Law

> Resistance is how hard a material makes charge work to get through. Once you can put a number on it, you can predict the current, the heat and the failure of every simple circuit.

In Phase 02 you built your first circuits and saw that "more stuff in the way" means "less current". This phase turns that intuition into numbers. You start with what resistance physically is (electrons bumping into atoms), see how a wire's material, length and thickness set its resistance, and arrive at Ohm's law, the single most used equation in electronics. Then you meet the real parts: how to read a resistor's color bands, how much heat it makes, what its tolerance and ratings mean, and finally where Ohm's law stops working (lamps, thermistors, diodes). It comes here because every later phase, from Kirchhoff's laws to transistors and chips, assumes you can look at a resistor and know its current, its voltage and its power without thinking twice.

**Prerequisites:** Phase 00 (Words and Units), Phase 01 (The Physics Underneath) and Phase 02 (Your First Circuits).

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [What Resistance Is](01-what-resistance-is/) | Why materials resist current: electrons colliding with atoms, and what an ohm is |
| 02 | [Resistivity and Wires](02-resistivity-and-wires/) | `R = ρ L / A`: how material, length and thickness set resistance, wire gauges and voltage drop in cables |
| 03 | [Ohm's Law](03-ohms-law/) | `V = I * R` in its three forms, where it comes from, and solving single-resistor circuits |
| 04 | [Resistors and Color Codes](04-resistors-and-color-codes/) | How resistors are made, reading 4- and 5-band color codes and SMD markings, and the E6/E12/E24 standard values |
| 05 | [Power and Heat](05-power-and-heat/) | `P = V * I = I^2 * R = V^2 / R`, energy and kWh, Joule heating, temperature rise from thermal resistance |
| 06 | [Tolerances and Ratings](06-tolerances-and-ratings/) | E12 values, tolerance ranges, worst-case analysis, power derating, voltage rating and temperature coefficient |
| 07 | [When Ohm's Law Fails](07-when-ohms-law-fails/) | Ohmic versus nonlinear parts: lamp filaments and inrush, thermistors, diodes, static and dynamic resistance |

## Labs in this phase

- **02 · Cut the hot wire to the right length** — size a nichrome foam-cutter wire from its resistance per length
- **03 · Nine milliamps from nine volts** — pick one resistor for a target current with Ohm's law
- **04 · Find the yellow-violet-red resistor** — choose the part by its color code to get about 2.5 mA from 12 V
- **05 · Warm the bottle, don't cook it** — choose a heating resistor that dissipates between 1 W and 2 W from 12 V
- **06 · Keep the power bank awake** — meet a minimum current while staying under a derated power limit

Run the first lesson:

```
uv run python phases/03-resistance-and-ohms-law/01-what-resistance-is/code/main.py
```
