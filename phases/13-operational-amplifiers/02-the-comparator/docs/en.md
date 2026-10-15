# The Comparator

> Without feedback, an op-amp answers one question: is V+ above V−? Set one input to a threshold and you have a decision maker. Add a little positive feedback and the decision stops dithering when the signal is noisy.

**Type:** Build
**Prerequisites:** 13-01 (The Ideal Op-Amp); Phase 04 (Kirchhoff's Laws), lesson 05-the-voltage-divider; Phase 09 (Alternating Current), lesson 02-sine-waves-frequency-and-phase
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Comparator | A circuit whose output is HIGH or LOW depending on which input is larger | A pair of scales that tips fully one way or the other |
| Threshold | The input voltage at which the output switches | The water level that triggers a flood alarm |
| Reference voltage (V_ref) | The fixed voltage the signal is compared against | The mark painted on the wall of the dam |
| Non-inverting / inverting comparator | Signal on the + input (output HIGH when signal is above V_ref) or on the − input (HIGH when below) | An alarm for "too high" versus one for "too low" |
| Chatter | Rapid, unwanted switching back and forth when a noisy signal hovers near the threshold | A light switch flicking on and off when someone leans on it |
| Positive feedback | Feeding the output back to the + input, so a change reinforces itself | A microphone near its own loudspeaker: a squeal that grows |
| Hysteresis | Two different thresholds: one for rising, one for falling signals | A thermostat that turns the heater on at 19 °C but off only at 21 °C |
| Schmitt trigger | A comparator with hysteresis | A light switch with a definite "click" between positions |
| Open-collector output | A comparator output that can only pull down; a resistor pulls it up (lesson's Use It) | A door that can be pulled shut by a rope but is pushed open by a spring |
| Logic level | The voltages a digital circuit treats as 0 and 1 | The two positions of a switch |

## Learning Objectives

- Use an op-amp without feedback as a comparator, and set its threshold with a divider.
- Choose between non-inverting and inverting comparators for "too high" and "too low" alarms.
- Explain why a noisy signal makes a plain comparator chatter.
- Design a Schmitt trigger: compute its two thresholds and its hysteresis from the resistor values.
- Simulate chatter and its cure in the time domain.

## The Problem

A battery charger must stop at 4.2 V per cell. A thermostat must turn the heater on below 19 °C. A night light must switch on when the light sensor's voltage falls below a level. A microcontroller must know when a signal has crossed zero. All of these turn a continuously varying voltage into a yes/no decision. That is the job of a comparator, the bridge between the analogue world of Phases 03-13 and the digital world of Phase 14.

The simplest comparator is an op-amp with no feedback at all. It works, until the signal is noisy (all real signals are). Then the output flickers several times at each crossing, and a relay buzzes, a motor stutters, or a counter counts wrong. This lesson builds both the simple comparator and its fix.

## The Physics

There is no new device physics: an op-amp open loop multiplies V+ − V− by 10⁵ (lesson 01), so any difference above about 100 µV drives the output to a rail. A dedicated comparator chip (LM393, LM339) is internally an op-amp optimised for exactly this: it switches fast, recovers quickly from being saturated, and has an output designed to talk to logic circuits. Op-amps used as comparators work, but slowly: they are designed to avoid saturation and take microseconds to recover from it.

Noise is the physics of this lesson. Every real signal carries random wiggles: thermal noise in resistors, interference from mains wiring (50/60 Hz), switching noise from digital circuits. If a slow signal crosses the threshold while noise of, say, 50 mV rides on top, the instantaneous voltage crosses the threshold several times in quick succession.

## The Concept

### The basic comparator

```
            +5 V
             |
           [R_T] 15 kΩ
             |
             +---- V_ref = 2.0 V ---|- \
             |                      |    >---- out (0 or 5 V)
           [R_B] 10 kΩ   sensor ----|+ /
             |                      rails: 0 V and 5 V
           ground
```

The divider sets the reference: V_ref = 5 × 10 k / (15 k + 10 k) = 2.0 V. With the sensor on the + input:

| Sensor | Output |
|---|---|
| 1.00 V | 0.000 V |
| 1.90 V | 0.000 V |
| 1.99 V | 0.000 V |
| 2.00 V | 2.501 V |
| 2.01 V | 5.000 V |
| 2.10 V | 5.000 V |

Ten millivolts either side of the threshold give a clean 0 or 5 V. Exactly at 2.000 V the model sits halfway, a point a real signal passes through in microseconds.

**Choosing the input.** Signal on + and reference on −: output HIGH when the signal is *above* the reference (a "too high" alarm). Swap them: HIGH when the signal is *below* (a "too low" alarm, a night light). The script's inverting example: input 2.4 V, reference 2.5 V, output 5.000 V.

**Designing the divider.** For a threshold V_th from a supply V_S with bottom resistor R_B:

```
V_th = V_S × R_B / (R_T + R_B)     →     R_T = R_B × (V_S / V_th − 1)
```

For 2.0 V from 5 V with R_B = 10 kΩ: R_T = 10 k × (2.5 − 1) = 15 kΩ.

### Chatter

The script makes a slow 10 Hz sine between 0.5 V and 4.5 V and adds 80 mV of 900 Hz "noise". Over 0.2 s the slow signal crosses 2.5 V four times, so a perfect comparator would produce four output edges. The plain comparator produces **8**: at some crossings the output flips, flips back, and flips again.

```
input:  slowly rising signal with ripple            output of a plain comparator
            /\/\/\/
    ---/\/\/-------- threshold                      ___    _   ________
     /\/                                         __|   |__| |_|
```

Why: near the crossing, the slow signal changes by only 2 V × 2π × 10 Hz = 126 V/s, while the noise changes by up to 0.08 × 2π × 900 = 452 V/s. While the slow signal is within ±80 mV of the threshold, the noise alone can push the total back and forth across it.

### The cure: hysteresis with positive feedback

Instead of one threshold, use two: switch up only when the input rises above an upper threshold, and switch down only when it falls below a lower one. Noise smaller than the gap between them cannot cause chatter. This is done by feeding a little of the output back to the + input:

```
             V_ref 2.5 V --[R1 10 kΩ]--+-- p ---|+ \
                                       |        |    >----+--- out
                                       +--[R2]----------- +
                       input -------------------|- /
```

This is an **inverting Schmitt trigger** (input on −). The + input is a divider between V_ref and the output:

```
V_p = V_ref × R2/(R1 + R2) + V_out × R1/(R1 + R2)
```

Read: "the plus input sits at V_ref, pulled slightly toward the output". When the output is HIGH (5 V), V_p is a little above V_ref; when LOW (0 V), a little below. So the threshold *moves away* from the input each time the output switches: that is positive feedback. Once the output has flipped, the input must travel all the way to the other threshold to flip it back.

**Worked example**, R1 = 10 k, R2 = 100 k: R1/(R1 + R2) = 10/110 = 0.0909, R2/(R1 + R2) = 0.909.

```
output LOW  (0 V): V_p = 2.5 × 0.909 + 0 × 0.0909 = 2.273 V   (lower threshold)
output HIGH (5 V): V_p = 2.5 × 0.909 + 5 × 0.0909 = 2.727 V   (upper threshold)
hysteresis = 2.727 − 2.273 = 0.455 V = 5 V × 0.0909
```

Simulated results:

| R2 | Thresholds | Hysteresis | Output edges (4 is right) |
|---|---|---|---|
| (plain comparator) | 2.500 V | 0 | 8 |
| 1 MΩ | 2.475 / 2.525 V | 0.050 V | 8 |
| 100 kΩ | 2.273 / 2.727 V | 0.455 V | 4 |
| 47 kΩ | 2.061 / 2.939 V | 0.877 V | 4 |

50 mV of hysteresis is less than the 160 mV peak-to-peak noise: still chatter. 455 mV is comfortably more: clean switching. **Rule: make the hysteresis larger than the peak-to-peak noise**, but not so large that the thresholds are too far from where you want them.

### Why positive feedback is "the other kind"

In lesson 01, negative feedback pulled the output toward a balanced state where V+ = V−. Positive feedback does the opposite: any change pushes the output further the same way, until it hits a rail. A circuit with positive feedback is not linear and has no "V+ = V−"; it has **two stable states** and snaps between them. That property is also the seed of memory: Phase 15 builds latches and flip-flops from exactly this idea.

### Timing it

In the lab you will work in the time domain. A 1 Hz sine centred on 2.5 V with 2.5 V amplitude is V(t) = 2.5 + 2.5 sin(2π t). It falls through 2.0 V when sin(2π t) = −0.2 on the way down: 2πt = π + 0.2014, t = 0.532 s; and rises back through 2.0 V when 2πt = 2π − 0.2014, t = 0.968 s.

## Build It

### Step 1: A divider-referenced comparator

```python
def threshold_detector(sensor_volts, top_ohms, bottom_ohms=10e3):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", 5.0)
    circuit.voltage_source("VS", "sensor", "0", sensor_volts)
    circuit.resistor("RT", "vcc", "ref", top_ohms)
    circuit.resistor("RB", "ref", "0", bottom_ohms)
    circuit.opamp("U1", plus="sensor", minus="ref", out="out", gain=1e5, rails=RAILS)
    return circuit.dc()
```

`rails=(0.0, 5.0)` makes the op-amp's output swing between 0 and 5 V, as a single-supply comparator would.

### Step 2: A noisy signal

```python
def noisy_input(circuit):
    circuit.sine_source("VSLOW", "a", "0", amplitude=2.0, freq=10.0, offset=2.5)
    circuit.sine_source("VNOISE", "in", "a", amplitude=0.08, freq=900.0, offset=0.0)
```

Two sources in series add their voltages: node `in` carries the slow signal plus the "noise".

### Step 3: Plain versus Schmitt

```python
circuit.voltage_source("VREF", "ref", "0", 2.5)
circuit.resistor("R1", "ref", "p", 10e3)
circuit.resistor("R2", "out", "p", feedback_ohms)
circuit.opamp("U1", plus="p", minus="in", out="out", gain=1e5, rails=RAILS)
```

### Step 4: Count edges

```python
def count_edges(result):
    output = np.asarray(result.v("out")) > 2.5
    return int(np.sum(output[1:] != output[:-1]))
```

Each time the output crosses 2.5 V between two time steps, that is one edge.

```
uv run python phases/13-operational-amplifiers/02-the-comparator/code/main.py
```

## Use It

- **Comparator chips**: LM393 (dual) and LM339 (quad) are the classics: cheap, 2-36 V supplies, **open-collector outputs**. The output transistor can only pull the output low; you add a pull-up resistor (say 10 kΩ) to whatever logic voltage you need (3.3 V or 5 V). That makes level shifting free, and lets several comparators share one output line (any of them can pull it low). Fast parts like the TLV3501 switch in 4.5 ns.
- **Built into microcontrollers**: most microcontrollers contain analogue comparators with selectable internal references and programmable hysteresis, used for zero-crossing detection and battery monitoring.
- **Battery protection**: a lithium cell protector compares the cell voltage with 4.25 V and 2.5 V references to disconnect the cell on over-charge and over-discharge, with hysteresis so it does not oscillate at the limit.
- **Schmitt-trigger logic**: the 74HC14 is six inverters with built-in hysteresis, used to clean up slow or bouncy signals (buttons, sensors) before they enter digital circuits (Phase 14).
- **Oscillators**: a Schmitt trigger plus an RC network that charges and discharges between its two thresholds makes a square-wave oscillator, the principle behind the 555 timer.

## Try It in the Lab

The lab is a frost alarm: a sensor voltage drifting as a slow 1 Hz sine between 0 and 5 V, a comparator powered from 0 and 5 V with the sensor on its plus input, and a reference divider whose bottom resistor is 10 kΩ. You choose the top resistor so the alarm flips exactly when the sensor passes 2.0 V.

Think about: the divider formula for the reference, and when the 1 Hz sine passes through 2.0 V going down and going up. Why do the wrong resistors fail the timing goals as well as the reference goal?

## Common Mistakes

- **Adding negative feedback to a comparator.** Then it is an amplifier again and no longer makes clean decisions.
- **Expecting a general-purpose op-amp to switch fast.** Op-amps saturate and recover slowly; for speed, use a comparator chip.
- **Forgetting the pull-up on an open-collector output.** Without it, the output can pull low but never goes high.
- **No hysteresis on slow or noisy signals.** Chatter causes relays to buzz and counters to miscount.
- **Too much hysteresis.** The output switches too late, or never if the signal does not reach the far threshold.
- **Inputs outside the allowed range.** Many comparators and op-amps misbehave if an input goes above their positive supply or below ground; check the "common-mode input range" in the datasheet.

## Exercises

1. Design a divider from 3.3 V that gives a threshold of 1.2 V with R_B = 10 kΩ. Which standard (E12) value is closest for R_T, and what threshold results?
2. A night light should turn on when a light sensor's voltage falls below 1.5 V. Which input does the sensor go to? Draw the circuit.
3. For the inverting Schmitt trigger with V_ref = 2.5 V, R1 = 10 kΩ and output swinging 0-5 V, what R2 gives 0.2 V of hysteresis? What are the two thresholds?
4. Noise of 300 mV peak-to-peak rides on a slow signal. Which of the lesson's R2 values would still chatter?
5. Modify the script so the Schmitt trigger's thresholds are centred on 2.5 V *exactly*. (Hint: the thresholds are V_ref × R2/(R1+R2) and that plus 5 × R1/(R1+R2); what V_ref centres them?)

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Comparator | "Comp" | Op-amp-like circuit used open loop: output at one rail or the other depending on the sign of V+ − V− |
| Threshold | "Trip point" | Input voltage at which the output switches |
| Chatter | "Bouncing", "multiple triggering" | Repeated switching caused by noise near the threshold |
| Hysteresis | "Dead band" | Separation between the rising and falling thresholds |
| Schmitt trigger | "Comparator with hysteresis" | Comparator with positive feedback that has two thresholds and two stable states |
| Positive feedback | "Regenerative feedback" | Output fed back to the + input; changes reinforce themselves |
| Open-collector / open-drain | "OC output" | Output that can only sink current; needs an external pull-up resistor |

## Further Reading

- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., section 4.3.2 (nonlinear op-amp circuits) and 12.3 "Comparators" (comparator chips and hysteresis).
- *All About Circuits*, Volume III, chapter 8, "The operational amplifier" (its use as a comparator) and "Positive feedback". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-8/positive-feedback/
- Texas Instruments, "Comparator with Hysteresis Reference Design" (TIDU020). https://www.ti.com/lit/ug/tidu020a/tidu020a.pdf
- Texas Instruments LM393 datasheet: open-collector outputs, response time, common-mode range. https://www.ti.com/product/LM393
