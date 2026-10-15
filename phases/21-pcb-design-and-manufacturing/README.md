# Phase 21: PCB Design and Manufacturing

> A schematic says what is connected. A board says where, and "where" turns out to matter.

Until now every circuit lived on paper, in our simulator or on a breadboard. Real products put their parts on a printed circuit board: a sheet of fibreglass with copper "wires" etched onto it. This phase follows a design from schematic to working board. We build a tiny board-layout model in Python (parts, pads, nets, ratsnest length, a design rule checker) and put numbers on the questions a schematic never asks: how wide must a trace be for 2 A, where does the return current really flow, why does every chip need a capacitor next to it, why a pad on a ground plane will not solder, and how to find the fault when the board does not work. It comes here because it needs almost everything before it: Ohm's law and resistivity for traces, capacitors and inductors for decoupling, diodes and LEDs for the example boards, and the simulator to predict what every node should read.

**Prerequisites:** Phases 00-07 (basics, Ohm and Kirchhoff, our simulator, capacitors), Phase 08 (Magnetism and Inductors), Phase 11 (Semiconductors and Diodes); Phase 18 (Power Electronics), Lesson 07 (Heat and Thermal Design) helps for Lesson 06.

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [From Schematic to Board](01-from-schematic-to-board/) | Board layers, the design flow, netlists and footprints, ratsnest length with a minimum spanning tree |
| 02 | [Footprints and Traces](02-footprints-and-traces/) | Package sizes and pitches, trace resistance, IPC-2221 width for a current, voltage drop on a heater feed |
| 03 | [Ground Planes and Current Return](03-ground-planes-and-current-return/) | Return paths, shared ground errors, star grounds, loop inductance, supply droop and decoupling capacitors |
| 04 | [Design Rules](04-design-rules/) | Factory and voltage rules, a capsule-geometry design rule checker, decoupling as an electrical rule |
| 05 | [Fabrication](05-fabrication/) | Imaging, etching and plating; etch undercut, panelization, cost versus quantity, yield, vias in parallel |
| 06 | [Soldering and Assembly](06-soldering-and-assembly/) | Wetting and alloys, paste and stencils, reflow profiles, the thermal-electrical analogy, thermal reliefs |
| 07 | [Debugging a Board](07-debugging-a-board/) | Safe bring-up, golden values from simulation, shorts and opens, a fault dictionary that diagnoses a board |

Labs in this phase:

- 02 · Pick a trace wide enough for the heater (dc)
- 03 · Stop the heater from lying to the sensor (dc)
- 04 · Follow the decoupling rule (transient)
- 06 · Make the ground pad solderable (transient, thermal circuit)
- 07 · Repair the board (dc)

Run the first lesson:

```
uv run python phases/21-pcb-design-and-manufacturing/01-from-schematic-to-board/code/main.py
```
