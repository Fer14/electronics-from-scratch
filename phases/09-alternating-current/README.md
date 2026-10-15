# Phase 09: Alternating Current

> The wall socket pushes back and forth fifty times a second. Learn to describe that push with one complex number, and AC circuits become as easy as DC ones.

Until now almost every source in this course pushed in one direction: batteries and DC supplies. The electricity in your wall does something different: it reverses direction 100 or 120 times a second, following a smooth sine wave. This phase explains why the world chose alternating current (transformers, and the huge savings of sending power at high voltage), how to describe a sine wave by its amplitude, frequency and phase, and what "230 volts" really means (the RMS value, the DC voltage with the same heating effect). Then it builds the mathematical tool that makes AC circuits manageable: complex numbers, taught from zero, as arrows you can stretch and turn. With them, every sine wave becomes a phasor, every resistor, capacitor and inductor gets an impedance, and Ohm's law, series and parallel rules and the voltage divider work again, one frequency at a time. The phase ends with AC power: why volts times amps is not always watts, and how a capacitor fixes a motor's power factor. It comes here because it needs capacitors (Phase 07) and inductors (Phase 08), and because Phase 10 (filters and resonance) is built entirely on impedance.

**Prerequisites:** Phase 04 (Kirchhoff's Laws), Phase 05 (Circuit Analysis and Our Simulator), Phase 07 (Capacitors), Phase 08 (Magnetism and Inductors)

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [Why Alternating Current](01-why-alternating-current/) | DC vs AC, why line loss falls as 1 / V^2, why transformers need AC, the war of the currents, 50 vs 60 Hz |
| 02 | [Sine Waves, Frequency and Phase](02-sine-waves-frequency-and-phase/) | The sine wave as the shadow of a spinning arrow, amplitude, period, omega, radians, phase, lead and lag, measuring them from samples |
| 03 | [RMS Values](03-rms-values/) | Why the average is useless, root mean square step by step, V_peak / sqrt(2), RMS of other waveforms, true-RMS meters |
| 04 | [Complex Numbers for Circuits](04-complex-numbers-for-circuits/) | j as a quarter turn, the complex plane, rectangular and polar forms, the four operations, conjugate, Euler's formula, Python's complex type |
| 05 | [Phasors](05-phasors/) | A sine wave as one complex number, adding waves as arrows, derivative = multiply by j omega, I = j omega C V and V = j omega L I, a series RC circuit solved by hand |
| 06 | [Impedance](06-impedance/) | Z = V / I, Z_R, Z_C and Z_L, resistance and reactance, series and parallel impedances, the impedance divider, checking with the simulator's AC analysis |
| 07 | [AC Power and Power Factor](07-ac-power-and-power-factor/) | Instantaneous, real, reactive and apparent power, complex power S = V conj(I), power factor and its correction with a capacitor |

**Labs in this phase:**

- 03 RMS Values: *Same heat on DC* (dc) — pick a series resistor so a heater on a 12 V battery makes the same heat as on its 10 V peak AC supply.
- 05 Phasors: *Two voltages that add to more than the source* (ac) — choose the capacitor that shares a 1 kHz source equally with a 1 kOhm resistor.
- 06 Impedance: *Let 50 Hz through, stop 10 kHz* (ac) — choose a series inductor that passes mains power and cuts switching noise by 20 dB.
- 07 AC Power and Power Factor: *Fix the motor's power factor* (ac) — choose the correction capacitor that brings a motor's line current back in step with the voltage.

Run the first lesson:

```bash
uv run python phases/09-alternating-current/01-why-alternating-current/code/main.py
```
