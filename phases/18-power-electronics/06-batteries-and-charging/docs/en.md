# Batteries and Charging

> A battery is not a perfect voltage source: its voltage depends on how full it is, it hides a resistance that turns current into heat, and it remembers recent use. Charging a lithium cell safely means pushing a constant current until 4.2 V, then holding 4.2 V while the current fades.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 06 (Sources, Batteries and Measurement), Lessons 02-03 (Internal Resistance, How Batteries Work); Phase 07 (Capacitors), Lesson 08 (Transient Simulation from Scratch); Phase 18 (Power Electronics), Lessons 01-03
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Cell | One electrochemical unit: two electrodes and an electrolyte. A battery is one or more cells. | One bottle in a crate. |
| Capacity | How much charge a cell can deliver, in ampere-hours (Ah) or milliampere-hours (mAh). 1 Ah = 3600 coulombs. | The volume of a water tank. |
| Energy (Wh) | Capacity times voltage, in watt-hours. 1 Wh = 3600 joules. | The tank's volume times how high it is: what it can really do. |
| State of charge (SoC) | How full the cell is, from 0% to 100%. | The fuel gauge. |
| Open-circuit voltage (OCV) | The cell's voltage with no current flowing; it depends on the state of charge. | The water level in the tank. |
| Internal resistance | A resistance inside the cell that makes its terminal voltage sag under load and turns current into heat. | A narrow outlet pipe. |
| Polarization | A slower, extra voltage sag (or rise) that builds up over minutes as chemicals redistribute inside the cell, and relaxes when current stops. | A crowd that takes a while to rearrange after a door opens. |
| C-rate | Current expressed relative to capacity: for a 2.5 Ah cell, 1C = 2.5 A, 0.5C = 1.25 A, 2C = 5 A. | Emptying the tank in one hour (1C), two hours (0.5C), half an hour (2C). |
| Cut-off voltage | The lowest terminal voltage at which discharge must stop to avoid damage (about 2.5-3.0 V for lithium-ion). | The "reserve" mark on the fuel gauge. |
| CC/CV charging | Constant current until the cell reaches its maximum voltage, then constant voltage while the current falls. | Filling a glass fast, then slowly near the brim. |
| Termination current | The current at which a CC/CV charger decides the cell is full (typically C/10 to C/20). | Stopping when the trickle is barely moving. |
| Series / parallel (S, P) | Cells end to end add voltages; side by side add capacities. "3S2P" is three series groups of two cells in parallel. | Stacking tanks to raise the level, or placing them side by side for more volume. |
| BMS | Battery management system: the circuit that watches every cell's voltage, current and temperature, and disconnects or balances them. | The lifeguard at the pool. |

## Learning Objectives

- Model a lithium-ion cell as an OCV that depends on state of charge, an internal resistance, and an RC polarization branch, and solve it at each time step with the simulator
- Convert between Ah, Wh, C-rate and run time, and explain why high currents deliver less capacity and less energy
- Simulate a CC/CV charge, find when the CC phase ends and how long the CV phase lasts, and estimate the round-trip efficiency
- Compute the voltage, capacity, energy and internal resistance of series-parallel packs
- List the safety rules for lithium cells and what a BMS does

## The Problem

Phase 06 met the battery as "a voltage source with some internal resistance". That is fine for a second. Over an hour, a battery is a changing thing: its voltage falls as it empties, it falls more under heavy load, it gets warm, and when you stop drawing current its voltage creeps back up. Then you have to refill it, and lithium cells are unforgiving: charge a little above 4.2 V or too fast when cold and they age quickly; much further and they can catch fire.

Every phone, laptop, drone and electric car has to answer the same questions: how long will it run? How fast can it be charged? When is it full, when is it empty? This lesson builds a small, realistic cell model, discharges it at different currents and charges it the way real chargers do.

## The Physics

### Inside a lithium-ion cell

A lithium-ion cell stores energy by moving lithium ions between two electrodes: graphite (the negative side) and a metal oxide (the positive side). Discharging, ions travel through the electrolyte from the graphite to the oxide while electrons travel the other way through your circuit. That is the current. Charging forces them back. (Phase 06, Lesson 03 covers electrochemistry in more detail.)

The voltage depends on how much lithium is in each electrode, so it falls as the cell empties: about 4.2 V full, 3.6-3.8 V in the middle, 3.0 V nearly empty. This curve is the **open-circuit voltage** curve, a property of the chemistry.

### Three reasons the terminal voltage differs from the OCV

1. **Internal resistance** (tens of milliohms): the electrolyte, electrodes and connections resist current. It acts instantly: `V_terminal = OCV - I x R` while discharging, `+ I x R` while charging.
2. **Polarization**: ions take time to diffuse through the electrodes. Under steady current an extra voltage builds up over minutes, and it relaxes over minutes when the current stops. Electrically, that behaves like a resistor in parallel with a capacitor (time constant `R_p x C_p`).
3. **State of charge changes the OCV** over hours.

Our model:

```
       + terminal
          |
       [ R_int ]               instant sag
          |
          +---[ R_p ]---+
          |             |      slow sag (polarization)
          +---[ C_p ]---+
          |
       ( OCV(SoC) )            depends on how full
          |
       - terminal
```

We use `R_int = 60 mohm`, `R_p = 40 mohm`, `C_p = 40 000 F` (a time constant of `0.04 x 40 000 = 1600 s`, about 27 minutes), for a 2.5 Ah cell. These are made-up but realistic values for a cylindrical 18650-size cell.

### Energy lost as heat

The resistances turn `I^2 x R` into heat. At 1C (2.5 A): `2.5^2 x 0.06 = 0.375 W` in the internal resistance alone. At 4C (10 A): `100 x 0.06 = 6 W`, enough to heat a small cell quickly. Heat is why fast charging needs cooling and why cells have current limits.

## The Concept

### Ah, Wh and C-rate

Capacity is charge: a 2.5 Ah cell can (ideally) give 2.5 A for 1 hour, 0.5 A for 5 hours, or 5 A for half an hour. Energy is charge times voltage. With an average voltage of about 3.7 V:

```
energy = 2.5 Ah x 3.7 V = 9.25 Wh
```

Read it as: "watt-hours are amp-hours times the average voltage". Power banks are often labelled in mAh at 3.7 V, which is why a "10 000 mAh" bank gives far fewer mAh at 5 V: `10 Ah x 3.7 V = 37 Wh`, and at 5 V with 90% conversion efficiency `37 x 0.9 / 5 = 6.7 Ah`.

C-rate turns current into "how many full discharges per hour": `C-rate = I / capacity`.

### Why heavy loads deliver less

The cell must stop when the *terminal* voltage reaches the cut-off (3.0 V). Under a heavy load, `I x R_int` plus the polarization pushes the terminal voltage down, so the cut-off arrives while charge is still inside. In the simulation:

| Current | C-rate | Ah delivered | Wh delivered | Left in the cell at cut-off |
|---------|--------|--------------|--------------|-----------------------------|
| 0.5 A | 0.2C | 2.48 | 9.16 | 0.7% |
| 2.5 A | 1C | 2.42 | 8.57 | 3% |
| 5 A | 2C | 2.29 | 7.81 | 8% |
| 10 A | 4C | 1.33 | 4.36 | 47% |

At 4C, the internal drop is already `10 x 0.06 = 0.6 V` and the polarization adds more, so the terminal voltage hits 3.0 V while the OCV is still around 3.7 V. The energy delivered falls even faster than the charge, because the voltage is lower all the way. The rest of the energy becomes heat. (Let the cell rest and its voltage recovers, and you could draw more at a lower current: that is the polarization relaxing.)

### CC/CV charging

A lithium-ion cell must never be pushed above about 4.2 V (some chemistries 4.35 V or 3.65 V for LiFePO4). But if you simply connected 4.2 V to an empty cell, the current would be `(4.2 - 3.0) / 0.06 = 20 A`: far too much. So chargers do it in two phases:

1. **Constant current (CC):** push a fixed current, typically 0.5C-1C. The terminal voltage climbs as the cell fills (and sits `I x R` above the OCV).
2. **Constant voltage (CV):** once the terminal reaches 4.2 V, hold it there. Now the current is whatever `(4.2 - OCV - polarization) / R_int` allows, and it shrinks as the cell fills.
3. **Termination:** stop when the current falls below C/10 to C/20.

In the simulation, charging at 0.5C (1.25 A):

```
CC phase:   0 to 110 min, terminal climbs from 3.08 V to 4.2 V, cell reaches 91%
CV phase:   110 to 134 min, current falls from 1.25 A to 0.125 A (0.05C)
finished:   about 97.5% charged
```

The CC phase does most of the work. The CV phase adds the last few percent slowly, because the voltage difference driving the current gets smaller and smaller. That is why phones charge "fast to 80%, slow to 100%".

### Round-trip efficiency

Energy in during the charge was 9.33 Wh; a 0.5C discharge gives back about 8.92 Wh. The 4% difference is `I^2 R` heat, both ways. Lithium-ion is one of the most efficient storage technologies; lead-acid batteries typically lose 15-25%.

### Packs

Cells in series add voltage (and internal resistance); cells in parallel add capacity (and divide internal resistance):

```
3S2P of our cell:  voltage   3 x 3.7 V = 11.1 V
                   capacity  2 x 2.5 Ah = 5 Ah
                   energy    11.1 x 5 = 55.5 Wh
                   R_int     3 x 60 / 2 = 90 mohm
```

Series cells must be kept at equal states of charge, otherwise one reaches 4.2 V (or 3.0 V) before the others. The BMS **balances** them, usually by bleeding a little current from the fullest cells through resistors.

### Worked example: how long will it run, and how long to charge?

A gadget draws 120 mA on average from one 2.5 Ah cell (our model). At 0.05C the cell delivers almost its full capacity:

```
run time = 2.5 Ah / 0.12 A = 20.8 h
```

If it has a 1.2 A peak while transmitting by radio, the voltage dips by `1.2 x 0.06 = 72 mV` instantly, plus some polarization. Near the end of the discharge (OCV about 3.3 V) that dip can trip a 3.0 V cut-off early: always check the minimum voltage *under the peak load*.

Charging at 0.5C (1.25 A) takes, roughly:

```
CC phase:  about 90% of 2.5 Ah = 2.25 Ah at 1.25 A  ->  1.8 h  (the simulation: 110 min)
CV phase:  the last few percent, typically another 20-40 minutes
```

So about 2.2 hours, which is why "fast charging" means both a higher CC current (1C or more, with cooling) and accepting that the last 20% is slow.

### Worked example: what a power bank's label really means

A power bank says "10 000 mAh". That is at the cell voltage, 3.7 V:

```
energy = 10 Ah x 3.7 V = 37 Wh
after a 90%-efficient boost to 5 V:  37 x 0.9 = 33.3 Wh
as charge at 5 V:                     33.3 / 5 = 6.66 Ah
```

A phone with a 4000 mAh, 3.85 V battery stores `4 x 3.85 = 15.4 Wh`. Its own charger circuit is perhaps 85% efficient, so it needs `15.4 / 0.85 = 18.1 Wh` from the USB port. The power bank can do `33.3 / 18.1 = 1.84` full charges, not the 2.5 that "10 000 / 4000" suggests.

### Worked example: measuring internal resistance

You can measure a cell's internal resistance with a voltmeter and a known load. At rest the cell reads 3.800 V. Connect a 2.5 A load: the voltage drops at once to 3.650 V (read it within a second, before polarization builds up):

```
R_internal = (3.800 - 3.650) / 2.5 = 0.15 / 2.5 = 0.06 ohm = 60 mohm
```

Wait a few minutes under load and the voltage keeps sinking slowly: that slower sag is the polarization branch of our model. Battery testers and phones' "battery health" estimates track exactly this resistance, which grows as cells age.

### Worked example: why packs need balancing

Three cells in series (3S) are charged to 12.6 V, which should mean 4.2 V each. But suppose one cell has slightly less capacity and arrives first. When the pack reaches 12.6 V the cells might be at 4.30 V, 4.15 V and 4.15 V. The high one is over-charged by 0.1 V on every cycle and ages quickly; on discharge it is the first to reach 3.0 V, so it also limits the usable capacity of the whole pack.

A **balancer** fixes this. The simplest (passive) kind connects a resistor across any cell that is above the others near the end of charge, bleeding, say, 50 mA from it while the others catch up. With a 33 ohm resistor across a 4.2 V cell: `4.2 / 33 = 127 mA` and `4.2 x 0.127 = 0.53 W` of heat, which is why passive balancers only work slowly and only near full charge.

## Build It

### Step 1: The OCV curve

`open_circuit_voltage(soc)` interpolates a table of 12 points, from 3.00 V at 0% to 4.20 V at 100%.

### Step 2: Solving the cell at one instant

```python
def solve_cell(soc, v_polarization, charger):
    circuit = Circuit()
    circuit.voltage_source("OCV", "e", "0", open_circuit_voltage(soc))
    circuit.voltage_source("VP", "p", "e", v_polarization)
    circuit.resistor("RINT", "term", "p", R_INTERNAL)
    ...
```

The OCV and the polarization voltage are *state*: they change slowly, so at each instant they are just voltage sources. The charger is a current source (CC), a voltage source (CV) or, for discharging, a current source pulling current out. The simulator solves for the terminal voltage and the current.

### Step 3: Stepping the state forward

```python
def step_state(soc, v_polarization, current_in, dt):
    soc += current_in * dt / (CAPACITY_AH * 3600)
    v_polarization += dt * (current_in / C_POLARIZATION - v_polarization / (R_POLARIZATION * C_POLARIZATION))
    return soc, v_polarization
```

The state of charge rises by the charge that flowed (current times time) divided by the capacity in coulombs. The polarization capacitor charges by `I / C_p` and leaks through `R_p`: the same step-by-step update you used in Phase 07, Lesson 08 (Transient Simulation from Scratch), here with 30-second steps.

### Step 4: Discharge and CC/CV loops

`discharge(current)` steps until the terminal voltage reaches 3.0 V, adding up charge, energy and heat. `charge_cc_cv(current)` runs the CC phase until the terminal reaches 4.2 V, then the CV phase until the current falls to 0.05C, logging every 10 minutes.

Run it:

```
uv run python phases/18-power-electronics/06-batteries-and-charging/code/main.py
```

You will get the discharge table above, the CC/CV log, the round-trip efficiency, and a table of packs.

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
Cell: 2.5 Ah lithium-ion, R_internal 60 mohm, polarization 40 mohm / 40000 F (tau 27 min)
  open-circuit voltage by state of charge: 0% 3.00 V, 10% 3.45 V, 30% 3.62 V, 50% 3.72 V, 70% 3.86 V, 90% 4.06 V

Discharging from full to the 3.0 V cut-off
   current C-rate     time  Ah out  Wh out  heat Wh left in cell
     0.5 A   0.2C   4.97 h  2.483   9.16    0.118        0.7%
     2.5 A   1.0C   0.97 h  2.417   8.57    0.462        3.3%
     5.0 A   2.0C   0.46 h  2.292   7.81    0.767        8.3%
    10.0 A   4.0C   0.13 h  1.333   4.36    0.812       46.7%

CC/CV charge at 1.25 A (0.5C) up to 4.2 V, stopping when the current falls to 0.05C
     time phase  current  terminal  charge
      0 min    CC  1.250 A   3.075 V    0.0%
     10 min    CC  1.250 A   3.491 V    8.3%
     20 min    CC  1.250 A   3.618 V   16.7%
     30 min    CC  1.250 A   3.694 V   25.0%
     40 min    CC  1.250 A   3.751 V   33.3%
     50 min    CC  1.250 A   3.796 V   41.7%
     60 min    CC  1.250 A   3.840 V   50.0%
     70 min    CC  1.250 A   3.891 V   58.3%
     80 min    CC  1.250 A   3.956 V   66.7%
     90 min    CC  1.250 A   4.028 V   75.0%
    100 min    CC  1.250 A   4.111 V   83.3%
    110 min    CV  1.127 A   4.200 V   91.7%
    120 min    CV  0.302 A   4.200 V   95.8%
    130 min    CV  0.147 A   4.200 V   97.2%
  CC phase ended after 110 min at 91.2% charged; total 134 min, finished at 97.5%
  energy in 9.33 Wh; the same cell gives back about 8.92 Wh at 0.5C (round trip 96%)

Building a pack from these cells
  1S1P: nominal  3.7 V,  2.5 Ah,   9.2 Wh, internal resistance  60.0 mohm
  3S1P: nominal 11.1 V,  2.5 Ah,  27.8 Wh, internal resistance 180.0 mohm
  3S2P: nominal 11.1 V,  5.0 Ah,  55.5 Wh, internal resistance  90.0 mohm
  4S4P: nominal 14.8 V, 10.0 Ah, 148.0 Wh, internal resistance  60.0 mohm
```

## Use It

- **Charger chips:** the TP4056 (a very common 1 A linear CC/CV charger on cheap modules), MCP73831 (small linear charger), BQ24xxx and BQ25xxx (switching chargers that use a buck converter, Lesson 03, so they waste less heat). Their datasheets show the same CC, CV and termination phases, plus a "pre-charge" at a low current for deeply discharged cells.
- **Cell datasheets** give capacity at a stated C-rate and temperature, maximum charge and discharge currents, internal resistance (often "AC impedance at 1 kHz"), and the cut-off and charge voltages. Discharge curves at different C-rates look just like our table.
- **Fuel gauges** in phones estimate state of charge by counting coulombs (integrating current, as our `step_state` does) and correcting with the OCV curve when the cell rests.
- **BMS chips** protect against over-voltage, under-voltage, over-current and over-temperature, and balance series cells.
- **Safety:** never short-circuit a lithium cell (its low internal resistance allows tens of amps), never charge below about 0 C or above about 45 C without checking the datasheet, never puncture or crush cells, and use a proper charger with a correct termination voltage.

## Common Mistakes

- **Confusing mAh and Wh.** Compare batteries of different voltages by Wh.
- **Expecting full capacity at high current.** Internal resistance and polarization reach the cut-off early.
- **Charging lithium cells with a plain voltage source.** Without current limiting, the initial current is enormous.
- **Holding a cell at 4.2 V forever.** Float charging lithium-ion ages it; chargers terminate and restart only when the voltage drops.
- **Mixing old and new cells in a pack.** Different capacities and resistances make them drift apart; the weakest cell sets the pack's limits.
- **Reading the voltage right after use.** Polarization makes the voltage creep back up for many minutes; a rested OCV is a much better state-of-charge indicator.

## Exercises

1. A 3000 mAh, 3.6 V nominal cell: how many Wh? At 600 mA, roughly how long does it last? What C-rate is that? (10.8 Wh; 5 h; 0.2C.)
2. A drone pack is 4S1P of 5 Ah cells with 15 mohm each. What is the pack voltage (nominal 3.7 V per cell), the energy, and the voltage sag at 40 A? (14.8 V; 74 Wh; 40 x 0.06 = 2.4 V.)
3. A charger in CV at 4.2 V sees a cell whose OCV plus polarization is 4.15 V. With R_int = 60 mohm, what is the charge current? (0.05 / 0.06 = 0.83 A.)
4. In `main.py`, double the internal resistance (an aged cell). How do the 2C discharge capacity and the CC phase length change? Why does the charge take longer overall?
5. Harder: add a rest period. After discharging at 2C to the cut-off, let the cell rest for 30 minutes (current 0) and print how the terminal voltage recovers as the polarization relaxes. Then discharge again at 0.2C: how much more charge comes out?

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Capacity | "The mAh" | Charge the cell delivers between full and cut-off, at a stated current |
| Watt-hours | "Battery size" | Energy: Ah times average voltage |
| C-rate | "Fast or slow" | Current divided by capacity (1C empties the cell in about an hour) |
| OCV | "Battery voltage" | Voltage at rest, a function of state of charge |
| Internal resistance | "How strong the battery is" | The series resistance that causes I R sag and I^2 R heat |
| CC/CV | "Proper charging" | Constant current to the maximum voltage, then constant voltage until the current tapers |
| BMS | "Protection board" | Monitors and protects each cell and balances series strings |

## Further Reading

- [Battery University (Cadex)](https://batteryuniversity.com/), articles "BU-409: Charging Lithium-ion" and "BU-501: Basics about Discharging" — practical, well-known explanations of CC/CV and C-rates
- [Texas Instruments, BQ24075 or MCP73831 (Microchip) charger datasheets](https://www.microchip.com/en-us/product/MCP73831) — real CC/CV charge profiles with pre-charge and termination
- Gregory L. Plett, *Battery Management Systems, Volume I: Battery Modeling* (Artech House) — the equivalent-circuit model with OCV, R and RC branches used in this lesson
- [Panasonic NCR18650B datasheet](https://www.batteryspace.com/prod-specs/NCR18650B.pdf) — discharge curves at several currents and temperatures for a real cell
