# Ground Planes and Current Return

> Every current comes home. Decide which road it takes, or it will choose one you did not want.

**Type:** Build
**Prerequisites:** Phase 21 (PCB Design and Manufacturing), Lessons 01-02; Phase 04 (Kirchhoff's Laws), Lessons 05 (The Voltage Divider) and 06 (The Current Divider); Phase 07 (Capacitors), Lesson 04 (The Time Constant); Phase 08 (Magnetism and Inductors), Lesson 04 (The Inductor)
**Time:** ~90 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Return path | The route the current takes back to the source after passing through the load | The road home after work |
| Ground (on a board) | The net that most currents return through and that we call 0 V | The floor everybody measures height from |
| Ground plane | A whole copper layer (or large area) connected to ground | A huge parking lot instead of a narrow lane |
| Shared impedance | A piece of copper that two circuits both use as their return | Two families sharing one narrow driveway |
| Ground bounce | The ground of a part moving up and down because current flows through the copper under it | A floor that sags when a heavy person walks past |
| Star ground | Wiring each circuit's ground separately back to one point | Spokes of a wheel meeting at the hub |
| Loop area | The area enclosed by the outgoing and returning current paths | The area of the lasso formed by the two roads |
| Loop inductance | How strongly the loop resists a change in current, set mostly by its area | The momentum of water in a long hose |
| Decoupling capacitor | A capacitor right next to a chip's power pin that supplies sudden bursts of current | A small water tank on the roof that covers short peaks |
| Bulk capacitor | A larger capacitor that refills the small ones and covers longer bursts | A bigger tank in the basement |
| Droop | How far the supply voltage sags during a sudden increase in current | The dip in water pressure when someone else turns on a shower |
| ESR / ESL | Equivalent series resistance / inductance: the small unwanted resistor and inductor inside every real capacitor | The narrow pipe between the tank and your tap |

## Learning Objectives

- Explain why every current needs a return path, and why on a board that path is real copper with resistance and inductance.
- Show with a voltage divider how a shared return lifts a sensor's ground and corrupts its reading, and fix it with a ground plane or a star ground.
- Explain why, at high speed, return current flows directly under the outgoing trace, and compute what fraction stays close to it.
- Estimate loop inductance for wires, a two-layer board and a four-layer board, and the voltage spike `V = L di/dt` for a fast edge.
- Simulate supply droop when a load switches on, and choose a decoupling capacitor using the estimate `droop ≈ I * sqrt(L / C)`.

## The Problem

You build a small board: a microcontroller measures a temperature sensor with its ADC (analog-to-digital converter, Phase 17, Lesson 04), and the same board switches a 1 A heater on and off. With the heater off, the reading is perfect. With the heater on, the temperature reading jumps by several degrees, even though nothing physical changed. And every time the heater switches on, the microcontroller sometimes resets.

The schematic is correct. Every ground symbol on it is "0 V". The problem is that on the real board, the ground is not a single point at 0 V. It is a piece of copper, and the heater's 1 A flows through it on its way home. That copper has resistance, so different spots of the "ground" sit at different voltages. And the supply wires have inductance, so when the 1 A suddenly starts flowing, the supply voltage at the chip collapses for a few microseconds.

This lesson is about the half of the circuit that schematics hide: the return path. We will see where return current really flows, how much voltage it creates, and the two standard cures: ground planes and decoupling capacitors.

## The Physics

### Current flows in loops

Kirchhoff's current law (Phase 04, Lesson 02) says charge does not pile up: whatever current leaves the battery's + terminal must come back into its - terminal. So a circuit is always a loop, and every trace that carries current *out* has a partner that carries the same current *back*. On a schematic the way back is a ground symbol. On a board it is copper with a length, a width and a position.

### At low frequency: the path of least resistance

When the current is steady (DC) or changes slowly, it divides among the possible return paths like water among pipes: the lower the resistance, the larger the share. This is the current divider of Phase 04, Lesson 06. If the way back is one thin trace, all the current goes through it, and it develops a voltage `V = I * R` along its length.

That voltage is the whole story of the temperature sensor. Suppose the heater's 1 A returns through a 0.2 Ω strip of ground copper. The far end of that strip sits at `1 A * 0.2 Ω = 0.2 V` above the connector's ground. If the sensor's ground pin is connected to that far end, the sensor sees its "zero" lifted by 0.2 V, and the ADC, which measures against the connector's ground, reads everything 0.2 V wrong (or, for a divider, a fraction of that).

### At high frequency: the path of least inductance

When the current changes quickly, a new effect dominates. A current loop creates a magnetic field, and changing that field induces a voltage that opposes the change (Phase 08, Lesson 03). This opposition is the loop's **inductance** `L`, measured in henries (H); on boards we talk in nanohenries (1 nH = 10^-9 H). The voltage it creates is

```
V = L * di/dt
```

"the voltage equals the inductance times how fast the current changes". `di/dt` is the change in current divided by the time it takes, in amperes per second.

Inductance grows with the **area** of the loop: the more space between the outgoing and returning paths, the more magnetic field fits in between. So, for fast-changing currents, nature picks the return path that makes the loop smallest. If there is a solid ground plane under a trace, the return current crowds into the plane directly underneath the trace, mirroring its route, even if that path is longer than going straight back. This surprises almost everyone the first time.

How concentrated is it? For a thin trace at height `h` above a wide plane, the return current density across the plane falls off as `1 / (1 + (x/h)^2)`, where `x` is the sideways distance from the point right under the trace. Integrating that shape gives the share that flows within a distance `d` on either side:

```
share within +/- d = (2 / pi) * arctan(d / h)
```

For a four-layer board where the plane is `h = 0.2 mm` below the trace, `(2/pi) * arctan(0.5 / 0.2) = (2/pi) * 1.190 = 0.758`: 76% of the return flows within half a millimetre of the trace, and 94% within 2 mm. For a two-layer board with the plane on the other side of a 1.6 mm board, only 19% stays within half a millimetre and 57% within 2 mm: the return spreads out.

### Why spikes appear

Digital chips switch in nanoseconds. A microcontroller pin driving a load, or the chip's own logic changing state, can pull an extra 0.5 A in about 2 ns. Through a loop of 50 nH:

```
V = L * di/dt = 50e-9 H * (0.5 A / 2e-9 s) = 50e-9 * 2.5e8 = 12.5 V
```

That is not a typo. The supply cannot deliver a fast step of current through any meaningful length of copper. The chip's supply pin would dip by volts, which is why every digital chip needs a capacitor right next to it.

### What a capacitor does about it

A capacitor holds charge (Phase 07). Placed right at the chip, with a tiny loop, it can deliver a sudden burst of current while the slow, inductive supply path catches up. During a burst of current `I` lasting `dt`, a capacitor `C` loses voltage

```
dV = I * dt / C
```

"the voltage drop equals the charge taken out (`I * dt`) divided by the capacitance". With 100 nF supplying 0.5 A for 2 ns: `dV = 0.5 * 2e-9 / 100e-9 = 0.01 V`. Ten millivolts instead of twelve volts.

For a step that lasts longer, the supply inductance and the capacitor form an LC circuit (Phase 10, Lesson 05). The voltage dips and rings. A handy estimate of the deepest dip is

```
droop ≈ I * sqrt(L / C)
```

"the current step times the square root of L over C". `sqrt(L/C)` has units of ohms and is called the characteristic impedance of the LC pair. A bigger capacitor makes it smaller.

## The Concept

### Picture 1: the shared ground return

```
   +5 V ----+-----------------+
            |                 |
           RL 4.7 Ω         R_TOP 10 kΩ
          (load, ~1 A)        |
            |               sense ----> to ADC (measured against connector ground)
            |                 |
            |               R_BOT 10 kΩ
            |                 |
            +----- ret -------+          <- the sensor's ground is the load's return node
                    |
                 S1 shared return copper (0.2 Ω thin trace / 0.02 Ω wide / 0.002 Ω plane)
                    |
   GND at the connector (0 V, the ADC's reference)
```

Work it by hand with the thin trace. The load current is about `5 / (4.7 + 0.2) = 1.02 A` (the sensor's 0.25 mA is negligible). The node `ret` sits at `1.02 * 0.2 = 0.204 V`. The divider splits what is left, `5 - 0.204`, in half, and adds it to `0.204`:

```
V(sense) = 0.204 + (5 - 0.204) / 2 = 0.204 + 2.398 = 2.602 V
```

The true answer is 2.500 V, so the reading is 102 mV high: 4% error caused by a strip of copper. With a wide trace (0.02 Ω) the error is about 11 mV; with a solid plane (0.002 Ω) about 1 mV.

### Picture 2: the star ground

The other classic cure is not to share at all:

```
   +5 V ---+----------------+
           |                |
          RL              R_TOP
           |                |
           |              sense
           |                |
           |              R_BOT
           |                |
     load return       sensor return
       (0.2 Ω)           (0.2 Ω)
           |                |
           +------ * -------+     <- star point at the connector
                   |
                  GND
```

Now the heater's current never flows through the sensor's ground copper. The sensor's return carries only the tiny divider current (0.25 mA through 0.2 Ω is 0.05 mV), so the reading is 2.500 V even though both returns are thin traces. Star grounds were the standard trick on single-layer and two-layer boards, and they are still used to separate noisy power returns from quiet analog ones. On multilayer boards a solid, unbroken ground plane usually does better, because it has tiny resistance *and* tiny inductance everywhere.

### Picture 3: the loop and its inductance

```
   out-and-back wires            trace over a plane (2-layer)     trace over a plane (4-layer)

   ->->->->->->->->->            ->->->->->->->->->->            ->->->->->->->->->->
         20 mm                      1.6 mm FR-4                     0.2 mm prepreg
   <-<-<-<-<-<-<-<-<-            ===<-<-<-<-<-=======            =====<-<-<-<-=======
                                    plane                           plane
   big loop area                 medium area                      tiny area
```

Two standard formulas (from magnetostatics; we use them, not derive them) give the inductance for 100 mm of path with a 0.25 mm effective radius:

```
two parallel wires, spacing s:       L = (mu0 * len / pi) * ln(s / r)
one wire at height h over a plane:   L = (mu0 * len / (2 pi)) * ln(2 h / r)
```

Here `mu0 = 4 pi * 10^-7 H/m` is the magnetic constant, `len` the length, `r` the wire radius, `ln` the natural logarithm. Numbers: about 175 nH for wires 20 mm apart, 51 nH over a plane 1.6 mm away, 9.4 nH over a plane 0.2 mm away. The same 0.5 A in 2 ns edge gives spikes of 44 V, 13 V and 2.4 V. Neither formula is exact for flat traces, but the trend is right and it is the reason four-layer boards with a ground plane right under the signal layer behave so much better.

### Picture 4: the supply loop and the decoupling capacitor

```
   battery 5 V --- R_LEADS 0.05 Ω --- L_LEADS 0.5 µH ---+--- vdd ---+
                                                         |           |
                                                       C_DEC       R_LOAD 5 Ω
                                                         |           |
                                                         |        S_LOAD (closes at t = 5 µs)
                                                         |           |
   GND --------------------------------------------------+-----------+
```

The 0.5 µH stands for the battery leads and long supply traces. At `t = 5 µs` the switch closes and asks for about 1 A. The inductor's current cannot jump, so for an instant the only source of current is the capacitor. Without a capacitor, `vdd` collapses to almost zero and recovers with the time constant `L / R = 0.5 µH / 5 Ω = 0.1 µs`: a microcontroller would reset. With a capacitor, the estimate `I * sqrt(L / C)` gives:

```
C = 1 µF:    sqrt(0.5e-6 / 1e-6)   = 0.707 Ω  -> droop ≈ 707 mV
C = 10 µF:   sqrt(0.5e-6 / 10e-6)  = 0.224 Ω  -> droop ≈ 224 mV
C = 100 µF:  sqrt(0.5e-6 / 100e-6) = 0.071 Ω  -> droop ≈  71 mV
```

Ten times more capacitance divides the droop by about three (the square root of ten).

### The practical recipe

Real boards use several capacitors because no single capacitor is good at every speed:

- **A small ceramic (100 nF is the classic value) on every power pin**, placed as close as possible with the shortest possible loop to ground: pad, short trace, via straight down into the ground plane. It covers the nanosecond bursts. Its own inductance (ESL, about 0.5-1 nH for an 0402/0603 part plus its vias) is what limits it, so placement matters more than value.
- **A bulk capacitor (10-100 µF) per board or per group of chips**, covering microsecond-to-millisecond bursts, like our switching load.
- **A solid ground plane**, so that every return path is short and every loop is small.

## Build It

Run:

```
uv run python phases/21-pcb-design-and-manufacturing/03-ground-planes-and-current-return/code/main.py
```

### Step 1: Return current under a trace

```python
def plane_return_fraction(height_m, half_width_m):
    return 2 / math.pi * math.atan(half_width_m / height_m)
```

Output: at 0.2 mm height, 75.8% of the return stays within ±0.5 mm, 93.7% within ±2 mm and 97.5% within ±5 mm; at 1.6 mm, only 19.3%, 57.0% and 80.3%. A cut ("slot") in the plane under the trace forces this current to detour around it, enlarging the loop: never route a fast signal across a gap in its reference plane.

### Step 2: Loop inductance and spikes

```python
def wire_pair_inductance(length_m, spacing_m, radius_m):
    return MU0 * length_m / math.pi * math.log(spacing_m / radius_m)


def wire_over_plane_inductance(length_m, height_m, radius_m):
    return MU0 * length_m / (2 * math.pi) * math.log(2 * height_m / radius_m)
```

Output: 175.3 nH, 51.0 nH and 9.4 nH, and spikes of 43.8 V, 12.8 V and 2.4 V for a 0.5 A step in 2 ns.

### Step 3: Shared versus star ground in the simulator

```python
def shared_ground(shared_ohms):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", 5.0)
    c.resistor("RL", "vcc", "ret", 4.7)
    c.resistor("R_TOP", "vcc", "sense", 10e3)
    c.resistor("R_BOT", "sense", "ret", 10e3)
    c.resistor("S1", "ret", "0", shared_ohms)
    return c.dc()
```

Output:

```
  shared return  200.0 mOhm: load current 1.020 A, ground lifted by  204.1 mV, ADC reads 2.6021 V
  shared return   20.0 mOhm: load current 1.059 A, ground lifted by   21.2 mV, ADC reads 2.5106 V
  shared return    2.0 mOhm: load current 1.063 A, ground lifted by    2.1 mV, ADC reads 2.5011 V
  star ground (two separate 200 mOhm returns): ADC reads 2.5000 V
```

The star version (function `star_ground`) gives the sensor its own return, and the error disappears even with thin traces.

### Step 4: Droop and decoupling

```python
def supply_droop(decoupling_farads):
    c = Circuit()
    c.voltage_source("V1", "bat", "0", 5.0)
    c.resistor("R_LEADS", "bat", "mid", 0.05)
    c.inductor("L_LEADS", "mid", "vdd", 0.5e-6)
    c.resistor("R_LOAD", "vdd", "sw", 5.0)
    c.switch("S_LOAD", "sw", "0", closed=False, toggle_at=(5e-6,))
    if decoupling_farads:
        c.capacitor("C_DEC", "vdd", "0", decoupling_farads)
    t = c.transient(t_stop=60e-6, dt=20e-9, initial="dc")
    return t
```

`initial="dc"` starts the simulation from the steady state (capacitor already charged to 5 V). The switch's `toggle_at` closes it at 5 µs. The script prints the lowest `vdd` after the switch closes:

```
  no capacitor: lowest vdd 0.454 V, droop   4546 mV
          1 uF: lowest vdd 4.356 V, droop    644 mV
         10 uF: lowest vdd 4.774 V, droop    226 mV
        100 uF: lowest vdd 4.917 V, droop     83 mV
```

The estimates `I * sqrt(L/C)` (707, 224 and 71 mV) are close. They differ because the load is a resistor, so its current falls a little as `vdd` sags, and because the 0.05 Ω of the leads adds a small DC drop. Without a capacitor the simulator's first sample after the switch shows 0.45 V; the true minimum is essentially zero.

### Step 5: Check the lab

The script tries each part of the lab task in the shared-ground circuit and prints which one keeps the reading within 5 mV.

## Use It

- **Four-layer boards** (signal / ground / power / signal) are the default for anything with a fast microcontroller, USB or radio. The extra two layers cost little today and give every signal a plane right underneath.
- **Datasheets tell you.** Microcontroller datasheets have a "power supply decoupling" section: typically one 100 nF ceramic per VDD pin plus a 4.7-10 µF bulk capacitor, and a separate filtered supply for the ADC reference (often a small ferrite bead and 1 µF).
- **Kelvin connections.** When you must measure a voltage across a low-ohm resistor (a current-sense resistor of 10 mΩ, for example), you route two separate thin "sense" traces from the resistor's pads to the amplifier, so the big current never flows through the measurement traces. It is the star-ground idea in miniature.
- **Analog and digital grounds.** Mixed-signal chips have AGND and DGND pins. Modern advice is usually one solid ground plane and careful placement (keep noisy current loops away from the analog part), rather than splitting the plane, which breaks return paths.
- **USB and cable shields** follow the same rule: the return current of a fast signal wants to run right next to it, which is why data lines come in tightly coupled pairs.

## Try It in the Lab

Open "Stop the heater from lying to the sensor". A 4.7 Ω load and a 10 kΩ / 10 kΩ sensor divider share one piece of return copper (slot S1). The ADC must read 2.500 V within 5 mV. Before you run it, estimate for each candidate how far the load's current lifts the node `ret`, and how much of that lift ends up in the reading. Then ask yourself: if you could rewire the board instead of changing S1, what would you change?

## Common Mistakes

- **Believing ground is one point.** Ground is copper. Any current through it creates a voltage along it. Ask "whose current flows here?" for every piece of ground copper near a sensitive part.
- **Cutting the ground plane.** A slot or a split under a fast trace forces the return current around the gap. The loop grows, the inductance grows, and the trace radiates and picks up noise.
- **Putting the decoupling capacitor "somewhere nearby".** A capacitor 20 mm away through a thin trace has tens of nanohenries in series and does little at nanosecond speeds. Put it right at the pin, with its ground via right at its pad.
- **Only one big capacitor.** A 100 µF electrolytic has too much internal inductance to help with nanosecond bursts; a 100 nF ceramic has too little charge for a millisecond burst. Use both.
- **Daisy-chaining grounds.** Running ground from part to part in a chain makes each part's ground depend on everybody else's current. Use a plane or a star.

## Exercises

1. A 2 A motor's return flows through 30 mm of 0.5 mm wide, 1 oz ground trace. Using about 1 mΩ per mm for that width, how many millivolts does the far end sit above the connector?
2. With a plane 0.2 mm under a trace, what share of the return current flows within ±1 mm of the trace? And with the plane 1.6 mm away?
3. A chip pulls 0.2 A in 1 ns through a 5 nH loop. What spike `V = L di/dt` appears? A 100 nF capacitor at the pin supplies that current for 1 ns instead: what is `dV = I dt / C`?
4. In the script, change `L_LEADS` to 2 µH and repeat Step 4. Compare the new droops with `I * sqrt(L/C)`. Which capacitor would you need to keep the droop under 100 mV?
5. Harder: modify `star_ground` so that the load return is 0.2 Ω but the sensor return goes to the *middle* of the load's return trace (split the 0.2 Ω into two 0.1 Ω halves). Predict the reading before running it.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Return path | "it goes to ground" | The real copper route the current takes back to the source; always part of the loop |
| Ground plane | "a big ground pour" | A continuous copper layer that gives every signal a short, low-resistance, low-inductance return |
| Shared impedance coupling | "ground noise" | One circuit's current flowing through copper another circuit uses as its reference, shifting that reference by `I * R` (or `L di/dt`) |
| Star ground | "single-point ground" | Each circuit's return wired separately to one common point, so no current shares another circuit's return |
| Loop inductance | "parasitic inductance" | Inductance of the whole out-and-back current loop; set mostly by the loop's area |
| Decoupling capacitor | "bypass cap" | A capacitor at a power pin that supplies fast current bursts locally; its benefit depends on the loop it forms with the pin |
| Droop | "the rail dips" | The temporary sag of a supply during a current step, about `I * sqrt(L/C)` for an LC supply path |

## Further Reading

- Henry W. Ott, *Electromagnetic Compatibility Engineering* (Wiley, 2009), chapters on grounding and digital layout — the standard reference for return paths.
- Howard Johnson and Martin Graham, *High-Speed Digital Design: A Handbook of Black Magic* (Prentice Hall, 1993) — ground planes, inductance and decoupling for fast logic.
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., sections on grounding and power supply bypassing.
- Analog Devices, *MT-031: Grounding Data Converters and Solving the Mystery of "AGND" and "DGND"* and *MT-101: Decoupling Techniques* (application notes, analog.com).
