# Energy and Power

> Voltage is energy per charge, current is charge per second, so voltage times current is energy per second. That is power, and it is what you pay for.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 01 (The Physics Underneath), Lesson 04 (Energy, Potential and Voltage) and Lesson 06 (Current as Moving Charge); Phase 00, Lesson 03 (Units and SI Prefixes)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Energy (E) | The ability to make something happen: lift, heat, light, move | Money in a bank account |
| Joule (J) | The unit of energy; about what it takes to lift an apple 1 metre | One coin |
| Power (P) | How fast energy is delivered or used: energy per second | How fast you spend money: euros per hour |
| Watt (W) | The unit of power: one joule per second | Spending one coin every second |
| Kilowatt-hour (kWh) | The energy used by 1000 watts running for one hour: 3.6 million joules | A "bulk pack" of coins, the unit your electricity company sells in |
| Watt-hour (Wh) | The energy of 1 watt for one hour: 3600 joules | A smaller pack, used for batteries |
| Efficiency (η, "eta") | The fraction of energy put in that comes out in the form you wanted | The share of your salary that is left after taxes and fees |
| Heat | Energy carried as the random jiggling of atoms; the most common "waste" form of energy | Money lost to small fees you did not notice |
| Load | The part of a circuit that turns electrical energy into something useful (light, motion, heat) | The shop where you spend the money |
| Conservation of energy | Energy is never created or destroyed, only moved and changed in form | Money only moves between accounts; the bank never prints it |
| Rating | The power, voltage or current a part is designed for, printed on it or in its datasheet | A speed limit sign |

## Learning Objectives

- Explain the difference between energy (an amount) and power (a rate), and convert between joules, watt-hours and kilowatt-hours
- Derive `P = V x I` from the definitions of the volt and the ampere, and check it by counting electrons
- Compute power, energy and cost for real appliances and estimate a monthly electricity bill
- Compute how much energy a battery stores from its voltage and mAh rating, and how long it can run a given load
- Use efficiency to find how much energy ends up as heat, and estimate how long a kettle takes to boil water

## The Problem

Look at the label on a phone charger. It says something like "Output: 5 V ⎓ 2 A". The label on a kettle says "230 V ~ 2000 W". A battery says "3.85 V, 4500 mAh" and sometimes "17.3 Wh". Your electricity bill charges you per "kWh". These numbers are all talking about the same physical thing, energy and how fast it moves, but in different units and from different angles.

Without a clear picture of energy and power you cannot answer simple, practical questions: Will this battery run my project for a day or for an hour? Why does the kettle need a thick cord while the phone charger uses a thin one? Why does a 60 W old-style bulb heat up so much? Is it worth leaving the router on all the time? Will this resistor get too hot and burn?

This lesson pulls together everything in Phase 01. Charge (Lesson 02) is what moves. Voltage (Lesson 04) is how much energy each coulomb of charge carries. Current (Lesson 06) is how many coulombs pass per second. Multiply them and you get the one number that everything in electronics eventually has to respect: power.

## The Physics

### Energy: the thing that is never lost

**Energy** is the capacity to do something physical: to lift a weight, warm water, push a car, make light. It comes in many forms: the energy of motion, the energy of height (gravitational potential energy), chemical energy in fuel and food and batteries, heat, light, and the electric potential energy you met in Lesson 04.

The most important law about energy is **conservation**: energy is never created or destroyed, only moved from place to place and changed from one form to another. A circuit never "makes" energy. A battery turns chemical energy into electrical energy; a lamp turns electrical energy into light and heat; a motor turns it into motion and heat. Following the energy through a circuit is one of the most powerful ways to understand it.

The unit of energy is the **joule** (J), named after James Prescott Joule, a brewer from Manchester who in the 1840s showed with careful experiments that mechanical work, electricity and heat are all forms of the same thing. He measured how much a paddle wheel driven by a falling weight warmed water, and how much a wire carrying a current warmed it, and found that they matched.

How big is one joule? Lifting something raises its energy by

*energy equals mass times the strength of gravity times the height.*

```
E = m x g x h
```

with `m` in kilograms, `g = 9.81 m/s^2` (how strongly Earth pulls), and `h` in metres. Lift a 102 g apple by 1 metre:

```
E = 0.102 kg x 9.81 m/s^2 x 1 m = 1.00 J
```

So **one joule is roughly the energy to lift an apple one metre**. A small amount. A slice of bread has about 300 000 J of food energy; a full phone battery about 62 000 J.

### Power: how fast

**Power** is the rate at which energy is moved or converted: how many joules per second. Read it as a sentence:

*power equals energy divided by the time taken.*

```
P = E / t
```

- `P` is power in **watts** (W), named after James Watt, whose improved steam engines (around 1776) made "how much work per hour" the question everybody cared about.
- `E` is energy in joules (J).
- `t` is time in seconds (s).

**1 watt = 1 joule per second.**

Energy and power are often confused, so here is the cleanest way to keep them apart:

- **Energy** is an **amount**, like the number of litres in a tank or euros in an account.
- **Power** is a **rate**, like litres per second through a tap or euros per hour spent.

A 2000 W kettle and a 10 W phone charger can deliver the same energy, but the kettle does it 200 times faster. Turning the formula around:

```
E = P x t
```

A 10 W charger running for 1 hour delivers 10 x 3600 = 36 000 J.

### Where electrical energy comes from and where it goes

In a flashlight, the battery's chemistry pushes charge to its + terminal, raising each coulomb's electric potential energy by the battery's voltage (Lesson 04: 1 volt = 1 joule per coulomb). As that charge drifts through the bulb's thin filament (Lesson 06), it collides constantly with the metal's atoms and hands its energy over to them. The atoms jiggle harder: the filament gets hot, so hot (around 2500 °C) that it glows. The charge comes back to the battery's - terminal with its energy spent, and the battery lifts it up again.

```
               each coulomb gains 6 J here
                     +  ______
              ------|  battery |------
             |       -  ------        |
             |                        |
             |        conventional    |
             |        current I --->  |
             |                        |
              -------[ bulb ]---------
                each coulomb gives up 6 J here, as light and heat
```

The charge is a delivery vehicle. It goes round and round unchanged. The energy is the cargo: loaded at the battery, unloaded at the bulb.

## The Concept

### Deriving P = V x I

We now have every ingredient. From Lesson 04, **voltage** is energy per unit charge:

```
V = E / Q        so 1 volt = 1 joule per coulomb
```

From Lesson 06, **current** is charge per unit time:

```
I = Q / t        so 1 ampere = 1 coulomb per second
```

Multiply them:

```
V x I = (E / Q) x (Q / t) = E / t = P
```

The `Q` cancels. What is left is energy per time, which is power. Read it as a sentence:

*the power delivered to a part equals the voltage across it times the current through it.*

```
P = V x I
```

The units do the same dance: volt x ampere = (J/C) x (C/s) = J/s = watt. This is why a power supply rated "5 V, 2 A" is a "10 W" supply: 5 x 2 = 10.

It is worth saying where this formula applies. It works for **any** part: a lamp, a motor, a battery, a phone, a resistor, a transistor. `V` must be the voltage **across that part** (between its two terminals) and `I` the current **through it**. In Phase 03 you will combine it with Ohm's law to get two more forms for resistors (`P = I^2 R` and `P = V^2 / R`), but `P = V x I` is the one that is always true.

Worked examples (all printed by the script):

| Device | Voltage | Current | Power |
|---|---|---|---|
| LED on a 9 V battery (whole circuit) | 9 V | 20 mA = 0.020 A | 9 x 0.020 = 0.18 W |
| USB phone charging | 5 V | 2 A | 10 W |
| Car headlight bulb | 12 V | 4.6 A | 55.2 W |
| Laptop charger output | 20 V | 3.25 A | 65 W |
| Electric kettle | 230 V | 8.7 A | 2001 W |

Look at the kettle versus the laptop. The kettle takes 30 times more power, but at 11.5 times the voltage it only needs 8.7 / 3.25 = 2.7 times the current. High voltage lets you move a lot of power with a modest current. That is the whole reason power lines run at hundreds of thousands of volts (Phase 08 and 09).

### Checking P = V x I by counting electrons

Algebra is convincing; counting is more convincing. Take the LED circuit: 9 V and 20 mA.

From Lesson 06, the number of electrons passing per second is

```
N = I / e = 0.020 / 1.602e-19 = 1.248e17 electrons per second
```

From Lesson 04, each electron that falls through 9 V gives up 9 electron-volts:

```
energy per electron = 9 V x 1.602e-19 C = 1.442e-18 J
```

Multiply: joules per electron times electrons per second.

```
1.248e17 x 1.442e-18 = 0.180 J per second = 0.180 W
```

Exactly `9 x 0.020 = 0.18 W`. Of course it is: we multiplied by `e` and divided by `e`. But it shows that `P = V x I` is nothing more than "energy per carrier times carriers per second".

### Joules, watt-hours and kilowatt-hours

The joule is a small unit. For bigger amounts, engineers use **power x time** with time in hours:

```
1 watt-hour     = 1 W x 3600 s     = 3600 J
1 kilowatt-hour = 1000 W x 3600 s  = 3 600 000 J = 3.6 MJ
```

So **1 kWh = 3.6 million joules**. It is the energy a 1000 W heater uses in one hour, or a 100 W device in ten hours, or a 10 W router in a hundred hours.

Converting is just multiplying: a 2000 W kettle used 15 minutes a day for 30 days uses

```
E = 2000 W x 0.25 h/day x 30 days = 15 000 Wh = 15 kWh
```

Notice we kept the power in watts and the time in hours, so the answer came out in watt-hours, and we divided by 1000 for kilowatt-hours. Mixing hours and seconds in one formula is the most common error in energy problems.

### The electricity bill

Your electricity company measures energy in kWh and charges a price per kWh. Here is an estimate for one month (30 days), at an example price of 0.25 EUR per kWh (prices vary a lot by country and year):

| Appliance | Power | Hours per day | kWh per month | Cost |
|---|---|---|---|---|
| Fridge (average draw) | 40 W | 24 | 28.8 | 7.20 EUR |
| LED lighting | 60 W | 5 | 9.0 | 2.25 EUR |
| Laptop | 45 W | 6 | 8.1 | 2.02 EUR |
| Television | 90 W | 3 | 8.1 | 2.02 EUR |
| Electric kettle | 2000 W | 0.25 | 15.0 | 3.75 EUR |
| Washing machine | 500 W | 1 | 15.0 | 3.75 EUR |
| Router | 10 W | 24 | 7.2 | 1.80 EUR |
| **Total** | | | **91.2** | **22.80 EUR** |

Two lessons hide in this table:

1. **Small things that never turn off add up.** The 10 W router costs about half as much as the 2000 W kettle, because it runs 96 times longer each day.
2. **Big power for a short time is not necessarily expensive.** The kettle is the most powerful device in the house but uses less energy than the fridge.

The fridge line uses "average draw". A real fridge compressor takes around 100 to 150 W when running, but it only runs part of the time. The average over a day is what sets the bill.

### Battery energy

A battery label gives a voltage and a charge capacity in mAh (milliamp-hours). From Lesson 06, mAh is a charge: current times time. Multiply by the voltage (energy per charge) and you get energy:

*battery energy equals its voltage times its charge capacity.*

```
E (Wh) = V x capacity (Ah) = V x capacity (mAh) / 1000
```

Worked example, a phone battery of 3.85 V and 4500 mAh:

```
E = 3.85 V x 4.5 Ah = 17.3 Wh
  = 17.3 x 3600 J = 62 370 J
```

This is why airlines ask about Wh, not mAh: a 10 000 mAh power bank at 3.7 V and a 10 000 mAh car battery pack at 12 V store very different energies.

| Battery | Voltage | Capacity | Energy |
|---|---|---|---|
| CR2032 coin cell | 3.0 V | 220 mAh | 0.66 Wh (2376 J) |
| AA alkaline | 1.5 V | 2500 mAh | 3.75 Wh (13 500 J) |
| 9 V block | 9 V | 500 mAh | 4.5 Wh (16 200 J) |
| Phone Li-ion | 3.85 V | 4500 mAh | 17.3 Wh (62 370 J) |
| Laptop pack | 11.4 V | 5000 mAh | 57 Wh |
| Car starter battery | 12 V | 60 Ah | 720 Wh |

Real batteries are less tidy than this: voltage sags as they empty and capacity shrinks at high current and low temperature. Phase 06 looks inside batteries; for now the product V x capacity is a good estimate.

**How long will it last?** Divide stored energy by power drawn:

```
time (h) = energy (Wh) / power (W)
```

The 9 V block powering our 0.18 W LED circuit: 4.5 Wh / 0.18 W = 25 hours. A phone with 17.3 Wh at an average of 1.2 W of use: 17.3 / 1.2 = 14.4 hours.

A surprising comparison: a full car battery holds 720 Wh, which is 2.6 million joules. A 100 g bar of chocolate holds about 2.2 million joules of food energy. Chemistry in food is far denser than chemistry in a lead-acid battery.

### Efficiency: energy that does not do what you wanted

Conservation says energy in equals energy out. But not all the energy out is in the form you wanted. **Efficiency**, written with the Greek letter η ("eta"), is

*efficiency equals useful power out divided by total power in.*

```
η = P_useful / P_in
```

It is a number between 0 and 1, often written as a percentage. Everything that is not useful ends up, almost always, as **heat**:

```
P_wasted = P_in - P_useful = P_in x (1 - η)
```

| Device | Power in | Efficiency | Useful out | Wasted as heat |
|---|---|---|---|---|
| Incandescent bulb (light) | 60 W | ~2 % | 1.2 W of light | 58.8 W |
| LED bulb (light) | 8 W | ~15 % | 1.2 W of light | 6.8 W |
| Phone charger | 12 W | ~85 % | 10.2 W to the phone | 1.8 W |
| Electric motor | 100 W | ~80 % | 80 W of motion | 20 W |
| Electric heater | 1500 W | 100 % | 1500 W of heat | 0 W |

(Light efficiencies here are rough: "useful" means energy that comes out as visible light.) The old bulb and the LED bulb make about the same light, but the old bulb is really a heater that happens to glow. The heater is the one device that is perfectly efficient, because heat is what you wanted.

Heat matters in electronics for a second reason: **parts can only shed so much of it**. A small resistor is rated for 0.25 W. A chip might be rated to dissipate 1 W. Go beyond the rating and the part gets too hot and fails. Every time we compute `P = V x I` for a component in later phases, we will ask: "can it survive this?" (Phase 03, Lesson 05 and Phase 18, Lesson 07).

### Heat in numbers: the kettle

To warm water, you need about 4186 J per kilogram per degree Celsius (water's **specific heat capacity**). One litre of water weighs 1 kg. From 20 °C to 100 °C is 80 degrees:

```
E = 4186 J/(kg °C) x 1 kg x 80 °C = 334 880 J
```

With a 2000 W kettle, if all the electrical energy went into the water:

```
t = E / P = 334 880 J / 2000 W = 167 s = 2.8 minutes
```

Real kettles lose some heat to the air and the kettle body. At 85 % efficiency:

```
t = 334 880 / (2000 x 0.85) = 197 s = 3.3 minutes
```

And the cost: 334 880 J / 3 600 000 J per kWh = 0.093 kWh, about 2.3 cents at 0.25 EUR/kWh. A boiled litre of water costs a couple of cents.

## Build It

Run the script from the repository root:

```
uv run python phases/01-the-physics-underneath/07-energy-and-power/code/main.py
```

### Step 1: Three formulas

```python
import numpy as np

ELECTRON_CHARGE = 1.602176634e-19
GRAVITY = 9.81
JOULES_PER_KWH = 3.6e6
WATER_HEAT_CAPACITY = 4186.0
PRICE_PER_KWH = 0.25


def power(volts, amps):
    return volts * amps


def energy(power_w, seconds):
    return power_w * seconds


def battery_energy_wh(volts, milliamp_hours):
    return volts * milliamp_hours / 1000.0
```

Each function is one line of the lesson: `P = V x I`, `E = P x t`, and `E = V x capacity`. The `/ 1000.0` turns mAh into Ah.

### Step 2: What a joule is, and P = V x I for real devices

`print_what_a_joule_is` computes `m g h` for 0.102 kg lifted 1 m and gets 1.001 J. `print_power_from_definitions` prints the unit argument and then loops over the five devices of the table above:

```python
    for label, volts, amps in devices:
        print(f"{label:24s} {volts:6.1f} V x {amps:6.3f} A = {power(volts, amps):8.2f} W")
```

### Step 3: Count electrons, get the same answer

```python
def print_electron_bookkeeping():
    print("=== The same power, counted electron by electron ===")
    volts = 9.0
    amps = 0.020
    electrons_per_second = amps / ELECTRON_CHARGE
    energy_per_electron = volts * ELECTRON_CHARGE
    total = electrons_per_second * energy_per_electron
    ...
```

Output:

```
Electrons per second          = 1.248e+17
Energy given up per electron  = 1.442e-18 J  (9 eV)
Product                       = 0.180 W
V x I directly                = 0.180 W
```

### Step 4: The monthly bill with numpy arrays

We put powers and hours in numpy arrays so one line computes every appliance at once:

```python
    watts = np.array([w for _, w, _ in appliances])
    hours_per_day = np.array([h for _, _, h in appliances])
    kwh = watts * hours_per_day * days / 1000.0
    cost = kwh * PRICE_PER_KWH
```

`watts * hours_per_day` multiplies element by element (watt-hours per day), `* days` gives watt-hours per month and `/ 1000.0` gives kWh. The last line prints the totals:

```
Total: 91.2 kWh = 3.28e+08 J  -> 22.80 EUR at 0.25 EUR/kWh
```

328 million joules in a month: the kWh exists so nobody has to read numbers like that on a bill.

### Step 5: Batteries and runtime

`print_batteries` applies `battery_energy_wh` to six batteries and also prints joules (`wh * 3600`). `print_runtime` divides stored energy by load power:

```python
def print_runtime():
    print("=== How long will it last? ===")
    stored_wh = battery_energy_wh(9.0, 500.0)
    load_w = power(9.0, 0.020)
    hours = stored_wh / load_w
    ...
```

which prints `9 V block (4.5 Wh) feeding 0.18 W lasts about 25 hours` and `Phone (17.32 Wh) at 1.2 W average lasts about 14.4 hours`.

### Step 6: Efficiency and the kettle

`print_efficiency` splits input power into useful and wasted parts for five devices. `print_kettle` computes the 334 880 J needed for one litre and the time at 100 % and 85 % efficiency (167 s and 197 s), plus the cost in cents (2.3).

```python
def print_kettle():
    print("=== Boiling water with a kettle ===")
    kettle_w = 2000.0
    litres = 1.0
    start_c = 20.0
    end_c = 100.0
    heat_needed = WATER_HEAT_CAPACITY * litres * (end_c - start_c)
    for efficiency in (1.0, 0.85):
        seconds = heat_needed / (kettle_w * efficiency)
        print(f"Efficiency {efficiency * 100:3.0f} %: {heat_needed:.0f} J needed, {seconds:.0f} s = {seconds / 60:.1f} min")
```

## Use It

- **Charger labels.** "5 V ⎓ 3 A" means up to 15 W. USB Power Delivery chargers negotiate higher voltages (9, 15, 20 V) so that a 65 W laptop charger can deliver 20 V x 3.25 A over a cable whose current is limited to a few amps.
- **Resistor power ratings.** Common through-hole resistors are rated 1/4 W (0.25 W); tiny surface-mount 0603 resistors are typically 1/10 W. If `V x I` for a resistor exceeds its rating, it overheats. You will check this routinely from Phase 03 on.
- **Battery Wh limits.** Airline rules commonly allow lithium batteries up to 100 Wh in cabin luggage without approval. A 20 000 mAh power bank at 3.7 V is 74 Wh: allowed.
- **Energy labels.** Appliance energy labels show yearly kWh. A fridge labelled 150 kWh/year costs 150 x 0.25 = 37.50 EUR a year at our example price.
- **Standby power.** A device drawing 0.5 W in standby all year uses 0.5 x 24 x 365 = 4380 Wh = 4.4 kWh, about 1.10 EUR. Small, but a house can have dozens of them.
- **Microcontroller projects.** A small board drawing 30 mA at 3.3 V uses 0.1 W. Two AA batteries (about 2 x 3.75 = 7.5 Wh) would run it for roughly 70 hours, ignoring converter losses. Put it to sleep at 10 µA most of the time and it runs for months (Phase 17).

## Try It in the Lab

Open the lab task **Pick the lantern bulb**. A 6 V battery and a closed switch feed a socket. You must choose a bulb, modelled as a resistor (a hot bulb behaves like a resistor of fixed value), so that the bulb glows with a power between 1 W and 2 W while the battery supplies no more than 0.4 A.

Things to think about before you try parts at random:

- What is the voltage across the socket when the switch is closed?
- For each bulb, what current would flow? You will learn Ohm's law properly in Phase 03; the hint gives you the preview you need.
- Then compute `P = V x I` for each candidate. Which bulb is too greedy, and which too feeble?

## Common Mistakes

- **Confusing power with energy.** "This battery has 10 W" makes no sense; a battery stores energy (Wh). "This kettle uses 2000 W per hour" is also wrong: it uses 2000 W, which is 2000 Wh (2 kWh) per hour.
- **Mixing hours and seconds.** `E = P x t` gives joules only with seconds, and watt-hours only with hours. Pick one and stick to it.
- **Forgetting the 1000 in kWh.** 500 W for 3 h is 1500 Wh, which is 1.5 kWh, not 1500 kWh.
- **Using the wrong voltage in P = V x I.** It must be the voltage across the part you are asking about, not the battery voltage, unless the part is the only thing connected to the battery.
- **Thinking mAh is energy.** mAh is charge. Two batteries with the same mAh store different energies if their voltages differ.
- **Thinking the charge is used up in the load.** The charge circulates; the energy is what the load takes (Lesson 06).
- **Assuming 100 % efficiency.** Chargers, motors and converters always waste some energy as heat. A design that ignores this can overheat.

## Exercises

1. **Unit drill.** Convert: (a) 3 kWh to joules; (b) 500 000 J to Wh; (c) 25 W for 8 hours to kWh.
2. **Power from labels.** A hair dryer draws 7.8 A from a 230 V socket. What is its power? How much does a 10-minute use cost at 0.25 EUR/kWh?
3. **Battery life.** A bike light uses 3 AA alkaline cells in series (4.5 V total) and draws 150 mA. Each cell stores 3.75 Wh. Estimate the run time in hours. (Hint: total energy from all three cells divided by power.)
4. **Electron bookkeeping.** A USB device takes 0.5 A at 5 V. How many electrons pass per second, how many joules does each give up, and does their product equal V x I? Modify `print_electron_bookkeeping` in `main.py` to check.
5. **Efficiency chain.** A solar panel delivers 100 W to a charger that is 90 % efficient, which charges a battery that returns 85 % of the energy stored in it, which drives an LED lamp that turns 30 % of its input into light. How many watts of light come out? How much power ends up as heat in total?

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Energy | "Electricity" | The capacity to do work; conserved; measured in joules |
| Joule (J) | "Energy unit" | The energy to push with 1 newton for 1 metre; about lifting an apple 1 m |
| Power | "How strong it is" | Rate of energy transfer, P = E / t |
| Watt (W) | "Watts" | One joule per second; also volt x ampere |
| P = V x I | "Watts equals volts times amps" | Energy per charge times charge per second, for any part, with V across it and I through it |
| kWh | "Units on the bill" | 1000 W for 1 hour = 3.6 MJ |
| Wh | "Battery size" | 1 W for 1 hour = 3600 J; voltage x amp-hours |
| mAh | "Battery capacity" | A charge, not an energy: milliamps x hours |
| Efficiency η | "How good it is" | Useful power out / power in, between 0 and 1 |
| Heat | "Wasted energy" | Energy as random atomic motion; where nearly all losses end up |

## Further Reading

- Richard Feynman, *The Feynman Lectures on Physics*, Vol. I, chapter 4 ("Conservation of Energy"), free at feynmanlectures.caltech.edu.
- All About Circuits, *Textbook Vol. I (DC)*, chapter 2 "Ohm's Law", section "Power in Electric Circuits" and "Calculating Electric Power".
- David J. C. MacKay, *Sustainable Energy - Without the Hot Air* (UIT Cambridge, 2008), free at withouthotair.com: a brilliant book on estimating energy in kWh per day.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., McGraw-Hill, 2016, chapter 2 (power and energy in circuits).
