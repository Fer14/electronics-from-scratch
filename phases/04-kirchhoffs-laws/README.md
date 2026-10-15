# Phase 04: Kirchhoff's Laws

> Charge is never lost at a junction and energy is never lost around a loop. Two bookkeeping rules, and every resistor circuit gives up its secrets.

Phase 03 gave you Ohm's law, which tells you what happens inside one resistor. Real circuits have many parts joined together, and to understand them you need rules for the joins. This phase starts by naming the pieces of any circuit (nodes, branches, loops), then shows where Kirchhoff's two laws come from physically: the current law is conservation of charge (whatever flows into a junction must flow out), and the voltage law is conservation of energy (a charge that goes around a loop and returns to where it started has gained and lost exactly the same energy). With these two laws plus Ohm's law you derive, rather than memorize, the rules for series and parallel resistors and the four small circuits that appear in nearly every schematic: the voltage divider, the current divider, the loaded divider, and the Wheatstone bridge. Everything is still solved by hand with plain Python; Phase 05 turns the same laws into a systematic method and into our own circuit simulator.

**Prerequisites:** Phase 02 (Your First Circuits) and Phase 03 (Resistance and Ohm's Law).

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [Nodes, Branches and Loops](01-nodes-branches-and-loops/) | The vocabulary for describing any circuit's shape: find the nodes, count the branches, trace the loops |
| 02 | [Kirchhoff's Current Law](02-kirchhoffs-current-law/) | Why the currents into a node add up to zero, and how to use it to find a missing current |
| 03 | [Kirchhoff's Voltage Law](03-kirchhoffs-voltage-law/) | Why the voltages around a loop add up to zero, with sign conventions you can trust |
| 04 | [Series and Parallel Resistors](04-series-and-parallel-resistors/) | The series and parallel formulas derived from KCL, KVL and Ohm's law, and how to collapse a network step by step |
| 05 | [The Voltage Divider](05-the-voltage-divider/) | Vout = Vin x R2/(R1+R2), why only the ratio matters, loading, potentiometers, and picking E12 values |
| 06 | [The Current Divider](06-the-current-divider/) | How a current splits between parallel branches, the conductance view, and meter shunts |
| 07 | [The Wheatstone Bridge](07-the-wheatstone-bridge/) | Two dividers compared: the balance condition, null measurements, strain gauges and RTDs |

## Labs in this phase

- [02 · Kirchhoff's Current Law](02-kirchhoffs-current-law/lab/task.json): "Make the meter read 15 mA"
- [03 · Kirchhoff's Voltage Law](03-kirchhoffs-voltage-law/lab/task.json): "Give the sensor its 3 volts"
- [04 · Series and Parallel Resistors](04-series-and-parallel-resistors/lab/task.json): "Make the battery see 1.5 kilohms"
- [05 · The Voltage Divider](05-the-voltage-divider/lab/task.json): "Bring 5 V down to 3.3 V"
- [06 · The Current Divider](06-the-current-divider/lab/task.json): "Protect the meter with a shunt"
- [07 · The Wheatstone Bridge](07-the-wheatstone-bridge/lab/task.json): "Balance the bridge"

Run the first lesson:

```
uv run python phases/04-kirchhoffs-laws/01-nodes-branches-and-loops/code/main.py
```
