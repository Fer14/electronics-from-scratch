# Voltage and Volts

> Voltage is the push, measured as a height. And a height only means something once you say where you measure it from.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 00 (Meet Electricity), Lessons 02 (What a Circuit Is), 03 (Charge and Electrons) and 04 (Current and Amperes)
**Time:** ~50 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| voltage | The electrical push between two points: how much energy each bit of charge gains or gives up going from one point to the other | The height difference between the top and the bottom of a slide |
| volt (V) | The unit of voltage, named after Alessandro Volta | The "metres" of electrical height |
| potential difference | Another name for voltage, used in physics books | Difference in height between two places |
| across | Voltage is always measured *across* something: between its two ends | Measuring the drop from the top of a waterfall to the bottom |
| ground | The point in a circuit we agree to call "zero volts", and measure every other voltage from; in simple circuits, the battery's minus side, which is also the common return path | Sea level, from which every mountain height is measured |
| reference point | Whatever point you choose as the zero for your measurements | The floor you measure a shelf's height from |
| earth | A real connection to the soil, through a metal rod, used for safety in home wiring; not the same thing as ground | A lightning rod's wire going into the ground |
| cell | A single chemical unit that makes a push, like one AA battery | One step of a staircase |
| polarity | Which side is + and which is - | Which end of a ramp is up |

## Learning Objectives

- Explain voltage in plain words as a push, and as the energy each bit of charge gains or gives up
- Use the height picture: the battery lifts charge up, the charge falls back down through the lamp
- Explain why a voltage is always between two points, and what "across" means
- Explain what ground is: the point we agree to call zero, usually the battery's minus side, the common return
- Tell ground from earth, and say where the course meets earth properly
- Give everyday voltages in words: an AA cell, a 9 V battery, a USB port, a car battery, a wall socket

## The Problem

Every battery has a number printed on it, followed by a V: an AA cell, a square 9 V battery, a car battery, a laptop charger. Electronics parts come with warnings like "do not exceed this voltage". Wall sockets are dangerous because of their voltage. So what *is* it?

Lesson 04 gave you current: how much charge flows by each second. But a current does not start by itself. Something has to **push** the charge round the loop, and something has to decide how much energy each bit of charge carries to the lamp. That push is **voltage**.

Voltage also hides the most common source of confusion for beginners: people say "this point is at five volts" as if voltage belonged to a single point. It never does. By the end of this lesson you will know why, and you will know what **ground** really means.

## The Physics

Think about what the battery is doing. Inside it, chemistry is at work: two different materials react, and the reaction drives electrons away from one terminal and towards the other. That leaves one terminal with a surplus of electrons (the minus side) and the other with a shortage (the plus side). Connect the two through a lamp, and the charge has a way to go round.

Each bit of charge that the battery sends round the loop has been given some **energy** by the chemistry. As it passes through the lamp, it hands that energy over, and the lamp turns it into light and heat. Then the charge returns to the battery, gets lifted again, and goes round again.

**Voltage** is the measure of that energy: how much energy each bit of charge gains in the battery, or gives up in the lamp. A bigger voltage means each bit of charge carries more energy round the loop. That is why we call voltage the push: a bigger push gives each bit of charge more to deliver.

Phase 01 (Lesson 06, Energy, Potential and Voltage) makes this precise and shows exactly how voltage, energy and charge are related. Here we only need the idea.

## The Concept

### The height picture

The most useful picture of voltage is **height**.

Imagine a playground slide. A child climbs the ladder (that takes energy) and then slides down (giving the energy back, as speed and a bit of warmth). The taller the slide, the more energy each trip involves.

```
          battery lifts the charge up
                   |
   9 V   +---------+                 +-----------+   top of the lamp
         |  ^      |                 |           |
         |  |      |  wire: flat, no |  lamp:    |
         |  |      |  change in      |  charge   |
         |  |      |  height         |  falls    |
         |  |      |                 |  down     |
   0 V   +--+------+-----------------+-----v-----+   bottom: back to ground
       battery -                     bottom of the lamp
```

In a circuit:

- **The battery is the ladder**, or a pump lifting water up a hill. It lifts each bit of charge from a low level to a high level.
- **The wires are flat paths.** Along a good wire, the height hardly changes at all.
- **The lamp is the slide.** The charge "falls" from the high level back down to the low level as it passes through, and the energy it gives up becomes light and heat.
- **Back at the bottom**, the charge returns to the battery to be lifted again.

The voltage of a battery is the **height of its ladder**: how far it lifts each bit of charge. A 9 V battery lifts it six times higher than a 1.5 V cell.

### What the height picture gets wrong

No picture is perfect:

- Water and children fall because of gravity, pulling downwards. Charge is pushed by electric forces, which work in any direction: a "high" point in a circuit need not be physically higher on the table.
- A sliding child speeds up. Charge in a wire does not speed up as it "falls" through the lamp; it keeps drifting slowly (Lesson 03), and the energy goes straight into the lamp as heat and light.

Phase 02 (Lesson 05, The Water Analogy and Its Limits) is an entire lesson on where these pictures work and where they break. For now, height is the picture to keep.

### The volt

The unit of voltage is the **volt**, written **V**, named after Alessandro Volta, who in 1800 stacked discs of zinc and copper with salty cloth between them and built the first battery. In formulas, voltage is also written V (sometimes U in European books); context tells you whether V means "the voltage" or "volts".

Everyday voltages, in words:

| Source | Voltage | Is it dangerous to touch? |
|--------|---------|---------------------------|
| one AA cell | 1.5 volts | no |
| a USB port | 5 volts | no |
| a square 9 V battery | 9 volts | no, but never short it |
| a car battery | 12 volts | not to touch, but a short is very dangerous |
| a wall socket | 230 volts in Europe, 120 in North America | yes: it can kill. Never touch. |

Lesson 08 (Safety First) explains why the wall socket is dangerous and why the batteries above are safe to learn with.

### Stacking cells

A flashlight with two AA cells, placed end to end (the plus of one touching the minus of the next), has twice the push of one cell. Each cell is one step of a staircase; stack the steps and the heights add up. That is also where the word "battery" comes from: a *battery* of cells working together, like a battery of drums. A square 9 V battery is really six small cells stacked inside one case.

Put one cell the wrong way round, and its step goes down instead of up: the pushes cancel. That is why battery holders mark + and -: the **polarity** matters.

### Voltage is always between two points

Here is the most important idea of the lesson.

A height only means something if you say what it is measured **from**. "This shelf is two metres high" means two metres above the floor. "The mountain is three thousand metres high" means above sea level. If you do not say "above what?", the number is meaningless.

Voltage is the same. A voltage is always **between two points**. We say the voltage **across** the lamp (between its two ends), the voltage across the battery (between its two terminals), the voltage between this wire and that one.

That is the difference with current, from Lesson 04:

```
     voltage is ACROSS something: between its two ends
     current is THROUGH something: past one point of it

            |<------- voltage across the lamp ------>|
     -->----o------------- ( lamp ) -----------------o----->--
            current flows through the lamp, the same on both sides
```

This also explains two facts that surprise beginners:

- **A battery in a drawer has a voltage but no current.** The push is there, between its two terminals, but there is no loop, so nothing flows.
- **An open switch has no current, but the whole push of the battery sits across its gap.** The battery is still pushing; the charge just cannot get through. That is why an "off" switch on a wall-socket circuit is still dangerous inside.

To measure a voltage you touch a meter's two probes to the two points. You do not need to open the loop as you did for current. Phase 02 (Lesson 07, Measuring with a Multimeter) shows how.

### Ground: the point we agree to call zero

Measuring every voltage between two named points gets tiring in a big circuit. So engineers do what map makers do with sea level: they **pick one point and agree to call it zero**. That point is called **ground**.

Once ground is chosen, "the voltage at the top of the lamp" is just a shorter way of saying "the voltage between the top of the lamp and ground". Every voltage in the circuit is measured from that one agreed zero, the way every height on a map is measured from sea level.

In most simple circuits, ground is **the battery's minus side**. In the flashlight:

```
   battery +  .............  9 V above ground
   top of the lamp ........  9 V   (joined to battery + by plain wire)
   bottom of the lamp .....  0 V   (joined to battery - by plain wire)
   battery -  .............  0 V   ground, by our choice
```

So the whole 9 V of the battery appears across the lamp, from its top to its bottom.

Ground is also the **common return path**. In a bigger circuit with many parts, every part sends its current back to the battery's minus side. All those return wires end up at the same place: ground. That is why designers draw ground with a special symbol, and why every ground symbol in a drawing means "connected back here". Lesson 07 (Your First Schematic) shows the symbol.

Three things to remember about ground:

1. **Ground is a choice.** Nothing physical changes when you call a point zero. You could pick a different point, and every "voltage at a point" would shift by the same amount, but the voltage *across* anything would not change at all. Sea level is useful because everyone agrees on it, not because the sea is special.
2. **Ground is usually the minus side** in battery circuits, because it makes most voltages positive and easy to read.
3. **Ground is not a wire into the soil.** In a battery gadget, nothing touches the Earth. "Ground" is just our zero.

### Ground is not earth

The word "ground" comes from the early telegraph, which really did use the soil as the return path. In home wiring, there is still a real connection to the soil: the third pin of many wall plugs connects, through the house wiring, to a metal rod driven into the ground outside. That is called **earth** (in North America also "ground", which adds to the confusion). Its job is **safety**: if a fault makes the metal case of a washing machine live, the earth wire carries the current away safely and trips a breaker instead of passing through you.

So keep two ideas apart:

| | Ground (in this course) | Earth |
|---|---|---|
| What it is | The point we agree to call zero volts | A real wire to a metal rod in the soil |
| Where it lives | In every circuit, usually the battery's minus | In mains wiring and the cases of appliances |
| Why it exists | To have one reference for every voltage, and one common return path | Safety: to carry fault current away from people |
| Where we study it | Here, and all through the course | Phase 06 (Sources, Batteries and Measurement) and Phase 21 (PCB Design and Manufacturing) |

## Build It

The program for this lesson draws the "height" of each point of a 9 V flashlight above ground, shows voltages between pairs of points, changes the choice of zero, and lists everyday voltages. Run it from the repository root:

```
uv run python phases/00-meet-electricity/05-voltage-and-volts/code/main.py
```

### Step 1: Heights above ground

Each point of the loop gets a height, with ground (the battery's minus side) at zero. A bar of `#` makes the height visible:

```
  battery -                         0 V
  battery +                         9 V  ###########################
  top of the lamp                   9 V  ###########################
  bottom of the lamp                0 V
```

### Step 2: Between two points

The voltage between two points is the difference of their heights. Across the lamp it is the full 9 V. Between the battery's plus and the top of the lamp it is zero: they are joined by plain wire, a flat path.

### Step 3: Choosing a different zero

```python
def heights_from(reference_name, loop):
    zero = dict(loop)[reference_name]
    return [(name, level - zero) for name, level in loop]
```

Measured from the battery's plus side instead, every label shifts down by 9 V (the minus side becomes "-9 V"), yet the voltage across the lamp is still 9 V. Ground is a choice of labels, not a change in the circuit.

### Step 4: The open switch and everyday voltages

The program shows the whole push across an open gap with no current, and prints the table of everyday voltages. Try changing `BATTERY_VOLTS` to 1.5 and run it again.

## Use It

- **Battery labels** give the voltage: the height of the battery's ladder. Devices are designed for a particular voltage; too low and they do not work, too high and they can be damaged.
- **USB** gives a steady 5 volts. Fast chargers can raise it after agreeing with the phone first (Lesson 01).
- **Circuit boards** have a large copper area marked **GND**: the ground of the whole board, the common return for every chip. Phase 21 shows how it is designed.
- **Birds on power lines** sit safely on one wire. Their two feet are on the same wire, at the same height, so there is no voltage across the bird and no current through it. Touching the wire and the ground at the same time would be a different story (Lesson 08).

## Common Mistakes

- **"The voltage at this point" without a reference.** Always ask "measured from where?". If nobody says, it usually means "from ground".
- **"The voltage through the lamp."** Voltage is *across*; current is *through*.
- **"No current means no voltage."** A battery in a drawer and an open switch both have voltage and no current.
- **"Ground is the soil" or "ground is where electricity disappears to."** In a circuit, ground is just the agreed zero and the common return path. The current comes back to the battery; it does not vanish into the ground.
- **Confusing ground with earth.** Earth is a safety wire to the soil in mains wiring; ground is the reference of a circuit. Sometimes they are connected, often they are not.
- **Putting a cell in backwards.** Its push then cancels the push of another cell.

## Exercises

1. **Easy.** Fill in "across" or "through": the voltage ___ the battery; the current ___ the wire; the voltage ___ the switch; the current ___ the lamp.
2. **Easy.** A flashlight holds four AA cells end to end. In words, how does its push compare with one cell's?
3. **Medium.** In `main.py`, change the reference to "top of the lamp". Predict all four heights before running it. What stays the same?
4. **Medium.** Explain, using the height picture, why a bird on a power line is safe.
5. **Hard.** A friend says: "My gadget's circuit is grounded, so it is connected to the Earth and safe." Explain the two different meanings of "ground" mixed up in that sentence, and which phase of the course deals with each.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| voltage | "the electricity at this point" | The push between two points: the energy each bit of charge gains or gives up between them |
| volt (V) | "how strong the battery is" | The unit of voltage, the electrical "height" |
| across | "through" (wrongly) | Between the two ends of a part; where a voltage is measured |
| ground | "the earth" or "negative" | The point we agree to call zero volts; in simple circuits the battery's minus, the common return path |
| earth | "ground" | A real safety connection to the soil in mains wiring; not the same as a circuit's ground |
| polarity | "which way up" | Which side is + and which is -; it matters for batteries and many parts |

## Further Reading

- [The Physics Classroom, "Electric Potential Difference"](https://www.physicsclassroom.com/class/circuits/Lesson-1/Electric-Potential-Difference) — voltage as an energy difference, with a gentle gravity comparison.
- [Wikipedia, "Ground (electricity)"](https://en.wikipedia.org/wiki/Ground_(electricity)) — the many meanings of "ground", from circuit reference to the safety earth in buildings.
- [Wikipedia, "Voltaic pile"](https://en.wikipedia.org/wiki/Voltaic_pile) — Volta's first battery and how stacking cells adds their pushes.
- [SparkFun, "Voltage, Current, Resistance, and Ohm's Law"](https://learn.sparkfun.com/tutorials/voltage-current-resistance-and-ohms-law) — voltage alongside current, with a water-tank picture to compare with our height picture.
