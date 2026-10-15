# Loading and Measurement Error

> Every meter becomes part of the circuit it measures. Your job is to make that part small enough not to matter.

**Type:** Build
**Prerequisites:** Phase 04 Lesson 05 (The Voltage Divider), Phase 05 Lesson 06 (Thevenin and Norton), Phase 06 Lesson 04 (Inside the Multimeter)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Loading | Changing a circuit by connecting something to it, including a meter | Checking the tyre pressure lets a little air out |
| Measurement error | The difference between what the meter shows and what was there before the meter came | The thermometer cooling the cup of tea it is measuring |
| Input resistance (R_m) | The resistance a voltmeter adds between the two points it touches | The size of the hole the gauge pokes in the pipe |
| Source resistance | How "stiff" the point you measure is: its Thevenin resistance | How hard the pipe pushes back when you take water out |
| Thevenin equivalent | Any circuit seen from two points, reduced to one voltage source and one series resistor | Summarising a whole plumbing system as "a tank and a pipe" |
| High-impedance node | A point driven through large resistances, easily disturbed | A whisper: any noise drowns it |
| Low-impedance node | A point driven through small resistances, hard to disturb | A shout |
| Burden | What an ammeter steals from the circuit, as a voltage drop | A toll booth on the road |
| Systematic error | An error that is always in the same direction and can be calculated | A scale that always reads 1 kg heavy |

## Learning Objectives

- Explain why connecting a voltmeter changes the voltage it measures.
- Predict a meter's reading from the Thevenin equivalent of the measured point and the meter's input resistance.
- Choose a meter (or decide a measurement is untrustworthy) using the ratio of meter resistance to source resistance.
- Recover the true voltage from readings of meters with known input resistance.
- Quantify an ammeter's burden error and choose the right way to connect a voltmeter and an ammeter to measure a resistance.

## The Problem

You build a voltage divider from two 1 Mohm resistors on a 10 V supply. The math says the middle is at 5 V. Your digital multimeter says 4.76 V. Your friend's old analog meter says 1.4 V. Neither meter is broken, and the resistors are fine.

Or: a sensor gives a weak signal through a 100 kohm resistor, your microcontroller's input reads it wrong, and you spend a day looking for a software bug.

The cause is the same: the measuring device draws current from the circuit and becomes part of it. In this lesson you learn to predict that effect exactly, to know when it matters, and to correct for it.

## The Physics

A voltmeter works by letting a small current flow through itself (Lesson 04): the analog movement needs current to move its needle, and the digital meter's input divider is a 10 Mohm chain of resistors. Either way, when you touch two points with the probes, you connect a resistor R_m between them.

That new resistor draws current. Where does the current come from? From the circuit, through whatever resistances lie between the measured point and the source. Current through those resistances makes voltage drops, so the measured point moves. The voltage you read is the voltage of the new circuit (circuit plus meter), not of the old one.

An ammeter has the opposite problem. It must sit in the path of the current, and it has a small but non-zero resistance (its shunt, fuse and leads). The current now flows through an extra resistor, so it gets smaller.

There is no meter that does not disturb anything. Even a perfect digital input has some resistance and some capacitance. The art is making the disturbance small compared to the accuracy you need.

## The Concept

### The divider before and after the meter

```
   before                         after
   10 V --[ R1 1 M ]--+           10 V --[ R1 1 M ]--+---------+
                      |                              |         |
                   [ R2 1 M ]                     [ R2 1 M ] [ R_m ]  meter
                      |                              |         |
   0 V ---------------+           0 V ---------------+---------+
```

Before: the middle is at 10 * 1 M / (1 M + 1 M) = 5 V.

After: the meter is in parallel with R2. Two resistors in parallel combine to (R2 * R_m) / (R2 + R_m) (Phase 04). With a 10 Mohm digital meter:

1. R2 parallel R_m = (1 M * 10 M) / (1 M + 10 M) = 10 / 11 M = 0.909 Mohm.
2. New divider: 10 * 0.909 / (1 + 0.909) = 10 * 0.909 / 1.909 = 4.762 V.

The meter shows 4.762 V, a -4.8 % error. With a 200 kohm analog meter:

1. 1 M parallel 200 k = 200 / 1.2 = 166.7 kohm.
2. 10 * 166.7 / (1000 + 166.7) = 1.429 V. Error: -71 %.

### The Thevenin shortcut

Recomputing the whole circuit every time is tedious. Phase 05 gave us a better tool: seen from the two points you measure, any linear circuit is equivalent to a voltage source V_th in series with a resistor R_th.

```
   the circuit, as the meter sees it

     (+) V_th
      |
    [ R_th ]
      |
      o-----------+
                [ R_m ]   meter
      o-----------+
```

- V_th is the voltage with nothing connected: the "true" value you wanted to measure.
- R_th is the resistance looking back into the circuit with its sources set to zero (voltage sources replaced by wires).

For a divider: V_th = V * R2 / (R1 + R2) and R_th = R1 parallel R2.

Now the meter and R_th form a simple divider, so the reading is:

    reading = V_th * R_m / (R_m + R_th)

Read it: "the meter shows the true voltage times the meter's share of the total resistance."

For the 1 M / 1 M divider: V_th = 5 V, R_th = 500 kohm. With the DMM: 5 * 10 / 10.5 = 4.762 V. Same answer, one line.

### The error depends on a ratio

Rewrite the relative error:

    error = reading / V_th - 1 = -R_th / (R_m + R_th)

When R_m is much bigger than R_th this is about -R_th / R_m. So:

| R_m / R_th | Error |
|---|---|
| 10 | about -9 % |
| 100 | about -1 % |
| 1000 | about -0.1 % |
| 10 000 | about -0.01 % |

**Rule of thumb:** for 1 % accuracy, the meter's input resistance must be at least 100 times the source resistance of the point you measure.

That explains the same meters giving perfect readings on a 1 k / 1 k divider (R_th = 500 ohm). The DMM's ratio is 10 M / 500 = 20 000: error -0.005 %. Even the 200 kohm analog meter has a ratio of 400: -0.25 %. The stiff circuit does not care; the soft one does.

### Choosing the range on an analog meter

On an analog meter the input resistance changes with the range: R_m = (ohms per volt) * (range). A higher range loads less but gives a smaller needle swing. Take a 20 kohm/V meter on the 1 M / 1 M divider (V_th = 5 V, R_th = 500 kohm):

| Range | R_m = 20 000 * range | Reading = 5 * R_m / (R_m + 500 k) | Needle position |
|---|---|---|---|
| 10 V | 200 kohm | 1.43 V | 14 % of scale |
| 50 V | 1 Mohm | 3.33 V | 7 % of scale |
| 250 V | 5 Mohm | 4.55 V | 2 % of scale |
| 1000 V | 20 Mohm | 4.88 V | 0.5 % of scale |

The higher ranges give a truer value but you can barely read the needle. There is no setting that is both accurate and readable here: the honest answer is "use a higher-resistance meter", or use the two-reading trick below.

### Undoing the error

If you know R_m and R_th, you can correct the reading:

    V_th = reading * (R_m + R_th) / R_m

Often you don't know R_th. Then take two readings with two meters (or two ranges of one analog meter, which have different R_m). Call them V_a with R_a and V_b with R_b. Each reading satisfies reading = V_th - (reading / R_m) * R_th (the true voltage minus the drop on R_th caused by the meter's current). Two equations, two unknowns:

    R_th = (V_b - V_a) / (V_a / R_a - V_b / R_b)
    V_th = V_a * (R_a + R_th) / R_a

Example: the DMM reads 4.762 V (R_a = 10 M) and the analog meter 1.429 V (R_b = 200 k).

1. V_a / R_a = 4.762 / 10 000 000 = 0.000 000 476 2 A (0.476 microamps).
2. V_b / R_b = 1.429 / 200 000 = 0.000 007 145 A (7.145 microamps).
3. R_th = (1.429 - 4.762) / (0.000 000 476 2 - 0.000 007 145) = -3.333 / -0.000 006 669 = about 500 000 ohm.
4. V_th = 4.762 * (10 M + 0.5 M) / 10 M = 5.000 V.

The circuit's hidden truth, recovered from two "wrong" readings.

### The ammeter's burden

An ammeter of resistance R_A in series with a circuit of resistance R adds to it. The current changes from V / R to V / (R + R_A). Error is about -R_A / R.

Example: 3.3 V across 33 ohm should give 100 mA. On a mA range whose shunt, fuse and leads total 1.5 ohm:

- I = 3.3 / (33 + 1.5) = 3.3 / 34.5 = 95.65 mA. Error -4.3 %.

On the 10 A range (about 0.06 ohm): 3.3 / 33.06 = 99.82 mA, error -0.18 %. Surprising but true: for a low-voltage circuit, the higher current range can be more accurate, because its shunt is smaller, even though its resolution is worse.

**Rule of thumb:** the ammeter's resistance must be much smaller than the circuit resistance; equivalently, its burden voltage must be much smaller than the supply voltage.

### Measuring a resistor with two meters

To measure a resistance R_x while it carries current, you can use a voltmeter and an ammeter at the same time. There are two ways to wire them, and each has its own error.

```
  (a) voltmeter right across R_x          (b) voltmeter across ammeter + R_x

  V --[ A ]--+-------+                    V --+--[ A ]--+
             |       |                        |         |
          [ R_x ]  ( V )                    ( V )    [ R_x ]
             |       |                        |         |
  0 ---------+-------+                    0 --+---------+
```

- **(a)** The voltmeter reads exactly the voltage on R_x, but the ammeter counts R_x's current plus the voltmeter's. You measure R_x parallel R_m: always a bit low. Fine when R_x is much smaller than R_m.
- **(b)** The ammeter reads exactly R_x's current, but the voltmeter includes the ammeter's burden. You measure R_x + R_A: always a bit high. Fine when R_x is much bigger than R_A.

With a 10 Mohm voltmeter and a 1 ohm ammeter:

| R_x | (a) result | (b) result |
|---|---|---|
| 10 ohm | 9.99999 ohm (-0.0001 %) | 11 ohm (+10 %) |
| 1 Mohm | 0.909 Mohm (-9.1 %) | 1.000001 Mohm (+0.0001 %) |

Small resistors: wiring (a). Large resistors: wiring (b). (For tiny resistances, engineers go further with "four-wire" or Kelvin measurement, where separate wires carry the current and sense the voltage.)

## Build It

### Step 1 and Step 2: Four meters, two dividers

```python
def divider_reading(top_ohms, bottom_ohms, meter_ohms, volts=10.0):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", volts)
    c.resistor("R1", "vcc", "mid", top_ohms)
    c.resistor("R2", "mid", "0", bottom_ohms)
    if meter_ohms is not None:
        c.resistor("Rmeter", "mid", "0", meter_ohms)
    return c.dc().v("mid")
```

A meter in the simulator is just a resistor. Output:

```
  ideal meter               : reads 5.000 V, error   +0.0 %
  DMM, 10 Mohm              : reads 4.762 V, error   -4.8 %
  analog 20 kohm/V on 10 V  : reads 1.429 V, error  -71.4 %
  analog 1 kohm/V on 10 V   : reads 0.098 V, error  -98.0 %
```

On the 1 kohm divider the same four meters read 5.0000, 4.9998, 4.9875 and 4.7619 V.

### Step 3: The Thevenin prediction

```python
def predicted_reading(open_volts, thevenin_ohms, meter_ohms):
    return open_volts * meter_ohms / (meter_ohms + thevenin_ohms)
```

For three dividers (including an unequal 100 k / 47 k one), the one-line prediction matches the full simulation to four decimals.

### Step 4: Recover the truth

```python
def solve_two_readings(reading_a, meter_a, reading_b, meter_b):
    thevenin_ohms = (reading_b - reading_a) / (reading_a / meter_a - reading_b / meter_b)
    open_volts = reading_a * (meter_a + thevenin_ohms) / meter_a
    return open_volts, thevenin_ohms
```

From the rounded readings 4.762 V and 1.429 V the script recovers 5.000 V and 500 kohm.

### Step 5: Burden

The script compares an ideal ammeter, a 1.5 ohm mA range and a 0.06 ohm 10 A range in a 3.3 V, 33 ohm circuit: 100.00, 95.65 and 99.82 mA.

### Step 6: Two wirings

`measure_resistor` builds both wirings with a 1 ohm ammeter and a 10 Mohm voltmeter and reproduces the table above.

Run it:

```bash
uv run python phases/06-sources-batteries-and-measurement/05-loading-and-measurement-error/code/main.py
```

## Use It

- **Typical DMM:** 10 Mohm on DC volts. Fine for anything with source resistance below about 100 kohm at 1 %. Some meters offer a "high input impedance" mode above 1 Gohm on the 200 mV range for this reason.
- **Oscilloscope inputs:** 1 Mohm, or 10 Mohm with a x10 probe (Lesson 06). Same rule applies.
- **Microcontroller ADC inputs:** datasheets specify a maximum source resistance (often around 10 kohm) because the converter briefly draws current to charge an internal capacitor. Feed it from a soft divider and the readings come out low and noisy; the fix is a buffer amplifier (Phase 13) or a capacitor at the pin.
- **pH electrodes and some sensors** have source resistances of hundreds of megaohms; they need meters with input resistance above 10^12 ohm.
- **"Ghost voltages."** A high-impedance meter on a disconnected mains wire can show tens of volts coupled from neighbouring wires through tiny capacitances. Electricians use "low impedance" (LoZ) modes, which deliberately load the wire to make such ghosts collapse.
- **Shunt-based current measurement in products** uses milliohm resistors so the burden is tiny, then amplifies the small voltage.

## Try It in the Lab

A 10 V source feeds a divider of two 100 kohm resistors. The true middle voltage is 5 V. You must choose which voltmeter to use; in the slot, a meter is simply its input resistance. The reading must be within 1 % of the truth.

Before you press RUN:

- What is the Thevenin resistance of the middle node?
- How large must R_m be for a -1 % error at most?
- Which candidates are too small, and by how much do they pull the voltage down?

## Common Mistakes

- **Blaming the circuit for a meter's effect.** If a reading looks wrong in a high-resistance circuit, compute R_m / R_th before changing anything.
- **Thinking the analog meter's sensitivity is fixed.** Its input resistance is (ohms per volt) * (range). A higher range loads less, at the cost of resolution.
- **Forgetting the meter's current in the ammeter.** In wiring (a), the ammeter counts the voltmeter's current too.
- **Using the mA range "for accuracy" in a low-voltage circuit.** Its higher burden can be a bigger error than its extra digit gains.
- **Assuming a digital input is infinite.** Microcontroller pins, ADCs and scope inputs all have finite resistance and some capacitance.
- **Measuring a node through a long thin wire or a resistor "because it was easier."** Anything in series with the probe adds to R_th as seen by the meter.

## Exercises

1. A 47 k / 47 k divider on 12 V is measured with a 10 Mohm DMM. What does it read? What is the error in percent?
2. A sensor has V_th = 2.000 V and R_th = 220 kohm. What minimum meter input resistance gives at most 0.5 % error?
3. An analog meter (20 kohm/V) reads 3.0 V on its 10 V range and 4.0 V on its 50 V range at the same point. Find V_th and R_th.
4. A 5 V circuit draws 25 mA through a 200 ohm load. You insert an ammeter with 4 ohm total resistance. What current does it read, and what is the burden voltage?
5. You must measure a 2.2 kohm resistor with a 10 Mohm voltmeter and a 5 ohm ammeter. Which wiring, (a) or (b), gives the smaller error? Compute both.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Loading | "The meter changed the voltage" | The meter's resistance becomes part of the circuit and moves the operating point |
| Input resistance | "Meter impedance" | Resistance the voltmeter connects between its probes |
| Source resistance | "Output impedance" | Thevenin resistance seen looking into the measured point |
| Loading error | "The meter reads low" | -R_th / (R_m + R_th), roughly -R_th / R_m |
| Burden | "Ammeter drop" | Voltage across an ammeter's internal resistance, which reduces the circuit's current |
| Four-wire measurement | "Kelvin connection" | Separate current-carrying and voltage-sensing wires to remove lead resistance from the reading |

## Further Reading

- All About Circuits, *Lessons in Electric Circuits*, Volume I (DC), chapter 8, section "Voltmeter impact on measured circuit" and section on Kelvin (4-wire) measurement: https://www.allaboutcircuits.com/textbook/direct-current/chpt-8/voltmeter-impact-measured-circuit/
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 1 (Thevenin equivalent, input and output impedance, and their "10x rule").
- Keithley (Tektronix), *Low Level Measurements Handbook*, for loading, burden voltage and high-impedance measurements.
- Microchip or STMicroelectronics application notes on ADC source impedance for microcontrollers (for example ST AN2834 "How to get the best ADC accuracy in STM32 microcontrollers").
