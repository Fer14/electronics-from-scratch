# Real Capacitors

> A real capacitor is an ideal capacitor wearing a disguise: a small resistor in series, a huge resistor across it, a little inductance, and a value that drifts with voltage, temperature and age.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 03 Lesson 06 (Tolerances and Ratings), Phase 07 Lessons 01-06
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Ideal capacitor | The perfect textbook part: exactly Q = C x V and nothing else | A frictionless spring |
| Model | A combination of ideal parts that behaves like the real part, close enough for a purpose | A cardboard mock-up that has the right size and weight |
| ESR (equivalent series resistance) | A small resistance in series with the capacitance, from leads, plates and the dielectric's losses | A narrow neck on a water bottle |
| Leakage current | A tiny current that flows through the dielectric even at steady voltage | A slow drip from a tank |
| Leakage resistance | The large resistance that models that leakage | The pinhole that causes the drip |
| ESL (equivalent series inductance) | A small inductance from the current path's loop, important at high frequency | The momentum of water in a long hose |
| Tolerance | How far the real value may be from the marked one, e.g. +/-20% | A recipe's "about a cup" |
| DC bias effect | The drop in capacitance of some ceramic capacitors when a DC voltage is applied | A sponge that holds less when squeezed |
| Temperature coefficient / class | How capacitance changes with temperature, coded like C0G, X7R, Y5V | How much a ruler expands in the sun |
| Polarized | A capacitor that must be connected one way round (+ to the higher voltage) | A one-way valve |
| Ripple current | The AC current a capacitor carries in a power supply; it heats the ESR | Waves sloshing in a tank, warming it a little each time |

## Learning Objectives

- Describe the main families of capacitors (ceramic, film, aluminium electrolytic, tantalum, supercapacitor) and what each is good for.
- Draw and use the standard model of a real capacitor: C with ESR and ESL in series and a leakage resistor across.
- Compute the instant voltage drop caused by ESR when a load current steps, and the heat ESR makes with ripple current.
- Estimate how long a capacitor holds its charge because of leakage.
- Account for tolerance and DC-bias derating when designing an RC time constant.
- Read the key lines of a capacitor datasheet.

## The Problem

You design a reset delay with 10 kOhm and a "10 uF" ceramic capacitor and expect tau = 100 ms. On the bench, running from 5 V, it is under 50 ms. You build a power supply with a big electrolytic and the output still dips sharply when the motor starts. You charge a capacitor to keep a clock alive and it is flat by the morning. You solder an electrolytic in backwards and it bulges.

Every one of these comes from the ways a real capacitor differs from Q = C x V. This lesson builds a model of a real capacitor out of ideal parts (a technique you will use for every component from now on), puts it into the simulator, and shows how big each effect is with real numbers.

## The Physics

### Where ESR comes from

The current reaching the plates passes through leads, thin metal films, the electrolyte (in electrolytics), and contact points. All of those have resistance. In addition, the dielectric's atoms do not polarize perfectly in step with the voltage; a little energy is lost as heat each time they flip, which looks electrically like extra series resistance. Together this is the **ESR**. It ranges from a few milliohms (good ceramics, polymer capacitors) to several ohms (small or old aluminium electrolytics, which also get worse when cold).

### Where leakage comes from

No insulator is perfect. A few charge carriers creep through the dielectric or along its surface. In aluminium electrolytics the oxide layer is only nanometres thick and constantly repaired by the electrolyte, so leakage is relatively large (microamps). Film and C0G ceramics leak extremely little (gigaohms and more).

### Where ESL comes from

Current flows in a loop: in one lead, through the plates, out the other lead. Any loop of current has inductance (Phase 08): it resists quick changes of current. A few nanohenries is typical. Below a few megahertz you can usually ignore it; above, it makes the capacitor stop behaving like a capacitor at all (Phase 10).

### Why ceramics lose capacitance under voltage

The high-eps_r ceramics (X5R, X7R, Y5V: "class II") are made of barium titanate, a ferroelectric material whose tiny electric domains do most of the polarizing. A strong DC field lines them up and "uses up" their ability to respond, so eps_r falls. A 10 uF, 6.3 V part in a small package can lose half or more of its capacitance at 5 V. Class I ceramics (C0G/NP0) and film capacitors do not do this.

### The model

```
          ESR        ESL
   a o---/\/\/---)))))----+----------+---o b
                          |          |
                         === C      R_leak
                          |          |
                          +----------+
```

A tiny resistor and inductor in series with an ideal capacitor that has a huge resistor across it. Each element is ideal and you already know how it behaves; together they behave like the real part. (In our code we leave out ESL, since our transient examples are slow enough for it not to matter.)

## The Concept

### The capacitor families

| Family | Typical range | Strengths | Weaknesses | Typical use |
|---|---|---|---|---|
| Ceramic class I (C0G/NP0) | 1 pF - 100 nF | Stable with temperature and voltage, very low loss | Small values only | Oscillators, filters, timing |
| Ceramic class II (X7R, X5R) | 1 nF - 100 uF | Tiny, cheap, very low ESR | Value drops with DC voltage and temperature, can "sing" | Decoupling next to every chip |
| Film (polyester, polypropylene) | 1 nF - 100 uF | Stable, low leakage, self-healing | Bigger | Audio, timing, mains filters |
| Aluminium electrolytic | 1 uF - 1 F | Big capacitance per volume and per cost | Polarized, high ESR and leakage, limited life (dries out) | Bulk smoothing in power supplies |
| Aluminium polymer | 10 uF - 2 mF | Very low ESR | Lower voltages, cost | Motherboard and GPU power |
| Tantalum | 0.1 uF - 1 mF | Compact, stable | Polarized, can fail short and burn if surged | Compact power rails |
| Supercapacitor (double layer) | 0.1 F - 3000 F | Enormous capacitance | Only about 2.7 V per cell, high ESR, leakage | Backup, energy buffering |

### ESR in numbers

A capacitor at 5 V suddenly supplies a load of 1 A. Two things happen:

1. **Instantly**, the 1 A flows through the ESR, and the output drops by I x ESR. With ESR = 0.1 Ohm: 0.1 V. With 1 Ohm: 1 V. The capacitor's own voltage has not changed yet; the drop is purely the series resistor.
2. **Over time**, the charge drains: the voltage slides down at I / C volts per second (Lesson 02). For 1000 uF: 1 A / 0.001 F = 1000 V/s = 1 V per millisecond.

So after 0.5 ms the output is 5 - I x ESR - 0.5 V. With a 1 Ohm ESR the instant drop is twice the slide. This is why power supply designers look at ESR first and capacitance second for fast load steps, and why they put low-ESR ceramics in parallel with electrolytics.

ESR also makes heat: a ripple current of I_rms through it dissipates P = I_rms^2 x ESR. 2 A of ripple through 0.1 Ohm is 0.4 W inside a small can. Heat dries out the electrolyte; electrolytic lifetime ratings (for example 2000 hours at 105 C) roughly double for every 10 C cooler they run.

### Leakage in numbers

A common rule in aluminium electrolytic datasheets gives the leakage after a few minutes at rated voltage as about I = 0.01 x C x V (C in uF, V in volts, result in uA), or 3 uA, whichever is larger. For 100 uF at 10 V: 0.01 x 100 x 10 = 10 uA. As a resistor: R_leak = 10 V / 10 uA = 1 MOhm.

The capacitor then discharges itself with tau = R_leak x C = 1 MOhm x 100 uF = 100 s. After a minute, 10 x e^(-60/100) = 5.5 V is left. A film capacitor with 10 GOhm of insulation resistance has tau = 10^6 s, about 12 days.

(Real leakage is not a perfect resistor: it is higher right after voltage is applied and falls as the oxide "re-forms", and it rises with temperature. A resistor is a first approximation.)

### Tolerance

Ceramic class II and electrolytics are often +/-20%, film +/-5 or 10%, C0G +/-1-5%. With a 1% resistor of 10 kOhm and a 10 uF +/-20% capacitor, tau can be anywhere from 0.99 x 0.8 x 100 ms = 79.2 ms to 1.01 x 1.2 x 100 ms = 121.2 ms. Electrolytics also lose capacitance as they age.

### DC bias derating

The capacitance of a class II ceramic at your working voltage is what matters, not the marked value. Manufacturers publish curves (and online tools) of capacitance versus DC voltage for each part number. The code uses an invented but realistic-looking curve to show the size of the effect: a 10 uF / 6.3 V part might keep about 90% at 1.8 V, 70% at 3.3 V, and under 50% at 5 V. Real curves depend heavily on package size and material; always check the specific part. Choosing a higher voltage rating or a larger package reduces the effect.

### Polarity and ratings

- Electrolytics and tantalums are polarized: reverse voltage destroys the oxide, causes heating, gas and sometimes a burst can (the vent scored into the top is there for that).
- Never exceed the rated voltage; designers typically use 50-80% of it (more margin for tantalum).
- Temperature range is part of the rating: a "105 C" electrolytic is rated to 105 C, but lasts much longer at 65 C.

### Worked example: picking a bulk capacitor for a load step

A 5 V rail must not drop more than 0.25 V when a motor driver suddenly draws 2 A for 0.2 ms before the regulator catches up.

1. Slide budget from capacitance: assume we split the budget evenly, 0.125 V for the charge drain. C = I x t / dV = 2 x 0.0002 / 0.125 = 3.2 mF.
2. ESR budget: the remaining 0.125 V for the instant drop. ESR = 0.125 / 2 = 62.5 mOhm or less.
3. A single 3300 uF general-purpose electrolytic might have 100-200 mOhm of ESR: the capacitance is fine but the ESR is not. Options: two or three in parallel (ESRs in parallel divide, capacitances add), a low-ESR polymer type, or a ceramic bank in parallel to take the fastest part of the step.

This kind of budget, splitting the allowed drop between I x ESR and I x t / C, is exactly how power designers size their capacitors.

### Ageing and temperature

- **Electrolytics** slowly dry out: capacitance falls and ESR rises over years, faster when hot. A common end-of-life definition in datasheets is capacitance down 20% or ESR doubled.
- **Class II ceramics** lose a few percent of capacitance per decade of time after manufacture ("ageing"), which the maker can reset by heating them above about 125 C (for example during soldering).
- **Temperature codes**: X7R means within +/-15% from -55 C to +125 C; X5R the same to +85 C; Y5V allows +22%/-82% from -30 C to +85 C, so a "10 uF" Y5V can be under 2 uF when cold or hot. C0G changes by at most 30 parts per million per degree.

### Reading a datasheet table

A typical general-purpose aluminium electrolytic series lists, for each part, numbers like these (illustrative values, not a specific product):

| Line | Example value | What it tells you |
|---|---|---|
| Capacitance | 470 uF +/-20% at 120 Hz | Measured at 120 Hz (the ripple frequency of rectified 60 Hz mains) |
| Rated voltage | 25 V DC | Never exceed; design for 80% or less |
| Surge voltage | 32 V | Short spikes it survives, not a working voltage |
| Leakage current | 0.01 CV or 3 uA, after 2 minutes | 0.01 x 470 x 25 = 118 uA worst case |
| Dissipation factor (tan delta) | 0.14 at 120 Hz | Loss ratio; ESR = tan delta / (2 pi f C) = 0.14 / (2 x 3.1416 x 120 x 470e-6) = 0.40 Ohm at 120 Hz |
| Impedance | 0.08 Ohm at 100 kHz, 20 C | Roughly the ESR at high frequency, where it is lowest |
| Ripple current | 1.0 A rms at 100 kHz, 105 C | The heating limit |
| Endurance | 2000 h at 105 C | Life at the maximum temperature; much longer when cooler |

The dissipation factor line uses ideas from Phase 09 (AC and impedance); for now, it is enough to know that it converts into an ESR.

### Why several small capacitors beat one big one

Two capacitors in parallel add their capacitance (Lesson 05), and their ESRs combine like resistors in parallel: two 0.1 Ohm ESRs give 0.05 Ohm. Ten 10 uF ceramics in parallel give 100 uF with an ESR ten times smaller than one part's, and also ten times less ESL, because ten small current loops side by side behave like inductors in parallel. That is why the area around a processor on a motherboard is carpeted with dozens of small capacitors rather than one large can.

Put differently: for fast load steps you buy **low ESR and low ESL**; for long dips you buy **capacitance**. A good design uses both kinds in parallel.

## Build It

```bash
uv run python phases/07-capacitors/07-real-capacitors/code/main.py
```

### Step 1: ESR and a load step

We model the capacitor as an ideal 1000 uF at 5 V plus an ESR resistor to the output node, and a current source that pulls 1 A from the output, starting at t = 0.

```python
def esr_step(esr_ohms, farads=1000e-6, start_volts=5.0, load_amps=1.0):
    circuit = Circuit()
    circuit.capacitor("C1", "inner", "0", farads, v0=start_volts)
    circuit.resistor("ESR", "inner", "out", esr_ohms)
    circuit.current_source("Iload", "out", "0", load_amps)
    result = circuit.transient(t_stop=0.5e-3, dt=1e-6)
    time = np.asarray(result.time)
    volts = np.asarray(result.v("out"))
    return float(np.interp(2e-6, time, volts)), float(volts[-1])
```

```
       ESR             C (ideal)
 out o--/\/\/--o inner---||---o 0
   |
 ( Iload 1 A )  pulls 1 A from out to ground
   |
   0
```

```
ESR: a 1000 uF capacitor at 5 V suddenly asked for 1 A
 ESR (ohm)  output right away (V)  after 0.5 ms (V)
      0.01                  4.988             4.490
      0.10                  4.898             4.400
      1.00                  3.998             3.500
  The instant drop is I * ESR; the slow slide is I * t / C = 0.5 V in 0.5 ms
```

"Right away" is 2 us after the step, so the capacitor has already lost 2 mV on top of the I x ESR drop.

### Step 2: Leakage

The capacitor alone, with a leakage resistor across it:

```python
def leakage_after(leak_ohms, farads=100e-6, start_volts=10.0, seconds=60.0):
    circuit = Circuit()
    circuit.capacitor("C1", "top", "0", farads, v0=start_volts)
    circuit.resistor("Rleak", "top", "0", leak_ohms)
    result = circuit.transient(t_stop=seconds, dt=seconds / 2000)
    return float(np.asarray(result.v("top"))[-1])
```

```
Leakage: a 100 uF capacitor charged to 10 V and left alone for 60 s
  aluminium electrolytic (0.01*C*V rule)   R_leak =  1.00e+06 ohm -> 5.488 V
  good electrolytic (0.5 uA)               R_leak =  2.00e+07 ohm -> 9.704 V
  film capacitor (about 10 GOhm)           R_leak =  1.00e+10 ohm -> 9.999 V
```

The first line is the datasheet's worst-case limit; a good part at room temperature usually leaks much less, as the second line shows.

### Step 3: DC bias

```python
def ceramic_dc_bias(nominal_farads, applied_volts, rated_volts):
    fraction_of_rating = applied_volts / rated_volts
    return nominal_farads * max(0.2, 1 - 0.75 * fraction_of_rating ** 1.5)
```

This curve is a made-up stand-in with a realistic shape, not data for any real part.

```
Class II ceramic (X5R/X7R) loses capacitance under DC voltage (illustrative curve)
  10 uF / 6.3 V part at 0.0 V behaves like 10.00 uF
  10 uF / 6.3 V part at 1.8 V behaves like  8.85 uF
  10 uF / 6.3 V part at 3.3 V behaves like  7.16 uF
  10 uF / 6.3 V part at 5.0 V behaves like  4.70 uF
```

Back to the opening puzzle: near 5 V, 10 kOhm with this "10 uF" behaves like tau of about 47 ms, not 100 ms. (The full story is a little more complicated: while the capacitor charges its voltage changes, so its capacitance changes along the way. The capacitor is larger at the start of charging and smaller near the end.)

### Step 4: Tolerance

```
Tolerance: tau = 10 kOhm (1%) * 10 uF (+/-20%)
  smallest  tau =   79.2 ms
  nominal   tau =  100.0 ms
  largest   tau =  121.2 ms
```

## Use It

- **Datasheet lines to look for.** For an aluminium electrolytic (for example Panasonic FR or Nichicon UHE series): capacitance and tolerance, rated voltage, ESR or impedance at 100 kHz, rated ripple current, leakage current formula, and endurance (hours at 105 C). For a ceramic (Murata GRM, TDK C series, Samsung CL): dielectric class (C0G, X7R, X5R), rated voltage, package size, and the DC-bias curve from the maker's online tool (Murata SimSurfing, TDK SEAT, KEMET K-SIM).
- **Decoupling.** Designers place a 100 nF X7R right at each chip's power pin (low ESR, low ESL because it is tiny and close) and a bulk electrolytic or polymer capacitor further away. Each covers a different range of speeds.
- **Timing and filters.** Use C0G or film for anything whose value must be accurate: oscillators, 555 timers, audio filters. Class II ceramics drift too much with voltage and temperature.
- **Failures.** Dried-out electrolytics with high ESR are one of the most common causes of dead power supplies and monitors. A capacitor ESR meter is a standard repair tool; a bulged top is the visual clue.
- **Microphonics.** Class II ceramics are slightly piezoelectric: they change size with voltage, so in audio or switching circuits they can audibly whine, and they can turn board vibration into electrical noise.

## Common Mistakes

- **Trusting the marked value of a ceramic.** Check the DC-bias curve at your working voltage; a 10 uF part may act like 4 uF.
- **Using an electrolytic for timing.** +/-20% tolerance, leakage and ageing make the timing poor. Use film or C0G with a larger resistor.
- **Ignoring ESR in power circuits.** A large capacitance with high ESR cannot hold a rail steady during a fast load step; the instant I x ESR drop comes first.
- **Reversing a polarized capacitor.** Electrolytics and tantalums can overheat, vent or explode. Check the stripe (negative) or the + mark.
- **Running at the rated voltage.** Leave margin, especially for tantalum and for anything hot.
- **Expecting a capacitor to hold charge for days.** Leakage empties electrolytics in minutes to hours.
- **Forgetting the temperature.** An electrolytic's ESR can rise several times in the cold, and every capacitor's life shortens in the heat. Check the conditions under which each datasheet number was measured.
- **Using the 120 Hz capacitance at high frequency.** At hundreds of kilohertz an electrolytic's behaviour is dominated by ESR and ESL, not by its capacitance. That is a Phase 10 topic, but it is why the datasheet gives impedance at 100 kHz.
- **Mixing up surge and rated voltage.** The surge voltage is a brief limit for spikes, not a working voltage.

## Exercises

1. A 470 uF electrolytic with 0.2 Ohm ESR supplies a 2 A step from 12 V. What is the instant drop? How far does the voltage slide in the next 1 ms?
2. The same capacitor carries 1.5 A rms of ripple current. How much heat does the ESR make?
3. Using the 0.01 x C x V rule, what leakage current and leakage resistance would you expect for a 1000 uF, 16 V electrolytic at 16 V? What is its self-discharge time constant?
4. You need tau = 50 ms +/- 5%. You have 1% resistors and capacitors in three kinds: electrolytic +/-20%, film +/-5%, C0G +/-2% (C0G only up to 100 nF). Which combination can meet the spec? Pick values.
5. Add ESL to your mental model: in Phase 08 you will learn that an inductor's voltage is L x di/dt. If a decoupling capacitor has 1 nH of ESL and the chip's current changes by 1 A in 1 ns, what voltage spike appears across the ESL? What does that suggest about using several small capacitors close to the chip?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| ESR | "The cap's resistance" | Series resistance from leads, plates, electrolyte and dielectric loss; causes instant I x ESR drops and heat |
| ESL | "Parasitic inductance" | Series inductance of the current loop; dominates at high frequency |
| Leakage current | "It discharges itself" | Small DC current through the dielectric, modelled as a large parallel resistance |
| DC bias derating | "Ceramics lie" | Class II ceramics lose capacitance as DC voltage rises |
| X7R / C0G | "Ceramic types" | Codes for temperature behaviour; C0G is stable, X7R allows about +/-15% over -55 to 125 C |
| Ripple current rating | "How much AC it can take" | The rms current the capacitor survives without overheating through its ESR |
| Polarized | "Has a + and -" | Must be biased one way; reversing it damages the dielectric |

## Further Reading

- [Murata: Capacitor basics and DC bias characteristics](https://article.murata.com/en-global/article/basics-of-capacitors-1) - how MLCCs are built and why they lose capacitance with voltage.
- [KEMET / TDK / Murata online capacitor simulation tools (K-SIM, SEAT, SimSurfing)](https://ksim3.kemet.com/) - real curves for real part numbers.
- *The Art of Electronics*, 3rd ed., Horowitz & Hill, and *The Art of Electronics: The x-Chapters*, sections on capacitor types and their non-idealities.
- [Analog Devices tutorial MT-101, "Decoupling Techniques"](https://www.analog.com/media/en/training-seminars/tutorials/MT-101.pdf) - ESR, ESL and decoupling practice.
