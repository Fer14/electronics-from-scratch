# Bring-Up

> The first boards are guilty until proven innocent. A plan, golden values and a fault dictionary turn "it doesn't work" into "R5 is from the wrong reel".

**Type:** Build
**Prerequisites:** Phase 22 (Capstone), Lessons 01-05; Phase 21 (PCB Design and Manufacturing), Lesson 07 (Debugging a Board); Phase 02 (Your First Circuits), Lesson 07 (Measuring with a Multimeter); Phase 06 (Sources, Batteries and Measurement), Lessons 04 (Inside the Multimeter) and 07 (Lab Power Supplies)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Bring-up | The careful first power-on and testing of new boards | A test drive of a new car, starting in the car park |
| Test firmware | A special program that puts the board into known states for measurement (for example, a pin held high) | A mechanic's diagnostic mode |
| Test point | A small exposed pad where a probe can touch a net | A tap on a pipe where you can attach a pressure gauge |
| Golden values | What every test point should read on a good board, from simulation | The answer key |
| Supply current | The current the board draws from the battery or bench supply, shown on the supply's display | The electricity meter of a house |
| Current limit | A bench supply setting that caps the current, so a short cannot burn anything (Phase 06, Lesson 07) | A fuse that resets itself |
| Fault dictionary | The simulated readings for each likely assembly fault (Phase 21, Lesson 07) | A doctor's chart of symptoms |
| Wrong reel | A part with the right package but the wrong value, loaded by mistake | Salt in the sugar jar |
| Rotated part | A part soldered turned by 180° or mirrored, so its pins land on the wrong pads | A plug inserted upside down |
| First article | The first boards of a production run, checked in depth before the rest are built | The first slice of a new cake, tasted before serving |
| Yield (assembly) | The share of assembled boards that pass test | The share of cakes that come out right |

## Learning Objectives

- Write a step-by-step bring-up plan for the night light that cannot damage a faulty board.
- Use test firmware to put the board into a known state and compare its test points with simulated golden values.
- Check for shorts with the power off by measuring resistance to ground, and know what a good board should read.
- Simulate the readings of nine likely assembly faults and diagnose real readings by finding the closest match, including the supply current.
- Repair a fault and confirm the fix against the requirements.

## The Problem

The first batch of ten night-light boards comes back from assembly. Most work. Three do not:

- Board 1: the LED lights, but very dimly.
- Board 2: the LED never turns on, not even in a completely dark cupboard.
- Board 3: the LED stays dark; the microcontroller seems fine.

In Phase 21, Lesson 07 we learned the general method on a small example board. Now we apply it to our own device, with everything we know about it: its schematic (Lesson 03), its expected behaviour (Lesson 04) and its layout (Lesson 05). The goal is to name the faulty part on each board in a few minutes, from a few measurements, without guessing or unsoldering parts at random.

## The Physics

Nothing new happens physically on a faulty board: Ohm's law, the LED's curve and the transistor's behaviour are the same. What changes is a component's value or connection. That is why a simulation can predict the symptoms of each fault exactly. Three kinds of measurements give complementary information:

- **Resistance with the power off** reveals shorts and opens without risk. An ohmmeter pushes a small known current and measures the voltage (Phase 06, Lesson 04).
- **Node voltages with the power on**, in a known state, reveal wrong values and misplaced parts.
- **The supply current**, read from the bench supply's display, sums up everything the board draws: a dead short shows as the current limit being reached; a missing load as an unusually small current.

A 1 kHz PWM signal would make the voltages on the LED side jump up and down, and a multimeter would show some average. So for measurement we use **test firmware** that holds the PWM pin (PB1) steadily high and powers the LDR divider (PB2) continuously. Every node then sits at a steady DC value that the simulator can predict.

## The Concept

### The plan

```
1. inspect      LED and transistor orientation (the LED's flat side is the cathode),
                solder bridges between the SOIC pins, missing parts
2. power off    resistance VBAT-GND and VDD-GND: no short
3. power on     bench supply at 4.5 V, current limit 50 mA (the board needs about 20 mA at most)
4. test FW      load the test firmware: PB1 high, PB2 high
5. measure      every test point, plus the supply current; compare with golden values
6. diagnose     find the closest fault in the dictionary; repair; re-measure
7. real FW      load the night-light firmware; cover and uncover the LDR; check sleep current
```

Each step protects the next. Step 2 finds a short before power can make it hot. The current limit in step 3 makes any short we missed harmless. Only when the hardware is proven do we load the real firmware, so we never confuse a hardware fault with a software bug.

### Power-off resistances on a good board

```
VBAT to GND:   940 kΩ    (the battery divider R2 + R3; the LED branch does not conduct
                          with a tiny ohmmeter current, and the LDO input is high impedance)
LIGHT to GND:  10.0 kΩ   (R1)
LED_K to GND:  thousands of MΩ (the transistor is off)
```

If LED_K reads 0 Ω to ground, there is a solder bridge across the transistor: the LED would light permanently, day and night.

### Golden values in the test state

With PB1 and PB2 high, a 4.5 V supply and the LDR at about 10 lux (10 kΩ; on the bench, a known lamp at a fixed distance, or a 10 kΩ resistor clipped in its place):

| Test point | Golden value |
|---|---|
| VBAT | 4.500 V |
| VDD | 3.300 V |
| LIGHT | 1.650 V |
| BAT_SENSE | 2.250 V |
| BASE | 0.733 V |
| LED_A | 3.213 V |
| LED_K | 0.080 V |
| supply current | 20.27 mA (LED 18.93 mA + base 1.17 mA + LDR divider 0.17 mA) |

### The fault dictionary

Nine cases, simulated:

| Fault | LIGHT | BAT_SENSE | BASE | LED_A | LED_K | Supply |
|---|---|---|---|---|---|---|
| board is good | 1.650 | 2.250 | 0.733 | 3.213 | 0.080 | 20.27 mA |
| R5 is 330 Ω (wrong reel) | 1.650 | 2.250 | 0.703 | 3.101 | 0.045 | 5.59 mA |
| R4 is 22 kΩ (wrong reel) | 1.650 | 2.250 | 0.718 | 3.702 | 0.594 | 12.02 mA |
| D1 soldered backwards | 1.650 | 2.250 | 0.677 | 4.500 | 0.018 | 1.36 mA |
| Q1 rotated (C and E swapped) | 1.650 | 2.250 | 0.660 | 4.418 | 1.428 | 2.57 mA |
| R1 not soldered (open) | 3.300 | 2.250 | 0.733 | 3.213 | 0.080 | 20.10 mA |
| LDR leg cracked (open) | 0.000 | 2.250 | 0.733 | 3.213 | 0.080 | 20.10 mA |
| R3 not soldered (open) | 1.650 | 4.500 | 0.733 | 3.213 | 0.080 | 20.26 mA |
| solder bridge LED_K to GND | 1.650 | 2.250 | 0.659 | 3.136 | 0.000 | 21.43 mA |

Some faults are almost invisible in the voltages but obvious in the current (R5 from the wrong reel: the voltages move by tens of millivolts, the current falls by three quarters). Others are invisible in the current but obvious in one voltage (R1 open: LIGHT jumps to 3.3 V). That is why we measure both.

Think about what each fault *does* to the product, using Lesson 04's firmware:

- **R1 open**: LIGHT reads 3.3 V, code 1023, "bright daylight" forever: **the light never turns on** at night.
- **LDR open**: LIGHT reads 0 V, code 0, "pitch dark" forever: the light stays on day and night and the batteries die in a week.
- **R3 open**: BAT_SENSE reads the full 4.5 V, code 1023 after the factor 2 means "9 V battery": the compensation thinks the battery is very strong, uses a small duty, and the light is too dim, increasingly so as the battery runs down.
- **R4 from the wrong reel**: the transistor is not saturated (LED_K at 0.59 V), the LED gets 11.7 mA instead of 18.9 mA, and the transistor wastes power.

### Diagnosing the three boards

To compare a board's readings with each row, compute a distance that combines the five voltages and the supply current (weighting 1 mA like 0.1 V, so that both kinds of measurement count):

```
distance = sqrt( sum over nodes of (V_measured - V_row)^2  +  (0.1 * (I_measured - I_row))^2 )
```

| Board | Readings | Closest row | Distance | Next |
|---|---|---|---|---|
| 1, LED very dim | LED_A 3.10, LED_K 0.05, supply 5.6 mA | R5 is 330 Ω | 0.008 | R4 wrong (1.035) |
| 2, never turns on | LIGHT 3.29, supply 20.1 mA | R1 open | 0.012 | board is good (1.640) |
| 3, LED dark | LED_A 4.49, supply 1.4 mA | D1 backwards | 0.011 | Q1 rotated (1.415) |

Each board's fault is clear, with the second suspect far behind. Board 2 is the instructive one: its LED circuit is perfect; the light never turns on because of a missing 10 kΩ resistor in the *sensor*. Without a test point on LIGHT, we would have been tempted to blame the LED or the firmware.

## Build It

Run:

```
uv run python phases/22-capstone/06-bring-up/code/main.py
```

### Step 1: The plan

Printed as a numbered list, the same steps as above.

### Step 2: One board function for every case

```python
def board(values, vbat=4.5, pwm_high=True, powered=True, ohmmeter=None):
    c = Circuit()
    if powered:
        c.voltage_source("BAT", "vbat", "0", vbat)
        c.voltage_source("U1", "vdd", "0", VDD)
        c.voltage_source("PB2", "ldr_pwr", "0", VDD)
        c.voltage_source("PB1", "pwm", "0", VDD if pwm_high else 0.0)
    ...
    if values["Q1"] == "normal":
        c.npn("Q1", c="led_k", b="base", e="0", beta=100)
    else:
        c.npn("Q1", c="0", b="base", e="led_k", beta=100)
    ...
    if values.get("bridge"):
        c.resistor("BRIDGE", "led_k", "0", 1e-3)
    if ohmmeter:
        c.current_source("OHM", "0", ohmmeter, 1e-5)
    return c
```

A fault is a dictionary that overrides values: a wrong reel is a different resistance, an open is 10^12 Ω, a backwards LED swaps its pins, a rotated transistor swaps collector and emitter (it then works poorly in "inverse" mode), a solder bridge adds a 1 mΩ resistor. With `powered=False` and an `ohmmeter` node, all sources are removed and a 10 µA current source measures resistance to ground.

### Step 3: Golden values and power-off resistances

`measure(GOOD)` gives the table of golden values; `resistance_to_ground` gives 939.9 kΩ, 10.0 kΩ and thousands of MΩ (0.001 Ω with a bridge).

### Step 4: The fault dictionary

```python
dictionary = {name: measure(dict(GOOD, **fault)) for name, fault in FAULTS.items()}
```

`measure` records the five test-point voltages and the supply current (battery plus the microcontroller pins' currents).

### Step 5: Diagnosis

```python
def diagnose(measured, dictionary):
    keys = ("light", "bat_sense", "base", "led_a", "led_k")
    ranked = []
    for name, expected in dictionary.items():
        volts = sum((measured[k] - expected[k]) ** 2 for k in keys)
        amps = (0.1 * (measured["i_supply_ma"] - expected["i_supply_ma"])) ** 2
        ranked.append((math.sqrt(volts + amps), name))
    return sorted(ranked)
```

The two best suspects for each board are printed.

### Step 6: The lab

The script evaluates the three resistors of the lab.

## Use It

- **First-article inspection**: the first boards of every production run are checked in depth (X-ray of hidden joints, every test point, every current) before the rest are built.
- **Production test**: once the design is proven, each board gets a quick automatic test (a few seconds on a bed-of-nails fixture that measures the test points and compares them with limits), exactly our fault dictionary, automated.
- **Test firmware** ships with many products in a hidden factory mode; it is also what repair technicians use.
- **Assembly faults** in real life are mostly the ones in our dictionary: wrong reels, rotated parts, bridges between fine-pitch pins, and missing or cracked joints, plus occasional damaged parts.
- **Keep records**: note every fault found and its cause (a reel loaded in the wrong feeder, a footprint error). Fix the process, not just the board.

## Try It in the Lab

Open "Fix the dim night light". Board 1's LED gets only about 4.2 mA with the PWM pin held high, and its transistor is saturated, so the suspect is the LED's series resistor (slot S1). Three resistors are offered. For each, estimate the LED current with `(4.5 - 3.1 - 0.1) / R`, and its power with `I^2 R`. Which one brings the LED back to 15-20 mA within 0.1 W, and which one would overdrive it?

## Common Mistakes

- **Measuring the PWM node with a multimeter.** It shows a meaningless average. Use test firmware to hold signals steady, or an oscilloscope.
- **Skipping the power-off checks.** A solder bridge across the battery is found in seconds with an ohmmeter, and costs a burnt trace if found with power.
- **Debugging firmware on unproven hardware.** If LIGHT reads 3.3 V because R1 is missing, no change to the thresholds will help.
- **Trusting one kind of measurement.** Voltages hide some faults and currents hide others; take both.
- **Repairing without understanding.** Swapping R5 fixes board 1, but if the reel was loaded in the wrong feeder, the next hundred boards have the same fault.

## Exercises

1. On a good board in the test state, what voltage should you read across R5? Across R4? Compute them from the golden values.
2. Predict the readings (LIGHT, BAT_SENSE, LED_A, LED_K, supply current) of a board where R2 is not soldered. Add the fault to `FAULTS` and check.
3. A board reads LED_K = 0.000 V and a supply current of 21.4 mA, and its LED never turns off, even with PB1 low. Which fault is it, and which power-off measurement would have found it first?
4. Run `measure` for the good board with the supply at 3.6 V. Which golden values change, and by how much? Why does a bring-up plan specify the supply voltage?
5. Harder: two faults at once (R5 from the wrong reel *and* R1 open). Add a combined fault to the dictionary. Does `diagnose` still find it if the combination is in the dictionary? What if it is not, which single fault does it pick, and how would you notice that the answer is incomplete?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Bring-up | "first power-on" | A safe, ordered sequence of checks from inspection to full function |
| Test firmware | "factory mode" | Firmware that holds the board in known states for measurement |
| Golden values | "expected readings" | Simulated (or known-good) readings at every test point in a test state |
| Fault dictionary | "symptom table" | Simulated readings for each candidate fault, matched against measurements |
| Wrong reel | "wrong value" | A correct-looking part with the wrong value, loaded by mistake |
| First article | "the first boards" | The first units of a run, inspected in depth before production continues |

## Further Reading

- Phase 21, Lesson 07 of this course (Debugging a Board) — the method on a smaller example.
- Bob Pease, *Troubleshooting Analog Circuits* (Butterworth-Heinemann, 1991).
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Appendix L (workbench instruments and tools) and Appendix O (the oscilloscope).
- IPC-A-610, *Acceptability of Electronic Assemblies* ([ipc.org](https://www.ipc.org/)) — what assembly defects look like and which are acceptable.
