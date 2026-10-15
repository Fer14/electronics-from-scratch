# Phase 18: Power Electronics

> Every circuit runs on power that someone had to convert, and every conversion either wastes energy as heat or uses switches clever enough not to.

So far every circuit had a tidy, fixed supply. Real devices get their energy from batteries that sag, adapters that vary and car electrics that spike, and they must turn it into the exact voltages their chips need, drive motors that draw amps, and stay cool while doing it. This phase is about moving energy, not information. It starts with linear regulators (zener, emitter follower and op-amp feedback), where efficiency can never beat Vout / Vin. Then it shows why a perfect switch dissipates nothing, and uses ideal switches in our simulator to build and measure the two basic switching converters: the buck (Vout = D x Vin) and the boost (Vout = Vin / (1 - D)), with their ripple formulas, losses and start-up behaviour. It models a DC motor, mechanics included, as a circuit, and drives it forwards, backwards, braking and coasting with an H-bridge and PWM. It builds a lithium-ion cell model and charges it with the CC/CV method. And it ends where every power design ends: turning watts into temperatures with thermal resistances and heat capacities, simulated with the same circuit solver. It comes here because it needs inductors and capacitors (Phases 07-08), diodes and transistors (Phases 11-12), op-amps (Phase 13) and PWM from microcontrollers (Phase 17).

**Prerequisites:** Phase 17 (Microcontrollers), Lesson 03 (PWM); Phase 08 (Magnetism and Inductors); Phase 07 (Capacitors); Phase 11 (Semiconductors and Diodes), Lesson 08 (Zener Diodes); Phase 12 (Transistors); Phase 13 (Operational Amplifiers).

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [Linear Regulators](01-linear-regulators/) | Zener shunt regulator design, emitter-follower and op-amp feedback regulators in `sim`, load and line regulation, dropout, efficiency limited to Vout / Vin |
| 02 | [Switching Converters](02-switching-converters/) | Why an ideal switch dissipates nothing, chopping into a heater, RC versus LC smoothing (12% versus 100% efficient), the inductive kick and freewheel paths |
| 03 | [The Buck Converter](03-the-buck-converter/) | Volt-second balance and Vout = D x Vin, choosing L and C from ripple formulas, conduction losses, start-up overshoot, light load, all checked against ideal-switch simulations |
| 04 | [The Boost Converter](04-the-boost-converter/) | Vout = Vin / (1 - D), input current, inductor and output ripple, why winding resistance caps the real gain, start-up and why a boost cannot switch off |
| 05 | [Motors and the H-Bridge](05-motors-and-the-h-bridge/) | A DC motor (back-EMF, torque, inertia, friction) built in `sim` with controlled sources; stall current and speed; H-bridge states, shoot-through, brake vs coast; PWM speed control |
| 06 | [Batteries and Charging](06-batteries-and-charging/) | A lithium-ion cell model (OCV curve, internal resistance, polarization), discharge at different C-rates, CC/CV charging, round-trip efficiency, series-parallel packs |
| 07 | [Heat and Thermal Design](07-heat-and-thermal-design/) | Thermal Ohm's law, heatsink selection, thermal circuits simulated with `sim`, warm-up time constants, short pulses by superposition, MOSFET thermal runaway |

**Labs in this phase:**

- 01: choose the series resistor of a zener regulator so the output holds and nothing overheats
- 03: choose the duty cycle that makes a buck converter give 5 V from 12 V
- 05: set the four switches of an H-bridge to drive a motor forwards without shorting the battery
- 07: choose a heatsink in a thermal circuit so the junction and heatsink stay below their limits

Run the first lesson:

```
uv run python phases/18-power-electronics/01-linear-regulators/code/main.py
```
