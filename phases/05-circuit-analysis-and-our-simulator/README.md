# Phase 05: Circuit Analysis and Our Simulator

> Stop solving circuits by cleverness. Write down the equations the same way every time, and let a machine do the arithmetic.

In Phase 04 you learned the two laws that hold every circuit together: currents meeting at a point must balance (Kirchhoff's current law) and voltages around a closed path must add up to zero (Kirchhoff's voltage law). With those and Ohm's law you could already solve dividers, bridges and series-parallel networks, but each new drawing needed a new trick. This phase replaces tricks with *methods*. You will learn nodal analysis (unknowns are node voltages), mesh analysis (unknowns are loop currents) and, the star of the phase, modified nodal analysis: the recipe every circuit simulator in the world uses, which you will build yourself from scratch in about a hundred lines of Python. From that lesson on, the course's own simulator (`sim/`) is our calculator, and we use it to explore the big ideas that make circuits understandable: superposition (one source at a time), Thevenin and Norton equivalents (any messy network seen from two terminals is just a battery and a resistor), maximum power transfer, and dependent sources, the building block of every transistor and amplifier model you will meet later. It comes here because you now know enough physics and enough laws to write the equations, and every later phase (capacitors, AC, diodes, transistors, op-amps) relies on the simulator you understand in this phase.

**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Phase 04 (Kirchhoff's Laws). Some comfort with solving two equations with two unknowns helps; Lesson 01 reviews it.

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [Systematic Analysis](01-systematic-analysis/) | Why tricks stop working, counting unknowns and equations, systems of linear equations, matrices as tidy bookkeeping, and the first run of our simulator |
| 02 | [Nodal Analysis](02-nodal-analysis/) | Choosing ground, node voltages as the unknowns, writing KCL with Ohm's law at every node, the conductance matrix, and grounded voltage sources |
| 03 | [Mesh Analysis](03-mesh-analysis/) | Loop currents as the unknowns, KVL around every window of the drawing, the resistance matrix, and what to do with current sources |
| 04 | [Modified Nodal Analysis from Scratch](04-modified-nodal-analysis-from-scratch/) | Element stamps, the extra unknown for every voltage source, a complete solver in NumPy built from a netlist, checked against `sim` |
| 05 | [Superposition](05-superposition/) | Turning sources off (shorts and opens), adding the effects of each source, and why power does not add |
| 06 | [Thevenin and Norton](06-thevenin-and-norton/) | Replacing any linear network by one source and one resistor, three ways to find them, and source transformations |
| 07 | [Maximum Power Transfer](07-maximum-power-transfer/) | Why the load that gets the most power equals the source's internal resistance, why efficiency is then only 50 %, and when you want that |
| 08 | [Dependent Sources](08-dependent-sources/) | Sources controlled by another voltage, the VCVS and VCCS, amplifier models, feedback, and Thevenin with a test source |

**Labs in this phase** (all `dc`):

- 01 · Find the missing resistor that puts node b at 7 V in a two-source network
- 02 · Set a node voltage in a circuit driven by a current source
- 03 · Balance a two-battery, two-loop circuit so the right current flows
- 04 · Lift a node above its neighbour with a floating battery
- 05 · Combine a battery and a current source to land on 4 V
- 06 · Use the Thevenin equivalent to pick the load that gets exactly 3 V
- 07 · Squeeze the most power out of a source
- 08 · Bias a transistor-like stage (a voltage-controlled current source) at mid-supply

Run the first lesson:

```
uv run python phases/05-circuit-analysis-and-our-simulator/01-systematic-analysis/code/main.py
```
