# Zener Diodes

> Push a diode backwards hard enough and it suddenly gives way, at a voltage you can choose when it is made. A zener is a diode designed to give way gracefully, and that makes it a voltage reference.

**Type:** Build
**Prerequisites:** 11-03 (The pn Junction), 11-04 (The Diode Equation), 11-07 (LEDs); Phase 04 (Kirchhoff's Laws), lesson 05-the-voltage-divider
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Breakdown | The point where a reverse-biased junction suddenly starts conducting heavily | A dam that overflows once the water reaches its top |
| Breakdown voltage (V_Z) | The reverse voltage at which breakdown happens | The height of the dam wall |
| Zener diode | A diode designed to be used in reverse breakdown, with a precise, stable V_Z | A spillway built on purpose at an exact height |
| Zener effect (tunnelling) | Breakdown where electrons pass straight through a very thin depletion region, without climbing over | Walking through a wall so thin that, in the quantum world, you sometimes just appear on the other side |
| Avalanche | Breakdown where a fast electron knocks loose more electrons, which knock loose more | One falling rock that triggers a landslide |
| Voltage regulator | A circuit that keeps its output voltage nearly constant despite changes in input and load | A float valve that keeps a tank at the same level however much water flows in or out |
| Shunt regulator | A regulator that holds the voltage by diverting (shunting) extra current to ground | A spillway that dumps whatever water the town does not use |
| Series resistor (R_S) | The resistor between the input and the zener; it drops the excess voltage | A narrow pipe feeding the tank |
| Load regulation | How much the output changes when the load current changes | Does the tank level drop when the town opens more taps? |
| Line regulation | How much the output changes when the input voltage changes | Does the level change when the river feeding it rises? |
| Dynamic resistance (r_z) | The small resistance-like slope of the zener in breakdown: extra volts per extra amp | How much the overflow level rises when more water pours over the spillway |
| Knee current | The minimum current needed to keep the zener firmly in breakdown | The minimum flow that keeps the spillway actually spilling |
| Temperature coefficient | How V_Z changes with temperature | Whether the dam wall grows or shrinks in the heat |

## Learning Objectives

- Explain what happens physically when a junction breaks down, and the difference between Zener tunnelling and avalanche.
- Read a zener's reverse I-V curve and explain why it acts like a voltage source.
- Design a zener shunt regulator: choose the series resistor from the worst-case input and load, and check both power ratings.
- Measure load regulation and line regulation in simulation, and estimate them with the dynamic resistance.
- Explain why a zener regulator beats a voltage divider, and what its limits are.

## The Problem

Phase 04's voltage divider seemed to make any voltage you liked: two resistors turn 12 V into 5 V. But the moment you connect something to its output, the voltage sags, because the load is now in parallel with the bottom resistor. And if the battery drops from 12 V to 10 V, the output drops by the same percentage. A divider is a ratio, not a source.

Real circuits need **rails**: voltages that stay put, whatever the load draws and whatever the battery is doing. A microcontroller specified for 5 V ± 5 % will misbehave at 4.3 V. A sensor whose reference moves will report garbage.

In lesson 04 we learned that a forward diode is "almost a voltage source" near 0.7 V. Here we look at the other side of the curve. Push a diode backwards hard enough and it suddenly conducts, holding its voltage very nearly constant. Manufacturers can place that point anywhere from about 2 V to 200 V. That gives us adjustable, cheap, sturdy voltage references.

## The Physics

### The reverse field gets very strong

Lesson 03 showed that reverse bias widens the depletion region and strengthens the field inside it. With heavy doping on both sides, the depletion region is extremely thin (tens of nanometres) and the field becomes enormous, over 10⁶ V/cm. Two different things can then happen.

### Zener breakdown: tunnelling

When the depletion region is thin enough (about 10 nm), an electron in the p side's valence band can find an empty slot in the n side's conduction band *at the same energy*, separated from it only by a very thin forbidden zone. Quantum mechanics lets particles pass through thin enough barriers they could never climb: **tunnelling**. The electron simply appears on the other side. Current flows without any carrier climbing any hill.

```
  energy        p side                   n side
               ######\                                   ###### = filled valence band
               ######  \                                 ...... = empty conduction band
               ######  ->-> tunnels straight across ......
                          \______________________ ......
                       thin forbidden zone
```

This is called the **Zener effect**, after Clarence Zener, who explained it in 1934. It dominates in heavily doped diodes with breakdown voltages below about 5 V.

What the analogy gets wrong: in the "walking through a wall" picture, tunnelling seems like magic. It is not rare in the microscopic world; it is how flash memory stores data and how the scanning tunnelling microscope sees atoms. Its probability falls exponentially with the barrier's thickness, which is why only very thin junctions show it.

### Avalanche breakdown: a chain reaction

In less heavily doped diodes the depletion region is wider, too wide to tunnel through. But the few minority carriers that drift across are accelerated by the strong field. If one gains enough energy between collisions (more than the band gap), it can smash an electron out of a bond: one carrier becomes three (the original, the freed electron and the hole it left). Those are accelerated too and repeat. Above a critical voltage the multiplication runs away like a landslide: **avalanche breakdown**. It dominates above about 6-7 V.

### Why breakdown is useful, not fatal

Breakdown sounds like destruction, but it is not, by itself. Neither process damages the crystal. What destroys diodes is **heat**: in breakdown the diode has a large voltage across it *and* a current through it, so it dissipates P = V × I. Keep the current limited (with a resistor!) and a diode can sit in breakdown forever. A zener is a diode built to do exactly that: its V_Z is set precisely by the doping, and its package is sized for the heat.

### Temperature behaviour

The two mechanisms drift with temperature in opposite directions. Tunnelling gets *easier* when hot (the gap shrinks a little), so low-voltage zeners have a **negative** temperature coefficient. Avalanche gets *harder* when hot (carriers collide more often and gain less energy between collisions), so high-voltage zeners have a **positive** coefficient. Around 5-6 V the two balance, and those zeners are the most temperature-stable. That's one reason 5.1 V and 5.6 V zeners are so popular.

## The Concept

### The zener's I-V curve

A zener is drawn like a diode with bent ends on the bar:

```
   anode ----|>|_---- cathode          used "backwards": cathode to the + side
              zener
```

Forward, it is an ordinary diode (about 0.7 V). Reverse, it blocks until V_Z, then conducts steeply. Our simulator models the reverse branch with its own exponential, set so the zener carries 5 mA (a typical datasheet test current) at exactly V_Z. Reverse voltage applied directly to a 5.1 V zener:

| Reverse voltage | Reverse current (sharp model) | With 10 Ω extra resistance |
|---|---|---|
| 4.50 V | 0.0000 mA | 0.0000 mA |
| 4.90 V | 0.0022 mA | 0.0022 mA |
| 5.00 V | 0.105 mA | 0.101 mA |
| 5.05 V | 0.723 mA | 0.578 mA |
| 5.10 V | 5.00 mA | 2.16 mA |
| 5.15 V | 34.6 mA | 5.00 mA |
| 5.20 V | 239 mA | 8.60 mA |

Over 0.3 V the current rises by a factor of 100,000. Just like a forward diode, this means **the zener behaves like a voltage source of about V_Z**, provided something else limits the current. Real zeners are softer than our sharp model: they have a **dynamic resistance** r_z of a few ohms to tens of ohms (a 1N4733A, 5.1 V, is specified at 7 Ω max at 49 mA). The right-hand column shows the effect of an extra 10 Ω: each extra milliamp now costs 10 mV more.

### The shunt regulator

```
             R_S
   V_in ----/\/\/----+------------+---- V_out ≈ V_Z
                     |            |
                   zener         [R_L] load
               (cathode up)       |
                     |            |
   ground -----------+------------+
```

How it works, in words: the resistor R_S carries a current I_S = (V_in − V_Z) / R_S, which is fixed as long as the output sits at V_Z. That current splits: the load takes what it needs, and the zener takes **all the rest**. If the load draws more, the zener draws less; if the input rises, the extra current goes into the zener. The output stays at V_Z as long as the zener keeps a little current (its knee current, a milliamp or so).

This is the float valve of the analogy: the zener is a spillway that dumps whatever the load does not use. Because it works by diverting current in parallel with the load, it is a **shunt** regulator.

### Designing it

Requirements (the script's example): input between 10 V and 14 V (say a 12 V lead-acid battery and charger), output 5.1 V, load anywhere between 0 and 20 mA.

**Step 1: the worst case for staying in regulation** is the *lowest* input with the *largest* load. Even then, R_S must deliver the load current plus a minimum zener current (choose 2 mA):

```
R_S ≤ (V_in,min − V_Z) / (I_load,max + I_Z,min) = (10 − 5.1) / (0.020 + 0.002) = 222.7 Ω
```

Pick the next standard value **below**: 220 Ω.

**Step 2: the worst case for the zener's power** is the *highest* input with *no* load: all of R_S's current goes into the zener.

```
I = (14 − 5.1) / 220 = 40.5 mA        P_zener = 5.1 × 0.0405 = 206 mW
```

A 500 mW zener (the common DO-35 glass package) has margin. A 1 W part like the 1N4733A has plenty.

**Step 3: the resistor's power**, at the highest input: (14 − 5.1)² / 220 = 360 mW. Use a 1/2 W resistor; a 1/4 W one would overheat.

Notice the trade-off. A smaller R_S lets you supply bigger loads, but wastes more power in the zener and resistor when the load is light. A shunt regulator always draws its full current from the input, even with no load at all: it is simple and robust, but not efficient.

### Load regulation, simulated

At 12 V input with R_S = 220 Ω:

| Load | V_out | I through R_S | I zener | I load | P zener |
|---|---|---|---|---|---|
| none | 5.147 V | 31.15 mA | 31.15 mA | 0 | 160 mW |
| 2000 Ω | 5.145 V | 31.16 mA | 28.59 mA | 2.57 mA | 147 mW |
| 500 Ω | 5.137 V | 31.20 mA | 20.92 mA | 10.27 mA | 108 mW |
| 255 Ω | 5.121 V | 31.27 mA | 11.19 mA | 20.08 mA | 57 mW |
| 200 Ω | 5.104 V | 31.35 mA | 5.83 mA | 25.52 mA | 30 mW |
| 150 Ω | 4.865 V | 32.43 mA | 0.00 mA | 32.43 mA | 0 |
| 100 Ω | 3.750 V | 37.50 mA | 0.00 mA | 37.50 mA | 0 |

Read the columns: the current through R_S barely changes (31.2 mA) while the zener hands its share over to the load. From no load to 20 mA the output moves by only 26 mV. Then, below about 200 Ω, the load asks for more than 31 mA. The zener has nothing left to give, it stops conducting, and the circuit becomes a plain voltage divider: 12 × 150 / (150 + 220) = 4.865 V. Exactly what the simulator prints.

### Line regulation and the dynamic resistance

With a 500 Ω load, sweep the input from 10 V to 14 V:

```
dynamic resistance    0 ohm: V_out = 5.122 / 5.137 / 5.146 V   (23.8 mV for 4 V of input change)
dynamic resistance   10 ohm: V_out = 5.233 / 5.332 / 5.426 V   (193.0 mV for 4 V of input change)
```

A quick estimate: for small changes, replace the zener by its dynamic resistance r_z. Then R_S and r_z form a divider for *changes*:

```
ΔV_out ≈ ΔV_in × r_z / (r_z + R_S)
```

With r_z = 10 Ω (plus the sharp model's own few ohms): 4 × 10 / 230 = 174 mV, close to the 193 mV simulated. A 4 V input swing became a 0.2 V output swing: about 20 times better than doing nothing, but not perfect. (The absolute voltage also shifted up because the extra resistance carries the zener current: 5.33 V instead of 5.14 V at 12 V. Datasheets specify V_Z at a stated test current for this reason.)

### Compared with a voltage divider

The same 12 V source with a divider designed for 5.1 V unloaded (220 Ω over 163 Ω):

| Load | Divider | Zener regulator |
|---|---|---|
| none | 5.107 V | 5.147 V |
| 1000 Ω | 4.670 V | 5.143 V |
| 500 Ω | 4.302 V | 5.137 V |
| 255 Ω | 3.735 V | 5.121 V |

The divider collapses as soon as it is loaded; the zener holds within 30 mV over the whole range.

### Limits of the zener regulator

- **Efficiency**: it always burns the full R_S current. For a 20 mA load from 12 V, at least 31 mA × 12 V = 374 mW goes in to deliver 102 mW.
- **Precision**: V_Z is usually ±5 % (the "B" or "C" suffix tightens it), and moves with temperature and current.
- **Current**: practical up to tens of milliamps. For more, a transistor is added (Phase 12) or a linear regulator chip is used (Phase 18), which internally uses a precise reference much like a zener, plus an amplifier.

## Build It

### Step 1: The reverse curve

```python
def zener_curve(reverse_volts, dynamic_ohms=0.0):
    circuit = Circuit()
    circuit.voltage_source("V1", "k", "0", reverse_volts)
    circuit.zener("Z1", "0", "k", vz=ZENER_VOLTS, rs=dynamic_ohms)
    result = circuit.dc()
    return -result.i("Z1")
```

The anode is at ground and the cathode at the source's + terminal: reverse bias. The simulator reports diode current from anode to cathode, so reverse current comes out negative; we flip the sign to print it as a positive "reverse current". The optional `rs` adds a series resistance, our stand-in for a softer real zener.

### Step 2: The regulator

```python
def regulator(input_volts, load_ohms, series_ohms=SERIES_OHMS, dynamic_ohms=0.0):
    circuit = Circuit()
    circuit.voltage_source("V1", "in", "0", input_volts)
    circuit.resistor("RS", "in", "out", series_ohms)
    circuit.zener("Z1", "0", "out", vz=ZENER_VOLTS, rs=dynamic_ohms)
    if load_ohms is not None:
        circuit.resistor("RL", "out", "0", load_ohms)
    return circuit.dc()
```

### Step 3: Design numbers

`show_design` evaluates the two worst-case formulas above and prints R_S ≤ 222.7 Ω, the zener's worst power (206 mW) and the resistor's (360 mW).

### Step 4: Sweeps and comparisons

`show_load_regulation` sweeps the load, `show_line_regulation` sweeps the input with and without extra dynamic resistance, and `show_compare_divider` puts a plain divider next to the zener regulator.

```
uv run python phases/11-semiconductors-and-diodes/08-zener-diodes/code/main.py
```

## Use It

- **Common parts**: BZX55 / BZX79 series (500 mW, glass DO-35, 2.4 V to 75 V, ±5 %), 1N4728A-1N4764A (1 W, 3.3 V to 100 V; the 1N4733A is 5.1 V with a test current of 49 mA), BZX84 (SOT-23 surface-mount, 250-300 mW). Datasheets give V_Z at a test current I_ZT, the dynamic impedance Z_ZT, the knee impedance at low current, and the maximum power.
- **Input protection**: a zener from a sensitive input to ground clamps any spike above V_Z, protecting the chip behind it. TVS (transient voltage suppressor) diodes are zeners built to absorb big, short surges such as electrostatic discharge.
- **Gate protection** for MOSFETs (Phase 12): a 12-15 V zener from gate to source stops the gate from seeing more than its 20 V limit.
- **References inside chips**: precision references such as the LM4040 or TL431 behave like an adjustable "super zener" with a dynamic resistance below 1 Ω. Inside, many use a *bandgap* circuit, which combines a diode's −2 mV/°C with a +2 mV/°C term from transistor current ratios to cancel the drift (Phase 12 sets the ground for it).
- **Simple bias rails** in audio amplifiers and test equipment, where a few milliamps at a fixed voltage are all that is needed.

## Try It in the Lab

A 12 V battery, a 5.1 V zener rated 0.5 W and a sensor that behaves like a 1 kΩ load. The series resistor slot is empty. Choose the resistor that keeps the output regulated while keeping both the zener and the resistor below 0.5 W.

Think about: how much current must the resistor deliver so that the zener keeps some after the load takes its share? What happens to the zener when the resistor is very small? What happens to the output when it is very large? Try both wrong parts after you pass and read which goal each breaks.

## Common Mistakes

- **Installing the zener forwards.** Forward, it is just a 0.7 V diode. The cathode (band) must go to the more positive side.
- **No series resistor.** A zener across a supply above V_Z is a short circuit: it burns out. Something must limit the current.
- **Designing for the typical case only.** Check regulation at minimum input and maximum load, and power at maximum input and *no* load.
- **Forgetting that no-load is the zener's worst case.** Remove the load and the zener takes everything.
- **Expecting precision.** A 5 % zener can be anywhere from 4.85 V to 5.36 V, and moves with current and temperature. For better, use a reference IC.
- **Using a zener as a power supply for big loads.** Beyond tens of milliamps, the wasted power becomes unreasonable; use a linear regulator or a switching converter (Phase 18).

## Exercises

1. A 9 V battery feeds a 3.3 V zener through R_S, and the load draws up to 10 mA. Keeping 1 mA minimum in the zener, what is the largest R_S if the battery may sag to 7 V? What power does the zener dissipate with a fresh 9.5 V battery and no load?
2. In the load table, the zener regulator holds 5.1 V up to about 25 mA of load. Compute by hand the load resistance at which regulation is lost with a 10 V input instead of 12 V.
3. A zener has r_z = 15 Ω and is fed through R_S = 470 Ω. The input has 1 V of ripple (from a rectifier, lesson 06). How much ripple reaches the output?
4. Combine lessons 06 and 08: put the regulator after the 470 µF half-wave rectifier of lesson 06 (in the simulator, `transient`). What R_S keeps the output steady at 5.1 V through the ripple with a 1 kΩ load?
5. Use the script's `zener_curve` with `vz=3.3` and with `vz=12`. Then read about temperature coefficients on a BZX55 datasheet: which of your two zeners would drift down with heat, and which up?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Zener diode | "A zener" | A diode built to operate in reverse breakdown at a precise voltage V_Z |
| V_Z | "Zener voltage" | Reverse voltage at the datasheet's test current I_ZT |
| Zener effect | "Tunnelling breakdown" | Electrons tunnel through a very thin depletion region; dominates below about 5 V, negative tempco |
| Avalanche | "Impact ionisation" | Accelerated carriers knock out more carriers in a chain reaction; dominates above about 6-7 V, positive tempco |
| Shunt regulator | "Zener regulator" | Series resistor plus a parallel element that diverts excess current to hold the voltage |
| Dynamic resistance r_z | "Zener impedance" | Slope ΔV/ΔI in breakdown; sets how much the output moves with current |
| Knee current | "Minimum zener current" | Smallest current that keeps the zener firmly in breakdown |
| Load / line regulation | "How stiff the rail is" | Output change per change in load current / input voltage |

## Further Reading

- *All About Circuits*, Volume III, chapter 3, "Zener Diodes". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-3/zener-diodes/
- Vishay, 1N4728A-1N4764A datasheet (1 W zeners): V_Z, test current, dynamic impedance, power derating. https://www.vishay.com/docs/85816/1n4728a.pdf
- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., section 9.1 (from zener to series-pass regulator) and section 9.10 (voltage references, starting with the zener diode).
- C. Zener, "A theory of the electrical breakdown of solid dielectrics", *Proceedings of the Royal Society A*, 1934: the original tunnelling explanation.
