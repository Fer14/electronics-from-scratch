# Rectifiers

> The wall gives you a current that sloshes back and forth fifty times a second. A diode only lets the forward half through; a capacitor fills up on each push and feeds the load in between. That is the first half of every power supply.

**Type:** Build
**Prerequisites:** 11-04 (The Diode Equation); Phase 07 (Capacitors), lessons 03-charging-and-discharging and 04-the-time-constant; Phase 09 (Alternating Current), lessons 02-sine-waves-frequency-and-phase and 03-rms-values
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| AC (alternating current) | Current that keeps reversing direction, usually following a sine wave | A saw cutting wood: push, pull, push, pull |
| DC (direct current) | Current that always flows the same way, ideally at a steady value | A river flowing downhill |
| Rectifier | A circuit that turns AC into current that flows only one way | A ratchet wrench: you swing back and forth, the bolt only turns one way |
| Half-wave rectifier | One diode: keeps the positive halves of the wave, blocks the negative halves | A door that opens only when pushed from one side |
| Full-wave rectifier | Keeps both halves, flipping the negative half to positive | A ratchet that turns the bolt on both the push and the pull |
| Bridge rectifier | Four diodes arranged so the load always sees the same polarity | A roundabout where every entrance leads to the same exit |
| Reservoir (smoothing) capacitor | A big capacitor after the rectifier that stores charge at each peak and releases it between peaks | A water tower: filled by pump strokes, gives steady pressure |
| Ripple | The leftover up-and-down wobble on the DC output | Small waves on a lake that is otherwise flat |
| Peak voltage | The highest value of a waveform | The crest of a wave |
| Conduction angle | The fraction of each cycle during which the diode actually conducts | The short moment a pump stroke actually pushes water into the tower |
| Surge (inrush) current | The large current that flows when an empty capacitor is first charged | The rush of water into an empty pipe when you open the tap |
| PIV (peak inverse voltage) | The largest reverse voltage a diode sees in a circuit | The highest wave that will hit a sea wall |
| Transformer | A part that changes AC voltage up or down (Phase 08) | A gearbox for voltage |

## Learning Objectives

- Explain how one diode turns a sine wave into positive half-waves.
- Explain how four diodes in a bridge flip the negative half too.
- Explain how a reservoir capacitor turns bumps into nearly steady DC, and estimate the ripple with ΔV ≈ I / (f × C).
- Recognise that diodes conduct in short, intense pulses, and why that matters for choosing parts.
- Simulate half-wave and full-wave rectifiers with and without capacitors.

## The Problem

Your laptop, your phone charger, your television, every LED bulb: all run on DC inside, and all plug into AC. In Europe the socket gives a sine wave of 230 V RMS (about 325 V peak) at 50 Hz; in North America 120 V RMS at 60 Hz. Before any of that energy can feed a chip, something must stop the current from reversing direction 100 times a second.

That something is a rectifier, and after this phase's diode lessons you already have everything needed to build one. But a bare rectifier gives you bumps, not DC. A chip powered by bumps would reset 100 times a second. We need to fill the gaps between bumps, and the right tool is a capacitor. Choosing how big a capacitor, and what the diodes must survive, is the bread and butter of power-supply design. Here we work with a safe, low voltage: a 12 V peak sine, as a small transformer would give.

## The Physics

A diode, from lesson 04, conducts when its anode is about 0.7 V more positive than its cathode, and blocks otherwise. A capacitor, from Phase 07, stores charge: Q = C × V. It cannot change its voltage instantly; to change its voltage by ΔV in a time Δt it needs a current I = C × ΔV / Δt. Read it backwards and you get the key fact for this lesson: **if a capacitor alone feeds a current I for a time Δt, its voltage drops by ΔV = I × Δt / C.**

Put those two together:

1. While the input rises above the capacitor voltage (plus the diode's 0.7 V), the diode conducts and the source tops up the capacitor.
2. After the peak, the input falls faster than the capacitor can discharge. The diode's anode becomes more negative than its cathode: it switches off. The capacitor alone feeds the load and slowly droops.
3. On the next peak the input catches up with the drooping capacitor, the diode turns on briefly, and the cycle repeats.

What the water analogy gets right and wrong: a water tower filled by a pump stroke and drained by a town is an excellent picture of steps 1-3. What it gets wrong: the pump here is a sine wave that also goes *negative*, which a water pump never does; the diode is what stops the tower from being sucked empty on the down stroke.

## The Concept

### The half-wave rectifier

```
             D1
   ~ AC ----|>|----+---- out
   12 V            |
   peak           [RL] 1 kΩ
                   |
   ground ---------+
```

During the positive half of the sine, D1 is forward biased and the output follows the input minus one diode drop. During the negative half, D1 is reverse biased and the output sits at 0 V (the load pulls it there).

```
 input:   /\      /\      /\             output:  /\      /\      /\
         /  \    /  \    /  \                    /  \    /  \    /  \
 -------/----\--/----\--/----\---        -------/    \__/    \__/    \__
              \/      \/                        (negative halves removed)
```

The simulator, with a 12 V-peak 50 Hz input and a 1 kΩ load, gives a peak output of **11.28 V** (12 V minus the diode's 0.72 V at 11 mA) and an average of **3.47 V**.

Check the average by hand: a half sine of peak V_p averages V_p / π over a full cycle (a standard result: the area under one sine bump is 2 V_p / ω, spread over one period). 11.28 / π = 3.59 V. The simulator's slightly lower 3.47 V comes from the diode's drop being *bigger than zero at every instant* it conducts, and from the diode not conducting at all while the input is below about 0.5 V. Sanity checks like this are worth doing on every simulation.

### The reverse voltage the diode must survive

During the negative peak, the cathode sits at the output (0 V without a capacitor) and the anode at −12 V: the diode sees 12 V reverse. **With** a reservoir capacitor holding the output near +11 V, the diode sees nearly 11 + 12 = 23 V in reverse: twice the peak. That is the **peak inverse voltage** (PIV), and the diode's reverse rating must exceed it with margin. The 1N4001 (50 V) would be fine here; at mains voltages you would choose a 1N4007 (1000 V).

### Adding the reservoir capacitor

```
             D1
   ~ AC ----|>|----+--------+---- out
   12 V            |        |
                  === C    [RL] 1 kΩ
                   |        |
   ground ---------+--------+
```

Now the output charges to the peak (about 11.3 V) and then droops between peaks as the capacitor alone feeds the 1 kΩ load:

```
  11.3 V  ._       ._       ._
          | `--._  | `--._  | `--._      <- droop: capacitor feeding the load
          |      `-|      `-|      `-
          |  ^ diode conducts only during these short rising edges
```

**Estimating the ripple.** The load current is about (11.25 V) / 1000 Ω = 11.25 mA. Between peaks the capacitor feeds it alone for almost a whole period, 1/f = 20 ms. Using ΔV = I × Δt / C:

```
ΔV ≈ I / (f × C)
```

Read: "the ripple is about the load current divided by the frequency of the bumps times the capacitance".

For C = 470 µF:

```
ΔV ≈ 0.01125 A / (50 Hz × 470e-6 F) = 0.01125 / 0.0235 = 0.479 V
```

For C = 100 µF: 0.01125 / (50 × 100e-6) = 2.25 V.

The simulator measures **0.440 V** and **1.851 V**. The estimate is always a bit pessimistic, for two reasons: the capacitor does not droop for the full 20 ms (the diode starts conducting again a few milliseconds before the peak), and as the voltage droops the load current shrinks a little. A pessimistic estimate is exactly what a designer wants: if you size the capacitor for 0.48 V you get 0.44 V.

**When is the estimate valid?** When the ripple is small compared to the output voltage, which is the same as saying that the time constant R_L × C is much longer than a period. For 1 kΩ and 470 µF, τ = 0.47 s, 23 periods: fine. For 10 µF, τ = 10 ms, half a period: the capacitor nearly empties between peaks and the formula (which would predict 22.5 V of ripple, more than the output itself) is meaningless.

### The diode works in short, violent pulses

This is the surprise of the lesson. Look at the simulator's peak diode currents:

| Circuit | Average load current | Peak diode current |
|---|---|---|
| half-wave, no capacitor | about 3.5 mA | 11.3 mA |
| half-wave, 100 µF | about 10 mA | 202 mA |
| half-wave, 470 µF | about 11 mA | 406 mA |

With the capacitor, all the charge the load uses in a whole cycle must be put back during the short time the diode conducts, just before each peak. The bigger the capacitor, the smaller the ripple, the shorter that window, and the more intense the pulse. With 470 µF, a 11 mA load causes **400 mA pulses**: 36 times the average.

Consequences in real designs:

- the diodes must be rated for the repetitive peak current, not only the average;
- the transformer and wiring see these pulses, which heat them more than a smooth current would (power goes as I², and I² of a pulse is large);
- the pulses are rich in harmonics (Phase 10), which is why power companies limit how much "pulsy" current an appliance may draw and why modern supplies add *power factor correction*.

And the very first charge of an empty capacitor, when you plug in, can draw a single large **inrush** surge. Some supplies add a thermistor or resistor in series to soften it.

### The full-wave bridge

Half-wave wastes half the cycles and gives bumps at 50 per second. A **bridge** of four diodes uses both halves:

```
                 ac1
               /     \
          D3 ▲         ▼ D1         D1: ac1 -> out    D3: gnd -> ac1
            /           \           D2: ac2 -> out    D4: gnd -> ac2
   gnd ----+             +---- out
            \           /
          D4 ▲         ▼ D2
               \     /
                 ac2

   AC source between ac1 and ac2; load and capacitor between out and gnd.
```

- When ac1 is positive relative to ac2: current flows ac1 → D1 → out → load → gnd → D4 → ac2.
- When ac2 is positive: ac2 → D2 → out → load → gnd → D3 → ac1.

Either way, current enters the load from the `out` side. The output gets a bump on **every** half-cycle: 100 bumps per second at 50 Hz. Two consequences:

1. The current always passes through **two** diodes, so the peak output is about 12 − 2 × 0.72 = 10.6 V. The simulator: **10.57 V** without a capacitor.
2. The capacitor only has to bridge half a period (10 ms), so the ripple halves: ΔV ≈ I / (2 f C).

Simulated full-wave results: 100 µF gives **0.846 V** of ripple (estimate with the actual 10.5 mA load current: 0.0105/(100 × 100 × 10⁻⁶) = 1.05 V), and 470 µF gives **0.194 V** (estimate 0.22 V). Peak diode currents are lower too (187 mA instead of 406 mA for 470 µF), because each diode pair recharges half as much charge, more often.

You can buy the four diodes in one package: a "bridge rectifier" with four pins marked ~, ~, + and −.

### Summary of the simulation

| Circuit | Peak | Min | Ripple | Average |
|---|---|---|---|---|
| half-wave, no capacitor | 11.28 V | 0.00 V | 11.28 V | 3.47 V |
| half-wave, 100 µF | 11.27 V | 9.42 V | 1.851 V | 10.35 V |
| half-wave, 470 µF | 11.25 V | 10.81 V | 0.440 V | 11.03 V |
| bridge, no capacitor | 10.57 V | 0.00 V | 10.57 V | 6.29 V |
| bridge, 100 µF | 10.54 V | 9.69 V | 0.846 V | 10.13 V |
| bridge, 470 µF | 10.48 V | 10.29 V | 0.194 V | 10.39 V |

The bridge without a capacitor averages 6.29 V, close to the expected 2 × 10.57 / π = 6.73 V minus the diode-drop effects. Open `code/out.png` to see four of these waveforms.

## Build It

### Step 1: A half-wave rectifier in the simulator

```python
def half_wave(capacitance):
    circuit = Circuit()
    circuit.sine_source("V1", "ac", "0", amplitude=PEAK_VOLTS, freq=FREQUENCY, offset=0.0)
    circuit.diode("D1", "ac", "out")
    circuit.resistor("RL", "out", "0", LOAD_OHMS)
    if capacitance:
        circuit.capacitor("C1", "out", "0", capacitance, v0=0.0)
    return circuit.transient(t_stop=STOP_TIME, dt=TIME_STEP)
```

We simulate 100 ms (five cycles) with a 20 µs step, which gives 1000 points per cycle: enough to resolve the short charging pulses. The capacitor starts empty (`v0=0.0`), so the first cycle shows the inrush.

### Step 2: The bridge

```python
circuit.sine_source("V1", "ac1", "ac2", amplitude=PEAK_VOLTS, freq=FREQUENCY, offset=0.0)
circuit.diode("D1", "ac1", "out")
circuit.diode("D2", "ac2", "out")
circuit.diode("D3", "0", "ac1")
circuit.diode("D4", "0", "ac2")
```

The source is connected between `ac1` and `ac2`, neither of which is ground: exactly like a transformer's secondary winding, which "floats".

### Step 3: Measure the last cycle

```python
def last_cycle(time, values):
    window = time >= STOP_TIME - 1.0 / FREQUENCY
    return values[window]
```

We only look at the final 20 ms, after the start-up surge has passed, and report the peak, minimum, ripple (peak minus minimum), average and the largest diode current.

### Step 4: Compare with the estimate

`show_estimates` prints I / (f C) and I / (2 f C) for 100 µF and 470 µF, so you can compare them with the simulated ripple line by line.

```
uv run python phases/11-semiconductors-and-diodes/06-rectifiers/code/main.py
```

## Use It

- **Old-style "wall warts"**: a heavy transformer, a bridge (e.g. a DB107 or a W04 package), a reservoir capacitor of 1000-4700 µF, often followed by a linear regulator such as a 7805 (Phase 18) that removes the remaining ripple. If you open one and see a big electrolytic capacitor next to four diodes, you are looking at this lesson.
- **Modern switching chargers** rectify the mains *directly* (a bridge and a 400 V capacitor charged to about 325 V), then chop that DC at tens of kHz to drive a tiny transformer (Phase 18). The rectifier is the same idea at higher voltage: the capacitor must be rated for 400 V and the bridge for 600-1000 V.
- **Choosing the capacitor in practice**: designers often allow 10 % ripple. For a 1 A load at 12 V with a 50 Hz bridge: C = I / (2 f ΔV) = 1 / (100 × 1.2) = 8300 µF. The capacitor's *ripple current rating* (on its datasheet) must also handle the charging pulses.
- **Datasheet numbers that matter**: for a 1N4001-1N4007: average forward current 1 A, non-repetitive surge 30 A for one half cycle (the inrush), reverse voltage 50-1000 V. For bridges like the GBU4 series: 4 A average, 150 A surge.
- **Signal rectifiers**: AM radio detectors and audio level meters use a small diode and capacitor to follow the peaks of a signal: the same circuit, used to measure instead of to power.

## Try It in the Lab

The lab gives you a 12 V-peak, 50 Hz source, one diode and a 1 kΩ load. One slot is empty: the reservoir capacitor. Pick the capacitor so the output ripple stays below 0.6 V and the output is still high just before the next peak.

Things to think about: what current does the load draw? How long must the capacitor carry it alone? Which capacitor value does ΔV ≈ I / (f C) suggest, and is the estimate optimistic or pessimistic? After you pass, try the smaller capacitors and watch how the output collapses between bumps.

## Common Mistakes

- **Forgetting the diode drops.** A half-wave rectifier loses one diode drop (about 0.7 V), a bridge loses two. With a 5 V transformer, a bridge leaves only about 3.6 V.
- **Confusing RMS and peak.** A transformer labelled "9 V" means 9 V RMS: the peak is 9 × 1.414 = 12.7 V, and the capacitor charges to the peak (minus diode drops). An "unloaded" supply is often much higher than its label.
- **Sizing diodes for the average current.** The repetitive peak current can be 10-40 times the average. Check the peak and surge ratings.
- **Underrating the capacitor's voltage.** It charges to the peak. A 16 V capacitor on a "12 V" transformer is at risk; a 25 V one is the safe choice. Electrolytic capacitors installed backwards can burst.
- **Ignoring PIV in half-wave circuits with a capacitor.** The diode sees about twice the peak voltage in reverse.
- **Measuring ripple with the meter on DC.** A DC voltmeter shows the average; ripple needs the AC range or, better, an oscilloscope (Phase 06).
- **Working on mains-powered circuits.** Do not. Everything in this lesson can be learned at 12 V. The mains can kill (Phase 00, Lesson 08).

## Exercises

1. A half-wave rectifier is fed by a 15 V-peak, 50 Hz source and drives a 500 Ω load. Estimate the DC output and ripple with C = 1000 µF.
2. The same circuit as a bridge at 60 Hz: what changes, and by how much?
3. You need at most 0.5 V of ripple on a 12 V output that supplies 200 mA, with a 50 Hz bridge. What capacitance? Pick the next standard value (E6 series: 1000, 1500, 2200, 3300, 4700, 6800 µF).
4. Change `LOAD_OHMS` in the script to 100 Ω with C = 470 µF (half-wave). Compare the ripple with the estimate. Why does the estimate get worse as the ripple grows?
5. A 9 V RMS transformer feeds a bridge and a capacitor with no load attached. What voltage does the capacitor reach? What reverse voltage does each diode see?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Rectifier | "The diodes" | A circuit that makes current flow one way only |
| Half-wave | "One-diode rectifier" | Passes one polarity of the input; bumps at the line frequency f |
| Bridge | "Full-wave" | Four diodes that steer both polarities to the same output; bumps at 2f, two diode drops |
| Reservoir capacitor | "Smoothing cap", "filter cap" | Stores charge at each peak and supplies the load between peaks |
| Ripple | "Hum" (in audio) | Peak-to-peak variation left on the output; ΔV ≈ I/(fC) half-wave, I/(2fC) full-wave |
| PIV | "Reverse rating" | Maximum reverse voltage across a diode during operation; about 2 V_peak for a half-wave with capacitor |
| Inrush | "Turn-on surge" | The large current that charges the empty capacitor at power-up |

## Further Reading

- *All About Circuits*, Volume III, chapter 3, "Rectifier circuits". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-3/rectifier-circuits/
- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., section 1.6.2-1.6.4 (rectification, power-supply filtering) and chapter 9 (power supplies).
- C. Platt, *Make: Electronics*, and P. Scherz and S. Monk, *Practical Electronics for Inventors*, 4th ed., section on power supplies: hands-on treatment of transformer-bridge-capacitor supplies.
- Vishay, 1N4001-1N4007 datasheet: average current, surge current and reverse ratings. https://www.vishay.com/docs/88503/1n4001.pdf
