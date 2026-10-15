# Ideal and Real Sources

> An ideal source never gives in. A real one always does, a little, and that little is a resistor hiding inside.

**Type:** Learn
**Prerequisites:** Phase 02 (Your First Circuits), Phase 03 (Resistance and Ohm's Law), Phase 04 (Kirchhoff's Laws), Phase 05 Lesson 06 (Thevenin and Norton)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Source | Anything that pushes charge around a circuit and hands it energy | The pump in a garden fountain |
| Voltage source | A source that tries to keep a fixed voltage between its two terminals | A water tower that keeps the same height of water above your tap |
| Current source | A source that tries to keep a fixed current flowing through itself | A conveyor belt that moves a fixed number of boxes per second, however heavy |
| Terminal | One of the two metal contacts where you connect wires to a part | The two ends of a battery |
| Load | Whatever the source is feeding: a lamp, a motor, a resistor | The person drinking from the tap |
| Ideal | A perfect, imaginary version with no losses or limits | A frictionless slide in a physics problem |
| Internal resistance | The resistance that is built into the source itself, in the path of its own current | A narrow pipe inside the pump that you cannot remove |
| EMF (electromotive force) | The voltage a source "wants" to give, before any of it is lost inside | The pressure the pump makes when nothing is flowing |
| Terminal voltage | The voltage you actually measure on the outside, between the terminals | The pressure you feel at the tap while water flows |
| Open circuit | Nothing connected: zero current flows out | A tap that is closed |
| Short circuit | The terminals joined by a wire with (almost) zero resistance | Ripping the tap off the pipe |
| Model | A drawing made of simple ideal parts that behaves like the real thing | A map: not the city, but good enough to find your way |

## Learning Objectives

- Say in your own words what an ideal voltage source and an ideal current source promise, and why no real device can keep that promise.
- Draw the model of a real voltage source (ideal source plus series resistor) and of a real current source (ideal source plus parallel resistor).
- Calculate the terminal voltage of a real source for any load with Ohm's law and Kirchhoff's voltage law.
- Show that a series model and a parallel model can behave identically from the outside.
- Build both models in our simulator and read their output lines.

## The Problem

You buy a 9 V battery. The label says 9 V, your multimeter says 9.4 V when nothing is attached. You connect a small motor and measure again: 7.8 V. You connect a bigger motor and the battery reads 5 V and gets warm. The label did not lie, and your meter is not broken. What is going on?

Until now, every circuit in this course had a "battery" drawn as a perfect thing that always gives exactly its voltage. That picture was a useful lie. It let us learn Ohm's law and Kirchhoff's laws without distractions. But it predicts nonsense in extreme cases: if you put a 9 V perfect battery across a 0.001 ohm wire, Ohm's law says 9000 A would flow. A real 9 V battery gives maybe 2 or 3 A into a short and gets hot.

In this lesson you learn two ideal sources, see exactly where they break, and fix them with one extra resistor. That one resistor explains the sagging battery, the warm battery, the dim headlights when you start a car, and why your phone charger can't run a hair dryer.

## The Physics

### What a source does physically

Inside a battery, a chemical reaction pulls electrons off one material and pushes them toward another. This piles extra electrons on one terminal (the negative one) and leaves the other one short of electrons (the positive one). That separation of charge is what creates the voltage between the terminals. Remember from Phase 01 that voltage is energy per unit of charge: 9 V means every coulomb of charge that goes around the circuit gets 9 joules of energy from the battery.

When you connect a load, charges flow out of one terminal, through the load, and back into the other terminal. For the battery to keep the voltage up, the chemistry must keep moving charge inside the battery, from one terminal back to the other, as fast as it leaves through the outside circuit.

### Why the voltage drops when current flows

The charges moving inside the battery have to travel through real materials: a paste of chemicals, a liquid or gel called the electrolyte, metal plates, the contacts. None of those is a perfect conductor. Pushing charge through them costs some energy, exactly like pushing it through a resistor costs energy. That energy is lost inside the battery as heat (this is why it gets warm).

So the battery "creates" its full voltage chemically, but it spends a part of it just getting the charge through its own insides. The more current you ask for, the bigger that internal loss is (Ohm's law: a voltage drop equals current times resistance). What is left over appears on the terminals.

A generator, a solar cell and a bench power supply all have the same story with different insides: some winding of copper wire, some semiconductor, some transistor. Every real source has an inside, and every inside has resistance.

### Why a current source is physically different

Some devices behave the other way round: they try to keep the *current* fixed. A solar cell in bright light is a good example. Each photon of light that is absorbed frees roughly one electron, so the number of electrons pushed around per second is set by how much light arrives, not by what you connect. Over a wide range of loads, a solar cell gives almost the same current. Transistor circuits (Phase 12) also make very good current sources.

A real current source also leaks. Some of the charge it pushes takes a shortcut back inside the device instead of going through your load. We model that leak as a resistor in *parallel* with the ideal current source.

## The Concept

### The ideal voltage source

An **ideal voltage source** promises: "the voltage between my terminals is exactly V, whatever you connect, and I will supply whatever current that takes."

```
        +  ideal voltage source, symbol: a circle with + and -
      (   )      or the long/short plate battery symbol
        -
```

Connect a load resistor R_L (R is resistance in ohms, the subscript L means "load"). The voltage across the load is V, so Ohm's law (I = V / R, current equals voltage divided by resistance) gives the current:

```
      +-----+-----+
      |           |
     (+) 9 V     [R_L]
     (-)          |
      |           |
      +-----------+
```

Read the formula out loud: "the current is nine volts divided by the load resistance."

    I = 9 V / R_L

| R_L | I = 9 / R_L |
|---|---|
| 10 000 ohm | 0.0009 A (0.9 mA) |
| 1000 ohm | 0.009 A (9 mA) |
| 100 ohm | 0.09 A |
| 10 ohm | 0.9 A |
| 1 ohm | 9 A |
| 0.001 ohm | 9000 A |

The last line is the problem. A perfect voltage source into a short circuit would push infinite current. Nothing in the real world does that. The ideal voltage source is a great model only while the current is small compared to what the real device can deliver.

### The ideal current source

An **ideal current source** promises: "the current through me is exactly I, whatever you connect, and I will make whatever voltage that takes." Its symbol is a circle with an arrow inside, pointing the direction the current is pushed.

```
      +-----+-----+
      |           |
     ( ^ ) 10 mA [R_L]
      |           |
      +-----------+
```

The current through R_L is 10 mA (milliamperes: one thousandth of an ampere each). The voltage across it follows from Ohm's law, V = I * R ("voltage equals current times resistance"):

| R_L | V = 0.010 * R_L |
|---|---|
| 1 ohm | 0.01 V |
| 100 ohm | 1 V |
| 1000 ohm | 10 V |
| 10 000 ohm | 100 V |
| open circuit (infinite R) | infinite V |

Now the last line is the problem. An ideal current source left open would make an infinite voltage, trying to push charge across the air gap. A real one cannot. The ideal current source is a good model only while the voltage stays small compared to what the real device can make.

Notice the symmetry:

| | Ideal voltage source | Ideal current source |
|---|---|---|
| Keeps fixed | Voltage | Current |
| Adjusts freely | Current | Voltage |
| Dangerous load | Short circuit (infinite current) | Open circuit (infinite voltage) |
| Happy load | Open circuit (zero current) | Short circuit (zero voltage) |

### The real voltage source: a resistor in series

To fix the voltage source, put a resistor inside the box, in series with the ideal source. We call the ideal part's voltage the **EMF** (written E or V_oc) and the resistor the **internal resistance** (written r, or R_int).

```
          the battery "box"
     +------------------------+
     |                        |
     |   (+) E = 9 V          |
     |    |                   |
     |   [r = 2 ohm]          |
     |    |                   |
     +----o terminal +--------+------+
          |                          |
                                    [R_L]
          o terminal - --------------+
```

The same current I goes through r and through R_L (they are in series, Phase 04). Kirchhoff's voltage law says the voltages around the loop add up to zero, so the EMF is split between r and R_L:

    E = I * r + I * R_L

Say it: "the nine volts the chemistry makes are shared between the inside resistor and the load, in proportion to their resistances." Solve for the current:

    I = E / (r + R_L)

And the **terminal voltage** (what you measure outside) is the EMF minus what is lost inside:

    V_terminal = E - I * r

Worked example. E = 9 V, r = 2 ohm, R_L = 10 ohm.

1. Total resistance: 2 + 10 = 12 ohm.
2. Current: 9 / 12 = 0.75 A.
3. Lost inside: 0.75 * 2 = 1.5 V.
4. Terminal voltage: 9 - 1.5 = 7.5 V. Check: 0.75 * 10 = 7.5 V across the load. Same answer.

Now the extremes behave:

- **Open circuit** (R_L infinite): I = 0, nothing is lost inside, V_terminal = E = 9 V. This is why a battery reads its full voltage when nothing is connected.
- **Short circuit** (R_L = 0): I = E / r = 9 / 2 = 4.5 A. Large, but finite. All 9 V are lost inside, and all the power (9 * 4.5 = 40.5 W) is heat inside the battery. That is why shorted batteries get dangerously hot.

### The output line

Put the terminal voltage on the vertical axis and the current on the horizontal axis. For the real voltage source, V_terminal = E - I * r is a straight line:

```
  V
  9 |*
    |   *
    |      *        slope = -r  (2 V lost for every 1 A drawn)
    |         *
    |            *
  0 +---------------*----  I
    0              4.5 A
```

It starts at E (the open-circuit voltage) on the voltage axis and ends at E / r (the short-circuit current) on the current axis. An ideal voltage source would be a perfectly flat line at 9 V. The steeper the line slopes down, the bigger the internal resistance and the "weaker" the source.

You can read the internal resistance straight off the line: r = (open-circuit voltage) / (short-circuit current) = 9 / 4.5 = 2 ohm.

### The real current source: a resistor in parallel

To fix the current source, put a resistor inside the box *in parallel* with it. Call it R_sh ("shunt", meaning a side path).

```
     +-----+---------+-------+
     |     |         |       |
   ( ^ )  [R_sh]     |      [R_L]
   10 mA  1 kohm     |       |
     |     |         |       |
     +-----+---------+-------+
```

The 10 mA arrives at the top node and splits between R_sh and R_L (current divider, Phase 04). The load gets:

    I_L = I * R_sh / (R_sh + R_L)

Read it: "the load gets the fraction of the current equal to the shunt's resistance over the total of both."

Worked example. I = 10 mA, R_sh = 1000 ohm.

| R_L | I_L = 10 mA * 1000 / (1000 + R_L) |
|---|---|
| 1 ohm | 9.99 mA |
| 100 ohm | 9.09 mA |
| 1000 ohm | 5.00 mA |
| 10 000 ohm | 0.91 mA |

Small loads get almost all the current, just like the ideal source. Big loads get less, because more of the current prefers the inside path. And when the load is removed (open circuit), all 10 mA flows through R_sh, making 10 mA * 1000 ohm = 10 V. Finite again. Fixed.

### Two models, one behaviour

Here is a surprise. A 9 V source with 2 ohm in series and a 4.5 A source with 2 ohm in parallel are indistinguishable from the outside.

```
  series model            parallel model
  (+) 9 V                 ( ^ ) 4.5 A  [2 ohm]
   |                        |            |
  [2 ohm]                   +------+-----+
   |                               |
   o out                           o out
```

Check with an open circuit: the series model gives 9 V. The parallel model sends all 4.5 A through 2 ohm, giving 4.5 * 2 = 9 V. Same.

Check with a short: the series model gives 9 / 2 = 4.5 A. The parallel model sends all 4.5 A through the short (the short has zero resistance, so the 2 ohm gets nothing). Same.

Check with 10 ohm: series gives 7.5 V (computed above). Parallel: the 4.5 A splits; the load gets 4.5 * 2 / 12 = 0.75 A, and 0.75 * 10 = 7.5 V. Same.

This is the Thevenin/Norton equivalence you met in Phase 05, seen from the source's point of view. The rule: a voltage source E with series r is equivalent to a current source E / r with the same r in parallel. Engineers choose whichever model makes the arithmetic easier. When r is small compared to the loads you use, the series (voltage) model feels natural: the voltage barely changes. When r is huge compared to the loads, the parallel (current) model feels natural: the current barely changes.

### When is "ideal" good enough?

A rule of thumb that will serve you for the whole course:

- A voltage source looks ideal when the load resistance is much bigger than its internal resistance. With r = 2 ohm and R_L = 1000 ohm, you lose 2 / 1002 = 0.2 % of the voltage. Nobody cares.
- A current source looks ideal when the load resistance is much smaller than its shunt resistance. With R_sh = 1 Mohm and R_L = 1 kohm, you lose 0.1 % of the current.

"Much bigger" usually means at least 10 times; for precise work, 100 times or more.

## Build It

The script `code/main.py` builds each model in our simulator and sweeps the load.

### Step 1: The ideal voltage source

A circuit with only a source and a load. We ask the simulator for the DC operating point (the steady values once everything settles) and read the node voltage and the resistor current.

```python
def ideal_voltage_source(volts, load_ohms):
    c = Circuit()
    c.voltage_source("V1", "out", "0", volts)
    c.resistor("RL", "out", "0", load_ohms)
    r = c.dc()
    return r.v("out"), r.i("RL")
```

The output shows 9.000 V on every line while the current climbs to 9 A at 1 ohm.

### Step 2: The real voltage source

We add the internal resistor between an inner node "emf" and the outer terminal "out". The load only sees "out".

```python
def real_voltage_source(volts, internal_ohms, load_ohms):
    c = Circuit()
    c.voltage_source("V1", "emf", "0", volts)
    c.resistor("Rint", "emf", "out", internal_ohms)
    c.resistor("RL", "out", "0", load_ohms)
    r = c.dc()
    return r.v("out"), r.i("RL")
```

Output (abridged):

```
    load (ohm)  V out (V)      I (A)  lost inside (V)
         10000      8.998     0.0009            0.002
            10      7.500     0.7500            1.500
             2      4.500     2.2500            4.500
             1      3.000     3.0000            6.000
```

Look at the 2 ohm line: when the load equals the internal resistance, exactly half the EMF is lost inside. Keep that in mind for Phase 05 Lesson 07 (maximum power transfer).

### Step 3 and Step 4: Current sources

`c.current_source("I1", "0", "out", amps)` pushes current from node "0" through the source into node "out", so it flows out into the load. The real version adds `Rsh` from "out" to ground.

```python
def real_current_source(amps, shunt_ohms, load_ohms):
    c = Circuit()
    c.current_source("I1", "0", "out", amps)
    c.resistor("Rsh", "out", "0", shunt_ohms)
    c.resistor("RL", "out", "0", load_ohms)
    r = c.dc()
    return r.v("out"), r.i("RL")
```

The ideal one prints 100 V across 10 kohm. The real one prints 0.909 mA into 10 kohm, with 9.091 mA "leaking" through the 1 kohm shunt.

### Step 5: Prove the equivalence

We build the series model (9 V, 2 ohm) and the parallel model (4.5 A, 2 ohm) and feed both the same loads. The two columns match to every printed digit.

### Step 6: Draw the output lines

The script sweeps the load from 0.1 ohm to 10 kohm and plots terminal voltage against current. The ideal source is a flat line; the real one is a line falling from 9 V to the short-circuit current of 4.5 A. The plot is saved as `out.png` next to the script.

Run it:

```bash
uv run python phases/06-sources-batteries-and-measurement/01-ideal-and-real-sources/code/main.py
```

## Use It

- **AA alkaline cell.** EMF about 1.5 V fresh; internal resistance roughly 0.1 to 0.3 ohm when new, rising as it is used. That is fine for a TV remote (milliamperes) and poor for a digital camera flash (amperes).
- **CR2032 coin cell.** 3 V, but internal resistance of 10 to 30 ohm or more. Draw 20 mA and you already lose a few tenths of a volt. That is why coin-cell devices sip current in short bursts.
- **Car battery.** 12.6 V with only a few milliohms inside, so it can deliver hundreds of amperes to the starter motor. Even so, the lights dim while cranking: 200 A * 0.01 ohm = 2 V lost inside.
- **USB port.** Specified around 5 V. A long thin cable adds its own series resistance, so a phone may see 4.6 V at the far end when charging hard.
- **Bench power supply.** Its internal resistance is made tiny electronically (milliohms), so it behaves like an ideal voltage source up to its current limit (Lesson 07).
- **Solar cell and LED driver.** Both behave like current sources over their working range: the solar cell because of light, the LED driver because a circuit inside actively holds the current fixed.
- **Simulators.** SPICE and our own `sim` only contain ideal sources. To model a real one you add the resistor yourself, exactly as in this lesson.

## Try It in the Lab

Open the lab task for this lesson. A small lab current source is set to 10 mA, but it has a 1 kohm resistance inside, in parallel. You must choose the load resistor so that at least 9 mA really reaches it and at least half a volt appears across it.

Things to think about before you press RUN:

- Which way does making the load bigger push each goal?
- How much of the current goes through the inside path for each candidate? Use the current-divider rule.
- Is there a window of resistances that satisfies both goals? Find its edges on paper first.

## Common Mistakes

- **Thinking a battery "contains" a fixed current.** A battery is close to a voltage source. The current is set by the load. A 9 V battery does not "give 1 A"; it gives whatever the load and its insides allow.
- **Measuring battery health with no load.** The open-circuit voltage barely changes as a battery ages, because no current flows through the growing internal resistance. Test under load.
- **Putting the internal resistor in the wrong place.** For a voltage source it goes in series. For a current source it goes in parallel. Swapping them gives a model that does not even have finite short-circuit current or open-circuit voltage.
- **Leaving a current source open.** In simulation an ideal current source with nowhere to go produces an error or an absurd voltage. In real life it produces the highest voltage the device can make, which can damage things.
- **Shorting a voltage source "because it has internal resistance".** Internal resistance limits the current, but all the power is then dumped inside the source. Lithium cells can catch fire this way.
- **Forgetting the source when calculating.** If a lamp's resistance is close to the source's internal resistance, ignoring r gives a big error.

## Exercises

1. A source has EMF 6 V and internal resistance 0.5 ohm. Find the current and terminal voltage with a 5.5 ohm load.
2. The same source is shorted. What current flows, and how much power turns into heat inside it?
3. A battery reads 1.58 V with no load and 1.40 V while delivering 0.6 A. What is its internal resistance? (Hint: the missing voltage is lost inside.)
4. Convert a 12 V source with 3 ohm internal resistance into its current-source model. Check both models with a 6 ohm load.
5. A current source of 2 mA has a 50 kohm shunt. Up to what load resistance does at least 1.9 mA reach the load? What voltage appears across that load?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Ideal voltage source | "A battery" | A perfect model that holds an exact voltage at any current, which no real part can do |
| Ideal current source | "A constant-current thing" | A perfect model that holds an exact current at any voltage |
| Internal resistance | "The battery is weak" | The resistance inside the source that the source's own current must pass through |
| EMF | "The battery voltage" | The voltage the source generates before internal losses; equal to the open-circuit voltage |
| Terminal voltage | "What the meter says" | EMF minus the drop on the internal resistance, at the current actually flowing |
| Short-circuit current | "What it gives if you short it" | E / r, the largest current the model can deliver |
| Source transformation | "Thevenin to Norton" | Swapping E with series r for E / r with parallel r; identical from the outside |

## Further Reading

- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 1.2 (voltage and current sources, Thevenin equivalent): a clear practical take on why "stiff" sources matter.
- All About Circuits, *Lessons in Electric Circuits*, Volume I (DC), chapter "Network Theorems" (Thevenin, Norton and source transformation): https://www.allaboutcircuits.com/textbook/direct-current/chpt-10/thevenins-theorem/
- MIT OpenCourseWare 6.002 *Circuits and Electronics* (Anant Agarwal), lectures on network theorems and the source models: https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/
- Energizer E91 (AA alkaline) product datasheet, for real internal-resistance and capacity numbers: https://data.energizer.com/pdfs/e91.pdf
