# The BJT as a Switch

> To use a transistor as a switch, give its base far more current than the load needs divided by β. Then β no longer matters, the transistor is "as on as it can be", and the load sees almost the full supply.

**Type:** Build
**Prerequisites:** 12-02 (The BJT); Phase 11 (Semiconductors and Diodes), lesson 07-leds; Phase 08 (Magnetism and Inductors), lesson 04-the-inductor
**Time:** ~65 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Low-side switch | A switch placed between the load and ground | A tap on the drain pipe rather than on the supply pipe |
| GPIO pin | A microcontroller's "general purpose input/output" pin, which outputs 0 V or its supply voltage (3.3 V or 5 V) and can only supply a few milliamps | A light finger that can press a button but cannot lift a box |
| Base resistor (R_B) | The resistor between the control signal and the base that sets the base current | A valve on the control line |
| Overdrive / forced β | Giving more base current than strictly needed; the ratio I_C / I_B you choose (typically 10-20) | Pushing a door harder than needed so it surely opens fully |
| V_CE(sat) | The small voltage left across a saturated transistor, about 0.05-0.3 V | The friction left in a fully open tap |
| Dissipation | Power turned into heat in the transistor: V_CE × I_C | The heat in a brake |
| Inductive load | A coil (relay, motor, solenoid) that resists changes in its current | A heavy flywheel: hard to start, hard to stop |
| Flyback diode | A diode across an inductive load that gives its current a safe path when the switch opens | A spillway for the flywheel's energy |
| Inductive kick | The huge voltage a coil produces when its current is suddenly interrupted | Water hammer when a tap is slammed shut |
| Relay | An electromagnet that closes a mechanical switch | A small hand pulling a lever that moves a big gate |
| Pull-down resistor | A resistor that holds a control input at 0 V when nothing drives it | A spring that returns a door to closed |

## Learning Objectives

- Explain why a saturated transistor makes a good switch: almost no voltage across it when on, no current when off, so very little heat in both states.
- Design the base resistor for a GPIO-driven switch with a chosen overdrive.
- Check that the design is safe for the pin and for the transistor, and robust against β variations.
- Explain the inductive kick and protect a switch with a flyback diode.

## The Problem

A microcontroller (Phase 17) decides when to turn things on, but its output pins are weak: a typical pin gives 3.3 V and should not supply more than about 8-20 mA. Yet you want to drive a 20 mA LED from 5 V, a 70 mA relay, a 200 mA buzzer, a motor. And you want the pin to remain safe even if a wire shorts.

A transistor in switch mode solves it: the pin only supplies the small base current, and the transistor routes the large load current from a separate supply. This is probably the single most common transistor circuit in hobby and industrial electronics. Done wrong, the transistor sits half-on and cooks, the LED is dim, or a relay's kick destroys the transistor the first time it turns off.

## The Physics

### Why a switch wastes little power

The power a transistor turns into heat is P = V_CE × I_C (plus a tiny V_BE × I_B). A perfect switch wastes nothing, because either the current through it is zero (off) or the voltage across it is zero (on). A transistor gets close in both states:

- **Off (cutoff)**: base at 0 V, I_C ≈ 0. P ≈ 0 whatever V_CE is.
- **On (saturated)**: V_CE ≈ 0.05-0.2 V. P = small V × the load current.
- **Half on (active)**: V_CE is several volts *and* the current is large: this is where heat is made. A switch must pass through this state quickly and never stay there.

### Saturation, physically

From lesson 02: in saturation both junctions are forward biased. The collector has been pulled down so far by the load current that it sits *below* the base. The BC junction starts injecting electrons back into the base, which costs extra base current and sets the collector current by the load rather than by β. The result: V_CE is just the difference of two diode voltages, a tenth of a volt or so.

### Why overdrive

The minimum base current for saturation is I_C / β. But β varies between parts (100-300 for a 2N3904), falls at high current and at low temperature. Designers therefore choose a **forced β** of 10-20: they supply 5-10 times the minimum base current. Then *any* transistor of that type saturates.

## The Concept

### The circuit

```
            +5 V
              |
           [R_LED] 150 Ω
              |
             LED (red)
              |
              +---- c
              |
 pin ---[R_B]--- b --|Q1  NPN, β = 100
 3.3 V        |
              e
              |
            ground
```

The LED and its resistor are the load, between the 5 V rail and the collector. The transistor is a **low-side switch**: it connects the bottom of the load to ground.

### Design, step by step

**1. Load current.** With the transistor saturated, V_CE ≈ 0.1 V. The LED takes about 1.85 V (lesson 11-07). For 20 mA:

```
R_LED = (5 − 1.85 − 0.1) / 0.020 = 152.5 Ω   →  use 150 Ω
```

**2. Minimum base current.** I_B,min = I_C / β = 20 mA / 100 = 0.20 mA.

**3. Overdrive.** Choose a forced β of 10: I_B = 20 mA / 10 = 2.0 mA.

**4. Base resistor.** The pin gives 3.3 V; the base sits about 0.7 V above ground; the resistor gets the rest:

```
R_B = (3.3 − 0.7) / 0.002 = 1300 Ω   →  use 1 kΩ  (I_B ≈ 2.6 mA)
```

**5. Check the pin.** 2.6 mA is well within a typical pin's limit (8-20 mA). ✓

### Simulated sweep of R_B

| R_B | I_B | I_C | V_CE | I_C / I_B | P transistor | State |
|---|---|---|---|---|---|---|
| 100 Ω | 25.4 mA | 20.57 mA | 0.027 V | 0.8 | 19.9 mW | saturated |
| 330 Ω | 7.74 mA | 20.48 mA | 0.040 V | 2.6 | 6.6 mW | saturated |
| **1 kΩ** | **2.56 mA** | **20.35 mA** | **0.062 V** | **7.9** | **3.1 mW** | **saturated** |
| 4.7 kΩ | 0.546 mA | 20.05 mA | 0.106 V | 36.7 | 2.5 mW | saturated |
| 10 kΩ | 0.257 mA | 19.76 mA | 0.151 V | 76.9 | 3.2 mW | saturated |
| 47 kΩ | 0.055 mA | 5.53 mA | 2.350 V | 100 | 13.1 mW | active |
| 100 kΩ | 0.026 mA | 2.62 mA | 2.826 V | 100 | 7.4 mW | active |

Read the table from the bottom up. With 100 kΩ the transistor is in its active region: I_C is exactly β × I_B = 2.6 mA, the LED is dim and V_CE is almost 3 V. At 47 kΩ, still active. At 10 kΩ the transistor just reaches saturation (I_C / I_B = 77 < 100). From there, more base current hardly changes the LED current (20.0-20.6 mA): the load is in charge. At 100 Ω the "transistor power" rises again, but that is now the *base* power: 25 mA through the base-emitter junction, which would overload the pin. The sweet spot is 1-4.7 kΩ.

### On and off

```
pin LOW : LED current  0.0000 mA   V_CE 4.235 V   transistor power   0.00 mW   pin current 0 mA
pin HIGH: LED current 20.3451 mA   V_CE 0.062 V   transistor power   3.14 mW   pin current 2.562 mA
```

Off: 4.2 V across the transistor but no current, so no heat. (The collector isn't at the full 5 V because the LED, with essentially no current, needs a little voltage to leak even a few picoamps.) On: 20 mA but only 0.062 V, so 3 mW. A 2N3904 in a TO-92 package can dissipate 625 mW: no heat sink needed.

### Robustness against β

The same design with three different transistors:

```
beta   50: LED current  20.33 mA, V_CE 0.064 V
beta  100: LED current  20.35 mA, V_CE 0.062 V
beta  300: LED current  20.35 mA, V_CE 0.060 V
```

A six-fold change in β changes the LED current by 0.1 %. That is the payoff of overdrive: **saturated switches do not care about β**. (Amplifiers do, and lesson 06 deals with that.)

### Inductive loads: the kick

A relay coil, a solenoid or a motor winding is an inductor (Phase 08): its current cannot change instantly. The voltage across an inductor is

```
V = L × dI/dt
```

Read: "the voltage equals the inductance times how fast the current changes". When the transistor turns off in a microsecond, dI/dt is enormous and the coil produces a huge voltage that tries to keep the current flowing, through the transistor if there is no other path. Our script switches a 60 Ω, 10 mH coil (a typical small relay) from 12 V:

```
without flyback diode: collector peaks at     3984.8 V when the transistor turns off
with flyback diode:    collector peaks at      12.79 V (one diode drop above 12 V)
```

Thousands of volts in the ideal simulation; in reality the transistor's collector junction breaks down at perhaps 40-60 V and is damaged after a few such events.

The cure is a **flyback diode** across the coil, cathode to the + supply:

```
        +12 V ---------+--------+
                       |        |
                     [coil]    ---  diode (cathode up, to +12 V)
                       |        ^
                       +--------+---- c
                                |
                       pin -[R_B]-|Q1
                                |
                              ground
```

While the transistor is on, the diode is reverse biased and does nothing. When it turns off, the coil's current continues around the small loop coil → diode → coil, the collector rises only to 12 V plus one diode drop (12.79 V), and the stored energy (½ L I²) is burnt slowly in the coil's own resistance. Any 1N4148 or 1N4001 does the job for small relays.

## Build It

### Step 1: The driver circuit

```python
def led_driver(base_ohms, pin_volts=PIN_HIGH, led_ohms=150.0):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", SUPPLY)
    circuit.voltage_source("PIN", "pin", "0", pin_volts)
    circuit.resistor("RB", "pin", "b", base_ohms)
    circuit.resistor("RLED", "vcc", "a", led_ohms)
    circuit.led("D1", "a", "c", color="red")
    circuit.npn("Q1", c="c", b="b", e="0", beta=BETA)
    return circuit.dc()
```

### Step 2: The design numbers

`show_design` prints steps 1-4 of the Concept section with the arithmetic.

### Step 3: Sweeps and robustness

`show_sweep` loops over base resistors and labels each result "saturated" when V_CE < 0.3 V. `show_on_off` compares the two pin levels, and `show_beta_spread` rebuilds the circuit with β = 50, 100 and 300.

### Step 4: The inductive kick

```python
circuit.pulse_source("PIN", "pin", "0", low=0.0, high=PIN_HIGH, period=4e-3, duty=0.5)
circuit.resistor("RM", "vcc", "m", 60.0)
circuit.inductor("LM", "m", "c", 10e-3, i0=0.0)
circuit.npn("Q1", c="c", b="b", e="0", beta=BETA)
unprotected = circuit.transient(t_stop=4e-3, dt=1e-6)
circuit.diode("DF", "c", "vcc")
protected = circuit.transient(t_stop=4e-3, dt=1e-6)
```

The pin turns the transistor on for 2 ms (the coil current builds up to 12/60 = 200 mA with time constant L/R = 0.17 ms) and then off. We run it once, add the diode, and run it again.

```
uv run python phases/12-transistors/03-the-bjt-as-a-switch/code/main.py
```

## Use It

- **Arduino / ESP32 / Raspberry Pi projects**: "NPN + 1 kΩ base resistor + flyback diode" is the standard way to drive relays, buzzers and LED strips. A Raspberry Pi pin (3.3 V, about 16 mA max) driving a 5 V relay module is exactly this circuit.
- **Relay modules** sold for microcontrollers contain a small NPN (often an S8050 or 2N3904), a base resistor, a flyback diode (1N4148) and an indicator LED.
- **Darlington arrays** like the ULN2003 contain seven pairs of transistors (two BJTs in cascade, total β around 1000) with built-in base resistors and flyback diodes, for driving stepper motors from logic pins. Their V_CE(sat) is about 1 V, a cost of the cascade.
- **Datasheet numbers to check**: maximum I_C (200 mA for a 2N3904, 600 mA for a 2N2222, 1.5 A for an S8050), V_CE(sat) at your I_C and I_B (given with a forced β of 10 in most datasheets, the same choice we made), maximum V_CEO, and total power dissipation.
- **When a BJT is the wrong choice**: above a few hundred milliamps, the base current becomes significant and V_CE(sat) × I_C heats the part. Logic-level MOSFETs (lesson 05) take over.

## Try It in the Lab

The lab is the LED driver from the Concept section: 3.3 V pin, 5 V rail, red LED with 150 Ω, NPN with β = 100. You choose the base resistor. Three goals: the LED gets at least 15 mA, the transistor is saturated, and the pin supplies less than 8 mA.

Think about: the minimum base current for 20 mA, how much overdrive is sensible, and what each wrong choice violates. Which goal does a very small base resistor break? A very large one?

## Common Mistakes

- **No base resistor.** The base-emitter junction is a diode: a pin driving it directly forces large current, overloading the pin and possibly the transistor.
- **Using β from the datasheet's best case.** Design with a forced β of 10-20 and you never need to know the real value.
- **Putting the load between emitter and ground with an NPN** ("high side" with an NPN). The emitter then follows the base minus 0.7 V, so with a 3.3 V pin the load sees at most 2.6 V and the transistor is never saturated. Use the low-side arrangement, or a pnp/P-MOSFET for high-side switching.
- **Forgetting the flyback diode on relays and motors.** It may work for a while; then the transistor dies.
- **Flyback diode backwards.** Installed with the cathode to the collector, it shorts the supply through the transistor when it turns on.
- **Leaving the base floating.** If the pin is not yet configured (during reset), the base can pick up noise. A 10-100 kΩ pull-down from base to emitter keeps the transistor firmly off.

## Exercises

1. Design a switch for a 12 V, 150 mA buzzer from a 5 V logic pin with a 2N2222 (β min 50). Use a forced β of 10. What base resistor? What pin current?
2. In the sweep table, at which R_B does the transistor dissipate the most heat? Why is it in the middle of the range?
3. A relay coil has 70 Ω and 20 mH and runs on 5 V. What current flows when on? What energy is stored in the coil, ½ L I²? Where does it go with a flyback diode?
4. Replace the red LED by three white LEDs in series (3.1 V each) on a 12 V rail. Redesign R_LED for 20 mA and R_B for a 3.3 V pin.
5. Add a 47 kΩ pull-down from base to ground in `led_driver`. Does the 1 kΩ design still saturate? What is the smallest R_B for which it would stop working?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Low-side switch | "NPN switch" | Transistor between the load and ground; the load connects to the positive rail |
| Saturation | "Fully on" | V_CE ≈ 0.05-0.3 V, the load sets I_C |
| Forced β | "Overdrive" | The ratio I_C / I_B you design for (10-20) to guarantee saturation |
| V_CE(sat) | "Saturation voltage" | Collector-emitter voltage of a saturated BJT at stated I_C and I_B |
| Flyback diode | "Freewheeling diode", "snubber diode" | Diode across an inductive load that carries its current when the switch opens |
| Inductive kick | "Back-EMF spike" | The voltage V = L dI/dt produced when a coil's current is interrupted |
| Dissipation | "How hot it gets" | P = V_CE × I_C (+ V_BE × I_B), mostly during switching for a good switch |

## Further Reading

- *All About Circuits*, Volume III, chapter 4, "The transistor as a switch". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-4/transistor-switch-bjt/
- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., section 2.2.1 "Transistor switch" and 1.6.7 "Inductive loads and diode protection".
- SparkFun tutorial, "Transistors" (switch applications and base-resistor sizing). https://learn.sparkfun.com/tutorials/transistors
- Texas Instruments ULN2003A datasheet (Darlington arrays with built-in flyback diodes). https://www.ti.com/product/ULN2003A
