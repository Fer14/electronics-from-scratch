# Inside the Multimeter

> A multimeter only ever measures one thing well. Every other range is a resistor trick that turns your quantity into that one thing.

**Type:** Build
**Prerequisites:** Phase 02 Lesson 07 (Measuring with a Multimeter), Phase 03 (Resistance and Ohm's Law), Phase 04 Lessons 05-06 (The Voltage Divider, The Current Divider), Phase 06 Lesson 01 (Ideal and Real Sources)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Multimeter | One instrument that measures voltage, current and resistance (and often more) | A Swiss army knife for circuits |
| Meter movement | The needle mechanism of an old analog meter: a coil of wire on a pivot, between magnets | A weather vane pushed by current instead of wind |
| Full-scale current | The current that swings the needle all the way to the end of the scale | The top mark on a measuring cup |
| Range | The largest value a meter setting can show | The size of the cup you chose |
| Multiplier | A large resistor put in series with the movement to make a voltmeter | A long narrow straw that limits how fast you can drink |
| Shunt | A small resistor put in parallel with the movement to make an ammeter, so most of the current bypasses it | A bypass road around a narrow village street |
| Sensitivity (ohms per volt) | How many ohms an analog voltmeter has for each volt of range | How gently the meter sips from the circuit |
| ADC (analog-to-digital converter) | A chip that turns a voltage into a number | A ruler that reads itself and writes the result down |
| Counts | The largest number the display can show, e.g. 2000 counts shows up to 1999 | The number of marks on the ruler |
| Resolution | The smallest step the display can show on a range | The spacing between the ruler's marks |
| Input resistance | The resistance a voltmeter presents to the circuit | How much water the gauge itself lets through |
| Burden voltage | The voltage an ammeter steals from the circuit, because current flows through its shunt | The pressure lost in a water meter |
| OL | "Over limit": the value is bigger than the range can show | A cup overflowing |

## Learning Objectives

- Describe how a moving-coil meter turns current into needle angle.
- Design the multiplier resistor that turns a movement into a voltmeter for any range.
- Design the shunt resistor that turns a movement into an ammeter for any range.
- Explain how an ohmmeter works and why its scale is backwards and nonlinear.
- Describe the parts of a digital multimeter: input divider, ADC, counts, resolution, shunts, burden voltage.
- Simulate each of these circuits with our simulator and check the results by hand.

## The Problem

You turn the dial of your multimeter from "20 V" to "200 mA" and suddenly the same two probes measure something completely different. How? The display inside is not three different instruments. It is one measuring core with a few resistors that the dial switches in and out.

Knowing what those resistors do is not trivia. It tells you why putting a meter set to "amps" across a battery can blow its fuse (or the meter); why the meter shows "OL"; why a cheap meter reads 4.76 V where you expected 5 V in a high-resistance circuit (next lesson); and how to turn any small current-measuring device into whatever meter you need. Engineers do this all the time, for example to measure a battery's current inside a gadget with a tiny shunt resistor and a microcontroller.

## The Physics

### The moving-coil movement

Before digital meters, every meter was built around a **moving-coil movement** (also called a d'Arsonval movement, after the French physicist who developed it, with improvements by Edward Weston).

```
        N  magnet  S
     +----+    +----+
     |    | /\ |    |     coil of fine wire on a pivot,
     |    |/  \|    |     with a light needle attached
     |    | () |    |
     |    |\  /|    |     a hair spring pulls the needle back to zero
     +----+ \/ +----+
```

A current through a coil of wire turns it into a small magnet (you will meet electromagnetism in Phase 08). Sitting between the poles of a permanent magnet, the coil feels a twisting force proportional to the current. A thin spring twists back with a force proportional to the angle. The needle settles where the two balance, so:

**The needle's angle is proportional to the current through the coil.**

That is all a movement measures: current. A typical good one reaches full scale with 50 microamps; a rugged one with 1 mA. The coil is made of fine copper wire, so it has resistance too, from tens of ohms to a few thousand.

Our example movement: **full scale 1 mA, coil resistance 200 ohm**. By Ohm's law the voltage across the coil at full scale is 1 mA * 200 ohm = 0.2 V. On its own, this movement is an ammeter for 0 to 1 mA, or a voltmeter for 0 to 0.2 V. Not very useful. Let's extend it.

### The digital core

A digital multimeter replaces the needle with an **analog-to-digital converter** (ADC). Typical meter ADCs measure a small voltage, for example 0 to 200 mV, and output a whole number. A "2000 count" meter shows 0 to 1999; on a 200 mV basic range each count is 0.1 mV. The converter's input draws almost no current. So the digital core measures **voltage**, while the analog movement measures **current**. Both use the same resistor tricks to measure everything else.

## The Concept

### Trick 1: The voltmeter (series multiplier)

To measure up to 10 V with a movement that is full scale at 0.2 V, put a big resistor in series. The resistor takes most of the voltage; the coil only gets its share.

```
   probe +  ----[ R_mult ]----[ coil 200 ohm ]---- probe -
                                 (needle)
```

At full range, 10 V must push exactly 1 mA through the whole chain. Ohm's law gives the total resistance:

    R_total = V_range / I_full_scale = 10 V / 0.001 A = 10 000 ohm

The coil already has 200 ohm, so the multiplier is the rest:

    R_mult = V_range / I_full_scale - R_coil

Read it: "the multiplier is whatever resistance is still missing to make the full-range voltage push exactly full-scale current."

| Range | R_total | R_mult |
|---|---|---|
| 1 V | 1000 ohm | 800 ohm |
| 10 V | 10 000 ohm | 9800 ohm |
| 100 V | 100 000 ohm | 99 800 ohm |

Because the current is proportional to the voltage, the scale stays linear: 5 V on the 10 V range swings the needle to exactly half.

**Sensitivity.** Every range has 1000 ohm of total resistance per volt of range. That number, 1 / I_full_scale, is printed on analog meters as "ohms per volt". A 50 microamp movement gives 1 / 0.00005 = 20 000 ohm per volt, which is why good analog meters used very sensitive movements: the voltmeter then draws less current from the circuit it measures (Lesson 05).

### Trick 2: The ammeter (parallel shunt)

To measure up to 100 mA with a 1 mA movement, let most of the current bypass the coil through a small parallel resistor, the **shunt**.

```
                +---[ coil 200 ohm ]---+
   probe in ----+                      +---- probe out
                +------[ R_shunt ]-----+
```

At full range, 1 mA must go through the coil and the remaining 99 mA through the shunt. They are in parallel, so they have the same voltage across them (Phase 04). The coil's voltage is 1 mA * 200 ohm = 0.2 V, so:

    R_shunt = 0.2 V / 0.099 A = 2.02 ohm

In general:

    R_shunt = R_coil * I_full_scale / (I_range - I_full_scale)

Read it: "the shunt is the coil resistance scaled down by how many times more current the shunt must carry than the coil."

| Range | R_shunt |
|---|---|
| 10 mA | 200 * 1 / 9 = 22.22 ohm |
| 100 mA | 200 * 1 / 99 = 2.020 ohm |
| 1 A | 200 * 1 / 999 = 0.2002 ohm |

Notice something important. At full scale on every range, the voltage across the meter is 0.2 V (the coil's full-scale voltage). That voltage is stolen from the circuit you are measuring: it is the **burden voltage**. An ammeter is placed *in series* with the circuit (all the current must pass through it), so its burden directly subtracts from what the circuit gets.

And notice the danger: on the 1 A range, the meter between its probes is about 0.2 ohm. Put those probes across a battery (as if measuring voltage) and Ohm's law says huge current flows. This is the number one way beginners destroy meters, and why every current range has a fuse.

### Trick 3: The ohmmeter (battery and movement)

To measure resistance, the meter must make its own current. It contains a battery (say 1.5 V) and a series "zero adjust" resistor chosen so that with the probes shorted together (0 ohm) exactly full-scale current flows:

```
   (+)1.5 V ---[ R_zero ]---[ coil ]--- probe A
     |                                      [ R_x unknown ]
     +------------------------------------- probe B
```

    R_zero + R_coil = 1.5 V / 0.001 A = 1500 ohm

With an unknown R_x between the probes:

    I = 1.5 / (1500 + R_x)

and the needle fraction is

    needle = 1500 / (1500 + R_x)

| R_x | Needle |
|---|---|
| 0 ohm | 100 % |
| 150 ohm | 90.9 % |
| 500 ohm | 75 % |
| 1500 ohm | 50 % |
| 4500 ohm | 25 % |
| 15 000 ohm | 9.1 % |
| infinite (open) | 0 % |

So the analog ohm scale runs **backwards** (zero ohms at the right end) and is **squashed**: the middle of the scale is exactly the meter's internal resistance (1500 ohm here), and big values crowd together near the left. Different ohm ranges change the internal resistance (and sometimes the battery), so the "mid-scale" value moves to where you want accuracy. As the battery ages, the zero-adjust knob compensates.

### Trick 4: The digital voltmeter (divider ladder)

The digital core measures 0 to 200 mV. To measure 12 V, the meter divides the input down with a chain of resistors, the **input divider**, typically 10 Mohm in total:

```
  probe + o---[ 9 M ]--+--[ 900 k ]--+--[ 90 k ]--+--[ 10 k ]--+--- probe - (COM)
                       |             |            |            |
                     tap 2 V       tap 20 V    tap 200 V
                     (1/10)        (1/100)     (1/1000)
```

Each tap is a voltage divider (Phase 04): the fraction is the resistance below the tap over the total.

- Tap below 9 M: (900k + 90k + 10k) / 10 M = 1 M / 10 M = 1/10.
- Next: 100 k / 10 M = 1/100.
- Last: 10 k / 10 M = 1/1000.

The range switch connects the ADC to the tap that brings the input below 200 mV. Worked example: 12 V on the 20 V range. The tap divides by 100: 12 / 100 = 0.120 V = 120 mV. The ADC reads 120.0 mV, which is 1200 counts. The meter multiplies back by 100 and shows **12.00 V**.

On the 200 V range the same 12 V gives 12 mV at the tap: 120 counts, displayed as **12.0 V**. One digit lost: choose the lowest range that does not overflow. Feed 230 V into the 200 V range: 230 mV at the tap is 2300 counts, more than 1999: the display shows **OL**. Many modern meters choose the range for you ("autoranging") by trying taps in turn.

**Resolution** on each range is the voltage of one count:

| Range | Divide by | One count is |
|---|---|---|
| 200 mV | 1 | 0.1 mV |
| 2 V | 10 | 1 mV |
| 20 V | 100 | 10 mV |
| 200 V | 1000 | 0.1 V |

Whatever range you choose, the probes see 10 Mohm. That is the meter's **input resistance**, and it is ten thousand times larger than our analog 10 V range. You will see in Lesson 05 why that matters.

### Trick 5: The digital ammeter (shunt and voltmeter)

A digital meter measures current by passing it through a known shunt and measuring the shunt's voltage with the ADC. For example, a 200 mA range might use a 1 ohm shunt: 150 mA makes 150 mV, which the ADC reads as 1500 counts. A 10 A range might use 0.01 ohm: 2.5 A makes only 25 mV.

The burden voltage is the shunt's voltage, here up to 200 mV, plus the resistance of fuses, switch contacts and test leads. Datasheets list it as "burden voltage" in mV per mA or mV per A.

### Accuracy specs

A digital meter's accuracy is written like "plus or minus (0.5 % + 2 counts)". On the 20 V range reading 12.00 V: 0.5 % of 12.00 is 0.06 V, and 2 counts are 0.02 V, so the true value lies between 11.92 and 12.08 V. The last digit is not a promise.

## Build It

### Step 1 and Step 2: Voltmeter

```python
def multiplier_for(volts_range):
    return volts_range / FULL_SCALE_AMPS - COIL_OHMS


def analog_voltmeter_reading(measured_volts, volts_range):
    c = Circuit()
    c.voltage_source("Vx", "x", "0", measured_volts)
    c.resistor("Rmult", "x", "coil", multiplier_for(volts_range))
    c.resistor("Rcoil", "coil", "0", COIL_OHMS)
    return c.dc().i("Rcoil")
```

The simulator confirms 100 % deflection at full range and 50 % at half range for each of 1, 10 and 100 V, with multipliers of 800, 9800 and 99 800 ohm.

### Step 3: Ammeter

```python
def shunt_for(amps_range):
    return COIL_OHMS * FULL_SCALE_AMPS / (amps_range - FULL_SCALE_AMPS)
```

We drive the meter with a current source (the "circuit current" we want to measure) and read the coil's share. Each range shows 100.0 % with 200 mV across the meter.

### Step 4: Ohmmeter

The simulator reproduces the backwards, squashed table: 100 % at 0 ohm, exactly 50 % at 1500 ohm, about 1 % at 150 kohm.

### Step 5: Digital voltmeter

```python
LADDER = [9e6, 900e3, 90e3, 10e3]
```

The script builds the 10 Mohm ladder in the simulator, reads the tap chosen by the range, turns it into counts and formats the display with the right number of decimals:

```
  measure   0.1234 V on 200 mV: converter sees  123.400 mV, display 0.1234
  measure   1.5000 V on    2 V: converter sees  150.000 mV, display 1.500
  measure  12.0000 V on   20 V: converter sees  120.000 mV, display 12.00
  measure  12.0000 V on  200 V: converter sees   12.000 mV, display 12.0
  measure 230.0000 V on  200 V: converter sees  230.000 mV, display OL
```

### Step 6: Digital current

Three shunts and three currents give 150, 150 and 25 mV of burden voltage.

Run it:

```bash
uv run python phases/06-sources-batteries-and-measurement/04-inside-the-multimeter/code/main.py
```

## Use It

- **Typical handheld DMM.** 10 Mohm input resistance on DC volts, 2000 to 6000 counts (cheap) or 20 000 to 50 000 counts (better), current ranges in mA and in A with separate fused jacks.
- **Fuses.** The mA jack typically has a fast fuse of a few hundred mA; the A jack a 10 A fuse. Good meters use special high-energy fuses rated for 600 or 1000 V so that a mistake does not turn into an arc.
- **Safety categories.** Meters are rated CAT II, CAT III or CAT IV with a voltage, describing which kind of mains wiring they can safely probe. A cheap meter rated only CAT II 300 V does not belong on a building's distribution panel.
- **Current-sense resistors.** Phone chargers, battery management chips and motor drivers all measure current exactly like Trick 5: a milliohm resistor in the current path and a small amplifier reading its voltage.
- **Analog panel meters.** Still sold for power supplies and audio equipment, always with a datasheet listing full-scale current and coil resistance, so you can design multipliers and shunts as in this lesson.

## Try It in the Lab

You have a moving-coil movement with 1 mA full scale and a 200 ohm coil, connected to a 10 V test source. You want a 10 V voltmeter: at 10 V the needle should sit at (or just below) full scale, never past it. Choose the multiplier resistor from the parts bin.

Questions to answer before pressing RUN:

- What total resistance makes 10 V push exactly 1 mA?
- The ideal multiplier is not a standard value. Which candidate gets closest without pinning the needle past full scale?
- How far below full scale is the needle with your choice, in percent?

## Common Mistakes

- **Measuring voltage with the probes in the amps jack.** The meter is then a near-short. Always move the red probe back to the V jack after measuring current.
- **Putting an ammeter in parallel.** An ammeter goes *in series*: break the circuit and let the current flow through the meter.
- **Measuring resistance in a powered circuit.** The ohmmeter's tiny test current is swamped by the circuit's own voltage; the reading is wrong and the meter can be damaged. Power off and, ideally, lift one leg of the part.
- **Trusting every digit.** Accuracy is a percentage plus a few counts. The last digit flickers for a reason.
- **Using a range that is too high.** 12 V on the 1000 V range might read "12" instead of "12.00". Choose the lowest range that does not show OL.
- **Ignoring burden voltage.** Measuring a circuit powered from 3.3 V with a 200 mV burden ammeter changes the circuit by 6 %.

## Exercises

1. A movement has 50 microamp full scale and 2 kohm coil resistance. What is its sensitivity in ohms per volt? Design the multiplier for a 50 V range.
2. Using the same movement, design a shunt for a 10 mA range. What is the burden voltage at full scale?
3. For the ohmmeter of this lesson (1.5 V, 1500 ohm internal), what unknown resistance puts the needle at 80 %? At 10 %?
4. A 4000-count meter has a 400 mV basic range and a 10 Mohm input divider. Draw a ladder for the 4 V, 40 V and 400 V ranges and give each resistor.
5. A 6000-count meter on its 6 V range reads 3.300 V. Its spec is plus or minus (0.5 % + 3 counts). What is the band in which the true value lies?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Multimeter | "The meter" | One measuring core (current for analog, voltage for digital) plus switched resistors |
| Multiplier | "The voltage range resistor" | Series resistor that sets the full-range voltage of a voltmeter |
| Shunt | "The current range resistor" | Parallel (bypass) resistor that sets the full-range current of an ammeter |
| Ohms per volt | "Analog meter quality" | 1 / full-scale current; voltmeter resistance per volt of range |
| Input resistance | "Meter impedance" | Resistance between the voltmeter's probes, typically 10 Mohm for a DMM |
| Burden voltage | "Ammeter drop" | Voltage lost across an ammeter in series with the circuit |
| Counts | "Digits" | The display's maximum number; sets resolution with the range |
| OL | "The meter is broken" | Over limit: the input exceeds the selected range |

## Further Reading

- All About Circuits, *Lessons in Electric Circuits*, Volume I (DC), chapter 8 "DC Metering Circuits" (movements, voltmeter and ammeter design, ohmmeters): https://www.allaboutcircuits.com/textbook/direct-current/chpt-8/what-is-a-meter/
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 1 (measuring voltage and current, and the effect of the meter).
- Fluke, "ABCs of Multimeter Safety" application note (measurement categories, fuses), from the Fluke library.
- Datasheet of a classic DMM converter chip such as the Intersil ICL7106/ICL7107 (3 1/2 digit, 2000-count, 200 mV basic range), the core of countless cheap multimeters.
