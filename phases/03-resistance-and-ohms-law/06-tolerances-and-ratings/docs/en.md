# Tolerances and Ratings

> A resistor labelled 1 kohm is not 1 kohm. It is "somewhere near 1 kohm, as long as you don't push it too hard". Good designs work across the whole "somewhere" and stay far from "too hard".

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Lesson 03 (Ohm's Law), Lesson 04 (Resistors and Color Codes) and Lesson 05 (Power and Heat)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Nominal value | The value printed on the part, the one it is "meant" to have. | The "500 g" printed on a bag of pasta. |
| Tolerance | How far the real value is allowed to be from the nominal one, as a percentage. | "500 g plus or minus 10 g": every bag is somewhere in between. |
| Preferred values (E-series) | The standard lists of values that resistors are actually made in, such as E12. | Shoe sizes: you can buy 42 or 43, not 42.37. |
| Worst case | The most extreme combination of all the allowed variations. | Planning a trip assuming every traffic light is red. |
| Rating | A maximum the maker promises the part can survive: power, voltage, temperature. | The maximum load printed on a shelf bracket. |
| Derating | Lowering a rating because the conditions are harsher than the maker assumed (usually: hotter). | A runner who can do 10 km in 50 minutes in spring, but should plan for 60 in a heat wave. |
| Limiting element voltage | The highest voltage you may put across a resistor, no matter how little power it dissipates. | A balloon that pops when stretched too far, even if you blow slowly. |
| Temperature coefficient (tempco) | How much the resistance changes per degree of temperature, in parts per million per kelvin (ppm/K). | A metal ruler that is slightly longer on a hot day. |
| ppm | Parts per million: 1 ppm is 0.0001 %. | One drop of ink in a bathtub of water. |
| Margin | The gap between what a part is asked to do and its limit. | Leaving 10 minutes early "just in case". |

## Learning Objectives

- Read a tolerance band and compute the smallest and largest values a resistor may really have
- Explain why resistors come in the E12 and E24 series and why those numbers look so odd
- Compute the worst-case current in a simple circuit when both the resistor and the supply vary
- Apply a power derating curve to find the safe power at a given ambient temperature
- Find whether a resistor is limited by power or by voltage, using the critical resistance
- Estimate how much a resistor drifts with temperature from its tempco

## The Problem

You design a circuit that needs 9 mA. You put a 9 V battery across a 1 kohm resistor, Ohm's law says `9 / 1000 = 9 mA`, done. You build a hundred of them. Some draw 8.6 mA, some 9.5 mA. When the batteries get old, some draw 7 mA. In summer, inside a hot box, some of the resistors fail after a few months.

None of this is a bug in Ohm's law. It is that real parts are not the perfect numbers on the schematic. Every number on a part has a "plus or minus" and a "no more than" attached to it. Professional engineers spend a large part of their time making sure a circuit still works when every one of those numbers lands at its worst. That is what this lesson is about.

## The Physics

### Why no two resistors are identical

A film resistor is made by coating a ceramic rod with a very thin film of carbon or metal, then cutting a spiral groove into the film to lengthen the path the current must take (Lesson 02, Resistivity and Wires: longer and thinner means more resistance). The film thickness varies a little from batch to batch, the spiral is cut by a machine that is only so precise, and the end caps make slightly different contact. So the factory measures each part and sorts them. A part that comes out within 1 % of 1 kohm can be sold as a 1 % part; one that is off by 4 % is sold as a 5 % part.

### Why heat sets the limits

From Lesson 05: every watt dissipated raises the temperature of the resistor. Hot films slowly change (oxidize, crack, change their crystal structure), so their resistance drifts. Much hotter, the coating chars and the film burns open. The maker picks a maximum "hot spot" temperature, often about 155 C for common film resistors, and the power rating is the power that brings the part to that temperature *when the surrounding air is at a stated temperature*, often 70 C. Hotter air means less room to heat up, so less allowed power. That is derating.

### Why voltage has its own limit

A very large resistor, say 10 Mohm, carries tiny currents and dissipates almost nothing even at hundreds of volts. But the voltage creates a strong electric field (Phase 01, Lesson 03) across the narrow groove of the film spiral. Push it too high and a spark jumps across the groove, burning a path. So resistors also have a **limiting element voltage**, often 200 to 350 V for a common 1/4 W through-hole part, and much less for tiny surface-mount chips.

### Why resistance changes with temperature

In a metal, hotter atoms vibrate more and get in the way of the electrons more often, so resistance rises with temperature. In carbon and in semiconductors, heat frees extra charge carriers, so resistance often falls. Lesson 07 (When Ohm's Law Fails) takes this to the extreme; here we only need the small, nearly straight-line drift that good resistors have.

## The Concept

### Tolerance: a range, not a number

A resistor with nominal value `R` and tolerance `t` (as a fraction, so 5 % is 0.05) may be anywhere in:

```
R_min = R * (1 - t)
R_max = R * (1 + t)
```

Read it as: "the smallest it may be is the nominal value minus t of it; the largest is the nominal value plus t of it".

Worked example: 4.7 kohm at 5 %.

```
R_min = 4700 * (1 - 0.05) = 4700 * 0.95 = 4465 ohm
R_max = 4700 * (1 + 0.05) = 4700 * 1.05 = 4935 ohm
```

On a four-band color code (Lesson 04) the fourth band is the tolerance: gold 5 %, silver 10 %, brown 1 %, red 2 %. Surface-mount chips usually have it only in the datasheet.

### The odd numbers of the E-series

Why are resistors sold as 100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820 ohm, and not 100, 200, 300? Because of tolerance. With 10 % parts, there is no point making 100 and 105 ohm: their ranges would overlap almost completely. The useful thing is to make values whose tolerance ranges just touch, so that *any* resistance you ask for is covered by some value.

To space 12 values evenly on a *ratio* scale across one decade (a factor of 10), each value must be about `10^(1/12) = 1.21` times the previous one. Rounded to two digits, that gives the **E12 series**:

```
1.0  1.2  1.5  1.8  2.2  2.7  3.3  3.9  4.7  5.6  6.8  8.2
```

Multiply by 10, 100, 1000, ... to get every decade: 4.7 ohm, 47 ohm, 470 ohm, 4.7 kohm, 47 kohm and so on.

Check that the ranges touch, with 10 % parts:

```
1000 ohm + 10 % = 1100 ohm
1200 ohm - 10 % = 1080 ohm      (overlaps 1100: no gap)
1800 ohm + 10 % = 1980 ohm
2200 ohm - 10 % = 1980 ohm      (exactly touching)
```

There are also E6 (6 values per decade, 20 % parts), E24 (24 values, 5 %), E96 (96 values, 1 %) and more. In practice, 1 % parts are now so cheap that many designers use E24 or E96 values with 1 % tolerance everywhere.

### Worst-case analysis

Real circuits have more than one thing that varies. The **worst case** is the combination that pushes your result furthest. For a resistor across a battery, the current is `I = V / R`:

- the *largest* current comes from the *highest* voltage and the *smallest* resistance;
- the *smallest* current comes from the *lowest* voltage and the *largest* resistance.

Worked example: a 9 V battery that is about 9.6 V when fresh and about 7.5 V when nearly flat, with a 1 kohm 5 % resistor.

```
nominal:  I = 9.0 V / 1000 ohm = 9.00 mA
minimum:  I = 7.5 V / 1050 ohm = 7.14 mA
maximum:  I = 9.6 V /  950 ohm = 10.11 mA
```

If your circuit only works between 8 and 10 mA, it will fail at both ends. Worst-case analysis tells you this on paper, before you build a hundred.

Worst case is pessimistic on purpose. In a real bag of resistors, most are close to the nominal value, and very few are at the edge. The script simulates a bag of 10 000 resistors where the spread follows a bell curve, and shows that most land within 1 to 2 % even though they are sold as 5 % parts. But "most" is not "all", and if you make thousands of a product, the unlucky ones will appear. Designers use worst case for anything safety-related and statistics (Monte Carlo) when they can accept a small reject rate.

### Power rating and the half-rating rule

From Lesson 05 the power in a resistor is `P = V * I = I^2 * R = V^2 / R`. The **power rating** is the most it may dissipate in the conditions the maker states. Common through-hole sizes are 1/8 W, 1/4 W, 1/2 W, 1 W, 2 W. A widely used design habit is to stay at **half the rating or less**, which keeps the part much cooler and makes it last far longer.

### Derating with temperature

A typical datasheet draws a **derating curve** like this:

```
 allowed power
 (% of rating)
   100 |------------\
       |             \
    50 |              \
       |               \
     0 +-------+-------+----> ambient temperature
       0      70      155  C
```

Read it as: "full power is allowed up to 70 C of surrounding air; from there the allowed power falls in a straight line, reaching zero at 155 C". In between:

```
P_allowed = P_rated * (155 - T_ambient) / (155 - 70)
```

Worked example: a 1/4 W resistor inside a box where the air reaches 100 C.

```
P_allowed = 0.25 * (155 - 100) / 85 = 0.25 * 55 / 85 = 0.25 * 0.647 = 0.162 W
```

So inside that hot box the "1/4 W" part is really a 0.16 W part, and with the half-rating habit you would keep it near 0.08 W. The exact corner temperatures vary by maker and family; always read the curve in the real datasheet.

### Voltage rating and the critical resistance

There are two ceilings on the voltage you may put across a resistor:

1. **Power:** `P = V^2 / R` must stay below the rating, so `V` must stay below `sqrt(P_rated * R)` (`sqrt` is the square root).
2. **Limiting element voltage:** `V` must stay below `V_max`, whatever the power.

For small resistances the power ceiling is lower; for large ones the voltage ceiling is lower. The switch-over point is the **critical resistance**, where both are equal:

```
R_critical = V_max^2 / P_rated
```

For a 1/4 W part with a 250 V limit:

```
R_critical = 250 * 250 / 0.25 = 62 500 / 0.25 = 250 000 ohm
```

| R | Power allows | Allowed voltage | Limited by |
|---|-------------|-----------------|-----------|
| 100 ohm | sqrt(0.25 * 100) = 5 V | 5 V | power |
| 10 kohm | sqrt(0.25 * 10 000) = 50 V | 50 V | power |
| 1 Mohm | sqrt(0.25 * 1 000 000) = 500 V | 250 V | voltage |
| 10 Mohm | 1581 V | 250 V | voltage |

This matters for anything connected to mains voltage or to high-voltage parts (camera flashes, tube amplifiers, power supplies): a chain of several resistors in series is used to share the voltage.

### Temperature coefficient

Over a normal temperature range, a resistor's value changes almost in a straight line:

```
R(T) = R_25 * (1 + alpha * (T - 25))
```

Read it as: "the resistance at temperature T is the resistance at 25 C, times one plus alpha times how many degrees above 25 C you are". `alpha` is the temperature coefficient. Datasheets give it in ppm/K, so 100 ppm/K means `alpha = 100 * 10^-6 = 0.0001` per kelvin.

Worked example: a 10 kohm metal-film resistor with 50 ppm/K, heated from 25 C to 85 C.

```
R(85) = 10 000 * (1 + 50e-6 * (85 - 25))
      = 10 000 * (1 + 50e-6 * 60)
      = 10 000 * (1 + 0.003)
      = 10 030 ohm      (+0.3 %)
```

Typical values: carbon film about -250 to -1000 ppm/K (resistance falls when hot), metal film 25 to 100 ppm/K, precision metal foil 0.2 to 5 ppm/K. For most beginner circuits the tolerance (1 to 5 %) is much larger than the tempco drift; in measuring instruments, it is the other way round.

### Putting it together: choosing a resistor

When you choose a resistor you are really answering four questions:

1. **Value:** what does Ohm's law say? Round to the nearest E-series value and check the result.
2. **Tolerance:** does the circuit still work at `R_min` and `R_max` (and with the supply at its extremes)?
3. **Power:** what is `P` in the worst case? Is it below half the derated rating?
4. **Voltage:** is the voltage across it below the limiting element voltage?

### A full worked example

Goal: a resistor straight across a 24 V supply (which may be 23 V to 25 V) must draw between 4 mA and 6 mA. The box reaches 85 C inside.

```
        +24 V
          |
         .-.
         | |  R = ?
         '-'
          |
         gnd
```

1. **Value.** Nominal: `R = 24 / 0.005 = 4800 ohm`. The nearest E12 value is 4.7 kohm.
2. **Tolerance.** Take a 5 % part: 4465 to 4935 ohm.

   ```
   I_max = 25 V / 4465 ohm = 5.60 mA     (below 6 mA: good)
   I_min = 23 V / 4935 ohm = 4.66 mA     (above 4 mA: good)
   ```

3. **Power.** Worst case is the highest voltage and the lowest resistance:

   ```
   P_max = 25^2 / 4465 = 625 / 4465 = 0.140 W
   ```

   A 1/4 W part derated to 85 C allows `0.25 * (155 - 85) / 85 = 0.206 W`. Half of that is 0.103 W, and 0.140 W is above it. A 1/2 W part derates to 0.41 W, half of which is 0.206 W: comfortable. Choose 1/2 W.
4. **Voltage.** 25 V is far below any common voltage limit (200 V and up). Done.

Result: 4.7 kohm, 5 %, 1/2 W. Notice that the power step changed the part even though Ohm's law was happy from the start.

## Build It

The script `code/main.py` runs each idea with numbers.

### Step 1: The E12 series

```python
E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
for decade in [100, 1000]:
    values = [round(v * decade) for v in E12]
```

It prints two decades and checks that 10 % ranges of neighbours touch or overlap.

### Step 2: Tolerance ranges

```python
def tolerance_range(nominal_ohms, tolerance):
    return nominal_ohms * (1 - tolerance), nominal_ohms * (1 + tolerance)
```

4.7 kohm at 1 %, 5 % and 10 %: 4653 to 4747, 4465 to 4935, 4230 to 5170 ohm.

### Step 3: Worst-case current

The lowest battery voltage divided by the highest resistance gives the minimum current (7.14 mA); the highest voltage over the lowest resistance gives the maximum (10.11 mA).

### Step 4: A simulated bag of resistors

```python
rng = np.random.default_rng(7)
bag = 1000 * (1 + rng.normal(0, 0.05 / 3, size=10_000))
```

`rng.normal` draws numbers from a bell curve. Spreading it so the 5 % edge is three "standard deviations" away is a common rough model of a production line. The fixed seed (`7`) makes the result the same every run. About 45 % of parts land within 1 %, about 99.7 % within 5 %.

### Step 5: Derating

```python
def derated_power(rated_watts, ambient_celsius, knee_celsius=70.0, zero_celsius=155.0):
    ...
    return rated_watts * (zero_celsius - ambient_celsius) / (zero_celsius - knee_celsius)
```

At 100 C ambient it returns 0.162 W, as in the worked example.

### Step 6: Voltage ceiling

```python
def max_safe_voltage(ohms, rated_watts, limiting_volts):
    power_limited_volts = np.sqrt(rated_watts * ohms)
    return min(power_limited_volts, limiting_volts), power_limited_volts
```

It reports which ceiling wins for resistors from 100 ohm to 10 Mohm.

### Step 7: Temperature drift

```python
def resistance_at(nominal_ohms, ppm_per_kelvin, celsius, reference_celsius=25.0):
    return nominal_ohms * (1 + ppm_per_kelvin * 1e-6 * (celsius - reference_celsius))
```

### Step 8: The lab question

The script tries each candidate keep-alive resistor on 5 V and checks the current and the power.

Run it:

```
uv run python phases/03-resistance-and-ohms-law/06-tolerances-and-ratings/code/main.py
```

## Use It

- **Datasheets.** Look up a common metal-film resistor family (for example Vishay MRS25 or Yageo MFR). You will find: tolerance (1 %), tempco (50 or 100 ppm/K), power rating at 70 C, a derating curve, and a "maximum working voltage". Every number in this lesson is on that page.
- **Surface-mount sizes.** Chip resistors are named by size: 0402 (1.0 x 0.5 mm) is often 1/16 W and 50 V; 0603 is often 1/10 W and 75 V; 0805 about 1/8 W and 150 V; 1206 about 1/4 W and 200 V. A small chip can be too small for the *voltage* even if the power is tiny.
- **Mains circuits.** In power supplies, the resistor that slowly drains a high-voltage capacitor (the "bleeder") is often two or three resistors in series, purely to respect the voltage rating.
- **Precision measurement.** A multimeter's internal resistors use 0.1 % parts with very low tempco, because a 1 % error would ruin the reading.
- **USB keep-alive loads.** Many power banks switch off when the load current is below some tens of milliamps. Low-power gadgets add a resistor (or a pulsed load) to keep them on, which is exactly the lab task.

## Try It in the Lab

Open the lab task **"Keep the power bank awake"**. A 5 V power bank turns off below 20 mA. You add a resistor across its output to keep it on. Because the resistors are 1/4 W parts in a warm, closed case, you have decided not to let any of them dissipate more than 0.15 W.

Things to think about:

- The current goal and the power goal push the resistance in opposite directions. Which one sets an upper limit on R, and which one a lower limit?
- Find the window of allowed resistance first, then look for a part inside it.
- Bonus: if your chosen part is a 5 % resistor and it lands at its *largest* allowed value, is the current still above 20 mA?

## Common Mistakes

- **Treating the printed value as exact.** A 5 % part can be 5 % off. If your circuit only works with the exact value, it does not really work.
- **Mixing worst cases.** For the maximum current you want the *smallest* resistance and the *largest* voltage, not both largest.
- **Using the full power rating.** A part at 100 % of its rating runs at its maximum temperature. Use half.
- **Ignoring the ambient temperature.** Ratings are given for a stated air temperature. Inside a sealed box next to a power transistor, the air can be 60 or 80 C.
- **Forgetting the voltage rating on big resistors.** A 10 Mohm resistor across 400 V dissipates only 0.016 W, but it may be over its voltage limit and arc.
- **Asking for a value that does not exist.** You cannot buy a 1234 ohm resistor in E12. Pick the nearest preferred value and check that the result is still acceptable.

## Exercises

1. Find the minimum and maximum resistance of a 330 ohm 10 % resistor and of a 330 ohm 1 % resistor.
2. A 12 V supply that may be anywhere from 11.4 V to 12.6 V feeds a 2.2 kohm 5 % resistor. Find the nominal, minimum and maximum current.
3. A 1/2 W resistor has a derating curve that is flat to 70 C and reaches zero at 155 C. What power may it dissipate at 40 C, at 90 C and at 130 C?
4. A 1206 chip resistor is rated 1/4 W and 200 V. What is its critical resistance? Is a 470 kohm chip across 230 V allowed?
5. (Harder) You need a resistor between two points that sit 15 V apart, and you want the current to be between 10 mA and 14 mA in the worst case, using 5 % parts from the E12 series. Which values work? What power rating would you pick with the half-rating rule?

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Tolerance | "The accuracy of the resistor" | The guaranteed maximum deviation from the nominal value when new, at 25 C |
| E12 / E24 | "The standard values" | Values spaced evenly on a ratio scale so that their tolerance ranges cover every possible resistance |
| Worst case | "Being paranoid" | Checking the design with every variable at the extreme that hurts most |
| Power rating | "How many watts it can take" | The power that brings the part to its maximum safe temperature at a stated ambient temperature |
| Derating | "Running it gently" | Reducing the allowed stress (usually power) when conditions (usually temperature) are worse than the rating assumes |
| Limiting element voltage | "Max voltage" | The highest voltage allowed across the part regardless of power, set by arcing across the resistive film |
| Temperature coefficient | "Drift" | Fractional change of resistance per kelvin, usually in ppm/K |

## Further Reading

- [All About Circuits reference: "Resistor Color Codes"](https://www.allaboutcircuits.com/textbook/reference/chpt-2/resistor-color-codes/) — tolerance bands and standard values in one page
- *Practical Electronics for Inventors* (Scherz & Monk), chapter on resistors — tolerances, standard values and ratings with practical advice
- *The Art of Electronics* (Horowitz & Hill), Chapter 1 and Appendix on resistor types — how professionals choose resistors
- A metal-film resistor datasheet such as Vishay MRS25 or Yageo MFR series — find the derating curve, tempco and maximum working voltage yourself
- IEC 60063 — the international standard that defines the E-series preferred numbers
