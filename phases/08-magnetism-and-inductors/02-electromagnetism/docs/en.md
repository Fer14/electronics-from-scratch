# Electromagnetism

> Every current makes a magnetic field. Wind the wire into a coil and you have a magnet you can switch on and off.

**Type:** Learn
**Prerequisites:** Phase 08 (Magnetism and Inductors), Lesson 01 (Magnets and Magnetic Fields); Phase 05 (Circuit Analysis and Our Simulator), Lesson 04 (Modified Nodal Analysis from Scratch)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Electromagnetism | The fact that electric currents make magnetic fields (and, in Lesson 03, the reverse) | A crane in a scrapyard that picks up cars with a switched-on magnet |
| Right-hand grip rule | A trick with your right hand to find which way the field circles a wire | Grabbing a broom handle: thumb along the current, fingers curl along the field |
| Coil | Wire wound in many turns, usually around a tube | Thread wound on a spool |
| Turn | One complete loop of wire in a coil | One lap of the thread around the spool |
| Solenoid | A long coil whose turns are packed side by side | A spring-shaped coil, longer than it is wide |
| Electromagnet | A coil, often wound on iron, that is a magnet only while current flows | The lifting magnet at a scrapyard, a door-lock bolt |
| Core | The material inside a coil (air, iron, ferrite) | The spool the thread is wound on |
| Relative permeability (mu_r) | How many times more a material multiplies the field compared with empty space | Iron "gathers" field lines the way a sponge gathers water |
| Saturation | The point where a core cannot be magnetised any further | A sponge that is already soaked |
| Relay | A switch that is flipped by an electromagnet | The click you hear when a washing machine or a car's indicator starts |
| Biot-Savart law | The rule that adds up the field of every tiny piece of a wire | Adding up the light from every bulb in a long string of fairy lights |

## Learning Objectives

- Describe Oersted's discovery and use the right-hand grip rule to find the direction of the field around a wire
- Calculate the field near a long straight wire with B = mu0 I / (2 pi r) and check it by adding up tiny pieces of wire
- Calculate the field inside a solenoid with B = mu0 n I and explain why an iron core makes it much stronger, up to saturation
- Calculate the force on a current-carrying wire in a field, F = B I L, and the force between two wires
- Design the drive circuit of a relay coil with our simulator

## The Problem

In Lesson 01 the magnets were permanent: you cannot turn a fridge magnet off. That makes them useless for anything that needs control. A door lock that opens when you press a button, a loudspeaker that follows music, a motor whose speed you choose, a relay that lets a tiny microcontroller pin switch a 230 V heater: all of these need a magnet you can switch on, switch off, reverse and make stronger or weaker on command.

The way to get one is surprisingly simple: **run a current through a wire**. Every current is surrounded by a magnetic field. Wind the wire into a coil and the fields of all the turns add up into something that behaves just like a bar magnet, but with a north and south you control with a switch. This is the bridge between the circuits of Phases 02 to 07 and the magnetic world of Lesson 01, and it is the reason inductors, transformers and motors exist.

## The Physics

### Oersted's compass, 1820

In April 1820, during a lecture in Copenhagen, Hans Christian Oersted noticed that a compass needle near a wire twitched when he connected the wire to a battery. Nobody had expected this: electricity and magnetism were thought to be unrelated. Within weeks, André-Marie Ampère in Paris had worked out the rules, and within a decade the electromagnet, the electric motor and the generator had all been invented.

What Oersted saw: a current in a straight wire creates a magnetic field that **circles around the wire**. The field lines are rings centred on the wire, lying in planes perpendicular to it. A compass held near the wire turns to point *along* these rings, which is sideways to the wire.

```
     looking along the wire, current coming towards you (.)

             <- - - -
          /           \
         |      .      |      field lines are circles around the wire
          \           /       (counter-clockwise for current towards you)
             - - - ->
```

### Why moving charge makes a field

Lesson 01 said the magnetic field is what electric charge does when it moves. Here is the fuller story in one paragraph. Special relativity (Einstein, 1905) shows that electric and magnetic fields are two faces of a single thing: what looks like a purely electric field to one observer looks partly magnetic to another observer moving relative to the first. A wire carrying current is electrically neutral (as many electrons as protons), but the electrons are drifting. The result, seen from outside, is a magnetic field around the wire. You do not need relativity to use any of this; the point is that magnetism is not a separate "magic" force: it is electricity seen in motion.

### The right-hand grip rule

To find which way the rings circle:

> Grip the wire with your right hand, thumb pointing in the direction of the (conventional) current. Your fingers curl in the direction of the field.

Remember that conventional current flows from + to - outside the source (Phase 01, Lesson 08); electrons drift the opposite way, but all the rules here use conventional current.

### Coils and solenoids

A single loop of wire makes a field that, at the centre of the loop, points straight through it (use the grip rule on each piece of the loop: every piece makes the field go the same way through the middle). Stack many loops side by side into a **solenoid** and their fields add up:

```
   current in -->  ( ( ( ( ( ( ( ( ( ( )  --> current out
                   | | | | | | | | | | |
     S  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  N     strong, uniform
                   | | | | | | | | | | |                  field inside,
                   ( ( ( ( ( ( ( ( ( ( )                  points along axis

   outside, the lines loop back around from N to S, like a bar magnet
```

Inside a long solenoid the field is strong, nearly uniform and points along the axis. Outside, the field loops around exactly like the field of a bar magnet (compare the picture in Lesson 01). **A solenoid with current is a bar magnet**, and a bar magnet is, at the atomic level, a huge number of tiny current loops. This is the same physics seen from two ends.

Which end is north? Curl the fingers of your right hand around the coil in the direction the current flows round the turns; your thumb points to the north end.

### Iron makes it stronger

Put an iron rod inside the solenoid. The coil's field lines up the iron's magnetic domains (Lesson 01), and the iron's own aligned atoms add their field to the coil's. The total field can be hundreds or thousands of times bigger. We describe this with the **relative permeability** mu_r:

```
B (with core) = mu_r * B (air)
```

"The field with the core is mu_r times the field in air." Soft iron can have mu_r in the thousands, ferrites (ceramic magnetic materials used in electronics) from tens to thousands.

Two warnings, both important for later lessons:

1. **Saturation.** Once nearly all the domains are lined up, the iron cannot add any more. Iron saturates around 1.5 to 2 T, ferrite around 0.3 to 0.5 T. Beyond that, extra current only adds the small "air" field. Inductors and transformers have a maximum current for exactly this reason.
2. **Gaps.** If the magnetic path goes partly through air (as in an electromagnet lifting something, or a core with a gap), the air dominates and the effective mu_r is much lower than the material's. Real electromagnet designs use an *effective* mu_r of tens or hundreds, not thousands.

### Forces on wires

In Lesson 01 a moving charge in a field felt a sideways force F = q v B. A wire carrying current is a long line of moving charges, so a wire in a field is pushed sideways too. Adding up the forces on all the charges in a length L of wire gives

```
F = B * I * L
```

"the force equals field times current times length" (for a wire straight across the field). That is the force that turns every electric motor (Lesson 07) and moves every loudspeaker cone.

Since each wire makes a field and each wire feels a field, **two parallel wires push on each other**: they attract if the currents go the same way, repel if opposite. The force per metre of wire is

```
F / L = mu0 * I1 * I2 / (2 pi d)
```

with d the distance between the wires. Until 2019 the ampere itself was *defined* by this: one ampere is the current that, in two long parallel wires one metre apart, gives a force of exactly 2 x 10^-7 newtons per metre.

## The Concept

### 1. The field of a long straight wire

```
B = mu0 * I / (2 pi r)
```

Read it: "the field is the magnetic constant, times the current, divided by two pi times the distance". B in teslas, I in amperes, r in metres, and mu0 = 4 pi x 10^-7 T·m/A as in Lesson 01. Since mu0 / (2 pi) = 2 x 10^-7 exactly, the formula is simply

```
B = 2e-7 * I / r
```

**Worked example.** A 10 A current (a kettle cable draws about this) at 1 cm from the wire:

- B = 2e-7 x 10 / 0.01 = 2e-4 T = 200 µT.

That is four times the Earth's field. At 2 cm it halves to 100 µT: the field of a wire falls as 1/r, slower than the 1/r³ of a magnet. That is why a compass near a cable carrying DC current points the wrong way, and why aircraft and ships keep compasses away from heavy wiring. (In a real kettle cable, the two conductors carry equal and opposite currents, and their fields almost cancel a few centimetres away. Good wiring practice uses this on purpose.)

### 2. Where the formula comes from: adding up pieces

Jean-Baptiste Biot and Félix Savart (1820) found the rule for the field of a *tiny piece* of wire. A piece of length dl carrying current I, seen from a point at distance s, contributes a field of size

```
dB = (mu0 / 4 pi) * I * dl * sin(angle) / s^2
```

where "angle" is between the piece and the line joining it to the point. To get the field of the whole wire, chop the wire into many pieces and add up their contributions. For a long straight wire the sum gives exactly mu0 I / (2 pi r). We will do this sum on a computer: it is the same "chop into small pieces and add" idea we used for the transient simulation of Phase 07 Lesson 08, now in space instead of time.

### 3. A single loop

At the centre of a circular loop of radius R:

```
B = mu0 * I / (2 R)
```

and along its axis, at distance z from the centre:

```
B = mu0 * I * R^2 / (2 (R^2 + z^2)^(3/2))
```

**Worked example.** R = 2 cm, I = 2 A, at the centre (z = 0): B = 1.2566e-6 x 2 / (2 x 0.02) = 6.28e-5 T = 62.8 µT. At z = 2 cm: R² + z² = 0.0004 + 0.0004 = 0.0008; (0.0008)^(3/2) = 2.263e-5; B = 1.2566e-6 x 2 x 0.0004 / (2 x 2.263e-5) = 22.2 µT. Far away (z much bigger than R) the formula becomes B = mu0 I R² / (2 z³), the 1/z³ of a magnet: **a current loop is a magnetic dipole** with moment m = I x (pi R²), current times area. That is the A·m² unit from Lesson 01.

### 4. The solenoid

Inside a long solenoid with N turns over a length l:

```
B = mu0 * n * I,     where n = N / l   (turns per metre)
```

"field equals the magnetic constant times the turns per metre times the current". The field does not depend on the coil's diameter, only on how tightly the turns are packed and how much current flows.

**Worked example.** 500 turns over 5 cm with 0.5 A:

- n = 500 / 0.05 = 10,000 turns per metre
- B = 1.2566e-6 x 10,000 x 0.5 = 6.28e-3 T = 6.28 mT.

That is a fridge-magnet-level field from a coil you could wind by hand. With an iron core and an effective mu_r of 100 (realistic once air gaps are included) it becomes 628 mT, a strong magnet. With mu_r = 1000 the formula would say 6.3 T, but iron saturates near 2 T, so you would never get it. Always check the answer against saturation.

**Ampere-turns.** Since B depends on N x I (through n), designers talk about **ampere-turns**: 500 turns at 0.5 A (250 A-turns) give the same field as 50 turns at 5 A. Many turns of thin wire need little current but have more resistance; few turns of thick wire need a lot of current. That trade-off shapes every coil.

### 5. The relay: an electromagnet in a circuit

A **relay** is an electromagnet that pulls a springy iron lever (the armature), which pushes a pair of contacts together. A small current through the coil switches a separate, possibly much larger, current through the contacts.

```
      control side                         load side
                                     contacts
   +24 V ---[ R1 ]---+               o----/ o------ to lamp, motor, heater
                     |                 ^
                   (coil)  ~~~~~~~~ pulls the lever
                     |
   0 V --------------+
```

At DC the coil is just its wire resistance: a length of copper wire, a resistor (Phase 03). A coil with **400 ohm** resistance that needs between **25 and 35 mA** to pull in reliably, from a **24 V** supply:

- Without any series resistor: I = 24 / 400 = 60 mA, almost twice the maximum: the coil gets hot and the extra current only wastes power.
- With a series resistor R1 the same current flows through R1 and the coil (series circuit, Phase 04), and I = 24 / (R1 + 400).
- For about 30 mA we need R1 + 400 = 24 / 0.03 = 800 ohm, so R1 = 400 ohm. The nearest standard value is 390 or 470 ohm.
- With 470 ohm: I = 24 / 870 = 27.6 mA. Inside the range.
- Power in R1: P = I² R = 0.0276² x 470 = 0.358 W. A quarter-watt resistor would overheat; use a half-watt one (Phase 03, Lesson 05).

In practice you buy a relay with a coil rated for your supply (a "24 V relay" already has the right resistance), but this calculation is exactly what the manufacturer did. In Lesson 05 you will see the other half of relay design: what happens to that coil's current when you switch it **off**.

## Build It

### Step 1: The wire formula

```python
MU0 = 4 * np.pi * 1e-7


def field_around_long_wire(current, distance):
    return MU0 * current / (2 * np.pi * distance)
```

Output: 20 µT for 1 A at 1 cm, 200 µT for 10 A at 1 cm, 100 µT at 2 cm, 400 µT for 100 A at 5 cm (a car starter cable, briefly).

### Step 2: Adding up tiny pieces (Biot-Savart)

```python
def biot_savart_straight_wire(current, distance, half_length, pieces):
    edges = np.linspace(-half_length, half_length, pieces + 1)
    centres = (edges[:-1] + edges[1:]) / 2
    piece_length = edges[1] - edges[0]
    r_squared = centres**2 + distance**2
    contributions = MU0 / (4 * np.pi) * current * piece_length * distance / r_squared**1.5
    return contributions.sum()
```

We chop a 2 m wire into pieces. For each piece, `distance / sqrt(r_squared)` is the sine of the angle, so `piece_length * distance / r_squared**1.5` is `dl * sin(angle) / s^2`. The output:

```
      10 pieces of a 2 m wire: B = 4.138 uT (formula 200.000 uT)
     100 pieces of a 2 m wire: B = 159.731 uT (formula 200.000 uT)
    1000 pieces of a 2 m wire: B = 199.990 uT (formula 200.000 uT)
```

With 10 pieces each is 20 cm long and their midpoints are all far from our point 1 cm away, so the sum misses the nearby wire that matters most: 4 µT, badly wrong. With 1000 pieces of 2 mm each the sum is right. The last 0.01 µT of difference is real physics: our wire is 2 m long, not infinite, and the formula is for an infinite wire.

### Step 3: A loop, with real vectors

```python
def biot_savart_loop_on_axis(current, radius, z, pieces):
    angles = np.linspace(0, 2 * np.pi, pieces, endpoint=False)
    step = 2 * np.pi / pieces
    positions = np.stack([radius * np.cos(angles), radius * np.sin(angles), np.zeros(pieces)], axis=1)
    pieces_dl = np.stack([-np.sin(angles), np.cos(angles), np.zeros(pieces)], axis=1) * radius * step
    point = np.array([0.0, 0.0, z])
    to_point = point - positions
    distances = np.linalg.norm(to_point, axis=1)[:, None]
    contributions = MU0 / (4 * np.pi) * current * np.cross(pieces_dl, to_point) / distances**3
    return contributions.sum(axis=0)[2]
```

Here each piece is a little arrow `dl` pointing along the wire, and the full Biot-Savart law uses the **cross product** `dl x s`, which automatically gives both the sin(angle) and the sideways direction. The sum matches the formula at every distance: 62.83 µT at the centre, 44.96 µT at 1 cm, 22.21 µT at 2 cm, 3.22 µT at 5 cm.

### Step 4: Solenoids and cores

```python
def solenoid_field(turns, length, current, relative_permeability=1.0):
    return relative_permeability * MU0 * (turns / length) * current
```

Output: 6.28 mT in air, 62.8 mT with mu_r = 10, 628.3 mT with mu_r = 100.

### Step 5: Forces

```python
def force_on_wire(field, current, length):
    return field * current * length


def force_per_metre_between_wires(current_a, current_b, separation):
    return MU0 * current_a * current_b / (2 * np.pi * separation)
```

5 cm of wire with 2 A in 0.2 T: F = 0.2 x 2 x 0.05 = 0.02 N = 20 mN, about the weight of a 2 g coin. Two wires 1 cm apart with 10 A each: 2 mN per metre. And the old ampere definition: 1 A, 1 A, 1 m apart gives 2.0e-7 N per metre.

### Step 6: Drive the relay coil with our simulator

```python
def relay_coil_current(supply_volts, series_ohms, coil_ohms):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", supply_volts)
    c.resistor("R1", "vcc", "coil", series_ohms)
    c.resistor("Rcoil", "coil", "0", coil_ohms)
    result = c.dc()
    return result.i("Rcoil"), result.v("coil"), result.p("R1")
```

The coil is modelled as its 400 ohm resistance, which is exactly what it is at DC. The script tries 100, 470 and 1000 ohm:

```
  24 V, series  100 ohm, coil 400 ohm: I =  48.0 mA, V_coil = 19.20 V, P_series =   230 mW -> out of range
  24 V, series  470 ohm, coil 400 ohm: I =  27.6 mA, V_coil = 11.03 V, P_series =   358 mW -> pulls in
  24 V, series 1000 ohm, coil 400 ohm: I =  17.1 mA, V_coil =  6.86 V, P_series =   294 mW -> out of range
```

Check 470 ohm by hand: 24 / 870 = 0.0276 A; V_coil = 0.0276 x 400 = 11.03 V.

## Use It

- **Relays.** A typical small signal relay such as the Omron G5V-1 in its 5 V version has a coil of roughly 170 ohm and draws about 30 mA; a 12 V automotive relay has a coil around 80 to 100 ohm. Datasheets give the *coil resistance*, the *must-operate voltage* (often 75% of nominal) and the *must-release voltage* (often 10%). A microcontroller pin (about 20 mA max) cannot drive most relay coils directly; a transistor does it (Phase 12).
- **Solenoid actuators** are coils with a movable iron plunger: door strikes, valve actuators in washing machines and coffee machines, pinball flippers.
- **Loudspeakers** put a coil in the gap of a permanent magnet, where F = B I L pushes the coil and the cone. With B = 1 T, a coil of 5 m of wire and 1 A, the force is 5 N.
- **Current sensing without touching.** Clamp meters measure the field around a wire to find the current in it without cutting the wire. B = 2e-7 I / r is the whole idea.
- **Electromagnetic interference.** Every wire with changing current makes a changing field, which can induce noise in nearby circuits (Lesson 03). Keeping the outgoing and return wires close together, so their fields cancel, is the first rule of low-noise wiring (Phase 21).

## Try It in the Lab

Open the lab task **"Pull in the relay without cooking its coil"**. A 24 V supply must drive a relay coil of 400 ohm, which needs 25 to 35 mA. Choose the series resistor from a drawer of four values. Before you run it, compute the current for each candidate by hand with I = 24 / (R + 400). Then think about the power the resistor must survive: which resistor gets hotter, the bigger or the smaller one, in this circuit? (The answer is not obvious: the current and the resistance change in opposite directions.)

## Common Mistakes

- **Using the left hand, or electron flow, with the grip rule.** The rule uses the right hand and conventional current.
- **Thinking the field points along the wire.** It circles around the wire. A compass next to the wire turns sideways.
- **Forgetting the return wire.** A real circuit always has current going and coming back. Two equal and opposite currents close together almost cancel each other's field.
- **Multiplying by a huge mu_r and ignoring saturation.** An iron core cannot exceed about 2 T, whatever the formula says.
- **Treating a coil as "just a wire" with no resistance.** A coil with hundreds of turns of thin wire has tens or hundreds of ohms. At DC, that resistance is what sets the current.
- **Choosing a resistor for current but forgetting its power.** Always check P = I² R against the resistor's rating.

## Exercises

1. **Easy.** Find the field 5 mm from a wire carrying 3 A. How far away do you need to be for the field to drop to Earth's 50 µT?
2. **Easy.** A solenoid has 200 turns over 4 cm and carries 1.2 A. Find n and B in air.
3. **Medium.** Two parallel wires 5 mm apart carry 20 A each, in opposite directions (a power cable's two conductors). Find the force per metre. Do they attract or repel?
4. **Medium.** A 12 V relay coil has 160 ohm and must-operate current of 50 mA, maximum 90 mA. You have a 15 V supply. Find the range of series resistors that works, pick a standard value (E12 series), and compute its power.
5. **Hard.** Modify `biot_savart_straight_wire` to compute the field at a point opposite the *end* of a wire instead of the middle. Show that it is half the infinite-wire value when the wire is long. Explain why using symmetry.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Electromagnet | "A magnet made with electricity" | A coil, usually on a ferromagnetic core, whose field exists only while current flows and is proportional to the ampere-turns until the core saturates |
| Right-hand grip rule | "Thumb and fingers" | Thumb along conventional current, fingers curl along B |
| Solenoid | "A coil" | A long, tightly wound coil; inside it B = mu0 n I, nearly uniform |
| Ampere-turns | "How strong the coil is" | N x I, the quantity that sets the field of a coil for a given geometry |
| Relative permeability | "How magnetic a core is" | mu_r, the factor by which a material multiplies the field; huge for iron, 1 for air, limited by saturation and gaps |
| Saturation | "The core is full" | The field above which a ferromagnetic material stops adding magnetisation |
| Biot-Savart law | "The wire field formula" | The rule for the field of each tiny piece of current; summing it gives the field of any wire shape |

## Further Reading

- [The Feynman Lectures on Physics, Vol. II, Chapter 13 (Magnetostatics) and Chapter 14 (The Magnetic Field in Various Situations)](https://www.feynmanlectures.caltech.edu/II_toc.html) — the field of wires, loops and solenoids from the ground up
- [All About Circuits, Volume I, Chapter 14: Magnetism and Electromagnetism](https://www.allaboutcircuits.com/textbook/direct-current/chpt-14/electromagnetism/) — a practical, circuit-oriented introduction
- [HyperPhysics: Magnetic field of a current loop and solenoid](http://hyperphysics.phy-astr.gsu.edu/hbase/magnetic/solenoid.html) — compact formula pages to check your numbers
- [Omron G5V-1 relay datasheet](https://omronfs.omron.com/en_US/ecb/products/pdf/en-g5v_1.pdf) — real coil resistance, must-operate and must-release values
