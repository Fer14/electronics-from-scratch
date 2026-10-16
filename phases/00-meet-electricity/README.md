# Phase 00: Meet Electricity

> Before any formula, get to know the thing itself: a loop, a push, a flow, and the energy it carries.

This is where the course begins, and it begins from nothing. You do not need to know any physics or any maths, and you do not need to buy anything. Electricity is all around you, but most of us have never been told what it actually is, so this phase introduces it slowly and in plain words. You will see what electronics is and where it came from, from rubbed amber to the chip. You will learn what a circuit is (a loop that goes out and comes back) and build everything else on top of that one idea: the electrons that are already sitting in every wire, current as the flow of charge, voltage as the push (and ground as the zero we measure it from), and power as how fast energy is delivered. Every idea is defined in everyday language before any symbol or unit appears, and numbers are kept to a minimum; the only formula in the whole phase is watts = volts x amps. Then you will read your first schematic, naming every symbol next to the real object, and learn the few safety habits that keep you and your parts safe. Whenever a topic deserves a deeper look, the lesson tells you which later phase gives it. Phase 01 (The Physics Underneath) then opens the box and starts calculating.

**Prerequisites:** None. If you can run a Python script, you are ready.

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [What Electronics Is](01-what-electronics-is/) | Electricity everywhere around you, electricity (moving energy) versus electronics (control and information), a tour of a flashlight and a charger, and the history from amber to the chip |
| 02 | [What a Circuit Is](02-what-a-circuit-is/) | The closed loop, source and load, conductors and insulators, the open circuit, and a first warning about the short circuit |
| 03 | [Charge and Electrons](03-charge-and-electrons/) | Atoms, positive and negative charge, static electricity, the free electrons already in every wire, the coulomb as a big crowd, and the slow crowd with the fast push |
| 04 | [Current and Amperes](04-current-and-amperes/) | Current as charge passing a point each second, the ampere, the same current all round a loop, conventional current versus electron flow, DC and AC |
| 05 | [Voltage and Volts](05-voltage-and-volts/) | Voltage as the push and as height, the volt, voltage across two points, ground as the agreed zero and common return, and why ground is not earth |
| 06 | [Power and Watts](06-power-and-watts/) | Energy versus power, the watt, watts = volts x amps, the kilowatt-hour on your bill, where the energy goes, and a preview of resistance |
| 07 | [Your First Schematic](07-your-first-schematic/) | A schematic as a map, each symbol named next to the real object (the lamp is the circle with an X), the ground symbol, junctions and crossings, and the flashlight read wire by wire |
| 08 | [Safety First](08-safety-first/) | Why current hurts and voltage pushes it, why small batteries are safe to learn with, never touching mains, why shorts burn, and the rules of this simulation-first course |

**Labs in this phase:** [What a Circuit Is](02-what-a-circuit-is/) has the course's first lab task, "Close the loop": fill the gap so the lamp lights.

Run the first lesson:

```
uv run python phases/00-meet-electricity/01-what-electronics-is/code/main.py
```
