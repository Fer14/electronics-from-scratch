# Debugging a Board

> A broken board is a puzzle with a known answer: the simulation tells you what every node should read, and the difference points at the fault.

**Type:** Build
**Prerequisites:** Phase 21 (PCB Design and Manufacturing), Lessons 01-06; Phase 02 (Your First Circuits), Lesson 07 (Measuring with a Multimeter); Phase 06 (Sources, Batteries and Measurement), Lesson 04 (Inside the Multimeter); Phase 11 (Semiconductors and Diodes), Lesson 08 (Zener Diodes)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Bring-up | The first careful power-on and testing of a new board | A pilot's first test flight of a new plane |
| Smoke test | Jokingly, the first power-on: does anything burn? | Turning the key of a car you just rebuilt |
| Current-limited supply | A lab supply set to give at most a chosen current, so a short cannot cause damage | A tap that can only open so far |
| Golden values | The voltages a correct board should show at each node, from simulation or a known-good board | The answer key at the back of the book |
| Fault | One specific thing wrong on the board: a short, an open, a wrong value, a reversed part | One wrong ingredient in a recipe |
| Solder bridge | Unwanted solder joining two pads that should be separate: a short | A puddle connecting two islands |
| Open | A connection that should exist but does not (cracked joint, broken trace, missing part) | A broken bridge |
| Symptom | What you observe, such as a wrong voltage or a dark LED | A fever |
| Fault dictionary | A table of the symptoms that each possible fault would cause | A doctor's chart of illnesses and their symptoms |
| Divide and conquer | Testing in the middle of a chain to find which half has the problem | Finding a dead bulb in a string by testing halfway |
| Probe | The tip you touch to a node to measure it | The tip of a thermometer |

## Learning Objectives

- Follow a safe bring-up order: inspect, check for shorts with power off, power up with a current limit, measure rails, then nodes.
- Use the simulator to produce the golden voltages of a board, and compare them with measurements.
- Explain what shorts, opens, wrong values and reversed parts do to node voltages, using Ohm's law and dividers.
- Build a fault dictionary by simulating each candidate fault, and diagnose a board by finding the closest match to its readings.
- Measure resistance to ground with power off and understand how a multimeter does it.

## The Problem

The assembled board arrives. You connect the battery and... the LED lights, but the sensor reading on the microcontroller is completely wrong. Or nothing lights. Or the regulator gets hot. Beginners at this point often start swapping parts at random or re-soldering everything, and sometimes make things worse.

Professionals do something calmer. Before the board arrived, they already knew what every node should read: the simulation told them. When the board disagrees, the *pattern* of the disagreement points at the fault. A node that reads 0 V when it should read 2.5 V is either shorted to ground or cut off from its supply; which one depends on what the neighbours read. This lesson turns that reasoning into a procedure and then into a small program.

## The Physics

Every fault on a board is, electrically, one of a few things, and each has a predictable effect:

- **A short** (solder bridge, tin whisker, wrong part rotation) is a near-zero resistance between two nodes that should be separate. The two nodes are forced to the same voltage. If one of them was ground, the other drops to 0 V, and a large current may flow from whatever drives it.
- **An open** (cracked joint, broken trace, part missing) is a near-infinite resistance where there should be a connection. No current flows through it. The node beyond it "floats" or is pulled to whatever else is connected to it. Across an open, you measure the full voltage difference (Phase 02, Lesson 03).
- **A wrong value** (a 1 kΩ from the wrong reel instead of 10 kΩ) changes ratios: a divider gives the wrong fraction, a current-setting resistor gives the wrong current.
- **A reversed polarised part** (diode, LED, electrolytic capacitor, transistor) behaves like a different component: a reversed LED does not conduct (an open, unless the reverse voltage exceeds its rating), a reversed zener conducts like an ordinary diode at about 0.7 V instead of regulating at 5.1 V.

Because each fault changes the circuit in a known way, we can **simulate** it. The circuit laws do not change on a broken board; only the component values do.

### Measuring resistance with the power off

A multimeter on its ohms range injects a small known current into the circuit and measures the voltage that appears (Phase 06, Lesson 04):

```
R = V / I
```

If it injects 0.1 mA and sees 1.0 V, the resistance is `1.0 / 0.0001 = 10,000 Ω`. This only works with the power off, because any other source in the circuit would add its own voltage. It is the safest first check on a new board: a power rail that measures 0 Ω to ground has a short, and powering it would make something hot.

## The Concept

### Our example board

```
   B1 9 V --- R1 220 Ω ---+--- rail (5.1 V) ---+------------------+
                          |                    |                  |
                       Z1 zener 5.1 V        R2 10 kΩ           R4 330 Ω
                       (cathode up)            |                  |
                          |                   mid  (2.55 V)     led_a
                          |                    |                  |
                          |                  R3 10 kΩ           D1 red LED
                          |                    |                  |
   GND -------------------+--------------------+------------------+
```

The zener and R1 form a simple shunt regulator (Phase 11, Lesson 08): R1 drops the extra `9 - 5.1 = 3.9 V` and the zener absorbs whatever current the loads do not take. The rail feeds an indicator LED through R4 and a divider R2/R3 whose middle a microcontroller reads.

Golden values by hand:

```
rail = 5.1 V                        (the zener holds it)
mid = 5.1 * 10k / (10k + 10k) = 2.55 V
LED current = (5.1 - 1.85) / 330 = 9.8 mA, so led_a ≈ 1.85 V
R1 current = (9 - 5.1) / 220 = 17.7 mA
zener current = 17.7 - 9.8 - 0.26 = 7.7 mA   (positive: it is regulating)
```

The simulator gives 5.111 V, 2.555 V and 1.849 V.

### The bring-up order

```
 1. look            orientation of polarised parts, bridges, missing parts, under a magnifier
 2. power off       resistance from each rail to ground: tens of ohms or less means a short
 3. power on        through a current-limited supply set a little above the expected current
 4. measure rails   every supply first, then every important node; compare with golden values
 5. functional      only now load firmware, plug in sensors, connect expensive things
```

Step 3 deserves a number. Our board should draw about 17.7 mA. Set the supply to 9 V with a 50 mA limit. If the supply hits its limit and its voltage collapses, there is a short: you lose nothing but a few seconds, instead of burning a trace.

### Reading the symptoms: think like Ohm

Suppose the board reads `rail = 5.09 V, mid = 0.46 V, led_a = 1.85 V`. The rail is fine and the LED is fine, so the problem is local to the divider. `mid` is low, but not zero. A dead short would give 0 V; an open R3 would give the full 5.1 V; a smaller R3 gives a smaller fraction. Solve the divider for R3:

```
mid = rail * R3 / (R2 + R3)
0.46 = 5.1 * R3 / (10k + R3)
0.46 * (10k + R3) = 5.1 * R3
4600 = 4.64 * R3
R3 = 991 Ω   -> about 1 kΩ: the wrong reel
```

Another board reads `rail = 5.14, mid = 2.56, led_a = 5.12`. The LED anode sits at the full rail voltage, so no current flows through R4 (no drop across it). The LED is not conducting: it is open or reversed. And the rail is slightly *higher* than normal, because the LED's 9.8 mA is no longer loading the regulator. Everything fits "LED soldered backwards".

A third reads `rail = 6.08, mid = 3.05, led_a = 1.86`. The rail is too high and the divider follows it (3.05 is half of 6.1). Something should be clamping the rail at 5.1 V and is not: the zener is missing or open. Without it, the rail is set by R1 and the loads alone.

### The fault dictionary

Reasoning like this is the core skill. But we can also let the simulator do the bookkeeping: list the faults we can imagine, simulate each, and record the node voltages. That is a **fault dictionary**:

```
  fault                                 rail     mid   led_a
  board is good                        5.111   2.555   1.849
  R3 shorted by a solder bridge        5.110   0.000   1.849
  R3 joint cracked (open)              5.111   5.111   1.849
  R3 loaded with 1 kOhm by mistake     5.110   0.465   1.849
  R2 loaded with 1 kOhm by mistake     5.110   4.645   1.849
  R1 joint cracked (open)              0.000   0.000   0.000
  Z1 missing                           6.105   3.052   1.863
  D1 (LED) soldered backwards          5.132   2.566   5.132
  R4 joint cracked (open)              5.132   2.566   0.716
```

To diagnose a board, compute how far its readings are from each row. A simple measure is the straight-line distance in "voltage space":

```
distance = sqrt( (rail_meas - rail_row)^2 + (mid_meas - mid_row)^2 + (led_meas - led_row)^2 )
```

The row with the smallest distance is the best suspect. For the first board above, the "1 kΩ" row is 0.020 V away and the next suspect (a short) is 0.46 V away: a clear answer.

Notice two rows that look alike: "LED backwards" and "R4 open" both stop the LED current and lift the rail to 5.132 V, but `led_a` differs (5.13 V versus 0.72 V). A floating node's voltage depends on what is still attached to it, so measuring the *right* node separates faults that look identical elsewhere. When two faults give the same readings everywhere you can measure, you need a different test (a resistance measurement with power off, or looking at the part).

### Limits of the method

- Measurements have error (a 3½-digit meter on its 20 V range resolves 10 mV) and parts have tolerance (Phase 03, Lesson 06). Never expect a perfect match; look for the clearly closest row.
- A dictionary only contains the faults you thought of. If no row is close, the fault is something new (two faults at once, a wrong part *type*, a design error). Then divide and conquer: measure along the signal path until the readings stop matching the simulation.
- Some faults are intermittent: a cracked joint that opens only when warm or when the board flexes. Gently pressing on parts or warming with a hairdryer while watching a reading can reveal them.

## Build It

Run:

```
uv run python phases/21-pcb-design-and-manufacturing/07-debugging-a-board/code/main.py
```

### Step 1: The board as a function of its part values

```python
def board(values, powered=True, ohmmeter_at=None):
    c = Circuit()
    if powered:
        c.voltage_source("B1", "vin", "0", 9.0)
    c.resistor("R1", "vin", "rail", values["R1"])
    if values["Z1"] == "normal":
        c.zener("Z1", "0", "rail", vz=5.1)
    c.resistor("R2", "rail", "mid", values["R2"])
    c.resistor("R3", "mid", "0", values["R3"])
    c.resistor("R4", "rail", "led_a", values["R4"])
    if values["D1"] == "normal":
        c.led("D1", "led_a", "0", color="red")
    else:
        c.led("D1", "0", "led_a", color="red")
    if ohmmeter_at:
        c.current_source("OHM", "0", ohmmeter_at, 1e-4)
    return c
```

One function builds both the good board and every faulty one: a fault is just a dictionary that overrides some values (`{"R3": 1e-3}` is a short, `{"R3": 1e12}` an open, `{"Z1": "missing"}` leaves the part out, `{"D1": "reversed"}` swaps its pins). The zener's anode is at ground and its cathode at the rail, as on the schematic.

### Step 2: Golden values

`voltages(GOOD)` runs the DC analysis and returns the three node voltages: 5.111, 2.555 and 1.849 V.

### Step 3: The ohmmeter

With `powered=False` and `ohmmeter_at="mid"`, the battery is removed and a 0.1 mA current source is connected from ground into `mid`, just like a meter on its ohms range. `R = V / I` gives 9999.9 Ω for the good board (R3 in parallel with a path through R2 that leads nowhere, because nothing conducts with the power off) and 0.0 Ω with a solder bridge across R3.

### Step 4: The fault dictionary

```python
dictionary = {name: voltages(with_fault(fault)) for name, fault in FAULTS.items()}
```

One line simulates all nine cases. The table printed is the one in The Concept.

### Step 5: Diagnosis

```python
def diagnose(measured, dictionary):
    scores = []
    for name, expected in dictionary.items():
        error = math.sqrt(sum((measured[n] - expected[n]) ** 2 for n in NODES))
        scores.append((error, name))
    return sorted(scores)
```

For the three example boards, the closest rows are "R3 loaded with 1 kOhm by mistake" (0.020 V), "D1 (LED) soldered backwards" (0.016 V) and "Z1 missing" (0.025 V), each far ahead of the second suspect.

### Step 6: The lab task

The script evaluates every part offered in the lab and prints the measured goals.

## Use It

- **Test points.** Add small exposed pads (labelled TP1, TP2...) on every rail and important node when you lay out the board (Lesson 01). Probing a test point is much easier than probing a 0402 pad.
- **Simulation as documentation.** Write the golden values on the schematic or in a bring-up checklist. Whoever debugs the board in a year will thank you.
- **Production test.** Factories do exactly what our script does, at scale: in-circuit testers with a bed of nails measure every node and component, and software compares the readings with expected values and tolerances to name the faulty part.
- **Thermal camera and finger test.** A short often makes something warm. A cheap thermal camera, or carefully touching parts with the power at a low current limit, finds the hot spot.
- **Debug firmware last.** If the hardware's DC voltages are wrong, no firmware fix will help. Get the golden values first.

## Try It in the Lab

Open "Repair the board". The prototype reads 0.46 V at `mid` instead of about 2.55 V. The bottom divider position (slot S1) might hold a solder bridge, a cracked joint, a resistor from the wrong reel or the right resistor. Before trying parts, predict what `mid` would read with each one and which matches the symptom. Then put in the part that meets the specification. Check that the rail stays regulated too.

## Common Mistakes

- **Powering a new board without a current limit.** A short then burns a trace or a part, and you have two faults instead of one.
- **Measuring resistance with the power on.** The reading is meaningless and can damage the meter.
- **Changing several things at once.** If you swap three parts and the board works, you do not know which fault it was, and the next board may have it too.
- **Trusting the schematic instead of the board.** Check that the part on the board is the part on the schematic: read its marking, measure it out of circuit if needed.
- **Forgetting that floating nodes read strange values.** A node cut off by an open is set by whatever is still attached (or by the meter itself). Do not read too much into its exact value; ask what it is connected to.

## Exercises

1. On the good board, what voltage would you measure across R1? Across R4? Which way does current flow in the zener?
2. A board reads `mid = 4.64 V` with a correct rail. Which fault from the dictionary fits? Confirm it by solving the divider for R2.
3. The rail reads 0.0 V and the supply is in current limit. Name two faults that could cause this. What resistance measurement with power off would tell them apart?
4. Add a new fault to `FAULTS`: "R1 loaded with 2.2 kOhm". Predict whether the zener still regulates (hint: compute the R1 current and compare it with what the loads need), then run the script.
5. Harder: add measurement noise to the readings (for example ±30 mV) and see how often `diagnose` still picks the right fault. Which pairs of faults are hardest to tell apart, and which extra node would you measure to separate them?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Bring-up | "first power-on" | A planned sequence: inspect, check shorts unpowered, power with a current limit, measure, then add function |
| Golden values | "what it should read" | The expected node voltages from simulation or a known-good board |
| Short | "a bridge" | An unwanted near-zero resistance forcing two nodes to the same voltage |
| Open | "a bad joint" | A missing connection; no current flows and the far node floats |
| Fault dictionary | "the symptom table" | Simulated node readings for each candidate fault, used to match measurements |
| Current limit | "CC mode" | A supply setting that caps the current, turning a short into a harmless voltage collapse |

## Further Reading

- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Appendix L (workbench instruments and tools) and Appendix O (the oscilloscope).
- Bob Pease, *Troubleshooting Analog Circuits* (Butterworth-Heinemann, 1991) — a classic, practical and funny book on finding faults.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., chapter on testing and troubleshooting.
- [MIT OpenCourseWare 6.002, Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) — the circuit analysis behind every golden value.
