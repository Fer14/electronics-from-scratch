# The Buck Converter

> An inductor's average voltage must be zero in steady state. Apply that one fact to a switch, an inductor and a capacitor and out falls Vout = D x Vin: a step-down converter that wastes almost nothing.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 18 (Power Electronics), Lesson 02 (Switching Converters); Phase 08 (Magnetism and Inductors), Lesson 04 (The Inductor); Phase 10 (Filters and Resonance), Lesson 05 (RLC Resonance); Phase 17 (Microcontrollers), Lesson 03 (PWM)
**Time:** ~95 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Buck converter | A switching converter whose output is lower than its input ("bucks" the voltage down). Also called a step-down converter. | A gearbox in a low gear: less speed, more force, same power. |
| High-side switch | The switch between the input and the switch node. | The tap from the mains. |
| Low-side switch | The switch between the switch node and ground; it provides the freewheel path. In older designs it is a diode. | The overflow return path. |
| Synchronous rectification | Using a switch (MOSFET) instead of a diode for the freewheel path, to avoid the diode's voltage drop. | Replacing a one-way flap with a door that opens exactly when needed. |
| Steady state | The repeating pattern the converter settles into, where every period looks the same. | A cyclist pedalling at a constant speed on flat road. |
| Volt-second balance | In steady state, the inductor's voltage times time must add up to zero over each period. | Going up and down the same staircase: the steps up must equal the steps down. |
| Ripple current (delta I) | How much the inductor current rises and falls in each period, peak to peak. | The small speed-up and slow-down with each pedal stroke. |
| Output ripple (delta V) | The small wobble of the output voltage at the switching frequency. | The bobbing of the cyclist's head. |
| CCM (continuous conduction mode) | The inductor current never drops to zero during a period. | The bike never comes to a stop between strokes. |
| DCM (discontinuous conduction mode) | The inductor current reaches zero and stays there for part of the period (with a diode). | Coasting to a stop, then pushing off again. |
| Overshoot | When the output shoots past its target during start-up or a change. | Braking too late and stopping past the line. |
| Inrush current | The large current drawn at start-up to charge the output capacitor. | The surge of water when you first open a valve into an empty tank. |
| Soft start | Raising the duty cycle slowly at start-up to avoid overshoot and inrush. | Easing the clutch out instead of dropping it. |
| Feedback loop | Measuring Vout and adjusting D to keep it right as the input and load change. | Watching the speedometer and adjusting the pedal. |

## Learning Objectives

- Derive Vout = D x Vin from volt-second balance on the inductor
- Compute the inductor ripple current `delta_I = (Vin - Vout) x D / (f x L)` and the output ripple `delta_V = delta_I / (8 f C)`, and use them to choose L and C
- Simulate a synchronous buck with ideal switches and check every formula against the waveforms
- Account for conduction losses (switch on-resistance and inductor resistance) and estimate the efficiency
- Explain start-up overshoot and inrush from the LC resonance, and why real converters use soft start and feedback

## The Problem

Your board has a 12 V battery and a microcontroller, sensors and radio that want 5 V at about 1 A. A linear regulator would turn 7 W into heat (Lesson 01). In Lesson 02 you saw that a switch plus an LC filter could do the job almost losslessly. Now you need to *design* one: what duty cycle, which inductor, which capacitor, how big will the ripple be, what happens at switch-on, how efficient will it really be?

The buck converter is the most used power circuit in electronics. Every phone, laptop, router and microcontroller board has several. Learning to design one from first principles is the gateway to every other converter.

## The Physics

### The inductor's rule

An inductor obeys (Phase 08, Lesson 04):

```
V_L = L x dI/dt
```

Read it as: "the voltage across an inductor equals its inductance times how fast its current is changing". A constant voltage across an inductor makes its current change at a constant rate: a straight ramp. Rearranged:

```
change in current = V_L x time / L
```

In steady state, the inductor current at the end of each period must be the same as at the start (otherwise it would keep growing or shrinking, which is not steady). So the ramp up must exactly cancel the ramp down:

```
V_L(on) x t_on + V_L(off) x t_off = 0
```

This is **volt-second balance**: the inductor's average voltage over a period is zero. A capacitor has the dual rule, **charge balance**: in steady state its average current is zero.

## The Concept

### The circuit

```
                 S_high
   Vin ----+-----o/ o-----+-----[ L ]-----+---------+----- Vout
           |              |      I_L ->   |         |
          ===             | sw            === C    [ R_load ]
           |              |               |         |
           |       S_low  /               |         |
           |              |               |         |
   gnd ----+--------------+---------------+---------+
```

The two switches are driven opposite (a half-bridge, Lesson 02).

### Two states, two ramps

**On (S_high closed, for `t_on = D x T`):** the switch node is at Vin. The inductor sees `Vin - Vout` (positive), so its current ramps **up** at `(Vin - Vout) / L`.

**Off (S_low closed, for `t_off = (1 - D) x T`):** the switch node is at 0. The inductor sees `0 - Vout` (negative), so its current ramps **down** at `Vout / L`.

```
I_L
  ^        /\        /\        /\
  |       /  \      /  \      /  \       <- ramps up for D T, down for (1 - D) T
  |      /    \    /    \    /    \         average = load current
  |     /      \  /      \  /      \
  +---------------------------------------> t
       |<-DT->|<-(1-D)T->|
```

### Volt-second balance gives Vout

```
(Vin - Vout) x D x T + (0 - Vout) x (1 - D) x T = 0
```

Divide by T and expand:

```
Vin x D - Vout x D - Vout + Vout x D = 0
Vin x D - Vout = 0
Vout = D x Vin
```

The output is the duty cycle times the input. For 12 V to 5 V: `D = 5 / 12 = 0.4167`. Note what the formula does *not* contain: the load, L or C. In continuous conduction, Vout depends only on D and Vin.

And energy conservation tells us the current: with no losses, `Vin x I_in = Vout x I_out`, so `I_in = D x I_out`. The buck turns a high voltage at low current into a low voltage at high current, like a gearbox. At 1 A out, the battery supplies only `0.4167 A` on average.

### Choosing L from the ripple current

During the on-time the current rises by:

```
delta_I = (Vin - Vout) x D x T / L = (Vin - Vout) x D / (f x L)
```

A common design rule is to allow about 20-40% of the load current as ripple. For 30% of 1 A (0.3 A) at 100 kHz:

```
L = (Vin - Vout) x D / (f x delta_I) = 7 x 0.4167 / (100 000 x 0.3) = 2.917 / 30 000 = 97.2 uH
```

Choose the standard 100 uH. Then:

```
delta_I = 7 x 0.4167 / (100 000 x 100e-6) = 2.917 / 10 = 0.292 A
peak inductor current = I_out + delta_I / 2 = 1 + 0.146 = 1.146 A
```

The inductor must be rated for that peak (its "saturation current", above which its core stops working well) and for the RMS current (heating).

Bigger L means smaller ripple but a physically bigger, slower-responding inductor. Higher frequency means smaller L for the same ripple, which is why modern converters run at MHz.

### Choosing C from the output ripple

The capacitor absorbs the inductor's ripple: the triangle of current above and below the average. The charge in one half of the triangle is a small triangle of area `1/2 x (T/2) x (delta_I / 2) = delta_I x T / 8`. That charge changes the capacitor's voltage by:

```
delta_V = charge / C = delta_I x T / (8 C) = delta_I / (8 x f x C)
```

For at most 10 mV:

```
C >= delta_I / (8 x f x delta_V) = 0.292 / (8 x 100 000 x 0.01) = 0.292 / 8000 = 36.5 uF
```

Choose 47 uF. Then `delta_V = 0.292 / (8 x 100 000 x 47e-6) = 0.292 / 37.6 = 7.8 mV`.

(Real capacitors also have a small series resistance, the ESR, which adds `delta_I x ESR` of ripple. With electrolytic capacitors it often dominates; ceramic capacitors have tiny ESR. Phase 07, Lesson 07 covers real capacitors.)

### Losses in a real buck

Ideal switches and inductor: 100% efficient. Real parts have resistance. The load current flows through either the high-side or the low-side switch at every moment, and always through the inductor's winding resistance (DCR):

```
P_conduction = I_out^2 x (R_on + R_DCR)       (ignoring the small ripple)
```

With 50 milliohm switches and a 0.1 ohm inductor at 1 A: `1 x (0.05 + 0.1) = 0.15 W`, so efficiency is about `5 / 5.15 = 97%`. Real converters also have switching losses and the controller's own consumption, so 90-95% is typical.

The resistances also lower Vout slightly (4.86 V instead of 5 V in the simulation). A real converter does not care: its **feedback loop** measures Vout and nudges D until it is exactly right, exactly like the linear regulator's loop in Lesson 01.

### Start-up: the LC resonance

The inductor and capacitor form a resonant circuit (Phase 10, Lesson 05) with natural frequency:

```
f0 = 1 / (2 pi sqrt(L C)) = 1 / (2 pi sqrt(100e-6 x 47e-6)) = 1 / (2 pi x 6.86e-5) = 2322 Hz
```

Switch on suddenly at full duty, with the capacitor empty, and the output rings: the inductor current builds up, overshoots the load's need, charges the capacitor past 5 V, then swings back. In the simulation the output reaches 8.15 V (63% overshoot) and the inductor current 3.8 A, more than three times the load current. Real converters prevent this with **soft start** (raising D slowly over a few milliseconds) and with feedback that damps the resonance.

### Light load and DCM

With two switches, the inductor current can go negative: at a 0.1 A load, the 0.29 A ripple swings it from about -0.05 A to +0.24 A. Energy flows back from the output capacitor towards the input for part of each cycle. That is harmless but wasteful. With a diode instead of the low-side switch, the current cannot reverse: it reaches zero and stops, and the converter enters **discontinuous conduction mode**, where `Vout = D x Vin` no longer holds exactly. Many controller chips deliberately switch to a "pulse skipping" mode at light load to save power.

### Worked example: a 5 V to 3.3 V buck for a microcontroller board

Design the converter that powers a board's 3.3 V rail at up to 2 A from a 5 V USB input, switching at 1 MHz.

**Duty cycle.** `D = 3.3 / 5 = 0.66`.

**Inductor**, for about 30% ripple (0.6 A):

```
L = (5 - 3.3) x 0.66 / (1 000 000 x 0.6) = 1.122 / 600 000 = 1.87 uH     -> use 2.2 uH
delta_I = 1.7 x 0.66 / (1e6 x 2.2e-6) = 1.122 / 2.2 = 0.51 A
peak = 2 + 0.255 = 2.26 A        -> inductor rated for at least 3 A saturation
```

**Output capacitor**, for 10 mV:

```
C >= 0.51 / (8 x 1e6 x 0.01) = 6.4 uF     -> use a 10 uF ceramic (delta_V = 6.4 mV)
```

**Input current.** Average `D x I_out = 0.66 x 2 = 1.32 A` from USB, but drawn in pulses of 2 A during the on-time. A 10 uF ceramic capacitor right at the input switch supplies those pulses, so the USB cable sees a smooth current.

**Losses**, with 30 mohm switches and a 20 mohm inductor:

```
conduction = 2^2 x (0.03 + 0.02) = 0.2 W
efficiency ~ 6.6 W / (6.6 + 0.2 + switching and controller) ~ 95%
```

A linear regulator would have dissipated `(5 - 3.3) x 2 = 3.4 W` for the same job, at 66% efficiency.

### Worked example: what if the input sags?

If the USB voltage sags to 4.5 V under load, the feedback loop raises D to `3.3 / 4.5 = 0.733`. The ripple becomes `(4.5 - 3.3) x 0.733 / (1e6 x 2.2e-6) = 0.40 A`: a bit smaller. A buck can regulate down to an input just above its output (limited by its maximum duty cycle and the resistances); below that it drops out, like an LDO.

## Build It

### Step 1: Switch timing and the circuit

The switches toggle on the simulator's time grid (see Lesson 02). The buck circuit:

```python
    circuit.voltage_source("VIN", "vin", "0", VIN)
    circuit.switch("SHIGH", "vin", "sw", closed=True, ron=switch_ohms, toggle_at=toggles)
    circuit.switch("SLOW", "sw", "0", closed=False, ron=switch_ohms, toggle_at=toggles)
    circuit.inductor("L1", inductor_end, "out", INDUCTANCE, i0=...)
    circuit.capacitor("C1", "out", "0", CAPACITANCE, v0=...)
    circuit.resistor("RL", "out", "0", load_ohms)
```

For steady-state measurements we start the capacitor at `D x Vin` and the inductor at the bottom of its ripple, so the simulator does not spend milliseconds settling. For the start-up experiment both start at zero.

### Step 2: Check the formulas

For D = 0.25, 0.4167 and 0.6, the script measures the average output, the inductor's peak-to-peak current over one period, and the output's peak-to-peak ripple over one period, and prints them next to `D x Vin`, `delta_I` and `delta_I / (8 f C)`.

### Step 3: Power and losses

It averages the source power and the load power over 20 periods for ideal parts, then again with 50 milliohm switches and a 0.1 ohm resistor in series with the inductor.

### Step 4: Variations

It replaces the two switches with a pulse source at the switch node (the model the lab uses: with ideal switches in continuous conduction the switch node *is* a square wave), runs a light load, and finally starts from zero to see the overshoot. A plot of the start-up is saved as `buck_startup.png`.

Run it:

```
uv run python phases/18-power-electronics/03-the-buck-converter/code/main.py
```

The simulated Vout matches `D x Vin` to a few millivolts, the ripple current matches within about 2%, the output ripple matches `delta_I / (8 f C)` almost exactly, the ideal efficiency is 100% and the lossy one about 97%.

## Use It

- **Controller chips:** the LM2596 (150 kHz, internal switch, external diode), MP2307 and similar synchronous bucks, and TI's TPS54xxx and TPS62xxx families. Their datasheets have a "Detailed Design Procedure" section that walks through exactly the L and C calculations of this lesson.
- **Datasheet language:** "output voltage set by a resistor divider" (the feedback loop, like Lesson 01), "switching frequency", "inductor saturation current", "output ripple", "soft-start time", "PFM / pulse skipping at light load".
- **Multiphase bucks** run several bucks in parallel, shifted in time, to supply a CPU's 100+ A at about 1 V with small ripple.
- **Battery-powered devices** use bucks to make 3.3 V or 1.8 V from a lithium cell (3.0-4.2 V) with over 90% efficiency.
- **Layout matters:** the loop from input capacitor through the high-side and low-side switches carries sharp current pulses; keeping it tiny on the board (Phase 21) is essential to avoid noise.

## Try It in the Lab

The lab is the buck of this lesson with ideal switches, drawn with its switch node as a pulse source between 0 V and 12 V at 100 kHz. L, C and the 5 ohm load are fixed. Choose the pulse source with the duty cycle that gives 5 V (between 4.8 and 5.2 V) after 4 ms. Think about volt-second balance, and note that the start-up overshoot has died away well before 4 ms.

## Common Mistakes

- **Using the wrong current rating for the inductor.** It must handle the peak current (`I_out + delta_I / 2`) without saturating, plus the start-up peak if there is no soft start.
- **Ignoring ESR.** The capacitor's series resistance can create more ripple than its capacitance does.
- **Expecting D = Vout / Vin exactly in a real circuit.** Losses push D a little higher; the feedback loop handles it.
- **Forgetting the input capacitor.** The input current is pulsed (on during D x T, zero otherwise). Without a capacitor right at the switches, these pulses travel back up the battery wires and make noise.
- **Overlap in a synchronous buck.** If both switches are on at the same instant, the input is shorted ("shoot-through"). Real controllers add a short "dead time" when both are off; during it the inductor current flows through the low-side MOSFET's body diode.
- **Assuming DCM behaves like CCM.** At light load with a diode, Vout depends on the load and on L.

## Exercises

1. A buck converts 24 V to 3.3 V. What is D? With 1 A out and no losses, what is the average input current? (0.1375; 0.1375 A.)
2. For that converter at 500 kHz, choose L for a ripple of 0.3 A. (L = (24 - 3.3) x 0.1375 / (500 000 x 0.3) = 19 uH, use 22 uH.)
3. With that L, how much C keeps the ripple under 5 mV? (delta_I = 0.259 A; C >= 0.259 / (8 x 500 000 x 0.005) = 12.9 uF, use 22 uF.)
4. In `main.py`, double the frequency to 200 kHz without changing L or C. Predict the new delta_I and delta_V, then run it. (Half the ripple current, a quarter of the output ripple.)
5. Harder: implement a crude soft start. Instead of a fixed D from the start, make the switch's toggle list raise D linearly from 0 to 0.4167 over 1 ms (recompute each period's on-time). How much does the overshoot drop?

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Buck | "Step-down regulator" | Half-bridge plus LC filter: Vout = D x Vin in CCM |
| Volt-second balance | "The inductor equation" | Average inductor voltage is zero in steady state |
| Ripple current | "Inductor ripple" | Peak-to-peak inductor current, (Vin - Vout) D / (f L) |
| Output ripple | "Noise" | delta_I / (8 f C), plus delta_I x ESR in real capacitors |
| CCM / DCM | "Modes" | Inductor current never zero / zero for part of each period |
| Synchronous | "No diode" | The freewheel path is a MOSFET switched in step with the main switch |
| Soft start | "Slow start" | Ramping the duty or reference at power-up to avoid overshoot and inrush |

## Further Reading

- [Texas Instruments, SLVA477 "Basic Calculation of a Buck Converter's Power Stage"](https://www.ti.com/lit/an/slva477b/slva477b.pdf) — the standard design equations with a worked example
- Robert W. Erickson and Dragan Maksimovic, *Fundamentals of Power Electronics*, 3rd ed. (Springer), Chapter 2 — volt-second and charge balance, and the small-ripple approximation
- [Texas Instruments, SNVA559 "Switching Regulator Fundamentals"](https://www.ti.com/lit/pdf/snva559) — buck, boost and buck-boost operation from first principles
- [TI, LM2596 datasheet](https://www.ti.com/lit/ds/symlink/lm2596.pdf) — a classic buck regulator chip with a design procedure and inductor-selection guide
