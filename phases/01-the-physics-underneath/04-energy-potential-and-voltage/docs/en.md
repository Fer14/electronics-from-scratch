# Energy, Potential and Voltage

> Voltage is energy per coulomb. A 9 V battery promises 9 joules to every coulomb of charge it pushes around the loop, and that is all the label on the battery means.

**Type:** Learn
**Prerequisites:** Phase 01 (The Physics Underneath), Lesson 02 (Electric Charge and Coulomb's Law) and Lesson 03 (The Electric Field)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Energy | The ability to make something happen: move, heat up, light up | Money in the bank: you can spend it in many ways, but the total is tracked |
| Joule (J) | The SI unit of energy | Lifting a 100 g apple by 1 metre takes about 1 J |
| Work | Energy transferred by a force pushing something along a distance | Pushing a shopping trolley across a car park |
| Potential energy | Energy stored because of where something is | A book on a high shelf: it can fall and do something |
| Electric potential (V) | Potential energy per coulomb at a point, in J/C | The "height" of a spot on an electrical hill |
| Voltage | The difference in potential between two points: energy per coulomb gained or lost going from one to the other | The height difference between two floors of a building |
| Potential difference | Another name for voltage | Same as above |
| Volt (V) | The unit of voltage: one joule per coulomb | 1 V gives each coulomb 1 J |
| Electron-volt (eV) | The energy one electron gains crossing 1 V: 1.602 x 10^-19 J | A tiny "coin" of energy sized for single particles |
| Equipotential | A line or surface where the potential is the same everywhere | A contour line on a hiking map |
| Ground | The point we choose to call 0 V | Sea level: heights are measured from it, but it is a choice |
| Reference point | Whatever point you measure potentials from | The "zero" mark on a ruler |
| Conservative force | A force where the work between two points does not depend on the route | Gravity: climbing to the top floor costs the same energy by stairs or by ramp |

## Learning Objectives

- Define work and potential energy, and compute them for gravity (m g h) and for a charge in a uniform field (q E d)
- Define electric potential as potential energy per coulomb and voltage as a difference in potential, with the unit volt = joule per coulomb
- Compute the energy a charge gains or loses crossing a voltage (energy = q x V), in joules and in electron-volts
- Use V = E x d for parallel plates and recognise that V/m and N/C are the same unit
- Compute the potential of a point charge (V = kQ / r) and show with code that the work between two points does not depend on the path
- Explain ground as a chosen zero and why only voltage differences have physical meaning

## The Problem

Every battery, charger and power supply has a voltage printed on it: 1.5 V, 3.7 V, 5 V, 12 V, 230 V. Every part's datasheet lists voltages it can handle. In Phase 00 we called voltage "the electrical push". That was a useful placeholder, but it leaves too many questions open. Push *what*, measured *how*? Why is a 9 V battery "stronger" than a 1.5 V one, yet a tiny 9 V battery can run out faster than a large 1.5 V cell? Why do we always talk about voltage *between* two points, or "with respect to ground"? What exactly does a multimeter show when you touch two probes to a circuit?

The answer is energy. Voltage tells you how much energy each unit of charge gains or gives up when it moves from one point to another. Once you see voltage as "energy per coulomb", the rest of electronics clicks into place: a lamp lights because charge loses energy crossing it; a battery runs out because its supply of energy, not its voltage, is limited; a component burns because too much energy per second is dumped into it (Lesson 07).

We will get there by the easiest route: start with gravity, which you already have a feel for, and then swap mass for charge and height for potential.

## The Physics

### Work: energy moved by a force

When a force pushes something along a distance in the direction of the force, it transfers energy. Physicists call that transfer **work**:

```
W = F x d
```

Read it: "work equals force times the distance moved along the force". W is in **joules (J)**, F in newtons, d in metres. One joule is one newton pushing over one metre.

If the force and the motion point in different directions, only the part of the force along the motion counts. Pushing sideways on a trolley that rolls forward does no work in the forward direction. (In code we will use the "dot product" `np.dot(force, step)`, which does exactly this: it keeps only the matching part of two arrows.)

### Gravity as a warm-up

Lift a 1 kg book from the floor onto a shelf 2 m high. Gravity pulls down with F = m x g = 1 x 9.81 = 9.81 N. You must push up with at least that force over 2 m:

```
W = m x g x h = 1 kg x 9.81 m/s^2 x 2 m = 19.62 J
```

That energy is not lost. It is stored as **gravitational potential energy**: if the book falls, gravity gives the 19.62 J back as motion (and then as a thump and a little heat).

Two observations will carry straight over to electricity:

1. **Energy per kilogram depends only on height.** A 1 kg book at 2 m stores 19.62 J; a 3 kg book stores 58.86 J. But per kilogram, both store 19.62 J/kg. So we can label each height with "joules per kilogram" without saying anything about the book. That label is a property of the *place*, not of the object.
2. **Only height differences matter.** Is the shelf at 2 m, or 102 m above sea level, or 6,371 km above the centre of the Earth? It depends where you measure from. But the energy released by the fall is set by the *difference* in height, 2 m, no matter which zero you chose.

### From gravity to electricity

Replace the pieces:

| Gravity | Electricity |
|---------|-------------|
| mass m (kg) | charge q (C) |
| gravitational field g (N/kg, points down) | electric field E (N/C, points from + to -) |
| force m g | force q E |
| height h | position along the field |
| potential energy m g h | electric potential energy |
| energy per kg (J/kg) | **electric potential**, energy per coulomb (J/C = V) |
| height difference | **voltage** (potential difference) |

The only real differences: charge comes in two signs, so a negative charge "falls up" (toward higher potential); and the electric field can point in any direction and change from place to place, while gravity near the ground is the same everywhere.

### Electric potential and the volt

The **electric potential** at a point, written V, is the potential energy a charge would have there divided by its charge:

```
V = U / q
```

Read it: "potential equals potential energy U, divided by charge q". Its unit is joules per coulomb, which has its own name, the **volt**, after Alessandro Volta, who built the first battery (the "voltaic pile" of zinc and copper discs separated by brine-soaked cloth) in **1800**:

```
1 V = 1 J / C
```

Like height, potential is only defined relative to some chosen zero. What matters physically is the **difference** between two points, called the **potential difference** or, most often, the **voltage**:

```
V_AB = V_A - V_B
```

Read it: "the voltage from A to B is the potential at A minus the potential at B". And from the definition, the energy a charge q releases moving from A to B is

```
energy = q x (V_A - V_B)
```

or simply **energy = charge x voltage**. A positive charge moving from high potential to low potential gives up energy (like a book falling). A negative charge, like an electron, gives up energy moving from *low* to *high* potential, which is why electrons in a wire drift toward the + terminal (Lesson 02).

### What a battery's label means

A 9 V battery keeps its + terminal 9 volts higher in potential than its - terminal. Every coulomb that leaves the + terminal, travels through the circuit and returns to the - terminal gives up 9 J along the way (in a lamp, a motor, a resistor). Inside the battery, chemistry lifts each coulomb back up by 9 J, like a pump lifting water to the top of a fountain. We look at that chemistry in Phase 06.

What the voltage label does **not** tell you: how many coulombs the battery can push before its chemicals are used up. That is its capacity (mAh, Phase 00 Lesson 03), and total energy = voltage x total charge. A big 1.5 V D-cell holds far more charge than a small 9 V block and can store more total energy despite the lower voltage.

What the "pump and fountain" picture gets wrong: it suggests charge is used up or piles up somewhere. It is not. Every coulomb that leaves the + terminal returns to the - terminal. What gets "used" is energy, never charge.

### The electron-volt

For single particles, joules are uncomfortably large. An electron crossing 1 V gains

```
energy = e x 1 V = 1.602 x 10^-19 C x 1 J/C = 1.602 x 10^-19 J
```

That amount is called **one electron-volt (1 eV)**. It is the natural energy unit in atoms and semiconductors: the energy to free silicon's valence electrons is about 1.1 eV (Phase 11), the light from a red LED carries about 1.9 eV per photon, the energy an electron gets crossing a 9 V battery is 9 eV. Note: the eV is a unit of **energy**, not of voltage.

### Voltage and field in a uniform field: V = E x d

Between two parallel plates the field E is uniform (Lesson 03). Move a charge q from the + plate to the - plate, a distance d, along the field. The force is q x E, constant, so the work done by the field is

```
W = F x d = q x E x d
```

Divide by q to get energy per coulomb, which is the voltage between the plates:

```
V = E x d
```

Read it: "the voltage across the gap equals the field times the width of the gap". Turned around, E = V / d. This shows that **N/C and V/m are the same unit**: both mean "the field that gives one joule per coulomb per metre". Engineers almost always use V/m, and from here on so will we.

This little formula explains a lot:

- 12 V across a 1 mm gap gives E = 12 / 0.001 = 12,000 V/m.
- 1 V across the 10 nm insulating layer of a transistor gate gives E = 1 / 1e-8 = 100,000,000 V/m (10^8 V/m), more than thirty times the field that makes air spark. Only very good insulators survive that.
- Air sparks at 3 x 10^6 V/m, so a 1 cm air gap holds off about 3 x 10^6 x 0.01 = 30,000 V. A static zap that jumps 5 mm from your finger to a door handle is roughly 15,000 V.

### Potential of a point charge: V = kQ / r

Around a single point charge Q, the potential (taking zero very far away) is

```
         k x Q
V   =   -------
           r
```

Read it: "potential equals the Coulomb constant times the charge, divided by the distance". Notice it is 1 / r, not 1 / r^2 like the field: potential fades more slowly than force. Also, potential is a plain number, not a vector, so adding up potentials from several charges is just adding numbers (no arrows), a big convenience.

Points at the same distance from Q have the same potential: the **equipotentials** of a point charge are spheres around it, like contour lines around a hilltop on a map. A positive charge is a hill; a negative charge is a pit. Field lines always run downhill, crossing equipotentials at right angles.

```
           equipotentials (circles) and field lines (arrows)

                 ^
           .  -  |  -  .
         /   .-  |  -.   \
       |   /     |     \   |
   <-- |--|---- (+) ----|--| -->      V high near +Q,
       |   \     |     /   |          lower farther out
         \   '-  |  -'   /
           '  -  |  -  '
                 v
```

### Path independence

Here is a deep fact. Take a charge from point A to point B by any route: straight, around the houses, a zig-zag. The total work the electric field does on it is the same every time, and equals q x (V_A - V_B). Forces with this property are called **conservative**; gravity is one too (a staircase or a ramp to the top floor costs the same energy).

This is what makes voltage meaningful at all. If the work depended on the route, "the potential at a point" would not be a single number. Because it does not, every point in a circuit has one potential, and every pair of points has one voltage. Our code checks this numerically below.

(When magnetic fields change in time, path independence fails, and that loophole is how generators and transformers work, Phase 08. For everything until then, it holds.)

### Ground: the zero we choose

Since only differences matter, we are free to pick any one point in a circuit and call it 0 V. That point is called **ground** (or "common", or "reference"). In most circuits it is the - terminal of the battery or power supply. Every other potential is then quoted "with respect to ground": "the output is at 3.3 V" means "3.3 V higher than ground".

Sometimes ground really is connected to the earth (the round pin of a mains plug, the metal case of an appliance), for safety. In battery circuits it is just a label. The symbol in schematics (Phase 00, Lesson 05) is

```
        |
      -----
       ---
        -
```

Changing which point you call ground shifts every potential by the same amount and changes no voltage. Look at a 9 V battery with two identical lamps in series (one after the other):

```
   + 9 V o------[ lamp 1 ]------o------[ lamp 2 ]------o 0 V
   (battery +)              midpoint               (battery -)
```

| Point | Ground at battery - | Ground at midpoint |
|-------|--------------------|--------------------|
| battery + | +9.0 V | +4.5 V |
| midpoint | +4.5 V | 0.0 V |
| battery - | 0.0 V | -4.5 V |
| voltage across the battery | 9.0 V | 9.0 V |

The numbers in each column differ, the differences do not. (The midpoint sits halfway because the lamps are identical; Phase 04 explains why with the voltage divider.) Negative potentials are perfectly normal: they just mean "below the point we called zero". Many audio and op-amp circuits (Phase 13) use supplies of +12 V and -12 V around a ground in the middle.

### The voltmeter measures differences

A voltmeter has two probes because it measures the difference in potential between two points. Touch both probes to the same wire and it reads 0 V, even if that wire is at 230 V relative to the earth (that is how birds sit safely on a single power line). Phase 02, Lesson 07 (Measuring with a Multimeter) shows how to use one in practice.

## The Concept

### Worked example 1: energy from a battery

A 9 V battery pushes 0.5 C of charge around a circuit. Energy delivered:

```
energy = q x V = 0.5 C x 9 J/C = 4.5 J
```

One electron crossing the same battery:

```
energy = 1.602e-19 C x 9 V = 1.442 x 10^-18 J = 9 eV
```

A 230 V mains supply gives 230 J to each coulomb, about 25 times what a 9 V battery gives.

### Worked example 2: q E d in a uniform field

A field of 2,000 V/m fills a 6 mm gap. Move a 1 uC charge across it, along the field.

```
force = q x E = 1e-6 x 2000      = 2 x 10^-3 N
work  = F x d = 2e-3 x 0.006     = 1.2 x 10^-5 J
work per coulomb = 1.2e-5 / 1e-6 = 12 J/C = 12 V
check: E x d = 2000 x 0.006      = 12 V
```

### Worked example 3: around a point charge

Q = 1 nC. Potentials at various distances:

```
r = 1 cm:  V = 8.988e9 x 1e-9 / 0.01 = 8.988 / 0.01 = 898.8 V
r = 2 cm:  V = 8.988 / 0.02                          = 449.4 V
r = 3 cm:  V = 8.988 / 0.03                          = 299.6 V
r = 10 cm: V = 8.988 / 0.10                          =  89.9 V
```

Doubling the distance halves the potential (1 / r), while in Lesson 03 it divided the field by 4 (1 / r^2).

The voltage from A (1 cm) to B (3 cm) is

```
V_AB = 898.8 - 299.6 = 599.2 V
```

So a +1 C charge moving from A to B would release 599.2 J; a +1 nC charge would release 599.2 x 10^-9 J.

### Worked example 4: how fast does an electron go?

An electron starts at rest and crosses a potential difference V. It gains kinetic energy (energy of motion) e x V, and kinetic energy is (1/2) m v^2. Setting them equal and solving for the speed v:

```
(1/2) m v^2 = e V      =>      v = sqrt(2 e V / m)
```

For 100 V:

```
v = sqrt(2 x 1.602e-19 x 100 / 9.109e-31)
  = sqrt(3.204e-17 / 9.109e-31)
  = sqrt(3.517e13)
  = 5.93 x 10^6 m/s
```

About 2% of the speed of light, after crossing just 100 V. The old TV tube used about 25,000 V, giving roughly 9.4 x 10^7 m/s, 31% of light speed (at such speeds Einstein's relativity trims the true value slightly, to about 30%). Only differences of potential matter here too: the electron does not care what "ground" is, only how many volts it fell through.

## Build It

The program `code/main.py` computes each example and checks path independence numerically. Run it from the repo root:

```
uv run python phases/01-the-physics-underneath/04-energy-potential-and-voltage/code/main.py
```

### Step 1: Gravity first

```python
GRAVITY = 9.81
mass = 1.0
for height in [1.0, 2.0]:
    energy = mass * GRAVITY * height
    print(f"  lift {mass:.0f} kg by {height:.0f} m: work = {energy:.2f} J, energy per kg = {energy / mass:.2f} J/kg")
```

Output: 9.81 J and 19.62 J.

### Step 2: Voltage = energy per charge

```python
for volts in [1.5, 9.0, 230.0]:
    print(f"  {volts:6.1f} V source: 1 C gains {volts:6.1f} J, 0.5 C gains {0.5 * volts:6.2f} J, one electron gains {volts * ELEMENTARY_CHARGE:.3e} J = {volts:.1f} eV")
```

Output: for 9 V, 0.5 C gains 4.50 J and one electron gains 1.442e-18 J = 9.0 eV.

### Step 3: Uniform field and V = E x d

```python
def work_by_constant_force(force, distance):
    return force * distance


field = 2000.0
gap = 0.006
charge = 1e-6
force = charge * field
work = work_by_constant_force(force, gap)
for volts, distance in [(12.0, 0.001), (5.0, 0.0001), (1.0, 1e-8)]:
    print(f"  {volts:5.1f} V across {distance * 1e6:7g} um -> E = {volts / distance:12,.0f} V/m")
```

Output: work 1.20e-05 J, 12.0 J/C = 12.0 V; fields of 12,000, 50,000 and 100,000,000 V/m.

### Step 4: Potential of a point charge

```python
def potential_of_point_charge(charge, distance):
    return COULOMB_CONSTANT * charge / distance


v_a = potential_of_point_charge(1e-9, 0.01)
v_b = potential_of_point_charge(1e-9, 0.03)
```

Output: 898.8, 449.4, 179.8, 89.9 V at 1, 2, 5, 10 cm, and V_AB = 599.2 V.

### Step 5: Path independence, checked numerically

We chop a path into thousands of tiny straight steps. For each step we evaluate the field at its middle, compute the force on a 1 C test charge, and keep only the part along the step with `np.dot`. Summing gives the total work per coulomb.

```python
def field_of_point_charge(charge, source, point):
    separation = point - source
    distance = np.linalg.norm(separation)
    return COULOMB_CONSTANT * charge * separation / distance**3


def work_along_path(charge, source, path, test_charge=1.0):
    total = 0.0
    for start, end in zip(path[:-1], path[1:]):
        middle = (start + end) / 2
        step = end - start
        force = test_charge * field_of_point_charge(charge, source, middle)
        total += float(np.dot(force, step))
    return total


def straight_path(start, end, steps):
    fractions = np.linspace(0.0, 1.0, steps + 1)[:, None]
    return start + fractions * (end - start)


def detour_path(start, corner, end, steps):
    return np.vstack([straight_path(start, corner, steps), straight_path(corner, end, steps)[1:]])
```

We go from A = (1 cm, 0) to B = (0, 3 cm) around a 1 nC charge at the origin, three different ways: straight, via the corner (3 cm, 3 cm), and via (-2 cm, 4 cm) which swings around the far side.

```
  work per coulomb, straight A -> B           = 599.200 J/C
  work per coulomb, detour via (3 cm, 3 cm)   = 599.200 J/C
  work per coulomb, detour via (-2 cm, 4 cm)  = 599.200 J/C
  potential difference V_A - V_B              = 599.200 V
```

Three routes, one answer, and it equals V_A - V_B from the formula. Path independence, verified by brute force. Note B is 3 cm from the charge, A only 1 cm: the routes have different lengths and pass through different field strengths, yet the totals agree.

### Step 6: Electron-volts and electron speeds

```python
def speed_from_volts(volts, mass=ELECTRON_MASS, charge=ELEMENTARY_CHARGE):
    return np.sqrt(2 * charge * volts / mass)
```

Output: 5.931e+05 m/s for 1 V, 5.931e+06 m/s for 100 V, 1.876e+07 m/s for 1 kV and 9.378e+07 m/s (31.3% of light, before relativity's correction) for 25 kV.

### Step 7: Ground is a choice

```python
potentials_battery_minus = {"battery -": 0.0, "battery +": 9.0, "between lamps": 4.5}
shift = -4.5
potentials_midpoint = {node: value + shift for node, value in potentials_battery_minus.items()}
```

Every potential shifts by -4.5 V; the voltage across the battery is 9.0 V both ways.

## Use It

- **Battery and supply labels.** 1.5 V (alkaline AA), 3.7 V (lithium-ion cell), 5 V (USB), 12 V (car), 230 V or 120 V (mains RMS, Phase 09). Each is a promise of joules per coulomb between two terminals.
- **Logic levels.** Digital chips represent 1 and 0 as potentials relative to ground: on a 3.3 V microcontroller, roughly "above 2 V" is a 1 and "below 0.8 V" is a 0 (Phase 14, Phase 17).
- **Voltage ratings.** Capacitors, transistors and insulation are rated for a maximum voltage because, for a fixed thickness d, voltage sets the field V / d, and too much field causes breakdown (Lesson 03).
- **Solar cells and LEDs.** A silicon solar cell gives about 0.6 V because each absorbed photon can lift an electron by roughly that many eV of usable energy. A red LED needs about 1.9 V because each photon it emits carries about 1.9 eV (Phase 11).
- **Oscilloscopes and multimeters.** Every reading is a difference between the probe and the reference (usually ground). Clipping a scope's ground lead to the wrong point is a classic way to short a circuit (Phase 06).

## Common Mistakes

- **"Voltage flows through a wire."** Current flows; voltage is a difference between two points. Say "the voltage across the lamp" and "the current through the lamp".
- **Quoting a voltage at a single point without a reference.** "This wire is at 5 V" only means something once you know where 0 V is. In a circuit it is ground unless someone says otherwise.
- **Thinking ground is "where electricity goes to disappear".** Ground is just the reference node. Current returns to the source through it like through any other wire.
- **Confusing V = E x d with V = kQ / r.** E x d is for a uniform field (parallel plates). kQ / r is the potential of a point charge relative to infinity. Different situations, different formulas.
- **Treating the eV as a voltage.** The electron-volt is an energy (1.602 x 10^-19 J). "A 9 eV electron" means its energy; "a 9 V battery" means its potential difference.
- **Forgetting the sign for electrons.** A positive charge releases energy going from high to low potential. An electron does so going from low to high. Energy = q x (V_A - V_B) handles it automatically if you keep q's sign.

## Exercises

1. **Energy from voltage.** A 3.7 V phone battery moves 2 C of charge through the phone. How much energy is delivered? How many eV does each electron deliver?
2. **Field from voltage.** A 5 V supply is connected across two plates 0.2 mm apart. What is the field between them in V/m? Is it safely below air's breakdown of 3 x 10^6 V/m?
3. **Ground shift.** In a circuit with ground at the battery's - terminal, three points are at +12 V, +7 V and +2 V. Re-express them with ground moved to the +7 V point. What is the voltage between the first and last points in both cases?
4. **Point charge.** A +2 nC charge sits at the origin. What is the potential at 4 cm and at 8 cm? How much energy does a +3 nC charge release moving from 4 cm to 8 cm? Extend `main.py` with another detour path and confirm the work does not change.
5. **Electron gun (harder).** What voltage must an electron cross, from rest, to reach 1% of the speed of light (3 x 10^6 m/s)? Use v = sqrt(2 e V / m) and solve for V.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Voltage | "The electrical pressure" | The difference in electric potential between two points: energy per coulomb, in volts |
| Potential | "Voltage at a point" | Potential energy per coulomb at a point, measured from a chosen zero |
| Volt | "A unit of electricity" | 1 V = 1 J/C |
| Electron-volt | "A voltage for electrons" | An energy: 1 eV = 1.602 x 10^-19 J, what one electron gains crossing 1 V |
| Ground | "Earth" or "where current dies" | The node we choose as 0 V; sometimes physically tied to the earth for safety |
| V = E x d | "Voltage equals field times distance" | Voltage across a gap of width d in a uniform field E; also why V/m = N/C |
| Conservative force | "Energy is conserved" | A force for which work from A to B depends only on A and B, not the path; this is what makes potential well defined |

## Further Reading

- [OpenStax University Physics Volume 2, Chapter 7 (Electric Potential)](https://openstax.org/books/university-physics-volume-2/pages/7-introduction) — the full development of potential and potential difference, with many worked examples
- [The Feynman Lectures on Physics, Volume II, Chapter 4 (Electrostatics), section 4-5 onward](https://www.feynmanlectures.caltech.edu/II_04.html) — why the electric field can be written as the slope of a potential
- [All About Circuits, Volume I (DC), Chapter 1: Voltage and Current](https://www.allaboutcircuits.com/textbook/direct-current/chpt-1/voltage-current/) — a practical, circuit-oriented introduction to voltage
- [Khan Academy: Electric potential energy, electric potential and voltage](https://www.khanacademy.org/science/physics/electric-charge-electric-force-and-voltage) — short videos with the gravity analogy
