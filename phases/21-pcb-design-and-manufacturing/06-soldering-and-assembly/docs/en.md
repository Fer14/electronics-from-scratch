# Soldering and Assembly

> Solder is a metal glue that only works if both surfaces get hot enough. Assembly is mostly the art of moving heat to the right place.

**Type:** Build
**Prerequisites:** Phase 21 (PCB Design and Manufacturing), Lessons 01-05; Phase 07 (Capacitors), Lesson 04 (The Time Constant); Phase 18 (Power Electronics), Lesson 07 (Heat and Thermal Design)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Solder | A metal alloy with a low melting point that wets copper and joins it when it solidifies | Hot glue, but metal |
| Wetting | Molten solder spreading over and bonding to a clean metal surface | Water spreading on clean glass instead of beading up |
| Intermetallic | The thin layer of new tin-copper compound that forms where solder meets copper; it is the real bond | The roots that hold a plant in the soil |
| Flux | A chemical that removes oxide from metal surfaces so solder can wet them | Soap that lets water reach the dirt |
| Solidus / liquidus | The temperature where an alloy starts to melt / is fully liquid | When butter starts to soften / is completely runny |
| Eutectic | An alloy that melts at a single temperature (solidus = liquidus) | Ice, which melts all at once at 0 °C |
| Solder paste | Tiny solder balls mixed with flux into a grey paste | Toothpaste with metal beads |
| Stencil | A thin metal sheet with holes where paste should be printed | A spray-paint stencil |
| Pick-and-place | A machine that picks parts from reels and places them on the pasted pads | A very fast robot hand |
| Reflow oven | An oven with several heating zones that melts the paste on every joint at once | A tunnel-shaped toaster with a conveyor belt |
| Reflow profile | The temperature-versus-time curve the board follows through the oven | A recipe: "bake at 180 for 2 minutes, then 245 for 30 seconds" |
| Thermal mass | How much heat a part needs to warm up by one degree (heat capacity) | A big pot of water takes longer to boil than a cup |
| Thermal relief | Thin copper spokes joining a pad to a plane so the plane cannot steal heat too fast | A narrow bridge to an island |
| Cold joint | A joint where the solder never properly wetted one surface; it may look dull and crack later | Glue that sat on dust instead of on the surface |
| Tombstoning | A two-pad part standing up on one end because one side melted first | A gravestone standing on its end |

## Learning Objectives

- Explain what happens physically when solder wets copper, and why flux and enough heat are both necessary.
- Compare common solder alloys by their melting ranges, and say why lead-free soldering runs hotter.
- Compute the paste volume printed through a stencil and check the area-ratio rule for good paste release.
- Model the temperature of a part in a reflow oven with a first-order thermal time constant, and see why big parts lag behind small ones.
- Use the thermal-electrical analogy to simulate a soldering iron on a pad connected to a ground plane, and size a thermal relief so the joint melts.

## The Problem

Your boards are back from the factory: bare copper (with a surface finish) and holes, but no parts. Now the parts have to be attached. For a handful of prototypes, you solder by hand with an iron. For hundreds, a machine prints solder paste, places parts and runs the boards through a reflow oven.

Both methods fail in the same way when the heat goes wrong. You press the iron on the ground pad of a connector, wait ten seconds, and the solder just sits there as a dull blob: the ground plane is pulling the heat away faster than the iron can supply it. In the oven, the tiny resistors are perfectly soldered but the big connector next to them has cold joints, because it never got hot enough for long enough. A small resistor stands up on one end like a tombstone because its two pads melted at different moments.

All of these are heat-flow problems, and heat flow follows exactly the same mathematics as current in a resistor-capacitor circuit. So we can use our circuit simulator to design for it.

## The Physics

### What a solder joint really is

Solder is not a glue that sticks to the surface. When molten tin touches clean copper, some atoms of each dissolve into the other and form a thin layer of new compounds (mostly Cu6Sn5), only a few micrometres thick. This **intermetallic** layer is what holds the joint together and conducts the current. For it to form, two things are needed:

1. **A clean metal surface.** Copper exposed to air grows a thin oxide in minutes. Molten solder cannot wet oxide; it beads up like water on a greasy pan. **Flux** is a mild acid (often based on rosin from pine trees) that dissolves the oxide when heated and protects the surface while the solder flows.
2. **Enough heat on both surfaces.** The solder must be liquid, and the copper pad *and* the part's lead must be above the solder's melting point, or the solder freezes as soon as it touches them. A joint where the solder touched a surface that was too cold is a **cold joint**: it looks dull or lumpy and may have a high resistance or crack later.

### Alloys and their melting points

| Alloy | Melts (solidus / liquidus) | Notes |
|---|---|---|
| Sn63Pb37 (63% tin, 37% lead) | 183 / 183 °C | eutectic: melts at one temperature; easy to use; contains lead |
| SAC305 (96.5% tin, 3% silver, 0.5% copper) | 217 / 220 °C | the common lead-free alloy |
| Sn99.3Cu0.7 | 227 °C | cheap lead-free alloy for wave soldering |

Since 2006, the European RoHS directive restricts lead in most consumer electronics, so production uses lead-free alloys that melt about 35 °C higher. That means hotter irons and ovens, and less margin before parts and boards are damaged (many parts are rated for a peak of 260 °C for a few seconds). Lead is toxic: if you use leaded solder at home, wash your hands and do not eat at the bench.

### Heat flow behaves like current

Heat flows from hot to cold, and the rate depends on how good the path is. This is the same structure as Ohm's law, and engineers use it directly (Phase 18, Lesson 07):

| Thermal quantity | Unit | Electrical twin |
|---|---|---|
| temperature difference | K (or °C) | voltage |
| heat flow | W | current |
| thermal resistance | K/W | resistance |
| heat capacity (thermal mass) | J/K | capacitance |

A thermal resistance of 15 K/W means "for every watt flowing through it, the two ends differ by 15 °C". A heat capacity of 0.02 J/K means "it takes 0.02 joules to warm it by one degree". A part with heat capacity `C` heated through thermal resistance `R` from a hotter environment warms up exponentially with time constant `tau = R * C`, exactly like a capacitor charging through a resistor (Phase 07, Lesson 04):

```
dT/dt = (T_environment - T) / tau
```

"the temperature changes at a rate proportional to how far it is from the surroundings, divided by the time constant". Big parts have more heat capacity, so a bigger `tau`, so they lag behind.

## The Concept

### Assembly by machine: paste, place, reflow

```
  1. stencil print     a squeegee pushes paste through a 0.1-0.15 mm thick steel stencil
  2. pick-and-place    nozzles pick parts from tape reels and place them on the paste
  3. reflow            the board rides a conveyor through heating zones; the paste melts
  4. inspection        automatic optical inspection (AOI), X-ray for hidden joints (BGA, QFN)
  5. through-hole      wave soldering or selective soldering for the remaining THT parts
  6. test              in-circuit or functional test (Lesson 07)
```

### Paste volume and the area-ratio rule

The paste printed on a pad is the stencil aperture area times the stencil thickness. Solder paste is about half metal and half flux by volume, so the joint will have about half that volume of solder. For an 0603 pad of 0.8 x 0.9 mm and a 0.12 mm stencil:

```
volume = 0.8 * 0.9 * 0.12 = 0.0864 mm^3 = 86.4 nL (nanolitres)
```

Will the paste come out of the hole? When the stencil lifts, the paste is pulled down by the pad (area of the opening) and held back by the walls of the hole (area of the four walls). The common rule is that the **area ratio** should be at least about 0.66:

```
area ratio = aperture area / wall area = (w * l) / (2 * (w + l) * thickness)
```

For a fine-pitch QFN pin of 0.25 x 0.70 mm: `0.175 / (2 * 0.95 * 0.12) = 0.175 / 0.228 = 0.77`, which passes, but only just. A thinner stencil or wider aperture improves it; that is why boards with very fine-pitch parts use 0.1 mm stencils.

### The reflow profile

A lead-free profile has four phases:

```
 temp (C)
  250 |                          ____
      |                         /    \        peak 235-250 C
  217 |- - - - - - - - - - - - /- - - -\- - -  liquidus: time above it 60-90 s
  190 |              _________/          \
  150 |        _____/  soak                \
      |       /                              \  cooling
   25 |______/                                \______
      +-----------------------------------------------> time (s)
        preheat        soak        reflow      cool
        (1-3 C/s)    (60-120 s)    (peak)
```

- **Preheat** warms the board gently (1-3 °C/s) so nothing cracks from thermal shock.
- **Soak** holds 150-190 °C so that big and small parts approach the same temperature and the flux activates.
- **Reflow** lifts everything above the liquidus for about 60-90 s, with a peak around 240-250 °C.
- **Cooling** freezes the joints with a fine grain structure.

Our oven model is a list of (time, air temperature) points: 25 °C at 0 s, 150 °C at 60 s, 190 °C at 150 s, 250 °C from 200 to 230 s, then cooling. A small part (tau = 15 s) follows the air closely: peak 247.7 °C, 64 s above 217 °C. A big connector (tau = 45 s) lags: peak only 228.6 °C, 41 s above 217 °C, short of the 60 s target. This is the main reason ovens use long soak phases and why profiles are tuned with thermocouples glued to the biggest part on the board.

Tombstoning is the same effect at small scale: if one pad of an 0402 resistor is joined to a big plane and the other to a thin trace, the thin side melts first, its surface tension pulls, and the part stands up.

### The soldering iron and the ground plane

Now model a hand-soldered ground pad as a thermal circuit. We measure temperatures **above room temperature** so that "ground" in the circuit means 25 °C:

```
   IRON 325 (350 C tip) --- R_TIP 15 K/W ---+--- joint ---- S1 (pad-to-plane link) ---+--- plane
                                            |                                         |
                                       C_JOINT 0.02 J/K                    C_PLANE 3 J/K   R_PLANE 10 K/W
                                            |                                         |          |
   room (25 C) -----------------------------+-----------------------------------------+----------+
```

- The iron tip is a "voltage source" of 325 (it is at 350 °C, 325 above room).
- Heat reaches the joint through the solder bridge between tip and pad: 15 K/W.
- The joint (pad + lead + a bit of solder) has a small heat capacity, 0.02 J/K.
- The pad connects to the ground plane through slot S1. A solid connection is about 2 K/W; four wide spokes about 8 K/W; four thin spokes about 25 K/W.
- The plane is a large heat capacity (3 J/K) that loses heat to the air through 10 K/W.

For the first seconds, the big plane barely warms, so it acts like a short to room temperature. The joint then sits on a **voltage divider** (Phase 04, Lesson 05):

```
T_joint above room ≈ 325 * R_link / (15 + R_link)

solid (2 K/W):     325 * 2 / 17   =  38  -> about  63 C   (never melts)
wide (8 K/W):      325 * 8 / 23   = 113  -> about 138 C   (never melts)
thin (25 K/W):     325 * 25 / 40  = 203  -> about 228 C   (melts!)
```

SAC305 needs 217 °C (192 above room), so only the thin relief lets the joint melt. The joint reaches that quasi-steady value with a time constant of `C_JOINT * (15 || R_link)` = `0.02 * 9.4 = 0.19 s` for the thin relief, so it melts in about half a second. Then, slowly, the plane warms and everything creeps up.

That is exactly why EDA tools add **thermal reliefs** to pads in copper pours by default. The price is a little more electrical resistance: each spoke is a short, narrow trace, so for high-current pads you check the spokes with the trace rules of Lesson 02 (or use more and wider spokes and a hotter iron).

### Cracked and cold joints are resistors

A good joint has a resistance of about a milliohm. A cracked or cold joint can be anything from a few ohms to an open circuit, and it often changes with temperature and vibration (the classic intermittent fault). In series with our USB LED from Lesson 01, a 100 Ω joint drops the LED current from 9.55 mA to 7.4 mA, and a 1 kΩ joint to 2.4 mA: the LED is dim but "works", which makes the fault confusing until you measure.

## Build It

Run:

```
uv run python phases/21-pcb-design-and-manufacturing/06-soldering-and-assembly/code/main.py
```

### Step 1: Alloys

A table of the three alloys and their solidus and liquidus temperatures.

### Step 2: Paste volume and area ratio

```python
def paste_volume(width_mm, length_mm, stencil_mm=0.12):
    aperture = width_mm * length_mm
    walls = 2 * (width_mm + length_mm) * stencil_mm
    return aperture * stencil_mm, aperture / walls
```

Output: 36.0 nL for an 0402 pad, 86.4 nL for 0603, 156 nL for 0805 and 21 nL for a QFN pin with an area ratio of 0.77.

### Step 3: The reflow oven

```python
def reflow(tau_s, dt=0.1, t_end=330.0):
    t = np.arange(0.0, t_end + dt, dt)
    temp = np.empty_like(t)
    temp[0] = AMBIENT_C
    for n in range(1, len(t)):
        temp[n] = temp[n - 1] + dt * (oven_temperature(t[n - 1]) - temp[n - 1]) / tau_s
    return t, temp
```

This is the forward-Euler method of Phase 07, Lesson 08, applied to `dT/dt = (T_oven - T) / tau`. `oven_temperature` interpolates between the zone points. Output: the small part peaks at 247.7 °C with 64.4 s above 217 °C; the large connector peaks at 228.6 °C with only 41.4 s.

### Step 4: The iron in the simulator

```python
def iron_on_pad(link_k_per_w, seconds=6.0):
    c = Circuit()
    c.voltage_source("IRON", "tip", "0", 350.0 - AMBIENT_C)
    c.resistor("R_TIP", "tip", "joint", 15.0)
    c.capacitor("C_JOINT", "joint", "0", 0.02)
    c.resistor("S1", "joint", "plane", link_k_per_w)
    c.capacitor("C_PLANE", "plane", "0", 3.0)
    c.resistor("R_PLANE", "plane", "0", 10.0)
    return c.transient(t_stop=seconds, dt=2e-3)
```

The circuit is the thermal model, with the units translated as above. `t.time_to_cross("joint", 192)` finds when the joint reaches 217 °C. Output:

```
  pad-to-plane link  2.0 K/W: joint reaches  91.7 C after 6 s, never melts
  pad-to-plane link  8.0 K/W: joint reaches 153.5 C after 6 s, never melts
  pad-to-plane link 25.0 K/W: joint reaches 233.2 C after 6 s, melts after 0.54 s
```

The temperatures after 6 s are higher than the divider estimates because the plane has begun to warm.

### Step 5: Cracked joint

`cracked_joint` puts a resistor named `JOINT` between the 330 Ω resistor and the LED and prints the LED current for joint resistances of 1 mΩ, 10 Ω, 100 Ω and 1 kΩ: 9.55, 9.28, 7.36 and 2.42 mA.

### Step 6: The lab task

The script evaluates the lab task with each candidate link and prints the time to melt.

## Use It

- **Hand soldering.** Use a temperature-controlled iron (about 330-370 °C for lead-free), a tip large enough for the pad, fresh flux, and heat the pad and the lead together for 2-3 seconds before feeding solder. For ground pads in planes, use a bigger tip, preheat the board with a hot-air tool, or design thermal reliefs.
- **Small-batch assembly.** A laser-cut stencil, paste, tweezers and a hot plate or a toaster-oven conversion with a controller can reflow prototypes at home. Many PCB fabs also offer assembly with parts from their own stock.
- **Production.** Pick-and-place machines place tens of thousands of parts per hour. AOI cameras check every joint; X-ray machines check hidden joints under BGAs and QFNs.
- **Design for assembly.** Keep all SMD parts on one side if you can (one reflow pass), orient polarised parts the same way, leave room around tall parts for the iron, add fiducials, and use thermal reliefs on plane-connected pads.
- **Inspection by eye.** A good joint is smooth and concave, with the solder wetting both the pad and the lead in a fillet. A ball of solder sitting on top of a pad is a cold joint.

## Try It in the Lab

Open "Make the ground pad solderable". It is a thermal circuit: volts are degrees above room temperature, amps are watts, ohms are K/W and farads are J/K. Choose the pad-to-plane link (solid, wide relief or thin relief) so that the joint reaches 217 °C within 3 seconds. Use the divider estimate first. Then think about the price you pay electrically for the option that wins.

## Common Mistakes

- **Melting solder on the iron and carrying it to the joint.** The flux burns off on the way and the solder lands on cold metal: a cold joint. Heat the joint, then feed solder to the joint.
- **Not enough heat for big pads.** If solder will not flow on a ground pad, the plane is stealing the heat. A bigger tip and preheating work; turning the iron up to 450 °C mostly burns the flux and damages the pad.
- **Too little flux.** Rework without fresh flux gives dull, spiky joints and solder bridges between pins.
- **Ignoring the biggest part in the oven profile.** A profile tuned for small resistors underheats connectors and shields.
- **Asymmetric pads on small two-pin parts.** Connecting one pad of an 0402 to a plane without relief invites tombstoning.

## Exercises

1. Compute the paste volume and area ratio for a 0.3 x 1.0 mm aperture in a 0.15 mm stencil. Does it pass the 0.66 rule? What if the stencil is 0.10 mm?
2. A part has a thermal time constant of 30 s and sits in a zone at 250 °C, starting at 190 °C. Using `T(t) = 250 - 60 * exp(-t / 30)`, when does it reach 217 °C?
3. With the divider estimate, which link resistance makes the joint sit exactly at 217 °C (192 above room) while the plane is cold? Solve `325 * R / (15 + R) = 192`.
4. In the script, use an iron at 400 °C with the 8 K/W relief. Does the joint melt now, and how long does it take?
5. Harder: four spokes of 0.3 mm wide, 0.5 mm long 1 oz copper form the thermal relief. Compute their electrical resistance in parallel (Lesson 02) and the heat they would dissipate at 3 A. Is the relief acceptable for a 3 A ground pin?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Wetting | "the solder flowed" | Molten solder spreading on clean metal and forming an intermetallic bond |
| Flux | "the stuff that smokes" | A chemical that removes oxide so solder can wet; it must be fresh and hot |
| Reflow | "baking the board" | Melting printed paste on all joints at once following a controlled temperature profile |
| Time above liquidus | "time in reflow" | How long a joint stays fully molten; typically 60-90 s for lead-free |
| Thermal mass | "it's a heat sink" | Heat capacity in J/K; the larger it is, the slower a part heats |
| Thermal relief | "spokes" | Narrow copper links from a pad to a plane, raising the thermal resistance so the pad can be soldered |
| Cold joint | "bad solder" | A joint where the solder did not wet one surface because it was too cold or oxidised |

## Further Reading

- IPC J-STD-001, *Requirements for Soldered Electrical and Electronic Assemblies*, and IPC-A-610, *Acceptability of Electronic Assemblies* ([ipc.org](https://www.ipc.org/)) — what good and bad joints look like.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., chapter on soldering and construction.
- The application notes on reflow profiles published by solder paste makers (for example Indium Corporation and Kester) and by part makers for their packages.
