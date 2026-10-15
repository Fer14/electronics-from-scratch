# The pn Junction

> Put p-type and n-type silicon together and they build a hill between them all by themselves. Push one way and you flatten the hill; push the other way and you make it taller. That is a one-way street for current.

**Type:** Learn
**Prerequisites:** 11-02 (Doping: n-type and p-type); Phase 01 (The Physics Underneath), lessons 03-the-electric-field and 04-energy-potential-and-voltage; Phase 07 (Capacitors), lesson 02-capacitance
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Junction | The boundary where p-type and n-type silicon meet inside one crystal | The border between two countries drawn on a single continuous field |
| Diffusion | Particles spreading from where there are many to where there are few, just by random motion | A drop of ink spreading through a glass of still water |
| Drift | Charged particles moving because an electric field pushes them | Leaves carried by the wind |
| Recombination | A free electron falling into a hole; both disappear | A wanderer finding an empty seat and sitting down |
| Depletion region | A thin layer around the junction that has lost its mobile carriers, leaving only fixed charged ions | A "no man's land" between two armies where nobody walks |
| Built-in potential (V_bi) | The voltage step that forms across the junction on its own, from the left-behind ions | A small hill that grows at the border until people stop crossing it |
| Bias | An external voltage applied to the junction | Tilting the playing field |
| Forward bias | p side made more positive than n side: the hill gets lower | Lowering the hill so more people can walk over it |
| Reverse bias | n side made more positive than p side: the hill gets taller | Raising the hill until nobody can cross |
| Diode | A two-terminal part made of a pn junction; it lets current flow mostly in one direction | A one-way valve in a pipe, or a turnstile |
| Anode / cathode | The diode's p-side terminal (anode) and n-side terminal (cathode); conventional current flows anode to cathode | The entrance and exit of the turnstile |
| Thermal voltage (V_T) | kT/q, about 25.85 mV at room temperature: the voltage scale of thermal energy | The "height of a typical jump" in a crowd of jumping people |
| Permittivity | How much a material lets an electric field build up stored charge (the "ε" from capacitors) | How springy a mattress is when you press it |

## Learning Objectives

- Explain, step by step, why a depletion region and a built-in voltage form when p and n silicon meet.
- Compute the built-in potential from the doping levels.
- Describe what forward and reverse bias do to the barrier and to the depletion width.
- Explain why the forward current grows exponentially with voltage (the seed of the diode equation).
- Use our simulator to show that a diode conducts in one direction only.

## The Problem

In Phase 03 every part obeyed Ohm's law: double the voltage, double the current, and reverse the voltage, reverse the current. That symmetry is a problem when you want to turn the alternating current from the wall (which flips direction 100 times a second in Europe) into the steady direct current your phone needs. You need a part that lets current through one way and blocks it the other way, like a one-way valve.

People first did this with hot filaments in glass tubes (vacuum tube diodes, from 1904) and with a fine wire touching a lead-sulphide crystal (the "cat's whisker" of crystal radios). Both were fragile and finicky. The modern answer is the **pn junction**: a single crystal of silicon, p-type on one side, n-type on the other. No moving parts, nothing to heat up, and billions of them fit on a chip.

The pn junction is also the building block of every LED, solar cell, transistor and image sensor you will meet. Understand this one boundary and the rest of the phase, and much of Phase 12, follows.

## The Physics

### Step 1: The moment of contact

Imagine (this is a thought experiment; real junctions are made by doping one region of a crystal, not by gluing two pieces) that we bring a block of p-type silicon and a block of n-type silicon into perfect contact.

```
        p-type                     n-type
   +---------------------+---------------------+
   |  h   h   h   h   h  |  e   e   e   e   e  |
   |  -   -   -   -   -  |  +   +   +   +   +  |
   |  h   h   h   h   h  |  e   e   e   e   e  |
   +---------------------+---------------------+
   h = mobile hole                e = mobile electron
   - = fixed acceptor ion         + = fixed donor ion
   Both blocks are neutral: each mobile carrier is balanced by a fixed ion.
```

The p side is crowded with holes and has almost no free electrons. The n side is crowded with free electrons and has almost no holes.

### Step 2: Diffusion

Carriers jiggle randomly (heat). Random motion always spreads things from crowded places to empty places: that is **diffusion**, the same process that spreads ink in water or the smell of coffee through a room. Nothing pushes them; there are simply more of them on one side to wander across.

So electrons wander from the n side into the p side, and holes wander from the p side into the n side. When a wandering electron meets a hole, it falls into it: **recombination**. Both carriers vanish.

### Step 3: The ions are left behind

Here is the crucial point from lesson 02. The carriers moved, but the dopant ions are welded into the crystal and **cannot** move. Near the boundary:

- the n side has lost its electrons, so its **positive donor ions** are now uncovered;
- the p side has lost its holes, so its **negative acceptor ions** are now uncovered.

```
        p-type          depletion region          n-type
   +-------------------+---------+---------+-------------------+
   |  h   h   h   h    | -  -  - | +  +  + |    e   e   e   e  |
   |  -   -   -   -    | -  -  - | +  +  + |    +   +   +   +  |
   |  h   h   h   h    | -  -  - | +  +  + |    e   e   e   e  |
   +-------------------+---------+---------+-------------------+
                       <-- no mobile carriers -->
                       negative ions | positive ions
                            electric field points  <---  (from + to -)
```

This layer, emptied of mobile carriers, is the **depletion region**. It contains a slab of fixed negative charge next to a slab of fixed positive charge. Charges of opposite sign separated in space create an electric field (Phase 01), pointing from the positive ions on the n side toward the negative ions on the p side.

### Step 4: The field stops the flow

That field pushes back. It drives electrons (negative) back toward the n side and holes (positive) back toward the p side: a **drift** current opposite to the diffusion current. The more carriers diffuse, the more ions are uncovered, the stronger the field, the harder it pushes back. Eventually the two balance exactly: as many carriers diffuse across per second as are pushed back. This balance is **equilibrium**, and it arrives in a tiny fraction of a second.

### Step 5: The hill

A field over a distance means a voltage difference (Phase 01: voltage is how much energy a unit of charge gains or loses moving between two points). So in equilibrium the n side sits at a slightly higher potential than the p side. This is the **built-in potential**, V_bi.

The best mental image is a hill. For an electron on the n side, getting to the p side means climbing an energy hill of height q·V_bi. Only electrons with enough thermal energy make it over. Holes face the same hill from the other side.

```
   electron energy

   p side                          n side
   ________
           \
            \       hill height = q * V_bi
             \
              \_______________________   <- electrons sit down here,
                                            most can't climb back up
```

What the analogy gets wrong: a real hill is in space and gravity pulls everything the same way. This "hill" is in energy, and it points **opposite ways** for electrons and holes: electrons have to climb to go from n to p, and holes have to "climb" (in their own sense) to go from p to n. Same barrier, both carriers blocked.

### How tall is the hill?

The formula comes from requiring that, in equilibrium, the fraction of electrons able to climb the hill exactly matches the electron population on the other side:

```
V_bi = V_T × ln( N_A × N_D / n_i² )
```

Read: "the built-in potential equals the thermal voltage times the natural logarithm of (acceptor doping times donor doping, divided by n_i squared)". Here:

- `V_T = kT/q` is the **thermal voltage**: lesson 01's kT, written as a voltage. At 300 K, V_T = 0.025852 V ≈ 25.85 mV.
- `N_A` is the acceptor concentration on the p side, `N_D` the donor concentration on the n side, both per cm³.
- `n_i` ≈ 1 × 10¹⁰ per cm³ (silicon, 300 K).
- `ln` is the natural logarithm, the inverse of e^x. ln(10) ≈ 2.303.

Worked example: N_A = 10¹⁷, N_D = 10¹⁶.

```
N_A × N_D / n_i² = 1e17 × 1e16 / 1e20 = 1e13
ln(1e13) = 13 × 2.303 = 29.93
V_bi = 0.025852 × 29.93 = 0.774 V
```

Notice how weakly V_bi depends on doping: multiplying both dopings by 100 adds only 2 × ln(100) × V_T ≈ 0.24 V. Our script's table:

| N_A | N_D | V_bi |
|---|---|---|
| 10¹⁵ | 10¹⁵ | 0.595 V |
| 10¹⁷ | 10¹⁶ | 0.774 V |
| 10¹⁹ | 10¹⁶ | 0.893 V |
| 10¹⁸ | 10¹⁸ | 0.952 V |

You will recognise these numbers: the famous "a silicon diode drops about 0.6-0.7 V" is closely related to this hill (lesson 04 shows exactly how).

**You cannot measure V_bi with a voltmeter.** Touching the diode's terminals adds metal-silicon contacts that have their own built-in steps, and they exactly cancel the junction's. If they didn't, a diode on the shelf would be a free battery, which would violate energy conservation.

## The Concept

### How wide is the depletion region?

The ions in the depletion region must hold enough charge to create the hill. Solving the electrostatics (Gauss's law, from Phase 01, applied to two uniform slabs of charge) gives:

```
W = sqrt( 2 ε (V_bi − V) / q × (1/N_A + 1/N_D) )
```

Read: "the depletion width equals the square root of: two times the permittivity of silicon times the barrier voltage divided by the electron charge, times the sum of the inverse dopings". Symbols:

- `W` is the total width, in cm.
- `ε` (epsilon) is silicon's permittivity, 11.7 times that of empty space: 11.7 × 8.854 × 10⁻¹⁴ = 1.036 × 10⁻¹² F/cm.
- `V` is the applied voltage, positive for forward bias (we'll get there). With nothing connected, V = 0.
- `q` = 1.602 × 10⁻¹⁹ C.

Worked example, N_A = 10¹⁷, N_D = 10¹⁶, no bias:

```
2 × 1.036e-12 × 0.774 / 1.602e-19 = 1.001e7
1/N_A + 1/N_D = 1e-17 + 1e-16 = 1.1e-16
W = sqrt(1.001e7 × 1.1e-16) = sqrt(1.101e-9) = 3.32e-5 cm = 0.332 µm
```

A third of a micrometre: about 1/200 of a human hair's width.

**It reaches further into the lightly doped side.** The two slabs must hold equal and opposite charges (the whole thing is neutral). The p side has 10 times more ions per cm³, so it needs a slab 10 times thinner. Our table: 0.030 µm into the p side, 0.302 µm into the n side.

**The field is strong.** The peak field is about 2 × barrier / W = 2 × 0.774 / 3.32 × 10⁻⁵ = 46,600 V/cm. If you stretched that field over a centimetre of air it would make a spark (air breaks down near 30,000 V/cm). Inside the junction it is perfectly normal.

### Forward bias: lowering the hill

Connect a battery with **+ to the p side** and **− to the n side**. The battery's voltage opposes the built-in voltage, so the hill gets lower: its height becomes V_bi − V.

```
   forward bias:  + on p, - on n

   p side                      n side
   ________
           \___                         hill only (V_bi - V) high
               \______________________  many electrons now make it over
```

Now, how many carriers can get over? The energies of carriers in a hot crowd follow the Boltzmann law from lesson 01: the fraction with enough energy to climb a hill of height H (in volts) is proportional to exp(−H / V_T). Lowering the hill by V multiplies that fraction by

```
exp(V / V_T)
```

Read: "e to the applied voltage divided by the thermal voltage". This is the most important formula of the whole phase. Every 59.6 mV of extra forward bias (that is V_T × ln 10) multiplies the number of carriers crossing by **ten**. Our script:

```
forward V = 0.3 V   hill = 0.474 V   climbers x  1.096e+05
forward V = 0.5 V   hill = 0.274 V   climbers x  2.510e+08
forward V = 0.7 V   hill = 0.074 V   climbers x  5.748e+11
```

Going from 0.3 V to 0.7 V raises the crossing rate by a factor of five million. Electrons that cross into the p side become *minority carriers* there; they diffuse onward and eventually recombine with holes, while the battery supplies fresh electrons on the n side and removes electrons (creates fresh holes) on the p side. The result is a steady current that is tiny at low voltage and then rises explosively once the hill is low enough. In silicon that "explosion" becomes noticeable around 0.5-0.6 V for everyday currents.

The depletion region also gets thinner (fewer ions are needed to hold a smaller barrier): 0.231 µm at +0.4 V.

### Reverse bias: raising the hill

Connect the battery the other way: **+ to the n side**. Now the battery adds to the built-in voltage. The hill becomes V_bi + |V| tall, and the fraction of carriers that can climb it collapses to essentially zero.

What does still flow? The **minority carriers**. A few holes do exist on the n side (10⁴ per cm³ for our doping), and a few electrons on the p side. Any of those that wander into the depletion region are **swept downhill** by the field. That trickle is independent of how high the hill is (they roll down it, they don't climb), so it is a tiny constant current called the **saturation current**, I_S. For a small silicon diode it is in the range of 10⁻¹⁵ to 10⁻⁹ A. (Real diodes leak somewhat more, because carriers are also generated inside the depletion region itself.)

The depletion region widens under reverse bias: 0.906 µm at −5 V, 1.72 µm at −20 V. More ions must be uncovered to hold the larger voltage.

### The one-way street

Put it together:

```
          FORWARD (+ on p)                        REVERSE (+ on n)
   hill lowered, carriers pour over      hill raised, only a trickle of minority
   current grows ×10 every ~60 mV       carriers rolls down: I ≈ −I_S, tiny
```

The schematic symbol of a diode is an arrow showing the easy direction for conventional current, with a bar at the n side:

```
        anode (p)  ----|>|----  cathode (n)
                   current flows this way -->
                   (the bar marks the cathode; on real parts it is a painted band)
```

### The depletion region is a capacitor

Two slabs of opposite charge separated by an insulating layer (the depletion region has no mobile carriers, so it insulates): that is a capacitor (Phase 07). Its capacitance per unit area is the parallel-plate formula, C = ε / W. Because W changes with voltage, so does C:

| Applied V | W (µm) | C (nF per cm²) |
|---|---|---|
| +0.4 | 0.231 | 44.9 |
| 0 | 0.332 | 31.2 |
| −5 | 0.906 | 11.4 |
| −20 | 1.719 | 6.0 |

A junction of 0.1 mm × 0.1 mm (10⁻⁴ cm²) at −5 V has about 1.1 pF. **Varactor diodes** exploit this: a voltage-controlled capacitor used to tune radios (Phase 10's resonance, tuned by a voltage).

### Ask the simulator

Our simulator models a diode by the law you will meet properly in the next lesson. Here we only ask it the one-way-street question: a 5 V source, a 1 kΩ resistor and a diode, first one way round, then the other:

```
        R1 1k                                 R1 1k
  5V ---/\/\/--- a ---|>|--- 0          5V ---/\/\/--- a ---|<|--- 0
                   forward                                reverse
```

The script prints:

```
forward (anode toward +)       V(diode) =  0.6925 V   I =   4.307456 mA
reverse (anode toward ground)  V(diode) =  5.0000 V   I =   0.000000 mA
```

Forward: the diode settles near 0.69 V (0.6925 V) and the resistor takes the rest, (5 − 0.69) / 1000 ≈ 4.3 mA. Reverse: essentially all 5 V appear across the diode and the current is about 10⁻¹⁴ A, a millionth of a millionth of a milliamp.

## Build It

### Step 1: The built-in potential

```python
def built_in_potential(acceptors, donors):
    return THERMAL_VOLTAGE * np.log(acceptors * donors / NI**2)
```

### Step 2: Depletion width and its split

```python
def depletion_width_cm(acceptors, donors, applied=0.0):
    barrier = built_in_potential(acceptors, donors) - applied
    return np.sqrt(2 * SILICON_PERMITTIVITY_F_PER_CM * barrier / ELECTRON_CHARGE * (1 / acceptors + 1 / donors))
```

`side_widths_cm` splits W in inverse proportion to the doping (equal charge on both sides), and `peak_field_v_per_cm` uses 2 × barrier / W (the field profile is a triangle, so the peak is twice the average).

### Step 3: Hill climbers

```python
ratio = np.exp(applied / THERMAL_VOLTAGE)
```

This is the Boltzmann factor for a hill lowered by `applied` volts.

### Step 4: The simulator test

```python
circuit = Circuit()
circuit.voltage_source("V1", "in", "0", 5.0)
circuit.resistor("R1", "in", "a", 1000)
circuit.diode("D1", anode, cathode, Is=1e-14, n=1.0)
result = circuit.dc()
```

Swapping `anode` and `cathode` turns the diode around.

Run it:

```
uv run python phases/11-semiconductors-and-diodes/03-the-pn-junction/code/main.py
```

## Use It

- **Rectifier diodes** such as the 1N4001-1N4007 family: large-area junctions that pass up to 1 A forward and block 50-1000 V in reverse (the 1N4007 blocks 1000 V). Their datasheets list "maximum repetitive reverse voltage" (how tall a hill you may build before something gives) and "forward voltage at 1 A" (about 1.1 V max).
- **Small-signal diodes** like the 1N4148: tiny junction, about 4 pF of junction capacitance at 0 V, switch in nanoseconds.
- **Varactors** (e.g. the BB910 family) are junctions optimised for a large change of capacitance with reverse voltage, used in TV and FM tuners.
- **Solar cells and photodiodes** are large pn junctions. Light creates electron-hole pairs in or near the depletion region, and the built-in field sweeps them apart: electrons to n, holes to p. That separated charge is the current a solar panel delivers.
- **Inside every chip**, each transistor sits in wells whose pn junctions are kept reverse-biased so that neighbouring devices are isolated from each other.

## Common Mistakes

- **"The depletion region is where current flows."** It is the region *with no* mobile carriers. Carriers cross it quickly under forward bias, but its defining feature is that it is emptied.
- **"Electrons flow because the n side has extra electrons and the p side wants them."** In equilibrium, net flow is zero: diffusion and drift exactly balance. A current needs an external voltage that upsets the balance.
- **"A diode in reverse has exactly zero current."** It has a tiny leakage current (I_S plus generation), which roughly doubles every 10 °C. It matters in sample-and-hold circuits and low-power designs.
- **"V_bi is the 0.7 V you measure across a diode."** They are related but different. The measured forward voltage depends on the current (next lesson), and V_bi cannot be measured with a voltmeter at all.
- **Mixing up which side is which.** Anode = p = the triangle's flat side in the symbol. Cathode = n = the bar, and the painted band on the part.

## Exercises

1. Compute V_bi for N_A = 10¹⁶ and N_D = 10¹⁸ per cm³. Which side does the depletion region mostly extend into?
2. Using the depletion-width formula, by what factor does W grow when the reverse bias goes from 0 V to −10 V for the junction in the lesson? (Hint: W is proportional to the square root of the barrier.)
3. How much extra forward voltage multiplies the current by 1000? By 1,000,000?
4. A photodiode has an area of 1 mm² and the same doping as the lesson. Estimate its capacitance at −5 V. If it drives a 10 kΩ resistor, what time constant (RC, Phase 07) limits its speed?
5. In the script, change `Is` in `one_way_street` from 1e-14 to 1e-9 (a leakier, more "1N4148-like" junction). How do the forward voltage and the reverse current change? Explain both with the hill picture.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| pn junction | "The diode" | The boundary inside one crystal between p-doped and n-doped silicon |
| Depletion region | "The barrier" | The layer around the junction emptied of mobile carriers, leaving fixed ions and a strong field |
| Built-in potential | "The junction voltage" | The equilibrium potential step V_bi = V_T ln(N_A N_D / n_i²), about 0.6-0.95 V in silicon; not measurable with a meter |
| Forward bias | "Turning the diode on" | p side more positive; lowers the barrier, current rises as exp(V/V_T) |
| Reverse bias | "Diode off" | n side more positive; raises the barrier, only the small saturation current flows |
| Saturation current I_S | "Leakage" | The reverse current from minority carriers swept across the junction; sets the scale of the forward current too |
| Junction capacitance | "Diode capacitance" | The voltage-dependent capacitance C = εA/W of the depletion region |
| Thermal voltage V_T | "26 millivolts" | kT/q, the voltage scale of thermal energy; 25.85 mV at 300 K |

## Further Reading

- *All About Circuits*, Volume III, chapter 2, "The P-N junction". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-2/the-p-n-junction/
- B. Van Zeghbroeck, *Principles of Semiconductor Devices*, chapter 4 "p-n Junctions" (electrostatics, depletion width, capacitance). https://web.archive.org/web/2021/https://ecee.colorado.edu/~bart/book/book/contents.htm (archived copy)
- P. Horowitz and W. Hill, *The Art of Electronics*, 3rd ed., chapter 1.6 "Diodes and diode circuits".
- MIT OpenCourseWare 6.012 *Microelectronic Devices and Circuits*, lecture notes on the pn junction. https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/
