# What a Sensor Is

> A sensor turns something in the world (heat, light, force, position) into an electrical quantity. Everything you need to know about it is in one curve, its transfer function, and in the honest list of ways the real curve differs from the ideal one.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 17 (Microcontrollers), Lesson 04 (ADC and DAC); Phase 04 (Kirchhoff's Laws), Lesson 05 (The Voltage Divider); Phase 05 (Circuit Analysis and Our Simulator), Lesson 06 (Thevenin and Norton)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Sensor | A device whose electrical output (voltage, current, resistance, capacitance) changes with a physical quantity. | A thermometer whose mercury column you read electronically. |
| Transducer | Anything that converts one form of energy or signal into another. Sensors are input transducers; speakers and motors are output transducers. | A translator between two languages. |
| Measurand | The physical quantity being measured (temperature, pressure...). | The thing you actually care about. |
| Transfer function | The rule, or curve, that relates the measurand to the sensor's output. | A conversion table from Celsius to sensor volts. |
| Sensitivity | How much the output changes per unit of measurand: the slope of the transfer function. | How far the mercury moves per degree. |
| Offset | The output when the measurand is zero (or at its reference point). | The mark the needle sits at before you start. |
| Range (span) | The interval of measurand the sensor is designed for. | The marks printed on the thermometer. |
| Linearity | How closely the transfer function follows a straight line. | Whether the marks on the ruler are evenly spaced. |
| Resolution | The smallest change that can be detected. | The spacing of the finest marks. |
| Accuracy | How close a reading is to the true value, on average. | Hitting the centre of the target. |
| Precision (repeatability) | How close repeated readings are to each other. | Grouping the shots tightly, wherever they land. |
| Calibration | Measuring known reference points and correcting the readings to match them. | Setting a kitchen scale to zero and checking it with a 1 kg bag. |
| Loading | When the thing reading the sensor draws current and changes the sensor's output. | Pressing on a bathroom scale to read it and changing the weight. |

## Learning Objectives

- Describe any sensor by its transfer function: sensitivity, offset, range and linearity
- Convert between sensor output, ADC code and measurand, and compute the resolution in physical units
- Show in the simulator how loading a potentiometer sensor bends its transfer function, and how to avoid it
- Correct gain and offset errors with a two-point calibration
- Tell accuracy from precision and from resolution, with numbers

## The Problem

Your thermostat must know the room temperature. Your phone must know which way is up. A car must know how far the accelerator pedal is pressed, how hot the engine is, how fast each wheel turns. Each of those needs a sensor, and behind every sensor lies the same chain:

```
physical world  ->  sensor  ->  electrical signal  ->  conditioning  ->  ADC  ->  number  ->  firmware
  (25.0 C)         (TMP36)       (0.750 V)            (Lesson 03)    (10 bit)    (232)      "24.8 C"
```

Errors creep in at every step. The sensor is not perfectly linear; its offset and gain differ from the datasheet; the circuit reading it disturbs it; the ADC rounds; noise adds scatter. A reading of "24.77 C" on a display looks precise, but is it right? This phase is about following a measurement down that chain and knowing, at each step, what you gained and what you lost. This first lesson sets up the vocabulary with three small experiments.

## The Physics

Sensors exploit some physical effect whose size depends on the measurand:

- **Resistance changes:** metals and semiconductors change resistance with temperature (thermistors, platinum RTDs); some materials change with light (photoresistors), with force (force-sensitive resistors), with stretching (strain gauges), with magnetic field.
- **Voltage generation:** two different metals joined make a voltage that depends on temperature (thermocouples, Phase 19, Lesson 02); a PN junction's voltage falls by about 2 mV per degree (Phase 11), which is what silicon temperature sensors like the TMP36 use; a magnetic field across a current-carrying chip makes a Hall voltage; light frees electrons in a photodiode, making a current.
- **Capacitance changes:** moving plates (accelerometers, pressure sensors, touch screens) change capacitance (Phase 07).

Whatever the effect, the sensor's job is to turn it into a voltage, current or resistance that a circuit can measure. The rest of this phase deals with that circuit.

## The Concept

### The transfer function

Describe a sensor by the curve "output versus measurand". For many sensors, over their working range, it is close to a straight line:

```
output = offset + sensitivity x measurand
```

The TMP36, a common silicon temperature sensor, is specified as 750 mV at 25 C with 10 mV per degree. Working back to 0 C: `750 - 25 x 10 = 500 mV`. So:

```
V_out = 0.500 V + 0.010 V/C x T
```

Read it as: "half a volt, plus ten millivolts for every degree Celsius". At 85 C: `0.5 + 0.85 = 1.35 V`. To read it, invert:

```
T = (V_out - 0.500) / 0.010
```

### Resolution in physical units

A 10-bit ADC on 3.3 V has an LSB of `3.3 / 1024 = 3.223 mV` (Phase 17, Lesson 04). With a sensitivity of 10 mV/C:

```
resolution = LSB / sensitivity = 3.223 mV / 10 mV/C = 0.32 C
```

The firmware cannot see changes smaller than about a third of a degree. In the simulation, a true 21.7 C becomes code 222 and reads back as 21.54 C. Notice also that the TMP36's output only spans 0.1 V to 1.75 V over its whole -40 C to 125 C range. It uses about half of the ADC's 3.3 V. Lesson 03 shows how to amplify and shift a signal to use the whole range and gain resolution.

### Loading: the reader changes the reading

A potentiometer makes a simple angle sensor: its wiper divides the supply in proportion to the shaft angle (Phase 04, Lesson 05). With a 10 kohm pot over 270 degrees on 3.3 V, the ideal output is `3.3 x angle / 270`.

```
  3.3 V --+
          |
        [ (1 - x) R ]
          |
          +------ wiper ----+----> to ADC
          |                 |
        [ x R ]           [ R_load ]
          |                 |
   gnd ---+-----------------+
```

But whatever reads the wiper is a load in parallel with the bottom part. With a 10 kohm load at mid-travel (x = 0.5): the bottom half is 5 k in parallel with 10 k, which is 3.33 k, so the output is `3.3 x 3.33 / (5 + 3.33) = 1.32 V` instead of 1.65 V. The simulation shows the error growing to about 33 degrees at 180 degrees of rotation, and zero at both ends. The transfer function has become a curve.

The remedy is the rule from Phase 06, Lesson 05 (Loading and Measurement Error): make the load at least 100 times bigger than the source's Thevenin resistance, or put a buffer amplifier between them (Lesson 03). A pot's Thevenin resistance is largest at mid-travel, `R / 4 = 2.5 kohm` for 10 kohm. With a 100 kohm load the error is a few percent; with a 1 Mohm load, under half a percent.

### Calibration: fixing gain and offset

Real sensors come with tolerances. Suppose ours reads 2% high in slope (gain error) and 15 mV high (offset error). Using the datasheet formula:

```
true 0 C:   V = 0.515 V   ->   reads 1.50 C
true 100 C: V = 0.500 + 1.02 + 0.015 = 1.535 V   ->   reads 103.5 C
```

The error grows with temperature. A **two-point calibration** measures the sensor at two known temperatures (an ice bath at 0 C and boiling water at 100 C, or two reference thermometers) and draws the straight line through them:

```
T = T_low + (V - V_low) x (T_high - T_low) / (V_high - V_low)
```

That removes both the gain and the offset error at once. The simulation shows every point back to the exact true value, because our fake sensor is perfectly linear. A real sensor's remaining error after calibration is its non-linearity.

### Accuracy, precision and resolution are different

- **Resolution** is the smallest step you can see (0.32 C above).
- **Precision** is how tightly repeated readings cluster (the standard deviation).
- **Accuracy** is how close the average is to the truth.

```
  precise, inaccurate      accurate, imprecise      accurate and precise
        . . .                 .         .                  ...
        ...                      . X .                     .X.
         X                    .    .    .                  ...
   (X = true value; dots = readings)
```

The simulation draws 1000 readings for each case. A sensor that always reads 26.50 C with a spread of 0.05 C is very precise and wrong by 1.5 C; one that averages 25.03 C with a spread of 1 C is accurate but noisy. Noise can be reduced by averaging (Lesson 06); bias can only be removed by calibration.

### Worked example: an error budget

Suppose a temperature reading has three independent error sources, each from its datasheet:

```
sensor accuracy:        +-0.5 C
ADC non-linearity:      +-2 LSB = +-2 x 3.22 mV = +-6.4 mV  ->  +-0.64 C at 10 mV/C
reference tolerance:    +-1% of the reading; at 25 C the sensor gives 0.750 V,
                        1% of that is 7.5 mV  ->  +-0.75 C
```

There are two ways to combine them:

- **Worst case:** all errors at their limit in the same direction: `0.5 + 0.64 + 0.75 = 1.89 C`. Guaranteed, but pessimistic.
- **Root sum of squares (RSS):** for independent random errors the squares add (the same rule as for noise in Lesson 06): `sqrt(0.5^2 + 0.64^2 + 0.75^2) = sqrt(0.25 + 0.41 + 0.5625) = sqrt(1.22) = 1.1 C`. A realistic "typical" figure.

So this design should be described as "about +-1 C typical, +-2 C worst case". Notice that the biggest term is the reference, not the ADC: buying a 16-bit ADC would hardly help; a better reference (0.1%) would cut the RSS error to about 0.8 C. An error budget tells you where to spend money.

### Worked example: when is a pot's load small enough?

A 10 kohm potentiometer's Thevenin resistance at position x is `x (1 - x) R` (the two parts in parallel), largest at mid-travel: `0.25 x 10 k = 2.5 kohm`. The loading error there is roughly `R_th / R_load` for large loads:

```
R_load = 100 k:  error about 2.5 k / 100 k = 2.5%    (the simulation shows 1.610 V instead of 1.650 V: -2.4%)
R_load = 1 M:    error about 0.25%
R_load = 10 M:   error about 0.025%
```

For a 10-bit ADC (one LSB is 0.1% of full scale), you need the error below about half an LSB, so the load must be above roughly 5 Mohm, or the signal must be buffered (Lesson 03).

### Worked example: reading a datasheet's error table

A pressure sensor's datasheet promises: offset 0.200 V +- 50 mV, sensitivity 45 mV/kPa +- 2%, non-linearity 0.25% of full scale, full scale 100 kPa. What is the worst error at 50 kPa before and after calibration?

```
offset error:       50 mV / 45 mV per kPa             = 1.11 kPa
gain error:         2% of 50 kPa                       = 1.00 kPa
non-linearity:      0.25% of 100 kPa                   = 0.25 kPa
worst case total:   1.11 + 1.00 + 0.25                 = 2.36 kPa   (4.7% of the reading)
```

A two-point calibration removes the offset and gain errors (they are straight-line errors), leaving only the non-linearity: 0.25 kPa, ten times better. That is why calibration matters so much: for most sensors the straight-line errors are the big ones.

### Hysteresis and drift

Two more words you will meet in datasheets:

- **Hysteresis:** the reading depends on the direction you came from. A sensor that reads 50.2 kPa when the pressure rises to 50 kPa and 49.8 kPa when it falls to 50 kPa has 0.4 kPa of hysteresis. Calibration cannot fix it, because there is no single straight line.
- **Drift:** slow change of offset or gain with time or temperature, for example "offset drift 0.1 mV/C". Over a 40 C temperature swing that is 4 mV, about 0.09 kPa here. Calibration at one temperature does not remove it; a temperature sensor next to the main sensor and a correction in firmware can.

## Build It

### Step 1: Sensor, ADC and back

`tmp36_volts` is the transfer function. `adc_code` floors to the 10-bit code; the script converts back to degrees and prints the readings for several temperatures.

### Step 2: The loaded potentiometer

```python
def potentiometer_reading(fraction, pot_ohms, load_ohms):
    top = max(pot_ohms * (1 - fraction), 1e-3)
    bottom = max(pot_ohms * fraction, 1e-3)
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", VDD)
    circuit.resistor("RTOP", "vdd", "wiper", top)
    circuit.resistor("RBOT", "wiper", "0", bottom)
    if load_ohms:
        circuit.resistor("RLOAD", "wiper", "0", load_ohms)
    return circuit.dc().v("wiper")
```

The pot is two resistors whose sum is constant. At the ends one of them would be zero ohms, which a resistor cannot be, so we use a milliohm instead.

### Step 3: Calibration

The script builds raw readings with a 2% gain error and 15 mV offset, converts them naively, then with the two-point line.

### Step 4: Accuracy and precision

Random readings with a fixed seed (`np.random.default_rng(1)`), so every run prints the same numbers.

Run it:

```
uv run python phases/19-sensors-and-signals/01-what-a-sensor-is/code/main.py
```

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
A linear temperature sensor (TMP36-like: 500 mV at 0 C, 10 mV per C) read by a 10-bit, 3.3 V ADC
  sensitivity 10 mV/C, ADC step 3.223 mV -> resolution 0.322 C per code
   true C  sensor V  code  reading C
    -10.0   0.400 V   124    -10.04 C
      0.0   0.500 V   155     -0.05 C
     21.7   0.717 V   222     21.54 C
     25.0   0.750 V   232     24.77 C
     85.0   1.350 V   418     84.71 C
    125.0   1.750 V   543    124.99 C

A potentiometer as an angle sensor (0 to 270 degrees), loaded by what reads it
   angle  ideal V  100 k load  10 k load  error at 10 k
     0 deg  0.000 V     0.000 V    0.000 V        -0.0 deg
    45 deg  0.550 V     0.542 V    0.483 V        -5.5 deg
    90 deg  1.100 V     1.076 V    0.900 V       -16.4 deg
   135 deg  1.650 V     1.610 V    1.320 V       -27.0 deg
   180 deg  2.200 V     2.152 V    1.800 V       -32.7 deg
   225 deg  2.750 V     2.712 V    2.415 V       -27.4 deg
   270 deg  3.300 V     3.300 V    3.300 V        -0.0 deg
  worst error with a 10 kohm load: -32.7 degrees, so the transfer function is no longer a straight line

Two-point calibration of a sensor with a 2% gain error and a +15 mV offset
  true   0.0 C: datasheet formula says   1.50 C (error +1.50), calibrated   0.00 C
  true  20.0 C: datasheet formula says  21.90 C (error +1.90), calibrated  20.00 C
  true  40.0 C: datasheet formula says  42.30 C (error +2.30), calibrated  40.00 C
  true  60.0 C: datasheet formula says  62.70 C (error +2.70), calibrated  60.00 C
  true  80.0 C: datasheet formula says  83.10 C (error +3.10), calibrated  80.00 C
  true 100.0 C: datasheet formula says 103.50 C (error +3.50), calibrated 100.00 C

Accuracy versus precision: 1000 readings of a 25.00 C object
  precise but inaccurate   mean  26.50 C (error +1.50), spread (std)  0.05 C
  accurate but imprecise   mean  25.03 C (error +0.03), spread (std)  1.02 C
  accurate and precise     mean  25.00 C (error +0.00), spread (std)  0.05 C
```

## Use It

- **Sensor datasheets** always have a table of "transfer function" or "output vs temperature", accuracy ("±1 C at 25 C, ±2 C over the full range" for the TMP36), and the conditions (supply, load) under which those numbers hold. Read the conditions.
- **Digital sensors** (for example the BME280 or TMP117) contain the sensor, the conditioning, the ADC and factory calibration in one package and send numbers over I2C or SPI (Phase 17, Lesson 06). The same chain is still there, just inside the chip.
- **Ratiometric measurement:** a potentiometer or resistive divider powered from the ADC's own reference gives readings that do not depend on the exact supply voltage, because both the sensor and the ADC scale with it.
- **Calibration** in industry follows standards traceable to national laboratories. In products, a one-point (offset only) or two-point calibration is often done on the production line and stored in the microcontroller's flash.

## Common Mistakes

- **Confusing resolution with accuracy.** A 16-bit reading of a sensor that is ±2 C accurate is still only ±2 C accurate.
- **Ignoring the load.** Whatever reads a sensor draws current; check its input resistance against the sensor's output resistance.
- **Using the datasheet's typical values as truth.** Typical means "many parts are close to this". Design with the minimum and maximum.
- **Calibrating at only one point when the gain is off.** One point fixes the offset only.
- **Forgetting the ADC reference.** If VDD is the ADC reference and it drifts, every reading drifts with it (unless the sensor is ratiometric).
- **Trusting a single reading.** Look at the spread of many readings before believing the last digit.

## Exercises

1. A pressure sensor outputs 0.5 V at 0 kPa and 4.5 V at 100 kPa, linearly. What is its sensitivity, and what pressure gives 2.3 V? (40 mV/kPa; 45 kPa.)
2. That sensor is read by a 12-bit ADC with a 5 V reference. What is the resolution in kPa? (1.22 mV / 40 mV/kPa = 0.031 kPa.)
3. A 50 kohm pot at mid-travel is read by an ADC whose input looks like 200 kohm. What is the output on 3.3 V, and the error in percent? (Bottom: 25 k || 200 k = 22.2 k; 3.3 x 22.2 / 47.2 = 1.553 V; error -5.9%.)
4. A thermometer reads 1.2 C in ice water and 98.1 C in boiling water (at a place where water boils at 99.5 C). Write the two-point correction and correct a reading of 37.0 C. (T = (R - 1.2) x 99.5 / 96.9; 36.76 C.)
5. Harder: in `main.py`, add a third load case of 1 Mohm and find the worst angle error. Then derive, for a pot of resistance R loaded by R_L at fraction x, the output formula `V = VDD x (x R || R_L) / ((1 - x) R + (x R || R_L))` and check it against the simulator at x = 0.5.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Transfer function | "The sensor's curve" | The relation between measurand and output |
| Sensitivity | "Gain" | Slope of the transfer function, e.g. 10 mV/C |
| Offset | "Zero error" | Output at the reference value of the measurand |
| Resolution | "Precision" (wrongly) | The smallest detectable change |
| Accuracy | "How good it is" | Closeness of the average reading to the truth |
| Precision | "Stability" | Closeness of repeated readings to each other |
| Calibration | "Adjusting it" | Measuring known references and correcting gain and offset |
| Loading | "The ADC pulls it down" | The reading circuit drawing current and changing the sensor's output |

## Further Reading

- [Analog Devices, TMP35/TMP36/TMP37 datasheet](https://www.analog.com/en/products/tmp36.html) — a clear example of a transfer function, accuracy specification and loading conditions
- Jacob Fraden, *Handbook of Modern Sensors*, 5th ed. (Springer), Chapter 3 (Transfer function, sensitivity, accuracy, calibration)
- [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/), sections on measurement process characterization (accuracy, precision, calibration)
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., chapter on sensors
