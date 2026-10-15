# Phase 10: Filters and Resonance

> Every signal is a chord of sine waves. Filters choose which notes to keep, and resonance lets an inductor and a capacitor pick a single note out of thousands.

With the impedances and phasors of Phase 09, a resistor, a capacitor and an inductor stop being three separate parts and become frequency-dependent voltage dividers. This phase uses them to separate wanted signals from unwanted ones. You start by seeing signals as sums of sine waves and filters as circuits that treat each frequency differently, then derive the RC low-pass and high-pass, learn the decibel and Bode-plot language every datasheet uses, build RL filters and a loudspeaker crossover, and meet resonance: the frequency where an inductor and a capacitor cancel, giving sharp band-pass filters, notches that kill mains hum, voltage magnification and ringing, all summarised by the quality factor Q. The phase ends by opening the last black box we have been using: you build the simulator's AC analysis (complex modified nodal analysis) from scratch and check it against `sim`. It comes after alternating current because it is built on impedance, and before semiconductors because the amplifiers and op-amp filters of Phases 12 and 13 are designed and judged with these same Bode plots.

**Prerequisites:** Phase 05 (Circuit Analysis and Our Simulator), Phase 07 (Capacitors), Phase 08 (Magnetism and Inductors), Phase 09 (Alternating Current)

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [What a Filter Does](01-what-a-filter-does/) | Signals as sums of sines, the four filter shapes, the RC divider, a square wave losing its harmonics |
| 02 | [RC Low-Pass and High-Pass](02-rc-low-pass-and-high-pass/) | H = 1 / (1 + j f/fc), magnitude and phase, design with standard values, loading, rise time |
| 03 | [Decibels and Bode Plots](03-decibels-and-bode-plots/) | Logarithms from zero, dB and dBm, straight-line Bode plots, stacking buffered stages |
| 04 | [RL Filters](04-rl-filters/) | fc = R / (2 pi L), RC/RL duality, a two-way speaker crossover, DCR, supply-line chokes |
| 05 | [RLC Resonance](05-rlc-resonance/) | f0 = 1 / (2 pi sqrt(L C)), series and parallel resonance, voltage magnification, ringing, tuning |
| 06 | [Band-Pass and Band-Stop](06-band-pass-and-band-stop/) | Wide and narrow band-pass filters, LC trap and twin-T notches, removing 50 Hz hum |
| 07 | [Quality Factor](07-quality-factor/) | Q as f0 / BW, as sqrt(L/C) / R and as an energy ratio; ringing for Q cycles; selectivity trade-offs |
| 08 | [AC Analysis in Our Simulator](08-ac-analysis-in-our-simulator/) | Complex MNA stamps, a frequency-sweep solver built from scratch, compared with `sim` and with a transient run |

Labs in this phase:

- **01 Keep the bass, drop the hiss** (ac): find the part that turns a resistor into a low-pass
- **02 Put the cutoff near 1 kHz** (ac): pick R for a target cutoff from standard values
- **03 Attenuate by exactly 20 dB** (ac): build a flat -20 dB divider
- **04 Keep the treble out of the woofer** (ac): choose the crossover coil for an 8 ohm woofer
- **05 Tune the circuit to the 1 kHz tone** (ac): choose C to put the resonance on the tone
- **06 Kill the 50 Hz hum** (ac): tune an LC trap to the mains frequency
- **07 Sharp enough, but not too sharp** (ac): choose R for the right Q

Run the first lesson:

```bash
uv run python phases/10-filters-and-resonance/01-what-a-filter-does/code/main.py
```
