# Schematic

> The schematic is the contract between the idea and the board. Every wire on it must have a reason, and every reason must survive a simulation.

**Type:** Build
**Prerequisites:** Phase 22 (Capstone), Lessons 01-02; Phase 00 (Meet Electricity), Lesson 07 (Your First Schematic); Phase 05 (Circuit Analysis and Our Simulator); Phase 12 (Transistors), Lesson 03 (The BJT as a Switch); Phase 17 (Microcontrollers), Lessons 02 (GPIO) and 04 (ADC and DAC)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Reference designator | The label of a part on the schematic and board: R1, C3, U2, Q1, D1 | A seat number in a theatre |
| BOM (bill of materials) | The list of every part, with value, package and quantity | A shopping list for the factory |
| Net name | A name given to a wire so it can be found on every page and on the board | A street name |
| Pin (of a chip) | One electrical connection of a part, named like PB1 or VCC | One door of a building |
| GPIO / ADC pin | A microcontroller pin used as a digital output or input, or as an analog input | A door that can be a shop entrance or a letterbox |
| Decoupling capacitor | A capacitor next to a power pin that supplies fast current bursts (Phase 21, Lesson 03) | A small water tank on the roof |
| Saturation (BJT) | The transistor fully on, with only about 0.1 V between collector and emitter | A tap opened all the way |
| Forced beta | The ratio of collector current to the base current we actually give: lower than the transistor's gain means it is driven hard into saturation | Pushing a door harder than needed so it surely opens |
| Operating point | The DC voltages and currents of a circuit in one state | A snapshot of the circuit in one moment |
| Design review | Checking a schematic against the requirements and the rules before the board is made | Proofreading with a checklist |
| Pin current limit | The most current a microcontroller pin may source or sink safely | The weight limit of a shelf |

## Learning Objectives

- Read the complete schematic of the night light and explain the purpose of every part.
- Write the netlist (every pin on every net) and check it for mistakes such as a pin on two nets.
- Simulate the operating points of the light input across a whole day of light levels and of the battery input across its voltage range.
- Size the transistor's base resistor so that the transistor saturates without overloading the microcontroller pin.
- Check every part against its ratings (power, current, voltage) and every requirement that can be checked in DC.

## The Problem

Lesson 02 decided the blocks. Now every block becomes real parts with real values, connected pin by pin. This is where most hardware bugs are born: a resistor ten times too big, a missing decoupling capacitor, a pin connected to the wrong net, a transistor that is only half on. On a breadboard you would find them by trial and error. On a board, each costs a new board.

So we draw the schematic, write its netlist, and then simulate every state the device can be in: dark and bright, fresh and empty batteries, LED on and off. If any number is outside its limits, we fix the schematic now, when a change costs nothing.

## The Physics

### The transistor as a switch, sized properly

The NPN transistor switches the LED (Phase 12, Lesson 03). In its active region, its collector current is `beta` times its base current, where `beta` is about 100 for our transistor. As a switch we want it *saturated*: fully on, with only about 0.1 V from collector to emitter, so that the LED's current is set by the LED resistor and not by the transistor.

To be sure of saturation, we give the base more current than the minimum `I_C / beta`:

```
I_B(min) = I_C / beta = 19 mA / 100 = 0.19 mA
```

The usual rule is a **forced beta** of about 10-20: `I_B ≈ I_C / 15 ≈ 1.3 mA`. That covers transistors whose gain is lower than typical (beta varies by a factor of 2-3 between samples and with temperature). The base resistor sets this current from the microcontroller's 3.3 V output, minus the base-emitter voltage of about 0.7 V:

```
R_B = (3.3 V - 0.7 V) / 1.2 mA ≈ 2.2 kΩ
```

With 22 kΩ the base current would be only `2.6 / 22,000 = 0.12 mA`, enough for at most `100 * 0.12 = 12 mA`: the transistor would limit the LED and run warm with several volts across it. With 47 Ω the pin would have to supply `2.6 / 47 = 55 mA`, far more than a microcontroller pin can give (typically 20 mA or less), and the base-emitter junction would waste it all.

### Ratings: power, current, voltage

Every part has limits (Phase 03, Lesson 06):

- **Resistors**: power. `P = I^2 R`. An 0805 chip resistor is typically rated 125 mW.
- **Transistors**: collector current, collector-emitter voltage and power (`V_CE * I_C`). A small SOT-23 transistor such as the MMBT3904 handles 200 mA and about 225-350 mW depending on the board.
- **LEDs**: forward current (typically 20-30 mA continuous for a small white LED).
- **Microcontroller pins**: source or sink current, typically up to 10-20 mA per pin with a total limit per chip.

## The Concept

### The complete schematic

```
                                  VBAT (3.6-4.5 V)
   BT1 3xAA ---+-------------+-------------+--------------------------------------+
     (+)       |             |             |                                      |
               |           C1 1µF       R2 470k                                R5 68Ω
               |             |             |                                      |
               |            GND        BAT_SENSE ---+----> U2.ADC1                LED_A
               |                           |        |                             |
               |                        R3 470k   C4 100nF                      D1 white LED
               |                           |        |                             |
               |                          GND      GND                          LED_K
               |                                                                  |
               +--> U1 LDO IN       OUT ---+--- VDD 3.3 V ---> U2.VCC          Q1 NPN (C)
                    (MCP1700)       GND    |                                      |
                                     |   C2 1µF   C3 100nF                 (B) ---+--- BASE --- R4 2.2k --- PWM <--- U2.PB1
                                    GND    |        |                             |
                                          GND      GND                          (E) GND

        U2.PB2 ---> LDR_PWR ---[ LDR1 ]--- LIGHT ---+----> U2.ADC0
                                                     |
                                                  R1 10k
                                                     |
                                                    GND

   BT1 (-) --- GND --- U1.GND --- U2.GND
```

Every part has a job that traces back to a requirement:

| Part | Job | Requirement |
|---|---|---|
| BT1 | three AA cells, 3.6-4.5 V | R4, R6 |
| U1, C1, C2 | LDO making a steady 3.3 V with 1.6 µA quiescent current; its datasheet asks for 1 µF on each side for stability | R4 |
| C3 | 100 nF decoupling right at the microcontroller's supply pin | reliable operation |
| U2 | microcontroller: sleeps, wakes each second, measures, decides, drives PWM | R1, R2, R3, R5 |
| LDR1, R1 | light sensor divider, powered from PB2 only during measurements | R1, R4 |
| R2, R3, C4 | battery sense (4.5 V becomes 2.25 V), 4.8 µA; C4 holds the voltage steady for the ADC's sampling | R5 |
| R4, Q1 | low-side switch: PB1 drives the base through 2.2 kΩ | R3 |
| R5, D1 | LED and its current-setting resistor, about 19 mA at 4.5 V | R3 |

### The netlist

Names make the schematic checkable. Each net lists every pin on it:

```
VBAT      BT1.+, U1.IN, C1.1, R2.1, R5.1
VDD       U1.OUT, C2.1, C3.1, U2.VCC
LDR_PWR   U2.PB2, LDR1.1
LIGHT     LDR1.2, R1.1, U2.ADC0
BAT_SENSE R2.2, R3.1, C4.1, U2.ADC1
PWM       U2.PB1, R4.1
BASE      R4.2, Q1.B
LED_A     R5.2, D1.A
LED_K     D1.K, Q1.C
GND       BT1.-, U1.GND, C1.2, C2.2, C3.2, U2.GND, R1.2, R3.2, C4.2, Q1.E
```

10 nets and 36 pin connections. A simple automatic check: no pin may appear on two nets (that would be a short between them). Lesson 05 uses this netlist to lay out the board.

### Operating points: the light input

With the battery at 4.2 V and the LED off, the simulator gives the light input across a day:

| Light | LDR | ADC0 voltage | ADC code |
|---|---|---|---|
| 0.2 lux (moonlight) | 154.6 kΩ | 0.200 V | 62 |
| 1 lux | 50.1 kΩ | 0.549 V | 170 |
| 5 lux (switch on) | 16.25 kΩ | 1.256 V | 389 |
| 10 lux | 10.0 kΩ | 1.648 V | 511 |
| 15 lux (switch off) | 7.53 kΩ | 1.880 V | 583 |
| 50 lux | 3.24 kΩ | 2.488 V | 771 |
| 400 lux (office) | 0.76 kΩ | 3.061 V | 949 |

The thresholds land at codes 389 and 583, one code below Lesson 01's 390 and 584: the pin that powers the divider has about 25 Ω of output resistance, which steals a few millivolts. It is a reminder that "ideal" sources are approximations, and a sign that the margin is comfortable (a 1-code shift does not matter when the thresholds are 194 codes apart).

### Operating points: the battery input

The 470 kΩ / 470 kΩ divider halves the battery voltage:

| Battery | ADC1 | Code |
|---|---|---|
| 4.5 V | 2.250 V | 697 |
| 4.2 V | 2.100 V | 651 |
| 3.9 V | 1.950 V | 604 |
| 3.6 V | 1.800 V | 558 |

The firmware converts back with `V_battery = code / 1023 * 3.3 * 2`. Unlike the light input, this one is *not* ratiometric: it compares the battery with the 3.3 V reference, so it relies on the LDO's accuracy (typically ±2-3%).

### The LED driver, worst case

With a fresh battery and the PWM pin high:

```
LED current       18.80 mA      (requirement: about 19 mA)
LED voltage       3.133 V
base current      1.154 mA      (forced beta 16.3: saturated)
V_CE              80 mV         (saturated: the transistor is a closed switch)
R5 power          24.0 mW       (0805 rating 125 mW: 19% of its rating)
Q1 power          1.5 mW        (rating about 225 mW)
pin PB1 current   1.15 mA       (limit about 20 mA)
```

Every number is comfortably inside its rating. With the PWM pin low, the LED current is essentially zero: the switch is off. Since the LED is pulsed at 30-84% duty, the average power is even lower than these "fully on" numbers.

### The requirement checks we can do in DC

- **R1**: thresholds at codes 389 and 583, far apart. Pass.
- **R6**: the highest node voltage on the board is the battery's 4.49 V. Pass.
- R2, R3 and R5 need time (averaging, PWM, battery compensation): Lesson 04.

## Build It

Run:

```
uv run python phases/22-capstone/03-schematic/code/main.py
```

### Step 1: The BOM

`PARTS` maps each reference designator to its description; the script prints it.

### Step 2: The netlist and a check

```python
all_pins = [p for pins in NETS.values() for p in pins]
print(f"  {len(NETS)} nets, {len(all_pins)} pin connections, no pin on two nets: {len(all_pins) == len(set(all_pins))}")
```

If a pin appeared twice, the list would be longer than the set of unique pins.

### Step 3: The whole circuit in the simulator

```python
def night_light(lux, vbat, pwm_high):
    c = Circuit("night light")
    c.voltage_source("BAT", "bat_ideal", "0", vbat)
    c.resistor("R_INT", "bat_ideal", "vbat", R_INTERNAL)
    c.voltage_source("U1", "vdd", "0", VDD)
    c.voltage_source("PB2", "pb2_ideal", "0", VDD)
    c.resistor("R_PB2", "pb2_ideal", "ldr_pwr", PIN_OHMS)
    c.resistor("LDR1", "ldr_pwr", "light", ldr_ohms(lux))
    c.resistor("R1", "light", "0", 10e3)
    c.resistor("R2", "vbat", "bat_sense", 470e3)
    c.resistor("R3", "bat_sense", "0", 470e3)
    c.voltage_source("PB1", "pb1_ideal", "0", VDD if pwm_high else 0.0)
    c.resistor("R_PB1", "pb1_ideal", "pwm", PIN_OHMS)
    c.resistor("R4", "pwm", "base", 2.2e3)
    c.npn("Q1", c="led_k", b="base", e="0", beta=100)
    c.resistor("R5", "vbat", "led_a", 68)
    c.led("D1", "led_a", "led_k", color="white")
    return c.dc()
```

Simplifications, stated honestly: the LDO is an ideal 3.3 V source (its dropout at our 1 mA is tens of millivolts, far inside the 3.6 V minimum battery); the microcontroller's pins are ideal sources with 25 Ω of output resistance; capacitors are left out because they carry no current at DC. One function covers every state, by its three arguments.

### Steps 3-5: The operating points

The light sweep, the battery sweep and the LED driver numbers in the tables above.

### Step 6: Requirement checks

The threshold codes and the maximum node voltage.

### Step 7: The lab

The script evaluates each base resistor offered in the lab.

## Use It

- **Schematic capture** in KiCad, Altium or similar draws the same thing with symbols, assigns footprints (Phase 21, Lesson 02) and exports the netlist for the board.
- **Electrical rules check (ERC)** in those tools finds unconnected pins, outputs driving outputs and missing power, the automated cousin of our "no pin on two nets" check.
- **Design reviews** go through the schematic part by part with a checklist: ratings, decoupling, pull-ups, programming access, test points, polarity of every diode and capacitor.
- **Programming header.** A real board would add a small connector for programming the microcontroller (for example the UPDI pin of newer ATtinys, or ISP on older ones). We leave it as an exercise.
- **Datasheet values.** The 1 µF capacitors around the LDO, the maximum pin current and the transistor's power rating all come from datasheets. Always read the "absolute maximum ratings" and "recommended operating conditions" tables.

## Try It in the Lab

Open "Choose the transistor's base resistor". With the PWM pin high (3.3 V), the LED must get 15-20 mA and the pin must supply at most 5 mA. Four resistors are offered: 100 kΩ, 22 kΩ, 2.2 kΩ and 47 Ω. For each, compute the base current `(3.3 - 0.7) / R` and the most the transistor could pass (`100` times that). Which ones starve the LED, and which one overloads the pin?

## Common Mistakes

- **Driving a BJT with just enough base current.** Gains vary; design for a forced beta of 10-20 so it saturates in every sample.
- **Forgetting the pin's limits.** A microcontroller pin is not a power supply. A small base resistor can exceed its current rating.
- **Leaving out decoupling and LDO capacitors.** Many LDOs oscillate without their specified capacitors, and microcontrollers reset on supply glitches.
- **High-value dividers straight into an ADC.** A 235 kΩ source (two 470 kΩ in parallel) cannot charge the ADC's sampling capacitor quickly; the 100 nF capacitor C4 fixes it.
- **Checking only one state.** A circuit that works with a fresh battery in the dark may fail with an empty battery or in daylight. Sweep every condition.

## Exercises

1. What base resistor would give a forced beta of exactly 10 for 19 mA? Pick the nearest standard value from the E12 series (1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2).
2. At 3.6 V with the LED on, compute by hand the LED current (use 3.05 V for the LED and 0.08 V for the transistor) and R5's power.
3. What is the Thevenin resistance seen by ADC1 (the two 470 kΩ in parallel)? If the ADC's sampling capacitor is 14 pF and must charge for 10 time constants, how long would it take without C4?
4. Add a programming header (3 pins: VDD, GND, UPDI) to `NETS` and `PARTS` in the script. Which existing nets does it join?
5. Harder: replace Q1 by an N-channel MOSFET in `night_light` (`c.nmos(..., vth=1.5, k=0.1)`, gate on the PWM net through 100 Ω). Compare the LED current and the pin current with the NPN version.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Schematic | "the circuit diagram" | The drawing of every part and connection, with values and reference designators |
| Netlist | "the connection list" | Every named net with every pin on it; the input to board layout |
| BOM | "the parts list" | Every part with value, package and quantity |
| Forced beta | "overdrive" | `I_C / I_B` chosen well below the transistor's gain so it surely saturates |
| Saturation | "fully on" | A BJT switch with only about 0.1 V from collector to emitter |
| Operating point | "the DC solution" | All node voltages and branch currents in one steady state |
| Rating | "the maximum" | The limit a part's datasheet guarantees (power, current, voltage) |

## Further Reading

- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., section 2.2 (the transistor switch) and Chapter 12 (logic interfacing, including driving external loads from logic).
- onsemi, *MMBT3904 / 2N3904 NPN transistor* datasheet — gain, saturation voltage and power ratings.
- Microchip, *MCP1700* datasheet — capacitor requirements and dropout.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., the chapters on transistors and microcontroller interfacing.
