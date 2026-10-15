# RL Transients

> In an RL circuit the current creeps towards its final value along the same exponential curve as an RC circuit, with tau = L / R. Interrupt that current and the inductor will do anything, including making a thousand volts, to keep it flowing.

**Type:** Learn
**Prerequisites:** Phase 08 (Magnetism and Inductors), Lesson 04 (The Inductor); Phase 07 (Capacitors), Lessons 03 (Charging and Discharging) and 04 (The Time Constant)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Transient | The short period while a circuit adjusts after something changes, before it settles | The wobble of a shelf after you put a book on it |
| Steady state | The condition after the transient has died out, when nothing changes any more | The shelf sitting still again |
| RL circuit | A circuit made of a resistor (R) and an inductor (L) | A flywheel with a brake |
| Time constant (tau) | The time it takes to cover 63.2 % of the way to the final value; for RL, tau = L / R | How long the flywheel takes to get most of the way up to speed |
| Exponential curve | A curve that changes fast at first and then slower and slower, always by the same fraction per unit time | A cup of tea cooling: quickly at first, then gently |
| Inductive kick | The large voltage spike produced when the current through an inductor is suddenly interrupted | The bang when you slam on the flywheel's brake |
| Flyback diode | A diode placed across an inductor to give its current a safe path when switched off | A soft cushion for the flywheel to coast down on |
| Arc | A spark jumping across a gap through the air, because the voltage is high enough to break the air down | The tiny blue spark when you unplug something that is running |

## Learning Objectives

- Derive the RL charging and discharging curves from v = L di/dt and Kirchhoff's voltage law
- Calculate the time constant tau = L / R and the current at any time with i(t) = I_final (1 - e^(-t/tau))
- Explain why a larger resistor makes an RL circuit faster, the opposite of an RC circuit
- Simulate RL rise and decay with our simulator and match the formulas
- Explain and simulate inductive kick and how a flyback diode tames it

## The Problem

Every relay coil, solenoid valve, motor and loudspeaker is an inductor with some resistance. When a microcontroller switches one on, the current does not appear instantly: it grows over milliseconds. If your program assumes the relay closes the moment the pin goes high, it may read a sensor before the contacts have even moved. You need to know how long the current takes.

Switching *off* is worse. The inductor's current wants to keep flowing (Lesson 04), but the switch has just removed its path. The coil responds by raising its voltage to whatever it takes to keep the current going: hundreds or thousands of volts, enough to make an arc across a mechanical switch or to destroy the transistor that was driving it. Engineers who forget this see their circuits work for a few minutes and then die. This lesson gives you the curve for switching on, the curve for switching off, and the one-cent part (a diode) that prevents the disaster.

## The Physics

### What happens when you connect the battery

Take a 10 V source, a 100 mH coil and a 100 ohm resistor in series, all initially at rest (no current).

```
         +---- L = 100 mH ----+
         |                    |
      +  |                    x
   10 V (V1)                  |
      -  |                  R = 100 ohm
         |                    |
         +--------------------+ 0 V
```

At the instant you connect the source:

1. **The current cannot jump** (Lesson 04). It was 0, so it is still 0 just after connecting.
2. With zero current, the resistor has zero voltage across it (v = I x R = 0).
3. Kirchhoff's voltage law (Phase 04) says the voltages around the loop add up to the source: 10 V = v_L + v_R. Since v_R = 0, **all 10 V are across the inductor**.
4. v_L = L di/dt, so di/dt = 10 / 0.1 = 100 A/s: the current starts growing at 100 A per second.

As the current grows, the resistor takes a bigger share of the 10 V, so less voltage is left for the inductor, so the current grows more slowly. The growth keeps slowing down. Eventually the current reaches the value where the resistor takes all 10 V: I_final = 10 / 100 = 0.1 A = 100 mA. Now v_L = 0, di/dt = 0, and the current stops changing. The inductor is a wire, as at DC.

This "the closer you get, the slower you go" behaviour always produces an **exponential curve**. You saw exactly the same thing for a capacitor charging through a resistor in Phase 07.

### The equations

Write Kirchhoff's voltage law at any instant:

```
V = L * di/dt + R * i
```

"the source voltage equals the inductor's voltage plus the resistor's voltage". The solution, starting from i = 0 at t = 0, is

```
i(t) = (V / R) * (1 - e^(-t / tau)),      tau = L / R
```

Read it: "the current equals its final value V over R, times one minus e to the minus t over tau". Here **e** is the number 2.71828..., the base of natural exponentials (Phase 07 introduced it), and e^(-t/tau) is a number that starts at 1 when t = 0 and shrinks towards 0 as time passes. So 1 - e^(-t/tau) grows from 0 to 1, and the current grows from 0 to V/R.

**Check it.** At t = 0: e^0 = 1, so i = (V/R)(1 - 1) = 0. Correct, the current starts at zero. At the start, the slope of the curve is (V/R) / tau = (V/R) x (R/L) = V/L, exactly the 100 A/s we found. Long after: e^(-large) is about 0, so i = V/R. Correct again.

### The time constant tau = L / R

The quantity tau (Greek letter, "tow") has units of seconds: henries divided by ohms is (V·s/A) / (V/A) = s. It sets the time scale:

| Time | e^(-t/tau) | Fraction of final value reached |
|---|---|---|
| 1 tau | 0.368 | 63.2 % |
| 2 tau | 0.135 | 86.5 % |
| 3 tau | 0.050 | 95.0 % |
| 4 tau | 0.018 | 98.2 % |
| 5 tau | 0.0067 | 99.3 % |

After 5 time constants, engineers call the transient "over".

For our circuit: tau = 0.1 / 100 = 0.001 s = 1 ms. After 1 ms the current is 63.2 mA, after 3 ms 95.0 mA, after 5 ms 99.3 mA.

**Why a bigger R is faster.** In an RC circuit, tau = R x C, so a bigger resistor makes the capacitor charge *slower* (it limits the current that fills it). In an RL circuit, tau = L / R, so a bigger resistor makes the current settle *faster*. Why? The final current V/R is smaller, so there is less current to build up, while the starting slope V/L is the same. Reaching a smaller target at the same initial speed takes less time. If R = 1000 ohm, tau = 0.1 ms and the final current is only 10 mA.

### Switching the source down to zero: decay

Now suppose the current has settled at I_0 = 100 mA and the source drops to 0 V (the source is still in the circuit, acting as a wire). The inductor's current cannot jump, so it keeps flowing at 100 mA, now driven by the inductor itself. The loop equation becomes 0 = L di/dt + R i, so di/dt = -R i / L: the current falls, faster when it is big, slower as it gets small:

```
i(t) = I_0 * e^(-t / tau)
```

After 1 tau it is 36.8 % of I_0, after 3 tau 5 %. At the very instant of the drop, the resistor still has 100 mA x 100 ohm = 10 V across it, and the loop must add to zero, so the inductor's voltage jumps to **-10 V**: it has flipped from being a load to being the source that pushes the current on. The energy stored in the field, ½ L I² = 0.5 x 0.1 x 0.01 = 0.5 mJ, is slowly turned into heat in the resistor.

### Opening the switch: inductive kick

Now the dangerous case. Instead of the source dropping to zero (which keeps a path for the current), a **switch opens** and breaks the loop.

```
   +10 V ---- S1 ----+---- L1 = 100 mH ----x
            (opens)  a                      |
                     |                 Rcoil = 100 ohm
                  Rleak = 10 k             |
                     |                      |
   0 V --------------+----------------------+
```

The inductor is carrying 100 mA. When S1 opens, that current has only one place to go: through Rleak (in a real circuit, this "leak" is the insulation of the switch, the air gap, or a transistor that is turned off; here we use 10 kilo-ohm, which is generous). The current must keep its value at the instant of opening, so 100 mA must flow through 10 k ohm: a voltage of 0.1 x 10,000 = **1000 V** appears across it, with node a driven to about -1000 V. A battery of 10 V has produced a kilovolt spike!

The spike does not last long. The total resistance in the loop is now 10,100 ohm, so tau = 0.1 / 10,100 = about 10 µs. All 0.5 mJ of energy is dumped in a few tens of microseconds. That is a peak power of tens of watts in a part that might be rated for a fraction of a watt.

In a real circuit with a truly open switch, Rleak is megaohms or more, and the voltage rises until something breaks down: air arcs across the switch contacts (this is the spark you sometimes see when unplugging a vacuum cleaner), or the transistor's junction fails. Car ignition systems use this on purpose. Everybody else must prevent it.

### The cure: the flyback diode

Place a diode across the coil, pointing so it does *not* conduct in normal operation (cathode to the + side). When the switch opens and node a tries to swing negative, the diode turns on as soon as a goes about 0.7 V below ground (Phase 11 explains diodes fully; for now, a diode is a one-way valve for current that needs about 0.7 V to open). The inductor's current now circulates through the diode and the coil's own resistance:

```
   +10 V ---- S1 ----+---- L1 ----x
                     a            |
                    _|_         Rcoil
          D1  ---   / \ (cathode at a)
                     |            |
   0 V --------------+------------+
```

The voltage at node a is clamped at about -0.7 V instead of -1000 V. The current now decays with tau = L / Rcoil = 1 ms (a bit faster in practice, because the diode's 0.7 V also helps soak up the energy). The relay releases a little later, but nothing is destroyed. This diode, often a 1N4148 or 1N4007, appears across practically every relay coil and small motor you will ever see.

## The Concept

The full RL toolkit on one card:

```
  time constant          tau = L / R
  final current          I_final = V / R           (inductor = wire)
  rise from zero         i(t) = I_final * (1 - e^(-t/tau))
  decay from I_0         i(t) = I_0 * e^(-t/tau)
  inductor voltage       v_L(t) = L di/dt = V * e^(-t/tau) during the rise
  at a switch instant    i(after) = i(before)      (current is continuous)
  energy to dispose of   E = 1/2 L I^2
```

**Worked example 1: a relay.** A 12 V relay coil has L = 0.4 H and R = 160 ohm. tau = 0.4 / 160 = 2.5 ms. Final current 12 / 160 = 75 mA. The relay pulls in at 50 mA, which is 50/75 = 66.7 % of the final value. Solve 1 - e^(-t/tau) = 0.667: e^(-t/tau) = 0.333, -t/tau = ln(0.333) = -1.10, t = 1.10 x 2.5 ms = 2.75 ms. The contacts start moving almost 3 ms after the pin goes high (plus the mechanical travel time).

**Worked example 2: choosing R for a speed.** You want a 100 mH coil's current to settle with tau = 1 ms. R = L / tau = 0.1 / 0.001 = 100 ohm. (That is the lab task.)

**Worked example 4: where the voltage goes during the rise.** Same 10 V, 100 mH, 100 ohm circuit. The inductor's voltage is v_L = V e^(-t/tau) and the resistor's is v_R = V (1 - e^(-t/tau)). They always add up to 10 V:

| t | e^(-t/tau) | v_L | v_R | i |
|---|---|---|---|---|
| 0 | 1.000 | 10.00 V | 0.00 V | 0 mA |
| 0.5 ms | 0.607 | 6.07 V | 3.93 V | 39.3 mA |
| 1 ms | 0.368 | 3.68 V | 6.32 V | 63.2 mA |
| 2 ms | 0.135 | 1.35 V | 8.65 V | 86.5 mA |
| 5 ms | 0.007 | 0.07 V | 9.93 V | 99.3 mA |

At the start the inductor "takes" the whole supply; at the end the resistor does. The voltage across the inductor is a falling exponential, the mirror image of the rising current.

**The tangent trick.** Draw the straight line that starts at the beginning of the curve with the initial slope (V / L for the current). It reaches the final value after exactly one tau. This gives a quick way to read tau off an oscilloscope screen (Phase 06): extend the first steep part of the curve until it hits the final level and read the time.

```
 i
 I_final |- - - - - - -/- - -___________
         |            /  _--
         |          /_--      <- real curve: 63 % at t = tau
         |        _/
         |     _-/   <- tangent at t = 0 reaches I_final at t = tau
         |   _/ /
         | _/  /
         |/   /
         +----+----+----+----+----> t
         0   tau  2tau 3tau 4tau
```

**Worked example 3: the kick.** A motor winding of 2 mH carries 1.5 A and is switched off by a transistor that, when off, behaves like 100 k ohm. Without protection, the voltage would try to reach 1.5 x 100,000 = 150,000 V. The transistor breaks down long before that, typically at 30 to 60 V for a small one, and dies.

## Build It

### Step 1: The formulas

```python
def time_constant(inductance, resistance):
    return inductance / resistance


def rise_current(final_current, tau, t):
    return final_current * (1 - np.exp(-t / tau))


def decay_current(start_current, tau, t):
    return start_current * np.exp(-t / tau)
```

For 100 mH and 100 ohm: tau = 1.000 ms and the table 63.21, 86.47, 95.02, 98.17, 99.33 mA at 1 to 5 tau.

### Step 2: Simulate the rise

```python
def simulate_rl_square(volts, inductance, resistance, period, t_stop, dt):
    c = Circuit()
    c.pulse_source("V1", "in", "0", low=0.0, high=volts, period=period, duty=0.5)
    c.inductor("L1", "in", "x", inductance)
    c.resistor("R1", "x", "0", resistance)
    return c.transient(t_stop=t_stop, dt=dt)
```

The pulse source is 10 V for the first half of its 12 ms period, then 0 V. We simulate 10 ms with 1 µs steps. The simulator and the formula agree to every printed digit:

```
  t = 1.0 ms: simulator  63.21 mA, formula  63.21 mA
  t = 3.0 ms: simulator  95.02 mA, formula  95.02 mA
  v across R1 reaches 63.2 % (6.32 V) at t = 1.000 ms (tau = 1.000 ms)
```

The voltage across R1 is the current times 100 ohm, so it is a scaled copy of the current. `run.time_to_cross("x", 6.32, "rising")` finds the moment it crosses 6.32 V: exactly one time constant.

### Step 3: Decay

At t = 6 ms the source drops to 0 V. The current at that moment is 99.70 mA (six time constants in), and from there:

```
  1.0 ms after: simulator  36.68 mA, formula  36.68 mA
  2.0 ms after: simulator  13.49 mA, formula  13.49 mA
  the voltage across L1 just after the drop: -9.95 V
```

36.68 = 99.70 x 0.368. And the inductor's voltage has flipped to almost -10 V, as predicted: it is now the source.

### Step 4: The kick, and the diode

```python
def simulate_switch_off(with_diode, t_stop, dt):
    steady = SUPPLY / RESISTANCE
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", SUPPLY)
    c.switch("S1", "vcc", "a", closed=True, toggle_at=(1e-3,))
    c.inductor("L1", "a", "x", INDUCTANCE, i0=steady)
    c.resistor("Rcoil", "x", "0", RESISTANCE)
    c.resistor("Rleak", "a", "0", 10e3)
    if with_diode:
        c.diode("D1", "0", "a")
    return c.transient(t_stop=t_stop, dt=dt)
```

`i0=steady` starts the inductor already carrying its 100 mA, so we do not have to wait for the rise. `toggle_at=(1e-3,)` makes the switch open at t = 1 ms. The diode's anode is ground and its cathode is node a, so it only conducts when a goes below ground.

```
  without a diode       lowest V(a) =   -951.92 V, current falls to 36.8 %    11.0 us after opening
  with flyback diode    lowest V(a) =     -0.77 V, current falls to 36.8 %   886.0 us after opening
  energy that must go somewhere: 1/2 L I^2 = 0.50 mJ
```

Without the diode: nearly -1000 V (the simulator's 1 µs time step lands just after the very peak, which is why it shows -952 V rather than exactly -1000 V), and the current is gone in about 11 µs, close to the predicted 10 µs. With the diode: the voltage never goes below -0.77 V, and the current takes 886 µs to fall to 36.8 %, a little less than the 1 ms of L / Rcoil because the diode's own voltage drop helps absorb the energy.

### Step 5: The picture

`save_plot` draws the source, the resistor voltage and the inductor current against time into `out.png`. You see the exponential rise, the flat top, and the exponential fall after 6 ms, with the formula's dotted curve lying exactly on the simulator's line.

## Use It

- **Relay drivers.** Any datasheet for a relay or a transistor relay driver (for example the ULN2003 Darlington array used to drive relays and stepper motors) shows a diode from each output to the coil supply. The ULN2003 has these "clamp diodes" built in; its pin 9 (COM) must be connected to the coil supply for them to work.
- **Release time.** A flyback diode slows the release of a relay, because the current decays with tau = L / R instead of in microseconds. Where fast release matters, designers put a Zener diode or resistor in series with the flyback diode: the clamp voltage is then higher (say 24 V instead of 0.7 V), and the energy is absorbed faster. That is a deliberate trade between speed and voltage stress.
- **Ignition coils** use the kick: interrupting a few amperes in the primary in microseconds, and the transformer action of Lesson 06 multiplies the voltage further.
- **Motors and solenoids** in robots, printers and cars all need flyback paths. In an H-bridge motor driver (Phase 18) the flyback diodes are built into the MOSFETs.
- **Inrush and settling.** A large inductor in a power supply input limits how fast current can rise at switch-on, protecting fuses and switches.

## Try It in the Lab

Open **"Set the RL time constant to 1 ms"**. A 10 V step drives a fixed 100 mH coil, and you must choose the series resistor so the resistor's voltage reaches 6.32 V (63.2 % of 10 V) in about 1 ms and is settled above 9.5 V at 6 ms. Before running, compute tau = L / R for every resistor in the drawer. Then think: one wrong resistor makes the circuit too fast; the other makes it too slow. Which is which, and does that match your intuition from RC circuits? (It should not!)

## Common Mistakes

- **Writing tau = R x L or tau = R / L.** For RL it is L / R. Check the units: H / ohm = seconds.
- **Assuming bigger R means slower, as with capacitors.** In RL circuits it means faster (and a smaller final current).
- **Forgetting that the current is continuous at a switching instant.** Every transient problem starts with "the current through the inductor just after equals the current just before".
- **Thinking the inductor voltage keeps its sign.** During the rise v_L is positive; after the source drops it is negative. The inductor switches from absorbing energy to giving it back.
- **Switching an inductor off with nowhere for the current to go.** Without a flyback path, the voltage spike will find one: through your transistor, your switch contacts or your microcontroller.
- **Putting the flyback diode the wrong way round.** Pointing the wrong way, it short-circuits the supply as soon as you switch on. The cathode goes to the positive end of the coil.

## Exercises

1. **Easy.** Find tau and the final current for a 24 V source, a 50 mH coil and a 12 ohm resistor. What is the current after 2 tau?
2. **Easy.** Which resistor gives tau = 0.5 ms with a 220 mH inductor?
3. **Medium.** A coil of 0.25 H and 50 ohm is connected to 5 V. How long until the current reaches 90 mA? (Hint: find the final current first; then solve 1 - e^(-t/tau) = fraction using the natural logarithm.)
4. **Medium.** In `simulate_switch_off`, change Rleak from 10 k ohm to 100 k ohm (keep no diode). Predict the peak voltage and the decay time before running. Then change the simulation step to 0.1 µs and see the peak get closer to the prediction.
5. **Hard.** Replace the flyback diode with a 100 ohm resistor across the coil (from a to ground). It clamps the kick to about -10 V. But it also wastes power while the relay is on. Compute that waste with the switch closed, compare it with the coil's own power, and explain why a diode is better.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| RL time constant | "How fast the coil charges" | tau = L / R, the time to cover 63.2 % of the change in current |
| Transient | "The switching bit" | The exponential adjustment between two steady states after a change |
| Steady state | "When it has settled" | After about 5 tau: the inductor current is V/R and the inductor voltage is 0 |
| Inductive kick | "The coil spike" | The voltage L di/dt produced when an inductor's current is interrupted; can be hundreds of times the supply |
| Flyback diode | "The protection diode" | A diode across an inductor, reverse-biased in normal use, that gives the current a path when switched off and clamps the voltage near -0.7 V |
| Exponential decay | "It dies away" | Falling by the same fraction (63.2 %) every tau, never quite reaching zero |

## Further Reading

- [All About Circuits, Volume I, Chapter 16: RC and L/R Time Constants](https://www.allaboutcircuits.com/textbook/direct-current/chpt-16/inductor-transient-response/) — inductor transient response with worked tables
- [MIT OpenCourseWare 6.002, lectures on first-order transients](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) — the RC and RL equations solved side by side
- [The Art of Electronics (Horowitz & Hill), 3rd edition, chapter 1, the section on inductive loads and diode protection](https://artofelectronics.net/) — why every relay coil needs a diode
- [ULN2003A datasheet (Texas Instruments)](https://www.ti.com/product/ULN2003A) — a real relay driver with built-in clamp diodes
