# PWM

> A pin can only be fully on or fully off, but if it switches fast enough, whatever comes after it only feels the average. Pulse-width modulation turns time into voltage.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 17 (Microcontrollers), Lessons 01-02; Phase 07 (Capacitors), Lesson 04 (The Time Constant); Phase 10 (Filters and Resonance), Lesson 02 (RC Low-Pass and High-Pass); Phase 15 (Sequential Logic), Lesson 05 (Counters)
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| PWM (pulse-width modulation) | Switching a pin on and off at a fixed rate and controlling how long it stays on in each cycle. | Flicking a light switch on and off very fast, keeping it on longer when you want it brighter. |
| Period (T) | The time of one full on-off cycle, in seconds. | One lap of a running track. |
| Frequency (f) | How many periods happen per second: f = 1 / T. Measured in hertz (Hz). | Laps per minute. |
| Duty cycle (D) | The fraction of the period the pin is high, from 0 (always off) to 1 (always on). Often given as a percentage. | The fraction of each lap you sprint. |
| Average value | The voltage you would get if you smeared the on and off times out evenly: D x VDD. | Your average speed over the whole lap. |
| Counter | A register that adds 1 on every tick of a clock (Phase 15, Lesson 05). | A tally counter clicked once per beat. |
| Prescaler | A divider that lets only every N-th clock tick reach the counter, to slow it down. | Only clicking the tally on every 64th beat. |
| Compare register | A register holding a number; when the counter reaches it, the pin changes. | A mark on the track where you switch from sprinting to walking. |
| TOP | The highest value the counter reaches before it starts again from 0. | The length of the track. |
| Low-pass filter | A circuit that lets slow changes through and blocks fast ones (Phase 10). | A heavy flywheel: it follows slow pushes but ignores quick jitters. |
| Ripple | The small up-and-down wobble left on the filtered voltage. | The waves on a mostly calm lake. |
| Resolution | How many different duty cycles you can choose (for example 256 steps). | How finely marked a ruler is. |

## Learning Objectives

- Build a PWM peripheral from a counter and a compare register, and compute its frequency from the clock, prescaler and TOP
- Compute the duty cycle and average voltage for any compare value, and the compare value for a target voltage
- Explain why a load that is slow (an LED seen by an eye, a motor, a heater, an RC filter) only responds to the average
- Use our simulator to feed PWM into an RC low-pass filter and measure the average and the ripple
- Derive and check the ripple estimate `ripple = VDD x D x (1 - D) x T / (R x C)` and use it to choose R and C

## The Problem

You want to dim an LED to 25% brightness, set a fan to half speed, or produce 1.25 V for an analog circuit. But a microcontroller's GPIO pin (Lesson 02) can only be at 0 V or at VDD. It has no "a bit" setting.

One option would be a real digital-to-analog converter (Lesson 04), but many cheap chips do not have one, and a DAC cannot deliver much current anyway. Every microcontroller, however, has timers, and a timer can switch a pin on and off thousands of times per second with no help from the program. If the thing on the other end is slow compared with the switching, it only notices the average. That idea, PWM, is behind LED dimmers, motor speed controllers, class-D audio amplifiers, the switching power supplies of Phase 18, and the brightness of almost every phone screen.

## The Physics

### Slow things average fast things

An LED switches on and off in nanoseconds. Your eye does not: the retina and brain integrate light over roughly 10-20 milliseconds. If the LED is on for 0.25 ms and off for 0.75 ms, a thousand times per second, your eye receives a quarter of the light it would get from a constantly-lit LED and sees a steady, dimmer LED.

A motor works the same way. Its rotor is heavy and its winding is an inductor (Phase 08): current through an inductor cannot change quickly. Pulses of voltage give a nearly steady current whose average follows the duty cycle. A heater element is even slower: it averages over seconds.

### The capacitor as an averaging machine

For electrical signals, the simplest averaging device is the RC low-pass filter from Phase 10, Lesson 02:

```
   pin ----[ R ]----+---- out
                    |
                   === C
                    |
                   gnd
```

When the pin is high, current `(VDD - Vout) / R` flows into the capacitor and its voltage rises. When the pin is low, current `Vout / R` flows out and its voltage falls. The capacitor voltage changes slowly when `R x C` is large, because, as you saw in Phase 07, the capacitor's voltage changes by `I x time / C`.

After a while, the voltage settles at a level where the charge pushed in during the high part equals the charge pulled out during the low part. Let us find that level. Call the high time `D x T` and the low time `(1 - D) x T`. If the ripple is small, Vout is roughly constant at some value `Vavg`. Then:

```
charge in  = (VDD - Vavg) / R  x  D x T
charge out = Vavg / R          x  (1 - D) x T
```

Set them equal and cancel `R` and `T`:

```
(VDD - Vavg) x D = Vavg x (1 - D)
VDD x D - Vavg x D = Vavg - Vavg x D
VDD x D = Vavg
```

So the filtered voltage is **D x VDD**. The capacitor really does compute the average. Note how the physics gives the rule: equal charge in and out per period.

### How big is the ripple?

During the high part, the current into the capacitor is about `(VDD - Vavg) / R = VDD x (1 - D) / R`. It flows for `D x T` seconds. A capacitor's voltage changes by charge / capacitance, so:

```
ripple (peak to peak) = current x time / C
                      = [VDD x (1 - D) / R] x D x T / C
                      = VDD x D x (1 - D) x T / (R x C)
```

Read it as: "the wobble equals the supply, times the duty, times one minus the duty, times the period, divided by the time constant". Three lessons fall out of it:

- Ripple is biggest at D = 0.5 (because 0.5 x 0.5 = 0.25 is the largest value of D x (1 - D)) and vanishes at D = 0 and D = 1.
- A shorter period (higher PWM frequency) means proportionally less ripple.
- A bigger time constant `RC` means less ripple, but also slower response: the output takes about `3 RC` to reach 95% of a new value (Phase 07, Lesson 04).

This estimate assumes the ripple is small compared with the output (true when `RC` is several times `T`).

## The Concept

### PWM from a counter and a comparator

Here is how almost every microcontroller makes PWM, with no help from the program once it is set up:

```
 clock 16 MHz -->[ prescaler / 64 ]--> 250 kHz ticks
                                           |
                                           v
                      +-----------------------------------+
                      |  counter: 0, 1, 2, ... 255, 0, 1  |
                      +-----------------------------------+
                                           |
                                           v
                compare register --->[ counter < compare ? ]---> pin
```

On every tick the counter adds 1. When it reaches TOP (255 here) it goes back to 0. The pin is high while `counter < compare` and low otherwise. With `compare = 64`:

```
counter: 0  1  2 ... 63 | 64 65 ... 255 | 0  1 ...
pin:     1  1  1 ...  1 |  0  0 ...   0 | 1  1 ...
         <-- 64 ticks -->< - 192 ticks ->
```

So the duty cycle is:

```
D = compare / (TOP + 1) = 64 / 256 = 0.25
```

And the period:

```
T = prescaler x (TOP + 1) / f_clock = 64 x 256 / 16 000 000 s = 1.024 ms
f = 1 / T = 976.56 Hz
```

Read it as: "each tick lasts prescaler clock cycles, and a period is TOP + 1 ticks". (This 976.56 Hz is exactly the default PWM frequency on two of the Arduino Uno's PWM pins, because the Arduino software sets up the timer this way.)

### Choosing compare for a target voltage

If you want an average of 1.25 V from a 5 V pin:

```
D = 1.25 / 5 = 0.25
compare = D x 256 = 64
```

With 256 steps, each step changes the average by `5 V / 256 = 19.5 mV`. That is the **resolution**. More steps (TOP = 1023 gives 1024 steps) means finer control, but at the same clock the period gets 4 times longer, so the frequency is 4 times lower and the ripple 4 times bigger. Resolution and frequency trade against each other:

```
f_PWM = f_clock / (prescaler x (TOP + 1))
```

### Worked example: ripple with our filter

With `R = 10 kohm`, `C = 1 uF`: `RC = 10 000 x 0.000 001 = 0.01 s = 10 ms`. At `D = 0.25` and `T = 1.024 ms`:

```
ripple = 5 x 0.25 x 0.75 x 1.024 ms / 10 ms = 5 x 0.1875 x 0.1024 = 0.096 V = 96 mV
```

At `D = 0.5`: `5 x 0.25 x 0.1024 = 0.128 V`. Settling to 95% takes `3 x 10 ms = 30 ms`.

### What PWM is not

PWM does not produce a true intermediate voltage on the pin. The pin is still digital. Only after a slow load or a filter does the average appear. If you connect a PWM pin to a fast circuit (say another digital input, or an op-amp with no filter), that circuit sees the full 0 V and 5 V swings.

### Worked example: settings for an LED dimmer

An LED dimmer should not flicker (keep PWM above about 1 kHz, more for cameras) and should fade smoothly (aim for 10 bits, 1024 steps). With a 16 MHz clock and TOP = 1023:

```
prescaler 1:  f = 16 000 000 / (1 x 1024) = 15 625 Hz      flicker-free, 10 bits
prescaler 8:  f = 16 000 000 / (8 x 1024) =  1 953 Hz      still fine, quieter for the timer
```

Either works. With TOP = 255 (8 bits) and prescaler 1 the frequency would be 62.5 kHz, but the darkest non-zero step would be 1/256 of full brightness, which the eye sees as a visible jump.

### Worked example: a PWM "DAC" for a slow control voltage

You need a 0-3.3 V control voltage with under 10 mV of ripple, settling within 50 ms. Compare two PWM frequencies, using the worst case D = 0.5 in the ripple formula, solved for RC:

```
RC >= VDD x D x (1 - D) x T / ripple
```

At 62.5 kHz (8-bit, no prescaler, T = 16 us):

```
RC >= 3.3 x 0.25 x 16e-6 / 0.01 = 1.32 ms
choose R = 10 k, C = 150 nF:  RC = 1.5 ms,  ripple = 3.3 x 0.25 x 16 us / 1.5 ms = 8.8 mV
settling to 95%: 3 RC = 4.5 ms                                  -> both requirements met
```

At 976 Hz (T = 1.024 ms):

```
RC >= 3.3 x 0.25 x 1.024e-3 / 0.01 = 84 ms     ->  settling 3 RC = 253 ms     too slow
```

A higher PWM frequency lets the filter be faster for the same ripple. That is the general rule: put the switching frequency far above the frequencies you care about, and the filter has an easy job. (A second RC stage in series gives far more ripple rejection for the same settling time, at the cost of a few parts.)

## Build It

### Step 1: The timer as a class

```python
class PwmTimer:
    def __init__(self, prescaler, top=255):
        self.prescaler = prescaler
        self.top = top
        self.counter = 0
        self.compare = 0

    def tick(self):
        output = 1 if self.counter < self.compare else 0
        self.counter = 0 if self.counter == self.top else self.counter + 1
        return output
```

`period_seconds`, `frequency_hz` and `duty` are the formulas of the Concept section. `write_compare` clamps the value to `0..TOP + 1`, so you can ask for 0% and 100%.

### Step 2: The pin, tick by tick

`pin_waveform` calls `tick()` 256 times per period and multiplies by VDD. Its mean is exactly `D x VDD`, which is the definition of the average.

### Step 3: Into the RC filter, with the simulator

The simulator's pulse source has the same period and duty as our timer:

```python
def filter_pwm(timer, ohms, farads, t_stop, dt):
    circuit = Circuit()
    circuit.pulse_source("PWM", "pwm", "0", low=0.0, high=VDD, period=timer.period_seconds, duty=timer.duty)
    circuit.resistor("R1", "pwm", "out", ohms)
    circuit.capacitor("C1", "out", "0", farads, v0=0.0)
    result = circuit.transient(t_stop=t_stop, dt=dt)
    return np.asarray(result.time), np.asarray(result.v("out")), np.asarray(result.v("pwm"))
```

We simulate 80 ms (eight time constants) with 2 us steps, which puts 512 steps in each PWM period: plenty to resolve the edges.

### Step 4: Measure average and ripple

Over the last five periods, the mean of `out` is the average and `max - min` is the ripple. We print them next to the targets and the ripple formula.

Run it:

```
uv run python phases/17-microcontrollers/03-pwm/code/main.py
```

You will see the mean output within a few millivolts of `D x 5 V` for every compare value, and the measured ripple close to the predicted one (the formula is an approximation, so expect agreement within a few percent). The second table shows the trade-off: a 1 ms time constant ripples by over a volt, a 100 ms one ripples by a few millivolts but needs 300 ms to settle. The script also saves `pwm_rc.png` with the pin and the filtered output.

### What you should see

The first lines of the output (the script is deterministic, so your numbers should match these exactly):

```
Timer: 16 MHz clock / prescaler 64 / 256 counts
  PWM period = 1.024 ms, frequency = 976.56 Hz

The pin, tick by tick, for one period (compare = 64): first and last ticks of each level
  high for ticks 0..63, low for ticks 64..255
  average of the pin over the period = 1.2500 V  (duty 0.2500 x 5.0 V = 1.2500 V)

PWM into an RC low-pass: R = 10 kohm, C = 1 uF, tau = RC = 10 ms
  compare   duty target V mean out ripple p-p predicted
       32  0.125    0.625    0.624     57.2 mV    56.0 mV
       64  0.250    1.250    1.249     97.4 mV    96.0 mV
      128  0.500    2.500    2.499    128.2 mV   128.0 mV
      192  0.750    3.750    3.749     97.4 mV    96.0 mV

The filter trade-off at duty 0.5: small RC ripples, big RC is slow
      tau ripple p-p  time to 95% (3 tau)
      1 ms   1280.0 mV                3 ms
     10 ms    128.0 mV               30 ms
...
```

## Use It

- **Arduino `analogWrite(pin, value)`** sets a timer's compare register to `value` (0-255). On the Uno it gives about 490 Hz on most PWM pins and 976 Hz on pins 5 and 6. The name is misleading: nothing analog comes out of the pin.
- **LED dimming:** LED drivers and phone screens use PWM, usually at hundreds of hertz to tens of kilohertz. Too low a frequency gives visible flicker, especially when you move your eyes or a camera rolls its shutter.
- **Motors and fans:** PC fans take a 25 kHz PWM signal (above hearing, so it does not whine). Motor drivers (Phase 18, Lesson 05) switch the full motor current with PWM.
- **Servos** use PWM differently: a 50 Hz signal whose pulse width (1 to 2 ms) encodes the position.
- **Switching regulators** (Phase 18) are PWM plus an LC filter, at hundreds of kilohertz, with feedback adjusting the duty.
- **Cheap DAC:** PWM plus an RC (or a two-stage RC) is a common way to get a slow analog voltage, for example for a bias or a reference that changes rarely.

## Try It in the Lab

The lab gives you a 10 kohm and 1 uF filter and a slot for the PWM source. The PWM runs at 1 kHz between 0 and 5 V, and three sources with different duty cycles are available. You need the filtered output to sit between 1.1 V and 1.4 V after 60 ms. Work out which duty cycle gives that average, and check that the ripple from the formula is small enough to stay inside the window.

## Common Mistakes

- **Measuring PWM with a multimeter and trusting the reading.** A multimeter in DC mode averages roughly, so you may see D x VDD, but some meters get confused by fast edges. An oscilloscope (Phase 06, Lesson 06) shows what is really there.
- **Too low a PWM frequency.** At 50 Hz an LED flickers visibly and an RC filter needs a huge time constant.
- **Too high a frequency for the resolution.** At 16 MHz with no prescaler and 8 bits, the maximum is 62.5 kHz. Asking for 1 MHz leaves only 16 steps.
- **Forgetting the filter's speed.** A big RC removes ripple but makes the output slow to follow changes.
- **Loading the RC output.** Connect a 1 kohm load to a 10 kohm RC output and it becomes a divider: the average drops. Buffer it with an op-amp (Phase 13) or keep the load much larger than R.
- **Off-by-one in duty.** Different chips define duty as `compare / (TOP + 1)` or `(compare + 1) / (TOP + 1)`. Read the datasheet's formula.

## Exercises

1. A timer runs from 8 MHz with prescaler 8 and TOP = 999. What are the PWM frequency and the number of duty steps? (1 kHz and 1000 steps.)
2. With VDD = 3.3 V and 8-bit PWM, which compare value gives 2.0 V? What voltage do you actually get? (compare = 2.0 / 3.3 x 256 = 155.15, so 155, giving 1.998 V.)
3. Using the ripple formula, find the smallest C with R = 4.7 kohm so a 20 kHz, 3.3 V PWM at 50% has under 10 mV of ripple. (C >= 3.3 x 0.25 x 50 us / (4.7 kohm x 0.01 V) = 0.88 uF, so 1 uF.)
4. In `main.py`, change the prescaler to 8. What happens to the frequency and to the ripple? Check the simulated numbers against the formula.
5. Harder: an LED takes 10 mA when on. Your eye sees the average. With 8-bit PWM, what is the smallest non-zero average current, and why do LED dimmers often need 12 or 16 bits for smooth fades near darkness? (39 uA; perceived brightness is roughly logarithmic, so the low steps look like big jumps.)

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| PWM | "Analog output" | A digital signal of fixed period whose high time is controlled |
| Duty cycle | "The PWM value" | Fraction of each period the signal is high: D = t_high / T |
| PWM frequency | "Speed" | 1 / T = f_clock / (prescaler x (TOP + 1)) |
| Resolution | "Bits of PWM" | Number of distinct duty values; trades against frequency |
| Ripple | "Noise on the output" | The periodic wobble left after filtering, about VDD D (1 - D) T / RC |
| Average | "The voltage" | D x VDD, what a slow load or a low-pass filter responds to |

## Further Reading

- [ATmega328P datasheet (Microchip)](https://www.microchip.com/en-us/product/ATmega328P), chapters on Timer/Counter0 and Timer/Counter1, "Fast PWM mode"
- [Arduino documentation, "Secrets of Arduino PWM"](https://docs.arduino.cc/tutorials/generic/secrets-of-arduino-pwm/) — how `analogWrite` sets up the timers
- [All About Circuits, "Low-Pass Filter a PWM Signal into an Analog Voltage"](https://www.allaboutcircuits.com/technical-articles/low-pass-filter-a-pwm-signal-into-an-analog-voltage/) — filter choice and ripple
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed. — PWM in power and motor control contexts
