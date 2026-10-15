# The Vocabulary

> Twenty words carry ninety percent of electronics. Learn each one with a picture, and learn where the picture lies.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 00 (Words and Units), Lesson 01 (What Electronics Is)
**Time:** ~60 minutes

## Words You'll Meet

This whole lesson is a list of words, so the table is long. Skim it now; the sections below take each word slowly.

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| charge | The property of tiny particles that makes them push or pull on each other | The "stuff" that flows, like water in a pipe |
| voltage | The push on charge between two points (energy per unit of charge) | Water pressure, or the height difference of a waterfall |
| potential difference | Another name for voltage | Height difference between two places |
| current | How much charge flows past a point every second | How many litres per second flow through a pipe |
| resistance | How strongly a part opposes current | How narrow a pipe is |
| power | How fast energy is delivered or used | How fast a car burns fuel |
| energy | The total amount of work that can be done | The fuel in the tank |
| circuit | A closed loop that charge can travel round | A running track |
| source | A part that pushes charge and gives energy | A pump |
| load | A part that receives energy and turns it into light, heat or motion | A water wheel |
| wire | A conductor whose job is to connect, ideally with no effect of its own | A wide, short pipe |
| node | All the points joined by plain wire; they share one voltage | One pool of water at one level |
| branch | One path between two nodes, holding one part | One road between two towns |
| ground | The node we choose to call 0 volts | Sea level for measuring heights |
| short circuit | An accidental path with almost no resistance | A hole in a dam |
| open circuit | A break in the loop; no current can flow | A drawbridge left up |
| conductor | A material in which charge moves easily | A wide motorway |
| insulator | A material in which charge almost cannot move | A wall |
| component | One part you can buy and place in a circuit | A Lego brick |
| terminal | A spot on a component where a wire connects | A plug socket on the brick |
| polarity | Which terminal is + and which is - | Which end of a battery points where |

## Learning Objectives

- Give a plain-language meaning, a symbol and a unit for charge, voltage, current, resistance, power and energy
- For each word, describe an everyday picture and say clearly where that picture breaks down
- Explain the difference between voltage (between two points) and current (through a point), and why that difference matters when measuring
- Identify the source, load, nodes, branches and ground in a simple circuit like a flashlight
- Predict, in words and with rough numbers, what happens in a short circuit and in an open circuit

## The Problem

Imagine reading this sentence on a forum: "Your LED died because you shorted the 9 V source through it with no series resistor, so the current wasn't limited and it dissipated way too much power. Measure the voltage across it relative to ground next time."

To a beginner that is a wall of noise. Every important word in it (short, source, series, current, limited, power, voltage, across, ground) is one of the words in this lesson. Once you have them, the sentence becomes a precise and helpful explanation.

The words are also traps. Everyday English uses "power", "energy", "current" and "charge" loosely ("my phone has no charge", "the power is out", "this battery has more power"). In electronics each one means one exact thing, and mixing them up leads to wrong calculations. So for each word we will do three things: say what it means, give a picture, and then say what the picture gets wrong. A picture you know is wrong in a specific way is far more useful than one you trust blindly.

## The Physics

Phase 01 (The Physics Underneath) builds all of this from atoms upward. Here is the shortest possible version, enough to anchor the words.

Matter is made of atoms. Each atom has a small, heavy, **positively charged** centre and much lighter **negatively charged** electrons around it. Opposite charges attract, like charges repel. Normally the plus and minus balance out, so ordinary objects feel no electric push at all.

In a metal, some electrons are free to wander between atoms. A battery, through chemistry, piles up extra electrons at one terminal and takes them away from the other. The free electrons in a wire connected between the terminals feel the push and drift along. That drift is **current**. The strength of the push is the **voltage**. Whatever slows the drift is **resistance**. The energy that the push hands over along the way, per second, is **power**.

One historical quirk to know now. Benjamin Franklin, around 1747, had to choose which kind of charge to call "positive". He guessed, and by chance chose the opposite of what the moving particles turned out to be: J. J. Thomson discovered in 1897 that the movers in a wire are electrons, which carry **negative** charge. By then everybody drew currents flowing from + to -, so the convention stayed. In this course, as in every textbook, **current arrows point from + to - outside the source** ("conventional current"), and you should remember that the electrons themselves drift the other way. For almost every calculation it makes no difference. Phase 01, Lesson 06 shows why.

## The Concept

### Charge (symbol Q, unit coulomb, C)

**Plain meaning.** Charge is a property of particles, like mass is. It comes in two kinds, positive and negative. It makes particles push or pull on each other. An electron carries a tiny fixed amount of negative charge; a proton carries the same amount of positive charge.

**Unit.** The coulomb (C), named after Charles-Augustin de Coulomb, who measured electric forces in 1785. One coulomb is a lot of electrons: an electron's charge is 1.602 x 10^-19 C (that is 0.0000000000000000001602 C), so

```
   1 C / 1.602e-19 C per electron = 6.24e18 electrons
```

That is about six billion billion electrons. (Writing numbers like `6.24e18` for 6.24 x 10^18 is explained in Lesson 04.)

**Picture.** Charge is the water in a water circuit. A pipe full of water is like a wire full of free electrons.

**What the picture gets wrong.** Water can pour out of a broken pipe; charge cannot pour out of the end of a wire into the air (at normal voltages). And water has only one "kind", while charge has two that attract each other. Most importantly, in everyday speech "my phone is out of charge" is wrong: the phone contains just as much charge when it is flat. What it lacks is **energy**.

### Voltage (symbol V, unit volt, V)

**Plain meaning.** Voltage is the electrical push between two points. More exactly, it is how much energy each coulomb of charge gains or loses going from one point to the other. It is also called **potential difference**, because it is the difference in "electrical level" (potential) between two places.

**Unit.** The volt (V), named after Alessandro Volta. One volt means one joule of energy per coulomb of charge. An AA cell is about 1.5 V, a car battery about 12 V, a USB port 5 V, a European wall socket 230 V.

**Picture.** Height. A ball at the top of a 1.5 m shelf can give up more energy rolling down than a ball on a 0.5 m step. Voltage is the "height" for charge. A battery is a lift that carries charge up to the top of the shelf; the circuit is the slope it rolls back down.

**What the picture gets wrong.** Very little at this level, which is why we use it so much. The main trap is this: **voltage is always between two points**. "The voltage at this point" only makes sense if somebody has silently chosen a reference point to measure from (see **ground** below). Saying "this wire has 5 volts" is like saying "this shelf is 1.5 metres": 1.5 metres above what?

The water version of the picture, "voltage is water pressure", is also popular. It works well for pushing, and we use it in Phase 02, Lesson 05, which is entirely about where the water analogy works and where it fails.

### Current (symbol I, unit ampere, A)

**Plain meaning.** Current is the amount of charge flowing past a point each second. One ampere is one coulomb per second.

**Why "I"?** It comes from the French *intensité de courant*, the expression Ampère used. Do not let it confuse you: in formulas, **I always means current**.

**Unit.** The ampere (A), or "amp", named after André-Marie Ampère. A phone charging cable carries around 1-3 A, an LED about 0.02 A, a kettle about 10 A, a car starter motor a few hundred amps.

**Picture.** Flow rate of water in a pipe: litres per second through a given cross-section.

**What the picture gets wrong.** Water in a hose really moves fast; electrons in a wire move astonishingly slowly (fractions of a millimetre per second), yet a lamp lights instantly because the push travels along the wire almost at the speed of light. Think of a tube already packed with marbles: push one in at one end and one pops out of the other end at once, even though each marble barely moved.

**Voltage versus current.** This is the single most important distinction in the course:

```
   voltage is ACROSS something (between its two ends)
   current is THROUGH something (past one point of it)

           +---- V across the bulb ----+
           |                           |
   ----->--o-----------[ bulb ]--------o---->-----
         I flows through the bulb, the same on both sides
```

You can have voltage without current: a battery sitting in a drawer has 1.5 V between its terminals but no current, because there is no loop. You cannot have current through a simple part like a bulb without a voltage across it. When you measure later (Phase 02, Lesson 07), voltage is measured by touching two points, while current is measured by breaking the loop and letting the current pass through the meter.

### Resistance (symbol R, unit ohm, Ω)

**Plain meaning.** Resistance says how hard a part makes it for current to flow. For a given push, a part with more resistance lets less current through.

**Unit.** The ohm, written with the Greek capital omega, Ω, named after Georg Ohm, who in 1827 published that current is proportional to voltage for a given wire. A short copper wire might be 0.01 Ω, a flashlight bulb about 12 Ω when hot, a typical resistor from a kit 1000 Ω, and dry human skin from hand to hand something like 100 000 Ω.

As a preview that we will earn properly in Phase 03 (Resistance and Ohm's Law), these three are linked by

```
   current = voltage / resistance          I = V / R
```

Read aloud: "the current through a part equals the voltage across it divided by its resistance". For the flashlight, 3 V across a 12 Ω bulb gives

```
   I = 3 V / 12 Ω = 0.25 A
```

**Picture.** A narrow section of pipe, or a crowded corridor that people push through.

**What the picture gets wrong.** A narrow pipe's resistance depends on how fast water flows (turbulence); a plain resistor's does not, which is what makes resistors so useful. And the energy "lost" in a resistor is not lost: it becomes heat. That is exactly how a toaster, a kettle and an old-style light bulb work.

### Power (symbol P, unit watt, W) and energy (symbol E, unit joule, J)

These two are the most confused words in everyday English, so we take them together.

**Energy** is an amount: how much work is done, how much heat is made, how much is stored. Unit: the joule (J), named after James Prescott Joule. Lifting a 100 g apple by 1 m takes about 1 J.

**Power** is a rate: how much energy per second. Unit: the watt (W), named after James Watt; 1 W = 1 J per second. A phone charger delivers around 10-20 W, a kettle 2000 W.

```
   energy = power x time          E = P x t
```

Read aloud: "energy equals power times how long". And, as a preview from Phase 01, Lesson 07:

```
   power = voltage x current      P = V x I
```

For the flashlight, P = 3 V x 0.25 A = 0.75 W. In one hour (3600 s) that is E = 0.75 W x 3600 s = 2700 J.

**Picture.** Energy is the fuel in a car's tank; power is how fast the engine burns it. A big tank does not make a car faster; a powerful engine empties a small tank quickly.

**What the picture gets wrong.** Fuel visibly travels with the car; electrical energy is not carried *inside* the electrons like fuel in a tank. It is passed along by the push, through the fields around the wire (Phase 01 and Phase 08 make this precise). For now: say "power" when you mean a rate (watts), and "energy" when you mean an amount (joules). "This battery has more power" is almost always wrong: it has more **energy**.

### Circuit, source, load and wire

A **circuit** is a closed loop. Charge leaves the source, goes through one or more parts, and returns to the source.

A **source** pushes the charge round and provides the energy: a battery, a solar cell, a wall socket, a bench power supply.

A **load** receives energy and turns it into something else: light (lamp, LED), heat (heater, toaster), motion (motor), sound (speaker).

A **wire** connects things. An ideal wire has zero resistance and no voltage across it, no matter how much current it carries. Real wires come close enough that we ignore them almost always (Phase 03, Lesson 02 shows when you cannot).

```
         source                  load
        +------+               +------+
   +----| +  - |---------------|      |----+
   |    +------+               +------+    |
   |                                       |
   +---------------------------------------+
            the wires close the loop
```

**Picture.** A water pump (source) driving water round a closed loop of pipes through a water wheel (load).

**What the picture gets wrong.** In a water loop you can see the water, and if you cut the pipe water spills. In a circuit, if you cut the wire, nothing spills: current simply stops everywhere at once, all around the loop. Also, the source does not "send out charge" that the load "eats": the same charge goes round and round.

### Node and branch

A **node** is a set of points joined by plain wire. Because an ideal wire has no voltage across it, every point in a node is at the same voltage. A node is not a single dot: it is a whole connected piece of wire, however long and however many arms it has.

A **branch** is one path between two nodes, holding one component.

Here is the flashlight drawn as a circuit, with its nodes named:

```
         top                      top
     +---o------------------------o---+
     |                                |
   (+)                             [ bulb ]
  battery                             |
   (-)                                o strip
     |                                |
     |                             [switch]
     |                                |
     +---o------------------------o---+
        gnd                      gnd
```

- **Node `top`**: the + terminal of the battery and the top of the bulb, and the wire joining them.
- **Node `strip`**: the bottom of the bulb and one side of the switch.
- **Node `gnd`**: the other side of the switch and the - terminal of the battery.

Three nodes, three branches (battery, bulb, switch). Notice that the two `top` dots drawn on the schematic are the *same* node, because they are joined by a wire. Counting nodes correctly is the first step of every circuit analysis in Phase 04 (Kirchhoff's Laws).

**Picture.** A node is a lake: wherever you dip a measuring stick, the water surface is at the same height. A branch is a river between two lakes.

**What the picture gets wrong.** A real lake has waves and currents; an ideal node is perfectly flat. Real wires do have a tiny resistance, so a node is "flat" only to a very good approximation.

### Ground

**Ground** is the node we choose to call 0 V. Since voltage is always between two points, we need a reference, and ground is it. When someone says "the voltage at node top is 3 V", they mean "3 V between node top and ground".

In the flashlight we choose the battery's - terminal as ground. Then, with the switch closed:

```
   top   = 3.0 V  (the battery lifts it 3 V above gnd)
   strip = 0.0 V  (joined to gnd through the closed switch)
   gnd   = 0.0 V  (by choice)
```

So the whole 3 V appears across the bulb, from `top` to `strip`.

The word comes from early telegraph systems, which literally used the earth as the return path. In mains wiring, "earth" or "ground" still means a real connection to a metal rod in the soil, for safety. In a battery gadget, "ground" is just the chosen reference; nothing touches the earth.

**Picture.** Sea level. Mountain heights are measured from sea level not because the sea is special, but because everyone agreed on it.

**What the picture gets wrong.** Sea level is a single global choice; ground is chosen per circuit, and you may choose any node. Changing your choice of ground changes every "voltage at a node" number by the same amount, but it never changes any voltage *between* two nodes, which is what physically matters. Phase 01, Lesson 04 returns to this.

### Short circuit and open circuit

An **open circuit** is a break in the loop: a switch turned off, a wire cut, a bulb filament burnt through. No current flows anywhere in the loop. But the voltage does not vanish: the whole push of the source appears across the gap. With the flashlight switch open:

```
   current          = 0 A
   voltage at top   = 3 V
   voltage at strip = 3 V  (no current, so the bulb takes no voltage)
   across the gap   = 3 V - 0 V = 3 V
```

That is why an "off" light switch at home can still give you a shock: the full mains voltage sits across its open contacts.

A **short circuit** ("a short") is a path with almost no resistance, usually by accident: a loose wire touching the two terminals of a battery, a screwdriver slipping across a circuit board. Current takes the easy path, and since there is almost no resistance to limit it, the current becomes huge.

Real batteries have a small resistance inside them (Phase 06, Lesson 02). Say the flashlight's battery has 0.2 Ω inside. Normally the current is

```
   I = 3 V / (12 Ω + 0.2 Ω) = 3 / 12.2 = 0.246 A
```

If a wire shorts across the bulb, only the 0.2 Ω is left:

```
   I = 3 V / 0.2 Ω = 15 A
```

Sixty-one times more current. The voltage lost inside the battery is 15 A x 0.2 Ω = 3 V, so the power turned into heat *inside the battery* is 3 V x 15 A = 45 W. That is like a small soldering iron, inside a sealed cell. Batteries get hot, swell, leak or (with lithium cells) catch fire. Phase 02, Lesson 03 is about exactly this.

**Picture.** Open: a drawbridge left up. Short: a hole punched in the dam, so all the water rushes through the hole and none goes through the turbine.

**What the picture gets wrong.** A real dam's hole lets water out of the system; a short is still part of the loop. And "short" says nothing about length: a short circuit can be a long wire; what makes it "short" is that it bypasses the load.

### Conductor and insulator

A **conductor** is a material in which charge moves easily: metals (copper, aluminium, silver, gold), salty water, the human body to some extent. An **insulator** is a material in which charge almost cannot move: plastic, glass, rubber, dry wood, air (at normal voltages).

A copper wire is a conductor wrapped in an insulator (the plastic sleeve) so that the current goes where we want and nowhere else.

**Picture.** A conductor is a motorway, an insulator a solid wall.

**What the picture gets wrong.** It is not black and white. Resistance of materials spans more than twenty powers of ten (Phase 01, Lesson 05), with **semiconductors** like silicon in the middle, and any insulator breaks down if the voltage is high enough: lightning goes through air.

### Component, terminal and polarity

A **component** is one part you can buy: a battery, a resistor, an LED, a switch, a capacitor, a chip. Each has **terminals**, the metal points where you connect wires. A resistor has two, a transistor three, a chip may have hundreds.

**Polarity** says which terminal is which, when it matters. A resistor has no polarity: you can put it in either way round. A battery has polarity (+ and -), and so do LEDs, many capacitors and almost every chip. Putting a polarised part in backwards is one of the commonest beginner mistakes: an LED simply stays dark, but some capacitors can burst.

**Picture.** Lego bricks with studs; polarity is like a USB-A plug, which only fits one way round.

**What the picture gets wrong.** A USB-A plug physically refuses to go in wrongly; most electronic parts with polarity will happily go in backwards. Nothing stops you except reading the markings.

### Putting it all together: the flashlight in our new words

> The **circuit** is a closed loop of **wire**. The **source** is a 3 V **battery** whose **polarity** is marked + and -. The **load** is a bulb with a **resistance** of 12 Ω when hot. Taking the battery's - **terminal** as **ground**, there are three **nodes**: `top` at 3 V, `strip` and `gnd` at 0 V. The **voltage** across the bulb is 3 V, so a **current** of 0.25 A flows through it, and it turns **power** of 0.75 W into light and heat. In an hour that is 2700 J of **energy** and 900 C of **charge** passing round the loop. Opening the switch makes an **open circuit**; a wire across the bulb makes a **short circuit**.

Where does 900 C come from? Current is charge per second, so

```
   charge = current x time = 0.25 A x 3600 s = 900 C
```

and the number of electrons is

```
   900 C / 1.602e-19 C = 5.6e21 electrons
```

about five and a half thousand billion billion electrons passing each point of the loop in an hour, while each one creeps along at less than a millimetre per second.

## Build It

The program prints the glossary, quizzes you on four words, describes the flashlight with nodes and branches, and computes the numbers from above. Run it from the repository root:

```
uv run python phases/00-words-and-units/02-the-vocabulary/code/main.py
```

### Step 1: The glossary

Each entry is a tuple `(word, symbol, unit, meaning)`, printed as a table.

```python
GLOSSARY = [
    ("charge", "Q", "coulomb (C)", "the property that makes particles push or pull on each other"),
    ("voltage", "V", "volt (V)", "the push on charge between two points: energy per charge"),
    ("current", "I", "ampere (A)", "how much charge flows past a point each second"),
    ...
]
```

### Step 2: Quiz yourself

A random generator with a fixed seed picks four entries, so the output is the same each time you run it. Change the seed to get different questions.

```python
rng = np.random.default_rng(7)
picks = rng.choice(len(GLOSSARY), size=4, replace=False)
```

### Step 3: The flashlight as parts and nodes

Each part lists its two terminals and the node each one touches. The function `nodes_of` collects the distinct nodes.

```python
FLASHLIGHT_PARTS = [
    ("battery", "source", "plus", "top", "minus", "gnd"),
    ("bulb", "load", "a", "top", "b", "strip"),
    ("switch", "control", "a", "strip", "b", "gnd"),
]
```

It prints `3 nodes, 3 branches`. This "list of parts and the nodes they touch" is called a **netlist**, and it is exactly how our simulator will describe circuits from Phase 05 on. Lesson 05 of this phase reads one.

### Step 4: The numbers

```python
def flashlight_state(battery_volts, bulb_ohms, switch_closed, internal_ohms=0.0, bulb_shorted=False):
    load_ohms = 0.0 if bulb_shorted else bulb_ohms
    if not switch_closed:
        return {"current": 0.0, "top": battery_volts, "strip": battery_volts, "across_switch": battery_volts}
    current = battery_volts / (internal_ohms + load_ohms)
    top = battery_volts - current * internal_ohms
    return {"current": current, "top": top, "strip": 0.0, "across_switch": 0.0}
```

It prints 0.25 A, 0.75 W, 2700 J, 900 C and 5.617e+21 electrons.

### Step 5: Open and short

With the switch open: 0 A and 3 V across the gap. With a 0.2 Ω battery: 0.246 A normally, 15 A with the bulb shorted, and 45 W of heat inside the battery. Try `internal_ohms = 0.05`, closer to a fresh alkaline AA, and see the short-circuit current climb to 60 A (a real cell cannot quite deliver that, which is a first hint that our simple model has limits).

## Use It

These words appear on every label and datasheet you will ever read:

- **On a battery:** "1.5 V" is its voltage; "2500 mAh" is a charge (Lesson 03 explains the unit); "+" and "-" mark its polarity.
- **On a phone charger:** "Input 100-240 V ~ 0.3 A" (what it takes from the mains), "Output 5 V ⎓ 2 A" (what it gives). The wavy `~` means alternating current and the `⎓` symbol means direct current.
- **On a light bulb box:** "7 W (equivalent to 60 W)" is power: the LED bulb uses 7 J per second to give about as much light as a 60 W filament bulb.
- **On an electricity bill:** "kWh" (kilowatt-hours) is energy, not power. You pay for energy.
- **On a resistor:** coloured bands give its resistance (Phase 03, Lesson 04).
- **On a circuit board:** a printed "GND" marks the ground node, often a large copper area.

## Common Mistakes

- **"The voltage through the bulb."** Voltage is *across* (between two points); current is *through*. Saying it right makes you measure it right.
- **"My phone has no charge."** It has no stored energy left. Its charge (the count of electrons and protons) is unchanged.
- **"More power" for "more energy".** A 100 Wh power bank does not have more *power* than a 50 Wh one; it stores more energy.
- **Forgetting the reference.** "This pin is at 5 V" is meaningless without a ground. Always ask "measured from where?".
- **Treating two dots on a drawing as two nodes.** If plain wire joins them, they are one node, however far apart they are drawn.
- **Thinking an open switch has no voltage.** It has no current. The voltage across an open gap is often the largest voltage in the circuit.
- **Thinking a short is "short".** A short circuit is any path that bypasses the load with very little resistance, whatever its length.
- **Mixing up conventional current and electron flow.** Arrows in schematics point from + to - outside the source; electrons drift the other way. Both describe the same physical event.

## Exercises

1. **Easy.** For each quantity give its symbol and unit: charge, voltage, current, resistance, power, energy.
2. **Easy.** A 9 V battery is connected to a 450 Ω resistor. Using the preview I = V / R, what is the current? What is the power, using P = V x I? (Answer: 0.02 A, 0.18 W.)
3. **Medium.** Draw a circuit with one battery and two bulbs side by side, each bulb connected directly across the battery terminals. How many nodes are there? How many branches? (Answer: 2 nodes, 3 branches.)
4. **Medium.** An LED carries 0.02 A for 10 minutes. How much charge passes through it? How many electrons is that? (Answer: 12 C, about 7.5 x 10^19 electrons.)
5. **Hard.** A 12 V car battery has about 0.01 Ω of resistance inside it. A spanner accidentally shorts its terminals. Estimate the current and the power turned into heat. Why do mechanics take off their wedding rings before working on cars? (Answer: about 1200 A and 14 400 W; a metal ring across the terminals becomes a red-hot short in a second.)

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| charge | "battery level" | A property of particles, measured in coulombs; it is not used up in a circuit |
| voltage | "the electricity at this point" | The energy per coulomb between two points; always needs a reference |
| current | "the electricity flowing" | Charge per second through a point, in amperes |
| resistance | "what slows electricity down" | Volts needed per amp of current through a part, in ohms |
| power | "how much energy something has" | Energy per second, in watts |
| energy | "power" | Power x time, in joules (or Wh, kWh) |
| node | "a dot on the diagram" | Everything connected by plain wire; one voltage |
| ground | "the earth" | The node chosen as 0 V; only sometimes really connected to the earth |
| short circuit | "a short wire" | A very low-resistance path that bypasses the load |
| open circuit | "the circuit is off" | A break in the loop: zero current, but voltage can appear across the gap |
| polarity | "which way up" | Which terminal is + and which is -; it matters for batteries, LEDs, many capacitors |

## Further Reading

- [All About Circuits, Volume I (DC), Chapter 1: "Voltage and Current"](https://www.allaboutcircuits.com/textbook/direct-current/chpt-1/voltage-current/) — a careful beginner treatment of the two most important words.
- [Khan Academy, Electrical engineering: Introduction to electricity](https://www.khanacademy.org/science/electrical-engineering/introduction-to-ee) — short videos on charge, current, voltage and resistance.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors* (4th ed.), Chapter 2 — each of these quantities with practical examples.
- Richard Feynman, *The Feynman Lectures on Physics*, Volume II, Chapter 1 (free at [feynmanlectures.caltech.edu](https://www.feynmanlectures.caltech.edu/II_01.html)) — for later: how big electric forces really are, and why matter is usually neutral.
