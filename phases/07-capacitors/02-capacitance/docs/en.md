# Capacitance

> Capacitance is how many coulombs a pair of plates holds for each volt. Big plates, a thin gap and a good dielectric make it large.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 01 (The Physics Underneath), Phase 07 Lesson 01 (Storing Charge)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Capacitance (C) | Charge stored per volt, Q / V | How many litres a tank holds per centimetre of water height |
| Farad (F) | The unit of capacitance: one coulomb per volt | A tank so wide that it is almost never built; we use micro, nano and pico |
| Plate area (A) | How big the facing surfaces of the plates are, in square metres | The floor area of the tank |
| Gap (d) | Distance between the plates, in metres | How thin the separating sheet is |
| Permittivity of free space (eps0) | A constant of nature, 8.854 x 10^-12 F/m, that links charge to field in empty space | A conversion factor nature hands us, like the speed of light |
| Relative permittivity (eps_r) | How many times more capacitance a material gives compared with vacuum | A sponge filling that lets more charge squeeze in per volt |
| Polarization | The tiny shift of electrons inside a dielectric's atoms toward the positive plate | Every atom leaning a little, like a crowd leaning toward a stage |
| Breakdown | When the field is so strong that the dielectric suddenly conducts and is usually destroyed | A dam bursting |
| Rated voltage | The highest voltage the maker guarantees the capacitor survives | The red line on a pressure gauge |

## Learning Objectives

- State the definition C = Q / V and use it in both directions.
- Explain physically why bigger plates and a smaller gap give more capacitance.
- Explain what a dielectric does at the atomic level and why it multiplies capacitance by eps_r.
- Compute the capacitance of a parallel-plate capacitor from its size and material.
- Use a constant current source in our simulator to measure capacitance from the slope of a voltage ramp: C = I / (dV/dt).
- Read the value and voltage markings found on real capacitors.

## The Problem

In Lesson 01 you watched a 100 uF capacitor charge and found that Q / V stayed fixed at 100 uF. Where did that number come from? Why is one capacitor the size of a grain of rice and 10 uF, while another is the size of a soup can and 10,000 uF? Why can't you just make a 1 F capacitor from two kitchen trays?

You need to know what sets capacitance so you can choose parts, read datasheets, and understand why capacitance can change (with temperature, voltage or age, as Lesson 07 will show). You also need a way to measure it. This lesson gives you both.

## The Physics

### Why more charge needs more voltage

Put +Q on one plate and -Q on the other. The charges create an **electric field** (Phase 01 Lesson 05) in the gap: an invisible push on any charge placed there. To bring one more electron onto the negative plate you must push it against that field. The work per coulomb is the voltage between the plates.

Double the charge on each plate and the field in the gap doubles; the work per coulomb doubles; the voltage doubles. That is why Q and V are proportional, and their ratio is a fixed property of the geometry and the material:

> Capacitance is the charge on one plate divided by the voltage between the plates.

    C = Q / V        (farads = coulombs per volt)

### Bigger plates

Spread the same charge over plates twice as large. The charge per square metre (the "crowding") halves, so the field in the gap halves, so the voltage halves. Same charge, half the voltage: double the capacitance. **Capacitance grows in proportion to plate area.**

### Smaller gap

The voltage is the field times the distance you carry the charge across (for a uniform field, V = E x d). Halve the gap with the same field and the voltage halves. Again: same charge, half the voltage, double capacitance. **Capacitance grows as the gap shrinks.**

Combining both for two flat plates in vacuum (or air, which is almost the same):

> Capacitance equals a constant of nature times the plate area, divided by the gap.

    C = eps0 x A / d

where eps0 = 8.854 x 10^-12 F/m is the **permittivity of free space**, A is the area of one plate in square metres and d the gap in metres. (This is the formula for plates much wider than the gap; near the edges the field bulges out a little, which we ignore.)

### What the dielectric does

Now fill the gap with an insulator. Its electrons cannot leave their atoms, but they can **shift** slightly. Each atom's electron cloud leans toward the positive plate, and its nucleus leans toward the negative one. This is **polarization**.

```
   + plate    (-+) (-+) (-+) (-+)    - plate
   + + + +    (-+) (-+) (-+) (-+)    - - - -
              each atom: electron cloud (-) leans toward +,
              nucleus (+) leans toward -
```

Look at the surface of the dielectric next to the positive plate: it is covered in the negative ends of the leaning atoms. That layer partly cancels the plate's charge as seen from the gap. The net field is weaker, so the voltage for the same charge is lower, so the capacitance is higher. The factor by which a material does this is its **relative permittivity** eps_r (also called the dielectric constant, sometimes k):

    C = eps0 x eps_r x A / d

| Material | eps_r (roughly) | Where you meet it |
|---|---|---|
| Vacuum / air | 1.0 | Variable tuning capacitors in old radios |
| PTFE (Teflon) | 2.1 | High-precision, low-loss capacitors |
| Polypropylene film | 2.2 | Audio and pulse film capacitors |
| Polyester (PET) film | 3.3 | Cheap general-purpose film capacitors |
| Aluminium oxide | about 9 | Aluminium electrolytic capacitors |
| Tantalum pentoxide | about 27 | Tantalum capacitors |
| C0G/NP0 ceramic | about 30-100 | Stable small-value ceramic capacitors |
| X7R/X5R ceramic (barium titanate) | 2000-4000 or more | The 100 nF and 10 uF chips on every board |

The analogy that a dielectric is a "sponge" for charge is useful but wrong in one way: the dielectric holds no free charge. All it does is lean, and the leaning reduces the field.

### The limit: breakdown

Shrinking the gap gives more capacitance but makes the field E = V / d stronger. Every insulator has a maximum field it survives (its **dielectric strength**); air breaks down at about 3 million volts per metre, which is 3 V per micrometre. Beyond that, electrons are ripped free and the insulator conducts, often with a spark and permanent damage. That is why every capacitor has a **rated voltage**, and why high-voltage capacitors of the same capacitance are physically larger: they need thicker dielectric.

## The Concept

### Worked example 1: two kitchen trays

Two square plates 10 cm x 10 cm, 1 mm apart, in air.

1. Area A = 0.1 m x 0.1 m = 0.01 m^2.
2. Gap d = 1 mm = 0.001 m.
3. C = 8.854 x 10^-12 x 0.01 / 0.001 = 8.854 x 10^-11 F = 88.5 pF (picofarads).

That is tiny: about a millionth of the 100 uF capacitor from Lesson 01.

### Worked example 2: how to get to microfarads

| Change | New C |
|---|---|
| Start: 0.01 m^2, 1 mm air | 88.5 pF |
| Gap to 0.1 mm | 885 pF (ten times more) |
| Fill with polyester, eps_r = 3.3 | 2.92 nF |
| Fill with X7R ceramic, eps_r = 3000 | 2.66 uF |

So real capacitors use three tricks at once: thin dielectric (micrometres, not millimetres), high eps_r materials, and huge area folded into a small box. A film capacitor rolls two long metallized plastic strips like a carpet. A multilayer ceramic capacitor (MLCC) stacks hundreds of thin layers. An electrolytic capacitor etches its aluminium foil into a sponge-like surface that multiplies the area by a hundred and grows a nanometre-thin oxide on it.

### Worked example 3: going backwards

How much plate area for 1 uF with a 1 mm air gap? Rearrange C = eps0 x A / d to A = C x d / eps0:

    A = 1 x 10^-6 x 0.001 / 8.854 x 10^-12 = 113 m^2

A square about 11 m on a side, the floor of a large classroom, for a part that a shop sells the size of a pea. With 5 um of polyester:

    A = 1 x 10^-6 x 5 x 10^-6 / (8.854 x 10^-12 x 3.3) = 0.171 m^2

About the size of an A3 sheet, which rolls up into a component the size of a sugar cube.

### Measuring capacitance with a steady current

Lesson 01 showed I = Q / t for a steady current. Feed a capacitor a **constant** current I. In time t it receives charge Q = I x t, so its voltage is

    V = Q / C = I x t / C

The voltage rises in a straight line. Its slope (volts per second) is

> The rate at which a capacitor's voltage rises equals the current into it divided by its capacitance.

    dV/dt = I / C        so        C = I / (dV/dt)

Example: 1 mA into 1 uF gives 0.001 / 0.000001 = 1000 V/s, which is 1 V per millisecond. Many multimeters measure capacitance exactly like this: they push a known small current and time how long the voltage takes to rise a known amount.

This little equation, **I = C x dV/dt**, is the most important rule about capacitors. Read it as a sentence: the current into a capacitor is its capacitance times how fast its voltage is changing. If the voltage is not changing, the current is zero (Lesson 01's "blocks DC"). If you want the voltage to jump instantly (dV/dt infinite), you would need infinite current, which is why **the voltage across a capacitor cannot jump**. Lessons 03 and 08 build everything on this.

### Reading capacitor markings

- **Electrolytics** print it plainly: "470 uF 25 V", with a stripe marking the negative lead.
- **Ceramic and film** often use a 3-digit code in picofarads: two digits and a number of zeros. "104" means 10 followed by 4 zeros = 100,000 pF = 100 nF = 0.1 uF. "472" = 4,700 pF = 4.7 nF. A letter after it gives tolerance: J = 5%, K = 10%, M = 20%.
- **Small surface-mount ceramics** usually have no marking at all; the value is on the reel label.

### Worked example 4: a capacitor microphone

In a condenser (capacitor) microphone, one plate is a thin metal-coated film that moves with sound, about 20 um from a fixed back plate. Say the plates are 12 mm in diameter.

1. Area: A = pi x r^2 = 3.1416 x (0.006)^2 = 1.13 x 10^-4 m^2.
2. C = 8.854 x 10^-12 x 1.13 x 10^-4 / 20 x 10^-6 = 50 pF.
3. A loud sound moves the film by 0.2 um, 1% of the gap. The capacitance changes by about 1%, 0.5 pF.
4. If the capsule is kept at a fixed charge Q, then V = Q / C changes by 1% too. With 48 V across it (the "phantom power" of studio microphones), that is a 0.48 V signal.

The microphone turns a change in d into a change in C, and then into a voltage. Many sensors (pressure, acceleration in your phone, touch) use the same idea.

### Capacitance is everywhere: stray capacitance

Any two conductors near each other form a capacitor, whether you wanted one or not. Two parallel copper traces on a circuit board, a wire and a metal case, the two leads of a resistor, or your body and the ground all have some capacitance, typically between a fraction of a picofarad and a few hundred picofarads. This is called **stray** or **parasitic** capacitance. It is tiny, but in fast circuits it slows edges (Lesson 04), and in high-impedance circuits it lets signals leak from one wire to another. Recognizing it starts with the formula you just learned: close conductors and large facing areas give more capacitance.

## Build It

The script is `code/main.py`:

```bash
uv run python phases/07-capacitors/02-capacitance/code/main.py
```

### Step 1: The parallel-plate formula

```python
EPSILON_0 = 8.854e-12


def plate_capacitance(area_m2, gap_m, relative_permittivity=1.0):
    return EPSILON_0 * relative_permittivity * area_m2 / gap_m
```

```
Parallel-plate capacitance C = eps0 * eps_r * A / d
  two 10 cm x 10 cm plates, 1 mm of air                0.089 nF
  same plates, gap shrunk to 0.1 mm                    0.885 nF
  same plates, 0.1 mm of polyester film                2.922 nF
  same plates, 0.1 mm of ceramic (X7R-like)         2656.200 nF
  a 1 m x 1 m sheet, 10 um of polyester             2921.820 nF
```

### Step 2: Area needed for a target value

```python
def plate_area_needed(target_farads, gap_m, relative_permittivity):
    return target_farads * gap_m / (EPSILON_0 * relative_permittivity)
```

```
Plate area for 1 uF with 1 mm of air: 113 m^2 (a square 11 m on a side)
Plate area for 1 uF with 5 um of polyester: 0.171 m^2 (rolled up inside a film capacitor)
```

### Step 3: Measure C with a constant current

We let the simulator push 1 mA into an empty capacitor and fit a straight line to the voltage. `current_source("I1", "0", "top", amps)` makes the current flow from ground, through the source, into node `top`.

```python
def ramp_with_constant_current(farads, amps=1e-3, t_stop=2e-3):
    circuit = Circuit()
    circuit.current_source("I1", "0", "top", amps)
    circuit.capacitor("C1", "top", "0", farads, v0=0.0)
    result = circuit.transient(t_stop=t_stop, dt=1e-6)
    time = np.asarray(result.time)
    volts = np.asarray(result.v("top"))
    slope = np.polyfit(time, volts, 1)[0]
    return slope, float(np.interp(1e-3, time, volts))
```

```
   0 --( I1 1 mA )--> top
                       |
                      C1
                       |
                       0
```

```
Pushing a steady 1 mA into different capacitors (simulated)
  capacitor  v after 1 ms (V)  slope (V/ms)  I / slope (uF)
     0.47uF             2.128         2.128           0.470
     1.00uF             1.000         1.000           1.000
     2.20uF             0.455         0.455           2.200
    10.00uF             0.100         0.100          10.000
```

Check one row by hand: 1 mA x 1 ms / 2.2 uF = 10^-6 / 2.2 x 10^-6 = 0.455 V. The simulator agrees and the recovered capacitance is exactly what we put in.

### Step 4: Q = C x V in a table

```
Q = C * V for a 47 uF capacitor
    1.0 V  ->     47.0 uC
    3.3 V  ->    155.1 uC
    5.0 V  ->    235.0 uC
   12.0 V  ->    564.0 uC
```

## Use It

- **Decoupling capacitors.** The 100 nF X7R ceramic next to every chip (code "104") is a tiny local tank of charge. Its high eps_r is what lets 100 nF fit in a 1 mm x 0.5 mm package (size 0402).
- **Bulk capacitors.** Electrolytics of 100-4700 uF smooth power rails. Their etched foil and nanometre oxide give the huge area-over-gap ratio.
- **Capacitive sensors.** A humidity sensor has a polymer dielectric whose eps_r changes as it absorbs water; a fuel-level sensor uses fuel as part of the dielectric. Both turn a physical quantity into a change of C.
- **Touch buttons and microphones.** A condenser (capacitor) microphone has a thin diaphragm as one plate; sound changes the gap d, which changes C.
- **Multimeters.** The capacitance range of a typical handheld meter charges the part with a known current and times the ramp, just like Step 3.

## Try It in the Lab

The lab task "Find the 1 V ramp" gives you a 1 mA current source and an empty slot for a capacitor. The goal is that the voltage on the capacitor is close to 1 V exactly 1 ms after the start. Before you try parts, write down what charge has flowed in 1 ms, then ask yourself which capacitance turns that charge into 1 V. Think also about what a capacitor ten times larger would do to the slope.

## Common Mistakes

- **Unit slips with prefixes.** 1 uF = 10^-6 F, 1 nF = 10^-9 F, 1 pF = 10^-12 F. Forgetting a factor of 1000 is the most common error with capacitors.
- **Using the area of both plates.** A in the formula is the area of **one** plate (the overlapping area).
- **Thinking the dielectric conducts a little.** An ideal dielectric conducts nothing; it polarizes. (Real ones leak a little; see Lesson 07.)
- **Ignoring the voltage rating.** A thinner dielectric gives more capacitance but breaks down at a lower voltage. Never put a 6.3 V capacitor on a 12 V rail.
- **Reading "104" as 104 pF.** It is 10 followed by four zeros: 100,000 pF = 100 nF.
- **Believing the voltage can jump.** I = C x dV/dt means a sudden voltage step needs infinite current. Circuits that try (a capacitor shorted across a battery) get huge current spikes, limited only by wire and internal resistance.

## Exercises

1. Two plates of 5 cm x 5 cm, 0.5 mm apart in air. What is C? What would it be with polypropylene (eps_r = 2.2)?
2. A capacitor is marked "473J". What is its value in nF and its tolerance?
3. A 10 uF capacitor receives a steady 50 uA. How long until it reaches 3.3 V from 0 V?
4. A capacitance meter pushes 10 uA into an unknown part and sees the voltage rise 2 V in 0.47 s. What is C?
5. A designer needs 1 nF with a breakdown of at least 500 V using a film with eps_r = 3 and a dielectric strength of 100 V per micrometre. What is the thinnest allowed film? What plate area is then needed?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Capacitance | "How much it holds" | Charge per volt, C = Q / V, set by geometry and material |
| Farad | "A unit" | One coulomb per volt; real parts are pF to mF, supercapacitors reach whole farads |
| Dielectric constant | "The k of the material" | eps_r, the factor by which a material increases C over vacuum by polarizing |
| Breakdown voltage | "Max volts" | The voltage at which the field rips electrons free and the dielectric conducts |
| I = C dV/dt | "The capacitor equation" | Current into a capacitor is capacitance times the rate of change of its voltage |
| MLCC | "Ceramic chip cap" | Multilayer ceramic capacitor, hundreds of thin ceramic layers stacked between electrodes |

## Further Reading

- [All About Circuits, Vol. I, Chapter 13: Factors Affecting Capacitance](https://www.allaboutcircuits.com/textbook/direct-current/chpt-13/factors-affecting-capacitance/) - plain-language discussion of area, distance and dielectric.
- [The Feynman Lectures on Physics, Vol. II, Chapter 10: Dielectrics](https://www.feynmanlectures.caltech.edu/II_10.html) - why polarization increases capacitance, from first principles.
- *The Art of Electronics*, 3rd ed., Horowitz & Hill, Section 1.4, and its companion *The Art of Electronics: The x-Chapters* (2020) for the practical differences between capacitor types.
- [Murata, "Basics of capacitors" (product articles)](https://article.murata.com/en-global/article/basics-of-capacitors-1) - how multilayer ceramic capacitors are built.
