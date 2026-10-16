# Batteries and Loads

> A source gives energy to charge; a load takes it away. Match them, and the load works as its maker intended.

**Type:** Build
**Prerequisites:** Phase 02 (Your First Circuits), Lesson 01 (The Closed Loop); Phase 01 (The Physics Underneath), Lesson 09 (Energy and Power); Phase 01, Lesson 01 (Units and Prefixes)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Source | A part that gives energy to the charge moving through it, pushing it around the loop | A pump lifting water up to a tank |
| Load | A part that takes energy from the moving charge and turns it into light, heat, motion or sound | A water wheel turned by the falling water |
| Cell | A single chemical unit that makes a voltage, such as one AA | One pump |
| Battery | Strictly, several cells joined together; in everyday speech any cell or group of cells | Several pumps stacked one on top of another |
| Terminal | A metal contact where a wire connects to a part | The two ends of an AA |
| Polarity | Which terminal is + and which is -; for some parts it matters which way round they go | The direction of a one-way door |
| Rating | The voltage, current or power a part was designed for, printed on it or in its datasheet | The "max 60 W" label inside a lamp shade |
| Capacity | How much charge a battery can deliver before it is flat, usually in milliampere-hours (mAh) | The size of a fuel tank |
| Series (cells in) | Cells joined + to - in a chain, so their voltages add | Stacking pumps so each one lifts the water higher |
| LED | Light-emitting diode: a small part that glows when current flows through it in one direction only | A one-way valve that glows when water passes |
| Datasheet | The document a manufacturer publishes with a part's ratings and behaviour | The nutrition label on a food packet |

## Learning Objectives

- Tell a source from a load by asking which way energy flows
- Explain what a battery does in terms of energy per charge, without needing its chemistry
- Compute the voltage of cells stacked in series
- Read a load's rating (volts, amps, watts) and work out whether a given battery suits it
- Explain why polarity matters for some loads (LEDs, motors) and not for others (bulbs, heaters)
- Estimate how long a battery will run a load from its capacity in mAh

## The Problem

You have a drawer full of bulbs and a drawer full of batteries. One bulb says "6 V 0.5 A". One battery says "9 V". Another says "1.5 V". Will the bulb work with either of them? Will it glow brightly, faintly, or flash once and die?

Getting this wrong is how people burn out LEDs in their first five minutes of electronics, how a toy motor ends up spinning sluggishly, and how a heater pad gets dangerously hot. Getting it right is easy once you see the circuit as two kinds of parts: one that **gives** energy (the source) and one that **takes** it (the load). The source sets the voltage. The load, given that voltage, decides how much current it draws. And the product of the two is the power the load turns into light, heat or motion.

This lesson builds that picture slowly, with real numbers from real batteries and real bulbs.

## The Physics

### Energy goes one way around the loop

In Lesson 01 you saw that charge flows around a closed loop and every bit of it returns to the battery. The charge is not used up. What changes as it goes round is its **energy**.

Remember from Phase 01, Lesson 06: a **voltage** of 1 volt between two points means each coulomb of charge gains or loses 1 joule moving between them. So:

- Inside a 3 V battery, every coulomb that passes from the - terminal to the + terminal **gains** 3 joules. The battery is **giving** energy.
- Inside the bulb, every coulomb that passes from the top contact to the bottom contact **loses** about 3 joules. The bulb is **taking** energy and turning it into light and heat.

That is the cleanest definition of the two roles:

```
SOURCE:  current goes IN at -  and comes OUT at +   -> charge gains energy
LOAD:    current goes IN at +  and comes OUT at -   -> charge loses energy
```

(Remember we always use conventional current, from + to - through the outside circuit. Electrons drift the other way, but the energy story is the same.)

### What a battery does inside

A battery cell contains two different materials (for an alkaline AA, zinc and manganese dioxide) separated by a paste called the electrolyte. The chemical reaction between them wants to happen, but it can only happen if electrons travel from one material to the other **through the outside circuit**. That is the trick: the reaction is held hostage until you close the loop. Close it, and the chemistry runs, pushing electrons out of one terminal and accepting them at the other.

The chemistry also fixes **how much energy each coulomb gets**. For the zinc and manganese dioxide pair it is about 1.5 joules per coulomb, so a fresh alkaline cell gives about 1.5 V. A lithium-ion cell uses different materials and gets about 3.7 V. A lead-acid cell (the kind in a car battery) gets about 2.1 V. You cannot make a single zinc cell give 3 V by making it bigger; bigger only means it can keep going longer. We will open up a battery properly in Phase 06, Lesson 03.

When Volta built his pile in 1800, he stacked many zinc-and-copper pairs on top of each other, because one pair gave less than a volt. Stacking was the only way to get a bigger push. We still do exactly that.

### What a load does

A load is anything that converts electrical energy into another form:

| Load | Energy becomes | How |
|------|----------------|-----|
| Incandescent bulb | Light (a little) and heat (mostly) | A thin tungsten filament gets so hot (about 2500 °C) that it glows |
| Heater, toaster, kettle element | Heat | A resistant wire gets hot; heat is the goal |
| LED | Light (mostly) and some heat | Electrons give up energy as light when they cross a special junction (Phase 11) |
| Motor | Motion, plus some heat | Current in a coil pushes against magnets (Phase 08) |
| Speaker, buzzer | Sound | A coil or crystal moves the air |
| Phone charger, laptop | Chemical energy in another battery, computation, light | Many smaller loads inside |

In every case, energy leaves the circuit. Some of it is useful (light, motion), and some always ends up as heat. Nothing converts electrical energy with 100 % efficiency.

### Voltage is set by the source, current by the load

This is the single most useful idea in the lesson. A battery tries to keep the same voltage between its terminals whatever you connect to it. (A real battery sags a little under heavy load; Phase 06, Lesson 02 deals with that. For now treat the voltage as fixed.) The battery does **not** decide how much current flows. The load does.

Connect a 6 V battery to a lantern bulb and about 0.5 A flows. Connect the same battery to a tiny indicator bulb and about 0.05 A flows. Connect it to nothing and 0 A flows. The battery's voltage was 6 V in every case. The current depended on how easy each load made it for charge to get through, which is what **resistance** measures (Phase 03).

Picture the battery as a staircase of a fixed height. The load is a slide from the top back to the bottom. A wide, slippery slide lets lots of children down per second; a narrow, bumpy one lets few. The height of the stairs is the same either way.

### Polarity

Because current goes in at the load's + side and out at its - side, it is natural to ask: what if you connect the battery backwards?

- **Bulbs and heaters** do not care. A hot wire glows just the same whichever way the current goes through it. They have no polarity.
- **LEDs** care a lot. An LED (light-emitting diode) only lets current through in one direction, from its **anode** (the longer leg, marked +) to its **cathode** (the shorter leg, flat side of the case, marked -). Put it in backwards and it simply stays dark; with too much reverse voltage it can be damaged.
- **DC motors** run backwards when the polarity is reversed. Toy cars use this to drive in reverse.
- **Electrolytic capacitors** (Phase 07) and **many chips** can be destroyed by reversed polarity. This is why battery holders have a spring on the - side and a flat contact on the + side, and why devices often include protection against batteries put in the wrong way round.

## The Concept

### Stacking cells: voltages add in series

Read it as a sentence: *when cells are joined + to -, one after another, the total voltage is the sum of the cell voltages.*

```
     +  1.5 V  -   +  1.5 V  -           total: 3.0 V
   ---|=======|-----|=======|---
   +                           -
```

Each cell lifts every coulomb by 1.5 J. After two cells, the coulomb has gained 3 J, so the pair gives 3 V. Some worked examples:

```
2 alkaline AA:     2 x 1.5 V = 3.0 V    (most flashlights)
4 alkaline AA:     4 x 1.5 V = 6.0 V
4 NiMH AA:         4 x 1.2 V = 4.8 V    (rechargeables give a bit less)
9 V battery:       6 x 1.5 V = 9.0 V    (six small cells inside the case)
car battery:       6 x 2.1 V = 12.6 V   (six lead-acid cells)
```

If you open a dead 9 V battery (carefully, and only an alkaline one) you really do find six little cells stacked inside.

Stacking cells in series raises the voltage but **not** the capacity: two 2500 mAh cells in series can still deliver 2500 mAh, just at twice the voltage. (Cells side by side, in parallel, are a different story; Lesson 04 introduces the idea for bulbs.)

### Reading a load's rating

A bulb printed "6 V 0.5 A" is telling you: *if you put 6 V across me, I will draw 0.5 A, and I will shine as designed.* Multiply them to get the power:

```
power = voltage x current
P = V x I = 6 V x 0.5 A = 3 W
```

"Power, P, in watts, equals voltage, V, in volts, times current, I, in amperes." You met this in Phase 01, Lesson 09. One watt is one joule per second, so this bulb turns 3 joules of electrical energy into light and heat every second.

For a hot bulb or a heater we can also squeeze the rating into one number, its resistance when hot, using the preview from Lesson 01 (we earn it properly in Phase 03):

```
resistance = voltage / current
R = V / I = 6 V / 0.5 A = 12 Ω
```

So "a 6 V 0.5 A bulb behaves like a 12 Ω resistor when hot". This lets us predict what happens at any other voltage, at least roughly. Here are four loads worked out the same way:

| Load | Rated V | Rated I | Power P = V x I | Hot resistance R = V / I |
|------|---------|---------|-----------------|---------------------------|
| Flashlight bulb | 3 V | 0.30 A | 0.90 W | 10.0 Ω |
| Lantern bulb | 6 V | 0.50 A | 3.00 W | 12.0 Ω |
| Car side-light bulb | 12 V | 0.42 A | 5.04 W | 28.6 Ω |
| Small 12 V heater pad | 12 V | 2.00 A | 24.0 W | 6.0 Ω |

A warning about the word "roughly": a filament's resistance changes a lot with temperature. A cold tungsten filament has about one tenth of its hot resistance, which is why bulbs usually fail at the moment you switch them on (a big surge of current flows for a few milliseconds). Phase 03, Lesson 07 looks at this. For matching batteries to bulbs, the hot value is the right one to use.

### Matching: what happens at the wrong voltage

Take the lantern bulb (12 Ω when hot, rated 3 W) and try it on five batteries. For each, current = V / R and power = V x I.

```
1.5 V:  I = 1.5 / 12 = 0.125 A   P = 1.5 x 0.125 = 0.19 W   ( 0.06 x rated)  barely glows
3.0 V:  I = 3.0 / 12 = 0.250 A   P = 3.0 x 0.250 = 0.75 W   ( 0.25 x rated)  dim
6.0 V:  I = 6.0 / 12 = 0.500 A   P = 6.0 x 0.500 = 3.00 W   ( 1.00 x rated)  about right
9.0 V:  I = 9.0 / 12 = 0.750 A   P = 9.0 x 0.750 = 6.75 W   ( 2.25 x rated)  burns out quickly
12  V:  I = 12  / 12 = 1.000 A   P = 12  x 1.000 = 12.0 W   ( 4.00 x rated)  burns out quickly
```

Look at the pattern. Going from 3 V to 6 V doubled the current, and the voltage was doubled too, so the power (voltage times current) went up four times (0.75 W to 3 W). Power grows with the **square** of the voltage. That is why "a bit too much voltage" is never a bit too much: 50 % more voltage (9 V instead of 6 V) means 2.25 times the power, and the filament overheats and melts.

(In reality, a filament on too low a voltage stays cooler, its resistance drops, and it draws a bit more current than our fixed 12 Ω predicts, so it is a little brighter than these numbers. The ranking does not change.)

The rule of thumb for simple loads: **use a battery whose voltage matches the load's rated voltage.** A little lower and it works weakly; a little higher and it works hard and dies young; a lot higher and it fails at once.

### LEDs are the exception

An LED does not behave like a resistor at all. A red LED keeps roughly 2 V across itself whatever the current, as long as current flows. If you put it straight across a 5 V battery, the 3 V left over has nothing to limit the current, and the LED is destroyed in a flash. So an LED is always paired with a resistor in series, which takes the extra voltage. With a 150 Ω resistor on 5 V:

```
voltage left for the resistor = 5 V - 2 V = 3 V
current = 3 V / 150 Ω = 0.020 A = 20 mA     (a normal LED current)
```

Turn the battery round and the LED blocks the current entirely: 0 mA, dark. LEDs get their own lesson in Phase 11, Lesson 07; here it is enough to know that they have polarity and need a current-limiting resistor.

### How long will the battery last?

A battery's **capacity** is printed in milliampere-hours (mAh), a unit of charge from Phase 01, Lesson 01. 2500 mAh means "2500 mA for 1 hour", or 250 mA for 10 hours, or 25 mA for 100 hours. So:

```
hours of use = capacity (mAh) / current (mA)
```

And the energy stored is capacity times voltage:

```
energy (Wh) = capacity (Ah) x voltage (V)
```

Worked examples:

```
2 x AA (2500 mAh, 3 V) running a flashlight bulb at 300 mA:
   hours  = 2500 / 300 = 8.3 h
   energy = 2.5 Ah x 3 V = 7.5 Wh = 7.5 x 3600 J = 27 000 J
   check:   0.9 W x 8.33 h x 3600 s/h = 27 000 J   ✓

9 V battery (550 mAh) running a red LED at 20 mA:
   hours  = 550 / 20 = 27.5 h
   energy = 0.55 Ah x 9 V = 4.95 Wh

4 x AA (2500 mAh, 6 V) running the lantern bulb at 500 mA:
   hours  = 2500 / 500 = 5.0 h
   energy = 2.5 Ah x 6 V = 15 Wh
```

These are optimistic: a real battery's voltage drops as it empties, and its usable capacity shrinks at high currents. Phase 06 and Phase 18 handle those details.

## Build It

### Step 1: Stacking cells in series

```python
def stack_voltage(cell_volts, cells_in_series):
    return cell_volts * cells_in_series


cells = [
    ("alkaline AA", 1.5, 2),
    ("alkaline AA", 1.5, 4),
    ("NiMH rechargeable AA", 1.2, 4),
    ("lithium-ion cell", 3.7, 1),
    ("coin cell CR2032", 3.0, 1),
    ("inside a 9 V battery", 1.5, 6),
    ("lead-acid car cell", 2.1, 6),
]
for name, volts, count in cells:
    print(f"  {count} x {name:22s} {volts:.1f} V each -> {stack_voltage(volts, count):5.1f} V")
```

Output (a few of the lines):

```
  2 x alkaline AA            1.5 V each ->   3.0 V
  4 x NiMH rechargeable AA   1.2 V each ->   4.8 V
  6 x inside a 9 V battery   1.5 V each ->   9.0 V
  6 x lead-acid car cell     2.1 V each ->  12.6 V
```

### Step 2: Ratings and hot resistance

```python
def hot_resistance(rated_volts, rated_amps):
    return rated_volts / rated_amps


loads = [
    ("flashlight bulb", 3.0, 0.3),
    ("lantern bulb", 6.0, 0.5),
    ("car side-light bulb", 12.0, 0.42),
    ("small 12 V heater pad", 12.0, 2.0),
]
for name, volts, amps in loads:
    print(f"  {name:22s} rated {volts:5.1f} V {amps:5.2f} A -> {volts * amps:5.2f} W, behaves like {hot_resistance(volts, amps):6.1f} ohm")
```

This prints the same table as in The Concept: 0.90 W and 10 Ω for the flashlight bulb, 3.00 W and 12 Ω for the lantern bulb, and so on.

### Step 3: Matching a bulb to five batteries

We use a numpy array of battery voltages, so one line computes all five currents at once (numpy divides element by element).

```python
bulb_ohms = hot_resistance(6.0, 0.5)
rated_power = 6.0 * 0.5
battery_volts = np.array([1.5, 3.0, 6.0, 9.0, 12.0])
currents = battery_volts / bulb_ohms
powers = battery_volts * currents
for volts, amps, watts in zip(battery_volts, currents, powers):
    ratio = watts / rated_power
    print(f"  {volts:5.1f} V battery: {amps:5.3f} A, {watts:6.2f} W = {ratio:5.2f} x rated -> {verdict(ratio)}")
```

`verdict` turns the power ratio into words: below 0.25 "barely glows", below 0.8 "dim", up to 1.2 "about right", up to 2 "overdriven, short life", above that "burns out quickly". The thresholds are our own rough choices for illustration, not an industry standard.

```
    1.5 V battery: 0.125 A,   0.19 W =  0.06 x rated -> barely glows
    3.0 V battery: 0.250 A,   0.75 W =  0.25 x rated -> dim
    6.0 V battery: 0.500 A,   3.00 W =  1.00 x rated -> about right
    9.0 V battery: 0.750 A,   6.75 W =  2.25 x rated -> burns out quickly
   12.0 V battery: 1.000 A,  12.00 W =  4.00 x rated -> burns out quickly
```

### Step 4: Polarity and the LED

A very simple LED model: below 2 V nothing flows; above it, the resistor sets the current.

```python
def led_current(applied_volts, series_ohms, forward_drop=2.0):
    if applied_volts <= forward_drop:
        return 0.0
    return (applied_volts - forward_drop) / series_ohms
```

With 5 V the right way round the LED gets 20.0 mA and lights; reversed (-5 V) it gets 0.0 mA and stays dark.

### Step 5: Battery life

```python
for label, capacity_mah, volts, amps in budgets:
    hours = capacity_mah / (amps * 1000.0)
    energy_wh = capacity_mah / 1000.0 * volts
```

Output:

```
  2 x AA (2500 mAh) + flashlight bulb         7.50 Wh stored, about   8.3 h of use
  9 V battery (550 mAh) + red LED at 20 mA    4.95 Wh stored, about  27.5 h of use
  4 x AA (2500 mAh) + lantern bulb           15.00 Wh stored, about   5.0 h of use
```

Run it yourself:

```
cd electronics_from_scratch
uv run python phases/02-your-first-circuits/02-batteries-and-loads/code/main.py
```

## Use It

**Battery labels.** Look at any battery: it shows the nominal voltage (1.5 V, 3.7 V, 9 V) and often the capacity. A typical alkaline AA holds about 2000 to 3000 mAh at low currents. A CR2032 coin cell holds about 220 mAh at 3 V, which is why it runs a watch for years (microamps) but cannot light a bulb (it cannot deliver large currents). A phone's lithium-ion battery is often printed as something like "3.85 V, 4000 mAh, 15.4 Wh"; check: 4 Ah x 3.85 V = 15.4 Wh.

**Bulb bases.** Small incandescent bulbs are stamped with ratings like "2.4 V 0.5 A" or "6 V 0.5 A". Car bulbs say "12 V 21 W" (a brake light), which you can turn into a current: 21 W / 12 V = 1.75 A.

**USB.** A USB port is a 5 V source. A USB fan, lamp or phone is a load designed for 5 V. Because the voltage is standard, anything USB can plug into anything USB. Matching was solved by agreement.

**Mains appliances.** A kettle in Europe is rated "230 V, 2200 W", which means about 2200 / 230 = 9.6 A. Take it to a 120 V country and it draws about half the current and delivers about a quarter of the power: a very slow kettle. (Mains is dangerous; this course stays at 12 V DC or below, see Phase 00, Lesson 08.)

**Motors.** A small toy DC motor might say "3 V". On 1.5 V it turns slowly, on 3 V normally, on 6 V too fast and too hot. A motor does not behave like a fixed resistor (it draws more current when you hold it still), which you will understand in Phase 08.

## Try It in the Lab

Open the lab task "Match the bulb to the battery". You have a 6 V lantern battery and a drawer of four bulbs, each described by its rated voltage and current and by the resistance it behaves like when hot: 1.5 V 0.3 A (5 Ω), 6 V 0.5 A (12 Ω), 12 V 0.25 A (48 Ω) and 24 V 0.1 A (240 Ω). Choose one for the socket.

Think about:

- For each bulb, what current would the 6 V battery push through it? Compare it with the bulb's rated current.
- What power would each bulb turn into light and heat? Compare with the rated power (V x I from its label).
- Which one would flash and die? Which would barely glow?

The goals ask for a current between 0.4 and 0.6 A and a power between 2.5 and 3.5 W.

## Common Mistakes

- **Thinking the battery "decides" the current.** The battery sets the voltage. The load decides the current at that voltage. The same battery gives very different currents to different loads.
- **"A bigger battery gives more power."** A D cell and an AAA cell are both 1.5 V. The D cell lasts longer (more capacity) but pushes exactly as hard. Power depends on voltage and the load, not on battery size.
- **"A little extra voltage is fine."** Power rises with the square of voltage for a resistive load. 50 % too much voltage means more than twice the power.
- **Connecting an LED straight to a battery.** With no resistor, nothing limits the current. Always put a resistor in series.
- **Ignoring polarity.** Bulbs and heaters do not care which way round they are; LEDs, motors, electrolytic capacitors and chips do.
- **Mixing up mAh and mA.** mA is a current (a rate). mAh is an amount of charge (current multiplied by time). A 2500 mAh battery does not "give 2500 mA"; it can give 2500 mA for one hour, or less current for longer.
- **Adding capacities in series.** Two 2500 mAh cells in series give 2500 mAh at double the voltage, not 5000 mAh. (The energy, in Wh, does double.)

## Exercises

1. How many alkaline cells in series do you need for a 4.5 V torch? How many NiMH cells would give about the same voltage? What voltage do they give exactly?

2. A bulb is rated 3.5 V 0.3 A. What power does it use at its rated voltage? What resistance does it behave like when hot? Using that resistance, what current and power would it get from a 4.5 V battery, and by what factor is the power above rated?

3. A 12 V car battery runs a 12 V 21 W brake lamp. What current flows? If the battery's capacity is 45 Ah, how many hours could it run that lamp (ignoring the voltage drop as it empties)? How many Wh are stored?

4. A red LED (2 V) must run at 15 mA from a 9 V battery. What voltage is left for the series resistor? What resistance gives 15 mA? Check your answer with `led_current` in the script.

5. (Harder) Edit `main.py` to sweep the battery voltage from 0 to 12 V in 0.5 V steps for the lantern bulb and print the voltage at which the verdict first becomes "burns out quickly". Then explain, using P = V x V / R, why the power ratio at voltage V equals (V / 6)^2 for this bulb.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Source | "The power", "the battery" | A part where charge gains energy: current enters at - and leaves at + |
| Load | "The thing being powered" | A part where charge loses energy, converted into light, heat, motion or sound: current enters at + and leaves at - |
| Nominal voltage | "It's a 1.5 V battery" | The typical voltage of a cell type, set by its chemistry; the real value drifts with charge level and load |
| Capacity | "How big the battery is" | The total charge it can deliver, in mAh or Ah; multiply by voltage for the stored energy in Wh |
| Rating | "It's a 6 V bulb" | The voltage, current and power a part is designed for; it works as intended near these values |
| Polarity | "Which way round" | Which terminal must be at the higher potential; critical for LEDs, motors, electrolytic capacitors and chips |
| Hot resistance | "Its resistance" | For a filament, the resistance at operating temperature, about ten times its cold value |

## Further Reading

- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, sections on batteries (cell types, voltages, capacities) and on lamps and LEDs.
- All About Circuits, *Lessons in Electric Circuits*, Volume I (DC), chapter 11 "Batteries and Power Systems": https://www.allaboutcircuits.com/textbook/direct-current/chpt-11/electron-activity-chemical-reactions/
- Battery University (Cadex Electronics), articles on primary and secondary cells and how capacity is measured: https://batteryuniversity.com/
- Energizer, *E91 (alkaline AA) product datasheet*, for real capacity versus current curves.
