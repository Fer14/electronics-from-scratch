# Conductors, Insulators and Semiconductors

> Every material holds electrons. What matters is how many of them are free to move, and that number ranges over more than thirty powers of ten.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 01 (The Physics Underneath), Lessons 01-04 (atoms and electrons, charge, the electric field, voltage); Phase 00, Lesson 04 (Scientific Notation and Orders of Magnitude)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Conductor | A material in which charge moves easily | A crowded dance floor where people can drift anywhere |
| Insulator | A material in which charge almost cannot move | A theatre where everyone is glued to their seat |
| Semiconductor | A material in between, whose ability to carry charge can be changed on purpose | A theatre where a few people are allowed to stand and walk, and you control how many |
| Free electron | An electron that is not tied to one particular atom and can wander through the material | A guest who left their table and walks around the party |
| Bound electron | An electron held tightly by its own atom | A guest who never leaves their chair |
| Carrier (charge carrier) | Anything charged that can move and so carry current: free electrons, holes, ions | Delivery vans carrying parcels (the parcels are the charge) |
| Carrier density | How many carriers sit in one cubic metre of material | How many vans are on the roads of a city |
| Resistivity (ρ, "rho") | How strongly a material, by its own nature, opposes the flow of charge, measured in ohm metres (Ω·m) | How hard it is to walk through a given kind of terrain: road, sand, swamp, wall |
| Conductivity (σ, "sigma") | The opposite of resistivity: 1/ρ, in siemens per metre (S/m) | How easy the terrain is to walk through |
| Energy band | A range of energies that electrons in a solid are allowed to have | A floor of a building where people may stand |
| Band gap | A range of energies electrons in a solid are not allowed to have; the "missing floor" | A staircase with several steps missing |
| Hole | The empty spot left when an electron leaves a bond; it behaves like a moving positive charge | An empty seat that "moves" backwards along a row as people shift over |
| Doping | Adding a tiny, controlled amount of another element to a semiconductor to change how many carriers it has | Adding a pinch of salt that completely changes the taste of a dish |
| Mobility (μ, "mu") | How fast a carrier drifts for a given push from an electric field | How quickly a person walks through a crowd when gently pushed |

## Learning Objectives

- Explain in plain words why copper conducts, glass does not, and silicon sits in between, using the idea of free electrons
- Read a resistivity table that spans about thirty orders of magnitude and place everyday materials on it
- Describe energy bands and the band gap without equations, and connect the size of the gap to how many carriers a material has
- Compute carrier densities and resistivities with simple formulas in Python, and see why one impurity atom in a million changes silicon by a factor of millions
- Predict whether warming a material raises or lowers its resistance, for a metal and for a semiconductor

## The Problem

Pick up a USB cable and cut it open (an old one). Inside you find shiny copper strands wrapped in soft plastic. The copper is there to carry charge from the charger to your phone. The plastic is there to stop charge from going anywhere else: into your fingers, into the other wire, into the table. Two materials sit a fraction of a millimetre apart, and one of them carries current about 10^20 times better than the other. That is not a small difference like "a car is faster than a bicycle". It is the difference between the width of an atom and the distance to a far galaxy.

Now open your phone. The processor inside is made mostly of silicon, a material that by itself is a poor conductor and a poor insulator. Engineers love it precisely because it is neither: by sprinkling in a few atoms of phosphorus or boron, they can make tiny regions conduct well and leave neighbouring regions blocking, and they can even switch a region between the two with a voltage. All of modern electronics rests on that trick.

So before we build any circuit we need to answer a physical question: what is it, inside a material, that decides whether charge can move through it? In Lesson 01 you met atoms and electrons, in Lesson 02 charge, in Lesson 03 the electric field that pushes charge, and in Lesson 04 voltage as energy per charge. This lesson asks: once there is a push, does anything actually move? The answer depends entirely on the material.

## The Physics

### Every material is full of electrons, but most are not free

A grain of salt, a drop of water, a copper coin and a glass marble all contain enormous numbers of electrons. A copper coin of a few grams holds around 10^24 of them. So "having electrons" is not what makes something a conductor. What matters is whether some of those electrons can leave their atom and roam.

Remember the picture from Lesson 01: an atom has a small positive nucleus and electrons around it, arranged in shells. The inner electrons are held very tightly. The outermost ones, the **valence electrons**, are held more loosely. What happens to those outer electrons when atoms pack together into a solid decides everything.

### Metals: a sea of shared electrons

In a metal like copper, each atom has one valence electron that is only weakly held. When billions of copper atoms sit side by side in a crystal, those outer electrons stop belonging to any one atom. They spread out over the whole piece of metal. Physicists call this the **electron sea** picture: a regular grid of positive copper ions, bathed in a gas of free electrons.

```
   copper: positive ions in a grid, free electrons everywhere between them

    (+)  e   (+)    e (+)  e  (+)
      e    e     e       e
    (+)    (+) e  (+)   (+) e
    e    e    e     e   e
    (+) e  (+)    (+) e  (+)

   (+) = copper ion (atom that gave away one electron)
    e  = free electron, wandering
```

Copper has roughly one free electron per atom. Count the atoms: copper has a density of 8960 kg/m^3 and a molar mass of 63.55 g/mol, so one cubic metre contains

```
atoms per m^3 = (8960 kg / 0.06355 kg per mol) x 6.022e23 per mol
              = 140 992 mol x 6.022e23
              = 8.49e28 atoms per m^3
```

and so about **8.5 x 10^28 free electrons per cubic metre**. That is the number we use throughout the course. Write it out: 85 000 000 000 000 000 000 000 000 000. A grain of sand's worth of copper (one cubic millimetre, 10^-9 m^3) holds 8.5 x 10^19 free electrons.

When you apply a voltage across a copper wire, the electric field (Lesson 03) pushes on every one of these free electrons. They do not need to be pulled out of anything; they are already loose. So a tiny push gives a large flow of charge. That is what "good conductor" means.

### Insulators: every electron is busy

In glass (mostly silicon dioxide), plastic or rubber, the outer electrons are locked into **chemical bonds** between neighbouring atoms. Each bond is a pair of electrons shared by two atoms, and those electrons are held firmly in place. There is no sea. To free an electron you would have to rip it out of its bond, and that costs a lot of energy, several electron-volts (you met the electron-volt, eV, in Lesson 04: the energy one electron gains crossing 1 volt).

At room temperature the random jiggling of atoms carries only about 0.026 eV of energy per "kick". Asking that kick to supply 9 eV is like asking a gentle breeze to lift a car. It essentially never happens. So a piece of glass may contain as many electrons as a piece of copper, yet almost none of them can move. Push on them with a field and they just shift a tiny bit inside their bonds and stop.

### Semiconductors: bonds that sometimes break

Silicon is in the same column of the periodic table as carbon. Each silicon atom has four valence electrons and bonds to four neighbours, building a crystal like diamond. Every electron is in a bond, just like an insulator. The difference is that silicon's bonds are much easier to break: about 1.12 eV instead of 5 to 10 eV.

```
   silicon crystal, flattened to 2-D (each = is a bond holding 2 electrons)

     Si = Si = Si = Si
     ||   ||   ||   ||
     Si = Si = Si = Si
     ||   ||   ||   ||
     Si = Si   Si = Si   <- one bond broken by heat:
     ||   ||  ^ ||   ||     the electron e is now free,
     Si = Si =|Si = Si      the empty spot (a "hole") is left behind
              e
```

At room temperature the random thermal kicks are still small compared with 1.12 eV, but they are not hopeless. Out of the enormous number of bonds, a tiny fraction break at any moment. Each break creates two carriers:

1. **A free electron** that wanders the crystal like the electrons in copper.
2. **A hole**: the bond the electron left now has a vacancy. A neighbouring bound electron can hop into it, which moves the vacancy one step the other way. The hole moves through the crystal like a bubble moves through water, and since it is a missing negative charge, it behaves like a positive charge.

That is why silicon conducts a little. How little? We will compute it below: around 10^16 free electrons per cubic metre in pure silicon at room temperature, compared with 8.5 x 10^28 in copper. Roughly ten trillion (10^13) times fewer.

### Bands: the gentle version

Physicists describe all of this with **energy bands**. In a single isolated atom, an electron can only have certain exact energies (the shells). When you pack a huge number of atoms into a crystal, each sharp energy level smears out into a **band**: a range of allowed energies. Between bands there can be **gaps** where no electron is allowed to sit.

Two bands matter for us:

- The **valence band**: the energies of electrons that are in bonds. Electrons here cannot carry current, because every spot is taken (like a car park that is completely full: no car can move).
- The **conduction band**: higher energies where electrons are free to move through the crystal (an empty car park above: a car lifted up there can drive anywhere).

The **band gap** is the energy step between the top of the valence band and the bottom of the conduction band.

```
      energy
        ^
        |   ___________          ___________          ___________
        |  | conduction|        | conduction|        | conduction|
        |  |  (empty)  |        |  (nearly  |        |  overlaps |
        |  |___________|        |   empty)  |        |  valence, |
        |                       |___________|        |  partly   |
        |     big gap              small gap         |  filled   |
        |     5-10 eV              ~1 eV             |           |
        |   ___________          ___________         |           |
        |  |  valence  |        |  valence  |        |           |
        |  |  (full)   |        |  (full)   |        |___________|
        |  |___________|        |___________|
        |
            INSULATOR           SEMICONDUCTOR            METAL
           (glass, PTFE)      (silicon, germanium)     (copper)
```

- **Metal:** no gap to cross. The highest-energy electrons already sit in a partly filled band and move freely.
- **Semiconductor:** a small gap. A few electrons get thermally kicked across and become free, leaving holes behind.
- **Insulator:** a big gap. Practically no electron ever makes it across.

What the band picture gets wrong if you take it too literally: the bands are not physical shelves in space. They are energies, and the "electron jumping up" is not a motion from one place to another but a change in the electron's state from bound to free. Keep that in mind and the picture is very useful.

### How many electrons get kicked across?

Here is the one formula of the lesson, in a simplified form good to roughly a factor of ten. Read it as a sentence first:

*The number of free carriers per cubic metre is roughly a big constant times a "chance" factor, and that chance factor falls off very steeply as the gap grows compared with the thermal energy.*

```
n  ≈  N_eff x exp( - E_gap / (2 k T) )
```

- `n` is the carrier density: free electrons per cubic metre.
- `N_eff` is about 2 x 10^25 per m^3 (a property of the crystal; we treat it as a fixed constant).
- `E_gap` is the band gap in electron-volts.
- `k` is Boltzmann's constant, 8.617 x 10^-5 eV per kelvin. It converts temperature into energy.
- `T` is the temperature in kelvin (room temperature is about 300 K, which is 27 °C).
- `exp(x)` means e^x, with e = 2.718... It is the function your calculator calls `e^x`.

At room temperature, `k T = 8.617e-5 x 300 = 0.0259 eV`. Now plug in silicon:

```
E_gap / (2 k T) = 1.12 / (2 x 0.0259) = 1.12 / 0.0517 = 21.66
exp(-21.66)     = 3.9e-10          (about 4 in ten billion)
n               = 2e25 x 3.9e-10   = 7.8e15 per m^3
```

The accepted measured value is about 1 x 10^16 per m^3, so our crude formula lands close. Now glass, with a gap of about 9 eV:

```
E_gap / (2 k T) = 9 / 0.0517 = 174
exp(-174)       = 2.5e-76
n               = 2e25 x 2.5e-76 = 5e-51 per m^3
```

That is less than one free electron in a block of glass the size of the Earth (about 10^21 m^3) by a factor of about 10^29. In reality glass carries a little current through other routes (impurities, slow-moving sodium ions, water on its surface), but the band picture explains why it is so very good at blocking.

The key lesson of the exponential: **a small change in the gap is a huge change in carriers**. Going from 1.12 eV (silicon) to 0.66 eV (germanium) only cuts the gap roughly in half, but multiplies the carriers by about 7000.

## The Concept

### Resistivity: a property of the material alone

You will meet resistance properly in Phase 03. For now think of it this way: a piece of material **resists** the flow of charge, and how much it resists depends on two things.

1. **What it is made of.** Copper resists little, glass resists enormously.
2. **Its shape.** A long thin wire resists more than a short fat one, just like a long thin straw is harder to drink through than a short wide one.

**Resistivity** captures the first part only: it is the material's built-in opposition to current, with the shape taken out. Its symbol is the Greek letter ρ ("rho") and its unit is the **ohm metre** (Ω·m). The ohm (Ω) is the unit of resistance; you met the name in Phase 00 and will learn exactly what it means in Phase 03.

As a preview of Phase 03, Lesson 02, the resistance of a uniform rod is:

*resistance equals resistivity times length, divided by the cross-section area.*

```
R = ρ x L / A
```

- `R` is resistance in ohms (Ω).
- `ρ` is resistivity in ohm metres (Ω·m).
- `L` is the length in metres (m).
- `A` is the cross-section area in square metres (m^2).

Worked example: a copper rod 1 m long with a cross-section of 1 mm^2. First convert: 1 mm = 0.001 m, so 1 mm^2 = 0.001 x 0.001 = 1 x 10^-6 m^2. Then:

```
R = 1.68e-8 Ω·m x 1 m / 1e-6 m^2 = 1.68e-2 Ω = 0.0168 Ω
```

Same rod in glass (ρ ≈ 10^12 Ω·m):

```
R = 1e12 x 1 / 1e-6 = 1e18 Ω
```

That is 10^18 ohms, a billion billion. Same shape, same size, a factor of 6 x 10^19 between them.

**Conductivity**, σ ("sigma"), is just the flip side: σ = 1/ρ, measured in **siemens per metre** (S/m). Copper: σ = 1 / 1.68e-8 = 5.95 x 10^7 S/m. Use whichever is more convenient; they hold the same information.

### The resistivity ladder

Here are typical room-temperature values. Exact numbers vary with purity and temperature (glass and wood can vary by a factor of 100 or more), but the orders of magnitude are what matter.

| Material | Resistivity (Ω·m) | Power of ten | Group |
|---|---|---|---|
| Silver | 1.59 x 10^-8 | -7.8 | conductor |
| Copper | 1.68 x 10^-8 | -7.8 | conductor |
| Gold | 2.44 x 10^-8 | -7.6 | conductor |
| Aluminium | 2.65 x 10^-8 | -7.6 | conductor |
| Iron | 9.7 x 10^-8 | -7.0 | conductor |
| Nichrome (heater wire) | 1.10 x 10^-6 | -6.0 | conductor |
| Graphite (pencil "lead") | ~1 x 10^-5 | -5 | conductor |
| Sea water | ~0.2 | -0.7 | in between |
| Germanium (pure) | 0.46 | -0.3 | semiconductor |
| Silicon (pure) | ~2.3 x 10^3 | 3.4 | semiconductor |
| Pure water | 1.8 x 10^5 | 5.3 | insulator |
| Dry wood | ~1 x 10^11 | 11 | insulator |
| Glass | ~1 x 10^12 | 12 | insulator |
| Rubber | ~1 x 10^13 | 13 | insulator |
| Fused quartz | 7.5 x 10^17 | 17.9 | insulator |
| PTFE (Teflon) | ~1 x 10^23 | 23 | insulator |

From silver to Teflon is about 31 powers of ten. No other everyday physical property varies that much across common materials. The "Power of ten" column is `log10(ρ)`: the exponent you would write in scientific notation (Phase 00, Lesson 04).

A few things worth noticing:

- **Silver beats copper**, but only by about 5 %. Copper is used for wires because it is far cheaper. Gold is used on connector contacts not because it conducts best but because it does not corrode.
- **Aluminium** conducts about 60 % as well as copper but weighs about a third as much, so long-distance power lines are aluminium.
- **Nichrome** is a "bad" metal on purpose: toasters and hair dryers use it so the wire gets hot.
- **Water** is interesting. Perfectly pure water is a fairly good insulator. Tap water, sweat and sea water contain dissolved salts whose ions (charged atoms) move and carry current. That is why wet hands and electricity are dangerous (Phase 00, Lesson 06).
- **Pure silicon** is closer to an insulator than to a metal. Its value also depends strongly on temperature and on tiny traces of impurities, which is exactly the point of the next sections.

### Carrier density times ease of motion

Why does copper conduct well? Two reasons multiply together:

1. **How many carriers** there are per cubic metre: `n`.
2. **How easily each one moves** when pushed: the **mobility** `μ`.

And each carrier carries the electron's charge `e = 1.602 x 10^-19` coulombs. Put together:

*conductivity equals number of carriers per cubic metre, times the charge of each, times how easily each moves.*

```
σ = n x e x μ          and so          ρ = 1 / (n x e x μ)
```

We can turn this around to estimate copper's mobility from numbers we already have:

```
μ = σ / (n x e)
  = 5.95e7 / (8.5e28 x 1.602e-19)
  = 5.95e7 / 1.362e10
  = 4.4e-3  m^2 per volt-second
```

The unit is strange but the meaning is simple: in a field of 1 volt per metre, a copper electron drifts at an average of 4.4 millimetres per second. Electrons in copper are actually not very mobile; they bump into vibrating ions constantly. Copper conducts well because it has a staggering number of them.

Electrons in pure silicon are about 30 times more mobile (μ ≈ 0.135 m^2/V·s) because the crystal is very orderly, but there are about 10^13 times fewer of them. Numbers win.

### The thermostat that runs backwards: temperature

Here is a fact that surprises everyone the first time.

- **Heat a metal** and its resistance goes **up**. The number of free electrons is fixed (one per atom), but the ions vibrate harder and the electrons bump into them more often. Copper's resistivity rises about 0.39 % per degree. A copper wire at 100 °C has about 31 % more resistance than at 20 °C.
- **Heat a semiconductor** and its resistance goes **down**, sharply. Hotter means harder thermal kicks, so many more bonds break and the carrier count shoots up. Pure silicon roughly doubles its carriers for every 10 °C of warming near room temperature.

Worked example for silicon from 300 K to 310 K, using our formula. Only the exponential changes:

```
at 300 K:  1.12 / (2 x 8.617e-5 x 300) = 21.66   exp(-21.66) = 3.91e-10
at 310 K:  1.12 / (2 x 8.617e-5 x 310) = 20.96   exp(-20.96) = 7.86e-10
ratio = 7.86e-10 / 3.91e-10 = 2.0
```

Ten degrees warmer, twice as many carriers. This is useful (temperature sensors called **thermistors** exploit it) and dangerous (a hot transistor can conduct more, get hotter, and run away; you will see that in Phase 18).

### Doping: the trick that built the modern world

Pure silicon has about 10^16 free electrons per m^3. Now replace **one silicon atom in every million** with a phosphorus atom. Phosphorus has five valence electrons instead of four. Four of them form bonds with the silicon neighbours; the fifth has no bond to join and is so loosely held that at room temperature it wanders off almost immediately.

```
     Si = Si = Si
     ||   ||   ||
     Si = P  = Si     P brings 5 outer electrons:
     ||   ||   ||     4 go into bonds, the 5th (e) is free
     Si = Si = Si
            e  ->
```

Silicon has about 5 x 10^28 atoms per m^3. One in a million of them is

```
donors = 5e28 x 1e-6 = 5e22 per m^3
```

each donating one free electron. That is **five million times** more carriers than pure silicon had. Using `ρ = 1 / (n e μ)` with silicon's electron mobility of 0.135:

```
ρ = 1 / (5e22 x 1.602e-19 x 0.135)
  = 1 / (1081)
  = 9.25e-4 Ω·m
```

A part-per-million impurity moved silicon's resistivity from thousands of ohm metres down to about one thousandth of an ohm metre, a factor of several million. And it can be done precisely, region by region, on a chip. Doping with boron (three valence electrons) does the reverse trick and creates extra holes. This is called **n-type** (extra negative electrons) and **p-type** (extra positive holes) silicon. Phase 11 ("Semiconductors and Diodes") builds diodes, LEDs and then, in Phase 12, transistors from exactly this idea. For now just remember: **silicon is special because we can choose how conductive it is.**

What the "pinch of salt" picture gets wrong: salt changes taste roughly in proportion to how much you add. Doping is wildly non-proportional at the start (the first part per million changes everything) and silicon's response depends on which element you add, not just how much.

## Build It

The script `code/main.py` turns all the numbers above into a small program. Run it from the repository root:

```
uv run python phases/01-the-physics-underneath/05-conductors-insulators-and-semiconductors/code/main.py
```

### Step 1: Constants and a material table

We store the electron charge, Boltzmann's constant in eV per kelvin, copper's free-electron density, silicon's atom density and our "effective states" constant. Then a list of materials with their resistivity and group, and a list of band gaps.

```python
import numpy as np

ELECTRON_CHARGE = 1.602176634e-19
BOLTZMANN_EV = 8.617e-5
COPPER_FREE_ELECTRONS = 8.5e28
SILICON_ATOMS = 5.0e28
EFFECTIVE_STATES = 2.0e25

MATERIALS = [
    ("silver", 1.59e-8, "conductor"),
    ("copper", 1.68e-8, "conductor"),
    ...
    ("PTFE (Teflon)", 1.0e23, "insulator"),
]

BAND_GAPS_EV = [
    ("germanium", 0.66),
    ("silicon", 1.12),
    ("gallium arsenide", 1.42),
    ("diamond", 5.5),
    ("glass (silica)", 9.0),
]
```

### Step 2: The formulas as functions

Each formula from The Concept becomes a one-line function. Reading the function name out loud should tell you what it computes.

```python
def resistance_of_rod(resistivity, length_m, area_m2):
    return resistivity * length_m / area_m2


def kicked_across_fraction(gap_ev, temperature_k):
    return np.exp(-gap_ev / (2 * BOLTZMANN_EV * temperature_k))


def carriers_per_m3(gap_ev, temperature_k):
    return EFFECTIVE_STATES * kicked_across_fraction(gap_ev, temperature_k)


def resistivity_from_carriers(carriers, mobility):
    return 1.0 / (carriers * ELECTRON_CHARGE * mobility)
```

### Step 3: The resistivity ladder as a text bar chart

We take `log10` of every resistivity (numpy does the whole array at once) and draw one `#` per order of magnitude above the best conductor. A bar chart on a log scale is the only way to fit 31 orders of magnitude on one screen.

```python
def print_resistivity_ladder():
    print("=== Resistivity ladder (ohm metres, room temperature) ===")
    resistivities = np.array([r for _, r, _ in MATERIALS])
    exponents = np.log10(resistivities)
    lowest = np.floor(exponents.min())
    for (name, rho, group), exponent in zip(MATERIALS, exponents):
        bar = "#" * int(round(exponent - lowest + 1))
        print(f"{name:15s} {rho:9.2e}  10^{exponent:6.1f}  {group:13s} {bar}")
    span = exponents.max() - exponents.min()
    print(f"Span from best conductor to best insulator: {span:.1f} orders of magnitude")
    print()
```

Part of the output:

```
copper           1.68e-08  10^  -7.8  conductor     #
silicon          2.30e+03  10^   3.4  semiconductor ############
glass            1.00e+12  10^  12.0  insulator     #####################
PTFE (Teflon)    1.00e+23  10^  23.0  insulator     ################################
Span from best conductor to best insulator: 30.8 orders of magnitude
```

### Step 4: Same rod, every material

`print_rod_resistances` applies `R = ρ L / A` to a rod 1 m long and 1 mm^2 thick (A = 1e-6 m^2). Copper gives 1.68e-02 Ω; Teflon gives 1.00e+29 Ω.

### Step 5: Copper's mobility

```python
def print_copper_mobility():
    print("=== How freely do copper's electrons move? ===")
    copper_rho = 1.68e-8
    conductivity = 1.0 / copper_rho
    mobility = conductivity / (COPPER_FREE_ELECTRONS * ELECTRON_CHARGE)
    ...
```

It prints a conductivity of 5.952e+07 S/m and a mobility of 4.37e-03 m^2/(V·s), matching the hand calculation. It also divides 8.5e28 by copper's atom density 8.49e28 to confirm roughly 1.00 free electron per atom.

### Step 6: Band gaps decide the carrier count

```python
def print_band_gap_table(temperature_k):
    print(f"=== Band gaps and carriers at {temperature_k:.0f} K ===")
    print(f"kT = {BOLTZMANN_EV * temperature_k:.4f} eV")
    for name, gap in BAND_GAPS_EV:
        fraction = kicked_across_fraction(gap, temperature_k)
        carriers = carriers_per_m3(gap, temperature_k)
        print(f"{name:17s} gap = {gap:4.2f} eV  factor = {fraction:9.2e}  carriers = {carriers:9.2e} per m^3")
    ratio = COPPER_FREE_ELECTRONS / carriers_per_m3(1.12, temperature_k)
    print(f"Copper has {ratio:.1e} times more free electrons than pure silicon")
```

Output:

```
germanium         gap = 0.66 eV  factor =  2.86e-06  carriers =  5.72e+19 per m^3
silicon           gap = 1.12 eV  factor =  3.91e-10  carriers =  7.82e+15 per m^3
gallium arsenide  gap = 1.42 eV  factor =  1.18e-12  carriers =  2.36e+13 per m^3
diamond           gap = 5.50 eV  factor =  6.31e-47  carriers =  1.26e-21 per m^3
glass (silica)    gap = 9.00 eV  factor =  2.51e-76  carriers =  5.03e-51 per m^3
Copper has 1.1e+13 times more free electrons than pure silicon
```

The measured values are about 2.4e19 for germanium, 1e16 for silicon and 2e12 for gallium arsenide. Our one-constant model is within a factor of about ten, which is good enough to understand why the gap matters so much.

### Step 7: Heat it up

`print_temperature_effect` loops over 250, 300, 350 and 400 K. Copper's resistivity rises gently (1.40e-8 to 2.38e-8 Ω·m) while silicon's carriers explode (1.03e14 to 1.76e18 per m^3, a factor of about 17 000). The last line confirms the "doubling every 10 degrees" rule: `2.01`.

### Step 8: Dope it

```python
def print_doping():
    electron_mobility_silicon = 0.135
    hole_mobility_silicon = 0.048
    intrinsic = 1.0e16
    pure_rho = 1.0 / (intrinsic * ELECTRON_CHARGE * (electron_mobility_silicon + hole_mobility_silicon))
    donors = SILICON_ATOMS * 1e-6
    doped_rho = resistivity_from_carriers(donors, electron_mobility_silicon)
    ...
```

Pure silicon has both electrons and holes, so we add both mobilities. The script prints a pure resistivity of 3.41e+03 Ω·m (the table's 2.3e3 uses a slightly higher measured carrier count; both say "thousands of ohm metres"), a doped resistivity of 9.25e-04 Ω·m, and an improvement factor of 3.7e+06.

## Use It

- **Wires and cables.** Copper (or aluminium in power lines) inside, PVC or rubber outside. A cable datasheet lists conductor resistance in Ω per km: a 1.5 mm^2 copper household wire is about 12 Ω/km, which you can check with `R = ρ L / A`: 1.68e-8 x 1000 / 1.5e-6 = 11.2 Ω.
- **Printed circuit boards.** The green board in every gadget is a glass-fibre and epoxy insulator (FR-4, resistivity around 10^12 Ω·m or more) with thin copper tracks on top. Phase 21 designs one.
- **Heating elements.** Toasters, kettles and 3D-printer hot ends use nichrome or similar alloys, chosen for high resistivity and resistance to oxidation.
- **Thermistors.** An NTC thermistor ("negative temperature coefficient") is a semiconductor bead whose resistance falls as it warms, exactly the silicon behaviour above. A common part is 10 kΩ at 25 °C and about 3.6 kΩ at 50 °C. They sit inside battery packs and 3D printers to measure temperature.
- **Chips.** A silicon wafer is grown with a specified resistivity (often between 1 and 100 Ω·cm, that is 0.01 to 1 Ω·m), already lightly doped, then doped further in tiny regions to make transistors. The resistivity is printed on the wafer's specification sheet.
- **Insulation ratings.** Cables and connectors list a maximum voltage. Every insulator eventually breaks down if the field is strong enough (dry air at about 3 million volts per metre, which is how lightning and sparks happen). Resistivity tells you how little current leaks at normal voltages; breakdown tells you where it stops being an insulator at all.

## Common Mistakes

- **"Insulators have no electrons."** They have just as many. Their electrons are bound in bonds, not free.
- **"Conductors make electricity."** A conductor does not create charge or energy. It only lets charge that is already there move when something pushes it.
- **Confusing resistivity with resistance.** Resistivity (Ω·m) belongs to the material. Resistance (Ω) belongs to an object of a particular shape. A thick copper bar and a thin copper hair have the same resistivity but very different resistances.
- **Treating "conductor" and "insulator" as yes/no.** It is a continuous scale over 30 orders of magnitude. Wet wood, skin and dirty glass are all "insulators" that conduct enough to hurt you at high voltage.
- **Thinking semiconductors are "half-conductors" that conduct half as well.** Pure silicon conducts about 10^11 times worse than copper. What makes it a semiconductor is that its conductivity can be controlled: by heat, light, doping and (in transistors) by voltage.
- **Expecting resistance to go down when a metal heats up.** For metals it goes up. A cold light-bulb filament has roughly a tenth of its hot resistance, which is why bulbs tend to fail at the moment you switch them on.
- **Forgetting the exponential.** A gap of 1.1 eV versus 0.7 eV sounds like a small difference. Through `exp(-E_gap / 2kT)` it becomes a factor of thousands.

## Exercises

1. **Gold contacts.** A gold-plated connector pin is 5 mm long with a cross-section of 0.5 mm^2. Using ρ = 2.44 x 10^-8 Ω·m, compute its resistance. (Remember to convert mm and mm^2 to m and m^2.)
2. **Copper or aluminium?** A 100 m power cable must have the same resistance whether you make it from copper or aluminium. If the copper version has a cross-section of 10 mm^2, what cross-section does the aluminium one need? Using densities 8960 kg/m^3 for copper and 2700 kg/m^3 for aluminium, which cable is lighter, and by how much?
3. **Free electrons in a coin.** A copper coin has a volume of 0.4 cm^3. How many free electrons does it contain? What is their total charge in coulombs? (Why doesn't the coin fly apart? Hint: Lesson 02.)
4. **Germanium versus silicon.** Using `n ≈ 2e25 x exp(-E_gap / 2kT)` at 300 K, compute the ratio of carriers in germanium (0.66 eV) to silicon (1.12 eV). Then repeat at 350 K. Does the ratio grow or shrink when it gets hotter? Modify `main.py` to print it.
5. **How much doping?** You want n-type silicon with a resistivity of 0.01 Ω·m. Using ρ = 1 / (n e μ) with μ = 0.135 m^2/(V·s), how many donor atoms per m^3 do you need? What fraction of silicon atoms (5 x 10^28 per m^3) is that? Express it as "one in N".

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Conductor | "Lets electricity through" | Has a huge number of free carriers (about 10^28 per m^3 in metals), so a small field gives a large current |
| Insulator | "Blocks electricity" | Its electrons are tied up in bonds behind a large band gap; resistivity typically above 10^10 Ω·m |
| Semiconductor | "Half conductor" | A small band gap (about 1 eV) so carrier count is low but controllable by temperature, light and doping |
| Resistivity ρ | "How resistive a material is" | Resistance of a 1 m x 1 m^2 block of the material, in Ω·m; shape-independent |
| Conductivity σ | "How conductive a material is" | σ = 1/ρ = n e μ, in siemens per metre |
| Free electron | "The electrons that move" | An electron in the conduction band (or the electron sea of a metal), not tied to one atom |
| Hole | "A positive charge in silicon" | A missing electron in a bond; neighbours hop into it so the vacancy moves like a positive carrier |
| Band gap | "Energy needed to free an electron" | The forbidden energy range between valence and conduction bands, in eV |
| Doping | "Adding impurities" | Deliberately adding a few parts per million of another element to set the number and type of carriers |
| Mobility μ | "How fast electrons go" | Average drift speed per unit field, in m^2/(V·s) |

## Further Reading

- Richard Feynman, *The Feynman Lectures on Physics*, Vol. III, chapter 14 ("Semiconductors"), free online at feynmanlectures.caltech.edu: holes and doping explained by the master.
- All About Circuits, *Textbook Vol. I (DC)*, chapter "Basic Concepts of Electricity" (conductors, insulators and electron flow) and Vol. III chapter "Solid-State Device Theory" (bands and doping).
- HyperPhysics (Georgia State University), pages "Band Theory of Solids" and "Resistivity and Temperature Coefficient", hyperphysics.phy-astr.gsu.edu: compact tables of resistivities and band gaps.
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Cambridge University Press, 2015: chapter 1 for practical conductors and resistors, chapter 2 for what doped silicon becomes.
