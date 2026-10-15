# Current as Moving Charge

> Current is a count: how much charge crosses a line each second. The electrons doing it crawl; the push that moves them travels at nearly the speed of light.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 01 (The Physics Underneath), Lessons 01-05 (atoms and electrons, charge and the coulomb, the electric field, voltage, conductors); Phase 00, Lesson 03 (Units and SI Prefixes)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Current (I) | How much electric charge passes a point each second | How many litres of water flow past a spot in a river each second |
| Ampere (A), "amp" | The unit of current: one coulomb per second | One bucket per second, if the bucket held one coulomb |
| Coulomb (C) | The unit of charge (from Lesson 02); about 6.24 x 10^18 electrons' worth | A sack that holds a fixed, huge number of grains of sand |
| Cross-section | The flat slice you would see if you cut the wire straight across | The cut face of a salami |
| Drift velocity | The slow average speed at which free electrons creep along a wire carrying current | A crowd shuffling slowly towards the exit while everyone fidgets |
| Signal speed | How fast the "start moving" message travels along a wire | A push passed along a line of people standing shoulder to shoulder |
| Conventional current | The direction we draw current: from + to - through the circuit outside the source | The direction an arrow on a road map points, chosen by agreement |
| Electron flow | The direction electrons actually move: from - to + outside the source | The cars on that road, which happen to drive against the painted arrows |
| DC (direct current) | Current that keeps flowing in one direction | A river |
| AC (alternating current) | Current that reverses direction back and forth many times a second | A tide going in and out, but 50 or 60 times a second |
| Ammeter | An instrument that measures current | A turnstile counter at a stadium gate |

## Learning Objectives

- Define current as charge per unit time, read `I = Q / t` out loud, and convert between amperes, coulombs and seconds
- Count how many electrons per second make up a given current, from a watch (microamps) to a car starter (hundreds of amps)
- Derive and use the drift-velocity formula `I = n e A v` and explain why electrons in a wire move at a fraction of a millimetre per second
- Explain why a lamp lights instantly even though the electrons crawl, by separating drift speed from signal speed
- State the conventional-current rule, explain its 18th-century origin, and never get confused by it again
- Describe in one sentence what changes in AC compared with DC

## The Problem

You flip a light switch. The lamp across the room lights up instantly. It seems natural to imagine electrons racing from the switch to the lamp like water shooting through a hose. But if you compute how fast the electrons in that cable actually move, you get something like a tenth of a millimetre per second. Slower than a snail. An electron leaving the switch would need hours to reach the lamp.

Both facts are true. If you do not understand how, you will be confused by a lot of things later: why a circuit must be a closed loop (Phase 02), why the current is the same everywhere along a single wire, why "the battery sends out electrons" is a misleading picture, and why signals in a computer travel at a large fraction of the speed of light.

There is also a smaller trap. Every circuit diagram you will ever see draws current as flowing from the **+** terminal of a battery, around the circuit, back to the **-** terminal. Yet the electrons, which are what actually move in a metal wire, go the other way. That looks like a mistake, and in a way it is: a historical one that we keep on purpose. This lesson explains why, so it never trips you up.

## The Physics

### What moves, and what pushes

From Lesson 05: a metal like copper is full of free electrons, about 8.5 x 10^28 per cubic metre. From Lesson 03: an electric field pushes on charges. From Lesson 04: a voltage (a difference in electric potential) between two points sets up a field in the material between them.

Put those together. Connect a battery across a copper wire. The battery's voltage creates an electric field inside the wire, pointing from the + end towards the - end. Each free electron, being negative, feels a force opposite to the field, so it gets pushed towards the + end. Billions of billions of electrons move together. Charge is moving. That movement of charge is what we call **electric current**.

### A short history of the word

- **1800.** Alessandro Volta stacks zinc and copper discs separated by brine-soaked cardboard and gets a steady flow of electricity: the first battery, the **voltaic pile**. For the first time people can make charge flow continuously instead of in a single spark.
- **1820.** Hans Christian Ørsted notices that a wire carrying this flow deflects a compass needle. Within weeks André-Marie Ampère in Paris shows that two current-carrying wires attract or repel each other, and starts measuring it. He coins the term "electric current" in its modern sense and insists it has a direction. The unit of current, the **ampere**, is named after him.
- **1897.** J. J. Thomson discovers the electron (Lesson 01). Only then does anyone know what is actually moving inside a wire.

Notice the order. People measured currents, built telegraphs, and argued about the direction of flow for a century before they knew what carried it. That is the root of the sign confusion below.

### Free electrons are already moving, fast and randomly

Before you connect any battery, the free electrons in copper are not sitting still. They whiz around in random directions at around 1.6 x 10^6 m/s (about 0.5 % of the speed of light; the exact reason is quantum mechanics, but "they are very fast and random" is all we need). They constantly bounce off vibrating copper ions and change direction.

Because the motion is random, as many electrons cross any slice of the wire going left as going right. The net flow is zero. No current.

When you apply a voltage, the field adds a tiny steady push on top of all that random motion. Each electron still zigzags wildly, but between collisions it gains a little extra speed in one direction. Averaged over many collisions, the whole population slowly creeps along. That slow average creep is the **drift velocity**.

```
   no field: random zigzag, no net motion          with field: same zigzag, tiny net creep

     e  /\    /\                                       e  /\    /\
       /  \  /  \  /                                     /  \  /  \  /     ---> creep
      /    \/    \/                                     /    \/    \/
   start ............ end (same place on average)     start ................ end (a little to the right)
```

The picture is like a bee swarm drifting slowly downwind while every bee darts around at full speed.

## The Concept

### Current is charge per second

Imagine standing next to a wire and counting all the charge that crosses an imaginary slice through it. If in a time `t` a total charge `Q` crosses, then the current is

*current equals charge that passed, divided by the time it took.*

```
I = Q / t
```

- `I` is the current, in **amperes** (A). The letter I comes from the French *intensité du courant*, as Ampère wrote it.
- `Q` is the charge, in **coulombs** (C).
- `t` is the time, in **seconds** (s).

So **1 ampere = 1 coulomb per second**. That is the whole definition.

Worked examples (each one is printed by the script):

```
10 C pass through a lamp in 5 s:           I = 10 / 5          = 2 A
0.06 C pass through an LED in 3 s:         I = 0.06 / 3        = 0.02 A = 20 mA
a phone battery delivers 14 400 C in 2 h:  I = 14 400 / 7 200  = 2 A
```

In the last one, 2 hours had to be converted to seconds first: 2 x 60 x 60 = 7200 s. Units always first.

The formula can be turned around. If you know the current and the time, the charge is

```
Q = I x t
```

A current of 0.5 A flowing for 1 minute moves 0.5 x 60 = 30 C. This is exactly what the "mAh" on a battery means (Phase 00, Lesson 03): milliamps times hours is a charge. A 4000 mAh phone battery holds 4 A x 3600 s = 14 400 C of charge it can push around the circuit.

### Since 2019, the ampere is defined by counting

For most of the 20th century, the ampere was defined by the force between two long parallel wires, an echo of Ampère's own experiments. In 2019 the SI system was redefined: the charge of one electron, `e`, was fixed to be exactly

```
e = 1.602176634 x 10^-19 C
```

So one coulomb is exactly 1 / 1.602176634e-19 = 6.241509 x 10^18 elementary charges, and one ampere is that many elementary charges passing per second. The ampere is now literally a counting rate.

### Counting electrons per second

To find how many electrons per second make a current, divide the current by the charge of one electron:

*electrons per second equals current divided by the charge of one electron.*

```
N per second = I / e
```

Worked example for a red LED at 20 mA:

```
N = 0.020 / 1.602e-19 = 1.25e17 electrons per second
```

About 125 thousand trillion electrons every second, for a small LED. Here is the full range:

| Device | Current | Electrons per second |
|---|---|---|
| Quartz watch | 1.5 µA = 1.5 x 10^-6 A | 9.4 x 10^12 |
| Red LED | 20 mA = 0.020 A | 1.25 x 10^17 |
| Phone charging | 2 A | 1.25 x 10^19 |
| Electric kettle (2000 W on 230 V) | 8.7 A | 5.4 x 10^19 |
| Car starter motor | 150 A | 9.4 x 10^20 |

Even the watch, at a millionth of an ampere, moves ten trillion electrons per second. This is why we never count electrons one by one in circuits: the numbers are so large that charge behaves like a smooth fluid. (Exceptions exist, in single-electron transistors and in noise, Phase 19, but not in everyday circuits.)

### Conventional current versus electron flow

Around 1747 Benjamin Franklin proposed that electricity was a single "fluid". Objects with too much of it he called **positive**, objects with too little **negative** (Lesson 02). When a charged object discharged, he imagined fluid flowing from the positive (excess) side to the negative (deficit) side. It was a perfectly reasonable guess with the information he had. He had to pick a direction, and he had a 50/50 chance.

A century and a half later, Thomson showed that in metals the moving charges are electrons, and electrons carry the charge Franklin had called negative. So in a wire, the actual movers travel from - to +. Franklin's guess was the wrong way round for metals.

By then every textbook, instrument and formula used Franklin's direction. Rather than flip everything, engineers kept it. So we have two descriptions:

```
             conventional current I  (what we draw)
           ------------------------------------>
    +  ___________________________________________  -
   [battery]          wire          [lamp]
    +  -------------------------------------------  -
           <------------------------------------
              electrons actually drift this way
```

- **Conventional current**: drawn from **+** to **-** through the external circuit (and from - to + inside the battery, completing the loop). This is what every schematic, every formula and every instrument in this course uses.
- **Electron flow**: the real motion of electrons in a metal, opposite to the conventional arrow.

Why it does not matter for the physics: a negative charge moving left carries charge the same way as a positive charge moving right. Both reduce the negative pile and the positive pile in the same way. In fact, in some conductors the movers really are positive: in salt water and in your body both positive and negative ions move; in p-type silicon (Lesson 05) holes, which act as positive charges, do much of the carrying. Conventional current describes them all with one arrow. **Rule for this course: current arrows always mean conventional current, + to - through the circuit outside the source.** When we care about electrons specifically, we will say "electrons drift the other way".

### Drift velocity: the counting box

Let us derive how fast the electrons creep. Picture a wire with cross-section area `A`, carrying current `I`. All the free electrons drift at the same average speed `v`. Draw an imaginary slice across the wire, and ask: in one second, which electrons cross it?

```
           the electrons that cross the slice in 1 second
           are exactly those within distance v behind it
                  |<------ v x 1 s ------>|
        __________|_______________________|_______
       |          |  e   e  e   e    e   e|       |
  A -> |          |   e  e   e  e   e  e  |       |  ---> drift
       |__________|_______________________|_______|
                                          ^
                                    counting slice
```

The electrons that will cross in one second are those currently in a little box of length `v` (metres travelled in one second) and area `A`. Its volume is `A x v`. Each cubic metre holds `n` free electrons, so the box holds `n x A x v` electrons. Each carries charge `e`. Charge crossing per second, which is current:

*current equals carrier density, times charge per carrier, times area, times drift speed.*

```
I = n x e x A x v      so      v = I / (n x e x A)
```

- `n` is the number of free electrons per cubic metre (8.5 x 10^28 for copper).
- `e` is the electron's charge, 1.602 x 10^-19 C.
- `A` is the cross-section area in m^2.
- `v` is the drift velocity in m/s.

Worked example: 1 A in a copper wire of cross-section 1 mm^2 (= 1 x 10^-6 m^2), a typical lamp cord.

```
n x e x A = 8.5e28 x 1.602e-19 x 1e-6
          = 1.362e4  coulombs per metre of wire
v         = 1 / 1.362e4 = 7.34e-5 m/s = 0.073 mm/s
```

Read the middle line out loud: every metre of this wire contains 13 620 coulombs of free electron charge. To make 1 coulomb per second pass the slice, that huge pool only has to slide along by 1/13 620 of a metre each second.

At 0.073 mm per second, an electron needs 1 / 7.34e-5 = 13 600 s, almost 4 hours, to drift one metre. A snail does about 1 mm/s, more than ten times faster.

| Wire | Current | Area | Drift speed | Time to move 1 m |
|---|---|---|---|---|
| Thin LED lead | 0.02 A | 0.2 mm^2 | 0.0073 mm/s | 38 hours |
| Lamp cord | 1 A | 1 mm^2 | 0.073 mm/s | 3.8 hours |
| Kettle cord | 8.7 A | 1.5 mm^2 | 0.43 mm/s | 39 minutes |
| Car starter cable | 150 A | 25 mm^2 | 0.44 mm/s | 38 minutes |

Notice the last two: engineers size wires so the current per unit area stays in a similar range, roughly 1 to 6 A per mm^2, because that is what keeps wires from overheating. Drift speeds in real wiring are therefore always around a tenth of a millimetre per second, give or take a factor of ten.

### Then why does the lamp light instantly?

Because the electrons do not need to travel from the switch to the lamp. The wire is **already full** of free electrons, end to end, all the way round the circuit. When you close the switch, the electric field is established along the whole wire almost at once, and every electron everywhere, including the ones already sitting inside the lamp's filament, starts drifting at the same moment.

Think of a garden hose that is already full of water. Turn the tap and water comes out of the far end immediately, but it is not the water that just left the tap; that water will take a while to arrive. Or a line of marbles in a tube: push one in at one end and one pops out at the other end at once.

What does travel fast is the **signal**, the change in the electric field (really, an electromagnetic wave guided by the wires). In a typical cable it moves at about two thirds of the speed of light:

```
signal speed ≈ 0.66 x 3.0e8 m/s = 1.98e8 m/s
time for 2 m of cable = 2 / 1.98e8 = 1.0e-8 s = 10 ns
```

Ten nanoseconds for the "go" message; about 7.6 hours for an individual electron to drift the same 2 m. So there are three very different speeds in a wire:

| Speed | Typical value | What it is |
|---|---|---|
| Drift | ~10^-4 m/s | Net creep of electrons that carries the current |
| Random thermal-quantum motion | ~10^6 m/s | How fast each electron zigzags; averages to zero |
| Signal | ~2 x 10^8 m/s | How fast the start/stop of current propagates |

What the hose and marble analogies get wrong: water in a hose is pushed by pressure from behind, one molecule shoving the next. In a wire, the push comes from the electric field set up by charges on the surface of the wire and the battery, and that field reaches each electron almost directly. The "full hose" idea is right; the "shoving" idea is not quite.

### Current is the same all along a single path

If electrons leaving one end of a wire did not equal electrons arriving at the other end, charge would pile up somewhere in the middle. A pile of charge creates a strong field (Lesson 03) that immediately pushes back and evens things out. In a steady circuit, therefore, the current is the same at every point along a single unbranched path: through the wire, through the lamp and through the battery. Nothing is "used up". The lamp uses **energy** (Lesson 07), not charge. Every electron that goes in one side of the lamp, one comes out the other. You will build on this in Phase 02 (the closed loop) and make it a law in Phase 04 (Kirchhoff's current law).

This also tells you how an **ammeter** must be connected: the current has to pass through it, so you break the loop and put the meter in the gap, in series. That is the practical topic of Phase 02, Lesson 07.

### DC and AC, a preview

- **DC (direct current)**: the current flows in one direction, steadily. Batteries, USB chargers, solar cells and everything inside your phone run on DC. All of Phases 01 to 08 are about DC.
- **AC (alternating current)**: the current reverses direction regularly, 50 times a second in Europe and most of the world (50 Hz, hertz meaning "per second"), 60 times in North America. Wall sockets deliver AC.

In AC the electrons do not go anywhere at all on average: they wiggle back and forth in place. How far? For a 1 A AC current in a 1 mm^2 copper wire at 50 Hz, the peak current is 1.414 A (you will see why in Phase 09), giving a peak drift speed of 1.04 x 10^-4 m/s, and the swing is

```
amplitude = peak speed / (2 x pi x frequency)
          = 1.04e-4 / (2 x 3.1416 x 50)
          = 1.04e-4 / 314.2
          = 3.3e-7 m = 0.33 micrometres
```

A third of a micrometre, about a hundredth of the width of a human hair. And still your kettle boils, because what the circuit delivers is energy, not electrons. Phase 09 is devoted to AC.

## Build It

Run the script from the repository root:

```
uv run python phases/01-the-physics-underneath/06-current-as-moving-charge/code/main.py
```

### Step 1: Three tiny formulas

```python
import numpy as np

ELECTRON_CHARGE = 1.602176634e-19
COPPER_FREE_ELECTRONS = 8.5e28
SPEED_OF_LIGHT = 2.998e8
CABLE_VELOCITY_FACTOR = 0.66
FERMI_SPEED_COPPER = 1.57e6


def current_from_charge(charge_c, time_s):
    return charge_c / time_s


def electrons_per_second(current_a):
    return current_a / ELECTRON_CHARGE


def drift_velocity(current_a, area_m2, carrier_density=COPPER_FREE_ELECTRONS):
    return current_a / (carrier_density * ELECTRON_CHARGE * area_m2)
```

`FERMI_SPEED_COPPER` is the name physicists give the random speed of copper's fastest free electrons; you only need to know it is "about a million metres per second".

### Step 2: Current from charge and time, and electron counts

`print_basic_currents` runs the three `I = Q / t` examples, and `print_electron_counts` loops over five devices:

```python
def print_electron_counts():
    print("=== How many electrons pass each second? ===")
    examples = [
        ("quartz watch", 1.5e-6),
        ("red LED", 0.020),
        ("phone charging", 2.0),
        ("electric kettle", 8.7),
        ("car starter motor", 150.0),
    ]
    for label, current in examples:
        count = electrons_per_second(current)
        print(f"{label:18s} I = {current:9.2e} A  ->  {count:9.2e} electrons per second")
```

Output:

```
quartz watch       I =  1.50e-06 A  ->   9.36e+12 electrons per second
red LED            I =  2.00e-02 A  ->   1.25e+17 electrons per second
phone charging     I =  2.00e+00 A  ->   1.25e+19 electrons per second
electric kettle    I =  8.70e+00 A  ->   5.43e+19 electrons per second
car starter motor  I =  1.50e+02 A  ->   9.36e+20 electrons per second
```

### Step 3: Drift speeds in real wires

```python
def print_drift_speeds():
    print("=== Drift speed in copper wire ===")
    cases = [
        ("LED wire, 0.02 A, 0.2 mm^2", 0.02, 0.2e-6),
        ("lamp cord, 1 A, 1 mm^2", 1.0, 1.0e-6),
        ("kettle cord, 8.7 A, 1.5 mm^2", 8.7, 1.5e-6),
        ("starter cable, 150 A, 25 mm^2", 150.0, 25e-6),
    ]
    for label, current, area in cases:
        v = drift_velocity(current, area)
        hours_per_metre = 1.0 / v / 3600.0
        print(f"{label:30s} v = {v * 1000:8.4f} mm/s  ->  {hours_per_metre:7.2f} hours to move 1 m")
```

Note the conversions: areas in mm^2 become m^2 by multiplying by 10^-6 (`0.2e-6`), the speed is shown in mm/s by multiplying m/s by 1000, and seconds become hours by dividing by 3600.

### Step 4: Three speeds side by side

`print_speed_comparison` prints drift (7.34e-05 m/s), random motion (1.57e+06 m/s) and signal speed (1.98e+08 m/s), and reports that the signal is about 2.7 x 10^12 times faster than the drift. For a 2 m cord: 10.1 ns versus 7.6 hours.

`print_charge_in_wire` multiplies 8.5e28 by the volume of 1 m of 1 mm^2 wire (1e-6 m^3) to get 8.50e+22 free electrons, holding 13 619 C of charge. At 1 A it takes 3.8 hours to replace them all, the same number as the drift time, as it must be.

### Step 5: Prove `I = n e A v` by counting

Here we build a toy wire to check the counting-box argument with real counting instead of algebra. We scatter 2000 charges at random along one metre of wire to the left of a line at `x = 0`, let them all drift at 0.05 m/s for 4 s, and count how many crossed the line.

```python
def simulate_counting(seed=7):
    print("=== Counting charges that cross a line (toy wire) ===")
    rng = np.random.default_rng(seed)
    wire_length = 1.0
    charges_per_metre = 2000
    drift = 0.05
    duration = 4.0
    positions = np.sort(rng.uniform(-wire_length, 0.0, charges_per_metre))
    final_positions = positions + drift * duration
    crossed = int(np.sum((positions < 0.0) & (final_positions >= 0.0)))
    measured_rate = crossed / duration
    predicted_rate = charges_per_metre * drift
    ...
```

The prediction is "charges per metre times metres per second", which is the 1-D version of `n A v`: 2000 x 0.05 = 100 charges per second. The simulation counts 405 crossings in 4 s, a rate of 101.2. The small difference is because the charges were placed at random, not perfectly evenly.

### Step 6: Fast zigzag, slow drift

To see how a tiny push survives inside violent random motion, we simulate 100 000 electrons taking 400 steps. Each step is +1 or -1 at random (the thermal zigzag), and we add a push of 0.01 per step (the field).

```python
def simulate_random_walk(seed=11):
    print("=== Fast random motion, slow average drift ===")
    rng = np.random.default_rng(seed)
    electrons = 100000
    steps = 400
    random_speed = 1
    drift_per_step = 0.01
    kicks = (2 * rng.integers(0, 2, size=(steps, electrons), dtype=np.int8) - 1) * random_speed
    displacement = kicks.sum(axis=0, dtype=np.int32) + drift_per_step * steps
    ...
```

`rng.integers(0, 2, ...)` gives 0 or 1; `2 * x - 1` turns that into -1 or +1. The table `kicks` has one row per step and one column per electron, and summing down each column gives each electron's total wander. Output:

```
Average displacement after 400 steps = 4.113 units
Expected from the push alone        = 4.000 units
Typical size of one electron's wander = 20.1 units
```

Any one electron wanders about 20 units, five times more than the push moved it, and in a random direction. But the average over all electrons is about 4, exactly what the tiny push predicts. Current only cares about the average.

### Step 7: The AC wiggle

`print_ac_wiggle` takes a 1 A (rms) AC current at 50 Hz in 1 mm^2 copper, computes the peak drift speed (1.04e-04 m/s) and the swing amplitude: about 0.33 micrometres.

## Use It

- **Datasheets list currents everywhere.** A typical small red LED datasheet gives a recommended forward current of 20 mA and an absolute maximum of about 30 mA. A USB 2.0 port supplies up to 500 mA; USB-C chargers commonly offer 3 A. An Arduino Uno pin is rated for an absolute maximum of 40 mA, with 20 mA recommended.
- **Battery life.** A battery's mAh rating is charge, `Q = I x t`. A 220 mAh CR2032 coin cell powering a sensor that draws 10 µA on average lasts 220 mAh / 0.010 mA = 22 000 hours, about 2.5 years.
- **Wire sizing.** Electrical codes limit current per wire size precisely because more current per area means more heating. Household 1.5 mm^2 wire is typically protected at 10 to 16 A, 2.5 mm^2 at 16 to 20 A (exact numbers depend on the country and installation).
- **Fast signals.** On a circuit board, signals travel about 15 cm per nanosecond. A computer memory bus running at several gigahertz has to account for this, which is why the tracks between a processor and its memory chips are carefully length-matched (Phase 21).
- **Electroplating and batteries.** In chemistry the charge really is carried by ions, and the amount of metal deposited by a current is proportional to `Q = I x t`, a law Faraday discovered in the 1830s.

## Common Mistakes

- **"The battery is a store of electrons that get used up."** The battery pushes charge around a loop; the same charge comes back. A battery runs out of chemical energy, not of electrons.
- **"Electrons travel from the switch to the lamp at the speed of light."** The signal does. The electrons drift at a fraction of a millimetre per second.
- **Mixing up current and charge.** Current is a rate (coulombs per second). Saying "the battery has 2 amps in it" is like saying "the tank has 2 litres per second in it".
- **Forgetting to convert units before dividing.** Hours to seconds, mm^2 to m^2, mA to A. `I = Q / t` only gives amperes if Q is in coulombs and t is in seconds.
- **Drawing current arrows the electron way.** In this course, and in nearly all engineering, an arrow labelled I points from + to - outside the source. Electrons go the other way.
- **Thinking current gets smaller after passing through a lamp.** The current is the same before and after; the energy is what the lamp takes.
- **Measuring current by touching the meter across a part.** Current has to flow through the meter, so you must break the circuit and insert it in series (Phase 02, Lesson 07).

## Exercises

1. **Charge and time.** A charger delivers 1.5 A for 40 minutes. How much charge flowed, in coulombs and in mAh? How many electrons is that?
2. **Electrons in a flash.** A camera flash discharges 0.05 C in 1 millisecond. What is the average current? How many electrons per second is that?
3. **Thin versus thick.** The same 2 A current flows first through a 0.5 mm^2 copper wire and then through a 2.5 mm^2 copper wire joined to it. Compute the drift speed in each. Which is faster, and by what factor? Is the current different in the two pieces?
4. **Aluminium wire.** Aluminium has about 1.8 x 10^29 free electrons per m^3 (three per atom). For 10 A in a 4 mm^2 aluminium wire, compute the drift speed. Compare with copper of the same size.
5. **Across the ocean.** A telegraph cable 3000 km long carries a steady 50 mA in a copper core of cross-section 3 mm^2. (a) How long would one electron need to drift the full length, in years? (b) How long does the signal need at two thirds of the speed of light? Modify `print_speed_comparison` in `main.py` to print both.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Current I | "The flow of electricity" | Rate of charge crossing a surface: I = Q / t, in amperes |
| Ampere (A) | "Amps" | One coulomb per second, about 6.24 x 10^18 elementary charges per second |
| Coulomb (C) | "A unit of charge" | Exactly 1 / 1.602176634e-19 elementary charges |
| Drift velocity | "How fast electricity moves" | The slow average speed of carriers, v = I / (n e A), typically ~0.1 mm/s |
| Signal speed | "Electricity travels at the speed of light" | Speed of the electromagnetic change along the wire, about 0.5 to 0.9 c |
| Conventional current | "Current flows from + to -" | The agreed direction of positive charge flow; opposite to electron motion in metals |
| Electron flow | "The real direction" | Physical electron motion, from - to + outside the source |
| DC | "Battery power" | Current in one direction, steady or nearly so |
| AC | "Mains power" | Current that reverses periodically, 50 or 60 times per second from the wall |
| Ammeter | "Current meter" | Instrument inserted in series so the current passes through it |

## Further Reading

- Richard Feynman, *The Feynman Lectures on Physics*, Vol. II, chapter 13 ("Magnetostatics", section on current density), free at feynmanlectures.caltech.edu.
- All About Circuits, *Textbook Vol. I (DC)*, chapter 1 "Basic Concepts of Electricity", sections on electron flow and conventional flow.
- BIPM, *The International System of Units (SI Brochure)*, 9th edition (2019), which defines the ampere through the fixed value of the elementary charge; free at bipm.org.
- HyperPhysics (Georgia State University), "Microscopic View of Ohm's Law" and "Drift Velocity" pages, hyperphysics.phy-astr.gsu.edu.
