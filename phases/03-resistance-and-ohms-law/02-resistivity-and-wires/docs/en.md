# Resistivity and Wires

> Resistance belongs to an object; resistivity belongs to a material. Shape does the rest: longer means more, thicker means less.

**Type:** Build
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Lesson 01 (What Resistance Is); Phase 01 (The Physics Underneath), Lesson 02 (Scientific Notation and Orders of Magnitude)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Resistivity (ρ, "rho") | How strongly a *material* resists current, no matter what shape you make it | How dense a forest is, regardless of how big the forest is |
| Ohm-meter (Ω·m) | The unit of resistivity | A "difficulty per size" score |
| Cross-section | The shape you see if you cut the wire straight across | The slice of a salami |
| Cross-sectional area (A) | The size of that slice, in square meters or square millimeters | How many people fit side by side in a corridor |
| Gauge | A standard number that tells how thick a wire is | Shoe sizes for wire |
| AWG | American Wire Gauge, the gauge system used in the US and on most hobby wire; bigger number = thinner wire | Like golf scores: lower is "more" |
| Voltage drop | The part of the voltage that a wire "uses up" just carrying current | Pressure you lose in a long garden hose |
| Temperature coefficient (α) | How much a material's resistance changes per degree of temperature | How much slower a crowd moves when the room is hotter and everyone fidgets |
| Alloy | A metal made by mixing two or more metals | A recipe instead of a single ingredient |
| Nichrome | An alloy of nickel and chromium used for heating wire | The wire inside a toaster |
| Trace | A flat copper "wire" printed on a circuit board | A painted road on a map |

## Learning Objectives

- Separate the material part of resistance (resistivity) from the shape part (length and area)
- Use R = ρ L / A to compute the resistance of wires, traces and heating elements, with correct unit conversions
- Read an AWG wire table and explain why every 3 gauges halves or doubles the area
- Estimate the voltage lost in a long cable and decide whether a thicker wire is needed
- Compute how much heating wire to cut to get a given resistance
- Correct a copper resistance for temperature with R = R₀ (1 + α ΔT)

## The Problem

You want to power a 12 V LED strip on your balcony from a power supply inside the house, 10 meters away. You grab the thinnest wire in your drawer because it is easy to hide under the door. The strip lights, but it is dim at the far end and the wire is warm to the touch. Why? Because a wire is not a perfect conductor. It is a resistor too, a very small one, and when a lot of current flows through even a small resistance, part of your voltage is lost before it reaches the load, and that loss turns into heat in the wire.

The same question shows up everywhere: Which wire gauge do you need for a 3-D printer heated bed? How wide must a copper trace on a circuit board be to carry 2 A? How much nichrome wire do you cut to make a heater of exactly 20 Ω? Why are power lines made of aluminium and not copper?

To answer these we need to know how resistance depends on *what* the object is made of and *how big* it is. That is what this lesson is about.

## The Physics

In Lesson 01 we saw that resistance comes from free electrons bumping into the lattice. We listed four things that make it bigger: fewer free electrons, more frequent collisions, a longer path, and a thinner path. Let us look at the last two carefully, because they give us a formula.

### Longer wire, more resistance

Take a copper wire with a certain resistance. Now put an identical wire right after it, end to end, so the path is twice as long. The current has to get through the first wire *and then* through the second one. Each one needs the same voltage to push a given current through it. So to push that current through both, you need twice the voltage. Twice the voltage for the same current means twice the resistance.

```
    one piece:      o====R====o          needs V volts for I amps

    two pieces:     o====R====o====R====o   needs 2V volts for the same I amps
                    <------- twice as long ------->
```

From the electron's point of view: the battery's voltage is now spread over twice the length, so the electric field (volts per meter) is half as strong. Half the push, half the drift speed, half the current. Either way:

> Resistance is proportional to length.

### Thicker wire, less resistance

Now put two identical wires side by side, connected at both ends, so the path is twice as wide. Each wire carries its own current with the same voltage across it. Together they carry twice the current for the same voltage. Twice the current for the same voltage means half the resistance.

```
                  o====R====o
    side by side: |         |      same V, but two paths: 2 x I
                  o====R====o
```

Doubling the width is the same as doubling the cross-sectional area. From the electron's point of view: each slice of the wire now has twice as many free electrons, and at the same drift speed they carry twice the charge per second. So:

> Resistance is inversely proportional to cross-sectional area. (Double the area, half the resistance.)

### What is left: the material

Once length and area are taken out, what remains is a number that depends only on the material (and its temperature): how many free electrons it has and how often they collide. That number is the **resistivity**, written ρ (the Greek letter "rho"). Lesson 01 called its reciprocal the conductivity σ, so ρ = 1/σ. For copper we estimated ρ ≈ 1.67 × 10⁻⁸ Ω·m from the collision picture.

## The Concept

### The formula

Putting the three ideas together:

> The resistance of a uniform piece of material equals its resistivity times its length, divided by its cross-sectional area.

```
R = ρ × L / A

R  resistance, in ohms (Ω)
ρ  resistivity of the material, in ohm-meters (Ω·m)
L  length of the path the current travels, in meters (m)
A  cross-sectional area, in square meters (m²)
```

Check that the units work: Ω·m × m / m² = Ω. Good.

What does "1 Ω·m" mean? A cube of material 1 m on each side, with current flowing from one face to the opposite face, has L = 1 m and A = 1 m², so R = ρ. Resistivity is the resistance of a one-meter cube. That is huge for metals' standards, which is why metals have tiny resistivities.

### Unit conversions you will need every time

Wires are measured in millimeters, but the formula wants meters. This is where most mistakes happen, so be careful:

```
1 mm   = 0.001 m       = 10^-3 m
1 mm^2 = 0.001 m × 0.001 m = 0.000001 m^2 = 10^-6 m^2
1 µm   = 10^-6 m        (micrometer, used for copper thickness on boards)
```

A wire's area from its diameter *d*: the cross-section is a circle, and a circle's area is π times the radius squared. The radius is half the diameter:

```
A = π × (d / 2)^2
```

For a 1 mm diameter wire: A = 3.1416 × (0.5 mm)² = 3.1416 × 0.25 = 0.785 mm² = 0.785 × 10⁻⁶ m².

Note: **doubling the diameter quadruples the area** (2² = 4), and so divides the resistance by four.

### A table of resistivities

| Material | ρ at 20 °C (Ω·m) | Kind | Used for |
|---|---|---|---|
| Silver | 1.59 × 10⁻⁸ | best metal | contacts, special cables |
| Copper | 1.68 × 10⁻⁸ | metal | almost every wire and circuit board |
| Gold | 2.44 × 10⁻⁸ | metal | connector plating (does not corrode) |
| Aluminium | 2.65 × 10⁻⁸ | metal | power lines, cheap house wiring in some countries |
| Tungsten | 5.6 × 10⁻⁸ | metal | lamp filaments (very high melting point) |
| Iron | 9.7 × 10⁻⁸ | metal | |
| Nichrome | 1.10 × 10⁻⁶ | alloy | heating elements, foam cutters |
| Graphite (carbon) | about 3.5 × 10⁻⁵ | in between | carbon resistors, pencil lines |
| Pure silicon | about 2.3 × 10³ | semiconductor | the base of chips (Phase 11) |
| Glass | 10¹⁰ to 10¹⁴ | insulator | |
| PTFE (Teflon) | about 10²³ | insulator | high-quality wire insulation |

Look at the range: from 10⁻⁸ to 10²³, about 31 orders of magnitude. No other everyday physical property varies that much between materials. This is why it is so easy to make wires (copper inside) with insulation (plastic outside) that keeps the current exactly where we want it.

Notice also: nichrome resists about 65 times more than copper. That is on purpose. Its mix of nickel and chromium atoms is a messy lattice, so electrons collide constantly. Lots of heat in a small piece of wire.

Values from semiconductors and insulators depend strongly on purity and temperature; treat them as rough.

### Worked example 1: a piece of copper

How much resistance has 1 m of copper wire with 1 mm² cross-section?

```
ρ = 1.68 × 10^-8 Ω·m
L = 1 m
A = 1 mm^2 = 1 × 10^-6 m^2

R = 1.68e-8 × 1 / 1e-6 = 1.68e-2 Ω = 0.0168 Ω = 16.8 mΩ
```

Sixteen milliohms. Remember this number: one meter of 1 mm² copper is about 17 mΩ. You can scale it in your head: 2 m is 34 mΩ; 0.5 mm² is 34 mΩ per meter.

### Worked example 2: the extension cord

A 10 m extension cord has two conductors of 1.5 mm² copper. A heater draws 10 A through it. How many volts are lost in the cord?

The current goes out along one conductor (10 m) and comes back along the other (10 m). The path is **20 m**, not 10. People forget this constantly.

```
R = 1.68e-8 × 20 / 1.5e-6 = 0.224 Ω
```

The lost voltage is resistance times current (from R = V / I, so V = R × I; Lesson 03 makes this the star of the show):

```
V_lost = 0.224 Ω × 10 A = 2.24 V
```

On 230 V mains that is only 1 %, fine. On a 12 V system it would be almost 19 %: a disaster. **Low-voltage systems need thicker wires** for the same current, because the same volts lost are a much bigger fraction.

### Worked example 3: cutting heater wire

You need a 20 Ω heater made from nichrome wire of 0.4 mm diameter. How long a piece?

First the area:

```
A = π × (0.2 mm)^2 = 3.1416 × 0.04 mm^2 = 0.1257 mm^2 = 1.257 × 10^-7 m^2
```

Resistance per meter of this wire:

```
R per m = 1.10e-6 / 1.257e-7 = 8.75 Ω per meter
```

Turn the formula around to find length: from R = ρ L / A, multiply both sides by A and divide by ρ:

```
L = R × A / ρ = 20 × 1.257e-7 / 1.10e-6 = 2.285 m
```

Or simply: 20 Ω / 8.75 Ω per m = 2.29 m. About 2.3 meters.

### Worked example 4: a trace on a circuit board

Circuit boards (Phase 21) have copper sheets 35 µm thick (called "1 ounce copper"). A trace 0.25 mm wide and 50 mm long:

```
A = 0.25e-3 m × 35e-6 m = 8.75e-9 m^2
L = 0.050 m
R = 1.68e-8 × 0.050 / 8.75e-9 = 0.096 Ω  (96 mΩ)
```

Almost a tenth of an ohm. At 2 A that trace would drop 0.19 V and get noticeably warm. This is why power traces are drawn wide.

### Wire gauges: AWG

Nobody buys wire by its area in square meters. Wire is sold by **gauge**. The most common system for hobby electronics is the **American Wire Gauge (AWG)**. Two rules:

1. **A bigger AWG number means a thinner wire.** (Historically, the number counted how many times the wire was drawn through a die to make it thinner.)
2. **Every 3 gauges, the area halves** (or doubles, going down). Every 6 gauges, the diameter halves. So 3 gauges thinner means twice the resistance per meter.

The diameter in millimeters is defined by a formula:

```
d = 0.127 mm × 92^((36 - AWG) / 39)
```

Read it as: AWG 36 is 0.127 mm; going down 39 gauges multiplies the diameter by 92. You never need to memorize it, but the script uses it to build a table.

| AWG | Diameter (mm) | Area (mm²) | Copper, Ω per meter | Typical use |
|---|---|---|---|---|
| 10 | 2.59 | 5.26 | 0.0032 | heavy power, 30 A |
| 12 | 2.05 | 3.31 | 0.0051 | house circuits (US), 20 A |
| 14 | 1.63 | 2.08 | 0.0081 | house circuits (US), 15 A |
| 16 | 1.29 | 1.31 | 0.0128 | appliance cords |
| 18 | 1.02 | 0.82 | 0.0204 | lamp cords, small motors |
| 20 | 0.81 | 0.52 | 0.0325 | hobby power leads |
| 22 | 0.64 | 0.33 | 0.0516 | breadboard jumper wire |
| 24 | 0.51 | 0.20 | 0.0821 | network cable (Ethernet) |
| 26 | 0.41 | 0.13 | 0.131 | ribbon cable |
| 28 | 0.32 | 0.081 | 0.208 | ribbon cable, small signals |
| 30 | 0.25 | 0.051 | 0.330 | wire-wrap, tiny signals |

Outside the US, wire is usually sold directly by area: 0.75 mm², 1.5 mm², 2.5 mm². The idea is identical.

Ampere ratings like "AWG 14: 15 A" are about *heat*, not voltage drop: they say how much current the wire can carry before its insulation gets dangerously hot. Lesson 05 (Power and Heat) and Lesson 06 (Tolerances and Ratings) explain this.

### Temperature changes resistivity

In Lesson 01 we saw that a hotter lattice vibrates more, so electrons collide more often. For metals, resistivity grows almost in a straight line with temperature:

> The resistance at a new temperature equals the resistance at 20 °C, times (1 plus the temperature coefficient times how many degrees warmer it is).

```
R(T) = R₂₀ × (1 + α × (T - 20 °C))

α for copper ≈ 0.00393 per °C   (0.393 % per degree)
```

Example: a copper motor winding measures 10.000 Ω at 20 °C. At 100 °C:

```
R = 10.000 × (1 + 0.00393 × 80) = 10.000 × 1.3144 = 13.14 Ω
```

31 % more. This effect is useful: engineers estimate how hot a motor winding is by measuring its resistance. It is also why a tungsten lamp filament, which runs at about 2500 °C, has more than ten times more resistance when lit than when cold (Lesson 07).

Nichrome's α is about 0.0004 per °C, ten times smaller than copper's. That is another reason it is used for heaters: its resistance (and so its power) stays nearly constant as it heats up.

## Build It

Run:

```
uv run python phases/03-resistance-and-ohms-law/02-resistivity-and-wires/code/main.py
```

### Step 1: The resistivity table

```python
def wire_resistance(resistivity, length_m, area_m2):
    return resistivity * length_m / area_m2
```

This one line is the whole formula. The script loops over the materials and prints the resistance of a 1 m × 1 mm² piece of each. It also prints the ratio between the best insulator and the best conductor: about 6 × 10³⁰.

### Step 2: Change the shape, keep the material

The script computes four copper wires: 1 m × 1 mm² (16.8 mΩ), 2 m × 1 mm² (33.6 mΩ, double), 1 m × 2 mm² (8.4 mΩ, half), and 10 m × 0.5 mm² (336 mΩ, twenty times). Check each one against the two rules before reading the output.

### Step 3: Build the AWG table

```python
def awg_diameter_mm(gauge):
    return 0.127 * 92 ** ((36 - gauge) / 39)


def circle_area(diameter_m):
    return math.pi * (diameter_m / 2) ** 2
```

For each gauge, it computes diameter, area, and ohms per meter and per 100 m. Then it checks the "every 3 gauges halves the area" rule numerically: the average ratio is 2.005. The rule of thumb is not exact, because 92^(6/39) = 2.005, but it is close enough to do in your head.

### Step 4: Worked examples

The script repeats the extension cord (0.224 Ω, 2.24 V lost at 10 A), the circuit-board trace (96 mΩ), and the nichrome heater (8.75 Ω per meter; 2.285 m for 20 Ω). It uses the rearranged formula:

```python
def length_for_resistance(target_ohms, resistivity, area_m2):
    return target_ohms * area_m2 / resistivity
```

### Step 5: Temperature

```python
def resistance_at_temperature(resistance_at_20c, temperature_c, alpha=COPPER_TEMPERATURE_COEFFICIENT):
    return resistance_at_20c * (1 + alpha * (temperature_c - 20.0))
```

A 10 Ω copper coil goes from 8.43 Ω at −20 °C to 13.14 Ω at 100 °C.

## Use It

- **Choosing wire for a project.** For a 5 A, 12 V load 3 m away (6 m round trip), AWG 18 gives 6 × 0.0204 = 0.12 Ω, so 0.6 V lost (5 %). AWG 22 would give 0.31 Ω and 1.5 V lost (13 %): too much. Datasheets of wire manufacturers (e.g. Alpha Wire, Belden) list "ohms per 1000 ft" for every gauge; the values match our table.
- **USB cables.** A cheap USB cable with AWG 28 power wires of 1 m has 2 × 0.21 = 0.42 Ω. At 2 A it drops 0.83 V, and a phone sees only 4.2 V instead of 5 V, so it charges slowly. Good cables use AWG 20 or 24 for power.
- **Power lines.** Aluminium has 1.6 times the resistivity of copper but only about one third of the density. For the same resistance, an aluminium cable is about half as heavy, and much cheaper. Overhead lines are aluminium around a steel core.
- **Circuit boards.** PCB design tools have "trace width calculators" built on exactly R = ρ L / A plus a heating model. Phase 21 uses them.
- **Heaters and 3-D printers.** The hot end of a 3-D printer uses a ceramic cartridge with a resistive coil inside, typically 12 V 40 W or 24 V 40 W, which means 3.6 Ω or 14.4 Ω.
- **Four-wire measurement.** To measure a few milliohms, the resistance of your multimeter leads gets in the way. Precision instruments use separate wires for current and for voltage (Kelvin connection). You will see why in Phase 06.

## Try It in the Lab

The lab task "Cut the hot wire to the right length" gives you a 12 V battery and four pieces of 0.4 mm nichrome wire of different lengths. Each piece is shown as a resistor, with the resistance it really has (8.75 Ω per meter). A foam cutter needs a current between 1 A and 2 A: less and it will not melt the foam, more and the wire overheats and snaps.

Before you try parts at random, think: which way does the current change if the wire gets longer? Can you estimate the right resistance range first, and then pick the length?

## Common Mistakes

- **Forgetting the return path.** A cable from A to B and back is twice as long as the distance between A and B.
- **Mixing mm² and m².** 1 mm² is 10⁻⁶ m², not 10⁻³ m². Getting this wrong gives an answer a thousand times off.
- **Using diameter instead of area.** Doubling the diameter does not halve the resistance; it quarters it.
- **Reading AWG backwards.** AWG 30 is thinner than AWG 10. Bigger number, thinner wire, more resistance.
- **Thinking thick wire is only about current rating.** Even when a thin wire does not overheat, its voltage drop can starve a low-voltage load (USB, LED strips, motors on batteries).
- **Ignoring temperature.** A motor, a coil, or a lamp filament has a different resistance when hot than what your multimeter shows when it is cold.

## Exercises

1. What is the resistance of 5 m of copper wire with a 0.5 mm² cross-section? Give the answer in milliohms.
2. An aluminium wire and a copper wire have the same length and the same resistance. How many times larger must the aluminium wire's area be?
3. You run AWG 22 jumper wire (0.0516 Ω/m) 2 m to a load and 2 m back. The load draws 0.5 A. How many volts are lost in the wires? Is that acceptable for a 5 V circuit?
4. How long a piece of 0.4 mm nichrome wire (8.75 Ω/m) do you need for a heater of 12 Ω? And with 0.2 mm wire? (Hint: half the diameter.)
5. (Harder) A copper coil measures 40.0 Ω at 20 °C. After running for an hour it measures 46.3 Ω. Estimate its temperature using α = 0.00393 per °C.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Resistivity | "Resistance of the material" | ρ, in Ω·m: the resistance of a 1 m cube of the material; shape-free |
| R = ρL/A | "The wire formula" | Resistance grows with length and shrinks with area, scaled by the material's resistivity |
| Cross-sectional area | "Thickness" | The area of the slice perpendicular to the current, in m²; for round wire π d² / 4 |
| AWG | "Wire size" | A logarithmic scale: +3 gauges halves the area and doubles the resistance per meter |
| Voltage drop | "Losses in the cable" | The voltage across a wire's own resistance, R_wire × I, which the load never sees |
| Temperature coefficient | "Resistance changes with heat" | α: the fractional change in resistance per degree; about +0.4 %/°C for copper |
| Nichrome | "Heater wire" | Nickel-chromium alloy, ρ ≈ 65× copper, stable when hot, does not oxidize easily |

## Further Reading

- *The Art of Electronics*, 3rd edition (Horowitz & Hill), section 1.2: concise and practical.
- *Practical Electronics for Inventors* (Scherz & Monk), chapter 2 (resistivity, wire gauges and their tables).
- *All About Circuits*, Volume I (DC), chapter "Physics of Conductors and Insulators", sections on conductor size and specific resistance.
- Any manufacturer's wire data sheet (search "AWG copper wire resistance table", e.g. from Alpha Wire or Belden) to compare with the table your script printed.
