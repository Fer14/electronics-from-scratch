# The MOSFET as a Switch

> A fully-on MOSFET is just a small resistor, R_DS(on). Give its gate enough voltage, give the gate a path to discharge, give the motor's current a path when you switch off, and a 3.3 V pin can run amps.

**Type:** Build
**Prerequisites:** 12-03 (The BJT as a Switch), 12-04 (The MOSFET); Phase 07 (Capacitors), lesson 04-the-time-constant; Phase 08 (Magnetism and Inductors), lessons 04-the-inductor and 07-motors-and-generators
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| R_DS(on) | The drain-source resistance of a fully-on MOSFET, usually milliohms | The width of a fully open gate in a fence: wider means less squeezing |
| Logic-level MOSFET | A power MOSFET designed to be fully on with only 2.5-5 V on its gate | A door that opens with a light push |
| Standard MOSFET | A power MOSFET specified at V_GS = 10 V, with a threshold of 2-4 V | A heavy door that needs a firm shove |
| Gate resistor (R_G) | A small resistor between the driver and the gate, which limits the charging current | A narrowing in the pipe that fills a tank |
| Pull-down resistor | A large resistor from gate to source that discharges the gate when nothing drives it | A spring that closes the door when you let go |
| Gate charge / gate capacitance | The charge that must be put on the gate to turn the MOSFET on | The water needed to fill the tank before the float rises |
| Switching loss | Energy turned into heat while the MOSFET passes through its half-on state | The friction heat each time a heavy door swings |
| Conduction loss | Heat in the fully-on MOSFET: I² × R_DS(on) | The steady effort of pushing water through the open gate |
| Avalanche | Breakdown of the MOSFET's drain-body junction when the drain voltage exceeds its rating | A dam overflowing |
| Flyback (freewheeling) diode | A diode that carries an inductive load's current when the switch opens | A bypass channel for a river when the sluice closes |
| Back-EMF | The voltage a spinning motor generates, opposing the supply (Phase 08) | A turbine pushing back against the water |

## Learning Objectives

- Compute R_DS(on) from the overdrive and predict the MOSFET's conduction loss.
- Choose between a logic-level and a standard MOSFET for a given gate voltage.
- Explain why a gate must never float, and why a gate resistor and pull-down form a divider.
- Estimate switching time from the gate RC and explain switching loss.
- Protect a MOSFET from an inductive load with a flyback diode, and quantify the energy involved.

## The Problem

A small 12 V DC motor (a fan, a pump, a toy car) can draw 2 A. A BJT switch (lesson 03) would need 100-200 mA of base current for a forced β of 10-20: far more than any microcontroller pin. A BJT also drops 0.2-0.5 V when saturated at amps, wasting a watt.

A MOSFET needs no steady gate current at all, and a good power MOSFET is fully on with a resistance of a few tens of milliohms. That is why every motor driver, LED driver, battery protection circuit and power converter uses MOSFETs. But a MOSFET switch has its own traps: a gate voltage that is "high" but not high enough, a gate left floating, a gate charged too slowly, and the inductive kick of the motor. This lesson works through each with numbers.

## The Physics

### Fully on means triode

From lesson 04: a MOSFET with a small V_DS is in its triode region and behaves like a resistor

```
R_DS(on) ≈ 1 / ( k × (V_GS − V_th) )
```

Read: "the on-resistance is one over k times the overdrive". Power MOSFETs are built with enormous effective gate widths (millions of tiny cells in parallel), so k is huge: amperes per volt squared rather than milliamperes. We use k = 5 A/V².

### Why gate voltage matters so much

The on-resistance depends on the **overdrive**. Same k, two thresholds:

| V_GS | Logic-level (V_th = 1.5 V) | Standard (V_th = 3.5 V) |
|---|---|---|
| 2.0 V | 400 mΩ | off |
| 3.3 V | 111 mΩ | off |
| 5.0 V | 57 mΩ | 133 mΩ |
| 10 V | 23.5 mΩ | 30.8 mΩ |

A 3.3 V pin turns the logic-level part well on and leaves the standard part completely off. At 5 V the standard part is *partly* on: the dangerous case.

What our simple model leaves out: real power MOSFETs have extra fixed resistance (in the package, the drift region), so R_DS(on) flattens out at high V_GS instead of falling forever, and the threshold falls as the part heats up.

### The gate is a capacitor that must be charged

Turning the MOSFET on means charging its gate capacitance (a few hundred picofarads to several nanofarads for power parts) to well above V_th. Through a resistance R_G, that takes a few time constants τ = R_G × C_G (Phase 07). While the gate voltage passes through the threshold region, the MOSFET is half on: it has both voltage across it and current through it, and heats up. Fast switching means less of this **switching loss**.

### Inductive loads, again

A motor winding is an inductor in series with a resistance (and, when spinning, a back-EMF). As in lesson 03, interrupting its current produces V = L dI/dt. The difference here: power MOSFETs are rated to **avalanche**. Their drain-body junction breaks down at a voltage above their rating (for a "60 V" MOSFET, perhaps 65-70 V) and can absorb a limited amount of energy, the datasheet's "E_AS" (single-pulse avalanche energy). Relying on it is bad practice; a flyback diode is cheap.

## The Concept

### The motor switch

```
          +12 V
            |
         [motor]  modelled as 6 Ω (2 A)
            |
            +---- d
            |
 pin --[R_G]--+-- g --|M1  N-channel, logic level
 3.3 V        |       |
           [R_PD]     s
           100 kΩ     |
              |       |
            ground --+
```

### Logic-level versus standard: simulated

| MOSFET | Pin | V_GS | Motor current | V_DS | P MOSFET | P motor |
|---|---|---|---|---|---|---|
| logic-level | 3.3 V | 3.30 V | 1.961 A | 0.233 V | 0.458 W | 23.1 W |
| logic-level | 5.0 V | 5.00 V | 1.981 A | 0.115 V | 0.228 W | 23.5 W |
| logic-level | 10 V | 9.99 V | 1.992 A | 0.047 V | 0.094 W | 23.8 W |
| standard | 3.3 V | 3.30 V | 0.000 A | 12.000 V | 0 | 0 |
| standard | 5.0 V | 5.00 V | 1.952 A | 0.289 V | 0.564 W | 22.9 W |
| standard | 10 V | 9.99 V | 1.990 A | 0.062 V | 0.123 W | 23.8 W |

Check the first row by hand. R_DS(on) = 1 / (5 × (3.3 − 1.5)) = 0.111 Ω. Total resistance 6 + 0.111 = 6.111 Ω; current 12 / 6.111 = 1.964 A (simulator 1.961 A, because the triode formula's V_DS²/2 term raises the effective resistance a little). Conduction loss: I² × R = 1.96² × 0.119 ≈ 0.46 W ✓.

Is 0.46 W a lot? A TO-220 package without a heat sink rises about 60-70 °C per watt above ambient: 0.46 W means roughly +30 °C. Fine. In a small SOT-23 package (about 100-250 °C/W) it would be too hot.

### The divider trap: gate resistor and pull-down

The pull-down R_PD (100 kΩ) keeps the gate at 0 V when the pin is not driving, for example during reset when the pin is still an input. But together with the gate resistor it forms a voltage divider:

```
V_GS = V_pin × R_PD / (R_G + R_PD)
```

| Gate resistor | V_GS | Motor current | MOSFET power |
|---|---|---|---|
| 100 Ω | 3.30 V | 1.961 A | 0.458 W |
| 100 kΩ | 1.65 V | 0.056 A | 0.656 W |
| 1 MΩ | 0.30 V | 0.000 A | 0 |

With 100 kΩ the gate only reaches 1.65 V, 0.15 V above threshold. In saturation, I_D = (5/2) × 0.15² = 56 mA: the motor barely twitches, but the MOSFET has 11.7 V across it and dissipates 0.66 W, *more* than when fully on while doing nothing useful. **The gate resistor must be small (10-100 Ω) and the pull-down large (10-100 kΩ).**

### Why a floating gate is dangerous

If neither the pin nor a pull-down defines the gate, the gate capacitor keeps whatever charge it last had, or picks up charge from nearby signals and from the drain through the drain-gate capacitance. The MOSFET can sit half on, getting hot, or turn on randomly when you touch the circuit. A pull-down makes the default state "off".

### Switching speed

Model the gate as a 2 nF capacitor, step the pin from 0 to 3.3 V, and vary R_G:

| R_G | τ = R_G × C_G | Drain below 1 V after | Switching energy |
|---|---|---|---|
| 10 Ω | 20 ns | 30 ns | 4.6 µJ |
| 100 Ω | 200 ns | 255 ns | 5.0 µJ |
| 1000 Ω | 2000 ns | 2505 ns | 8.9 µJ |

The drain falls once the gate passes the threshold and gets some overdrive, after about 1.25-1.5 τ here. The switching energy is the integral of V_DS × I_D over the run (10 µs), so it also includes the conduction loss over that window, about 4.6 µJ for 0.46 W × 10 µs; the *extra* energy from slow switching is the difference: almost nothing at 10 Ω, about 4 µJ at 1 kΩ. Per switching event that seems small, but at 20 kHz PWM (Phase 17), 4 µJ × 20,000 = 80 mW extra; in a 100 kHz converter at 20 A it becomes watts. This is why power converters use dedicated **gate driver** chips that push amps into the gate. (A real gate also shows a "Miller plateau", where the gate voltage stalls while the drain voltage falls; our simple model leaves it out.)

### The inductive kick, quantified

Now a motor winding: 6 Ω in series with 1 mH, switched off after 1 ms. We give the MOSFET a realistic avalanche limit (a zener-like breakdown at 60 V):

```
without flyback diode: drain peaks at  60.77 V, energy dumped into the MOSFET's avalanche  2.060 mJ
with flyback diode   : drain peaks at  12.85 V, energy dumped into the MOSFET's avalanche  0.000 mJ
energy stored in the winding at turn-off: 0.5 L I^2 = 0.5 x 1e-3 x 1.957^2 = 1.915 mJ
```

Without the diode, the drain flies up until the MOSFET avalanches and the winding's stored energy, ½ L I² ≈ 1.9 mJ, plus a little more pushed in by the supply while the current dies away, is burnt *inside the MOSFET*. At 20 kHz that would be 40 W: instant death. With a flyback diode from drain to +12 V, the drain stops one diode drop above the supply and the energy recirculates harmlessly through the winding's resistance.

For motors driven with PWM, the flyback diode conducts every cycle; use a fast diode (Schottky such as an SS34 or 1N5819) rated for the motor current.

## Build It

### Step 1: The switch circuit

```python
def motor_switch(gate_volts, vth, k, gate_ohms=100.0, pulldown_ohms=100e3):
    circuit = Circuit()
    circuit.voltage_source("VM", "vm", "0", MOTOR_SUPPLY)
    circuit.voltage_source("PIN", "pin", "0", gate_volts)
    circuit.resistor("RG", "pin", "g", gate_ohms)
    circuit.resistor("RPD", "g", "0", pulldown_ohms)
    circuit.resistor("RM", "vm", "d", MOTOR_OHMS)
    circuit.nmos("M1", d="d", g="g", s="0", vth=vth, k=k)
    return circuit.dc()
```

### Step 2: Tables

`show_on_resistance` evaluates 1/(k V_ov); `show_motor` simulates both MOSFET types at three gate voltages; `show_pulldown` tries three gate resistors.

### Step 3: Gate charging

```python
circuit.pulse_source("PIN", "pin", "0", low=0.0, high=3.3, period=20e-6, duty=0.5)
circuit.resistor("RG", "pin", "g", gate_ohms)
circuit.capacitor("CG", "g", "0", 2e-9)
```

The 2 nF capacitor stands in for the gate capacitance (our simulator's MOSFET model itself has none). The script finds the first time the drain drops below 1 V and integrates the MOSFET's power.

### Step 4: The winding and its kick

```python
circuit.pulse_source("PIN", "g", "0", low=0.0, high=3.3, period=2e-3, duty=0.5, rise=1e-6, fall=1e-6)
circuit.resistor("RM", "vm", "x", MOTOR_OHMS)
circuit.inductor("LM", "x", "d", 1e-3, i0=0.0)
circuit.nmos("M1", d="d", g="g", s="0", **params)
circuit.zener("ZAV", "0", "d", vz=60.0, nz=5.0)
```

The zener from source (ground) to drain plays the MOSFET's own avalanche breakdown at 60 V; `nz=5.0` gives it a softer knee, more like a real avalanche. Then the run is repeated with `circuit.diode("DF", "d", "vm")`.

```
uv run python phases/12-transistors/05-the-mosfet-as-a-switch/code/main.py
```

## Use It

- **Choosing a part**: check that R_DS(on) is specified at *your* gate voltage (look for "R_DS(on) @ V_GS = 2.5 V" or "4.5 V" for 3.3 V/5 V logic), that V_DS(max) is at least 1.5-2× your supply, and that I_D(max) and the package's thermal resistance handle the conduction loss. Examples: AO3400 (30 V, SOT-23, ~30 mΩ at 4.5 V), IRLZ44N (55 V, TO-220, 22 mΩ at 5 V), IRLB8721 (30 V, ~9 mΩ at 4.5 V). The popular IRF540N is a *standard* part: 44 mΩ at 10 V, and unreliable from 3.3 V.
- **Gate drivers**: TC4420, UCC27511 and similar chips take a logic signal and drive the gate with amps, for fast switching. Half-bridge drivers like the IR2110 also handle the "high-side" MOSFET whose source is not at ground.
- **H-bridges** (Phase 18) use four MOSFETs to run a motor in both directions; each MOSFET's body diode often acts as the flyback diode.
- **LED strips**: a single logic-level MOSFET per colour channel, driven by PWM from a microcontroller, is the standard RGB strip controller.
- **Reverse-polarity protection**: a P-MOSFET in the supply line, turned on only when the battery is connected the right way round, replaces a lossy series diode.

## Try It in the Lab

The lab is the motor switch: 12 V, a 6 Ω motor, a logic-level MOSFET (V_th = 1.5 V), a 100 kΩ pull-down, and a 3.3 V pin. You choose the gate resistor. Goals: at least 1.8 A in the motor and less than 0.6 W in the MOSFET.

Think about: the gate draws no current, so why does the gate resistor matter at all? Compute V_GS for each choice from the divider. Which choice leaves the MOSFET half on, and why is that the worst case for heat?

## Common Mistakes

- **Using a standard MOSFET from a 3.3 V pin.** It is off or half on. Use a logic-level part, or a gate driver.
- **Reading V_th as "fully on".** V_th is where the MOSFET *starts* to conduct (at about 250 µA). Look at R_DS(on) at your V_GS.
- **No pull-down.** During reset or when the controller is unplugged, the gate floats and the motor may run or the MOSFET may cook.
- **Big gate resistor.** Slow switching heats the MOSFET, and with a pull-down it can prevent full turn-on.
- **No flyback diode on motors, solenoids, relays.** The avalanche energy can destroy the part on the first switch-off.
- **Forgetting the ground connection.** The pin's ground and the motor supply's ground must be connected, or V_GS is undefined.
- **Ignoring heat.** P = I² R_DS(on): at 10 A even 20 mΩ is 2 W, which needs a heat sink.

## Exercises

1. A logic-level MOSFET has R_DS(on) = 25 mΩ at V_GS = 4.5 V and carries 8 A. What is its conduction loss? With a thermal resistance of 62 °C/W (TO-220, no heat sink) and 25 °C ambient, how hot does it get?
2. With k = 5 A/V² and V_th = 1.5 V, what gate voltage gives R_DS(on) = 50 mΩ?
3. A gate resistor of 1 kΩ and a pull-down of 10 kΩ are driven from 3.3 V. What is V_GS? Would the logic-level part be fully on?
4. A solenoid has 24 Ω and 50 mH and runs on 24 V. How much energy does it store? If switched 10 times a second without a flyback diode, how much power would the MOSFET's avalanche absorb?
5. In `show_gate_charging`, change the gate capacitance to 10 nF. Predict the turn-on time for each gate resistor before running.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| R_DS(on) | "On-resistance" | Drain-source resistance when fully on; roughly 1/(k(V_GS − V_th)) plus fixed parts |
| Logic-level | "LL MOSFET" | Specified fully on at V_GS = 2.5-5 V |
| Gate resistor | "R_G" | Limits gate charging current and ringing; small values (10-100 Ω) |
| Pull-down | "Gate-source resistor" | Large resistor (10-100 kΩ) that holds the gate off when undriven |
| Conduction loss | "I²R loss" | I_D² × R_DS(on) while on |
| Switching loss | "Transition loss" | Energy lost while V_DS and I_D are both large during switching |
| Avalanche energy | "E_AS" | Energy the drain-body junction can absorb in breakdown before failing |
| Flyback diode | "Freewheel diode" | Gives an inductive load's current a path when the switch opens |

## Further Reading

- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., section 3.4-3.5 (power MOSFETs, switching, gate drive).
- Infineon IRLZ44N datasheet: R_DS(on) versus V_GS, gate charge, avalanche energy. https://www.infineon.com/cms/en/product/power/mosfet/n-channel/irlz44n/
- Texas Instruments, "Fundamentals of MOSFET and IGBT Gate Driver Circuits" (application report SLUA618). https://www.ti.com/lit/an/slua618a/slua618a.pdf
- *All About Circuits*, Volume III, chapter 6, "Enhancement-type IGFETs" and "Active-mode operation". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-6/enhancement-type-igfets/
