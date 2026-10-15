# The Board

> Placement turns a list of connections into a small, quiet, cheap object. Put the parts where the wires want them, then check every rule.

**Type:** Build
**Prerequisites:** Phase 22 (Capstone), Lessons 01-04; Phase 21 (PCB Design and Manufacturing), Lessons 01 (From Schematic to Board), 02 (Footprints and Traces), 03 (Ground Planes and Current Return), 04 (Design Rules) and 05 (Fabrication)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Board outline | The shape and size of the finished board | The plot of land a house is built on |
| Courtyard | The keep-out rectangle around a part that no other part may enter | The personal space around a seat |
| Placement check | Verifying that no courtyards overlap and that parts keep away from the board edge | Checking that no furniture blocks a door |
| Ratsnest | The straight connection lines still to be routed (Phase 21, Lesson 01) | String tied between pins that must be joined |
| Ground pour | A large copper area connected to ground, usually filling a whole layer | A car park instead of a lane |
| Net class | A group of nets that share a trace width or clearance rule | Lanes reserved for buses |
| Decoupling distance | How far a decoupling capacitor sits from the pin it serves | How far the fire extinguisher hangs from the stove |
| Keep-out zone | An area where copper or parts are forbidden (for example under a light sensor's window) | A no-parking zone |
| BOM cost | The total price of all parts for one unit | The shopping bill for one cake |
| Panel / quantity price | The price per board once the setup is shared over many boards (Phase 21, Lesson 05) | Bulk discount |

## Learning Objectives

- Place the night light's parts on a 40 x 30 mm board following signal flow, with each decoupling capacitor next to its pin.
- Check the placement automatically: no overlapping courtyards, edge clearance, decoupling distance.
- Compute the ratsnest length of every net with a minimum spanning tree, and choose trace widths per net.
- Simulate the LED path with the trace resistances included, and show when the copper does and does not matter.
- Compute the bill of materials and board cost per unit, and check requirement R6.

## The Problem

We have a schematic that works in simulation (Lessons 03-04). Now it must become a board small enough for a night light's case, cheap enough to sell, and laid out so that nothing on it misbehaves. Phase 21 gave us the tools: footprints, ratsnest, trace widths, ground planes, design rules, fabrication costs. This lesson applies all of them to one real design, with a tiny layout model in Python.

Our board is simple and slow (the fastest signal is a 1 kHz PWM), so we do not need four layers or controlled impedance. But even a simple board has rules worth following: the LDR must face the room (not be shadowed by the LED's light!), the decoupling capacitor must sit at the microcontroller's power pin, the LED's current should not flow through the sensor's ground, and the whole thing must fit in 40 x 30 mm and cost under \$3 in parts.

## The Physics

Two pieces of physics from Phase 21 guide this layout:

- **Return currents** (Phase 21, Lesson 03): the LED's 19 mA pulses leave the battery, go through R5, the LED and Q1, and must come back to the battery's negative terminal. If that return shares a thin ground trace with the light sensor's divider (R1) or the battery divider (R3), the pulses lift their ground by `I * R` and the ADC sees a voltage that switches at 1 kHz. With a ground pour on the bottom layer, the ground resistance is tiny everywhere and the problem disappears. A good placement also keeps the LED's loop (battery, R5, D1, Q1) compact and away from the sensor's inputs.
- **Optics, not just electronics**: the LDR sees all light, including our own LED. If the LED shines onto the LDR, the night light could see its own light at night and switch off, then on again in the dark: an oscillator made of light. On a real product the LDR faces outward through a window and the LED is shielded or points another way. On our board they sit at opposite corners and the case is responsible for keeping them optically apart.

## The Concept

### Placement by signal flow

```
   +--------------------------------------------------------------+  30 mm
   |                 C1                         LDR1  (top right,  |
   |          U1 (LDO)    C2              C3       faces the room)|
   |  BT1                            +--------+        R1          |
   |  (battery,                      |   U2   |                    |
   |   left edge)      R2            | (MCU)  |        R5          |
   |                   R3   C4       +--------+   R4               |
   |                                               Q1      D1 (LED)|
   +--------------------------------------------------------------+
   0                                                           40 mm
```

From left to right: the battery connector at the edge (where the wires come in), the regulator and its capacitors next to it, the microcontroller in the middle, the light sensor at the top right corner, the LED driver and the LED at the bottom right. The battery divider (R2, R3, C4) sits between the battery and the microcontroller. C3 sits 2.7 mm from the microcontroller's VCC pin.

### The placement check

Each footprint has a **courtyard**, a rectangle around it that no other part may enter (it leaves room for the assembly machine's nozzle and for rework). Two rectangles `(x0, y0, x1, y1)` and `(u0, v0, u1, v1)` overlap if

```
x0 < u1  and  u0 < x1  and  y0 < v1  and  v0 < y1
```

"each one starts before the other ends, in both directions". The check also requires every courtyard to stay at least 1 mm from the board edge, and the decoupling capacitor's pad to be within 3 mm of the pin it serves. Our placement passes all three: 0 problems, and C3 at 2.74 mm.

### Ratsnest and trace widths

The minimum spanning tree of each net (Phase 21, Lesson 01) estimates its copper:

| Net | Pins | Length |
|---|---|---|
| VBAT | 5 | 57.9 mm |
| VDD | 4 | 17.8 mm |
| LDR_PWR | 2 | 14.0 mm |
| LIGHT | 3 | 24.0 mm |
| BAT_SENSE | 4 | 22.9 mm |
| PWM | 2 | 6.7 mm |
| BASE | 2 | 7.4 mm |
| LED_A | 2 | 9.2 mm |
| LED_K | 2 | 8.8 mm |
| GND | 10 | 83.1 mm |

About 252 mm of copper in total. Ground is the longest net, as on every board, and it is the one we will replace with a pour.

For trace widths, IPC-2221 (Phase 21, Lesson 02) asks for only about 0.001 mm for 21 mA: any trace the factory can make is far more than enough for heat. So the widths are set by other rules: 0.25 mm for signals (comfortably above the 0.15 mm fab minimum), 0.4 mm for the power nets as a net class, so that their resistance stays low. The resulting drops are tiny: about 1.5 mV along VBAT and 2.1 mV along the (worst-case, as if it were a single trace) ground net.

### Does the copper matter here?

Put the trace resistances into the LED path and simulate:

```
ideal wires                  LED 18.802 mA
our traces                   LED 18.750 mA   (0.3% less)
3x longer, 0.15 mm traces    LED 18.392 mA   (2.2% less)
```

At our currents, the copper hardly matters for the LED. It is still good practice to make power traces wider, and the ground pour matters for a different reason (the sensor's reference, above). Compare with the 2 A heater of Phase 21, Lesson 02, where the trace decided whether the board worked at all: the same rules, applied with numbers, give very different answers for different designs.

### Two layers, one pour

A low-cost two-layer board is plenty:

- **Top layer**: all parts and almost all signal traces.
- **Bottom layer**: a solid ground pour, connected to every ground pad through a via next to the pad (with thermal reliefs on through-hole pads so they can be soldered, Phase 21, Lesson 06).
- A few signal traces may jump to the bottom layer to cross each other, cutting the pour as little as possible and never under the sensor's path.

### Cost

| Item | Price (100 units) |
|---|---|
| battery holder and connector | \$0.70 |
| microcontroller (8-pin) | \$0.60 |
| LDO | \$0.25 |
| LDR | \$0.10 |
| LED | \$0.05 |
| transistor | \$0.03 |
| 4 capacitors | \$0.04 |
| 5 resistors | \$0.025 |
| **parts total** | **\$1.79** |
| bare board 40 x 30 mm (toy cost model of Phase 21, Lesson 05, 100 boards) | \$0.44 |
| **total** | **\$2.24** |

R6 asked for parts under \$3: pass, with room for a case and assembly. (Prices vary by supplier and year; the method is what matters: list every part, look up the price at your quantity, add the board.)

## Build It

Run:

```
uv run python phases/22-capstone/05-the-board/code/main.py
```

### Step 1: Footprints, parts and pads

```python
FOOTPRINTS = {
    "SOT23": {"size": (3.2, 3.2), "pads": {"1": (-0.95, 1.0), "2": (0.95, 1.0), "3": (0.0, -1.0)}},
    "SOIC8": {"size": (6.0, 5.4), "pads": {...}},
    "0805": {"size": (3.0, 1.8), "pads": {"1": (-0.95, 0.0), "2": (0.95, 0.0)}},
    ...
}

PARTS = {
    "U1": ("SOT23", (13.0, 9.0), {"GND": "1", "OUT": "2", "IN": "3"}, 0.25),
    ...
}
```

Each part has a footprint, a position, a **pin map** from schematic pin names (like `U1.IN`) to footprint pad numbers (`3` on the SOT-23), and a price. The pin map is where datasheets matter: an LDO and a transistor in the same SOT-23 package have completely different pinouts. `pad_xy` turns a schematic pin into board coordinates.

### Step 2: The placement check

```python
def placement_drc():
    errors = []
    refs = list(PARTS)
    for i, a in enumerate(refs):
        ax0, ay0, ax1, ay1 = courtyard(a)
        if min(ax0, ay0, BOARD_W - ax1, BOARD_H - ay1) < EDGE_CLEARANCE - 1e-9:
            errors.append(...)
        for b in refs[i + 1:]:
            bx0, by0, bx1, by1 = courtyard(b)
            if ax0 < bx1 and bx0 < ax1 and ay0 < by1 and by0 < ay1:
                errors.append(f"{a} and {b} overlap")
    return errors
```

Output: 0 problems, and 2.74 mm from C3 to the VCC pin.

### Step 3: Ratsnest and widths

`mst_length` is Prim's method with Manhattan distances (as in Phase 21, Lesson 01); `ipc_width_mm` is the IPC-2221 formula of Phase 21, Lesson 02; `trace_ohms` is `rho L / (w t)`. The script prints each net's length, the IPC minimum, the chosen width, the resistance and the drop at that net's current.

### Step 4: Copper in the simulation

`led_current` builds the LED path with a resistor for each piece of copper (`T_VBAT`, `T_LED_A`, `T_LED_K`, `T_GND`) and simulates three cases.

### Step 5: Cost

The parts' prices are summed and the board price comes from Phase 21's toy cost model (\$30 setup plus \$0.012 per cm^2, for 100 boards).

## Use It

- **In KiCad**, the same steps are: assign footprints (with the right pinout!), "Update PCB from Schematic", place by hand following signal flow, set net classes for power, route, pour ground on the bottom layer, run DRC, review the 3D view (is the LDR exposed? does the LED clear the case?), and export Gerbers and the BOM.
- **Footprint pinout mistakes** are the classic first-board error: SOT-23 parts in particular come with many different pin orders. Always check the footprint against the exact part number's datasheet.
- **Mechanical constraints** often come first: the case decides the outline, mounting holes, the battery holder's position and where the LDR and LED must be.
- **Assembly service**: a board this small with 0805 and SOT-23 parts can be ordered assembled from many fabs; through-hole parts (LED, LDR) may be hand-soldered afterwards.
- **Design for test**: add test points on VBAT, VDD, LIGHT, BAT_SENSE and PWM; Lesson 06 uses them.

## Common Mistakes

- **Shadowing or blinding the sensor.** An LDR next to the LED sees its own light; one under a tall part sees nothing.
- **Decoupling capacitor far from the pin.** It must be placed first, right at the pin, with a short ground connection.
- **Routing the LED's current through the sensor's ground.** Use a ground pour or keep the LED's return separate from the divider returns.
- **Wrong pin map.** The schematic is right, the board is right, but pad 1 of the footprint is not pin 1 of the part. Check every three-pin package.
- **Squeezing too hard.** Parts packed at their courtyard limits are harder to assemble, probe and repair. Leave space where you can.

## Exercises

1. Move the LDR to (8, 25) in `PARTS`. Does the placement check pass? How do the LIGHT and LDR_PWR ratsnest lengths change? Is it a better or worse place, considering the optics?
2. Compute by hand the resistance of 57.9 mm of 0.4 mm wide, 35 µm copper. Does it match the script?
3. Add test points (small 1.5 mm pads, footprint size 2 x 2 mm) for VBAT, VDD and LIGHT to the placement. Where would you put them so that a probe can reach them easily?
4. Make the board 30 x 25 mm. Rearrange the parts so the placement check still passes. What is the new total ratsnest length?
5. Harder: write a tiny greedy placer, like the one in Phase 20, Lesson 11, that swaps the positions of the 0805 parts to reduce the total ratsnest length while keeping the placement check clean. How much shorter does it get?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Courtyard | "keep-out box" | The rectangle around a footprint that no other part may enter |
| Placement check | "courtyard DRC" | Automatic test for overlaps, edge clearance and placement rules |
| Pin map | "pinout" | The mapping from schematic pin names to footprint pad numbers |
| Net class | "power nets" | A set of nets with their own width or clearance rules |
| Ground pour | "copper fill" | A ground plane made by filling a layer with copper connected to GND |
| BOM cost | "parts cost" | Sum of all part prices at a given quantity |

## Further Reading

- [KiCad documentation: PCB Editor](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html) — placement, net classes, pours and DRC in practice.
- Phase 21 of this course, especially Lessons 01-05 — the methods reused here.
- Microchip, *ATtiny85 datasheet*, pinout and package drawings; onsemi *MMBT3904* and Microchip *MCP1700* package drawings (the SOT-23 pinouts differ).
- Henry W. Ott, *Electromagnetic Compatibility Engineering* (Wiley, 2009) — grounding and layout for mixed analog and switching circuits.
