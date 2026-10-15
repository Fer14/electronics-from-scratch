# Motors and Generators

> A motor and a generator are the same machine. Push current in and it turns; turn it and current comes out. The back-EMF is the generator hiding inside every running motor.

**Type:** Learn
**Prerequisites:** Phase 08 (Magnetism and Inductors), Lessons 02 (Electromagnetism), 03 (Faraday's Law and Induction) and 05 (RL Transients)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Motor | A machine that turns electrical energy into rotation | The thing that spins a fan, a drill or a toy car's wheels |
| Generator | A machine that turns rotation into electrical energy | A bicycle dynamo, a wind turbine, a power station |
| Torque | A turning force: force times the distance from the axle, in newton-metres (N·m) | How hard a spanner twists a bolt |
| Rotor / stator | The part that spins / the part that stays still | The wheel and the frame of a bicycle |
| Armature | The coil (winding) of a motor that carries the main current | The copper windings you see when you open a small motor |
| Commutator | A split ring with brushes that reverses the coil's current every half turn | A railway turntable that flips the tracks as the train comes round |
| Brushes | Carbon or metal contacts that rub on the commutator to feed current to the spinning coil | The pickup shoe on an electric train |
| Back-EMF | The voltage a spinning motor generates in its own winding, opposing the supply | The headwind you make yourself by cycling faster |
| Stall | The motor is powered but held still, so it draws its largest current | Pushing against a wall with all your strength |
| Motor constant (k) | Volts generated per rad/s of speed, which equals N·m of torque per ampere | A gear ratio between the electrical and the mechanical world |
| rad/s and rpm | Two units of rotation speed: radians per second, revolutions per minute (1 rev = 2 pi rad) | 1000 rpm = 104.7 rad/s |

## Learning Objectives

- Explain how the force on a current in a magnetic field becomes a torque on a coil, and why a commutator is needed
- Explain back-EMF and derive the motor equation V = I R + k omega
- Calculate stall current, stall torque, no-load speed and efficiency of a DC motor from its constants
- Simulate a motor spinning up and see the current fall as the back-EMF grows
- Use the same machine as a generator and see that electrical load becomes mechanical braking

## The Problem

A small DC motor from a toy or a robot kit has two wires. Connect it to a 12 V battery and it spins. That seems simple until you measure the current: at the instant you connect it, the motor draws 6 A; a quarter of a second later, spinning freely, it draws 30 mA. Grab the shaft to slow it down and the current climbs again. Stop it completely and 6 A flows until something gets hot.

Why does the same winding, with the same resistance, draw two hundred times less current when it spins? If you design a battery pack, a fuse, a motor driver chip or a transistor switch for a motor and do not know the answer, you will choose parts that are too weak for the start-up or far too big for the running current. The answer is that a spinning motor is also a generator, and the voltage it generates pushes back against the battery. This lesson builds that idea from the forces of Lesson 02 and the induction of Lesson 03.

## The Physics

### From force to torque

Lesson 02: a wire of length L carrying current I across a field B feels a sideways force F = B I L. Bend the wire into a rectangular loop and put it between the poles of a magnet, with the loop free to rotate on an axle:

```
          N pole
     ---------------
           F up
         ^
    +----|----+        the two long sides carry current
    |  side 1 |        in opposite directions, so the forces
    |    o    |  <- axle   are opposite: one up, one down
    |  side 2 |
    +----|----+        opposite forces on opposite sides of the
         v             axle make a TURNING force, a torque
           F down
     ---------------
          S pole
```

The two long sides carry current in opposite directions (it goes up one side and comes back down the other), so they are pushed in opposite directions. Two opposite forces on opposite sides of an axle make the loop **turn**. The turning effect is **torque**, force times its distance from the axle, measured in newton-metres (N·m).

For a coil of N turns and area A, the torque is

```
T = N * B * I * A * sin(angle)
```

"torque equals turns times field times current times area times the sine of the angle", where the angle is between the field and the line sticking straight out of the coil. It is biggest when the coil's plane is *along* the field (90°) and zero when the coil faces the field squarely (0°).

**Worked example.** 50 turns, B = 0.4 T, I = 1 A, A = 10 cm² = 0.001 m², at 90°: T = 50 x 0.4 x 1 x 0.001 = 0.02 N·m = 20 mN·m. At 45° it is 20 x 0.707 = 14.1 mN·m. At 0° it is zero.

### The commutator

There is a problem. When the coil turns past 0° (facing the field), sin(angle) changes sign and the torque reverses: the coil would rock back and forth and stop. The fix, invented in the 1830s, is the **commutator**: a ring split into two halves fixed to the axle, with two stationary **brushes** pressing on it. Every half turn, just as the torque would reverse, the brushes swap to the other halves of the ring and the current in the coil reverses. The torque keeps pointing the same way.

```
    brush  +  ->  [ half A | half B ]  <-  brush -
                   (ring spins with the coil;
                    every half turn the halves swap brushes)
```

Real motors use several coils at different angles and a commutator with many segments, so the torque is smooth instead of pulsing. **Brushless** motors (in drones, computer fans, electric cars) replace the mechanical commutator with transistors that switch the coils electronically (Phase 18).

### Back-EMF: the motor is also a generator

Here is the key insight. A spinning coil in a magnetic field is exactly the generator of Lesson 03: its flux changes, so an EMF is induced in it. **When a motor spins, it generates a voltage in its own winding.** By Lenz's law, that voltage opposes the current that is making it spin. It is called the **back-EMF**, and it is proportional to the speed:

```
E_back = k * omega
```

"the back-EMF equals the motor constant times the angular speed". omega (ω) is the speed in **radians per second** (one revolution is 2 pi radians, so 1 rpm = 2 pi / 60 = 0.1047 rad/s). **k** is the **motor constant** in volts per rad/s.

And here is a small miracle. The same k sets the torque per ampere:

```
T = k * I
```

The volts-per-rad/s and the newton-metres-per-ampere are the same number in SI units. This is energy conservation: the electrical power absorbed by the back-EMF, E_back x I = k omega I, must equal the mechanical power delivered, T x omega = k I omega. They match only if the same k appears in both.

### The motor equation

Model the motor as its winding resistance R and inductance L in series with the back-EMF voltage source:

```
   +12 V ---[ R = 2 ohm ]---[ L = 1 mH ]---( E_back = k omega )--- 0 V
              (winding wire)  (winding coil)  (generator inside)
```

Kirchhoff's voltage law, once the current has settled (inductor = wire, Lesson 04):

```
V = I * R + k * omega
```

"the supply voltage equals the drop in the winding resistance plus the back-EMF". So the current is

```
I = (V - k * omega) / R
```

Everything about DC motors follows from this one line:

- **At stall** (omega = 0): no back-EMF, I = V / R. This is the largest current, and the largest torque. Our motor: I = 12 / 2 = 6 A, torque k I = 0.02 x 6 = 0.12 N·m.
- **At full speed with no load**: the motor speeds up until the back-EMF almost equals the supply, leaving just enough current to overcome friction. Ignoring friction, omega = V / k = 12 / 0.02 = 600 rad/s = 5730 rpm. With a little friction (b = 1e-6 N·m per rad/s) it settles at 597 rad/s, drawing only 30 mA.
- **In between**: a load torque T_load needs a current I = T_load / k. That current causes a drop I R in the winding, so the back-EMF is V - I R, and the speed is (V - I R) / k. **More load, more current, lower speed.**

That is why the current falls from 6 A to 30 mA as the motor spins up: the back-EMF grows with speed and cancels most of the supply voltage.

### Efficiency

The supply delivers V x I. The winding resistance turns I² R into heat. The rest, E_back x I, becomes mechanical power. Efficiency = E_back / V:

| Load torque | Current | Back-EMF | Speed | Heat I² R | Mechanical | Efficiency |
|---|---|---|---|---|---|---|
| 10 mN·m | 0.5 A | 11 V | 5252 rpm | 0.5 W | 5.5 W | 91.7 % |
| 30 mN·m | 1.5 A | 9 V | 4297 rpm | 4.5 W | 13.5 W | 75.0 % |
| 60 mN·m | 3.0 A | 6 V | 2865 rpm | 18 W | 18 W | 50.0 % |

Check the 30 mN·m line: I = 0.03 / 0.02 = 1.5 A; I R = 3 V; back-EMF 12 - 3 = 9 V; speed 9 / 0.02 = 450 rad/s = 4297 rpm; heat 1.5² x 2 = 4.5 W; mechanical 9 x 1.5 = 13.5 W; efficiency 9 / 12 = 75 %. At half the stall torque (60 mN·m) the mechanical power is at its maximum but half the input is wasted as heat. This is maximum power transfer (Phase 05, Lesson 07) again: the back-EMF source "sees" the winding resistance as its source resistance.

### Two time constants

Starting a motor involves two very different time scales:

- **Electrical**: tau_e = L / R = 0.001 / 2 = 0.5 ms. The current can rise this fast (Lesson 05).
- **Mechanical**: tau_m = J R / k², where J is the rotor's **moment of inertia** (its resistance to being spun up, in kg·m²). For J = 1e-5 kg·m²: tau_m = 1e-5 x 2 / 0.0004 = 0.05 s = 50 ms.

The current rises to nearly its stall value in about a millisecond, before the rotor has time to move; then over tens of milliseconds the rotor speeds up, the back-EMF grows, and the current falls. That initial surge is the **inrush current**.

### Generators: the same machine run backwards

Disconnect the battery and turn the shaft by hand at 300 rad/s. The back-EMF is now the output: E = k omega = 0.02 x 300 = 6 V. Connect a load resistor R_load:

```
   ( E = k omega )---[ R_w = 2 ohm ]---+---[ R_load ]--- back to E
```

The current is I = E / (R_w + R_load). With 10 ohm: I = 6 / 12 = 0.5 A, V_out = 0.5 x 10 = 5 V, P_load = 2.5 W, winding loss 0.5 W.

And here is Lenz's law in action: the current in the winding produces a torque T = k I = 0.02 x 0.5 = 0.01 N·m, which opposes your turning. You must supply mechanical power T x omega = 0.01 x 300 = 3 W, exactly the 2.5 W in the load plus the 0.5 W in the winding. **Electrical load becomes mechanical braking.** Lower the load resistance to 2 ohm and the current triples, and so does the braking torque: a generator gets harder to turn the more power you take from it. Short the motor's terminals and spin the shaft: it feels "sticky". Electric cars use exactly this for *regenerative braking*, charging the battery while slowing the car.

### Switching a motor off

The winding is an inductor. If a transistor or switch interrupts 6 A in a 1 mH winding, Lesson 05 applies: the voltage spikes to whatever it takes to keep the current flowing. Every motor driver needs a flyback path. That is the lab for this lesson.

## The Concept

The DC motor on one card:

```
  torque from current       T = k * I
  back-EMF from speed       E = k * omega
  winding equation          V = I * R + L dI/dt + k * omega
  steady current            I = (V - k omega) / R
  stall                     I = V / R,  T = k V / R
  no-load speed             omega = V / k   (minus a little for friction)
  mechanical power          P = T * omega = E * I
  efficiency                E / V
  time constants            L / R (electrical),  J R / k^2 (mechanical)
```

**Worked example: sizing a driver.** A 24 V motor has R = 1.2 ohm and k = 0.05. Stall current: 24 / 1.2 = 20 A. Even if the motor normally runs at 2 A, the driver (and the fuse, and the battery) must survive 20 A at every start, or limit the current. Running at 2 A: back-EMF = 24 - 2.4 = 21.6 V, speed = 21.6 / 0.05 = 432 rad/s = 4125 rpm, torque = 0.05 x 2 = 0.1 N·m, efficiency 90 %.

## Build It

### Step 1: Torque on a loop

```python
def loop_torque(turns, field, current, area, angle_deg):
    return turns * field * current * area * np.sin(np.radians(angle_deg))
```

Output: 20.00 mN·m at 90°, 14.14 at 45°, 0 at 0°.

### Step 2: Key numbers

```python
def no_load_speed(volts, k, resistance, friction):
    return volts * k / (k**2 + resistance * friction)
```

This comes from the steady state with only friction as load: I = b omega / k and V = I R + k omega, solved for omega. The script prints: stall current 6.0 A, stall torque 120 mN·m, no-load speed 597.0 rad/s = 5701 rpm, no-load current 29.9 mA, electrical tau 0.50 ms, mechanical tau 50.0 ms.

### Step 3: Spin-up, step by step

```python
def spin_up(volts, load_torque, t_stop, dt):
    steps = int(round(t_stop / dt))
    t = np.arange(steps + 1) * dt
    current = np.zeros(steps + 1)
    speed = np.zeros(steps + 1)
    for n in range(steps):
        back_emf = MOTOR_CONSTANT * speed[n]
        di = (volts - WINDING_OHMS * current[n] - back_emf) / WINDING_HENRIES
        current[n + 1] = current[n] + di * dt
        torque = MOTOR_CONSTANT * current[n + 1] - FRICTION * speed[n] - load_torque
        speed[n + 1] = speed[n] + torque / INERTIA * dt
    return t, current, speed
```

Two equations advance together in small steps of 10 µs (the Euler method from Phase 07, Lesson 08): the electrical one (L di/dt = V - I R - k omega) and the mechanical one (J domega/dt = k I - friction - load). Our simulator handles electrical circuits, not spinning rotors, so this coupled electro-mechanical part is written by hand. Output:

```
  peak current 5.78 A at t = 2.32 ms
  t =    10 ms: speed   1000 rpm, back-EMF  2.10 V, current  5.00 A
  t =    50 ms: speed   3614 rpm, back-EMF  7.57 V, current  2.24 A
  t =   100 ms: speed   4945 rpm, back-EMF 10.36 V, current  0.83 A
  t =   250 ms: speed   5665 rpm, back-EMF 11.86 V, current  0.07 A
```

The current peaks at 5.78 A (a little below 6 A because the rotor has already started moving after 2.3 ms) and then falls as the back-EMF climbs. At 50 ms, one mechanical time constant, the speed has reached 3614 / 5701 = 63 % of its final value. The same 63 % you met in every first-order transient.

### Step 4: The stalled winding in our simulator

```python
def stalled_inrush():
    c = Circuit()
    c.pulse_source("V1", "vcc", "0", low=0.0, high=SUPPLY, period=1.0, duty=0.99)
    c.resistor("Rw", "vcc", "x", WINDING_OHMS)
    c.inductor("Lw", "x", "0", WINDING_HENRIES)
    run = c.transient(t_stop=3e-3, dt=1e-6)
    return np.asarray(run.time), np.asarray(run.i("Lw"))
```

With the rotor held still there is no back-EMF, and the motor is just an RL circuit: 3.79 A at 0.5 ms (63 % of 6 A, one electrical tau), 5.19 A at 1 ms, 5.96 A at 2.5 ms.

### Step 5: Running under load

```python
def running_motor_dc(back_emf):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", SUPPLY)
    c.resistor("Rw", "vcc", "x", WINDING_OHMS)
    c.inductor("Lw", "x", "y", WINDING_HENRIES)
    c.voltage_source("Eback", "y", "0", back_emf)
    result = c.dc()
    return result.i("Rw"), result.p("Rw"), back_emf * result.i("Rw")
```

The back-EMF is modelled as a voltage source opposing the supply. For each load torque we compute the needed current and back-EMF, and the simulator confirms the current and splits the power into heat and mechanical work. The output is the efficiency table above (plus a 5 mN·m line: 95.8 %).

### Step 6: The generator

```python
def generator_into_load(speed, load_ohms):
    c = Circuit()
    c.voltage_source("Egen", "e", "0", MOTOR_CONSTANT * speed)
    c.resistor("Rw", "e", "out", WINDING_OHMS)
    c.resistor("Rload", "out", "0", load_ohms)
    result = c.dc()
    return result.v("out"), result.i("Rload"), result.p("Rload"), result.p("Rw")
```

```
  load   1000000 ohm: V_out =  6.00 V, I = 0.000 A, ... braking torque =   0.0 mN*m, P_mech =  0.00 W
  load        10 ohm: V_out =  5.00 V, I = 0.500 A, P_load =  2.50 W, P_winding =  0.50 W, braking torque =  10.0 mN*m, P_mech =  3.00 W
  load         2 ohm: V_out =  3.00 V, I = 1.500 A, P_load =  4.50 W, P_winding =  4.50 W, braking torque =  30.0 mN*m, P_mech =  9.00 W
```

With nothing connected (1 M ohm) the generator spins freely. The more power you draw, the harder it is to turn, and the mechanical power in always equals load plus winding loss.

## Use It

- **Motor datasheets** list exactly the numbers of this lesson. A typical small brushed motor (for example, the Mabuchi RS-385 family or a Pololu gearmotor) gives: nominal voltage, no-load speed and current, stall torque and stall current, terminal resistance, and often the *torque constant* (mN·m/A) and *speed constant* (rpm/V). For a motor with k = 0.02 V·s/rad, the speed constant is 1 / 0.02 = 50 rad/s per volt = 477 rpm/V.
- **Hobby brushless motors** for drones are labelled with a "KV" rating in rpm per volt (for example 2300 KV): that is 1/k in different units.
- **Motor drivers.** Chips like the DRV8833 or L298 must be chosen for the *stall* current, not the running current, unless they limit current. They include flyback diodes or use the MOSFETs' built-in body diodes (Phase 18).
- **Regenerative braking** in electric cars, trains and some e-bikes runs the motor as a generator to recover energy when slowing down.
- **Power stations** use synchronous generators (AC machines) rated hundreds of megawatts. Their rotor is an electromagnet, and the field strength controls the output voltage, while the turbine's power sets the current.
- **Measuring speed.** Since back-EMF is proportional to speed, you can measure a motor's speed by briefly switching off the drive and measuring the voltage on its terminals. Small motors used this way are called *tachogenerators*.

## Try It in the Lab

Open **"Switch off the motor without a spark"**. A stalled motor winding (1 mH, 2 ohm) carries 6 A. At 1 ms the switch opens; when open it leaks like 10 k ohm. Choose a part to place across the winding, from ground to node a. Two goals must pass: node a must not go below -5 V after the switch opens, and the part must waste less than 1 mA while the motor runs. For each part in the drawer, estimate the most negative voltage at node a right after opening (the 6 A has to go somewhere!) and the current through the part while the switch is closed. One part passes one goal but not the other; one fails both.

## Common Mistakes

- **Sizing everything for the running current.** A motor draws its stall current V / R every time it starts and whenever it jams.
- **Thinking the winding's resistance changes with speed.** It does not. The current drops because the back-EMF grows.
- **Mixing rpm and rad/s.** The formulas use rad/s. 1 rpm = 0.1047 rad/s.
- **Forgetting that torque and back-EMF share one constant.** If a datasheet gives the torque constant in N·m/A, that same number (in SI units) is the back-EMF constant in V·s/rad.
- **Running a motor stalled for long.** At stall all the input power becomes heat in the winding (72 W for our 12 V, 2 ohm motor). Small motors burn out in seconds.
- **Switching a motor with no flyback path.** It is an inductor; Lesson 05 applies.

## Exercises

1. **Easy.** A motor has R = 3 ohm and is supplied with 9 V. What is its stall current? If k = 0.015 V·s/rad, what is its stall torque?
2. **Easy.** Convert 3000 rpm to rad/s. What back-EMF does a motor with k = 0.03 produce at that speed?
3. **Medium.** Our motor (12 V, 2 ohm, k = 0.02) drives a fan needing 20 mN·m. Find the current, back-EMF, speed in rpm and efficiency.
4. **Medium.** In `spin_up`, add a constant load torque of 30 mN·m. Predict the final speed and current from the motor equation, then check with the simulation.
5. **Hard.** Using our motor as a generator spun at 300 rad/s, find the load resistance that delivers the most power to the load. (Hint: Phase 05, Lesson 07.) What is the efficiency at that point, and why would a real power station never operate there?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Torque | "Twisting force" | Force times lever arm, in N·m; for a DC motor T = k I |
| Back-EMF | "The motor's own voltage" | The generator voltage k omega induced in a spinning motor's winding, opposing the supply |
| Motor constant | "Kt" or "Ke" | k, in V·s/rad = N·m/A, linking speed to back-EMF and current to torque |
| Stall current | "Start-up current" | V / R, the current when the rotor is not moving and there is no back-EMF |
| No-load speed | "Free speed" | The speed at which the back-EMF nearly equals the supply: about V / k |
| Commutator | "The brushes thing" | The split ring and brushes that reverse a DC motor's coil current every half turn |
| Regenerative braking | "Charging while braking" | Running a motor as a generator so the vehicle's motion becomes stored electrical energy |
| Inrush current | "Start surge" | The large current drawn while the motor accelerates from rest |

## Further Reading

- [The Feynman Lectures on Physics, Vol. II, Chapter 16 (Induced Currents), sections on motors and generators](https://www.feynmanlectures.caltech.edu/II_16.html) — how forces on currents and induction make the same machine work both ways
- [All About Circuits, Volume II, Chapter 13: AC Motors, and Volume I, Chapter 14 on electromagnetism](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-13/introduction-ac-motors/) — the practical motor families
- [MIT OpenCourseWare 6.685 Electric Machines](https://ocw.mit.edu/courses/6-685-electric-machines-fall-2013/) — the full engineering theory, for the curious
- [Texas Instruments DRV8833 datasheet](https://www.ti.com/lit/ds/symlink/drv8833.pdf) and [Pololu micro metal gearmotor pages](https://www.pololu.com/category/60/micro-metal-gearmotors) — real stall currents, speed constants and driver protection
