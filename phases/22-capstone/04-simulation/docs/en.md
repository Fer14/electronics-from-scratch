# Simulation

> A design is a prediction. Simulation lets you test that prediction through a whole night, a dying battery and a passing car, before you solder anything.

**Type:** Build
**Prerequisites:** Phase 22 (Capstone), Lessons 01-03; Phase 07 (Capacitors), Lesson 08 (Transient Simulation from Scratch); Phase 17 (Microcontrollers), Lessons 03 (PWM), 05 (Timers and Interrupts) and 07 (A Virtual Microcontroller); Phase 19 (Sensors and Signals), Lessons 05 (Quantization), 06 (Noise) and 07 (Digital Filtering)
**Time:** ~85 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Transient simulation | Computing how voltages and currents change over time, step by step | A film instead of a photograph |
| Behavioural model | A simple program that imitates what a part does, without simulating every transistor in it | An actor playing a doctor, not a real doctor |
| Firmware | The program inside the microcontroller | The recipe the cook follows |
| State machine | A program that is always in one of a few states (here: LED off, LED on) and moves between them on rules | A traffic light |
| Moving average | The average of the last few readings, updated each time a new one arrives | Judging the weather by the last few days, not the last minute |
| Compensation | Adjusting a setting to cancel an unwanted change | Pressing the accelerator harder on a hill |
| Calibration | Measuring how a system really behaves and storing the result to correct it | Checking a kitchen scale with a known weight |
| Scenario | A made-up but realistic sequence of events used to test a design | A fire drill |
| Edge case | An unusual situation at the limits of what the design must handle | A leap year in a calendar program |
| Flicker | Visible, unwanted changes in a light's brightness | A failing fluorescent tube |
| Co-simulation | Simulating the electronics and the software together | Rehearsing the actors with the stage machinery running |

## Learning Objectives

- Simulate the PWM-driven LED in time and measure its peak and average current.
- Write the night light's firmware as a small Python state machine with a moving average and hysteresis.
- Compensate for the falling battery voltage, using a calibration fitted to the circuit simulation, and verify requirement R5.
- Run a whole night (15 hours, one decision per second) with dusk, dawn, flicker-prone fluctuations and passing headlights, and verify requirements R1, R2 and R3.
- Compare the final firmware with a naive one and count how often each switches.

## The Problem

Lesson 03 checked every DC operating point. But three of our requirements are about *time*:

- **R2**: no flicker at dusk, and no reaction to a car's headlights for a second or two.
- **R3**: an even, soft light from a PWM signal switching a thousand times per second.
- **R5**: the same brightness from the first night to the thirtieth, as the batteries fall from 4.5 V to 3.6 V.

None of these can be checked with a DC analysis. They depend on how the circuit behaves over microseconds (PWM) and on how the firmware behaves over hours (the night). We simulate both: the circuit with our transient simulator, and the firmware with a Python model that reads simulated ADC codes and decides what to do, once per second, for a whole night.

## The Physics

### PWM and the eye

The microcontroller switches the LED fully on and fully off 1,000 times per second. The LED itself responds in nanoseconds, so its light really is a train of pulses. Our eyes and brains average light over roughly 10-50 ms: a train of pulses faster than about 100 Hz looks like a steady light whose brightness is the **average** (Phase 17, Lesson 03). Some people notice flicker in peripheral vision or in fast eye movements up to a few hundred hertz, which is why our requirement asks for more than 200 Hz and we use 1 kHz.

The average LED current is

```
I_average = duty * I_on
```

"the fraction of time the LED is on, times the current while it is on". With `I_on = 18.8 mA` and 30% duty: `0.3 * 18.8 = 5.64 mA`.

### Measuring an average with a filter

To check an average in a real circuit (and in the lab of this lesson), put a small resistor under the transistor's emitter so the LED current makes a small voltage across it (1 Ω gives 1 mV per mA), and smooth that voltage with an RC low-pass filter (Phase 10, Lesson 02) whose time constant is much longer than the PWM period. A 10 kΩ and 1 µF filter has `tau = R * C = 10 ms`, ten PWM periods, so its output settles to the average with a small ripple. That is exactly what the DC range of a multimeter does internally, in effect.

### Noise and quantization

The ADC returns integer codes (Phase 19, Lesson 05), and real readings wobble by a code or two because of noise (Phase 19, Lesson 06). Our model adds a deterministic wobble of up to ±2 codes to every light reading, so the firmware is tested against imperfect data.

## The Concept

### The firmware as a state machine

Once per second the microcontroller wakes up and runs this logic:

```
read light code (ADC0) and battery code (ADC1)
keep the last 4 light codes; average = mean of them
if LED is off and average < 390:  LED on
if LED is on  and average > 584:  LED off
if LED is on:  duty = compensated duty for this battery voltage
else:          duty = 0
go back to sleep
```

```
            average < 390
   +-------+ -----------> +------+
   |  OFF  |              |  ON  |
   +-------+ <----------- +------+
            average > 584
```

Two states, two transitions, two different thresholds: hysteresis. The 4-sample moving average means a change must last a few seconds before it can cross a threshold.

### Battery compensation, calibrated

To keep the average current at 5.7 mA, the firmware needs the LED's on-current at the present battery voltage, then sets `duty = 5.7 mA / I_on`. It can measure the battery (ADC1, Lesson 03). It needs a formula for `I_on`. Instead of guessing the LED and transistor voltages, we **calibrate**: Lesson 02's simulation gave 18.8 mA at 4.5 V and 6.8 mA at 3.6 V. A straight line through those two points is

```
I_on ≈ (V_battery - 3.09 V) / 75 Ω
```

Check it at 4.2 V: `(4.2 - 3.09) / 75 = 14.8 mA` (simulation: 14.7 mA). At 3.9 V: 10.8 mA (simulation: 10.7 mA). Good enough. A real product would calibrate against measurements of real LEDs, or use a constant-current driver instead.

The duties that result, and the simulated average currents with them:

| Battery | Duty | Average (compensated) | Average with a fixed 30% |
|---|---|---|---|
| 4.5 V | 30.2% | 5.71 mA | 5.66 mA |
| 4.2 V | 38.5% | 5.72 mA | 4.42 mA |
| 3.9 V | 53.0% | 5.65 mA | 3.21 mA |
| 3.6 V | 83.8% | 5.70 mA | 2.04 mA |

The compensated average stays within 1.2% across the whole battery range (R5 asks for 20%). Without compensation the light would fall to a third of its brightness by the end of the batteries.

### The night scenario

A realistic test needs a realistic night. Our scenario, from 18:00 to 09:00:

```
18:00-19:30   evening, about 120 lux
19:30-21:00   dusk: light falls smoothly from 120 to about 0.5 lux
21:00-06:00   night, about 0.5 lux
06:00-07:30   dawn: light rises from 0.5 to about 400 lux
07:30-09:00   day, 400 lux
all the time  a slow random-looking wobble of +/-25% (clouds, trees, curtains)
23:30, 02:12  car headlights: 60 lux for 2 seconds
```

The wobble is the dangerous part: during dusk and dawn, the light crosses each threshold slowly while wobbling, exactly the situation in which a single threshold chatters.

### What happens

Running both firmwares on this night, one decision per second:

| Firmware | Switchings | Hours on | Headlights |
|---|---|---|---|
| hysteresis + 4 s average | 2 | 10.4 | LED stays on |
| single threshold, no averaging | 32 | 10.4 | LED goes off, twice |

The final firmware switches exactly twice: on once at dusk (about 20:19), off once at dawn (about 06:44). The naive firmware chatters 30 extra times during dusk and dawn and blinks off at each car. Both are "on" for the same total time, which is why such bugs survive simple tests and show up only in a scenario.

## Build It

Run:

```
uv run python phases/22-capstone/04-simulation/code/main.py
```

### Step 1: PWM in the transient simulator

```python
def pwm_led(vbat, duty, cycles=40):
    period = 1 / PWM_HZ
    c = Circuit()
    c.voltage_source("BAT", "bat_ideal", "0", vbat)
    c.resistor("R_INT", "bat_ideal", "vbat", 0.5)
    c.pulse_source("PB1", "pin", "0", low=0.0, high=VDD, period=period, duty=duty)
    c.resistor("R4", "pin", "base", 2200)
    c.npn("Q1", c="led_k", b="base", e="0", beta=100)
    c.resistor("R5", "vbat", "led_a", 68)
    c.led("D1", "led_a", "led_k", color="white")
    t = c.transient(t_stop=cycles * period, dt=period / 200)
    last = t.time >= (cycles - 10) * period
    current = t.i("D1")
    return t.time, current, float(current[last].mean()), float(current.max())
```

40 PWM periods with 200 time steps each; the average is taken over the last 10 periods. Output: peak 18.80 mA, average 5.66 mA, LED on 30.1% of the time.

### Step 2: The firmware and its compensation

```python
class Firmware:
    def __init__(self, hysteresis=True, averaging=True):
        ...

    def duty_for(self, vbat_code):
        vbat = vbat_code / ADC_MAX * VDD * 2
        on_current = max((vbat - 3.09) / 75.0, 1e-4)
        return min(TARGET_AVG_A / on_current, 1.0)

    def tick(self, light, vbat_code):
        self.history = (self.history + [light])[-AVERAGE_SAMPLES:]
        value = sum(self.history) / len(self.history) if self.averaging else light
        if self.hysteresis:
            wanted = (value < ON_CODE) if not self.on else not (value > OFF_CODE)
        else:
            wanted = value < (ON_CODE + OFF_CODE) / 2
        ...
```

`duty_for` converts the battery code back to volts (times 2 for the divider), estimates the on-current with the calibrated line, and returns the duty, never above 100%. For each battery voltage, the script runs `pwm_led` with the compensated duty and with a fixed 30%: the table above.

### Step 3: The night

```python
def run_night(firmware, vbat=4.2):
    seconds = np.arange(0, 15 * 3600)
    ...
    for n, s in enumerate(seconds):
        lux[n] = night_lux(float(s))
        noise = 2.0 * math.sin(s * 1.7)
        duties[n] = firmware.tick(light_code(lux[n], noise), battery_code(vbat))
```

54,000 decisions, one per simulated second. `night_lux` is the scenario; `light_code` uses the LDR model and the divider and rounds to a 10-bit code, plus the small deterministic noise. The script prints the switchings, the hours on, the first and last "on" times, and what happens at each headlight flash, for both firmwares.

### Step 4: The plot

The light on a logarithmic axis and the duty of both firmwares, saved as `night.png`.

### Step 5: The lab

The script evaluates each PWM duty offered in the lab, reading the filtered sense voltage.

## Use It

- **Firmware-in-the-loop testing**: real teams run their actual firmware against simulated sensors (or recorded sensor data) on a PC before the hardware exists. Our Python `Firmware` class plays that role; in Phase 17, Lesson 07 we ran real assembly code on a virtual microcontroller.
- **Hardware-in-the-loop**: later, the real board is connected to a test rig that plays back scenarios (a programmable light source in a dark box, for example).
- **SPICE simulations of LED drivers** are standard in LED and power design, often with manufacturers' device models (LTspice from Analog Devices is free).
- **Scenario libraries**: automotive and medical products are tested against long, documented lists of scenarios and edge cases; finding the "headlights at 2 am" case is the engineer's job.
- **Calibration in production**: sensors are often calibrated per unit at the factory and the constants stored in the microcontroller's non-volatile memory.

## Try It in the Lab

Open "Dim the night light with PWM". The LED draws about 19 mA when on. Choose the PWM duty (10%, 30%, 50% or 90%) so the average is between 5.0 and 6.5 mA. The circuit measures the average with a 1 Ω resistor under the emitter and a 10 ms RC filter, so the filtered voltage in millivolts equals the average current in milliamps. Estimate each duty's result with `duty * 19 mA` before running. Why is the filtered value slightly higher than the true average in the simulation? (Hint: the filter's ripple and where the last sample falls.)

## Common Mistakes

- **Testing firmware only with clean, steady inputs.** Real light wobbles; test with noise, slow ramps and short disturbances.
- **Hysteresis without averaging, or averaging without hysteresis.** Each solves a different problem: hysteresis stops chatter near a threshold, averaging ignores short flashes. The night light needs both.
- **Compensating with a guessed formula.** Fit the compensation to simulation or measurement; check it at the edges of the range.
- **Forgetting the duty limit.** Compensation cannot exceed 100%; below about 3.5 V the target cannot be met and the firmware should say so (blink, or accept dimming).
- **Too slow PWM.** At 50-100 Hz, PWM flicker is visible, especially when moving your eyes.

## Exercises

1. What average current does 45% duty give at 4.2 V (on-current 14.7 mA)? What duty would you need for 5.7 mA at 4.0 V, using the calibrated formula?
2. Change `AVERAGE_SAMPLES` to 1 (no averaging) but keep the hysteresis. Run the night. Does it chatter at dusk? Does it react to the headlights?
3. Lengthen the headlight flash in `night_lux` to 4 seconds. Does the final firmware still keep the LED on? What is the longest flash it ignores, and how would you change the firmware to ignore 10-second flashes?
4. Run `pwm_led` at 200 Hz and at 5 kHz (change `PWM_HZ`). Does the average current change? What changes?
5. Harder: simulate a whole month. Start the battery at 4.5 V and lower it each night according to the charge used (61.8 mAh per day out of 2,000 mAh, with the voltage falling linearly from 4.5 V to 3.6 V as the charge is used). Record the average LED current each night. On which night does the duty first reach 100%?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Transient simulation | "simulating over time" | Solving the circuit at many successive time steps |
| PWM average | "the brightness" | `duty * I_on`, what the eye perceives above about 100 Hz |
| State machine | "on/off logic" | A small set of states with rules for moving between them |
| Moving average | "smoothing" | The mean of the last N samples, which ignores events shorter than a few samples |
| Hysteresis | "dead band" | Separate on and off thresholds; no chatter near a threshold |
| Compensation | "correction" | Changing the duty with the battery voltage to keep the average current constant |
| Scenario test | "a realistic run" | Testing the whole system against a sequence of events including edge cases |

## Further Reading

- Phase 17, Lesson 07 of this course (A Virtual Microcontroller) — the same night light running as real assembly on a simulated chip.
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., the sections on LED drive and on digital filtering of sensor data.
- Analog Devices, *LTspice* (free) and its LED driver examples ([analog.com](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html)).
- Elecia White, *Making Embedded Systems* (O'Reilly, 2nd ed., 2024) — state machines, testing and low-power firmware.
