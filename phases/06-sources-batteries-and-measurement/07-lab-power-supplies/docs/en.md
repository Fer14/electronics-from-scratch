# Lab Power Supplies

> A bench supply is a voltage source with a guard dog: it holds the voltage you set until the current reaches the limit you set, then it holds the current instead.

**Type:** Build
**Prerequisites:** Phase 06 Lesson 01 (Ideal and Real Sources), Phase 06 Lesson 02 (Internal Resistance), Phase 06 Lesson 05 (Loading and Measurement Error)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Bench power supply | A box that plugs into the wall and gives an adjustable, steady DC voltage for experiments | An adjustable tap with a flow limiter |
| DC (direct current) | Current that flows in one direction only, from a steady voltage | A river flowing one way |
| Set voltage (V_set) | The voltage you dial in on the front panel | The pressure you choose on a pressure washer |
| Current limit (I_limit) | The most current the supply will allow; you dial it in too | A fuse that never blows, it just stops more from flowing |
| CV mode (constant voltage) | The supply is holding the voltage at V_set; the load decides the current | Cruise control holding speed on a flat road |
| CC mode (constant current) | The load wanted more than I_limit, so the supply holds the current at I_limit and lets the voltage fall | Cruise control giving up on a steep hill and holding engine power instead |
| Crossover | The load resistance where the supply switches between CV and CC: V_set / I_limit | The slope where cruise control gives up |
| Output resistance | The tiny internal resistance of the supply in CV mode | A very short, very wide pipe |
| Load regulation | How much the output voltage changes from no load to full load | How much the shower weakens when you open it fully |
| Ripple and noise | Small leftover wiggles on the "steady" output | Ripples on a calm pond |
| Remote sensing | Extra thin wires that let the supply measure the voltage right at the load | Checking the water pressure at the shower head instead of at the boiler |
| Split supply | Two outputs in series, giving a positive and a negative rail around a common middle (ground) | A seesaw with the pivot as zero |
| Rail | A supply line in a circuit, like +12 V or -12 V | A rail on a train track, carrying the power |
| Linear / switching supply | Two ways of building a supply: burning the excess as heat, or chopping it at high frequency | A brake versus a gearbox |

## Learning Objectives

- Explain CV and CC modes and predict which one a supply is in for any load.
- Compute the crossover load resistance and draw a supply's output "rectangle".
- Use the current limit to protect parts, in particular LEDs and circuits under test.
- Calculate the voltage lost in test leads and explain how remote sensing removes it.
- Read the main specs of a bench supply: load regulation, ripple and noise, ranges.
- Connect two outputs in series to make a split +/- supply.

## The Problem

You build a circuit on a breadboard, connect it to a 9 V battery, and something smells hot. A chip was in backwards. The battery happily delivered amperes into it until it was too late.

Now picture the same mistake on a bench supply with its current limit set to 50 mA. The moment you connect, the display shows 0.3 V and 50 mA and a "CC" light comes on. Nothing gets hot. You flip the chip and try again. The current limit turned a destroyed chip into a five-second lesson.

A bench supply is the most useful tool after the multimeter, but only if you understand its two modes. This lesson explains them, builds a model of a bench supply in our simulator, and covers the practical traps: thin leads, LEDs, and making negative voltages.

## The Physics

### What is inside

A classic **linear** bench supply does four things:

1. A **transformer** (Phase 08) turns the 230 V or 120 V mains into a lower AC voltage and isolates the output from the mains wiring.
2. A **rectifier** made of diodes (Phase 11) turns that AC into a bumpy DC.
3. A big **capacitor** (Phase 07) smooths the bumps into a DC with some ripple.
4. A **regulator** (Phase 12 and 18): a transistor in series with the output that acts like an automatically adjusted resistor. A control circuit compares the output with the voltage you set and turns the transistor "more on" or "less on" thousands of times per second to keep the output exactly right. The excess voltage is burned in the transistor as heat, which is why linear supplies have big heat sinks and fans.

A **switching** supply replaces the transformer and the hot transistor with a fast electronic switch chopping the current tens or hundreds of thousands of times per second (Phase 18). It is smaller, lighter and more efficient, with somewhat more high-frequency noise on its output.

### Why it behaves as an almost ideal source

Because the control circuit constantly corrects the output, a supply in CV mode acts like a voltage source with a tiny internal resistance, often a few milliohms. Compare that with a 9 V battery's 1 or 2 ohm (Lesson 02). That is why the bench supply's voltage barely moves when you change the load.

### The current limit

The control circuit also measures the output current through a small shunt resistor (the trick from Lesson 04). If the current would exceed the limit you set, a second control loop takes over and reduces the output voltage just enough to keep the current at exactly I_limit. Two loops, one in charge at a time.

## The Concept

### CV or CC? Ask the load

Set V_set = 12 V and I_limit = 0.5 A. Connect a load R.

1. **Try CV.** If the supply holds 12 V, the current is I = 12 / R (Ohm's law).
2. **Check the limit.** If 12 / R is at most 0.5 A, the supply stays in CV. Done.
3. **Otherwise CC.** The current is held at 0.5 A, and the voltage is whatever Ohm's law gives for that current: V = 0.5 * R.

| Load R | Wanted 12 / R | Mode | V out | I |
|---|---|---|---|---|
| 1000 ohm | 0.012 A | CV | 12 V | 0.012 A |
| 100 ohm | 0.12 A | CV | 12 V | 0.12 A |
| 24 ohm | 0.5 A | CV (at the edge) | 12 V | 0.5 A |
| 20 ohm | 0.6 A | CC | 0.5 * 20 = 10 V | 0.5 A |
| 10 ohm | 1.2 A | CC | 5 V | 0.5 A |
| 1 ohm | 12 A | CC | 0.5 V | 0.5 A |
| short circuit | infinite | CC | 0 V | 0.5 A |

The load resistance where the switch happens is the **crossover**:

    R_crossover = V_set / I_limit = 12 / 0.5 = 24 ohm

Read it: "loads heavier (smaller) than the set voltage divided by the set current push the supply into constant current."

### The rectangle

Plot output voltage against output current for every possible load:

```
   V
  12 |*****************+          CV edge: voltage fixed, current varies
     |                 *
     |                 *          CC edge: current fixed, voltage varies
     |                 *
   0 +-----------------*---- I
     0              0.5 A
```

Every operating point lies on the two edges of this rectangle. Compare it with a battery's sloping line (Lesson 01): the bench supply is an ideal voltage source on the top edge and an ideal current source on the right edge. You choose where the corner is.

### Protecting an LED

An LED (Phase 11 Lesson 07) is not a resistor. Below about 1.8 V a red LED conducts almost nothing; above about 2 V its current shoots up enormously for tiny extra voltage. Connected to a 5 V source with no resistor, it wants far more current than it can survive.

On a bench supply set to 5 V:

- With the current limit at 3 A, the supply goes into CC and pushes 3 A through the LED. The LED, rated about 20 mA, is destroyed in moments.
- With the current limit at 20 mA, the supply goes into CC at 20 mA. The output voltage settles at the LED's own voltage at that current, about 1.9 V. The LED glows normally.

In CC mode, the supply *is* the current-limiting resistor. This is a standard trick to test LEDs, and a reason to always set the current limit before connecting anything.

### The leads are part of the circuit

The front panel shows the voltage at the supply's terminals. Between the terminals and your circuit are two test leads, and each has resistance. A typical 1 m lead with crocodile clips can be 0.05 to 0.2 ohm, and banana-plug contacts add more.

```
  supply +5.000 V --[ lead 0.1 ohm ]--+
                                    [ board 2 ohm ]
  supply   0 V    --[ lead 0.1 ohm ]--+
```

The current flows through both leads, so they add 0.2 ohm in series:

1. I = 5 / (2 + 0.2) = 2.273 A.
2. Each lead drops 2.273 * 0.1 = 0.227 V.
3. The board gets 5 - 2 * 0.227 = 4.545 V. A 9 % shortfall, while the display proudly says 5.000 V.
4. Each lead also burns 2.273^2 * 0.1 = 0.52 W, which you can feel as warm wires.

**Remote sensing** fixes it. Better supplies have two extra "sense" terminals. You run two thin wires from them to the board itself. No load current flows in those wires, so they report the true board voltage (the same idea as the four-wire measurement in Lesson 05). The regulator then raises its output until the board sees 5 V: here 5 * (2 + 0.2) / 2 = 5.5 V at the terminals.

Without remote sensing: use short, thick leads, and measure the voltage at the board with your multimeter, not on the front panel.

### Where the heat goes in a linear supply

The regulator transistor sits in series between the smoothed internal DC and the output. All the load current flows through it, and it must drop the difference between the internal voltage and the output voltage. Power is voltage times current (Phase 03), so it burns:

    P_transistor = (V_internal - V_out) * I

Read it: "the heat in the regulator is the voltage it throws away times the current through it."

Worked example. A 0-30 V, 3 A linear supply has about 35 V inside.

| Setting | Voltage thrown away | Current | Heat in the regulator |
|---|---|---|---|
| 30 V, 3 A | 35 - 30 = 5 V | 3 A | 15 W |
| 12 V, 3 A | 35 - 12 = 23 V | 3 A | 69 W |
| 3.3 V, 3 A | 35 - 3.3 = 31.7 V | 3 A | 95 W |
| short circuit in CC at 3 A | 35 - 0 = 35 V | 3 A | 105 W |

The supply works hardest, and its fan is loudest, at *low* output voltage and high current, not at maximum voltage. Better linear supplies switch between transformer taps to keep V_internal only a few volts above the output, and switching supplies avoid the problem altogether.

### Load regulation and ripple

Datasheets describe how close to ideal a supply is:

- **Load regulation**: the change of output voltage from no load to full load, often written like "less than 0.01 % + 3 mV". A supply with 5 milliohm output resistance changes by 3 A * 0.005 = 15 mV from 0 to 3 A, which is 0.125 % of 12 V.
- **Line regulation**: the change when the mains voltage changes.
- **Ripple and noise**: the leftover wiggle, given in mV RMS or mV peak-to-peak over a frequency band. Linear supplies: often under 1 mV RMS. Switching supplies: a few mV, with spikes at the switching frequency.
- **Transient response**: how fast the voltage recovers after a sudden load change, for example "less than 50 microseconds to within 15 mV".

### Making plus and minus

Many circuits (op-amp circuits in Phase 13, audio amplifiers) need a positive and a negative supply around a common ground. A bench supply's outputs are **floating**: neither terminal is tied to earth unless you connect it. So you can put two outputs in series and call the middle "ground":

```
   output 1 (+)  ----------------- +12 V rail
   output 1 (-) --+
                  +--------------- 0 V (ground)
   output 2 (+) --+
   output 2 (-)  ----------------- -12 V rail
```

Measured from the middle: +12 V on top, -12 V at the bottom, 24 V rail to rail. Each output supplies its own rail's current, which can differ: here 100 mA on the positive rail into 120 ohm and 50 mA on the negative rail into 240 ohm. Many dual supplies have a "series" or "tracking" mode that does this internally and keeps both voltages equal.

You can also put two outputs in **parallel** for more current, but only if the supply supports it: two regulators fighting to hold slightly different voltages share current badly.

## Build It

### Step 1: A bench-supply model

Our simulator has ideal voltage and current sources. A bench supply is "one or the other, depending on the load". The model tries CV first; if that would exceed the limit, it rebuilds the circuit with a current source.

```python
def bench_supply(volts_set, amps_limit, attach_load):
    constant_voltage = Circuit()
    constant_voltage.voltage_source("Vset", "inner", "0", volts_set)
    constant_voltage.resistor("Rout", "inner", "out", OUTPUT_OHMS)
    attach_load(constant_voltage)
    result = constant_voltage.dc()
    amps = result.i("Rout")
    if amps <= amps_limit:
        return "CV", result.v("out"), amps
    constant_current = Circuit()
    constant_current.current_source("Iset", "0", "out", amps_limit)
    attach_load(constant_current)
    result = constant_current.dc()
    return "CC", result.v("out"), amps_limit
```

`attach_load` is a small function that adds whatever load we want to the circuit, so the same model works for resistors and LEDs. The table it prints matches the hand table above (with 11.998 V instead of 12.000 V at 24 ohm because of the 5 milliohm output resistance).

### Step 2: The rectangle

Sweeping the load from 0.01 ohm to 1 kohm and plotting every point draws the two edges. The plot is saved as `out.png`.

### Step 3: The LED test

```python
mode, volts, amps = bench_supply(5.0, limit, lambda c: c.led("D1", "out", "0", color="red"))
```

With a 3 A limit the model ends in CC at 3000 mA; with 20 mA it ends in CC at 20 mA and about 1.89 V across the LED (our simulator's red LED model).

### Step 4: Leads and remote sensing

```python
def board_with_leads(volts_set, lead_ohms, board_ohms):
    c = Circuit()
    c.voltage_source("Vset", "plus", "0", volts_set)
    c.resistor("Rlead_plus", "plus", "board_plus", lead_ohms)
    c.resistor("Rboard", "board_plus", "board_minus", board_ohms)
    c.resistor("Rlead_minus", "board_minus", "0", lead_ohms)
    r = c.dc()
    return r.v("board_plus", "board_minus"), r.i("Rboard")
```

`r.v("board_plus", "board_minus")` is the voltage between two nodes: what a meter clipped on the board would read. Output: 4.545 V at 2.273 A; with sensing, 5.500 V at the terminals and 5.000 V on the board.

### Step 5 and Step 6: Regulation and the split supply

No load to 3 A changes the output by 15.0 mV (0.125 %). Two 12 V sources in series with the middle as node "0" give +12.00 V and -12.00 V.

Run it:

```bash
uv run python phases/06-sources-batteries-and-measurement/07-lab-power-supplies/code/main.py
```

## Use It

- **A typical first supply:** one output, 0 to 30 V, 0 to 3 A or 5 A, with two knobs (voltage and current) and two displays. Many have a "CV/CC" indicator light.
- **Programmable supplies** (from makers such as Rigol, Siglent, Keysight, Rohde & Schwarz and others) add several outputs, remote sensing, USB/LAN control and logging. Their datasheets give load regulation, ripple and noise, and the resolution of the setting and readback.
- **Setting up safely:** before connecting a new circuit, short the output leads together and set the current limit (the display then shows the limit current), unshort, set the voltage, connect, and only then switch the output on. Raise the limit gradually.
- **Charging batteries:** a lithium-ion cell is charged with exactly this CC-then-CV pattern: constant current until the cell reaches 4.2 V, then constant voltage while the current tapers off (Phase 18). A bench supply can do it, carefully, with the right settings.
- **USB power delivery chargers and phone chargers** are switching supplies with a fixed set of voltages and their own current limits.

## Try It in the Lab

Your supply is set to 5.00 V, and a board that behaves like a 10 ohm resistor (it draws about 0.5 A) needs at least 4.9 V at its own pins. You must choose the two test leads, one for the positive side and one for the negative side. Each lead is modelled by its resistance.

Think about it before pressing RUN:

- What is the most total lead resistance the board can tolerate? Solve 5 * 10 / (10 + R_leads) = 4.9.
- Both leads carry the same current. Does it matter which one is the bad one?
- How much power would the worst lead burn at about 0.5 A?

## Common Mistakes

- **Leaving the current limit at maximum.** Then the supply is "a battery that can deliver amps", and a mistake can burn parts. Set the limit just above what the circuit should draw.
- **Thinking CC mode is a fault.** It is the supply doing its job. If you see CC when you didn't expect it, your circuit draws more than you think: look for a short or a wrong part.
- **Trusting the front-panel voltage at high current.** Measure at the board, or use remote sensing.
- **Connecting a supply to a battery without thinking.** A battery is a voltage source too. If the supply's voltage is lower, current flows backwards into the supply; if higher, it charges the battery at up to the current limit. Both need care.
- **Forgetting the outputs float.** Two supplies whose minus terminals are not connected do not share a ground. Join them where you want ground to be.
- **Adjusting the voltage with the output on and a sensitive circuit attached.** Turning the knob the wrong way can overvolt the circuit. Set first, then enable.

## Exercises

1. A supply is set to 9 V and 0.1 A. What mode is it in with a 47 ohm load? What are the voltage and current? Repeat for 220 ohm.
2. What is the crossover resistance of a supply set to 3.3 V and 250 mA? Draw its rectangle with numbers on the axes.
3. A board draws 3 A from a 3.3 V supply through leads of 0.08 ohm each. What voltage does the board see? What output voltage must remote sensing produce to give the board 3.3 V?
4. A supply has 2 milliohm output resistance. What is its load regulation from 0 to 5 A, in mV and as a percentage of 5 V?
5. You need +15 V and -15 V around ground, with 200 mA on the positive rail and 80 mA on the negative rail. Draw the connection of two outputs, and give a safe current limit for each. Then modify Step 6 of the script to check your design.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| CV mode | "Normal mode" | Supply regulates voltage at V_set; current set by the load, below I_limit |
| CC mode | "It's current limiting" | Supply regulates current at I_limit; voltage set by the load, below V_set |
| Crossover | "Where it switches" | Load resistance V_set / I_limit separating CV and CC |
| Current limit | "The fuse setting" | The maximum current the regulator will allow; it never blows, it regulates |
| Load regulation | "How stiff it is" | Output change from no load to full load, a percentage plus a fixed offset |
| Ripple and noise | "Dirt on the output" | Residual AC on the DC output, in mV RMS or peak-to-peak |
| Remote sensing | "Sense leads" | Separate wires that let the regulator correct for the voltage drop in the load leads |
| Floating output | "Isolated" | Output terminals not tied to earth, so outputs can be stacked in series |

## Further Reading

- Keysight (Agilent), *DC Power Supply Handbook* / application note AN 90B, covering CV/CC operation, remote sensing and series/parallel connection.
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 9 (voltage regulation and power conversion), for what is inside a supply.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., the power-supply and test-equipment sections.
- EEVblog video tutorials on choosing and using a bench power supply, on YouTube.
