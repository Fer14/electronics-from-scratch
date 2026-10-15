# Signal Conditioning

> A raw sensor signal is usually too small, sitting at the wrong level, too weak to drive anything, or buried on top of a big common voltage. Conditioning is the circuit that shifts, stretches, buffers and cleans it until it fits the ADC exactly.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 19 (Sensors and Signals), Lessons 01-02; Phase 13 (Operational Amplifiers), Lessons 01, 03 and 04 (The Ideal Op-Amp, Inverting and Non-Inverting Amplifiers, Summers and Difference Amplifiers); Phase 04 (Kirchhoff's Laws), Lesson 07 (The Wheatstone Bridge)
**Time:** ~85 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Signal conditioning | Any circuit between a sensor and an ADC that makes the signal easier to measure. | Adjusting a photo's brightness and contrast before printing it. |
| Gain | How many times the circuit multiplies the signal (Phase 13). | The zoom on a camera. |
| Offset (level shift) | Adding or subtracting a fixed voltage to move the signal. | Moving a picture up or down on the page. |
| Full-scale range | The voltages the ADC can measure, here 0 to 3.3 V. | The size of the page. |
| Difference amplifier | An op-amp circuit whose output is a gain times the difference of two inputs. | A balance scale that shows only the difference in weight. |
| Buffer (voltage follower) | An op-amp with gain 1 that copies a voltage while drawing almost no current from it. | A relay runner who takes the baton and does the hard running. |
| Output impedance | The Thevenin resistance behind a signal (Phase 05): how much its voltage drops when loaded. | How weak a person's voice is: the weaker, the more a noisy room drowns it. |
| Clipping | When an amplifier's output hits its supply rail and cannot go further. | Shouting into a microphone louder than it can record. |
| Strain gauge | A thin metal foil pattern glued to a part; stretching it changes its resistance slightly. | A rubber band that gets a bit thinner when pulled. |
| Gauge factor | The fractional change of resistance per unit of strain (about 2 for metal foil). | How sensitive the rubber band is. |
| Strain | Stretch divided by original length, a pure number; often in microstrain (1 ue = 1e-6). | A 1 m bar stretched by 1 mm has 1000 microstrain. |
| Common-mode voltage | The average voltage of two inputs, which is not the signal. | The water level of a lake on which two boats bob: you care about the waves between them, not the level. |
| CMRR | Common-mode rejection ratio: how well an amplifier ignores a voltage common to both inputs. | How well the scale ignores the weight of the pans. |
| Instrumentation amplifier | A precision difference amplifier with very high input impedance and high CMRR, made for bridges and small differences. | A laboratory balance. |

## Learning Objectives

- Compute the gain and offset needed to map a sensor's output range onto an ADC's full range, and the resolution gained
- Build a difference amplifier in the simulator that subtracts a reference and amplifies, and see clipping at the rails
- Show how a high-impedance source is loaded by an ADC input and fixed by a buffer
- Compute the tiny output of a strain-gauge bridge and amplify it, and explain why resistor mismatch turns common-mode voltage into error
- Choose resistors for a conditioning stage and check them with `sim`

## The Problem

In Lesson 01 the TMP36 gave 0.5 V to 1.0 V over 0-50 C, on an ADC that spans 0 to 3.3 V. It uses 15% of the ADC's range: 85% of the codes are wasted. A strain gauge measuring the bending of a steel beam produces a couple of millivolts, riding on top of 2.5 V. A pH probe or a piezoelectric sensor has an output impedance of megohms: connect it to an ADC and the reading collapses.

Each of these problems is solved by a small op-amp circuit placed between sensor and ADC. Conditioning is where analog design meets measurement: get it right and a cheap ADC gives excellent readings; get it wrong and no amount of software can recover what was lost.

## The Physics

### Information lives in codes

An ADC with N bits divides its full range into `2^N` steps (Phase 17, Lesson 04). A signal that spans only a fraction of the range uses only that fraction of the codes. The resolution in physical units is:

```
resolution = LSB / (sensitivity x gain)
```

So amplifying the signal by `G` before the ADC makes each code `G` times finer in physical terms. (It does not remove noise that is already on the sensor; that is Lesson 06.)

### Amplifiers cannot exceed their supply

An op-amp's output is made by transistors between its supply rails. It cannot produce a voltage outside them (and many cannot even reach them). Ask for more and it clips. This is a feature here as well as a limit: an op-amp powered from 0 V and 3.3 V can never feed more than 3.3 V into the ADC. Rail-to-rail op-amps get within millivolts of both rails.

### Small strain, small signal

A metal foil gauge's resistance is `R = rho L / A` (Phase 03, Lesson 02). Stretch it: it gets longer and thinner, so its resistance rises. The fractional change is proportional to the strain:

```
delta_R / R = GF x strain
```

With `GF = 2` and 1000 microstrain (a steel beam near its working limit): `delta_R / R = 0.002`. A 350 ohm gauge changes by 0.7 ohm. That is far too small to see in a simple divider, which is why gauges go in a **Wheatstone bridge** (Phase 04, Lesson 07): two dividers side by side, whose outputs are equal at rest, so only the change appears between them.

## The Concept

### Mapping a range onto the ADC

Sensor range 0.5 V to 1.0 V; ADC range 0 V to 3.3 V. We want:

```
V_adc = G x (V_sensor - V_offset)
```

so that 0.5 V maps to 0 V and 1.0 V maps to (just under) 3.3 V:

```
V_offset = 0.5 V
G = 3.3 / (1.0 - 0.5) = 6.6
```

Leave a little headroom for tolerances and choose `G = 6.2` (a standard resistor ratio: 62 k / 10 k). Then 50 C gives `6.2 x 0.5 = 3.1 V`.

With a 12-bit ADC (`LSB = 3.3 / 4096 = 0.806 mV`):

```
raw:          0.806 mV / 10 mV per C            = 0.081 C per code
conditioned:  0.806 mV / (10 mV per C x 6.2)    = 0.013 C per code
```

### The difference amplifier

From Phase 13, Lesson 04:

```
   V_sensor --[ R1 ]--+------------ (+)
                      |                 \
                    [ R2 ]               op-amp >---+--- V_out
                      |                 /           |
                     gnd     +-------- (-)          |
                             |                      |
   V_ref ----[ R1 ]----------+-------[ R2 ]---------+
```

If both R1 match and both R2 match:

```
V_out = (R2 / R1) x (V_sensor - V_ref)
```

Read it as: "the output is the resistor ratio times the difference between the two inputs". Our numbers: `R1 = 10 k`, `R2 = 62 k`, `V_ref = 0.5 V`. Note the requirement that the pairs match. If they do not, the circuit no longer subtracts exactly; we will see the consequences below.

Below 0 C, the ideal output would be negative; at 60 C it would be 3.72 V. With the op-amp powered from 0 V and 3.3 V, the simulation shows both clipped to the rails: 0.000 V and 3.300 V. The ADC is safe, but readings outside the designed range all look the same. Firmware should treat codes at the very top or bottom as "out of range", not as valid temperatures.

### Buffering a weak source

A source with 100 kohm of output impedance (a high-value divider, a pH probe through a cable, a filter) into an ADC whose input looks like 1 Mohm on average (the sample-and-hold capacitor being charged repeatedly behaves like a resistance):

```
V_adc = 1.000 x 1 M / (100 k + 1 M) = 0.909 V       a 9% error
```

A **voltage follower** (op-amp with its output tied to its minus input) has a gain of exactly 1 and an input that draws almost nothing:

```
  source --[ 100 k ]--+-- (+)
                      |       \
                      |        op-amp >---+--- to ADC
                      |       /           |
                      +-(-)--/------------+   (minus tied to output)
```

Its output is a copy of its input, now driven by the op-amp's low output impedance. In the simulation: 0.99999 V.

### The strain-gauge bridge

```
          V_ex = 5 V
           |       |
         [R1]     [R3]
           |       |
   left ---+       +--- right
           |       |
         [R2]     [R_gauge]
           |       |
          gnd     gnd
```

At rest all four are 350 ohm: both midpoints sit at 2.5 V and the difference is 0. With the gauge at `R (1 + x)` where `x = GF x strain`, the right side moves by about `V_ex x x / 4`:

```
V_bridge = V_ex x GF x strain / 4 = 5 x 2 x 0.001 / 4 = 2.5 mV       (at 1000 microstrain)
```

To read it with a 3.3 V ADC we want about 1 V for the full load, so a gain of 400. But both bridge outputs sit at 2.5 V. That 2.5 V is the **common-mode voltage**: it is the same on both inputs, it carries no information, and the amplifier must ignore it while amplifying the 2.5 mV difference by 400.

### Why matching matters: common-mode rejection

If the difference amplifier's resistor ratios differ by a fraction `epsilon`, part of the common-mode voltage leaks through. Roughly, the error at the output is about `epsilon x V_cm` (times a factor close to 1 for high gains):

```
0.1% mismatch:   0.001 x 2.5 V = 2.5 mV at the output
1% mismatch:     0.01  x 2.5 V = 25 mV at the output
```

Divide by the gain and the bridge sensitivity to see what strain that looks like: 25 mV / 400 / 2.5 mV per 1000 ue = about 25 microstrain of fake reading, with nothing applied. The simulation shows exactly these numbers. That is why bridge measurements use **instrumentation amplifiers** (the INA128, AD620, INA333 and friends), with laser-trimmed internal resistors that match to 0.01% or better, and why their datasheets quote CMRR of 100 dB or more (a factor of 100 000).

### Worked example: a 4-20 mA current loop

Industrial sensors often send their reading as a current between 4 mA (bottom of the range) and 20 mA (top), because a current is not changed by the resistance of long wires. The receiver turns it into a voltage with a **shunt resistor** to ground. Which resistor for a 3.3 V, 12-bit ADC?

```
165 ohm:  20 mA x 165 = 3.30 V    exactly full scale: no headroom
150 ohm:  4 mA -> 0.60 V,  20 mA -> 3.00 V              leaves 10% headroom
```

Choose 150 ohm. Then:

```
span: 3.00 - 0.60 = 2.40 V, which is 2.40 / 0.000 806 = 2978 codes over the 16 mA span
resolution: 16 mA / 2978 = 5.4 uA per code, or 0.034% of the range
power in the shunt at 20 mA: 0.020^2 x 150 = 60 mW
```

The 4 mA "live zero" is a feature: a reading below about 3.6 mA (0.54 V) means a broken wire or a dead sensor, which a 0-20 mA or a 0-10 V signal could not tell apart from "zero". The firmware maps `I = V / 150` and then `value = (I - 4 mA) / 16 mA x full range`.

### Worked example: offset and gain from two points

Any linear mapping is fixed by two points. For the TMP36 example we wanted `(0.5 V -> 0 V)` and `(1.0 V -> 3.1 V)`:

```
gain   = (3.1 - 0) / (1.0 - 0.5) = 6.2
offset = the input that must map to 0 V = 0.5 V
V_out  = 6.2 x (V_in - 0.5)
```

Check the middle: 25 C gives 0.75 V, and `6.2 x 0.25 = 1.55 V`, the middle of 0-3.1 V. The same two-point method gives the gain and offset for any sensor and ADC pair; then you pick resistors (R2 / R1 = gain) and a reference voltage (the offset).

## Build It

### Step 1: A difference amplifier with optional rails

```python
def difference_amplifier(v_sensor, v_reference, r1, r2, rails=None, mismatch=1.0):
    circuit = Circuit()
    circuit.voltage_source("VS", "sensor", "0", v_sensor)
    circuit.voltage_source("VREF", "ref", "0", v_reference)
    circuit.resistor("R1A", "sensor", "plus", r1)
    circuit.resistor("R2A", "plus", "0", r2 * mismatch)
    circuit.resistor("R1B", "ref", "minus", r1)
    circuit.resistor("R2B", "minus", "out", r2)
    circuit.opamp("U1", plus="plus", minus="minus", out="out", gain=1e5, rails=rails)
    return circuit.dc().v("out")
```

Without `rails` the op-amp is linear and can output any voltage; with `rails=(0.0, VDD)` its output is limited to the supply.

### Step 2: Buffer or no buffer

`source_into_adc` puts a 1 V source behind 100 kohm and loads it with 1 Mohm, either directly or through a voltage follower.

### Step 3: The bridge and the instrumentation stage

`bridge_output` builds the four-resistor bridge with the gauge changed by `R x GF x strain` and returns the difference and the common-mode voltage. `instrumentation_stage` is a difference amplifier with a gain of 400 and an optional mismatch on one resistor.

Run it:

```
uv run python phases/19-sensors-and-signals/03-signal-conditioning/code/main.py
```

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
A TMP36-like sensor gives 0.5 V at 0 C and 1.0 V at 50 C; the 12-bit ADC spans 0 to 3.3 V (LSB 0.806 mV)
  raw: 0.5 V of a 3.3 V range is used -> 0.081 C per code
  difference amplifier: Vout = (R2 / R1) x (Vsensor - 0.5 V), R2 / R1 = 62 k / 10 k = 6.2
   temp   sensor  amp out   ideal
    0 C  0.500 V  0.000 V 0.000 V
   10 C  0.600 V  0.620 V 0.620 V
   25 C  0.750 V  1.550 V 1.550 V
   40 C  0.900 V  2.480 V 2.480 V
   50 C  1.000 V  3.100 V 3.100 V
  conditioned: 0.0130 C per code, 6.2 times finer

If the op-amp runs from 0 V and 3.3 V, outputs beyond its rails are clipped
   -5 C: ideal -0.310 V, with rails  0.000 V
   50 C: ideal  3.100 V, with rails  3.100 V
   60 C: ideal  3.720 V, with rails  3.300 V

A high-impedance source (1.000 V behind 100 kohm) into an ADC that looks like 1 Mohm
  direct: 0.9091 V (error -9.09%), through a voltage follower: 0.99999 V

Strain gauge in a Wheatstone bridge (350 ohm, gauge factor 2, 5 V excitation)
      strain  bridge out   formula  x 400 amp
       0 ue    0.000 mV   0.000 mV    0.000 V
     250 ue    0.625 mV   0.625 mV    0.250 V
     500 ue    1.249 mV   1.250 mV    0.500 V
    1000 ue    2.498 mV   2.500 mV    0.999 V
  both bridge outputs sit near 2.50 V: that common-mode voltage must NOT be amplified
  resistor ratio off by  0.0%: output with zero strain =     0.00 mV (equivalent to    0.0 microstrain)
  resistor ratio off by  0.1%: output with zero strain =     2.49 mV (equivalent to    2.5 microstrain)
  resistor ratio off by  1.0%: output with zero strain =    24.69 mV (equivalent to   24.7 microstrain)
```

## Use It

- **Op-amps for conditioning:** rail-to-rail input and output parts that run from a single 3.3 V or 5 V supply, such as the MCP6002, OPA333, TLV9002 or LMV358. Their datasheets give "output swing to rail" (how close they get) and input offset voltage (a few microvolts to millivolts, which adds directly to your signal).
- **Instrumentation amplifiers:** INA128/INA129 and AD620 (one resistor sets the gain), INA333 (low power, rail-to-rail). Load cells in kitchen and bathroom scales use bridge sensors with dedicated 24-bit bridge ADCs like the HX711, which include the amplifier.
- **Reference voltages** for the offset come from a divider buffered by an op-amp, or better from a reference chip (TL431, REF30xx), because any noise or drift on V_ref goes straight into the result.
- **ADC driver amplifiers** buffer the signal and often add an RC filter right at the ADC input (Lesson 04): the capacitor supplies the sample-and-hold's charge spikes, the resistor isolates the op-amp.
- **Programmable gain amplifiers (PGAs)** inside many ADC chips let firmware choose the gain for each channel.

## Try It in the Lab

The lab has the difference amplifier of this lesson with R1 = 10 kohm fixed, a 0.5 V reference, and the sensor at its hottest (1.0 V, meaning 50 C). Choose the two R2 resistors so the output lands between 2.9 V and 3.3 V. The op-amp runs from 5 V in this lab, so too much gain will not clip at 3.3 V: it will push the ADC pin over its limit. Also think about what happens if the two R2 are not equal.

## Common Mistakes

- **Amplifying the offset along with the signal.** A gain of 6.6 applied to the TMP36's 0.5-1.0 V without subtracting 0.5 V gives 3.3-6.6 V: always clipped. Shift first, or shift and amplify together as the difference amplifier does.
- **No headroom.** Designing for exactly 3.3 V full scale means resistor tolerances push some boards over. Aim for 90-95% of the range.
- **Ignoring the op-amp's output swing.** A non-rail-to-rail op-amp on 3.3 V might only reach 1.5 V to 2 V from each rail. Read the datasheet.
- **Loading a high-impedance source.** Always compare the source's Thevenin resistance with the input resistance of what follows; buffer if they are within a factor of 100.
- **Mismatched resistors in difference amplifiers.** 1% resistors give poor common-mode rejection; use 0.1% resistors, matched networks, or an instrumentation amplifier.
- **Forgetting the reference's noise.** Whatever wobbles on V_ref is subtracted from the signal, sign and all.

## Exercises

1. A pressure sensor outputs 0.2 V to 2.2 V. Map it to 0-3.0 V on a 3.3 V ADC: what offset and gain? (Offset 0.2 V; gain 3.0 / 2.0 = 1.5.)
2. Choose R2 for that gain with R1 = 10 kohm, from the E24 series (10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91). (15 k gives exactly 1.5.)
3. A source with 47 kohm output impedance feeds an input of 470 kohm. What is the error? With a 0.1% target, what minimum input resistance is needed? (-9.1%; 47 Mohm.)
4. A bridge of 120 ohm gauges (GF 2.1) at 3.3 V excitation sees 500 microstrain. What is the bridge output? Which gain gives about 2 V? (3.3 x 2.1 x 0.0005 / 4 = 0.866 mV; gain about 2300.)
5. Harder: in `main.py`, replace the single-op-amp difference amplifier by a three-op-amp instrumentation amplifier (two non-inverting buffers with a shared gain resistor, followed by a difference amplifier with gain 1). Check that its CMRR with a 1% mismatch in the second stage is better than the single-stage version, because most of the gain now happens before the mismatched stage.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Signal conditioning | "The analog front end" | Shifting, scaling, buffering and filtering a signal for the ADC |
| Difference amplifier | "A subtractor" | Vout = (R2 / R1)(V+ - V-) with matched resistor pairs |
| Buffer | "A follower" | Unity-gain op-amp that isolates a weak source from its load |
| Clipping | "Saturation" | Output stuck at a supply rail because the requested value is beyond it |
| Common-mode voltage | "The DC level" | The average of the two inputs, carrying no signal |
| CMRR | "Noise rejection" | Ratio of differential gain to common-mode gain, usually in dB |
| Instrumentation amplifier | "In-amp" | A difference amplifier with high input impedance, set gain and very high CMRR |

## Further Reading

- [Texas Instruments, "Handbook of Operational Amplifier Applications" (SBOA092)](https://www.ti.com/lit/an/sboa092b/sboa092b.pdf) — difference amplifiers, buffers and single-supply design
- [Analog Devices, "A Designer's Guide to Instrumentation Amplifiers" (Kitchin and Counts)](https://www.analog.com/media/en/training-seminars/design-handbooks/designers-guide-instrument-amps-complete.pdf) — CMRR, bridges and the three-op-amp in-amp
- [Texas Instruments, INA333 datasheet](https://www.ti.com/product/INA333) — a modern low-power instrumentation amplifier with bridge application circuits
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 5 (Precision Circuits)
