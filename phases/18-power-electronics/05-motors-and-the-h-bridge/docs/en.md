# Motors and the H-Bridge

> A DC motor is a resistor, an inductor and a generator in one can, and the generator part fights back harder the faster it spins. Four switches around it, an H-bridge, let a microcontroller choose forwards, backwards, brake or coast, and PWM chooses how fast.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 08 (Magnetism and Inductors), Lesson 07 (Motors and Generators); Phase 18 (Power Electronics), Lessons 02-03; Phase 17 (Microcontrollers), Lesson 03 (PWM); Phase 05 (Circuit Analysis and Our Simulator), Lesson 08 (Dependent Sources)
**Time:** ~95 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| DC motor | A machine that turns electric current into rotation, using magnets and coils (Phase 08, Lesson 07). | An electric drill's insides. |
| Armature | The rotating coil of the motor. Its wire has resistance R and inductance L. | The spinning part. |
| Torque | The twisting force the motor produces, in newton metres (N m). | How hard a spanner turns a bolt. |
| Angular speed (omega) | How fast the shaft turns, in radians per second (rad/s). One turn is 2 pi radians, so rpm = omega x 60 / (2 pi). | The speedometer of a wheel. |
| Motor constant (k) | One number that links current to torque (torque = k x I) and speed to voltage (back-EMF = k x omega). | The gearing between the electrical and the mechanical side. |
| Back-EMF | The voltage the spinning motor generates, opposing the supply. EMF means electromotive force, an old name for a generated voltage. | Pedalling a bike with a dynamo: the faster you go, the more it pushes back. |
| Stall | The motor is held still while powered: no back-EMF, maximum current. | Pushing against a wall. |
| Inertia (J) | How hard it is to change the rotor's speed, in kg m^2. | A heavy flywheel. |
| H-bridge | Four switches arranged like the letter H, with the motor as the crossbar, that can connect either motor terminal to either supply rail. | A railway crossing that can route a train either way. |
| Shoot-through | Both switches on one side of the bridge closed at once: a short circuit across the battery. | Opening both ends of a canal lock at once. |
| Brake | Both motor terminals connected together (to ground), so the back-EMF drives a current that slows the motor. | Shorting a dynamo so pedalling becomes hard. |
| Coast | All switches open; the motor spins down slowly on its own. | Freewheeling downhill. |
| Body diode | The diode that every power MOSFET has built in, from source to drain. It catches the inductive current when a switch opens. | A built-in overflow valve. |

## Learning Objectives

- Model a DC motor as resistance + inductance + back-EMF, coupled to inertia and friction, and build that model in our simulator with controlled sources
- Compute stall current, stall torque, no-load speed and the speed under load from four motor numbers
- Explain why a motor draws a big current at start-up and a small one at speed
- Use an H-bridge to drive a motor forwards, backwards, brake or coast, and recognise the shoot-through state
- Control speed with PWM and show that the speed follows D x Vbat while the current ripple stays small thanks to the armature inductance

## The Problem

Fans, pumps, toy cars, robot wheels, drones, window lifts, 3D printers and electric bikes all spin motors. A microcontroller pin can supply 20 mA (Phase 17, Lesson 02); a small motor wants amps, and much more at the instant it starts. The motor also needs to go both ways (a robot must reverse), at controlled speeds, and stop quickly when told to. Worse, it is an inductor: switch it off carelessly and it produces the voltage spike of Lesson 02.

To design the driver, we need to know what a motor looks like electrically, and it turns out to be a beautiful little circuit: the electrical side and the mechanical side are described by the *same* equations as resistors, inductors and capacitors, so our circuit simulator can simulate the whole thing.

## The Physics

### Current makes torque, speed makes voltage

In Phase 08, Lesson 07 you saw that a current-carrying wire in a magnetic field feels a force (that makes the motor turn) and that a wire moving through a magnetic field has a voltage induced in it (that is a generator). A DC motor does both at once, all the time. For a permanent-magnet DC motor both effects are proportional, with the same constant k:

```
torque   T = k x I              (newton metres)
back-EMF E = k x omega          (volts)
```

Read them as: "the twisting force is k times the current" and "the generated voltage is k times the speed". It is the same k in both (in SI units) because of energy conservation: the electrical power absorbed by the back-EMF, `E x I = k omega I`, must equal the mechanical power delivered, `T x omega = k I omega`.

### The electrical side

The armature winding has resistance `R` and inductance `L`. Kirchhoff's voltage law around the motor:

```
V_applied = I x R + L dI/dt + k x omega
```

"The applied voltage is shared by the winding's resistance, its inductance and the back-EMF."

### The mechanical side

Newton's law for rotation: the torque that is left after friction speeds the rotor up.

```
J x d omega / dt = k x I - b x omega - T_load
```

"Inertia times angular acceleration equals motor torque minus friction minus the load's torque." `b` is a friction coefficient (torque per unit speed).

### The mechanical side is a circuit too

Compare that equation with a capacitor fed by a current source and drained by a resistor (Phase 07):

```
C x dV/dt = I_in - V / R
```

They are the same equation if we say: speed omega is a "voltage", torque is a "current", inertia J is a "capacitance", and friction b is a "conductance" 1/R. So we can draw the motor's mechanics as a node called `omega` with a capacitor J and a resistor 1/b to ground, fed by a current source of value `k x I`. And the back-EMF is a voltage source of value `k x omega` in the armature loop. The two are joined by the dependent sources of Phase 05, Lesson 08:

```
  A ---[ R ]---m1---[ L ]---m2---( + EMF = k x V(omega) - )--- B
                                                                       electrical side

  omega node: ---( torque source k x I )--->  omega  ---+---------+
                                                         |         |
                                                        === J    [ 1/b ]       mechanical side
                                                         |         |
                                                        gnd       gnd
```

The current `I` is measured as the voltage across `R` divided by `R`, so the torque source is a voltage-controlled current source with gain `k / R` looking at the resistor.

### Steady state

At constant speed, `dI/dt = 0` and `d omega/dt = 0`:

```
V = I R + k omega
k I = b omega + T_load
```

Solve for omega (substitute `I = (b omega + T_load) / k` into the first equation):

```
omega = (k V - R T_load) / (k^2 + b R)
```

## The Concept

### The motor's four numbers

Our motor: `R = 2 ohm`, `L = 1 mH`, `k = 0.02 V s/rad` (equivalently 0.02 N m per amp), `J = 1e-5 kg m^2`, `b = 1e-5 N m s/rad`, on 12 V.

```
stall current     = V / R = 12 / 2 = 6 A                 (omega = 0, no back-EMF)
stall torque      = k x 6 = 0.12 N m
no-load speed     = k V / (k^2 + b R) = 0.24 / (0.0004 + 0.00002) = 571 rad/s = 5457 rpm
no-load current   = b x omega / k = 1e-5 x 571 / 0.02 = 0.29 A
```

So the motor draws 6 A when it starts and only 0.29 A when running free: a factor of 20. This is why lights dim when a big motor starts, and why motor drivers are sized for the stall current, not the running current.

### Two time constants

```
electrical:  L / R      = 1 mH / 2 ohm         = 0.5 ms
mechanical:  J R / k^2  = 1e-5 x 2 / 0.0004    = 50 ms
```

The current responds in about half a millisecond; the speed takes tens of milliseconds. Both matter for the driver: the PWM period must be much shorter than L / R so the current stays smooth.

### With a load

A load torque of 0.02 N m:

```
omega = (0.02 x 12 - 2 x 0.02) / 0.00042 = (0.24 - 0.04) / 0.00042 = 476 rad/s
I = (b omega + T_load) / k = (0.00476 + 0.02) / 0.02 = 1.24 A
```

The motor slows a little and draws more current to produce the extra torque. Back-EMF is a built-in feedback: the slower it goes, the less it opposes the supply, so the more current and torque it gets.

### The H-bridge

```
             Vbat
              |
        +-----+-----+
        |           |
       S1          S3
        |           |
        A---[ M ]---B
        |           |
       S2          S4
        |           |
        +-----+-----+
              |
             gnd
```

| State | Closed | Motor sees | Effect |
|-------|--------|-----------|--------|
| Forward | S1, S4 | A = Vbat, B = 0 | current A to B |
| Reverse | S2, S3 | A = 0, B = Vbat | current B to A |
| Brake | S2, S4 (or S1, S3) | A and B shorted | back-EMF drives a current that stops the motor fast |
| Coast | none | open circuit | motor spins down on friction |
| Shoot-through | S1, S2 (or S3, S4) | **battery shorted** | huge current, destroyed switches |

The simulation shows the shoot-through state: with only 12 milliohms in the loop (two switches and the wiring), 1000 A flows. Real drivers prevent it with logic that never allows both switches of a leg on, plus a short **dead time** between turning one off and the other on.

### Braking versus coasting

When a spinning motor's terminals are shorted (brake), its back-EMF `k omega` drives a current `k omega / R` through its own winding. That current produces a torque *against* the rotation, so the motor stops in roughly the mechanical time constant: from 571 rad/s down to about 200 rad/s in 50 ms in the simulation. When all switches are open (coast), only friction slows it: after 200 ms it is still above 460 rad/s.

At the moment the switches open, the armature's inductor is still carrying current. With ideal switches it would cause the kick of Lesson 02. In real bridges, each MOSFET's **body diode** catches that current and returns it to the supply. Our simulation includes those diodes.

### Speed control with PWM

Keep S4 closed and switch the left leg (S1 and S2, opposite to each other) with PWM at 20 kHz. Terminal A becomes a square wave between 0 and 12 V; the motor's inductance smooths the current (as the buck's inductor did in Lesson 03); its inertia smooths the speed even more. The motor responds to the average voltage:

```
omega = k x D x Vbat / (k^2 + b R)       (no load)
```

At D = 0.5: `0.02 x 6 / 0.00042 = 286 rad/s`. The current ripple can be estimated like a buck's: during the on-time the inductance sees about `Vbat - D Vbat` (minus the small `I R`), for `D T`:

```
delta_I ~ (Vbat (1 - D)) x D x T / L = 12 x 0.5 x 0.5 x 50 us / 1 mH = 0.15 A
```

The simulator measures 149 mA. A higher PWM frequency means less ripple and less audible whine (20 kHz is above human hearing, which is why it is popular).

### Worked example: a robot's motor from its datasheet

A small 6 V gear motor's datasheet says: no-load speed 10 000 rpm (at the motor shaft, before the gearbox), no-load current 0.15 A, stall current 2.5 A. Extract the model:

```
R = V / I_stall = 6 / 2.5 = 2.4 ohm
omega_no_load = 10 000 x 2 pi / 60 = 1047 rad/s
at no load: V = I R + k omega   ->   k = (6 - 0.15 x 2.4) / 1047 = 5.64 / 1047 = 0.0054 V s/rad
stall torque = k x I_stall = 0.0054 x 2.5 = 0.0135 N m       (before the gearbox multiplies it)
```

Now choose a driver. The stall current, 2.5 A, flows every time the robot starts or bumps into a wall. A driver rated "1.5 A continuous, 2 A peak" per channel would be overloaded at stall; it needs either current limiting (many driver chips have it: they chop the PWM when the current exceeds a set value) or a bigger driver.

### Worked example: speed with PWM and a load

With the lesson's motor (k = 0.02, R = 2 ohm, b = 1e-5) on 12 V at D = 0.6 and a load torque of 0.03 N m:

```
average voltage = 0.6 x 12 = 7.2 V
omega = (k V - R T_load) / (k^2 + b R) = (0.144 - 0.06) / 0.00042 = 200 rad/s  (1910 rpm)
current = (b omega + T_load) / k = (0.002 + 0.03) / 0.02 = 1.6 A
```

The motor current (1.6 A) is not the battery current. The H-bridge acts like a buck converter (Lesson 03): the battery supplies the motor current only during the on-time, so on average `D x 1.6 = 0.96 A`. The motor runs at 7.2 V and 1.6 A (11.5 W) while the battery gives 12 V and 0.96 A (11.5 W): power in equals power out, ignoring losses.

### Worked example: energy dumped when braking

At 571 rad/s the rotor stores `1/2 J omega^2 = 0.5 x 1e-5 x 571^2 = 1.63 J` of kinetic energy. Braking (shorting the terminals) turns all of it into heat in the 2 ohm winding within a few tenths of a second. Coasting turns it into friction heat slowly. A regenerative drive would push it back into the battery instead: on an electric car, that energy is large enough to matter for range.

## Build It

### Step 1: The motor as a circuit

```python
def add_motor(circuit, a, b, load_torque=0.0):
    circuit.resistor("RA", a, "m1", R_ARMATURE)
    circuit.inductor("LA", "m1", "m2", L_ARMATURE)
    circuit.vcvs("EMF", "m2", b, "omega", "0", K_MOTOR)
    circuit.vccs("TORQUE", "0", "omega", a, "m1", K_MOTOR / R_ARMATURE)
    circuit.capacitor("J", "omega", "0", INERTIA)
    circuit.resistor("FRICTION", "omega", "0", 1 / FRICTION)
    if load_torque:
        circuit.current_source("TLOAD", "omega", "0", load_torque)
```

The voltage of node `omega` is the speed in rad/s. `TORQUE` injects `k x V(RA) / R = k x I` into it; `J` and `FRICTION` are the inertia and friction; `TLOAD` pulls the load torque out.

### Step 2: Start-up and load

`start_up` applies 12 V to a motor at rest for 300 ms and samples speed and current. Then it repeats with load torques and compares the final speed with the formula.

### Step 3: The H-bridge states

`h_bridge_dc` builds the bridge with the stalled motor (its 2 ohm winding) and solves each switch combination.

### Step 4: Brake and coast

`braking` starts the motor at full speed (the capacitor `J` begins at the no-load speed, the inductor at the no-load current) and opens or shorts the bridge, with a diode across each switch.

### Step 5: PWM

`pwm_drive` toggles S1 and S2 at 20 kHz, starting from the predicted steady state, and measures the average terminal voltage, the average and ripple current, and the speed over the last 10 periods.

Run it:

```
uv run python phases/18-power-electronics/05-motors-and-the-h-bridge/code/main.py
```

You will see the current peak near 5.8 A and fall to 0.3 A as the speed climbs to 570 rad/s, the speeds under load matching the formula, the H-bridge table with the 1000 A shoot-through, braking stopping the motor much faster than coasting, and PWM speeds matching `k D V / (k^2 + b R)`.

## Use It

- **Driver chips:** the L298N (an old bipolar dual H-bridge, losing about 2-4 V in its transistors), the DRV8833 and TB6612FNG (MOSFET bridges with tiny losses, for small robots), the DRV8871 and BTS7960 for several amps. They include shoot-through protection, dead time, current limiting and thermal shutdown.
- **Datasheet numbers for motors:** "no-load speed", "no-load current", "stall torque", "stall current", "torque constant" (our k in N m/A) and "speed constant" (rpm per volt, the inverse of k in other units). From any two you can estimate the others with this lesson's formulas.
- **Brushless motors** (drones, hard disks, electric cars) use three half-bridges and switch the coils electronically in sequence; the same back-EMF and H-bridge ideas apply.
- **Regenerative braking** in electric vehicles uses the back-EMF to push energy back into the battery instead of burning it in the winding, using the bridge as a boost converter (Lesson 04).
- **Always include a freewheel path.** A single-transistor motor driver (no bridge) needs a diode across the motor, as in Lesson 02.

## Try It in the Lab

The lab has an H-bridge with four empty switch positions around a 4 ohm stalled motor, a 12 V battery and 0.1 ohm of wiring. Make at least 2 A flow through the motor from A to B without the wiring ever carrying more than 5 A. Every combination is either forward, reverse, brake, coast or shoot-through: decide which you need, and which single change would turn it into a short circuit.

## Common Mistakes

- **Sizing the driver for running current.** The stall (start-up) current is many times larger.
- **Shoot-through.** Two switches on the same leg on together short the supply. Use drivers with built-in interlocks and dead time.
- **No path for the inductive current.** Without diodes (body diodes or external), opening the bridge produces a spike.
- **Low PWM frequency.** Below about L / R in period terms the current becomes jerky, and the motor whines audibly in the kilohertz range.
- **Ignoring supply sag.** The 6 A start-up current through battery and wiring resistance can drop the supply enough to reset a microcontroller. Separate the motor supply, or add capacitance and soft starting.
- **Confusing rpm and rad/s.** One rpm is 2 pi / 60 = 0.105 rad/s.

## Exercises

1. A motor has R = 1.5 ohm and k = 0.01 V s/rad, on 6 V. Ignoring friction, what are its stall current, stall torque and no-load speed in rpm? (4 A, 0.04 N m, 600 rad/s = 5730 rpm.)
2. The same motor under 0.01 N m of load: speed and current (no friction)? (omega = (0.06 - 0.015) / 0.0001 = 450 rad/s; I = 1 A.)
3. For our lesson's motor at 20 kHz and D = 0.25, estimate the current ripple with the buck-like formula. Compare with the simulator's 112.6 mA. (12 x 0.75 x 0.25 x 50 us / 1 mH = 112.5 mA.)
4. In the H-bridge, what is the battery current in "reverse"? Why is the motor current negative? (5.96 A, the same as forward: the battery does not care which way the motor turns. The motor current is negative because it now flows from B to A, against the reference direction of the resistor, which was defined from A to B.)
5. Harder: add a load torque that depends on speed (a fan: torque proportional to speed) by adding a second resistor on the `omega` node. Choose its value so that at full voltage the fan spins at 400 rad/s. (A resistor of value 1/b_fan adds b_fan omega of torque; solve 0.24 = 400 x (0.0004 + 2 (1e-5 + b_fan)) for b_fan.)

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Back-EMF | "The motor's voltage" | The generated voltage k x omega that opposes the supply |
| Stall current | "Start-up current" | V / R: the current with the rotor not turning |
| Torque constant | "Kt" | Torque per amp; equal to the back-EMF constant in SI units |
| H-bridge | "Motor driver" | Four switches that connect each motor terminal to either rail |
| Shoot-through | "A short" | Both switches of one leg on: supply shorted |
| Brake | "Short the motor" | Terminals connected together so back-EMF current stops the rotor |
| Dead time | "Delay" | A short pause with both switches of a leg off, to prevent shoot-through |

## Further Reading

- [Texas Instruments, DRV8833 datasheet](https://www.ti.com/lit/ds/symlink/drv8833.pdf) — a small dual H-bridge: states table (forward, reverse, brake, coast), current limiting and PWM control
- [STMicroelectronics, L298 datasheet](https://www.st.com/resource/en/datasheet/l298.pdf) — the classic bipolar bridge, with the external diodes it needs
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., sections on motor drive and H-bridges
- [MIT OpenCourseWare 6.302 "Feedback Systems" notes on DC motor modelling](https://ocw.mit.edu/courses/6-302-feedback-systems-spring-2007/) — the same electromechanical equations used for control
