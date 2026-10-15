# Electric Charge and Coulomb's Law

> Like charges push apart, unlike charges pull together, and the push fades with the square of the distance. Almost everything in electronics grows out of that one sentence.

**Type:** Learn
**Prerequisites:** Phase 01 (The Physics Underneath), Lesson 01 (Atoms and Electrons); Phase 00 (Words and Units), Lessons 03 and 04 (units, prefixes and scientific notation)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Electric charge | A property of particles that makes them push or pull on each other electrically | A label, "+" or "-", that decides who is attracted to whom |
| Positive / negative | The two kinds of charge; protons are +, electrons are - | Two teams: same team players shove each other away, opposite teams cling |
| Net charge | Total positive minus total negative on an object | A bank balance: deposits minus withdrawals |
| Charging (by rubbing) | Moving electrons from one object to another by contact and friction | Rubbing a balloon on your hair so it sticks to the wall |
| Conservation of charge | Charge is never created or destroyed, only moved | Money moved between two pockets: the total in your trousers stays the same |
| Quantization of charge | Every charge is a whole number of elementary charges e | You can only pay in whole cents, never half a cent |
| Coulomb (C) | The SI unit of charge, about 6.24 x 10^18 elementary charges | A dozen eggs is a unit of eggs; a coulomb is a unit of charge |
| Force | A push or a pull, measured in newtons (N) | 1 N is roughly the weight of a small apple in your hand |
| Newton (N) | The SI unit of force | See above |
| Coulomb's law | The rule giving the force between two charges | A recipe: multiply the charges, divide by distance squared, multiply by a constant |
| Inverse-square law | A force that drops by 4 when distance doubles, by 9 when it triples | Light from a lamp spread over a bigger and bigger sphere |
| Coulomb constant (k) | The number 8.988 x 10^9 N m^2/C^2 in Coulomb's law | The conversion factor that turns "charges and distances" into newtons |
| Vector | A quantity with both a size and a direction | "5 km north-east", not just "5 km" |
| Superposition | The total force is the sum of the forces from each charge separately | Several people pushing a car: add up all their pushes, with directions |
| Conventional current | The agreed direction of current, from + to -, opposite to how electrons move in wires | Driving on the left or right: an arbitrary rule everyone follows |

## Learning Objectives

- Explain that charge comes in two kinds, that like charges repel and unlike charges attract, and where the names "positive" and "negative" came from
- State conservation and quantization of charge and use them to count electrons moved in everyday charging
- Use Coulomb's law to compute the force between two point charges, with the arithmetic shown
- Explain the inverse-square law and predict how the force changes when distance changes
- Add forces from several charges as vectors (superposition), by hand and with numpy
- Compare the electric force with gravity and explain why electric forces dominate electronics
- Explain why "conventional current" flows from + to - while electrons in a wire move the other way

## The Problem

Rub a balloon on a wool jumper and it sticks to the wall. Pull off a fleece in winter and you hear crackles and see tiny sparks. Touch a door handle after walking across a carpet and you get a small zap. These are the oldest electrical experiences humanity has: the Greek philosopher Thales noticed around 600 BC that rubbed amber attracts bits of straw, and the word "electric" comes from *elektron*, Greek for amber.

These tricks look like party games, but the force behind them is the same force that holds every atom together, that makes a current flow in a wire, that stores energy in a capacitor (Phase 07) and that switches the transistors in your phone (Phase 12). If you understand how two charges push on each other, you understand the engine underneath all of electronics.

There is also a practical problem hiding here. The static zap from a door handle is a few thousand volts (we define volts in Lesson 04). It does not hurt you much, but it can destroy a chip whose insulating layers are a few nanometres thick. Engineers wear grounded wrist straps when handling boards for exactly this reason. To understand why a tiny amount of charge can do so much, we need numbers, and Coulomb's law gives them.

## The Physics

### Two kinds of charge

By the 1730s, the French chemist Charles du Fay had noticed that there are exactly two kinds of "electricity". Rubbed glass repelled other rubbed glass, rubbed amber (or resin) repelled other rubbed amber, but glass and amber attracted each other. Every charged object ever tested behaves like one or the other.

The rules:

```
   same kind:       (+)  <-- push -->  (+)        (-)  <-- push -->  (-)

   opposite kind:   (+)  --> pull <--  (-)
```

- Like charges **repel** (push apart).
- Unlike charges **attract** (pull together).

### Franklin's names, and the sign that confuses everyone

Around **1747**, Benjamin Franklin in Philadelphia proposed that there is really only one "electric fluid". An object with too much of it was "plus" (positive), one with too little was "minus" (negative). He had to pick which was which, and he guessed: rubbed glass has *extra* fluid, so it is positive.

Franklin's picture was half right: charge does move from one object to another, and the total is conserved. But he had no way of knowing what the "fluid" was made of. When Thomson found the electron in 1897 (Lesson 01), it turned out that the thing that actually moves in most cases is the electron, and by Franklin's labelling, the electron is **negative**. Rubbed glass is positive because it has *lost* electrons, not gained fluid.

By then, more than a century of books, instruments and formulas used Franklin's labels and said that current flows from + to -. Nobody changed them. So today:

- **Conventional current** is defined as flowing out of the **+** terminal of a source, through the circuit, and back into the **-** terminal. Every schematic, every textbook formula and every part datasheet in this course uses conventional current.
- **Electrons in a wire move the opposite way**, from - to + through the outside circuit.

```
          conventional current I  ---->
      +----------------------------------+
      |                                  |
    [+]  battery                     [ lamp ]
    [-]                                  |
      |                                  |
      +----------------------------------+
          <----  electrons drift

```

Is this a problem? Almost never. A negative charge moving left has exactly the same electrical effect as a positive charge moving right: both make the right side more positive and the left side more negative. Every calculation comes out identical. You just need to remember that "current direction" is a bookkeeping convention, not a claim about which particles are moving. Lesson 06 returns to this when we define current properly.

### Charging by rubbing: moving electrons around

When you rub two different materials together, electrons from the surface of one jump to the other. Which way they go depends on how tightly each material holds its outer electrons. Hair and wool give electrons up easily; rubber and many plastics grab them. So after rubbing:

```
 before:    hair: neutral          balloon: neutral
 rubbing:   electrons hop from hair to balloon
 after:     hair: positive (lost electrons)
            balloon: negative (gained electrons)
```

Nothing new was created. Electrons were moved from one place to another. This is a law of nature called **conservation of charge**: in any process, the total charge before equals the total charge after. It has never been seen to fail, from rubbing balloons to particle colliders.

### Quantization: charge comes in lumps

In **1909**, Robert Millikan and his student Harvey Fletcher sprayed tiny oil droplets between two horizontal metal plates. The droplets picked up a few stray electrons. By adjusting the electrical push between the plates until a droplet hovered (electric force up balancing gravity down), they could compute each droplet's charge.

Every droplet's charge came out as a **whole-number multiple** of one smallest amount, about 1.6 x 10^-19 C. Never 1.5 times it, never 2.7 times it. That smallest amount is the elementary charge e from Lesson 01. This is **quantization of charge**:

```
Q = n x e        with n = ..., -2, -1, 0, 1, 2, ...
```

Read it as: "any charge Q is a whole number n of elementary charges". For electronics this mostly matters in one way: since e is so tiny, everyday charges involve billions of electrons, and we can treat charge as a smooth quantity, just as you treat water as smooth even though it is made of molecules.

### Coulomb's torsion balance (1785)

How strong is the force between two charges? In **1785**, the French engineer Charles-Augustin de Coulomb measured it with a **torsion balance**: a light horizontal rod hanging from a thin silver wire, with a small charged ball on one end. When he brought another charged ball near, the rod turned and twisted the wire. The angle of twist told him the force, because he had first measured how much force it takes to twist that wire by a given angle.

```
              thin wire (twists)
                   |
                   |
     o=============+               o = charged ball on the rod
                                   * = fixed charged ball brought nearby
    *
```

By changing the distance between the balls he found that the force is proportional to 1 / (distance)^2. Halve the distance, and the force becomes 4 times bigger. Contemporary measurements (and his own estimates of charge, made by sharing charge between identical balls) showed the force is also proportional to each charge.

## The Concept

### Coulomb's law in words

"The force between two small charged objects equals a constant k, times the first charge, times the second charge, divided by the square of the distance between them."

```
        k x q1 x q2
F  =  -------------
           r^2
```

Symbol by symbol:

- **F** is the force in newtons (N).
- **q1** and **q2** are the two charges in coulombs (C), each with its sign.
- **r** is the distance between their centres in metres (m).
- **k** is the **Coulomb constant**, 8.988 x 10^9 N m^2/C^2. Its strange unit is exactly what is needed so that C x C / m^2 times the unit of k comes out in N. You will also see k written as 1 / (4 pi eps0), where eps0 = 8.854 x 10^-12 F/m is the "permittivity of free space"; we meet eps0 again in Lesson 03 and in Phase 07 (capacitors).

The sign tells you the direction:

- **F positive**: q1 and q2 have the same sign, the force **repels**.
- **F negative**: opposite signs, the force **attracts**.

The force acts along the line joining the two charges, equally on both: charge 1 pushes charge 2 exactly as hard as charge 2 pushes charge 1, in opposite directions.

What the formula assumes: the charges are **point charges** (tiny compared with the distance between them) and sitting still. For big spread-out objects you would add up many tiny pieces, which is what superposition, below, lets you do.

### Worked example 1: two microcoulomb charges

Two small metal balls each carry +1 uC (one microcoulomb, 1 x 10^-6 C), 10 cm apart (0.10 m).

```
F = 8.988e9 x (1e-6) x (1e-6) / (0.10)^2
  = 8.988e9 x 1e-12 / 0.01
  = 8.988e-3 / 0.01
  = 0.8988 N
```

Positive, so they repel, with roughly the weight of a 90 gram object. And 1 uC is a modest amount of charge: about 6 x 10^12 electrons.

If one ball is -1 uC instead, the arithmetic is identical, but F = -0.8988 N: same size, now attracting.

### Worked example 2: why a coulomb is a lot

Imagine two objects with **+1 C** each, a full kilometre apart:

```
F = 8.988e9 x 1 x 1 / (1000)^2
  = 8.988e9 / 1e6
  = 8988 N
```

That is the weight of about 916 kg, a small car, pushing between two objects a kilometre apart. In practice you can never pile up a whole coulomb of excess charge on an ordinary object: the charge would tear itself apart (leak into the air as sparks) long before. Yet a coulomb flows through a phone charger cable every second or so. The difference is that in a wire the moving electrons are always balanced by the positive ions they move past (Lesson 01), so the net charge stays near zero. Current is huge amounts of charge *moving*, not huge amounts of charge *piled up*.

### Worked example 3: counting the electrons on a balloon

A balloon rubbed on hair picks up roughly -50 nC (nanocoulombs, 50 x 10^-9 C). How many extra electrons is that?

```
n = Q / e = 50e-9 / 1.602e-19 = 3.12 x 10^11 electrons
```

Three hundred billion extra electrons sounds like a lot. But a 5 gram balloon contains roughly 1.5 x 10^24 electrons in its atoms, so the balloon gained about

```
3.12e11 / 1.5e24 = 2.1 x 10^-13
```

0.2 extra electrons per trillion. The tiniest imbalance is enough to make it stick to a wall. That is how strong the electric force is.

And by conservation, the hair lost exactly as many: it is now about +50 nC.

### The inverse-square law

Keep both charges at +1 uC and change the distance:

| r | r^2 | F |
|---|-----|---|
| 5 cm | 0.0025 m^2 | 3.595 N |
| 10 cm | 0.01 m^2 | 0.8988 N |
| 20 cm | 0.04 m^2 | 0.2247 N |
| 40 cm | 0.16 m^2 | 0.0562 N |

Each time the distance doubles, the force divides by four. Why the square? Picture the influence of a charge spreading out evenly in all directions, like light from a bulb. At distance r it is spread over the surface of a sphere of area 4 pi r^2. Double r and that area is 4 times bigger, so the influence on each little patch is 4 times weaker. (This picture becomes precise in Lesson 03 with field lines.)

### Electric force versus gravity

Gravity also follows an inverse-square law: F = G x m1 x m2 / r^2, with G = 6.674 x 10^-11 N m^2/kg^2. Compare both forces between the electron and the proton in a hydrogen atom, 5.29 x 10^-11 m apart:

```
electric: 8.988e9 x (1.602e-19)^2 / (5.29e-11)^2
        = 8.988e9 x 2.567e-38 / 2.798e-21
        = 8.25 x 10^-8 N

gravity:  6.674e-11 x 9.109e-31 x 1.6726e-27 / (5.29e-11)^2
        = 1.017e-67 / 2.798e-21
        = 3.63 x 10^-47 N

ratio:    8.25e-8 / 3.63e-47 = 2.3 x 10^39
```

The electric force is about **10^39 times** stronger. That number is so large it is hard to feel. Gravity only wins at planet scale, because planets are almost exactly neutral (positive and negative cancel) while mass never cancels. In every circuit, gravity is irrelevant. Charges and their electric forces run the show.

### Superposition: adding forces as arrows

When several charges act on one charge, the total force is the **sum of the individual forces**, each computed with Coulomb's law as if the others were not there. This is the **superposition principle**. The catch: forces have directions, so we add them as **vectors** (arrows), not just as numbers.

A vector in 2-D is a pair of numbers [x, y]: how much it points right (x) and how much up (y). To add two vectors, add the x parts and add the y parts.

To find the force vector from one charge on another:

1. Find the separation vector from the source to the target: target position minus source position.
2. Its length r is sqrt(x^2 + y^2) (Pythagoras).
3. Divide the separation by r to get a **unit vector**: an arrow of length 1 that just says "which way".
4. Multiply that unit vector by the Coulomb force F (with its sign). A positive F points away from the source (repulsion), a negative F points toward it (attraction).

### Worked example 4: three charges pushing on one

A +2 nC charge sits at the origin (0, 0). Around it:

```
                    (-4 nC)  at (0, +4 cm)
                       |
                       |
  (+3 nC) ---------- (+2 nC) ---------- (+1 nC)
  at (-3 cm, 0)      origin             at (+3 cm, 0)
```

Force from the +3 nC at (-3 cm, 0): distance 0.03 m, same signs, repel, so it pushes the target away, toward +x.

```
F = 8.988e9 x 2e-9 x 3e-9 / (0.03)^2 = 8.988e9 x 6e-18 / 9e-4 = 5.992e-5 N = 59.92 uN
vector = [+59.92, 0] uN
```

Force from the -4 nC at (0, +4 cm): distance 0.04 m, opposite signs, attract, so it pulls the target toward the -4 nC, i.e. toward +y.

```
F = 8.988e9 x 2e-9 x 4e-9 / (0.04)^2 = 8.988e9 x 8e-18 / 1.6e-3 = 4.494e-5 N = 44.94 uN
vector = [0, +44.94] uN
```

Force from the +1 nC at (+3 cm, 0): repel, pushes toward -x.

```
F = 8.988e9 x 2e-9 x 1e-9 / (0.03)^2 = 1.997e-5 N = 19.97 uN
vector = [-19.97, 0] uN
```

Add the arrows component by component:

```
x: 59.92 + 0 - 19.97 = 39.95 uN
y: 0 + 44.94 + 0    = 44.94 uN

size  = sqrt(39.95^2 + 44.94^2) = sqrt(1596 + 2020) = 60.13 uN
angle = arctan(44.94 / 39.95) = 48.4 degrees above the +x axis
```

The target is pushed up and to the right. Notice the left and right charges partly cancel: you cannot just add the three sizes (59.92 + 44.94 + 19.97 = 124.8 uN would be wrong).

## Build It

The program `code/main.py` repeats each worked example. Run it from the repo root:

```
uv run python phases/01-the-physics-underneath/02-electric-charge-and-coulombs-law/code/main.py
```

### Step 1: Electrons in a coulomb and on a balloon

```python
ELEMENTARY_CHARGE = 1.602176634e-19


def electrons_for_charge(charge):
    return charge / ELEMENTARY_CHARGE


print(f"  electrons in 1 C            = {electrons_for_charge(1.0):.3e}")
balloon_charge = -50e-9
print(f"  balloon rubbed on hair, -50 nC -> {electrons_for_charge(-balloon_charge):.2e} extra electrons")
```

Output: 6.242e+18 electrons per coulomb, 3.12e+11 extra electrons on the balloon, about 0.2 per trillion.

### Step 2: Conservation

We move 3.1 x 10^11 electrons from the hair to the balloon and check that the total is still zero.

```python
transferred = 3.1e11
hair = +transferred * ELEMENTARY_CHARGE
balloon = -transferred * ELEMENTARY_CHARGE
print(f"  total                 = {(hair + balloon) * 1e9:+.2f} nC")
```

Output: hair +49.67 nC, balloon -49.67 nC, total +0.00 nC.

### Step 3: Quantization, Millikan style

We take six droplet charges (invented, with small measurement errors, in the spirit of Millikan's data) and divide each by e. Each ratio lands next to a whole number.

```python
measured_drops = np.array([3.21e-19, 8.00e-19, 4.82e-19, 1.123e-18, 1.60e-19, 6.39e-19])
multiples = measured_drops / ELEMENTARY_CHARGE
for charge, ratio in zip(measured_drops, multiples):
    print(f"  drop charge {charge:.3e} C  ->  {ratio:5.2f} e  ->  n = {round(ratio)}")
```

Output: 2.00, 4.99, 3.01, 7.01, 1.00 and 3.99, so n = 2, 5, 3, 7, 1, 4.

### Step 4: Coulomb's law

```python
COULOMB_CONSTANT = 8.988e9


def coulomb_force(q1, q2, distance):
    return COULOMB_CONSTANT * q1 * q2 / distance**2


force = coulomb_force(1e-6, 1e-6, 0.10)
```

Output: 0.8988 N for two +1 uC at 10 cm, -0.8988 N for +1 uC and -1 uC, and 8.988e+03 N (about 916 kg of weight) for two 1 C charges a kilometre apart.

### Step 5: The inverse-square law

```python
for distance in [0.05, 0.10, 0.20, 0.40]:
    force = coulomb_force(1e-6, 1e-6, distance)
    print(f"  r = {distance * 100:4.0f} cm   F = {force:7.4f} N")
```

Output: 3.5952, 0.8988, 0.2247, 0.0562 N. Each line is a quarter of the one before.

### Step 6: Electric force versus gravity

```python
GRAVITATIONAL_CONSTANT = 6.674e-11
HYDROGEN_RADIUS = 5.29e-11


def gravity_force(m1, m2, distance):
    return GRAVITATIONAL_CONSTANT * m1 * m2 / distance**2


electric = abs(coulomb_force(ELEMENTARY_CHARGE, -ELEMENTARY_CHARGE, HYDROGEN_RADIUS))
gravity = gravity_force(ELECTRON_MASS, PROTON_MASS, HYDROGEN_RADIUS)
```

Output: 8.245e-08 N versus 3.634e-47 N, a ratio of 2.27e+39.

### Step 7: Superposition with numpy

`force_vector_on` follows the four steps above: separation, length, unit vector, times the Coulomb force. `net_force` adds the vectors.

```python
def force_vector_on(target_charge, target_position, source_charge, source_position):
    separation = target_position - source_position
    distance = np.linalg.norm(separation)
    direction = separation / distance
    return coulomb_force(target_charge, source_charge, distance) * direction


def net_force(target_charge, target_position, sources):
    total = np.zeros(2)
    for source_charge, source_position in sources:
        total += force_vector_on(target_charge, target_position, source_charge, source_position)
    return total


sources = [
    (3e-9, np.array([-0.03, 0.0])),
    (-4e-9, np.array([0.0, 0.04])),
    (1e-9, np.array([0.03, 0.0])),
]
total = net_force(2e-9, np.array([0.0, 0.0]), sources)
angle = np.degrees(np.arctan2(total[1], total[0]))
```

`np.linalg.norm` computes the length sqrt(x^2 + y^2); `np.arctan2(y, x)` gives the angle of an arrow, handling all four quadrants. Output: net force [+39.947, +44.940] uN, size 60.128 uN at 48.4 degrees, matching the hand calculation.

## Use It

- **Electrostatic discharge (ESD).** Walking on carpet can leave you with a few hundred nanocoulombs. When you touch a circuit board, that charge rushes out in a tiny spark. For a person it is a tickle; for a transistor gate insulated by an oxide a few nanometres thick, it can punch a hole. That is why chips ship in anti-static bags and why datasheets list an "ESD rating" (often 2 kV human body model). We follow ESD habits from the first lab.
- **Laser printers and photocopiers.** A drum is charged, light discharges parts of it, and charged toner powder sticks only where Coulomb attraction pulls it. Then the paper is charged to pull the toner off the drum.
- **Electrostatic precipitators.** Factory chimneys charge soot particles and then attract them to plates with opposite charge, cleaning the smoke.
- **Capacitors.** In Phase 07 we will store charge on two metal plates facing each other. Coulomb attraction between the + plate and the - plate is what holds the charge there.
- **Touchscreens.** Your finger changes how charge sits on a grid of transparent electrodes; the phone measures the change. Same physics, different packaging.

## Common Mistakes

- **Forgetting to square the distance.** Doubling r divides F by 4, not 2. Always write r^2 and compute it as its own line.
- **Using centimetres or microcoulombs directly.** Coulomb's law needs metres and coulombs. 10 cm is 0.10 m; 1 uC is 1 x 10^-6 C. Mixing units gives answers off by factors of millions.
- **Adding force sizes instead of vectors.** Forces in different directions can partly cancel. Split each into x and y parts, add the parts, then combine.
- **Thinking current flows the way electrons move.** By convention, current goes from + to - through the outside circuit. Electrons in wires go the other way. Both descriptions predict exactly the same behaviour; only the label differs.
- **Believing rubbing "creates" charge.** It only separates it. If the balloon gained -50 nC, something else gained +50 nC.
- **Using Coulomb's law for big spread-out objects.** It is exact for point charges (or spheres, measured from their centres). For other shapes, split the object into small pieces and use superposition.

## Exercises

1. **Counting.** A static zap transfers 0.3 uC. How many electrons is that?
2. **Plain Coulomb.** A +5 nC charge and a -2 nC charge are 3 cm apart. Compute the force (size and whether it attracts or repels).
3. **Inverse square.** Two charges repel with 0.36 N at a distance of 6 cm. What is the force at 2 cm? At 18 cm? (No need for k: think in ratios.)
4. **Balance against gravity.** A tiny charged plastic bead of mass 2 milligrams (2 x 10^-6 kg) hangs 5 cm directly below a fixed charge of +40 nC and is held up by attraction alone. What charge must the bead carry? (Hint: the electric force must equal the weight m x g, with g = 9.81 m/s^2.)
5. **Superposition (harder).** Put -1 nC at (0, 0), +1 nC at (4 cm, 0) and a test charge of +1 nC at (2 cm, 2 cm). Find the net force vector on the test charge. Then modify the `sources` list in `main.py` and check your answer.

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Charge | "Electricity" | A property of particles, in coulombs, that causes electric forces; it comes in + and - |
| Positive / negative | "Has charge / has no charge" | Two kinds of charge; the signs were picked by Franklin and are a convention |
| Conservation of charge | "You can't make charge" | In any process the total charge (positive minus negative) stays exactly the same |
| Quantization | "Charge comes in packets" | Every observed free charge is a whole number of e = 1.602 x 10^-19 C |
| Coulomb's law | "Opposites attract" | F = k q1 q2 / r^2: the size and sign of the force between two point charges |
| Inverse-square law | "It gets weaker with distance" | Specifically, it falls as 1 / r^2: twice as far, a quarter as strong |
| Superposition | "Add up the forces" | Add the force vectors from each charge, component by component |
| Conventional current | "Current flows + to -" | A bookkeeping direction; in wires the electrons actually drift from - to + |

## Further Reading

- [OpenStax University Physics Volume 2, Chapter 5 (Electric Charges and Fields), sections 5.1 to 5.3](https://openstax.org/books/university-physics-volume-2/pages/5-introduction) — charge, conservation and Coulomb's law with many worked examples
- [The Feynman Lectures on Physics, Volume II, Chapter 1 (Electromagnetism)](https://www.feynmanlectures.caltech.edu/II_01.html) — the famous passage comparing electric and gravitational forces
- [HyperPhysics: Coulomb's law](http://hyperphysics.phy-astr.gsu.edu/hbase/electric/elefor.html) — compact page with an interactive calculator
- [Khan Academy: Electric charge, field and potential](https://www.khanacademy.org/science/physics/electric-charge-electric-force-and-voltage) — short videos on charge and Coulomb's law
