# Phase 11: Semiconductors and Diodes

> Everything so far obeyed straight lines. A pinch of the right impurity in silicon gives you a one-way street for current, and from then on electronics is exponential.

Up to now every part had a fixed personality: resistors obey Ohm's law, capacitors and inductors store energy, and doubling the voltage doubles the current. This phase introduces the first part that refuses to be linear, and the material that makes it possible. We start inside silicon with an intuitive picture of energy bands as "allowed shelves" for electrons, and see why silicon conducts a little, why heat changes that dramatically, and why chips are made of it. Then we add a few foreign atoms (doping) to create two kinds of silicon: n-type, where free electrons carry the current, and p-type, where the carriers are holes, empty seats that drift around like positive charges. Join the two and a depletion region and a built-in hill form by themselves: a pn junction, the diode. We derive the Shockley diode equation from the hill picture, and then do what every circuit simulator does with it: solve nonlinear circuits by building Newton-Raphson from scratch, with companion models and junction limiting, and check it against our simulator. The last three lessons put diodes to work: rectifiers that turn AC into DC, LEDs whose colour is their band gap, and zener diodes that hold a voltage steady. This phase comes here because transistors (Phase 12) are two junctions back to back, and op-amps (Phase 13) are built from transistors.

**Prerequisites:** Phase 01 (The Physics Underneath), Phase 03 (Resistance and Ohm's Law), Phase 05 (Circuit Analysis and Our Simulator), Phase 07 (Capacitors) and Phase 09 (Alternating Current).

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [Why Silicon](01-why-silicon/) | Energy bands as allowed shelves, the band gap, thermal energy kT, intrinsic carriers, and why silicon beat germanium and glass |
| 02 | [Doping: n-type and p-type](02-doping-n-and-p/) | Donors and acceptors, holes as moving vacancies, the mass-action law, resistivity versus doping, and temperature stability |
| 03 | [The pn Junction](03-the-pn-junction/) | Diffusion, the depletion region, the built-in potential, forward and reverse bias, junction capacitance, and a one-way street in the simulator |
| 04 | [The Diode Equation](04-the-diode-equation/) | The Shockley equation, 60 mV per decade, why "0.7 V", three diode models, and the -2 mV/°C temperature drift |
| 05 | [Solving Nonlinear Circuits](05-solving-nonlinear-circuits/) | Load lines, fixed-point iteration, bisection, Newton-Raphson with junction hold-back, companion models and MNA by hand, checked against `sim` |
| 06 | [Rectifiers](06-rectifiers/) | Half-wave and bridge rectifiers, reservoir capacitors, ripple ΔV ≈ I/(fC), diode current pulses and reverse voltage |
| 07 | [LEDs](07-leds/) | Light from recombination, colour from the band gap (E = 1240/λ), the series resistor, series strings and current hogging |
| 08 | [Zener Diodes](08-zener-diodes/) | Tunnelling and avalanche breakdown, the shunt regulator, worst-case design, load and line regulation |

## Labs in this phase

- [04 · The Diode Equation](04-the-diode-equation/lab/task.json): "Bias a diode at one milliamp"
- [05 · Solving Nonlinear Circuits](05-solving-nonlinear-circuits/lab/task.json): "A two-diode voltage reference"
- [06 · Rectifiers](06-rectifiers/lab/task.json): "Smooth the bumps" (transient: choose the reservoir capacitor)
- [07 · LEDs](07-leds/lab/task.json): "A green power light for a USB gadget"
- [08 · Zener Diodes](08-zener-diodes/lab/task.json): "A 5 V rail from a 12 V battery"

Run the first lesson:

```
uv run python phases/11-semiconductors-and-diodes/01-why-silicon/code/main.py
```
