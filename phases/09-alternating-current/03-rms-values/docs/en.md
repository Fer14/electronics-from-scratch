# RMS Values

> "230 volts" at the wall is not the highest voltage, nor the average. It is the DC voltage that would heat a kettle exactly as much.

**Type:** Build
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Lesson 05 (Power and Heat); Phase 09, Lessons 01 (Why Alternating Current) and 02 (Sine Waves, Frequency and Phase)
**Time:** ~55 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Average (mean) | Add all the values and divide by how many there are | Your average speed on a trip: total distance over total time |
| Instantaneous power | The power at one exact instant, p = v x i | The speedometer reading at one moment, not the trip average |
| Square (of a number) | The number times itself: 3 squared is 9; a negative number squared is positive | Area of a square tile with that side length: never negative |
| Square root | The number that, multiplied by itself, gives the original: the square root of 9 is 3 | Undoing the "area of a tile" to get back the side |
| RMS (root mean square) | Square every value, take the mean, take the square root: the "heating" size of a changing signal | The steady speed that would cover the same "effort" as your stop-and-go drive |
| Effective value | Another name for RMS: the DC value with the same heating effect | The fixed salary that pays the same per year as a variable one |
| Rectified average | The average of the absolute value (all the negatives flipped up) | Average distance from home, ignoring which direction you went |
| Crest factor | Peak divided by RMS: how "spiky" a waveform is | How much higher the tallest wave is compared with the typical sea state |
| True-RMS meter | A multimeter that really computes the RMS of any waveform | A scale that weighs the actual parcel instead of guessing from its size |
| Duty cycle | Fraction of each period a pulse wave spends "on" | A light switched on 15 minutes of every hour: 25% duty |

## Learning Objectives

- Explain why the plain average of an AC voltage is useless for describing it, and why we need a different kind of "size".
- Define RMS as "root of the mean of the square" and compute it by hand from a few samples and by computer from many.
- Show that for a sine wave V_rms = V_peak / sqrt(2) = 0.7071 x V_peak, and use it both ways (230 V RMS has a 325 V peak).
- Compute the RMS and the average of square, triangle, rectified and offset waveforms.
- Confirm with the simulator that an AC sine heats a resistor exactly like a DC voltage equal to its RMS value.

## The Problem

The label on your kettle says "230 V ~ 50 Hz, 2000 W". From Lesson 02 you know the voltage at the socket is a sine wave that swings up and down, through zero, negative and back. So which number is "230 V"? It cannot be the voltage at every instant, because the voltage is changing all the time. It cannot be the average either: a sine wave spends exactly as long positive as negative, so its average is zero. A kettle running on "zero volts on average" would never boil.

And it is not the peak. If you look at the mains with an oscilloscope (through a proper isolating probe: do not try this yourself), the peaks reach about 325 V. So we need a single number that says "how strong" an AC voltage is, in a way that lets you use all the DC formulas you know (P = V x V / R, for instance) without lying. That number is the RMS value, and every AC voltage and current printed on a label, a datasheet or a multimeter display is an RMS value unless it says otherwise.

## The Physics

### Heating does not care about direction

From Phase 03, Lesson 05, a resistor R with voltage v across it turns electrical energy into heat at a rate

```
p = v x v / R      (read: "power equals voltage squared over resistance")
```

We write lower-case p and v for values that change with time ("instantaneous" values), and capital P and V for fixed or summary values. Now notice: v is squared. A voltage of -100 V gives (-100) x (-100) / R = 10,000 / R, exactly the same heating as +100 V. Electrons pushed left or right rub against the metal lattice just the same, and the resistor warms up either way.

So for heating, the sign does not matter, but the size does, and it matters **squared**: 200 V heats four times as much as 100 V, not twice.

### What actually reaches your kettle

The kettle element is a resistor. As the mains sine wave goes round, the heating power goes up and down: zero when the voltage crosses zero, maximum at the positive peak, zero again, maximum again at the negative peak. Twice per cycle, so 100 times per second on 50 Hz mains. The water is far too slow to notice the wiggle: what matters for boiling is the **average power**, averaged over a full cycle.

So the honest question is: what DC voltage would give the same **average power** in the same resistor? That DC voltage is called the **effective value**, and its recipe gives its other name, root mean square.

## The Concept

### Why not just average?

Take the 10 V amplitude, 50 Hz sine wave of Lesson 02, sampled at eight evenly spaced moments of one period:

| t (ms) | 0 | 2.5 | 5 | 7.5 | 10 | 12.5 | 15 | 17.5 |
|---|---|---|---|---|---|---|---|---|
| v (V) | 0 | 7.071 | 10 | 7.071 | 0 | -7.071 | -10 | -7.071 |

Average: (0 + 7.071 + 10 + 7.071 + 0 - 7.071 - 10 - 7.071) / 8 = 0 / 8 = 0 V. The positive and negative halves cancel exactly. Useless.

You could average the absolute values (flip the negatives up): (0 + 7.071 + 10 + 7.071 + 0 + 7.071 + 10 + 7.071) / 8 = 48.28 / 8 = 6.04 V. This "rectified average" is closer to something meaningful, but it does not predict heating correctly, because heating goes with the **square** of the voltage.

### Root, mean, square: read it backwards

To get a voltage whose square gives the right average heating, follow the name from right to left:

1. **Square** every value (this makes them all positive and weighs them like heating does).
2. Take the **mean** (average) of the squares.
3. Take the square **root** of that mean (to get back to volts instead of volts squared).

```
V_rms = square root of ( mean of v^2 )
```

Read it aloud: "the RMS voltage is the square root of the average of the voltage squared".

With the eight samples:

| v (V) | 0 | 7.071 | 10 | 7.071 | 0 | -7.071 | -10 | -7.071 |
|---|---|---|---|---|---|---|---|---|
| v^2 (V^2) | 0 | 50 | 100 | 50 | 0 | 50 | 100 | 50 |

(7.071 x 7.071 = 50.0, and (-7.071) x (-7.071) is also 50.0.)

Mean of the squares: (0 + 50 + 100 + 50 + 0 + 50 + 100 + 50) / 8 = 400 / 8 = 50 V^2.

Square root: sqrt(50) = 7.071 V.

So a 10 V peak sine wave has an RMS value of 7.071 V. Using more samples does not change the answer for a sine wave (the script uses 100,000 per period and gets the same 7.071 to many decimals).

### Why it works: a 7.071 V battery heats the same

Put the 10 V peak sine across a 50 ohm resistor. The instantaneous power is v^2 / 50, so the mean power is (mean of v^2) / 50 = 50 / 50 = 1 W.

Now put a 7.071 V battery across the same resistor: P = 7.071 x 7.071 / 50 = 50 / 50 = 1 W. Identical. That is the definition working: **the RMS value is the DC value that delivers the same average power to a resistor.** And because it is defined this way, the DC formulas work for AC as long as you use RMS values:

```
P_average = V_rms x V_rms / R = I_rms x I_rms x R = V_rms x I_rms     (for a resistor)
```

### The magic number sqrt(2)

For any sine wave, the RMS value is the peak divided by the square root of 2:

```
V_rms = V_peak / sqrt(2) = 0.7071 x V_peak
V_peak = sqrt(2) x V_rms = 1.4142 x V_rms
```

Why exactly sqrt(2)? Look again at the squared samples: 0, 50, 100, 50, 0, 50, 100, 50. They swing between 0 and 100 (the peak squared), symmetrically around 50. The squared sine always spends as much time above half its maximum as below it, so its average is exactly half its maximum: mean of v^2 = V_peak^2 / 2. (Trigonometry says the same thing with the identity sin^2(x) = (1 - cos(2x)) / 2: a constant 1/2 plus a wave that averages to zero.) Taking the root: V_rms = sqrt(V_peak^2 / 2) = V_peak / sqrt(2).

Mains examples (using sqrt(2) = 1.4142):

| Label (RMS) | Peak = 1.4142 x RMS | Peak-to-peak |
|---|---|---|
| 230 V (Europe) | 325.3 V | 650.5 V |
| 120 V (North America) | 169.7 V | 339.4 V |
| 100 V (Japan) | 141.4 V | 282.8 V |
| 12 V AC doorbell transformer | 17.0 V | 33.9 V |

That is why a "230 V" capacitor in a mains circuit must be rated well above 325 V: insulation fails at the peak, not at the RMS.

### The kettle in numbers

A 1000 W heater on 230 V has resistance R = V^2 / P = 230 x 230 / 1000 = 52.9 ohm. At the peak, 325.3 V across 52.9 ohm gives an instantaneous power of 325.3 x 325.3 / 52.9 = 2,000 W. At the zero crossings it is 0 W. The average of a "squared sine" is half its peak, so the average is 1,000 W, exactly the label. The power pulses between 0 and 2,000 W a hundred times a second.

```
 p(t)
 2000 W |   _       _       _       _
        |  / \     / \     / \     / \
 1000 W |-/---\---/---\---/---\---/---\--   <- average
        |/     \_/     \_/     \_/     \_
    0 W +---------------------------------- t
        0     10 ms   20 ms   30 ms
```

### RMS of other shapes

RMS is defined for any waveform, not just sines. The factor sqrt(2) is **only** for sines. Some useful results, all with peak 1 V:

| Waveform | Average | RMS | Why |
|---|---|---|---|
| Sine, +-1 V | 0 | 0.7071 | peak / sqrt(2) |
| Square, +-1 V | 0 | 1.0000 | v^2 is 1 all the time |
| Triangle, +-1 V | 0 | 0.5774 | peak / sqrt(3): spends more time near zero than a sine |
| Half-wave rectified sine | 0.3183 | 0.5000 | half the cycle is cut to zero, so the mean square halves |
| Full-wave rectified sine | 0.6366 | 0.7071 | flipping negatives does not change v^2 |
| Sine of peak 1 on a 0.5 V offset | 0.5 | 0.8660 | sqrt(0.5^2 + 0.7071^2): DC and AC parts add "in squares" |
| Pulse 0 to 1 V, 25% duty | 0.25 | 0.5000 | sqrt(0.25 x 1^2) |

Two lessons hide in this table. First, the rectified sine's average (0.6366 = 2 / pi) differs from its RMS (0.7071): they are different ideas. Second, when a DC part and an AC part are mixed, their RMS values combine like the sides of a right triangle: total RMS = sqrt(DC^2 + AC_rms^2). The square-of-a-sum cross term averages to zero over a cycle.

### Worked example: a pulse train by hand

A microcontroller pin (Phase 17) switches between 0 V and 5 V: on for 1 ms, off for 3 ms, repeating every 4 ms. That is a 25% duty cycle. Take four samples per period, one per millisecond: 5, 0, 0, 0 volts.

- Average: (5 + 0 + 0 + 0) / 4 = 1.25 V.
- Squares: 25, 0, 0, 0 V^2. Mean of squares: 25 / 4 = 6.25 V^2. Root: sqrt(6.25) = 2.5 V.

So a 100 ohm resistor on this pin gets 2.5 x 2.5 / 100 = 0.0625 W = 62.5 mW of heat on average (check directly: 5 x 5 / 100 = 0.25 W for a quarter of the time is 0.0625 W). Using the average (1.25 V) instead would predict 1.25 x 1.25 / 100 = 15.6 mW, four times too little. For heating, always use RMS.

### Worked example: RMS current and a fuse

A 2,000 W kettle on 230 V draws I_rms = P / V_rms = 2,000 / 230 = 8.70 A RMS. Its peak current is 8.70 x 1.4142 = 12.3 A. A 10 A fuse is fine, because a fuse heats according to I_rms^2 x R_fuse: it "sees" 8.7 A, not the 12.3 A peaks. A fuse rated by peak current would be the wrong idea entirely.

### How a computer finds RMS

With samples taken evenly over a whole number of periods, the recipe is three lines: square the array, average it, take the square root. That is a numerical version of the integral that textbooks write as

```
V_rms = sqrt( (1/T) x integral from 0 to T of v(t)^2 dt )
```

Read it: "the square root of: one over the period, times the area under the v-squared curve over one period". The area under a curve divided by its width is its average height, so this is exactly "mean of the square", made continuous. With many evenly spaced samples, the plain average approximates the integral very well.

Measure over **whole periods**. If you average 1.5 cycles of a sine, the extra half-cycle biases the result.

### What your multimeter shows

Cheap multimeters measure the **rectified average** and multiply it by 1.111 (which is 0.7071 / 0.6366), a factor that is right only for pure sine waves. On a square wave or the spiky current of a phone charger they can be wrong by 10-50%. Meters labelled **true RMS** compute the real thing. Remember this when you meet distorted waveforms in Phases 11 and 18.

## Build It

### Step 1: The plain average

```python
SAMPLES_PER_PERIOD = 100_000


def one_period(freq):
    return np.arange(SAMPLES_PER_PERIOD) / (SAMPLES_PER_PERIOD * freq)


def mean(values):
    return float(np.mean(values))
```

`one_period` returns 100,000 evenly spaced times covering exactly one period (the last sample stops one step before T so the period is not counted twice). For a 325.27 V peak sine, the average comes out as 0.000000 V and the rectified average 207.07 V, matching 2 / pi x 325.27.

### Step 2: The RMS function

```python
def rms(values):
    return math.sqrt(mean(np.square(values)))
```

Root, mean, square, read right to left in code too. It prints a mean square of 52,900.3 V^2 and an RMS of 230.001 V (the peak 325.27 V is rounded, so the RMS is not exactly 230).

### Step 3: The kettle

The script computes R = 52.90 ohm, the instantaneous power `v**2 / resistance` (from 0.0 W to 2000.0 W) and its average (1000.0 W).

### Step 4: Other waveforms

```python
def waveforms(peak, freq):
    t = one_period(freq)
    phase = (t * freq) % 1.0
    s = np.sin(2 * np.pi * freq * t)
    return {
        "sine": peak * s,
        "square": np.where(phase < 0.5, peak, -peak),
        "triangle": peak * (1 - 4 * np.abs(phase - 0.5)),
        "half-wave rectified sine": peak * np.maximum(s, 0),
        "full-wave rectified sine": peak * np.abs(s),
        "sine on a DC offset of peak/2": peak / 2 + peak * s,
        "PWM 0 to peak, 25% duty": np.where(phase < 0.25, peak, 0.0),
    }
```

`phase` runs from 0 to 1 over each period; `np.where(condition, a, b)` picks a where the condition holds and b elsewhere, which builds square and pulse waves. The printed table reproduces the one in The Concept.

### Step 5: AC versus DC in the simulator

```python
def average_power(time, volts, amps, freq, cycles):
    keep = time >= time[-1] - cycles / freq
    p = volts[keep] * amps[keep]
    return float(np.trapezoid(p, time[keep]) / (time[keep][-1] - time[keep][0]))
```

We simulate a 10 V peak, 50 Hz sine across a 50 ohm "heater", multiply voltage by current at every time step to get the instantaneous power, and average it over the last two full cycles. `np.trapezoid` computes the area under the power curve (energy, in joules); dividing by the time span gives average power. Then we build a second circuit with a 7.0711 V battery and ask the DC solver for the resistor's power. Expected output:

```
  AC: 10 V peak sine into 50 ohm, average power = 1.0000 W
  DC: 7.0711 V battery into 50 ohm, power        = 1.0000 W
  DC at the peak value 10 V would give 2.00 W (twice too much)
```

### Step 6: Mains numbers

A short loop prints peak and peak-to-peak for 230 V, 120 V and 100 V RMS mains.

## Use It

- **Every AC rating is RMS.** "230 V", "12 V AC", "a 10 A fuse", "a 3 A RMS current rating": all RMS. Peak voltages are what insulation and component voltage ratings must survive.
- **Audio amplifiers.** "50 W RMS" is a (roughly) honest average power into a speaker; "peak music power" figures can be several times bigger and mean little.
- **Fuses and wires.** A fuse melts from heat, so it responds to RMS current. A 13 A fuse in a British plug is about RMS current.
- **Capacitor ratings in power supplies.** Capacitors in chargers carry spiky currents; datasheets give an "RMS ripple current" rating because internal heating goes with I_rms^2 x ESR (equivalent series resistance, Phase 07, Lesson 07).
- **PWM dimming and motor control.** A microcontroller pin switching between 0 and 5 V at 25% duty (Phase 17) has an average of 1.25 V but an RMS of 2.5 V. An LED's brightness follows the average current; a resistor heater's power follows the RMS.

## Try It in the Lab

The lab task "Same heat on DC" gives you a 50 ohm heater element that was designed to run from an AC supply of 10 V peak. You only have a 12 V battery, so you must add a series resistor that makes the heater produce the same heat it would on that AC supply. Before choosing, work out the heater power on the AC supply (use RMS!), then the current that gives the same power, then the resistor that lets that current flow from 12 V. Think about what answer you would get if you wrongly used the peak value, or the rectified average, and look for those traps among the parts.

## Common Mistakes

- **Using the peak in P = V^2 / R.** 10 V peak across 50 ohm is 1 W, not 2 W. Use V_rms.
- **Using sqrt(2) for every waveform.** 0.7071 x peak is only for sines. A square wave's RMS equals its peak; a triangle's is peak / sqrt(3).
- **Confusing rectified average and RMS.** 0.6366 x peak vs 0.7071 x peak for a sine. A cheap meter hides the difference by scaling, which only works on sines.
- **Averaging over a non-whole number of periods.** Partial cycles bias both the average and the RMS.
- **Forgetting that a 230 V line peaks at 325 V.** Rate insulation, capacitors and semiconductors for the peak (plus margin for spikes).
- **Thinking RMS is "the average of the absolute value".** It is the root of the average of the squares; for most waveforms it is larger than the rectified average.

## Exercises

1. **Hand RMS.** A waveform repeats the four values 3 V, -1 V, 3 V, -1 V (equal time each). Compute its average and its RMS with the root-mean-square recipe.
2. **Mains.** A heater draws 8.7 A RMS from 230 V mains. What is its power? What is the peak current? What is its resistance?
3. **Doorbell.** A 12 V AC (RMS) doorbell transformer feeds a 6 ohm coil. Compute the RMS current, the peak current and the average power.
4. **Mixed signal.** A signal is 2 V DC plus a sine of 3 V peak. Compute its total RMS value and its maximum and minimum voltage.
5. **Code.** Add a "sawtooth" (rising linearly from -1 to +1 each period, then dropping back) to `waveforms` in the script. Predict its RMS first (hint: it should match the triangle's; why?), then run.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| RMS | "The AC voltage" | Square root of the mean of the square over whole periods; the DC value with the same heating in a resistor |
| Effective value | "What it's worth in DC" | Same as RMS |
| Peak | "The top" | Maximum instantaneous value; sqrt(2) x RMS for a sine |
| Average value | "The mean" | Mean of the signal over whole periods; 0 for any symmetric AC wave |
| Rectified average | "The meter's average" | Mean of the absolute value; 2/pi x peak for a sine |
| Crest factor | "Peakiness" | Peak / RMS; 1.414 for a sine, 1 for a square wave, larger for spiky currents |
| True RMS | "A better meter" | A meter that computes the actual RMS of any waveform instead of scaling the rectified average |

## Further Reading

- [All About Circuits, Vol. II (AC), Chapter 1: Measurements of AC Magnitude](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-1/measurements-ac-magnitude/) — peak, average and RMS side by side.
- *Practical Electronics for Inventors*, Scherz & Monk, 4th ed., Chapter 2 (AC sections on RMS and power) — many practical examples with real mains numbers.
- [Fluke: What is true-RMS?](https://www.fluke.com/en-us/learn/blog/electrical/what-is-true-rms) — a meter maker's explanation of why averaging meters go wrong on distorted waveforms.
- [MIT OpenCourseWare 6.002 Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) — the AC lectures treat average power and RMS rigorously.
