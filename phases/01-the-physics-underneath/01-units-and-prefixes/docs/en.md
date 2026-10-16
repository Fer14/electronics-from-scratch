# Units and Prefixes

> A number without a unit is a rumour. A unit without the right prefix is a factor of a thousand waiting to bite you.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 00 (Meet Electricity), especially Lessons 03-06 (charge, current, voltage and power)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| unit | The agreed-upon size of "one" of something | A metre stick: "3 metres" means three of these |
| SI | The International System of Units, the metric system used by science worldwide | The one shared rulebook everyone measures with |
| base unit | One of the seven units that everything else is built from (metre, kilogram, second, ampere, ...) | The basic Lego bricks |
| derived unit | A unit made by multiplying or dividing base units (the volt, the watt, the ohm) | A Lego model built from basic bricks |
| prefix | A letter in front of a unit that multiplies it by a power of ten (k = x 1000, m = / 1000) | "Kilo" in kilogram, "milli" in millimetre |
| conversion | Rewriting a quantity with a different prefix or unit, without changing its size | 1.5 km is the same distance as 1500 m |
| dimensional analysis | Checking a formula by checking that its units come out right | Checking a recipe gives you a cake and not a litre of flour |
| capacitance (F) | How much charge a part stores per volt; unit farad (Phase 07) | A tank's size per metre of water height |
| inductance (H) | How strongly a coil resists changes in current; unit henry (Phase 08) | The heaviness of a flywheel |
| frequency (Hz) | How many times per second something repeats; unit hertz | Beats per minute in music, but per second |
| ampere-hour (Ah, mAh) | An amount of charge: one ampere flowing for one hour | A battery's "tank of charge" |
| watt-hour (Wh, kWh) | An amount of energy: one watt delivered for one hour | A battery's "tank of energy"; what the electricity bill counts |

## Learning Objectives

- Name the SI base units used in electronics (metre, kilogram, second, ampere) and say which derived units (V, Ω, W, J, C, F, H, Hz) are built from them
- Convert confidently between prefixes from pico to giga: 4.7 kΩ = 4700 Ω, 20 mA = 0.02 A, 100 nF = 0.0000001 F
- Do arithmetic with prefixed quantities by converting to base units first, and convert the answer back to a readable prefix
- Check a formula by its units, and spot a wrong formula because its units come out wrong
- Read battery labels in mAh and Wh, convert between them, and explain why Wh is the fair way to compare batteries

## The Problem

In Phase 00 (Meet Electricity) you met the volt, the ampere and the watt as words: the push, the flow and the rate of energy. We kept the numbers small and friendly on purpose. From here on the course starts calculating, and real circuits use numbers that are thousands of times bigger or smaller than one: a few thousandths of an amp through an LED, thousands of ohms in a resistor. This lesson gives you the tools to write and handle those numbers without fear. It opens Phase 01 because every later lesson of this phase uses them.

On 23 September 1999, NASA's Mars Climate Orbiter flew too low into the Martian atmosphere and was lost. The investigation found that one piece of software produced thrust data in pound-force seconds, while the software that used it expected newton seconds. Both sides had correct numbers. The units did not match. A spacecraft of several hundred million dollars was lost to a missing conversion factor of about 4.45.

Electronics has its own version of this trap, and it is usually a factor of 1000. A resistor marked "4k7" is 4700 Ω. Use it as if it were 4.7 Ω and your calculated current is a thousand times too big. A capacitor is labelled "100n"; is that nanofarads, or did someone mean microfarads? A battery says "3000 mAh"; is that more or less energy than a "15 Wh" one? A datasheet gives a leakage current of "5 µA"; your code prints `5e-06`. Are those the same?

Every number in electronics carries a unit and very often a prefix, and confident engineers convert between them without thinking. This lesson builds that habit, one small step at a time.

## The Physics

Units are a human agreement, but what they measure is physical, and the agreement has a history.

In 1791, after the French Revolution, France defined the metre as one ten-millionth of the distance from the North Pole to the equator, to replace hundreds of local measures. The idea spread and in 1960 became the **Système International d'Unités**, the SI. Today it has seven **base units**, defined since 2019 by fixing the exact values of constants of nature, so that anyone in any lab can reproduce them:

| Quantity | Base unit | Symbol | Defined by fixing |
|----------|-----------|--------|-------------------|
| time | second | s | the vibration frequency of the caesium-133 atom |
| length | metre | m | the speed of light |
| mass | kilogram | kg | the Planck constant |
| electric current | ampere | A | the charge of one electron, e = 1.602176634 x 10^-19 C exactly |
| temperature | kelvin | K | the Boltzmann constant |
| amount of substance | mole | mol | the Avogadro number |
| light intensity | candela | cd | the brightness of a specified green light |

Notice the ampere. Since 2019, one ampere is *defined* as the current that carries exactly 1 / (1.602176634 x 10^-19) electron charges per second, about 6.24 x 10^18 electrons per second. Electronics is built right into the foundations of the measuring system.

In electronics we mostly need four base units: **metre, kilogram, second and ampere**. Everything else we use, from the volt to the farad, is **derived**: built by multiplying and dividing those four.

## The Concept

### Derived units: the names of electronics

Here are the derived units you will use in this course, each named after a scientist (which is why their symbols are capital letters, while the unit names are written in lowercase: "volt", symbol "V").

| Quantity | Symbol in formulas | Unit | Unit symbol | Means | Named after |
|----------|-------------------|------|-------------|-------|-------------|
| charge | Q | coulomb | C | ampere x second | Charles-Augustin de Coulomb |
| energy | E or W | joule | J | newton x metre | James Prescott Joule |
| power | P | watt | W | joule per second | James Watt |
| voltage | V | volt | V | joule per coulomb (= watt per ampere) | Alessandro Volta |
| current | I | ampere | A | (base unit) | André-Marie Ampère |
| resistance | R | ohm | Ω | volt per ampere | Georg Ohm |
| capacitance | C | farad | F | coulomb per volt | Michael Faraday |
| inductance | L | henry | H | volt x second per ampere | Joseph Henry |
| frequency | f | hertz | Hz | per second (1/s) | Heinrich Hertz |

Two warnings hiding in that table:

- **The letter V does two jobs.** In a formula, `V` is the *quantity* voltage; after a number, `V` is the *unit* volt. "V = 5 V" reads "the voltage is five volts". Context always tells you which.
- **The letter C also does two jobs.** As a unit, C is the coulomb; as a quantity in a formula, C is capacitance. Phase 07 lives with this; it is never really confusing once you know.

You do not need to remember what the farad and the henry mean yet. They appear here only so that the prefixes and the unit check below have something to work on.

### The prefixes

Electronics spans an enormous range. A watch draws about a millionth of an ampere; a lightning bolt carries tens of thousands. A radio signal at your antenna can be a millionth of a volt; a power line carries hundreds of thousands. Writing all those zeros is tiring and error-prone, so SI uses **prefixes**: a letter in front of the unit that multiplies it by a power of ten.

| Prefix | Symbol | Multiply by | As a number | Example |
|--------|--------|-------------|-------------|---------|
| giga | G | 10^9 | 1 000 000 000 | 3 GHz processor clock |
| mega | M | 10^6 | 1 000 000 | 2.2 MΩ resistor |
| kilo | k | 10^3 | 1 000 | 4.7 kΩ resistor |
| (none) | | 10^0 | 1 | 5 V |
| milli | m | 10^-3 | 0.001 | 20 mA LED current |
| micro | µ (or u) | 10^-6 | 0.000 001 | 10 µF capacitor |
| nano | n | 10^-9 | 0.000 000 001 | 100 nF capacitor |
| pico | p | 10^-12 | 0.000 000 000 001 | 22 pF capacitor |

(The notation 10^3 means 10 x 10 x 10 = 1000, and 10^-3 means 1 / 1000 = 0.001. The next lesson, Lesson 02, is all about powers of ten. For now the "As a number" column is enough.)

Each step in the table is a factor of 1000. Those are the prefixes engineers use day to day. There are others (centi, c = 1/100 as in centimetre; deci; hecto; tera, T = 10^12; femto, f = 10^-15) but in electronics you will rarely see anything except the eight in the table, plus tera for very large numbers and femto for very tiny ones.

Some details matter:

- **Case matters.** `m` (milli, a thousandth) and `M` (mega, a million) differ by a factor of a thousand million. A 1 mΩ resistance is a piece of thick copper; a 1 MΩ resistance is nearly an insulator. Kilo is always lowercase `k`.
- **The micro sign.** The proper symbol is the Greek letter mu, µ. On keyboards and in old datasheets you will often see `u` instead: "10uF" means 10 µF. Very old American parts may say "MFD" or "mfd" and mean microfarads; in modern usage "mF" means millifarads, a thousand times more, so watch out.
- **No space inside, a space before.** Write "4.7 kΩ", not "4.7k Ω" or "4.7 K ohm". The prefix sticks to the unit; the number is separated by a space.
- **One prefix at a time.** Never "1 µµF" (an old way of writing pF) or "1 kkΩ".

### Converting: two ways to think about it

**Way 1: replace the prefix by its number.** The prefix is just a multiplier, so substitute it:

```
   4.7 kΩ  = 4.7 x 1000 Ω        = 4700 Ω
   20 mA   = 20 x 0.001 A        = 0.02 A
   100 nF  = 100 x 0.000000001 F = 0.0000001 F
   2.2 MΩ  = 2.2 x 1 000 000 Ω   = 2 200 000 Ω
   47 pF   = 47 x 10^-12 F       = 0.000000000047 F
```

**Way 2: move the decimal point.** Each step of 1000 is three places:

```
   kilo -> base: move the point 3 places right    4.7   -> 4700.
   milli -> base: move the point 3 places left     20.   -> 0.020
   base -> milli: move the point 3 places right    0.02  -> 20.
   mega -> kilo: move the point 3 places right     2.2   -> 2200.     (2.2 MΩ = 2200 kΩ)
   nano -> micro: move the point 3 places left     100.  -> 0.1       (100 nF = 0.1 µF)
```

A good sanity question: **when the prefix gets smaller, the number must get bigger**, and the other way round. 1 metre is 1000 millimetres: smaller pieces, more of them. If you convert 20 mA to amps and get 20 000, you moved the point the wrong way.

Going the other way, from a raw number to a readable one, pick the prefix that leaves a number between 1 and 1000. This is called **engineering notation** (Lesson 02 gives the full story):

```
   0.001064 A   -> 1.064 mA       (not 1064 µA, not 0.001064 A)
   0.066 W      -> 66 mW
   0.001 s      -> 1 ms
   16 000 000 Hz-> 16 MHz
```

### Resistor shorthand: the letter is the decimal point

On circuit boards and in parts lists you will see codes like `4k7`, `2R2` or `1M5`. This is a printing trick: a decimal point is tiny and easily lost when printed or smudged, so the prefix letter itself stands where the point would be, and `R` stands for "no prefix" (ohms).

```
   4k7  = 4.7 kΩ = 4700 Ω
   2R2  = 2.2 Ω
   1M5  = 1.5 MΩ = 1 500 000 Ω
   470R = 470 Ω
   0R1  = 0.1 Ω
```

The same trick is used for capacitors: `4n7` is 4.7 nF, `2u2` is 2.2 µF.

### Arithmetic with prefixes

The safest rule for a beginner: **convert everything to base units, calculate, then convert the answer back**.

**Example 1.** What current flows when 5 V is across a 4.7 kΩ resistor? (Using the preview I = V / R, read "current equals voltage divided by resistance", which we earn in Phase 03.)

```
   R = 4.7 kΩ = 4700 Ω
   I = V / R  = 5 V / 4700 Ω = 0.001064 A
   0.001064 A = 1.064 mA      (move the point 3 places right)
```

**Example 2.** An LED takes 20 mA from a 3.3 V supply. What power does the circuit draw? (Using the preview P = V x I.)

```
   I = 20 mA = 0.02 A
   P = 3.3 V x 0.02 A = 0.066 W = 66 mW
```

**Example 3.** A 10 kΩ resistor works with a 100 nF capacitor. Multiplying them (you will see in Phase 07 why this product matters) gives:

```
   10 kΩ x 100 nF = 10 000 Ω x 0.000 000 1 F
                  = 0.001 Ω·F
                  = 0.001 s            (an ohm times a farad is a second; see below)
                  = 1 ms
```

With practice you can shortcut: kilo (10^3) times nano (10^-9) is 10^-6, micro, so 10 kΩ x 100 nF = 10 x 100 µs = 1000 µs = 1 ms. But the "convert to base units" method never lets you down, and our code always works in base units.

### Unit sanity checks (dimensional analysis, light version)

Here is a powerful idea. Every derived unit is a product of base units raised to powers. If you write a formula and multiply the units the same way you multiply the numbers, the result must have the unit you expected. If it does not, the formula is wrong, guaranteed.

Start with what we know:

```
   newton (force)  N = kg m / s^2           (mass times acceleration)
   joule (energy)  J = N m = kg m^2 / s^2   (force times distance)
   watt (power)    W = J / s = kg m^2 / s^3
   coulomb         C = A s
   volt            V = W / A = kg m^2 / (s^3 A)
   ohm             Ω = V / A = kg m^2 / (s^3 A^2)
```

You do not need to memorise those strings of base units. What matters is that units multiply and divide exactly like numbers. Let's check a few formulas. P = V x I is the one you met in Phase 00, Lesson 06; the others are previews that later lessons of this phase (and Phase 03) earn properly:

```
   P = V x I      volt x ampere   = (W / A) x A = W            correct
   I = V / R      volt / ohm      = V / (V / A) = A            correct
   Q = I x t      ampere x second = A s = C                    correct
   E = P x t      watt x second   = (J / s) x s = J            correct
   E = V x Q      volt x coulomb  = (J / C) x C = J            correct
```

Now suppose a tired student writes "power equals voltage divided by current", P = V / I. Check the units:

```
   V / I   ->   volt / ampere  =  ohm
```

That is a resistance, not a power. The formula is wrong before you even put numbers in. This check takes ten seconds and catches a surprising fraction of mistakes.

One more fun result, which explains Example 3:

```
   Ω x F = (V / A) x (C / V) = C / A = (A s) / A = s
```

An ohm times a farad is a second. That is why a resistor and a capacitor together set a **time**, the famous RC time constant of Phase 07.

### Battery units: mAh and Wh

Battery labels use two units that are not "pure" SI but are everywhere.

**The ampere-hour (Ah) and milliampere-hour (mAh)** are units of **charge**. One ampere-hour is the charge carried by 1 A flowing for 1 hour:

```
   1 Ah = 1 A x 3600 s = 3600 C
   1 mAh = 0.001 A x 3600 s = 3.6 C
```

A rechargeable AA cell rated 2500 mAh can, ideally, deliver 2500 mA for one hour, 250 mA for ten hours, or 20 mA for

```
   time = charge / current = 2500 mAh / 20 mA = 125 h
```

Note how the "m"s cancel: mAh / mA = h. No conversion needed when the prefixes match.

**The watt-hour (Wh)** is a unit of **energy**. One watt-hour is 1 W for one hour:

```
   1 Wh = 1 W x 3600 s = 3600 J
   1 kWh = 1000 Wh = 3 600 000 J = 3.6 MJ
```

The kilowatt-hour is what your electricity bill counts.

**From mAh to Wh: multiply by the voltage.** Energy = voltage x charge (from E = V x Q above), so

```
   Wh = Ah x V
```

| Battery | Label | Ah | Voltage | Wh | Joules |
|---------|-------|----|---------|----|--------|
| AA NiMH rechargeable | 2500 mAh | 2.5 | 1.2 V | 2.5 x 1.2 = 3.0 | 10 800 |
| Phone battery | 4000 mAh | 4.0 | 3.85 V | 4.0 x 3.85 = 15.4 | 55 440 |
| Power bank | 20 000 mAh | 20 | 3.7 V | 20 x 3.7 = 74 | 266 400 |
| CR2032 coin cell | 225 mAh | 0.225 | 3.0 V | 0.225 x 3.0 = 0.675 | 2430 |

Now you can see why **mAh alone is not a fair comparison**. The phone battery is 4000 / 2500 = 1.6 times the AA in mAh, but 15.4 / 3.0 = 5.1 times in energy, because each coulomb in it is pushed by 3.85 V instead of 1.2 V. Watt-hours include the voltage, so they compare batteries of any kind fairly.

That is also why airlines set their limits in Wh. Most allow lithium power banks up to 100 Wh in the cabin without special approval. Our 74 Wh power bank passes; a 30 000 mAh one at 3.7 V would be 30 x 3.7 = 111 Wh and would need approval.

(Power-bank labels have a further twist: the mAh printed on them is usually counted at the internal cell voltage, 3.6-3.7 V, not at the 5 V of the USB output, and conversion losses eat another 10-20%. So a "20 000 mAh" bank delivers well under 20 000 mAh at 5 V. Wh avoids the confusion.)

A coin cell, for comparison: a quartz watch might draw about 0.01 mA on average (10 µA), so

```
   225 mAh / 0.01 mA = 22 500 hours = 22 500 / 24 / 365 = 2.6 years
```

which matches the experience that watch batteries last a few years. "Ideal" is doing a lot of work in all these numbers: real batteries deliver less at high currents and in the cold, as Phase 06 will show.

## Build It

The program converts labels, decodes resistor codes, does the prefix arithmetic above, checks units with small arrays, and prints the battery table. Run it from the repository root:

```
uv run python phases/01-the-physics-underneath/01-units-and-prefixes/code/main.py
```

### Step 1: The prefixes as a dictionary

```python
PREFIXES = {"p": 1e-12, "n": 1e-9, "u": 1e-6, "µ": 1e-6, "m": 1e-3, "": 1.0, "k": 1e3, "M": 1e6, "G": 1e9}
```

In Python, `1e-9` is how you write 10^-9 (Lesson 02 explains this notation). Both `u` and `µ` map to micro.

### Step 2: Reading a label

```python
def parse_quantity(text):
    match = re.fullmatch(r"\s*([0-9]*\.?[0-9]+)\s*(\S*)\s*", text)
    number, rest = float(match.group(1)), match.group(2)
    if rest in UNITS:
        return number, rest
    prefix, unit = rest[0], rest[1:]
    return number * PREFIXES[prefix], unit
```

The regular expression splits "4.7 kΩ" into the number `4.7` and the rest `kΩ`. If the rest is already a unit, there is no prefix. Otherwise the first letter is the prefix. The reverse direction, `engineering(value, unit)`, picks the prefix that leaves a number between 1 and 1000:

```python
def engineering(value, unit):
    exponent = int(np.floor(np.log10(abs(value)) / 3) * 3)
    ...
    return f"{value / 10 ** exponent:g} {symbol}{unit}"
```

It prints lines like `4.7 kΩ = 4700 Ω = 4.7 kΩ` and `100 nF = 1e-07 F = 100 nF`.

### Step 3: Resistor codes

```python
def parse_resistor_code(code):
    for letter, multiplier in (("R", 1.0), ("k", 1e3), ("M", 1e6)):
        if letter in code:
            whole, fraction = code.split(letter)
            return float(f"{whole or 0}.{fraction or 0}") * multiplier
    return float(code)
```

`"4k7"` splits at `k` into `"4"` and `"7"`, becomes `4.7`, times 1000.

### Step 4: Arithmetic in base units

```python
ohms, _ = parse_quantity("4.7 kΩ")
amps = volts / ohms
```

It prints `1.06383 mA`, `66 mW` and `1 ms`, as in the worked examples.

### Step 5: Unit checks with arrays

Each unit is stored as an array of powers of `[kg, m, s, A]`. Multiplying quantities adds the powers; dividing subtracts them.

```python
DIMENSIONS = {
    "V": np.array([1, 2, -3, -1]),
    "A": np.array([0, 0, 0, 1]),
    "W": np.array([1, 2, -3, 0]),
    ...
}

def combine(first, operator, second):
    if operator == "x":
        return DIMENSIONS[first] + DIMENSIONS[second]
    return DIMENSIONS[first] - DIMENSIONS[second]
```

`V x A` gives `[1, 2, -3, 0]`, which the program recognises as W. `Ω x F` gives `[0, 0, 1, 0]`, a second. And the wrong formula `V / A` comes out as Ω, not W.

### Step 6: Batteries

```python
def battery_summary(name, milliamp_hours, volts):
    amp_hours = milliamp_hours / 1000
    coulombs = amp_hours * 3600
    watt_hours = amp_hours * volts
    joules = watt_hours * 3600
    return name, amp_hours, coulombs, watt_hours, joules
```

It prints the battery table above, 125 hours for the LED, 2.6 years for the watch and the airline verdict.

## Use It

- **Resistor kits** come in values like 10 Ω, 100 Ω, 220 Ω, 470 Ω, 1 kΩ, 4.7 kΩ, 10 kΩ, 100 kΩ, 1 MΩ. On the bag they are often written 220R, 4K7, 1M.
- **Capacitors** span pF to mF. A ceramic disc printed "104" means 10 x 10^4 pF = 100 000 pF = 100 nF (the third digit is the number of zeros, in picofarads). A big electrolytic might say "1000 µF 25 V".
- **Microcontroller datasheets** list supply currents in mA when running and µA or even nA when asleep. The difference between 5 mA and 5 µA is the difference between a battery lasting two days and lasting years.
- **Clock frequencies**: a small microcontroller runs at 16 MHz, a phone processor at around 3 GHz, a quartz watch crystal at 32.768 kHz.
- **Your electricity bill**: if 1 kWh costs 0.25 euros, a 2 kW heater for 3 hours uses 2 x 3 = 6 kWh and costs 1.50 euros.
- **Phone specs**: "4500 mAh" and "17.3 Wh" (often printed in small type on the battery itself) are the same battery seen through two units.

## Common Mistakes

- **Moving the decimal point the wrong way.** Converting to a smaller prefix makes the number bigger. 2 A is 2000 mA, not 0.002 mA.
- **Confusing m and M.** Milli is a thousandth, mega a million. Read the case of every letter.
- **Mixing prefixes in one calculation.** 5 V / 4.7 kΩ is not 1.06 A. Either convert to base units first, or carefully track the prefix (volts per kilo-ohm gives milliamps).
- **Writing "K" for kilo.** Capital K is the kelvin. Kilo is lowercase k, even though many shops write "4K7".
- **Comparing batteries by mAh across voltages.** Use Wh, which includes the voltage.
- **Thinking mAh is a current.** It is a charge: current multiplied by time. A "2000 mAh" battery does not push 2000 mA; it can supply, ideally, 2000 mA for one hour, or 200 mA for ten.
- **Thinking kW is energy.** kW is power; kWh is energy. "This heater uses 2 kW per hour" mixes them up: it uses 2 kW, which is 2 kWh in each hour.
- **Dropping units in your working.** Keep the units next to every number until the end. Most errors show up as a unit that comes out wrong.

## Exercises

1. **Easy.** Convert to base units: 330 Ω, 2.2 kΩ, 15 mA, 470 µF, 33 pF, 12 MHz. (Answers: 330 Ω, 2200 Ω, 0.015 A, 0.00047 F, 0.000000000033 F, 12 000 000 Hz.)
2. **Easy.** Write in engineering notation with a prefix: 0.0047 A, 47 000 Ω, 0.000000022 F, 2 500 000 Hz. (Answers: 4.7 mA, 47 kΩ, 22 nF, 2.5 MHz.)
3. **Medium.** A 9 V battery drives 9 V across a 1k5 resistor. What current flows in mA, and what power is used in mW? (Answers: 9 / 1500 = 0.006 A = 6 mA; 9 x 0.006 = 0.054 W = 54 mW.)
4. **Medium.** Which stores more energy: a 3000 mAh battery at 3.7 V, or a pack of four 2000 mAh NiMH cells (1.2 V each) connected end to end (so 4.8 V, still 2000 mAh)? (Answers: 3.0 x 3.7 = 11.1 Wh against 2.0 x 4.8 = 9.6 Wh, so the first. It also wins on mAh, but by 1.5 times, while in energy it wins by only 1.16 times.)
5. **Hard.** Using unit checks only, decide which of these formulas could possibly be right for an energy in joules: (a) V x I, (b) V x I x t, (c) V / R x t, (d) V x V / R x t. Then, with V = 12 V, R = 6 Ω, t = 10 s, compute the energy from each formula that passes the check. (Answers: (b) and (d) give joules; (a) is watts and (c) is coulombs. (d) gives 12 x 12 / 6 x 10 = 240 J, and (b) with I = V / R = 2 A gives 12 x 2 x 10 = 240 J too.)

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| unit | "volts" | The agreed size of one of a quantity; every number in electronics needs one |
| SI | "the metric system" | The International System of Units: 7 base units, many derived ones, and decimal prefixes |
| prefix | "k" or "m" | A multiplier by a power of ten stuck to the front of a unit |
| engineering notation | "4k7" | Writing a value with a prefix so the number is between 1 and 1000 |
| mAh | "battery capacity" | A charge: milliamps times hours; 1 mAh = 3.6 C |
| Wh | "battery size" | An energy: watts times hours; 1 Wh = 3600 J; the fair way to compare batteries |
| kWh | "kilowatts" | 1000 Wh = 3.6 MJ of energy; what you pay for on the electricity bill |
| dimensional analysis | "checking units" | Multiplying and dividing the units like the numbers to verify a formula |

## Further Reading

- [BIPM, The International System of Units (SI Brochure, 9th edition, 2019)](https://www.bipm.org/en/publications/si-brochure) — the official definition of the SI, including the 2019 redefinition based on fixed constants. Readable sections on the base units and prefixes.
- [NIST, "SI Units" and "Metric (SI) Prefixes"](https://www.nist.gov/pml/owm/metric-si-prefixes) — short, clear reference pages on prefixes and writing style (spaces, capitals, symbols).
- [NASA, Mars Climate Orbiter Mishap Investigation Board Phase I Report (1999)](https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf) — the real report on the unit mix-up that lost a spacecraft.
- [All About Circuits, Volume I (DC), Chapter 4: Scientific Notation and Metric Prefixes](https://www.allaboutcircuits.com/textbook/direct-current/chpt-4/metric-notation/) — more practice with prefixes in circuit calculations.
