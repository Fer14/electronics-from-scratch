# Phase 00: Words and Units

> Before you can understand a circuit, you have to be able to read the sentence that describes it.

Electronics has its own language. People talk about "five volts on the rail", "a 4.7 k pull-up", "twenty milliamps through the LED", or "don't short the battery", and every one of those phrases hides a word, a unit and a habit of mind. This phase teaches that language from nothing. You will learn what electronics actually is and what circuits are for. You will meet the core vocabulary (charge, voltage, current, resistance, power, source, load, node, ground, open, short), each with an everyday picture and a note on where that picture fails. Then come the units and prefixes that turn "0.0047 farads" into "4.7 mF", scientific notation and orders of magnitude so that a nanoamp and a kiloamp both feel like real quantities, how to read a schematic drawing, and the safety rules that keep you and your parts alive. It comes first because every later lesson uses these words without stopping to explain them again.

**Prerequisites:** None. This is where the course starts. If you can use a calculator and run a Python script, you are ready.

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [What Electronics Is](01-what-electronics-is/) | Electricity vs electronics, what circuits do with energy and information, a short history from amber to the integrated circuit, and how this course is built |
| 02 | [The Vocabulary](02-the-vocabulary/) | Charge, voltage, current, resistance, power, source, load, node, ground, open and short, each with a plain meaning, an everyday picture and that picture's limits |
| 03 | [Units and SI Prefixes](03-units-and-si-prefixes/) | Volts, amps, ohms, watts, joules, coulombs and friends, prefixes from pico to giga, conversions, unit sanity checks, mAh and Wh |
| 04 | [Scientific Notation and Orders of Magnitude](04-scientific-notation-and-orders-of-magnitude/) | Powers of ten, engineering notation, the range of real currents, voltages and resistances, and quick Fermi estimates |
| 05 | [Reading a Schematic](05-reading-a-schematic/) | Schematic symbols, junctions vs crossings, ground symbols, net names, and turning a drawing into a list of parts and connections |
| 06 | [Safety First](06-safety-first/) | Why current hurts and voltage pushes it, body resistance, danger thresholds, battery shorts, charged capacitors, heat, and the rules for this course |

**Labs in this phase:** none. The interactive lab starts in Phase 02, once you know enough words to follow a circuit.

Run the first lesson:

```
uv run python phases/00-words-and-units/01-what-electronics-is/code/main.py
```
