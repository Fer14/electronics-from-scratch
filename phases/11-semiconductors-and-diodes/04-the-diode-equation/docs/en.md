# The Diode Equation

> A diode's current is a tiny number multiplied by e to the voltage over 26 mV. That one exponential explains the "0.7 V drop", the knee, the 60 mV per decade and why diodes are thermometers.

**Type:** Build
**Prerequisites:** 11-03 (The pn Junction); Phase 03 (Resistance and Ohm's Law), lesson 07-when-ohms-law-fails; Phase 05 (Circuit Analysis and Our Simulator), lesson 04-modified-nodal-analysis-from-scratch
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| I-V curve | A graph of a part's current (I) against the voltage (V) across it | A part's "personality chart" |
| Exponential | A quantity that multiplies by the same factor every time its input grows by a fixed step | Bacteria doubling every 20 minutes |
| Shockley equation | The formula I = I_S (e^(V/(n V_T)) − 1) for an ideal pn junction | The diode's Ohm's law, but curved |
| Saturation current (I_S) | The tiny reverse current of the junction; also the scale factor of the forward current | The size of the "seed" that the exponential multiplies |
| Ideality factor (n) | A number between about 1 and 2 that stretches the exponential for real diodes | A correction for "real life is a bit lazier than the ideal" |
| Knee | The region where the curve bends from "almost no current" to "lots of current" | The bend of your leg: flat thigh, then steep shin |
| Forward voltage (V_F) | The voltage across a diode when it is conducting a given current | The "toll" the current pays to cross |
| Decade | A factor of 10 | One step on the 1-10-100-1000 ladder |
| Logarithm (ln) | The inverse of the exponential: ln(e^x) = x | Asking "how many doublings got me here?" |
| Series resistance | The ordinary resistance of the silicon and contacts, in series with the ideal junction | A short narrow corridor after the turnstile |
| Temperature coefficient | How much a quantity changes per degree of temperature | How much a metal ruler grows on a hot day |
| Model | A simplified description of a part, good enough for a purpose | A map: useful precisely because it leaves things out |

## Learning Objectives

- State the Shockley diode equation, read it out loud and explain each symbol.
- Compute a diode's current from its voltage and its voltage from its current.
- Explain the "60 mV per decade" rule and why the knee seems to sit near 0.6-0.7 V.
- Use three diode models (ideal switch, constant drop, exponential) and know when each is good enough.
- Explain why a diode's forward voltage falls by about 2 mV per °C.
- Check the formula against our simulator.

## The Problem

In lesson 03 we saw *why* a junction conducts one way: lowering the hill multiplies the number of carriers that cross by exp(V/V_T). To design circuits we need more than "one way": we need numbers. If I put a diode in series with a resistor across a 5 V supply, what current flows? How hot will the diode get at 1 A? If the temperature rises by 30 °C, how much does the voltage change?

Ohm's law can't answer, because a diode is not a resistor. Its "resistance" changes by a factor of a million across a few tenths of a volt. We need the diode's own law. It was written down by William Shockley in 1949, and it is the single most used equation in analogue electronics after Ohm's.

## The Physics

From lesson 03: with forward voltage V applied, the barrier is lower by V and the flow of carriers climbing over it is multiplied by e^(V/V_T). Meanwhile, the small reverse flow of minority carriers rolling *down* the hill does not depend on V at all; call it I_S.

At zero volts the two flows balance (no net current): the climbing flow equals I_S. With bias V the climbing flow becomes I_S × e^(V/V_T), and the rolling flow is still I_S in the opposite direction. The net current is the difference:

```
I = I_S × e^(V / V_T)  −  I_S  =  I_S × ( e^(V / V_T) − 1 )
```

That is the whole derivation, physically. (A full derivation solves the diffusion of minority carriers on each side and gives I_S in terms of doping, area and how long carriers live before recombining; the shape is the same.)

What sets I_S? It is proportional to the junction area and to n_i² (the number of minority carriers available, from lesson 02's mass action law). For a small silicon diode it is somewhere between 10⁻¹⁵ and 10⁻⁹ A. Since n_i² depends on temperature exponentially, so does I_S: this will make the diode a thermometer.

## The Concept

### The Shockley equation

```
I = I_S × ( exp( V / (n × V_T) ) − 1 )
```

Read it out loud: "the diode current equals the saturation current times (e raised to the diode voltage divided by n times the thermal voltage, minus one)". Symbols:

- `I`: current through the diode, in amperes, positive from anode to cathode.
- `V`: voltage across the diode, anode minus cathode, in volts.
- `I_S`: saturation current, in amperes. We will use 10⁻¹⁴ A (a typical textbook small-signal value, and our simulator's default).
- `V_T`: thermal voltage kT/q, 0.02585 V at 300 K (27 °C).
- `n`: ideality factor. 1 for a perfect junction, up to about 2 for real ones (some carriers recombine inside the depletion region, which "softens" the exponential). We use 1 here.
- `exp(x)` = e^x, with e ≈ 2.718.

### Worked numbers

At V = 0.6 V:

```
V / V_T = 0.6 / 0.02585 = 23.21
e^23.21 = 1.20e10
I = 1e-14 × (1.20e10 − 1) = 1.20e-4 A = 0.12 mA
```

At V = 0.7 V:

```
0.7 / 0.02585 = 27.08,   e^27.08 = 5.75e11
I = 1e-14 × 5.75e11 = 5.75e-3 A = 5.75 mA
```

Adding 0.1 V multiplied the current by 48. Our script prints the table:

| V | I |
|---|---|
| −1.00 V | −1.0 × 10⁻¹⁴ A |
| 0.00 V | 0 |
| 0.30 V | 1.1 nA |
| 0.50 V | 2.5 µA |
| 0.60 V | 0.12 mA |
| 0.65 V | 0.83 mA |
| 0.70 V | 5.75 mA |
| 0.75 V | 39.8 mA |
| 0.80 V | 275 mA |

Look at the reverse row: at −1 V the term e^(V/V_T) is e^(−38.7) ≈ 10⁻¹⁷, practically zero, so I ≈ −I_S. That is the "−1" in the equation at work: in reverse, the current is stuck at −I_S whatever the voltage (until breakdown, lesson 08).

### Going backwards: voltage from current

Often you know the current (a resistor sets it) and want the voltage. Solve the equation for V: add 1 to both sides of I/I_S = e^(V/(nV_T)) − 1 and take the logarithm.

```
V = n × V_T × ln( I / I_S + 1 )
```

Read: "the diode voltage equals n times the thermal voltage times the natural log of (current over saturation current, plus one)".

At 1 mA: I/I_S = 10⁻³ / 10⁻¹⁴ = 10¹¹. ln(10¹¹) = 11 × 2.3026 = 25.33. V = 0.02585 × 25.33 = **0.6548 V**.

### 60 mV per decade

Since V depends on the *logarithm* of I, multiplying I by 10 adds the same voltage every time:

```
ΔV = n × V_T × ln(10) = 1 × 0.02585 × 2.3026 = 0.0595 V  ≈ 60 mV
```

The script confirms:

```
I =   1e-06 A  ->  V = 0.4762 V
I =   1e-05 A  ->  V = 0.5357 V   (+59.5 mV)
I =   1e-04 A  ->  V = 0.5952 V   (+59.5 mV)
I =   1e-03 A  ->  V = 0.6548 V   (+59.5 mV)
I =   1e-02 A  ->  V = 0.7143 V   (+59.5 mV)
I =   1e-01 A  ->  V = 0.7738 V   (+59.5 mV)
```

Five decades of current (100,000×) for 0.3 V of voltage. For a diode with n = 2 (many LEDs and power diodes), it is 119 mV per decade.

### Why "0.7 V"?

Everyday circuits run diodes between about 0.1 mA and 100 mA. Over that range the voltage only moves from 0.60 to 0.77 V. So a designer who says "a silicon diode drops 0.7 V" is right within about ±0.1 V for almost any circuit, without ever touching a logarithm. The **knee** you see on a linear plot near 0.65 V is not a property of silicon: it is where the current becomes big enough to see on the chosen scale. Plot on a log scale and the knee vanishes into a straight line (open `code/out.png`).

```
  I (mA)                                    log I
   20 |                    /                 |               /
      |                   /                  |            /
   10 |                  /                   |         /     straight line:
      |                 /                    |      /        x10 every 60 mV
    0 |________________/                     |   /
      +----+----+----+----+--- V             +----+----+----+---- V
      0   0.2  0.4  0.6  0.8                 0   0.2  0.4  0.6
          linear axes: "knee"                    log axis: no knee
```

### Three models

You will choose among three levels of detail:

```
  1. IDEAL SWITCH            2. CONSTANT DROP             3. EXPONENTIAL
  forward: short circuit     forward: a 0.7 V "battery"   I = I_S (e^(V/nV_T) - 1)
  reverse: open circuit      reverse: open circuit        (needs iteration, lesson 05)
```

How good are they? Two circuits from the script, a diode in series with a resistor:

| Circuit | Ideal switch | Constant drop | Exponential (simulator) |
|---|---|---|---|
| 5 V, 1 kΩ | 5.000 mA | 4.300 mA | 4.307 mA (V_D = 0.6925 V) |
| 1 V, 100 Ω | 10.000 mA | 3.000 mA | 3.155 mA (V_D = 0.6845 V) |

With 5 V of supply, the 0.7 V drop is a small part of the story; the constant-drop model is within 0.2 %. With 1 V of supply, the diode eats most of it, the ideal switch is off by a factor of 3, and the constant drop is off by 5 %. **Rule of thumb: when the supply is many times larger than 0.7 V, use constant drop; when it is comparable, use the exponential.**

### Series resistance

Real diodes have a little ordinary resistance r_s in series (the bulk silicon and the leads), typically 0.05 Ω for a big rectifier, around 1 Ω for a small signal diode. At low current it is irrelevant; at high current it dominates. A 1N4148 at 100 mA drops about 1 V instead of the ideal 0.77 V partly for this reason. The full voltage is

```
V_total = n V_T ln(I / I_S + 1)  +  I × r_s
```

### Temperature: the diode as a thermometer

I_S is built from n_i², which grows like T³ × e^(−E_g/kT). Hotter junction, bigger I_S, so the same current needs less voltage. The script holds 1 mA and heats the diode:

```
   0 C   I_S = 1.07e-16 A   V = 0.7030 V
  25 C   I_S = 7.50e-15 A   V = 0.6581 V
  50 C   I_S = 2.78e-13 A   V = 0.6127 V
 100 C   I_S = 9.39e-11 A   V = 0.5203 V
 slope = -1.83 mV per degree C
```

I_S grows by about a million between 0 and 100 °C, and V falls by roughly **2 mV per °C**. This is reliable enough that the temperature sensors inside many chips (and parts such as the LM35) are built around this effect.

Note that V_T itself *grows* with temperature (kT/q). That pushes the other way, but the I_S effect wins easily.

## Build It

### Step 1: The equation and its inverse

```python
def diode_current(volts, saturation=SATURATION_CURRENT, ideality=IDEALITY, kelvin=300.0):
    return saturation * (np.exp(volts / (ideality * thermal_voltage(kelvin))) - 1.0)


def diode_voltage(amps, saturation=SATURATION_CURRENT, ideality=IDEALITY, kelvin=300.0):
    return ideality * thermal_voltage(kelvin) * np.log(amps / saturation + 1.0)
```

Both work on single numbers or on whole NumPy arrays.

### Step 2: The decade ladder

`show_decades` walks the current up by factors of 10 and prints the extra voltage each time: 59.5 mV, exactly n × V_T × ln 10.

### Step 3: Temperature

```python
def saturation_at(kelvin, saturation_300=SATURATION_CURRENT):
    return saturation_300 * (kelvin / 300.0) ** 3 * np.exp(-SILICON_GAP_EV / BOLTZMANN_EV * (1 / kelvin - 1 / 300.0))
```

This scales I_S from its 300 K value using the T³ e^(−E_g/kT) law, then `diode_voltage` gives V at 1 mA.

### Step 4: Ask the simulator

```python
circuit = Circuit()
circuit.voltage_source("V1", "a", "0", volts)
circuit.diode("D1", "a", "0", Is=SATURATION_CURRENT, n=IDEALITY)
result = circuit.dc()
simulated = result.i("D1")
```

The simulator and the formula agree to all printed digits (for example 8.3084 × 10⁻⁴ A at 0.65 V; the last digit can differ by one from rounding). That is no surprise when the voltage is forced by a source; the interesting case is a diode with a resistor, where nobody tells us V. The simulator solves it by iteration. Lesson 05 builds that iteration ourselves.

### Step 5: Compare the models and plot

`compare_models` prints the table of the three models above, and `plot_curves` saves `out.png` with linear and log views of the same curve.

```
uv run python phases/11-semiconductors-and-diodes/04-the-diode-equation/code/main.py
```

## Use It

Reading real datasheets with the equation in mind:

- **1N4148** (small-signal switching diode): forward voltage max 1.0 V at 10 mA (typical about 0.72 V at 10 mA), reverse leakage max 25 nA at 20 V. Fits roughly I_S ≈ 2-4 nA with n ≈ 1.8-1.9 plus a little series resistance. Notice the leakage is far above I_S = 10⁻¹⁴: real reverse currents are dominated by generation in the depletion region and surface leakage.
- **1N4001-1N4007** (1 A rectifiers): V_F max 1.1 V at 1 A. At 1 A the series resistance matters.
- **Schottky diodes** (1N5817-1N5819, BAT54): a metal-semiconductor junction with a much larger I_S, so the forward voltage is only about 0.3-0.45 V. Used where every tenth of a volt counts (battery inputs, fast converters), at the cost of more leakage.
- **Temperature sensing**: many microcontrollers read an internal diode-connected transistor (about −2 mV/°C) to report chip temperature. The LM35's datasheet output (10 mV/°C) is derived from transistor junctions.
- **Log amplifiers**: because V is proportional to ln(I), a diode in an op-amp feedback loop (Phase 13) computes logarithms, used in audio level meters and RF power detectors.

## Try It in the Lab

Open the lab for this lesson: a 5 V supply, an empty resistor slot and a silicon diode to ground. Your job is to bias the diode at about 1 mA, the current at which small-signal diodes are usually characterised, and keep its voltage in the range typical of that current.

Things to think about: estimate the diode voltage first (is "0.7 V" good enough here?), then use Ohm's law on the resistor. Then check: does your choice keep the diode voltage in the target window? What happens to the voltage if you pick a resistor ten times smaller?

## Common Mistakes

- **Treating 0.7 V as a law of nature.** It is a convenient approximation. A diode at 1 µA sits near 0.48 V; at 1 A it may be above 1 V.
- **Forgetting the "−1".** It barely matters forward, but without it the reverse current would be zero instead of −I_S.
- **Using the equation with a voltage source directly across a diode in real life.** On paper it's fine; in a real circuit, 0.85 V across a small diode would ask for amps and destroy it. Always limit current with a resistor.
- **Mixing log bases.** ln is the natural log (base e). 60 mV per decade comes from ln(10) = 2.303. Using log10 by mistake gives answers off by that factor.
- **Ignoring temperature.** Two diodes in parallel do not share current equally: the hotter one has lower V_F, takes more current, gets hotter still. This is called thermal runaway.
- **Thinking I_S is the leakage you measure.** Measured reverse leakage is usually much larger than the I_S fitted from the forward curve.

## Exercises

1. Using I_S = 10⁻¹⁴ A and n = 1, what current flows at 0.62 V? At 0.68 V? Check that the ratio is close to 10.
2. What voltage gives 20 mA? Compare with the "0.7 V" rule.
3. A diode with n = 2 and I_S = 10⁻⁹ A: what is its voltage at 10 mA? How many mV per decade?
4. A 3.3 V supply drives a diode through a 220 Ω resistor. Estimate the current with the constant-drop model, then improve it once: compute V from the diode equation at that current, recompute the current. How much did it change?
5. A diode sensor reads 0.600 V at 25 °C at a constant 100 µA. Later it reads 0.552 V. Using −2 mV/°C, what is the new temperature?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Shockley equation | "The diode equation" | I = I_S (e^(V/nV_T) − 1): net current from barrier-climbing carriers minus the reverse minority flow |
| I_S | "Saturation current" | Scale factor of the exponential; proportional to junction area and n_i², strongly temperature dependent |
| n | "Ideality factor" | 1 to 2; stretches the exponential, giving 60-120 mV per decade |
| V_F | "Forward drop" | Voltage across a conducting diode at a specified current |
| Knee | "Turn-on voltage" | Where the exponential becomes visible on a linear current scale; not a sharp threshold |
| Constant-drop model | "0.7 V model" | Replace a forward diode by a fixed 0.7 V source; good when supplies are much larger than 0.7 V |
| −2 mV/°C | "Diode tempco" | Forward voltage at fixed current falls about 2 mV per degree in silicon |

## Further Reading

- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., section 1.6 and section 2.3 (the Ebers-Moll/exponential view of junctions).
- *All About Circuits*, Volume III, chapter 3 "Diodes and Rectifiers", section "Meter check of a diode" and "Diode ratings". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-3/meter-check-of-a-diode/
- 1N4148 datasheet (onsemi or Vishay): forward voltage curves at several temperatures. https://www.vishay.com/docs/81857/1n4148.pdf
- MIT OpenCourseWare 6.002 *Circuits and Electronics*, lecture on nonlinear analysis (diode models). https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/
