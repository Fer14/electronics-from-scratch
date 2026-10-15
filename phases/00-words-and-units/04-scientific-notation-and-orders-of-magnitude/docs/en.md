# Scientific Notation and Orders of Magnitude

> Electronics spans numbers from a billionth to a billion. Count the zeros once, write them as a power of ten, and never lose them again.

**Type:** Learn
**Prerequisites:** Phase 00 (Words and Units), Lesson 02 (The Vocabulary) and Lesson 03 (Units and SI Prefixes)
**Time:** ~50 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| power of ten | 10 multiplied by itself some number of times, like 10 x 10 x 10 = 1000 | the number of zeros after the 1 |
| exponent | the small raised number that says how many tens to multiply (the 3 in 10^3) | a counter of zeros |
| negative exponent | divide by ten that many times instead of multiplying (10^-3 = 1/1000) | moving the decimal point to the left |
| scientific notation | writing a number as (a number between 1 and 10) x (a power of ten) | a price tag plus a "how many zeros" sticker |
| mantissa | the "between 1 and 10" part of scientific notation (the 4.7 in 4.7 x 10^3) | the digits that actually matter |
| engineering notation | like scientific notation, but the exponent is always a multiple of 3 | the version that lines up with k, M, m, µ |
| order of magnitude | roughly "which power of ten is this number closest to" | is it in the tens, the thousands, the millions? |
| significant figures | the digits of a number you actually trust | a bathroom scale that shows 72.4 kg, not 72.41837 kg |
| Fermi estimate | a quick calculation with rounded numbers to get the right power of ten | guessing how many piano tuners live in a city |
| logarithm (log10) | the exponent you need: log10(1000) = 3 because 10^3 = 1000 | "how many zeros?" as a function |

## Learning Objectives

- Write any number in plain decimal, scientific notation and engineering notation, and switch between them without a calculator
- Multiply and divide numbers in scientific notation by handling the mantissas and the exponents separately
- Connect engineering notation to the SI prefixes from Lesson 03 (10^-3 is milli, 10^3 is kilo, and so on)
- Recall the rough order of magnitude of everyday currents, voltages and resistances, from a watch to lightning
- Do a Fermi estimate and judge whether a calculated answer is believable
- Print numbers in Python in scientific, engineering and fixed formats, and know why 0.1 + 0.2 is not exactly 0.3

## The Problem

Here are four numbers you will meet in the next few phases of this course:

```
current through a red LED            0.02 A
current drawn by a quartz watch      0.0000015 A
a resistor on a microcontroller pin  47000 Ω
charge of a single electron          0.0000000000000000001602 C
```

Try reading the last one out loud. Now try to count the zeros without your finger on the screen. That number has eighteen zeros after the decimal point before the first non-zero digit, and if you miscount by one your answer will be wrong by a factor of ten. In electronics a factor of ten is not "a bit off". A 47 Ω resistor where you wanted 470 Ω lets ten times the current through and can burn out an LED. A capacitor of 100 nF where the circuit needed 100 µF (a thousand times more) will simply not do its job.

The numbers in this field are spread out over an enormous range. A watch battery delivers about a millionth of an amp. A lightning bolt carries tens of thousands of amps. That is a ratio of about ten billion. No other everyday subject asks you to juggle that many zeros, and that is why engineers, starting with astronomers and chemists centuries ago, invented a compact way to write them. This lesson teaches that way, and it teaches a second skill that matters even more: knowing the rough size of things, so that when a calculation gives "the LED current is 3000 A" you immediately know something went wrong.

## The Physics

There is not much physics in this lesson, but there is one physical fact that explains why we need it: nature is built from tiny pieces in enormous numbers.

A single electron carries a charge of about 1.602 x 10^-19 coulombs (the coulomb, C, is the unit of electric charge you met in Lesson 03; we will meet charge properly in Phase 01, Lesson 02). An ordinary current of one amp means one coulomb flowing past a point every second. So one amp is about

```
1 / (1.602 x 10^-19) = 6.24 x 10^18 electrons every second
```

That is six billion billion electrons per second. Whenever we connect the world of single particles (tiny) to the world of things we can hold (ordinary), we multiply or divide by numbers with around twenty zeros. The same happens with atoms: a few grams of copper wire contain about 10^22 atoms. Robert Millikan measured the electron's charge in 1909 by watching charged oil droplets float between two metal plates, and the number he found has nineteen zeros after the decimal point. Without a compact notation, every such calculation would be a counting exercise.

The second fact: physical quantities in circuits genuinely spread across many powers of ten. The resistance of a short copper wire is a few thousandths of an ohm; the resistance of a glass insulator is around a trillion ohms. That is a ratio of about 10^14, and both values matter in the same circuit. Good copper and good glass are useful precisely because they are so far apart.

## The Concept

### Powers of ten

Start with what you already know:

```
10^1 = 10                       one zero
10^2 = 10 x 10 = 100            two zeros
10^3 = 10 x 10 x 10 = 1000      three zeros
10^6 = 1 000 000                six zeros (a million)
10^9 = 1 000 000 000            nine zeros (a billion)
```

Read "10^3" as "ten to the third" or "ten to the power three". The small number (the exponent) counts how many tens are multiplied together, which is the same as the number of zeros after the 1. In this course we write the exponent with a caret, `10^3`, because that is easy to type. Books print it as a raised 3.

What about 10^0? It is 1. One way to see it: every time the exponent goes down by one, we divide by ten. 10^2 = 100, 10^1 = 10, so the next step down is 10 / 10 = 1. Keep going and you get negative exponents:

```
10^0  = 1
10^-1 = 1/10      = 0.1
10^-2 = 1/100     = 0.01
10^-3 = 1/1000    = 0.001
10^-6 = 1/1000000 = 0.000001
```

A negative exponent means "divide by ten that many times". Read 10^-3 as "ten to the minus three". In a decimal number, 10^-3 has the 1 in the third place after the point.

The picture to keep in your head: the exponent tells you how far and in which direction to slide the decimal point. Positive slides it right (bigger), negative slides it left (smaller).

### Scientific notation

Any number can be written as

```
number = mantissa x 10^exponent      with 1 <= mantissa < 10
```

Read it as: "a number between one and ten, times ten to some power". Examples:

```
47000      = 4.7  x 10^4      (slide the point 4 places left to get 4.7)
0.02       = 2    x 10^-2     (slide the point 2 places right to get 2)
0.0000015  = 1.5  x 10^-6     (slide 6 places right)
230        = 2.3  x 10^2
```

The recipe for converting a plain number:

1. Move the decimal point until exactly one non-zero digit is to its left. That gives the mantissa.
2. Count how many places you moved it. That is the size of the exponent.
3. If you moved the point to the left (the original number was big), the exponent is positive. If you moved it to the right (the number was small), the exponent is negative.

Worked example: 0.000047.

```
0.000047  ->  move the point right: 0.00004.7 ... after 5 moves we have 4.7
moved 5 places to the right, so exponent = -5
0.000047 = 4.7 x 10^-5
```

Check by going backwards: 4.7 x 10^-5 means 4.7 divided by ten five times: 0.47, 0.047, 0.0047, 0.00047, 0.000047. Correct.

Calculators and Python write the same thing with an "e": `4.7e-5` means 4.7 x 10^-5. The "e" stands for "exponent", not for the electron and not for Euler's number. You will see `1.602e-19` in every piece of code in this course.

### Why the mantissa is between 1 and 10

You could also write 47000 as 47 x 10^3 or 0.47 x 10^5. All are correct. Scientific notation picks the one with a single digit before the point so that every number has exactly one standard form. That makes comparison instant: 3.2 x 10^7 is bigger than 9.9 x 10^6 because 7 is bigger than 6, no matter what the mantissas are.

### Engineering notation: multiples of three

Engineers prefer a slightly different rule: the exponent must be a multiple of 3 (..., -9, -6, -3, 0, 3, 6, 9, ...) and the mantissa is allowed to be anywhere from 1 up to (but not including) 1000. Why? Because each multiple of three has a name, the SI prefix you learned in Lesson 03:

```
exponent   prefix   symbol   example
  10^12    tera       T      1 TΩ   (a glass insulator)
  10^9     giga       G      2.4 GHz (Wi-Fi)
  10^6     mega       M      10 MΩ  (multimeter input)
  10^3     kilo       k      47 kΩ  (a resistor)
  10^0     (none)            12 V   (a car battery)
  10^-3    milli      m      20 mA  (an LED)
  10^-6    micro      µ      1.5 µA (a watch)
  10^-9    nano       n      100 nF (a capacitor)
  10^-12   pico       p      22 pF  (a tiny capacitor)
```

So engineering notation is just scientific notation adjusted until the prefix pops out:

```
47000 Ω   = 4.7 x 10^4 Ω  (scientific)
          = 47  x 10^3 Ω  (engineering)  = 47 kΩ
0.02 A    = 2   x 10^-2 A (scientific)
          = 20  x 10^-3 A (engineering)  = 20 mA
```

To convert scientific to engineering: if the exponent is not a multiple of 3, lower it to the next multiple of 3 below and multiply the mantissa by 10 for each step you lowered it. For 4.7 x 10^4: the multiple of 3 below 4 is 3, one step, so the mantissa becomes 47: 47 x 10^3. For 2 x 10^-2: the multiple of 3 below -2 is -3, one step, so 20 x 10^-3.

This is exactly why the parts in a shop are labelled 4.7 kΩ, 100 nF, 22 pF and not 4.7 x 10^3 Ω.

### Multiplying in scientific notation

The rule: multiply the mantissas, add the exponents.

Why add? Because 10^2 x 10^3 = (10 x 10) x (10 x 10 x 10) = five tens multiplied = 10^5. Counting zeros: two zeros and three zeros make five zeros.

Worked example. A resistor of 680 Ω carries a current of 15 mA. As a preview of Ohm's law (we will earn it properly in Phase 03), the voltage across it is current times resistance, V = I x R. Read that as "the voltage in volts equals the current in amperes times the resistance in ohms".

```
I = 15 mA  = 1.5 x 10^-2 A
R = 680 Ω  = 6.8 x 10^2 Ω

V = (1.5 x 6.8) x 10^(-2 + 2)
  = 10.2 x 10^0
  = 1.02 x 10^1 V        (re-normalised: 10.2 is not below 10)
  = 10.2 V
```

Note the last step. Multiplying two mantissas between 1 and 10 can give up to 100, so sometimes you have to slide the point once more and add 1 to the exponent.

### Dividing in scientific notation

The rule: divide the mantissas, subtract the exponents.

Worked example: how many electrons flow past a point each second in a current of 1 mA? A current of 1 mA is 10^-3 coulombs per second. Each electron carries 1.602 x 10^-19 C.

```
electrons per second = (1 x 10^-3) / (1.602 x 10^-19)
                     = (1 / 1.602) x 10^(-3 - (-19))
                     = 0.6242 x 10^16
                     = 6.242 x 10^15       (re-normalised: 0.6242 is below 1)
```

Subtracting a negative exponent is the same as adding: -3 - (-19) = -3 + 19 = 16. That double minus is the single most common place to slip. Say it out loud: "minus three, minus minus nineteen, is plus sixteen".

So a modest 1 mA, the current of a dim indicator LED, is six thousand million million electrons per second.

### Powers of powers and square roots

Two more rules you will occasionally need:

```
(10^3)^2 = 10^6            raise to a power: multiply the exponents
sqrt(10^6) = 10^3          square root: halve the exponent
sqrt(4 x 10^6) = 2 x 10^3  (square-root the mantissa, halve the exponent)
```

If the exponent is odd, borrow a ten first: sqrt(10^7) = sqrt(10 x 10^6) = 3.16 x 10^3.

### Orders of magnitude

The order of magnitude of a number is the power of ten it is closest to. 47000 is about 10^4.7, so its order of magnitude is 10^5 if you round, or "tens of thousands" if you speak. Two numbers are "two orders of magnitude apart" when one is about 100 times the other.

The mathematical tool is the base-ten logarithm, written log10. It answers the question "ten to what power gives this number?":

```
log10(1000) = 3        because 10^3 = 1000
log10(0.001) = -3      because 10^-3 = 0.001
log10(47000) ≈ 4.67
```

You will not need logarithms for calculations in this phase, but they explain the bar charts our code prints: a bar of length log10(value) lets a nanoamp and a lightning bolt share the same page.

Here is the ladder of currents you will meet, roughly:

```
   10^-9 A   1 nA     leakage through a good capacitor
   10^-6 A   1 µA     a quartz wristwatch, a TV remote waiting for a button
   10^-2 A   10 mA    a red indicator LED
   10^0  A   1 A      a phone charging over USB
   10^1  A   10 A     an electric kettle on mains
   10^2  A   200 A    a car starter motor turning the engine
   10^4  A   30 kA    a typical lightning stroke
```

Thirteen orders of magnitude separate the top and the bottom. The ladder of voltages:

```
   70 mV     the electrical signal across a nerve cell's wall
   0.65 V    the drop across a silicon diode (Phase 11)
   1.5 V     an AA cell
   5 V       a USB port
   12 V      a car battery (the most we use in this course)
   230 V     a European wall outlet (120 V in North America)
   400 kV    a long-distance transmission line
   ~100 MV   a thundercloud relative to the ground
```

And resistances:

```
   5 mΩ      one metre of thick copper cable
   30 Ω      the hot filament of a small 6 V lamp
   1 kΩ      a human body with wet hands (Lesson 06)
   10 kΩ     the most common resistor on a breadboard
   100 kΩ    a human body with dry skin
   10 MΩ     the input of a multimeter (Phase 06)
   1 TΩ      a glass insulator
```

You do not need to memorise every line. You need a feel: milliamps are LED territory, amps are motor and charger territory, kiloamps are lightning and welding. If a calculation lands in the wrong territory, stop and check.

### Fermi estimates

Enrico Fermi, a physicist famous in the 1940s, liked to ask students questions like "how many piano tuners work in Chicago?". Nobody knows exactly, but you can break the question into rough guesses (people in the city, pianos per household, tunings per year, tunings a tuner can do) and get within a factor of a few. The trick works because errors in rough guesses tend to partly cancel, and because you only want the power of ten.

Electronics example: how many electrons pass through your phone cable during one night of charging?

```
current        about 1 A           (1 coulomb per second)
time           about 8 hours = 8 x 3600 s = 28 800 s ≈ 3 x 10^4 s
total charge   1 A x 3 x 10^4 s = 3 x 10^4 C
electrons      3 x 10^4 / 1.6 x 10^-19
             = (3 / 1.6) x 10^(4 + 19)
             ≈ 1.9 x 10^23
```

The careful version with 28 800 s and 1.602 x 10^-19 C gives 1.80 x 10^23. Our head-only estimate was off by about 5%. For a Fermi estimate that is excellent. The answer to remember: about 10^23 electrons, roughly a third of the number of atoms in a gram of hydrogen.

The point is not this specific number. The point is that you can now sanity-check any result. If someone tells you a phone charger moves 10^40 electrons a night, you know they are wrong by a factor of 10^17.

### Significant figures, briefly

Real components are not exact. A resistor marked 4.7 kΩ with 5% tolerance (Phase 03, Lesson 06) can be anywhere from 4.465 kΩ to 4.935 kΩ. So writing the current through it as 2.553191489 mA is pretending to know more than you do. Two or three significant figures are almost always enough in electronics: 2.55 mA. Our code prints with `:.3g` or `:.4g` for this reason.

## Build It

The script `code/main.py` builds the conversions from scratch, checks them against plain Python floats, prints the three ladders and the Fermi estimate.

### Step 1: Split a number into mantissa and exponent

The exponent is the floor (round down) of the base-ten logarithm. The mantissa is what is left after dividing that power of ten out.

```python
def split_scientific(value):
    if value == 0:
        return 0.0, 0
    exponent = math.floor(math.log10(abs(value)))
    mantissa = value / 10**exponent
    if abs(mantissa) >= 10:
        mantissa /= 10
        exponent += 1
    return mantissa, exponent
```

For 47000, log10 is 4.67, the floor is 4, and 47000 / 10^4 = 4.7. The `if` handles a rare rounding hiccup where the computer's logarithm lands a hair below a whole number.

### Step 2: Engineering notation and SI prefixes

Round the exponent down to a multiple of 3 and look up the prefix:

```python
def split_engineering(value):
    if value == 0:
        return 0.0, 0
    mantissa, exponent = split_scientific(value)
    engineering_exponent = 3 * math.floor(exponent / 3)
    return value / 10**engineering_exponent, engineering_exponent


def with_prefix(value, unit, digits=3):
    mantissa, exponent = split_engineering(value)
    prefix = ENGINEERING_PREFIXES.get(exponent)
    if prefix is None:
        return f"{value:.{digits - 1}e} {unit}"
    return f"{mantissa:.{digits}g} {prefix}{unit}"
```

`ENGINEERING_PREFIXES` is a small dictionary from exponent to letter (`-3: "m"`, `3: "k"`, ...). The electron's charge falls outside our table (it would need the rare prefix "zepto"), so it falls back to plain scientific form. The output:

```
  pull-up resistor
    plain decimal : 47000 Ω
    scientific    : 4.7 x 10^4 Ω
    engineering   : 47 x 10^3 Ω  ->  47 kΩ
```

### Step 3: Multiply and divide by hand, then check

```python
def multiply_scientific(first, second):
    m1, e1 = split_scientific(first)
    m2, e2 = split_scientific(second)
    raw_mantissa = m1 * m2
    raw_exponent = e1 + e2
    mantissa, shift = split_scientific(raw_mantissa)
    return raw_mantissa, raw_exponent, mantissa, raw_exponent + shift
```

It returns both the raw result (mantissas multiplied, exponents added) and the re-normalised one, so you can see the extra step. `divide_scientific` is identical except it divides mantissas and subtracts exponents. The script prints:

```
    (1.5 x 10^-2 A) x (6.8 x 10^2 Ω) = 10.2 x 10^0 = 1.02 x 10^1 V
    check with plain floats: 10.2 V
    (1 x 10^-3 C/s) / (1.602 x 10^-19 C) = 0.6242 x 10^16 = 6.242 x 10^15 electrons/s
```

### Step 4: The ladders

```python
def show_ladder(title, unit, entries):
    print(f"=== {title} ===")
    values = np.array([value for _, value in entries])
    exponents = np.log10(values)
    for (name, value), exponent in zip(entries, exponents):
        bar = "#" * int(round(exponent - exponents.min())) + "#"
        print(f"  {name:<34} {with_prefix(value, unit):>12}   10^{order_of_magnitude(value):>3}  {bar}")
    span = exponents.max() - exponents.min()
    print(f"  span: about {span:.0f} orders of magnitude (largest / smallest = {values.max() / values.min():.1e})")
    print()
```

Each `#` is one power of ten. On a normal (linear) scale the lightning bar would be 30 trillion times longer than the leakage bar; on the log scale it is fourteen characters.

### Step 5: The Fermi estimate and Python formatting

The script repeats the phone-cable estimate both carefully and "head-only", then shows Python's format codes:

```
  f'{value:e}'    -> 4.700000e-05
  f'{value:.2e}'  -> 4.70e-05
  f'{value:.3g}'  -> 4.7e-05
  f'{value:.6f}'  -> 0.000047
  with_prefix      -> 47 µF
  4.7e3 == 4700    -> True
  0.1 + 0.2        -> 0.30000000000000004
  math.isclose     -> True
```

- `e` forces scientific notation; `.2e` keeps two digits after the point.
- `g` ("general") picks plain or scientific automatically and keeps a given number of significant figures.
- `f` forces fixed-point; `.6f` shows six decimals.
- `0.1 + 0.2` is not exactly 0.3 because computers store numbers in binary, where 0.1 is a repeating fraction (like 1/3 = 0.333... in decimal). The error is around 10^-17, utterly irrelevant for circuits, but it means you should compare floats with `math.isclose`, never with `==`.

Run it:

```
cd /home/fer/Escritorio/youtube/electronics_from_scratch
uv run python phases/00-words-and-units/04-scientific-notation-and-orders-of-magnitude/code/main.py
```

## Use It

- **Component markings.** A capacitor stamped `104` means 10 x 10^4 pF = 100 000 pF = 100 nF. The third digit is literally an exponent. A resistor marked `4702` (on surface-mount parts) is 470 x 10^2 = 47 kΩ. You will decode these in Phase 03, Lesson 04.
- **Datasheets.** A typical small-signal transistor datasheet lists leakage current in nA, maximum current in mA, and switching time in ns, all on the same page. The ATmega328P microcontroller (the chip in an Arduino Uno) draws a few mA when running and well under 1 µA in its deepest sleep: three or four orders of magnitude, which is why battery gadgets spend most of their life asleep.
- **Simulators and meters.** Circuit simulators (SPICE and our own `sim`, from Phase 05) print results like `2.127e-03`. Multimeters show `2.13 mA` and switch ranges by powers of ten.
- **Batteries.** A coin cell holds about 220 mAh; a car battery about 60 Ah. That is about 300 times more charge, between two and three orders of magnitude.
- **Sanity checks in every lab.** Before you trust any reading, ask: is this the right order of magnitude? An LED at 20 A or a 9 V battery reading 900 V means a wrong range, a wrong decimal point, or a wrong formula.

## Common Mistakes

- **Sign of the exponent flipped.** 0.002 is 2 x 10^-3, not 2 x 10^3. Small numbers have negative exponents. Check: is the original number smaller than 1? Then the exponent must be negative.
- **Counting zeros instead of places.** 2500 has two zeros but is 2.5 x 10^3, because the point moves three places. 0.05 is 5 x 10^-2: the 5 sits in the second place after the point. Count how far the point moves, not how many zeros you see.
- **Subtracting negative exponents.** 10^-3 / 10^-19 = 10^16, not 10^-22. Minus a minus is a plus.
- **Forgetting to re-normalise.** 8 x 5 = 40, so (8 x 10^3)(5 x 10^2) = 40 x 10^5 = 4 x 10^6, not 4 x 10^5.
- **Mixing "m" and "M".** Lower-case m is milli (10^-3), upper-case M is mega (10^6). A 1 mΩ and a 1 MΩ resistor differ by a factor of 10^9.
- **Reading `e` as Euler's number.** In `2.2e-6`, the e means "times ten to the". It has nothing to do with 2.718.
- **Too many digits.** Writing 3.333333333 mA for a circuit built with 5% resistors claims precision you do not have. Keep two or three significant figures.

## Exercises

1. Write in scientific notation and in engineering notation (with an SI prefix): 330 000 Ω, 0.000 000 022 F, 0.0045 A, 13 800 000 Hz.
2. Without a calculator: (3 x 10^-3) x (2 x 10^4) and (6 x 10^5) / (3 x 10^-2). Then check with Python.
3. A 9 V battery is connected across a 1.5 MΩ resistor. Using the preview V = I x R rearranged as I = V / R, find the current in scientific notation and with a prefix. Which line of the current ladder is it closest to?
4. Fermi estimate: a TV remote draws 2 µA while waiting and 20 mA for the 0.1 s it sends a code. You press it 40 times a day. Over a year, which uses more charge, the waiting or the sending? By about what factor?
5. (Harder) Copper has about 8.5 x 10^28 free electrons per cubic metre. A wire 1 m long with a cross-section of 1 mm^2 (= 10^-6 m^2) has a volume of 10^-6 m^3. How many free electrons does it contain? If 1 A flows (6.24 x 10^18 electrons/s), how many seconds would it take for a number of electrons equal to the whole wire's population to pass a point? Convert to hours. (This is a first look at why electrons drift so slowly, Phase 01, Lesson 06.)

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| scientific notation | "the e-numbers on a calculator" | mantissa between 1 and 10 times a power of ten; `4.7e3` = 4.7 x 10^3 |
| engineering notation | "with the k and the m" | exponent restricted to multiples of 3 so it matches an SI prefix |
| exponent | "the little number" | how many times you multiply (positive) or divide (negative) by ten |
| order of magnitude | "about that size" | the nearest power of ten; two numbers one order apart differ by about 10x |
| Fermi estimate | "a guess" | a structured rough calculation aimed at the right power of ten |
| significant figures | "the digits" | the digits supported by how precisely you know the value |
| floating-point | "decimals on a computer" | the binary format computers use for real numbers; tiny rounding errors near 10^-16 relative |

## Further Reading

- [All About Circuits, "Scientific Notation" and "Metric Prefixes" in Volume I, Chapter 4](https://www.allaboutcircuits.com/textbook/direct-current/chpt-4/scientific-notation/): free textbook chapter on notation as used in electronics.
- [Khan Academy, "Scientific notation"](https://www.khanacademy.org/math/pre-algebra/pre-algebra-exponents-radicals): short videos and exercises if the exponent rules feel shaky.
- [Powers of Ten (Charles and Ray Eames, 1977)](https://www.youtube.com/watch?v=0fKBhvDjuy0): a nine-minute film that zooms by a factor of ten every ten seconds; the best feeling for orders of magnitude ever made.
- Sanjoy Mahajan, *Street-Fighting Mathematics* (MIT Press, 2010, free online from MIT OpenCourseWare): the art of estimation and sanity checks.
- [Python documentation, "Format Specification Mini-Language"](https://docs.python.org/3/library/string.html#formatspec): every format code (`e`, `f`, `g`) explained.
