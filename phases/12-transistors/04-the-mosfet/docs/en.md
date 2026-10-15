# The MOSFET

> A MOSFET's control terminal is one plate of a capacitor. Put enough charge on it and the other "plate", the silicon surface, fills with electrons and becomes a wire between source and drain. No steady current flows into the gate: control costs almost nothing.

**Type:** Learn
**Prerequisites:** 12-02 (The BJT); Phase 11 (Semiconductors and Diodes), lessons 01-why-silicon and 02-doping-n-and-p; Phase 07 (Capacitors), lesson 02-capacitance
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| MOSFET | Metal-Oxide-Semiconductor Field-Effect Transistor: a transistor controlled by the electric field of a gate electrode | A drawbridge raised or lowered by a remote control, without anyone touching it |
| Gate (G) | The control electrode, insulated from the silicon by a thin oxide | The remote control's button |
| Source (S) | The terminal carriers come from | The river's spring |
| Drain (D) | The terminal carriers go to | Where the river drains away |
| Body / substrate | The silicon underneath, usually tied to the source | The riverbed |
| Gate oxide | The thin glass (SiO₂) layer between gate and silicon, a few nanometres thick | The thin window glass between you and a magnet on the other side |
| Channel | The thin conducting layer of carriers induced under the gate | A temporary road that appears only when the bridge is lowered |
| Inversion | Making the surface of p-type silicon act as n-type by attracting enough electrons | So many visitors arrive that the locals become a minority |
| Threshold voltage (V_th) | The gate-source voltage at which the channel forms | The water level at which the meadow becomes a lake |
| Overdrive (V_GS − V_th) | How far above threshold the gate is; sets how conductive the channel is | How far above "just flooded" the water is |
| Triode (linear) region | Small V_DS: the channel behaves like a resistor set by the gate | A road with traffic moving freely in proportion to the push |
| Saturation (MOSFET) | V_DS ≥ V_GS − V_th: the channel pinches off near the drain and the current stops growing with V_DS | A road narrowed to one lane at the end: more pressure behind does not get more cars through |
| k (transconductance parameter) | How much current a MOSFET carries per volt squared of overdrive, set by its size | The width of the road |
| NMOS / PMOS | N-channel (electrons, turned on by positive V_GS) and P-channel (holes, turned on by negative V_GS) | A drawbridge that opens with "up" versus one that opens with "down" |
| Square law | I_D = (k/2)(V_GS − V_th)² in saturation | Double the overdrive, four times the current |

## Learning Objectives

- Describe the structure of an n-channel MOSFET and explain how a gate voltage creates a channel.
- Compute the gate capacitance from the oxide thickness and area.
- Use the square law and the triode formula; identify cutoff, triode and saturation.
- Explain why the gate draws no steady current and why that matters.
- Contrast the MOSFET with the BJT, and recognise the PMOS as its mirror image.

## The Problem

The BJT needs a continuous base current to stay on: a little power is always spent just holding it in place. In a chip with ten billion transistors, a microamp per transistor would be ten thousand amps. Computers as we know them would be impossible.

The MOSFET solves this. Its control is a capacitor: you charge it once to turn the transistor on, and after that no current flows. This is why every processor, memory chip and smartphone is built from MOSFETs, and why the power switches in chargers and electric cars are MOSFETs too. This lesson explains how the field from the gate turns an insulator into a wire, and gives you the equations to predict its current.

## The Physics

### The structure

An n-channel MOSFET (NMOS) starts with a p-type silicon body. Two heavily doped n⁺ islands are made in it: the **source** and the **drain**. Between them, on the surface, sits a very thin layer of silicon dioxide (glass), and on top of that the **gate** electrode (historically metal, then heavily doped polysilicon, today metal again).

```
              S          G           D
              |      ==========      |
              |      | oxide  |      |          gate oxide: 1-100 nm of SiO2
          +---+---+--+--------+--+---+---+
          |  n+   |   channel    |  n+   |      channel forms here, at the surface
          |source |   region     | drain |
          +-------+              +-------+
          |        p-type body (substrate)       |
          +--------------------------------------+
                          |
                        body (usually tied to S)
```

With the gate at 0 V, going from source to drain means n⁺ → p → n⁺: two pn junctions back to back, one of which is always reverse biased. No current flows. That is the **off** state.

### The gate is a capacitor

Gate, oxide and silicon form a parallel-plate capacitor (Phase 07). Its capacitance per unit area is

```
C_ox = ε_ox / t_ox
```

Read: "the oxide capacitance per area equals the permittivity of the oxide divided by its thickness". SiO₂ has ε_ox = 3.9 × 8.854 × 10⁻¹² = 3.45 × 10⁻¹¹ F/m. For a 10 nm oxide:

```
C_ox = 3.45e-11 / 10e-9 = 3.45e-3 F/m²  =  3.45 fF per square micrometre
```

A gate 10 µm wide and 1 µm long: 10 µm² × 3.45 fF/µm² = 34.5 fF (femtofarads, 10⁻¹⁵ F). Tiny, but each volt on it holds Q = C × V = 34.5 × 10⁻¹⁵ C, which is 34.5 × 10⁻¹⁵ / 1.602 × 10⁻¹⁹ ≈ **215,000 electrons**.

### Making a channel: inversion

Put a positive voltage on the gate (relative to the source and body). The gate collects positive charge; the silicon surface underneath must collect an equal negative charge. Two things happen as the voltage rises:

1. **Depletion.** First, holes (the p-type majority carriers) are pushed away from the surface, leaving fixed negative acceptor ions (lesson 11-02). No mobile carriers yet.
2. **Inversion.** Above a certain gate voltage, the surface attracts so many electrons (from the n⁺ source and drain next to it) that it has more electrons than holes. The p-type surface has been **inverted** to n-type: a thin layer of electrons connects source to drain. That layer is the **channel**.

The gate-source voltage at which inversion begins is the **threshold voltage**, V_th. Typical values: 0.3-0.7 V in modern chips, 1-2 V in logic-level power MOSFETs, 2-4 V in standard power MOSFETs.

Above threshold, each extra volt adds C_ox × (extra volts) of electrons to the channel. So the channel's charge is proportional to the **overdrive**, V_GS − V_th.

What the analogy gets wrong: a drawbridge is either down or up. The channel appears gradually: below V_th there is still a tiny "subthreshold" current that grows exponentially with V_GS (like a BJT!). It matters a lot in chips, where billions of slightly-leaking transistors add up, but it is left out of our simulator's model.

### Current in the channel

With a channel in place, a voltage V_DS between drain and source drives electrons along it.

**Small V_DS (triode region).** The channel is uniform, and it is simply a resistor: more overdrive, more electrons, less resistance. Current is proportional to V_DS.

**Larger V_DS.** The voltage between gate and channel is V_GS at the source end but only V_GS − V_DS at the drain end. So the channel gets thinner toward the drain. When V_DS reaches V_GS − V_th, the gate-to-channel voltage at the drain end is just the threshold: the channel **pinches off** there. Beyond that, extra V_DS appears across a short depleted gap near the drain, and electrons reaching the gap are swept across by its field (just as at a BJT's collector). The current stops growing: this is **saturation**.

```
   triode (small V_DS)                 saturation (V_DS > V_GS - V_th)
   S ================ D                S ==========---  D
     uniform channel                     channel pinched off near drain
```

**Warning about words**: "saturation" means *opposite* things for the two transistor families. For a BJT it means "fully on, V_CE tiny" (a switch). For a MOSFET it means "current no longer grows with V_DS" (the region used for amplifiers and current sources, like the BJT's *active* region). Blame history.

## The Concept

### The equations (our simulator's model)

**Cutoff**: V_GS < V_th → I_D = 0.

**Triode**: V_GS > V_th and V_DS < V_GS − V_th:

```
I_D = k × ( (V_GS − V_th) × V_DS − V_DS² / 2 )
```

**Saturation**: V_GS > V_th and V_DS ≥ V_GS − V_th:

```
I_D = (k / 2) × (V_GS − V_th)²
```

Read the last one: "the drain current equals half of k times the overdrive squared". `k` (in A/V²) combines the electrons' mobility, C_ox and the gate's width-to-length ratio W/L: k = μ C_ox W / L. A wider gate means a wider road and proportionally more current.

Our script uses V_th = 1.0 V and k = 2 mA/V².

### Worked example: the transfer curve

At V_GS = 3 V, V_DS = 5 V. Overdrive = 3 − 1 = 2 V. Is it in saturation? V_DS = 5 ≥ 2: yes.

```
I_D = (0.002 / 2) × 2² = 0.001 × 4 = 4 mA
```

| V_GS | Formula | Simulator |
|---|---|---|
| 0.0-1.0 V | 0 | 0 |
| 1.5 V | 0.250 mA | 0.250 mA |
| 2.0 V | 1.000 mA | 1.000 mA |
| 3.0 V | 4.000 mA | 4.000 mA |
| 4.0 V | 9.000 mA | 9.000 mA |
| 5.0 V | 16.000 mA | 16.000 mA |

Doubling the overdrive from 1 V to 2 V multiplies the current by 4: a square law. Compare the BJT, where +60 mV multiplies the current by 10. A MOSFET needs much larger gate swings for the same change in current, which is why BJTs still win in some analogue jobs.

### Output curves

| V_GS | V_DS = 0.25 | 0.5 | 1.0 | 1.5 | 2.0 | 3.0 | 5.0 V |
|---|---|---|---|---|---|---|---|
| 2 V | 0.438 | 0.750 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 mA |
| 3 V | 0.938 | 1.750 | 3.000 | 3.750 | 4.000 | 4.000 | 4.000 mA |
| 4 V | 1.438 | 2.750 | 5.000 | 6.750 | 8.000 | 9.000 | 9.000 mA |

Each row rises (triode) and then flattens once V_DS exceeds the overdrive (1, 2 and 3 V respectively). Check one triode value by hand: V_GS = 3 V, V_DS = 1 V: I_D = 0.002 × (2 × 1 − 1²/2) = 0.002 × 1.5 = 3.0 mA ✓. `code/out.png` plots these curves with the dashed boundary I_D = (k/2) V_DS² between the two regions.

### The voltage-controlled resistor

For very small V_DS the V_DS² term vanishes and I_D ≈ k (V_GS − V_th) V_DS. That is Ohm's law with

```
R_DS = 1 / ( k × (V_GS − V_th) )
```

| V_GS | Formula | Simulator (V_DS = 10 mV) |
|---|---|---|
| 1.5 V | 1000 Ω | 1010 Ω |
| 2.0 V | 500 Ω | 502.5 Ω |
| 3.0 V | 250 Ω | 250.6 Ω |
| 5.0 V | 125 Ω | 125.2 Ω |

(The tiny differences are the V_DS²/2 term, still not quite zero at 10 mV.) This formula is the key to MOSFET switches (lesson 05): a power MOSFET with k = 5 A/V² and 2 V of overdrive has R_DS = 0.1 Ω.

### No gate current

The gate sits on glass. In steady state, no current flows into it at all. The script drives the gate of our 1 kΩ-loaded MOSFET with 3 V:

```
gate current 0.003 nA, drain current 4.000 mA, V_DS = 6.000 V
```

The 3 pA is not physics: it is a tiny conductance (10⁻¹² S) the simulator adds at every device for numerical safety. A real gate oxide leaks perhaps picoamps to nanoamps in modern ultra-thin chips, and essentially nothing in discrete parts. Compare the BJT, which needed 40 µA of base current for the same 4 mA.

The catch: the gate is a capacitor, so **changing** its voltage needs current (I = C dV/dt). A power MOSFET's gate can be several nanofarads; switching it in 100 ns needs amps of short pulses. Lesson 05 deals with it.

### PMOS: the mirror image

Swap every n for p: an n-type body, p⁺ source and drain, and a channel of holes. A PMOS turns on when its gate is *below* its source by more than |V_th|. It is normally used with the source at the positive rail:

```
        +5 V
          |
          S
   G --|PMOS        on when V_G < 5 - |V_th|
          D
          |
        [1 kΩ]
          |
        ground
```

With the gate at 2 V, V_SG = 3 V, overdrive 2 V. In saturation it would carry 4 mA, but 4 mA through 1 kΩ would put the drain at 4 V, leaving only 1 V across the PMOS, which is less than the 2 V overdrive, so it is in triode. Solving the triode equation together with the resistor gives the simulator's answer: **3.618 mA**, drain at 3.618 V. Pairs of NMOS and PMOS transistors make **CMOS** logic (Phase 14), the basis of every modern digital chip.

### MOSFET versus BJT

| | BJT | MOSFET |
|---|---|---|
| Control | base current, V_BE exponential | gate voltage, square law; no steady gate current |
| Turn-on voltage | ~0.6-0.7 V | V_th: 0.3-4 V depending on type |
| "Fully on" looks like | V_CE(sat) ≈ 0.1-0.3 V | a resistor R_DS(on), milliohms in power parts |
| g_m at 1 mA | 38.7 mA/V (I/V_T) | typically 2-10 mA/V |
| Main uses | precision analogue, RF, references | logic, memory, power switching, most of everything |

## Build It

### Step 1: The gate capacitor

`gate_capacitance` computes C_ox for 10 nm of SiO₂ and the electrons per volt for a 10 µm × 1 µm gate.

### Step 2: The model by hand and in the simulator

```python
def square_law(vgs, vds):
    overdrive = vgs - THRESHOLD
    if overdrive <= 0:
        return 0.0
    if vds < overdrive:
        return TRANSCONDUCTANCE_PARAMETER * (overdrive * vds - 0.5 * vds * vds)
    return 0.5 * TRANSCONDUCTANCE_PARAMETER * overdrive**2


def nmos_current(vgs, vds):
    circuit = Circuit()
    circuit.voltage_source("VG", "g", "0", vgs)
    circuit.voltage_source("VD", "d", "0", vds)
    circuit.nmos("M1", d="d", g="g", s="0", vth=THRESHOLD, k=TRANSCONDUCTANCE_PARAMETER)
    return circuit.dc().i("M1")
```

Our `square_law` and the simulator's `nmos` share the same equations, so the tables agree digit for digit.

### Step 3: Curves, resistance, gate current and PMOS

`show_transfer`, `show_output`, `show_resistor_mode`, `show_no_gate_current` and `show_pmos` print the tables of the Concept section; `plot` saves the output curves.

```
uv run python phases/12-transistors/04-the-mosfet/code/main.py
```

## Use It

- **2N7000 / BS170**: small NMOS parts (V_th 0.8-3 V, a few ohms on-resistance, 200-500 mA), the MOSFET equivalent of the 2N3904. Fine for driving an LED from 5 V logic; marginal from 3.3 V because of the wide threshold range.
- **Power MOSFETs**: IRLZ44N (logic-level, R_DS(on) about 22-35 mΩ at V_GS = 4-5 V, 47 A), AO3400 (SOT-23, 30 V, about 30-50 mΩ at 2.5-4.5 V). Datasheets give R_DS(on) only at specific V_GS values: always read it at *your* gate voltage.
- **Chips**: a modern CMOS process has V_th around 0.3-0.5 V, gate oxides (now "high-k" materials such as hafnium oxide) equivalent to about 1 nm of SiO₂, and channel lengths of a few tens of nanometres. The square law becomes only approximate at such sizes ("velocity saturation"), but the ideas here still hold.
- **ESD sensitivity**: a 10 nm oxide breaks down at about 10 V. The static on your finger is thousands of volts, which is why MOSFET parts ship in anti-static bags and have protection diodes on their gates.
- **Analogue switches** (e.g. CD4066) are MOSFETs used as voltage-controlled resistors in their triode region.

## Common Mistakes

- **Calling V_th "the on voltage".** At V_th the MOSFET is just barely on. Datasheets define V_th at a tiny current (often 250 µA). Fully on needs several volts of overdrive.
- **Confusing MOSFET and BJT "saturation".** For a MOSFET switch you want the *triode* region (small V_DS, resistor-like).
- **Ignoring the gate capacitance.** No DC gate current, but switching current pulses can be large.
- **Leaving a gate floating.** A charged gate stays charged: the MOSFET may stay on, or half on, indefinitely. Always give the gate a defined path (lesson 05).
- **Forgetting the body diode.** The body-to-drain pn junction is a diode from source to drain in every power MOSFET (drawn in its symbol). It conducts if the drain goes below the source.
- **Mixing up NMOS and PMOS gate polarity.** PMOS turns on when the gate is pulled *below* its source.

## Exercises

1. A gate oxide is 5 nm thick. What is C_ox in fF/µm²? How many electrons per volt does a 1 µm × 0.1 µm gate hold?
2. With V_th = 1 V and k = 2 mA/V², find I_D at V_GS = 2.5 V for V_DS = 0.5 V and for V_DS = 4 V. Which region is each in?
3. What V_GS makes R_DS = 100 Ω for k = 2 mA/V² and V_th = 1 V?
4. A MOSFET in saturation carries 1 mA at V_GS = 2 V and 4 mA at 3 V. Find V_th and k.
5. In `show_pmos`, change the gate to 0 V and to 3.5 V. In each case predict the region before running the script, then compare.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| MOSFET | "FET", "MOS" | Gate-insulated transistor; a gate voltage induces a channel between source and drain |
| Threshold V_th | "Turn-on voltage" | V_GS at which inversion begins; current is still small there |
| Overdrive | "V_ov" | V_GS − V_th; channel charge is proportional to it |
| Triode region | "Linear", "ohmic" | V_DS < V_GS − V_th; the channel acts as a resistor 1/(k V_ov) |
| Saturation (MOSFET) | "Active" | V_DS ≥ V_GS − V_th; I_D = (k/2) V_ov², nearly independent of V_DS |
| k | "β", "K_n", "μC_ox W/L" | Transconductance parameter in A/V², proportional to width over length |
| Gate capacitance | "C_iss", "gate charge" | The oxide capacitor that must be charged to turn the MOSFET on |
| Body diode | "Intrinsic diode" | The body-drain pn junction, a diode from source to drain |

## Further Reading

- *All About Circuits*, Volume III, chapter 6 "Insulated-Gate Field-Effect Transistors". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-6/insulated-gate-field-effect-transistors-igfet/
- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., chapter 3 "Field-Effect Transistors".
- B. Van Zeghbroeck, *Principles of Semiconductor Devices*, chapter 7 "MOS Field-Effect Transistors". https://web.archive.org/web/2021/https://ecee.colorado.edu/~bart/book/book/contents.htm (archived copy)
- MIT OpenCourseWare 6.012 *Microelectronic Devices and Circuits*, MOSFET lectures. https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/
