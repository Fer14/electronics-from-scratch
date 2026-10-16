# The Water Analogy and Its Limits

> Water in pipes is the best picture of a circuit anyone has found. Use it to think, then know exactly where it lies to you.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 01 (The Physics Underneath), especially Lesson 06 (Energy, Potential and Voltage) and Lesson 08 (Current as Moving Charge); Phase 02 (Your First Circuits), Lessons 01-04
**Time:** ~50 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| analogy | explaining something unfamiliar by comparing it to something familiar | "the heart is a pump" |
| pressure | how hard a fluid pushes on each square metre of whatever it touches | the push you feel when you cover the end of a running hose with your thumb |
| pascal (Pa) | the unit of pressure: one newton of force on one square metre | a sheet of paper lying on a table presses down with about 1 Pa |
| flow rate | how much water passes a point each second | litres per minute from a tap |
| pump | a machine that raises the pressure of water so it can be pushed around a loop | the pump in a fish-tank filter |
| hydraulic resistance | how hard a pipe makes it for water to get through | a thin drinking straw versus a wide one |
| viscosity | how "thick" or sticky a fluid is, how much it resists sliding past itself | honey has high viscosity, water low |
| drift speed | the slow average speed at which electrons creep along a wire | a crowded corridor where everyone shuffles forward a few centimetres |
| signal speed | how fast the *push* travels down a wire, which is close to the speed of light | the click you hear at the far end of a long line of touching marbles |

## Learning Objectives

- Map the four basic electrical quantities (voltage, current, resistance, power) onto a water system (pressure difference, flow rate, pipe resistance, pressure times flow) and explain why each pair matches.
- Use the water picture to predict what happens when you double the battery voltage, double the resistance, or put two loads in series or in parallel.
- List at least four places where the water picture gives a *wrong* answer, and say what really happens in the wire.
- Compute, with your own calculator, the drift speed of electrons in a copper wire and compare it with the speed at which a signal travels.

## The Problem

In the first four lessons of this phase you built closed loops, met batteries and loads, opened and shorted switches, and saw bulbs share a battery in series and in parallel. You did all of that with words like "push", "flow" and "path". Those words are borrowed from water, and that is no accident: water is something you have handled your whole life, while electrons are invisible, unbelievably small and move in ways no one can watch.

So almost every teacher, textbook and YouTube video reaches for pipes and tanks. The trouble is that each one stretches the analogy a little differently, and sooner or later you meet a question where the water answer is just wrong. Ask a beginner "if I cut a wire, does electricity pour out of the end?" and the water picture says yes. Ask "when I flick a light switch, how long until the electrons from the switch reach the bulb?" and the water picture gives an answer that is off by many hours.

This lesson does two jobs. First, it builds the water analogy carefully, quantity by quantity, with real numbers, so you have a reliable thinking tool for the next several phases. Second, it marks the edges of that tool in red, so that when you reach capacitors, magnets and fast signals you know to put the pipes down.

## The Physics

### What a water loop actually does

Picture a closed loop of pipe completely filled with water, with a small pump somewhere in it. The pump does not create water. It takes the water arriving at its inlet and pushes it out of its outlet at a higher pressure. Pressure is force per area: if water presses with 10 newtons on every square centimetre of the pipe wall, that is 10 N / 0.0001 m² = 100 000 Pa (100 kPa, roughly the pressure of the air around you).

Water flows from high pressure to low pressure, the same way a ball rolls downhill. So water leaves the pump's high-pressure outlet, travels round the loop, loses pressure as it rubs against the walls of a narrow section, and arrives back at the pump's low-pressure inlet. The pump lifts it up again. Round and round.

Three facts about that loop matter:

1. **The amount of water never changes.** Every litre that leaves the pump comes back. Water is not used up, it is only pushed.
2. **What the pump gives is energy.** Each litre leaves with more pressure than it came in with, and it spends that extra pressure on the way round, mostly as a tiny bit of heat from friction in the narrow pipe.
3. **The narrow part decides the flow.** A thick pipe barely resists the water. A thin, long section resists a lot, and it is there that most of the pressure is lost.

### What an electric loop actually does

Now the circuit. A battery does not create charge. It takes charge arriving at its minus terminal and, using chemical energy, delivers it out of its plus terminal at a higher electric potential (Phase 01, Lesson 06). The difference in potential between its terminals is its **voltage**, measured in **volts (V)**: one volt means one joule of energy for every coulomb of charge.

Charge flows round the loop (we follow **conventional current**, from + to - outside the battery; the electrons themselves drift the other way, as you saw in Phase 01, Lesson 08). The rate of flow is the **current**, measured in **amperes (A)**: one ampere is one coulomb passing each second. In the load (a bulb, a resistor) the charges bump through the material and give up their energy as heat or light, and they arrive back at the battery's minus terminal with low potential. The battery lifts them up again.

Look how the same three facts appear:

1. **The amount of charge never changes.** Every coulomb that leaves the battery comes back (conservation of charge, Phase 01, Lesson 04).
2. **What the battery gives is energy.** Charges leave with more energy per coulomb than they arrived with, and spend it in the load.
3. **The load decides the current.** A thick copper wire barely resists. A resistor or a bulb filament resists a lot, and it is there that most of the voltage is "used".

That is why the analogy is so good: both systems are loops where a pump lifts a conserved "stuff" to a higher energy level and the stuff spends that energy going through a narrow place.

### Where the push comes from: the height picture

Pumps are a bit abstract, so many people prefer **height**. Put a tank of water on a shelf 1 metre above a bucket and connect them with a pipe. The water at the top of the pipe is pushed down by the weight of the water above it. The pressure at the bottom of a column of water is

```
pressure = density x g x height
```

Read it out loud: "pressure equals how heavy each cubic metre of water is, times the strength of gravity, times how tall the column is". For water the density is 1000 kg per cubic metre and g is 9.81 m/s², so a 1 m column gives

```
pressure = 1000 kg/m^3 x 9.81 m/s^2 x 1 m = 9810 Pa
```

Height in this picture is exactly like electric potential: the absolute height of the shelf does not matter (whether the room is on the ground floor or the tenth floor), only the *difference* in height between the tank and the bucket. Voltage works the same way, which is why we choose a reference point, **ground**, and call its potential 0 V. A battery is then like a person carrying water from the bucket back up to the tank, over and over, so the flow never stops.

## The Concept

### The translation table

Here is the dictionary. Keep it next to you through Phases 03 and 04.

| Electric | Symbol and unit | Water | Unit |
|---|---|---|---|
| charge | Q, coulomb (C) | amount of water | litre or m³ |
| voltage (potential difference) | V, volt (V) | pressure difference (or height difference) | pascal (Pa) |
| current | I, ampere (A) | flow rate | litres per second, m³/s |
| resistance | R, ohm (Ω) | hydraulic resistance of a narrow pipe | Pa·s/m³ |
| battery | source | pump (or someone lifting water) | |
| wire | conductor | wide, short, smooth pipe | |
| switch | | valve (tap) | |
| power | P = V x I, watt (W) | pressure difference x flow rate | W |
| ground | 0 V reference | the floor you measure heights from | |

The letter I for current comes from the French *intensité du courant*, the term André-Marie Ampère used in the 1820s. Do not worry about why it is not C: that letter was already taken by charge (and later by capacitance).

### One pump, one pipe: a worked example

Let us run the same calculation on both sides. On the water side we need the resistance of a thin pipe. For slow, smooth flow, the 19th-century engineer Gotthilf Hagen and physician Jean Poiseuille found (Poiseuille was studying blood in thin glass tubes) that a pipe of length L and inner radius r resists with

```
pipe resistance = 8 x viscosity x L / (pi x r^4)
```

Do not memorise this, it is here so the numbers are real. Take a pipe 1 m long with a radius of 1 mm (0.001 m), and water with a viscosity of 0.001 Pa·s:

```
pipe resistance = 8 x 0.001 x 1 / (3.1416 x 0.001^4)
                = 0.008 / (3.1416 x 1e-12)
                = 2.55e9 Pa*s/m^3
```

Flow is push divided by resistance (the water version of the rule you will earn properly in Phase 03):

```
flow = pressure difference / pipe resistance
     = 9810 Pa / 2.55e9 Pa*s/m^3
     = 3.85e-6 m^3/s  = 3.85 mL per second
```

That is a slow trickle, a teaspoon every second or so. Now the electric side: a 9 V battery and a 450 Ω resistor. As a preview of Ohm's law (Phase 03), current is voltage divided by resistance:

```
current = voltage / resistance = 9 V / 450 ohm = 0.020 A = 20 mA
```

And the power each system moves. Water: pressure times flow, 9810 x 3.85e-6 = 0.0378 W. Electric: voltage times current, 9 x 0.020 = 0.18 W. Both have the same shape: *push times flow equals power*. You met P = V x I in Phase 01, Lesson 09; now you can see why it has that form. A joule per coulomb (volt) times coulombs per second (ampere) is joules per second, which is a watt. A joule per cubic metre (a pascal is exactly that) times cubic metres per second is again joules per second.

### Doubling experiments

The water picture shines when you ask "what if?" questions.

- **Double the push.** Raise the tank to 2 m (19 620 Pa). Twice the pressure pushes twice the flow: 7.7 mL/s. Use an 18 V battery instead of 9 V: 18 / 450 = 40 mA. Twice the voltage, twice the current.
- **Double the opposition.** Make the thin pipe 2 m long. Twice the resistance, half the flow: 1.93 mL/s. Use a 900 Ω resistor: 9 / 900 = 10 mA. Half the current.

The picture tells you the *direction* of the change before you do any arithmetic, which is exactly what you want from intuition.

### Series and parallel pipes

In Lesson 04 you saw two bulbs in series get dimmer and two bulbs in parallel stay bright while the battery worked harder. Here is why, in water.

```
 SERIES                                  PARALLEL

  pump ===[thin pipe]===[thin pipe]===+    pump ===+===[thin pipe]===+===+
   ^                                  |     ^      |                  |   |
   +==================================+     |      +===[thin pipe]===+   |
                                            +============================+
```

In series, all the water must squeeze through *both* thin pipes, one after the other. Twice the resistance, half the flow (1.93 mL/s instead of 3.85 mL/s). In parallel, the water has two separate paths, each with the full pressure across it, so each carries 3.85 mL/s and the pump delivers 7.7 mL/s in total. The pump really does work twice as hard: double the flow at the same pressure is double the power.

The electric version is identical: two 450 Ω resistors in series on 9 V carry 10 mA; two in parallel each carry 20 mA and the battery supplies 40 mA. You will make this exact in Phase 04 (Kirchhoff's Laws).

### A switch is a valve, a short is a wide bypass

A switch is a tap. Closed (on), the pipe is open to flow. Open (off), the valve blocks the pipe. Careful: the words are flipped! An *open* switch is a *closed* valve. Electricians say "open" because the metal contacts are physically apart, opening a gap in the loop.

A short circuit (Lesson 03) is a fat, wide pipe connected straight from the pump's outlet to its inlet. Almost no resistance, so the flow is enormous, the pump strains, and all the pressure difference collapses. In a battery, that means a huge current, heat, and maybe fire.

### Where the analogy breaks

Now the important half. Each item below is a place where water gives a wrong answer.

**1. Cut the loop and nothing leaks.** Cut a water pipe while the pump runs and water sprays out. Water can leave the loop because it has somewhere to go: the air will take it. Cut a wire and the current stops *everywhere* in the loop at the same moment. The charge does not pour out of the ends, because a lone wire end cannot hold more than a minuscule extra charge before the electric force pushes back (Phase 01, Lesson 05). This is why a circuit *must* be a closed loop (Lesson 01), while a garden hose can happily water the lawn without any return pipe.

**2. Thickness matters differently.** In the pipe formula above, the radius appears as r⁴. Halve the radius and the pipe resistance goes up 2⁴ = 16 times. A wire's resistance depends on its cross-section area, which goes as r², so halving the radius of a wire only makes it 2² = 4 times more resistive (Phase 03, Lesson 02). The water picture gets the direction right (thinner is harder) and the size of the effect badly wrong.

```
radius factor   pipe resistance factor   wire resistance factor
     0.5               16                       4
     1.0                1                       1
     2.0             0.0625                   0.25
```

**3. Speed is completely different.** This is the big one. Ask how fast things travel.

The electrons themselves crawl. In Phase 01, Lesson 08 you met drift speed:

```
drift speed = current / (n x e x A)
```

where n is the number of free electrons per cubic metre of copper (8.5e28), e is the charge of one electron (1.602e-19 C) and A is the cross-section area of the wire. For a 1 mm² wire (A = 1e-6 m²) carrying 1 A:

```
drift speed = 1 / (8.5e28 x 1.602e-19 x 1e-6)
            = 1 / 13.6
            = 0.0734 mm per second
```

At that pace an electron needs 1 m / 0.0000734 m/s = 13 600 s, almost **4 hours**, to cross a 1 m wire. Yet the bulb lights the instant you flick the switch. Why? Because the wire is already *full* of free electrons, end to end, just like a hose that is already full of water. When the battery pushes at one end, the push (the electric field) travels down the wire at around two thirds of the speed of light, about 2e8 m/s. Across 1 m, that takes 1 / 2e8 = 5 nanoseconds. The electrons near the bulb start moving almost at once; they are not the ones that left the battery.

The water analogy actually *helps* here, as long as the hose is full. Open a tap at the end of a 20 m hose that is already full and water comes out right away: the pressure travels at the speed of sound in water, about 1480 m/s, so it arrives in 20 / 1480 = 13.5 ms. The drop that was at the tap end at that moment comes out first; a drop that entered at the faucet with water moving at 1 m/s needs 20 s to arrive. What the analogy gets wrong is the scale: the electric push is more than 100 000 times faster than the water push, and the electric "drops" are about 10 000 times slower than water drops in a hose.

**4. The energy is not carried inside the wire.** In the water picture, energy rides inside the pipe with the water. In a real circuit, careful physics (the Poynting vector, which you will meet only in advanced courses like the Feynman Lectures, vol. II, chapter 27) shows that the energy travels through the electric and magnetic fields in the space *around* the wires, and the wires guide it. You do not need this for anything in the next ten phases, but it is the deepest reason why the water picture can never be the full story.

**5. Gravity does not care about wires.** Water in a vertical pipe falls. Electrons in a vertical wire do not: the gravitational force on an electron (9.1e-31 kg x 9.81 m/s² ≈ 9e-30 N) is hundreds of millions of times weaker than even the gentle electric push on it inside a wire carrying 1 A (about 3e-21 N). A circuit works the same upside down.

**6. Storage and inertia arrive later.** A capacitor (Phase 07) is often drawn as a rubber membrane stretched across a pipe: water pushes it, it bulges, it pushes back. An inductor (Phase 08) is often drawn as a heavy water wheel that resists changes in flow. These extensions are useful, but they get stretched thin quickly, and with alternating current (Phase 09) and filters (Phase 10) you will be much better off with the real mathematics.

**7. Not everything obeys "flow proportional to push".** A thin pipe at high speed becomes turbulent and stops following the simple rule. Many electric parts also break the simple rule, but in different ways: an LED (Phase 11) lets almost no current through until the voltage reaches about 2 V, then lets a lot through. Water has a version of this (a check valve with a spring) but it is a stretch.

### So how should you use the analogy?

Use it to predict *directions*: more push, more flow; more resistance, less flow; parallel paths share; series paths stack; a loop is needed; the source supplies energy, not stuff. Do not use it to predict *sizes* of effects, speeds, or anything about what happens in empty space around a wire. When in doubt, go back to the physics of Phase 01: charges, fields and energy per charge.

## Build It

The script in `code/main.py` runs a water calculation and an electric calculation side by side, then prints the three places where the comparison breaks.

### Step 1: The physical constants and the two "laws"

```python
WATER_DENSITY = 1000.0
WATER_VISCOSITY = 1.0e-3
G = 9.81
ELEMENTARY_CHARGE = 1.602176634e-19
COPPER_ELECTRON_DENSITY = 8.5e28
SOUND_SPEED_IN_WATER = 1480.0
SIGNAL_SPEED_IN_CABLE = 2.0e8


def pressure_from_height(height_m):
    return WATER_DENSITY * G * height_m


def pipe_resistance(length_m, radius_m):
    return 8 * WATER_VISCOSITY * length_m / (np.pi * radius_m**4)


def flow(pressure_pa, resistance):
    return pressure_pa / resistance


def current(volts, ohms):
    return volts / ohms
```

`flow` and `current` are the same function with different names. That is the whole point of the analogy.

### Step 2: Side by side

```python
def print_side_by_side(pressure_pa, pipe_r, volts, ohms):
    water_flow = flow(pressure_pa, pipe_r)
    electric_current = current(volts, ohms)
    ...
    print(f"  power     : pressure x flow     = {pressure_pa * water_flow:10.4f} W       | V x I      = {volts * electric_current:6.4f} W")
```

With a 1 m tank, a 1 m pipe of 1 mm radius, a 9 V battery and a 450 Ω resistor, it prints:

```
  push      : pressure difference =     9810.0 Pa      | voltage    =   9.00 V
  opposition: pipe resistance     =  2.546e+09 Pa*s/m^3 | resistance =    450 ohm
  flow      : water flow          =      3.852 mL/s    | current    =  20.00 mA
  power     : pressure x flow     =     0.0378 W       | V x I      = 0.1800 W
```

### Step 3: Doubling and combining

```python
def doubling_experiments(pressure_pa, pipe_r, volts, ohms):
    cases = [("baseline", 1, 1), ("double the push", 2, 1), ("double the opposition", 1, 2)]
    for name, push_factor, opposition_factor in cases:
        q = flow(push_factor * pressure_pa, opposition_factor * pipe_r)
        i = current(push_factor * volts, opposition_factor * ohms)
        ...


def series_and_parallel_pipes(pressure_pa, pipe_r):
    one = flow(pressure_pa, pipe_r)
    series = flow(pressure_pa, 2 * pipe_r)
    parallel = 2 * flow(pressure_pa, pipe_r)
    ...
```

Series pipes: the water fights two resistances one after the other, so we pass `2 * pipe_r`. Parallel pipes: each pipe sees the full pressure, so we compute one flow and double it.

### Step 4: Where it breaks

```python
def where_shape_matters():
    for factor in [0.5, 1.0, 2.0]:
        print(f"  {factor:13.1f} | {1 / factor**4:30.4f} | {1 / factor**2:30.4f}")


def drift_speed(amps, area_m2):
    return amps / (COPPER_ELECTRON_DENSITY * ELEMENTARY_CHARGE * area_m2)


def where_speed_matters(hose_length_m, water_speed_m_s, amps, wire_area_m2, wire_length_m):
    water_trip = hose_length_m / water_speed_m_s
    pressure_trip = hose_length_m / SOUND_SPEED_IN_WATER
    v_drift = drift_speed(amps, wire_area_m2)
    electron_trip = wire_length_m / v_drift
    signal_trip = wire_length_m / SIGNAL_SPEED_IN_CABLE
    ...
```

Run it from the repository root:

```
uv run python phases/02-your-first-circuits/05-the-water-analogy-and-its-limits/code/main.py
```

The speed section prints:

```
  a 20 m hose, water moving at 1.0 m/s
    one drop travelling the whole hose :       20.0 s
    the push arriving (full hose)      :       13.5 ms
  a 1 m copper wire of 1.0 mm^2 carrying 1.0 A
    electron drift speed               :     0.0734 mm/s
    one electron travelling the wire   :       3.78 hours
    the push (signal) arriving         :        5.0 ns
```

Change the numbers and predict the output before you run it. That habit, predict and then check, is what turns an analogy into real intuition.

## Use It

- **Plumbing words in electronics.** Engineers really do say a power supply can "source" or "sink" current, that current "flows", that a capacitor is a "reservoir" and that a big wire has "headroom". The water picture is baked into the language.
- **Pressure gauges and voltmeters.** A plumber reads pressure by tapping a gauge onto the pipe at one point relative to the air. You read voltage by touching two probes at two points (Lesson 07). Both measure a *difference*, never an absolute value.
- **Flow meters and ammeters.** To measure flow you must cut the pipe and put the meter *in line* so all the water goes through it. Same for current (Lesson 07). This is the single most useful practical consequence of the analogy.
- **Fuses and pressure-relief valves.** A relief valve opens when pressure gets dangerously high; a fuse (Lesson 03) melts when current gets dangerously high. Not quite the same (one is about push, the other about flow), and that difference is worth noticing.
- **Real numbers.** A household water main runs at roughly 300 000 Pa (3 bar) and a shower uses about 10 litres per minute. A phone charger delivers 5 V at up to 2 A. Neither number means anything to the other system; only the *shape* of the relationships carries over.

## Common Mistakes

- **Thinking the battery is a tank of electricity that empties.** A battery is a pump with a limited supply of chemical *energy*, not a tank of charge. When it is "flat", it has exactly as many electrons as when it was new; it has simply run out of the chemical reactions that lift them.
- **Thinking current is "used up" by the bulb.** Water is not consumed by a water wheel; current is not consumed by a bulb. The current going in equals the current coming out. Energy is what the bulb takes.
- **Expecting electricity to spill from an open socket or a cut wire.** Unlike water, charge cannot leave the conductor in any useful amount. A dangling wire connected to a battery's plus terminal carries no current at all. (It can still be at a dangerous voltage if the source is mains, which is why Phase 00, Lesson 08 told you never to touch one.)
- **Mixing up "open" switch and "open" tap.** Open switch: no current. Open tap: water flows. Say "the switch is off" if it helps.
- **Using the analogy to compute sizes.** "Twice as thick wire, sixteen times less resistance" is a water answer. The electric answer is four times.
- **Believing electrons travel from the battery to the bulb when you flip the switch.** They barely move. The push travels; the electrons near the bulb are the ones that light it.

## Exercises

1. **Translate.** A tank sits 3 m above a bucket. What pressure difference does it create (use pressure = 1000 x 9.81 x height)? What is the electrical equivalent of raising the tank from 1 m to 3 m?
2. **Predict, then compute.** A 6 V battery drives 30 mA through a bulb. Using the water picture, predict what happens to the current if you use a 12 V battery with the same bulb (assume the bulb behaves like a fixed resistor). Then compute it with current = voltage / resistance, after first finding the resistance from 6 V / 0.030 A.
3. **Series and parallel pipes.** Three identical thin pipes each carry 2 mL/s when connected alone to a pump. How much flow does the pump deliver if all three are in series? If all three are in parallel? Write the electrical version of your answer for three identical 300 Ω resistors on a 6 V battery.
4. **Drift speed.** A thin 0.25 mm² copper wire in a phone charger cable carries 2 A. Compute the electron drift speed in mm/s. How long would an electron need to travel the 1 m cable? How long does the push need?
5. **Find the lie.** A friend explains: "When you unplug a lamp from the wall, electricity is still flowing in the cord, it just has nowhere to go, so it builds up until you plug it back in." Using the list of where the analogy breaks, explain in three or four sentences what is actually going on in the cord.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| water analogy | "electricity is like water in pipes" | voltage ~ pressure difference, current ~ flow rate, resistance ~ narrow pipe; good for directions, poor for sizes and speeds |
| pressure difference | "the water pressure" | force per area between two points; drives the flow, like voltage drives current |
| flow rate | "how much water" | volume per second through a point; the analogue of current (charge per second) |
| hydraulic resistance | "a narrow pipe" | pressure drop per unit flow; for a long thin pipe it grows as length / radius⁴ |
| drift speed | "how fast electricity goes" | the slow average speed of electrons in a wire, fractions of a millimetre per second |
| signal speed | "the speed of electricity" | how fast the push travels along the wire, close to the speed of light |
| conservation | "it all comes back" | neither water in a closed loop nor charge in a circuit is created or destroyed; only energy is handed over |

## Further Reading

- [All About Circuits, Vol. I (DC), chapter 1 "Basic Concepts of Electricity"](https://www.allaboutcircuits.com/textbook/direct-current/chpt-1/voltage-current/) - a free textbook that uses the water picture and is careful about where it stops working.
- Richard Feynman, Robert Leighton, Matthew Sands, *The Feynman Lectures on Physics*, Vol. II, chapter 27 "Field Energy and Field Momentum" ([online](https://www.feynmanlectures.caltech.edu/II_27.html)) - where the energy in a circuit really flows.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, chapter 2 - a practical introduction to voltage, current and resistance with several hydraulic comparisons.
- Khan Academy, "Circuits" unit in physics ([khanacademy.org](https://www.khanacademy.org/science/physics/circuits-topic)) - short videos on current, voltage and resistance with water-flow pictures.
