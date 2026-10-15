# GPIO

> A general-purpose pin is three bits of configuration and a pair of transistors: it can push current out, pull current in, or quietly listen.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 17 (Microcontrollers), Lesson 01 (What a Microcontroller Is); Phase 11 (Semiconductors and Diodes), Lesson 07 (LEDs); Phase 06 (Sources, Batteries and Measurement), Lesson 02 (Internal Resistance); Phase 14 (Digital Logic), Lesson 05 (CMOS Gates from Transistors)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| GPIO | "General-purpose input/output": a pin the program can use either as an output or as an input. | A door that can be used to go out or to let visitors in. |
| Output | The pin is driven by the chip to a voltage: high (near the supply) or low (near 0 V). | The chip shouting "yes" or "no" down a wire. |
| Input | The chip only measures the pin's voltage and turns it into a 0 or a 1. It does not push current. | The chip listening at the door. |
| Direction register (DDR) | A register whose bits choose, pin by pin, input (0) or output (1). | A switch by each door: "in" or "out". |
| Output register (PORT) | A register whose bits set the level of each output pin. | What the chip shouts at each door. |
| Input register (PIN) | A register the chip fills by reading the pins' voltages. | What the chip heard at each door. |
| Source / sink | Sourcing: current flows out of the pin (pin high). Sinking: current flows into the pin (pin low). | A tap that pours water out versus a drain that swallows it. |
| Pull-up resistor | A resistor from the pin to the supply, so an unconnected input reads 1. | A spring that holds a door closed unless somebody pushes it. |
| Pull-down resistor | A resistor from the pin to ground, so an unconnected input reads 0. | The same spring, pulling the other way. |
| Floating input | An input connected to nothing. Its voltage is undefined and drifts. | A weathervane: it points wherever the wind blows. |
| Threshold (VIL, VIH) | The voltages below which a pin is a guaranteed 0 (VIL) and above which it is a guaranteed 1 (VIH). | The lines on a football pitch: inside one box is "ours", inside the other is "theirs", the middle is disputed. |
| Driver resistance | The small resistance of the output transistors when they are on. | The narrowness of a tap: even fully open it limits the flow a little. |
| Active low | A signal that "means yes" when it is at 0 V. | A "do not disturb" sign that is valid when it is hanging down. |

## Learning Objectives

- Configure a pin as an output or an input with three registers (DDR, PORT, PIN), bit by bit
- Model an output pin as a voltage source with a series driver resistance and compute how its voltage sags under load
- Size the resistor between a pin and an LED so the current is safe for both the LED and the pin
- Explain why an input needs a pull-up or a pull-down, and compute how much current a pull-up wastes when a button is pressed
- Translate a voltage into a logic level using VIL and VIH, including the undefined band

## The Problem

In the previous lesson the pin was perfect: 3.3 V or 0 V, as much current as you liked. Real pins are not perfect. Connect an LED straight to a pin with no resistor and three things happen at once: the LED draws far more current than it should, the pin's voltage sags because the chip's output transistors cannot supply that much, and the chip gets hot. Do it to enough pins and the chip dies. Microcontroller datasheets put hard limits on this, for example "20 mA recommended, 40 mA absolute maximum per pin, 200 mA for the whole chip" on the ATmega328P.

Inputs have the opposite problem. A push-button wired from a pin to ground connects the pin to 0 V when pressed. When released, it connects the pin to *nothing*. The program then reads 0, 1, 0, 1 at random, because the pin's voltage is set by stray charge and by electric fields from your hand and nearby wires. Beginners spend whole evenings on this bug.

Both problems are solved by understanding what is physically behind the pin. This lesson builds a GPIO port in Python with real register semantics and lets our simulator compute the voltages and currents for each configuration.

## The Physics

### Behind an output pin

Inside the chip, each output pin is driven by a CMOS pair (Phase 14, Lesson 05): a P-channel MOSFET from the supply to the pin, and an N-channel MOSFET from the pin to ground. Only one is on at a time. A turned-on MOSFET behaves like a small resistor (Phase 12, Lesson 05): tens of ohms for a typical pin driver.

```
     VDD = 3.3 V                         VDD = 3.3 V
        |                                    |
       [P on: ~40 ohm]                     [P off]
        |                                    |
        +----- pin  (output high)            +----- pin  (output low)
        |                                    |
       [N off]                             [N on: ~40 ohm]
        |                                    |
       gnd                                  gnd
```

So an output-high pin is, electrically, **a 3.3 V source in series with about 40 ohm**. You met exactly this shape in Phase 06, Lesson 02 (Internal Resistance): an ideal source plus an internal resistor. Everything from that lesson applies. With no load, the pin sits at 3.3 V. Draw current `I` and the pin drops by `I x 40 ohm`.

How do we know it is about 40 ohm? Datasheets give the output voltage at a test current. For instance a datasheet might say "VOH is at least 2.3 V when the pin sources 10 mA at VDD = 3 V". That means the drop is at most 0.7 V at 10 mA, so the driver resistance is at most 0.7 / 0.010 = 70 ohm. Typical values are lower. We use 40 ohm as a round, realistic number.

### Behind an input pin

An input pin is connected to the gates of a CMOS inverter. A MOSFET gate is a tiny capacitor with an insulator under it (Phase 12, Lesson 04), so almost no current flows in: typically less than 1 microamp of leakage. Electrically, an input is **a very large resistance** (we use 100 megaohm) in parallel with a few picofarads.

The inverter switches somewhere around the middle of the supply, but the exact point varies with temperature and from chip to chip. So the datasheet promises two thresholds:

```
3.3 V  +-----------------------------+
       |   guaranteed 1   (>= VIH)   |
1.98 V +-----------------------------+   VIH = 0.6 x VDD
       |   undefined: could be       |
       |   either, may even toggle   |
0.99 V +-----------------------------+   VIL = 0.3 x VDD
       |   guaranteed 0   (<= VIL)   |
0 V    +-----------------------------+
```

(0.3 and 0.6 of VDD are the values for the ATmega328P family; other chips use 0.3 and 0.7, so always check.)

### Why a floating input floats

If nothing drives the input, its voltage is set by whatever tiny currents reach it: leakage, charge left from the last time it was touched, and capacitive coupling from nearby wires carrying signals, including the 50/60 Hz from mains wiring that your body picks up like an antenna. Because the input resistance is so huge, even a nanoamp makes a big voltage: 1 nA x 100 Mohm = 0.1 V. A floating input can wander through the undefined band, and the program reads noise.

A **pull-up resistor** fixes this by giving the pin a definite, gentle connection to VDD. Gentle means a large resistance, tens of kilohms: strong enough to swamp nanoamp leakage, weak enough that a button to ground easily wins.

## The Concept

### Three registers per port

Many microcontrollers group pins in **ports** of 8 (or 16, or 32) and give each port three registers. We use the AVR names, since they are the most common in teaching:

| Register | You write it? | Meaning of bit n |
|----------|---------------|------------------|
| DDRx | yes | 1 = pin n is an output, 0 = pin n is an input |
| PORTx | yes | if output: the level (1 high, 0 low); if input: 1 enables the internal pull-up |
| PINx | no, read it | the logic level the chip sees on pin n right now |

That PORT has two meanings is an AVR quirk; other families (STM32, RP2040) have separate pull-up registers. The idea is the same everywhere: some bits choose direction, some set the level, some enable pulls, and one register reports what the pins actually read.

Combining the DDR and PORT bit gives four pin modes:

```
DDR bit  PORT bit   mode
   1        1       output high   (source current)
   1        0       output low    (sink current)
   0        1       input with internal pull-up
   0        0       input, floating (high impedance)
```

### Setting one bit without touching the others

To make PB0 an output while leaving the other seven pins alone, read the register, OR in the bit, and write back:

```
DDRB = DDRB | 0b00000001        (set bit 0)
DDRB = DDRB & 0b11111110        (clear bit 0)
```

`|` is bitwise OR, `&` is bitwise AND (Phase 14, Lesson 03). `0b` marks a binary number. `1 << n` builds a number with only bit n set: `1 << 2 = 0b00000100 = 4`.

### Sizing the LED resistor, step by step

Circuit: pin (3.3 V source + 40 ohm inside the chip), then our series resistor `R`, then a red LED to ground.

```
  [3.3 V]--[40 ohm]--pin--[ R ]--+--|>|-- gnd
   inside the chip               a   LED
```

Kirchhoff's voltage law around the loop says the 3.3 V is shared by the driver resistance, `R` and the LED:

```
3.3 V = I x 40 ohm + I x R + V_LED
```

A red LED at a few milliamps has `V_LED` of roughly 1.8-1.9 V (Phase 11, Lesson 07). Solve for the current:

```
I = (3.3 V - V_LED) / (40 ohm + R)
```

Read it as: "the current is the voltage left over after the LED, divided by all the resistance in the loop".

With `R = 220 ohm` and `V_LED = 1.85 V`:

```
I = (3.3 - 1.85) / (40 + 220) = 1.45 / 260 = 0.0056 A = 5.6 mA
pin voltage = 3.3 - 0.0056 x 40 = 3.3 - 0.22 = 3.08 V
```

That is bright enough for an indicator, well under the 20 mA pin limit, and the pin still reads as a solid 1.

With no resistor at all (`R` close to 0), the LED's own exponential curve and the driver's 40 ohm are all that limit the current. The LED climbs to about 1.95 V and `I = (3.3 - 1.95) / 40 = 34 mA`: well over the recommended 20 mA pin limit and close to the absolute maximum, and the pin voltage collapses to about 1.95 V, which another input might not even read as a 1. Our simulator solves this case exactly.

Going the other way, to pick `R` for a target current of 5 mA:

```
R = (3.3 V - V_LED) / I - 40 ohm = (3.3 - 1.85) / 0.005 - 40 = 290 - 40 = 250 ohm
```

The nearest standard value is 220 or 270 ohm. Either is fine.

### Sourcing versus sinking

You can also connect the LED the other way: from VDD, through the LED and the resistor, *into* the pin. Now the LED lights when the pin is **low**, because then there is 3.3 V across the LED-plus-resistor. When the pin is high, both ends are at 3.3 V and nothing flows. This is "active low" wiring. Some older logic families could sink much more current than they could source, so active-low LEDs became a habit; on modern CMOS chips both directions are similar.

### Inputs, pull-ups and the button

Circuit: internal pull-up of about 35 kohm from VDD to the pin, button from the pin to ground.

```
   VDD --[ 35 kohm pull-up ]--+-- PD2 (input)
                              |
                           [button]
                              |
                             gnd
```

- **Released:** no current flows (only nanoamps of leakage), so there is no voltage drop across the pull-up, and the pin sits at about 3.3 V. Reads 1.
- **Pressed:** the button shorts the pin to ground. The pin reads 0, and the pull-up carries `3.3 V / 35 000 ohm = 94 uA` for as long as the button is held. That is the price of a pull-up: a small current while the input is low.

Notice that the button reads 1 when released and 0 when pressed. That is active-low again, and completely normal: the program just checks for 0.

Datasheets give the internal pull-up as a range, for example 20 to 50 kohm. If you need something more precise or stronger (for long wires or noisy places), you add an external resistor, often 4.7 kohm or 10 kohm.

## Build It

### Step 1: A port with three registers

```python
class GpioPort:
    def __init__(self, name):
        self.name = name
        self.ddr = 0
        self.port = 0
        self.pin_voltages = [0.0] * 8

    def mode(self, number):
        if self.bit(self.ddr, number):
            return "output-high" if self.bit(self.port, number) else "output-low"
        return "input-pullup" if self.bit(self.port, number) else "input-floating"
```

`mode` is the four-row table above, written as code.

### Step 2: Reading voltages as logic levels

```python
def logic_level(volts):
    if volts <= VIL_FRACTION * VDD:
        return 0
    if volts >= VIH_FRACTION * VDD:
        return 1
    return None
```

`None` means "undefined": the real chip might read either. `read_pin_register` builds the PIN register from the eight pin voltages.

### Step 3: Turning a pin's mode into circuit elements

This is the bridge between the register world and the circuit world:

```python
def add_pin(circuit, port, number, node):
    mode = port.mode(number)
    if mode.startswith("output"):
        circuit.voltage_source(f"DRV{number}", f"drv{number}", "0", VDD if mode == "output-high" else 0.0)
        circuit.resistor(f"RDRV{number}", f"drv{number}", node, DRIVER_OHMS)
    elif mode == "input-pullup":
        circuit.resistor(f"RPU{number}", "vdd", node, PULL_UP_OHMS)
    circuit.resistor(f"RLEAK{number}", node, "0", INPUT_LEAK_OHMS)
```

An output is a source plus 40 ohm. An input with pull-up is a 35 kohm resistor to VDD. Every pin also gets a 100 Mohm leak to ground, which stands for the input's tiny leakage and keeps the simulator from meeting a node connected to nothing (a node with no path to anything has no defined voltage, and the equations of Phase 05 would have no solution).

### Step 4: Three experiments

- `led_on_output(R)` sets DDRB bit 0 and PORTB bit 0, adds the resistor and LED, and returns the pin voltage and LED current. The script sweeps R from 1 ohm to 4.7 kohm.
- `led_sinking(pin_high)` wires the LED from VDD into PB1 and shows it lights only when the pin is low.
- `button_with_pullup(pressed, pullup_enabled)` builds the button circuit with the `sim` switch and reads PIND.

Run it:

```
uv run python phases/17-microcontrollers/02-gpio/code/main.py
```

Look at the sweep: with 1 ohm the LED current is above 20 mA and the pin sags well below 3.3 V, flagged "too much for the pin". With 47 ohm it is about 16 mA: legal, but far more than an indicator needs. From 220 ohm up the current is comfortable (about 5.7 mA at 220 ohm, with the pin still above 3 V); 4.7 kohm still lights the LED, faintly (modern LEDs are visible even at a fraction of a milliamp). In the button table, with the pull-up on, the pin reads 1 released and 0 pressed, with about 94 uA flowing while pressed. With the pull-up off and the button released, the pin is held only by the 100 Mohm leak: in the simulator it sits at 0 V, but on a real chip nothing holds it there, and that is the floating input.

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
Logic thresholds at VDD = 3.3 V: a 0 is below 0.99 V, a 1 is above 1.98 V, in between is undefined
  0.2 V reads as 0
  0.9 V reads as 0
  1.6 V reads as undefined
  2.1 V reads as 1
  3.3 V reads as 1

LED on PB0 (sourcing), driver resistance 40 ohm
   series R  pin volts   LED mA  verdict
        1 ohm    1.947 V    33.83  too much for the pin
       47 ohm    2.645 V    16.37  fine
      100 ohm    2.886 V    10.34  fine
      220 ohm    3.072 V     5.69  fine
      470 ohm    3.181 V     2.97  fine
     1000 ohm    3.240 V     1.49  fine
     4700 ohm    3.286 V     0.34  dim

LED from VDD into PB1 (sinking, 220 ohm): the LED lights when the pin is LOW
...
```

## Use It

- **Arduino:** `pinMode(13, OUTPUT)` sets a DDR bit, `digitalWrite(13, HIGH)` sets a PORT bit, `pinMode(2, INPUT_PULLUP)` clears the DDR bit and sets the PORT bit (enabling the pull-up), and `digitalRead(2)` reads a PIN bit.
- **Raspberry Pi Pico (MicroPython):** `Pin(15, Pin.IN, Pin.PULL_UP)` does the same; the RP2040 has separate pull-up and pull-down enables and selectable drive strengths (2, 4, 8 or 12 mA).
- **Current limits are real:** the ATmega328P datasheet lists 40 mA per pin as an absolute maximum (do not even approach it), and a total limit for the whole package. The RP2040 is designed around a few milliamps per pin. For anything bigger (a relay, a motor, a strip of LEDs) the pin drives a transistor (Phase 12, Lesson 03) and the transistor carries the current.
- **Voltage limits are real too:** a 3.3 V chip's pins usually must not see more than about VDD + 0.3 V. Connecting a 5 V sensor output straight to a 3.3 V input can damage it; use a divider (Phase 04, Lesson 05) or a level shifter, unless the datasheet says the pin is "5 V tolerant".
- **Buttons almost always use pull-ups**, and the program treats "0" as "pressed". Lesson 05 deals with the other problem of buttons: bouncing.

## Try It in the Lab

The lab gives you a 3.3 V GPIO pin, drawn as an ideal 3.3 V source and a fixed 40 ohm "driver" resistor, and a red LED. You pick the series resistor. Two goals: the LED current must be between 2 and 8 mA (bright enough, and well inside the pin's comfort zone), and the pin voltage must stay above 3 V so the output still looks like a clean 1 to anything else connected to it. Before dropping parts, estimate the current for each resistor with `I = (3.3 - V_LED) / (40 + R)` and think about which goal each wrong part breaks.

## Common Mistakes

- **No resistor in series with an LED.** The LED is not a resistor; its current rises exponentially with voltage. The only thing limiting it is the pin's driver, which is then overloaded.
- **Leaving inputs floating.** An unused input or a released button with no pull-up reads random values and can even make the input stage draw extra current, because its transistors sit half-on. Enable a pull-up or pull-down, or set unused pins as outputs.
- **Forgetting the logic is inverted with pull-ups.** Pressed reads 0. Write `if pin == 0: pressed()`.
- **Exceeding the total chip current.** Eight pins each at 20 mA is 160 mA, which may exceed the package limit even though each pin is within its own.
- **Driving a pin above VDD.** Inputs have protection diodes to VDD; a higher voltage pushes current through them into the supply and can latch up or damage the chip.
- **Reading PORT when you meant PIN.** PORT is what you asked for; PIN is what is really on the pin. If something external fights the output (a short to ground), they differ.

## Exercises

1. A pin at 3.3 V with 40 ohm driver resistance feeds a green LED (V_LED about 2.1 V) through 150 ohm. Compute the current and the pin voltage. (About 6.3 mA and 3.05 V.)
2. You want 2 mA through a red LED (V_LED 1.8 V) from a 5 V pin with 30 ohm driver resistance. Which resistor? Pick the nearest standard value from 1.5 k, 1.6 k, 1.8 k. (R = 3.2 / 0.002 - 30 = 1570 ohm, so 1.6 k.)
3. An internal pull-up is specified as 20 to 50 kohm at VDD = 5 V. What is the range of current wasted while a button is held? (100 to 250 uA.)
4. A sensor output connects to an input pin through 1 m of cable and sits at 1.5 V when it means "1". With VDD = 3.3 V and VIH = 0.7 x VDD, does the chip see a 1? (VIH = 2.31 V, so no: it is in the undefined band.)
5. Harder: modify `main.py` to drive four LEDs from four pins of the same port at once, each with 100 ohm. Add up the currents. If the chip's total limit is 100 mA, how many such LEDs can you light at once? Then repeat with 330 ohm.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| GPIO | "A digital pin" | A pin whose direction, level and pulls are set by registers |
| Output high | "The pin is on" | The upper driver transistor connects the pin to VDD through tens of ohms |
| Input | "Reading the pin" | A near-infinite resistance whose voltage is compared to VIL and VIH |
| Pull-up | "A resistor to keep it high" | A weak resistor to VDD that sets the idle level and swamps leakage |
| Floating | "The pin is off" | Connected to nothing, so its voltage is undefined |
| Source / sink | "Output / input current" | Current flowing out of / into the pin |
| VIL, VIH | "Low and high" | Guaranteed thresholds; between them the reading is undefined |

## Further Reading

- [ATmega328P datasheet (Microchip)](https://www.microchip.com/en-us/product/ATmega328P), chapter "I/O-Ports" and the "Electrical Characteristics" tables for VIL, VIH, VOH and pull-up resistance
- [RP2040 datasheet (Raspberry Pi)](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf), section "GPIO" and "Pads" for drive strength and pulls
- [SparkFun, "Pull-up Resistors"](https://learn.sparkfun.com/tutorials/pull-up-resistors) — a gentle explanation with examples
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., chapter on microcontrollers — interfacing LEDs, switches and loads to pins
