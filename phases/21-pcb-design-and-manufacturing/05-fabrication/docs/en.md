# Fabrication

> A factory turns your Gerber files into copper with light, drills and chemistry. Knowing how it works tells you what it can and cannot make, and what it costs.

**Type:** Learn
**Prerequisites:** Phase 21 (PCB Design and Manufacturing), Lessons 01-04; Phase 03 (Resistance and Ohm's Law), Lesson 02 (Resistivity and Wires)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Laminate (copper-clad) | A sheet of FR-4 with copper foil glued to both faces, the raw material of a board | Plywood with a metal skin |
| Prepreg | Glass cloth soaked in half-cured resin, used as glue between layers of a multilayer board | Sticky tape between sheets |
| Panel | A large sheet on which many copies of a board are made at once | A baking tray of biscuits |
| Photoresist | A light-sensitive film that hardens where UV light hits it and protects the copper underneath | A stencil made with light |
| Etching | Dissolving the copper that is not protected | Washing away the sand around a sandcastle |
| Undercut / etch factor | Etching also eats sideways under the edges of the resist; the etch factor says how much less sideways than down | Water eroding a river bank under its edge |
| Plating | Depositing copper inside drilled holes with electricity, so the hole connects the layers | Painting the inside of a pipe |
| Surface finish | A thin coating on the bare pads (solder, gold, or organic) that stops them oxidising | Varnish on bare wood |
| Electrical test | Checking every net of every board for opens and shorts before shipping | Testing every light switch in a new house |
| NRE / setup cost | The one-off cost of preparing an order, paid once no matter how many boards | The cost of setting up the printing press |
| Yield | The fraction of boards that come out good | The share of biscuits that are not burnt |
| Stack-up | The order and thickness of copper and insulating layers in a multilayer board | The layers of a club sandwich |

## Learning Objectives

- Describe, in order, the steps that turn a copper-clad laminate into a finished printed circuit board.
- Explain why etching narrows traces, and estimate the final width of a trace from its drawn width, copper thickness and etch factor.
- Compute how many boards fit on a production panel, and why board shape changes the waste.
- Use a simple cost model to see why the price per board falls so steeply with quantity and rises with layer count.
- Estimate the resistance of a plated via and simulate how current shares between vias in parallel.

## The Problem

You send your Gerber files to a factory and ten days later a parcel arrives with five shiny green boards. What happened in between? It matters for three practical reasons.

First, **what can be made**: the design rules of Lesson 04 are not arbitrary; each one is a limit of a specific step (photo imaging, etching, drilling, plating). Knowing the steps, you can guess why a factory refuses a 0.1 mm trace in 2 oz copper but accepts it in 1 oz.

Second, **what it costs**: five boards for a few dollars, or five hundred for less than a dollar each, or a 6-layer board for ten times more. The cost model is simple once you see it.

Third, **what can go wrong**: a via that is not plated properly, a trace that is etched thinner than you drew it, a board that is too big and has a low yield. Bring-up (Lesson 07) is easier if you know where defects come from.

## The Physics

### Light makes the pattern

The pattern of copper is printed with light, as in old film photography. The copper is covered with **photoresist**, a polymer that changes when ultraviolet (UV) light hits it. A mask or a laser direct-imaging machine shines UV only where copper should stay. The exposed resist hardens; the unexposed resist is washed off in a developer. Now the copper that should become traces is covered, and the rest is bare.

### Chemistry removes copper

The board then goes through an **etchant**, a chemical solution (for example cupric chloride or ammoniacal etchant) that dissolves copper. The bare copper disappears; the copper under the hardened resist survives. Then the resist is stripped off.

Etching is not perfectly vertical. While the etchant works its way down through the 35 µm of copper, it also eats sideways under the edges of the resist:

```
         resist              resist
       +--------+          +--------+
       |########|          |########|
        \ copper/  etched   \      /
         \     /   away      \    /
   ======================================  FR-4
```

The **etch factor** is the ratio of depth etched to sideways undercut. With an etch factor of 3, etching through 35 µm of copper also eats about `35 / 3 = 11.7 µm` from each side. A trace drawn 150 µm wide comes out about

```
150 - 2 * 11.7 = 126.7 µm
```

Twice as thick copper (70 µm) means twice the undercut: the same drawing ends at about 103 µm. That is why factories demand bigger minimum widths and gaps for thicker copper, and why they quietly widen your traces in their own copy of the artwork ("etch compensation") so that the final width matches what you drew.

### Electricity plates the holes

A drilled hole through FR-4 is just a hole through an insulator. To make it connect the top and bottom copper, its wall must be coated with copper. First a very thin conductive seed layer is deposited chemically (electroless copper). Then the whole panel is put in a copper sulphate bath as the negative electrode of an electrolysis cell: copper ions are pulled out of the solution onto every conducting surface, including the hole walls, building up about 20-25 µm of copper. This is the same electrochemistry as in Phase 06, Lesson 03, run in reverse: we push current *in* to deposit metal.

A plated via is therefore a tiny copper tube. Its resistance follows the usual formula, with the cross-section of the tube wall:

```
A ≈ pi * (drill - plating) * plating          (a thin tube, unrolled)
R = rho * board thickness / A
```

For a 0.3 mm drill, 25 µm plating and a 1.6 mm thick board: `A = pi * 0.275e-3 * 25e-6 = 2.16e-8 m^2`, so `R = 1.72e-8 * 1.6e-3 / 2.16e-8 = 1.27 mΩ`. Tiny, but the tube has little surface to shed heat, so designers use a rule of thumb of about 1 A per small via and put several in parallel for power.

## The Concept

### The sequence for a two-layer board

```
  1. cut laminate      FR-4 with copper on both faces, cut to panel size
  2. drill             every hole, by CNC drill (or laser for micro-vias)
  3. plate             seed copper, then electroplate the hole walls (~25 um)
  4. image             photoresist + UV pattern
  5. etch              dissolve unprotected copper, strip the resist
  6. solder mask       liquid photo-imageable varnish, opened over the pads
  7. silkscreen        print the legend
  8. surface finish    HASL (hot-air solder levelling), ENIG (nickel + thin gold) or OSP
  9. electrical test   flying probe or bed of nails, every net
 10. rout              mill each board out of the panel
```

A **multilayer** board adds steps at the start: the inner layers are imaged and etched first, then stacked with sheets of prepreg and outer copper foil, and pressed under heat until the resin cures into one solid block. Only then are the through-holes drilled and plated, so they connect all layers. A four-layer board's typical stack-up:

```
   top copper (signals)          35 um
   prepreg                       ~0.2 mm
   inner 1 (ground plane)        35 um
   core                          ~1.1 mm
   inner 2 (power plane)         35 um
   prepreg                       ~0.2 mm
   bottom copper (signals)       35 um
                                 total ~1.6 mm
```

That thin prepreg between the top signals and the ground plane is the 0.2 mm that made return paths so good in Lesson 03.

### Panels and waste

Factories work with big panels, for example 457 x 610 mm (18 x 24 inches). Your board is copied as many times as fits, with a margin around the panel edge (for handling and test coupons) and a gap between copies for the milling bit. How many 50 x 50 mm boards fit with a 10 mm margin and 2 mm gaps?

```
usable width  = 457 - 2 * 10 = 437 mm      across = floor((437 + 2) / (50 + 2)) = floor(8.44) = 8
usable height = 610 - 2 * 10 = 590 mm      down   = floor((590 + 2) / (50 + 2)) = floor(11.38) = 11
total = 8 * 11 = 88 boards
```

Those 88 boards use `88 * 2500 / (457 * 610) = 78.9%` of the panel; the rest is margin, gaps and leftover strips. A board size that divides the panel badly wastes more. Low-cost "prototype" services combine many customers' boards on one shared panel, which is why they are so cheap for small quantities.

### Cost: a fixed part and a per-area part

A useful toy model of the price of an order:

```
total = setup * layer_factor + quantity * area * price_per_area * layer_factor
```

Read it as: "there is a fixed setup cost (preparing the files, tooling, test programme) and a cost proportional to the total area of copper-clad board you use; more layers multiply both". Our toy numbers: $30 setup, $0.012 per cm², and a layer factor of 1 for 2 layers, 2.2 for 4, 3.5 for 6. They are made up but have the right shape.

For a 50 x 50 mm (25 cm²) two-layer board:

```
5 boards:    30 + 5 * 25 * 0.012    = 30 + 1.5  = $31.50  -> $6.30 each
500 boards:  30 + 500 * 25 * 0.012  = 30 + 150  = $180    -> $0.36 each
```

The per-board price falls from $6.30 to $0.36 because the setup is shared among more boards. For very large quantities the price per board approaches `area * price_per_area` = $0.30. This "fixed cost plus per-unit cost" shape appears everywhere in manufacturing; in Phase 20, Lesson 09 the same reasoning decides between an FPGA and a custom chip.

### Yield

Defects (a scratch, a speck of dust in the imaging, a void in a plated hole) land randomly on the panel. If they land at an average density `D` per unit area, the chance that a board of area `A` has none is given by the Poisson formula

```
yield = exp(-D * A)
```

"the probability of zero defects is e to the minus (defect density times area)". With `D = 0.05` defects per square decimetre (1 dm² = 100 cm²): a 50 x 50 mm board (0.25 dm²) has yield `exp(-0.0125) = 98.8%`, a 200 x 200 mm board (4 dm²) `exp(-0.2) = 81.9%`. Bigger boards are not only more expensive by area, they also fail more often. Factories electrically test every board and throw away the bad ones, so you rarely see this as a customer, but you pay for it in the price. The same formula is central to chip manufacturing (Phase 20, Lesson 11), where it makes very large chips extremely expensive.

## Build It

Run:

```
uv run python phases/21-pcb-design-and-manufacturing/05-fabrication/code/main.py
```

### Step 1: The sequence

The script prints the ten steps with a short note each, the same list as above.

### Step 2: Panelization

```python
def boards_per_panel(board_w, board_h, panel_w=457.0, panel_h=610.0, margin=10.0, spacing=2.0):
    usable_w = panel_w - 2 * margin
    usable_h = panel_h - 2 * margin
    best = 0
    for w, h in ((board_w, board_h), (board_h, board_w)):
        across = int((usable_w + spacing) // (w + spacing))
        down = int((usable_h + spacing) // (h + spacing))
        best = max(best, across * down)
    return best
```

The function tries both orientations and keeps the better one. Output: 88 boards of 50 x 50 mm (78.9% of the panel), 28 of 100 x 80 mm (80.4%), 12 of 160 x 100 mm (68.9%) and 529 of 23 x 17 mm (74.2%).

### Step 3: Cost versus quantity

```python
def order_cost(quantity, board_w, board_h, layers=2, setup=30.0, per_cm2=0.012):
    area_cm2 = board_w * board_h / 100
    layer_factor = {2: 1.0, 4: 2.2, 6: 3.5}[layers]
    return setup * layer_factor + quantity * area_cm2 * per_cm2 * layer_factor
```

Output for 2 layers: $6.30, $0.90, $0.36 and $0.306 per board for 5, 50, 500 and 5000 boards. Four layers cost 2.2 times more at every quantity.

### Step 4: Yield

`board_yield` is `exp(-D * A)` with the area in dm². The script prints 98.8%, 95.1% and 81.9% for 50, 100 and 200 mm square boards.

### Step 5: Etching

```python
def etched_width(drawn_width_um, copper_um=35.0, etch_factor=3.0):
    undercut_each_side = copper_um / etch_factor
    return drawn_width_um - 2 * undercut_each_side
```

A 100 µm line drawn in 70 µm copper comes out at only 53 µm: that is why such a combination is refused.

### Step 6: Vias in the simulator

```python
def current_through_vias(count, amps=3.0):
    r_via = via_resistance()
    c = Circuit()
    c.current_source("I1", "0", "top", amps)
    for n in range(count):
        c.resistor(f"VIA{n + 1}", "top", "0", r_via)
    r = c.dc()
    return r.v("top"), r.i("VIA1"), r.p("VIA1")
```

A current source pushes 3 A from the bottom layer to the top through `count` vias in parallel. Each via is a 1.27 mΩ resistor. With one via the drop is 3.8 mV and the via dissipates 11.5 mW; with four, each carries 0.75 A and only 0.7 mW (the power per via falls with the square of its current). The drop is never the problem; heat in the thin barrel and the risk of a single bad via are, which is why power paths use several.

## Use It

- **Ordering a prototype.** Online fabs ask for: number of layers, board thickness (1.6 mm default), copper weight (1 oz default), solder mask colour, surface finish (HASL is cheapest; ENIG gives flat pads for fine-pitch parts), minimum trace/space and drill. The defaults are the cheap path.
- **Gerber X2 and drill files.** You upload one Gerber file per copper layer, solder mask, paste and silkscreen layer, plus an Excellon drill file. Most fabs show a preview: always look at it.
- **Panelization for assembly.** If boards are to be assembled by machine, you often order them in a small panel with breakaway tabs ("mouse bites") or V-grooves, plus fiducial marks for the camera of the pick-and-place machine.
- **Test coupons.** The strips at the panel edge carry test patterns the factory cuts and examines (for example, a cross-section through plated holes to measure plating thickness).
- **Environmental notes.** Etchants and plating baths are hazardous chemicals; that is one reason home etching has largely been replaced by cheap professional services.

## Common Mistakes

- **Choosing thick copper without updating rules.** 2 oz copper needs bigger minimum width and gap. Change your rules before routing, not after the factory rejects the files.
- **Odd board sizes for volume production.** A board that is just too large to fit an extra row on the panel can cost 20-30% more. Check panel utilisation before freezing the outline.
- **Forgetting that every extra layer multiplies cost.** Use four layers when you need them (fast signals, dense routing), not by habit.
- **Too few vias on power paths.** One via for an amp-level current concentrates heat and creates a single point of failure.
- **Not checking the fab's preview.** A missing drill file or a mirrored layer is obvious in the preview and expensive afterwards.

## Exercises

1. A 0.2 mm (200 µm) trace is drawn in 1 oz copper and etched with an etch factor of 2.5. What final width do you expect?
2. How many 80 x 60 mm boards fit on a 457 x 610 mm panel with a 10 mm margin and 2 mm spacing? Try both orientations by hand, then check with the script.
3. Using the toy cost model, at what quantity does the per-board price of a 50 x 50 mm two-layer board fall below $0.50?
4. With a defect density of 0.05 per dm², what is the yield of a 300 x 300 mm board? What defect density would give that board a 95% yield?
5. Harder: model a via with poor plating (10 µm instead of 25 µm). How does its resistance change? Modify `current_through_vias` so that two vias are good and one is poorly plated, and find how 3 A shares among them.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Etching | "the copper is removed" | Chemical dissolution of copper not covered by hardened photoresist; it undercuts the edges |
| Etch compensation | "the fab adjusts widths" | The factory widens drawn features so the final etched width matches the design |
| Plated through-hole | "a via" | A drilled hole whose wall is electroplated with about 25 µm of copper to join layers |
| Panel | "the production sheet" | A large laminate on which many boards are made together and then cut out |
| Setup cost | "the engineering fee" | Fixed cost of an order, independent of quantity |
| Yield | "the good ones" | Fraction of boards without defects, about `exp(-D * A)` for random defects |
| Stack-up | "the layer build" | The sequence and thickness of copper and dielectric layers |

## Further Reading

- Clyde F. Coombs and Happy T. Holden, *Printed Circuits Handbook*, 7th ed. (McGraw-Hill, 2016) — the reference on every fabrication step.
- IPC-6012, *Qualification and Performance Specification for Rigid Printed Boards* ([ipc.org](https://www.ipc.org/)) — what "a good board" means, including plating thickness.
- The "how PCBs are made" pages and factory-tour videos published by PCB manufacturers such as Eurocircuits and JLCPCB.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., section on PCB fabrication.
