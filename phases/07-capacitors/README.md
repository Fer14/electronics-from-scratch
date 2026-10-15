# Phase 07: Capacitors

> The first part with memory: a capacitor's voltage today depends on every bit of current it received before.

Until now every circuit you met lived only in the present: change the battery and every current changed at once. A capacitor, two conductors separated by an insulator, changes that. It holds separated charge, so its voltage cannot jump; it fills fast while empty and slowly as it gets full, along an exponential curve whose speed is set by one number, the time constant R x C. This phase starts from what happens to the electrons on the plates, builds up capacitance from plate size and material, derives the charging and discharging curves step by step, shows how to combine capacitors and how much energy they store, and then looks at the real parts on a shop shelf with their leakage, series resistance and drifting values. It ends with you writing your own transient simulator, the time-stepping engine behind every `circuit.transient(...)` call in this course. It comes right after Phase 06 because you now have the circuit-analysis tools and the simulator to watch time unfold, and it prepares Phase 08 (inductors), Phase 09 (AC) and Phase 10 (filters), which all reuse the same ideas.

**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Phase 04 (Kirchhoff's Laws), Phase 05 (Circuit Analysis and Our Simulator), Phase 06 (Sources, Batteries and Measurement)

| # | Lesson | What you learn |
|---|---|---|
| 01 | [Storing Charge](01-storing-charge/) | What moves inside a capacitor, why the current stops when it is full, Q = C x V found by simulation |
| 02 | [Capacitance](02-capacitance/) | C = eps0 eps_r A / d, dielectrics and breakdown, measuring C with a constant current, reading markings |
| 03 | [Charging and Discharging](03-charging-and-discharging/) | Where the exponential comes from, step by step by hand, then formulas checked against a square-wave simulation |
| 04 | [The Time Constant](04-the-time-constant/) | tau = RC, the 63% / 5 tau table, time to a threshold, rise time, designing a reset delay |
| 05 | [Capacitors in Series and Parallel](05-capacitors-in-series-and-parallel/) | Deriving both rules from Q = C x V, voltage sharing in series, measuring combinations by timing |
| 06 | [Energy in the Electric Field](06-energy-in-the-electric-field/) | E = 1/2 C V^2, why charging always wastes half, hold-up time after a power cut |
| 07 | [Real Capacitors](07-real-capacitors/) | Capacitor families, ESR, leakage, DC-bias derating and tolerance, modelled with ideal parts |
| 08 | [Transient Simulation from Scratch](08-transient-simulation-from-scratch/) | Companion models, backward Euler and trapezoidal rule on top of MNA, compared with `sim` |

## Labs in this phase

- 02 · Find the 1 V ramp: pick the capacitor that a 1 mA current source charges at 1 V per millisecond.
- 03 · Soften the edges, keep the levels: pick the resistor that rounds a square wave but still reaches both levels.
- 04 · Release reset at the right moment: make a reset pin cross 2.5 V between 0.6 ms and 0.8 ms.
- 05 · Build the missing capacitor: fill two parallel pads to make about 3.2 uF from standard values.
- 06 · Ride through the power cut: choose a hold-up capacitor that keeps a load above 3 V for 10 ms.

Run the first lesson:

```bash
uv run python phases/07-capacitors/01-storing-charge/code/main.py
```
