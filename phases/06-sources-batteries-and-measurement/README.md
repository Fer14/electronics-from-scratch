# Phase 06: Sources, Batteries and Measurement

> Nothing is ideal: every source sags, every meter disturbs. Knowing by how much is what makes a measurement worth trusting.

Until now our batteries were perfect and our meters were invisible. In this phase both become real. You learn what an ideal voltage source and an ideal current source promise and why real ones need a resistor inside to be described honestly; how to catch that hidden internal resistance with two measurements; what the chemistry inside a battery does and why its capacity shrinks under heavy loads; how a multimeter turns one measuring core into voltmeter, ammeter and ohmmeter with a handful of resistors; why connecting a meter changes the very voltage it reads, and how to correct for it; how an oscilloscope draws a voltage against time; and how to use a bench power supply's two modes to protect what you build. It comes right after circuit analysis (Phase 05) because every idea here is a Thevenin model, a voltage divider or a current divider in disguise, and it comes before capacitors (Phase 07) because from now on you will measure what you build, and you need to know how far to trust the numbers.

**Prerequisites:** Phase 02 (Your First Circuits), Phase 03 (Resistance and Ohm's Law), Phase 04 (Kirchhoff's Laws), Phase 05 (Circuit Analysis and Our Simulator)

| # | Lesson | What you learn |
|---|---|---|
| 01 | [Ideal and Real Sources](01-ideal-and-real-sources/) | Ideal voltage and current sources, where they break, and the series/parallel resistor that makes them real |
| 02 | [Internal Resistance](02-internal-resistance/) | Measuring a source's hidden resistance, the power it wastes, and how cells combine in series and parallel |
| 03 | [How Batteries Work](03-how-batteries-work/) | Redox reactions split in two, cell voltages from electrode potentials, capacity, energy and simulated discharge curves |
| 04 | [Inside the Multimeter](04-inside-the-multimeter/) | Multipliers, shunts and ohmmeters around a moving-coil movement, and the divider, ADC and counts of a digital meter |
| 05 | [Loading and Measurement Error](05-loading-and-measurement-error/) | Predicting and correcting the error a voltmeter or ammeter adds, using the Thevenin view |
| 06 | [The Oscilloscope](06-the-oscilloscope/) | Divisions, triggers, automatic measurements, x10 probes and aliasing, with a text-mode scope on our simulator |
| 07 | [Lab Power Supplies](07-lab-power-supplies/) | Constant-voltage and constant-current modes, current limits, lead drop, remote sensing and split supplies |

## Labs in this phase

- **06-01 Catch the current before it leaks:** choose the load for a real (leaky) current source.
- **06-02 Radio on a coin cell:** find the load a high-resistance coin cell can drive while staying above 2.7 V.
- **06-04 Turn a needle into a 10 V voltmeter:** pick the multiplier resistor for a moving-coil movement.
- **06-05 Pick a voltmeter that doesn't lie:** choose a meter input resistance that keeps loading error under 1 %.
- **06-07 Don't lose the volts in the leads:** choose test leads so a half-ampere board still gets 4.9 V.

Run the first lesson:

```bash
uv run python phases/06-sources-batteries-and-measurement/01-ideal-and-real-sources/code/main.py
```
