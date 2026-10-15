# Heat and Thermal Design

> Heat flows from hot to cold the way current flows from high to low voltage, and it obeys its own Ohm's law: temperature rise = power x thermal resistance. Every watt a part dissipates has to find a path to the air, and the path decides how hot the silicon gets.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Lesson 05 (Power and Heat); Phase 18 (Power Electronics), Lessons 01-05; Phase 07 (Capacitors), Lesson 04 (The Time Constant); Phase 05 (Circuit Analysis and Our Simulator), Lesson 05 (Superposition)
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Junction temperature (Tj) | The temperature of the silicon inside a part, where the heat is made. | The temperature of the hob ring itself, not of the kitchen. |
| Case temperature (Tc) | The temperature of the part's package surface or metal tab. | The temperature of the pan. |
| Ambient temperature (Ta) | The temperature of the air around the device. | The kitchen's air. |
| Thermal resistance (theta, or R_th) | How many kelvin (degrees) of temperature difference it takes to push one watt of heat through a path. Units: K/W (same as degrees C per watt). | How thick a coat is: a thicker coat needs a bigger temperature difference for the same heat to escape. |
| theta_JC, theta_CS, theta_SA, theta_JA | Thermal resistance from junction to case, case to heatsink (through the pad or paste), heatsink to air, and junction to air (the whole path). | Layers of clothing, one after another. |
| Heatsink | A piece of metal with fins bolted to a part to spread heat into the air. | A radiator. |
| Thermal interface material | Paste or a pad between part and heatsink to fill tiny air gaps. | The water between a hot pan and a wet towel. |
| Thermal capacitance | How much heat (joules) it takes to raise something by one kelvin: J/K. | How long a pot of water takes to heat compared with an empty pan. |
| Thermal time constant | Thermal resistance times thermal capacitance: how long a part takes to approach its final temperature. | Why a radiator takes minutes to warm up but a hair dryer element seconds. |
| Derating | Using a part below its maximum rating, especially at high temperature, for reliability. | Not driving a car at its top speed all the time. |
| Thermal runaway | Heating that causes more heating, until destruction. | A fire that makes its own wind. |
| Thermal shutdown | A protection circuit that turns a chip off when its junction gets too hot. | An oven's safety cut-out. |

## Learning Objectives

- Use the thermal Ohm's law, `delta_T = P x theta`, to compute junction temperature through a chain of thermal resistances
- Choose the largest heatsink thermal resistance allowed for a given power, ambient and maximum junction temperature
- Model the thermal path as an electrical circuit (power as current, temperature as voltage, thermal resistance as resistance, heat capacity as capacitance) and simulate it with `sim`
- Explain why short pulses heat a part much less than steady power, using superposition of step responses
- Recognise positive thermal feedback (a MOSFET's on-resistance rising with temperature) and the condition for thermal runaway

## The Problem

Lesson 01's linear regulator dissipated 3.5 W turning 12 V into 5 V at 0.5 A. Lesson 03's buck lost 0.15 W in its switches. Lesson 05's motor driver might lose watts in its MOSFETs. Each of those watts heats the silicon, and silicon has limits: typically 125 C or 150 C for the junction, beyond which the part shuts itself down, ages rapidly, or dies. A small plastic package with nothing attached can only get rid of a watt or two before it reaches those limits.

So every power design ends with a thermal question: given the power, how hot does the junction get, and what do I need (copper area, a heatsink, a fan) to keep it under its limit, on the hottest day, inside a closed box? The good news is that you already know the maths: it is Ohm's law and RC circuits, with different units.

## The Physics

### Heat flows down a temperature difference

Heat moves from hot to cold. Through a solid (conduction), across a gap into air (convection), and as infrared light (radiation). For conduction, the heat flow per second (power, in watts) is proportional to the temperature difference:

```
P = delta_T / theta     or equivalently     delta_T = P x theta
```

Read it as: "the temperature rise equals the power flowing times the thermal resistance of the path". Compare with Ohm's law, `V = I x R`:

| Electrical | Thermal |
|------------|---------|
| voltage V (volts) | temperature T (degrees C or kelvin) |
| current I (amps) | heat flow P (watts) |
| resistance R (ohms) | thermal resistance theta (K/W) |
| capacitance C (farads) | heat capacity (J/K) |
| ground (0 V) | ambient temperature (a fixed temperature source) |

A difference of 1 kelvin is the same as a difference of 1 degree Celsius, so K/W and C/W are the same unit.

Convection and radiation are not perfectly linear (they get more effective at higher temperatures), but over normal ranges a constant thermal resistance is a good approximation, and it is what datasheets give.

### Heat capacity makes temperature change slowly

To raise a lump of material by one kelvin takes energy equal to its heat capacity: `mass x specific heat`. Aluminium has about 0.9 J per gram per kelvin, so a 33 g heatsink needs about 30 J/K. The silicon die itself is tiny: around 0.05 J/K. Exactly as a capacitor's voltage changes by `charge / C`, a body's temperature changes by `heat / heat capacity`. Resistances and capacities together give **thermal time constants**: seconds for a bare chip, minutes for a heatsink.

## The Concept

### The chain from junction to air

```
  junction        case          heatsink         air
    Tj --[theta_JC]-- Tc --[theta_CS]-- Ts --[theta_SA]-- Ta
     ^
     | P (watts of heat)
```

Every watt passes through all the resistances in series, so:

```
Tj = Ta + P x (theta_JC + theta_CS + theta_SA)
```

For a TO-220 regulator (the common package with a metal tab and a hole for a screw), typical numbers are `theta_JC` of a few K/W and `theta_JA` (no heatsink, standing in still air) around 50 K/W. We use `theta_JC = 5 K/W`, `theta_CS = 0.5 K/W` (with a thermal pad), `theta_JA = 50 K/W` bare.

### Worked example: is a heatsink needed?

Power 3.5 W, inside a box at 40 C, maximum junction 125 C.

**No heatsink:**

```
Tj = 40 + 3.5 x 50 = 40 + 175 = 215 C        far too hot
```

**What heatsink is needed?** Solve for theta_SA:

```
125 = 40 + 3.5 x (5 + 0.5 + theta_SA)
85 / 3.5 = 24.3 = 5.5 + theta_SA
theta_SA <= 18.8 K/W
```

**With a 15 K/W heatsink:**

```
Tj = 40 + 3.5 x (5 + 0.5 + 15) = 40 + 3.5 x 20.5 = 40 + 71.75 = 111.75 C
Ts = 40 + 3.5 x 15 = 92.5 C
```

It works, but the heatsink is at 92.5 C: painful to touch and heating everything near it. A designer would add margin (a smaller-resistance heatsink, a fan) or, better, reduce the power: a buck converter (Lesson 03) would dissipate a fraction of a watt instead of 3.5 W.

Heatsink catalogues list theta_SA for each profile, often with a curve for different air speeds. A small clip-on TO-220 heatsink is around 20-30 K/W; a palm-sized finned extrusion maybe 3-5 K/W; with a fan, below 1 K/W.

### Thermal circuits are circuits

Because the equations are identical, we can build the thermal path in our circuit simulator: a current source of `P` amps for the power, resistors of `theta` ohms, a voltage source of `Ta` volts for the ambient, and capacitors of the heat capacities in farads. The node voltages *are* the temperatures.

```
                 die 0.05 J/K   case 2 J/K    heatsink 30 J/K
                    ===            ===             ===
                     |              |               |
   P  --->  Tj ------+--[ 5 ]-- Tc -+--[ 0.5 ]-- Ts -+--[ 15 ]--+-- Ta (40 V source)
                     |              |               |           |
                    gnd            gnd             gnd         gnd
```

(The capacitors go to "ground", which here means absolute zero of our temperature scale. Starting them all at 40 means everything starts at ambient.)

### Warming up

In the transient simulation, after switch-on the junction jumps up within a second (the tiny die capacity charges through 5 K/W: time constant 0.25 s), then follows the slow heatsink. The heatsink's own time constant is `theta_SA x C = 15 x 30 = 450 s`, and with the case and junction in the chain the whole thing takes about 1300 s (over 20 minutes) to reach 95% of its final rise. Two lessons:

- **Test thermal designs for long enough.** A design that looks fine after one minute may overheat after twenty.
- **Short overloads are survivable** if they are much shorter than the relevant time constant.

### Short pulses: superposition

What if the part dissipates 50 W, but only for a short pulse? Steady 50 W would give `50 x 20.5 = 1025 K` of rise: instant death. But a pulse of width `w` is a step of +50 W at time 0 plus a step of -50 W at time `w`. The thermal circuit is linear, so (Phase 05, Lesson 05, Superposition) the temperature is the step response minus the same step response shifted by `w`. The simulation gives:

| Pulse | Peak junction rise |
|-------|-------------------|
| 1 ms | 1.0 K |
| 10 ms | 9.8 K |
| 100 ms | 82 K |
| 1 s | 255 K |

For 1 ms, the die just soaks up the energy: `50 W x 1 ms = 0.05 J` into `0.05 J/K` gives exactly 1 K. Datasheets of power MOSFETs give a **transient thermal impedance** curve that encodes the same thing: the effective thermal resistance for a pulse of a given length.

### Thermal feedback and runaway

A MOSFET's on-resistance rises with temperature, roughly +0.5% per kelvin (it can be 1.5-2 times higher at 125 C than at 25 C). More resistance means more `I^2 R` loss, which means more heat, which means more resistance. Write it as a loop:

```
T  ->  R_on = R_25 x (1 + alpha (T - 25))  ->  P = I^2 R_on  ->  T = Ta + theta x P
```

Each degree of temperature rise causes `theta x I^2 x R_25 x alpha` more degrees. Call that the **loop gain** `g`. If `g < 1` the extra heating shrinks each time round and the temperature settles. If `g >= 1` each degree causes a degree or more: there is no balance point, and the temperature climbs until the part fails. That is **thermal runaway**. With `R_25 = 20 mohm`, `alpha = 0.005 /K`, `theta_JA = 40 K/W`:

```
g = 40 x I^2 x 0.02 x 0.005 = 0.004 x I^2       ->  g = 1 at I = 15.8 A
```

At 5 A the MOSFET settles at 64 C; at 10 A it settles at 183 C, above its limit; at 16 A it runs away. (For MOSFETs in *parallel*, the same effect is actually helpful: the hotter one gets more resistance and takes less current, so they share. Bipolar transistors are the opposite: hotter means *more* current, and they need small emitter resistors to share safely.)

### Worked example: the buck's MOSFETs versus the linear regulator

Lesson 03's buck at 1 A had 50 mohm switches. Each one carries the load current for part of the period; together they lose about `1^2 x 0.05 = 0.05 W`, say 0.025 W each. In a tiny SOT-23 package with a theta_JA of about 200 K/W:

```
rise = 0.025 W x 200 K/W = 5 K        ->  Tj = 40 + 5 = 45 C at 40 C ambient
```

No heatsink, no worry. The linear regulator doing the same job needed a heatsink to survive at 3.5 W. Same output, a hundredth of the heat. This, more than anything, is why switching converters took over.

### Worked example: a surface-mount part on copper

A DPAK regulator (a surface-mount package with a big metal tab soldered to the board) dissipates 1.5 W. Its datasheet gives theta_JA = 50 K/W when soldered to one square inch of copper, and 90 K/W with the minimum pad:

```
one square inch:  Tj = 40 + 1.5 x 50 = 115 C     inside a 125 C limit, little margin
minimum pad:      Tj = 40 + 1.5 x 90 = 175 C     far too hot
```

On a board, copper area *is* the heatsink. Doubling the copper helps less and less (the copper itself has thermal resistance), so beyond a few square inches designers add thermal vias to the back layer or a real heatsink.

### Worked example: how long can it survive without the heatsink?

The bare regulator (theta_JA = 50 K/W) at 3.5 W would end at 215 C, far above 125 C. But it does not get there instantly. If the package and its leads have a heat capacity of about 1 J/K, the time constant is `50 x 1 = 50 s`. The temperature follows `T(t) = 40 + 175 x (1 - e^(-t / 50))`. It reaches 125 C when:

```
1 - e^(-t/50) = 85 / 175 = 0.486    ->   e^(-t/50) = 0.514    ->   t = 50 x ln(1 / 0.514) = 33 s
```

Half a minute. Enough for a quick test on the bench, which is exactly how people get fooled: "it worked when I tried it". Then the thermal shutdown circuit (around 150-170 C in most regulators) cycles the output on and off.

## Build It

### Step 1: Steady temperatures with `dc()`

```python
def steady_junction(power, theta_sa=None):
    circuit = Circuit()
    circuit.voltage_source("TAMB", "amb", "0", AMBIENT)
    circuit.current_source("P", "0", "j", power)
    circuit.resistor("RJC", "j", "c", THETA_JC)
    circuit.resistor("RCS", "c", "s", THETA_CS)
    circuit.resistor("RSA", "s", "amb", theta_sa)
    result = circuit.dc()
    return result.v("j"), result.v("c"), result.v("s")
```

The current source pushes `power` amps from ground into the junction node; it flows out through the resistances into the ambient source. The node voltages are the temperatures.

### Step 2: Warming up with `transient()`

`heating_curve` adds the three heat capacities as capacitors starting at 40 (ambient) and simulates 3000 s with 1 s steps.

### Step 3: Pulses by superposition

`step_response` simulates a 50 W step from a zero-degree ambient (so the result is the *rise*), and the script subtracts a shifted copy of it to build each pulse.

### Step 4: The thermal feedback loop

`mosfet_temperature` iterates "temperature gives resistance gives power gives temperature" until it stops changing (or exceeds 2000 C), and `loop_gain` computes `g`.

Run it:

```
uv run python phases/18-power-electronics/07-heat-and-thermal-design/code/main.py
```

You will see the 215 C bare regulator, the 18.8 K/W budget, the heatsink table, the slow warm-up curve, the pulse table and the MOSFET loop.

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
A linear regulator dropping 12 V to 5 V at 0.5 A dissipates 3.5 W; ambient 40 C, maximum junction 125 C
  no heatsink (theta_JA = 50 K/W): Tj = 215.0 C  TOO HOT
  largest heatsink thermal resistance allowed: (125 - 40) / 3.5 - 5.0 - 0.5 = 18.8 K/W
  heatsink 30.0 K/W: junction  164.2 C, case  146.7 C, heatsink  145.0 C  TOO HOT
  heatsink 15.0 K/W: junction  111.7 C, case   94.2 C, heatsink   92.5 C  OK
  heatsink  8.0 K/W: junction   87.2 C, case   69.7 C, heatsink   68.0 C  OK

Warming up after switch-on (15 K/W heatsink, thermal capacities 0.05, 2 and 30 J/K)
  t =     1 s: junction   54.6 C, heatsink   40.0 C
  t =    10 s: junction   60.1 C, heatsink   41.0 C
  t =    60 s: junction   65.2 C, heatsink   46.0 C
  t =   300 s: junction   83.5 C, heatsink   64.3 C
  t =   600 s: junction   96.6 C, heatsink   77.4 C
  t =  1200 s: junction  107.4 C, heatsink   88.2 C
  t =  3000 s: junction  111.6 C, heatsink   92.4 C
  95% of the final rise after 1280 s; heatsink time constant theta_SA x C = 450 s

Short power pulses (superposition of two step responses), 50 W, 15 K/W heatsink
       1 ms pulse: peak junction rise   1.00 K (steady 50 W would give 1025 K)
      10 ms pulse: peak junction rise   9.80 K (steady 50 W would give 1025 K)
     100 ms pulse: peak junction rise  82.47 K (steady 50 W would give 1025 K)
    1000 ms pulse: peak junction rise 254.97 K (steady 50 W would give 1025 K)

A MOSFET carrying DC: on-resistance grows with temperature (20 mohm at 25 C, +0.5%/K, theta_JA 40 K/W)
   5.0 A: loop gain 0.10, after   5 rounds Tj =    63.9 C, R_on   23.9 mohm  fine
  10.0 A: loop gain 0.40, after  11 rounds Tj =   183.3 C, R_on   35.8 mohm  balances, but above a 175 C maximum
  14.0 A: loop gain 0.78, after  41 rounds Tj =   820.3 C, R_on   99.5 mohm  balances, but above a 175 C maximum
  16.0 A: loop gain 1.02, after   9 rounds Tj =  2000.0 C, R_on  213.2 mohm  loop gain >= 1: no balance point, thermal runaway
```

## Use It

- **Datasheets** list "Thermal Information": theta_JA, theta_JC (top and bottom), and sometimes psi_JT (junction to top of package, for estimating Tj from a thermocouple on the case). Note that theta_JA is measured on a standard test board (JEDEC); on your board it can be very different.
- **PCB copper as a heatsink:** surface-mount power parts (DPAK, SOT-223, QFN with exposed pad) sink heat into copper planes. Datasheets and application notes give theta_JA versus copper area; a square inch of 1 oz copper can bring a DPAK down to roughly 40-50 K/W. Thermal vias carry heat to inner and back layers (Phase 21).
- **Thermal shutdown** in regulators and drivers (typically around 150-170 C) protects the chip, but repeatedly hitting it shortens its life. Design so it never triggers in normal use.
- **Reliability:** a common rule of thumb is that many failure mechanisms roughly double in rate for every 10 C rise. Running parts cooler makes products last longer.
- **Electrolytic capacitors** are especially temperature-sensitive: their rated life (for example 2000 hours at 105 C) roughly doubles for every 10 C cooler. Keep them away from heatsinks.
- **Measuring:** a thermocouple or an infrared camera on the case, plus the datasheet's theta_JC, lets you estimate Tj.

## Try It in the Lab

The lab is a thermal circuit: 3.5 W of heat (a current source of 3.5 A), 5 K/W junction-to-case and 0.5 K/W of thermal pad (resistors), and a 40 C box (a 40 V source). Choose the heatsink resistance so the junction stays below 110 C and the heatsink below 85 C. Remember that temperatures add like voltages along a chain of resistors.

## Common Mistakes

- **Using theta_JA when a heatsink is attached.** theta_JA describes the part alone on a test board; with a heatsink, use theta_JC + theta_CS + theta_SA.
- **Designing for room temperature.** Inside a closed box in summer, ambient can be 50-70 C. Use the worst case.
- **Forgetting the interface.** Without paste or a pad, the air gap between case and heatsink can add several K/W.
- **Testing for one minute.** Heatsinks take tens of minutes to reach their final temperature.
- **Ignoring rising resistance.** MOSFET losses at 100 C can be 1.5 times those at 25 C. Use the hot value of R_on.
- **Insulating the tab carelessly.** Many TO-220 tabs are electrically connected to a pin; bolting two of them to one heatsink without insulators can short circuits together.

## Exercises

1. A part dissipates 2 W with theta_JA = 60 K/W at 25 C ambient. What is Tj? What is the most power it can dissipate if Tj must stay under 125 C at 50 C ambient? (145 C; 75 / 60 = 1.25 W.)
2. A MOSFET has theta_JC = 1 K/W; its pad adds 0.3 K/W; it dissipates 8 W at 45 C ambient with Tj max 150 C. Which heatsinks work: 15, 10 or 5 K/W? (Budget: 105 / 8 - 1.3 = 11.8 K/W, so 10 and 5.)
3. A heatsink of 40 g of aluminium (0.9 J/(g K)) has theta_SA = 8 K/W. What is its thermal time constant? (36 J/K x 8 = 288 s.)
4. In `main.py`, find the pulse width at which a 50 W pulse raises the junction by 50 K. Is it closer to 10 ms or 100 ms?
5. Harder: two of our MOSFETs in parallel share 20 A. Using the loop of Step 4 for each (10 A each), does either run away? Now model them sharing a single heatsink: write the thermal circuit with two power sources into two junction nodes, each with its own theta_JC, joined at the heatsink, and solve it with `sim`.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Thermal resistance | "How good the cooling is" | Kelvin of rise per watt along a path, K/W |
| Junction temperature | "Chip temperature" | Temperature of the silicon where power is dissipated |
| theta_JA | "The package's rating" | Junction-to-air resistance on a standard test board |
| Heatsink theta_SA | "Heatsink size" | Sink-to-air resistance; smaller is better |
| Thermal time constant | "Warm-up time" | theta x heat capacity: how fast a part approaches its final temperature |
| Transient thermal impedance | "Pulse rating" | Effective theta for a pulse of given length; much less than steady theta for short pulses |
| Thermal runaway | "It blew up" | Positive feedback where heating raises losses faster than cooling can follow |

## Further Reading

- [Texas Instruments, SPRA953 "Semiconductor and IC Package Thermal Metrics"](https://www.ti.com/lit/an/spra953c/spra953c.pdf) — what theta_JA, theta_JC and psi_JT mean and how to use them
- Infineon, AN2008-03 "Thermal equivalent circuit models" (application note) — transient thermal impedance and Foster/Cauer RC thermal networks for power semiconductors
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 9, section on power dissipation and heatsinking
- Heatsink datasheets from makers such as Aavid (Boyd) or Fischer Elektronik — real theta_SA values for standard heatsink profiles
