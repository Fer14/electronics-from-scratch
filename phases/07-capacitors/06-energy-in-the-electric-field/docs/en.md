# Energy in the Electric Field

> A capacitor stores energy, not charge: E = 1/2 x C x V^2. Charging it from a fixed voltage through any resistor always wastes the other half.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 01 Lesson 07 (Energy and Power), Phase 03 Lesson 05 (Power and Heat), Phase 07 Lessons 01-04
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Energy (E) | The ability to do work, measured in joules (J) | The effort stored in a stretched spring |
| Joule (J) | The unit of energy: one watt for one second | Lifting a small apple (100 g) by one metre |
| Power (P) | How fast energy moves, in watts (W): joules per second | How fast you pour water, not how much |
| Electric field energy | Energy stored in the space between separated charges | Tension stored in a stretched rubber sheet |
| Energy density | Energy per unit volume or mass | How much "fuel" fits in a given tank |
| Hold-up time | How long a capacitor keeps a circuit powered after the supply fails | Coasting on a bicycle after you stop pedalling |
| Efficiency | Useful energy out divided by energy in, as a percentage | How much of the petrol actually moves the car |
| Supercapacitor | A capacitor with huge capacitance (farads to thousands of farads) but low voltage | A wide, shallow reservoir |

## Learning Objectives

- Derive E = 1/2 x C x V^2 from the work needed to move charge onto a capacitor.
- Explain where the energy lives (in the electric field of the dielectric) and why it grows with the square of the voltage.
- Compute the energy stored in real capacitors, from decoupling chips to camera flashes and supercapacitors, and compare with a battery.
- Prove with the simulator that charging from a fixed voltage through a resistor wastes exactly half the energy, whatever the resistor.
- Design a hold-up capacitor for a circuit that must survive a power cut.

## The Problem

A data logger must save its last readings when the battery is pulled out. That takes 10 ms. How big a capacitor do you need to keep it alive? Or: a camera flash needs a few joules in a millisecond; a phone battery holds tens of thousands of joules; why doesn't the flash just run from the battery? And why is a big electrolytic capacitor in a power supply dangerous even after unplugging?

All three questions are about energy, not charge. To answer them you need the energy formula for a capacitor and a feel for its size compared to batteries. You will also meet a surprising fact that matters in every switching circuit: charging a capacitor from a fixed voltage loses half the energy along the way, no matter how good your wires are.

## The Physics

### Work to move charge

Voltage is energy per unit charge (Phase 01 Lesson 04): moving a small charge q across a voltage v takes energy q x v.

Charging a capacitor means moving charge from one plate to the other, a little at a time. But the voltage is not fixed while you do it: the first coulomb moves across 0 V (free), and the last coulomb moves across almost the full final voltage V (expensive). Because v = q / C grows in a straight line with the charge moved, the **average** voltage during the whole process is half the final voltage, V / 2.

```
 voltage
   V |                    /
     |                  / |
     |                /   |       the energy is the area under this line:
     |              /     |       a triangle of base Q and height V
     |            /       |
     |          /         |       E = 1/2 x Q x V
     |        /           |
     |      /             |
     |    /               |
     |  /                 |
     |/___________________|______ charge moved
     0                    Q
```

So the total work is (total charge) x (average voltage):

    E = Q x V / 2

Substituting Q = C x V:

> The energy stored in a capacitor is half its capacitance times the square of its voltage.

    E = 1/2 x C x V^2        (joules, with C in farads and V in volts)

Equivalent forms: E = 1/2 x Q x V = Q^2 / (2C).

### Why the square

Double the voltage and you move twice as much charge, and each bit of charge is moved across a voltage that is, on average, twice as large. Twice times twice: four times the energy. This is why high-voltage capacitors are so much more energetic (and dangerous) than low-voltage ones of the same capacitance.

### Where the energy lives

The energy is not "in the electrons" on the plates. It is stored in the **electric field** between them, in the strained, polarized dielectric (Lesson 02). Physics gives an energy per cubic metre of field of 1/2 x eps0 x eps_r x E_field^2. Multiply by the volume between the plates (A x d) and use E_field = V / d and C = eps0 eps_r A / d, and you get back exactly 1/2 C V^2. This field picture becomes important when you study how energy flows through circuits and radio waves; for now, think of the dielectric as a stretched spring.

The water picture: a tank that you fill from the bottom. The first litre is easy to push in; the last litre has to be pushed against the full height of the water. The stored energy is half of "total water times final height", for the same triangle reason. What the analogy hides: water's energy is gravitational and depends on the tank shape; a capacitor's depends only on C and V.

### Charging from a fixed voltage wastes half

Charge a capacitor from a battery of voltage V. When it is full it holds Q = C x V. The battery pushed every one of those coulombs out at its full voltage V, so the battery delivered

    E_battery = Q x V = C x V^2

but the capacitor holds only 1/2 x C x V^2. The other half, 1/2 x C x V^2, turned into heat in the resistor (and in wires and the battery's internal resistance). The striking part: **the loss does not depend on R.** A smaller resistor gives a bigger current for a shorter time; the heat I^2 x R x t comes out the same. Even with a "zero" resistance, the energy would be lost in sparks and radiation.

The only ways to avoid this loss are to charge with a voltage that **rises gradually** along with the capacitor (so the resistor never sees much voltage), or to use an inductor (Phase 08), which is how switching power supplies get high efficiency.

## The Concept

### Worked example 1: a few sizes

| Capacitor | Calculation | Energy |
|---|---|---|
| 100 nF decoupling chip at 3.3 V | 0.5 x 100e-9 x 3.3^2 | 0.54 uJ |
| 100 uF at 9 V | 0.5 x 100e-6 x 81 | 4.05 mJ |
| 100 uF at 18 V | 0.5 x 100e-6 x 324 | 16.2 mJ (four times more) |
| 120 uF flash capacitor at 330 V | 0.5 x 120e-6 x 108,900 | 6.53 J |
| 10 F supercapacitor at 2.7 V | 0.5 x 10 x 7.29 | 36.5 J |
| An AA alkaline cell (for comparison) | about 2.5 Ah x 1.2 V x 3600 s/h | about 10,800 J |

Even a supercapacitor holds hundreds of times less energy than a single AA cell of similar size. Capacitors are not good at storing **lots** of energy. They are good at **releasing it fast**: a flash capacitor can deliver its 6.5 J in a millisecond, which is 6500 W. A battery's internal chemistry and resistance cannot do that.

### Worked example 2: the usable part

A circuit works between 5 V and 3 V. A 220 uF capacitor at 5 V holds 0.5 x 220e-6 x 25 = 2.75 mJ. At 3 V it still holds 0.5 x 220e-6 x 9 = 0.99 mJ, which the circuit cannot use. The usable energy is

    E_usable = 1/2 x C x (V_start^2 - V_min^2) = 0.5 x 220e-6 x (25 - 9) = 1.76 mJ

So 36% of the stored energy is stranded below the circuit's minimum voltage. A voltage regulator that works from a lower input recovers more of it.

### Worked example 3: hold-up time

If the load draws a constant **power** P, the time is energy over power: t = E_usable / P. If the load behaves like a **resistor** R (more common for simple circuits), it is a discharge from Lesson 04:

    t = R x C x ln(V_start / V_min)

For 100 Ohm, 220 uF, 5 V down to 3 V: t = 100 x 220e-6 x ln(5/3) = 0.022 x 0.511 = 11.2 ms.

Check with energy: the 100 Ohm load draws 0.25 W at 5 V and 0.09 W at 3 V; a rough average of about 0.16 W over 11 ms is 1.76 mJ. The two views agree.

### Worked example 4: the danger

A 470 uF capacitor in a mains power supply is charged to 325 V (the peak of 230 V mains). E = 0.5 x 470e-6 x 325^2 = 24.8 J. Delivered through a hand, that is far more than enough to injure or kill. This is the reason for bleeder resistors and the safety rules of Phase 00.

### Worked example 5: charging in steps loses less

The "half is lost" rule applies to charging from a **fixed** voltage. Charge instead in two steps: first from a 4.5 V source to 4.5 V, then from a 9 V source to 9 V.

1. Step 1: the source gives Q1 x 4.5 V with Q1 = C x 4.5. Heat = half of the energy given = 1/2 x C x 4.5^2.
2. Step 2: the capacitor goes from 4.5 V to 9 V, so the resistor starts with 4.5 V across it, the same as step 1. Same shape, same heat: 1/2 x C x 4.5^2.
3. Total heat: C x 4.5^2 = C x 20.25. Single step: 1/2 x C x 9^2 = C x 40.5. Two steps lose exactly half as much.

With n equal steps the loss is 1/n of the single-step loss. In the limit of a smoothly rising source the loss tends to zero. "Adiabatic" logic circuits and some LED and display drivers use this idea; switching power supplies achieve a similar effect with inductors.

### Energy in watts and milliseconds

It helps to turn joules into "watts for how long" (1 J = 1 W for 1 s = 1000 W for 1 ms):

| Energy | Could power... |
|---|---|
| 0.54 uJ (100 nF at 3.3 V) | a 10 mW microcontroller for 54 us |
| 4 mJ (100 uF at 9 V) | a 20 mA LED (about 40 mW) for 0.1 s |
| 6.5 J (camera flash) | 6500 W for 1 ms, the flash tube's burst |
| 36 J (10 F supercapacitor) | a 1 mW real-time clock for 10 hours |

### Worked example 6: energy in the field, not the plates

Check the field picture with numbers. Take the 10 cm x 10 cm air capacitor of Lesson 02 (88.5 pF, 1 mm gap) at 1000 V.

1. Energy from the circuit formula: E = 1/2 x 88.5 x 10^-12 x 1000^2 = 44.3 uJ.
2. Field in the gap: E_field = V / d = 1000 / 0.001 = 10^6 V/m.
3. Energy per cubic metre of field: 1/2 x eps0 x E_field^2 = 0.5 x 8.854 x 10^-12 x 10^12 = 4.43 J/m^3.
4. Volume of the gap: 0.01 m^2 x 0.001 m = 10^-5 m^3.
5. Energy in the field: 4.43 x 10^-5 J = 44.3 uJ. The same number, computed only from the field in the empty space between the plates.

Note the field of 1 million volts per metre: about a third of the way to the breakdown of air. Energy density is limited by breakdown, which is why capacitors store so much less energy per volume than batteries.

### Battery and capacitor side by side

| Property | Capacitor | Battery |
|---|---|---|
| How it stores energy | Electric field between separated charges | Chemical reactions |
| Voltage as it empties | Falls steadily (V = Q / C) | Stays fairly flat, then drops near the end |
| Energy per volume | Low (supercapacitors: a few Wh per litre) | High (lithium-ion: hundreds of Wh per litre) |
| How fast it can deliver | Extremely fast, limited by ESR | Limited by chemistry and internal resistance |
| Charge/discharge cycles | Millions | Hundreds to thousands |
| Losses when charged from a fixed voltage | Half, as heat in the resistance | Depends on chemistry, typically 5-20% |

The two are partners, not rivals: a battery holds the energy, a capacitor next to it delivers the sudden bursts.

## Build It

```bash
uv run python phases/07-capacitors/06-energy-in-the-electric-field/code/main.py
```

### Step 1: The formula

```python
def stored_energy(farads, volts):
    return 0.5 * farads * volts ** 2
```

```
Energy stored E = 1/2 * C * V^2
  100 uF at 9 V                           0.00405 J
  100 uF at 18 V (double voltage)          0.0162 J
  200 uF at 9 V (double capacitance)       0.0081 J
  camera flash, 120 uF at 330 V             6.534 J
  supercapacitor, 10 F at 2.7 V             36.45 J
  AA alkaline cell, 2.5 Ah at 1.2 V      1.08e+04 J
```

Doubling the voltage multiplies the energy by four; doubling the capacitance only by two.

### Step 2: Follow the energy during charging

We simulate a 9 V battery charging 100 uF through a resistor, and integrate three powers over time (power is volts times amps; energy is power added up over time):

- what the battery gives: 9 V x i
- what goes into the capacitor: v_cap x i
- what the resistor turns into heat: i^2 x R

```python
def charge_through(ohms):
    circuit = Circuit()
    circuit.voltage_source("B1", "plus", "0", SUPPLY_VOLTS)
    circuit.resistor("R1", "plus", "top", ohms)
    circuit.capacitor("C1", "top", "0", CAPACITOR_FARADS, v0=0.0)
    tau = ohms * CAPACITOR_FARADS
    result = circuit.transient(t_stop=12 * tau, dt=tau / 1000)
    time = np.asarray(result.time)
    current = np.asarray(result.i("R1"))
    cap_volts = np.asarray(result.v("top"))
    from_battery = integrate(time, SUPPLY_VOLTS * current)
    into_capacitor = integrate(time, cap_volts * current)
    in_resistor = integrate(time, current ** 2 * ohms)
    return from_battery, into_capacitor, in_resistor
```

We run each case for 12 tau, so the capacitor is charged to within 0.0006% of 9 V.

```
Charging 100 uF to 9 V through different resistors (simulated, energies in mJ)
 R (ohm)  battery gave  capacitor got  resistor heat  efficiency
      10         8.100          4.050          4.050       50.0%
    1000         8.100          4.050          4.050       50.0%
  100000         8.100          4.050          4.050       50.0%
Formula: battery gives C*V^2 = 8.100 mJ, capacitor keeps 1/2*C*V^2 = 4.050 mJ
```

A 10,000-to-1 range of resistors, and the split is always exactly half and half. Only the time changes (1 ms versus 10 s).

### Step 3: Hold-up

```python
def hold_up_time(farads, load_ohms, start_volts, minimum_volts):
    return load_ohms * farads * math.log(start_volts / minimum_volts)
```

And a simulation of the capacitor alone feeding the load, starting at 5 V:

```
Hold-up: a 220 uF capacitor keeps a 100 ohm load alive after the supply fails
  usable energy between 5 V and 3 V: 1.760 mJ
  formula: time to fall from 5 V to 3 V = R*C*ln(5/3) = 11.24 ms
  simulator: rail at 10 ms = 3.174 V, drops below 3 V at 11.24 ms
```

## Use It

- **Camera flashes and defibrillators.** Both charge a capacitor slowly from a battery and dump it fast. A medical defibrillator stores up to a few hundred joules in a capacitor of the order of 100 uF charged to well over a thousand volts.
- **Hold-up and "last gasp" circuits.** Smart meters, SSDs and car electronics keep a capacitor (or supercapacitor) charged so they can finish writing data after a power cut. SSD datasheets for enterprise drives mention "power-loss protection" built this way.
- **Supercapacitors.** Parts like the Eaton/Maxwell or Panasonic electric double-layer capacitors (1-3000 F at 2.7 V per cell) back up real-time clocks, buffer regenerative braking in buses and smooth bursts from small solar harvesters.
- **Switching losses.** Every time a transistor charges a capacitance (a MOSFET's gate, a cable, a chip's input) from a fixed supply, half of 1/2 C V^2 is burned. Processors burn power roughly as C x V^2 x f for this reason: billions of tiny capacitors charged and discharged every second. Lowering V is the most effective way to save energy, which is why chips run at about 1 V.
- **Safety.** Datasheets for big electrolytics and power-supply designs specify bleeder resistors to discharge stored energy within seconds after switch-off.

## Try It in the Lab

The lab "Ride through the power cut" gives you a 100 Ohm load and a pad for a pre-charged capacitor (5 V). The rail must still be at 3 V or more 10 ms after the supply disappears. Find the minimum capacitance first, with the discharge formula or with energy, then choose from the box. Why would a capacitor just below your minimum fail by a lot, not just a little?

## Common Mistakes

- **Forgetting the 1/2.** E = C x V^2 is what the battery gives; the capacitor keeps half of it.
- **Forgetting to square the voltage.** 100 uF at 330 V is not 3.3 times more energetic than at 100 V; it is about 11 times more.
- **Counting all stored energy as usable.** The load stops working at its minimum voltage; use V_start^2 - V_min^2.
- **Thinking a better (smaller) resistor reduces the charging loss.** It does not: the loss is 1/2 C V^2 for any resistance when charging from a fixed voltage.
- **Treating supercapacitors as batteries.** They store much less energy and their voltage falls steadily as they discharge, unlike a battery's fairly flat voltage.
- **Assuming a disconnected capacitor is harmless.** High-voltage capacitors can hold joules for minutes or longer.

## Exercises

1. How much energy does a 4700 uF capacitor store at 25 V? At 50 V?
2. A camera flash needs 5 J. What capacitance at 300 V? At 150 V?
3. A 1 F supercapacitor charged to 2.5 V powers a clock that works down to 1.5 V and draws a constant 10 uW. Ignoring leakage, how long does it run? (Use usable energy / power.)
4. Charging a 10 uF capacitor to 12 V through 1 kOhm: how much energy does the source deliver, how much ends in the capacitor, how much is heat? What changes with 10 Ohm?
5. Modify `charge_through` so the source is not a fixed battery but rises in two steps: first 4.5 V until the capacitor is nearly there, then 9 V. (Hint: use two runs, or a `pulse_source`.) Show that the loss in the resistor drops to about half of the single-step case. Why?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Stored energy | "How much charge it has" | E = 1/2 C V^2, energy held in the electric field of the dielectric |
| Charging loss | "Wire losses" | When charging from a fixed voltage, 1/2 C V^2 is always dissipated, independent of R |
| Usable energy | "The energy in the cap" | 1/2 C (V_start^2 - V_min^2): only the part above the load's minimum voltage |
| Hold-up time | "How long it lasts" | Time to fall from the starting voltage to the minimum the load accepts |
| Supercapacitor | "A capacitor battery" | Very high capacitance at low voltage per cell; high power, modest energy |
| Energy density | "How much it holds" | Energy per volume or mass; capacitors are far below batteries |

## Further Reading

- [The Feynman Lectures on Physics, Vol. II, Chapter 8: Electrostatic Energy](https://www.feynmanlectures.caltech.edu/II_08.html) - energy of a capacitor and energy in the field.
- [HyperPhysics: Capacitor energy](http://hyperphysics.phy-astr.gsu.edu/hbase/electric/capeng.html) - the triangle derivation and the field energy density.
- *The Art of Electronics*, 3rd ed., Horowitz & Hill, Section 1.4 (capacitors) and the chapter on power supplies for hold-up and bleeders.
- [Eaton supercapacitor product pages and application guides](https://www.eaton.com/us/en-us/products/electronic-components/supercapacitors.html) - real hold-up calculations with supercapacitors.
