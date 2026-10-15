# Footprints and Traces

> A trace is a resistor you did not mean to buy. Make it wide enough and it stops mattering.

**Type:** Build
**Prerequisites:** Phase 21 (PCB Design and Manufacturing), Lesson 01 (From Schematic to Board); Phase 03 (Resistance and Ohm's Law), Lessons 02 (Resistivity and Wires) and 05 (Power and Heat)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Package | The physical body a component comes in (its plastic or ceramic shell and its pins) | The box a product is shipped in |
| Through-hole (THT) | Parts whose legs go through drilled holes in the board and are soldered on the other side | A fence post pushed into the ground |
| Surface mount (SMD/SMT) | Parts that sit flat on pads on the surface and are soldered there | A sticker stuck onto a page |
| Pitch | The distance from the centre of one pin to the centre of the next | The spacing between the teeth of a comb |
| Chip size code (0805, 0603...) | A code giving the length and width of tiny rectangular parts, in hundredths of an inch | A shoe size for components |
| Copper weight (oz) | How thick the board's copper is, given as ounces of copper per square foot | The thickness of the asphalt on a road |
| Cross-section | The area you would see if you cut the trace across | The slice you see when you cut a sausage |
| Temperature rise | How many degrees hotter a trace gets than the board around it when current flows | How much warmer a busy road gets than the field next to it |
| IPC-2221 | An industry standard with design rules for boards, including a formula for trace width vs current | A building code for circuit boards |
| Voltage drop | The voltage "used up" across a conductor because of its resistance | Pressure lost along a long garden hose |
| Thermal relief | Thin spokes joining a pad to a big copper area so the pad is easier to solder | A narrow bridge to an island, so heat cannot escape too fast |

## Learning Objectives

- Read package names and size codes (0402, 0805, SOT-23, SOIC-8, DIP-8) and say what they mean physically.
- Compute the resistance of a trace from its length, width and copper weight, including the effect of temperature.
- Use the IPC-2221 formula to find the minimum width of a trace for a given current and temperature rise, and to estimate how hot an existing trace runs.
- Simulate a load fed through a trace and decide whether the trace is wide enough, both by voltage drop and by power.

## The Problem

You have a 12 V battery and a small heater element of 6 Ω (think of a hand warmer or a heated pad for a sensor). By Ohm's law it should draw `I = V / R = 12 / 6 = 2 A` and turn `P = V * I = 24 W` into heat. On a breadboard with thick jumper wires that is what you measure.

You lay out a board. The heater connector is 200 mm away from the battery connector, and you draw the trace between them with the default width of your EDA tool: 0.2 mm. The board comes back, you plug it in, and the heater gets only about 11 V instead of 12 V. Worse, after a minute the thin trace is too hot to touch, the board turns brown under it and eventually the trace lifts off and breaks like a fuse.

Nothing was wrong with the schematic. The trace was simply a resistor you did not mean to put there, and it burnt 1.7 W in a strip of copper thinner than a hair. In this lesson we learn to choose two things on purpose: the **footprint** of each part, and the **width** of each trace.

## The Physics

### Why a trace heats up

A current is charge moving through the copper. The moving electrons constantly bump into the vibrating copper atoms and hand them energy (Phase 03, Lesson 01). That energy is heat. The rate at which a resistor turns electrical energy into heat is

```
P = I^2 * R
```

"power equals the current squared times the resistance". `P` is in watts (W), `I` in amperes (A), `R` in ohms (Ω). The square is the important part: doubling the current makes four times as much heat in the same trace.

The heat has to leave. A trace on the outside of the board loses heat into the air and spreads it into the board. A trace buried in an inner layer is wrapped in epoxy and glass, which are poor conductors of heat, so it gets hotter for the same current. That is why the rules below are different for outer and inner layers.

### Why a hot trace gets worse

Copper's resistance rises with temperature, by about 0.39% per °C (the temperature coefficient, 0.00393 per °C). A trace at 70 °C has

```
R(70 C) = R(20 C) * (1 + 0.00393 * (70 - 20)) = R(20 C) * 1.197
```

about 20% more resistance than at room temperature. More resistance means more heat, which means more resistance. For a reasonable design this feedback settles at a slightly higher temperature. For a badly undersized trace it runs away until the copper or the board fails.

### The shape of a trace

A trace is a flat rectangle in cross-section:

```
            width (you choose: 0.1 mm ... 10 mm)
         <--------------------------->
         +---------------------------+   ^
         |        copper             |   | thickness (fixed by the fab:
         +---------------------------+   v  35 um for 1 oz, 70 um for 2 oz)
   ======================================== FR-4 board
```

The resistance formula from Phase 03 becomes

```
R = rho * L / (w * t)
```

"resistance equals resistivity times length, divided by width times thickness". With `rho = 1.72e-8 Ω·m`, length `L`, width `w` and thickness `t` all in metres.

Worked example: 100 mm of 0.25 mm wide, 1 oz (35 µm) trace.

```
w * t = 0.25e-3 * 35e-6 = 8.75e-9 m^2
R = 1.72e-8 * 0.100 / 8.75e-9 = 1.72e-9 / 8.75e-9 = 0.197 Ω
```

So about 2 mΩ per millimetre. The two levers are clear: making the trace twice as wide halves the resistance; ordering 2 oz copper halves it too.

## The Concept

### Footprints: from datasheet drawing to pads

Every component's datasheet has a "package drawing" with exact dimensions, and usually a "recommended land pattern": the pads the manufacturer suggests. The EDA library calls this a footprint. The common families:

**Through-hole (THT).** Legs go through plated holes. The classic is the DIP (dual in-line package) chip with pins 2.54 mm (0.1 inch) apart, the same spacing as a breadboard. Strong joints, easy to hand-solder, but they use space on both sides of the board and need drilling.

**Surface mount (SMT).** Parts sit on pads on one face. Almost every modern board is mostly SMT because it is smaller and machines can place it quickly. The common shapes:

```
  chip resistor/capacitor (0805)        SOT-23 (small transistor)     SOIC-8 (8-pin chip)

   +--+---------+--+                       +--+    +--+               +--+ +--+ +--+ +--+
   |  |  body   |  |                       |  |    |  |               |  | |  | |  | |  |
   |  |         |  |                       +--+----+--+               +--+-+--+-+--+-+--+
   +--+---------+--+                          | body |                |      body       |
   pad          pad                        +--+------+                +--+-+--+-+--+-+--+
                                           |  |                       |  | |  | |  | |  |
                                           +--+                       +--+ +--+ +--+ +--+
                                                                      <-->  pitch 1.27 mm
```

The chip size codes for rectangular resistors and capacitors are in hundredths of an inch (the imperial code; there is a metric code too, which causes confusion: imperial 0603 is metric 1608):

| Imperial code | Length x width | Typical use |
|---|---|---|
| 0402 | 1.0 x 0.5 mm | phones, dense boards (hard to hand-solder) |
| 0603 | 1.6 x 0.8 mm | general SMT boards |
| 0805 | 2.0 x 1.25 mm | general boards, fine for hand-soldering |
| 1206 | 3.2 x 1.6 mm | higher power, higher voltage |

Bigger bodies can dissipate more heat: a typical 0402 resistor is rated about 1/16 W, an 0805 about 1/8 W, a 1206 about 1/4 W. When you choose a footprint you are also choosing a power rating (Phase 03, Lesson 06).

Pin pitch matters for chips: DIP 2.54 mm, SOIC 1.27 mm, TSSOP 0.65 mm, small QFN 0.5 mm or less. The finer the pitch, the thinner the traces that can escape between the pins, and the more demanding the fabrication (Lesson 04).

### Trace width versus current: the IPC-2221 formula

How wide must a trace be? Engineers asked this so often that the IPC (the electronics industry association) published charts based on experiments, and a curve fitted to those charts:

```
I = k * dT^0.44 * A^0.725
```

Read it as: "the current a trace can carry equals a constant `k`, times the allowed temperature rise to the power 0.44, times the cross-section area to the power 0.725". The units are odd because the formula was fitted in imperial units:

- `I` in amperes,
- `dT` the temperature rise above the surroundings, in °C (10 °C is a common, conservative choice),
- `A` the cross-section area in **square mils** (1 mil = 1/1000 inch = 25.4 µm),
- `k = 0.048` for outer layers and `0.024` for inner layers (inner traces cool worse, so they carry about half the current).

Notice the powers are below 1. Doubling the area does not double the current: bigger traces have relatively less surface per unit of copper to shed heat.

To find the width, we solve for `A` and divide by the thickness:

```
A = (I / (k * dT^0.44)) ^ (1 / 0.725)
w = A / t
```

Worked example: 2 A on an outer 1 oz layer, 10 °C rise.

```
dT^0.44 = 10^0.44 = 2.754
k * dT^0.44 = 0.048 * 2.754 = 0.1322
I / 0.1322 = 2 / 0.1322 = 15.13
A = 15.13 ^ (1/0.725) = 15.13 ^ 1.379 = 42.4 square mils
t = 35 um / 25.4 um per mil = 1.378 mil
w = 42.4 / 1.378 = 30.8 mil = 30.8 * 0.0254 mm = 0.78 mm
```

So a 2 A trace on the outside of a 1 oz board should be at least about 0.8 mm wide. An inner layer would need 2 mm. The formula is old and conservative; the newer standard IPC-2152 uses better measurements and also accounts for nearby copper planes, which help to cool the trace. For a first design, IPC-2221 is the number to remember.

You can also run the formula backwards: given a trace, how hot will it get?

```
dT = (I / (k * A^0.725)) ^ (1 / 0.44)
```

For a 0.25 mm (9.84 mil) outer trace, `A = 9.84 * 1.378 = 13.6 mil^2`. At 1 A, `A^0.725 = 13.6^0.725 = 6.63`, so `I / (k * A^0.725) = 1 / (0.048 * 6.63) = 3.14`, and `dT = 3.14^(1/0.44) = 3.14^2.27 = 13.5 °C`. At 2 A it would be about 65 °C above the board. Thin default traces are fine for signals and LEDs but not for amps.

### Two separate questions: heat and voltage drop

IPC-2221 answers "will the trace get too hot?". It does **not** answer "will the load get enough voltage?". A long trace can be perfectly cool and still drop too many volts. Always check both:

1. **Heat:** is the trace wide enough by IPC-2221 for the current?
2. **Drop:** is `I * R_trace` small enough for the load? Remember the return path drops voltage too, unless it is a solid plane.

Worked example, the heater from The Problem. The trace is 200 mm long and 0.2 mm wide:

```
R = 1.72e-8 * 0.2 / (0.2e-3 * 35e-6) = 3.44e-9 / 7e-9 = 0.491 Ω
I = 12 / (6 + 0.491) = 1.849 A
V heater = 1.849 * 6 = 11.09 V
P trace = 1.849^2 * 0.491 = 1.68 W
```

Now 1 mm wide: `R = 0.098 Ω`, `I = 12 / 6.098 = 1.968 A`, `V heater = 11.81 V`, `P trace = 1.968^2 * 0.098 = 0.38 W`. Better, but still almost 0.4 W in a strip of copper.

And 3 mm wide: `R = 0.033 Ω`, `I = 1.989 A`, `V heater = 11.93 V`, `P trace = 0.13 W`.

Note how the 2 A current barely changes while the trace's share of the power falls by a factor of 13. The trace is in **series** with a much bigger resistance (the 6 Ω heater), so the heater sets the current and the trace just takes its small slice: this is a voltage divider (Phase 04, Lesson 05).

## Build It

Run:

```
uv run python phases/21-pcb-design-and-manufacturing/02-footprints-and-traces/code/main.py
```

### Step 1: Footprint sizes

The script starts with two small tables, the chip size codes and the pin pitches of common chip packages, so you can compare them with the drawings above.

### Step 2: Trace resistance

```python
def trace_resistance(length_m, width_m, copper_oz=1.0, temperature_c=20.0):
    thickness = copper_oz * OZ_TO_METRES
    rho = RHO_COPPER * (1 + TEMPCO_COPPER * (temperature_c - 20.0))
    return rho * length_m / (width_m * thickness)
```

For 100 mm of 1 oz copper it prints 327.6 mΩ at 0.15 mm, 196.6 mΩ at 0.25 mm, 49.1 mΩ at 1 mm and 9.8 mΩ at 5 mm. It also shows that the 0.25 mm trace at 70 °C has 235 mΩ, 20% more than at 20 °C.

### Step 3: IPC-2221 width

```python
def ipc2221_width(current_a, rise_c, copper_oz=1.0, outer=True):
    k = 0.048 if outer else 0.024
    area_mil2 = (current_a / (k * rise_c ** 0.44)) ** (1 / 0.725)
    thickness_mil = copper_oz * OZ_TO_METRES / METRES_PER_MIL
    return area_mil2 / thickness_mil * METRES_PER_MIL
```

The printed table (for a 10 °C rise):

```
   current  outer 1oz  inner 1oz  outer 2oz
     0.1 A     0.01 mm     0.03 mm     0.01 mm
     0.5 A     0.12 mm     0.30 mm     0.06 mm
     1.0 A     0.30 mm     0.78 mm     0.15 mm
     2.0 A     0.78 mm     2.03 mm     0.39 mm
     5.0 A     2.77 mm     7.19 mm     1.38 mm
```

Small currents give widths below anything a fab can make (0.01 mm), so in practice the minimum width rule of the factory (around 0.15 mm, Lesson 04) wins for signals.

### Step 4: Temperature rise of a given trace

`ipc2221_rise` is the same formula solved for `dT`. A 0.25 mm outer trace rises about 0.6 °C at 0.25 A, 2.8 °C at 0.5 A, 13.5 °C at 1 A and 65 °C at 2 A.

### Step 5: Simulate the heater

```python
def heater_through_trace(trace_ohms):
    c = Circuit()
    c.voltage_source("B1", "vcc", "0", 12.0)
    c.resistor("S1", "vcc", "load", trace_ohms)
    c.resistor("RL", "load", "0", 6.0)
    return c.dc()
```

The trace is a resistor named `S1` (the same name as the lab slot). The return is a perfect ground plane, so there is no resistor on the way back. The simulator confirms the hand numbers above: about 11.09 V and 1.68 W in the trace for 0.2 mm, 11.81 V and 0.38 W for 1 mm, 11.93 V and 0.13 W for 3 mm.

### Step 6: Check the lab task

The script loads `lab/task.json`, tries every candidate trace and prints which one meets both goals. This is how we prove that a lab task is solvable and that the wrong parts really are wrong.

## Use It

- **Default widths.** Many designers use 0.2-0.25 mm for signals, 0.4-0.5 mm for low-current power (up to a few hundred mA) and pour wide copper areas ("pours" or "planes") for amps. KiCad lets you define "net classes" so all power nets automatically get wider traces.
- **Calculators.** KiCad ships a calculator with the IPC-2221 and IPC-2152 formulas; Saturn PCB Toolkit is a popular free one. They give the same numbers as our script.
- **Thicker copper.** Motor drivers and power supplies often use 2 oz or 3 oz copper. It costs more and needs larger spacing between traces (the etching is less precise in thick copper).
- **Connectors and vias count too.** A single small via can carry roughly 1 A. High-current paths use several vias in parallel.
- **Thermal reliefs.** A pad connected to a big copper pour is hard to solder because the pour soaks up the iron's heat. EDA tools connect such pads through thin spokes called thermal reliefs. The spokes must still carry the current, so for high-current pads use wider spokes or a solid connection.
- **Datasheet land patterns.** For anything other than standard chip resistors, copy the recommended land pattern from the part's datasheet into your footprint (or use a library footprint that matches it). A QFN footprint that is 0.1 mm off will not solder.

## Try It in the Lab

Open the lab task "Pick a trace wide enough for the heater". A 12 V battery feeds a 6 Ω heater through a 200 mm trace. The tray holds three traces, each shown as its resistance: 0.2 mm wide, 1 mm wide and 3 mm wide. Two goals must both pass: the heater must get at least 11.85 V, and the trace must dissipate at most 0.25 W. Before pressing RUN, compute the current, the heater voltage and the trace power for each candidate by hand. Which goal does each wrong trace fail, the voltage goal, the power goal or both?

## Common Mistakes

- **Using the default trace width for everything.** EDA defaults are chosen for signals. Power nets need deliberate widths.
- **Checking heat but not voltage drop (or the other way round).** IPC-2221 limits temperature; Ohm's law limits drop. A long low-voltage line (3.3 V at 1 A) is often limited by drop, a short high-current one by heat.
- **Forgetting the return path.** If the ground return is also a trace, it has its own resistance and drop. The load sees the supply minus both drops.
- **Using outer-layer numbers for inner layers.** Inner traces need roughly 2.5 times the width for the same current and temperature rise.
- **Mixing imperial and metric codes.** An "0603" in an imperial catalogue is 1.6 x 0.8 mm; a "0603" metric part is 0.6 x 0.3 mm, a completely different, tiny part.
- **Footprint not matching the bought part.** Check the exact package suffix in the part number; the same chip often comes in several packages.

## Exercises

1. Compute the resistance of a 50 mm long, 0.5 mm wide trace in 1 oz copper. How many millivolts does it drop at 300 mA?
2. Using IPC-2221, how wide must an outer 1 oz trace be to carry 3 A with a 20 °C rise? (Hint: `20^0.44 = 3.74`.)
3. A 3.3 V microcontroller draws 150 mA through 120 mm of 0.25 mm trace, and the ground return is an identical trace. What voltage does the microcontroller actually see? Is that acceptable if it needs at least 3.0 V?
4. Repeat the heater example in the script with 2 oz copper (`copper_oz=2.0`). What is the narrowest of the three widths (0.2, 1, 3 mm) that now meets both lab goals?
5. Harder: the 0.2 mm heater trace from The Problem warms up. Use `trace_resistance(..., temperature_c=T)` and `ipc2221_rise` in a loop: start at 20 °C, compute the resistance, the current, the temperature rise, the new temperature, and repeat. Does it settle? At what temperature? (IPC-2221 is only approximate this far outside its range, so treat the answer as "very hot".)

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Footprint | "the land pattern" | The set of pads and their positions that one package needs on the board |
| Pitch | "pin spacing" | Centre-to-centre distance of adjacent pins, e.g. 2.54 mm for DIP, 1.27 mm for SOIC |
| 1 oz copper | "standard copper" | A copper layer weighing 1 ounce per square foot, about 35 µm thick |
| Trace resistance | "the copper is free" | `rho * L / (w * t)`, about 2 mΩ per mm for a 0.25 mm, 1 oz trace |
| IPC-2221 width | "the trace width calculator" | An empirical fit `I = k * dT^0.44 * A^0.725` giving the current for a chosen temperature rise |
| Voltage drop | "losses in the wiring" | `I * R` of the supply and return paths, subtracted from what the load sees |

## Further Reading

- IPC-2221B, *Generic Standard on Printed Board Design*, and IPC-2152, *Standard for Determining Current-Carrying Capacity in Printed Board Design* ([ipc.org](https://www.ipc.org/)).
- [KiCad PCB Calculator documentation](https://docs.kicad.org/10.0/en/pcb_calculator/pcb_calculator.html) — the built-in trace width and via calculators.
- Henry W. Ott, *Electromagnetic Compatibility Engineering* (Wiley, 2009) — the reference on why layout geometry matters.
