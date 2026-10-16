# Magnets and Magnetic Fields

> A magnetic field is the invisible pattern around a magnet or a moving charge. It pushes only on charges that move, and it pushes them sideways.

**Type:** Learn
**Prerequisites:** Phase 01 (The Physics Underneath), Lesson 05 (The Electric Field) and Lesson 08 (Current as Moving Charge); Phase 07 (Capacitors), Lesson 06 (Energy in the Electric Field)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Magnet | An object that pulls on iron and pushes or pulls on other magnets | The thing holding a shopping list to your fridge |
| Pole | One of the two ends of a magnet where the pull is strongest, called north (N) and south (S) | The two ends of a fridge magnet's strip, or of a compass needle |
| Magnetic field | The "influence" a magnet spreads into the space around it; at every point it has a strength and a direction | Iron filings sprinkled on paper over a magnet line up in curved patterns: they are drawing the field |
| Field line | A curve drawn so that at every point it follows the field's direction | Like the lines on a weather map that show which way the wind blows |
| Tesla (T) | The unit of magnetic field strength (more precisely, of *magnetic flux density*, symbol **B**) | 1 T is strong: a big neodymium magnet touching your hand is about 0.5 T |
| Gauss (G) | An older, smaller unit: 1 T = 10,000 G | Earth's field is about half a gauss |
| Magnetic moment | How "strong" a whole magnet is as a source of field, symbol **m**, unit A·m² | A bigger, stronger magnet has a bigger moment |
| Dipole | A source with a north and a south end, like a bar magnet or a compass needle | Every magnet you have ever held |
| Lorentz force | The sideways push that a magnetic field gives to a moving charge | A ball rolling across a turntable seems to curve sideways |
| Permanent magnet | A material that keeps its magnetism without any current | Fridge magnets, speaker magnets, the magnets in a motor |
| Ferromagnetic | A material (iron, nickel, cobalt) whose atoms can line up and become strongly magnetic | Why a paperclip sticks to a magnet but an aluminium can does not |

## Learning Objectives

- Describe what a magnetic field is, how its strength is measured in teslas, and how it is drawn with field lines
- Explain why magnetic poles always come in pairs and why like poles repel
- Calculate the field of a small magnet at a distance and see why it falls off with the cube of the distance
- Calculate the force on a moving charge with F = q v B and explain why the force is sideways
- Connect magnetism to electronics: every inductor, transformer, motor, speaker and hard disk in later lessons runs on this idea

## The Problem

Up to now, every circuit in this course has been about electric charge sitting on capacitor plates or flowing through resistors. That is half of the story. Open almost any device and you will find parts that work on the *other* half: the coil in a phone charger, the transformer in an old power brick, the motor that spins a fan, the speaker that makes sound, the relay that clicks when your washing machine starts, the wireless charging pad under your phone. None of them can be understood with Ohm's law alone.

All of them use **magnetism**. And magnetism is not a separate force that happens to live next door to electricity. It is what electric charge does when it *moves*. A magnet on your fridge works because of electrons spinning and orbiting inside its atoms. A wire carrying current makes a magnetic field. A changing magnetic field pushes current around a wire. This phase follows that chain: magnets (this lesson), current making magnetism (Lesson 02), magnetism making current (Lesson 03), and then the components built on these ideas: the inductor, the transformer and the motor.

Before any of that, we need a clear picture of what a magnetic field *is*, how strong typical fields are, and what they do to a moving charge.

## The Physics

### What people noticed first

People in ancient Greece and China found a rock, *lodestone* (a natural magnetic iron ore called magnetite), that attracted iron. Chinese navigators used magnetised needles as compasses by around the 11th century. In 1600 William Gilbert, an English physician, published *De Magnete*, where he argued that the Earth itself is a giant magnet. That explains why a compass points north: the needle is a tiny magnet lining up with the Earth's field.

Here are the basic facts any child with two magnets can discover:

1. Every magnet has two ends, called **poles**. We call them **north (N)** and **south (S)**. The north pole of a compass needle is the end that points (roughly) towards the geographic north of the Earth.
2. **Like poles repel** (N pushes N away, S pushes S away) and **unlike poles attract** (N pulls S).
3. **You cannot isolate a pole.** Cut a bar magnet in half and you do not get a lonely north and a lonely south. You get two smaller magnets, each with its own N and S. Cut again and again, down to single atoms: still N and S together.

Fact 3 is the big difference from electric charge. In Phase 01 you met positive and negative charges that can exist on their own: an electron is a lonely negative charge. Magnetism has no such "lonely" pole. Nobody has ever found one.

A side fact that confuses everyone: since unlike poles attract, and the north pole of a compass points north, the Earth's *geographic* north is actually near a magnetic *south* pole. The naming is historical, not physical.

### Why some materials are magnetic

Every electron behaves like a microscopic magnet. Part of this comes from the electron's motion around its atom (a circulating charge is a tiny current loop) and part from a built-in property called **spin**, which makes each electron a tiny magnet even when it is not orbiting anything. You do not need quantum mechanics for this course; just keep the picture of "each electron is a tiny compass needle".

In most materials these tiny magnets point in random directions or pair up and cancel, so the material is not magnetic. In a few materials (iron, nickel, cobalt and some alloys, called **ferromagnetic**), neighbouring atoms *prefer* to line their tiny magnets up in the same direction. They form regions called **domains**, each maybe a tenth of a millimetre across, where everything points the same way.

```
 unmagnetised iron                 magnetised iron
 (domains point every which way)   (domains lined up)

 +-----+-----+-----+               +-----+-----+-----+
 |  ^  | <-  |  v  |               | ->  | ->  | ->  |
 +-----+-----+-----+               +-----+-----+-----+
 | ->  |  v  |  ^  |               | ->  | ->  | ->  |
 +-----+-----+-----+               +-----+-----+-----+
   net field: about zero             net field: strong, points ->
```

A paperclip is unmagnetised iron. When you bring a magnet close, its field pushes the domains in the paperclip to line up, so the paperclip briefly becomes a magnet itself, with the opposite pole facing your magnet. That is why it sticks. Take the magnet away and the domains mostly fall back to random: the paperclip lets go.

A **permanent magnet** is a material where, once the domains are lined up (usually by a very strong field in the factory), they *stay* lined up. Modern permanent magnets are made from alloys such as neodymium-iron-boron (NdFeB, "neodymium magnets") or ferrite ceramics (the dark grey fridge and speaker magnets).

Aluminium, copper and plastic are not ferromagnetic. A magnet does not stick to a soda can or to a copper wire. (We will see in Lesson 03 that a *moving* magnet does push on copper, through a completely different effect.)

### What a field is

In Phase 01, Lesson 05 you met the **electric field**: a way of saying "at every point in space, there is an arrow telling you which way and how hard a test charge would be pushed". The **magnetic field** is the same kind of idea: at every point there is an arrow, a strength and a direction. We write it **B**.

How do you see it? Two ways:

- Sprinkle iron filings on a sheet of paper over a magnet and tap the paper. Each filing becomes a tiny magnet and turns to line up with the field. The filings form curves.
- Walk a small compass around a magnet. At each spot the needle points along the field.

We draw **field lines**, curves that follow those arrows:

```
              field lines of a bar magnet (side view)

          .  -  -  -  .            lines leave the N end,
       .                 .         loop around outside,
     .     .  -  -  -  .   .       and come back into the S end
    .    .               .  .
    .   .    +-------+    .  .
   <----<----|  N    |---->---->    (lines come out of N on top
    .   .    |       |    .  .       in the full picture; this
    .   .    |  S    |    .  .       sketch is squashed)
    .    .   +-------+   .  .
     .     .  -  -  -  .   .
       .                 .
          .  -  -  -  .
```

The code for this lesson draws the real thing as a picture (`out.png`). Rules for reading field lines:

- The **direction** of a line at a point is the direction a compass needle's north end would point there.
- Outside a magnet, lines go **from N to S**. Inside the magnet they continue from S back to N, so **every field line is a closed loop**. That is the drawing version of "no lonely poles": lines never start or end on a point, unlike electric field lines which start on + charges and end on - charges.
- Where lines are **crowded**, the field is **strong**. Where they spread out, it is weak.

### The unit: the tesla

Field strength **B** is measured in **teslas (T)**, after Nikola Tesla. One tesla is a big field. Typical values:

| Situation | B |
|---|---|
| Earth's field at the surface | about 25 to 65 µT (we will use 50 µT = 0.00005 T) |
| Fridge magnet, at its surface | a few mT (say 5 mT) |
| Neodymium magnet, at its surface | 0.3 to 0.6 T |
| Hospital MRI scanner | 1.5 to 3 T |
| Strongest steady lab magnets | around 45 T |

Many datasheets and older books still use the **gauss (G)**: 1 T = 10,000 G. So Earth's field is about 0.5 G and a neodymium magnet is about 5,000 G.

The definition of the tesla comes from the force on a moving charge, which we meet next: a field of 1 T pushes with 1 newton on a charge of 1 coulomb moving at 1 metre per second across the field. Since a coulomb is a huge amount of charge (Phase 01), you can see why 1 T is a strong field.

## The Concept

### 1. How fast does a magnet's field fade with distance?

Put a small magnet at the origin, with its north pole pointing up (along an axis we call z). Far from the magnet compared with its own size, the field straight above it is

```
B = (mu0 / (4 pi)) * 2 m / z^3
```

Read it aloud: "the field on the axis is a constant, times two, times the magnet's moment, divided by the distance cubed". The pieces:

- **B** is the field in teslas.
- **mu0** (Greek letter mu, "mew-zero") is the **magnetic constant** or *permeability of free space*. It plays the same role for magnetism that epsilon-zero played for electric fields. Its value is very close to 4 x pi x 10^-7 = 1.2566 x 10^-6 in SI units (T·m/A). Notice that `mu0 / (4 pi)` is then exactly 10^-7, a handy number.
- **m** is the **magnetic moment** of the magnet, in ampere-square-metres (A·m²). It measures how strong the magnet is as a whole. (The unit hints at the deep truth of Lesson 02: a magnet behaves like a loop of current, and current times area is its strength.)
- **z** is the distance from the magnet's centre, in metres.

The key feature is the **z^3** in the denominator. Double the distance and the field drops by 2 x 2 x 2 = 8. Go ten times further and it drops by 1,000. Compare with the electric field of a single charge, which falls as 1/r^2. The magnet falls faster because its north and south poles partly cancel each other when you are far away.

**Where does m come from?** For a magnet of volume V made of a material with remanence B_r (the field the material keeps after magnetisation, about 1.2 to 1.4 T for neodymium alloys), a good estimate is

```
m = B_r * V / mu0
```

**Worked example.** A neodymium cube 1 cm on each side:

- Volume: V = 0.01 m x 0.01 m x 0.01 m = 1 x 10^-6 m³.
- Remanence: B_r = 1.3 T.
- m = 1.3 x 1e-6 / 1.2566e-6 = 1.035 A·m².

Field 10 cm (0.1 m) above its centre:

- z^3 = 0.1 x 0.1 x 0.1 = 0.001 m³
- B = 1e-7 x 2 x 1.035 / 0.001 = 2.07e-4 T = 207 µT.

That is about four times the Earth's field. Now at 20 cm: z^3 = 0.008, B = 1e-7 x 2.07 / 0.008 = 25.9 µT, half the Earth's field. Somewhere around 16 cm the magnet's field equals Earth's field, which is exactly the distance where a compass starts noticeably pointing at the magnet instead of north. The code finds 16.1 cm. Try it with a phone compass app and a fridge magnet!

The formula is only valid far from the magnet (several times its size). At 1 cm from the centre of a 1 cm cube you are only 5 mm from its face, and the exact formula for a cube-shaped magnet gives about 0.175 T there, lower than the far-field formula's 0.207 T. (On the face itself, the exact field is about 0.57 T.) At 10 cm the two agree to better than 0.1%. Keep "far away" in mind whenever you use a far-field formula.

### 2. What a field does: the force on a moving charge

Here is the strange heart of magnetism. A magnetic field does **nothing** to a charge sitting still. It only pushes on charges that **move**, and the push is **sideways**: at right angles both to the direction of motion and to the field.

The size of the force, when the charge moves straight across the field, is

```
F = q * v * B
```

Read it: "the force equals the charge times its speed times the field". Units: F in newtons (N), q in coulombs (C), v in metres per second (m/s), B in teslas.

If the charge moves at an angle theta to the field, only the part of its velocity *across* the field counts:

```
F = q * v * B * sin(theta)
```

`sin(theta)` is 1 at 90 degrees (moving straight across, full force), 0.707 at 45 degrees, and 0 at 0 degrees (moving along the field lines: no force at all).

This sideways push is called the **Lorentz force** (after Hendrik Lorentz, who wrote the combined electric plus magnetic force law in the 1890s).

**The direction** is given by a right-hand rule. Point the fingers of your right hand along the velocity of a *positive* charge, curl them towards the field direction; your thumb points along the force. For a negative charge, like an electron, the force is the other way.

```
   field B points into the page (x x x)

     x    x    x    x    x
                 ^ F (on a + charge)
     x    x    x | x    x
        + ------>         v
     x    x    x    x    x

   positive charge moving right, field into page -> pushed up
   an electron moving right would be pushed down
```

**Worked example.** An electron (charge 1.602 x 10^-19 C) moving at one million metres per second (1 x 10^6 m/s) straight across a 0.5 T field:

- F = 1.602e-19 x 1e6 x 0.5 = 8.01e-14 N.

That sounds tiny, but the electron's mass is also tiny (9.109 x 10^-31 kg), so the acceleration is huge: a = F / m = 8.8 x 10^16 m/s². The force is always sideways, so it never speeds the electron up or slows it down; it only bends its path. The electron goes round in a **circle**. The radius is

```
r = m_e * v / (q * B)
```

"radius equals mass times speed, divided by charge times field": r = 9.109e-31 x 1e6 / (1.602e-19 x 0.5) = 1.137e-5 m, about 11 micrometres. Old television tubes (cathode ray tubes) used exactly this effect, with coils around the neck of the tube, to steer the electron beam across the screen. Particle accelerators and mass spectrometers use it today.

### 3. Why the force is sideways matters for electronics

A wire carrying current is full of moving charges. Put the wire in a magnetic field and every moving electron gets a sideways push; the electrons push on the metal; **the wire moves**. That is the motor of Lesson 07. Conversely, if you *move* a wire through a field, you push the free electrons inside it sideways, *along* the wire, and a voltage appears between its ends. That is the generator, and the first glimpse of Faraday's law in Lesson 03. Both effects come from F = q v B.

There is one more subtle point that will matter a lot. Because the force is always perpendicular to the motion, **a magnetic field alone does no work on a charge**. It can steer, but it cannot give or take energy directly. In motors and generators the energy is still exchanged, but through the electric forces inside the wire and the circuit. Physicists sometimes say "the magnetic field is the steering wheel, not the engine".

### 4. Why a compass needle turns: torque on a magnet

A compass needle is a tiny magnet with moment m. Put it in a field B at an angle theta to the field and the field twists it with a **torque** (a turning force, measured in newton-metres, N·m):

```
torque = m * B * sin(theta)
```

When the needle points along the field (theta = 0) the torque is zero, and if you nudge it, the torque pushes it back: that is a stable position. At 90 degrees the twist is strongest. At 180 degrees (pointing exactly backwards) the torque is zero again, but any nudge makes it flip round: an unstable position.

For a needle with m = 0.05 A·m² in Earth's 50 µT field, at 90 degrees: torque = 0.05 x 50e-6 x 1 = 2.5 x 10^-6 N·m. That is tiny, which is why compass needles are mounted on a sharp pivot with very little friction.

Motors (Lesson 07) work by keeping a coil, which behaves like a magnet, permanently at an angle to a field so that it is always twisted.

## Build It

The code in `code/main.py` turns each idea above into numbers you can check by hand.

### Step 1: Units

```python
def tesla_to_gauss(b):
    return b * 1e4


for name, b in [("Earth's field", EARTH_FIELD), ("fridge magnet surface", 5e-3),
                ("neodymium magnet surface", 0.5), ("MRI scanner", 3.0)]:
    print(f"  {name:<26} {b:>10.6f} T = {tesla_to_gauss(b):>10.1f} gauss")
```

Output: Earth 0.00005 T = 0.5 G, fridge magnet 50 G, neodymium 5,000 G, MRI 30,000 G. Notice the range: the MRI field is 60,000 times stronger than Earth's.

### Step 2: The moment of a neodymium cube

```python
def magnet_moment_from_remanence(remanence, volume):
    return remanence * volume / MU0


side = 0.01
volume = side**3
moment = magnet_moment_from_remanence(1.3, volume)
```

This prints `m = 1.035 A*m^2`, the same number as the worked example.

### Step 3: The 1/z³ fall-off

```python
def dipole_field_on_axis(moment, distance):
    return MU0 / (4 * np.pi) * 2 * moment / distance**3


def distance_where_field_equals(moment, target_field):
    return (MU0 / (4 * np.pi) * 2 * moment / target_field) ** (1 / 3)
```

The script prints the field at 1, 2, 5, 10, 20 and 50 cm:

```
   10 cm from the centre: B =       206.90 uT  (     4.14 x Earth)
   20 cm from the centre: B =        25.86 uT  (     0.52 x Earth)
   50 cm from the centre: B =         1.66 uT  (     0.03 x Earth)
  the magnet matches Earth's 50 uT at 16.1 cm
```

Check the ratio between 10 cm and 20 cm: 206.90 / 25.86 = 8.0. Doubling the distance divided the field by 8, the cube law.

`distance_where_field_equals` is the same formula solved for z: if B = k / z^3 then z = (k / B)^(1/3), the cube root.

### Step 4: The Lorentz force and the electron's circle

```python
def magnetic_force_on_charge(charge, speed, field, angle_deg=90.0):
    return abs(charge) * speed * field * np.sin(np.radians(angle_deg))


def circle_radius(mass, speed, charge, field):
    return mass * speed / (abs(charge) * field)
```

The output gives F = 8.011e-14 N at 90 degrees, 5.665e-14 N at 45 degrees (8.011 x 0.7071), and exactly zero at 0 degrees, and a radius of 11.37 µm.

### Step 5: Compass torque

```python
def compass_torque(moment, field, angle_deg):
    return moment * field * np.sin(np.radians(angle_deg))
```

Torque is 0 at 0 degrees, 1.25 µN·m at 30 degrees (half of the maximum, because sin 30° = 0.5), 2.5 µN·m at 90 degrees, and 0 again at 180 degrees.

### Step 6: Draw the field lines

`dipole_field_at(moment, x, z)` computes both components of the dipole field at every point of a grid, and `save_field_plot` hands them to matplotlib's `streamplot`, which traces curves that follow the arrows. Open `out.png`: lines leave the top (N), swing around and enter the bottom (S), crowded near the magnet and sparse far away. Colour shows strength on a logarithmic scale.

## Use It

- **Speakers and headphones.** A permanent magnet (ferrite in cheap speakers, neodymium in earbuds) sits inside a coil glued to the speaker cone. Current in the coil feels a force in the magnet's field (Lesson 02) and pushes the cone. Neodymium is why earbuds can be so small: more field from less material.
- **Hall-effect sensors.** The Lorentz force on charges moving through a thin semiconductor plate pushes them to one side, producing a small voltage across the plate proportional to B. Parts like the Allegro A1324 output a voltage that changes by a few millivolts per gauss. Phones use similar sensors as a compass (magnetometer) and laptops use one to detect when the lid, which hides a small magnet, is closed.
- **Reed switches** are two thin iron contacts in a glass tube; a nearby magnet magnetises them, they attract and close a circuit. Door and window alarms use them.
- **Hard disks** store bits as tiny magnetised regions on a spinning platter, pointing one way or the other.
- **Magnet datasheets.** A neodymium magnet grade like "N42" refers to its maximum energy product (42 MGOe). Datasheets give remanence (B_r around 1.3 T for N42) and the maximum working temperature: neodymium magnets lose strength when hot, which is a real design limit in motors.

## Common Mistakes

- **Thinking a magnetic field pushes on any charge.** It pushes only on *moving* charges, and only on the part of the motion across the field. A charged balloon sitting next to a magnet feels nothing magnetic.
- **Expecting the force along the field.** The Lorentz force is sideways. Beginners draw it pointing along B or along v; it is perpendicular to both.
- **Mixing up the right-hand rule for electrons.** The rule is for positive charges. Electrons get pushed the opposite way. Since current in circuits is conventional current (positive charge direction, Phase 01), using the rule with the *current* direction gives the right answer for wires.
- **Using the far-field formula right next to the magnet.** The 1/z³ formula is for distances several times the magnet's size. Close up it overestimates.
- **Believing every metal sticks to a magnet.** Only ferromagnetic ones (iron, steel, nickel, cobalt). Aluminium, copper, brass and most stainless steels used in kitchens do not.
- **Thinking you can separate N and S.** Breaking a magnet gives two magnets.

## Exercises

1. **Easy.** Convert to teslas: 0.6 G, 1,200 G, 25 mT. Convert to gauss: 0.25 T, 40 µT.
2. **Easy.** Using the cube law, if a magnet's field is 800 µT at 5 cm, what is it at 10 cm and at 2.5 cm?
3. **Medium.** A proton (charge 1.602e-19 C, mass 1.673e-27 kg) moves at 2 x 10^5 m/s across a 0.1 T field. Find the force and the radius of its circle. Compare the radius with that of an electron at the same speed: why is it 1,836 times larger?
4. **Medium.** A neodymium disc has a volume of 0.5 cm³ (5 x 10^-7 m³) and B_r = 1.25 T. Estimate its moment, then the distance at which its on-axis field equals 50 µT. Change `main.py` to check.
5. **Hard.** At what angle is the torque on a compass needle half its maximum value? There are two answers between 0 and 180 degrees. Which one is stable? Explain using the sign of the torque when you nudge the needle a little.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Magnetic field B | "The magnetism around a magnet" | A vector at every point in space whose direction a compass follows and whose strength (in teslas) sets the force on moving charges |
| Field line | "The lines of force" | A curve tangent everywhere to B; for magnetism they always close on themselves |
| Tesla | "A unit of magnet strength" | 1 T pushes 1 N on 1 C moving at 1 m/s across the field; 1 T = 10,000 G |
| Magnetic moment | "How strong a magnet is" | The quantity m (A·m²) that sets the far field of a magnet: B on axis = 1e-7 x 2 m / z³ |
| Lorentz force | "Magnets push on electrons" | F = q v B sin(theta), perpendicular to both the velocity and the field; zero for charges at rest |
| Ferromagnetism | "Magnetic metals" | The tendency of iron, nickel and cobalt atoms to align their magnetic moments in domains |
| Permeability mu0 | "A physics constant" | The constant (about 1.2566e-6 T·m/A) that links currents and magnets to the fields they produce in vacuum |

## Further Reading

- [The Feynman Lectures on Physics, Vol. II, Chapter 1 (Electromagnetism) and Chapter 13 (Magnetostatics)](https://www.feynmanlectures.caltech.edu/II_toc.html) — why magnetism is the "moving charge" side of electricity
- [HyperPhysics: Magnetic field and magnetic force](http://hyperphysics.phy-astr.gsu.edu/hbase/magnetic/magfor.html) — short pages with the Lorentz force and right-hand rules
- [Khan Academy: Magnetic forces, magnetic fields and Faraday's law](https://www.khanacademy.org/science/physics/magnetic-forces-and-magnetic-fields) — gentle videos on magnets and moving charges
- *Practical Electronics for Inventors* (Scherz & Monk), chapter on magnetism and inductors — the practical side: magnets, coils and sensors
