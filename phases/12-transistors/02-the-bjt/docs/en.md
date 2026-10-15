# The BJT

> Make the middle layer of an npn sandwich very thin. Electrons injected by the emitter do not have time to recombine in it: almost all of them fall into the collector. The few that do recombine are the base current, and their ratio is the transistor's gain.

**Type:** Learn
**Prerequisites:** 12-01 (The Transistor Idea); Phase 11 (Semiconductors and Diodes), lessons 02-doping-n-and-p, 03-the-pn-junction and 04-the-diode-equation
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| BJT (bipolar junction transistor) | A transistor made of three doped layers (npn or pnp) with two pn junctions | A sandwich with a very thin filling |
| Emitter (E) | The heavily doped outer layer that injects carriers | A crowded stadium exit pushing people out |
| Base (B) | The thin, lightly doped middle layer; the control terminal | A narrow corridor people run through |
| Collector (C) | The other outer layer, which collects the carriers | A big empty hall that swallows everyone arriving from the corridor |
| npn / pnp | Which way round the layers are doped; npn uses electrons as the main carriers, pnp uses holes | The same building in mirror image |
| β (beta), h_FE | Current gain: collector current divided by base current | How many people get through for each one who stops in the corridor |
| α (alpha) | Fraction of emitter current that reaches the collector, β/(β+1) | The percentage who make it through |
| Active region | Base-emitter forward, base-collector reverse: the transistor acts as a controlled current source | The corridor working as designed |
| Saturation | Both junctions forward biased: V_CE is tiny and the load limits the current | A traffic jam at the exit: pushing harder doesn't help |
| Cutoff | Base-emitter not forward biased: no current | The exit door shut |
| Output characteristic | A family of curves I_C versus V_CE, one per base current | A map of every possible state |
| V_CE | Collector-to-emitter voltage | How much "head room" the main path has |
| Recombination | An electron falling into a hole and both disappearing (Phase 11) | A runner tripping and sitting down in the corridor |

## Learning Objectives

- Describe the structure of an npn BJT and say why the base must be thin and the emitter heavily doped.
- Explain, step by step, how electrons get from emitter to collector, and where the base current comes from.
- Use I_C = I_S e^(V_BE/V_T), I_C = β I_B, I_E = I_C + I_B and α = β/(β+1).
- Identify the four operating regions from the bias of the two junctions.
- Read output characteristic curves and set a collector current with a base resistor.

## The Problem

Lesson 01 showed that a real NPN transistor lets microamps control milliamps, exactly 100 to 1 in our simulator. Why 100? Why does the current depend exponentially on the base-emitter voltage, like a diode, but flow out of a *different* terminal? And why does the "100 to 1" break down when the collector voltage gets too low?

Without the answers, you can copy circuits but not design them. With them, you can predict the current in any BJT circuit with a calculator, which is what this lesson does at the end: set 4.6 mA in a collector with nothing but a 180 kΩ resistor.

## The Physics

### The sandwich

An npn transistor is three regions in one crystal:

```
   emitter (n+)      base (p, thin)        collector (n)
  +--------------+------+---------------------------+
  | e e e e e e  | h  h |                           |
  | e e e e e e  |      |      e   e   e            |
  | e e e e e e  | h  h |                           |
  +--------------+------+---------------------------+
   heavily doped  ~1 µm   lightly doped, large
         E          B                C
```

Three design choices make it work:

1. **The emitter is heavily doped** (n⁺, perhaps 10¹⁹ donors per cm³): it has an enormous supply of electrons to inject.
2. **The base is thin** (around a micrometre or less) and only moderately doped p-type (say 10¹⁷ per cm³).
3. **The collector is large** and lightly doped, so it can stand a large reverse voltage.

There are two junctions: base-emitter (BE) and base-collector (BC). In normal use, the **BE junction is forward biased** (about 0.6-0.7 V) and the **BC junction is reverse biased** (the collector is several volts above the base).

### Step by step, an electron's journey

1. **Injection.** Forward-biasing BE lowers its barrier (lesson 11-03). Electrons pour from the n⁺ emitter into the p-type base, where they are *minority carriers*. How many? Exactly as in a diode: proportional to e^(V_BE/V_T).
2. **Crossing the base.** In the base they diffuse (wander randomly) away from the emitter, where they are crowded, toward the collector side, where there are none. A few meet holes and recombine on the way. But the base is so thin that crossing takes far less time than an electron typically survives before recombining. So almost all make it across.
3. **Collection.** At the far side of the base sits the reverse-biased BC junction, with its strong depletion field pointing from collector to base. For an electron arriving from the base that field is *downhill*: it is swept into the collector immediately. The collector is not "pulling" through some special force; it is the same field that blocks majority carriers but happily sweeps minority carriers across (the reverse saturation current of lesson 11-03, now fed by a huge injected supply).

```
         emitter          base           collector
        ----------->-----~~~~~->--------->------------>   most electrons (I_C)
                         \
                          x  recombines with a hole  ->  must be replaced: base current (I_B)
        <-----------  a few holes injected backwards from base into emitter (also I_B)
```

### Where the base current comes from

Two small leaks make up the base current:

- holes injected from the base back into the emitter (kept small because the emitter is far more heavily doped than the base);
- holes lost to recombination in the base (kept small because the base is thin).

Both leaks are proportional to the same e^(V_BE/V_T) as the main electron flow. So the *ratio* of collector current to base current is a constant, fixed by geometry and doping. That constant is **β** (beta). Typical small-signal transistors have β between 100 and 400; power transistors 20-100.

What the analogy gets wrong: in the corridor picture, people "decide" to sit down. Electrons don't decide; recombination is random, and β is a statistical average over trillions of electrons. It also varies a lot between individual transistors of the same type (a 2N3904 datasheet allows β from 100 to 300) and with temperature and current. Good circuits never rely on the exact value of β (lesson 06).

### Why "bipolar"

Both kinds of carriers matter: electrons carry the main current in an npn, holes make up the base current. Hence *bi*-polar. (In a MOSFET, lesson 04, only one kind matters: it is a *unipolar* device.)

### pnp

Swap every n and p and you get a **pnp**: holes are injected from a p⁺ emitter, cross an n base and are collected. All voltages and currents flip sign: the emitter sits at the top (most positive), the base is about 0.65 V *below* it, and current flows out of the collector. Same physics, mirror image.

## The Concept

### The three equations

```
I_C = I_S × e^(V_BE / V_T)          (the junction law, collector side)
I_B = I_C / β                        (the leak)
I_E = I_C + I_B = (β + 1) × I_B      (Kirchhoff: what goes in must come out)
```

Read them: "the collector current is the saturation current times e to the base-emitter voltage over the thermal voltage"; "the base current is the collector current divided by beta"; "the emitter current is the sum of the other two".

The fraction of emitter current that reaches the collector is

```
α = I_C / I_E = β / (β + 1)
```

For β = 100, α = 100/101 = 0.9901: 99 % of the injected electrons make it.

Our simulator, with I_S = 10⁻¹⁴ A and β = 100, collector held at 5 V:

| V_BE | I_C (formula I_S e^(V_BE/V_T)) | I_C (simulator) | I_B | I_E | α |
|---|---|---|---|---|---|
| 0.55 V | 0.0174 mA | 0.0174 mA | 0.174 µA | 0.0175 mA | 0.9901 |
| 0.60 V | 0.1201 mA | 0.1201 mA | 1.201 µA | 0.1213 mA | 0.9901 |
| 0.65 V | 0.8308 mA | 0.8308 mA | 8.308 µA | 0.8392 mA | 0.9901 |
| 0.70 V | 5.7475 mA | 5.7475 mA | 57.48 µA | 5.805 mA | 0.9901 |

Worked check at 0.65 V: 0.65 / 0.025852 = 25.14; e^25.14 = 8.31 × 10¹⁰; × 10⁻¹⁴ = 0.831 mA. ✓ I_B = 0.831 / 100 = 8.31 µA. ✓ I_E = 0.831 + 0.0083 = 0.839 mA. ✓

### Two ways to think about control

- **Voltage control** (physicist's view): V_BE sets I_C exponentially. This is what really happens, and it is the view you need for amplifiers (lesson 07).
- **Current control** (designer's shortcut): feed a base current I_B and the collector carries β × I_B. This view is handy for switch and bias calculations, because V_BE hardly changes (0.6-0.7 V) while the base current is set by a resistor.

Both are true at once; they are the same transistor described from two sides.

### The four regions

Two junctions, each forward or reverse, give four combinations. Our script forces each one:

| Region | BE junction | BC junction | Behaviour | Simulated (V_BE, V_BC → I_C, I_B) |
|---|---|---|---|---|
| Cutoff | reverse or off | reverse | no current: an open switch | 0, −5 V → 0, 0 |
| Active | forward | reverse | I_C = β I_B: amplifier / current source | 0.65, −4.35 V → 0.831 mA, 8.3 µA |
| Saturation | forward | forward | V_CE ≈ 0.1-0.2 V, I_C < β I_B: a closed switch | 0.75, +0.65 V → 38.1 mA, 1.23 mA |
| Reverse active | off | forward | emitter and collector swap roles, gain about 1 | 0, +0.65 V → −1.66 mA, 0.83 mA |

In saturation, look at the ratio: 38.1 / 1.23 ≈ 31, not 100. The forward-biased BC junction injects electrons *back* from the collector into the base, which cancels part of the forward flow and costs extra base current. Reverse active works but badly (the device is not built for it; our model uses a reverse β of 1).

### Output characteristics

Feed a fixed base current and sweep V_CE, the collector-emitter voltage. The simulator gives:

| I_B | V_CE = 0.05 | 0.10 | 0.15 | 0.20 | 0.30 | 0.50 | 1.0 | 5.0 | 10 V |
|---|---|---|---|---|---|---|---|---|---|
| 10 µA | 0.046 | 0.310 | 0.763 | 0.957 | 0.999 | 1.000 | 1.000 | 1.000 | 1.000 mA |
| 20 µA | 0.092 | 0.620 | 1.527 | 1.915 | 1.998 | 2.000 | 2.000 | 2.000 | 2.000 mA |
| 50 µA | 0.230 | 1.551 | 3.817 | 4.787 | 4.995 | 5.000 | 5.000 | 5.000 | 5.000 mA |

```
  I_C (mA)
   5 |      ___________________________________  I_B = 50 µA
     |     /
     |    /
   2 |   /________________________________________  I_B = 20 µA
   1 |  /_________________________________________  I_B = 10 µA
     | /
   0 +/----+----+----+----+----+----+----+----+--- V_CE (V)
     0  saturation |       active region (flat)
                 ~0.2 V
```

Above about 0.3 V the curves are **flat**: the collector current is β × I_B no matter what V_CE is. That is what "current source" means. The transistor adjusts its own voltage drop to keep the current constant. Below about 0.2 V the curves fall: saturation, where there is not enough V_CE to keep BC reverse biased. `code/out.png` plots these curves.

Real transistors' flat lines tilt slightly upward (the **Early effect**: a larger V_CE widens the BC depletion region, thinning the effective base and raising β a little). Our simulator's model leaves it out, so its lines are perfectly flat; keep that in mind when comparing with datasheets.

### Setting a current with a base resistor

```
          +9 V ----+----------+
                   |          |
                 [R_B]      [R_C] 1 kΩ
                 180 kΩ       |
                   |          +--- c
                   +--- b ---|Q1 (β = 100)
                              |
                            ground (e)
```

By hand, using the designer's shortcut: the base sits about 0.65 V above ground, so

```
I_B = (9 − 0.65) / 180,000 = 46.4 µA
I_C = β × I_B = 100 × 46.4 µA = 4.64 mA
V_CE = 9 − I_C × R_C = 9 − 4.64 = 4.36 V      (> 0.3 V, so the transistor is active: ✓)
```

The simulator gives V_BE = 0.6943 V (a bit more than our 0.65 V guess, as lesson 11-04 predicts for 4.6 mA), I_B = 46.14 µA, I_C = 4.614 mA, V_CE = 4.386 V. Our hand calculation was within 0.6 %. The transistor dissipates V_CE × I_C (plus a tiny V_BE × I_B) = 20.3 mW.

Notice that this design depends directly on β: a transistor with β = 200 would give 9.2 mA and saturate. Lesson 06 fixes that.

## Build It

### Step 1: Input side

```python
circuit = Circuit()
circuit.voltage_source("VC", "c", "0", 5.0)
circuit.voltage_source("VB", "b", "0", vbe)
circuit.npn("Q1", c="c", b="b", e="0", beta=BETA)
result = circuit.dc()
collector, base, emitter = result.i("Q1"), result.i("Q1.b"), result.i("Q1.e")
```

The simulator names a BJT's currents `Q1` (collector), `Q1.b` (base) and `Q1.e` (emitter).

### Step 2: Output curves with a sweep

```python
circuit.current_source("IB", "0", "b", base_current)
circuit.voltage_source("VC", "c", "0", 0.0)
circuit.npn("Q1", c="c", b="b", e="0", beta=BETA)
sweep = circuit.sweep("VC", collector_volts)
```

A current source pushes a fixed base current; `sweep` re-solves the operating point for each collector voltage, reusing each answer as the next starting guess.

### Step 3: Regions and the biased circuit

`regions()` forces both junction voltages with sources and prints I_C and I_B in each region. `biased_with_resistors()` builds the 9 V circuit above and compares hand and simulator.

```
uv run python phases/12-transistors/02-the-bjt/code/main.py
```

## Use It

- **2N3904 / BC547 / 2N2222**: the classic small NPNs. Datasheet h_FE (β) ranges such as 100-300 at 10 mA, V_CE(sat) about 0.2 V at 10 mA with I_B = 1 mA, maximum I_C 200 mA (2N3904) or 600 mA (2N2222), V_CEO (maximum collector-emitter voltage) 40 V.
- **Pinouts differ**: a 2N3904 in a TO-92 package is E-B-C looking at the flat face; a BC547 is C-B-E. Always check the datasheet: swapped C and E still "work" with β around 1-5, which is very confusing.
- **2N3906 / BC557**: their pnp complements, used for "high-side" switching, where the load sits between the transistor and ground.
- **Inside chips**: BJTs are still used in precision analogue chips (op-amps such as the OP07, bandgap references) and in RF (SiGe transistors in phones and radar) because their g_m per milliamp is the highest of any transistor.
- **Testing**: many multimeters have an "h_FE" socket that measures β by feeding a fixed base current. A diode-test across B-E and B-C shows two diodes of about 0.6-0.7 V, a quick way to tell npn from pnp and find the base.

## Try It in the Lab

The lab is the circuit from the Concept section: 9 V, a 1 kΩ collector resistor and an NPN with β = 100. Only the base resistor is free. Get about 5 mA of collector current while keeping the transistor in its active region.

Think about: how much base current do you need for 5 mA? What voltage does the base resistor see? After passing, try the smaller resistor. The collector current stops following β × I_B: why, and which goal catches it?

## Common Mistakes

- **Assuming β is a precise number.** It varies by 2-3× between parts and with temperature. Designs that need a precise current must not depend on it.
- **Forgetting V_BE.** The base resistor sees V_supply − 0.65 V, not V_supply. At low supplies (3.3 V) that matters.
- **Applying I_C = β I_B in saturation.** In saturation, the load sets I_C and β I_B is only an upper limit.
- **Driving the base with a voltage source and no resistor.** V_BE is exponential: 0.8 V straight on the base is amps of current. Always limit base current.
- **Mixing up npn and pnp polarity.** In a pnp the emitter is at the top, the base 0.65 V below it, and the collector current flows out toward the load.
- **Expecting reverse operation to work.** Swapping C and E gives β of about 1-5: the device is not symmetric.

## Exercises

1. An NPN with β = 150 carries I_B = 20 µA in the active region. What are I_C, I_E and α?
2. Using I_S = 10⁻¹⁴ A, what V_BE gives I_C = 2 mA?
3. In the lab circuit (9 V, R_C = 1 kΩ, β = 100), what is the smallest base resistor that keeps the transistor out of saturation (say V_CE ≥ 0.3 V)?
4. A pnp transistor has its emitter at +5 V, its base pulled through 100 kΩ to ground and its collector connected to ground through a 470 Ω resistor. With β = 100, estimate I_C, the direction it flows and the voltage across the 470 Ω resistor.
5. Modify `biased_with_resistors` to use β = 50 and β = 200. Tabulate I_C and V_CE. Which one saturates?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| BJT | "Transistor" | Three-layer, two-junction device; I_C = I_S e^(V_BE/V_T) in the active region |
| β, h_FE | "Gain" | I_C / I_B in the active region; set by emitter doping and base thinness; varies widely |
| α | "Transport factor" | I_C / I_E = β/(β+1), just under 1 |
| Active region | "Linear region" | BE forward, BC reverse; the collector acts as a current source |
| Saturation | "Fully on" | Both junctions forward; V_CE(sat) ≈ 0.1-0.3 V; I_C set by the load |
| Cutoff | "Off" | BE not forward biased; I_C ≈ 0 |
| Output characteristic | "Transistor curves" | I_C versus V_CE for a family of base currents |
| Early effect | "Output resistance" | Slight rise of I_C with V_CE from base-width narrowing (not modelled in our simulator) |

## Further Reading

- *All About Circuits*, Volume III, chapter 4 "Bipolar Junction Transistors" (active-mode operation, the transistor as a current source). https://www.allaboutcircuits.com/textbook/semiconductors/chpt-4/active-mode-operation-bjt/
- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., sections 2.1 (current-amplifier view) and 2.3 (Ebers-Moll view).
- onsemi 2N3904 datasheet: h_FE versus I_C, V_CE(sat), pinout. https://www.onsemi.com/pdf/datasheet/2n3903-d.pdf
- B. Van Zeghbroeck, *Principles of Semiconductor Devices*, chapter 5 "Bipolar Transistors" (carrier transport, Ebers-Moll model, Early effect). https://web.archive.org/web/2021/https://ecee.colorado.edu/~bart/book/book/contents.htm (archived copy)
