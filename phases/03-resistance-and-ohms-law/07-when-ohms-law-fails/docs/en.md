# When Ohm's Law Fails

> Ohm's law is not a law of nature. It is a very good description of some materials, under some conditions. Knowing where it stops is as useful as knowing the law.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Lesson 01 (What Resistance Is), Lesson 03 (Ohm's Law), Lesson 05 (Power and Heat) and Lesson 06 (Tolerances and Ratings)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Ohmic | Behaves like Ohm's law: double the voltage, double the current, always. | A tap where turning it twice as far always gives twice the water. |
| Non-ohmic (nonlinear) | The current does NOT grow in proportion to the voltage. | A stuck tap that does nothing at first, then suddenly gushes. |
| I-V curve (characteristic) | A graph of the current through a part (vertical) against the voltage across it (horizontal). | A part's "personality chart". |
| Linear | Its graph is a straight line through the origin. | Price of apples: twice the apples, twice the price. |
| Filament | The thin coiled tungsten wire inside an incandescent bulb that glows. | A tiny electric stove ring inside glass. |
| Inrush current | The large current a part draws in the first instant after switch-on, before it settles. | The crowd pushing through a door the moment a shop opens. |
| Thermistor | A resistor designed to change its resistance a lot with temperature. | A thermometer that reports in ohms instead of a mercury line. |
| NTC | Negative temperature coefficient: resistance goes DOWN when temperature goes UP. | Honey: the warmer it gets, the more easily it flows. |
| Diode | A part that lets current flow easily in one direction only (Phase 11). | A one-way turnstile. |
| Static resistance | The ratio `V / I` at one point of the curve. | Your average speed for the whole trip. |
| Dynamic (incremental) resistance | How much the voltage changes for a small change of current at that point: `dV / dI`. | Your speed at this very moment. |

## Learning Objectives

- State precisely what Ohm's law claims and what it does not claim
- Recognize ohmic and non-ohmic behavior from a table of measurements or an I-V curve
- Explain why an incandescent lamp's resistance changes ten-fold or more between cold and hot, and compute its inrush current
- Read a thermistor's resistance from its B-parameter formula
- Distinguish static resistance `V / I` from dynamic resistance `dV / dI`
- List the conditions (temperature, very high fields, semiconductors, very high frequency) where Ohm's law stops being a good model

## The Problem

You measure a car's small 12 V, 5 W bulb with a multimeter set to ohms. The display says about 2 ohm. Ohm's law then says that on 12 V the bulb should draw `12 / 2 = 6 A` and dissipate `12 * 6 = 72 W`. But the box clearly says 5 W, and if you measure the current in a running lamp, you get about 0.42 A. One of these numbers is very wrong, and it is not the multimeter.

Or: you put 0.3 V across a silicon diode and measure about a nanoamp. At 0.6 V you get a tenth of a milliamp. At 0.75 V, forty milliamps. Doubling the voltage multiplied the current by tens of thousands. What happened to `V = I * R`?

In both cases Ohm's law has stopped describing the part. If you design with it anyway, you will choose the wrong fuse, blow transistors at switch-on, or build an LED circuit that burns out the LED. This lesson shows when and why.

## The Physics

### What Ohm's law really says

In Lesson 03 you wrote `V = I * R`. That equation can be read in two very different ways:

1. **As a definition.** "Resistance is the ratio of voltage to current": `R = V / I`. This is always true, for any part, at any moment, because it just *defines* a number. It is true of a lamp, a diode, a human body. It is not very useful by itself.
2. **As a law.** "For this material, `R` is a constant: it does not depend on the voltage or the current." This is the real content of Ohm's law, and it is only true for some materials and some conditions.

A part is called **ohmic** when the second statement holds: its I-V curve is a straight line through the origin, and the slope of that line is `1 / R`.

### Why metals are ohmic (as long as the temperature stays put)

From Lesson 01 (What Resistance Is): electrons in a metal drift slowly under the push of the electric field and keep colliding with the vibrating atoms. Between collisions they speed up; at each collision they lose their extra speed. The average drift speed ends up proportional to the push, so the current is proportional to the voltage. The key condition is hidden: the rate of collisions must stay the same. That rate depends on how much the atoms vibrate, which is the temperature. Keep the temperature constant and a metal is beautifully ohmic. Let it heat up and the constant is no longer constant.

### Failure 1: things heat up

The current heats the part (Lesson 05). In a metal, hotter atoms vibrate more and scatter electrons more often, so the resistance rises. In a normal resistor this effect is tiny (tens of ppm per kelvin, Lesson 06) and the part stays only a little warm, so Ohm's law holds well.

An incandescent lamp is the opposite extreme: its whole purpose is to get a tungsten wire white-hot, about 2700 K (about 2400 C). Tungsten's resistance at that temperature is roughly 14 times its resistance at room temperature. So the lamp is a resistor whose value is set by its own current. That is a feedback loop:

```
more voltage -> more current -> more heat -> hotter filament
     ^                                             |
     |                                             v
     +-------- less current than expected <- more resistance
```

### Failure 2: materials where heat creates carriers

In carbon, in many metal oxides and in semiconductors (Phase 01, Lesson 07), there are few free electrons at room temperature. Heat shakes some loose, so *more* carriers can move and the resistance *falls* when warm. A **thermistor** is a part built to exaggerate this so you can measure temperature. Each thermistor has a constant resistance at a fixed temperature (it is ohmic at that temperature), but its resistance moves a lot when the temperature changes, including when it heats itself.

### Failure 3: the material itself is nonlinear

In a diode (Phase 11), the current does not come from electrons drifting through a uniform material. It comes from charges having to climb an energy barrier at the junction between two kinds of silicon. The number of charges with enough energy to climb grows exponentially with the voltage. No amount of keeping the temperature constant makes that a straight line. The I-V curve is a steep exponential:

```
I = I_s * (exp(V / V_T) - 1)
```

Read it as: "the current equals a tiny constant `I_s`, times `e` raised to the voltage divided by about 26 millivolts, minus one". You do not need to work with this formula yet; Phase 11 builds it from the physics. Just notice the shape: every extra 60 mV multiplies the current by about ten.

### Failure 4: extremes

- **Very strong fields.** Any insulator breaks down when the field is strong enough: air sparks at about 3 million volts per metre, and a resistor's film can arc (the limiting element voltage of Lesson 06).
- **Very high frequencies.** At radio frequencies, current crowds near the surface of a wire (the "skin effect"), so its resistance rises with frequency. Inductance and capacitance (Phases 07 and 08) also start to matter.
- **Very small or very cold things.** Superconductors drop to exactly zero resistance below a critical temperature. Atom-sized wires show resistance in fixed steps. Both are outside everyday circuits.

## The Concept

### The ohmic test

Measure the current at several voltages and compute `V / I` at each point. If the ratio stays the same, the part is ohmic in that range. A 100 ohm resistor:

| V | I | V / I |
|---|---|-------|
| 1 V | 10 mA | 100 ohm |
| 2 V | 20 mA | 100 ohm |
| 5 V | 50 mA | 100 ohm |
| 10 V | 100 mA | 100 ohm |

The ratio never moves. Its I-V curve is a straight line through zero:

```
 I
 |            /  ohmic: straight line
 |          /
 |        /
 |      /
 |    /
 |  /
 |/____________ V
```

### The lamp: hot and cold resistance

Take a 12 V, 5 W lamp. When it runs normally, Lesson 05 gives its hot resistance:

```
R_hot = V^2 / P = 12^2 / 5 = 144 / 5 = 28.8 ohm
I_hot = V / R_hot = 12 / 28.8 = 0.417 A
```

Tungsten's resistance grows roughly like the temperature (in kelvin) to the power 1.2. Going from room temperature (300 K) to 2700 K is a factor of 9 in temperature, so:

```
R_hot / R_cold = (2700 / 300)^1.2 = 9^1.2 = about 14
R_cold = 28.8 / 14 = about 2.06 ohm
```

That is the 2 ohm your multimeter read: the multimeter sends a tiny current that does not warm the filament.

The script works out the filament temperature at each voltage by balancing heat in against heat out: electrical power in (`V^2 / R(T)`) must equal the power the hot filament radiates as light and heat (which grows with `T^4`, the fourth power of the temperature). It finds the temperature where the two match, by trying a middle value and halving the search range again and again (a method called **bisection**). Results:

| V | Filament T | I | V / I |
|---|-----------|---|-------|
| 0.1 V | ~450 K | 30 mA | 3.3 ohm |
| 1 V | ~1040 K | 109 mA | 9.2 ohm |
| 2 V | ~1360 K | 159 mA | 12.6 ohm |
| 6 V | ~2070 K | 287 mA | 20.9 ohm |
| 12 V | 2700 K | 417 mA | 28.8 ohm |

The ratio `V / I` changes almost nine-fold across the range. The I-V curve bends over:

```
 I
 |         ___----  lamp: bends over, resistance grows
 |     _--
 |   /
 |  /
 | /
 |/____________ V
```

Doubling the voltage from 6 V to 12 V does not double the current: it goes from 287 mA to 417 mA, only 1.45 times.

### Inrush: the cold-filament surprise

At the instant you close the switch, the filament is still cold. It takes tens of milliseconds to heat. During that instant:

```
I_inrush = 12 / 2.06 = about 5.8 A      (14 times the running current)
```

This is why incandescent bulbs usually fail at the moment you switch them on, why old car circuits use fuses that tolerate short surges ("slow-blow"), and why a transistor that drives a lamp must survive many times the lamp's rated current for a moment.

### Static and dynamic resistance

For a nonlinear part, "its resistance" can mean two things:

- **Static resistance** `R_static = V / I`: draw a line from the origin to the operating point; it is the inverse slope of that line.
- **Dynamic resistance** `r = dV / dI`: the inverse slope of the curve itself at that point. Read `dV / dI` as "the small change in voltage divided by the small change in current it causes". It answers "if I wiggle the voltage a little, how much does the current wiggle?"

Numerically: measure the current at 5.99 V and 6.01 V, divide the voltage difference (0.02 V) by the current difference. For the lamp at 6 V:

```
static  V / I  = 20.9 ohm
dynamic dV/dI  = 38.8 ohm
```

They differ by almost a factor of two. For an ohmic resistor the two are always equal, which is one more way to test for ohmic behavior. Dynamic resistance becomes central in Phase 11 (diodes) and Phase 12 (transistors as amplifiers, "small-signal thinking").

### The thermistor formula

A typical NTC thermistor is described by its resistance at 25 C, `R_25`, and a constant `B` (in kelvin) from its datasheet:

```
R(T) = R_25 * exp( B * (1/T - 1/298.15) )
```

Read it as: "the resistance at temperature T (in kelvin) is the 25 C resistance, times `e` raised to B times the difference between one over T and one over 298.15 K". 298.15 K is 25 C. `exp(x)` means `e^x`, with `e = 2.718...`.

Worked example for a 10 kohm part with `B = 3950 K`, at 50 C (323.15 K):

```
1/323.15 - 1/298.15 = 0.0030945 - 0.0033540 = -0.0002595
B * (-0.0002595)    = 3950 * -0.0002595   = -1.025
exp(-1.025)         = 0.359
R(50 C) = 10 000 * 0.359 = about 3590 ohm
```

From 0 C to 100 C, the resistance falls from about 33.6 kohm to about 700 ohm: a factor of almost 50. A plain resistor with a tempco of 100 ppm/K would change by only 1 % over the same range.

### The diode: Ohm's law does not even start

Using a typical small silicon diode (`I_s = 10^-14 A`, `V_T = 0.02585 V` at room temperature):

| V | I | V / I |
|---|---|-------|
| 0.30 V | 1.1 nA | 270 Mohm |
| 0.50 V | 2.5 uA | 200 kohm |
| 0.60 V | 0.12 mA | 5 kohm |
| 0.70 V | 5.8 mA | 122 ohm |
| 0.75 V | 40 mA | 19 ohm |
| -1.00 V | -10 fA | 10^14 ohm |

(`nA` is nanoamp, 10^-9 A; `uA` is microamp, 10^-6 A; `fA` is femtoamp, 10^-15 A.) The "resistance" goes from 270 million ohms to 19 ohms over less than half a volt. Backwards, it blocks almost completely. Asking "what is the resistance of a diode?" has no single answer; you can only ask it at a given operating point.

```
 I
 |              |
 |              |  diode: nothing, then a wall
 |             /
 |           _/
 |________---______ V
            ~0.6 V
```

### So is Ohm's law useless?

Not at all. It is exact for the resistors you will use in almost every circuit, as long as they stay within their ratings. And even for nonlinear parts, engineers use it locally: near one operating point, any smooth curve looks like a straight line, with slope `1 / r`. That trick, "linearize around the operating point", is how we will analyze diodes and transistors later in the course. Ohm's law is the straight-line approximation that everything else is built on.

## Build It

The script `code/main.py` builds each example numerically and saves a three-panel plot, `out.png`.

### Step 1: The ohmic baseline

```python
for volts in [1.0, 2.0, 5.0, 10.0]:
    amps = volts / 100.0
    print(volts, amps * 1000, volts / amps)
```

`V / I` prints 100.0 ohm every time.

### Step 2: The lamp model

```python
def lamp_resistance(kelvin):
    return lamp_cold_ohms * (kelvin / ROOM_KELVIN) ** TUNGSTEN_EXPONENT


def heat_balance(kelvin, volts):
    electrical_in = volts**2 / lamp_resistance(kelvin)
    radiated_out = radiation_constant * (kelvin**4 - ROOM_KELVIN**4)
    return electrical_in - radiated_out
```

The cold resistance and the radiation constant are chosen so that at exactly 12 V the filament sits at 2700 K and dissipates 5 W, matching the box. `heat_balance` is positive when more power comes in than goes out (the filament would keep heating), negative when it would cool.

### Step 3: Finding the temperature by bisection

```python
def lamp_filament_temperature(volts):
    low, high = ROOM_KELVIN, 5000.0
    for _ in range(100):
        middle = (low + high) / 2
        if heat_balance(middle, volts) > 0:
            low = middle
        else:
            high = middle
    return (low + high) / 2
```

The answer is somewhere between 300 K and 5000 K. Test the middle: if the filament would still heat up there, the answer is hotter, so move the lower bound up; otherwise move the upper bound down. After 100 halvings the range is far smaller than any meaningful temperature difference.

### Step 4: Inrush and dynamic resistance

The inrush current is just `12 / R_cold`. The dynamic resistance is computed with a small step on each side of 6 V:

```python
dynamic = (2 * step) / (lamp_current(6.0 + step) - lamp_current(6.0 - step))
```

### Step 5 and Step 6: Thermistor and diode

```python
def thermistor_resistance(celsius, ohms_at_25=10_000.0, beta=3950.0):
    kelvin = celsius + 273.15
    return ohms_at_25 * np.exp(beta * (1 / kelvin - 1 / 298.15))


def diode_current(volts, saturation_amps=1e-14, thermal_volts=0.02585):
    return saturation_amps * (np.exp(volts / thermal_volts) - 1)
```

### Step 7: An automatic ohmic test

The script fits the best straight line through the origin (`I = slope * V`) and reports how far the worst point is from it. A resistor misses by 0.00 %; the lamp by over 80 % at its lowest voltage.

Run it:

```
uv run python phases/03-resistance-and-ohms-law/07-when-ohms-law-fails/code/main.py
```

## Use It

- **Inrush in real life.** Incandescent lamps, motors (Phase 08) and the big capacitors in power supplies (Phase 07) all draw a surge at switch-on. Power supplies often include an NTC thermistor in series with the input: cold, it has a few ohms and limits the surge; after a few seconds it heats up and drops to a fraction of an ohm.
- **Temperature sensing.** 10 kohm NTC thermistors with B around 3950 K are among the most common sensors in 3D printers, battery packs (so the charger can stop if the cells get hot), fridges and car engines.
- **PTC fuses.** "Polyfuses" (resettable fuses) are PTC parts: their resistance jumps up sharply when they get hot from too much current, limiting it, and comes back when they cool.
- **Diodes and LEDs.** Every LED circuit needs a series resistor (Phase 11, Lesson 07) because the LED's own "resistance" collapses once it turns on. The resistor, which *is* ohmic, is what sets the current.
- **Vintage tricks.** Old audio oscillators used a small incandescent lamp as an automatic volume control, exploiting exactly the resistance-grows-with-current effect shown here.

## Common Mistakes

- **Measuring a lamp with a multimeter and trusting the result.** The meter measures cold resistance. A lamp's working resistance can be over ten times higher.
- **Applying `R = V / I` from one operating point to another.** The 20.9 ohm the lamp shows at 6 V tells you nothing reliable about what it does at 12 V.
- **Believing `V = I * R` is always true and always useful.** As a definition it is always true; as a prediction with a constant `R` it is only true for ohmic parts.
- **Connecting a diode or LED straight to a battery.** With no resistor, the exponential curve means a small voltage excess gives an enormous current. The part burns.
- **Ignoring self-heating in sensors.** A thermistor carrying too much measuring current warms itself and reports a temperature higher than the real one.
- **Mixing up static and dynamic resistance.** For a nonlinear part they can differ by a large factor, and they answer different questions.

## Exercises

1. A part gives these readings: 1 V, 4 mA; 2 V, 8 mA; 3 V, 12 mA; 6 V, 24 mA. Is it ohmic? What is its resistance?
2. Another part gives: 1 V, 50 mA; 2 V, 80 mA; 4 V, 120 mA. Compute `V / I` at each point. Is it ohmic? Does its resistance grow or shrink with voltage, and what kind of part might it be?
3. A 230 V, 60 W household bulb runs with a filament at about 2800 K. Find its hot resistance and running current. If its cold resistance is 14 times smaller, what is the inrush current?
4. Using the thermistor formula with `R_25 = 10 kohm` and `B = 3950 K`, find the resistance at 0 C (273.15 K). Check against the script.
5. (Harder) Using the lamp table above, estimate the dynamic resistance between 10 V and 12 V by `(12 - 10) / (I_12 - I_10)`. Compare with the static resistance at 11 V (take the current as the average of the two). Why is the dynamic one larger?

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Ohm's law | "Voltage equals current times resistance, always" | For ohmic materials at fixed conditions, the ratio V / I is a constant independent of V and I |
| Ohmic | "A normal resistor" | A part whose I-V curve is a straight line through the origin |
| Nonlinear | "Weird part" | A part whose current is not proportional to voltage: lamps, thermistors, diodes, transistors |
| Static resistance | "The resistance" | V / I at a single operating point |
| Dynamic resistance | "The small-signal resistance" | dV / dI: the inverse slope of the I-V curve at the operating point |
| Inrush current | "Switch-on spike" | The large current drawn before a part reaches its steady state (cold filament, empty capacitor, stopped motor) |
| NTC thermistor | "A temperature sensor" | A resistor whose resistance falls strongly and predictably as temperature rises |

## Further Reading

- [All About Circuits, Vol. I, Chapter 2: "Nonlinear Conduction"](https://www.allaboutcircuits.com/textbook/direct-current/chpt-2/nonlinear-conduction/) — more examples of parts that do not follow Ohm's law
- *The Feynman Lectures on Physics*, Vol. II — the chapters on conduction give the physical picture behind ohmic behavior
- *Practical Electronics for Inventors* (Scherz & Monk), sections on thermistors and incandescent lamps
- A real NTC thermistor datasheet (for example the TDK/EPCOS B57164 or Vishay NTCLE100 series) — find R_25, the B value, and the resistance-temperature table
