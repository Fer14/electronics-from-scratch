# Storing Charge

> A capacitor is two conductors that are not allowed to touch. Push charge onto one, and the other gives up the same amount.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 01 (The Physics Underneath), Phase 03 (Resistance and Ohm's Law), Phase 04 (Kirchhoff's Laws), Phase 05 (Circuit Analysis and Our Simulator)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Capacitor | A part made of two conductors separated by an insulator, able to hold separated charge | Two metal plates facing each other with a sheet of plastic between them |
| Plate | One of the two conductors of a capacitor | One slice of bread in a sandwich |
| Dielectric | The insulator between the plates | The filling of the sandwich, which no electron can cross |
| Charge (Q) | An amount of electric charge, measured in coulombs (C) | A count of how many electrons were moved, written in big bundles |
| Coulomb (C) | The unit of charge: about 6.24 x 10^18 electrons' worth | A "dozen", but a ridiculously large one |
| Charging | Moving charge from one plate to the other through the outside circuit | Pumping air from one balloon into another |
| Discharging | Letting that charge flow back | Letting the balloons equalize again |
| Transient | The part of a circuit's life when things are still changing | The seconds after you open a tap, before the flow settles |
| Steady state | What the circuit settles into when nothing changes any more | The flow once the bucket is full and the tap is closed |
| Microfarad (uF) | A millionth of a farad, the common size of capacitors | The "gram" of capacitance; farads are rarely used whole |

## Learning Objectives

- Describe what physically happens inside a capacitor while it charges: which electrons move, where they go, and why the insulator never conducts.
- Explain why current flows "through" a capacitor only while its voltage is changing, and why it stops when the capacitor is full.
- Compute the charge on a capacitor from its capacitance and voltage, and convert that charge to a number of electrons.
- Use our simulator's `transient()` analysis to watch a capacitor charge and to add up the charge that moved.
- Explain why a charged capacitor keeps its voltage after you disconnect it, and what makes it slowly lose it.

## The Problem

Everything you have analyzed so far had no memory. A resistor's current depends only on the voltage across it right now. Change the battery and every current in a resistor network changes instantly. Unplug the battery and everything drops to zero at once.

Real electronics needs memory. Your phone's camera flash charges for a second, then dumps that energy in a millisecond. A power supply has to keep the voltage steady during the tiny gaps between the bumps of rectified mains. A microcontroller needs its reset line held low for a few milliseconds after power-up. A computer's memory chip stores a 1 or a 0 as a tiny bit of charge that must still be there a few milliseconds later. All of these use the same part: the **capacitor**.

In this lesson you will open one up (in your mind), see what is moving, and then watch our simulator charge one, step by step. You will add up the current flowing into it and discover a very simple rule hiding in the numbers.

## The Physics

### Two plates and a gap

Take two flat sheets of metal. Put them face to face, very close, but with a thin sheet of plastic between them so they never touch. That is a capacitor. The metal sheets are the **plates**; the plastic is the **dielectric** (an insulator: a material whose electrons are tightly bound to their atoms and cannot wander, as you saw in Phase 01).

```
        wire                      wire
         |                         |
         |   +-----+   +-----+     |
         +---|plate|   |plate|-----+
             |  A  | ? |  B  |
             +-----+   +-----+
                   ^
          insulator (dielectric): nothing can cross
```

Each metal plate is full of free electrons, the same free electrons that carry current in a wire. Right now each plate is neutral: it has exactly as many electrons as it has positive protons, so the charges cancel.

### Connect a battery

Now connect plate A to the + terminal of a 9 V battery and plate B to the - terminal, with a resistor in the wire to keep things slow.

```
        +9V ----[ R ]----+
                         |
                       =====   plate A  (top)
                       =====   plate B  (bottom)
                         |
        0V  -------------+
```

Remember from Phase 01 what a battery does: it is a charge pump. It pulls electrons in at its + terminal and pushes them out at its - terminal, giving each one energy.

So the battery starts **pulling free electrons out of plate A** (through the resistor) and **pushing the same number of electrons into plate B**. No electron crosses the gap. The electrons that land on plate B came from the battery; the electrons leaving plate A go into the battery. The battery is the only path.

After a while:

- Plate A is missing some electrons: it has a net **positive** charge, +Q.
- Plate B has extra electrons: a net **negative** charge, -Q.
- The two charges are exactly equal and opposite. The capacitor as a whole is still neutral. It does not "store charge" in the sense of holding extra electrons; it stores **separated** charge.

### Why it slows down and stops

Each extra electron on plate B is repelled by the electrons already there and pulled back toward the positive plate A across the gap. As more charge piles up, a voltage builds between the plates (Phase 01: voltage is energy per unit charge; it takes energy to push one more electron onto an already crowded negative plate). This voltage opposes the battery.

At the start, the capacitor has 0 V across it, so the full 9 V of the battery sits across the resistor and a large current flows: I = 9 V / R. As the capacitor fills, its voltage rises, the resistor sees less and less voltage, and the current shrinks. When the capacitor reaches 9 V, the resistor sees 0 V and the current is zero. The capacitor is "full" **for that voltage**.

### The water picture, and where it breaks

Think of a tank divided in two by a rubber membrane, with pipes on both sides. A pump pushes water into one side; the membrane stretches; exactly as much water leaves the other side as enters this one. Water never crosses the membrane, yet water moves in both pipes. As the membrane stretches it pushes back harder until the pump cannot push more. That is a capacitor: a stretched membrane holding separated "water".

What the picture gets wrong: real charge does not pile up "on the side" of a balloon in any visible way. The excess electrons sit in a microscopically thin layer on the plate surfaces facing each other, and what really stores the energy is the **electric field** in the gap (Lesson 06). Also, a membrane has a natural length; a capacitor has no preferred state other than 0 V.

### Current "through" a capacitor

Here is the most surprising fact of the lesson. If you put an ammeter in the top wire and another in the bottom wire, they show the **same** current at every instant: electrons leave plate A at the same rate as they arrive at plate B. From outside, the capacitor looks like something current flows through, even though no electron crosses the insulator. Kirchhoff's current law (Phase 04) still holds for the capacitor as a whole box: what goes in one lead comes out the other.

But this "current through" only exists **while the charge is changing**. A capacitor at a steady voltage passes no current at all. That is why people say a capacitor **blocks DC** (steady current) but lets changes through.

## The Concept

### Charge, measured in coulombs

We count moved charge in **coulombs** (symbol C, careful: the same letter we will use for capacitance; context tells you which). One coulomb is the charge of about 6.24 x 10^18 electrons. One ampere of current means one coulomb passing per second:

> Current is how many coulombs pass each second.

    I = Q / t        (for a steady current)

So a current of 9 mA (0.009 A) flowing for 0.1 s moves Q = 0.009 x 0.1 = 0.0009 C = 900 uC (microcoulombs).

When the current changes over time, we add up tiny slices: in each tiny time slice dt the current I moves charge I x dt. Adding all those slices is what the code does in `charge_moved`, and it is the area under the current-versus-time curve.

### The rule hiding in the numbers

Measure two things at many moments while the capacitor charges: the total charge Q that has moved so far, and the voltage V across the capacitor. Divide them. You will find (and the code shows) that **Q / V is the same number at every moment**. For a given capacitor, charge and voltage are proportional:

> The charge on a capacitor equals its capacitance times the voltage across it.

    Q = C x V

C here is the **capacitance**, measured in **farads** (F). One farad means one coulomb per volt. A 100 uF capacitor at 9 V holds

    Q = 100 x 10^-6 F x 9 V = 900 x 10^-6 C = 900 uC

on its positive plate (and -900 uC on the other). Lesson 02 is entirely about where C comes from.

### How many electrons is that?

Divide by the charge of one electron, 1.602 x 10^-19 C:

    900 x 10^-6 / 1.602 x 10^-19 = 5.6 x 10^15 electrons

Five and a half thousand million million electrons moved from one plate to the other. That sounds huge, but a cubic millimetre of copper has around 8 x 10^19 free electrons, so the plates barely notice. The extra charge is a tiny ripple on a sea.

### What happens when you disconnect it

Remove the battery. The extra electrons on plate B want to go back to plate A, but the only way is through the outside circuit, and there is no outside circuit any more. So they stay. The capacitor keeps its 9 V. That is the "memory".

If you now touch a voltmeter to it, the voltmeter itself is a path (a very large resistor, typically 10 MOhm). A small current flows through it, and the charge slowly drains. With 100 uF and 10 MOhm the voltage falls so slowly that after 10 s you still read 8.91 V. If instead you touch the two leads with a wire, the charge rushes back in a spark. Large capacitors can stay dangerously charged for minutes after a device is unplugged, which is why Phase 00's safety lesson tells you to discharge them through a resistor first.

### A worked example by hand

A 47 uF capacitor is charged to 12 V.

1. Charge: Q = C x V = 47 x 10^-6 x 12 = 564 x 10^-6 C = 564 uC.
2. If you discharge it with a steady 2 mA, how long does it last? t = Q / I = 564 x 10^-6 / 0.002 = 0.282 s.
3. Electrons moved: 564 x 10^-6 / 1.602 x 10^-19 = 3.5 x 10^15.

### Thinking with KCL: current in, current out

Draw a dashed box around the capacitor. Kirchhoff's current law (Phase 04) says that whatever current enters a box must leave it, because charge cannot pile up in the box as a whole. Does the capacitor break this rule, since charge piles up on plate A?

No. Charge piles up on plate A (+Q) but an equal negative charge piles up on plate B (-Q), so the **total** charge inside the box stays zero. At every instant the current entering through the top lead equals the current leaving through the bottom lead. KCL is safe, and so are all the analysis methods of Phase 05. What is new is only the relation between that current and the voltage, which is no longer Ohm's law.

```
          i  ->            i  ->
   o--------[ + | - ]--------o
            plate A  plate B
         (gains +Q)  (gains -Q)
   same current in both leads, total charge in the box: zero
```

### A second worked example: a 1000 uF capacitor and a motor

A small toy motor needs 0.5 A for a moment when it starts. A 1000 uF capacitor charged to 6 V sits next to it.

1. Stored charge: Q = 1000 x 10^-6 x 6 = 6 x 10^-3 C = 6 mC.
2. If the motor took a steady 0.5 A from the capacitor alone, the charge would last t = Q / I = 0.006 / 0.5 = 12 ms.
3. In practice the voltage falls as the charge leaves (V = Q / C), so long before 12 ms the voltage is too low for the motor. If the motor stops working below 4.5 V, the usable charge is only the part between 6 V and 4.5 V: 1000 uF x 1.5 V = 1.5 mC, which lasts 1.5 mC / 0.5 A = 3 ms.

That is the typical job of a capacitor in a power circuit: not to run the motor, but to cover the first few milliseconds of a sudden demand while the battery and wires catch up.

## Build It

The full script is `code/main.py`. Run it from the repository root:

```bash
uv run python phases/07-capacitors/01-storing-charge/code/main.py
```

### Step 1: The charging circuit

We describe a battery, a 1 kOhm resistor and a 100 uF capacitor with our simulator. `v0=0.0` says the capacitor starts empty.

```python
def build_charging_circuit():
    circuit = Circuit()
    circuit.voltage_source("B1", "plus", "0", BATTERY_VOLTS)
    circuit.resistor("R1", "plus", "top", RESISTOR_OHMS)
    circuit.capacitor("C1", "top", "0", CAPACITOR_FARADS, v0=0.0)
    return circuit
```

```
   plus o----[ R1 1k ]----o top
        |                 |
     B1 9V              C1 100uF
        |                 |
        +--------o--------+
                 0
```

Until now you used `dc()`, which finds the one settled state of a circuit. With a capacitor the circuit has a history, so we use `transient(t_stop, dt)`: the simulator steps through time, `dt` seconds at a time, up to `t_stop`. (You will build exactly this kind of time-stepper yourself in Lesson 08.)

### Step 2: Add up the charge

The resistor carries the same current that flows onto the capacitor's top plate. We add up current x time slice by slice (the trapezoid rule: the average of the current at the two ends of each slice, times the slice width).

```python
def charge_moved(time, current):
    steps = np.diff(time)
    return np.concatenate([[0.0], np.cumsum(steps * (current[1:] + current[:-1]) / 2)])
```

### Step 3: Compare charge and voltage

At several moments the script prints the current, the charge moved so far, the capacitor voltage and the ratio Q / V:

```
Charging a 100 uF capacitor from a 9 V battery through 1 kOhm
 time (ms)  current (mA)  charge moved (uC)  cap voltage (V)  Q / V (uF)
         1         8.910                9.0            0.090      100.01
        50         5.459              354.1            3.541      100.00
       100         3.311              568.9            5.689      100.00
       200         1.218              778.2            7.782      100.00
       300         0.448              855.2            8.552      100.00
       500         0.061              893.9            8.939      100.00
Total charge pushed onto the top plate: 897.8 uC
Charge a full 9 V needs on 100 uF:      900.0 uC
```

Read the table row by row:

- The current starts at 9 V / 1000 Ohm = 9 mA and keeps falling.
- The charge keeps rising, but more and more slowly.
- The ratio Q / V is 100 uF in every row (the 100.01 in the first row is rounding in our charge adding, which uses 0.1 ms slices). That is the capacitance, found by experiment.
- After half a second the capacitor holds almost all of the 900 uC that Q = C x V predicts for 9 V.

### Step 4: Disconnect and watch it hold

A second circuit has only the charged capacitor (`v0=9.0`) and a 10 MOhm resistor standing in for a voltmeter:

```python
circuit = Circuit()
circuit.capacitor("C1", "top", "0", CAPACITOR_FARADS, v0=BATTERY_VOLTS)
circuit.resistor("Rmeter", "top", "0", 10e6)
result = circuit.transient(t_stop=10.0, dt=1e-2)
```

```
Battery removed: the charged capacitor watched by a 10 MOhm voltmeter
  after    0 s the capacitor still shows 9.000 V
  after    1 s the capacitor still shows 8.991 V
  after    5 s the capacitor still shows 8.955 V
  after   10 s the capacitor still shows 8.910 V
```

The capacitor remembers. It forgets slowly, and how slowly depends on R x C, a number you will meet properly in Lesson 04.

### Step 5: Count electrons

```
900 uC is 5.62e+15 electrons moved from one plate to the other
```

## Use It

- **Camera flash.** A small flash charges a capacitor of around 100-200 uF to about 300 V for a second or two, then empties it into a xenon tube in about a millisecond. The battery could never deliver that burst directly; the capacitor stores it and releases it fast.
- **Power-supply smoothing.** Almost every board has electrolytic capacitors (tens to thousands of microfarads) right after the rectifier and small 100 nF ceramic capacitors next to every chip. They hold charge so the voltage does not dip when the chip suddenly draws a burst of current.
- **DRAM memory.** Each bit of your computer's RAM is a capacitor of a few tens of femtofarads (10^-15 F). A "1" is a few femtocoulombs of charge. It leaks away in milliseconds, which is why the memory controller rewrites (refreshes) every row roughly every 64 ms.
- **Touch screens.** Your finger changes how much charge a grid of tiny electrode pairs can hold. The phone measures that change in charge to find where you touched.
- **Datasheets.** Look at any capacitor datasheet (for example a Panasonic FR-series aluminium electrolytic or a Murata GRM ceramic) and the first two numbers are capacitance and rated voltage: how much charge per volt, and how many volts before the dielectric fails.

## Common Mistakes

- **"Current flows through the capacitor."** No electron crosses the dielectric. Current flows **onto** one plate and **off** the other. From outside the effect is the same, which is why we can still use KCL, but the physics is a separation of charge.
- **"A capacitor stores charge like a battery stores charge."** The capacitor's total charge is zero (+Q and -Q). What it stores is **energy**, in the field between separated charges. A battery stores energy in chemicals and makes the separation continuously.
- **Expecting a steady current into a charged capacitor.** Once its voltage equals the source, current is zero. A capacitor in a DC circuit, after the transient, is an open circuit.
- **Using `dc()` and expecting to see the charging.** `dc()` jumps straight to the end: the capacitor is open, and its voltage is whatever the rest of the circuit sets. To see the history you need `transient()`.
- **Thinking an unplugged device is safe.** Big capacitors can hold a lethal charge long after unplugging. Always discharge them through a resistor and check with a meter.
- **Mixing the two C's.** C (italic, the quantity) is capacitance in farads; C (the unit) is coulombs. Q = C x V uses the first.

## Exercises

1. A 220 uF capacitor is charged to 5 V. How much charge sits on its positive plate? How many electrons is that?
2. A 10 uF capacitor holds 150 uC. What is the voltage across it?
3. You charge a capacitor with a steady 2 mA for 30 ms and its voltage rises from 0 to 6 V. What is its capacitance?
4. In the code, change the resistor to 4.7 kOhm. Before running: what is the starting current? Will the capacitor be as full at 500 ms as before? Run it and check, and check that Q / V is still 100 uF.
5. A DRAM cell of 25 fF stores a "1" as 1.0 V. How many electrons is that? If it leaks 0.1 fA (10^-16 A), how long until it has lost 20% of its charge? (Hint: t = Q / I.)

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Capacitor | "It stores charge" | It stores separated charge, +Q on one plate and -Q on the other, and the energy of the field between them |
| Charge Q | "The capacitor is full" | Q = C x V; it is "full" only for a given voltage, and more voltage pushes more charge on (up to its rating) |
| Current through a capacitor | "DC goes through it" | Only changing voltage drives current onto and off its plates; steady DC sees an open circuit |
| Dielectric | "The plastic in the middle" | The insulator between the plates; it sets how much charge fits per volt and how many volts it can take |
| Transient | "The start-up part" | The period while voltages and currents change before reaching steady state |
| Discharging | "It empties" | The separated charge flows back through an outside path until both plates are neutral |

## Further Reading

- [All About Circuits, Vol. I, Chapter 13: Capacitors](https://www.allaboutcircuits.com/textbook/direct-current/chpt-13/electric-fields-capacitance/) - a gentle, well-illustrated introduction to electric fields and capacitance.
- *The Art of Electronics*, 3rd ed., Horowitz & Hill, Section 1.4 (Capacitors and AC circuits) - the classic practical treatment.
- *Practical Electronics for Inventors*, 4th ed., Scherz & Monk, the section on capacitors - many real-part photos and applications.
- [The Feynman Lectures on Physics, Vol. II, Chapter 6 (The Electric Field in Various Circumstances) and Chapter 8 (Electrostatic Energy)](https://www.feynmanlectures.caltech.edu/II_toc.html) - the physics of charges on conductors, for the curious.
