# The Electric Field

> A charge changes the space around it. Any other charge that wanders in feels that change as a push. The field is the map of those pushes.

**Type:** Learn
**Prerequisites:** Phase 01 (The Physics Underneath), Lesson 02 (Electric Charge and Coulomb's Law)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Electric field (E) | The force a charge would feel at a point, divided by the size of that charge | A weather map of wind: at every spot, an arrow saying how hard and which way the wind blows |
| Test charge | A tiny imaginary charge used to probe the field without disturbing it | A feather dropped to see which way the wind blows |
| Source charge | A charge that creates a field | The fan that makes the wind |
| N/C (newtons per coulomb) | The unit of electric field: newtons of force per coulomb of charge | "Kilometres per hour" for wind; here it is "newtons per coulomb" |
| Field line | A curve drawn so that at every point it follows the direction of the field | Streamlines of water flowing in a river |
| Point charge | A charge so small compared with the distances involved that it is effectively a dot | A star seen from Earth: a dot, though really huge |
| Dipole | A + charge and an equal - charge, close together | A tiny bar magnet, but electric |
| Uniform field | A field with the same size and direction everywhere in a region | A steady breeze across a flat field: same everywhere |
| Parallel plates | Two flat metal sheets facing each other, one + and one - | Two slices of bread with the sandwich filling being the field |
| Surface charge density (sigma) | Charge per square metre on a surface, in C/m^2 | How thickly butter is spread on bread |
| Permittivity of free space (eps0) | A constant, 8.854 x 10^-12 F/m, describing how vacuum "lets" fields form | A conversion factor of nature, like the speed of light |
| Dielectric breakdown | When a field is so strong it rips electrons out of an insulator and a spark jumps | A dam that holds until the water is high enough, then bursts |

## Learning Objectives

- Define the electric field as force per unit charge and compute the force on any charge from a known field (F = qE)
- Compute the field of a point charge, E = kQ / r^2, and say which way it points
- Read and draw field lines and know their rules (start on +, end on -, never cross, dense where strong)
- Add fields from several charges as vectors (superposition), by hand and over a whole grid with numpy
- Compute the uniform field between two parallel plates from the charge on them (E = sigma / eps0)
- Estimate when air breaks down (about 3 x 10^6 N/C) and connect that to sparks and static zaps

## The Problem

In Lesson 02 we computed the force between two charges. That works fine with two charges. Now think of a real situation: a battery's terminals, a wire full of electrons, a chip with millions of charged regions. Every charge pushes on every other charge. If you have to compute every pair every time something moves, you drown in arithmetic.

There is also a puzzle. Coulomb's law says two charges a metre apart push on each other right now, with nothing in between. How does charge A "know" where charge B is? Michael Faraday, who never trusted action at a distance, found a better way to think: each charge sets up something in the space around it, and other charges respond to what is *right where they are*. That something is the **electric field**.

Thinking in fields is how engineers reason about almost everything that follows: why current flows the moment a switch closes (the field travels along the wire at near light speed), why a capacitor stores energy (Phase 07, the energy lives in the field), why a transistor's gate can control a channel without touching it (Phase 12), and why sharp points on high-voltage gear spark (fields are strongest there). So we build the idea carefully now.

## The Physics

### Faraday's lines of force

Michael Faraday (1791-1867) was the son of a blacksmith, left school at 14 and taught himself science while working as a bookbinder. He had little mathematics, so he thought in pictures. Sprinkling iron filings around a magnet, he saw them line up in curves, and imagined the space around magnets and charges filled with **lines of force**. Where lines crowd together the force is strong; where they spread out it is weak.

Physicists of his time found the idea charming but unscientific. Then James Clerk Maxwell (1860s) turned Faraday's pictures into exact equations and showed that changing fields travel through space as waves at the speed of light. Light itself is a wave of electric and magnetic fields. Fields went from cartoon to the most real thing in physics.

### The field is "force per charge"

Put a small charge q at some point. It feels a force F (from all the other charges around). Now double q: Coulomb's law says the force doubles. Halve q: the force halves. The ratio F / q is the same no matter which small charge you use. That ratio depends only on the *place* and on the *other charges*, so it is a property of the space itself. We call it the electric field:

```
E = F / q
```

Read it: "the electric field at a point is the force a charge would feel there, divided by that charge". Turn it around and you have the most useful form:

```
F = q x E
```

"The force on a charge equals its charge times the field where it sits."

- E is measured in **newtons per coulomb (N/C)**. In Lesson 04 we will see that this is exactly the same unit as **volts per metre (V/m)**, the form engineers use most.
- E is a **vector**: it has a size and a direction. By definition, it points the way a **positive** charge would be pushed.
- A **negative** charge (such as an electron) at the same spot is pushed in the **opposite** direction to E, because q is negative in F = q x E.

The small charge we imagine is called a **test charge**. "Small" matters: a big test charge would push the source charges around and change the very field we are trying to measure.

What the "wind map" picture gets right: an arrow at every point, telling you what a small object placed there will feel. What it gets wrong: wind is air actually moving. The electric field is not anything flowing; it is a push waiting to happen.

### Field of a single point charge

Combine E = F / q with Coulomb's law for a source charge Q and a test charge q at distance r:

```
F = k x Q x q / r^2
E = F / q = k x Q / r^2
```

The test charge cancels out, as promised. So the field of a point charge is:

```
         k x Q
E   =   -------        pointing straight away from Q if Q is positive,
          r^2          straight toward Q if Q is negative
```

with k = 8.988 x 10^9 N m^2/C^2, Q in coulombs, r in metres.

### Field lines and their rules

We draw fields with **field lines**:

```
   isolated + charge              isolated - charge

        \  |  /                       \  |  /
         \ | /                         v v v
     ---- (+) ---->                --->( - )<---
         / | \                         ^ ^ ^
        /  |  \                       /  |  \
   lines point outward            lines point inward
```

The rules:

1. Lines **start on positive** charges and **end on negative** charges (or go off to infinity).
2. The direction of a line at any point is the direction of E there (the push on a + test charge).
3. Where lines are **close together**, the field is **strong**; where they spread out, it is weak.
4. Lines **never cross**. At a crossing E would point two ways at once, which is impossible.
5. The number of lines leaving a charge is proportional to its charge: a +2 nC charge gets twice as many as a +1 nC charge.

Rule 3 explains the inverse-square law visually. A fixed number of lines leave a point charge. At distance r they pierce a sphere of area 4 pi r^2. Double r and the same lines spread over 4 times the area, so they are 4 times less crowded: the field is 4 times weaker. That is exactly 1 / r^2.

### Dipoles: a + and a - side by side

Put +Q and -Q close together and the lines leave the + charge, curve around and land on the - charge:

```
               . - ~ ~ ~ - .
            .'               '.
          /    . - ~ ~ - .     \
         |   /             \    |
    <--- (+) ---->----->----> (-) <---
         |   \             /    |
          \    ' - ~ ~ - '     /
            '.               .'
               ' - ~ ~ ~ - '
```

This pattern, called a **dipole**, appears everywhere: a water molecule, a radio antenna, the two plates of a charged capacitor seen from a distance, a battery with nothing connected.

### Parallel plates: the uniform field

Take two large flat metal plates, facing each other a small distance apart, one with +Q and the other with -Q. Between them, the field lines run straight across from + to -, evenly spaced:

```
     + + + + + + + + + + + + +     plate with +Q
     |   |   |   |   |   |   |
     v   v   v   v   v   v   v     E: same size, same direction everywhere
     |   |   |   |   |   |   |
     - - - - - - - - - - - - -     plate with -Q
```

Evenly spaced parallel lines mean the field is **uniform**: the same strength and direction at every point between the plates (except near the edges, where lines bulge out; we ignore that "fringing"). Its size depends only on how thickly the charge is spread:

```
         sigma          Q / A
E   =   -------   =   ---------
         eps0            eps0
```

Read it: "the field between the plates equals the surface charge density (charge per square metre) divided by the permittivity of free space". Symbols:

- **sigma** = Q / A is the charge on one plate divided by its area, in C/m^2.
- **eps0** = 8.854 x 10^-12 F/m (the F is the farad, the unit of capacitance from Phase 07; for now just treat eps0 as a number). It is linked to k: k = 1 / (4 pi eps0). Check: 1 / (4 x 3.1416 x 8.854e-12) = 8.988e9.

Surprisingly, the field does not depend on the gap between the plates, as long as the gap is small compared with the plate size. Moving the plates apart spreads the same lines over a longer path, but they are still just as crowded across the area. This parallel-plate arrangement is a **capacitor**, the star of Phase 07, and the place where Lesson 04 defines voltage most cleanly.

### Conductors and fields: a preview

Inside a piece of metal that is sitting still, with no current flowing, the field is zero. Why? Any field would push the free electrons (Lesson 01), and they would keep moving until their new arrangement cancelled the field. So charges on a conductor at rest end up on its **surface**.

When a battery is connected, it keeps a field alive inside the wire. That field is what pushes the electrons along. The field spreads along the wire at close to the speed of light, which is why a lamp lights instantly even though each electron creeps (Lesson 06).

### Breakdown: when the field is too strong

Air is an insulator: its electrons are bound to molecules. But a strong enough field can pull an electron off a molecule and accelerate it so hard that it knocks electrons off other molecules, in an avalanche. Suddenly the air conducts and a spark jumps. For dry air at normal pressure this happens at about

```
E_breakdown = 3 x 10^6 N/C   (3 million newtons per coulomb, or 3 kV per mm)
```

Lightning, static zaps, the click of a gas lighter and the ozone smell near old TVs are all air breaking down.

## The Concept

### Worked example 1: from force to field and back

A test charge of 1 pC (one picocoulomb, 10^-12 C) feels a force of 4.5 x 10^-8 N to the right.

```
E = F / q = 4.5e-8 / 1e-12 = 45,000 N/C, pointing right
```

Now put a 3 pC charge at the same spot:

```
F = q x E = 3e-12 x 45,000 = 1.35 x 10^-7 N, pointing right
```

And an electron (q = -1.602 x 10^-19 C):

```
F = -1.602e-19 x 45,000 = -7.21 x 10^-15 N   (minus sign: it points left)
```

### Worked example 2: field of a 1 nC charge

```
r = 1 cm  = 0.01 m:  E = 8.988e9 x 1e-9 / (0.01)^2 = 8.988 / 1e-4 = 89,880 N/C
r = 2 cm  = 0.02 m:  E = 8.988 / 4e-4                            = 22,470 N/C
r = 5 cm  = 0.05 m:  E = 8.988 / 2.5e-3                          =  3,595 N/C
r = 10 cm = 0.10 m:  E = 8.988 / 0.01                            =    899 N/C
```

Doubling r from 1 cm to 2 cm divides E by 4 (89,880 / 4 = 22,470). Going from 1 cm to 10 cm (ten times farther) divides it by 100.

### Superposition of fields

Fields from several charges add just like forces did in Lesson 02: compute each one separately, then add the arrows component by component.

```
E_total = E_1 + E_2 + E_3 + ...        (vector addition)
```

### Worked example 3: the dipole, point by point

Put +1 nC at (-1 cm, 0) and -1 nC at (+1 cm, 0).

**At the midpoint (0, 0).** Each charge is 1 cm away, so each field has size 89,880 N/C.

- From the +1 nC: points *away* from it, so toward +x: [+89,880, 0].
- From the -1 nC: points *toward* it, which is also toward +x: [+89,880, 0].

```
E = [+179,760, 0] N/C
```

Both push a + test charge the same way (away from + and toward -), so they add up. Between the two charges the field is strong.

**Straight above, at (0, +1 cm).** Each charge is now sqrt(1^2 + 1^2) = 1.414 cm away, so each field has size 89,880 / 2 = 44,940 N/C (the distance squared is 2 cm^2 instead of 1). Directions:

- From the + at (-1, 0): away from it, along the arrow (+1, +1) / 1.414.
- From the - at (+1, 0): toward it, along (+1, -1) / 1.414.

```
x: 44,940 x (1/1.414) + 44,940 x (1/1.414) = 31,777 + 31,777 = 63,555 N/C
y: 44,940 x (1/1.414) - 44,940 x (1/1.414) = 0
E = [+63,555, 0] N/C
```

The up and down parts cancel; the sideways parts add. The field above the dipole points parallel to the line from + to -.

**On the axis, to the right, at (3 cm, 0).** The + charge is 4 cm away, the - charge 2 cm away.

```
from +1 nC: 8.988 / (0.04)^2 = 5,617.5 N/C, away from it: toward +x
from -1 nC: 8.988 / (0.02)^2 = 22,470 N/C, toward it:   toward -x
E = 5,617.5 - 22,470 = -16,852.5 N/C   (points left, back toward the - charge)
```

Out here the closer - charge wins. By the symmetry of the setup, at (-3 cm, 0) you get the same answer: -16,852.5 N/C, also pointing left (now away from the closer + charge).

### Worked example 4: parallel plates and an electron

Two square plates, 10 cm x 10 cm, carry +1 nC and -1 nC.

```
A     = 0.10 x 0.10 = 0.01 m^2
sigma = 1e-9 / 0.01 = 1e-7 C/m^2
E     = 1e-7 / 8.854e-12 = 11,294 N/C
```

An electron between the plates feels

```
F = e x E = 1.602e-19 x 11,294 = 1.81 x 10^-15 N   (toward the + plate)
a = F / m = 1.81e-15 / 9.109e-31 = 1.99 x 10^15 m/s^2
```

That is 2 x 10^14 times the acceleration of gravity (g = 9.81 m/s^2). The electron's weight, m x g = 8.9 x 10^-30 N, is fifteen orders of magnitude smaller than the electric force: forget it. Starting from rest, how long to cross a 5 mm gap? From d = (1/2) a t^2, t = sqrt(2d / a):

```
t = sqrt(2 x 0.005 / 1.99e15) = sqrt(5.03e-18) = 2.2 x 10^-9 s = 2.2 ns
```

Two nanoseconds. Electrons in a field respond fast, which is why electronics is fast.

### Worked example 5: how much charge before sparks?

How much charge can those plates hold before the air between them breaks down? Set E = 3 x 10^6 N/C and solve E = Q / (A x eps0) for Q:

```
Q = E x eps0 x A = 3e6 x 8.854e-12 x 0.01 = 2.66 x 10^-7 C = 266 nC
```

And near a single 1 uC point charge, the field drops below breakdown only beyond

```
r = sqrt(k x Q / E_breakdown) = sqrt(8.988e9 x 1e-6 / 3e6) = sqrt(3.0e-3) = 0.055 m = 5.5 cm
```

So a ball with 1 uC on it, smaller than 5.5 cm in radius, would leak charge into the air with a hiss and a glow (corona). This is why you cannot pile up coulombs on things, as Lesson 02 claimed.

## Build It

The program `code/main.py` reproduces every example and draws the dipole field. Run it from the repo root:

```
uv run python phases/01-the-physics-underneath/03-the-electric-field/code/main.py
```

### Step 1: Field = force per unit charge

```python
test_charge = 1e-12
force_on_test = np.array([4.5e-8, 0.0])
field = force_on_test / test_charge
print(f"  a {test_charge * 1e12:.0f} pC test charge feels {force_on_test[0]:.1e} N -> E = {field[0]:,.0f} N/C")
print(f"  a 3 pC charge at the same spot feels {3e-12 * field[0]:.2e} N")
print(f"  an electron there feels {-ELEMENTARY_CHARGE * field[0]:.3e} N (opposite way)")
```

Output: E = 45,000 N/C; 1.35e-07 N on 3 pC; -7.210e-15 N on an electron.

### Step 2: Field of a point charge

```python
source_charge = 1e-9
for distance in [0.01, 0.02, 0.05, 0.10]:
    strength = COULOMB_CONSTANT * source_charge / distance**2
```

Output: 89,880.0, 22,470.0, 3,595.2 and 898.8 N/C.

### Step 3: Superposition for a dipole

`point_charge_field` returns the vector kQ / r^2 times the unit vector from the charge to the point. If Q is negative the vector automatically flips toward the charge. `total_field` adds them.

```python
def point_charge_field(charge, source_position, point):
    separation = point - source_position
    distance = np.linalg.norm(separation)
    return COULOMB_CONSTANT * charge / distance**2 * separation / distance


def total_field(sources, point):
    field = np.zeros(2)
    for charge, position in sources:
        field += point_charge_field(charge, position, point)
    return field


dipole = [
    (+1e-9, np.array([-0.01, 0.0])),
    (-1e-9, np.array([+0.01, 0.0])),
]
```

Output: [+179,760, 0] at the midpoint, [+63,554.8, 0] above it, [-16,852.5, 0] at both (3 cm, 0) and (-3 cm, 0). These match the hand calculations.

### Step 4: Parallel plates

```python
EPSILON_0 = 8.854e-12


def parallel_plate_field(charge, area):
    return charge / area / EPSILON_0


uniform = parallel_plate_field(1e-9, 0.10 * 0.10)
electron_acceleration = ELEMENTARY_CHARGE * uniform / ELECTRON_MASS
time_to_cross = np.sqrt(2 * 0.005 / electron_acceleration)
```

Output: E = 11,294 N/C, acceleration 1.987e+15 m/s^2 (2.03e+14 g), crossing time 2.2 ns.

### Step 5: Breakdown

```python
AIR_BREAKDOWN_FIELD = 3e6
charge_for_spark = AIR_BREAKDOWN_FIELD * EPSILON_0 * plate_area
radius_for_1uC = np.sqrt(COULOMB_CONSTANT * 1e-6 / AIR_BREAKDOWN_FIELD)
```

Output: 266 nC on the plates, 5.5 cm around a 1 uC charge.

### Step 6: The whole field on a grid

Calling `total_field` point by point works, but numpy can do a whole grid at once. `np.meshgrid` builds two 2-D arrays holding the x and y coordinate of every grid point; then the same formula runs on all points simultaneously. Note `distance**3`: kQ / r^2 times the unit vector (dx / r, dy / r) is kQ dx / r^3.

```python
def field_on_grid(sources, xs, ys):
    grid_x, grid_y = np.meshgrid(xs, ys)
    field_x = np.zeros_like(grid_x)
    field_y = np.zeros_like(grid_y)
    for charge, position in sources:
        dx = grid_x - position[0]
        dy = grid_y - position[1]
        distance = np.sqrt(dx**2 + dy**2)
        strength = COULOMB_CONSTANT * charge / distance**3
        field_x += strength * dx
        field_y += strength * dy
    return grid_x, grid_y, field_x, field_y


xs = np.linspace(-0.04, 0.04, 21)
ys = np.linspace(-0.03, 0.03, 15)
grid_x, grid_y, field_x, field_y = field_on_grid(dipole, xs, ys)
magnitude = np.sqrt(field_x**2 + field_y**2)
```

The grid is chosen so no point lands exactly on a charge (that would divide by zero). The script checks that the grid value at the centre equals the point-by-point answer, then saves `out.png` with `plt.quiver`: one arrow per grid point, all the same length (we divide by the magnitude) and coloured by the logarithm of the strength so both strong and weak regions show. You will see arrows pouring out of the red + charge, curving around and into the blue - charge, the dipole picture from above.

Output: 315 points, strongest about 2.27 million N/C (near the charges, close to breakdown!), weakest about 2,500 N/C at the corners.

## Use It

- **Capacitors.** Every capacitor is two conductors with a field between them. Its maximum voltage rating comes from the breakdown field of the insulator between the plates (Phase 07).
- **Transistor gates.** A MOSFET (Phase 12) has a metal gate separated from silicon by a very thin insulator. A field through that insulator pulls charges into a channel and turns the transistor on, without any current flowing into the gate. Oxide layers only a few nanometres thick see fields near 10^9 N/C, which is why ESD (Lesson 02) can destroy them.
- **Lightning rods and sharp points.** Fields concentrate at sharp tips of conductors, so sparks and corona start there. High-voltage equipment uses smooth, round shapes to avoid it; lightning rods use points on purpose.
- **Shielding.** Since the field inside a closed conductor is zero, a metal box (a "Faraday cage") shields its contents from outside fields. Your microwave oven door's metal mesh and the metal can over a radio chip both use this.
- **Old CRT screens and oscilloscopes.** Electron beams were steered by uniform fields between pairs of deflection plates, exactly worked example 4.

## Common Mistakes

- **Mixing up E and F.** E is a property of the place (N/C). F is the push on a particular charge (N). F = q x E connects them.
- **Forgetting that electrons go against the field.** E points the way a positive charge is pushed. An electron, being negative, is pushed the opposite way.
- **Thinking field lines are paths that charges follow.** A charge starting at rest accelerates along the line, but once it is moving it can swing off it. Field lines show the direction of the force, not trajectories.
- **Adding field sizes instead of vectors.** Above the dipole, each charge contributes 44,940 N/C, yet the total is 63,555, not 89,880, because the vertical parts cancel.
- **Using kQ / r^2 for plates.** That formula is for point charges. Between large parallel plates the field is uniform: sigma / eps0, independent of position.
- **Putting a probe right on a charge.** At r = 0 the point-charge formula divides by zero. Real charges have size; in code, keep grid points off the charges.

## Exercises

1. **Force from a field.** In a region where E = 2,000 N/C pointing up, what force acts on a +5 nC charge? On a proton? On an electron (size and direction)?
2. **Point charge.** At what distance from a +4 nC charge is the field 10,000 N/C?
3. **Two equal charges.** Put +1 nC at (-1 cm, 0) and +1 nC at (+1 cm, 0). What is the field at the midpoint? At (0, 1 cm)? Change `dipole` in `main.py` and look at the new plot: where do the lines go?
4. **Plates.** Two plates of 5 cm x 5 cm hold +-2 nC. Compute the field between them. Would a proton or an electron cross a 2 mm gap faster from rest, and by what factor?
5. **Millikan's drop (harder).** An oil drop of mass 3.27 x 10^-15 kg hovers between horizontal plates where the field is 1.0 x 10^5 N/C pointing up. What is the drop's charge? How many elementary charges is that, and of which sign?

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Electric field | "The electricity in the air" | At each point, the force per coulomb a small positive charge would feel there: E = F / q, a vector in N/C (= V/m) |
| Field line | "The path electricity takes" | A curve tangent to E at every point; density shows strength; not a particle path |
| Point charge | "A tiny charge" | Any charge small compared with the distances you care about, so kQ / r^2 applies |
| Uniform field | "Constant field" | Same size and direction throughout a region, as between large parallel plates |
| Superposition | "Fields add" | The total field is the vector sum of the fields of each charge alone |
| Breakdown | "It sparked" | The field became strong enough (about 3 x 10^6 N/C in air) to make the insulator conduct |

## Further Reading

- [OpenStax University Physics Volume 2, Sections 5.4 to 5.6 (Electric Field, Field Lines)](https://openstax.org/books/university-physics-volume-2/pages/5-4-electric-field) — clear derivations and field-line pictures
- [The Feynman Lectures on Physics, Volume II, Chapters 4 and 5 (Electrostatics, Gauss's law)](https://www.feynmanlectures.caltech.edu/II_04.html) — where the parallel-plate result comes from, beautifully explained
- [PhET simulation "Charges and Fields" (University of Colorado)](https://phet.colorado.edu/en/simulations/charges-and-fields) — drag charges around and watch the field change
- [HyperPhysics: Electric field](http://hyperphysics.phy-astr.gsu.edu/hbase/electric/elefie.html) — compact reference with formulas for common shapes
