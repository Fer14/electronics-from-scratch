# Requirements

> Before you choose a single part, write down what "working" means, in numbers you can measure.

**Type:** Learn
**Prerequisites:** The whole course so far, especially Phase 03 (Resistance and Ohm's Law), Phase 04 (Kirchhoff's Laws), Lesson 05 (The Voltage Divider), Phase 17 (Microcontrollers), Phase 18 (Power Electronics), Lesson 06 (Batteries and Charging) and Phase 19 (Sensors and Signals), Lesson 02 (Temperature, Light and Force)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Capstone | A final project that uses everything learned before | The keystone at the top of an arch, holding it together |
| Requirement | A statement of what the product must do, written so it can be checked | A line in a contract |
| Specification (spec) | The measurable numbers that turn a requirement into a test | "The door must be at least 80 cm wide" instead of "a wide door" |
| Lux | The unit of illuminance: how much light falls on a surface | How brightly a page is lit |
| Photoresistor (LDR) | A resistor whose resistance falls as more light falls on it | A gate that opens wider in the sun |
| Threshold | The value at which a decision changes | The temperature at which a thermostat switches on |
| Hysteresis | Using a different threshold for switching on than for switching off, so the output does not chatter | A thermostat that heats at 19 °C but stops only at 21 °C |
| Duty cycle | The fraction of time a PWM signal is on (Phase 17, Lesson 03) | How much of each minute a lamp is switched on |
| Battery capacity (mAh) | How much charge a battery can deliver: milliamps times hours | The size of a fuel tank |
| Budget | A limit you must divide among the parts of the design | Monthly money split among rent, food and fun |
| Traceability | Being able to point from each requirement to the design choice and the test that covers it | A receipt for every expense |

## Learning Objectives

- Turn vague wishes ("it should come on when it's dark") into measurable requirements with numbers and units.
- Use the photoresistor model and a voltage divider to translate light levels into voltages and ADC codes.
- Choose on and off thresholds with hysteresis and check that they are far apart in ADC codes.
- Write a first energy budget from battery capacity and estimate how many nights the device will last.
- Explain why requirements come before parts, and how each one will be tested later in this phase.

## The Problem

This phase builds one complete device from start to finish: a **battery-powered night light**. It sits in a hallway or a child's room. When the room gets dark, it lights a soft white LED; when daylight returns, it switches off. It runs on three AA batteries for at least a month.

Phase 17, Lesson 07 already built a tiny night light on a virtual microcontroller. Now we do it the way a real product is done. We will write requirements (this lesson), choose an architecture and a power budget (Lesson 02), draw and check the full schematic (Lesson 03), simulate it in time, including the firmware's decisions over a whole night (Lesson 04), lay out the board (Lesson 05), plan its bring-up and diagnose faults (Lesson 06), and finally look back and ahead (Lesson 07).

The most common reason hobby projects disappoint is not a wrong resistor. It is never having decided what "working" means. "Comes on when it's dark": how dark? Does it flicker at dusk? What if a car's headlights sweep across the window at 2 am? How long do the batteries last, and does the light get dimmer as they run down? Each of these questions needs an answer with a number, before any part is chosen.

## The Physics

### Light and the photoresistor

Illuminance is measured in **lux**: the amount of visible light falling on a square metre. Some reference points: direct summer sun about 50,000-100,000 lux, an office about 300-500 lux, a living room in the evening about 50-150 lux, dusk about 10-20 lux, a dark room lit by a distant street light a few lux, full moonlight about 0.1-0.3 lux. The range covers six orders of magnitude, so we think about light on a logarithmic scale (Phase 00, Lesson 04).

A **photoresistor** (LDR, light-dependent resistor) is a film of cadmium sulphide whose free charge carriers increase with light: photons with enough energy knock electrons into the conduction band (Phase 01, Lesson 05). More carriers, lower resistance. A typical LDR follows a power law; the model we used in Phase 17, Lesson 07 (and keep here) is

```
R_LDR = 10 kΩ * (lux / 10) ^ (-0.7)
```

"10 kilohms at 10 lux, and the resistance falls as the light rises, by a factor of 10^0.7 = 5 for every factor of 10 in light". At 5 lux: `10k * 0.5^(-0.7) = 10k * 1.625 = 16.25 kΩ`. At 15 lux: `10k * 1.5^(-0.7) = 10k * 0.753 = 7.53 kΩ`. In bright sun, tens of ohms; in moonlight, over 150 kΩ. Real LDRs vary by a factor of two or more between samples, so a product would calibrate or leave margin.

(Cadmium sulphide LDRs are restricted under RoHS in many markets; a phototransistor or an ambient light sensor chip is the modern choice. The LDR is still the clearest teaching part, and the design method is the same.)

### Light to voltage: the divider

A microcontroller cannot measure resistance directly; its ADC measures voltage (Phase 17, Lesson 04). So the LDR goes in a voltage divider with a fixed resistor (Phase 04, Lesson 05):

```
   3.3 V ---[ LDR ]---+--- sense ---> ADC
                      |
                  [ R_FIX ]
                      |
                     GND

   V(sense) = 3.3 V * R_FIX / (R_LDR + R_FIX)
```

More light means a smaller `R_LDR` and a higher `V(sense)`. The ADC turns `V(sense)` into a code from 0 to 1023 (10 bits):

```
code = round(V(sense) / 3.3 V * 1023)
```

### Charge and battery life

A battery's capacity in milliamp-hours tells how much charge it can deliver: 2,000 mAh means 2,000 mA for 1 hour, or 2 mA for 1,000 hours (Phase 18, Lesson 06). An AA alkaline cell delivers about 2,000-2,500 mAh at small currents (less at high currents), its voltage falling from about 1.5 V when fresh towards 1.0-1.2 V when nearly empty. Three in series: about 4.5 V fresh, about 3.6 V at our chosen end point.

## The Concept

### From wishes to requirements

A good requirement is **measurable**: a test can say yes or no. Here are ours, each with the spec we will test against:

| # | The user wants | Spec |
|---|---|---|
| R1 | it turns on when the room gets dark | on below 5 lux, off above 15 lux |
| R2 | it never flickers at dusk or when headlights pass | hysteresis (3x in lux); decisions on a 4-second average |
| R3 | a soft, even light | white LED at about 30% of 19 mA; PWM above 200 Hz (no visible flicker) |
| R4 | it runs a month on one set of batteries | 3 x AA (2,000 mAh), at least 30 nights of 10 hours |
| R5 | it stays as bright as the batteries run down | LED average current within 20% from 4.5 V down to 3.6 V |
| R6 | it is safe and cheap | below 5 V everywhere; parts under \$3; board under 40 x 30 mm |

Notice what is *not* here: no part numbers. "Use an ATtiny" is a design decision, not a requirement. Requirements describe the *what*; the next lessons choose the *how*.

### R1 and R2: thresholds with hysteresis

Why two thresholds? Imagine a single threshold at 10 lux. At dusk the light falls slowly through 10 lux, with small fluctuations (clouds, a tree moving in the wind). Each wobble across the line would switch the light on and off: flicker. With **hysteresis** the light turns on below 5 lux and off only above 15 lux. Once on, a small wobble cannot switch it off; once off, it cannot switch it on. This is the same idea as the Schmitt trigger (Phase 13, Lesson 02).

Translate the thresholds into what the microcontroller will actually see, with `R_FIX = 10 kΩ`:

```
5 lux:   R_LDR = 16.25 kΩ   V = 3.3 * 10 / (16.25 + 10) = 1.257 V   code = 1.257 / 3.3 * 1023 = 390
15 lux:  R_LDR =  7.53 kΩ   V = 3.3 * 10 / ( 7.53 + 10) = 1.883 V   code = 1.883 / 3.3 * 1023 = 584
```

The two thresholds are 194 codes apart: far more than the few codes of ADC noise (Phase 19, Lesson 06). The light turns on when the averaged code drops below 390 and off when it rises above 584.

Why `R_FIX = 10 kΩ`? A divider is most sensitive, in volts per percent change of `R_LDR`, when the two resistors are equal; that puts the decision region in the middle of the ADC's range. Our decision region is around 10 lux, where `R_LDR = 10 kΩ`, so `R_FIX = 10 kΩ`. That is the lab of this lesson.

Car headlights are the other half of R2: a short flash of perhaps 50 lux for a second or two. Averaging the readings over 4 seconds (Phase 19, Lesson 07) makes such flashes too short to cross the off threshold. We will test this in Lesson 04.

### R4: the first energy budget

Before any circuit exists, a rough budget tells us if the goal is even possible. At night the LED draws on average `0.3 * 19 mA = 5.7 mA` (30% duty). During the day, the electronics sleep and draw, say, 10 µA (we will check that number in Lesson 02). Per day:

```
night:  5.7 mA * 10 h        = 57 mAh
day:    0.01 mA * 14 h       =  0.14 mAh
total                        ≈ 57.1 mAh per day
nights = 2000 mAh / 57.1 mAh ≈ 35
```

35 nights meets the 30-night target, with a little margin. The budget also tells us where to spend effort: the LED is 99.7% of the energy. Saving a microamp in the microcontroller is pointless; the LED's current and duty cycle decide the battery life. To last 30 nights we may spend at most `2000 / 30 = 66.7 mAh` per day.

### R5: why brightness would fade

As the batteries fall from 4.5 V to 3.6 V, a simple resistor-limited LED loses most of its current, because the LED keeps about 3.1 V and the resistor sees the remainder: from about 1.3 V down to about 0.4 V. That would make the light three times dimmer by the end of the month. R5 asks the firmware to compensate: measure the battery voltage and raise the duty cycle as it falls (Lesson 04).

### Traceability

For every requirement we will have a design decision and a test:

| Req | Design decision (lesson) | Test (lesson) |
|---|---|---|
| R1 | LDR + 10 kΩ divider, thresholds at codes 390 / 584 (01, 03) | DC sweep of light levels (03); night simulation (04) |
| R2 | hysteresis + 4 s moving average in firmware (04) | headlight test in the night simulation (04) |
| R3 | NPN low-side driver, 68 Ω, 1 kHz PWM at 30% (03, 04) | transient PWM simulation (04) |
| R4 | sleep between samples, LDO with tiny quiescent current (02) | power budget (02); measured currents at bring-up (06) |
| R5 | battery measurement and duty compensation (04) | simulation at 4.5, 4.0 and 3.6 V (04) |
| R6 | 3 x AA, parts list and board (02, 05) | BOM cost and board size check (05) |

## Build It

Run:

```
uv run python phases/22-capstone/01-requirements/code/main.py
```

### Step 1: The requirements as data

```python
REQUIREMENTS = [
    ("R1", "turns the light on when the room gets dark", f"on below {LUX_ON:.0f} lux, off above {LUX_OFF:.0f} lux"),
    ...
]
```

Keeping requirements in a list makes it easy to print them with the results of each later lesson, which is what Lesson 07 does.

### Step 2: Light levels

```python
def ldr_ohms(lux):
    return 10_000 * (lux / 10) ** -0.7
```

The script prints the LDR resistance for six familiar light levels, from 30 Ω in summer sun to 155 kΩ in moonlight.

### Step 3: The divider at the thresholds

```python
def divider(lux, r_fixed=R_FIXED):
    c = Circuit()
    c.voltage_source("VDD", "vdd", "0", VDD)
    c.resistor("LDR", "vdd", "sense", ldr_ohms(lux))
    c.resistor("R_FIX", "sense", "0", r_fixed)
    return c.dc().v("sense")
```

The simulator confirms 1.257 V (code 390) at 5 lux and 1.883 V (code 584) at 15 lux.

### Step 4: The energy budget

The arithmetic of R4: 57.1 mAh per day and 35 nights.

### Step 5: The lab

The script tries each fixed resistor in the lab.

## Use It

- **Real products** start from a product requirements document (PRD) written with users and marketing, then an engineering specification with numbers, then a test plan. Medical, automotive and aerospace products must keep formal traceability from every requirement to its tests.
- **Ambient light sensor chips** (for example the TI OPT3001 or the Vishay VEML7700) measure lux directly over I2C (Phase 17, Lesson 06) with a calibrated response close to the human eye; phones use them to set screen brightness.
- **Commercial night lights** usually use a phototransistor and an analog comparator or a tiny microcontroller, and many run from the mains. A battery version must care about every microamp in standby, as ours will.
- **Energy budgets first.** Wearables, remote sensors and IoT devices are designed around their energy budget from day one; battery life is often their most important specification.

## Try It in the Lab

Open "Size the light sensor's divider". The LDR measures 10 kΩ at the decision point of about 10 lux. Choose the fixed resistor so that the ADC sees between 1.5 and 1.8 V there, without the divider drawing more than 0.2 mA. Compute `V(sense)` and the divider current for each candidate first. Which candidate fails both goals?

## Common Mistakes

- **Requirements without numbers.** "Low power" and "bright enough" cannot be tested. Write mA, lux, hours.
- **Requirements that are really designs.** "Use a 555 timer" is a solution; the requirement is what it must achieve.
- **A single threshold.** Without hysteresis, slow signals near the threshold make the output chatter.
- **Forgetting the end of battery life.** A design that works only with fresh batteries fails for most of its life. Check every requirement at the lowest battery voltage too.
- **Budgeting the wrong thing.** The LED uses 99.7% of the energy; optimise it before worrying about microamps elsewhere.

## Exercises

1. Using the LDR model, what is `R_LDR` at 1 lux and at 1,000 lux? What does the divider with `R_FIX = 10 kΩ` give at each, and which ADC codes?
2. Suppose you wanted the light to turn on below 2 lux instead of 5. What would the on-threshold ADC code be?
3. With a duty of 20% instead of 30%, how many nights would the batteries last? What duty gives exactly 30 nights?
4. An LDR sample is twice as resistive as our model at every light level. At what light level would our firmware (thresholds at codes 390 and 584) actually switch on? What does this say about calibration?
5. Harder: write one more requirement for a feature you would like (for example "turn off after 8 hours to save the batteries" or "a button to force the light on"). Give it a measurable spec, a design decision and a test, as in the traceability table.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Requirement | "what it should do" | A checkable statement of required behaviour |
| Specification | "the numbers" | Measurable limits (with units) that a test can pass or fail |
| Hysteresis | "a dead band" | Separate on and off thresholds that stop chattering near a threshold |
| Lux | "brightness" | Illuminance in lumens per square metre |
| Energy budget | "battery maths" | Charge per day by state (mA x h), compared with the battery capacity |
| Traceability | "why is this here?" | A link from each requirement to the design decision and the test that covers it |

## Further Reading

- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., section 10.7 (micropower digital design).
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., sections on photoresistors and microcontroller projects.
- Texas Instruments, *OPT3001 Ambient Light Sensor* datasheet — what a modern light sensor offers.
- Energizer, *Alkaline Handbook / AA (E91) product datasheet* — capacity versus discharge current for AA cells.
