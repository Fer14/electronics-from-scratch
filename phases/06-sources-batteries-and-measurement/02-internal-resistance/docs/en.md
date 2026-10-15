# Internal Resistance

> You can't see the resistor inside a battery, but you can catch it: load the battery and watch how far the voltage falls.

**Type:** Build
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Phase 04 (Kirchhoff's Laws), Phase 06 Lesson 01 (Ideal and Real Sources)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Internal resistance (r) | The resistance inside a source that its own current must flow through | A kink in the hose inside the pump housing |
| Open-circuit voltage (V_oc) | The voltage a source shows when no current flows out of it | Tap pressure with the tap closed |
| Loaded voltage | The voltage a source shows while it is delivering current | Tap pressure while the shower runs |
| Voltage sag | How far the voltage falls when you load the source | The shower going weak when someone flushes the toilet |
| Efficiency | Useful power out divided by all the power the source produced | Of all the fuel burned, how much moved the car |
| Heavy load / light load | A load that takes a lot of current (small resistance) / a little current (big resistance) | A kettle versus a night light |
| Cells in series | Cells stacked plus-to-minus, one after the other | People standing on each other's shoulders |
| Cells in parallel | Cells side by side, all pluses joined, all minuses joined | People pulling the same rope together |
| ESR | Equivalent series resistance: datasheet name for internal resistance | Same as above, in datasheet language |
| State of charge | How full a battery is, from 0 % to 100 % | The fuel gauge |

## Learning Objectives

- Measure the internal resistance of a source from two voltage readings at two different currents.
- Calculate how a source's power splits between the load and its own insides, and its efficiency.
- Predict the EMF and internal resistance of cells connected in series and in parallel.
- Explain why an old battery can still run a TV remote but not a camera.
- Reproduce all these effects in our simulator and check them by hand.

## The Problem

Two AA batteries from the same drawer both read 1.5 V on your multimeter. You put them in a digital camera: one works, the other makes the camera shut down as soon as the lens moves. You put the "dead" one in the TV remote and it works for months.

The multimeter did not lie: it measured the open-circuit voltage, which is almost the same for a new cell and a tired one. What changed between the two is a number your meter does not show on its own: the internal resistance. A camera motor pulls about 1 A; the remote pulls about 20 mA. A fraction of an ohm of extra resistance inside the cell is invisible at 20 mA and decisive at 1 A.

In this lesson you learn to catch that hidden resistor, predict what it does, and design around it.

## The Physics

### Where the resistance lives

Inside an alkaline AA cell the current must travel: through the steel can, through a cylinder of manganese dioxide paste, across a soaked paper separator, through a gel of zinc powder and potassium hydroxide, and out through a brass nail. Each step resists the flow:

- **Electronic resistance.** Electrons moving through the metal parts and the powders. Small, but not zero.
- **Ionic resistance.** In the electrolyte (the liquid or gel between the electrodes) charge is carried by ions, which are whole atoms with missing or extra electrons. Ions are heavy and bump into everything; they move far less easily than electrons in copper.
- **Reaction resistance.** The chemical reaction at each electrode's surface can only run so fast. Asking for more current forces it harder, and that costs voltage.

As a battery is used, its reaction products clog the electrodes and the electrolyte runs short, so all three parts grow. Cold makes ions sluggish, so r rises in winter (that is why cars struggle to start on frosty mornings).

### Why it acts like a resistor

For moderate currents the voltage lost inside grows roughly in proportion to the current: twice the current, twice the loss. That proportionality is exactly the definition of a resistor (Ohm's law, V = I * R). So we draw the inside losses as one resistor r in series with an ideal EMF E. It is a model, not a literal part, and it is only approximately constant. But it is accurate enough to predict most of what you will see.

## The Concept

### The model again

```
     +---- battery ----+
     |  (+) E          |
     |   |             |
     |  [ r ]          |
     |   |             |
     +---o + ----------+--------+
                                |
                              [R_L]
     +---o - -------------------+
```

From Lesson 01, with a load R_L:

- Current: I = E / (r + R_L). Say it: "the EMF divided by all the resistance in the loop."
- Terminal voltage: V = E - I * r. Say it: "the EMF minus what the inside resistor eats."

### Catching r with two measurements

You can't put an ohmmeter on r: it is buried inside a part that also contains a voltage source. But you can watch what it does.

**Method 1: open circuit, then a load.**

1. Measure the voltage with nothing connected (a digital meter barely loads the battery, Lesson 05). With no current, nothing is lost inside, so this reading is E.
2. Connect a known load R_L and measure the terminal voltage V and the current I (or compute I = V / R_L).
3. The difference E - V is what r ate. So:

        r = (E - V) / I

Read it: "the internal resistance is the voltage that went missing divided by the current that made it go missing."

Worked example. A cell reads 1.550 V open. With a 10 ohm load it reads 1.523 V.

- I = 1.523 / 10 = 0.1523 A
- Missing voltage: 1.550 - 1.523 = 0.027 V
- r = 0.027 / 0.1523 = 0.177 ohm

**Method 2: two different loads.** The open-circuit reading is sometimes unreliable (a rested battery "recovers" a little extra voltage that vanishes as soon as current flows). So engineers use two loads, a light one and a heavy one:

    r = (V_light - V_heavy) / (I_heavy - I_light)

Read it: "the extra voltage lost divided by the extra current drawn." This is just the slope of the output line from Lesson 01.

Worked example. With 10 ohm: 1.523 V, 0.1523 A. With 2 ohm: 1.422 V, 0.711 A.

- Extra voltage lost: 1.523 - 1.422 = 0.101 V
- Extra current: 0.711 - 0.1523 = 0.5587 A
- r = 0.101 / 0.5587 = 0.181 ohm

Both methods agree with each other (and with the true value 0.18 ohm hidden in the script) to within the rounding of a 3-digit meter.

### Where the power goes

Power is voltage times current (Phase 03): P = V * I. With the same current I through both resistors:

- Power in the load: P_load = I^2 * R_L
- Power wasted inside: P_inside = I^2 * r
- Total power the chemistry produced: P_total = E * I

The **efficiency** is the useful fraction:

    efficiency = P_load / P_total = R_L / (R_L + r)

Read it: "the share of the power the load gets equals its share of the total resistance." This works because the same current flows through both, so power splits in proportion to resistance.

Worked example with E = 9 V and r = 2 ohm:

| R_L | I = 9 / (2 + R_L) | P_load | P_inside | Efficiency |
|---|---|---|---|---|
| 100 ohm | 0.088 A | 0.779 W | 0.016 W | 98 % |
| 10 ohm | 0.75 A | 5.63 W | 1.13 W | 83 % |
| 2 ohm | 2.25 A | 10.1 W | 10.1 W | 50 % |
| 0.5 ohm | 3.6 A | 6.48 W | 25.9 W | 20 % |

Two lessons hide in this table:

1. **Light loads are efficient.** When R_L is many times r, the battery wastes almost nothing.
2. **The most load power happens at R_L = r**, but then half the energy is heat inside the battery. Below that, the load gets *less* power and the battery cooks. This is maximum power transfer (Phase 05 Lesson 07). Batteries are never run this way on purpose.

### Old cells, heavy loads

Take one cell with E = 1.5 V. Watch the terminal voltage as r grows with age, in two devices:

- a TV remote, roughly a 75 ohm load (20 mA);
- a camera, roughly a 1.5 ohm load (1 A).

| r | Remote: 1.5 * 75 / (75 + r) | Camera: 1.5 * 1.5 / (1.5 + r) |
|---|---|---|
| 0.15 ohm (new) | 1.497 V | 1.364 V |
| 0.3 ohm | 1.494 V | 1.250 V |
| 0.6 ohm | 1.488 V | 1.071 V |
| 1.0 ohm | 1.480 V | 0.900 V |
| 1.5 ohm (tired) | 1.471 V | 0.750 V |

If the camera shuts down below 1.1 V, the cell is "dead" for the camera once r passes about 0.55 ohm. (Solve 1.5 * 1.5 / (1.5 + r) = 1.1: 1.5 + r = 2.045, r = 0.545.) The remote never notices. Same cell, same open-circuit voltage, opposite verdicts. This is the mystery from The Problem, solved.

### Cells in series

Stack cells plus-to-minus. Kirchhoff's voltage law adds the EMFs. The same current goes through every internal resistor, so they are in series too and add up.

```
  (+)E1-[r1]-(+)E2-[r2]-(+)E3-[r3]-(+)E4-[r4]--o +
```

For n identical cells: E_total = n * E and r_total = n * r.

Four AA cells (1.5 V, 0.2 ohm each): E = 6 V, r = 0.8 ohm. Into 4 ohm: I = 6 / 4.8 = 1.25 A, V = 1.25 * 4 = 5.0 V.

### Cells in parallel

Put n identical cells side by side. They all have the same EMF, so the voltage stays E. Their internal resistors are now in parallel, so r_total = r / n. Each cell supplies only 1 / n of the current.

Four AA cells in parallel: E = 1.5 V, r = 0.2 / 4 = 0.05 ohm. Into 4 ohm: I = 1.5 / 4.05 = 0.370 A, V = 1.481 V.

Parallel cells must be matched. If one cell is fuller than another, its EMF is higher and current flows from the full cell into the empty one even with no load, wasting energy and heating both. That is why battery packs use cells from the same batch.

### Two series strings in parallel

Two strings of 2 cells each, joined in parallel: each string is 3 V with 0.4 ohm; two in parallel make 3 V with 0.2 ohm. Into 4 ohm: I = 3 / 4.2 = 0.714 A, V = 2.857 V. Laptop and e-bike packs are built this way: series for voltage, parallel for current and capacity.

## Build It

### Step 1: Measure a hidden resistance

The script hides a cell with E = 1.55 V and r = 0.18 ohm. It "measures" it like you would, with readings rounded to a 3-digit meter: once with only a 10 Mohm meter attached, once with 10 ohm, once with 2 ohm.

```python
def battery_with_load(emf, internal_ohms, load_ohms):
    c = Circuit()
    c.voltage_source("E", "emf", "0", emf)
    c.resistor("Rint", "emf", "plus", internal_ohms)
    c.resistor("RL", "plus", "0", load_ohms)
    return c.dc()


def internal_resistance_from_two_loads(v1, i1, v2, i2):
    return (v1 - v2) / (i2 - i1)
```

Output:

```
  r from open and 10 ohm  = (1.550 - 1.523) / 0.1523 = 0.177 ohm
  r from 10 ohm and 2 ohm = (1.523 - 1.422) / (0.7110 - 0.1523) = 0.181 ohm
  the hidden value was 0.18 ohm
```

The small errors come from rounding the readings, just like on a real meter. With small voltage differences, every rounded digit matters: that is a reason to use a heavy enough second load.

### Step 2: The power budget

For loads from 100 ohm to 0.5 ohm the script asks the simulator for `r.p("RL")` and `r.p("Rint")`, the power in each resistor, and prints the efficiency. It reproduces the table above, including the 50 % line at 2 ohm.

### Step 3: Building packs

Three functions build four cells in series, in parallel and as two-by-two, each cell as its own ideal source plus 0.2 ohm, and feed a 4 ohm load. The simulator results (5.000 V, 1.481 V, 2.857 V) match the hand formulas.

```python
def stack_in_parallel(cells):
    c = Circuit()
    for k in range(cells):
        c.voltage_source(f"E{k}", f"m{k}", "0", 1.5)
        c.resistor(f"R{k}", f"m{k}", "out", 0.2)
    c.resistor("RL", "out", "0", 4.0)
    r = c.dc()
    return r.v("out"), r.i("RL")
```

### Step 4: The aging cell

The script sweeps r from 0.15 to 1.5 ohm and prints the remote and camera voltages, reproducing the age table.

### Step 5: Starting a car

A car battery (12.6 V, 0.01 ohm) runs the headlamps (about 1.2 ohm in total, roughly 130 W). Then a switch connects the starter motor, which at stall looks like about 0.07 ohm. The terminal voltage falls from about 12.5 V to about 11.0 V while about 154 A flows into the starter, and the lamps lose roughly a quarter of their power. That is the familiar dimming of the dashboard when you turn the key.

Run it:

```bash
uv run python phases/06-sources-batteries-and-measurement/02-internal-resistance/code/main.py
```

## Use It

- **Battery testers.** A cheap battery tester is not just a voltmeter: it puts a fixed load (a few ohms) across the cell while it measures, so a tired cell with high r shows a low reading.
- **Datasheets.** Battery datasheets list internal resistance, often measured with a 1 kHz AC signal ("AC impedance") and sometimes by a DC pulse method similar to our two-load method. A fresh alkaline AA is typically 0.1 to 0.3 ohm; a NiMH AA around 0.02 to 0.05 ohm; an 18650 lithium-ion cell around 0.02 to 0.06 ohm; a CR2032 coin cell 10 ohm or much more.
- **Why NiMH beats alkaline in flashes.** Same size, lower voltage (1.2 V), but far lower r, so under a 2 A load the NiMH cell's terminal voltage ends up higher.
- **Electric vehicles and drones.** Pack builders measure r of every cell and group similar cells together, because a cell with higher r heats more and ages faster.
- **Lab supplies and USB chargers.** Their "internal resistance" is made very small electronically, but the cable is not: 1 m of thin USB cable can add 0.2 to 0.3 ohm round trip.

## Try It in the Lab

A CR2032 coin cell (3.0 V EMF, about 15 ohm inside) powers a radio module. The module needs at least 2.7 V at its pins, and it must draw at least 10 mA to transmit. You choose the resistor that represents how hard the module works.

Think about it before you press RUN:

- Which way does a smaller load resistance push the current? And the voltage?
- Write the terminal voltage for each candidate with V = 3 * R / (R + 15).
- Is the window between the two goals wide or narrow? What does that tell you about using coin cells for radios?

## Common Mistakes

- **Using an ohmmeter on a battery.** An ohmmeter injects its own small current and measures the voltage it creates. A battery's own voltage swamps that, and you can damage the meter. Use the load method.
- **Too light a second load.** If the two currents are almost the same, the voltage difference is tiny and lost in the meter's last digit. Make the heavy load draw meaningfully more current.
- **Waiting too long under load.** A battery's voltage keeps drifting as it heats and as the chemistry near the electrodes changes. Take the loaded reading quickly.
- **Expecting r to be constant.** It changes with temperature, age, state of charge and how long the load has been on. Our model gives a snapshot.
- **Mixing old and new cells.** In series, the old cell's high r drags the whole string down and can even be driven into reverse. In parallel, the fresh cell discharges into the old one.
- **Confusing efficiency with power.** The load gets the most power at R_L = r, but then half the energy is wasted. A battery system aims for R_L many times r.

## Exercises

1. A 9 V battery reads 9.40 V open and 8.70 V with a 47 ohm load. Find the current and the internal resistance.
2. A cell has E = 1.2 V and r = 0.04 ohm. Find the terminal voltage and the efficiency at a 2 A load current.
3. Three cells of 3.7 V, 0.05 ohm each are put in series. What are E_total and r_total? What is the terminal voltage at 10 A?
4. A cell with E = 1.5 V must keep at least 1.2 V while delivering 0.8 A. What is the largest internal resistance it may have?
5. A pack of two parallel strings of two series cells (1.5 V, 0.2 ohm each) feeds a load. For what load resistance does the pack deliver its maximum power, and what is that power? Check your answer by modifying `two_by_two()` in the script.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Internal resistance | "The battery is getting weak" | The series resistance inside a source; it sets the voltage sag under load |
| Voltage sag | "The voltage drops when I turn it on" | The I * r drop across the internal resistance while current flows |
| Open-circuit voltage | "The battery voltage" | Terminal voltage at zero current; nearly equal to the EMF |
| Efficiency | "How good the battery is" | P_load / P_total = R_L / (R_L + r) for a resistive load |
| Series cells | "More voltage" | EMFs add and internal resistances add |
| Parallel cells | "More capacity" | EMF stays, internal resistance divides by n, current is shared |
| ESR | "A capacitor/battery spec" | Equivalent series resistance: one resistor standing in for all internal losses |

## Further Reading

- Battery University, "BU-802a: How does Rising Internal Resistance affect Performance?" and related articles on measuring internal resistance: https://batteryuniversity.com/article/bu-802a-how-does-rising-internal-resistance-affect-performance
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., the chapter on batteries (internal resistance, series and parallel packs).
- All About Circuits, *Lessons in Electric Circuits*, Volume I (DC), chapter "Batteries and Power Systems": https://www.allaboutcircuits.com/textbook/direct-current/chpt-11/battery-ratings/
- Energizer alkaline handbook and E91 datasheet, for real internal resistance and load curves: https://data.energizer.com/pdfs/alkaline_appman.pdf
