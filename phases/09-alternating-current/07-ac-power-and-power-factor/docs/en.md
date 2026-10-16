# AC Power and Power Factor

> In AC, volts times amps is not always watts. Part of the current just carries energy back and forth, heating the wires and doing no work, and the power factor tells you how big that part is.

**Type:** Build
**Prerequisites:** Phase 01 (The Physics Underneath), Lesson 09 (Energy and Power); Phase 09, Lessons 03 (RMS Values), 05 (Phasors) and 06 (Impedance)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Instantaneous power | p(t) = v(t) x i(t): power flowing at one instant; can be negative | The water flow through a door at one moment: in or out |
| Real power (P), also active power | The average of the instantaneous power: energy per second that actually does work or makes heat; in watts (W) | The beer in a glass |
| Reactive power (Q) | The size of the energy that sloshes back and forth between source and fields each cycle without being used; in volt-amperes reactive (var) | The foam on the beer: takes room in the glass, does not quench thirst |
| Apparent power (S) | V_rms x I_rms: what the wires and the source must carry; in volt-amperes (VA) | The whole glass, beer plus foam |
| Complex power | S = V x conj(I) with RMS phasors: P is its real part, Q its imaginary part | The glass described by two numbers: beer and foam |
| Power factor (PF) | P / S: the fraction of the apparent power that is real power; equal to cos(phi) for sine waves | How much of the glass is beer |
| Lagging / leading PF | Current behind the voltage (inductive loads) / current ahead (capacitive loads) | Which way the timing is off |
| Power triangle | A right triangle with sides P, Q and hypotenuse S | A ramp: horizontal distance, height, and the slope length |
| Power factor correction | Adding a part (usually a capacitor) that cancels a load's reactive power locally | Giving the foam its own small glass right next to the drinker |

## Learning Objectives

- Compute the instantaneous power p(t) = v x i and show that pure inductors and capacitors take zero average power.
- Explain real power, reactive power and apparent power, and why the wires must carry the apparent power.
- Compute P = V_rms I_rms cos(phi), Q = V_rms I_rms sin(phi), S = V_rms I_rms, and the power factor for a load given as an impedance.
- Use complex power S = V x conj(I) to get P and Q in one step.
- Size a power factor correction capacitor and show, with the simulator, that it reduces the line current while the load still receives the same real power.

## The Problem

An electrician measures an old workshop motor: 230 V RMS across it, 11.5 A RMS through it. Volts times amps is 230 x 11.5 = 2,645 "watts". But a wattmeter on the same line reads only 2,116 W. Where did the other 529 go? Nowhere: they never existed. In AC circuits with inductors or capacitors, volts times amps does not equal watts.

This matters for money and for heat. The electricity meter at home bills real energy (kWh). But the wires, fuses, transformers and generators must carry the full 11.5 A, and the heat in a wire depends on current squared (Lesson 01). A factory full of motors draws much more current than its real power needs, so its utility charges it for poor "power factor", and engineers bolt banks of capacitors onto the switchboard to fix it. Your laptop charger has a power factor correction circuit inside, by law in Europe for chargers above 75 W. This lesson explains why.

## The Physics

### Power at every instant

From Phase 01, Lesson 09: power is voltage times current. In AC both change all the time, so the power at each instant is

```
p(t) = v(t) x i(t)        (read: "the power at time t is the voltage at time t times the current at time t")
```

When p(t) is positive, energy flows from the source into the part. When p(t) is negative, energy flows **back** from the part to the source. A resistor never sends energy back: it turns it into heat. But inductors and capacitors store energy, in a magnetic field (Phase 08) or an electric field (Phase 07, Lesson 06), and they give it back.

### Resistor: power always positive

In a resistor, current and voltage are in step (Lesson 06, angle 0). When v is negative, i is negative too, and their product is positive. For a 52.9 ohm resistor on 230 V RMS (325.3 V peak), the peak current is 325.3 / 52.9 = 6.149 A, and p(t) swings between 0 and 325.3 x 6.149 = 2,000 W, twice per cycle. Its average is 1,000 W: the real power, V_rms x I_rms = 230 x 4.348 = 1,000 W.

### Inductor and capacitor: power sloshes back and forth

In an inductor, the current lags the voltage by 90 degrees. Now for a quarter of a cycle v and i have the same sign (p positive, energy goes into the magnetic field), for the next quarter they have opposite signs (p negative, the field gives the energy back), and so on.

```
 v, i
     v_         i_
    /  \       /  \
 --/----\-----/----\----- t
         \__/        \__/
 p = v x i
     _      _      _
    / \    / \    / \         +  energy into the field
 --/---\--/---\--/---\--- t
        \/     \/     \/      -  energy back to the source
```

The positive and negative lobes are equal, so the **average is exactly zero**. A 168.4 mH inductor at 50 Hz has |Z| = 314.16 x 0.1684 = 52.9 ohm, so it draws the same 4.348 A RMS as the resistor, yet its average power is 0 W: p(t) swings between -1,000 W and +1,000 W. The same holds for a capacitor, with the current leading instead of lagging.

So an ideal inductor connected to the mains consumes nothing on average. But the 4.348 A really does flow, through the wires, the fuse, the transformer down the street, each with some resistance, each heated by I x I x R. The energy is just borrowed and returned a hundred times a second, and the borrowing costs real losses on the way.

## The Concept

### Real power: the average

For a load with voltage V_rms and current I_rms, where the current lags the voltage by an angle phi (phi is the angle of the load's impedance from Lesson 06), the average power is

```
P = V_rms x I_rms x cos(phi)
```

Read it: "the real power is the RMS voltage times the RMS current times the cosine of the angle between them". Where does the cosine come from? Split the current phasor into two parts: one **in phase** with the voltage, of size I_rms cos(phi), and one **90 degrees out of phase**, of size I_rms sin(phi). The in-phase part behaves like the current in a resistor and carries real power, V_rms x I_rms cos(phi). The quadrature part behaves like the current in a pure inductor or capacitor and averages to zero.

Checks: a resistor has phi = 0 and cos(0) = 1, so P = V_rms I_rms. A pure inductor has phi = 90 degrees and cos(90°) = 0, so P = 0. A capacitor has phi = -90 degrees, also cos = 0.

### Reactive and apparent power

The other part gets its own name:

```
Q = V_rms x I_rms x sin(phi)        reactive power, in var (volt-ampere reactive)
S = V_rms x I_rms                   apparent power, in VA (volt-ampere)
```

Q measures how much energy sloshes back and forth (its sign tells you which way: positive for inductive loads, negative for capacitive ones). S is what the wires and the source feel, because it is set by the current that actually flows. They form a right triangle, because cos^2 + sin^2 = 1:

```
S^2 = P^2 + Q^2

               /|
          S  /  |  Q (reactive, var)
           /    |
         / phi  |
        +-------+
          P (real, W)
```

The units W, var and VA are all volts times amps; the different names are only there to stop people from adding them carelessly.

### Power factor

```
power factor = P / S = cos(phi)        (for sine waves)
```

It ranges from 0 to 1. A heater has PF = 1. An induction motor at full load has around 0.8 to 0.9, and much worse when lightly loaded. The PF is called **lagging** when the current lags (inductive, Q positive) and **leading** when it leads (capacitive, Q negative).

### Complex power: P and Q in one multiplication

With RMS phasors V and I (sizes V_rms and I_rms), there is a neat shortcut:

```
S = V x conj(I)       (read: "complex power is the voltage phasor times the conjugate of the current phasor")
```

Multiplying by the conjugate **subtracts** the current's angle (Lesson 04: conj flips the angle, and multiplication adds angles). So S has size V_rms I_rms and angle (angle of V) - (angle of I) = phi. In rectangular form, its real part is V_rms I_rms cos(phi) = P and its imaginary part is V_rms I_rms sin(phi) = Q. One multiplication gives both.

### Worked example: the workshop motor

Model the motor as a resistor in series with an inductor. (The resistance stands for the mechanical work done and the heat; the inductance for the magnetic field the motor needs to run.) Take R = 16 ohm and X_L = 12 ohm at 50 Hz, so L = 12 / 314.16 = 38.20 mH.

1. Impedance: Z = 16 + j12 ohm. Size sqrt(256 + 144) = sqrt(400) = 20 ohm. Angle atan2(12, 16) = 36.87 degrees.
2. Current: I = 230 / (20 at 36.87°) = 11.5 A RMS at -36.87 degrees (lagging).
3. Apparent power: S = 230 x 11.5 = 2,645 VA.
4. Real power: P = 2,645 x cos(36.87°) = 2,645 x 0.8 = 2,116 W. Check: it is also the heat in R, I^2 R = 11.5 x 11.5 x 16 = 2,116 W.
5. Reactive power: Q = 2,645 x sin(36.87°) = 2,645 x 0.6 = 1,587 var. Check: I^2 X = 11.5 x 11.5 x 12 = 1,587 var.
6. Power factor: 2,116 / 2,645 = 0.80 lagging.
7. Complex power in one go: S = 230 x conj(11.5 at -36.87°) = 230 x (11.5 at +36.87°) = 2,645 at 36.87° = 2,116 + j1,587 VA.

That is the electrician's puzzle solved: 2,645 VA of apparent power, 2,116 W of real power.

### Worked example: power factor from three meter readings

You can find the power factor of any load with a voltmeter, an ammeter and a wattmeter (or a plug-in energy meter, which contains all three). Suppose a fridge on 120 V shows 4.2 A and 380 W.

1. Apparent power: S = 120 x 4.2 = 504 VA.
2. Power factor: PF = P / S = 380 / 504 = 0.754.
3. Angle: phi = arccos(0.754) = 41.1 degrees (the fridge's compressor motor is inductive, so the current lags).
4. Reactive power, from the triangle: Q = sqrt(S^2 - P^2) = sqrt(504^2 - 380^2) = sqrt(254,016 - 144,400) = sqrt(109,616) = 331 var.

Notice that the meters alone cannot tell you whether the PF is lagging or leading: you need to know what kind of load it is, or measure the phase.

### Where the reactive energy actually goes

Reactive power sounds abstract, so let us follow the energy in the motor's inductance through one cycle. The motor current is 11.5 A RMS, so its peak is 11.5 x 1.4142 = 16.26 A. From Phase 08, the energy stored in an inductor's magnetic field is

```
W = (1/2) x L x i^2       (read: "the stored energy is half the inductance times the current squared")
```

At each current peak the field holds W = 0.5 x 0.0382 x 16.26 x 16.26 = 5.05 joules. A quarter cycle later the current is zero and the field holds nothing: those 5.05 J went back to the source. Then the current peaks again in the other direction and the field fills up again. This happens twice per cycle, so 100 times per second at 50 Hz.

The average stored energy is half the peak, 2.53 J, and a neat result ties it to Q: Q = 2 x omega x (average stored energy) = 2 x 314.16 x 2.53 = 1,587 var. Reactive power is literally "how much energy sits in the fields, times how often it is shuttled back and forth".

### Typical power factors

| Load | Typical PF | Why |
|---|---|---|
| Kettle, toaster, incandescent lamp | 1.00 | Pure resistance |
| Induction motor, full load | 0.80 - 0.90 lagging | Needs a magnetising current in its windings |
| Induction motor, lightly loaded | 0.20 - 0.50 lagging | Same magnetising current, little real power |
| Fluorescent lamp with plain inductor ballast | about 0.5 lagging | Ballast inductor in series |
| Cheap LED bulb or phone charger (no PFC) | 0.4 - 0.6 | Spiky current, not phase shift (see below) |
| Laptop or PC supply with active PFC | 0.95 - 0.99 | A converter shapes the current into a sine |

### What the utility sees

Imagine a workshop with 20 of these motors. Real power: 20 x 2,116 = 42.3 kW. Apparent power: 20 x 2,645 = 52.9 kVA. The transformer feeding the workshop, the cables and the switchgear must all be sized for 52.9 kVA, even though only 42.3 kW is being used. That is why many utilities charge industrial customers for reactive energy (kvarh) beyond a set limit, and why correction pays for itself.

### Power factor correction

The motor needs its 1,587 var of reactive power: its magnetic field must be built up and torn down every half cycle. But nothing says that energy must come all the way from the power station. A capacitor stores energy too, and its reactive power has the opposite sign: when the motor's inductance is giving energy back, the capacitor is taking it, and vice versa. Put a capacitor right across the motor, sized so its reactive power is -1,587 var, and the energy just sloshes between the motor and the capacitor. The line only has to deliver the real power.

The capacitor's reactive power at voltage V_rms is Q_C = -V_rms^2 x omega C (from Q = V^2 / X with X = -1 / (omega C)). Setting its size equal to the motor's 1,587 var:

```
C = Q / (omega x V_rms^2) = 1,587 / (314.16 x 230 x 230) = 1,587 / 16,619,000 = 95.5 microfarads
```

With it, the line current drops from 11.5 A to P / V = 2,116 / 230 = 9.2 A, and the power factor seen by the line becomes 1.00. The motor itself is untouched: it still draws 11.5 A and gets 2,116 W. Only the part of the circuit **between** the capacitor and the power station sees less current.

What does that buy? Suppose the cable from the switchboard to the motor has 0.5 ohm. Loss before: 11.5 x 11.5 x 0.5 = 66.1 W. After: 9.2 x 9.2 x 0.5 = 42.3 W. A 36% cut in cable heating, for free, forever. And a transformer rated in kVA can now feed 25% more motors.

Too much correction is also bad: a 150 microfarad capacitor would overshoot, making the total leading, and the line current would grow again (to about 10.0 A at PF 0.92 leading).

### A warning about non-sine currents

The formulas cos(phi) above assume sine-wave current. Many electronic loads (old phone chargers, LED bulbs, computers without correction circuits) draw current in short spikes near the voltage peaks. Their current is not a sine wave at all, and their PF is poor even with no phase shift, because the spiky current has a large RMS value for the power delivered (Lesson 03's crest factor). The general definition PF = P / (V_rms I_rms) still holds. Active PFC circuits in modern power supplies (Phase 18) shape the current into a sine in phase with the voltage.

## Build It

### Step 1: Instantaneous power in R, L and C

```python
for name, (size, angle) in loads.items():
    i = peak / size * np.sin(OMEGA * t - math.radians(angle))
    p = v * i
    print(f"  {name:<20} p(t) from {p.min():8.1f} W to {p.max():8.1f} W, average {p.mean():8.2f} W")
```

Each load has an impedance size and angle (Lesson 06). The current is the voltage divided by the size and delayed by the angle. Sampled over one full period, the resistor's power ranges from 0 to 2,000 W with an average of 1,000 W; the inductor's and the capacitor's range from about -1,000 to +1,000 W with an average of 0.00 W.

### Step 2: The motor in phasors

```python
def complex_power(v_rms_phasor, i_rms_phasor):
    return v_rms_phasor * i_rms_phasor.conjugate()
```

`.conjugate()` is Python's conj. The script prints Z = 16 + j12 ohm = 20 ohm at 36.87 deg, I = 11.50 A at -36.87 deg, S = 2116.0 + j1587.0 VA, and PF 0.800.

### Step 3: Time simulation check

```python
c = Circuit()
c.sine_source("V1", "line", "0", amplitude=peak, freq=FREQ)
c.resistor("Rm", "line", "m", MOTOR_R)
c.inductor("Lm", "m", "0", MOTOR_L)
tr = c.transient(t_stop=0.2, dt=1e-5)
p_avg = cycle_average(tr.time, tr.v("line") * tr.i("Rm"), cycles=5)
```

We simulate ten cycles of the real 325 V peak sine. The current through `Rm` is the motor current. Averaging v x i over the last five cycles (the start-up transient has died out after a few L / R = 2.4 ms time constants) gives about 2,116 W; the RMS current is 11.50 A, so V_rms x I_rms = 2,645 VA. No phasors were used here: the simulator just stepped through time, and the numbers agree with the phasor formulas.

### Step 4: Correction capacitor

```python
c_needed = q / (OMEGA * V_RMS**2)
...
a = net.ac([FREQ], source="V1")
line_current = complex(a.i("V1")[0]) * V_RMS
pf = math.cos(cmath.phase(line_current))
```

The AC analysis uses a source of size 1, so multiplying its current by 230 gives the RMS line current for a 230 V RMS supply (everything is linear: twice the voltage, twice the current). The angle of the line current relative to the source voltage gives the power factor. Expected output:

```
  no capacitor       line current  11.50 A RMS, power factor 0.800, loss in a 0.5 ohm cable  66.1 W
  95.5 uF            line current   9.20 A RMS, power factor 1.000, loss in a 0.5 ohm cable  42.3 W
  150 uF (too big)   line current  10.01 A RMS, power factor 0.919, loss in a 0.5 ohm cable  50.1 W
```

## Use It

- **Industrial capacitor banks.** Factories install switched capacitor banks at the main switchboard, often controlled automatically, to keep the PF above about 0.95 and avoid reactive-energy charges on their bill.
- **Fluorescent lamp fittings.** Old fluorescent tubes use an inductor "ballast" with a PF around 0.5; better fittings include a small correction capacitor across the mains (often 3-10 microfarads).
- **Ceiling fans and washing machines.** Single-phase induction motors use a "run capacitor"; it is mainly there to make the motor start and run, but it also improves the PF.
- **Power supplies.** EU regulation (EN 61000-3-2) limits harmonic currents for equipment above 75 W, which in practice forces active PFC in laptop chargers, TVs and PC power supplies. Their datasheets quote PF > 0.9 or > 0.95.
- **Ratings in VA.** UPS units, transformers and generators are rated in VA or kVA, not in W, because their heating depends on the current, whatever the power factor.

## Try It in the Lab

The lab task "Fix the motor's power factor" builds the motor of this lesson (16 ohm in series with 38.2 mH, on 50 Hz) with a tiny 0.1 ohm "current sense" resistor in the return wire, so the voltage across it shows the line current. Your job: put a capacitor across the motor so the line current is at least about 1.7 dB smaller than without correction (below -47.7 dB relative to the source) and in phase with the voltage within 10 degrees. Before trying parts, compute Q for the motor and the capacitor that cancels it. Also predict what happens with a capacitor much bigger than needed.

## Common Mistakes

- **Multiplying volts and amps to get watts in an AC circuit.** That gives apparent power (VA). Real power needs the cos(phi), or an average of v x i.
- **Thinking reactive power is "wasted" in the load.** It is not consumed at all; it is borrowed and returned. The waste is the extra I^2 R in the wires that carry it.
- **Forgetting the conjugate in S = V conj(I).** V x I (without conj) has angle phi_V + phi_I, which has no physical meaning.
- **Using peak values in power formulas.** P = V_rms I_rms cos(phi). With peak values you get twice the answer (P = V_pk I_pk cos(phi) / 2).
- **Over-correcting.** A capacitor bigger than needed turns a lagging PF into a leading one, and the line current rises again.
- **Expecting a capacitor to reduce the motor's own current.** Correction reduces the current in the supply wiring, not in the motor.

## Exercises

1. **Watts and VA.** A load draws 5 A RMS from 120 V at a power factor of 0.6 lagging. Compute S, P and Q, and draw the power triangle.
2. **From impedance.** A load has Z = 30 + j40 ohm on 230 V RMS. Find I, S, P, Q and the PF. Check P with I^2 R.
3. **Capacitive load.** What are P and Q for a 10 microfarad capacitor alone on 230 V, 50 Hz? Is its Q positive or negative?
4. **Correction.** For the load of Exercise 2 at 50 Hz, compute the capacitor that brings the PF to 1, and the new line current. How much less heat is produced in a 1 ohm supply cable?
5. **Simulator.** Change the script's correction loop to try 47, 68, 82, 100 and 120 microfarads. Plot line current against capacitance. Where is the minimum, and how does the PF behave on each side?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Real power P | "Watts", "active power" | Average of v(t) i(t) over whole cycles; V_rms I_rms cos(phi) |
| Reactive power Q | "Vars", "wattless power" | V_rms I_rms sin(phi): amplitude of the energy exchanged back and forth with fields each cycle |
| Apparent power S | "VA" | V_rms x I_rms; what sizes wires, fuses and transformers |
| Complex power | "S = V I*" | V x conj(I) with RMS phasors = P + jQ |
| Power factor | "cos phi" | P / S; cos(phi) for sine waves, lower for spiky currents |
| Lagging / leading | "Inductive / capacitive" | Current behind / ahead of the voltage |
| Power factor correction | "PFC", "adding caps" | Supplying a load's reactive power locally (capacitor) or shaping its current (active PFC) so the line carries less current |

## Further Reading

- [All About Circuits, Vol. II (AC), Chapter 11: Power Factor](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-11/power-resistive-reactive-ac-circuits/) — true, reactive and apparent power with worked correction examples.
- *The Art of Electronics*, Horowitz & Hill, 3rd ed., Section 1.7.6 (Power in reactive circuits) and Chapter 9 (power supplies) — power factor from a designer's perspective.
- [MIT OpenCourseWare 6.002, lectures on AC power](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) — average power and complex power derived carefully.
- [onsemi, Power Factor Correction (PFC) Handbook, HBD853](https://www.onsemi.com/pub/collateral/hbd853-d.pdf) — why modern supplies need active PFC and how it is done.
