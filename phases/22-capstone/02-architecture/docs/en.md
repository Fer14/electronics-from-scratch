# Architecture

> Architecture is choosing the blocks and how energy and information flow between them. Get it right and every later step is easy; get it wrong and no clever resistor will save you.

**Type:** Build
**Prerequisites:** Phase 22 (Capstone), Lesson 01 (Requirements); Phase 12 (Transistors), Lesson 03 (The BJT as a Switch); Phase 17 (Microcontrollers), Lessons 03 (PWM), 04 (ADC and DAC) and 05 (Timers and Interrupts); Phase 18 (Power Electronics), Lessons 01 (Linear Regulators) and 06 (Batteries and Charging)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Architecture | The choice of main blocks and the connections between them | The floor plan of a house before choosing the tiles |
| Block diagram | A drawing of the blocks as boxes and the signals or power between them as arrows | A subway map |
| Power tree | Which supply feeds which part, through which regulators | The pipes from the water main to every tap |
| LDO | Low-dropout linear regulator: makes a steady lower voltage from a higher one, even when the two are close | A pressure-reducing valve |
| Dropout voltage | The minimum difference between input and output for an LDO to keep regulating | The pressure the valve needs to work |
| Quiescent current | The current a part draws just by being on, doing nothing useful | A fridge's hum when the door is closed |
| Low-side switch | A transistor between the load and ground that turns the load on and off | A tap on the drain instead of the inlet |
| Sleep mode | A state in which a microcontroller stops its CPU and most clocks, drawing microamps | A phone with its screen off |
| Watchdog / wake-up timer | A small always-running timer that wakes the microcontroller periodically | An alarm clock |
| Duty of operation (wake fraction) | The fraction of time a block is awake and drawing its active current | Hours per day a shop is open |
| Ratiometric measurement | Measuring a sensor with the same voltage that powers it as the ADC reference, so supply changes cancel | Measuring a picture's proportions, not its absolute size |
| Trade-off | Accepting a worse number in one place for a better one elsewhere | Paying more for a car that uses less fuel |

## Learning Objectives

- Draw the block diagram and the power tree of the night light, and justify each block from the requirements.
- Compare alternative architectures (analog, microcontroller-based, different batteries) by battery life and features.
- Build a current budget for every operating state (sleep, wake-up, LED on) and turn it into nights of battery life.
- Simulate the LED driver at several battery voltages and compute the PWM duty needed to keep the brightness constant (requirement R5).
- Spot the biggest consumer in the budget and propose where to improve the design.

## The Problem

Lesson 01 said *what* the night light must do. Now we decide *how*, at the level of blocks. There are many possible designs:

- No microcontroller at all: an LDR and a transistor wired so that darkness turns the transistor on. Cheap, but it cannot dim the LED, has no clean hysteresis, and its sensor divider draws current day and night.
- A microcontroller that sleeps most of the time, wakes once a second to read the light, and drives the LED with PWM. More parts, but it can do hysteresis, averaging, dimming and battery compensation.
- Different power sources: three AA cells, a rechargeable lithium-ion cell, a coin cell.

Each choice changes the battery life, the cost, the features, and which requirements can be met at all. This lesson makes the choice with numbers.

## The Physics

### Where the energy goes

Every block draws current from the battery in each state. The charge taken per day is the sum, over states, of current times time:

```
charge per day = sum over states of (current in that state * hours in that state)
```

"Add up milliamps times hours for every state." Divide the battery capacity by it to get days. Two kinds of current matter:

- **Active current**: what a block draws while doing its job (the LED lit, the microcontroller computing).
- **Quiescent current**: what it draws just by being powered (the regulator's own circuits, a resistor divider permanently across the battery, a sleeping microcontroller's timer).

A device that sleeps most of the time is often dominated by quiescent currents; ours is the opposite, because its main job (light) is energy-hungry.

### The LED driver and the falling battery

The LED and its resistor are powered straight from the battery, and an NPN transistor switches them to ground (a low-side switch, Phase 12, Lesson 03). When the transistor is saturated, the LED current is set by Ohm's law across the resistor:

```
I_LED = (V_battery - V_LED - V_CE(sat)) / R_LED
```

With a white LED's 3.1 V, a saturated transistor's 0.1 V and 68 Ω: at 4.5 V, `(4.5 - 3.1 - 0.1) / 68 = 19 mA`; at 3.6 V, `(3.6 - 3.1 - 0.1) / 68 = 6 mA`. The battery's fall of 20% cuts the LED current by two thirds, because only the small *difference* between the battery and the LED's voltage drives the current. That is why R5 needs the firmware to compensate.

### Why an LDO, and why such a small one

The microcontroller and the ADC want a steady supply. A linear regulator (Phase 18, Lesson 01) drops the battery's 3.6-4.5 V to 3.3 V. Its efficiency is poor in principle (`3.3 / 4.5 = 73%` at best), but the microcontroller draws so little that the loss is microwatts. Two numbers matter more:

- **Dropout**: the LDO must still regulate when the batteries are down to 3.6 V. A low-dropout part like the Microchip MCP1700 drops under 0.2 V even at 250 mA, and only tens of millivolts at our 1 mA.
- **Quiescent current**: about 1.6 µA for the MCP1700, against 5 mA for the classic 7805-style regulators. With a 5 mA regulator, the "sleeping" device would draw 120 mAh per day: twice the LED's budget.

The LED does not go through the LDO: it takes its current directly from the battery, so the LDO only has to supply the microcontroller.

## The Concept

### The block diagram

```
   3 x AA (4.5 V fresh, 3.6 V end) --+--> LDO 3.3 V --> microcontroller
          (about 0.5 Ω internal)     |                   | PB2 -> powers the LDR divider only while measuring
                                     |                   | ADC0 <- LDR / 10 kΩ divider (light)
                                     |                   | ADC1 <- 470 kΩ / 470 kΩ divider (battery voltage)
                                     |                   | PB1 -> PWM 1 kHz -> 2.2 kΩ -> NPN base
                                     |
                                     +--> 68 Ω --> white LED --> NPN collector; emitter to ground
```

Design choices worth noticing:

- **The LDR divider is powered from a microcontroller pin**, not from the 3.3 V rail. The pin is switched on only during the 2 ms of each measurement, so the divider's 0.165 mA flows 0.2% of the time.
- **The light measurement is ratiometric**: the divider and the ADC both use the same 3.3 V, so the code depends only on the resistor ratio, not on the exact supply voltage.
- **The battery is measured** through a high-value divider (two 470 kΩ) on a second ADC input. Its 4.8 µA is permanent but small. (A capacitor at the ADC pin, 100 nF, gives the ADC the brief current it needs at the moment of sampling.)
- **The LED takes its current from the battery directly**, switched by the NPN transistor; the microcontroller pin only supplies the base current.

### The current budget

| State | Block | Current | Time fraction | Average |
|---|---|---|---|---|
| always | microcontroller asleep, wake-up timer | 4.0 µA | 100% | 4.0 µA |
| always | LDO quiescent | 1.6 µA | 100% | 1.6 µA |
| always | battery divider (4.5 V / 940 kΩ) | 4.8 µA | 100% | 4.8 µA |
| every second | microcontroller awake 2 ms (1 mA) + LDR divider (0.165 mA) | 1.165 mA | 0.2% | 2.3 µA |
| **day total** | | | | **12.7 µA** |
| night | LED (average, 5.7 mA target) | | | 5.7 mA |
| night | transistor base current (1.16 mA while on, about 39% duty) | | | 0.45 mA |
| **night total** | | | | **6.16 mA** |

Per day: `6.161 mA * 10 h + 0.0127 mA * 14 h = 61.6 + 0.18 = 61.8 mAh`. From 2,000 mAh: **32 nights**, meeting R4 (30 nights) with a small margin. That is a little less than the 35 nights of Lesson 01's first estimate, because now we have counted the base current and the duty needed at a typical, partly used battery voltage (4.2 V).

Where does it go?

```
LED              57.0 mAh per day  (92.3%)
transistor base   4.5 mAh per day   (7.3%)
everything else   0.3 mAh per day   (0.5%)
```

This tells us exactly where to look for improvements. Everything except the LED and the base current is irrelevant. The base current is a surprise: 7% of the energy just to hold the transistor on. A logic-level N-channel MOSFET instead of the NPN would need no steady gate current at all (Phase 12, Lesson 05), adding about 2 nights. We keep the NPN for now, because its behaviour is easy to check by hand, and note the MOSFET as an improvement for Lesson 07.

### R5: compensation as the battery falls

The simulator gives the LED current with the transistor fully on, including the battery's internal resistance:

| Battery | At its terminals | LED current (on) | Duty for a 5.7 mA average |
|---|---|---|---|
| 4.5 V | 4.491 V | 18.8 mA | 30.3% |
| 4.2 V | 4.193 V | 14.7 mA | 38.8% |
| 3.9 V | 3.895 V | 10.7 mA | 53.4% |
| 3.6 V | 3.597 V | 6.8 mA | 83.9% |

So the firmware can keep the average current constant all the way down to 3.6 V by raising the duty from 30% to 84%. Below about 3.5 V even 100% duty would not be enough; that is a natural "battery empty" point at which the firmware could blink a warning.

A subtle point: the *peak* current changes even if the average does not. At the end of the batteries the LED is on longer at a lower current. Our eyes respond to the average light (at 1 kHz they cannot see the pulses), so brightness stays constant to a good approximation.

### Alternatives, compared

| Option | Nights | Notes |
|---|---|---|
| 3 x AA, our design | 32.4 | meets every requirement |
| 3 x AA, analog LDR + transistor, LED at full brightness | 10.3 | no dimming, no hysteresis; the divider draws 0.165 mA day and night |
| 1 x Li-ion 18650, 2,500 mAh | 40.5 | rechargeable, but needs a charger circuit (Phase 18, Lesson 06) and a different LED resistor |
| 1 x CR2032 coin cell, 220 mAh | 3.6 | far too small, and coin cells cannot deliver 19 mA pulses without a large voltage drop |

The microcontroller costs more than a comparator, but it is what makes the month of battery life possible: dimming to 30% alone triples the battery life, and it adds hysteresis, averaging and battery compensation in software for free.

## Build It

Run:

```
uv run python phases/22-capstone/02-architecture/code/main.py
```

### Step 1: The blocks

The block diagram is printed as text, so it lives next to the numbers that justify it.

### Step 2: Sleep and wake currents

```python
SLEEP_CURRENTS_UA = {
    "microcontroller asleep, watchdog running": 4.0,
    "LDO quiescent current": 1.6,
    "battery-sense divider (2 x 470 kOhm)": 4.5 / 940e3 * 1e6,
}

WAKE = {"period_s": 1.0, "awake_s": 0.002, "mcu_active_ma": 1.0, "ldr_divider_ma": 3.3 / 20e3 * 1000}
```

The microcontroller numbers are typical of small 8-bit parts (ATtiny- or PIC-class) at 1 MHz; the LDO number is from the MCP1700 datasheet. Output: 12.72 µA daytime average.

### Step 3: The LED driver at four battery voltages

```python
def led_on_current(vbat):
    c = Circuit()
    c.voltage_source("BAT", "bat_ideal", "0", vbat)
    c.resistor("R_INT", "bat_ideal", "vbat", R_INTERNAL)
    c.voltage_source("PIN", "pin_ideal", "0", VDD)
    c.resistor("R_PIN", "pin_ideal", "pin", PIN_OHMS)
    c.resistor("R_BASE", "pin", "base", R_BASE)
    c.npn("Q1", c="col", b="base", e="0", beta=100)
    c.resistor("R_LED", "vbat", "led_a", R_LED)
    c.led("D1", "led_a", "col", color="white")
    r = c.dc()
    return r.i("D1"), r.i("R_BASE"), r.v("vbat")
```

The battery is an ideal source plus 0.5 Ω of internal resistance (Phase 06, Lesson 02); the microcontroller pin is an ideal 3.3 V source with about 25 Ω of output resistance. The table above is the output.

### Step 4: Battery life

`average_currents_ma` adds the sleep currents, the wake-ups, the LED average and the base current; `nights_from` turns them into mAh per day and nights. Output: 61.8 mAh per day, 32 nights, with the shares of LED, base and everything else.

### Step 5: Alternatives

The same function for the other options.

## Use It

- **Real parts for these blocks:** an MCP1700 or TPS7A02 LDO (around 1 µA or less quiescent current); an ATtiny202/ATtiny85, PIC12, or a small ARM Cortex-M0+ such as the STM32L0 (sleep currents from below 1 µA to a few µA); a 2N3904 or BC547 NPN, or a 2N7002/AO3400 MOSFET; a 5 mm or SMD white LED.
- **Battery datasheets** show capacity falling at high current and low temperature; designers derate (use 70-80% of the nominal capacity) for safety.
- **Constant-current LED drivers** are the professional alternative to our resistor plus compensation: a small chip regulates the LED current regardless of the battery voltage, at the cost of another part.
- **Boost converters** (Phase 18, Lesson 04) let a single AA cell (1.5 V) drive a white LED (3.1 V); that is how many cheap torches work.
- **Low-power design practice:** turn sensors on only while measuring, use high-value resistors in always-on dividers, prefer MOSFETs to BJTs for switches, sleep as much as possible.

## Common Mistakes

- **Picking an LDO by output voltage only.** A regulator with milliamps of quiescent current can drain the battery faster than the load.
- **Leaving dividers permanently powered.** A 20 kΩ divider across 3.3 V draws 0.165 mA forever; switched by a pin it costs 0.2% of that.
- **Feeding the LED through the regulator.** It would put the LED's current through the LDO's dropout and waste its headroom; the LED does not need a precise supply.
- **Forgetting the base current.** A BJT switch needs a steady base current; for a small load it can be a noticeable share of the budget.
- **Budgeting only with fresh batteries.** Requirements must hold at the end voltage too; here it decides the duty range the firmware needs.

## Exercises

1. If the microcontroller woke every 4 seconds instead of every second, what would the daytime average current be? Does it change the number of nights noticeably? Why?
2. Replace the 470 kΩ battery divider by two 10 kΩ resistors. How many nights do you lose?
3. Replace the NPN by a MOSFET (no gate current). Recompute the nights with the script (set the base current to zero in Step 4).
4. With `R_LED = 47 Ω` instead of 68 Ω, what LED current flows at 4.5 V and at 3.6 V? What duty range would the firmware need? Use `led_on_current` with a modified resistor.
5. Harder: estimate how many nights a single 18650 Li-ion cell (3.0-4.2 V) would give if you redesigned `R_LED` for 19 mA at 3.7 V. What duty would the firmware need at 3.0 V? Is it still possible?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Architecture | "the high-level design" | The blocks, their interfaces and the flow of power and signals |
| Power tree | "who powers what" | The path from the battery through regulators to every load |
| LDO | "a regulator" | A linear regulator that works with a small input-output difference; low quiescent current matters for batteries |
| Quiescent current | "standby current" | Current drawn by a part just by being on |
| Low-side switch | "a transistor to ground" | A switch between the load and ground, driven from a logic-level pin |
| Current budget | "power budget" | Current x time per state, summed per day, compared with battery capacity |
| Ratiometric | "relative measurement" | Using the sensor's supply as the ADC reference so supply variations cancel |

## Further Reading

- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., section 10.7 (micropower digital design) and section 13.10.3 (micropower A/D converters).
- Microchip, *MCP1700 Low Quiescent Current LDO* datasheet, and Texas Instruments, *TPS7A02* datasheet.
- Microchip, *ATtiny202/402 datasheet*, section on sleep modes and power consumption.
- Jack Ganssle, "The Embedded Muse" and his articles on battery life of microcontroller designs ([ganssle.com](http://www.ganssle.com/)).
