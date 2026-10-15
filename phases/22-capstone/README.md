# Phase 22: Capstone

> Specify it, simulate it, lay it out, bring it up: one small device, everything you have learned.

The last phase builds one complete product from start to finish: a battery-powered night light. A photoresistor in a voltage divider tells a sleeping microcontroller how dark the room is; the microcontroller wakes once a second, averages its readings, decides with hysteresis, and dims a white LED through a transistor with PWM, compensating as the three AA batteries run down so that the light stays even for a month. Every lesson is one stage of a real hardware project: measurable requirements, an architecture with a power budget, the full schematic checked in our simulator, a time simulation of the circuit and its firmware through a whole night, a board laid out with the tools of Phase 21, a bring-up plan with a fault dictionary, and finally a verification matrix and a look at what comes next. Nothing here is new physics; the point is to use all of it together, with numbers, the way engineers do.

**Prerequisites:** The whole course, especially Phases 03-04 (Ohm, Kirchhoff, dividers), 05 (our simulator), 11-12 (LEDs and transistors), 17 (microcontrollers), 18-19 (power and sensors) and 21 (PCB design).

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [Requirements](01-requirements/) | Measurable requirements, light levels and the LDR model, thresholds with hysteresis, a first energy budget |
| 02 | [Architecture](02-architecture/) | Blocks and power tree, sleep and wake currents, the LED driver as the battery falls, alternatives compared |
| 03 | [Schematic](03-schematic/) | The full schematic and netlist, operating points across light and battery, sizing the base resistor, ratings |
| 04 | [Simulation](04-simulation/) | PWM in the transient simulator, firmware as a state machine, battery compensation, a whole night with headlights |
| 05 | [The Board](05-the-board/) | Placement and its checks, ratsnest and trace widths, copper in the simulation, BOM and board cost |
| 06 | [Bring-Up](06-bring-up/) | A safe bring-up plan, golden values, a fault dictionary with supply current, diagnosing the first boards |
| 07 | [What Comes Next](07-what-comes-next/) | The verification matrix, a measured improvement, version-2 ideas, where to go after this course |

Labs in this phase:

- 01 · Size the light sensor's divider (dc)
- 03 · Choose the transistor's base resistor (dc)
- 04 · Dim the night light with PWM (transient)
- 06 · Fix the dim night light (dc)

Run the first lesson:

```
uv run python phases/22-capstone/01-requirements/code/main.py
```
