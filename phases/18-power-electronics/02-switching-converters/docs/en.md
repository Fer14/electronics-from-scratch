# Switching Converters

> A perfect switch never gets warm: when it is closed there is no voltage across it, and when it is open there is no current through it. Chop the input with one, smooth the result with parts that store energy instead of burning it, and you can change voltage with almost no loss.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 18 (Power Electronics), Lesson 01 (Linear Regulators); Phase 17 (Microcontrollers), Lesson 03 (PWM); Phase 08 (Magnetism and Inductors), Lessons 04-05 (The Inductor, RL Transients); Phase 07 (Capacitors), Lesson 06 (Energy in the Electric Field); Phase 12 (Transistors), Lesson 05 (The MOSFET as a Switch)
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Switching converter | A circuit that changes one DC voltage into another by switching on and off very fast and smoothing the result. Also called a switch-mode power supply (SMPS). | Filling a bucket by opening and closing a tap in quick bursts, instead of keeping it half-open. |
| Ideal switch | A switch with zero resistance when closed and infinite resistance when open, that changes state instantly. | A perfect door: either wide open or sealed shut. |
| Chopping | Switching the input on and off to produce pulses. | Slicing a long sausage into pieces. |
| Duty cycle (D) | The fraction of each period the switch is closed (Phase 17, Lesson 03). | The fraction of each minute the tap is open. |
| Switching frequency | How many on-off cycles per second, typically 100 kHz to a few MHz. | How many bursts per second. |
| Switch node | The point where the switch connects to the filter; its voltage jumps between levels. | The spot right under the tap. |
| Filter | Parts that smooth the pulses into a steady voltage. | A big tank that turns bursts of water into a steady flow. |
| Lossless element | A part that stores energy and gives it back, instead of turning it into heat: ideal inductors and capacitors. | A spring, which gives back what you put in, versus friction, which keeps it. |
| Freewheeling | Giving an inductor's current a path to keep flowing when the main switch opens. | A bicycle's freewheel: the wheel keeps turning when you stop pedalling. |
| Inductive kick | The huge voltage an inductor makes when its current is suddenly interrupted. | Water hammer: slam a tap shut and the pipes bang. |
| Conduction loss | Heat from current flowing through a switch's small on-resistance: I^2 x R_on. | Friction in a door hinge that is almost, but not quite, frictionless. |
| Switching loss | Heat during the brief moment while a real switch changes state and has both voltage and current. | The scrape as the door swings. |

## Learning Objectives

- Explain, from P = V x I, why an ideal switch dissipates no power in either state
- Show in the simulator that chopping a voltage into a resistor delivers D x V^2 / R with no loss in the switch
- Compare smoothing pulses with an RC filter (lossy) and an LC filter (lossless) and compute the efficiency of each
- Explain why an inductor needs a freewheel path, and estimate the inductive kick I x sqrt(L / C) when it has none
- Compare linear and switching regulation by efficiency and heat for different input voltages

## The Problem

Lesson 01 ended with a bleak table. Making 5 V at 1 A from 24 V with a linear regulator throws away 19 W as heat and has an efficiency of 21%. From 48 V (common in telecom and electric bikes) it is 43 W wasted, 10% efficient. A laptop that needs 20 W at 1 V for its processor from a 20 V adapter would turn 380 W into heat, more than a room heater. Phones would burn your hand and last an hour.

Every modern device solves this with switching converters. Your phone charger, your laptop's power brick, the dozen little regulators on a computer's motherboard, an LED bulb's driver, an electric car's motor inverter: all switch. They routinely reach 85-97% efficiency, whatever the ratio of input to output voltage. This lesson shows the two ideas that make that possible: switches that do not dissipate, and filters that store rather than burn.

## The Physics

### A switch that does no work

Power in any part is voltage across times current through (Phase 03, Lesson 05). Look at a perfect switch in its two states:

```
closed:   V across = 0          I through = anything   ->  P = 0 x I = 0
open:     V across = anything   I through = 0          ->  P = V x 0 = 0
```

In neither state does it turn energy into heat. A linear regulator's transistor is the opposite: it sits *between* those states, with several volts across it and amps through it, by design.

Real switches are MOSFETs (Phase 12, Lesson 05). Fully on, a power MOSFET has an on-resistance of a few milliohms to tens of milliohms; fully off it leaks microamps. So it is very close to ideal *in each state*. Its losses come from the small on-resistance (`I^2 x R_on`) and from the few nanoseconds of each transition when both voltage and current are present. Switching faster reduces the transition loss per switch but adds more transitions per second; that trade-off sets the practical frequency range.

### Chopping gives the right average, but in pulses

If the switch connects 12 V to a heater for 40% of the time, the heater gets 12 V for 40% of the time and 0 V for 60%. A heater (a resistor) does not care about pulses: its power is `V^2 / R` while on, so its average power is `D x V^2 / R`. Electric stoves and soldering irons control power exactly like that. Electronics, though, needs a steady voltage, not pulses.

### Smoothing without burning

The RC low-pass filter of Phase 17, Lesson 03 averages pulses, but its resistor carries the whole load current and big ripple currents. That resistor turns power into heat; you are back to a lossy regulator.

The way out is to smooth with parts that **store energy instead of dissipating it**:

- An **inductor** stores energy in its magnetic field, `E = 1/2 L I^2` (Phase 08). It resists changes of current: `V = L dI/dt`. Put it in series with the load and the current through it cannot jump; it ramps.
- A **capacitor** stores energy in its electric field, `E = 1/2 C V^2` (Phase 07). It resists changes of voltage. Put it across the load and the voltage cannot jump.

An ideal L and C absorb energy during part of the cycle and return it later. Nothing is lost.

### The inductor must always have a path

An inductor's current cannot change instantly: `V = L dI/dt` means a sudden stop needs an enormous voltage. If the switch opens and the inductor's current has nowhere to go, the inductor *creates* that voltage, as large as needed to keep the current flowing through whatever is there: the stray capacitance of the wiring, or an arc across the switch. The energy `1/2 L I^2` must go somewhere.

When the inductor's current pours into a stray capacitance `C`, energy conservation gives the peak voltage:

```
1/2 L I^2 = 1/2 C V^2   ->   V = I x sqrt(L / C)
```

With 1.2 A, 100 uH and 100 pF: `V = 1.2 x sqrt(100e-6 / 100e-12) = 1.2 x sqrt(1e6) = 1.2 x 1000 = 1200 V`. That destroys a 30 V MOSFET instantly. This is the same physics as a car's ignition coil, used on purpose there.

The fix is a **freewheel path**: a diode (or a second switch) from ground to the switch node. When the main switch opens, the inductor's current simply flows up through the diode instead, and the switch node only goes about 0.7 V below ground.

## The Concept

### The basic switching cell

Put it together: a switch, a freewheel path, an inductor and a capacitor.

```
           S_high (main switch)
   Vin ----o/ o----+----[ L ]----+------+---- Vout
                   |  sw node    |      |
                   |            === C  load
         S_low or  |             |      |
         diode    /              |      |
                   |             |      |
   gnd ------------+-------------+------+
```

- S_high closed (time `D x T`): the switch node is at Vin. The inductor has `Vin - Vout` across it, so its current ramps up.
- S_high open, S_low closed (time `(1 - D) x T`): the switch node is at 0 V. The inductor has `-Vout` across it, so its current ramps down, flowing through S_low.

The switch node is a square wave between 0 and Vin, with average `D x Vin`. The LC filter passes the average and blocks the switching frequency. That is exactly the PWM-plus-filter of Phase 17, with a lossless filter. It is the **buck converter**, studied in the next lesson. Swapping the positions of the parts gives a **boost** (Lesson 04), which can raise the voltage, something no linear regulator can do.

### RC versus LC, with numbers

Both filters below take the same half-bridge switching between 12 V and 0 V and feed a 5 ohm load.

**RC filter** (1 ohm, 1000 uF): to get 5 V at the load, the average switch node must be `5 x 6/5 = 6 V` (the 1 ohm and 5 ohm form a divider), so D = 0.5. The resistor then carries `(12 - 5) / 1 = 7 A` while the switch is high and `5 / 1 = 5 A` backwards while it is low:

```
loss in R = 0.5 x 7^2 x 1 + 0.5 x 5^2 x 1 = 24.5 + 12.5 = 37 W
P_load = 5^2 / 5 = 5 W
efficiency = 5 / (5 + 37) = 12%
```

Worse than a linear regulator.

**LC filter** (100 uH, 100 uF): D = 5/12. No resistor; an ideal inductor and capacitor dissipate nothing. Efficiency: 100%, within the simulator's rounding.

### Ripple of the LC filter

During the on-time the inductor current rises by:

```
delta_I = (Vin - Vout) x D x T / L = (12 - 5) x (5/12) x 20 us / 100 uH = 7 x 8.33e-6 / 1e-4 = 0.583 A
```

This ripple current flows into and out of the capacitor. A standard result for the buck (derived in Lesson 03) is that the output ripple is:

```
delta_V = delta_I / (8 x f x C) = 0.583 / (8 x 50 000 x 100e-6) = 0.583 / 40 = 14.6 mV
```

The simulator measures 15.1 mV.

### Linear versus switching

Making 5 V at 1 A (5 W):

| Input | Linear efficiency | Linear heat | Switcher at 90% heat |
|-------|-------------------|-------------|----------------------|
| 7 V | 71% | 2.0 W | 0.56 W |
| 12 V | 42% | 7.0 W | 0.56 W |
| 24 V | 21% | 19 W | 0.56 W |
| 48 V | 10% | 43 W | 0.56 W |

A switcher's heat barely depends on the input voltage. (A switcher at 90% loses `5 / 0.9 - 5 = 0.56 W`.)

Why not always switch? Switchers are more complex, need an inductor, and produce **noise** at the switching frequency and its harmonics, both on the output (ripple) and radiated (fast edges are little radio transmitters). Sensitive circuits often get a switcher followed by a small LDO.

### Worked example: following the energy for one period

Where does the energy go in the LC case? At 5 W and 50 kHz, the load takes `5 W x 20 us = 100 uJ` per period. Look at the inductor:

```
current at the bottom of its ripple:  1.0 - 0.29 = 0.71 A   ->  stored 1/2 x 100e-6 x 0.71^2 = 25 uJ
current at the top of its ripple:     1.0 + 0.29 = 1.29 A   ->  stored 1/2 x 100e-6 x 1.29^2 = 83 uJ
```

During the on-time the source pushes energy both into the load and into the inductor (its store grows by 58 uJ); during the off-time the inductor hands those 58 uJ to the load while the source supplies nothing. The capacitor, holding `1/2 x 100e-6 x 5^2 = 1.25 mJ`, barely notices: it is a big reservoir that smooths the small ripple. Nothing is burned; energy is only moved around in time.

Compare the RC case: every joule that reaches the load first passes through the 1 ohm resistor, which takes its `I^2 R` toll on the way, both when the current flows in and when it flows back out.

### Worked example: how fast is "fast enough"?

Why switch at 50 kHz and not 50 Hz? The ripple current is `(Vin - Vout) x D / (f x L)`. To keep 0.29 A of ripple at 50 Hz instead of 50 kHz, the inductor would have to be 1000 times bigger: 100 mH, a heavy iron-cored part the size of a fist, carrying 1 A. At 1 MHz it could be 5 uH, smaller than a fingernail. That is the whole reason for high switching frequencies: smaller, cheaper, lighter inductors and capacitors. The limit is the switches' transition losses, which happen at every edge and so grow with frequency.

### Worked example: the cost of a slow switch

A real MOSFET takes perhaps 20 ns to switch, and during that time it has, on average, about half the voltage and half the current. With 12 V and 1 A, each transition costs roughly:

```
energy per edge = 1/2 x (12 V x 1 A) x 20 ns ~ 0.5 x 12 x 20e-9 = 120 nJ   (a rough triangle estimate)
two edges per period at 50 kHz:  2 x 120 nJ x 50 000 = 12 mW
the same at 1 MHz:               2 x 120 nJ x 1 000 000 = 240 mW
```

At 50 kHz switching loss is negligible; at 1 MHz it is 5% of a 5 W converter. Designers choose the frequency where the sum of switching loss and the size of the passives is best.

### Worked example: average versus RMS of a chopped voltage

Chop 12 V at D = 0.25. Two different "sizes" of the result matter:

```
average:  D x 12 V = 0.25 x 12 = 3 V
RMS:      sqrt(mean of V^2) = sqrt(0.25 x 12^2 + 0.75 x 0^2) = sqrt(36) = 6 V
```

A resistive heater responds to the RMS (its power is `V_rms^2 / R = 36 / 10 = 3.6 W`, as in the simulation's first row); an LC filter delivers the average (3 V) to its load. A cheap multimeter in DC mode shows roughly the average. So the same chopped waveform is "3 V" or "6 V" depending on who is looking. Always ask which one a load cares about.

## Build It

### Step 1: Switch timing on the simulator's grid

The simulator's switches accept a list of moments at which they toggle. `pwm_toggles` makes that list for any duty cycle. It places each toggle half a time step away from a sample, so there is never any doubt about which state the switch is in at each step, and every period has exactly the same on-time:

```python
def pwm_toggles(duty, cycles=CYCLES, steps=STEPS):
    on_steps = round(duty * steps)
    dt = PERIOD / steps
    moments = []
    for k in range(cycles):
        moments += [(k * steps + on_steps - 0.5) * dt, ((k + 1) * steps - 0.5) * dt]
    return moments
```

(With 120 steps per period, both 5/12 and 1/2 are exact.)

### Step 2: Chopping into a heater

`chopper_into_heater` puts one switch between 12 V and a 10 ohm resistor. The script averages the source power and the heater power over the last 10 periods. They agree with `D x V^2 / R`, and the difference ("lost") is under a few milliwatts, the switch's 1 milliohm on-resistance.

### Step 3: A half-bridge and two filters

```python
def add_half_bridge(circuit, duty, node="sw"):
    toggles = pwm_toggles(duty)
    circuit.switch("SHIGH", "vin", node, closed=True, toggle_at=toggles)
    circuit.switch("SLOW", node, "0", closed=False, toggle_at=toggles)
```

Two switches toggling at the same moments, one starting closed and one open, are always opposite: a **half-bridge**. `filtered("rc", ...)` and `filtered("lc", ...)` add the two filters. To skip the slow start-up, the capacitor starts at the expected output and the inductor at the expected lowest current of its ripple.

### Step 4: The inductive kick

`inductive_kick` lets 1.2 A flow through 100 uH, opens the switch after 11 ns, and watches the switch node with only 100 pF of stray capacitance. Then it repeats with a diode from ground to the switch node.

Run it:

```
uv run python phases/18-power-electronics/02-switching-converters/code/main.py
```

You will see the heater receiving exactly `D x V^2 / R`; the RC filter at 12% efficiency and the LC filter at 100% with about 15 mV of ripple; the switch node diving to about -1190 V without a freewheel path and to under 1 V below ground with the diode; and the linear-versus-switching table.

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
An ideal switch chopping 12 V into a 10 ohm heater at 50 kHz
   duty   avg V    P in  P heater      lost  D x V^2/R
   0.25  3.01 V  3.61 W    3.61 W   0.36 mW   3.60 W
   0.50  6.00 V  7.21 W    7.20 W   0.72 mW   7.20 W
   0.75  9.00 V 10.80 W   10.80 W   1.08 mW  10.80 W

Smoothing the chopped voltage for a 5 ohm electronic load
  1 ohm + 1000 uF (RC)   duty 0.500: Vout = 5.000 V, ripple   59.5 mV, P in  41.97 W, P load  5.00 W, efficiency  11.9%
  100 uH + 100 uF (LC)   duty 0.417: Vout = 4.999 V, ripple   15.1 mV, P in   5.00 W, P load  5.00 W, efficiency 100.0%

Opening a switch while 1.2 A flows in a 100 uH inductor (100 pF of stray capacitance)
  no freewheel path: the switch node swings to  -1190.5 V  (estimate -I sqrt(L/C) = -1200 V)
  with a freewheel diode: the switch node only reaches  -0.86 V
  energy stored in the inductor: 1/2 L I^2 = 72 uJ

Making 5 V at 1 A from different inputs
    Vin linear eff linear heat  90% switcher heat
    7 V     71.4%       2.0 W             0.56 W
   12 V     41.7%       7.0 W             0.56 W
   24 V     20.8%      19.0 W             0.56 W
   48 V     10.4%      43.0 W             0.56 W
```

## Use It

- **Every USB charger** is a switching converter (an isolated "flyback" type with a transformer, Phase 08, Lesson 06), running at tens to hundreds of kilohertz. Modern GaN (gallium nitride) chargers switch at up to a few MHz, which is why they can use smaller transformers and be so small.
- **Point-of-load converters** on a computer motherboard turn 12 V into about 1 V at over 100 A for the processor, using many buck phases in parallel.
- **LED drivers** in bulbs and backlights are switching converters that regulate current instead of voltage.
- **Ready-made modules:** the LM2596 (a 150 kHz buck regulator chip, common on cheap adjustable modules) and the MP1584 or similar are hobby favourites; the TPS62xxx family from TI are tiny high-frequency bucks.
- **Freewheel diodes are everywhere:** across every relay coil and motor (Lesson 05), a diode in reverse catches the inductive kick. Forget it and the transistor driving the coil dies.

## Common Mistakes

- **Thinking a switching converter "wastes the off-time".** Energy is not lost during the off-time; it is stored in the inductor and capacitor and delivered then.
- **Using a resistor to smooth power.** Fine for a signal (Phase 17), disastrous for power: the resistor carries the full current.
- **No freewheel path for an inductor.** The switch sees a voltage spike of hundreds of volts and fails.
- **Assuming switchers are always better.** Their output has ripple and their edges radiate noise. Analog and radio circuits often need an LDO after the switcher, or a linear regulator only.
- **Ignoring the switch's real losses.** On-resistance and switching transitions are why real converters reach 90-97%, not 100%. Lesson 07 turns those watts into temperatures.

## Exercises

1. A switch chops 24 V into a 12 ohm heater at D = 0.25. What average power does the heater get? What would a steady voltage of `D x 24 V = 6 V` give? Why are they different? (12 W versus 3 W: power depends on V^2, and the average of V^2 is not the square of the average of V.)
2. An RC filter of 0.5 ohm feeds a 2 ohm load from a 12 V half-bridge at D = 0.5. Find the output voltage, the loss in the resistor and the efficiency. (Vout = 6 x 2 / 2.5 = 4.8 V; the resistor carries 14.4 A for half the time and 9.6 A for the other half, so it loses 0.5 x 14.4^2 x 0.5 + 0.5 x 9.6^2 x 0.5 = 74.9 W; P_load = 11.5 W; efficiency 13%.)
3. A relay coil of 50 mH carries 80 mA. Its wiring has 50 pF. How big is the kick if the transistor switches off with no diode? (0.08 x sqrt(0.05 / 50e-12) = 2530 V.)
4. In `main.py`, make the LC filter's inductor 22 uH instead of 100 uH. Predict the new ripple current and output ripple, then run it. (delta_I = 2.65 A, delta_V = 66 mV.)
5. Harder: a switcher with 95% efficiency and a linear regulator both make 3.3 V at 2 A. Above which input voltage does the switcher waste less power? (Linear loss = (Vin - 3.3) x 2; switcher loss = 6.6 / 0.95 - 6.6 = 0.35 W; equal at Vin = 3.47 V.)

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| SMPS | "A switching power supply" | A converter that chops with switches and filters with L and C |
| Ideal switch | "On or off" | Zero V when closed, zero I when open: zero power either way |
| Half-bridge | "Two transistors" | A high-side and a low-side switch driven opposite, making a switch node between two rails |
| Freewheel diode | "The protection diode" | A path that lets an inductor's current continue when its switch opens |
| Inductive kick | "A spike" | The voltage L dI/dt produced when inductor current is forced to change quickly |
| Ripple | "Noise on the output" | The periodic variation of the output at the switching frequency |

## Further Reading

- Robert W. Erickson and Dragan Maksimovic, *Fundamentals of Power Electronics*, 3rd ed. (Springer), Chapter 1 — why switching, and the ideal switch argument
- [Texas Instruments, "Power Topologies Handbook"](https://www.ti.com/lit/pdf/slyu036) — a catalogue of switching converter circuits with their waveforms
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 9 (Voltage Regulation and Power Conversion), sections on switching regulators
- [MIT OpenCourseWare 6.334 "Power Electronics"](https://ocw.mit.edu/courses/6-334-power-electronics-spring-2007/) — lecture notes on basic converter operation
