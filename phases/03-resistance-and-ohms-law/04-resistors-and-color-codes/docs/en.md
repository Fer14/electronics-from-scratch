# Resistors and Color Codes

> A resistor is resistance you can buy. Its value is painted on in stripes, and it only comes in a few dozen "preferred" numbers per decade.

**Type:** Build
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Lessons 01 to 03; Phase 00 (Words and Units), Lesson 03 (Units and SI Prefixes)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Resistor | A component made on purpose to have a known resistance | A measured cup in a kitchen: a known amount, on demand |
| Through-hole | A component with long wire legs that go through holes in a board | A plant with roots through a pot |
| Lead | One of the wire legs of a through-hole part | A leg of a table |
| SMD / surface-mount | A tiny component without legs, soldered flat on top of the board | A sticker on a page |
| Color code | Colored stripes ("bands") on a resistor that tell its value | A barcode you read with your eyes |
| Band | One colored stripe | A ring on a finger |
| Significant digits | The first digits of the value, before the zeros | The "47" in 4700 |
| Multiplier | The number of zeros to add (a power of ten) | "×100" on a price tag |
| Tolerance | How far the real value may be from the printed one, in percent | "Weight 500 g ± 10 g" on a bag of flour |
| Nominal value | The value printed or painted on the part | The size on a clothing label |
| E-series (E6, E12, E24...) | Standard lists of values that resistors are made in | Shoe sizes: only certain sizes exist |
| Decade | A range from some value to ten times that value (for example 100 Ω to 1 kΩ) | A row on a ruler from 1 to 10 |
| Preferred value | A value that belongs to an E-series and is easy to buy | A standard paper size like A4 |

## Learning Objectives

- Describe how a resistor is built and what the main types (carbon film, metal film, wirewound, SMD) are used for
- Decode 4-band and 5-band color codes, including gold and silver multipliers
- Encode a value into color bands, and write values in the "4k7" notation
- Read the 3-digit and 4-digit codes printed on SMD resistors
- Explain why resistor values come from the E-series and why the steps are about 20 % apart for E12
- Pick the nearest standard value for a resistance calculated with Ohm's law, and check how much the result changes

## The Problem

In Lesson 03 you computed that a 12 V circuit needs 4.8 kΩ to give 2.5 mA. You open your resistor kit and there is no 4.8 kΩ. There are 4.7 kΩ and 5.6 kΩ. Which one? Does it matter?

Then you look at the resistors themselves. They are tiny cylinders, a few millimeters long, with no numbers printed on them, only colored stripes. Some have four stripes, some five. Some are blue, some beige. On the circuit board of your old router you find even smaller black rectangles with "472" printed on them.

To build anything, you need to recognise a resistor's value at a glance, and you need to know which values exist so your designs can be built with real parts. This lesson is about the real objects.

## The Physics

### How a resistor is made

Lesson 02 told us that R = ρ L / A: a long, thin path of a resistive material gives a high resistance. A resistor factory uses exactly that idea.

**Carbon film and metal film resistors** (the most common through-hole types) start as a small ceramic rod. A very thin film of carbon or of a metal alloy (nickel-chromium, for instance) is deposited on its surface. Then a laser or a diamond wheel cuts a **spiral groove** through the film, around the rod. The current can no longer go straight from one end to the other; it has to follow the spiral path. A longer spiral (more turns) means a longer, thinner path, and a higher resistance. The factory measures the resistance *while* cutting and stops when it reaches the target value. Then metal caps with wire leads are pressed on the ends, and the whole thing is covered in lacquer and painted with bands.

```
   lead     end cap       spiral-cut film on ceramic rod      end cap     lead
  ------====[|]////\\\\////\\\\////\\\\////\\\\////[|]====------
               \__________ current follows the spiral ______/
```

- **Carbon film**: cheap, beige body, usually ±5 %, slightly noisier.
- **Metal film**: usually blue body, ±1 % or better, more stable with temperature, low noise. The default in modern kits.
- **Wirewound**: a nichrome-type wire wound on a ceramic core, often in a white rectangular ceramic or aluminium case. Used for high power (several watts) and low values.
- **Thick-film SMD**: a paste of metal oxide and glass printed on a tiny ceramic chip and baked; trimmed by a laser. These are the black rectangles on every modern circuit board. Common sizes are named by their dimensions: 0603 is 0.06 × 0.03 inches (1.6 × 0.8 mm).

The body size of a resistor sets how much heat it can get rid of (its power rating, Lessons 05 and 06), not its resistance. A 1/4 W through-hole resistor is about 6 mm long, whatever its value.

## The Concept

### The color code

Through-hole resistors are too small and too round for printed numbers, so their value is painted as colored bands. Each color stands for a digit:

| Color | Digit | Multiplier | Tolerance |
|---|---|---|---|
| Black | 0 | × 1 | |
| Brown | 1 | × 10 | ±1 % |
| Red | 2 | × 100 | ±2 % |
| Orange | 3 | × 1 000 | |
| Yellow | 4 | × 10 000 | |
| Green | 5 | × 100 000 | ±0.5 % |
| Blue | 6 | × 1 000 000 | ±0.25 % |
| Violet | 7 | × 10 000 000 | ±0.1 % |
| Grey | 8 | | ±0.05 % |
| White | 9 | | |
| Gold | | × 0.1 | ±5 % |
| Silver | | × 0.01 | ±10 % |
| (no band) | | | ±20 % |

The digits follow the rainbow (red, orange, yellow, green, blue, violet) after black and brown, and before grey and white. A common way to remember the order is to say the colors out loud a few times while looking at the table; inventing your own sentence with the initials B B R O Y G B V G W works better than any borrowed one.

The **multiplier** is simply "how many zeros to add": its color's digit is the number of zeros. Red (2) means "add two zeros" (× 100). Gold and silver are the exceptions that make small values: gold means "divide by 10", silver "divide by 100".

### Reading a 4-band resistor

The four bands are: **digit, digit, multiplier, tolerance**. The tolerance band is usually gold or silver and is set slightly apart from the others. Hold the resistor so that the tolerance band is on your **right**, and read from left to right.

```
     ___________________________________
  --|  ||    ||    ||          ||       |--
    |  ||    ||    ||          ||       |
  --|__||____||____||__________||_______|--
      1st   2nd   multi-     tolerance
     digit digit  plier
```

**Example 1: yellow, violet, red, gold.**

```
yellow = 4     first digit
violet = 7     second digit         -> 47
red    = 2     multiplier: add two zeros -> 4700 Ω
gold   = ±5 %
```

4700 Ω = 4.7 kΩ, ±5 %. The real value is somewhere between 4700 × 0.95 = 4465 Ω and 4700 × 1.05 = 4935 Ω.

**Example 2: brown, black, red, gold.** 1, 0, add two zeros: 1000 Ω = 1 kΩ, ±5 %.

**Example 3: red, red, brown, gold.** 2, 2, add one zero: 220 Ω, ±5 %.

**Example 4: orange, orange, gold, silver.** 3, 3, gold multiplier (× 0.1): 33 × 0.1 = 3.3 Ω, ±10 %.

**Example 5: brown, black, orange, gold.** 1, 0, add three zeros: 10 000 Ω = 10 kΩ.

Notice that yellow-violet-red (4.7 kΩ) and yellow-violet-orange (47 kΩ) differ only in the third band. Confusing red and orange under a desk lamp is the most common reading mistake; it gives an error of exactly ten times.

### Reading a 5-band resistor

Precision resistors (±1 % and better) need three significant digits, so they have five bands: **digit, digit, digit, multiplier, tolerance**.

**Example 6: brown, black, black, brown, brown.**

```
brown = 1, black = 0, black = 0       -> 100
brown multiplier = add one zero       -> 1000 Ω
brown tolerance = ±1 %
```

1 kΩ ±1 %. Note that 5-band resistors often have brown at both ends, which makes the direction ambiguous. Clues: the tolerance band is usually a bit wider or further from the others; and only one reading direction will give a standard value (see the E-series below). When in doubt, measure it with your multimeter (Phase 02, Lesson 07).

**Example 7: yellow, violet, black, brown, brown.** 4, 7, 0 → 470, add one zero → 4700 Ω = 4.7 kΩ ±1 %.

### Encoding: from a value to bands

To find the bands for a value, write it with two significant digits followed by zeros:

```
470 Ω   = 47 followed by 1 zero    -> yellow violet brown
10 kΩ   = 10 followed by 3 zeros   -> brown black orange
1 MΩ    = 10 followed by 5 zeros   -> brown black green
3.3 Ω   = 33 × 0.1                 -> orange orange gold
```

### The "4k7" notation

On schematics and parts lists, values are often written with the prefix letter in place of the decimal point:

| Written | Means |
|---|---|
| 4R7 | 4.7 Ω |
| 470R | 470 Ω |
| 4k7 | 4.7 kΩ = 4700 Ω |
| 47k | 47 kΩ |
| 1M | 1 MΩ |
| 2M2 | 2.2 MΩ |

This avoids decimal points, which disappear when a schematic is photocopied or printed small. "4.7k" with a lost dot becomes "47k", a tenfold error; "4k7" cannot be misread that way.

### SMD codes

Surface-mount resistors print a short number instead of colors:

- **3 digits** (for ±5 % parts): two significant digits, then the number of zeros. "472" = 47 followed by 2 zeros = 4700 Ω. "103" = 10 000 Ω = 10 kΩ. "221" = 220 Ω.
- **4 digits** (for ±1 % parts): three significant digits, then the number of zeros. "1002" = 100 followed by 2 zeros = 10 kΩ. "4701" = 4.7 kΩ.
- **R marks the decimal point**: "4R7" = 4.7 Ω.
- **"000" or "0"** is a **zero-ohm resistor**: a jumper, a piece of wire in resistor form, used so pick-and-place machines can also place wire links.

(There is a third system for 1 % parts, EIA-96, with two digits and a letter, like "01C". You will look it up the day you need it.)

### Why only certain values exist: the E-series

Imagine you are a resistor factory. You make ±10 % resistors. Is there any point in making both 100 Ω and 105 Ω? No: a "100 Ω ±10 %" resistor can already be anywhere from 90 to 110 Ω, so the 105 Ω part is not really a different product. It makes sense to space the values so that their tolerance ranges just touch:

```
 value:         100              120              150
 ±10 % range:  [90 ......... 110]
                          [108 ......... 132]
                                      [135 ....... 165]
```

If each value is about 1.2 times the previous one, a ±10 % band around each covers nearly all values in between. And because the step is a *ratio*, not a fixed difference, the same pattern repeats in every decade: 1.0, 1.2, 1.5 ... then 10, 12, 15 ... then 100, 120, 150 ... and so on.

How many steps per decade? If each step multiplies by a factor *k*, then 12 steps must multiply by 10 in total:

```
k^12 = 10     ->     k = 10^(1/12) = 1.212
```

Starting from 1.0 and multiplying by 1.212 repeatedly gives 1.00, 1.21, 1.47, 1.78, 2.15, 2.61, 3.16, 3.83, 4.64, 5.62, 6.81, 8.25. Rounded to two digits (and with a few historical adjustments), these are the **E12 series**:

```
E12:  1.0  1.2  1.5  1.8  2.2  2.7  3.3  3.9  4.7  5.6  6.8  8.2
```

Multiply by any power of ten: 10, 12, 15, 18, 22 ... 100, 120 ... 1k, 1k2, 1k5 ... 4k7, 5k6, 6k8, 8k2, 10k ...

The family:

| Series | Values per decade | Step ratio | Typical tolerance |
|---|---|---|---|
| E6 | 6 | 1.468 | ±20 % |
| E12 | 12 | 1.212 | ±10 % |
| E24 | 24 | 1.101 | ±5 % (and 1 % kits) |
| E48 | 48 | 1.049 | ±2 % |
| E96 | 96 | 1.024 | ±1 % |

Every E6 value is also in E12, and every E12 value is in E24. E24 adds 1.1, 1.3, 1.6, 2.0, 2.4, 3.0, 3.6, 4.3, 5.1, 6.2, 7.5, 9.1.

The coverage is not perfect, because of the rounding. The script measures it: E12 with ±10 % has 10 of its 12 neighbour pairs touching or overlapping, and the worst gap (between 1.2 and 1.5) is 2.5 % of the value. That is why the E-series are called "preferred values", not "perfect values".

Fun fact: 4.7 is in E6, E12 and E24. That is why 4.7 kΩ, 47 kΩ and 470 Ω are everywhere.

### Picking a standard value

Back to the problem. Ohm's law said 4.8 kΩ for 2.5 mA at 12 V. The E12 neighbours are 4.7 kΩ and 5.6 kΩ.

```
with 4.7 kΩ:  I = 12 / 4700 = 2.553 mA     (2.1 % above target)
with 5.6 kΩ:  I = 12 / 5600 = 2.143 mA     (14 % below target)
```

4.7 kΩ is much closer. To compare fairly, compare **ratios**, not differences, because the E-series is spaced by ratios: 4.8 / 4.7 = 1.02, while 5.6 / 4.8 = 1.17. The script's `nearest_standard` function does exactly that (it compares the logarithms of the ratios).

Sometimes direction matters more than closeness. If the target is a *maximum* (for example "the LED must not get more than 20 mA"), you round the resistance **up** to the next value, so the current is a bit lower, never higher. You will meet this in Phase 11.

And remember tolerance: even a 4.7 kΩ ±5 % resistor can be 4465 to 4935 Ω, so the current can be 2.43 to 2.69 mA. Lesson 06 (Tolerances and Ratings) deals with this properly.

## Build It

Run:

```
uv run python phases/03-resistance-and-ohms-law/04-resistors-and-color-codes/code/main.py
```

### Step 1: Decode bands

```python
def decode_bands(bands):
    *digit_bands, multiplier_band, tolerance_band = bands
    digits = 0
    for color in digit_bands:
        digits = digits * 10 + COLOR_DIGITS[color]
    ohms = digits * 10 ** multiplier_power(multiplier_band)
    return ohms, TOLERANCE_PERCENT[tolerance_band]
```

The last two bands are always multiplier and tolerance; everything before them is digits. That single rule handles both 4-band and 5-band resistors. Building the number with `digits * 10 + next` is exactly how you read "4, 7" as 47. `multiplier_power` returns the color's digit, or −1 for gold and −2 for silver. The script prints each example with its range, e.g. `yellow-violet-red-gold -> 4,700.0 ohm (4k7) +/-5% [4,465.0 .. 4,935.0]`.

### Step 2: Encode values

```python
def encode_bands(ohms, significant_digits=2, tolerance_band="gold"):
    power = math.floor(math.log10(ohms)) - (significant_digits - 1)
    digits = round(ohms / 10**power)
    ...
```

`log10` tells you how many digits the number has (log10(4700) = 3.67, floor 3). Subtract one to leave two significant digits: power = 2, so 4700 = 47 × 10². Then each digit is turned back into a color. The `format_ohms` helper writes the "4k7" style.

### Step 3: SMD codes

```python
def decode_smd(code):
    if "R" in code:
        return float(code.replace("R", "."))
    return int(code[:-1]) * 10 ** int(code[-1])
```

All digits but the last are significant; the last digit is the number of zeros. "R" is a decimal point.

### Step 4: The E-series are geometric

The script computes 10^(k/N) for N = 6, 12, 24 and prints it next to the real, rounded series. You can see where the rounding happened (2.61 became 2.7, 3.16 became 3.3, 4.64 became 4.7).

### Step 5: Tolerance coverage

For each series and its usual tolerance, the script computes the upper edge of each value's range and the lower edge of the next one, and reports the worst gap and how many neighbour pairs touch.

### Step 6: Nearest standard value

```python
def nearest_standard(target_ohms, series=E12):
    values = series_values(series, decades=(0.1, 1, 10, 100, 1000, 10000, 100000, 1000000))
    ratios = np.abs(np.log(values / target_ohms))
    return float(values[np.argmin(ratios)])
```

It lists every E12 value from 0.1 Ω to 8.2 MΩ, measures how far each is from the target as a ratio (the absolute value of the logarithm of the ratio, so 0.9× and 1.1× count about the same), and returns the closest. Then it prints the bands and the real current. For 12 V and 2.5 mA it picks 4k7, yellow-violet-red-gold, giving 2.55 mA.

## Use It

- **Resistor kits** sold for hobbyists usually contain E12 or E24 values from 10 Ω to 1 MΩ, metal film, ±1 %, 1/4 W. With E12 you can build almost anything; when you need an in-between value, you combine two (series and parallel, Phase 04, Lesson 04).
- **Datasheets** of resistor families (for example the Vishay MRS25 metal film series or the Yageo CFR carbon film series) list the available E-series, tolerance, power rating, temperature coefficient and maximum voltage. Lesson 06 reads one.
- **Schematics** from open-source hardware (Arduino boards, for instance) use notation like "10k", "4k7", "1M", "22R". Now you can read them.
- **Repair**: when a resistor on an old board is burnt, its color bands are often black. The schematic, or the neighbouring identical circuit, tells you the value.
- **Zero-ohm resistors** are everywhere on machine-assembled boards as jumpers and as optional links that can be fitted or left out to configure a product.

## Try It in the Lab

The lab task "Find the yellow-violet-red resistor" gives you a 12 V battery, an empty slot, and a bag of five unlabelled resistors described only by their color bands. The goal is a current between 2.3 mA and 2.8 mA. Decode all five bag descriptions first and write the value next to each. Then use Ohm's law to check which of them gives a current in range. Watch out for the pair that differ only in the third band.

## Common Mistakes

- **Reading the resistor backwards.** Put the gold or silver band on the right. On 5-band parts, look for the wider gap or try both directions and see which gives a standard value.
- **Confusing the multiplier with a digit.** Brown-black-red is 1-0-and-two-zeros = 1000 Ω, not 102 Ω.
- **Mixing up red, orange and brown** under poor light. A mistake here is a factor of ten. When unsure, measure.
- **Forgetting gold and silver as multipliers.** Orange-orange-gold is 3.3 Ω, not 33 Ω.
- **Designing with values that do not exist.** If your calculation gives 4.8 kΩ, your circuit must work with 4.7 kΩ or 5.6 kΩ. Check the current with the real value.
- **Rounding the wrong way for a limit.** For "at most 20 mA", round the resistance up, not to the nearest.
- **Measuring a resistor while it is still in a circuit.** Other parts in parallel change the reading. Take one leg out first.

## Exercises

1. Decode: (a) red-violet-orange-gold; (b) brown-green-brown-gold; (c) blue-grey-red-silver; (d) brown-black-black-red-brown (5-band).
2. Write the color bands (4-band, ±5 %) for: 330 Ω, 2.2 kΩ, 68 kΩ, 1.5 MΩ, 4.7 Ω.
3. Decode the SMD codes 334, 100, 1001, 2R2 and 0.
4. A 5 V circuit needs 3 mA through a resistor. Compute the exact value, the nearest E12 value, and the resulting current.
5. (Harder) Compute 10^(k/24) for k = 0 to 23 and compare with the real E24 list in the code. Which values differ from the rounded ideal? Then compute how many E24 neighbour pairs fail to overlap at ±5 % without looking at the script's output.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Color code | "The stripes" | Bands encoding significant digits, a power-of-ten multiplier and a tolerance |
| Multiplier band | "The zeros band" | The power of ten applied to the digits; gold = ×0.1, silver = ×0.01 |
| Tolerance | "Accuracy" | The guaranteed maximum deviation of the real value from the nominal one, in percent |
| E12 | "Standard values" | Twelve values per decade spaced by about 10^(1/12) ≈ 1.21 |
| Preferred value | "A value you can buy" | A value belonging to an E-series |
| 4k7 notation | "Engineer's shorthand" | The prefix letter replaces the decimal point: 4k7 = 4.7 kΩ |
| SMD code | "The number on the chip" | Significant digits followed by a number of zeros; R marks the decimal point |
| Zero-ohm resistor | "A resistor that does nothing" | A jumper in resistor packaging, for machine assembly or configuration links |

## Further Reading

- *Practical Electronics for Inventors* (Scherz & Monk), chapter 2, section on resistors: color code tables, types and E-series.
- *The Art of Electronics*, 3rd edition (Horowitz & Hill), section 1.2.2 and appendix C on resistor types.
- Datasheet of a common metal film resistor family (for example Vishay MRS25 or Yageo MFR) and of a thick-film SMD family (for example Yageo RC series): look up the tables of sizes, tolerances and E-series.
- IEC 60063, the international standard that defines the E-series (summarised in many places, including the Wikipedia article "E series of preferred numbers").
