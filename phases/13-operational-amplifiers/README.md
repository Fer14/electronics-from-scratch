# Phase 13: Operational Amplifiers

> An op-amp is an amplifier with an absurd gain and two inputs. Wrap it in negative feedback and it does exactly what two resistors tell it to.

Phase 12 built amplifiers from single transistors and found them fiddly: their gain depended on beta, on temperature and on the bias current. The operational amplifier packages a whole multi-transistor amplifier (a differential pair, mirror loads, a gain stage and an output stage) into one part whose gain is so large that, with negative feedback, it no longer matters. This phase starts from the ideal op-amp and its two golden rules (no input current; with negative feedback the inputs are equal), and shows that the second rule is a consequence of feedback, not a property of the chip. Without feedback the op-amp is a comparator, and with a little positive feedback a Schmitt trigger that ignores noise. With negative feedback come the workhorses: inverting and non-inverting amplifiers set by resistor ratios, summers and digital-to-analogue converters built on the virtual ground, difference amplifiers that pull a millivolt signal off a large common voltage, integrators and differentiators built with capacitors, and active filters that are flat to their cutoff without inductors. The last lesson builds a realistic op-amp from simulator parts and measures what the golden rules leave out: gain-bandwidth, slew rate, offset voltage, bias current and output swing. Every circuit is derived by hand and checked with our simulator's DC, AC and transient analyses. Digital logic (Phase 14) takes the comparator's yes/no decisions and runs with them.

**Prerequisites:** Phase 12 (Transistors); Phase 04 (Kirchhoff's Laws); Phase 07 (Capacitors); Phase 10 (Filters and Resonance).

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [The Ideal Op-Amp](01-the-ideal-op-amp/) | Open-loop gain and saturation, the follower's A/(1+A), the two golden rules, buffering a divider against loading |
| 02 | [The Comparator](02-the-comparator/) | Thresholds from dividers, "too high" and "too low" alarms, chatter from noise, Schmitt triggers and hysteresis |
| 03 | [Inverting and Non-Inverting Amplifiers](03-inverting-and-non-inverting-amplifiers/) | Gains 1 + R_F/R_G and -R_F/R_I, the virtual ground, input resistance, finite-gain error A/(1+AB), saturation |
| 04 | [Summers and Difference Amplifiers](04-summers-and-difference-amplifiers/) | Mixers and weighted sums, a 4-bit DAC, the four-resistor difference amp, CMRR and resistor matching, bridges and in-amps |
| 05 | [Integrators and Differentiators](05-integrators-and-differentiators/) | Constant-current ramps, square to triangle and back, drift and the leak resistor, +/-20 dB/decade, taming the differentiator |
| 06 | [Active Filters](06-active-filters/) | First-order active low-pass with gain, why passive RC-RC droops, Sallen-Key design for f0 and Q, Butterworth, high-pass by swapping R and C |
| 07 | [Real Op-Amp Limits](07-real-op-amp-limits/) | A macro-model from simulator parts, gain-bandwidth, slew rate and full-power bandwidth, offset, bias current, output swing, choosing a part |

## Labs in this phase

- [01 · The Ideal Op-Amp](01-the-ideal-op-amp/lab/task.json): "Buffer the divider"
- [02 · The Comparator](02-the-comparator/lab/task.json): "A frost alarm at 2.0 V" (transient: comparator threshold)
- [03 · Inverting and Non-Inverting Amplifiers](03-inverting-and-non-inverting-amplifiers/lab/task.json): "An op-amp amplifier with a gain of 10"
- [04 · Summers and Difference Amplifiers](04-summers-and-difference-amplifiers/lab/task.json): "Measure a 0.2 V difference sitting on 5 V"
- [05 · Integrators and Differentiators](05-integrators-and-differentiators/lab/task.json): "A ramp that reaches 5 V in about a millisecond" (transient)
- [06 · Active Filters](06-active-filters/lab/task.json): "A flat 1 kHz low-pass filter" (ac)
- [07 · Real Op-Amp Limits](07-real-op-amp-limits/lab/task.json): "Enough gain, enough bandwidth" (ac, macro-model op-amp)

Run the first lesson:

```
uv run python phases/13-operational-amplifiers/01-the-ideal-op-amp/code/main.py
```
