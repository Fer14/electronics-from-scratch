# Linear Regulators

> A linear regulator is a smart resistor: it continuously adjusts itself to burn off exactly the extra voltage, so the output stays put. Simple and quiet, but every volt it drops becomes heat.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 11 (Semiconductors and Diodes), Lesson 08 (Zener Diodes); Phase 12 (Transistors), Lessons 02-03 (The BJT, The BJT as a Switch); Phase 13 (Operational Amplifiers), Lesson 03 (Inverting and Non-Inverting Amplifiers); Phase 03 (Resistance and Ohm's Law), Lesson 05 (Power and Heat)
**Time:** ~90 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Power supply | Whatever provides the voltage a circuit runs on. | The water mains of a house. |
| Regulator | A circuit that keeps its output voltage constant even when the input or the load changes. | A pressure-reducing valve that keeps the tap pressure the same whatever the mains does. |
| Linear regulator | A regulator that drops the extra voltage across a transistor working as a variable resistor. | A valve partly closed to throttle the flow. |
| Input voltage (Vin) | The voltage going into the regulator, from a battery or adapter. | Mains pressure. |
| Output voltage (Vout) | The steady voltage the regulator produces. | Tap pressure. |
| Load | Whatever draws current from the output. | The taps that are open. |
| Load current | How much current the load takes; it can change at any moment. | How much water is being used. |
| Line regulation | How little the output changes when the input changes. | Tap pressure staying put when the mains pressure varies. |
| Load regulation | How little the output changes when the load current changes. | Tap pressure staying put when someone opens the shower. |
| Shunt regulator | A regulator that sits in parallel with the load and soaks up extra current. | An overflow pipe that dumps whatever the house does not use. |
| Series regulator | A regulator that sits in series with the load and throttles the current. | The valve in the pipe. |
| Pass transistor | The transistor in a series regulator that carries the load current and drops the extra voltage. | The valve itself. |
| Reference voltage | A very stable small voltage the regulator compares its output to. | A spirit level the plumber checks against. |
| Feedback | Measuring the output and correcting the control to keep it at the target (Phase 13). | Watching a pressure gauge and turning the valve. |
| Dropout voltage | The smallest Vin - Vout at which the regulator still regulates. | The valve can only reduce pressure; if the mains drops too low, it cannot help. |
| Efficiency | The fraction of input power that reaches the load: P_out / P_in. | How much of the water you pay for comes out of the taps. |

## Learning Objectives

- Explain why almost every circuit needs a regulated supply, and what "line regulation" and "load regulation" mean
- Design a zener shunt regulator: choose the series resistor from the minimum input, the maximum load and the zener's minimum current, and check the power in each part
- Improve it with an emitter-follower pass transistor, and then with an op-amp feedback loop, and compare their load regulation in the simulator
- Compute the efficiency (at best Vout / Vin) and the heat dissipated by any linear regulator, and explain dropout
- Recognise the classic parts (7805, LM317, LDOs) and read their key datasheet numbers

## The Problem

A 9 V battery starts at about 9.5 V and ends its life near 6 V. A car's "12 V" rail swings from 11 V to over 14 V, with spikes when the engine starts. A cheap wall adapter labelled 12 V may give 16 V with no load and 11 V at full load. Meanwhile the microcontroller of Phase 17 wants 3.3 V or 5 V within a few percent, and its ADC measures everything relative to its supply (Phase 17, Lesson 04). If the supply wanders, so does every reading.

The circuit also changes its own demands: an LED turns on, a radio transmits, a motor starts. Each change in load current would change the voltage of a simple divider (Phase 04, Lesson 05). So we need a box that takes a messy, varying input and delivers a fixed voltage, whatever the load does. The simplest such box is a linear regulator. This lesson builds three of them, from crude to good, and finds their one big weakness: heat.

## The Physics

### Where the extra voltage goes

Energy conservation (Phase 01, Lesson 07) is the whole story of linear regulators. The same current that flows into the load flows through the regulator (plus a little for the regulator itself). If the input is 12 V and the output is 5 V, the regulator has 7 V across it while carrying the load current. Power is voltage times current (Phase 03, Lesson 05), so:

```
heat in the regulator = (Vin - Vout) x I_load
```

Read it as: "the regulator burns the voltage difference times the current". At 1 A that is 7 W, enough to make a small part too hot to touch within seconds (Lesson 07 deals with getting rid of that heat). The load receives `5 V x 1 A = 5 W` while the source delivers `12 V x 1 A = 12 W`:

```
efficiency = P_out / P_in = (Vout x I) / (Vin x I) = Vout / Vin = 5 / 12 = 41.7%
```

No cleverness inside a linear regulator can beat `Vout / Vin`, because the current in and the current out are the same. Beating it needs a completely different idea, which is the subject of the next lesson.

### The zener: a voltage that does not want to move

A zener diode (Phase 11, Lesson 08) conducts in reverse once the voltage reaches its zener voltage Vz, and above that its current rises steeply: a small change in voltage makes a big change in current. Turned around: over a wide range of currents, its voltage barely moves. That makes it a cheap, decent voltage reference. Its weakness: below a minimum current (a milliamp or so for small zeners) it stops "holding" and its voltage sags.

### The transistor as a variable resistor

A BJT in its active region (Phase 12, Lesson 02) has its emitter following its base, about 0.6-0.7 V lower, almost regardless of the collector voltage and of how much current flows. If you hold the base at a fixed voltage, the emitter becomes a fixed voltage that can supply a lot of current, because the base only needs `I_load / beta`. The collector-emitter voltage takes up whatever is left over. That is the pass transistor.

## The Concept

### Regulator 1: the zener shunt

```
   Vin ----[ RS ]----+---------+------ Vout
                     |         |
                   zener      load
                   (5.1 V)     |
                     |         |
   gnd --------------+---------+
```

`RS` carries the total current. The zener takes whatever the load does not:

```
I_RS = (Vin - Vz) / RS
I_zener = I_RS - I_load
```

As long as `I_zener` stays above its minimum, the output is close to Vz.

**Worked example.** Vin = 12 V, Vz = 5.1 V, RS = 330 ohm, load 1 kohm.

```
I_RS = (12 - 5.1) / 330 = 6.9 / 330 = 20.9 mA
I_load = 5.1 / 1000 = 5.1 mA
I_zener = 20.9 - 5.1 = 15.8 mA
P_RS = 6.9 V x 20.9 mA = 144 mW
P_zener = 5.1 V x 15.8 mA = 81 mW
```

**Designing RS.** The dangerous case for regulation is lowest input and highest load: the resistor must still supply the load plus the zener's minimum current. The dangerous case for heat is highest input and no load: then all of `I_RS` goes through the zener.

```
RS <= (Vin_min - Vz) / (I_load_max + I_zener_min)
P_zener_max = Vz x (Vin_max - Vz) / RS       (load disconnected)
```

Example: Vin from 9 to 15 V, load up to 10 mA, zener minimum 2 mA:

```
RS <= (9 - 5.1) / (10 mA + 2 mA) = 3.9 / 0.012 = 325 ohm     -> use 300 ohm
P_zener_max = 5.1 x (15 - 5.1) / 300 = 5.1 x 33 mA = 168 mW  -> a 0.5 W zener is fine
```

The zener shunt is simple and robust, but wasteful (it draws full current even with no load) and only suitable for tens of milliamps. The simulation shows its limit: at 12 V with RS = 330 ohm, a load of 220 ohm wants `5.1 / 220 = 23 mA`, more than the 20.9 mA the resistor can supply. The zener current hits zero and the output falls to 4.8 V. With 100 ohm, the output collapses to 2.8 V: the "regulator" is now just a voltage divider.

### Regulator 2: zener plus emitter follower

```
   Vin ----+--------------+
           |              |  collector
         [ RB ]         |/
           |      base  |    NPN pass transistor
           +------------|
           |            |\
        zener 5.6 V       v  emitter
           |              +------ Vout (about 5.6 - 0.7 = 4.9 V)
          gnd             |
                        load
                          |
                         gnd
```

Now the zener only has to supply the transistor's *base* current, `I_load / beta`. With beta = 100, a 500 mA load needs only 5 mA of base current. The transistor carries the load current and drops `Vin - Vout`.

The cost: the output is `Vz - V_BE`, and `V_BE` rises slowly with current (60 mV per tenfold increase, from the diode equation of Phase 11, Lesson 04) and changes with temperature (about -2 mV per degree). The simulation shows the output drifting from 4.91 V at 5 mA to 4.76 V at 476 mA: 150 mV of load regulation error. Better than collapsing, but not precise.

### Regulator 3: feedback with an op-amp

Measure the output, compare it with a reference, and let an amplifier adjust the base until they agree. This is the structure of every real linear regulator:

```
                    Vin
                     |
                   |/  pass transistor
       +---[100]---|
       |           |\
       |             +-----+-------- Vout
     op-amp out      |     |
       |           [ R1 ]  load
     +-+-+           |     |
 ref-|+   |          +--- fb (feedback)
     |  - |----------+
     +----+        [ R2 ]
                     |
                    gnd
```

The op-amp drives its output until its two inputs are equal (Phase 13, Lesson 01): `V_fb = V_ref`. The divider R1/R2 makes `V_fb = Vout x R2 / (R1 + R2)`, so:

```
Vout = V_ref x (1 + R1 / R2)
```

Read it as: "the output is the reference multiplied by the non-inverting amplifier's gain". With `V_ref = 2.5 V`, `R2 = 10 kohm`, `R1 = 10 kohm`: `Vout = 2.5 x 2 = 5.0 V`.

All the transistor's imperfections (its V_BE, its beta, temperature) are inside the feedback loop, so the op-amp corrects them. In the simulation the output stays at 5.000 V from 5 mA to 500 mA: load regulation better than 0.01%.

A note on the simulation: a circuit with high-gain feedback and exponential transistors is hard for Newton's method (Phase 11, Lesson 05) to solve in one go. Real regulators have the same start-up problem in hardware, and many solve it with a **soft start**: the reference rises slowly from 0 V. Our code does exactly that with `circuit.sweep("VREF", ...)`, which solves 251 operating points with the reference rising to 2.5 V, each starting from the previous answer.

### Dropout

The pass transistor can only *reduce* voltage. Its base is driven by the op-amp, which is powered from Vin and cannot drive above Vin. So the highest possible output is about:

```
Vout_max = Vin - V_BE - I_base x R_base
```

When Vin falls too low, the op-amp's output hits its upper limit and the output simply follows the input down. The smallest `Vin - Vout` that still regulates is the **dropout voltage**. In the simulation, with 500 mA:

```
Vin = 7.0 V   ->  Vout = 5.000 V    (regulating, 2 V of headroom)
Vin = 6.0 V   ->  Vout = 4.72 V     (dropped out: about 1.3 V below Vin)
```

Real numbers: the classic 7805 needs about 2 V of headroom (it uses a two-transistor pass stage). "LDO" (low-dropout) regulators use a P-channel MOSFET as the pass element, which can be turned fully on, and drop out at a few hundred millivolts or less. For example, the MCP1700 is specified at 178 mV typical at 250 mA.

### Worked example: an LM317 for 3.3 V

The LM317 keeps 1.25 V between its output and its adjust pin (an internal reference inside a feedback loop, exactly our regulator 3). With R1 from output to adjust and R2 from adjust to ground, and ignoring the tiny adjust-pin current:

```
Vout = 1.25 V x (1 + R2 / R1)
```

For 3.3 V with the usual R1 = 240 ohm:

```
R2 = R1 x (Vout / 1.25 - 1) = 240 x (2.64 - 1) = 240 x 1.64 = 394 ohm      -> use 390 ohm
Vout = 1.25 x (1 + 390 / 240) = 1.25 x 2.625 = 3.281 V
```

From a 9 V adapter at 300 mA:

```
heat = (9 - 3.28) x 0.3 = 1.72 W
efficiency = 3.28 / 9 = 36%
```

1.7 W in a TO-220 package with no heatsink (about 50 K/W) raises it about 86 C above the air: too hot. Lesson 07 sizes the heatsink; Lesson 03 shows how a buck converter would do the same job with a tenth of the heat.

### Worked example: is the headroom enough?

The LM317 needs roughly 1.5 to 2.5 V between input and output, depending on current and temperature (its datasheet's dropout curve). At 3.3 V out, the input must stay above about 5.8 V. A 9 V battery that sags to 6.5 V near the end of its life is still fine; a 5 V USB input would not be, and calls for an LDO instead.

## Build It

### Step 1: The zener shunt regulator

```python
def zener_regulator(vin, series_ohms, load_ohms):
    circuit = Circuit()
    circuit.voltage_source("VIN", "vin", "0", vin)
    circuit.resistor("RS", "vin", "out", series_ohms)
    circuit.zener("Z1", "0", "out", vz=VZ)
    circuit.resistor("RL", "out", "0", load_ohms)
    result = circuit.dc()
    ...
```

The zener's anode is at ground and its cathode at the output, the reverse-biased way zeners are used. The simulator reports diode current from anode to cathode, so the reverse zener current comes out negative; the code flips its sign.

### Step 2: Line and load sweeps

The script runs the zener regulator at Vin = 7, 9, 12 and 15 V (line regulation) and then at 12 V with loads from 10 kohm down to 100 ohm (load regulation), and flags when the zener current reaches zero.

### Step 3: The emitter follower

`follower_regulator` adds an NPN transistor with the zener (5.6 V) and a 1 kohm resistor setting its base.

### Step 4: The feedback regulator with soft start

```python
    circuit.opamp("U1", plus="ref", minus="fb", out="drive", gain=1e4, rails=(0.0, vin))
    circuit.resistor("RB", "drive", "b", 100)
    circuit.npn("Q1", c="vin", b="b", e="out", beta=100)
    circuit.resistor("R1", "out", "fb", top)
    circuit.resistor("R2", "fb", "0", 10_000)
    circuit.resistor("RL", "out", "0", load_ohms)
    soft_start = circuit.sweep("VREF", np.linspace(0.0, vref, 251))
```

`rails=(0.0, vin)` makes the op-amp unable to swing above its own supply, which is what produces dropout. A gain of 10 000 (80 dB) is typical for a regulator's error amplifier.

Run it:

```
uv run python phases/18-power-electronics/01-linear-regulators/code/main.py
```

Compare the three load tables: zener alone collapses past about 20 mA, the follower droops by 150 mV, the feedback regulator holds 5.000 V. Then look at the transistor heat: 3.5 W at 500 mA, and efficiency stuck at about 42% whatever the circuit, exactly `5 / 12`. The final table shows why linear regulators are fine from 5.5 V (91%) and terrible from 24 V (21%, 19 W of heat at 1 A).

## Use It

- **78xx family (7805, 7812...):** three-pin fixed regulators: input, ground, output. About 2 V dropout, up to 1 A with a heatsink, built-in current limit and thermal shutdown. Needs small capacitors on input and output (0.33 uF and 0.1 uF in the classic datasheet).
- **LM317:** adjustable: it keeps 1.25 V between its output and adjust pins, so `Vout = 1.25 V x (1 + R2 / R1)` (plus a tiny adjust-pin current term). The same feedback formula as our op-amp regulator.
- **LDOs:** AMS1117 (about 1.1-1.3 V dropout, common on Arduino-style boards), MCP1700 and many others with a few hundred millivolts of dropout and tiny quiescent current for battery devices.
- **TL431:** an adjustable "programmable zener" (an op-amp plus a 2.5 V reference in one part), used as the reference in most switching power supplies.
- **When to use linear:** small voltage differences, low currents, or when noise matters (audio, precision ADC references, radio). They produce no switching noise at all. For large differences or big currents, use a switching converter (next lessons), often followed by an LDO for a clean final rail.

## Try It in the Lab

You get a 12 V source, a 5.1 V zener and a 1 kohm load, and you pick the series resistor of a shunt regulator. The output must stay between 4.9 and 5.3 V, the zener must stay under 0.1 W, and the quarter-watt resistor must stay under 0.25 W. For each candidate, compute the resistor current, subtract the load's 5.1 mA, and see which goal it breaks: one starves the zener, one cooks things.

## Common Mistakes

- **Designing for the typical input.** Check the lowest input (does it still regulate?) and the highest input (does anything overheat?).
- **Forgetting the no-load case of a shunt regulator.** When the load is unplugged, the zener takes everything. That is when it overheats.
- **Ignoring heat in series regulators.** A 7805 dropping 12 V to 5 V at 1 A dissipates 7 W; without a heatsink it reaches thermal shutdown in seconds (Lesson 07).
- **Too little headroom.** A 7805 fed from 6 V is not regulating. Check the dropout in the datasheet, at your current and temperature.
- **Leaving out the capacitors.** Regulators are feedback loops; without the recommended input and output capacitors many of them oscillate.
- **Expecting a linear regulator to step up.** It can only drop voltage. To get 5 V from a 3.7 V battery you need a boost converter (Lesson 04).

## Exercises

1. A zener shunt regulator: Vin = 9 V, Vz = 3.3 V, load up to 15 mA, zener minimum 1 mA. Find the largest RS. What does the zener dissipate with no load? (RS <= 5.7 / 0.016 = 356 ohm; with 330 ohm, 3.3 x 17.3 mA = 57 mW.)
2. A feedback regulator has V_ref = 1.25 V and R2 = 240 ohm. Which R1 gives 3.3 V? (R1 = 240 x (3.3 / 1.25 - 1) = 394 ohm, so 390 ohm.)
3. A 7805 supplies 300 mA from a 9 V battery. What are the efficiency and the dissipation? (55.6%, 1.2 W.)
4. An LDO with 200 mV dropout makes 3.3 V from a single lithium cell (4.2 V full, 3.0 V empty). Below which battery voltage does it stop regulating? (3.5 V.) What fraction of the battery's range is then unusable?
5. Harder: in `main.py`, give the feedback regulator a 15 V input and a 10 ohm load. How much power does the transistor dissipate? Then replace the op-amp regulator by a zener shunt regulator for the same 500 mA load and compute the zener's no-load dissipation. Why is the shunt design hopeless at this current?

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Linear regulator | "A 7805" | A series transistor controlled by feedback to hold Vout; drops (Vin - Vout) as heat |
| Shunt regulator | "A zener regulator" | A part in parallel with the load that absorbs the excess current |
| Dropout | "Minimum input" | The smallest Vin - Vout at which regulation still works |
| LDO | "Low-noise regulator" | A low-dropout regulator, usually with a PMOS pass device |
| Line regulation | "Input rejection" | Change in Vout per change in Vin |
| Load regulation | "Stiffness" | Change in Vout per change in load current |
| Efficiency | "How good it is" | P_out / P_in; for a linear regulator at best Vout / Vin |

## Further Reading

- [Texas Instruments, LM340 / LM78xx datasheet](https://www.ti.com/lit/ds/symlink/lm340.pdf) and [LM317 datasheet](https://www.ti.com/lit/ds/symlink/lm317.pdf) — dropout, thermal limits and the adjustable-output formula
- [Texas Instruments, SLVA079 "Understanding the Terms and Definitions of LDO Voltage Regulators"](https://www.ti.com/lit/an/slva079/slva079.pdf) — dropout, line and load regulation explained
- [Microchip, MCP1700 datasheet](https://www.microchip.com/en-us/product/MCP1700) — a low-quiescent-current LDO for battery devices
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 9 (Voltage Regulation and Power Conversion)
