# Reading a Schematic

> A schematic is a map of connections, not a photograph. It tells you what touches what, and nothing else.

**Type:** Learn
**Prerequisites:** Phase 00 (Words and Units), Lesson 02 (The Vocabulary) and Lesson 03 (Units and SI Prefixes)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| schematic | a drawing of a circuit that uses standard symbols and lines to show which parts are connected | a metro map: it shows which stations connect, not where they really are |
| symbol | a small standard drawing that stands for one kind of component | the knife-and-fork sign on a motorway that means "restaurant" |
| reference designator | the short label that names one part, like R1 or D2 | a seat number in a theatre |
| terminal (pin) | a point on a component where a wire can attach | the two ends of a battery |
| wire (in a schematic) | a line meaning "these points are electrically the same" | a corridor between rooms: its length on paper means nothing |
| node (net) | everything joined by wires with no component in between; one electrical "place" | one room, however oddly shaped |
| junction dot | a filled dot where wires meet and really connect | a roundabout where roads join |
| crossing | two wires drawn across each other that do NOT connect | a bridge: one road passes over the other |
| net label | a name written on a wire; every wire with the same name is connected | two signposts saying "Station Street": same street |
| ground symbol | a symbol marking the node we choose as 0 volts | sea level, the height we measure everything from |
| netlist | a text list of every part and the nodes its terminals touch | a guest list saying who sits at which table |
| layout | how the parts are physically placed on a board | the real streets, as opposed to the metro map |

## Learning Objectives

- Recognise the symbols for cell, battery, resistor (both US and European styles), lamp, LED, diode, switch, capacitor, wire and the three common ground symbols
- Tell a junction (connected) from a crossing (not connected), and know why four-way junctions are avoided
- Identify the nodes of a circuit from its schematic and count them
- Explain why a schematic and a physical layout of the same circuit can look completely different but be identical electrically
- Read the flashlight and the LED schematics of this course out loud, part by part and node by node
- Write and read a simple netlist, and use code to find dangling wires and shorted parts

## The Problem

Imagine you want to build a small circuit you found online: a battery, a resistor and an LED. You open the page and see a photo of a breadboard full of coloured wires. The wires loop over each other, the LED is half hidden behind a jumper, and the resistor's legs disappear into holes you cannot see. You copy what you think you see, and nothing lights up.

Now imagine the same page also shows this:

```
   +---[ R1 330 ]---+
   |                |
  +|                V  D1
  === B1           ---  red LED
  -|  5 V           |
   |                |
   +----------------+
```

Six lines of drawing and you know everything: the battery's plus side goes to one end of a 330 Ω resistor, the other end of the resistor goes to the LED's anode, the LED's cathode goes back to the battery's minus. Any layout that makes those three connections will work. Any layout that does not, will not.

That is the job of a schematic. Photos show where things are. Schematics show how things are connected, and in electronics, connection is everything. Every datasheet, every repair manual, every project in this course and every simulator you will use speaks this language. This lesson teaches you to read it.

## The Physics

Why can a drawing throw away the positions and lengths of the wires? Because of one physical fact that we will justify in later phases: a good wire (copper, a few centimetres to a few metres long, carrying a modest current) has a tiny resistance, a few thousandths of an ohm, so almost no voltage is lost along it. To a very good approximation, every point along a connected piece of wire is at the same voltage (the "electrical pressure" you met in Lesson 02). So all the points joined by wires behave as one single place: a node.

That is what makes a schematic possible. A wire on paper means "same voltage at both ends". Whether the real wire is 2 cm or 20 cm long, straight or curled, it is still the same node.

The approximation breaks in two places we will meet much later. When currents are huge (a car starter motor, Phase 03), even copper loses noticeable voltage, and the schematic must show the wire's resistance as a resistor. When signals change extremely fast (millions of times per second and up, Phase 21 on circuit boards), wires behave like little capacitors and inductors and their length matters. For everything we do in the first half of this course, "a wire is a perfect connection" is the right picture.

## The Concept

### A schematic is a graph

Strip a schematic down and it is two kinds of things: components (the symbols) and nodes (the connected groups of wire). Each component has terminals, and each terminal lands on exactly one node. Mathematicians would call this a graph. You do not need the word; you need the habit of asking, for every part, "which node is each of its legs on?".

### The symbols

There are two families of standards: the American one (IEEE 315, from 1975) and the international one (IEC 60617). Most schematics use a mix. You only need a handful to start. Here they are in proper form (described in words) and in the ASCII form this course uses in its code blocks.

**Wire.** A straight line. Corners in our ASCII are drawn with `+`. A corner is just the wire changing direction; it is not a component and not a special point.

```
   ----------+
             |
             +-------
```

**Cell.** A single chemical cell (like one AA, 1.5 V) is drawn as two parallel plates: a long thin line (the positive terminal) and a short thick line (the negative terminal). The rule to remember: long line is plus.

```
        |  +
     -------        long plate  = + (positive)
       ---          short plate = - (negative)
        |  -
```

**Battery.** Strictly, a battery is several cells stacked, drawn as two or more plate pairs. In everyday speech and in this course, any source drawn with plates is "a battery". In our ASCII we use `===` with the plus and minus marked beside it, and we always write the voltage.

```
       +|
       === B1   9 V
       -|
```

**Resistor.** Two styles exist and you must know both. The US style is a zigzag. The European (IEC) style is an empty rectangle. They mean exactly the same thing. Our ASCII uses the rectangle with the name and value inside.

```
   US:     ---/\/\/\/---
   IEC:    ---[      ]---
   ours:   ---[ R1 330 ]---
```

**Lamp (incandescent bulb).** A circle with an X inside (sometimes a circle with a little loop, the filament).

```
   ---(X)---
```

**Diode.** A triangle pointing at a bar. The triangle is the anode side, the bar is the cathode. Conventional current (the "plus to minus" direction of Lesson 02) can flow in the direction the triangle points, and is blocked the other way. We will meet the physics in Phase 11.

```
   horizontal:   anode ---|>|--- cathode     (often typed as  --->|---)
   vertical:        | anode
                    V
                   ---
                    | cathode
```

**LED (light-emitting diode).** A diode symbol with two small arrows pointing away from it, meaning "light comes out". It has polarity just like a diode: the anode must be on the more positive side. In ASCII the arrows are hard to draw, so we write "LED" next to it.

**Switch.** A gap in the wire with a little lever. Schematics draw a switch in its resting position, usually open (not connected).

```
   open:     ---o/  o---      the lever is lifted, no connection
   closed:   ---o---o---      the lever is down, a perfect connection
```

**Capacitor.** Two parallel plates of equal length with a gap: a device that stores charge (Phase 07). Some capacitors (electrolytic) have polarity; their symbol has one curved plate or a small + sign.

```
   ---| |---         plain capacitor
   ---|+ (---        polarised capacitor, + side marked
```

**Ground.** The node we decide to call 0 volts. Every voltage in the circuit is then measured relative to it, just as heights are measured from sea level. Three symbols are common:

```
     |              |              |
   -----          -----          _____
    ---           / / /          \   /
     -                            \ /
   earth          chassis         signal
```

- Earth ground (three shrinking lines): literally connected to the earth through the building's wiring.
- Chassis ground (a comb): connected to the metal case of a device.
- Signal ground (a hollow triangle): the common return of a circuit, the 0 V reference.

In battery circuits like ours, all three mean the same thing: the 0 V node, usually the battery's minus. In our ASCII we just write `gnd`. A key rule: every ground symbol in a schematic is connected to every other ground symbol, even if no line joins them. The symbol is a shortcut that saves drawing the same return wire ten times.

### Junction or crossing?

This is the single most important detail in reading a schematic. When two lines meet:

```
   connected (junction dot):        not connected (crossing):

            |                                |
       -----*-----                      -----)-----
            |                                |
```

- A **junction** is marked with a filled dot (our ASCII uses `*`). All wires touching the dot are one node.
- A **crossing** is two wires that pass over each other with no connection. Modern schematics draw them as a plain cross with no dot; older ones and our ASCII draw a little hop (`)`) so there is no doubt.

Because a dot can disappear when a drawing is photocopied or printed small, careful designers never draw a four-way junction. They offset it into two T-junctions:

```
   risky:                  safe:

        |                       |
   -----*-----             -----*
        |                       |
                                *-----
                                |
```

A T-junction (three wires meeting) is always a connection, even if the dot is missing, because a wire cannot "cross" something it stops at. So when you see a plain `+` shape with four arms and no dot, assume a crossing; when you see a T, assume a connection.

### Nodes: colour the wires

Here is the most useful trick for reading any schematic. Take a set of coloured pencils. Pick a wire, colour it, and keep colouring every wire you can reach without passing through a component. Stop at every component's terminal. That coloured region is one node. Pick a fresh colour for an uncoloured wire and repeat.

Do this for the flashlight:

```
  vcc     S1      lamp_top
   +---o/  o---+
   |           |
  +|          (X) L1
  === B1       |  3 V, 0.3 A lamp
  -|  3 V      |
   |           |
   +-----------+
  gnd
```

- Start at B1's plus terminal. The wire goes up and right to S1's left contact, and stops there. Colour 1: the node `vcc`. It touches B1.plus and S1.a.
- From S1's right contact, the wire goes right and down to the top of the lamp L1. Colour 2: the node `lamp_top`. It touches S1.b and L1.a.
- From the bottom of the lamp, the wire goes down, left, and up to B1's minus. Colour 3: the node `gnd`. It touches L1.b and B1.minus.

Three nodes, three components. Notice the bottom wire has two corners and is drawn long, but it is all one node. That long bottom line is exactly the same electrical "place" as the little stub under the battery.

### Reading the flashlight out loud

Practise saying a schematic as a sentence; it forces you to check every connection.

"Two AA cells in series, together 3 volts, make battery B1. Its plus terminal goes to switch S1. When S1 is closed, the other side of the switch reaches lamp L1, a 3 V, 0.3 A bulb. The lamp's other end returns to the battery's minus, which we call ground. Closing the switch completes the loop; conventional current leaves the battery's plus, flows through the switch and the lamp, and returns to the minus."

As a preview of Phase 03 (V = I x R, read "voltage equals current times resistance"), a lamp that draws 0.3 A at 3 V behaves, when hot, like a resistance of 3 / 0.3 = 10 Ω. That 10 is the value our netlist stores for L1.

### Reading the LED circuit out loud

```
  vcc              led_a
   +---[ R1 330 ]---+
   |                |
  +|                V  D1
  === B1           ---  red LED
  -|  5 V           |
   |                |
   +----------------+
  gnd              gnd
```

"A 5 V source B1. Its plus goes to node vcc and through a 330 Ω resistor R1 to node led_a. Node led_a is the anode of a red LED, D1. The LED's cathode is on ground, which is the battery's minus." The triangle points down, from led_a to gnd, which is the same direction conventional current flows around this loop. If you turned the LED around (bar on top) the triangle would point against the current and the LED would stay dark. Schematics make polarity mistakes visible.

The order in a loop does not matter for which current flows (Phase 04 will show why): the resistor could be on the ground side of the LED instead, and the circuit would work the same. Different drawing, same behaviour.

### Schematic versus physical layout

Here is the same LED circuit as you might build it on a breadboard (Phase 02, Lesson 06), seen from above:

```
     battery clip                 breadboard
   red  ------------------------> row 3
   black ------------------------> row 12

   row 3:  red wire, R1 left leg
   row 7:  R1 right leg, LED long leg (anode)
   row 12: LED short leg (cathode), black wire
```

On the board the resistor and LED are side by side, the battery is off to the left, the wires are long and colourful. Nothing looks like the schematic. Yet the connections are identical: three nodes (rows 3, 7 and 12), the same three parts on the same nodes. The schematic is the truth; the layout is one of thousands of ways to make it real.

Conventions you will see in most schematics, to make them easy to read:

- Higher voltages near the top, ground at the bottom.
- Signals flow left to right (input on the left, output on the right).
- Reference designators use standard letters: R resistor, C capacitor, L inductor, D diode or LED, Q transistor, U integrated circuit, S or SW switch, B or BT battery, F fuse, J connector.
- Values next to the symbol, with SI prefixes from Lesson 03 (330, 4.7k, 100n). European schematics often put the prefix where the decimal point would go: 4k7 means 4.7 kΩ, 2R2 means 2.2 Ω. It avoids losing a tiny decimal point in a smudged print.

### Net labels and power symbols

Big schematics would be a mess of lines if every connection were drawn. Instead, designers write a name on a wire, a net label. Two wires labelled `VCC` anywhere on the page, even on different pages, are the same node. The same goes for power symbols (an arrow or a bar labelled `+5V`) and ground symbols. When you colour nodes, wires with the same label get the same colour.

This is also where most real-world mistakes hide: a label typed `LED_A` in one place and `led_a` in another is two different nets, and the circuit silently has a break in it. Our code will catch exactly that.

### Netlists: a schematic as text

A computer does not need the picture, only the connections. A netlist is a list with one line per component: its name, its type, the node each terminal sits on, and its value. Our course's tiny format is:

```
NAME TYPE NODE_1 NODE_2 VALUE
B1   battery  vcc   gnd  5V
R1   resistor vcc   led_a 330
D1   led      led_a gnd  red
```

For polarised parts the order matters: battery is plus then minus, LED is anode then cathode. This is the same idea as the netlists used by SPICE, the circuit simulator developed at UC Berkeley in the early 1970s that every professional tool still descends from. Our own simulator `sim` (from Phase 05) takes the same information as Python calls instead of text.

## Build It

`code/main.py` stores the two schematics of this lesson as ASCII art and as netlists, parses the netlists, prints which part touches which node, walks around the loop, and checks for mistakes.

### Step 1: Know each part's terminal names

```python
TERMINAL_NAMES = {
    "battery": ("plus", "minus"),
    "resistor": ("a", "b"),
    "lamp": ("a", "b"),
    "led": ("anode", "cathode"),
    "diode": ("anode", "cathode"),
    "switch": ("a", "b"),
    "capacitor": ("a", "b"),
}
```

The first node in a netlist line goes to the first terminal name, the second to the second.

### Step 2: Parse the netlist

```python
def parse_netlist(text):
    parts = []
    for line_number, raw_line in enumerate(text.strip().splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("*"):
            continue
        fields = line.split()
        if len(fields) < 4:
            raise ValueError(f"line {line_number}: expected NAME TYPE NODE NODE [VALUE], got {line!r}")
        name, kind, first_node, second_node = fields[:4]
        if kind not in TERMINAL_NAMES:
            raise ValueError(f"line {line_number}: unknown part type {kind!r}")
        value = fields[4] if len(fields) > 4 else ""
        parts.append({"name": name, "kind": kind, "nodes": (first_node, second_node), "value": value})
    return parts
```

Lines starting with `*` are remarks (the same habit as SPICE). Each part becomes a small dictionary.

### Step 3: Build the node map ("colour the wires")

```python
def build_node_map(parts):
    node_map = defaultdict(list)
    for part in parts:
        for terminal, node in zip(TERMINAL_NAMES[part["kind"]], part["nodes"]):
            node_map[node].append(f"{part['name']}.{terminal}")
    return dict(sorted(node_map.items()))
```

For every node, the list of terminals that touch it. For the flashlight:

```
  nodes (who touches whom):
    gnd       : B1.minus, L1.b
    lamp_top  : S1.b, L1.a
    vcc       : B1.plus, S1.a
```

Exactly the three colours we found by hand.

### Step 4: Walk the loop

`trace_loop` starts at the battery's plus node, repeatedly crosses the next unused part touching the current node, and stops when it reaches the battery's minus (a closed loop) or gets stuck (a broken loop):

```
  walk from B1 plus: vcc -> S1 -> lamp_top -> L1 -> gnd  (closed loop back to the battery's minus)
```

This tiny walker only handles a single loop, which is all we have in this phase. Real tools handle any shape; you will build one in Phase 05.

### Step 5: Find mistakes

```python
def find_problems(parts, node_map):
    problems = []
    for node, terminals in node_map.items():
        if len(terminals) == 1:
            problems.append(f"node '{node}' touches only {terminals[0]}: a dangling end, nothing can flow through it")
    for part in parts:
        if part["nodes"][0] == part["nodes"][1]:
            problems.append(f"{part['name']} has both ends on node '{part['nodes'][0]}': it is shorted out and does nothing")
    if "gnd" not in node_map:
        problems.append("no node called 'gnd': this circuit has no reference point")
    return problems
```

Two classic mistakes: a node with only one terminal on it (a wire that goes nowhere) and a part with both legs on the same node (shorted out, Lesson 02's "short"). The broken netlist in the script has a typo (`led_A` versus `led_a`) and a capacitor with both legs on ground:

```
  walk from B1 plus: vcc -> R1 -> led_a  (loop is broken)
  problems found: 3
    - node 'led_A' touches only D1.anode: a dangling end, nothing can flow through it
    - node 'led_a' touches only R1.b: a dangling end, nothing can flow through it
    - C1 has both ends on node 'gnd': it is shorted out and does nothing
```

One wrong capital letter, and the LED is disconnected from its resistor. On paper the two labels look almost the same; to the computer, and to the electrons, they are different places.

Run it:

```
cd /home/fer/Escritorio/youtube/electronics_from_scratch
uv run python phases/00-words-and-units/05-reading-a-schematic/code/main.py
```

## Use It

- **Datasheets.** Every chip datasheet has an "application circuit" or "typical application": a schematic of the minimum parts around the chip. The LM7805 voltage regulator's typical circuit, for example, is the chip plus two capacitors, one on the input and one on the output. Reading it is exactly this lesson.
- **EDA tools.** KiCad (free) and commercial tools work in two stages: you draw the schematic, the tool extracts a netlist, and then you arrange the physical board layout (Phase 21). The tool constantly checks that the layout's copper matches the netlist. Schematic, netlist and layout are three views of one design.
- **Repair.** Service manuals for amplifiers, TVs and appliances are bundles of schematics with node voltages written on them ("12 V here, 0.6 V there"). Technicians measure the real board and compare.
- **This course.** Every circuit from now on is shown as an ASCII schematic, every simulator call in Phase 05 onward is a netlist written in Python, and the lab boards (Phase 02 onward) are described by nodes and terminals in exactly this way.

## Common Mistakes

- **Thinking line length or position matters.** A long wire on paper is not "more resistance" and parts drawn far apart are not "far apart" electrically. Only connections matter.
- **Missing a junction dot, or inventing one.** Four lines crossing without a dot are two separate wires. A T is always a connection. Look carefully before deciding two wires share a node.
- **Forgetting that all grounds are connected.** Ground symbols at the bottom of five different parts of a page are one single node even with no line between them.
- **Reversing polarised parts.** Battery: long plate is plus. Diode and LED: the triangle points from anode to cathode, in the direction conventional current is allowed to flow. A backwards LED simply stays dark (and a backwards electrolytic capacitor can burst, Phase 07).
- **Copying the picture, not the connections.** When building from a schematic, check connections one node at a time ("what touches vcc? B1.plus and R1. Done.") instead of trying to make the board look like the drawing.
- **Typos in net labels.** `VCC`, `Vcc` and `VCC1` are three different nets to a computer. Keep labels consistent.
- **Confusing the US and IEC resistor symbols with other parts.** The IEC rectangle is a resistor, not a fuse (a fuse is often drawn as a rectangle with a line running through it) and not an integrated circuit (a larger box with many pins).

## Exercises

1. Draw (in ASCII or on paper) a 9 V battery, a closed switch, a 1 kΩ resistor and a green LED in one loop. Name the nodes and write the netlist in our format.
2. Count the nodes in the LED schematic of this lesson. Then imagine moving R1 to the bottom wire, between the LED's cathode and the battery's minus. Redraw it. How many nodes now, and which terminals are on each?
3. A schematic shows two vertical wires and two horizontal wires forming a `#` shape, with dots on two of the four crossings only. How many separate wire segments are connected to each other? Draw your interpretation.
4. Add a second lamp to the flashlight netlist so that both lamps are switched by S1 and each lamp has one leg on `lamp_top` and the other on `gnd`. Run the parser on your netlist (edit `main.py` or paste the functions into a Python session). How many terminals are on `lamp_top` now? (This is "parallel", which you will meet in Phase 02, Lesson 04.)
5. (Harder) Extend `find_problems` so it also warns when a battery's plus and minus are on the same node, or when two terminals of the circuit are joined only by a closed switch across the battery. Why would either of these be dangerous in real life? (Hint: Lesson 06 and Phase 02, Lesson 03.)

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| schematic | "the circuit diagram" | a drawing of connections using standard symbols; positions and lengths carry no meaning |
| node / net | "a point in the circuit" | every piece of wire joined together with no component in between; one voltage |
| junction | "where wires meet" | a connection, marked with a dot; only Ts and dotted crossings connect |
| ground | "the earth", "negative" | the node we choose as 0 V; in battery circuits usually the battery's minus, not literally the earth |
| reference designator | "the part number" | a unique label for one part in a design (R1, D2), not the manufacturer's part number |
| netlist | "the list of parts" | the list of parts and the nodes each terminal is on; all a simulator needs |
| layout | "the circuit" | the physical arrangement of parts and copper; one of many ways to realise a schematic |
| polarity | "which way round" | which terminal of a part must be on the more positive node |

## Further Reading

- [SparkFun, "How to Read a Schematic"](https://learn.sparkfun.com/tutorials/how-to-read-a-schematic): a friendly illustrated walk through symbols, designators and nets.
- [All About Circuits, Volume I, Chapter 2 "Ohm's Law", section "Circuit Wiring"](https://www.allaboutcircuits.com/textbook/direct-current/chpt-2/circuit-wiring/): free textbook section on how wires and electrically common points appear in schematics.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors* (McGraw-Hill, 4th edition, 2016): the appendix and early chapters use and explain the standard symbol set.
- [KiCad documentation, "Schematic Editor"](https://docs.kicad.org/10.0/en/eeschema/eeschema.html): see how a professional free tool turns schematics into netlists and boards.
