# Design Rules

> The factory has limits and so does physics. Write both down as rules and let the computer check every millimetre.

**Type:** Build
**Prerequisites:** Phase 21 (PCB Design and Manufacturing), Lessons 01-03; Phase 07 (Capacitors), Lesson 03 (Charging and Discharging)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Design rule | A minimum (or maximum) size or distance that every part of the layout must respect | A building code: "doors at least 80 cm wide" |
| DRC (design rule check) | A program that measures the whole layout and lists every rule that is broken | A building inspector with a tape measure |
| Clearance | The gap of bare board between two pieces of copper on different nets | The space between two cars in a car park |
| Trace/space | Shorthand for the minimum trace width and minimum clearance a factory can make, e.g. "6/6 mil" | The thinnest line and the narrowest gap a printer can draw |
| Drill | The hole size for a via or a through-hole pin | The size of the drill bit |
| Annular ring | The ring of copper left around a drilled hole | The ring of a doughnut around its hole |
| Board edge clearance | How far copper must stay from the outline where the board is cut | Not parking right on the edge of a cliff |
| Creepage | The distance along the board surface between two conductors at different voltages | The path an ant would walk from one to the other |
| Capsule | Our geometric model of a trace or a round pad: a line segment with a thickness | A sausage seen from above |
| Electrical rule | A rule that comes from circuit behaviour, not from the factory, like "every chip gets a decoupling capacitor" | A safety rule, not a construction limit |
| Netclass | A group of nets that share rules, such as "power: 0.5 mm wide" | Different lanes for trucks and bicycles |

## Learning Objectives

- List the main manufacturing rules of a low-cost PCB factory and say where each one comes from.
- Model traces, pads and vias as capsules and compute the copper-to-copper gap between them.
- Write and run a small design rule checker that finds width, clearance, drill, annular ring and edge violations.
- Use a voltage-dependent clearance table for higher-voltage nets.
- Turn an electrical requirement (supply droop) into a design rule and verify it by simulation.

## The Problem

You finish your layout, send it to a cheap online factory, and get an email the next day: "Your design has traces of 0.1 mm; our minimum is 0.127 mm. Your vias have 0.2 mm drills; our minimum is 0.3 mm. One trace runs off the board outline. Please fix and resubmit." That costs you a day. Worse is the case where the factory makes the board anyway: two traces 0.08 mm apart get bridged by a speck of copper, and the board has a short that no simulation predicted.

The factory has physical limits: how thin a line its photo process can draw, how small a drill it can use without breaking bits, how accurately it can line up a drill with a pad. Physics adds its own limits: higher voltages need wider gaps to stop sparks and surface leakage; fast loads need capacitors close by. Professionals write all of these down as **design rules** and let the EDA tool check every millimetre of copper against them before anything is sent out. In this lesson we write a small rule checker ourselves.

## The Physics

### Where the factory rules come from

A board's copper pattern is made by covering copper with a light-sensitive film, exposing it to the pattern, and etching away the copper that is not protected (Lesson 05). Three physical effects set the limits:

- **Etching goes sideways too.** The chemicals eat the copper not just downwards but also under the edges of the protective film ("undercut"). A 35 µm thick copper layer loses some width at each edge. A line drawn too thin can be eaten through; a gap drawn too small can be left with copper bridges. That sets the minimum **trace width** and **clearance**. A typical low-cost rule is 0.15 mm (about 6 mil) for both; advanced factories go to 0.075 mm (3 mil) and below for a higher price. Thicker copper needs bigger values, because more copper must be etched.
- **Drill bits and registration.** Small drill bits break and wander. The drilled hole also never lands exactly at the centre of its pad: the layers are aligned ("registered") to within maybe ±0.05-0.1 mm. The **annular ring** is the copper left around the hole; if it is too thin, the drill can break out of the pad and the connection fails. Typical values: 0.3 mm minimum drill, 0.15 mm annular ring (so a 0.3 mm via needs at least a 0.6 mm pad).
- **Cutting the outline.** The board is routed out of a big panel with a milling bit. Copper too close to the edge can be cut, or left exposed and peeling. Typical **edge clearance**: 0.25-0.5 mm.

### Where the voltage rules come from

Air and the board surface are insulators, but not perfect ones. Two conductors at very different voltages, too close together, can spark across the air (that needs high fields: about 3 kV per mm in dry air at sea level), or slowly conduct along a surface that is dusty or damp. Standards such as IPC-2221 therefore give a minimum spacing that grows with the voltage between the conductors. For bare (uncoated) outer layers, roughly:

| Voltage between conductors | Minimum spacing |
|---|---|
| up to 30 V | 0.10 mm |
| up to 100 V | 0.60 mm |
| up to 300 V | 1.25 mm |
| up to 500 V | 2.50 mm |

These numbers are a simplified summary for teaching; the standard has more categories (inner layers, coated boards, altitude). For mains voltages, safety standards such as IEC 62368-1 require much larger "creepage" and "clearance" distances, often several millimetres. In this course we stay at 12 V or less, so the factory rule (0.15 mm) always wins over the voltage rule (0.10 mm), but the checker should still know about it.

### Electrical rules

Some rules come from the circuit itself. "Every power pin gets a 100 nF capacitor within 3 mm", "power nets at least 0.5 mm wide", "this pair of traces must have equal length" are all electrical rules. EDA tools can check many of them (netclass widths, lengths), and the rest you check with simulation. At the end of this lesson we turn the decoupling lesson of Lesson 03 into a rule with a number in it: no supply sags more than 150 mV when a load switches on.

## The Concept

### A geometry everyone can compute: capsules

A trace is a line segment (its centre line) with a width. If you draw every point within `width/2` of the centre line, you get a shape like a sausage: a rectangle with round ends. We call that a **capsule**. A round pad or a via is a capsule of zero length (a circle). Square pads are not capsules, but for this lesson we approximate them as circles of the same width; real DRC engines handle every shape exactly.

The great thing about capsules is that the gap between two of them is easy:

```
gap = (distance between the two centre-line segments) - radius1 - radius2
```

"The copper gap is the distance between the two centre lines, minus half of each width." If the result is negative, the copper overlaps.

```
         <-- 0.5 mm wide -->
   ======================================   trace A, centre line at y = 0.00
   ======================================
                  ^
                  |  copper gap = 0.60 - 0.25 - 0.25 = 0.10 mm
                  v
   ======================================   trace B, centre line at y = 0.60
   ======================================
```

### Distance between two segments

The distance from a point P to a segment AB is found by projecting P onto the line through A and B, clamping the projection to the segment, and measuring:

```
t = ((P - A) . (B - A)) / |B - A|^2        "how far along AB the closest point is" (0 to 1)
t = clamp(t, 0, 1)
closest = A + t (B - A)
distance = |P - closest|
```

The `.` is the dot product: `(x1, y1) . (x2, y2) = x1 x2 + y1 y2`. For two segments that do not cross, the shortest distance is always achieved at an end point of one of them, so we take the smallest of the four point-to-segment distances. If they cross, the distance is zero.

Worked example: P = (5, 1), A = (0, 0), B = (10, 0). `P - A = (5, 1)`, `B - A = (10, 0)`, dot product = 50, `|B - A|^2 = 100`, so `t = 0.5`, the closest point is (5, 0) and the distance is 1.

### The rules our checker enforces

| Rule | Value | Applies to |
|---|---|---|
| minimum trace width | 0.15 mm | every trace |
| minimum clearance | 0.15 mm, or the voltage table if larger | every pair of items on different nets |
| minimum drill | 0.30 mm | every via |
| minimum annular ring | 0.15 mm, i.e. `(pad diameter - drill) / 2` | every via |
| board edge clearance | 0.30 mm, measured from the copper edge | every item |

Annular ring example: a via with a 0.45 mm pad and a 0.20 mm drill has a ring of `(0.45 - 0.20) / 2 = 0.125 mm`. That breaks two rules at once: the drill is below 0.30 mm and the ring is below 0.15 mm.

Edge example: a 0.5 mm trace whose centre line ends 0.2 mm from the edge has its copper `0.2 - 0.25 = -0.05 mm` from the edge, that is, 0.05 mm of copper hangs over the outline.

### Clearance between every pair

The checker compares every item with every other item on a different net. With N items that is `N (N - 1) / 2` pairs: 7 items give 21 pairs, but a real board with 20,000 track segments would give 200 million. Real DRC engines first sort items into a grid or a tree of boxes and only compare neighbours. For our tiny boards the simple double loop is fine.

### The decoupling rule as a simulation

From Lesson 03 we know the droop after a current step `I` through a supply inductance `L` with a capacitor `C` is about `I * sqrt(L / C)`. If the rule is "at most 150 mV", then

```
sqrt(L / C) <= 0.150 V / 1 A = 0.15 Ω
L / C <= 0.0225
C >= L / 0.0225 = 0.5e-6 / 0.0225 = 22 µF
```

So we need at least about 22 µF; from the values in our drawer (1, 10 and 100 µF), 100 µF. The estimate ignores the small resistance of the leads, so we confirm it with the simulator in the lab.

## Build It

Run:

```
uv run python phases/21-pcb-design-and-manufacturing/04-design-rules/code/main.py
```

### Step 1: The rules as data

```python
RULES = {
    "min_trace_width": 0.15,
    "min_clearance": 0.15,
    "min_drill": 0.30,
    "min_annular_ring": 0.15,
    "edge_clearance": 0.30,
}

VOLTAGE_CLEARANCE_OUTER = [(30, 0.10), (100, 0.60), (300, 1.25), (500, 2.50)]
```

Keeping rules as data, not buried in code, is exactly what EDA tools do: you load the factory's rule file and the checker uses it.

### Step 2: Capsules and gaps

```python
@dataclass
class Capsule:
    kind: str
    name: str
    net: str
    start: tuple
    end: tuple
    radius: float


def gap(x, y):
    return segment_distance(x.start, x.end, y.start, y.end) - x.radius - y.radius
```

`trace(...)`, `pad(...)` and `via(...)` are small helpers that build capsules (a via also remembers its drill). `segment_distance` uses `point_segment_distance` four times and a crossing test, as described above. The script checks the example from the drawing: two 0.5 mm traces with centre lines 0.6 mm apart have a 0.10 mm copper gap.

### Step 3: The checker

```python
def drc(items, board_w, board_h, net_volts):
    errors = []
    for item in items:
        if item.kind == "trace" and 2 * item.radius < RULES["min_trace_width"] - 1e-9:
            errors.append(...)
        if item.kind == "via":
            ...drill and annular ring...
        ...edge clearance at both ends...
    for i, x in enumerate(items):
        for y in items[i + 1:]:
            if x.net == y.net:
                continue
            needed = max(RULES["min_clearance"], voltage_clearance(abs(net_volts[x.net] - net_volts[y.net])))
            g = gap(x, y)
            if g < needed - 1e-9:
                errors.append(...)
    return errors
```

The tiny `1e-9` tolerance avoids flagging a gap of exactly 0.15 mm because of rounding in floating-point arithmetic.

The first layout is a 20 x 10 mm board with a 12 V input (VIN), ground (GND) and a 3.3 V signal (SIG). The checker prints:

```
  ERROR T2: width 0.10 mm < 0.15 mm
  ERROR V1: drill 0.20 mm < 0.3 mm
  ERROR V1: annular ring 0.12 mm < 0.15 mm
  ERROR T4: -0.05 mm from the board edge < 0.3 mm
  ERROR T1 (VIN) to T2 (SIG): gap 0.10 mm < 0.15 mm
  ERROR T2 (SIG) to T4 (VIN): gap 0.10 mm < 0.15 mm
  6 violations
```

### Step 4: Fix and re-check

The fixed layout widens T2 to 0.20 mm and moves it away from T1, uses a 0.30 mm drill with a 0.60 mm via pad, and stops T4 1 mm from the edge. The checker prints `0 violations`. This loop (check, fix, check again) is how every real layout is finished.

### Step 5: The electrical rule

```python
task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
for part in task["parts"]:
    result = evaluate(task, {"S1": part})[0]
```

`sim.lab.evaluate` builds the lab circuit with the chosen capacitor, runs the transient simulation and measures the lowest `vdd`. Output: 4.356 V for 1 µF, 4.774 V for 10 µF and 4.917 V for 100 µF; only 100 µF keeps the droop under 150 mV.

## Use It

- **Get the fab's rules first.** Every factory publishes its capabilities: minimum trace/space, drill, annular ring, solder mask sliver, silkscreen line width, edge clearance. Load them into your EDA tool before you start routing. KiCad's "Board Setup > Design Rules" and its custom rules language serve exactly this purpose.
- **Design looser than the minimum.** If the factory can do 0.127 mm, design at 0.15-0.2 mm where you can. Yield is better and you can switch factories.
- **Netclasses.** Give power nets a wider default width, high-voltage nets a bigger clearance, and fast signals their own rules. The checker then applies the right rule automatically.
- **Electrical rules check (ERC)** in the schematic is the cousin of DRC: it flags outputs driving outputs, unconnected pins and power pins with no source.
- **DRC is necessary, not sufficient.** A board with zero DRC errors can still have a decoupling capacitor 30 mm from its chip or a ground plane cut in half. Review those by eye and by simulation.

## Try It in the Lab

Open "Follow the decoupling rule". The rule says no supply may sag more than 150 mV, so `vdd` must stay at or above 4.85 V when a 1 A load switches on through leads with 0.5 µH. Choose the capacitor. Use the estimate `I * sqrt(L/C)` for each capacitor before running, and compare your estimates with the simulated minimum. Why does the simulated dip come out a little deeper than the estimate for the large capacitor?

## Common Mistakes

- **Designing at the factory's absolute minimum everywhere.** It works but costs yield; use the minimum only where you must (between fine-pitch pins).
- **Forgetting the annular ring.** A via is defined by two numbers, pad and drill. Shrinking the pad to squeeze a via in can break the ring rule.
- **Measuring centre lines instead of copper.** Clearance is copper edge to copper edge: subtract half of each width.
- **Ignoring voltage.** Two traces at 0.15 mm are fine at 5 V and dangerous at 230 V. High-voltage nets need their own netclass.
- **Treating DRC as a formality.** Read every error. "Waiving" a clearance error without understanding it is how shorts reach production.

## Exercises

1. A via has a 0.35 mm drill and a 0.60 mm pad. What is its annular ring? Does it meet our rules?
2. Two parallel 0.25 mm traces have centre lines 0.45 mm apart. What is the copper gap? Which rule does it break, if any?
3. Using the segment distance method, find the distance from P = (3, 4) to the segment from (0, 0) to (6, 0), and from P = (8, 1) to the same segment.
4. Add a net "HV" at 48 V to `net_volts` in the script and a trace on it 0.4 mm (copper gap) from a ground trace. What does the checker report, and why?
5. Harder: the decoupling rule tightens to 100 mV. Using `C >= L / (droop / I)^2`, what capacitance do you need? Add that part to a copy of the lab task and check it with `uv run python -m sim.lab`.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Design rules | "the fab's limits" | Minimum widths, gaps, drills and rings (plus your own electrical rules) that every piece of copper must meet |
| DRC | "run the checker" | Software that measures every item and pair of items against the rules |
| Clearance | "spacing" | Copper-edge-to-copper-edge distance between different nets, larger for higher voltages |
| Annular ring | "the via ring" | `(pad diameter - drill) / 2`, the copper left around a hole after drilling |
| Trace/space | "6/6" | The minimum trace width and gap, often quoted in mils |
| Creepage | "surface distance" | The distance along the surface between conductors; matters for high voltage and dirty, damp boards |

## Further Reading

- IPC-2221B, *Generic Standard on Printed Board Design* ([ipc.org](https://www.ipc.org/)) — the clearance table and many other rules.
- [KiCad documentation: Board Setup and Custom Design Rules](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html) — how a real tool stores and checks rules.
- The capabilities pages of low-cost PCB factories (JLCPCB, PCBWay, OSH Park) — compare their minimum trace/space, drill and ring values.
