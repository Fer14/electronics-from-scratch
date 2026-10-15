# Phase 12: Transistors

> A small signal on one terminal decides how much current flows between the other two. Use it fully on or off and you have a switch; use it half on and you have an amplifier.

Phase 11 gave us the pn junction: a one-way street for current. A transistor puts two junctions (or a junction and a capacitor) together so that one terminal controls the current between the other two, and that single idea is behind every computer and every amplifier. This phase starts with the idea itself, modelled as an ideal controlled current source, and then opens up the two great families. The bipolar junction transistor (BJT) works because its middle layer is so thin that carriers injected by the emitter fall into the collector before they can recombine; the MOSFET works because a voltage on an insulated gate pulls a conducting channel into existence. For each we build the practical switch: a 3.3 V microcontroller pin running an LED through a BJT, and a 12 V, 2 A motor through a logic-level MOSFET, with the flyback diode that keeps the transistor alive. Then we use transistors half on: a divider-biased common-emitter amplifier whose operating point survives a six-fold change in beta, the small-signal (hybrid-pi) model that turns a nonlinear transistor back into resistors and a controlled source, and the current mirror that copies one current into many. All of it is computed by hand first and checked with our simulator's DC, AC and transient analyses. Op-amps (Phase 13) are built from exactly these pieces.

**Prerequisites:** Phase 11 (Semiconductors and Diodes); Phase 05 (Circuit Analysis and Our Simulator), especially lessons 06 (Thevenin and Norton) and 08 (Dependent Sources); Phase 07 (Capacitors) and Phase 08 (Magnetism and Inductors); Phase 10 (Filters and Resonance), lessons 03 and 08.

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [The Transistor Idea](01-the-transistor-idea/) | Control path versus main path, the ideal valve as a VCCS, switch and amplifier modes, gain -g_m R_L, and a real NPN where microamps control milliamps |
| 02 | [The BJT](02-the-bjt/) | npn structure, injection-diffusion-collection, I_C = I_S e^(V_BE/V_T), beta and alpha, the four regions, output curves, setting I_C with a base resistor |
| 03 | [The BJT as a Switch](03-the-bjt-as-a-switch/) | Saturation and overdrive, base-resistor design from a GPIO pin, robustness to beta, and the inductive kick tamed by a flyback diode |
| 04 | [The MOSFET](04-the-mosfet/) | The gate as a capacitor, inversion and threshold, triode and saturation, the square law, the voltage-controlled resistor, PMOS |
| 05 | [The MOSFET as a Switch](05-the-mosfet-as-a-switch/) | R_DS(on), logic-level versus standard parts, the gate divider trap, switching speed and loss, avalanche energy without a flyback diode |
| 06 | [Amplifiers and Biasing](06-amplifiers-and-biasing/) | The operating point, fixed versus divider bias, Thevenin bias analysis, gain R_C/(R_E + r_e), bypassing, clipping |
| 07 | [Small-Signal Thinking](07-small-signal-thinking/) | Linearisation, g_m = I_C/V_T, r_pi and r_e, the hybrid-pi model built from linear parts, input resistance, distortion v/(4 V_T) |
| 08 | [Current Mirrors](08-current-mirrors/) | Diode-connected transistors, the beta error, compliance, area ratios, MOSFET mirrors and output resistance |

## Labs in this phase

- [02 · The BJT](02-the-bjt/lab/task.json): "Set the collector current with the base"
- [03 · The BJT as a Switch](03-the-bjt-as-a-switch/lab/task.json): "Let a 3.3 V pin switch a 20 mA LED"
- [05 · The MOSFET as a Switch](05-the-mosfet-as-a-switch/lab/task.json): "Run a 12 V motor from a 3.3 V pin"
- [06 · Amplifiers and Biasing](06-amplifiers-and-biasing/lab/task.json): "A common-emitter amplifier with a gain of 10" (ac)
- [08 · Current Mirrors](08-current-mirrors/lab/task.json): "Copy one milliamp"

Run the first lesson:

```
uv run python phases/12-transistors/01-the-transistor-idea/code/main.py
```
