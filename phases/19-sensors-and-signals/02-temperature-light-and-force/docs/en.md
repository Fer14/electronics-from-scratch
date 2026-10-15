# Temperature, Light and Force

> Many of the most useful sensors are just resistors that change with the world. Put one in a divider with the right partner and its resistance becomes a voltage the ADC can read; choose the partner badly and you throw most of the signal away.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 19 (Sensors and Signals), Lesson 01 (What a Sensor Is); Phase 04 (Kirchhoff's Laws), Lesson 05 (The Voltage Divider); Phase 11 (Semiconductors and Diodes), Lesson 01 (Why Silicon); Phase 17 (Microcontrollers), Lesson 04 (ADC and DAC)
**Time:** ~85 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Thermistor | A resistor made of a semiconducting ceramic whose resistance changes strongly with temperature. "Thermal resistor". | A sponge that soaks up more water the warmer it gets. |
| NTC / PTC | Negative / positive temperature coefficient: resistance falls / rises as temperature rises. Most sensing thermistors are NTC. | Honey, which flows more easily when warm (NTC), versus a self-resetting fuse that blocks current when it heats up (PTC). |
| R25 | The thermistor's resistance at 25 C, its "name" value (for example 10 kohm). | Its shoe size. |
| B value (beta) | One number, in kelvin, that says how steeply an NTC's resistance changes with temperature. | How quickly the sponge changes. |
| Steinhart-Hart equation | A more accurate three-constant formula for thermistors. | A finer conversion table. |
| Kelvin (K) | Temperature measured from absolute zero: K = C + 273.15. Physics formulas need it. | Counting floors from the basement instead of from the ground floor. |
| Self-heating | The measuring current warming the thermistor itself, making it read high. | A thermometer warmed by the hand holding it. |
| Dissipation constant | How many watts raise a thermistor by one kelvin above its surroundings (mW/K). | How easily the hand's warmth leaks away. |
| LDR (photoresistor) | A resistor whose resistance falls as light increases. | A window blind that opens wider in sunlight. |
| FSR (force-sensitive resistor) | A thin film whose resistance falls as it is pressed. | A sponge that conducts better when squeezed. |
| Thermocouple | Two different metals joined at a point; a voltage appears that depends on the temperature difference between the hot and cold junctions. | A tiny battery powered by a temperature difference. |
| Cold-junction compensation | Measuring the temperature where the thermocouple wires meet the circuit, and correcting for it. | Knowing the temperature of your own hand when you judge how hot water is. |
| Geometric mean | The square root of the product of two numbers: sqrt(a x b). | The "middle" of two numbers on a logarithmic scale. |

## Learning Objectives

- Compute an NTC thermistor's resistance at any temperature with the B equation, and invert it to turn a resistance back into a temperature
- Design a divider for a resistive sensor: choose the fixed resistor for the largest swing over a range (`sqrt(R_min x R_max)`) or the highest sensitivity at one temperature (`R_fixed = R_sensor` there)
- Follow a reading all the way from temperature to ADC code and back, with the simulator solving the divider
- Estimate self-heating error from the dissipation constant
- Compare thermistors, LDRs, force-sensitive resistors and thermocouples, and know what each needs from the circuit

## The Problem

A 10 kohm thermistor costs a few cents and is in every kettle, battery pack, 3D printer and car. It is not a voltage source: it is a resistor. To read it with an ADC (Phase 17, Lesson 04) you must turn resistance into voltage, and the simplest way is a divider with a fixed resistor. But which fixed resistor? With 1 kohm, the ADC sees a reading that moves only 0.6 V over 0 to 50 C; with 10 kohm it moves 1.7 V. The same thermistor, the same ADC, nearly three times the information, just from choosing one resistor well.

And the thermistor is not linear: its resistance falls by a factor of nearly ten between 0 C and 50 C. The firmware must undo that curve to show degrees. LDRs and force sensors have the same structure and the same problems. This lesson builds the tools once and applies them to all of them.

## The Physics

### Why a thermistor's resistance falls with temperature

An NTC thermistor is a ceramic of metal oxides that behaves like a semiconductor (Phase 11, Lesson 01). Its charge carriers have to be freed by thermal energy before they can conduct. The number of free carriers grows roughly like `e^(-E / kT)`: a little more temperature frees many more carriers, so the resistance drops steeply. (A metal does the opposite: it already has plenty of free electrons, and heat just makes the atoms vibrate more and scatter them, so its resistance rises slowly. That is how platinum RTDs work.)

This gives the **B equation**:

```
R(T) = R25 x e^( B x (1/T - 1/T25) )
```

Read it as: "the resistance at temperature T is the 25-degree resistance times e raised to B times the difference of the inverse absolute temperatures". T must be in kelvin: `T = C + 273.15`, and `T25 = 298.15 K`.

For a 10 kohm, B = 3950 thermistor at 0 C (273.15 K):

```
1/273.15 - 1/298.15 = 0.003 661 0 - 0.003 354 0 = 0.000 307 0
B x 0.000 307 0 = 3950 x 0.000 307 0 = 1.2126
R = 10 000 x e^1.2126 = 10 000 x 3.362 = 33.6 kohm
```

At 50 C the same steps give 3.59 kohm; at 100 C, 0.70 kohm.

Inverting (solve for T):

```
1/T = 1/T25 + ln(R / R25) / B
```

`ln` is the natural logarithm, the inverse of `e^x`. For higher accuracy, the Steinhart-Hart equation adds a cubic term: `1/T = A + B ln(R) + C (ln R)^3`, with three constants from the datasheet or from calibration at three temperatures.

### Light and force

An **LDR** (Phase 17, Lesson 07) is a semiconductor film whose carriers are freed by photons instead of heat; its resistance follows roughly `R = R10 x (lux / 10)^(-gamma)`. It is slow (tens of milliseconds) and imprecise, but cheap and sensitive.

An **FSR** is a polymer film with conductive particles; pressing pushes them into contact. Its resistance falls roughly in inverse proportion to force (from megohms untouched to a few kohm under a firm press). It is good for "how hard" (touch, grip, a weight on a seat), not for precise weighing.

### The thermocouple: a voltage, not a resistance

Join two different metals (for type K, chromel and alumel) at a "hot" end. Along each wire, a temperature gradient pushes electrons differently (the Seebeck effect), so a small voltage appears between the two free ends, proportional to the temperature *difference* between the hot junction and the "cold" junction where the wires meet your circuit:

```
V = S x (T_hot - T_cold),     S ~ 41 uV/C for type K
```

Read it as: "the voltage is the Seebeck coefficient times the temperature difference". Two consequences: the signal is tiny (4.1 mV at 100 C above the cold junction) so it needs a large gain (Lesson 03), and you must measure the cold-junction temperature separately (often with a thermistor or a silicon sensor) and add it back. Thermocouples shine at high temperatures (type K works to over 1000 C) where thermistors cannot go.

## The Concept

### Turning resistance into voltage

```
   3.3 V
     |
   [ R_sensor ]       thermistor, LDR or FSR
     |
     +------> V_out  (to the ADC)
     |
   [ R_fixed ]
     |
    gnd
```

```
V_out = VDD x R_fixed / (R_sensor + R_fixed)
```

With the sensor on top, a falling sensor resistance (hotter, brighter, harder) raises the output. Putting the sensor at the bottom inverts the direction; either is fine.

### Choosing R_fixed for the biggest swing

Over a range, the sensor goes from `R_max` (cold) to `R_min` (hot). The swing of the output is:

```
swing = VDD x [ R_f / (R_min + R_f) - R_f / (R_max + R_f) ]
```

If `R_f` is tiny, both readings sit near 0 V; if it is huge, both sit near VDD. In between there is a best value. Taking the derivative of the swing with respect to `R_f` and setting it to zero (or simply trying many values in the code, as exercise 5 does) gives:

```
R_f(best) = sqrt(R_min x R_max)
```

For 0-50 C: `sqrt(3.59 k x 33.6 k) = sqrt(120.6e6) = 10.98 kohm`. A standard 10 kohm is almost perfect. The simulation compares five values:

| R_fixed | V at 0 C | V at 50 C | Swing |
|---------|----------|-----------|-------|
| 1 k | 0.095 V | 0.719 V | 0.62 V |
| 3.3 k | 0.295 V | 1.581 V | 1.29 V |
| 10 k | 0.757 V | 2.429 V | 1.67 V |
| 33 k | 1.635 V | 2.976 V | 1.34 V |
| 100 k | 2.470 V | 3.186 V | 0.72 V |

Notice the symmetry: 1 k and 100 k give the same swing, as do 3.3 k and 33 k. On a logarithmic scale they are equally far from 10 k.

### Choosing R_fixed for the best sensitivity at one point

If one temperature matters most (a fridge at 4 C, a body at 37 C), make `R_fixed` equal to the sensor's resistance *at that temperature*. The divider's slope `dV/dR_sensor` is then steepest there. With R_fixed = 10 k, the sensitivity at 25 C is about 37 mV per degree: more than three times the TMP36's 10 mV/C, from one cheap part.

### From code back to temperature

The firmware reverses every step:

```
code  ->  V = (code + 0.5) x VDD / 1024           (the middle of the code's interval)
V     ->  R_sensor = R_fixed x (VDD - V) / V      (the divider, solved for R_sensor)
R     ->  T = 1 / (1/T25 + ln(R / R25) / B) - 273.15
```

In the simulation, true temperatures of 5, 21.3, 37 and 48 C come back as 5.04, 21.30, 37.01 and 48.04 C. Notice that if the ADC uses VDD as its reference, VDD cancels out: the code depends only on the ratio of resistances. That is a **ratiometric** measurement, insensitive to supply drift.

### Self-heating

The divider's current flows through the thermistor and heats it by `P = I^2 R`. A small bead thermistor might have a dissipation constant of about 1.5 mW per kelvin in still air: every 1.5 mW it dissipates raises it 1 K above the air it is measuring. With 10 k at 50 C the thermistor carries about 0.24 mA with 0.87 V across it: 0.21 mW, so `0.21 / 1.5 = 0.14 K` too warm. With 1 k fixed the current is larger and the error reaches 1.2 K. Big fixed resistors reduce self-heating; for precision, also power the divider only while reading.

### Worked example: finding the best fixed resistor by trying

Instead of calculus, try values around the expected answer and compute the swing by hand, with the thermistor at 33.62 kohm (0 C) and 3.588 kohm (50 C):

```
R_f = 8.2 k:   cold 3.3 x 8.2 / 41.82  = 0.647 V    hot 3.3 x 8.2 / 11.79  = 2.296 V    swing 1.648 V
R_f = 10 k:    cold 3.3 x 10 / 43.62   = 0.757 V    hot 3.3 x 10 / 13.59   = 2.429 V    swing 1.672 V
R_f = 10.98 k: cold 3.3 x 10.98 / 44.60 = 0.812 V   hot 3.3 x 10.98 / 14.57 = 2.487 V   swing 1.675 V
R_f = 12 k:    cold 3.3 x 12 / 45.62   = 0.868 V    hot 3.3 x 12 / 15.59   = 2.540 V    swing 1.672 V
R_f = 15 k:    cold 3.3 x 15 / 48.62   = 1.018 V    hot 3.3 x 15 / 18.59   = 2.663 V    swing 1.645 V
```

The maximum is indeed at the geometric mean, and it is very flat: anything from 8.2 k to 15 k is within 2% of the best. Good news for designers, who can pick a standard value without worrying.

### Worked example: a fridge thermometer

A fridge should be read accurately around 4 C. The thermistor there is:

```
1/277.15 - 1/298.15 = 0.003 608 2 - 0.003 354 0 = 0.000 254 2
R(4 C) = 10 000 x e^(3950 x 0.000 254 2) = 10 000 x e^1.004 = 27.3 kohm
```

For the best sensitivity *at 4 C*, choose `R_fixed = R(4 C)`, so 27 kohm. The divider then sits near mid-supply (1.65 V) at 4 C, where its slope is steepest. A quick check of the sensitivity: at 3.5 C and 4.5 C the thermistor is about 28.0 k and 26.6 k, giving 1.620 V and 1.662 V: about 42 mV per degree, so a 10-bit ADC (3.2 mV per code) resolves better than 0.1 C.

### Worked example: is the self-heating acceptable?

With 27 k fixed and 27.3 k of thermistor, the divider current is `3.3 / 54.3 k = 61 uA`, and the thermistor dissipates `61e-6^2 x 27 300 = 0.10 mW`. With a dissipation constant of 1.5 mW/K that is 0.07 C of self-heating: smaller than the resolution, so fine. Inside a sealed probe in still air the dissipation constant can be several times smaller; then powering the divider only during readings helps.

### Worked example: an LDR night switch

A street light should switch on below about 10 lux. Use the LDR on top and a fixed resistor equal to its resistance at the switching point, `R(10 lux) = 10 kohm`, so the divider sits at mid-supply exactly there and has its steepest slope:

```
 5 lux:  R = 10 k x 0.5^(-0.7) = 16.2 k   ->  V = 3.3 x 10 / 26.2 = 1.26 V
10 lux:  R = 10 k                         ->  V = 1.65 V
20 lux:  R = 10 k x 2^(-0.7)   = 6.16 k   ->  V = 3.3 x 10 / 16.16 = 2.04 V
```

A comparator (or the ADC) switches at 1.65 V. Halving or doubling the light moves the voltage by about 0.4 V either way, a big, easy-to-detect change. To stop the light flickering on and off at dusk, real designs add hysteresis: switch on below 1.55 V and off above 1.75 V (Phase 13, Lesson 02).

## Build It

### Step 1: The thermistor equations

```python
def thermistor_ohms(celsius):
    return R25 * np.exp(BETA * (1 / (celsius + KELVIN) - 1 / (25 + KELVIN)))


def thermistor_celsius(ohms):
    return 1 / (1 / (25 + KELVIN) + np.log(ohms / R25) / BETA) - KELVIN
```

### Step 2: The divider in the simulator

```python
def divider_volts(sensor_ohms, fixed_ohms):
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", VDD)
    circuit.resistor("RSENSOR", "vdd", "out", float(sensor_ohms))
    circuit.resistor("RFIX", "out", "0", float(fixed_ohms))
    result = circuit.dc()
    return result.v("out"), result.p("RSENSOR")
```

It also returns the sensor's power, for self-heating.

### Step 3: Compare fixed resistors

For each of 1 k to 100 k, the script prints the readings at 0 C and 50 C, the swing, the sensitivity at 25 C (the change between 24.5 C and 25.5 C) and the self-heating at 50 C.

### Step 4: The full read-back chain, and other sensors

It converts four temperatures to codes and back, then runs the LDR, the FSR and the thermocouple.

Run it:

```
uv run python phases/19-sensors-and-signals/02-temperature-light-and-force/code/main.py
```

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
NTC thermistor: R25 = 10 kohm, B = 3950 K
     0 C:   33.621 kohm
    25 C:   10.000 kohm
    50 C:    3.588 kohm
   100 C:    0.698 kohm

Divider with the thermistor on top and a fixed resistor below, read from 0 C to 50 C
  fixed resistor that maximises the swing: sqrt(R(0 C) x R(50 C)) = 10.98 kohm
     fixed  V at 0 C  V at 50 C   swing  mV/C at 25 C  self-heat at 50 C
     1.0 k   0.095 V    0.719 V 0.624 V        12.1         1.237 C
     3.3 k   0.295 V    1.581 V 1.286 V        27.4         0.549 C
    10.0 k   0.757 V    2.429 V 1.672 V        36.7         0.141 C
    33.0 k   1.635 V    2.976 V 1.342 V        26.2         0.019 C
   100.0 k   2.470 V    3.186 V 0.716 V        12.1         0.002 C

Reading it back: 10-bit ADC code -> volts -> resistance -> temperature (10 k fixed)
  true   5.0 C -> 0.9186 V -> code  285 ->  25.867 kohm ->   5.04 C
  true  21.3 C -> 1.5130 V -> code  469 ->  11.810 kohm ->  21.30 C
  true  37.0 C -> 2.0639 V -> code  640 ->   5.988 kohm ->  37.01 C
  true  48.0 C -> 2.3789 V -> code  738 ->   3.866 kohm ->  48.04 C

Light: LDR on top of a 10 k resistor
       1 lux: LDR    50.12 kohm -> 0.549 V
      10 lux: LDR    10.00 kohm -> 1.650 V
     100 lux: LDR     2.00 kohm -> 2.751 V
...
```

## Use It

- **Thermistor datasheets** (for example Vishay's NTCLE100E3 series or Murata's NCP series) give R25, the B value (often specified between two temperatures, like B25/85), a resistance-temperature table, the tolerance (1-5%) and the dissipation constant.
- **Battery packs** have an NTC on a dedicated "thermistor" pin of the charger chip (Lesson 06 of Phase 18), which stops charging when the cell is too cold or too hot.
- **3D printers** read their hot-end thermistors with exactly this divider (often a 4.7 k pull-up) and a lookup table in the firmware.
- **LDRs** turn street lights on at dusk; photodiodes and digital light sensors (like the BH1750) replace them where speed or accuracy matters.
- **FSRs** (for example the Interlink FSR 402) are used in musical controllers, seat occupancy sensors and robot grippers.
- **Thermocouple interface chips** like the MAX31855 or MAX31856 contain the amplifier, cold-junction sensor, linearisation and ADC, and output degrees over SPI.

## Try It in the Lab

The lab draws the same thermistor divider twice, once at 0 C (33.6 kohm) and once at 50 C (3.59 kohm), and asks for the fixed resistor in both. The cold reading must be above 0.5 V, the hot one below 2.8 V, and the difference at least 1.5 V. Compute the three candidates' readings with the divider formula and think about which goal each wrong choice breaks, and why the right one is close to the geometric mean.

## Common Mistakes

- **Using Celsius in the B equation.** It needs kelvin. With Celsius the numbers are wildly wrong.
- **Picking R_fixed equal to R25 out of habit.** It is ideal only if 25 C is where you need the most sensitivity, and close to ideal for ranges centred on it. For a range, use `sqrt(R_min R_max)`.
- **Treating the divider output as linear in temperature.** It is not; convert through resistance and the B or Steinhart-Hart equation, or use a lookup table.
- **Too much current.** Self-heating makes the sensor read high, especially in still air.
- **Forgetting the cold junction.** A thermocouple measures a difference; without the cold-junction temperature, its reading is meaningless.
- **Expecting precision from LDRs and FSRs.** They vary from part to part and with temperature and age; use them for "more or less", not for exact values.

## Exercises

1. Compute the resistance of a 10 k, B = 3950 thermistor at 37 C. (T = 310.15 K; 1/310.15 - 1/298.15 = -0.000 129 8; x 3950 = -0.5126; R = 5.99 kohm.)
2. A thermistor reads 15 kohm. What is its temperature? (1/T = 1/298.15 + ln(1.5)/3950 = 0.003 456 7; T = 289.3 K = 16.1 C.)
3. For a fridge sensor (0 to 10 C), what fixed resistor gives the biggest swing? (R(10 C) = 20.2 k; sqrt(33.6 x 20.2) = 26.0 k, so 27 k.)
4. A 4.7 k pull-up and a 100 k thermistor are used on a 3D printer hot-end at 230 C (where the thermistor is about 0.25 kohm). What is the reading on 3.3 V with the thermistor at the bottom? What is the self-heating power? (3.3 x 0.25 / 4.95 = 0.167 V; I = 0.667 mA, P = 0.11 mW.)
5. Harder: modify `main.py` to sweep R_fixed from 1 k to 100 k in fine steps and find the swing maximum numerically. Does it land at 10.98 k? Then repeat for the range -20 C to 80 C.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| NTC thermistor | "A temperature resistor" | A ceramic semiconductor whose resistance falls steeply with temperature |
| B value | "Beta" | The constant in R = R25 e^(B (1/T - 1/T25)) |
| Steinhart-Hart | "The accurate formula" | 1/T = A + B ln R + C (ln R)^3 |
| Ratiometric | "Supply-independent" | The reading depends only on a ratio of resistances when the ADC reference is the divider's supply |
| Self-heating | "Reading high" | The measuring current warms the sensor |
| Thermocouple | "A high-temperature probe" | A junction of two metals giving about tens of microvolts per degree of difference |
| Cold-junction compensation | "CJC" | Measuring and adding the temperature where the thermocouple meets the circuit |

## Further Reading

- [Vishay, NTCLE100E3 thermistor datasheet](https://www.vishay.com/docs/29049/ntcle100.pdf) — R/T tables, B values and dissipation constants for a common 10 k part
- [Texas Instruments, SBAA338 "Monitoring NTC Thermistor Circuit With Single-Ended ADC" (Analog Engineer's Circuit)](https://www.ti.com/lit/an/sbaa338/sbaa338.pdf) — linearising and reading NTCs with an ADC
- [Interlink Electronics, FSR 400 Series integration guide](https://www.interlinkelectronics.com/fsr-400) — force-to-resistance curves and the divider circuit for FSRs
- [Analog Devices, MAX31855 datasheet](https://www.analog.com/en/products/max31855.html) — thermocouple signal levels and cold-junction compensation in one chip
