# Your First Schematic

> A schematic is a map of a circuit, not a picture of it. It shows what connects to what, and nothing else.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 00 (Meet Electricity), Lessons 02 (What a Circuit Is), 04 (Current and Amperes) and 05 (Voltage and Volts)
**Time:** ~50 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| schematic | A drawing of a circuit that uses standard symbols and lines to show which parts are connected to which | A metro map: it shows which stations connect, not where they really are |
| symbol | A small standard drawing that stands for one kind of part | The knife-and-fork sign that means "restaurant" |
| lamp symbol | A circle with an X inside: a light bulb | A round bulb seen from the front, with its glowing wire crossed |
| battery symbol | A long line and a short line side by side; the long line is plus, the short line is minus | A tall step and a short step |
| ground symbol | A short stack of lines getting smaller, like an upside-down pyramid: "this is our zero, everything connects back here" | The sea-level mark on a map |
| junction | A point where wires meet and are really joined, drawn with a dot | A roundabout where roads join |
| crossing | Two wires drawn across each other that are NOT joined | A bridge: one road passes over the other |
| node | Everything joined together by plain wire, with no part in between; one electrical "place" (studied properly in Phase 04) | One room of a house, however oddly shaped |
| label (name) | A short name next to a part, like B1, S1 or L1 | A seat number in a theatre |
| netlist | A text list of every part and the two places (nodes) it connects | A guest list saying who sits at which table |

## Learning Objectives

- Explain why a schematic shows connections, not positions or lengths
- Recognise and name, next to the real object, the symbols for battery, wire, switch, lamp, ground, and (as previews) resistor and LED
- Explain what the ground symbol means: our agreed zero, the place everything connects back to
- Tell a junction (joined) from a crossing (not joined)
- Read the flashlight schematic wire by wire, following the current
- Write the flashlight as a short parts list, a netlist

## The Problem

Picture a photo of a small project on a breadboard: coloured wires looping over each other, a battery off to one side, a lamp half hidden behind a jumper. Copy what you *think* you see, and very often nothing lights up. The photo shows where things are, but in electronics, where things are hardly matters. What matters is **what is connected to what**.

Engineers solved this long ago with a drawing language: the **schematic**. Each part becomes a small standard symbol, each connection becomes a line, and everything else is thrown away. A schematic of a flashlight is a few lines; anyone in the world who knows the symbols reads the same circuit from it.

Every datasheet, every repair manual, every project in this course and every simulator speaks this language. This lesson teaches the first words of it: the symbols for the parts you already know, each one shown next to the real object it stands for.

## The Physics

Why can a drawing throw away the positions and lengths of the wires? Because of one fact from Lesson 05: along a good wire, the "height" (the voltage) hardly changes. A copper wire is such an easy path that, to a very good approximation, every point along a connected piece of wire is at the same voltage. Whether the real wire is short or long, straight or curly, it behaves as a single electrical place.

That is what makes a schematic possible. A line on paper means "these points are joined, at the same voltage". Its length and shape mean nothing.

This approximation breaks in two places we will meet much later: when currents are very large (Phase 03, Lesson 02, Resistivity and Wires), and when signals change extremely fast (Phase 21, PCB Design and Manufacturing). For the first half of this course, "a wire is a perfect connection" is the right picture.

## The Concept

### A map, not a picture

The best comparison is a metro map. On a metro map, the lines are straight, the stations are evenly spaced, and the river is a neat curve. None of that is true on the ground. But the map tells you exactly what you need: which stations connect, and in which order. A schematic does the same for a circuit.

So when you read a schematic, never ask "where is this part?" or "how long is this wire?". Ask only: **what does each end of each part connect to?**

### The symbols, one by one

Here are the symbols you need for this phase, each with the real thing it stands for. There are two families of standards in the world (an American one and an international one), and most drawings mix them a little. We show the common forms, and the plain text versions this course uses in its code blocks.

**Battery.** A real battery is a cylinder (an AA cell) or a box (a 9 V battery) with a plus end and a minus end. Its symbol is a pair of parallel lines: a **long line for plus** and a **short line for minus**. A single pair is one cell; several pairs are a battery of cells. The rule to remember: *long line, plus*.

```
        |  +
     -------      long line  = plus  (+)
       ---        short line = minus (-)
        |  -
```

**Wire.** A real wire is copper in a plastic sleeve. Its symbol is simply a line. Corners (drawn with `+` in our text drawings) are just the wire changing direction; they are not parts.

```
   ----------+
             |
             +---------
```

**Switch.** A real switch is a slider or a button that joins or separates two metal contacts. Its symbol is a gap with a little lever. A switch is usually drawn **open** (off).

```
   open:    ---o/  o---     the lever is up: no connection
   closed:  ---o---o---     the lever is down: a perfect connection
```

**Lamp.** A real lamp is a light bulb: a glass globe with a thin wire inside that glows. Its symbol is **a circle with an X inside**. When you see `(X)` in a schematic, read "light bulb".

```
   ---(X)---       a lamp: the light bulb of the flashlight
```

**Resistor (a preview).** A real resistor is a small cylinder with coloured stripes and a wire at each end. Its job is to make it harder for current to get through (Lesson 06's preview of resistance). Its symbol is either a zigzag (American style) or an empty rectangle (international style). Both mean the same thing. Phase 03 (Resistance and Ohm's Law) is all about it.

```
   ---/\/\/\---     zigzag style
   ---[    ]---     box style
```

**LED (a preview).** A real LED is a small coloured dome with two legs, one longer than the other. It is a lamp made from a semiconductor, and it only lets current through in one direction. Its symbol is a triangle pointing at a bar, with two small arrows coming out of it for the light. Phase 11 (Semiconductors and Diodes) explains it; for now, know that it has a right way round.

```
   ---|>|---        triangle points the way current is allowed to flow
```

**Ground.** Ground is not a part you can buy; it is the point we agree to call zero (Lesson 05). In battery circuits it is usually the battery's minus side, the common return of every current. Its symbol is a short stack of lines getting smaller, like an upside-down pyramid. It says: **"this is our zero; everything with this symbol connects back here"**.

```
         |
       -----
        ---
         -          ground: our zero, the common return
```

A very useful rule: **every ground symbol in a schematic is connected to every other ground symbol**, even if no line is drawn between them. In a big drawing, instead of running a return wire from every part back to the battery, the designer just puts a ground symbol under each part. You will also see other ground symbols later (a hollow triangle, a comb-like shape for a metal case), and in mains equipment the same three lines are often used for earth, the safety connection to the soil. Phase 21 sorts these out. In this course, until then, the three shrinking lines mean our zero.

### Junction or crossing?

When two lines meet in a schematic, there are two possibilities, and telling them apart is the most important detail in reading a drawing:

```
   joined (junction):           not joined (crossing):

   ------*------                     |
         |                      -----)-----
                                     |
```

- A **junction** is marked with a **dot**. All wires touching the dot are joined.
- A **crossing** is two wires passing over each other *without* touching. Modern drawings show it as a plain cross with no dot; older drawings and our text drawings draw a little hop.

A T-shape (three wires meeting) is always a junction, dot or no dot. A plain four-way cross with no dot is a crossing. Careful designers avoid four-way junctions altogether, because a tiny dot can disappear in a bad print.

### Nodes: colour the wires

Here is the trick for reading any schematic. Take some coloured pencils. Choose a wire and colour it, and keep colouring every wire you can reach **without passing through a part**. Stop at the ends of parts. That coloured region is one electrical place, called a **node**. Then take a new colour and repeat.

Every point of one node is at the same voltage, because plain wire joins it (that is the physics above). A node is not a single dot on the page: it can be a long wire with several branches. A junction dot is simply a place where a node branches.

Phase 04 (Lesson 01, Nodes, Branches and Loops) studies nodes properly; it is the starting point of every circuit calculation. For now, colouring is enough.

### Reading the flashlight

Here is the flashlight of Lessons 01 and 02, now as a real schematic:

```
            S1
   +-------o/ o-------+
   |                  |
  +|                 (X) L1
 ----- B1             |
  ---                 |
  -|                  |
   +--------+---------+
            |
          -----
           ---
            -
```

Name every symbol first:

- **B1** is the **battery**: long line on top, so its plus side is at the top.
- **S1** is the **switch**, drawn open.
- **L1** is the **lamp**: the circle with an X, a light bulb.
- The three shrinking lines at the bottom are **ground**: our zero, joined to the battery's minus side.

Now colour the wires. There are three nodes:

1. From B1's plus, along the top-left wire, to the left contact of S1.
2. From the right contact of S1, along the top-right wire, down to the top of L1.
3. From the bottom of L1, along the bottom wire, to B1's minus and to the ground symbol. (The bottom wire has a junction where the ground symbol hangs off it; it is all one node.)

Now read it out loud, following the current (conventional current, from plus round to minus, Lesson 04):

> "The current leaves the plus side of battery B1, runs along the top wire to switch S1. When S1 is closed, it passes through the switch and along to the top of lamp L1. It passes through the lamp, which glows, and returns along the bottom wire to the minus side of the battery, which is our ground."

Saying a schematic as a sentence forces you to check every connection. If at some point you cannot say where the current goes next, you have found an open circuit (Lesson 02).

And voltages, read from ground (Lesson 05): the bottom node is zero; the left part of the top wire is at the full height of the battery; when the switch is closed, the right part of the top wire (and the top of the lamp) is at that full height too, so the whole push of the battery is across the lamp.

### Conventions that make schematics easy to read

- The higher voltages are drawn near the top, ground at the bottom (like the heights of Lesson 05).
- Signals usually flow from left to right.
- Every part gets a short label: a letter for its kind and a number. B for battery, S for switch, L for lamp (or LP), R for resistor, D for diode or LED. B1, S1, L1, R1, R2, D1.
- Values (like the voltage of a battery) are written next to the symbol. Phase 01 (Lesson 01, Units and Prefixes) teaches the shorthand that engineers use for them.

### A schematic as text: the netlist

A computer does not need the picture, only the connections. So a circuit can also be written as a list: one line per part, giving its name, its kind, and the two nodes its ends touch. This is called a **netlist**. Give each node a name (`top`, `lamp_top`, `gnd` for ground), and the flashlight becomes:

```
B1  battery  top       gnd
S1  switch   top       lamp_top
L1  lamp     lamp_top  gnd
```

Three lines, and nothing is lost. For a battery the order matters: plus first, then minus. Professional circuit simulators read netlists exactly like this, and the simulator we build in Phase 05 (Circuit Analysis and Our Simulator) takes the same information as Python instructions.

## Build It

The program for this lesson prints each symbol with the real object it stands for, draws the flashlight schematic, writes it as a netlist, finds the nodes, and walks the loop following the current. Run it from the repository root:

```
uv run python phases/00-meet-electricity/07-your-first-schematic/code/main.py
```

### Step 1: The symbol gallery

Each entry is the symbol's name, the real object, and its text drawing:

```python
SYMBOLS = [
    ("battery", "a cell or a pack of cells", [...]),
    ("lamp", "a light bulb", ["  ---(X)---    a circle with an X"]),
    ("ground", "the point we call zero", [...]),
    ...
]
```

### Step 2: The netlist and its nodes

The netlist is read line by line, and every end of every part is filed under the node it touches:

```python
def node_map(parts):
    nodes = defaultdict(list)
    for part in parts:
        for terminal, node in zip(TERMINALS[part["kind"]], part["nodes"]):
            nodes[node].append(f"{part['name']}.{terminal}")
    return dict(nodes)
```

```
  top       B1.plus, S1.a
  gnd       B1.minus, L1.b
  lamp_top  S1.b, L1.a
```

These are exactly the three colours we found by hand.

### Step 3: Walk the loop

Starting at the battery's plus, the program keeps crossing the next part that touches the current node, until it arrives back at the battery's minus:

```
  start at B1's plus, on 'top'
  through S1 (switch) to 'lamp_top'
  through L1 (lamp) to 'gnd'
  back into B1's minus: the loop is closed
```

Try deleting the line for S1 from the netlist and run it again. What happens when the walk cannot find a next part? (That is an open circuit, and the program stops with an error, which you could turn into a friendly message as an exercise.)

## Use It

- **Datasheets.** Every chip comes with a small schematic called a "typical application": the minimum parts you need around it. Reading it is exactly this lesson.
- **Circuit design tools.** Free tools like KiCad work in two stages: you draw the schematic, the tool extracts the netlist, and then you lay out the real board (Phase 21). The tool constantly checks that the board matches the netlist.
- **Repair manuals** for amplifiers, TVs and appliances are bundles of schematics, often with the expected voltage written next to each node.
- **This course.** From now on every circuit is shown as a text schematic, the lab boards are described by nodes, and the simulator of Phase 05 starts from a netlist.

## Common Mistakes

- **Thinking line length or position matters.** A long line is not "more wire" and parts drawn far apart are not far apart electrically. Only connections matter.
- **Not naming a symbol.** Every symbol stands for a real object. The circle with an X is a light bulb; the long and short lines are a battery; the shrinking lines are ground. Say the name as you read.
- **Getting the battery upside down.** Long line, plus. Short line, minus.
- **Forgetting that all grounds are joined.** Ground symbols in different corners of a drawing are one single node.
- **Confusing junctions and crossings.** A dot (or a T) joins; a plain cross or a hop does not.
- **Copying the picture instead of the connections.** When building from a schematic, check one node at a time: "what touches this node? the battery's plus and the switch. Done."

## Exercises

1. **Easy.** Draw the symbols for a battery, an open switch, a lamp and ground, and write next to each the real object it stands for.
2. **Easy.** In the flashlight schematic, which line of the battery symbol is plus? Which node is ground?
3. **Medium.** Draw a schematic with one battery, one switch and *two* lamps, each lamp connected between the right side of the switch and ground. Colour the nodes. How many are there?
4. **Medium.** Write the netlist for your drawing in exercise 3, using the format of this lesson, and add it to `main.py` to check the nodes.
5. **Hard.** Read your exercise 3 schematic out loud, following the current. Where does the current split, and where does it come back together? (Phase 02, Lesson 04, Series and Parallel Intuition, is about exactly this.)

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| schematic | "the circuit diagram" | A drawing of connections using standard symbols; positions and lengths carry no meaning |
| lamp symbol | "a circle thing" | A circle with an X: a light bulb |
| ground symbol | "the earth" | Shrinking lines meaning our zero; every ground symbol is the same node, usually the battery's minus |
| junction | "where wires meet" | A real connection, marked with a dot (or a T) |
| node | "a point in the circuit" | Everything joined by plain wire, with no part in between; one voltage |
| netlist | "the list of parts" | The parts and the nodes each end touches; all a simulator needs |

## Further Reading

- [SparkFun, "How to Read a Schematic"](https://learn.sparkfun.com/tutorials/how-to-read-a-schematic) — a friendly illustrated walk through symbols, labels, junctions and nets.
- [The Physics Classroom, "Circuit Symbols and Circuit Diagrams"](https://www.physicsclassroom.com/class/circuits/Lesson-4/Circuit-Symbols-and-Circuit-Diagrams) — turning a picture of a circuit into a schematic, step by step.
- [Wikipedia, "Electronic symbol"](https://en.wikipedia.org/wiki/Electronic_symbol) — a large table of symbols in both the American and international styles, for reference.
- [Wikipedia, "Circuit diagram"](https://en.wikipedia.org/wiki/Circuit_diagram) — the history and conventions of schematics.
