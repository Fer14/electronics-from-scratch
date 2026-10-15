# Atoms and Electrons

> Every wire is a crowd of atoms, and every atom gives up one tiny, light, charged passenger that is free to move. Electronics is the art of telling those passengers where to go.

**Type:** Learn
**Prerequisites:** Phase 00 (Words and Units), especially Lesson 02 (The Vocabulary) and Lesson 04 (Scientific Notation and Orders of Magnitude)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Atom | The smallest piece of a chemical element that is still that element | One brick in a huge wall: the wall is copper, each brick is a copper atom |
| Nucleus | The tiny, heavy centre of an atom | The pit in a cherry, except far smaller compared with the fruit |
| Proton | A heavy particle in the nucleus that carries positive charge | A heavy anchor that holds the atom in place |
| Neutron | A heavy particle in the nucleus with no charge | A second anchor that adds weight but takes no side |
| Electron | A very light particle around the nucleus that carries negative charge | A moth buzzing around a lamp |
| Charge | The property that makes particles push or pull on each other electrically | Like the "N" and "S" of magnets, a label that decides attraction or repulsion (Lesson 02 makes this precise) |
| Elementary charge (e) | The size of the charge on one proton or one electron: 1.602 x 10^-19 coulombs | The smallest coin in a currency: every amount is a whole number of these coins |
| Coulomb (C) | The SI unit of charge | A "bucket" that holds about 6.24 x 10^18 electrons' worth of charge |
| Shell | A group of electrons at roughly the same distance and energy around the nucleus | Rows of seats in a theatre around the stage |
| Valence electron | An electron in the outermost shell, the most loosely held | A guest in the back row, easiest to leave the theatre |
| Free electron | A valence electron that has left its own atom and wanders through the whole metal | A guest who leaves the theatre and walks the streets of the city |
| Ion | An atom that has lost or gained electrons, so it is no longer neutral | A theatre with one empty seat, or one extra person standing |
| Mole | A counting unit: 6.022 x 10^23 things | Like "a dozen" (12), but enormous |

## Learning Objectives

- Describe an atom as a tiny heavy nucleus (protons and neutrons) surrounded by light electrons, and state the mass and charge of each particle
- Explain what a valence electron is and why copper, silver and gold each have exactly one
- Count the atoms and free electrons in a real piece of copper wire using density, molar mass and Avogadro's number
- Explain why an ordinary wire has zero net charge even though it contains hundreds of thousands of coulombs of electrons
- Describe J.J. Thomson's 1897 cathode-ray experiment and what "charge-to-mass ratio" tells us
- Explain, with numbers, why electrons (not protons) are the particles that move in a wire

## The Problem

You flip a light switch and the lamp turns on. In Phase 00 we said "current flows through the wire". But what, exactly, is flowing? The copper wire does not get lighter. Nothing drips out of the end. The wire does not visibly change at all, yet it delivers enough energy to light a room.

To understand anything else in this course (voltage, current, resistance, why a diode only conducts one way, why a transistor can switch a billion times a second) you need a picture of what is inside the wire. Without it, every rule you learn later is a magic spell: you can recite it but you cannot reason with it. With it, the rules become obvious consequences of a few particles pushing and pulling on each other.

So this lesson zooms in. We take a 1 metre piece of ordinary household wire, the kind inside a lamp cord, and count what is in it. The numbers are huge, and they explain a lot: why a wire can carry current without running out of "stuff", why touching a wire does not shock you when nothing is connected, and why it is the electrons, not the rest of the atom, that do the moving.

## The Physics

### A short history of "what is matter made of"

The ancient Greeks guessed that matter was made of tiny indivisible pieces, *atomos* ("uncuttable"). For two thousand years that was a philosophical guess. In the early 1800s John Dalton showed that chemical reactions always combine elements in fixed whole-number ratios, which is exactly what you would expect if each element were made of identical little units. Chemists then measured how heavy those units are relative to each other.

Nobody, however, knew what was *inside* an atom, or even whether it had an inside. That changed in **1897**, when **J.J. Thomson** in Cambridge studied *cathode rays*: the glow that appears in a glass tube with most of the air pumped out and a high voltage between two metal plates. (Voltage is the "electrical push" we met in Phase 00; Lesson 04 of this phase defines it properly.)

```
   glass tube, almost no air inside
  +-------------------------------------------------+
  |  cathode (-)                      anode (+)     |
  |   |||  ----- beam of "rays" ----->   |  glow    |
  |   |||                                |  on the  |
  |                                          glass  |
  +-------------------------------------------------+
          bend the beam with charged plates
          or a magnet, and measure how much it bends
```

Thomson bent the beam with charged plates and with magnets. From how much it bent he worked out two things:

1. The rays were made of **particles with negative charge** (they were pulled toward the positive plate).
2. The ratio "charge divided by mass" of these particles was enormous: about **1800 times larger** than for a charged hydrogen atom, the lightest thing known.

Whatever these particles were, they were either far more charged or far lighter than an atom. Thomson argued they were tiny pieces *of* atoms, and that every element contained them, because he got the same particle no matter which metal the cathode was made of. The particle was later named the **electron**. It was the first subatomic particle ever discovered.

In **1909** Robert Millikan measured the electron's charge directly (we will meet his oil-drop experiment in Lesson 02), and once you know both the ratio and the charge, you know the mass: about 1/1836 of a hydrogen atom.

In **1911** Ernest Rutherford fired small particles at very thin gold foil. Most passed straight through, but a few bounced back almost the way they came. His conclusion: almost all of an atom's mass is packed into a tiny, positively charged centre, the **nucleus**, and the rest is nearly empty space where the electrons live. Niels Bohr (1913) then proposed that electrons sit in fixed "shells" at definite energies. Modern quantum mechanics has replaced Bohr's neat circular orbits with fuzzy clouds, but the shell idea is still the best beginner picture, and it is the one we use.

### The three particles

An atom is built from three kinds of particles:

| Particle | Where | Mass | Charge |
|----------|-------|------|--------|
| Proton | nucleus | 1.6726 x 10^-27 kg | +1 e = +1.602 x 10^-19 C |
| Neutron | nucleus | 1.6749 x 10^-27 kg | 0 |
| Electron | around the nucleus | 9.109 x 10^-31 kg | -1 e = -1.602 x 10^-19 C |

Read the masses out loud: a proton weighs 1.67 times ten to the minus 27 kilograms. That is 0.000...0167 with 26 zeros after the decimal point. An electron is about **1836 times lighter** still. Check it:

```
1.6726e-27 / 9.109e-31 = 1836.2
```

The charges are where the story gets interesting. A proton and an electron carry charges that are **exactly equal in size and opposite in sign**. Nobody has ever measured the slightest difference. We call that size the **elementary charge**, written **e**:

```
e = 1.602176634 x 10^-19 C
```

C is the **coulomb**, the SI unit of charge (named after Charles-Augustin de Coulomb, Lesson 02). One coulomb is a lot of electrons:

```
1 C / 1.602e-19 C per electron = 6.24 x 10^18 electrons
```

That is six billion billion electrons. Keep that number in mind; it shows up again in Lesson 06 when we count electrons per second in a current.

### Neutral atoms

An atom of an element always has the same number of protons. That number is the **atomic number**, often written Z:

- Hydrogen: 1 proton
- Carbon: 6 protons
- Silicon: 14 protons (the heart of every chip, Phase 11)
- Copper: 29 protons

A normal, undisturbed atom has exactly as many electrons as protons. Its total charge is then

```
total charge = (number of protons) x (+e) + (number of electrons) x (-e) = 0
```

So copper has 29 protons, 29 electrons, and a net charge of zero. We say the atom is **neutral**. If it loses an electron it has one more proton than electrons and a net charge of +e: it has become a **positive ion**. If it gains one, it is a **negative ion**.

What the picture gets wrong: "the atom has charge zero" does not mean "there is no charge in it". There is a lot of charge, perfectly balanced. Remember this, because a copper wire is the same story at a gigantic scale.

### Sizes: an atom is mostly empty

A copper atom is about 2.6 x 10^-10 m across (a quarter of a nanometre). Its nucleus is about 10^-14 m across. The ratio is

```
2.6e-10 / 1.0e-14 = 26,000
```

Blow the atom up to the size of a 100 metre football stadium. The nucleus becomes

```
1.0e-14 m x (100 m / 2.6e-10 m) = 0.0038 m = 3.8 mm
```

a small pea on the centre spot. Yet that pea holds 99.97% of the atom's mass. The electrons buzz around the stands. Everything between is empty.

### Shells and valence electrons

In the Bohr-style picture, electrons fill **shells** from the inside out. The first shell holds at most 2 electrons, the second at most 8, the third up to 18 (the real rules are a bit more complicated, but these numbers are right for the atoms we care about). Here are some elements drawn as shells:

```
 hydrogen (1)      carbon (6)        silicon (14)            copper (29)

     .              . . . .         . . . .             .
    (+)            ( (+) )         ( ( (+) ) )         ( ( ( (+) ) ) )
                     2   4           2  8  4              2  8  18  1
```

The numbers under each atom are how many electrons sit in each shell, innermost first.

The electrons in the **outermost** shell are called **valence electrons**. They matter most because:

- They are farthest from the nucleus, so the positive nucleus holds them least tightly.
- The inner electrons partly "shield" them: from far away, 28 negative inner electrons cancel 28 of copper's 29 protons, so the outermost electron only feels a net pull of about +1 e.

Copper's last shell has a **single electron**, alone in the back row. The same is true of silver (2, 8, 18, 18, 1) and gold. Not by coincidence, copper, silver and gold are the three best conductors of electricity among ordinary metals.

Silicon has 4 valence electrons. That half-full outer shell is why silicon is neither a good conductor nor a good insulator, a "semiconductor" (Lesson 05 previews this; Phase 11 builds on it).

### From one atom to a piece of metal: free electrons

When copper atoms pack together into a solid, something remarkable happens. The lonely valence electron of each atom is held so weakly that it no longer belongs to any particular atom. It wanders through the whole piece of metal. What is left behind at each spot in the crystal is a **copper ion** with charge +e, locked in place by its neighbours.

```
   +     +     +     +     +        + = copper ion (29 protons, 28 electrons), fixed
      -      -    -     -           - = free electron, wandering
   +     +     +     +     +
    -     -      -    -    -
   +     +     +     +     +
```

Physicists call this the "electron sea" or "electron gas". The free electrons move at enormous random speeds (around a million metres per second in copper), bouncing around in every direction, but on average they go nowhere, like a swarm of gnats that stays in one spot even though every gnat is flying fast.

When we connect a battery, we add a tiny steady push on top of that random motion, and the whole sea slowly drifts in one direction. *That drift is an electric current.* Lesson 06 measures how slow the drift is (spoiler: fractions of a millimetre per second).

### Why electrons, and not protons, do the moving

Two reasons, both physical:

1. **The protons are trapped.** They sit inside nuclei, and the nuclei are locked into the crystal of the solid. Moving a proton means moving a whole copper ion out of its place in the crystal, which a battery simply cannot do in a wire.
2. **Electrons are light.** Even if something pushes on an electron and on a proton with the same force, the electron accelerates 1836 times more. Newton's second law says acceleration = force / mass (a = F / m), and the electron's mass is 1836 times smaller.

There are places where positive particles do move: in batteries, in salt water, in your nerves, ions carry the current. And in semiconductors (Phase 11) a missing electron, a "hole", behaves like a moving positive charge. But in every wire and in every metal part of a circuit, the movers are electrons.

## The Concept

### Idea 1: charge comes in whole numbers of e

Every amount of charge you will ever meet on an object is a whole number of elementary charges:

```
Q = n x e        n is a whole number (positive, negative or zero)
```

Read it as: "the charge Q equals some count n of electrons gained or lost, times the charge of one electron". You never find half an electron's worth of charge on a balloon or a wire. (Quarks inside protons carry thirds of e, but they never appear alone, so for electronics, e is the smallest piece.)

### Idea 2: counting atoms with density and Avogadro's number

To count atoms in a piece of copper we chain three facts:

- **Density** of copper: 8960 kg per cubic metre (a 1 m cube of copper would weigh almost 9 tonnes).
- **Molar mass** of copper: 63.55 grams per mole, i.e. 0.06355 kg per mole. A **mole** is just a counting unit like "a dozen", but it means 6.022 x 10^23 things (**Avogadro's number**). Chemists chose it so that a mole of an element weighs, in grams, about its number of protons plus neutrons.
- **Avogadro's number**: 6.022 x 10^23 atoms per mole.

Then, in words: "kilograms per cubic metre, divided by kilograms per mole, gives moles per cubic metre; times atoms per mole, gives atoms per cubic metre".

```
moles per m^3 = 8960 / 0.06355           = 140,991 mol/m^3
atoms per m^3 = 140,991 x 6.022e23       = 8.49 x 10^28 atoms/m^3
```

Since each copper atom releases one free electron, copper has about **8.5 x 10^28 free electrons per cubic metre**. That number (8.5e28) is used everywhere in this course.

### Worked example: 1 metre of lamp cord

A common household wire has a copper cross-section of 1.5 mm^2 (square millimetres). One square millimetre is 10^-6 m^2 (a millimetre is 10^-3 m, squared gives 10^-6). So 1 metre of it has volume

```
volume = length x area = 1 m x 1.5e-6 m^2 = 1.5e-6 m^3 = 1.5 cm^3
```

(One cubic centimetre is 10^-6 m^3, a sugar cube.) Its mass:

```
mass = density x volume = 8960 x 1.5e-6 = 0.01344 kg = 13.44 g
```

About the mass of three coins. The number of atoms:

```
atoms = 8.49e28 atoms/m^3 x 1.5e-6 m^3 = 1.27 x 10^23 atoms
```

One hundred and twenty-seven thousand billion billion atoms, each lending one free electron. If you counted one electron per second, you would need about 4 x 10^15 years, a few hundred thousand times the age of the universe.

### Worked example: the charge hiding in the wire

Each copper atom has 29 electrons, so the wire holds

```
electrons = 29 x 1.274e23 = 3.69 x 10^24 electrons
charge    = 3.69e24 x (-1.602e-19 C) = -5.9 x 10^5 C
```

Almost six hundred thousand coulombs of negative charge, in a piece of wire you can hold in your hand. And exactly the same amount of positive charge in the protons. Net: zero. Even the free electrons alone carry

```
1.274e23 x (-1.602e-19 C) = -2.04 x 10^4 C
```

twenty thousand coulombs. A phone charger pushes about 1 coulomb per second through its cable. So the wire is not "filled" by the charger; it was always full. The charger just sets the existing electron sea in motion. That is why current starts everywhere in a circuit almost instantly when you close a switch: the movers are already there, along the whole wire.

Picture a bicycle chain: when you push the pedal, every link moves at once, not because a link travelled from the pedal to the wheel, but because the chain was full of links all along.

What the chain picture gets wrong: chain links are rigidly connected, while electrons push each other through their electric charge and bounce around randomly. The signal still travels fast (a sizeable fraction of the speed of light, Lesson 06) even though each electron creeps.

### Worked example: Thomson's ratio

The charge-to-mass ratio (e/m) of the electron:

```
e / m = 1.602e-19 C / 9.109e-31 kg = 1.759 x 10^11 C/kg
```

For a hydrogen ion (a bare proton):

```
e / m = 1.602e-19 C / 1.6726e-27 kg = 9.58 x 10^7 C/kg
```

Ratio: 1.759e11 / 9.58e7 = 1836. Thomson's measured value was rougher, but in the same ballpark, and that ratio alone told him he had found something far lighter than any atom.

### Worked example: the same push on an electron and a proton

Push each with a force of 10^-15 newtons (a newton, N, is the SI unit of force; 1 N is roughly the weight of a small apple). Acceleration is force divided by mass:

```
electron: a = 1e-15 / 9.109e-31  = 1.10 x 10^15 m/s^2
proton:   a = 1e-15 / 1.6726e-27 = 5.98 x 10^11 m/s^2
```

Starting from rest, the distance covered in time t is d = (1/2) x a x t^2. After one nanosecond (10^-9 s):

```
electron: 0.5 x 1.10e15 x (1e-9)^2 = 5.5 x 10^-4 m = 0.55 mm
proton:   0.5 x 5.98e11 x (1e-9)^2 = 3.0 x 10^-7 m = 0.30 um
```

(um is micrometre, a millionth of a metre.) The electron moves almost two thousand times further. And in a wire the proton cannot move at all, because it is locked in the crystal. Electrons win on both counts.

## Build It

The program `code/main.py` redoes every calculation above. Run it from the repository root:

```
uv run python phases/01-the-physics-underneath/01-atoms-and-electrons/code/main.py
```

### Step 1: The three particles

We store each particle's mass and its charge as a count of e, then print both.

```python
ELEMENTARY_CHARGE = 1.602176634e-19
ELECTRON_MASS = 9.109e-31
PROTON_MASS = 1.6726e-27
NEUTRON_MASS = 1.6749e-27

PARTICLES = {
    "proton": (PROTON_MASS, +1),
    "neutron": (NEUTRON_MASS, 0),
    "electron": (ELECTRON_MASS, -1),
}

for name, (mass, charge_units) in PARTICLES.items():
    charge = charge_units * ELEMENTARY_CHARGE
    print(f"  {name:8s} mass = {mass:.4e} kg   charge = {charge:+.4e} C   ({charge_units:+d} e)")
print(f"  proton mass / electron mass = {PROTON_MASS / ELECTRON_MASS:.1f}")
```

Output: the proton/electron mass ratio is 1836.2.

### Step 2: Shells and valence electrons

A small table of real shell fillings. The `assert` checks that the electrons in all shells add up to the number of protons, so each atom is neutral. The valence count is simply the last shell.

```python
SHELLS = {
    "hydrogen": (1, [1]),
    "silicon": (14, [2, 8, 4]),
    "copper": (29, [2, 8, 18, 1]),
    "silver": (47, [2, 8, 18, 18, 1]),
}

for element, (protons, shells) in SHELLS.items():
    assert sum(shells) == protons
    print(f"  {element:9s} {protons:2d} protons  shells {str(shells):20s} valence electrons = {shells[-1]}")
```

(The script includes a few more elements: helium, carbon, neon, sodium.)

### Step 3: Sizes

```python
atom_diameter = 2.6e-10
nucleus_diameter = 1.0e-14
scale = 100.0 / atom_diameter
print(f"  ratio atom / nucleus   = {atom_diameter / nucleus_diameter:,.0f}")
print(f"  if the atom were a 100 m stadium, the nucleus would be {nucleus_diameter * scale * 1000:.1f} mm wide")
```

Output: ratio 26,000; the nucleus would be 3.8 mm wide.

### Step 4: Counting atoms in a copper wire

```python
AVOGADRO = 6.022e23
COPPER_DENSITY_KG_PER_M3 = 8960.0
COPPER_MOLAR_MASS_KG_PER_MOL = 0.06355


def atoms_per_cubic_meter(density, molar_mass):
    return density / molar_mass * AVOGADRO


def wire_volume(length_m, area_mm2):
    return length_m * area_mm2 * 1e-6


atoms_m3 = atoms_per_cubic_meter(COPPER_DENSITY_KG_PER_M3, COPPER_MOLAR_MASS_KG_PER_MOL)
volume = wire_volume(1.0, 1.5)
atoms_in_wire = atoms_m3 * volume
```

Output: 8.490e+28 atoms per m^3, a 13.44 g wire, 1.274e+23 atoms and the same number of free electrons.

### Step 5: The charge hiding in the wire

```python
all_electrons = atoms_in_wire * COPPER_PROTONS
negative_charge = -all_electrons * ELEMENTARY_CHARGE
positive_charge = atoms_in_wire * COPPER_PROTONS * ELEMENTARY_CHARGE
free_charge = -atoms_in_wire * ELEMENTARY_CHARGE
```

Output: -5.917e+05 C of electrons, +5.917e+05 C of protons, net 0.0 C, and -2.040e+04 C carried by the free electrons alone.

### Step 6: Thomson's charge-to-mass ratio

```python
def charge_to_mass_ratio(charge, mass):
    return charge / mass


electron_ratio = charge_to_mass_ratio(ELEMENTARY_CHARGE, ELECTRON_MASS)
hydrogen_ion_ratio = charge_to_mass_ratio(ELEMENTARY_CHARGE, PROTON_MASS)
```

Output: 1.759e+11 C/kg for the electron, 9.579e+07 C/kg for the hydrogen ion, a factor of 1836.

### Step 7: Why electrons are the movers

We use numpy to do both particles in one line: an array of two accelerations, then an array of two distances.

```python
force = 1e-15
accelerations = np.array([force / ELECTRON_MASS, force / PROTON_MASS])
time = 1e-9
distances = 0.5 * accelerations * time**2
```

Output: the electron covers 0.549 mm in a nanosecond, the proton 0.299 um.

## Use It

- **Why wires are copper.** Copper gives one free electron per atom, is cheap, easy to draw into thin wire and does not corrode badly. Silver conducts about 6% better but costs far more; it is used only in special contacts and some high-frequency parts. Gold (also one valence electron) conducts a little worse than copper but never tarnishes, which is why connector pins and the pads of a SIM card are gold-plated.
- **Aluminium power lines.** Aluminium has 3 valence electrons per atom and conducts worse than copper for the same thickness, but it is so light that for long overhead lines it wins per kilogram.
- **The cathode-ray tube.** Thomson's tube became the old television and oscilloscope screen: a beam of electrons, steered by charged plates or magnets, painting light on phosphor. Phase 06 shows the modern oscilloscope that replaced it.
- **Chip wiring.** Inside a modern processor, the tiny wires connecting billions of transistors are copper (since the late 1990s; before that, aluminium). Some of them are only a few dozen atoms wide, so "counting atoms in a wire" is a real engineering question there.

## Common Mistakes

- **"Current is electrons coming out of the battery and travelling to the bulb."** The electrons were already in the wire. The battery pushes the whole sea at once; each electron moves only a tiny distance.
- **"A neutral object has no charge in it."** It has huge, balanced amounts of positive and negative charge. "Neutral" means "net zero", not "empty".
- **"Protons flow in the opposite direction to electrons."** In a metal wire, protons do not flow at all. They are locked inside fixed ions. (The "opposite direction" idea comes from the sign convention for current, which Lesson 02 and Lesson 06 explain.)
- **"Electrons orbit the nucleus like planets."** Bohr's picture is a useful cartoon, not reality. Electrons are spread out in fuzzy clouds. For electronics, the cartoon is enough: inner electrons are held tightly, the outermost loosely.
- **"More electrons in an atom means a better conductor."** What matters is how loosely the outermost electrons are held, not how many electrons there are in total. Lead has 82 electrons and is a mediocre conductor; copper with 29 is excellent.

## Exercises

1. **Counting electrons in a coulomb.** How many electrons make up -2 C of charge? Show the division.
2. **A thinner wire.** Repeat the lamp-cord example for 1 metre of 0.5 mm^2 wire (a typical USB cable wire). How many grams of copper? How many free electrons? (Hint: everything scales with the area.)
3. **Silver.** Silver has density 10,490 kg/m^3 and molar mass 107.87 g/mol, with one free electron per atom. Compute its free electrons per m^3 and compare with copper's 8.5 x 10^28.
4. **Ions.** A copper atom loses 2 electrons. What is its net charge in units of e, and in coulombs?
5. **Thomson's challenge (harder).** A mystery particle has a charge-to-mass ratio of 4.8 x 10^7 C/kg and a charge of +2e. What is its mass in kg, and roughly how many proton masses is that? (It is a famous particle: what might it be?)

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Atom | "The smallest thing there is" | The smallest unit of an element, itself made of a nucleus and electrons |
| Electron | "The thing that is electricity" | A light particle with charge -e; electricity involves its motion, but also fields and energy (Lessons 03, 04) |
| Elementary charge e | "The charge of an electron" | 1.602176634 x 10^-19 C, the size of the charge on one proton or electron; an electron has -e |
| Neutral | "Has no charge" | Has equal amounts of positive and negative charge, so the net is zero |
| Valence electron | "The outer electron" | An electron in the outermost shell, the most weakly held and the one that takes part in bonding and conduction |
| Free electron | "Loose electron" | A valence electron in a metal that belongs to the whole crystal rather than one atom |
| Mole | "Some chemistry unit" | 6.022 x 10^23 of anything, used to go from grams to number of atoms |

## Further Reading

- [OpenStax University Physics Volume 2, Chapter 5 (Electric Charges and Fields)](https://openstax.org/books/university-physics-volume-2/pages/5-introduction) — free textbook, a clear section on charge, atoms and conductors
- [HyperPhysics: Bohr model and electron shells](http://hyperphysics.phy-astr.gsu.edu/hbase/Bohr.html) — short linked pages with the numbers
- [The Feynman Lectures on Physics, Volume II, Chapter 1](https://www.feynmanlectures.caltech.edu/II_01.html) — Feynman on why electrical forces dominate everyday matter
- J.J. Thomson, "Cathode Rays", *Philosophical Magazine* 44 (1897) — the original paper; the American Institute of Physics history pages at aip.org tell the story for non-specialists
