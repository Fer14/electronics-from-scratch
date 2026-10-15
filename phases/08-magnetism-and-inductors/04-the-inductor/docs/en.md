# The Inductor

> A capacitor resists changes in voltage. An inductor resists changes in current. Everything else about it follows from v = L di/dt.

**Type:** Learn
**Prerequisites:** Phase 08 (Magnetism and Inductors), Lesson 03 (Faraday's Law and Induction); Phase 07 (Capacitors), Lessons 02 (Capacitance) and 06 (Energy in the Electric Field)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Inductor | A component, usually a coil of wire, that opposes changes in the current through it | A heavy flywheel: hard to start spinning, hard to stop |
| Inductance (L) | How strongly a coil opposes changes in current: the volts it produces per (ampere per second) of change | How heavy the flywheel is |
| Henry (H) | The unit of inductance. 1 H makes 1 V when the current changes by 1 A every second | Real inductors range from nanohenries to a few henries |
| Self-induction | A coil inducing a voltage in itself because its own field changes | Pushing on a revolving door that pushes back on you |
| Back-EMF | The voltage an inductor makes to oppose a change in current | The push-back you feel from the flywheel |
| Choke | An inductor used to let DC through while blocking fast changes | A heavy door that lets you walk through slowly but stops a sudden rush |
| DCR | The plain wire resistance of an inductor (DC resistance) | The friction in the flywheel's bearings |
| Saturation current | The current at which the core is "full" and the inductance collapses | The point where the flywheel's clutch slips |
| di/dt | "How fast the current changes", in amperes per second (A/s) | The acceleration of the flywheel |

## Learning Objectives

- Explain self-induction: how a coil's own changing field produces a voltage that opposes the change in current
- Calculate the inductance of a solenoid and see why it grows with the square of the number of turns
- Use the inductor law v = L di/dt to compute voltages from current changes and current ramps from voltages
- Calculate the energy stored in an inductor's magnetic field, E = ½ L I²
- Predict an inductor's behaviour at DC (a wire) and at a sudden change (the current cannot jump), and confirm both with our simulator

## The Problem

In Phase 07 you met the capacitor, a part whose voltage cannot jump: to change it, you must move charge, and that takes time. Capacitors smooth voltages, store energy in an electric field, and set the timing of countless circuits.

There is a partner component that does the same thing for **current**. Open any switching power supply (the brick that charges your laptop, the small module on a microcontroller board that turns 12 V into 3.3 V) and you will find a few coils of copper wire wound on dark grey cores. These are **inductors**. They keep current steady while a transistor switches on and off thousands of times a second. They block high-frequency noise from escaping along cables. In radios they combine with capacitors to pick one station out of hundreds (Phase 10). And in a car's ignition coil, the very same "current cannot stop suddenly" behaviour is used to make a spark of tens of thousands of volts from a 12 V battery.

To use them, we need one rule, v = L di/dt, and we need to know where it comes from.

## The Physics

### A coil talks to itself

Take a coil of wire and push a current through it. From Lesson 02, the current makes a magnetic field through the coil. From Lesson 03, if the flux through a coil changes, an EMF appears in the coil. Put those together:

1. You *increase* the current through the coil.
2. The field inside the coil grows, so the flux through the coil's own turns grows.
3. By Faraday's law, a changing flux induces an EMF in those same turns.
4. By Lenz's law, that EMF opposes the change: it pushes *against* the increase in current.

That is **self-induction**. The coil fights changes in its own current. When you try to increase the current, the coil produces a voltage that resists; when you try to decrease it, the coil produces a voltage that tries to keep the current flowing. If the current is steady, the flux is steady, nothing is induced, and the coil is just a piece of wire.

### The flywheel picture

Think of current as the spinning of a heavy **flywheel** (a big, heavy wheel on an axle):

- To spin it up you must push (apply a voltage), and the speed rises gradually, not instantly.
- Once it spins at a steady speed, it keeps spinning with no effort except to overcome friction (a steady current needs no voltage across an ideal inductor).
- If you try to stop it suddenly, it fights back with an enormous force (an inductor whose current is interrupted produces an enormous voltage: Lesson 05).
- The heavier the flywheel, the harder all of this is. The "heaviness" is the **inductance**.

What the picture gets wrong: a flywheel stores energy as motion of mass; an inductor stores it in the magnetic field around the coil, and there is nothing physically spinning. Also, a real flywheel keeps its energy when you disconnect it; an inductor's current needs a closed path to keep flowing, and when you open the circuit the energy has to go somewhere, fast.

### Inductance defined

The flux linkage of a coil (turns times flux, Lesson 03) is proportional to the current through it: double the current, double the field, double the flux. The constant of proportionality is the **inductance**, symbol **L**:

```
N * Phi = L * I
```

"the flux linkage equals the inductance times the current". Faraday's law says the EMF is the rate of change of flux linkage, so the voltage across the coil is the inductance times the rate of change of current:

```
v = L * di/dt
```

This is **the inductor law**. Read it aloud: "the voltage across an inductor equals its inductance times how fast its current is changing". It is as fundamental for inductors as v = I x R is for resistors and i = C dv/dt is for capacitors (Phase 07).

Units: L is measured in **henries (H)**, after the American physicist Joseph Henry, who discovered self-induction independently around the same time as Faraday. From the law, 1 H = 1 V / (1 A/s) = 1 V·s/A. A coil of 1 H produces 1 V when its current changes by 1 ampere every second.

**Signs.** We measure v from terminal a to terminal b and i flowing from a to b through the coil (the same convention as a resistor). If the current is increasing (di/dt > 0), v is positive: terminal a is higher, the coil acts like a load that is "being charged". If the current is decreasing, v is negative: the coil acts like a source pushing current onwards.

### Compare with the capacitor

| | Capacitor | Inductor |
|---|---|---|
| Law | i = C dv/dt | v = L di/dt |
| Cannot jump | voltage | current |
| At DC, after settling | open circuit (no current) | short circuit (no voltage) |
| Stores energy in | electric field, ½ C V² | magnetic field, ½ L I² |
| Unit | farad (F) | henry (H) |

The two laws are mirror images with v and i swapped. This "duality" will make Lesson 05 (RL transients) look almost identical to Phase 07's RC transients.

## The Concept

### 1. How big is L? The solenoid formula

For a long coil of N turns, cross-section area A and length l, wound on a core of relative permeability mu_r:

```
L = mu_r * mu0 * N^2 * A / l
```

"inductance equals mu-r times mu-zero times the turns squared times the area, divided by the length". Where does the N² come from? The field inside a solenoid is proportional to N (Lesson 02: B = mu0 N I / l). And the flux linkage counts that field once in *every* turn, which multiplies by N again. **Double the turns, four times the inductance.**

**Worked example.** 100 turns on a tube of radius 5 mm, 2 cm long, air core.

- A = pi x r² = 3.1416 x 0.005² = 3.1416 x 0.000025 = 7.854e-5 m²
- N² = 10,000
- L = 1.2566e-6 x 10,000 x 7.854e-5 / 0.02 = 4.935e-5 H = 49.35 µH

With 50 turns: N² = 2,500, a quarter: 12.34 µH. With 200 turns: four times as much, 197.4 µH. On a ferrite rod with an effective mu_r of 200: 200 x 49.35 µH = 9.87 mH. Cores are how practical inductors get large values in small packages.

Typical real values: 1 to 100 nH for the tiny inductors in phones and radio circuits, 1 to 100 µH in switching power supplies, millihenries in audio crossovers and mains filters, and around a henry for old-fashioned power-supply chokes.

### 2. Using the law: from current change to voltage

**Worked example A.** A 10 mH inductor's current rises steadily from 0 to 1 A in 1 ms. The rate of change is di/dt = 1 A / 0.001 s = 1,000 A/s. The voltage: v = 0.01 x 1,000 = 10 V, constant during the whole ramp.

**Worked example B.** Same inductor, but now the current changes by 1 A in 1 µs (one millionth of a second): di/dt = 1,000,000 A/s and v = 0.01 x 1e6 = 10,000 V. **Fast changes of current make huge voltages.** That is the root of inductive kick (Lesson 05), of ignition coils, and of the voltage spikes that destroy transistors that switch relays without protection.

**Worked example C.** A 100 µH inductor in a power supply sees its current change by 2 A in 10 µs: v = 100e-6 x 2 / 10e-6 = 20 V.

### 3. Using the law backwards: from voltage to current ramp

Rearranged, the law says di/dt = v / L: **a constant voltage across an inductor makes its current ramp up in a straight line**, at v / L amperes per second. After a time t, starting from zero:

```
i(t) = v * t / L
```

**Worked example.** 1 V across 10 mH: the current grows by 1 / 0.01 = 100 A per second, so after 1 ms it is 0.1 A = 100 mA, after 2 ms 200 mA. It keeps growing for as long as the voltage is applied. In a real circuit something always limits it: the wire resistance (here we add 0.1 ohm), the source's internal resistance, or the core saturating. Compare a capacitor fed by a constant *current*, whose voltage ramps in a straight line (Phase 07).

### 4. The current cannot jump

If the current through an inductor could jump instantly from one value to another, di/dt would be infinite and so would the voltage. No real circuit can supply an infinite voltage, so **the current through an inductor is always continuous**. Its voltage, on the other hand, *can* jump: flip the voltage across an inductor from +5 V to -5 V and the current simply changes from ramping up to ramping down, starting from the very same value.

```
 v_L   +5 |-------+         +-----     voltage jumps
          |       |         |
       -5 |       +---------+
 i_L      |      /\
          |     /  \                    current is continuous:
          |    /    \                   it only changes slope
          |   /      \
          |  /        \
        0 +-/----------\------> t
          0   1 ms     2 ms
```

This continuity is the single most useful fact for analysing circuits with inductors, exactly as "the voltage across a capacitor cannot jump" was for capacitors.

### 5. At DC, an inductor is a wire

When everything has settled and the current is steady, di/dt = 0 and therefore v = L x 0 = 0. An ideal inductor at DC is a plain wire (a short circuit). A real inductor at DC is a small resistor, its DCR.

**Worked example.** 9 V battery, a 100 ohm resistor from the battery to node a, and then something from node a to ground:

- **Inductor (ideal)**: it is a wire at DC, so node a is at 0 V and I = 9 / 100 = 90 mA.
- **Capacitor**: at DC it is open; no current flows, so there is no drop across the resistor and node a sits at 9 V.
- **Another 100 ohm resistor**: a voltage divider (Phase 04), node a at 4.5 V, I = 9 / 200 = 45 mA.

This is the idea behind a **choke**: it passes DC (and slow changes) freely while it fights fast changes.

### 6. Energy in the magnetic field

To build up a current I in an inductor, the source must push against the back-EMF the whole time. The energy it spends is stored in the magnetic field:

```
E = 1/2 * L * I^2
```

"energy equals one half times the inductance times the current squared", in joules. You can see where it comes from with the ramp: while the current grows from 0 to I in time T, the voltage is v = L I / T, and the average current is I / 2, so the average power is v x I / 2 = L I² / (2T); multiply by the time T and you get ½ L I². It has exactly the same form as a capacitor's ½ C V².

**Worked examples.** 10 mH at 1 A: E = 0.5 x 0.01 x 1 = 5 mJ. At 2 A it is four times as much (20 mJ), because of the square. 100 µH at 5 A: 0.5 x 1e-4 x 25 = 1.25 mJ. These are small energies, but released in microseconds they make big power pulses.

## Build It

### Step 1: The solenoid formula

```python
def solenoid_inductance(turns, area, length, relative_permeability=1.0):
    return relative_permeability * MU0 * turns**2 * area / length
```

Output:

```
   50 turns, radius 5 mm, length 2 cm, air: L =   12.34 uH
  100 turns, radius 5 mm, length 2 cm, air: L =   49.35 uH
  200 turns, radius 5 mm, length 2 cm, air: L =  197.39 uH
  100 turns on a ferrite rod with effective mu_r = 200: L = 9.87 mH
```

Each doubling of turns multiplies L by 4.

### Step 2: v = L di/dt

```python
def inductor_voltage(inductance, current_change, seconds):
    return inductance * current_change / seconds
```

The four cases print 10 V, 10 kV, 20 V and 100 mV. The second line is the one to remember: the same 1 A change done a thousand times faster gives a thousand times the voltage.

### Step 3: Stored energy

```python
def stored_energy(inductance, current):
    return 0.5 * inductance * current**2
```

5 mJ, 20 mJ, 1.25 mJ and 5 mJ. Notice that 1 H at 0.1 A stores the same as 10 mH at 1 A: a hundred times the inductance, a tenth of the current, and 0.1² = 1/100.

### Step 4: The DC test with our simulator

```python
def dc_with_part(part):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", 9.0)
    c.resistor("R1", "vcc", "a", 100.0)
    if part == "inductor":
        c.inductor("X", "a", "0", 10e-3)
    elif part == "capacitor":
        c.capacitor("X", "a", "0", 1e-6)
    else:
        c.resistor("X", "a", "0", 100.0)
    result = c.dc()
    return result.v("a"), result.i("R1")
```

The simulator's DC analysis treats inductors as shorts and capacitors as opens, exactly the rule above:

```
  inductor  to ground: V(a) =  0.000 V, current in R1 =  90.00 mA
  capacitor to ground: V(a) =  9.000 V, current in R1 =   0.00 mA
  resistor  to ground: V(a) =  4.500 V, current in R1 =  45.00 mA
```

### Step 5: The current ramp

```python
def current_ramp(volts, winding_ohms, inductance, t_stop, dt):
    c = Circuit()
    c.pulse_source("V1", "in", "0", low=0.0, high=volts, period=1.0, duty=0.99)
    c.resistor("Rw", "in", "a", winding_ohms)
    c.inductor("L1", "a", "0", inductance)
    run = c.transient(t_stop=t_stop, dt=dt)
    return np.asarray(run.time), np.asarray(run.i("L1")), np.asarray(run.v("a"))
```

A pulse source with a 1 s period simply switches on at t = 0 and stays at 1 V for the 2 ms we simulate. The inductor starts with zero current (its default `i0=0`). We include 0.1 ohm of winding resistance to be realistic. Output:

```
  t = 0.5 ms: i =   49.88 mA (ideal ramp V t / L =   50.00 mA), v_L = 0.995 V
  t = 1.0 ms: i =   99.50 mA (ideal ramp V t / L =  100.00 mA), v_L = 0.990 V
  t = 2.0 ms: i =  198.01 mA (ideal ramp V t / L =  200.00 mA), v_L = 0.980 V
```

The current is almost exactly the ideal straight line. The tiny shortfall is the winding resistance: at 198 mA it drops 0.0198 V, so only 0.980 V is left across the inductor itself and the ramp slows slightly. In Lesson 05 we will see that this slowing is the start of an exponential curve.

### Step 6: Flip the voltage; the current does not jump

```python
def current_after_voltage_flip(volts, inductance, flip_time, t_stop, dt):
    c = Circuit()
    c.pulse_source("V1", "in", "0", low=-volts, high=volts, period=2 * flip_time, duty=0.5)
    c.resistor("Rw", "in", "a", 0.01)
    c.inductor("L1", "a", "0", inductance)
    run = c.transient(t_stop=t_stop, dt=dt)
    return np.asarray(run.time), np.asarray(run.i("L1")), np.asarray(run.v("a"))
```

The source is +5 V for 1 ms, then -5 V for 1 ms. Ramp up at 5 / 0.01 = 500 A/s for 1 ms reaches 0.5 A; then ramp down at the same rate back to 0:

```
  t =  0.999 ms: v_L =  +5.00 V, i =   499.3 mA
  t =  1.001 ms: v_L =  -5.00 V, i =   499.7 mA
  t =  1.500 ms: v_L =  -5.00 V, i =   250.1 mA
  t =  2.000 ms: v_L =  +5.00 V, i =     0.5 mA
```

Across the flip at 1 ms the voltage jumped by 10 V, but the current changed by less than half a milliamp. This triangle wave of current is exactly what flows in the inductor of a switching power supply (Phase 18).

## Use It

- **Switching power supplies.** A buck converter (Phase 18) switches a transistor on and off at hundreds of kilohertz. The inductor keeps the current flowing smoothly between switching events. A typical part like the Würth WE-PD or Coilcraft XAL series 10 µH inductor lists: inductance 10 µH ± 20%, DCR about 20 to 40 milliohm, saturation current a few amperes, and a rated (heating) current.
- **Ferrite beads** on USB and HDMI cables (the lumps near the plug) are tiny inductors made by threading the wire through a ferrite ring. They let the DC and the slow signal through and damp fast noise.
- **Ignition coils.** A car's ignition coil builds up a few amperes in its primary winding, then the current is interrupted in microseconds. di/dt is enormous, and (with help from the transformer action of Lesson 06) the result is the 20 to 40 kV spark.
- **Radio and RF.** Inductors of a few nanohenries to microhenries, combined with capacitors, form the tuned circuits of Phase 10. In a phone they are tiny chips, 0.4 mm long.
- **Datasheet words.** *Inductance* (with tolerance, usually ±10 to 30%), *DCR* (the resistance, which costs I² R of heat), *I_sat* (current where L has dropped by typically 20 to 30%), *I_rms* or *I_rated* (current that heats it by about 40 °C), and *SRF* (self-resonant frequency: above it, the winding's own capacitance makes the inductor behave like a capacitor).

## Try It in the Lab

Open **"Let the DC through"**. A 9 V supply feeds a sensor (modelled with the cable as a 100 ohm resistor) and the current must return to ground through an empty slot. Your drawer has an inductor, a capacitor and a resistor. Before running, predict the voltage at node a and the current for each one, using only "what does this part do when nothing is changing?". Then run all three. Which part would you choose if, in addition, you wanted to *block* fast noise from reaching ground?

## Common Mistakes

- **Saying "an inductor resists current".** It resists *changes* in current. A steady current flows through an ideal inductor with no voltage drop at all.
- **Expecting an inductor's voltage to follow its current.** The voltage follows the *rate of change* of current. At the peak of a current waveform, the voltage is zero.
- **Forgetting that the current is continuous.** When a switch changes, the inductor's current at the instant after is the same as at the instant before. Start every analysis from there.
- **Forgetting the N².** Halving the turns of a coil does not halve its inductance; it quarters it.
- **Ignoring saturation and DCR.** Beyond I_sat, a real inductor's L drops sharply and current can surge. And the DCR turns current into heat.
- **Confusing mH and µH.** Datasheets use both; a factor of 1,000 error turns a filter into a short.

## Exercises

1. **Easy.** A 47 µH inductor's current rises by 0.5 A in 2 µs. What voltage is across it?
2. **Easy.** How long does it take for 12 V across 220 µH to ramp the current from 0 to 3 A (ignore resistance)?
3. **Medium.** You need a 1 mH air-core coil 3 cm long with a radius of 1 cm. How many turns do you need? (Rearrange the solenoid formula for N.)
4. **Medium.** An inductor stores 18 mJ at 3 A. What is its inductance? How much energy does it store at 1 A?
5. **Hard.** In `main.py`, change the winding resistance in `current_ramp` from 0.1 ohm to 2 ohm and simulate 20 ms instead of 2 ms. The current no longer grows forever. What final value does it approach, and why? (Use the DC rule.) How long does it take to get two-thirds of the way there? Keep your answer for Lesson 05.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Inductor | "A coil" | A two-terminal part obeying v = L di/dt: it opposes changes in its current by self-induction |
| Inductance | "How big the coil is" | L = N Phi / I, in henries; for a solenoid mu_r mu0 N² A / l |
| Henry | "The inductor unit" | 1 H = 1 V·s/A: one volt for a change of one ampere per second |
| Back-EMF | "The coil fighting back" | The voltage L di/dt that opposes the change in current |
| Choke | "A filter coil" | An inductor used to pass DC and block fast-changing currents |
| DCR | "The coil's resistance" | The resistance of the winding wire, which sets the DC drop and the heating |
| Saturation current | "Max current" | The current at which the core saturates and the inductance falls sharply |
| Current continuity | "Inductors don't like change" | The current through an inductor cannot change instantly, because that would need infinite voltage |

## Further Reading

- [All About Circuits, Volume I, Chapter 15: Inductors](https://www.allaboutcircuits.com/textbook/direct-current/chpt-15/magnetic-fields-and-inductance/) — magnetic fields, inductance and the inductor law, with practical notes
- [The Art of Electronics (Horowitz & Hill), 3rd edition, chapter 1 (inductors and transformers)](https://artofelectronics.net/) — the practical engineer's view of inductors in circuits
- [MIT OpenCourseWare 6.002 Circuits and Electronics, lectures on energy storage elements](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) — the inductor law and duality with the capacitor
- [Coilcraft: "Key Parameters for Selecting RF Inductors" and the XAL series datasheets](https://www.coilcraft.com/en-us/resources/application-notes/key-parameters-for-selecting-rf-inductors/) — what DCR, I_sat and SRF mean on a real part
