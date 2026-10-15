# The Time Constant

> Multiply R by C and you get a time. After one of those times the capacitor has covered 63% of the way; after five, it is done.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 07 Lesson 03 (Charging and Discharging)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Time constant (tau, τ) | The product R x C, measured in seconds; the natural "clock" of an RC circuit | The time a bucket takes to get about two-thirds full |
| Threshold | A voltage level that something reacts to when it is crossed | The line on a measuring jug you fill up to |
| Natural logarithm (ln) | The inverse of e^x: ln(e^x) = x. It answers "e to what power gives this number?" | Undoing an exponential, like square root undoes squaring |
| Rise time | How long a signal takes to go from 10% to 90% of its final value | How long a sprinter takes from "moving" to "near top speed" |
| Settling | Getting close enough to the final value that you stop caring | Waiting for ripples in a pond to die down |
| Power-on reset | A circuit that holds a chip in reset for a short time after power appears | Counting to three before starting a race |
| Schmitt trigger | A logic input that switches at a clean threshold even when the input rises slowly | A doorbell that only rings once however shakily you press it |

## Learning Objectives

- Show that R x C has units of seconds, and explain what tau means physically.
- Recall the "tau table": 63%, 86%, 95%, 98%, 99.3% after 1 to 5 tau.
- Solve the charging formula backwards to find the time to reach any threshold: t = tau x ln(V / (V - Vth)).
- Use the shortcuts 0.69 tau (half-way) and 2.2 tau (10%-90% rise time).
- Design an RC delay for a given time, pick a standard value, and verify it in the simulator.

## The Problem

A microcontroller datasheet says: "hold the reset pin below 2.5 V for at least 5 ms after power-up". You have a 5 V supply, a 100 nF capacitor and a drawer of resistors. Which resistor do you pick?

The formulas from Lesson 03 tell you the voltage at a given time. Here the question is the opposite: the voltage is given (2.5 V) and you need the time. And you want to answer it in your head when possible. The time constant is the tool that makes both easy.

## The Physics

### Why R x C is a time

Look at the units. Resistance is volts per ampere (Ohm's law, R = V / I). Capacitance is coulombs per volt (C = Q / V). Multiply:

    R x C  ->  (volts / amperes) x (coulombs / volts) = coulombs / amperes

An ampere is a coulomb per second, so coulombs divided by amperes is **seconds**. R x C is a time.

### What tau means physically

At the start of charging, the current is V / R (Lesson 03). If that starting current **stayed** constant, how long would it take to fill the capacitor to V? The capacitor needs Q = C x V; the current delivers V / R each second; so the time is

    (C x V) / (V / R) = R x C = tau

So tau is the time the capacitor would take to charge **if it kept its starting speed**. It does not keep it: the current falls, so in one tau it only gets 63% of the way.

```
  V |                  .......................  final value
    |              . '   /
    |           .'      /   <- tangent at t = 0 reaches V at t = tau
    |         .'      /
    |       .'      /
    |     .'      /
    |    /      /
    |   /     /
    |  /   /
    | /  /
    |/ /
    +-----------+---------------------------------> t
    0          tau
```

### Big R or big C: both slow it down

- A bigger R lets less current flow, so charging takes longer.
- A bigger C needs more charge for each volt, so charging takes longer.

They multiply: doubling either doubles tau. A 10 kOhm and 100 nF circuit has exactly the same timing as a 1 kOhm and 1 uF circuit (both tau = 1 ms). That freedom is useful: you can choose small capacitors (cheap, small) and large resistors, as long as the resistor is not so large that leakage currents matter (Lesson 07).

## The Concept

### The tau table

Put t = tau, 2 tau, ... into v = V x (1 - e^(-t/tau)):

| Time | e^(-t/tau) | Charged (fraction of V) | Still missing |
|---|---|---|---|
| 1 tau | 0.368 | 63.2% | 36.8% |
| 2 tau | 0.135 | 86.5% | 13.5% |
| 3 tau | 0.050 | 95.0% | 5.0% |
| 4 tau | 0.018 | 98.2% | 1.8% |
| 5 tau | 0.0067 | 99.3% | 0.7% |

For discharging, read the "still missing" column as "still left". Memorize the first and last rows: **63% after one tau, done after five**.

A pattern worth seeing: each tau, the missing part is multiplied by 0.368 (about a third). After 2 tau a third of a third, and so on.

### Solving for time

We want the time t at which the charging voltage reaches a threshold Vth. Start from

    Vth = V x (1 - e^(-t/tau))

Step by step:

1. Divide by V: Vth / V = 1 - e^(-t/tau).
2. Rearrange: e^(-t/tau) = 1 - Vth / V = (V - Vth) / V.
3. Take the natural log of both sides (ln undoes e^): -t / tau = ln((V - Vth) / V).
4. Flip the fraction to remove the minus sign: t / tau = ln(V / (V - Vth)).

> The time to reach a threshold is tau times the natural log of the supply voltage divided by the voltage still missing at the threshold.

    t = tau x ln(V / (V - Vth))

For discharging from V0 down to a threshold Vth:

    t = tau x ln(V0 / Vth)

### Handy shortcuts

| Question | Answer | Where it comes from |
|---|---|---|
| Time to reach 50% | 0.693 tau | ln(2) = 0.693 |
| Time to reach 63.2% | 1 tau | definition |
| 10% to 90% rise time | 2.197 tau (about 2.2 tau) | ln(9) = 2.197 |
| Time to reach 99% | 4.6 tau | ln(100) = 4.605 |
| Time to settle within 0.1% (for a 10-bit converter) | 6.9 tau | ln(1000) |

Why 2.2 tau for 10-90%: reaching 10% takes tau x ln(1/0.9) = 0.105 tau; reaching 90% takes tau x ln(1/0.1) = 2.303 tau; the difference is 2.197 tau.

### Worked example: the reset delay

Requirement: 5 V supply, reset pin crosses 2.5 V no sooner than 5 ms, capacitor 100 nF.

1. 2.5 V is half of 5 V, so the crossing is at 0.693 tau.
2. We need 0.693 tau = 5 ms, so tau = 5 / 0.693 = 7.21 ms.
3. R = tau / C = 0.00721 / 0.0000001 = 72,100 Ohm = 72.1 kOhm.
4. Standard resistor values near it (E12 series): 68 kOhm and 82 kOhm. 68 kOhm would give 0.693 x 6.8 ms = 4.71 ms, too short. 82 kOhm gives 0.693 x 8.2 ms = 5.68 ms, which meets "at least 5 ms".

A careful designer would also add the tolerances (Lesson 07): a 20% capacitor can make it 20% shorter. The simulator in the code checks the 68 kOhm case and confirms 4.71 ms.

### Worked example: a 3.16 V threshold

Why 3.16 V? It is 63.2% of 5 V, so it should take exactly one tau. Check: ln(5 / (5 - 3.16)) = ln(5 / 1.84) = ln(2.717) = 1.000. Yes.

### Worked example: discharging to a threshold

A 470 uF capacitor at 12 V discharges through 1 kOhm (tau = 0.47 s). When does it reach the "safe to touch" level of 2 V?

    t = 0.47 x ln(12 / 2) = 0.47 x 1.792 = 0.842 s

### Estimating tau from a measurement

If you see a charging curve on an oscilloscope (Phase 06), find where it reaches 63% of its final value: that time is tau. Or find the 50% point and divide by 0.693. Divide tau by R to find an unknown C.

### Why five tau counts as "done"

There is nothing magic about 5. It is a convention that fits most practical needs: after 5 tau the capacitor is within 0.7% of its final value, which is smaller than the tolerance of most resistors and capacitors. When more precision matters, the required number of tau grows only slowly, because it is a logarithm:

| Precision needed | Number of tau | Example |
|---|---|---|
| 1% | 4.6 | "Good enough" for most timing |
| 0.1% | 6.9 | A 10-bit ADC (1 part in 1024) |
| 0.01% | 9.2 | A 13-bit measurement |
| 1 ppm (0.0001%) | 13.8 | Precision instruments |

Each extra factor of 10 in precision costs only 2.3 more tau, because ln(10) = 2.303.

### Worked example: finding tau from a measurement

You charge an unknown capacitor through a 22 kOhm resistor from 5 V and measure (with an oscilloscope, Phase 06):

| Time | Voltage |
|---|---|
| 0 ms | 0.00 V |
| 5 ms | 2.21 V |
| 10 ms | 3.44 V |

1. From the 5 ms point: t / tau = ln(5 / (5 - 2.21)) = ln(1.792) = 0.583, so tau = 5 / 0.583 = 8.57 ms.
2. From the 10 ms point: ln(5 / 1.56) = ln(3.205) = 1.165, so tau = 10 / 1.165 = 8.58 ms. Two measurements agree, a good sign that it really is a simple RC.
3. C = tau / R = 8.58 x 10^-3 / 22,000 = 0.39 uF, probably a "390 nF" part.

## Build It

```bash
uv run python phases/07-capacitors/04-the-time-constant/code/main.py
```

### Step 1: The tau table

```python
def show_tau_table():
    for multiple in range(1, 6):
        charged = 1 - math.exp(-multiple)
        print(f"{multiple:>4} t {charged * 100:>12.1f} {(1 - charged) * 100:>18.1f}")
```

```
How far a charging capacitor gets after whole numbers of tau
  time  charged (%)  still missing (%)
   1 t         63.2               36.8
   2 t         86.5               13.5
   3 t         95.0                5.0
   4 t         98.2                1.8
   5 t         99.3                0.7
```

### Step 2: Time to reach a threshold

```python
def time_to_reach(threshold, supply, tau):
    return tau * math.log(supply / (supply - threshold))
```

`math.log` is the natural logarithm, ln.

### Step 3: Measure crossings in the simulator

We simulate a 5 V step into an RC and find the first sample above the threshold, then interpolate linearly between that sample and the one before it to get a precise time.

```python
def first_crossing(time, volts, threshold):
    index = int(np.argmax(volts >= threshold))
    if volts[index] < threshold:
        return float("nan")
    if index == 0:
        return float(time[0])
    t0, t1, v0, v1 = time[index - 1], time[index], volts[index - 1], volts[index]
    return float(t0 + (threshold - v0) * (t1 - t0) / (v1 - v0))
```

Three very different R and C pairs:

```
Simulated time to cross thresholds vs the formula t = tau * ln(V / (V - Vth))
       R        C  tau (ms)  Vth (V)  sim (ms)  formula (ms)
  10.0k   0.10u     1.000     2.50     0.693         0.693
  10.0k   0.10u     1.000     3.16     1.000         1.000
  10.0k   0.10u     1.000     4.50     2.303         2.303
   4.7k   1.00u     4.700     2.50     3.258         3.258
   4.7k   1.00u     4.700     3.16     4.700         4.700
   4.7k   1.00u     4.700     4.50    10.822        10.822
 100.0k  10.00u  1000.000     2.50   693.148       693.147
 100.0k  10.00u  1000.000     3.16  1000.001      1000.000
 100.0k  10.00u  1000.000     4.50  2302.586      2302.585
```

The timing scales perfectly with tau: from one millisecond to one second, same multipliers. (The simulator takes 5000 steps in every run, so its answers differ from the formula only in the sixth or seventh digit.)

The middle threshold of each group is exactly 63.2% of 5 V, which is printed as 3.16 V; it is crossed after exactly one tau.

### Step 4: Shortcuts

```
10%-90% rise time for tau = 1 ms: 2.197 ms (about 2.2 tau)
Half-way point for tau = 1 ms:    0.693 ms (about 0.69 tau)
```

### Step 5: Design and verify

```python
def design_reset_delay(delay, threshold, farads):
    tau = delay / math.log(SUPPLY_VOLTS / (SUPPLY_VOLTS - threshold))
    return tau / farads
```

```
Reset delay design: 5 ms to reach 2.5 V with 100 nF needs R = 72.1 kOhm
With the nearest standard value 68 kOhm the simulator crosses 2.5 V at 4.71 ms
```

## Use It

- **Microcontroller reset.** Many datasheets (for example the ATmega328P used on Arduino Uno boards) describe the external reset pin with an internal pull-up of a few tens of kilohms. Adding a capacitor to ground delays the release of reset by roughly 0.7 x R x C.
- **Debouncing.** Pick tau a few times longer than the contact bounce (typically 5-20 ms) so the input crosses its threshold only once.
- **Oscilloscope probes and logic edges.** The 10%-90% rise time of an edge is 2.2 tau of whatever RC is slowing it. A 50 Ohm source driving 20 pF of cable and input capacitance has tau = 1 ns and a rise time of 2.2 ns.
- **Sensor settling.** An ADC with a 10 pF sampling capacitor behind a 1 kOhm source has tau = 10 ns; for 12-bit accuracy (1 part in 4096) it needs ln(4096) = 8.3 tau = 83 ns of sampling time. Datasheets give exactly this kind of minimum sampling time.
- **The 555 timer.** In astable mode the capacitor swings between 1/3 and 2/3 of the supply. Charging from 1/3 to 2/3 takes tau x ln(2) = 0.693 tau, which is the famous 0.693 in its formulas.

## Try It in the Lab

In the lab "Release reset at the right moment", a 5 V supply charges a 100 nF capacitor through a resistor you choose. A chip watching the capacitor leaves reset when it crosses 2.5 V, and that must happen between 0.6 ms and 0.8 ms after power-up. Turn the window of times into a window of tau values using the half-way shortcut, then into a window of resistances. Which of the offered resistors lands inside?

## Common Mistakes

- **Thinking tau is the time to fully charge.** After one tau it is only 63% charged. "Fully" means about 5 tau.
- **Using log base 10.** The formulas need the natural log (ln, `math.log` in Python). log10(2) = 0.301 gives a very wrong answer.
- **Swapping V - Vth and Vth.** For charging toward V, the time depends on the voltage still missing, V - Vth. Sanity check: a threshold close to V must give a long time.
- **Forgetting prefixes in R x C.** kOhm x uF = ms. MOhm x uF = s. kOhm x nF = us. Write them out until the pattern is automatic.
- **Using the supply voltage when the start is not 0 V.** If the capacitor starts at some voltage, use the general recipe from Lesson 03 and solve it the same way.
- **Ignoring tolerance.** A 20% capacitor makes tau 20% uncertain; design with margin.

## Exercises

1. What is tau for 47 kOhm and 220 nF? How long until the capacitor reaches 95% of the supply?
2. A 3.3 V supply charges an RC with tau = 2 ms. When does the capacitor reach 2.0 V (a typical logic-high threshold)?
3. You see a capacitor charging toward 12 V on a scope. It reaches 6 V at 3.5 ms. What is tau? If R = 10 kOhm, what is C?
4. Design a debounce circuit: 3.3 V supply, the input must not cross 1.65 V sooner than 10 ms after the button releases. You have a 1 uF capacitor. Which standard resistor (E12: 10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82 times a power of ten) do you choose?
5. A 1000 uF capacitor at 400 V is discharged by a 100 kOhm "bleeder" resistor when a device is switched off. How long until it is below 50 V? Below 5 V? Is that fast enough for someone who opens the case right away?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Time constant | "RC" | tau = R x C seconds: the time to cover 63% of the remaining distance, or the time to finish at the starting speed |
| Five tau | "Fully charged" | 99.3% charged; the usual engineering meaning of "settled" |
| Rise time | "How fast the edge is" | Time from 10% to 90% of the step, equal to 2.2 tau for an RC |
| Threshold crossing | "When it switches" | The moment v(t) passes a level, t = tau x ln(V / (V - Vth)) |
| ln | "log" | The natural logarithm, the inverse of e^x; not log base 10 |
| Settling time | "Wait a bit" | Time to get within a given error of the final value: tau x ln(1 / error fraction) |

## Further Reading

- [All About Circuits, Vol. I, Chapter 16: Voltage and Current Calculations](https://www.allaboutcircuits.com/textbook/direct-current/chpt-16/voltage-current-calculations/) - the universal time-constant formula with worked problems.
- *Practical Electronics for Inventors*, 4th ed., Scherz & Monk, section on RC time constants - practical timing circuits.
- [Texas Instruments NE555 precision timer datasheet](https://www.ti.com/product/NE555) - timing equations built on 0.693 RC.
- [Microchip ATmega328P datasheet, System Control and Reset chapter](https://www.microchip.com/en-us/product/atmega328p) - a real reset pin, its pull-up and its thresholds.
