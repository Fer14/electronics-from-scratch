# Charging and Discharging

> The capacitor fills fast while it is empty and slowly as it gets full, because the current that fills it is set by how much voltage is still missing.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Phase 04 (Kirchhoff's Laws), Phase 07 Lessons 01-02 (Storing Charge, Capacitance)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| RC circuit | A resistor and a capacitor connected together, usually in series with a source | A narrow pipe filling a bucket |
| Exponential curve | A curve where each step changes by a fixed **fraction** of what is left | Each day you eat half of the remaining cake |
| Exponential decay | An exponential curve that shrinks toward zero | A hot cup of tea cooling toward room temperature |
| Euler's number e | A constant, about 2.718, that appears whenever change is proportional to what is left | The "natural" base for growth and decay, like pi is for circles |
| exp(x) or e^x | e raised to the power x; on calculators the "e^x" key | |
| Square wave | A voltage that jumps between two values, high and low, at a regular rhythm | Flicking a light switch on and off every few seconds |
| Initial condition | The state the capacitor starts in (its voltage at t = 0) | How full the bucket was when you opened the tap |
| Final value | The voltage the capacitor heads toward if you wait forever | The water level where the bucket stops filling |

## Learning Objectives

- Use Ohm's law and Q = C x V together to explain, step by step, why the charging current shrinks over time.
- Compute the charging curve with small time steps by hand and see it bend into an exponential.
- Use the charging formula v(t) = V x (1 - e^(-t / RC)) and the discharging formula v(t) = V0 x e^(-t / RC).
- Predict the current at any moment, including the direction of current during discharge.
- Simulate a capacitor driven by a square wave and compare the result with the formulas.

## The Problem

You want an LED to fade out slowly when you switch off a toy, rather than snapping off. You want a doorbell button to ignore the few milliseconds of rattling contacts. You want a microcontroller's reset pin to stay low for a while after the batteries go in. All three are the same circuit: a resistor feeding a capacitor. To design them you need to know **how long** the capacitor takes to reach a given voltage, and what the voltage looks like on the way.

In Lesson 01 you saw the charging curve rise quickly and then flatten. In this lesson you will understand exactly why it has that shape, derive the formula for it with nothing more than Ohm's law and Q = C x V, and check it against the simulator, both while charging and while discharging.

## The Physics

Connect a 5 V source through a 1 kOhm resistor to an empty 1 uF capacitor.

```
     in o----[ R 1k ]----o cap
        |                |
     V 5V             C 1uF       capacitor starts at 0 V
        |                |
        +-------o--------+
                0
```

Follow one moment at a time:

1. **The instant you connect.** The capacitor has 0 V across it (its voltage cannot jump, Lesson 02). Kirchhoff's voltage law (Phase 04) says the source's 5 V must be shared between the resistor and the capacitor. The capacitor takes 0 V, so the resistor takes all 5 V. Ohm's law gives the current: I = 5 V / 1000 Ohm = 5 mA.
2. **That current moves charge onto the capacitor.** Charge raises its voltage: in a short time dt the voltage rises by I x dt / C.
3. **Now the capacitor has a little voltage, say 1 V.** The resistor only gets 5 - 1 = 4 V, so the current drops to 4 mA. The capacitor keeps filling, but more slowly.
4. **The closer the capacitor gets to 5 V, the less voltage is left for the resistor**, the smaller the current, and the slower the filling. It never quite gets there in finite time, but it gets as close as you like.

The key sentence is:

> The current at every moment equals the voltage still missing, divided by R.

    i = (V - v) / R

where V is the source voltage and v (small letter) is the capacitor's voltage right now. And the capacitor's voltage rises at the rate i / C (Lesson 02). So the voltage rises at a rate proportional to what is still missing. A quantity whose change is proportional to "what is left" always follows an **exponential** curve.

### Discharging is the mirror image

Now replace the source with a wire (set it to 0 V). The capacitor is at, say, 5 V. The only path is through the resistor, so current flows out of the capacitor's + plate, through R, back to the - plate. The current is v / R, which is largest at the start and shrinks as the capacitor empties. The voltage falls by a fixed fraction in each equal slice of time: exponential decay.

Notice the **direction**: during charging current flows into the top plate; during discharging it flows out. A simulator reports this as positive then negative current through the resistor.

### The water picture

A bucket with a hole near the bottom, connected by a narrow pipe to a big tank whose water level is fixed (the source). The flow through the pipe depends on the difference in water level. When the bucket is empty, the difference is big and water rushes in; as the bucket fills, the difference shrinks and the flow slows. That captures charging well. What it gets wrong: water levels depend on bucket shape and gravity; a capacitor's "level" is exactly proportional to charge, which is what makes the math so clean.

## The Concept

### Step by step by hand

Take R = 1 kOhm, C = 1 uF, V = 5 V. Use time steps of 0.2 ms. At each step:

    current        i = (5 - v) / 1000
    voltage rise   dv = i x 0.0002 / 0.000001 = i x 200

| Step | Time (ms) | v at start (V) | i = (5 - v)/1000 (mA) | dv = i x 200 (V) | v at end (V) |
|---|---|---|---|---|---|
| 1 | 0.0 | 0.000 | 5.000 | 1.000 | 1.000 |
| 2 | 0.2 | 1.000 | 4.000 | 0.800 | 1.800 |
| 3 | 0.4 | 1.800 | 3.200 | 0.640 | 2.440 |
| 4 | 0.6 | 2.440 | 2.560 | 0.512 | 2.952 |
| 5 | 0.8 | 2.952 | 2.048 | 0.410 | 3.362 |

Look at the "missing" voltage 5 - v: 5, 4, 3.2, 2.56, 2.048 ... every step it is multiplied by 0.8. That is the fingerprint of an exponential. These big steps slightly overshoot the truth (the current is actually falling during each step, but we used the value from the start of it), so the hand table runs a little ahead of reality. Make the steps smaller and the table converges on the exact curve. Lesson 08 turns this idea into a real simulator.

### The formulas

Making the steps infinitely small gives exact formulas. The product R x C appears in them so often that it gets its own symbol, the Greek letter tau (written τ, "tau"), called the **time constant**. With R in ohms and C in farads, R x C comes out in **seconds** (Lesson 04 shows why).

Charging from 0 toward V:

> The capacitor voltage equals the source voltage times one minus e to the power of minus time over RC.

    v(t) = V x (1 - e^(-t / RC))

Discharging from V0 toward 0:

> The capacitor voltage equals its starting voltage times e to the power of minus time over RC.

    v(t) = V0 x e^(-t / RC)

The current in both cases:

    charging:    i(t) = (V / R) x e^(-t / RC)        (positive, into the capacitor)
    discharging: i(t) = -(V0 / R) x e^(-t / RC)      (negative, out of the capacitor)

Here e^(-t/RC) is "e to the power minus t divided by RC". At t = 0 it is e^0 = 1, and it shrinks toward 0 as t grows. On a calculator: divide t by RC, change the sign, press e^x.

### Worked example: charging

R = 1 kOhm, C = 1 uF, so RC = 1000 x 0.000001 = 0.001 s = 1 ms. V = 5 V.

At t = 2 ms:

1. t / RC = 2 ms / 1 ms = 2.
2. e^(-2) = 0.1353.
3. 1 - 0.1353 = 0.8647.
4. v = 5 x 0.8647 = 4.32 V.
5. Current: i = (5 / 1000) x 0.1353 = 0.677 mA. Check with "missing voltage over R": (5 - 4.32) / 1000 = 0.68 mA. Same.

### Worked example: discharging

The same capacitor starts at 5 V and discharges through the same 1 kOhm. At t = 0.5 ms:

1. t / RC = 0.5.
2. e^(-0.5) = 0.6065.
3. v = 5 x 0.6065 = 3.03 V.
4. i = -(5 / 1000) x 0.6065 = -3.03 mA (flowing out of the top plate).

### A general recipe

Every RC circuit with a constant source goes from an **initial** value to a **final** value along the same shape:

    v(t) = final + (initial - final) x e^(-t / RC)

Charging is initial = 0, final = V. Discharging is initial = V0, final = 0. A capacitor at 2 V connected to a 5 V source through R: initial = 2, final = 5, so v(t) = 5 - 3 x e^(-t/RC). This one formula covers almost every hand calculation you will do with a single capacitor.

### Driving with a square wave

A square wave that sits at 5 V for 10 ms and 0 V for 10 ms makes the capacitor charge, then discharge, then charge again:

```
 source  5V  ____________              ____________
            |            |            |
         0V |            |____________|

 cap     5V      ___________
               /            \
              /              \
         0V  /                \___________/
```

If each half-period is much longer than RC, the capacitor fully charges and discharges and you see clean exponential "shark fins". If the half-period is shorter than RC, the capacitor never gets near 0 or 5 V; it wobbles around the middle. That second behaviour is the beginning of filtering (Phase 10).

### Reading the curve: the tangent trick

Draw the charging curve and, at t = 0, draw its tangent (the straight line that just touches it at the start). Its slope is the starting current divided by C: (V / R) / C = V / RC. So the tangent reaches the final value V after exactly RC seconds. The same is true at **every** point: wherever you are on the curve, if the capacitor kept its current speed, it would reach the final value one RC later. This is a handy way to estimate RC from a sketch or an oscilloscope screen, and Lesson 04 builds on it.

### Worked example: a capacitor that is not empty

A 10 uF capacitor sits at 2 V. At t = 0 it is connected through 4.7 kOhm to a 9 V supply.

1. RC = 4700 x 10 x 10^-6 = 0.047 s = 47 ms.
2. Initial current: the resistor sees 9 - 2 = 7 V, so i = 7 / 4700 = 1.49 mA.
3. Using the general recipe with initial = 2 V and final = 9 V, at t = 47 ms: v = 9 + (2 - 9) x e^(-1) = 9 - 7 x 0.368 = 6.42 V.
4. At t = 100 ms: e^(-100/47) = e^(-2.128) = 0.119, so v = 9 - 7 x 0.119 = 8.17 V.

Notice that the capacitor still covers 63% of the **remaining** distance in one RC: from 2 V the remaining distance is 7 V, and 63% of 7 V is 4.42 V, landing at 6.42 V.

## Build It

```bash
uv run python phases/07-capacitors/03-charging-and-discharging/code/main.py
```

### Step 1: Small steps by hand, in code

The function repeats the table above: current from the missing voltage, voltage rise from the current.

```python
def small_steps_by_hand(step, steps):
    volts = 0.0
    rows = []
    for index in range(steps + 1):
        current = (SUPPLY_VOLTS - volts) / RESISTOR_OHMS
        rows.append((index * step, current, volts))
        volts += current * step / CAPACITOR_FARADS
    return rows
```

```
Charging step by step: every 0.2 ms the current refills the capacitor a little
 time (ms)  current (mA)  cap volts (V)  formula (V)
       0.0         5.000          0.000        0.000
       0.2         4.000          1.000        0.906
       0.4         3.200          1.800        1.648
       0.6         2.560          2.440        2.256
       0.8         2.048          2.952        2.753
       1.0         1.638          3.362        3.161
       1.2         1.311          3.689        3.494
       1.4         1.049          3.951        3.767
       1.6         0.839          4.161        3.991
       1.8         0.671          4.329        4.174
       2.0         0.537          4.463        4.323
```

The step-by-step values have the right shape but run ahead of the exact formula, as predicted. 0.2 ms is one fifth of RC: too coarse for accuracy, perfect for understanding.

### Step 2: Simulate charging and discharging

A `pulse_source` makes the square wave: 5 V for the first half of each period, 0 V for the second half. The period is 20 x RC = 20 ms, and the simulator steps every RC / 1000 = 1 us.

```python
def simulate_square_wave():
    circuit = Circuit()
    circuit.pulse_source("V1", "in", "0", low=0.0, high=SUPPLY_VOLTS, period=PERIOD, duty=0.5)
    circuit.resistor("R1", "in", "cap", RESISTOR_OHMS)
    circuit.capacitor("C1", "cap", "0", CAPACITOR_FARADS, v0=0.0)
    result = circuit.transient(t_stop=PERIOD, dt=TAU / 1000)
    return np.asarray(result.time), np.asarray(result.v("in")), np.asarray(result.v("cap")), np.asarray(result.i("R1"))
```

### Step 3: Compare with the formulas

```python
def charging_formula(time):
    return SUPPLY_VOLTS * (1 - np.exp(-time / TAU))


def discharging_formula(time, start_volts):
    return start_volts * np.exp(-time / TAU)
```

```
Simulated: 5 V for 10 ms (charging), then 0 V for 10 ms (discharging), R = 1 kOhm, C = 1 uF
       phase  t (ms)  sim (V)  formula (V)  current (mA)
    charging     0.5    1.967        1.967         3.033
    charging     1.0    3.161        3.161         1.839
    charging     2.0    4.323        4.323         0.677
    charging     3.0    4.751        4.751         0.249
    charging     5.0    4.966        4.966         0.034
 discharging    10.5    3.034        3.033        -3.034
 discharging    11.0    1.840        1.839        -1.840
 discharging    12.0    0.677        0.677        -0.677
 discharging    13.0    0.249        0.249        -0.249
 discharging    15.0    0.034        0.034        -0.034
```

Three things to notice:

- Simulator and formula agree to about a millivolt. The tiny difference after the fall comes from the source's jump landing between two of the simulator's 1 us time steps.
- The current during discharge is negative: it flows back out of the capacitor through the resistor.
- The charging and discharging tables are mirror images. After 0.5 ms of charging the capacitor has gained 1.967 V; after 0.5 ms of discharging it has 3.033 V left, and 1.967 + 3.033 = 5.

### Step 4: Plot

The script saves `charge_discharge.png` next to itself: the square wave and the capacitor's shark fin on top, the current spikes below (positive spike when the source jumps up, negative when it jumps down).

## Use It

- **Switch debouncing.** A mechanical button bounces for 1-10 ms. A 10 kOhm resistor and 1 uF capacitor (RC = 10 ms) smooth those bounces into a single slow edge that a logic input reads cleanly (usually with a Schmitt-trigger input, Phase 13).
- **Power-on reset.** Many microcontrollers have a reset pin with an internal pull-up resistor of tens of kilohms. A small external capacitor to ground holds the pin low for a few milliseconds after power-up while the supply settles.
- **Slow LED fade.** An LED driven from a capacitor through a resistor dims gradually as the capacitor discharges; some night lights and toys use this.
- **555 timer.** The classic NE555 chip measures how long an RC takes to charge from 1/3 to 2/3 of the supply. Its datasheet formula t = 0.693 x R x C comes straight from the exponential (you will derive 0.693 in Lesson 04).
- **Sample-and-hold.** In analog-to-digital converters (Phase 17), a switch charges a small capacitor to the input voltage through the switch's resistance; the converter must wait several RC before the capacitor is accurate enough.

## Common Mistakes

- **Expecting a straight line.** The capacitor does not charge at a constant rate unless the current is constant (as with a current source, Lesson 02). Through a resistor the rate falls as it fills.
- **Thinking the capacitor reaches the source voltage.** Mathematically it never quite does. In practice after five RC it is within 1%, which we usually call "fully charged".
- **Forgetting the sign of the discharge current.** It flows the other way. If your calculation shows positive current during discharge, check your reference direction.
- **Using the source voltage in the discharge formula when the capacitor was not fully charged.** V0 is wherever the capacitor actually was when discharging started.
- **Mixing milliseconds and seconds in e^(-t/RC).** t and RC must be in the same units. With R in kOhm and C in uF, RC comes out in milliseconds, which is convenient but only if t is also in ms.
- **Big time steps.** As the hand table showed, a step of RC/5 gives visibly wrong answers. Simulators need steps much smaller than RC (we used RC/1000).

## Exercises

1. R = 2.2 kOhm, C = 10 uF, V = 9 V, starting empty. What are RC, the initial current, and the voltage after 22 ms?
2. A 100 uF capacitor at 12 V discharges through 470 Ohm. What is its voltage and current after 47 ms?
3. Use the general recipe: a 1 uF capacitor at 1 V is connected through 1 kOhm to a 3.3 V source. What is its voltage 1 ms later?
4. Redo the hand table with steps of 0.1 ms for the first 1 ms. How close to the formula's 3.161 V do you get at 1 ms? What do you expect with 0.05 ms steps?
5. In the code, change `PERIOD` to 2 x TAU (so each half-period is one RC). Before running, sketch what the capacitor voltage will look like after a few periods. Run it (extend `t_stop` to several periods) and compare. Between which two voltages does it settle?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Charging curve | "It fills up" | v(t) = V(1 - e^(-t/RC)): fast at first, slower as the missing voltage shrinks |
| Discharging curve | "It drains" | v(t) = V0 e^(-t/RC): loses the same fraction of what remains in each equal slice of time |
| Exponential | "Grows really fast" | A curve where change is proportional to the current amount (here, to the missing voltage) |
| Initial condition | "Where it starts" | The capacitor voltage at t = 0, which cannot jump |
| Final value | "Where it ends up" | The voltage approached as t goes to infinity; the capacitor then carries no current |
| Square wave | "On-off signal" | A source alternating between two levels; it makes the capacitor charge and discharge in turn |

## Further Reading

- [All About Circuits, Vol. I, Chapter 16: RC and L/R Time Constants](https://www.allaboutcircuits.com/textbook/direct-current/chpt-16/electrical-transients/) - step-by-step transient analysis with tables.
- [MIT OpenCourseWare 6.002 Circuits and Electronics (Agarwal), lectures on first-order transients](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) - the same derivation done with differential equations.
- [Khan Academy, Electrical engineering: RC natural response](https://www.khanacademy.org/science/electrical-engineering/ee-circuit-analysis-topic/ee-natural-and-forced-response) - a friendly derivation of the exponential.
- [Texas Instruments NE555 datasheet](https://www.ti.com/product/NE555) - see how its timing formulas come from RC charging.
