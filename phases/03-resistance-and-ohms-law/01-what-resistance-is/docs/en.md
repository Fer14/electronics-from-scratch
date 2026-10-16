# What Resistance Is

> Electrons do not flow through a wire like water through an empty pipe. They stumble through a forest of atoms, and resistance is the price of every bump.

**Type:** Learn
**Prerequisites:** Phase 01 (The Physics Underneath), especially Lesson 06 (Energy, Potential and Voltage) and Lesson 08 (Current as Moving Charge); Phase 02 (Your First Circuits)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Resistance | How hard a piece of material makes it for current to flow through it | How narrow and crowded a corridor is |
| Ohm (Ω) | The unit of resistance: 1 ohm lets 1 amp flow when you push with 1 volt | A "difficulty score" for a path |
| Lattice | The orderly, repeating grid that the atoms of a solid sit in | Rows of seats in a stadium |
| Free electron | An electron that is not tied to one atom and can wander through the metal | A fan who left their seat and walks the aisles |
| Thermal motion | The fast, random jiggling every particle has just because the material is warm | People milling around randomly in a crowd |
| Drift | The slow average movement of electrons in one direction, on top of the random jiggling | The whole crowd slowly shuffling towards one exit |
| Drift speed | How fast that slow average movement is | How many meters per minute the crowd moves towards the exit |
| Collision (scattering) | An electron bumping into a vibrating atom or an impurity and losing its direction | Bumping into someone and having to start walking again |
| Mean free time | The average time an electron travels between two collisions | How long you can walk before bumping into somebody |
| Conductance | The opposite of resistance: how easily current flows, measured in siemens (S) | How wide and empty the corridor is |
| Resistor | A part made on purpose to have a known resistance | A turnstile placed on purpose to slow people down |

## Learning Objectives

- Describe, in your own words, what happens to an electron inside a metal wire when a voltage is applied
- Explain why electrons drift slowly (fractions of a millimeter per second) even though a lamp lights up instantly
- Define resistance as "volts needed per amp of current" and use the ohm as a unit
- Explain why the collision picture predicts that current is proportional to voltage
- Name the things that make resistance bigger: fewer free electrons, more collisions, a longer or thinner path
- Estimate the conductivity of copper from the number of free electrons and the time between collisions

## The Problem

In Phase 02 you built your first circuits: a battery, a wire, a lamp, a switch. You learned that you need a closed loop for current to flow, and that a "short circuit" (a plain wire straight across the battery) is dangerous. But why is it dangerous? Why does a lamp limit the current while a wire does not? Why does a thin wire get hot and a thick one stays cool? Why does a 9 V battery not hurt you when you touch both terminals, but a wall socket can kill you?

All of these questions have the same answer: **resistance**. Every material, and every object made of it, makes it more or less hard for charges to move through it. That difficulty decides how much current flows for a given push (voltage). If you do not know how to think about resistance, you cannot predict anything about a circuit. You would not know whether your LED will glow or burn, whether a wire will melt, or whether your battery will last a day or a minute.

This lesson is about what resistance *is*, physically. We will not use any formula as a black box. We will look inside a copper wire, watch electrons bumping into atoms, and see the idea of resistance appear on its own. The next lessons turn this picture into the tools you will use every day: resistivity (Lesson 02), Ohm's law (Lesson 03) and real resistors (Lesson 04).

## The Physics

### A quick reminder of what you already know

From Phase 01 you know three things:

1. **Charge** is a property of particles. Electrons carry a tiny negative charge, about 1.6 × 10⁻¹⁹ coulombs (C). One coulomb is the charge of about 6.24 × 10¹⁸ electrons.
2. **Voltage** (V, measured in volts) is the energy each coulomb of charge gains or loses when it moves between two points. A 9 V battery gives every coulomb that goes around the loop 9 joules of energy. Voltage creates an **electric field** inside the wire, and that field pushes on the charges.
3. **Current** (I, measured in amperes or "amps", A) is how much charge passes a point every second. 1 A means 1 coulomb per second.

What we did not answer is: **if the field pushes the electrons, why don't they go faster and faster forever?** A force on a free object makes it accelerate. A ball rolling down a smooth slope keeps speeding up. If electrons in a wire behaved like that, the current would grow without limit as soon as you connected a battery. That does not happen. The current settles at a fixed value almost instantly. Something is holding the electrons back.

### Inside a metal: a stadium full of people

A piece of copper is made of copper atoms packed in a regular, repeating 3-D grid called a **lattice**. Think of a stadium where every seat is an atom. Each copper atom gives away one of its outer electrons to the whole metal. Those electrons are **free electrons**: they are not attached to any particular atom, they wander through the whole lattice. That is exactly why copper is a conductor (Phase 01, Lesson 07).

There are a lot of them. In copper there are about 8.5 × 10²⁸ free electrons in every cubic meter. Written out, that is 85 000 000 000 000 000 000 000 000 000 electrons per cubic meter. In a single cubic millimeter of copper there are 8.5 × 10¹⁹ of them.

These free electrons are not sitting still. Because the metal is at room temperature, they rush around randomly at enormous speeds, about a million meters per second. This is **thermal motion**. But the motion is random: for every electron going left there is one going right. On average, nothing goes anywhere. No current.

```
   no voltage applied: random motion, no net flow

    o  ->     <-  o     o ^       o  ->
       o  v    o ->        <- o      o v
    <- o     o ^      o ->     v o
                                         average movement = 0
```

### Switching on the field

Now connect a battery across the wire. The voltage creates an electric field along the wire. The field pushes every free electron a little in the same direction (towards the + terminal, since electrons are negative). Each electron now has two motions on top of each other:

- the huge random thermal motion, in all directions;
- a small extra push, always the same way.

If that were all, the extra push would keep adding up and electrons would accelerate forever. But they cannot travel far. Every so often an electron **collides** with something:

- an atom of the lattice that is vibrating because of heat (the warmer the metal, the more the atoms shake);
- an impurity, a foreign atom that does not fit the grid;
- a defect, a missing atom or a boundary between crystal grains.

After a collision the electron flies off in a random new direction. It "forgets" the speed it had built up in the direction of the field. Then the field starts pushing it again from scratch, until the next collision.

```
   field pushes to the right  ===>

   electron path (zig-zag, but slowly creeping right):

   start *--.        .--*         .---*        .---* ...
             \      /    \       /     \      /
              *----*      *-----*       *----*
                 bump        bump          bump

   each "*" is a collision; between bumps the field speeds it up a little
```

The average time between two collisions is called the **mean free time**, written τ (the Greek letter "tau"). In copper at room temperature it is about 2.5 × 10⁻¹⁴ seconds: 25 femtoseconds. That is an absurdly short time. In one second an electron collides about 40 trillion times.

### Drift: the slow creep

Average over all the electrons and all the collisions, and the random part cancels. What is left is a slow, steady movement in one direction: the **drift**. Its speed is the **drift speed**.

How fast is it? Let us compute it for a normal case. Take a copper wire with a cross-section of 1 square millimeter (1 mm², roughly a household lamp cable) carrying 1 A.

Current is charge per second. The charge that passes a cross-section each second is:

> (number of free electrons per cubic meter) × (charge of each electron) × (area of the cross-section) × (drift speed)

Read it as a sentence: imagine the electrons all moving at the drift speed. In one second, the ones within one "drift speed" distance of the cross-section pass through it. That slice has a volume of area × drift speed. Multiply by how many electrons fit in each cubic meter and by the charge of each one, and you get coulombs per second, which is amps.

In symbols, with *n* the electrons per cubic meter, *e* the charge of one electron, *A* the area and *v* the drift speed:

```
I = n × e × A × v       so       v = I / (n × e × A)
```

Now the numbers:

```
n = 8.5 × 10^28   electrons per m^3
e = 1.602 × 10^-19 C
A = 1 mm^2 = 1 × 10^-6 m^2      (1 mm = 10^-3 m, so 1 mm^2 = 10^-6 m^2)
I = 1 A

n × e × A = 8.5e28 × 1.602e-19 × 1e-6 = 13 617   (coulombs per meter of wire)
v = 1 / 13 617 = 7.34 × 10^-5 m/s = 0.073 mm/s
```

Less than a tenth of a millimeter per second. A snail is about a hundred times faster. An electron at 1 A needs almost four hours to drift one meter along the wire.

### Then why does the lamp light instantly?

This surprises everybody. The answer: the wire is **already full** of free electrons, from end to end. When you close the switch, the electric field spreads along the whole wire at nearly the speed of light, and *every* electron in the loop starts drifting at the same moment. The lamp filament's own electrons start moving immediately. You do not have to wait for "the electrons from the battery" to arrive.

A good picture is a bicycle chain. When you push the pedal, the back wheel turns immediately, even though each link of the chain moves slowly. Energy travels fast; the individual links (electrons) move slowly.

### Where the energy goes

Each time an electron is pushed by the field, it gains a little energy. Each time it collides with a vibrating atom, it hands that energy to the atom, which vibrates more. More vibration means a hotter material. That is why **current flowing through a resistance always produces heat**. A toaster, an electric heater, an incandescent bulb, a warm phone charger: all of them are electrons bumping into lattices. We come back to this in Lesson 05 (Power and Heat).

## The Concept

### Resistance: how many volts per amp

Here is the key experimental fact, and the collision picture explains it: **for most materials, if you double the voltage, the current doubles.** Triple the voltage, triple the current. Current is proportional to voltage.

Why? Look at a single electron between two collisions. The field gives it a push proportional to the voltage. It has (on average) the same time τ to speed up before the next bump wipes out its gain. So the extra speed it builds up, on average, is proportional to the push. Double the push, double the average extra speed, double the drift, double the current. The time between collisions does not depend on the push, because the thermal motion (about a million m/s) is enormously faster than the drift (a fraction of a mm/s); the field hardly changes how often electrons bump into things.

So for a given object, the ratio "voltage divided by current" stays the same no matter how hard you push. That ratio is a property of the object. We call it its **resistance**, with the symbol **R**:

> Resistance is the voltage you need across an object for each ampere of current you want through it.

```
R = V / I
```

Read it as: "resistance equals voltage divided by current". If you apply 6 V and measure 2 A, the object needs 3 volts for every amp: its resistance is 3 ohms.

### The ohm

The unit of resistance is the **ohm**, written with the Greek capital letter omega, **Ω**, and named after Georg Ohm, who measured this proportionality in the 1820s.

> 1 ohm is the resistance of an object that lets 1 ampere flow when 1 volt is applied across it.

```
1 Ω = 1 V / 1 A
```

The SI prefixes from Phase 01 (Lesson 01) apply:

| Written | Spoken | Value | Where you meet it |
|---|---|---|---|
| 10 mΩ | 10 milliohms | 0.010 Ω | a short piece of thick wire, a fuse |
| 1 Ω | 1 ohm | 1 Ω | a loudspeaker coil is 4 or 8 Ω |
| 470 Ω | 470 ohms | 470 Ω | an LED's current-limiting resistor |
| 10 kΩ | 10 kilohms | 10 000 Ω | a common "pull-up" resistor |
| 1 MΩ | 1 megohm | 1 000 000 Ω | dry skin, hand to hand (very roughly) |
| 10 MΩ | 10 megohms | 10 000 000 Ω | the input of a typical multimeter |

In schematics people often skip the Ω symbol: "4k7" means 4.7 kΩ, "1M" means 1 MΩ, "220R" means 220 Ω. The letter takes the place of the decimal point so a smudged dot cannot turn 4.7k into 47k.

### Worked example: measure, then divide

You put a mystery object across a 9 V battery and your multimeter (Phase 02, Lesson 07) says 9 mA (milliamps) flows.

```
Step 1: convert to base units     9 mA = 9 / 1000 A = 0.009 A
Step 2: divide                     R = V / I = 9 / 0.009 = 1000 Ω
Step 3: use a prefix               1000 Ω = 1 kΩ
```

The object is a 1 kΩ resistor. Check: 1000 Ω × 0.009 A = 9 V. Correct.

Another: a car headlight bulb on a 12 V battery draws 5 A.

```
R = 12 V / 5 A = 2.4 Ω
```

Notice how small it is. A headlight is a "heavy load": low resistance, lots of current.

### Conductance: the other way around

Sometimes it is easier to talk about how *easily* current flows. That is **conductance**, symbol **G**, the reciprocal of resistance:

```
G = 1 / R = I / V
```

Its unit is the **siemens** (S). A 1 kΩ resistor has a conductance of 1/1000 = 0.001 S = 1 mS (millisiemens). You will use conductance in Phase 05 when we solve circuits with nodal analysis, because conductances of parallel paths simply add.

### What makes resistance big or small

The collision picture tells us what controls resistance. For the same voltage, the current is smaller (resistance is bigger) when:

1. **There are fewer free electrons per cubic meter.** Fewer carriers, less charge moves. Insulators like glass have almost none: enormous resistance. Semiconductors have a few, metals have a lot.
2. **Electrons collide more often** (shorter mean free time). More impurities, more defects, or a hotter lattice that vibrates more. This is why most metals get *more* resistive when they heat up, and why alloys (mixtures of metals, like nichrome) resist more than pure metals.
3. **The path is longer.** The same voltage spread over twice the length gives a weaker field at each point: half the push, half the drift.
4. **The path is thinner.** A thinner wire has fewer electrons in each slice: less current for the same drift.

Points 1 and 2 are about the *material*. Points 3 and 4 are about the *shape*. Lesson 02 separates the two: the material gets a number called resistivity, and the shape enters through length and area.

### Copper's conductivity from first principles

We can turn the collision picture into an actual estimate. The material's ability to conduct (independent of shape) is the **conductivity**, σ (Greek "sigma"), measured in siemens per meter. A careful version of the argument above (it is called the Drude model) gives:

> conductivity = (free electrons per cubic meter) × (electron charge)² × (mean free time) ÷ (electron mass)

```
σ = n × e² × τ / m
```

Each factor makes sense: more electrons (n) means more carriers; charge appears twice, once because the field pushes harder on a bigger charge, once because each moving electron carries that charge; a longer time between bumps (τ) means more speed built up; a heavier particle (m) accelerates less for the same push.

For copper:

```
n = 8.5e28 /m^3      e = 1.602e-19 C      τ = 2.5e-14 s      m = 9.109e-31 kg

e^2        = 2.566e-38
n × e^2    = 2.181e-9
× τ        = 5.453e-23
÷ m        = 5.99e7 S/m
```

The measured value is 5.96 × 10⁷ S/m. Our simple picture of bumping electrons gets it essentially right. (To be honest, τ was chosen from measurements, so the agreement partly comes from that. The real triumph is that one picture explains the proportionality, the heating and the effect of temperature together.)

### What the analogy gets wrong

The stadium crowd is a helpful picture, but it has limits:

- Real electrons are quantum particles. A perfectly regular lattice at absolute zero would not scatter them at all; only vibrations and imperfections do. The crowd picture suggests every atom is an obstacle, which overestimates collisions.
- The "million meters per second" random speed in metals comes from quantum effects (the Pauli exclusion principle), not just temperature. It barely changes when the metal warms up.
- In a crowd, people choose where to walk. Electrons do not "want" anything; they respond to forces.

None of these change the main conclusions: current is proportional to the push, and collisions turn electrical energy into heat.

## Build It

The script `code/main.py` does four things. Run it from the repository root:

```
uv run python phases/03-resistance-and-ohms-law/01-what-resistance-is/code/main.py
```

### Step 1: How slowly electrons drift

```python
ELECTRON_CHARGE = 1.602e-19
COPPER_FREE_ELECTRONS_PER_M3 = 8.5e28


def drift_speed(current_amps, area_m2, electrons_per_m3=COPPER_FREE_ELECTRONS_PER_M3):
    return current_amps / (electrons_per_m3 * ELECTRON_CHARGE * area_m2)
```

This is exactly `v = I / (n e A)`. For 1 A in 1 mm² of copper it prints about 0.073 mm/s, and tells you that drifting one meter takes almost four hours. Change the area to 0.1 mm² (a thin wire) and the drift becomes ten times faster: the same current has to squeeze through fewer electrons.

### Step 2: A toy crowd of colliding electrons

```python
def simulate_average_drift(push, mean_free_time, steps=4000, dt=0.01, electrons=5000, seed=0):
    rng = np.random.default_rng(seed)
    velocity = rng.normal(0.0, 1.0, electrons)
    drift_history = []
    collision_probability = dt / mean_free_time
    for step in range(steps):
        velocity += push * dt
        collided = rng.random(electrons) < collision_probability
        velocity[collided] = rng.normal(0.0, 1.0, collided.sum())
        if step >= steps // 2:
            drift_history.append(velocity.mean())
    return float(np.mean(drift_history))
```

This is a tiny simulation in made-up units. 5000 electrons start with random velocities (the thermal motion, average zero). At every small time step `dt`:

- the field adds `push × dt` to every velocity (constant acceleration);
- each electron has a small chance `dt / mean_free_time` of colliding; a collided electron gets a fresh random velocity, forgetting what the field gave it.

We skip the first half of the run (while things settle) and average the velocity of all electrons over the second half. That average is the drift. The output shows:

```
mean free time 1.0  push 1.0 -> average drift  0.979   (prediction push x time = 1.000)
mean free time 1.0  push 2.0 -> average drift  1.965   (prediction push x time = 2.000)
mean free time 0.5  push 1.0 -> average drift  0.485   (prediction push x time = 0.500)
```

Two patterns:

- **Double the push, double the drift.** Since current is proportional to drift and push is proportional to voltage, current is proportional to voltage. That is Ohm's law appearing from nothing but random collisions.
- **Halve the time between collisions, halve the drift.** More collisions mean more resistance.

The small difference from the prediction (0.979 instead of 1.000) comes from the finite time step and the randomness; with smaller `dt` and more electrons it shrinks.

### Step 3: Resistance as volts per amp

```python
def resistance_from_measurement(volts, amps):
    return volts / amps
```

The script applies it to four made-up but realistic measurements, from a short copper wire (0.02 Ω) to dry skin (around 1 MΩ). Look at the range: about eight orders of magnitude. Electronics constantly deals with resistances from milliohms to megohms.

### Step 4: Copper's conductivity from collisions

```python
def conductivity_from_collisions(electrons_per_m3, mean_free_time):
    return electrons_per_m3 * ELECTRON_CHARGE**2 * mean_free_time / ELECTRON_MASS
```

It prints about 5.99 × 10⁷ S/m against the measured 5.96 × 10⁷ S/m, and the reciprocal, the resistivity 1.67 × 10⁻⁸ Ω·m, which is the number Lesson 02 starts from.

## Use It

- **Resistors** are components built to have a precise resistance: a film of carbon or metal alloy on a ceramic rod, with a spiral groove cut to make the path long and thin. Lesson 04 shows how to read their values.
- **Heating elements** (kettles, hair dryers, 3-D printer hot ends, toasters) use a nichrome alloy: lots of impurities and collisions, high resistance, good at turning current into heat, and it does not oxidise at red heat.
- **Fuses** are a short, thin piece of metal chosen so that too much current heats it until it melts and opens the circuit.
- **Strain gauges** in digital kitchen scales are thin metal patterns whose resistance rises slightly when they are stretched (longer and thinner path). You will meet them again in the Wheatstone bridge (Phase 04, Lesson 07).
- **Thermistors and RTDs** are temperature sensors that work because collisions depend on temperature. A platinum RTD (Pt100) is exactly 100 Ω at 0 °C and rises by about 0.385 Ω per degree.
- **Your body** has resistance too. Dry skin, hand to hand, is somewhere around 100 kΩ to 1 MΩ; wet skin can drop below 1 kΩ. That is why 9 V is harmless (9 V / 100 kΩ = 0.09 mA) but mains voltage on wet hands is deadly (Phase 00, Lesson 08).

## Common Mistakes

- **Thinking electrons from the battery have to "reach" the lamp.** They do not. The wire is full of electrons already. The field arrives almost instantly and all of them start drifting at once.
- **Thinking electrons race through wires.** Their drift is millimeters per minute or slower. What is fast is the field (the signal), not the charges.
- **Thinking resistance "uses up" current.** Current going into a resistor equals current coming out. Charge is not destroyed. What a resistor takes is *energy*: it turns electrical energy into heat. Voltage drops across it; current does not.
- **Mixing up resistance and resistivity.** Resistance (Ω) belongs to an object: this wire, this resistor. Resistivity (Ω·m, Lesson 02) belongs to a material: copper, nichrome.
- **Forgetting to convert milliamps to amps** before dividing. 9 V / 9 mA is 1000 Ω, not 1 Ω.
- **Assuming every object has a fixed resistance.** It works for metals at a fixed temperature. A lamp filament, a diode or an LED does not follow it (Lesson 07, When Ohm's Law Fails).

## Exercises

1. A toy motor connected to a 3 V battery draws 0.6 A while spinning. What resistance does it present? Give the answer in ohms.
2. You measure 120 µA (microamps) through an unknown part when 1.2 V is across it. What is its resistance, in kΩ? What is its conductance in siemens?
3. Compute the drift speed of electrons in a copper wire of cross-section 0.25 mm² carrying 2 A. How long does an electron take to drift 1 cm?
4. Using the collision picture, explain in three or four sentences why heating a copper wire raises its resistance.
5. (Harder) Aluminium has about 18.1 × 10²⁸ free electrons per cubic meter and a mean free time of about 0.8 × 10⁻¹⁴ s. Estimate its conductivity with σ = n e² τ / m and compare with copper. Which conducts better, and why, even though aluminium has more free electrons?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Resistance | "How much the part blocks the electricity" | The voltage needed per ampere of current through an object: R = V / I, in ohms |
| Ohm | "The resistance unit" | 1 Ω lets 1 A flow when 1 V is across it |
| Drift speed | "How fast electricity travels" | The slow average speed of the charges themselves, often well under 1 mm/s; the signal travels near light speed |
| Free electron | "The electricity inside the wire" | An electron not bound to one atom that can move through the metal and carry current |
| Collision / scattering | "Friction" | An electron bouncing off a lattice vibration or impurity and losing its direction, handing energy to the lattice as heat |
| Conductance | "Inverse resistance" | G = 1 / R, in siemens; how many amps you get per volt |
| Conductivity | "How good a conductor the material is" | σ, in siemens per meter: the material's property, independent of shape |

## Further Reading

- *Feynman Lectures on Physics*, Volume II (Feynman, Leighton, Sands), chapters on conductors and currents: a physicist's look at why charges move the way they do. Free online at feynmanlectures.caltech.edu.
- *All About Circuits*, Volume I (DC), chapter "Basic Concepts of Electricity": a gentle introduction to resistance and the ohm.
- *Practical Electronics for Inventors* (Scherz & Monk), chapter 2: resistance, resistivity and resistors from a practical point of view.
- Khan Academy, Electrical engineering: "Introduction to circuits and Ohm's law": short videos with worked examples.
