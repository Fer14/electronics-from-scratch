# Faraday's Law and Induction

> A magnetic field that stays still does nothing to a wire. A magnetic field that *changes* pushes a voltage around it.

**Type:** Learn
**Prerequisites:** Phase 08 (Magnetism and Inductors), Lesson 01 (Magnets and Magnetic Fields) and Lesson 02 (Electromagnetism); Phase 07 (Capacitors), Lesson 08 (Transient Simulation from Scratch)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Induction | Making a voltage in a wire by changing the magnetic field through it | Waving a magnet near a coil makes the needle of a meter twitch |
| Magnetic flux (Phi) | How much magnetic field passes *through* a surface: field strength times area, counting only the part that goes straight through | How much rain falls through an open window: depends on how hard it rains, how big the window is, and its angle |
| Weber (Wb) | The unit of flux: 1 Wb = 1 T x 1 m² | A "litre of rain through the window", but for field |
| EMF (electromotive force) | A voltage created by something other than a battery's chemistry, here by changing flux; measured in volts | The push a pump gives to water, even though it is not a "force" in newtons |
| Flux linkage | The flux through one turn times the number of turns, N x Phi | Twenty windows in a row, each catching the same rain |
| Lenz's law | The induced current always flows so as to *oppose* the change that caused it | A door spring that pushes back whichever way you swing the door |
| Eddy currents | Swirling currents induced inside a chunk of metal by a changing field | Whirlpools in a river behind a rock |
| Generator | A machine that turns motion into voltage by moving coils and magnets relative to each other | A bicycle dynamo |
| Rate of change | How fast something changes per second, written d(something)/dt | A car's speed is the rate of change of its position |

## Learning Objectives

- Define magnetic flux and compute it for a coil at different angles to a field
- State Faraday's law (EMF = -N dPhi/dt) and use it to compute induced voltages from changes in field, area or angle
- Explain Lenz's law with energy conservation and predict the direction of induced current
- Show numerically that a coil spinning in a field produces a sine wave whose peak is N B A omega
- Simulate the voltage pulses of a magnet falling through a coil and a generator lighting a lamp

## The Problem

Lesson 02 showed that a current makes a magnetic field. In 1821, Michael Faraday asked the obvious question: can a magnetic field make a current? He put strong magnets next to wires and coils and watched a sensitive meter. Nothing. For ten years, on and off, nothing happened.

The breakthrough, on 29 August 1831, was that a field does make a current, but **only while it is changing**. Faraday wound two coils on an iron ring. When he connected a battery to the first coil, the meter on the second coil kicked, then went back to zero. When he disconnected the battery, it kicked the other way. A steady current in the first coil did nothing at all to the second. Only *switching on* and *switching off* mattered.

This single discovery runs the modern world. Every power station spins magnets past coils (generators). Every transformer that steps voltage up and down (Lesson 06) works by it. Every inductor (Lesson 04) resists changes in current because of it. Wireless chargers, induction hobs, electric guitar pickups, metal detectors, card readers and the magnetic brakes of roller coasters are all applications. If you understand this lesson, half of electrical engineering opens up.

## The Physics

### Flux: how much field goes through a loop

Picture a loop of wire as a window and the magnetic field lines as rain. The amount of "rain" passing through the window depends on three things: how strong the field is (B), how big the window is (area A), and its angle. A window facing the rain catches the most; a window edge-on to the rain catches none.

That amount is the **magnetic flux**, written with the Greek letter Phi (Φ, say "fye" or "fee"):

```
Phi = B * A * cos(angle)
```

Read it aloud: "flux equals field times area times the cosine of the angle". The angle is measured between the field and the line sticking straight out of the loop (its *normal*). At 0 degrees the field goes straight through, cos(0) = 1, maximum flux. At 90 degrees the field skims along the loop's surface, cos(90°) = 0, no flux.

```
   angle 0: field straight through     angle 90: field along the loop
      |  |  |  |                          ------------------>
     +----------+                         +----------+  (edge view)
     |  |  |  | |   Phi = B A             ------------------>
     +----------+                          Phi = 0
      |  |  |  |
```

Flux is measured in **webers (Wb)**, after Wilhelm Weber. 1 Wb = 1 T x 1 m².

**Worked example.** A square loop 2 cm x 2 cm has area A = 0.02 x 0.02 = 0.0004 m² (4 cm²). In a field of 0.3 T straight through it: Phi = 0.3 x 0.0004 = 0.00012 Wb = 120 µWb. Tilt it to 60 degrees: cos(60°) = 0.5, so Phi = 60 µWb. Edge-on (90 degrees): 0.

A coil with N turns catches the same flux in each turn, so the total, called the **flux linkage**, is N x Phi.

### Faraday's law: change makes voltage

Faraday's law says:

> The EMF induced in a coil equals the number of turns times how fast the flux through it changes, with a minus sign.

```
EMF = -N * dPhi/dt
```

The symbol `dPhi/dt` means "the rate of change of Phi with time": how many webers per second the flux is changing *right now*. If you have not met this notation, think of it as a speed: if your position changes by 30 m in 2 s, your speed is 30/2 = 15 m/s. Same idea: if the flux changes by 120 µWb in 0.05 s, its rate of change is 120e-6 / 0.05 = 0.0024 Wb/s. For changes that happen steadily, we can use the **average** version:

```
EMF = -N * (Phi_after - Phi_before) / (time taken)
```

Units: Wb/s is the same as volts. (1 Wb = 1 T·m², and from Lesson 01, 1 T = 1 N/(C·m/s); working it through gives 1 Wb/s = 1 J/C = 1 V.)

**EMF** stands for *electromotive force*, an old name. It is not a force in newtons; it is a voltage, in volts. We use the word EMF to say "a voltage created by some process" (here, changing flux; in a battery, chemistry) as opposed to the voltage *drop* across a resistor.

**Worked example.** A coil of 200 turns, each 2 cm x 2 cm. A magnet is pushed up to it and the field through it rises from 0 to 0.3 T in 50 ms (0.05 s).

- Change in flux per turn: 120 µWb - 0 = 120e-6 Wb.
- Rate: 120e-6 / 0.05 = 0.0024 Wb/s.
- EMF = -200 x 0.0024 = -0.48 V.

Push the magnet ten times faster (5 ms) and the EMF is ten times bigger: -4.8 V. Push it slowly over half a second: only -0.048 V. **The voltage depends on how fast you change the flux, not on how big the field is.** Pull the magnet away again in 50 ms and you get +0.48 V: the sign flips.

### Three ways to change the flux

Since Phi = B x A x cos(angle), there are three knobs, and every induction device uses one of them:

1. **Change B.** Move a magnet towards or away from the coil, or change the current in a nearby coil. That is the transformer (Lesson 06): an AC current in one coil makes a changing field through another coil.
2. **Change A.** Slide part of the circuit so the loop gets bigger or smaller. A metal rod rolling along two rails in a field sweeps out area. The EMF works out to

   ```
   EMF = B * L * v
   ```

   "field times length of rod times its speed". With B = 0.5 T, L = 10 cm, v = 2 m/s: EMF = 0.5 x 0.1 x 2 = 0.1 V. This is called *motional EMF*, and it is the same physics as the Lorentz force of Lesson 01: the free electrons in the moving rod are moving charges in a field, so they get pushed along the rod.
3. **Change the angle.** Spin the coil in a steady field. That is the generator in every power station, and it is the next section.

### Spinning a coil: where AC comes from

Put a coil of N turns and area A in a uniform field B and spin it at a steady rate of f turns per second. The angle grows steadily: angle = omega x t, where **omega** (Greek letter ω) is the **angular speed** in radians per second, omega = 2 pi f. (One full turn is 2 pi radians, about 6.283.) So the flux linkage is

```
N * Phi(t) = N * B * A * cos(omega * t)
```

Its rate of change gives the EMF:

```
EMF(t) = N * B * A * omega * sin(omega * t)
```

You do not need calculus to trust this: the code computes the slope of the cosine numerically and finds the sine. The **peak** EMF is N B A omega.

**Worked example.** 100 turns, B = 0.1 T, area 10 cm x 10 cm = 0.01 m², spinning at 50 turns per second (f = 50 Hz).

- omega = 2 x pi x 50 = 314.16 rad/s.
- Peak EMF = 100 x 0.1 x 0.01 x 314.16 = 31.42 V.

Look at the timing:

| Time | Coil angle | Flux | EMF |
|---|---|---|---|
| 0 ms | 0° (facing the field) | maximum | 0 |
| 5 ms | 90° (edge-on) | 0 | +31.4 V (maximum) |
| 10 ms | 180° | minimum (negative) | 0 |
| 15 ms | 270° | 0 | -31.4 V |

The EMF is biggest when the flux is *zero*, because that is when the flux is changing fastest. And the EMF is zero when the flux is at its peak, because at the top of a hill the slope is flat. This quarter-cycle offset between flux and voltage will come back in Phase 09 as **phase**.

The output keeps alternating between + and -: it is **alternating current (AC)**, and 50 Hz is the mains frequency in Europe (60 Hz in the Americas). Phase 09 is all about AC.

### Lenz's law: nature pushes back

What about the minus sign? It encodes **Lenz's law** (Heinrich Lenz, 1834):

> The induced current flows in the direction that **opposes the change** in flux that produced it.

Push the north pole of a magnet towards a coil. The flux through the coil grows. The induced current flows in the direction that makes the coil's own field point *against* the incoming magnet: the coil's near end becomes a north pole, which **repels** the magnet. You have to push harder. Pull the magnet away and the induced current reverses: the coil's near end becomes a south pole, which **attracts** the magnet back. You have to pull harder.

Why must it be this way? **Energy conservation.** The induced current heats the wire (P = I² R) and could light a lamp. That energy must come from somewhere: from the work you do against the push. If the sign were the other way, the coil would *pull* the magnet in, which would make the flux change faster, which would make more current, which would pull harder... an endless free-energy machine. Nature does not allow it. The minus sign is the universe refusing to give energy for free.

A beautiful demonstration: drop a strong magnet down a vertical copper pipe. Copper is not magnetic, yet the magnet falls in slow motion. The falling magnet changes the flux through every ring of the pipe; swirling **eddy currents** flow in the copper and their field opposes the motion. The magnet's lost gravitational energy becomes heat in the pipe.

### The falling magnet, step by step

Let a small magnet fall through a coil along its axis. As it approaches, the flux through the coil rises; as it passes the centre, the flux is at its maximum and momentarily not changing; as it leaves, the flux falls. So the EMF is:

```
 EMF
  |               _
  |              / \        second pulse: opposite sign, taller and
  |             /   \       narrower because the magnet is faster
  +------------/-----\-------------------------->  time
  |   \       /
  |    \_____/   first pulse (flux rising)
  |
```

Two pulses of opposite sign, with zero at the moment the magnet is in the middle. The second pulse is bigger because the magnet has accelerated while falling: same change in flux, done faster. The code computes this curve with real numbers.

## The Concept

The whole lesson fits on one card:

```
  flux            Phi = B * A * cos(angle)                  [Wb]
  Faraday         EMF = -N * dPhi/dt                         [V]
  average form    EMF = -N * (Phi_after - Phi_before) / dt   [V]
  moving rod      EMF = B * L * v                            [V]
  spinning coil   EMF(t) = N * B * A * omega * sin(omega t)  [V], omega = 2 pi f
  Lenz            the induced current opposes the change
```

Two consequences we will build on immediately:

1. **A coil induces a voltage in itself.** A current in a coil makes a field through that same coil (Lesson 02). If the current changes, that field changes, so the coil's own flux changes, so Faraday's law induces an EMF in the coil itself, and by Lenz's law it opposes the change in current. That self-opposition is **inductance**, the subject of Lesson 04.
2. **A coil induces a voltage in a neighbour.** Two coils sharing a core share flux. A changing current in one induces an EMF in the other. That is the **transformer**, Lesson 06.

## Build It

### Step 1: Flux

```python
def flux(field, area, angle_deg=0.0):
    return field * area * np.cos(np.radians(angle_deg))
```

`np.radians` converts degrees to radians because `np.cos` works in radians. The output for our 2 cm x 2 cm loop in 0.3 T: 120 µWb at 0°, 60 µWb at 60°, 0 at 90°.

### Step 2: Average EMF

```python
def average_emf(turns, flux_before, flux_after, seconds):
    return -turns * (flux_after - flux_before) / seconds
```

The output shows -0.05 V, -0.48 V and -4.80 V for the same flux change done in 500, 50 and 5 ms, and +0.48 V when the field is removed in 50 ms.

### Step 3: Motional EMF

```python
def motional_emf(field, length, speed):
    return field * length * speed
```

0.05, 0.10 and 0.25 V for 1, 2 and 5 m/s: voltage proportional to speed. This is exactly how a bicycle dynamo's lamp gets brighter as you pedal faster.

### Step 4: The spinning coil, by numerical slope

```python
def rotating_coil_flux(turns_area_field, omega, t):
    return turns_area_field * np.cos(omega * t)


def numerical_derivative(values, t):
    return np.gradient(values, t)


t = np.linspace(0, 2 / freq, 4001)
linked = rotating_coil_flux(turns * field * coil_area, omega, t)
emf = -numerical_derivative(linked, t)
```

`np.gradient` computes the slope between neighbouring samples, the same "small steps" idea as Phase 07 Lesson 08. We never wrote the sine formula into the code: the sine comes out of the slope of the cosine. The result:

```
  peak EMF from the numerical derivative: 31.42 V
  peak EMF predicted N B A omega:          31.42 V
  at t =  5.0 ms: flux linkage    0.00 mWb-turns, EMF   31.42 V
  at t = 10.0 ms: flux linkage -100.00 mWb-turns, EMF   -0.00 V
```

(At t = 0 the script prints 0.05 V instead of exactly 0. At the very first sample `np.gradient` can only look forward one step, so its slope is slightly off. A good reminder that numerical derivatives have small errors at the edges.)

### Step 5: The falling magnet

The flux that a small magnet (moment m) sends through a loop of radius R when it sits on the loop's axis at distance z is

```
Phi = mu0 * m * R^2 / (2 (R^2 + z^2)^(3/2))
```

which has exactly the same shape as the field of a current loop from Lesson 02. That is not a coincidence (it follows from a symmetry called *reciprocity*), but here we just use it.

```python
def falling_magnet_emf(moment, loop_radius, turns, drop_height, duration, steps):
    t = np.linspace(0, duration, steps)
    z = drop_height - 0.5 * G * t**2
    linked = turns * dipole_flux_through_loop(moment, loop_radius, z)
    return t, z, -numerical_derivative(linked, t)
```

The magnet (our 1 cm neodymium cube from Lesson 01, m = 1.035 A·m²) is dropped from 10 cm above a 50-turn coil of radius 1.5 cm. Free fall: z = 0.10 - ½ x 9.81 x t². Output:

```
  magnet crosses the coil at t = 142.8 ms at 1.40 m/s
  approaching: peak EMF  -167.2 mV at t = 137.5 ms
  leaving:     peak EMF  +180.3 mV at t = 148.2 ms
  EMF exactly at the centre: -0.24 mV
```

Check the crossing: ½ x 9.81 x t² = 0.10 gives t = sqrt(0.2 / 9.81) = 0.1428 s, and speed = 9.81 x 0.1428 = 1.40 m/s. The two pulses have opposite signs, and the leaving pulse is larger because the magnet is moving faster. (We ignore the small braking force of Lenz's law here; with the coil open, no current flows, so there is no braking at all.)

### Step 6: The generator lights a lamp

Our spinning coil makes 31.42 V peak at 50 Hz. Connect a 100 ohm lamp and let our simulator run it:

```python
def lamp_on_generator(peak_volts, freq, lamp_ohms):
    c = Circuit()
    c.sine_source("Vgen", "a", "0", amplitude=peak_volts, freq=freq)
    c.resistor("Rlamp", "a", "0", lamp_ohms)
    run = c.transient(t_stop=4 / freq, dt=1 / freq / 2000)
    current = np.asarray(run.i("Rlamp"))
    voltage = np.asarray(run.v("a"))
    last_cycle = np.asarray(run.time) >= 3 / freq
    return current[last_cycle].max(), np.mean((voltage * current)[last_cycle])
```

The ideal sine source stands in for the coil (we ignore the coil's own resistance and inductance). Peak current is 31.42 / 100 = 0.314 A. The **average** power, measured over the last full cycle, is 4.93 W, which is exactly *half* of the peak power 31.42² / 100 = 9.87 W. Why half? Because the power goes up and down with the sine squared, and the average of sine squared is ½. Phase 09, Lesson 03 (RMS values) is built on that one fact.

## Use It

- **Power stations.** Large generators spin electromagnets (the *rotor*) inside fixed coils (the *stator*) at 3000 rpm (50 Hz) or 3600 rpm (60 Hz), producing tens of thousands of volts.
- **Electric guitar pickups.** A magnet under each string magnetises it; the vibrating steel string changes the flux through a coil of thousands of turns of hair-thin wire, producing a few hundred millivolts that follow the string's motion.
- **Induction hobs** drive a coil at 20 to 100 kHz. The changing field induces large eddy currents in the bottom of a steel pan, which heats up. A glass hob stays cool because glass does not conduct.
- **Wireless phone chargers** (the Qi standard) use two flat coils, one in the pad and one in the phone, coupled by flux at around 100 to 200 kHz.
- **Card readers and NFC** work the same way at 13.56 MHz, harvesting enough energy from the reader's field to power the chip in the card.
- **Eddy current brakes** on trains and roller coasters use strong magnets near a metal fin: no contact, no wear, braking force grows with speed.
- **Transformer cores are laminated** (made of thin insulated sheets) precisely to *stop* eddy currents, which would otherwise waste energy as heat. You will meet this in Lesson 06.

## Common Mistakes

- **Thinking a strong field alone induces voltage.** A huge but steady field induces nothing in a still coil. Only the *rate of change* of flux matters.
- **Forgetting the angle.** A coil edge-on to the field has zero flux, however strong the field.
- **Confusing flux with field.** B is per square metre; flux is B times area. A big loop in a weak field can have more flux than a tiny loop in a strong field.
- **Ignoring the turns.** N turns give N times the EMF. That is why pickup coils have thousands of turns.
- **Getting Lenz's law backwards.** The induced current never helps the change; it always opposes it. If you get "helps", check the energy: it would be a perpetual motion machine.
- **Thinking the EMF is biggest when the flux is biggest.** In the spinning coil the EMF is biggest when the flux is passing through zero, because that is when it changes fastest.

## Exercises

1. **Easy.** A circular coil of radius 3 cm sits in a 0.2 T field at 30 degrees from the field. Find its area and the flux through it.
2. **Easy.** A 500-turn coil sees its flux per turn drop from 80 µWb to 20 µWb in 10 ms. Find the average EMF and its sign.
3. **Medium.** A bicycle dynamo has 400 turns, a magnet giving 0.08 T and a coil area of 2 cm². At what rotation frequency does it reach a 6 V peak? Convert to revolutions per minute.
4. **Medium.** In `main.py`, drop the magnet from 30 cm instead of 10 cm. Predict how the crossing speed and the size of the pulses change before running it (hint: speed grows as the square root of the height).
5. **Hard.** A 0.5 T field passes through a single rectangular loop of resistance 0.1 ohm. One side of the loop, 10 cm long, slides outwards at 2 m/s. Find the EMF, the current, the force the field puts on the sliding side (F = B I L, Lesson 02), and the mechanical power you need to keep it moving. Compare with the electrical power I² R. What does the comparison tell you about Lenz's law?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Magnetic flux | "How much magnetism goes through" | Phi = B A cos(angle), in webers; the field times the area it crosses straight on |
| Faraday's law | "Moving magnets make electricity" | EMF = -N dPhi/dt: the induced voltage equals the turns times the rate of change of flux |
| Lenz's law | "The minus sign" | The induced current opposes the change that caused it, which is energy conservation in action |
| EMF | "Voltage" | A voltage produced by a non-resistive process (changing flux, chemistry), measured in volts |
| Flux linkage | "Flux times turns" | N x Phi, the quantity whose rate of change gives the EMF of a coil |
| Eddy currents | "Currents in the metal" | Loops of current induced inside solid conductors by changing flux, which waste energy as heat or provide braking |
| Generator | "Makes electricity" | A machine that changes the flux through coils by motion, converting mechanical work into electrical energy |

## Further Reading

- [The Feynman Lectures on Physics, Vol. II, Chapter 16 (Induced Currents) and Chapter 17 (The Laws of Induction)](https://www.feynmanlectures.caltech.edu/II_toc.html) — the deepest friendly treatment of why induction works
- [Khan Academy: Faraday's law and Lenz's law](https://www.khanacademy.org/science/physics/magnetic-forces-and-magnetic-fields) — short videos with worked examples
- [HyperPhysics: Faraday's law and Lenz's law](http://hyperphysics.phy-astr.gsu.edu/hbase/electric/farlaw.html) — compact pages with generators and motional EMF
- [Royal Institution: Faraday's induction ring](https://www.rigb.org/explore-science/explore/collection/michael-faradays-ring-coil-apparatus) — the original 1831 apparatus is still on display in London
