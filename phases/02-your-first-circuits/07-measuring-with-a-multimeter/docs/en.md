# Measuring with a Multimeter

> Voltage is measured across, current is measured through, resistance is measured with the power off. Remember those three and your meter will live a long life.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 00 (Words and Units), Lessons 03 (Units and SI Prefixes) and 06 (Safety First); Phase 02 (Your First Circuits), Lessons 01-06
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| multimeter | one handheld instrument that can measure voltage, current, resistance and more, chosen with a dial | a kitchen scale that can also be a thermometer and a timer |
| voltmeter | a meter (or a multimeter setting) that measures voltage between two points | a spirit level that compares the height of two spots |
| ammeter | a meter (or setting) that measures current through a point | a turnstile counter that counts people walking through it |
| ohmmeter | a meter (or setting) that measures resistance | squeezing a sponge to feel how stiff it is |
| probe / test lead | the insulated wire with a pointed metal tip that you touch to the circuit | the two hands of a doctor taking a pulse |
| COM jack | the "common" socket on the meter; the black lead always goes here | the zero mark on a ruler |
| in parallel (across) | connected to the same two points as a part, side by side with it | standing on both banks of a river to measure its width |
| in series (through, in line) | connected so that the current has to pass through the meter on its way round the loop | a toll booth on a single-lane road |
| range | the largest value the meter can show in a given setting | the top of a scale: a kitchen scale that goes up to 5 kg |
| resolution | the smallest step the display can show in a given range | the finest marks on a ruler |
| OL | "overload": the value is too big for the selected range | the needle of a scale hitting its stop |
| continuity | whether there is an unbroken, low-resistance path between two points | checking a garden hose by blowing through it |
| fuse | a thin wire inside the meter that melts and opens the circuit if too much current flows | a deliberately weak link in a chain |

## Learning Objectives

- Set up a multimeter for voltage, current, resistance and continuity: dial position, jacks, and where the two probes touch the circuit.
- Explain why voltage is measured in parallel and current in series, using the idea that a good meter must disturb the circuit as little as possible.
- Read a digital display correctly: range, resolution, sign, OL, and a typical accuracy specification like "±(0.5 % + 2 counts)".
- Predict what goes wrong with the two classic hookup mistakes (voltmeter in series, ammeter across a source) and compute the numbers yourself.

## The Problem

Everything in this course so far has been a prediction: "the current should be 20 mA", "the voltage across this bulb should be 6 V". In real life a circuit that does not work gives you no error message. The LED just stays dark. To find out *why*, you need to look inside the circuit, and the eyes of an electronics engineer are measuring instruments. The first and most important is the multimeter.

A basic digital multimeter costs less than a pizza and can measure voltage, current and resistance. Used right, it answers almost every beginner's question: Is the battery flat? Is this wire broken? Is the current what I calculated? Used wrong, it gives nonsense readings, changes the very circuit you are trying to measure, or, in the most famous beginner accident of all, blows its own internal fuse with a little pop the first time you try to "measure the current of a battery".

This lesson is the practical "how to hold it" version. What is inside the meter and how its own resistance subtly changes your circuits is Phase 06, Lessons 04 and 05.

## The Physics

### A tiny bit of history

The first current detectors appeared within months of Hans Christian Ørsted's 1820 discovery that a current deflects a compass needle. Johann Schweigger wrapped many turns of wire around a compass and made the "multiplier", the ancestor of the **galvanometer** (named after Luigi Galvani). In 1882 Jacques-Arsène d'Arsonval built the moving-coil meter: a small coil hanging in the field of a magnet, twisting against a spring by an amount proportional to the current. For a hundred years every voltmeter, ammeter and ohmmeter was a moving needle on a scale. In 1923 the British engineer Donald Macadie, tired of carrying separate meters to test telephone lines, combined them into one box with a selector: the AVOmeter (Amps, Volts, Ohms), the first multimeter. Digital multimeters, with numbers instead of a needle, became common in the 1970s.

A needle meter responds to the **current** passing through its coil, and every other setting is a clever way of turning the quantity you want into such a current. A digital meter works the other way round: at heart it measures a small **voltage**, and turns currents and resistances into voltages first. How both do it is Phase 06, Lesson 04. For using one, the rules below are all you need.

### What each measurement physically means

**Voltage** is a *difference* in electric potential between two points (Phase 01, Lesson 04): how much energy each coulomb gains or loses going from one point to the other. You cannot measure the voltage "of" a single point any more than you can measure the height of a single shelf without saying "above what". So a voltmeter always has two probes, and it reports the potential of the red probe minus the potential of the black probe.

**Current** is how much charge passes a point each second (Phase 01, Lesson 06). To count charge, it has to go *through* the meter. So the meter must become part of the loop: you open the loop and let the meter close it again.

**Resistance** is how much a part opposes current (we meet it properly in Phase 03, Lesson 01). A meter cannot see resistance directly. Instead, it pushes a small, known current through the part from its own battery and measures the voltage that appears across it. A part that needs a big voltage to pass the small current has a big resistance. (This uses V = I x R, the preview of Ohm's law we have been borrowing; you will earn it in Phase 03.)

### The golden rule: don't change what you measure

A meter that changes the circuit gives you the wrong answer. That one idea explains how every setting must be connected.

- **A voltmeter is placed across a part, side by side with it.** If it drew a lot of current it would steal current from the part and change its voltage. So a good voltmeter has a *huge* resistance between its probes: a typical digital meter has 10 MΩ (10 million ohms). Almost no current goes into it. In the water picture of Lesson 05, it is a pressure gauge tapped into the side of the pipe: it feels the pressure but lets no water through.
- **An ammeter is placed in the path of the current.** If it resisted the current, it would reduce it. So a good ammeter has a *tiny* resistance: around 1 Ω on a milliamp range and 0.01 Ω on a 10 A range. It is nearly a piece of wire. In the water picture, it is a flow meter fitted in-line in the pipe: all the water goes through it, and it barely slows the water down.

Read those two bullets again, because they explain both classic mistakes:

- A voltmeter *in series* is a 10 MΩ resistor dropped into the loop. It blocks almost all the current. The circuit stops working, and the meter shows nearly the full battery voltage (it is now the biggest resistance in the loop, so it gets almost all the push).
- An ammeter *across* a battery is a 1 Ω wire connected straight from + to -. That is a short circuit (Lesson 03). A huge current flows, and the meter's fuse melts to save it.

## The Concept

### Anatomy of a digital multimeter

```
   +---------------------------+
   |        [  6.00  ]  V DC   |   <- display
   |                           |
   |      OFF        V=        |   <- the dial (rotary switch):
   |   V~               mA=    |      V= DC volts, V~ AC volts,
   |   A~                A=    |      mA= and A= DC current,
   |      beep      ohm        |      ohm resistance, beep continuity
   |                           |
   |  (10A)  (mA)  (COM)  (VΩ) |   <- jacks (sockets)
   +---------------------------+
        |      |      |      |
        |      |    black   red (for V, ohm, beep)
        |      |
        |    red, for currents up to about 200 mA (fused)
        |
      red, for currents up to 10 A (fused, a stronger fuse)
```

- **The black lead always goes in COM.** "Common" is the meter's reference point.
- **The red lead moves** depending on what you measure: VΩ for voltage, resistance and continuity, mA for small currents, 10A for big ones. Many accidents come from leaving the red lead in the mA or 10A jack after measuring a current and then touching it across a battery to measure "volts".
- **The dial** chooses the quantity and, on manual meters, the range. A straight line (or "DC", or ⎓) means direct current, what batteries give. A wavy line (~) means alternating current, what wall sockets give (Phase 09). In this course you almost always want the DC settings.

### Measuring voltage: across

Take the circuit from the code: a 9 V battery with R1 = 1000 Ω and R2 = 2000 Ω in one loop.

```
          +-----[ R1 1000 ohm ]-----+
          |                         |
        + |                         | node X
        9 V                         |
        - |                         |
          |                      [ R2 2000 ohm ]
          |                         |
          +-------------------------+   node 0 V (ground)

   voltmeter on R2:   red probe on node X, black probe on ground
```

The loop current is 9 V / (1000 + 2000) Ω = 0.003 A = 3 mA, and the voltage across R2 is 3 mA x 2000 Ω = 6 V. Across R1 it is 3 mA x 1000 Ω = 3 V. Notice 3 + 6 = 9: the battery's push is shared between the two resistors (Phase 04 will make this a law).

Steps:

1. Black lead in COM, red lead in VΩ.
2. Dial to DC volts, a range bigger than you expect (20 V for a 9 V circuit).
3. Leave the circuit running. Touch the red probe to one end of R2 and the black probe to the other end. You do not unplug anything.
4. Read 6.00 V.

How much does the meter's 10 MΩ disturb things? It sits beside R2, giving the current a second path. The two together behave like a resistance of 2000 x 10 000 000 / (2000 + 10 000 000) = 1999.6 Ω instead of 2000 Ω (this "product over sum" rule for two side-by-side resistors is Phase 04, Lesson 04). The voltage becomes 5.9996 V instead of 6 V, an error of 0.007 %. The display cannot even show it. That is what a good voltmeter looks like.

If you swap the probes, the meter shows **-6.00 V**. Nothing is wrong: it reports red minus black, and now red is on the lower side. A minus sign simply tells you that you have the probes the other way round from the direction of the push, which is actually useful information.

### Measuring current: through

To measure current you must **break the loop** and let the meter close it again:

```
   before:   battery + -----[ R1 ]----- ...

   after:    battery + ----(red  METER  black)----[ R1 ]---- ...
                        meter on mA, red lead in the mA jack
```

Steps:

1. Turn the circuit off (disconnect the battery).
2. Black lead in COM, red lead in **mA** (or 10A if you expect more than about 200 mA, or if you have no idea, start with 10A).
3. Dial to DC mA (or A).
4. Open the loop at one point: pull one end of a wire or a part out of its breadboard hole.
5. Put the red probe on the side towards the battery's plus terminal and the black probe on the other side, so the current enters through red and leaves through black (conventional current, + to - outside the battery; the meter would just show a minus sign otherwise).
6. Reconnect the battery and read: 3.00 mA.

With 1 Ω inside the meter, the loop has 3001 Ω instead of 3000 Ω, so the current is 9 / 3001 = 2.999 mA instead of 3 mA: an error of 0.03 %. Again, too small to see.

Because every bit of current in a single loop is the same (Lesson 01: every charge returns), it does not matter *where* in the loop you break it. Between the battery and R1, between R1 and R2, or between R2 and the battery: all three places read 3 mA.

### The blown-fuse story

Almost everyone does this once. You have just measured a current, the red lead is still in the mA jack, and you want to check the battery. You touch the probes to its terminals.

```
         +----(red  METER on mA, 1 ohm  black)----+
         |                                        |
      battery +                              battery -
```

The meter is now a 1 Ω path straight across the battery. A real 9 V battery has a little resistance of its own inside, about 1-2 Ω when fresh (Phase 06, Lesson 02). The current is limited only by those two:

```
current = 9 V / (1.5 ohm + 1 ohm) = 3.6 A
```

That is 18 times the 0.2 A fuse rating. The fuse melts in a fraction of a second, with or without a little pop, and from then on the mA setting reads 0.00 whatever you do. The meter did its job: the fuse died so that the meter's circuit board did not. Replace it with exactly the same type (the rating is printed on the fuse and in the manual).

With a car battery (12 V, with an internal resistance of only a few thousandths of an ohm) the same mistake can make hundreds of amperes flow. That is why the 10A jack has a special high-energy fuse, and why the rule is: **never put the probes across a source with the red lead in a current jack**.

### Measuring resistance: power off, part out

Steps:

1. Turn the circuit off. Ideally, take the part out of the circuit (or lift one leg out of the breadboard).
2. Black lead in COM, red in VΩ, dial to Ω.
3. Touch the probes to the two legs. Polarity does not matter for a resistor.
4. Read.

Why power off? The ohmmeter works by pushing its own small test current (in our model 0.1 mA) and reading the voltage. If the circuit's battery is also pushing, the meter reads that voltage too and divides by its own test current. Our program measures R2 with the battery still connected and gets about 60 700 Ω for a 2000 Ω resistor: complete nonsense. (Real meters may show nonsense of a different kind, or a negative value, or warn you; the point is that the reading is meaningless.)

Why out of the circuit? Because other parts connected to the same two points give the test current other paths, and the meter measures all of them together. With R1 and R2 side by side, for example, you would read their combination, not R2.

Do not hold both metal tips with your fingers while measuring big resistances: your body (around 100 kΩ to 1 MΩ with dry hands) becomes a parallel path and the reading drops.

### Continuity: the beep

Continuity mode is a resistance measurement with a buzzer: the meter beeps if the resistance between the probes is below a threshold, typically a few tens of ohms. It is the fastest tool for finding broken wires and checking which breadboard holes are connected (Lesson 06). Power off, probes on the two points, listen. A jumper wire beeps; a 1 kΩ resistor does not; a broken wire does not.

### Reading the display: digits, ranges and OL

A typical cheap meter is called "3½ digits" or "2000 counts". It shows numbers from -1999 to 1999 with a decimal point that moves with the range. The "half digit" is the leading one, which can only be blank or 1.

| Range | Largest reading | Resolution (one count) | 6 V shows as |
|---|---|---|---|
| 200 mV | 199.9 mV | 0.1 mV | OL |
| 2 V | 1.999 V | 0.001 V | OL |
| 20 V | 19.99 V | 0.01 V | 6.00 |
| 200 V | 199.9 V | 0.1 V | 6.0 |
| 600 V | 600 V | 1 V | 6 |

So:

- **Pick the smallest range that does not overflow.** 6 V on the 20 V range shows 6.00 (three significant digits). On the 200 V range it shows 6.0, wasting a digit. On the 2 V range it shows **OL** (overload): too big to display.
- **OL is not zero.** On the voltage settings it means "too big for this range, go up". On the resistance setting it means "more than the range can show", which with nothing connected means an open circuit (infinite resistance).
- **The 2000-count trap.** A 2000 Ω resistor on the "2k" range shows OL, because the display stops at 1999. Go up to 20k: it shows 2.00 kΩ.
- **Autoranging** meters pick the range for you, at the cost of being a little slower. The display then shows the unit and prefix (mV, V, kΩ, MΩ); read them every time.

### Accuracy: the number after the ±

The manual of a meter lists something like "DC V: ±(0.5 % + 2 counts)". Read it as "the true value is within half a percent of the reading, plus or minus two steps of the last digit". For 6.00 V on the 20 V range:

```
0.5 % of 6.00 V   = 0.03 V
2 counts x 0.01 V = 0.02 V
total             = ± 0.05 V      ->  the true voltage is between 5.95 V and 6.05 V
```

So if you calculated 6 V and read 5.97 V, that is a perfect match. If you read 4.5 V, something is really different from what you expected, and that is when you start looking for a problem.

## Build It

Our script models a 2000-count meter and the circuit above, then performs each measurement, the right way and the wrong way.

### Step 1: The meter's display

```python
COUNTS = 2000
VOLT_RANGES = [0.2, 2.0, 20.0, 200.0, 600.0]


def display(value, ranges, unit, fixed_range=None):
    candidates = [fixed_range] if fixed_range else ranges
    for full_scale in candidates:
        if abs(value) < full_scale * (COUNTS - 0.5) / COUNTS:
            step = full_scale / COUNTS
            decimals = max(0, -int(math.floor(math.log10(step))))
            return f"{round(value / step) * step:.{decimals}f} {unit}  (range {full_scale:g} {unit})"
    return f"OL  (range {candidates[-1]:g} {unit})"
```

With no fixed range it acts like an autoranging meter: it tries ranges from smallest to largest and uses the first one that fits. The step is range / 2000, and the value is rounded to a whole number of steps, just like the real display.

### Step 2: The circuit and the meter as resistors

```python
VOLTMETER_INPUT_OHMS = 10e6
AMMETER_SHUNT_OHMS = 1.0
BATTERY_VOLTS = 9.0
R1_OHMS = 1000.0
R2_OHMS = 2000.0


def parallel(first, second):
    return first * second / (first + second)


def voltmeter_across(resistor_ohms, other_ohms):
    loaded = parallel(resistor_ohms, VOLTMETER_INPUT_OHMS)
    return BATTERY_VOLTS * loaded / (loaded + other_ohms)


def voltmeter_in_series():
    total = R1_OHMS + R2_OHMS + VOLTMETER_INPUT_OHMS
    loop_current = BATTERY_VOLTS / total
    return loop_current * VOLTMETER_INPUT_OHMS, loop_current


def ammeter_in_series():
    return BATTERY_VOLTS / (R1_OHMS + R2_OHMS + AMMETER_SHUNT_OHMS)


def ammeter_across_battery(battery_internal_ohms):
    return BATTERY_VOLTS / (battery_internal_ohms + AMMETER_SHUNT_OHMS)
```

The trick is to treat the meter as just another resistor in the circuit: 10 MΩ for the voltmeter, 1 Ω for the ammeter. Each function adds that resistor in the right place and recomputes. (The series-sharing and side-by-side formulas are previews of Phase 04; here we only need the numbers.)

### Step 3: Ohmmeter and continuity

```python
OHMMETER_TEST_AMPS = 1e-4
CONTINUITY_THRESHOLD_OHMS = 30.0


def ohmmeter(resistance, voltage_already_there=0.0, thevenin_ohms=None):
    seen_ohms = resistance if thevenin_ohms is None else thevenin_ohms
    measured_volts = voltage_already_there + OHMMETER_TEST_AMPS * seen_ohms
    return measured_volts / OHMMETER_TEST_AMPS


def continuity(resistance):
    return "BEEP" if resistance < CONTINUITY_THRESHOLD_OHMS else "silent"
```

The ohmmeter divides the voltage it sees by its own test current. If the circuit is powered, `voltage_already_there` sneaks into that voltage and ruins the answer. (The odd name `thevenin_ohms` is the resistance the meter "sees" looking into the powered circuit; you will meet Thévenin in Phase 05.)

### Step 4: Run it

```
uv run python phases/02-your-first-circuits/07-measuring-with-a-multimeter/code/main.py
```

```
Circuit: 9 V battery, R1 = 1000 ohm and R2 = 2000 ohm in one loop
  true current 3.0000 mA, true V(R1) 3.0000 V, true V(R2) 6.0000 V

1. Voltage: probes ACROSS a part (in parallel), meter input 10 Mohm
  across R2: exact 5.99960 V  display 6.00 V  (range 20 V)
  across R1: exact 2.99980 V  display 3.00 V  (range 20 V)
  across R2 on the 2 V range : OL  (range 2 V)
  across R2 on the 200 V range: 6.0 V  (range 200 V)
  probes swapped on R2       : -6.00 V  (range 20 V)

2. Mistake: voltmeter put IN SERIES (loop broken, meter in the gap)
  meter shows 9.00 V  (range 20 V), loop current drops to 0.900 uA

3. Current: break the loop and put the meter IN SERIES (mA jack, 1 ohm inside)
  exact 2.9990 mA  display 3.00 mA  (range 20 mA)
  error caused by the meter: 0.033 %

4. Mistake: ammeter put ACROSS the battery (in parallel)
  battery inside resistance 1.5 ohm -> 3.60 A through a 0.2 A fuse: fuse BLOWS
  battery inside resistance 0.5 ohm -> 6.00 A through a 0.2 A fuse: fuse BLOWS

5. Resistance: power OFF, part out of circuit, meter pushes 0.1 mA and reads the voltage
    1000 ohm part -> 1000 ohm  (range 2000 ohm)
    2000 ohm part -> 2000 ohm  (range 20000 ohm)
  2000 ohm on the 2000 ohm range: OL  (range 2000 ohm)
  R2 measured with the battery still ON: 60700 ohm  (range 200000 ohm)  (nonsense)

6. Continuity (beeps below 30 ohm)
  jumper wire : BEEP
  R1          : silent
  broken wire : silent
```

Check section 2 by hand: the loop now has 1000 + 2000 + 10 000 000 = 10 003 000 Ω, so the current is 9 / 10 003 000 = 0.0000009 A = 0.9 µA, and the meter's share of the push is 0.9 µA x 10 000 000 Ω = 8.997 V, which displays as 9.00. The circuit has stopped working and the meter proudly shows the battery voltage: a very confusing reading if you do not know what happened.

Check section 5's powered case: the battery puts 6 V on R2; the meter adds 0.1 mA x 667 Ω = 0.067 V of its own; it divides 6.067 V by 0.0001 A and gets 60 670 Ω, displayed as 60 700.

## Use It

- **Is my battery flat?** DC volts across its terminals. A fresh alkaline AA reads about 1.5-1.6 V; below about 1.1 V it is nearly done. A 9 V battery reads about 9.5 V new. Measured with no load, a weak battery can still look fine, which is why battery testers put a resistor across it while they measure (the reason is internal resistance, Phase 06, Lesson 02).
- **Why doesn't my LED light?** Volts across the LED: about 1.8-2 V for a red LED that is conducting. 0 V means no current is reaching it (open loop, or the LED shorted out by the breadboard). Full battery voltage means the LED is in backwards or the loop is open on its far side.
- **How much current does my circuit draw?** Break the loop at the battery's plus wire and put the meter in series. Useful for estimating battery life (Phase 00, Lesson 03: hours = mAh / mA).
- **Which wire is which?** Continuity beep from one end of a cable to the other end.
- **Real numbers to expect.** A typical handheld meter: 10 MΩ input on volts, 2000 to 6000 counts, DC volts accuracy around ±0.5 %, mA jack fused at 200-500 mA, 10 A jack fused at 10 A with a high-energy fuse. Meters carry a safety category rating (CAT II, CAT III...) that says what kind of mains circuits they survive; in this course we stay at 12 V DC, where any meter is safe.

## Try It in the Lab

The lab task "Measure the bulb current without changing it" gives you a 6 V battery and a bulb that behaves like a 30 Ω resistor, with the loop already broken between the battery and the bulb. You choose what goes in the gap: a meter on its amps jack (behaves like a wire), a meter left on volts (behaves like a 10 MΩ resistor), or a meter with a blown fuse (behaves like an open switch). Before you try, work out what the bulb current *should* be with no meter at all, and then ask which choice lets the meter read that current while leaving the bulb exactly as bright as before.

## Common Mistakes

- **Measuring voltage with the red lead still in the mA or 10A jack.** You are shorting whatever you touch through the meter. At best you blow the fuse; on a car battery or a power supply that can deliver many amps, you can melt the probes. Before every voltage measurement, glance at the red lead.
- **Putting the voltmeter in series.** You read roughly the full supply voltage and the circuit stops working. Voltage is measured *across*, without disconnecting anything.
- **Putting the ammeter across a part (in parallel).** You short that part out, steal its current and probably blow the fuse. Current is measured *through*, by breaking the loop.
- **Measuring resistance in a powered circuit.** The readings are meaningless and you can damage the meter. Power off, and lift at least one leg of the part.
- **Ignoring the prefix and the range.** "4.70" on the 20k range is 4.70 kΩ, not 4.70 Ω. On autoranging meters, read the little m, k or M every time.
- **Thinking OL means zero.** It means "too big". On the ohms setting with nothing connected, OL is correct: the probes are not touching anything, which is an infinite resistance.
- **Worrying about a minus sign.** -6.00 V just means the probes are reversed relative to the push. Swap them or note the sign; nothing is damaged.
- **Touching both probe tips with your fingers on the ohms setting.** Your body becomes part of what you measure.

## Exercises

1. **Hook it up.** For each task, say which jack the red lead goes in, where the dial goes, and whether the meter goes across or in series: (a) the voltage of a 9 V battery, (b) the current through an LED, (c) the resistance of a resistor you just pulled out of a breadboard, (d) whether a USB cable's red wire is broken.
2. **Read the range.** A 3½-digit (2000 count) meter on manual ranges is measuring a 12.6 V car battery. What does it show on the 2 V, 20 V and 200 V ranges? Which range gives the best reading, and what is its resolution?
3. **Accuracy.** A meter specified at ±(0.8 % + 3 counts) on its 20 V range shows 4.85 V. Between which two values is the true voltage? You calculated 4.90 V. Is your calculation consistent with the reading?
4. **The series mistake.** A 12 V supply lights a lamp that behaves like a 48 Ω resistor. You accidentally put a voltmeter with 10 MΩ input resistance in series with it. What current flows, what does the meter read, and does the lamp light? What should the current be without the meter?
5. **The fuse.** A meter's mA jack has 1 Ω of internal resistance and a 0.4 A fuse. You touch it across (a) a fresh AA cell (1.5 V, about 0.15 Ω internal resistance), and (b) a 3 V coin cell (about 15 Ω internal resistance). Compute the current in each case and decide whether the fuse survives. Why are coin cells much more forgiving?

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| multimeter, DMM | "the meter" | an instrument that measures voltage, current, resistance and continuity, selected with a dial |
| across / in parallel | "put the probes on it" | connecting the meter to the two ends of a part without disconnecting anything; used for voltage |
| in series / in line | "break the circuit" | opening the loop so the current must pass through the meter; used for current |
| input resistance | "the meter's impedance" | the resistance the voltmeter puts between its probes, typically 10 MΩ; the higher, the less it disturbs |
| burden / shunt resistance | "the meter's resistance on amps" | the small resistance the ammeter adds to the loop, around 1 Ω on mA ranges; the lower, the less it disturbs |
| counts / 3½ digits | "the resolution" | how many different values the display can show: 2000 counts means -1999 to 1999 |
| OL | "overload" | the quantity is bigger than the selected range can display |
| accuracy spec | "±0.5 % plus 2" | the true value lies within that percentage of the reading plus that many steps of the last digit |
| continuity | "the beep test" | a low-resistance check that beeps when two points are connected |

## Further Reading

- [SparkFun, "How to Use a Multimeter"](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter) - photos of every setting and hookup.
- [All About Circuits, Vol. VI (Experiments), chapter 2 "Basic Concepts and Test Equipment"](https://www.allaboutcircuits.com/textbook/experiments/chpt-2/voltage-usage/) - hands-on voltmeter, ammeter and ohmmeter exercises.
- Fluke, "ABCs of Multimeter Safety" (application note, free on fluke.com) - why fuses and CAT ratings matter.
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., chapter 1 - short, sharp notes on voltmeter and ammeter loading.
