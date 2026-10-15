# Power and Heat

> Every resistor is a tiny heater. Power tells you how fast it turns electrical energy into warmth, and heat is what eventually kills parts.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 01 (The Physics Underneath), Lesson 07 (Energy and Power); Phase 03 (Resistance and Ohm's Law), Lesson 03 (Ohm's Law)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Energy | The ability to make something happen: lift, push, warm, light. Measured in joules (J). | The fuel in a car's tank. |
| Power | How fast energy is delivered or used. Measured in watts (W). One watt is one joule every second. | How fast the fuel is burned, not how much is in the tank. |
| Dissipate | To turn electrical energy into heat that leaves the part. | A brake pad turning a car's motion into hot metal. |
| Joule heating | The warming of any conductor when current flows through it. | Rubbing your hands together: friction makes heat. |
| Watt-hour, kilowatt-hour | Energy units used on bills: 1 Wh = 3600 J, 1 kWh = 3 600 000 J. | The number on your electricity bill. |
| Thermal resistance | How many degrees hotter a part gets for each watt it has to get rid of. Measured in kelvin per watt (K/W). | A thick coat: the thicker the coat, the warmer you stay for the same body heat. |
| Ambient temperature | The temperature of the air around the part. | The room temperature. |
| Power rating | The most power the maker says the part can dissipate safely. | The top speed printed on a tyre. |

## Learning Objectives

- Explain where `P = V * I` comes from, using "volts are joules per coulomb" and "amps are coulombs per second"
- Derive the two other forms of the power formula, `P = I^2 * R` and `P = V^2 / R`, from Ohm's law, and pick the one that fits the numbers you have
- Predict whether a bigger or a smaller resistor gets hotter, and explain why the answer depends on whether voltage or current is held fixed
- Convert between watts, joules, and kilowatt-hours
- Estimate how hot a resistor body gets using `temperature rise = power * thermal resistance`

## The Problem

You build a little circuit: a 9 V battery and a 10 ohm resistor. You touch the resistor a second later and it burns your finger. A minute later it smells, the paint turns brown, and a thin line of smoke rises. Nothing in Ohm's law warned you: Ohm's law told you the current (0.9 A), and that number looked harmless.

What Ohm's law did not tell you is how much *energy per second* that resistor was swallowing. The answer is 8.1 watts, and the little resistor was built to handle a quarter of a watt. It was being asked to get rid of more than 30 times the heat it can shed.

Every circuit you will ever build has this second question hiding behind the first: "the current is right, but will something overheat?" Phone chargers, LED lamps, laptop processors and electric kettles are all designed around this question. This lesson gives you the tool to answer it.

## The Physics

### Voltage is energy per charge

In Phase 01, Lesson 04 (Energy, Potential and Voltage) you met voltage as **energy per unit of charge**. A 12 volt battery gives every coulomb of charge that passes through it 12 joules of energy:

```
1 volt = 1 joule per coulomb        (1 V = 1 J/C)
```

Read it as: "one volt means each coulomb gains (or loses) one joule".

### Current is charge per second

In Phase 01, Lesson 06 (Current as Moving Charge) you met current as **charge per unit of time**:

```
1 ampere = 1 coulomb per second     (1 A = 1 C/s)
```

Read it as: "one amp means one coulomb flows past every second".

### Multiply them and the coulombs cancel

Now ask: how much energy does the battery hand out every second? Each coulomb carries `V` joules, and `I` coulombs go by each second. So every second the battery hands out `V` times `I` joules:

```
  joules     coulombs     joules
  ------  x  --------  =  ------  = watts
  coulomb     second      second
```

That is the whole derivation of the most important power formula in electronics:

> Power equals voltage times current.

```
P = V * I
```

Here `P` is power in watts (W), `V` is voltage in volts (V) and `I` is current in amperes (A). Careful: the letter V is used both for the *quantity* voltage and for the *unit* volt. Context tells them apart.

Worked example: a battery at 12 V pushes 0.5 A.

```
P = 12 V * 0.5 A = 6 W     (6 joules every second)
```

### Where does the energy go inside a resistor?

Inside a resistor the electrons are pushed along by the electric field, gain speed, and keep bumping into the vibrating atoms of the material. Each bump hands some of their energy to the atoms, which then vibrate harder. Atoms vibrating harder is exactly what "hotter" means. So a resistor turns all of the electrical energy it receives into heat. This is called **Joule heating**, after James Prescott Joule, who measured it in the 1840s.

The everyday picture: pushing a heavy box across a carpet. You keep pushing (the battery keeps supplying energy), the box moves at a steady speed (steady current), and the carpet and box get slightly warm (heat). None of your effort is stored; all of it turns into warmth.

What the picture gets wrong: the box is one object. In a wire there are about 10^23 electrons, each colliding trillions of times per second, and the "steady speed" is a very slow average drift (Phase 01, Lesson 06). The picture is right about the most important point: a steady current through a resistance means a steady flow of energy into heat.

### Heat must leave

Heat produced inside a part does not vanish. It warms the part until the part is hot enough to push the heat out to the air, the board and the leads as fast as it is produced. Then the temperature stops rising: the part has reached a balance, called **thermal equilibrium**. The more power, the hotter the balance point. If the balance point is above what the materials can stand, the part is damaged.

## The Concept

### Three formulas that say the same thing

For a resistor we also have Ohm's law (Lesson 03):

```
V = I * R
```

"The voltage across a resistor equals the current through it times its resistance." `R` is resistance in ohms (written ohm or the Greek letter omega).

Combine it with `P = V * I` in two ways.

**If you know the current and the resistance**, replace `V` with `I * R`:

```
P = V * I = (I * R) * I = I^2 * R
```

Read it as: "power equals the current squared, times the resistance". `I^2` means `I * I`.

**If you know the voltage and the resistance**, replace `I` with `V / R`:

```
P = V * I = V * (V / R) = V^2 / R
```

Read it as: "power equals the voltage squared, divided by the resistance".

All three give the same number when the values belong to the same resistor:

```
        +12 V
          |
         .-.
         | | 100 ohm
         | |
         '-'
          |
         gnd
```

```
I = V / R = 12 / 100 = 0.12 A

P = V * I     = 12 * 0.12        = 1.44 W
P = I^2 * R   = 0.12 * 0.12 * 100 = 0.0144 * 100 = 1.44 W
P = V^2 / R   = 12 * 12 / 100    = 144 / 100    = 1.44 W
```

Use whichever formula matches the two numbers you already have. That saves a step and a chance to make an arithmetic slip.

### The famous puzzle: does a bigger resistor get hotter or cooler?

Look at the two forms again:

```
P = I^2 * R       bigger R -> more power?
P = V^2 / R       bigger R -> less power?
```

They seem to contradict each other. They do not, because they answer different situations.

**Situation A: the voltage is fixed.** A battery or a wall socket holds the voltage steady and the resistor decides the current. Then use `P = V^2 / R`. With 12 V:

| R (ohm) | I = 12 / R | P = 144 / R |
|---------|-----------|-------------|
| 10 | 1.2 A | 14.4 W |
| 47 | 0.255 A | 3.06 W |
| 100 | 0.12 A | 1.44 W |
| 220 | 0.0545 A | 0.65 W |
| 1000 | 0.012 A | 0.144 W |

Smaller resistance, more current, much more heat. This is why a **short circuit** (Phase 02, Lesson 03), a path with almost zero resistance, gets dangerously hot: `V^2 / R` with `R` near zero is huge.

**Situation B: the current is fixed.** Several resistors in a single loop all carry the same current (Phase 02, Lesson 04). Then use `P = I^2 * R`. With 20 mA (0.02 A):

| R (ohm) | V = 0.02 * R | P = 0.0004 * R |
|---------|-------------|----------------|
| 10 | 0.2 V | 0.004 W |
| 100 | 2 V | 0.04 W |
| 1000 | 20 V | 0.4 W |

Now the biggest resistor gets the hottest. This is why a bad, slightly resistive connection in a high-current cable (say a loose screw terminal carrying 10 A) can melt: the current is set by the load, and the extra resistance right at the terminal turns `I^2 * R` into heat in one tiny spot. With 10 A and just 0.05 ohm of bad contact:

```
P = 10^2 * 0.05 = 100 * 0.05 = 5 W
```

5 W concentrated in a screw terminal the size of a pea is enough to char plastic.

### Notice the square

Both forms have a square. Double the current through a resistor and the heat goes up four times, not two:

```
I = 1 A, R = 2 ohm:  P = 1 * 1 * 2 = 2 W
I = 2 A, R = 2 ohm:  P = 2 * 2 * 2 = 8 W
```

This is why power lines carry electricity at very high voltage and low current: the losses in the long wires are `I^2 * R`, so cutting the current by 10 cuts the wire losses by 100.

### From power to energy

Power is a *rate*. To get the total energy, multiply by how long it lasts:

```
E = P * t
```

"Energy equals power times time", with `E` in joules, `P` in watts, `t` in seconds.

An electric kettle element of 2000 W running for 60 seconds:

```
E = 2000 W * 60 s = 120 000 J
```

Joules get large quickly, so electricity bills use the **kilowatt-hour** (kWh): the energy used by 1000 W for one hour.

```
1 kWh = 1000 W * 3600 s = 3 600 000 J
```

The same kettle running a full hour uses `2000 * 3600 = 7 200 000 J = 2 kWh`.

### How hot does it get? Thermal resistance

The simplest useful model of heating is a straight line:

> The temperature rise of a part equals the power it dissipates times its thermal resistance.

```
temperature rise = P * R_th
T_part = T_ambient + P * R_th
```

`R_th` (read "R thermal") is in kelvin per watt (K/W). A kelvin step is the same size as a degree Celsius step, so a rise of 30 K means 30 degrees Celsius hotter. `T_ambient` is the temperature of the surrounding air.

Notice the shape: it looks exactly like Ohm's law, `V = I * R`, with temperature playing the role of voltage and heat flow (watts) playing the role of current. Engineers really do draw "thermal circuits" this way. Thermal resistance is large for small parts in still air (heat has a hard time leaving) and small for big parts, parts with metal tabs, or parts bolted to a heatsink.

Rough numbers (the real value depends on board, airflow and the maker; always check the datasheet):

| Part | Approximate R_th to air |
|------|------------------------|
| 1/4 W through-hole resistor | ~250 K/W |
| 1/2 W through-hole resistor | ~150 K/W |
| 0603 surface-mount resistor (tiny chip) | ~400 K/W |
| 5 W ceramic-cased resistor | ~30 K/W |

Worked example: 12 V across 1 kohm (1000 ohm).

```
P = V^2 / R = 144 / 1000 = 0.144 W
rise for a 1/4 W part = 0.144 * 250 = 36 K
body temperature      = 25 + 36   = 61 C
```

61 C is hot enough to be uncomfortable to touch but well inside what the resistor can stand. The same 0.144 W in a tiny 0603 chip gives `0.144 * 400 = 57.6 K` of rise: about 83 C. Same power, smaller part, hotter part.

### Why "power rating" is really "temperature rating"

A resistor's datasheet gives a **power rating**, such as 1/4 W. That number is really a promise about temperature: at that power, in the stated ambient temperature, the hottest spot on the part stays below the temperature its materials can stand (often around 155 C for common film resistors). Lesson 06 (Tolerances and Ratings) shows how that rating shrinks when the air around is already hot.

Practical rule used by most designers: **keep a resistor at half its rating or less**. A 1/4 W resistor should normally dissipate at most about 0.125 W. That leaves margin for warm boxes, bad airflow and part-to-part differences.

## Build It

The script `code/main.py` walks through each idea with numbers you can check on a calculator.

### Step 1: Power from energy per charge

```python
charge_per_second = 0.5
energy_per_charge = 12.0
print(f"  energy delivered per second = {energy_per_charge * charge_per_second} J/s")
```

12 joules per coulomb times 0.5 coulombs per second is 6 joules per second, which is 6 W. This is `P = V * I` with the units spelled out.

### Step 2: Three formulas, one answer

```python
def power_from_voltage_and_current(volts, amps):
    return volts * amps


def power_from_current(amps, ohms):
    return amps**2 * ohms


def power_from_voltage(volts, ohms):
    return volts**2 / ohms
```

For 12 V across 100 ohm all three print 1.440 W. If they ever disagree in your own calculations, you have mixed numbers from two different parts.

### Step 3 and Step 4: Fixed voltage versus fixed current

```python
for resistance in [10, 47, 100, 220, 1000, 10000]:
    current = volts / resistance
    print(resistance, current * 1000, power_from_voltage(volts, resistance))
```

The first table shows the power falling as the resistance grows (fixed 12 V). The second table, with a fixed 20 mA, shows the power rising with resistance. Same physics, different constraint.

### Step 5: Energy over time

```python
heater_watts = power_from_voltage(230.0, 26.45)
joules = energy_joules(heater_watts, minutes * 60)
```

A 26.45 ohm element on a 230 V socket dissipates `230^2 / 26.45 = 52900 / 26.45 = 2000 W`: a typical European kettle. One hour of it is 2 kWh.

### Step 6: Temperature rise

```python
def temperature_rise(watts, kelvin_per_watt):
    return watts * kelvin_per_watt
```

The script prints the body temperature of four package sizes, all dissipating the same 0.144 W. The tiny surface-mount chip runs hottest, the big ceramic resistor barely warms up.

### Step 7: The lab question

```python
candidates = np.array([47.0, 100.0, 220.0])
powers = volts**2 / candidates
```

NumPy applies `V^2 / R` to all candidates at once. Only 100 ohm lands between 1 W and 2 W.

Run it:

```
uv run python phases/03-resistance-and-ohms-law/05-power-and-heat/code/main.py
```

## Use It

- **Resistor datasheets.** A common carbon-film resistor series lists 1/4 W (0.25 W) at an ambient temperature of 70 C. Metal-film parts in the same size are often rated 0.4 to 0.6 W. Surface-mount chips range from about 0.05 W (0201, smaller than a grain of salt) to 0.25 W (1206) and up. Ceramic "cement" resistors go to 5, 10, 20 W.
- **LED current resistors.** An LED on a 5 V supply with a 150 ohm resistor carrying 20 mA: the resistor drops about 3 V, so `P = 3 * 0.02 = 0.06 W`. A 1/4 W part is plenty.
- **Heaters.** Kettles, hair dryers, 3D-printer hot ends, rear-window defrosters and the heated bed of a 3D printer are all just resistors designed to dissipate a lot of power on purpose. A 3D-printer hot end commonly uses a 12 V or 24 V, 40 W cartridge: at 12 V that is `R = V^2 / P = 144 / 40 = 3.6 ohm`.
- **Fuses.** A fuse is a short piece of thin wire meant to heat up by `I^2 * R` and melt when the current is too large, opening the circuit before the wiring catches fire.
- **Processors.** A laptop CPU dissipating 15 to 45 W is a pile of billions of tiny resistive paths. Its heatsink and fan exist only to lower the thermal resistance to air.
- **Current sensing.** A "shunt" resistor of 0.01 ohm carrying 10 A dissipates `10^2 * 0.01 = 1 W`, so even a tiny resistance needs a hefty package at high current.

## Try It in the Lab

Open the lab task **"Warm the bottle, don't cook it"**. A 12 V battery drives one heating resistor that you choose from four parts. The goal: the resistor must give off at least 1 W but no more than 2 W.

Things to think about before you drag a part in:

- The whole battery voltage sits across your resistor. Which of the three power formulas uses only the numbers you know?
- Work backwards: what resistance would give exactly 1 W? Exactly 2 W? Is the right answer above or below each of those?
- Check one wrong part on purpose and see which goal fails, and why.

## Common Mistakes

- **Thinking "bigger resistor, more heat" always.** It depends on what is held fixed. Across a fixed voltage the smaller resistor gets hotter.
- **Mixing numbers from different parts.** `P = V * I` needs the voltage *across* a part and the current *through* the same part. Using the battery voltage with the current of a different branch gives nonsense.
- **Forgetting the square.** Doubling the current quadruples the heat. A circuit that is "only a bit over" in current can be far over in power.
- **Forgetting the unit prefixes.** 20 mA is 0.02 A, not 20 A. `0.02^2 * 100 = 0.04 W`, but `20^2 * 100 = 40 000 W`. Always convert to base units first (Phase 00, Lesson 03).
- **Running parts at their full rating.** A 1/4 W resistor dissipating 0.25 W in a closed box is running hot and will age fast. Aim for half the rating.
- **Confusing power and energy.** A 2000 W kettle and a 2000 W heater use the same power. The heater uses far more *energy* because it runs for hours.

## Exercises

1. A 5 V USB supply delivers 2 A to a phone. What power does it deliver? How much energy in one hour, in joules and in watt-hours?
2. A 470 ohm resistor carries 15 mA. Find the voltage across it and the power it dissipates, using two different formulas. Is a 1/4 W part enough with the "half the rating" rule?
3. You want a resistor that dissipates exactly 0.5 W when connected straight across a 9 V battery. What resistance do you need? Which standard value from 120, 150, 180 ohm comes closest, and what power does it actually dissipate?
4. A 1/4 W resistor with a thermal resistance of 250 K/W sits in a box at 40 C and dissipates 0.2 W. What is its body temperature? What would it be at 0.1 W?
5. (Harder) A car headlamp draws 5 A from a 12 V battery through a long cable whose total resistance (both wires together) is 0.08 ohm. How much power is lost in the cable? If you could rebuild the system at 48 V for the same lamp power, what current would the lamp need, and what would the cable lose then (same cable)?

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Power | "How strong the electricity is" | The rate of energy transfer: joules per second, `P = V * I` |
| Watt | "A measure of electricity" | One joule per second |
| Kilowatt-hour | "Kilowatts per hour" | An amount of energy: 1000 W for 1 h = 3.6 million joules |
| Joule heating | "Wires get hot because of friction" | Electrons give energy to the atoms they collide with, raising their vibration (temperature) |
| Dissipation | "Wasted power" | Electrical energy turned into heat; in a heater it is the whole point |
| Thermal resistance | "How heat-proof a part is" | Temperature rise per watt of heat flow, in K/W |
| Power rating | "The part's maximum power" | The power at which the part reaches its maximum safe temperature under stated conditions |

## Further Reading

- [All About Circuits, Vol. I, Chapter 2: "Calculating Electric Power" and "Resistors"](https://www.allaboutcircuits.com/textbook/direct-current/chpt-2/calculating-electric-power/) — the power formulas with more worked examples
- *Practical Electronics for Inventors* (Scherz & Monk), chapter on resistors and power ratings — practical advice on choosing wattage
- *The Art of Electronics* (Horowitz & Hill), Chapter 1 and the section on power dissipation — how professionals think about heat
- A resistor datasheet such as Vishay's MRS25 or Yageo's CFR series — look for the "power rating" and the derating curve
