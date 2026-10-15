# ADC and DAC

> The world speaks in volts; the processor speaks in numbers. The ADC translates volts into numbers by asking yes/no questions, and the DAC translates numbers back into volts with a ladder of resistors.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 17 (Microcontrollers), Lessons 01-03; Phase 04 (Kirchhoff's Laws), Lesson 05 (The Voltage Divider); Phase 05 (Circuit Analysis and Our Simulator), Lesson 06 (Thevenin and Norton); Phase 13 (Operational Amplifiers), Lesson 02 (The Comparator); Phase 14 (Digital Logic), Lesson 02 (Binary Numbers)
**Time:** ~90 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Analog | A quantity that can take any value in a range, like a voltage of 1.2345... V. | The height of water in a glass. |
| Digital | A quantity stored as a whole number from a fixed set. | Marks on the glass: "between mark 3 and mark 4". |
| ADC (analog-to-digital converter) | A circuit that measures a voltage and outputs a number. | Reading the nearest mark on a measuring jug. |
| DAC (digital-to-analog converter) | A circuit that takes a number and outputs a voltage. | Filling a jug up to a chosen mark. |
| Reference voltage (VREF) | The voltage that the largest code corresponds to. Every conversion is a comparison with it. | The full-scale line on the jug. |
| Resolution (bits) | How many codes the converter has: N bits give 2^N codes. | How many marks the jug has. |
| LSB (least significant bit) | The voltage step between two neighbouring codes: VREF / 2^N. | The distance between two marks. |
| Code | The number an ADC outputs or a DAC takes in. | Which mark. |
| Successive approximation (SAR) | An ADC method that finds the code one bit at a time by trying guesses, like a binary search. | Guessing a number between 0 and 1000 by asking "is it higher than 500?" and halving each time. |
| Sample-and-hold | A switch and a small capacitor that freeze the input voltage while it is being converted. | Taking a photo so you can measure a moving thing calmly. |
| R-2R ladder | A chain of resistors of only two values (R and 2R) that turns binary bits into a weighted voltage. | A set of scales where each weight is half the previous one. |
| Source resistance | The resistance "behind" a signal, its Thevenin resistance (Phase 05). | How narrow the pipe is that fills the sample capacitor. |
| Full scale | The biggest input the ADC can measure (just under VREF). | The top of the jug. |

## Learning Objectives

- Compute the LSB size and the code an ideal N-bit ADC gives for a voltage, and convert a code back into volts
- Run a successive-approximation conversion by hand, bit by bit, and explain why it takes exactly N steps
- Design a voltage divider that brings a big voltage (a 12 V battery) into an ADC's range, and convert the code back to the original voltage in firmware
- Explain why the ADC needs a low source resistance and compute the Thevenin resistance of a divider
- Build an R-2R ladder DAC in the simulator, check that it outputs `code x VREF / 2^N`, and see how one mismatched resistor spoils the biggest step

## The Problem

A thermostat must know the temperature. A battery-powered gadget must know when its battery is getting empty. A guitar pedal must turn sound into numbers and back. Sensors (Phase 19) produce voltages that vary smoothly. The processor only handles whole numbers. Something has to translate.

Two practical problems show up at once. First, ranges: a 12 V car battery can sit anywhere from 10.5 V to 14.4 V, but the ADC on a 3.3 V microcontroller can only measure 0 to 3.3 V, and a higher voltage can damage the pin. Second, precision: how small a change can we see, and how accurately? A 10-bit ADC cannot tell 1.0000 V from 1.0020 V. This lesson builds both converters, and uses our simulator to design the divider that feeds the ADC.

## The Physics

### Comparing is easy, measuring is hard

There is no physical device that directly "outputs the number of volts". What electronics does well is **comparing**: the comparator of Phase 13, Lesson 02 outputs 1 if its plus input is higher than its minus input, and 0 otherwise. An ADC is a clever way of turning a measurement into a series of comparisons.

### Holding still while measuring

A conversion takes time (microseconds). If the input changes during that time, the comparisons disagree with each other. So the ADC first closes a switch that connects the input to a small capacitor (a few picofarads), then opens it. The capacitor keeps the voltage frozen while the comparisons run. That is the **sample-and-hold**.

```
 input --[ source R ]--o/ o--+--> to comparator
                     switch  |
                            === C_hold (about 14 pF)
                             |
                            gnd
```

The capacitor must charge to the input voltage while the switch is closed, through whatever resistance is in front of it. That is an RC charge (Phase 07, Lesson 03): it needs several time constants to come within 1 LSB. With a big source resistance, the capacitor does not finish charging and the reading is wrong. Datasheets therefore say something like "the ADC is optimised for signals with an output impedance of approximately 10 kohm or less" (this is the ATmega328P's recommendation).

### Making a voltage from a number

The opposite direction needs weighted sums: bit 7 should count 128 times as much as bit 0. Kirchhoff's current law (Phase 04) does the weighting for us if the resistors are arranged right. That is the R-2R ladder, built below.

## The Concept

### Codes, LSB and full scale

An N-bit converter has `2^N` codes, from 0 to `2^N - 1`. With a reference `VREF`, each code is worth one **LSB**:

```
LSB = VREF / 2^N
```

Read it as: "one step is the reference divided by the number of codes". For a 10-bit ADC with VREF = 3.3 V:

```
2^10 = 1024 codes,   LSB = 3.3 V / 1024 = 0.003 222 7 V = 3.223 mV
```

An ideal ADC outputs the largest code whose voltage does not exceed the input:

```
code = floor(Vin / LSB),   clipped to 0 ... 2^N - 1
```

`floor` means "round down to a whole number". For `Vin = 1.000 V`: `1.000 / 0.003 222 7 = 310.3`, so code 310. Converting back: `310 x 3.2227 mV = 0.999 02 V`. The difference, 0.98 mV, is the **quantization error**, always less than 1 LSB here. (Phase 19, Lesson 05 studies it in depth.)

### Successive approximation: binary search with a comparator

Think of guessing a number between 0 and 1023 with yes/no questions. The fastest way is to ask about the biggest bit first: "is it at least 512?" Then 256, then 128, and so on. Ten questions, ten bits. A SAR ADC does exactly that, with a small internal DAC to produce each guess and a comparator to answer.

For `Vin = 1.000 V`, 10 bits, 3.3 V reference:

```
try bit 9: 1000000000 = 512 x 3.2227 mV = 1.6500 V   input lower  -> 0
try bit 8: 0100000000 = 256 ->            0.8250 V   input higher -> 1
try bit 7: 0110000000 = 384 ->            1.2375 V   input lower  -> 0
try bit 6: 0101000000 = 320 ->            1.0313 V   input lower  -> 0
try bit 5: 0100100000 = 288 ->            0.9281 V   input higher -> 1
try bit 4: 0100110000 = 304 ->            0.9797 V   input higher -> 1
try bit 3: 0100111000 = 312 ->            1.0055 V   input lower  -> 0
try bit 2: 0100110100 = 308 ->            0.9926 V   input higher -> 1
try bit 1: 0100110110 = 310 ->            0.9990 V   input higher -> 1
try bit 0: 0100110111 = 311 ->            1.0022 V   input lower  -> 0
result: 0100110110 = 310
```

Each step halves the range of possible answers, so N bits need exactly N comparisons. That is why SAR ADCs are the standard choice inside microcontrollers: simple, small, and fast enough (tens of thousands to a few million conversions per second).

### Fitting a big voltage into the ADC: the divider

To measure a 12 V battery with a 3.3 V ADC, divide it down (Phase 04, Lesson 05):

```
  battery + --+
              |
            [ R_top = 33 k ]
              |
              +------> ADC pin
              |
            [ R_bottom = 8.2 k ]
              |
  battery - --+-- gnd
```

The divider ratio is:

```
ratio = R_bottom / (R_top + R_bottom) = 8.2 / (33 + 8.2) = 8.2 / 41.2 = 0.199 03
```

The highest battery voltage we expect is 14.4 V (a car battery while charging). Then the pin sees `14.4 x 0.199 03 = 2.866 V`: below 3.3 V, so it is safe and measurable, with some headroom. Why not use exactly 3.3 V of range? Because resistors have tolerances (Phase 03, Lesson 06) and VREF itself varies a little. Clipping at the top would lose information right when the battery is fully charged.

The firmware turns a code back into a battery voltage by undoing both steps:

```
V_battery = code x LSB / ratio
```

For a 12.6 V battery: pin = `12.6 x 0.199 03 = 2.5078 V`, code = `floor(2.5078 / 0.003 222 7) = 778`, firmware says `778 x 0.003 222 7 / 0.199 03 = 12.597 V`. One ADC step is worth `3.2227 mV / 0.199 03 = 16.2 mV` of battery voltage: that is the resolution of our battery meter.

Two more checks every divider design needs:

- **Current wasted:** `14.4 V / 41.2 kohm = 0.35 mA`. Small, but it drains the battery forever. Bigger resistors waste less...
- **...but source resistance:** the ADC sees the Thevenin resistance of the divider (Phase 05, Lesson 06), which is the two resistors in parallel: `33 k x 8.2 k / 41.2 k = 6.57 kohm`. That is under the 10 kohm recommendation. If you scaled both resistors up by 10 to save current, the source resistance would be 65.7 kohm and the sample capacitor would not charge in time. (A common fix: add a 100 nF capacitor from the ADC pin to ground. It acts as a reservoir that refills the tiny sample capacitor instantly.)

### The R-2R ladder DAC

Here is a 3-bit version. Each bit is a digital output pin, at VREF (1) or 0 V (0):

```
 b0 (LSB)        b1             b2 (MSB)
  |               |               |
 [2R]            [2R]            [2R]
  |               |               |
  n0 ----[ R ]--- n1 ----[ R ]--- n2 ------> OUT
  |
 [2R]
  |
 gnd
```

Why does it work? Look at node n0 from the right. Below it are two 2R resistors to "ground" (b0 is a voltage source, which looks like ground to any change, by superposition, Phase 05, Lesson 05). Two 2R in parallel make R. Add the R in series to n1: 2R. At n1, that 2R is in parallel with b1's 2R: R again. Every node sees the same pattern, so each node halves the contribution of the bits before it. Apply superposition, one bit at a time:

- Only b2 (MSB) at VREF, b1 and b0 at 0 V: from n2, the whole network to the left is the R between n1 and n2 plus the R that n1 sees to ground, which is 2R. So n2 sits in the middle of two equal 2R resistors, one to VREF and one to ground: `V_out = VREF / 2`.
- Only b1 at VREF: node n1 has 2R up to VREF, 2R to ground on its left (the R to n0 plus the R that n0 sees), and 3R to ground on its right (the R to n2 plus b2's 2R). 2R in parallel with 3R is 1.2R, so `V_n1 = VREF x 1.2R / (2R + 1.2R) = 0.375 x VREF`. Then n2 is a divider of n1 through R over 2R: `V_out = 0.375 x VREF x 2R / 3R = 0.25 x VREF = VREF / 4`.
- Only b0 at VREF: each node passes on half of what it receives, so `V_out = VREF / 8`.

So:

```
V_out = VREF x (b2/2 + b1/4 + b0/8) = VREF x code / 2^N
```

The beauty: only two resistor values are needed for any number of bits, and they can be made to match well on a chip. Our simulator builds an 8-bit version and checks it.

### Where DACs go wrong: the MSB step

The step from code 127 (01111111) to code 128 (10000000) switches **every** bit at once: the MSB turns on and all seven others turn off. If the MSB's weight is slightly off, this one step can be too big or too small, even negative. That error is called **differential nonlinearity (DNL)**. With 8 bits, an LSB is 1/256 of full scale, about 0.4%, so a resistor that is 2% off on the MSB branch causes an error of more than two LSB on that step (the simulation below shows it). This is why high-resolution DACs need trimmed or very well matched resistors, or completely different designs.

### Worked example: a two-cell battery monitor

A robot uses a 2-cell lithium pack: 6.0 V empty, 8.4 V full. The microcontroller has a 12-bit ADC on 3.3 V. Design the divider and work out what the firmware can see.

**Ratio.** Keep the pin under about 3.0 V at 8.4 V: `ratio <= 3.0 / 8.4 = 0.357`. Try 100 k over 51 k:

```
ratio = 51 / (100 + 51) = 0.3377
pin at 8.4 V = 8.4 x 0.3377 = 2.837 V      pin at 6.0 V = 2.026 V
```

**Resolution.** `LSB = 3.3 / 4096 = 0.806 mV`; at the battery that is `0.806 / 0.3377 = 2.39 mV` per code. Between empty and full there are `(2.837 - 2.026) / 0.000 806 = 1006` codes: plenty to show a percentage.

**Source resistance.** `100 k || 51 k = 33.8 k`: above the 10 kohm advice. Add a 100 nF capacitor from the pin to ground; it charges the ADC's sample capacitor in an instant. Its time constant with the divider, `33.8 k x 100 nF = 3.4 ms`, is irrelevant for a battery that changes over minutes.

**The hidden cost.** The divider always draws `8.4 / 151 k = 56 uA`. That sounds small, but over a year:

```
56 uA x 8760 h = 490 mAh
```

A quarter of a 2000 mAh pack, drained by the voltmeter alone while the robot sits on a shelf. Real products switch the divider with a MOSFET, powered only for the moment of the reading.

### Worked example: reading the DAC's code from a target voltage

To output 1.000 V from an 8-bit DAC with a 3.3 V reference: `code = 1.000 / 3.3 x 256 = 77.6`. Choose 78 (1.0055 V) or 77 (0.9926 V). The nearest is 78, an error of 5.5 mV, under half an LSB (6.4 mV), as it should be.

## Build It

### Step 1: The SAR ADC

```python
class SarAdc:
    def __init__(self, bits, vref):
        self.bits = bits
        self.vref = vref

    @property
    def lsb(self):
        return self.vref / 2 ** self.bits

    def convert(self, volts, verbose=False):
        code = 0
        for bit in reversed(range(self.bits)):
            trial = code | (1 << bit)
            keep = volts >= self.dac_voltage(trial)
            if keep:
                code = trial
        return max(0, min(code, 2 ** self.bits - 1))
```

The loop is the bit-by-bit table above. `code | (1 << bit)` is "the code so far, with this bit tried as 1".

### Step 2: The divider, solved by the simulator

```python
def divider_voltage(battery_volts):
    circuit = Circuit()
    circuit.voltage_source("VBAT", "bat", "0", battery_volts)
    circuit.resistor("RTOP", "bat", "adc", R_TOP)
    circuit.resistor("RBOT", "adc", "0", R_BOTTOM)
    result = circuit.dc()
    return result.v("adc"), result.i("RTOP")
```

The script runs it for batteries from 10.5 V (flat) to 14.4 V (charging), converts each pin voltage with the ADC, and lets the "firmware" compute the battery voltage back.

### Step 3: The R-2R ladder in the simulator

`r2r_output(code, bits)` builds the ladder: one voltage source per bit (a GPIO pin), a 2R from each bit to its node, R between neighbouring nodes, and a 2R termination at the LSB end. The output is the last node. An optional `mismatch` dictionary scales one 2R resistor to model a manufacturing error.

Run it:

```
uv run python phases/17-microcontrollers/04-adc-and-dac/code/main.py
```

You will see the ten-step SAR trace for 1.000 V ending at code 310, the battery table with errors smaller than one step (16.2 mV), the ladder outputs matching `code x 3.3 / 256` to the printed digits, and the MSB-mismatch experiment. There the 127-to-128 step becomes about -1.5 LSB: the output goes *down* when the code goes up. A DAC that does this is called **non-monotonic**, and in a control loop it can make the loop hunt back and forth.

## Use It

- **Arduino `analogRead(A0)`** runs one conversion of the ATmega328P's 10-bit SAR ADC and returns 0-1023. With the default reference it is 5 V full scale, about 4.9 mV per step. A conversion takes about 100 us.
- **ESP32 and STM32** have 12-bit ADCs (4096 codes). The RP2040 has a 12-bit, 500 thousand samples per second ADC. More bits do not automatically mean more accuracy: noise and reference errors often make the last bit or two meaningless (Phase 19).
- **Battery monitors** in phones, e-bikes and cars use exactly the divider-plus-ADC trick, often with a transistor switch so the divider only draws current while measuring.
- **DACs:** the STM32F4 and ESP32 have built-in DACs; dedicated chips like the MCP4725 (12-bit, controlled over I2C, see Lesson 06) are common add-ons. Audio DACs use other designs (delta-sigma) with 16-24 bits.
- **Reference choice:** using VDD as VREF means any wobble on the supply shows up as a measurement error. Precision designs use a separate voltage reference chip (for example 2.5 V or 4.096 V references).

## Try It in the Lab

The lab is a battery monitor. A 14.4 V source (the highest the battery will ever reach) feeds a fixed 33 kohm resistor; you choose the bottom resistor of the divider. The ADC input must sit between 2.7 V and 3.3 V: high enough to use most of the ADC's range, low enough to stay measurable and safe. Compute the ratio each candidate gives and see why the "obvious" round number does not work.

## Common Mistakes

- **Feeding more than VREF (or VDD) into the ADC pin.** Codes clip at full scale, and above VDD the pin's protection diodes conduct and can be damaged.
- **Using huge divider resistors to save power.** The source resistance gets too high and the sample capacitor never charges fully; readings come out low and depend on the previous channel. Add a capacitor at the pin or a buffer op-amp.
- **Forgetting to undo the divider in firmware.** The ADC measures the pin, not the battery. Multiply back by `1 / ratio`.
- **Dividing by 1023 instead of 1024 (or the reverse).** Both appear in tutorials. With `LSB = VREF / 2^N` the top code 1023 means "between 1023 and 1024 LSB". The difference is one LSB; know which convention your code uses.
- **Trusting all the bits.** A 12-bit ADC with a noisy supply may only give 9-10 useful bits.
- **Assuming the DAC can drive a load.** An R-2R ladder has an output resistance of R. Load it with less than many times R and the voltage drops; use an op-amp buffer.

## Exercises

1. A 12-bit ADC uses VREF = 2.5 V. What is the LSB? What code does 1.234 V give? (0.610 mV; floor(1.234 / 0.000 610 35) = 2021.)
2. Run the SAR algorithm by hand for 2.000 V with a 4-bit ADC and VREF = 3.3 V. Write each try. (LSB = 0.206 25 V; result 1001 = 9, i.e. 1.856 V.)
3. Design a divider for a 0-24 V signal into a 0-3.3 V ADC with at least 10% headroom (pin at most 3.0 V at 24 V) and Thevenin resistance under 10 kohm. (For example 68 k over 10 k: 24 x 10 / 78 = 3.08 V, slightly over; 75 k over 10 k gives 2.82 V and 8.8 k Thevenin.)
4. An 8-bit R-2R DAC has VREF = 5 V. What does code 0b10100000 give? What is its output resistance with R = 10 k? (160 x 5 / 256 = 3.125 V; R = 10 kohm.)
5. Harder: in `main.py`, make the 2R of bit 6 (not the MSB) 2% high. Which code transitions are affected now, and by roughly how much compared with the MSB case? Why?

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| ADC resolution | "Precision" | Number of codes, 2^N; says nothing by itself about accuracy |
| LSB | "One step" | VREF / 2^N, the voltage worth of one code |
| SAR ADC | "The microcontroller's ADC" | A binary-search converter: one comparison per bit |
| Sample-and-hold | "The input" | A switch and capacitor that freeze the input during conversion |
| Source impedance | "The sensor's resistance" | The Thevenin resistance driving the ADC pin; it must charge the hold capacitor |
| R-2R ladder | "A DAC" | A resistor network that weights each bit by powers of two |
| DNL | "A glitch at mid-scale" | The difference between a real step size and the ideal 1 LSB |

## Further Reading

- [ATmega328P datasheet (Microchip)](https://www.microchip.com/en-us/product/ATmega328P), chapter "Analog-to-Digital Converter", including the analog input circuitry and the 10 kohm source impedance advice
- [Analog Devices, MT-015 "Basic DAC Architectures II: Binary DACs"](https://www.analog.com/media/en/training-seminars/tutorials/MT-015.pdf) — the R-2R ladder and its errors
- [Analog Devices, MT-021 "Successive Approximation ADCs"](https://www.analog.com/media/en/training-seminars/tutorials/MT-021.pdf) — how SAR converters work inside
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 13 (Digital meets Analog)
