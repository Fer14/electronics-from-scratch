# From Schematic to Board

> A schematic says what is connected. A board says where, and "where" turns out to matter.

**Type:** Learn
**Prerequisites:** Phase 00 (Meet Electricity), Lesson 07 (Your First Schematic); Phase 02 (Your First Circuits), Lesson 06 (The Breadboard); Phase 03 (Resistance and Ohm's Law), Lesson 02 (Resistivity and Wires); Phase 11 (Semiconductors and Diodes), Lesson 07 (LEDs)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| PCB (printed circuit board) | A flat board of insulating material with copper "wires" printed on it, onto which parts are soldered | A city map where the roads are made of copper |
| Substrate | The insulating sheet in the middle of the board, usually FR-4 (glass cloth soaked in epoxy) | The ground the roads are built on |
| Copper layer | A thin sheet of copper glued to the substrate and etched into a pattern | The asphalt of the roads |
| Trace (or track) | One copper road on the board, joining two or more pins | A street between two houses |
| Pad | A small bare copper patch where a part's pin is soldered | A driveway where a car parks |
| Footprint | The exact pattern of pads one part needs on the board | The parking space painted on the floor for one model of car |
| Via | A plated hole that connects a trace on one copper layer to a trace on another | A staircase between two floors of a car park |
| Netlist | A list of every connection in the schematic: which pins belong together | A guest list saying who must be able to call whom |
| Net | One group of pins that must all be electrically joined | One family on the guest list |
| Placement | Deciding where each part sits on the board | Arranging furniture in a room |
| Routing | Drawing the copper traces that make each net real | Building the roads after the houses are placed |
| Ratsnest | Straight "rubber band" lines an editor draws between pins that still need to be connected | String tied between pins that should be joined |
| Solder mask | The coloured (often green) varnish that covers copper you do not solder | Paint on a road that says "no parking" |
| Silkscreen | The white printed letters and outlines on top of the board | Street signs and house numbers |
| Gerber file | The standard file format that tells a factory what each layer of the board looks like | The blueprint you send to the builder |
| EDA tool | "Electronic design automation" software used to draw schematics and boards (KiCad is a free one) | The architect's drawing program |

## Learning Objectives

- Describe the physical layers of a printed circuit board and what each one is for.
- Explain the journey from a schematic to a manufactured board: netlist, footprints, placement, routing, checks, output files.
- Read a netlist and say which pins must be joined by copper.
- Compute ratsnest lengths for a placement with a minimum spanning tree and Manhattan distance, and see why placement decides most of a layout's quality.
- Estimate the resistance that a board's traces add, using the resistivity of copper from Phase 03.

## The Problem

Up to now every circuit in this course has lived in two places: on paper (a schematic) and inside our simulator. Some of them could also live on a breadboard (Phase 02, Lesson 06), with jumper wires sprouting everywhere. That is fine for an afternoon experiment, but nobody ships a breadboard inside a product. The springy contacts wear out, the wires fall off when you drop it, and it is far too big.

Every electronic object you own, from a phone charger to a TV remote, contains a printed circuit board instead: a stiff, flat board where copper paths replace the jumper wires and every part is soldered into place. The moment you go from a schematic to such a board, you face questions a schematic never asked you. Where does each part sit? Which way does it face? How wide is each copper path, and how long? Does the path from the battery to the LED run right next to the path from the sensor? A schematic is a drawing of *connections*; a board is a drawing of *geometry*. Two boards with identical schematics can behave differently because their geometry is different.

This phase is about that geometry. In this first lesson we follow the whole path from a finished schematic to a finished board, and we build the smallest possible "board model" in Python, so that in the next lessons we can put numbers on things like trace width, return current and design rules.

## The Physics

A copper trace is just a flat wire. Everything you learned about wires in Phase 03 still applies. Its resistance is

```
R = rho * L / A
```

Read it aloud: "the resistance equals the resistivity of the material, times the length, divided by the cross-section area." Here `R` is resistance in ohms (Ω), `rho` (the Greek letter rho, ρ) is the resistivity of copper, about 1.72 × 10^-8 Ω·m at 20 °C, `L` is the length in metres, and `A` is the cross-section area in square metres.

What is new on a board is the *shape* of that cross-section. A round wire has a circle for a cross-section. A trace is a very thin, flat rectangle: its width is something you choose (0.15 mm to several mm), and its thickness is fixed by the copper sheet the factory uses. The most common sheet is called "1 ounce copper", because one square foot of it weighs one ounce. That works out to a thickness of about 35 micrometres (35 µm = 0.035 mm), roughly half the thickness of a human hair.

So a 0.25 mm wide trace has a cross-section of

```
A = width * thickness = 0.25e-3 m * 35e-6 m = 8.75e-9 m^2
```

and every millimetre of it adds

```
R per mm = 1.72e-8 * 1e-3 / 8.75e-9 = 0.00197 Ω  (about 2 milliohms)
```

Two milliohms per millimetre sounds like nothing, and for an LED drawing 10 mA it is nothing. But a motor drawing 2 A through 100 mm of that trace would lose `2 A * 0.197 Ω = 0.39 V` and heat the trace with `2^2 * 0.197 = 0.79 W`. Geometry has physical consequences. We will make this precise in Lesson 02.

There is a second piece of physics that the schematic hides completely: a current always flows in a *loop*. When current leaves the battery through one trace, the same current comes back through another (often the ground). On a schematic the return is just a ground symbol. On a board the return is a real piece of copper, at a real place, and the area enclosed by the outgoing and returning paths matters (Lesson 03).

## The Concept

### What a board is made of

Cut a simple two-layer board in half and look at the edge with a magnifying glass:

```
   silkscreen (white ink: "R1", outlines)    ...........
   solder mask (green varnish)               ===========
   top copper (traces and pads)              ##  ###  ##
   FR-4 substrate (1.6 mm of glass + epoxy)  |||||||||||
                                             |||||||||||
   bottom copper (often a ground plane)      ###########
   solder mask                               ===========
```

- The **substrate** is the stiff, insulating core. The most common one, FR-4, is woven fibreglass soaked in epoxy resin; "FR" means flame retardant. A standard board is 1.6 mm thick.
- The **copper layers** are where the conductors live. A cheap board has two (top and bottom). Phones use eight, ten or more, stacked like a sandwich with substrate between each pair.
- The **solder mask** covers the copper everywhere except the pads. It stops solder from flowing along traces and protects the copper from oxidising. It is what gives boards their typical green colour.
- The **silkscreen** prints the names of parts ("R1", "D1"), their outlines and polarity marks, so a human can assemble and repair the board.
- **Vias** are small holes drilled through the board and plated with copper on the inside, so that a trace on top can continue on the bottom.

### The design flow

Every board, from a hobby LED blinker to a graphics card, goes through the same steps:

```
  1. schematic        what connects to what (Phase 00, Lesson 07)
        |
  2. simulate         does it work? (our sim, Phases 05-19)
        |
  3. netlist          the list of nets, exported from the schematic
        |
  4. footprints       pick the physical package of every part
        |
  5. placement        put the parts on the board outline
        |
  6. routing          draw traces (and planes, and vias) for every net
        |
  7. checks           design rules (Lesson 04) and "does the copper match the netlist?"
        |
  8. outputs          Gerber files, drill file, bill of materials, pick-and-place file
        |
  9. fabrication and assembly (Lessons 05 and 06)
        |
 10. bring-up and debugging (Lesson 07)
```

The tool we use is called an EDA tool (electronic design automation). KiCad is a free, open-source one used by hobbyists and professionals; others you will hear about are Altium, Eagle/Fusion and OrCAD. They all follow this flow.

### Our example: a USB-powered LED with a button

We will carry one tiny circuit through the flow. A USB port gives 5 V. A push button connects it to a 330 Ω resistor, the resistor feeds a red LED, and the LED returns to ground.

```
   J1 (USB 5 V)
   pin 1 ---- VBUS ---- SW1 ---- SW_OUT ---- R1 330 Ω ---- LED_A ---- D1 (red) ----+
                                                                                  |
   pin 2 ---- GND ----------------------------------------------------------------+
```

Before touching the board, we check the schematic does what we want (step 2). The LED keeps roughly 1.9 V across itself, so the resistor sees about `5 - 1.9 = 3.1 V` and the current is about

```
I = 3.1 V / 330 Ω = 0.0094 A = 9.4 mA
```

That is a comfortable current for an indicator LED. The resistor dissipates `P = V * I = 3.1 * 0.0094 = 0.029 W`, about 29 mW, so a tiny 0805 resistor (rated 125 mW) is plenty. Our simulator will confirm these numbers in Build It.

### The netlist: connections without geometry

Name every pin with "part reference" dot "pin name": `J1.1` is pin 1 of the USB connector, `D1.A` is the anode of the LED, `D1.K` its cathode (K comes from the German "Kathode"). Grouping pins that touch the same wire gives the netlist:

```
VBUS   : J1.1, SW1.1
SW_OUT : SW1.2, R1.1
LED_A  : R1.2, D1.A
GND    : D1.K, J1.2
```

This is exactly the information in the schematic and nothing more. It says nothing about where `R1` will sit. That is why the same netlist can produce countless different boards.

### Footprints: the parking spaces

A schematic symbol for a resistor is a zigzag. The physical resistor might be a through-hole part with long legs, or a surface-mount chip only 2.0 mm long. Each choice needs a different pattern of pads on the board: a **footprint**. The footprint fixes where the pads are *relative to the centre of the part*. For our parts:

```
  R_0805 (2.0 x 1.25 mm resistor)      pad 1 at (-0.95, 0), pad 2 at (+0.95, 0)
  LED_0805                             pad A at (-0.95, 0), pad K at (+0.95, 0)
  Button_6mm                           pad 1 at (-3.25, 0), pad 2 at (+3.25, 0)
  USB_power_2pin (simplified)          pad 1 at (0, -1.25), pad 2 at (0, +1.25)
```

The name "0805" is a size code in hundredths of an inch: 0.08 inch by 0.05 inch, which is about 2.0 mm by 1.25 mm. Lesson 02 has more on footprints.

Once a part has a position `(x, y)` on the board, each pad sits at

```
pad position = part position + pad offset
```

For example, if R1 is placed at (14.0, 4.0) mm, its pad 1 is at `(14.0 - 0.95, 4.0 + 0) = (13.05, 4.0)` mm.

### Placement decides almost everything

After placement, the EDA tool draws the **ratsnest**: for each net, thin straight lines joining the pins that still need copper. Routing then replaces each rubber band with a real trace.

How long will the copper be? We can estimate it before routing. Two rules make the estimate realistic:

1. **Manhattan distance.** Traces usually run horizontally and vertically (sometimes at 45°), like streets in a grid city. The distance between `(x1, y1)` and `(x2, y2)` along such streets is `|x1 - x2| + |y1 - y2|`, "the horizontal gap plus the vertical gap". Example: from (2, 3.75) to (4.75, 2) is `2.75 + 1.75 = 4.5` mm.
2. **Minimum spanning tree.** If a net has three or more pins, you do not need a trace from every pin to every other pin. You need just enough traces to connect them all, with no loops. The cheapest such set is the *minimum spanning tree* (MST). A simple way to build it (Prim's method): start from any pin; repeatedly add the shortest connection from a pin already in the tree to a pin not yet in it; stop when all pins are in.

The total MST length of all nets is a good first measure of a placement's quality. Shorter usually means less resistance, less inductance, less area wasted on traces and an easier routing job.

Worked example for the tidy placement, net `LED_A` (R1.2 to D1.A). With R1 at (14, 4) and D1 at (14, 7):

```
R1.2 = (14 + 0.95, 4) = (14.95, 4.00)
D1.A = (14 - 0.95, 7) = (13.05, 7.00)
distance = |14.95 - 13.05| + |4.00 - 7.00| = 1.90 + 3.00 = 4.90 mm
```

Notice something: if we rotated D1 by 180° so that its anode faced R1's pad 2, the distance would drop to 3.0 mm. Rotation is part of placement too.

## Build It

The full script is `code/main.py`. Run it from the repository root:

```
uv run python phases/21-pcb-design-and-manufacturing/01-from-schematic-to-board/code/main.py
```

### Step 1: Check the schematic with the simulator

Before any geometry, we make sure the circuit works. The USB port is a 5 V source, the button is a closed switch (we are pressing it), and the LED uses the red preset of our simulator.

```python
def simulate_schematic():
    c = Circuit()
    c.voltage_source("J1", "vbus", "0", 5.0)
    c.switch("SW1", "vbus", "sw_out", closed=True)
    c.resistor("R1", "sw_out", "led_a", 330)
    c.led("D1", "led_a", "0", color="red")
    return c.dc()
```

The script prints an LED voltage of 1.848 V, an LED current of 9.55 mA and a resistor power of 30.1 mW. Our simulator's red LED keeps a little less than the 1.9 V we guessed, so the current comes out slightly above our 9.4 mA estimate.

### Step 2: The netlist as data

A netlist is just a dictionary from net name to a list of `(part, pad)` pairs:

```python
NETLIST = {
    "VBUS": [("J1", "1"), ("SW1", "1")],
    "SW_OUT": [("SW1", "2"), ("R1", "1")],
    "LED_A": [("R1", "2"), ("D1", "A")],
    "GND": [("D1", "K"), ("J1", "2")],
}
```

### Step 3: Parts, footprints and pad positions

A `Part` remembers its reference, its footprint name, its position in millimetres and the offsets of its pads. `pad_position` adds the offset to the part position:

```python
@dataclass
class Part:
    ref: str
    footprint: str
    x: float
    y: float
    pads: dict = field(default_factory=dict)

    def pad_position(self, pad):
        dx, dy = self.pads[pad]
        return self.x + dx, self.y + dy
```

We make two placements of the same four parts. In the "tidy" one, the parts sit in signal order from left to right (connector, button, resistor, LED). In the "messy" one they are scattered.

### Step 4: Ratsnest length with a minimum spanning tree

```python
def manhattan(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def minimum_spanning_tree(points):
    in_tree = [0]
    edges = []
    while len(in_tree) < len(points):
        best = None
        for i in in_tree:
            for j in range(len(points)):
                if j in in_tree:
                    continue
                d = manhattan(points[i], points[j])
                if best is None or d < best[0]:
                    best = (d, i, j)
        edges.append(best)
        in_tree.append(best[2])
    return edges
```

Every net here has two pins, so its tree is a single edge, but the same function works for a net with ten pins (a ground net on a real board often has dozens). The script prints:

```
  net          tidy    messy
  VBUS         4.50    16.00
  SW_OUT       3.80    18.20
  LED_A        4.90    22.10
  GND         13.70    22.20
  total       26.90    78.50
  the messy placement needs 2.92x more copper
```

Same schematic, same parts, almost three times more copper. Notice also that in the tidy placement the GND net is by far the longest (13.7 mm): the LED is at the far end of the board and its current has to come all the way back to the connector. Real designers solve that with a *ground plane* (a whole copper layer used as the return path), which is the subject of Lesson 03.

### Step 5: What the copper costs

Using the resistance formula from The Physics with a 0.25 mm wide, 35 µm thick trace:

```python
rho = 1.72e-8
area = 0.25e-3 * 35e-6
resistance = rho * total * 1e-3 / area
```

The tidy board adds about 53 mΩ in total, the messy one about 154 mΩ. At 9.4 mA neither matters (154 mΩ × 9.4 mA ≈ 1.4 mV). At 2 A the messy board would lose 0.3 V in its copper. Hold on to that thought for Lesson 02.

## Use It

- **KiCad** (free) follows exactly this flow: Schematic Editor, "Update PCB from Schematic" (that is the netlist step), footprint assignment, the PCB Editor with its ratsnest lines, an interactive router, the Design Rules Checker, and "Plot" to produce Gerber files.
- **Placement first, routing second.** Experienced designers spend most of their layout time on placement. A good rule: place parts in the order the signal flows (input connector, protection, regulator, microcontroller, outputs), put parts that talk a lot next to each other, and put each decoupling capacitor right at the power pin it serves (Lesson 03).
- **Real ratsnest tools** in KiCad and Altium compute exactly the minimum spanning tree we computed, and many auto-placers minimise its total length (or a smoother version of it) as their main goal. Chip design uses the same idea at a much larger scale (Phase 20, Lesson 11).
- **Board sizes and costs.** A two-layer 50 × 50 mm board made by a low-cost online fab costs a few dollars for five copies today; the price depends mostly on area, layer count and how fine the features are (Lesson 05).

## Common Mistakes

- **Treating the schematic as the layout.** Drawing the board in the same arrangement as the schematic rarely gives the shortest connections. Place by signal flow and by which pins connect, not by where the symbols happened to sit on paper.
- **Forgetting that rotation is part of placement.** Rotating a two-pin part by 180° can shorten two traces at once, as in the `LED_A` example.
- **Choosing footprints carelessly.** If the footprint does not match the part you buy (for example a 0603 footprint for an 0805 resistor), the part will not fit. Always check the footprint against the manufacturer's datasheet drawing.
- **Ignoring the return path.** A schematic hides the ground return under a symbol. On the board it is a real path with real length, often the longest one, as our GND net showed.
- **Routing before the schematic is simulated.** Fixing a wrong resistor value costs nothing in the schematic and costs a new board run after fabrication.

## Exercises

1. A trace is 0.5 mm wide, 35 µm thick and 40 mm long. Compute its resistance in milliohms. How many millivolts does it drop at 1 A?
2. Pad P is at (3, 2) mm and pad Q at (10, 7) mm. What is the Manhattan distance between them? What is the straight-line (Euclidean) distance? Why do EDA tools often prefer the Manhattan estimate?
3. A ground net has four pins at (0, 0), (10, 0), (10, 5) and (0, 5) mm. Build its minimum spanning tree by hand with Prim's method starting at (0, 0). What is the total length? Compare it with joining every pin straight back to (0, 0).
4. In the tidy placement, rotate D1 by 180° (swap the offsets of its A and K pads). Recompute the `LED_A` and `GND` distances. Does the total go up or down? Edit `FOOTPRINTS` or the placement in the script to check.
5. Harder: move J1 in the tidy placement so that the total ratsnest length is as small as possible while keeping the other three parts fixed. Try a few positions in the script and explain the trade-off between the VBUS and GND nets.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| PCB | "the green board" | Insulating substrate plus etched copper layers, solder mask and silkscreen, holding and connecting the parts |
| Footprint | "the pads for a part" | The exact pad pattern, positions and sizes that one physical package needs |
| Netlist | "the connections" | The list of nets, each naming every pin that must be electrically joined |
| Ratsnest | "the airwires" | Straight lines between pins of a net that are not yet joined by copper, usually drawn as a minimum spanning tree |
| Placement | "putting parts down" | Choosing the position and rotation of every footprint; the step that most decides trace lengths |
| Routing | "drawing tracks" | Turning each ratsnest connection into copper traces, vias and planes |
| Gerber | "the board files" | The standard layer-by-layer file format sent to a PCB factory |

## Further Reading

- [KiCad documentation: Getting Started](https://docs.kicad.org/10.0/en/getting_started_in_kicad/getting_started_in_kicad.html) — the official walkthrough of the schematic-to-board flow in a free EDA tool.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., the chapter on building circuits and PCBs.
- [IPC-2221B, Generic Standard on Printed Board Design](https://www.ipc.org/) — the industry standard behind most of the numbers in this phase.
