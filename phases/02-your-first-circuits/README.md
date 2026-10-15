# Phase 02: Your First Circuits

> Electricity only does work when it has a complete path to travel and a way back home.

You now know the words (Phase 00) and the physics behind them (Phase 01). Now we put them together into real circuits, the kind you could build on a kitchen table with a battery, a few bulbs or LEDs, a switch and some wire. You will see why a circuit has to be a closed loop. You will learn what a battery does and what a load does with the energy, why an open switch stops everything while a short circuit is dangerous, and why two bulbs in series glow dimmer than two in parallel. We use the water analogy carefully, saying exactly where it stops working, and then move to real hardware: how a breadboard is wired inside and how to measure voltage, current and resistance with a multimeter without blowing its fuse. The goal is intuition before equations. Ohm's law and Kirchhoff's laws arrive properly in Phases 03 and 04, and this phase is what makes them feel obvious. This is also where the interactive lab begins. You drop parts into the slots on a board, press RUN, and the simulator tells you whether your circuit meets the goal.

**Prerequisites:** Phase 00 (Words and Units) and Phase 01 (The Physics Underneath), especially Lesson 04 (Energy, Potential and Voltage), Lesson 06 (Current as Moving Charge) and Lesson 07 (Energy and Power).

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [The Closed Loop](01-the-closed-loop/) | Why current needs a complete path, what physically happens when the loop closes, and why every charge comes back to the source |
| 02 | [Batteries and Loads](02-batteries-and-loads/) | Sources vs loads, the battery as a charge pump, bulbs, LEDs, motors and heaters as energy converters, polarity, and matching voltages |
| 03 | [Switches, Open and Short Circuits](03-switches-open-and-short-circuits/) | What a switch does, why an open circuit has full voltage and no current, why a short has huge current and no voltage, and how fuses protect you |
| 04 | [Series and Parallel Intuition](04-series-and-parallel-intuition/) | Bulbs in a chain vs side by side: brightness, what happens when one fails, how hard the battery works, fairy lights and house wiring |
| 05 | [The Water Analogy and Its Limits](05-the-water-analogy-and-its-limits/) | Pressure, flow and narrow pipes as voltage, current and resistance, and the places where the picture breaks |
| 06 | [The Breadboard](06-the-breadboard/) | How a breadboard's strips and rails connect inside, how to place parts, and how to spot the wiring mistakes that cause accidental shorts |
| 07 | [Measuring with a Multimeter](07-measuring-with-a-multimeter/) | Measuring voltage across, current in series and resistance with the power off, continuity, ranges, and protecting the meter's fuse |

**Labs in this phase:**
- [Close the loop and light the flashlight](01-the-closed-loop/) (`02-01-closed-loop`)
- [Match the bulb to the battery](02-batteries-and-loads/) (`02-02-match-the-bulb`)
- [Clip across the lamp without starting a fire](03-switches-open-and-short-circuits/) (`02-03-open-not-short`)
- [Two bulbs, both at full brightness](04-series-and-parallel-intuition/) (`02-04-parallel-bulbs`)
- [Push in the missing jumper wire](06-the-breadboard/) (`02-06-missing-jumper`)
- [Measure the bulb current without changing it](07-measuring-with-a-multimeter/) (`02-07-meter-in-series`)

Run the first lesson:

```
uv run python phases/02-your-first-circuits/01-the-closed-loop/code/main.py
```
