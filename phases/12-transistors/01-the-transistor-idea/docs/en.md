# The Transistor Idea

> A transistor is a valve: a small signal on one terminal decides how much current flows between the other two. Open and shut it, and you have a switch. Turn it gently, and you have an amplifier. Everything digital and most things analogue are built from that one idea.

**Type:** Learn
**Prerequisites:** Phase 11 (Semiconductors and Diodes), especially 11-03 (The pn Junction) and 11-04 (The Diode Equation); Phase 05 (Circuit Analysis and Our Simulator), lesson 08-dependent-sources
**Time:** ~50 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Transistor | A three-terminal semiconductor part in which one terminal controls the current between the other two | A tap: a small twist of the handle controls a large flow of water |
| Control terminal | The terminal that receives the small signal: the base (BJT) or gate (MOSFET) | The tap's handle |
| Main path | The two terminals the large current flows between: collector-emitter or drain-source | The pipe through the tap |
| Switch (mode) | Using a transistor fully on or fully off | Turning the tap fully open or fully shut |
| Amplifier (mode) | Using a transistor partly on, so small changes at the control make large changes in the output | Fine-adjusting the tap so a tiny twist changes the flow a lot |
| Gain | How many times bigger the output change is than the input change | The lever ratio of a crowbar |
| Transconductance (g_m) | Output current change per volt of input change, in amperes per volt (siemens) | "Litres per minute per degree of handle turn" |
| Dependent source | A circuit element whose voltage or current is set by another voltage or current in the circuit (Phase 05) | A puppet whose movement is set by the puppeteer's hand |
| Load | Whatever the transistor's main current flows through: an LED, a motor, a resistor | The garden the hose waters |
| Supply (rail) | The fixed voltage that provides the energy, such as 5 V or 12 V | The water main behind the tap |
| Saturation (BJT) | The state where the transistor is "as on as it can be": the load, not the transistor, now limits the current | The tap fully open: the pipe itself is the limit |
| Cutoff | Fully off: no main current | The tap shut |
| Vacuum tube | The transistor's ancestor: a heated filament in a glass bulb, with a grid controlling electron flow | An old radio's glowing glass bulbs |

## Learning Objectives

- Explain what a transistor does in one sentence, and why that is enough for both switches and amplifiers.
- Distinguish the control path from the main path, and explain where the energy actually comes from.
- Model an idealised transistor as a voltage-controlled current source and compute its voltage gain, −g_m × R_L.
- Recognise the limits any real transistor has: it cannot push its output past its supply rails.
- See, in our simulator, a real NPN transistor in which microamps control milliamps.

## The Problem

Phase 11 gave us diodes. A diode decides whether current flows based on the voltage *across itself*. That is useful, but it is not *control*: you cannot use one signal to steer another. Every interesting electronic system needs exactly that:

- A microcontroller pin can only supply a few milliamps at 3.3 V, but you want it to run a 2 A motor at 12 V.
- A microphone produces a signal of a few millivolts, but a loudspeaker needs volts.
- A computer needs billions of switches in which the output of one switch controls the next.

All three need a part with a *control input* that is separate from the path doing the work. That part is the transistor. Since 1947 it has gone from a hand-assembled lump of germanium the size of your thumb to switches 20 nanometres across, manufactured 10²¹ per year: more transistors are made every year than grains of rice are grown.

This lesson introduces the idea without the device physics. The next lessons open the box: lesson 02 the bipolar junction transistor (BJT), lesson 04 the MOSFET.

## The Physics

### The tap analogy

A garden tap has three "terminals": the water main, the outlet and the handle. The handle needs very little effort; the water does the work. Turning the handle a bit changes the flow a lot. Crucially, **the energy in the water comes from the main**, not from your hand. Your hand only decides how much of it gets through.

A transistor is the same:

```
            supply (energy source)
              |
            [load]                  main path: large current
              |
   control --|<transistor>          control: small current or just a voltage
              |
            ground
```

- The **main path** (collector to emitter in a BJT, drain to source in a MOSFET) carries the load current.
- The **control terminal** (base or gate) sets how much current the main path allows.
- The **energy** comes from the supply. The transistor converts a small input signal into a large copy of it by *releasing* the supply's energy in the right pattern.

What the analogy gets wrong: a tap is a resistance you vary. A transistor in its amplifying mode is better described as a *current source* whose value the control sets: within limits, it delivers the same current almost regardless of the voltage across the main path. That difference is why a transistor makes a much better amplifier than a variable resistor would.

### Where does the "control" come from, physically?

Both main transistor families use the junction physics of Phase 11.

- In a **BJT** (bipolar junction transistor), the control is the base-emitter pn junction. Forward-biasing it by a few tenths of a volt injects carriers that, instead of recombining, are swept across a very thin middle layer into the collector. The control voltage changes the barrier height, and the main current follows the diode equation: it grows ×10 for every 60 mV.
- In a **MOSFET** (metal-oxide-semiconductor field-effect transistor), the control is a gate electrode separated from the silicon by a thin layer of glass (the native oxide of lesson 11-01). A voltage on the gate attracts carriers to the surface underneath and creates a conducting channel between source and drain. No steady current flows into the gate at all: it is a capacitor.

### Before transistors

The same idea existed before semiconductors. A **relay** (1830s) uses a small current in a coil to pull a mechanical switch shut: a switch, but slow and unable to amplify smoothly. The **vacuum tube triode** (Lee de Forest, 1906) put a wire grid between a heated cathode, which boils off electrons, and a plate that collects them; a small voltage on the grid controls a large electron current. Tubes made radio, television and the first electronic computers possible (ENIAC, 1945, had 17,468 of them). They were also hot, fragile and power-hungry. The point-contact transistor (Bardeen, Brattain and Shockley at Bell Labs, 1947) and the junction transistor (Shockley, 1948) did the same job in a solid crystal.

## The Concept

### The ideal transistor: a controlled current source

Strip away the physics and keep only the behaviour: **the main-path current equals a constant times the control voltage**. In Phase 05 you met exactly this element: a voltage-controlled current source (VCCS).

```
I_out = g_m × V_control
```

Read: "the output current equals the transconductance times the control voltage". `g_m` (transconductance) is in amperes per volt. "Trans" because the control is on one pair of terminals and the effect on another.

Our script builds this ideal valve with the simulator's `vccs`, with g_m = 5 mA/V, a 1 kΩ load and a 10 V supply:

```
        +10 V
          |
        [R_L] 1 kΩ
          |
          +---- out
          |
     ( G1: 5 mA per volt of V_in )
          |
        ground
```

Results:

| Control V | Control current | Load current | V out | Control power | Load power |
|---|---|---|---|---|---|
| 0.0 V | 0 | 0 mA | 10.00 V | 0 | 0 |
| 0.5 V | 0.5 µA | 2.50 mA | 7.50 V | 0.25 µW | 6.3 mW |
| 1.0 V | 1.0 µA | 5.00 mA | 5.00 V | 1.00 µW | 25.0 mW |
| 1.5 V | 1.5 µA | 7.50 mA | 2.50 V | 2.25 µW | 56.3 mW |
| 2.0 V | 2.0 µA | 10.00 mA | 0.00 V | 4.00 µW | 100.0 mW |

(The control current is just the 1 MΩ resistor we put on the input so it isn't floating; the VCCS itself draws nothing.)

Look at the power columns: **4 microwatts of control power steer 100 milliwatts of load power**. That is a power gain of 25,000. The 100 mW comes from the 10 V supply.

Check the output voltage with Kirchhoff and Ohm: V_out = 10 V − I × 1000 Ω. At 1.0 V of control: 10 − 0.005 × 1000 = 5.00 V. ✓

### Mode 1: the switch

Use only two control levels: 0 V (off) and enough to turn the valve fully on (2 V here).

```
OFF (0 V): load current  0.00 mA, output 10.00 V
ON  (2 V): load current 10.00 mA, output  0.00 V
```

That is a switch, operated by a voltage, with no moving parts. Notice the *inversion*: control high gives output low. That is a logic NOT gate, and Phase 14 will build all of digital logic from such inverting switches.

### Mode 2: the amplifier

Now wiggle the control a little around a middle value: from 0.9 V to 1.1 V (a 0.2 V change).

```
output moves from 5.50 V to 4.50 V: voltage gain = -5.0
```

A 0.2 V change in became a 1.0 V change out: a **voltage gain** of 5, with a minus sign because the output moves the opposite way (inverting). Where does 5 come from? A change ΔV_in changes the current by g_m × ΔV_in, which changes the resistor's voltage by g_m × ΔV_in × R_L, and the output (supply minus resistor voltage) by the negative of that:

```
A_v = ΔV_out / ΔV_in = −g_m × R_L = −0.005 A/V × 1000 Ω = −5
```

Read: "the voltage gain equals minus the transconductance times the load resistance". This is the most important amplifier formula in electronics. Bigger g_m or bigger R_L, more gain. Lessons 06 and 07 apply it to a real transistor, where g_m is set by the current: g_m = I_C / V_T, about 40 mA/V per milliamp.

The **operating point** (1.0 V in, 5.0 V out here) is chosen in the middle of the output range so the output can swing both up and down. Choosing and stabilising that point is called **biasing** (lesson 06).

### Every real transistor runs out of room

Push the ideal model further, to 3 V of control:

```
3.0 V   15.00 mA   -5.00 V
```

The ideal VCCS happily pushes the output to −5 V, below ground. No real part can do that: a transistor connected between a load and ground can at best connect its output to ground (0 V); it can never *generate* a voltage below its own ground. **Models have limits.** A real transistor in this position hits about 0 V and stays there, which is called **saturation** for a BJT. Every amplifier's output is confined between its supply rails, and the art of amplifier design is to keep the signal well inside them.

### A real transistor in the same place

Replace the ideal source by a real NPN transistor from the simulator (β = 100), and drive its base directly with a voltage:

| V_BE | Base current | Collector current | V out | I_C / I_B |
|---|---|---|---|---|
| 0.50 V | 0.025 µA | 0.0025 mA | 10.00 V | 100 |
| 0.60 V | 1.20 µA | 0.120 mA | 9.88 V | 100 |
| 0.64 V | 5.64 µA | 0.564 mA | 9.44 V | 100 |
| 0.66 V | 12.2 µA | 1.22 mA | 8.78 V | 100 |
| 0.70 V | 57.5 µA | 5.75 mA | 4.25 V | 100 |
| 0.72 V | 1383 µA | 9.94 mA | 0.06 V | 7.2 |
| 0.75 V | 15290 µA | 9.97 mA | 0.03 V | 0.7 |

Three things to notice:

1. **Microamps control milliamps.** The collector current is exactly 100 times the base current: that is the current gain β (beta), the subject of lesson 02.
2. **The control is exponential.** Each 60 mV of V_BE multiplies the collector current by 10 (0.60 V → 0.12 mA, 0.66 V → 1.22 mA): the diode equation of lesson 11-04 at work in the base-emitter junction.
3. **Saturation is real.** At 0.72 V the transistor "wants" 12.6 mA, but the 1 kΩ load cannot pass more than 10 mA from a 10 V supply. The output collapses to about 0.06 V and extra base current is simply wasted (the ratio I_C / I_B collapses). That is the fully-on switch state.

### Two families

| | BJT (bipolar junction transistor) | MOSFET |
|---|---|---|
| Terminals | collector, base, emitter | drain, gate, source |
| Control | base current (or V_BE, exponentially) | gate voltage (square law), no steady gate current |
| Strengths | high, predictable g_m; good analogue behaviour | almost no control power; tiny; perfect for logic and power switching |
| Where | audio amps, RF, references, some power | every chip, power converters, motor drivers |

Lessons 02-03 cover the BJT, 04-05 the MOSFET, and 06-08 their use as amplifiers and current sources.

## Build It

### Step 1: The ideal valve

```python
def ideal_valve(control_volts, transconductance, load_ohms=LOAD_OHMS):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", SUPPLY)
    circuit.voltage_source("VIN", "in", "0", control_volts)
    circuit.resistor("RL", "vcc", "out", load_ohms)
    circuit.vccs("G1", "out", "0", "in", "0", transconductance)
    circuit.resistor("RIN", "in", "0", 1e6)
    return circuit.dc()
```

`vccs("G1", "out", "0", "in", "0", gm)` pulls a current g_m × V(in) from node `out` to ground. It is the transistor's behaviour without the transistor.

### Step 2: Switch and amplifier

`show_switch` uses two control levels; `show_amplification` measures the output at 0.9 V and 1.1 V and divides the change by 0.2 V.

### Step 3: The real thing

```python
def real_transistor(base_emitter_volts, load_ohms=LOAD_OHMS):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", SUPPLY)
    circuit.voltage_source("VIN", "b", "0", base_emitter_volts)
    circuit.resistor("RL", "vcc", "out", load_ohms)
    circuit.npn("Q1", c="out", b="b", e="0", beta=100)
    return circuit.dc()
```

`result.i("Q1")` is the collector current and `result.i("Q1.b")` the base current.

```
uv run python phases/12-transistors/01-the-transistor-idea/code/main.py
```

## Use It

- **Counting transistors**: an Intel 4004 (1971) had 2,300. An Apple M-series or a high-end GPU has tens of billions to over 100 billion. All are switches of the kind in Mode 1.
- **Everyday discrete transistors**: the 2N3904 and BC547 (small NPN BJTs, around β = 100-300, up to 100-200 mA), the 2N2222 (up to 600 mA), the 2N7000 and BS170 (small MOSFETs), and the IRLZ44N or AO3400 (logic-level power MOSFETs that switch amps from a 3.3-5 V pin).
- **Amplifiers everywhere**: the first stage of a microphone preamp, the RF front end of your phone, and the inside of every op-amp (Phase 13) are transistors in Mode 2.
- **Datasheet vocabulary preview**: "h_FE" (β, current gain), "V_CE(sat)" (voltage across a fully-on BJT, about 0.1-0.3 V), "R_DS(on)" (resistance of a fully-on MOSFET, milliohms for power parts), "V_GS(th)" (gate threshold).

## Common Mistakes

- **"The transistor creates the energy."** It controls energy from the supply. No supply, no output.
- **"A transistor amplifies current, so the output can be anything."** The output is confined between the rails; the load limits the current. A transistor can't push 15 mA through 1 kΩ from 10 V.
- **"A transistor is a variable resistor."** In amplifying mode it acts much more like a current source; this is what makes high gain possible.
- **Forgetting the minus sign.** The simple amplifier inverts: when the input goes up, the output goes down.
- **Confusing the terminals.** Base/gate is the control; the main current flows collector→emitter (NPN) or drain→source (N-channel).

## Exercises

1. An ideal valve has g_m = 20 mA/V and drives a 470 Ω load from 12 V. What is the voltage gain? At what control voltage does the output reach 0 V?
2. In the switching table, how much power is delivered to the load when ON? Where does it come from?
3. Change `LOAD_OHMS` to 2200 Ω in the script. What happens to the gain of the ideal valve? To the control voltage at which the real transistor saturates?
4. From the real-transistor table, estimate the V_BE that gives exactly 1 mA. (Use the 60 mV per decade rule between two rows.)
5. A relay coil needs 70 mA at 5 V and a microcontroller pin can give 10 mA. Explain, in one paragraph, how a transistor solves this, and which mode it uses.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Transistor | "A switch" or "an amplifier" | A three-terminal device whose control terminal sets the current in its main path |
| Transconductance g_m | "Gain" | ΔI_out / ΔV_in, in A/V; for a BJT, I_C / V_T |
| Voltage gain | "Gain" | ΔV_out / ΔV_in; for a simple stage −g_m R_L |
| Operating point | "Bias" | The steady voltages and currents around which the signal varies |
| Saturation (BJT) | "Fully on" | Load-limited state: V_CE near 0.1-0.2 V and I_C < β I_B |
| Cutoff | "Off" | No main current: control below its threshold |
| VCCS | "Dependent source" | Ideal element I = g_m × V_control, the simplest transistor model |

## Further Reading

- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., chapter 2 "Bipolar Transistors", sections 2.1-2.2 (the "current amplifier" and "transconductance" views).
- *All About Circuits*, Volume III, chapter 4 "Bipolar Junction Transistors", section "Introduction" and "The transistor as a switch". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-4/bipolar-junction-transistors-bjt/
- Computer History Museum, "1947: Invention of the Point-Contact Transistor" (The Silicon Engine timeline). https://www.computerhistory.org/siliconengine/invention-of-the-point-contact-transistor/
- MIT OpenCourseWare 6.002 *Circuits and Electronics*, lectures on dependent sources and amplifiers. https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/
