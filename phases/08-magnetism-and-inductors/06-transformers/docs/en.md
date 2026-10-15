# Transformers

> Two coils sharing one magnetic core trade voltage for current: wind ten times fewer turns and you get a tenth of the voltage and ten times the current, with almost no power lost.

**Type:** Learn
**Prerequisites:** Phase 08 (Magnetism and Inductors), Lessons 03 (Faraday's Law and Induction) and 04 (The Inductor); Phase 05 (Circuit Analysis and Our Simulator), Lesson 08 (Dependent Sources)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Transformer | Two (or more) coils wound on a shared core, passing energy from one to the other through a changing magnetic field | The heavy block inside an old phone charger or a doorbell |
| Primary | The coil you drive (the input side) | The pedal side of a bicycle's gears |
| Secondary | The coil that delivers power to the load (the output side) | The wheel side of the gears |
| Turns ratio (n) | Primary turns divided by secondary turns | The gear ratio |
| Step-down / step-up | A transformer that lowers / raises the voltage | Low gear / high gear |
| Mutual inductance (M) | How much a change of current in one coil induces a voltage in the other, in henries | How strongly two gears are meshed |
| Coupling coefficient (k) | The fraction of one coil's flux that also passes through the other, between 0 and 1 | 1 = perfectly meshed gears, 0 = not touching |
| Magnetizing current | The small current the primary draws just to keep the core's field going, even with no load | The effort to spin the gears with nothing attached |
| Reflected impedance | How a load on the secondary looks from the primary side: n² times bigger | A heavy bike feels lighter in a low gear |
| Isolation | No wire connects primary and secondary; only the magnetic field does | Talking through a closed window by sign language |
| Laminations | Thin insulated steel sheets stacked to make a core, to stop eddy currents | A ream of paper instead of a solid block of wood |

## Learning Objectives

- Explain how a changing current in one coil induces a voltage in another coil on the same core
- Use the turns ratio to calculate secondary voltage and current, and check power conservation
- Calculate how a load is "reflected" to the primary as n² times its resistance
- Simulate two coupled coils from their equations and compare with an equivalent circuit in our simulator
- Describe why transformers need AC, why cores are laminated, and where the losses go

## The Problem

The electricity grid generates power at around 10 to 25 kV, sends it across the country at 110 to 400 kV, distributes it through town at 10 to 20 kV, and delivers it to your home at 230 V (120 V in North America). Your laptop needs 20 V; the chips inside it need about 1 V. Something has to change voltages, efficiently, at every step.

For mains AC, that something has been the **transformer** for 140 years. It has no moving parts, it can be 99 % efficient for big units, it can handle megawatts, and it gives **isolation**: the low-voltage side is not wired to the dangerous high-voltage side at all, so touching your phone charger's cable does not put mains voltage through you. Even modern switching power supplies (the small, light chargers) still contain a transformer; they just run it at much higher frequencies so it can be tiny.

To understand any of this you need one idea from Lesson 03 applied twice.

## The Physics

### Two coils, one flux

Wind two coils on the same iron ring, like Faraday's 1831 experiment (Lesson 03):

```
          core (iron ring or rectangle)
       +---------------------------+
       |    ->  flux Phi  ->       |
   +---+===+                   +===+---+
   |   |   |  primary          |   |   |  secondary
 V_p   |   |  N_p turns        |   |   |  N_s turns      V_s
   |   |   |                   |   |   |
   +---+===+                   +===+---+
       |    <-  flux Phi  <-       |
       +---------------------------+
```

Drive the primary with an alternating voltage. The primary current makes a changing magnetic field, which the iron core channels almost entirely through the secondary too. Now both coils see **the same changing flux Phi**. Faraday's law, applied to each coil:

```
V_p = N_p * dPhi/dt          V_s = N_s * dPhi/dt
```

The rate of change dPhi/dt is the same for both, because it is the same flux. Divide one equation by the other and it cancels:

```
V_s / V_p = N_s / N_p
```

**The voltage per turn is the same on both coils.** Read it: "the secondary voltage over the primary voltage equals the secondary turns over the primary turns". A coil with a tenth of the turns gets a tenth of the voltage.

**Worked example.** A primary of 1000 turns connected to a sine of 325 V peak (this is European mains, called "230 V" for reasons Phase 09 explains), and a secondary of 100 turns: V_s = 325 x 100 / 1000 = 32.5 V peak.

### The turns ratio

We write n = N_p / N_s. A **step-down** transformer has n > 1, a **step-up** transformer n < 1. To get 12 V from 230 V with 1000 primary turns: N_s = 1000 x 12 / 230 = 52.2 turns, so about 52.

### Power in equals power out

An ideal transformer has no resistance and no losses: it cannot make energy, and it does not use any. So the power delivered by the secondary equals the power taken by the primary:

```
V_p * I_p = V_s * I_s
```

Since V_s is n times smaller, I_s must be n times bigger:

```
I_s / I_p = N_p / N_s = n
```

**Worked example.** A 12 V load drawing 2 A takes 24 W. With the 230 to 12 V transformer (n = 230 / 12 = 19.17), the primary current is 2 / 19.17 = 0.104 A = 104 mA, and 230 x 0.104 = 24 W. Thin wire is enough for the primary; the secondary needs thick wire.

This is exactly like bicycle gears: a low gear turns a lot of pedalling force at slow speed into less force at higher speed (or the other way round), but the power (force times speed) stays the same. A transformer trades voltage for current.

### Why a transformer needs AC

Faraday's law needs a **changing** flux. Connect a battery to the primary and, after the first instant, the current is steady, the flux is steady, and the secondary produces nothing. Worse, the primary is an inductor: at DC it is just its wire resistance (Lesson 04), so a big current flows, heating the coil and saturating the core. **Never connect a transformer's primary to DC.** Transformers work with alternating current, which is the main reason the grid uses AC (Phase 09, Lesson 01).

### Mutual inductance and coupling

In Lesson 04 the inductance L described how a coil's *own* current induces a voltage in *itself*. With two coils there is a second quantity, the **mutual inductance M**: the voltage induced in one coil per unit rate of change of current in the other.

```
v_1 = L_1 * di_1/dt + M * di_2/dt
v_2 = M * di_1/dt + L_2 * di_2/dt
```

Read the first line: "the primary voltage is its own inductance times its own current's rate of change, plus the mutual inductance times the secondary current's rate of change". These two equations are the complete description of two coupled coils, and the code simulates them directly.

How big is M? If every field line of one coil passes through the other, M = sqrt(L_1 x L_2). In practice some flux "leaks" around, and we write

```
M = k * sqrt(L_1 * L_2)
```

with the **coupling coefficient** k between 0 and 1. Iron-core power transformers reach k = 0.99 or more. Two coils on the same rod with a gap might have 0.5. Two air coils a few centimetres apart (a wireless charger) might have 0.2 to 0.7.

Since inductance goes with N² (Lesson 04), the turns ratio is the square root of the inductance ratio: n = sqrt(L_1 / L_2). A 10:1 transformer has L_1 = 100 x L_2.

### The magnetizing current

Even with nothing connected to the secondary, the primary is still an inductor across the AC source, and it draws a small current to keep the core's field changing. This is the **magnetizing current**. It is why a transformer plugged in with no load is slightly warm, and why old chargers wasted power while plugged in. A good transformer has a large primary inductance so that this current is small.

### Reflected impedance: how the load looks from the primary

From the primary side, what does a load resistor R_L on the secondary look like? The primary voltage is V_p = n V_s, and the primary current is I_p = I_s / n. So

```
V_p / I_p = (n V_s) / (I_s / n) = n^2 * (V_s / I_s) = n^2 * R_L
```

**A load seen through a transformer looks n² times bigger.** (Or n² times smaller from the other side.) An 8 ohm loudspeaker on a 10:1 transformer looks like 800 ohm to the amplifier on the primary. This was how valve (tube) amplifiers, which like high-resistance loads, drove low-resistance speakers. It is also how radio engineers match antennas to amplifiers (Phase 05, Lesson 07: maximum power transfer needs matched resistances).

## The Concept

### An equivalent circuit you can simulate

Our simulator does not have a "transformer" part, but we can build one out of parts it does have. A near-ideal transformer with primary inductance L_1 behaves like this:

```
   Vs ---[Rs]---+-------+                    +------+
                |       |                    |      |
               Lm   n^2 R_L         E1: V_out = V_p / n    R_L
               (L1)     |                    |      |
                |       |                    |      |
   0 V ---------+-------+--------------------+------+
                p (primary node)               out
```

- **Lm** (the magnetizing inductance, equal to L_1) carries the magnetizing current.
- **n² R_L** is the load reflected to the primary: it carries the primary current that feeds the load.
- **E1** is a voltage-controlled voltage source (Phase 05, Lesson 08) with gain 1/n: it makes the secondary voltage exactly V_p / n. It drives the actual load R_L.

This is a standard engineering trick: split a component into simple ideal pieces, each with one job.

### Worked example for the simulation

Our test transformer: L_1 = 10 H, ratio 10:1 (so L_2 = 10 / 100 = 0.1 H), coupling k = 0.999, primary driven by 325 V peak at 50 Hz through 1 ohm of source resistance, secondary loaded with 10 ohm.

- Secondary peak voltage, ideally: 325 / 10 = 32.5 V.
- Secondary peak current: 32.5 / 10 = 3.25 A.
- Reflected load: 10² x 10 = 1000 ohm. Primary current feeding the load: 325 / 1000 = 0.325 A peak (= 3.25 / 10, as it should).
- Magnetizing current: the primary inductance at 50 Hz behaves like an "AC resistance" of 2 pi f L = 2 x 3.1416 x 50 x 10 = 3142 ohm (Phase 09 will call this *reactance*), so the magnetizing current is about 325 / 3142 = 0.103 A peak. It peaks a quarter of a cycle later than the load current, so the two do not simply add; combined (Phase 09 shows how) they give sqrt(0.325² + 0.103²) = 0.341 A.

## Build It

### Step 1: Turns ratio

```python
def secondary_voltage(primary_volts, primary_turns, secondary_turns):
    return primary_volts * secondary_turns / primary_turns


def turns_for(primary_volts, secondary_volts, primary_turns):
    return primary_turns * secondary_volts / primary_volts
```

Output: 32.5 V for 1000:100, 16.9 V for 1000:52, 650 V for a step-up 500:1000, and 52.2 secondary turns for 12 V from 230 V.

### Step 2: Power conservation

The script prints a 24 W load at 12 V and 2 A, and a primary current of 104 mA at 230 V: 24 W on both sides.

### Step 3: Reflected resistance

```python
def reflected_resistance(load_ohms, ratio):
    return ratio**2 * load_ohms
```

8 ohm through 10:1 is 800 ohm, 10 ohm through 10:1 is 1000 ohm, 50 ohm through 2:1 is 200 ohm.

### Step 4: Two coupled coils from their equations

We simulate the coupled-coil equations directly, with the backward Euler method from Phase 07, Lesson 08. With the source on the primary and the load on the secondary, the two loop equations are

```
L1 di1/dt + M di2/dt = Vs(t) - Rs i1
M di1/dt + L2 di2/dt = -RL i2
```

Replace each derivative by (new - old) / dt and evaluate the right sides with the *new* currents. Collecting the unknowns on the left gives a 2 x 2 linear system that is the same at every step:

```python
def coupled_coils(peak, freq, source_ohms, load_ohms, l1, l2, coupling, t_stop, dt):
    mutual = coupling * np.sqrt(l1 * l2)
    inductance = np.array([[l1, mutual], [mutual, l2]])
    system = inductance / dt + np.diag([source_ohms, load_ohms])
    solver = np.linalg.inv(system)
    steps = int(round(t_stop / dt))
    t = np.arange(steps + 1) * dt
    currents = np.zeros((steps + 1, 2))
    for n in range(1, steps + 1):
        drive = np.array([peak * np.sin(2 * np.pi * freq * t[n]), 0.0])
        currents[n] = solver @ (inductance / dt @ currents[n - 1] + drive)
    load_current = -currents[:, 1]
    return t, currents[:, 0], load_current, load_ohms * load_current, mutual
```

The secondary current i2 is defined flowing *into* the coil's top terminal, so the current the coil pushes out into the load is -i2. Running 0.2 s (10 cycles) with 10 µs steps:

```
  L1 = 10.0 H, L2 = 100 mH, k = 0.999, M = 999.0 mH
  turns ratio from sqrt(L1 / L2) = 10.0
  secondary peak voltage 32.42 V across 10 ohm (ideal 32.5 V)
  secondary peak current 3.242 A, primary peak current 0.341 A
```

The voltage is within 0.3 % of ideal (the 1 ohm source resistance and the 0.1 % of flux that leaks both cost a little), and the primary current is the 0.341 A we predicted.

### Step 5: The equivalent circuit in our simulator

```python
def equivalent_circuit(peak, freq, source_ohms, load_ohms, l1, ratio, t_stop, dt):
    c = Circuit()
    c.sine_source("Vs", "in", "0", amplitude=peak, freq=freq)
    c.resistor("Rs", "in", "p", source_ohms)
    c.inductor("Lm", "p", "0", l1)
    c.resistor("Rreflected", "p", "0", reflected_resistance(load_ohms, ratio))
    c.vcvs("E1", "out", "0", "p", "0", 1 / ratio)
    c.resistor("RL", "out", "0", load_ohms)
    run = c.transient(t_stop=t_stop, dt=dt, method="be")
    return np.asarray(run.time), np.asarray(run.v("out")), np.asarray(run.i("Rs"))
```

`method="be"` asks for backward Euler, the same method as our hand-written loop, so the comparison is fair. Output:

```
  ideal transformer + magnetizing inductance + reflected load: secondary peak 32.46 V
  primary peak current 0.341 A
  largest difference between the two secondary waveforms: 0.206 V (0.64 %)
```

The two approaches agree to within 0.64 %. The remaining difference is the leakage (k = 0.999 instead of 1), which the simple equivalent circuit leaves out. Set `COUPLING = 0.99` and the difference grows; real transformer models add a small "leakage inductance" in series to account for it.

### Step 6: Efficiency

A small 24 W mains transformer might lose 1.8 W in the resistance of its windings (*copper loss*, I² R) and 1.2 W in its core (*core loss*: eddy currents and the energy needed to flip the domains back and forth). Efficiency = 24 / (24 + 1.8 + 1.2) = 88.9 %. Large grid transformers reach 99 % and more.

## Use It

- **Mains transformers** ("linear" power supplies, doorbells, old audio gear). Datasheets give primary voltage (230 V or 115 V), secondary voltage at full load (say 12 V), VA rating (volt-amperes, roughly watts: 24 VA), regulation (how much the voltage rises with no load, often 10 to 20 % for small units) and isolation test voltage (3 to 4 kV).
- **Switching power supplies** (every USB charger) chop the rectified mains at 50 to 200 kHz and feed a tiny ferrite transformer. Faraday's law: the voltage per turn is proportional to dPhi/dt, so at 2000 times the frequency, the same voltage needs 2000 times less flux, which means a far smaller core. That is why a 65 W laptop charger fits in your hand.
- **Isolation.** Medical equipment and lab instruments use transformers so that no wire connects the mains to anything a person can touch. Phase 06's safety notes apply: an isolation transformer is a common safety tool for working on mains equipment.
- **Current transformers** put the wire to be measured through a ring core with many secondary turns; the secondary carries a small, safe copy of a large current (Use It in Lesson 02 was the DC version).
- **Audio and data.** Ethernet ports contain small transformers ("magnetics") on every pair of wires, so that two computers with different ground voltages can still talk.
- **Laminated cores.** Mains transformer cores are stacks of steel sheets about 0.35 to 0.5 mm thick, each coated with insulation. A solid core would be one big loop for eddy currents (Lesson 03) and would get hot. High-frequency transformers use ferrite, a ceramic that barely conducts at all.

## Common Mistakes

- **Connecting a transformer to DC.** There is no changing flux, so no output, and the primary draws a large current limited only by its wire resistance.
- **Thinking a step-up transformer creates power.** Voltage goes up, current goes down by the same factor. Power in is always at least power out.
- **Mixing up the ratio.** n = N_p / N_s. A 10:1 transformer makes the voltage 10 times *smaller* and the current 10 times *larger* on the secondary.
- **Forgetting the square in reflected impedance.** The voltage ratio is n, the current ratio is n, so the resistance ratio is n².
- **Expecting the rated secondary voltage with no load.** Real transformers have winding resistance, so their output drops under load; the rated value is usually *at full load*, and the no-load voltage is higher.
- **Ignoring the magnetizing current.** An unloaded transformer still draws current from the mains.

## Exercises

1. **Easy.** A transformer has 1200 primary turns and 60 secondary turns. With 230 V on the primary, what is the secondary voltage? What is the turns ratio?
2. **Easy.** A 9 V secondary delivers 1.5 A. The primary is at 230 V. Ignoring losses, what is the primary current?
3. **Medium.** You want a 4 ohm speaker to look like 1600 ohm to an amplifier. What turns ratio do you need?
4. **Medium.** Two coils of 4 mH and 1 mH have coupling k = 0.8. What is their mutual inductance? What would the turns ratio be if they were perfectly coupled?
5. **Hard.** In `main.py`, change `COUPLING` to 0.95 and then 0.8. Record the secondary peak voltage and the difference from the equivalent circuit each time. Explain why weaker coupling lowers the output voltage, thinking of the flux that "leaks" without passing through the secondary.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Transformer | "Changes the voltage" | Magnetically coupled coils on a common core; V_s / V_p = N_s / N_p for a changing flux |
| Turns ratio | "10 to 1" | n = N_p / N_s; voltages scale by 1/n, currents by n, resistances by 1/n² from primary to secondary |
| Mutual inductance | "How well they couple" | M, in henries: voltage in one coil per A/s of current change in the other; M = k sqrt(L1 L2) |
| Coupling coefficient | "Leakage" | k, the fraction of flux shared by both coils, 0 to 1 |
| Magnetizing current | "No-load current" | The current the primary inductance draws from the source to keep the flux changing |
| Reflected impedance | "What the load looks like" | A load R_L on the secondary appears as n² R_L at the primary |
| Isolation | "No connection" | Primary and secondary share no conductor; energy crosses only through the magnetic field |
| Core loss / copper loss | "Losses" | Energy lost in the core (eddy currents, hysteresis) and in the windings' resistance (I² R) |

## Further Reading

- [All About Circuits, Volume II, Chapter 9: Transformers](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-9/mutual-inductance-and-basic-operation/) — mutual inductance, step-up and step-down, and real transformer behaviour
- [The Feynman Lectures on Physics, Vol. II, Chapter 17 (The Laws of Induction), section on mutual inductance](https://www.feynmanlectures.caltech.edu/II_17.html) — where M = k sqrt(L1 L2) comes from
- [MIT OpenCourseWare 6.061 Introduction to Electric Power Systems, notes on transformers](https://ocw.mit.edu/courses/6-061-introduction-to-electric-power-systems-spring-2011/) — equivalent circuits, magnetizing branch and leakage
- *Practical Electronics for Inventors* (Scherz & Monk), section on transformers — practical selection of real transformers
