# Why Silicon

> An electron can only sit on certain shelves. In a metal the top shelf is half empty, so electrons move freely. In glass the next shelf is far out of reach. In silicon it is just out of reach, and that "just" is the whole electronics industry.

**Type:** Learn
**Prerequisites:** Phase 01 (The Physics Underneath), especially 03-atoms-and-electrons and 07-conductors-insulators-and-semiconductors; Phase 03 (Resistance and Ohm's Law), lesson 02-resistivity-and-wires
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Energy level | One of the specific amounts of energy an electron in an atom is allowed to have | A shelf in a bookcase: a book can sit on a shelf, never between two shelves |
| Energy band | In a solid, millions of atoms' levels merge into a thick stack of very close shelves | A shelf so wide and so packed with slots that it looks like one long plank |
| Valence band | The highest band that is completely full of electrons at very low temperature | The packed bottom shelf of a library: every slot holds a book |
| Conduction band | The next band up, empty at very low temperature | The empty shelf above: any book that gets there can slide around freely |
| Band gap | The energy distance between the top of the valence band and the bottom of the conduction band; no allowed shelves in between | The height you must lift a book to get it from the full shelf onto the empty one |
| Electronvolt (eV) | A tiny unit of energy: the energy one electron gains crossing 1 volt | A "small coin" for counting electron energies |
| Thermal energy (kT) | The typical amount of energy heat hands to one particle at temperature T | The random shoves people give each other in a crowd: bigger when the crowd is more agitated |
| Kelvin (K) | Temperature measured from absolute zero; 0 °C = 273.15 K | The Celsius scale shifted so that "no heat at all" is zero |
| Intrinsic | Pure, with no foreign atoms added | Plain water, before you add salt |
| Carrier | Anything that carries charge and can move: a free electron, or (next lesson) a hole | A delivery van: what matters is that it moves and carries something |
| Crystal | Atoms arranged in a perfectly repeating 3-D pattern | Oranges stacked in a market in a regular pyramid |
| Covalent bond | Two neighbouring atoms sharing a pair of electrons | Two people holding the same rope, one hand each |
| Semiconductor | A material whose band gap is small enough that a few electrons cross it at room temperature | A wall short enough that a few athletic people climb over it, but not most |

## Learning Objectives

- Describe energy bands as "allowed shelves" for electrons and explain the band gap in plain words.
- Explain why metals conduct, insulators do not, and semiconductors sit in between, using only the idea of full and empty shelves.
- Compute the thermal energy kT at a given temperature and compare it with a band gap.
- Estimate how many free electrons pure silicon has at room temperature, and why that number explodes when it warms up.
- Say why silicon (and not germanium, copper or glass) became the material of chips.

## The Problem

Everything you have built so far uses parts with a fixed personality. A resistor of 1 kΩ is 1 kΩ whether you look at it or not. A wire conducts, a plastic insulator does not. Those parts are useful, but they cannot *decide* anything. They cannot let current pass one way and block it the other way, they cannot amplify a faint signal, and they certainly cannot compute.

To build a radio, a phone charger or a processor, you need a material whose ability to conduct can be *changed*: by adding a pinch of other atoms, by applying a voltage, by shining light on it. That is what a semiconductor offers, and almost all of modern electronics is built on one semiconductor in particular: silicon.

The question for this lesson is simple to ask and deep to answer: what is so special about silicon? To answer it we have to look at where electrons are allowed to be inside a solid. By the end you will be able to calculate, with a pocket calculator, why a block of pure silicon is a poor conductor at room temperature, why it becomes a much better one when hot, and why that is both a feature and a headache.

## The Physics

### Electrons live on shelves

In Phase 01 you met the atom: a tiny heavy nucleus with electrons around it. One fact from quantum physics changes everything here: **an electron bound to an atom cannot have just any energy**. It can only have certain specific amounts. Physicists call them *energy levels*.

Picture a bookcase. A book can rest on the first shelf or on the second shelf, but never float halfway between them. To move a book from a lower shelf to a higher one you must lift it, which costs energy. If a book falls down a shelf, it releases energy (in an atom that energy often leaves as a flash of light: remember this, it comes back in the LED lesson).

What the analogy gets wrong: real electrons are not little balls sitting still on a plank. "Being on a shelf" really means "having that much energy", and the electron is spread out like a cloud around the atom. But for everything in this phase, the shelf picture gives the right answers.

There is one more rule: **each slot on a shelf holds at most one electron** (this is the Pauli exclusion principle; strictly, each slot holds two electrons with opposite "spin", which we can fold into the count of slots). So shelves fill up from the bottom, like a library where books are pushed as low as possible.

### Many atoms: shelves become bands

One atom has a few sharp shelves. Now put many atoms close together, as in a solid. Their electron clouds overlap, and the atoms feel each other. Each sharp shelf splits into many shelves at slightly different heights, one per atom. A grain of silicon the size of a sugar cube has about 10²² atoms, so each original shelf turns into 10²² shelves packed so tightly that they act like a continuous plank. That plank is an **energy band**.

```
   one atom                    a solid (many atoms)

   ---------  level 2          ===================  band from level 2
                               (billions of very close shelves)
   ---------  level 1          ===================  band from level 1

```

Between the bands there may be regions with **no shelves at all**. An electron simply cannot have an energy in that range. Those empty regions are **band gaps**.

### Which bands matter

Only two bands matter for conduction:

- the **valence band**: the highest band that the atoms' outer electrons fill completely (at very low temperature);
- the **conduction band**: the next band above it.

Here is the key idea of the whole lesson. To carry current, an electron must be able to *gain a tiny bit of energy* when you push it with an electric field. Gaining a little energy means moving to a slightly higher slot. In a **completely full** band, every slot is taken: an electron cannot move up because the slot above is occupied, and nothing changes. A full band carries no current, no matter how hard you push. An **empty** band also carries no current, because there is nothing in it to move.

So current needs a band that is **partly** filled.

### Metal, insulator, semiconductor

```
  METAL (copper)          INSULATOR (glass)          SEMICONDUCTOR (silicon)

  |..........|            |          |  conduction    |   . .    |  conduction
  |##########|  <- top    |          |  band (empty)  |          |  band (almost empty)
  |##########|  band is   |          |                +----------+
  |##########|  half full +----------+                     ^ gap 1.12 eV
  |##########|                 ^                      +----------+
                               |  gap about 9 eV      |######o###|  valence band
                          +----------+                |##########|  (almost full)
                          |##########|  valence band  +----------+
                          |##########|  (full)
                          +----------+
  # = shelf slot filled    . = electron in an upper band    o = empty slot left behind
```

- **Metal.** The top band is only half full. Every electron near the top has an empty slot just above it, so the smallest push moves it. Copper has about one free electron per atom: a huge crowd of carriers. Copper conducts superbly.
- **Insulator.** The valence band is completely full and the conduction band completely empty, with a big gap between them (about 9 eV for glass). No band is partly filled, so no current flows.
- **Semiconductor.** Same structure as an insulator (full band, gap, empty band) but the gap is **small**: 1.12 eV for silicon. Small enough that heat alone kicks a few electrons across. Each one that makes it lands in an almost empty conduction band and can move freely. It also leaves an empty slot behind in the valence band, which (as the next lesson shows) also lets current flow.

What the shelf picture gets wrong: in reality, bands are not flat planks the same everywhere; the allowed energies depend on the electron's direction of motion in the crystal. That detail decides things like how fast electrons move, and why silicon emits light poorly. We will not need it.

### Heat is a random shove

Atoms in a solid jiggle all the time; that jiggling *is* temperature. The jiggling constantly hands small random amounts of energy to electrons. The typical size of these shoves is

```
thermal energy = k × T
```

Read it as: "the typical energy heat gives one particle equals Boltzmann's constant times the absolute temperature". Here:

- `T` is the temperature in **kelvin** (K): degrees Celsius plus 273.15. Room temperature, 27 °C, is about 300 K.
- `k` is **Boltzmann's constant**, 8.617 × 10⁻⁵ eV per kelvin. It just converts "how hot" into "how much energy per particle".
- The result is in **electronvolts** (eV). One eV is the energy an electron picks up when it crosses a 1 V difference, 1.602 × 10⁻¹⁹ joules. Electron energies are so small that joules are awkward; eV is the natural coin.

Worked example, room temperature:

```
kT = 8.617e-5 eV/K × 300 K = 0.02585 eV = 25.85 meV  (milli-electronvolts)
```

Remember that number, **about 26 mV when written as a voltage**: it will appear in the diode equation in lesson 04 and in every transistor formula in Phase 12.

Compare: silicon's gap is 1.12 eV, which is **43 times** larger than kT. So a typical shove is far too small. But shoves are random, and once in a while one is huge. How often? Statistical physics (the Boltzmann factor) says the chance of a shove big enough falls off exponentially:

```
chance  ~  exp( -Eg / (2 kT) )
```

Read it: "the chance roughly equals e raised to minus the gap divided by two kT". (`exp(x)` means e^x, with e ≈ 2.718. The factor 2 appears because the crossing creates two carriers at once, an electron and an empty slot, and the energy cost is shared; you can take that as given.)

For silicon at 300 K: Eg / (2kT) = 1.12 / 0.0517 = 21.7, and e^(-21.7) ≈ 3.9 × 10⁻¹⁰. Tiny, but silicon has 5 × 10²² atoms per cubic centimetre, so even a tiny fraction adds up to billions of free electrons.

## The Concept

### The number of free electrons in pure silicon

The careful formula for the number of free electrons per cubic centimetre in a pure ("intrinsic") semiconductor is

```
n_i = sqrt(Nc × Nv) × exp( -Eg / (2 kT) )
```

Read it: "the intrinsic carrier density equals the square root of Nc times Nv, times the Boltzmann chance". `Nc` and `Nv` are the "effective number of slots" near the edge of the conduction and valence bands (for silicon at 300 K about 2.8 × 10¹⁹ and 1.04 × 10¹⁹ per cm³). Think of them as "how many seats are available close to the edge of each shelf". They grow slowly with temperature, as T^1.5.

Worked example, silicon at 300 K:

```
sqrt(2.8e19 × 1.04e19) = sqrt(2.91e38) = 1.71e19
n_i = 1.71e19 × 3.91e-10 = 6.7e9   free electrons per cm³
```

Our simple model gives 6.7 × 10⁹; careful measurements give about 1 × 10¹⁰ per cm³ (the exact value depends on subtle corrections). Either way the size is what matters. Compare with silicon's 5 × 10²² atoms per cm³:

```
5e22 / 6.7e9 ≈ 7.5e12
```

**Only about one atom in seven trillion has lost an electron to the conduction band.** Copper, by contrast, has roughly one free electron per atom: 8.5 × 10²² per cm³, ten trillion times more.

### From carriers to resistivity

In Phase 03 you met resistivity ρ (rho), measured in ohm-metres: how strongly a material resists current, independent of its shape. Its inverse, conductivity σ (sigma), is roughly

```
σ = q × (n × μn + p × μp)
```

Read: "conductivity equals the charge of one carrier times the sum, over the kinds of carriers, of how many there are times how easily they move". Here `q` is 1.602 × 10⁻¹⁹ coulombs, `n` the number of free electrons per cm³, `p` the number of empty slots (holes, next lesson; in pure silicon p = n), and `μ` (mu) the **mobility**: how fast a carrier drifts per volt per centimetre of push, in cm²/(V·s). In silicon, electrons drift with μn ≈ 1350 and holes with μp ≈ 480.

Worked example, pure silicon:

```
σ = 1.602e-19 × (6.7e9 × 1350 + 6.7e9 × 480)
  = 1.602e-19 × 6.7e9 × 1830
  = 1.96e-6   siemens per cm
ρ = 1 / σ = 5.1e5 ohm·cm = 5.1e3 ohm·m
```

A 1 cm cube of pure silicon (side 0.01 m) has resistance R = ρ × length / area = 5100 × 0.01 / 0.0001 = 510 kΩ. The same cube of copper: 1.7 microohms. Pure silicon is a lousy conductor, about **3 × 10¹¹ times worse than copper**. But it is about 10¹⁰ times better than glass.

### The odd temperature behaviour

Copper gets slightly *worse* at conducting when it warms up: its number of free electrons is fixed, and the stronger atomic jiggling scatters them more. Pure silicon does the opposite and does it violently, because the Boltzmann chance is exponential. Our script finds that warming from 300 K to 310 K **doubles** n_i. From 25 °C to 125 °C, n_i grows by a factor of about 370.

This is a feature (thermistors and temperature sensors exploit it) and a problem: a chip that relied on intrinsic carriers would change its behaviour every time the room warmed up. The fix, in the next lesson, is to add a controlled number of carriers on purpose, so many that the thermal ones become a rounding error. That is called **doping**.

### Why silicon won

Three semiconductors appear in the code. Why did silicon take over?

| Material | Gap (eV) | n_i at 300 K (our model) | Story |
|---|---|---|---|
| Germanium | 0.66 | 2.3 × 10¹³ per cm³ | First transistors (1947). Small gap: too many thermal carriers, leaky and unreliable when warm. |
| Silicon | 1.12 | 6.7 × 10⁹ per cm³ | Gap large enough to work up to ~150 °C. Its oxide, SiO₂, is a superb insulator that grows on it naturally. Made from sand: cheap and abundant. |
| Gallium arsenide | 1.42 | 2.1 × 10⁶ per cm³ | Fast electrons and good at emitting light, but expensive, brittle and lacks a good native oxide. Used for RF and LEDs/lasers. |

The **native oxide** deserves one more sentence. Heat silicon in oxygen and it grows a glass skin (silicon dioxide) that sticks perfectly to it. That skin insulates, protects, and can be patterned with light. The MOSFET in Phase 12 is literally "Metal on Oxide on Semiconductor": a gate sitting on that glass skin. No other semiconductor has an oxide as good, and that is a big part of why your phone is made of silicon.

### Crystals and bonds: where the gap comes from

A silicon atom has 4 outer electrons (it sits in column 14 of the periodic table, below carbon). In a crystal, each silicon atom shares one electron with each of its 4 neighbours, and each neighbour shares one back. Every atom ends up "holding" 8 shared electrons in 4 covalent bonds, a very stable arrangement.

```
     Si   Si   Si          each "=" is a covalent bond:
      \\  ||  //           a pair of shared electrons
   Si = Si = Si = Si
      //  ||  \\           (drawn flat; really a 3-D diamond pattern)
     Si   Si   Si
```

In the band picture, "all bonds intact" means "valence band full". To free an electron you must break a bond, which costs about 1.12 eV: that is the band gap seen from the chemistry side. Break one, and you get a free electron **and** a broken bond with a missing electron. That missing electron is the hero of the next lesson.

## Build It

The script `code/main.py` turns the formulas above into numbers. It uses plain Python and NumPy; no circuit simulator is needed yet.

### Step 1: Thermal energy

```python
BOLTZMANN_EV = 8.617e-5

def thermal_energy_ev(kelvin):
    return BOLTZMANN_EV * kelvin
```

The output shows kT = 6.64 meV in liquid nitrogen (77 K), 25.85 meV at room temperature (300 K) and 34.47 meV in a hot chip (400 K).

### Step 2: How unlikely a jump is

```python
def boltzmann_chance(gap_ev, kelvin):
    return np.exp(-gap_ev / (2 * thermal_energy_ev(kelvin)))
```

At 300 K the script prints:

```
germanium         Eg = 0.66 eV   exp(-Eg/2kT) = 2.86e-06
silicon           Eg = 1.12 eV   exp(-Eg/2kT) = 3.91e-10
gallium arsenide  Eg = 1.42 eV   exp(-Eg/2kT) = 1.18e-12
glass (SiO2)      Eg = 9.00 eV   exp(-Eg/2kT) = 2.51e-76
```

Notice how a gap only 8 times larger (glass vs silicon) changes the chance by 66 orders of magnitude. Exponentials are brutal.

### Step 3: Intrinsic carrier density

```python
def intrinsic_density(material, kelvin):
    scale = (kelvin / 300.0) ** 1.5
    nc = material["nc_300"] * scale
    nv = material["nv_300"] * scale
    return np.sqrt(nc * nv) * np.exp(-material["gap_ev"] / (2 * thermal_energy_ev(kelvin)))
```

Each material is a small dictionary with its gap, its Nc and Nv at 300 K, and its mobilities. The output for silicon: `n_i = 6.67e+09 per cm^3 (about 1 in 7.5e+12 atoms)`.

### Step 4: Resistivity

```python
def resistivity_ohm_m(electrons_per_cm3, holes_per_cm3, mu_n, mu_p):
    conductivity_per_ohm_cm = ELECTRON_CHARGE * (electrons_per_cm3 * mu_n + holes_per_cm3 * mu_p)
    return 1.0 / conductivity_per_ohm_cm / 100.0
```

Because the densities are per cm³ and mobilities in cm²/(V·s), the conductivity comes out in siemens per centimetre; dividing the resulting ohm·cm by 100 converts to ohm·m. Output: pure silicon 5.1 × 10³ Ω·m, about 3 × 10¹¹ times copper.

### Step 5: The temperature sweep

The last table runs from -40 °C to 150 °C:

```
 T (C)   n_i (per cm^3)   rho (ohm*m)
   -40         9.17e+06     3719343.8
    25         5.78e+09        5904.0
   100         6.46e+11          52.8
   150         6.11e+12           5.6
```

Resistivity falls by a factor of almost a million over that range. This is why "intrinsic" silicon is useless for building predictable circuits, and why the next lesson matters.

Run it:

```
uv run python phases/11-semiconductors-and-diodes/01-why-silicon/code/main.py
```

## Use It

- **Wafers.** Chips start as cylinders of nearly perfect single-crystal silicon (purity better than 99.9999999 %, "nine nines") grown by slowly pulling a seed crystal out of molten silicon (the Czochralski process). The cylinder is sliced into wafers, 300 mm across in modern fabs.
- **Thermistors and temperature sensors.** NTC (negative temperature coefficient) thermistors use semiconducting oxides whose resistance falls steeply with temperature, exactly the behaviour of our table. A typical 10 kΩ NTC drops to about 3.6 kΩ at 50 °C.
- **Maximum junction temperature.** Datasheets of silicon parts list a maximum junction temperature, usually 150 °C or 175 °C. Above that, thermal carriers start to rival the designed ones and the device stops behaving. Germanium parts were limited to about 75-100 °C for the same reason, with its smaller gap.
- **Solar cells.** A photon (a particle of light) with energy above 1.12 eV can kick an electron across silicon's gap. Red light carries about 1.8 eV, so visible light works. Infrared beyond about 1100 nm does not, and silicon is transparent to it.
- **Wide-gap materials.** Silicon carbide (SiC, gap about 3.3 eV) and gallium nitride (GaN, about 3.4 eV) power electric-car inverters and small USB-C chargers. Their large gaps keep thermal carriers rare even when very hot and let them withstand high voltages.

## Common Mistakes

- **"Semiconductors conduct half as well as metals."** No. Pure silicon conducts about 10¹¹ times worse than copper. "Semi" refers to sitting between conductors and insulators on a scale of many orders of magnitude, and to being *controllable*.
- **"The band gap is a physical gap in space."** It is a gap in *energy*, not in distance. Electrons in the valence and conduction bands occupy the same crystal.
- **"A full band is full of current."** A completely full band carries none: no electron can change its state because every nearby slot is taken.
- **"Heat always increases resistance."** True for metals, false for pure semiconductors, whose resistance drops steeply when hot.
- **Mixing up kT in joules and in eV.** In eV, kT at 300 K is 0.0259. In joules it is 4.14 × 10⁻²¹. Pick one unit and stay with it.
- **Forgetting kelvin.** Plugging 27 (°C) into kT instead of 300 (K) gives an answer 11 times too small and a Boltzmann chance that is absurdly tiny.

## Exercises

1. Compute kT in eV at 0 °C and at 100 °C. By what percentage does it change?
2. Using `chance ~ exp(-Eg / 2kT)`, how much more likely is a jump across germanium's gap than across silicon's at 300 K? (Answer to check: about 7300 times.)
3. A cube of pure silicon 1 mm on each side sits between two metal plates. Using ρ = 5100 Ω·m, what is its resistance? What current flows if you apply 5 V? (R = ρ·L/A.)
4. Change the script to add diamond (Eg = 5.5 eV, take Nc = Nv = 1 × 10¹⁹ per cm³, μn = 2000, μp = 1800). Is pure diamond a semiconductor or an insulator at room temperature? What about at 1000 K?
5. A red photon has a wavelength of 650 nm. Its energy in eV is about 1240 / wavelength-in-nm. Can it free an electron in silicon? In gallium arsenide? In glass?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Band gap | "How hard it is to conduct" | The energy range with no allowed electron states between the full valence band and the empty conduction band |
| Valence band | "Where the bonded electrons are" | The highest band that is full at low temperature; it carries current only once it has empty slots |
| Conduction band | "Where free electrons go" | The band above the gap; electrons there have empty slots around them and move freely |
| kT | "Thermal voltage" (when divided by q) | Typical thermal energy per particle; 25.85 meV at 300 K |
| Intrinsic | "Pure silicon" | A semiconductor whose carriers all come from thermal excitation across the gap |
| n_i | "Intrinsic concentration" | Number of free electrons (and equal number of holes) per cm³ in intrinsic material; about 10¹⁰ in silicon at 300 K |
| Semiconductor | "Half a conductor" | A material with a gap small enough (roughly 0.5 to 3.5 eV) that its conductivity can be set over many orders of magnitude |

## Further Reading

- *All About Circuits*, Volume III (Semiconductors), chapter "Solid-state device theory": a free, gentle tour of bands and quantum basics. https://www.allaboutcircuits.com/textbook/semiconductors/chpt-2/introduction-to-solid-state-device-theory/
- *The Feynman Lectures on Physics*, Volume III, chapter 14 "Semiconductors": Feynman's own intuitive treatment of electrons and holes in crystals. https://www.feynmanlectures.caltech.edu/III_14.html
- HyperPhysics (Georgia State University), "Band theory of solids": short pages with diagrams and the numbers used here. http://hyperphysics.phy-astr.gsu.edu/hbase/Solids/band.html
- B. Van Zeghbroeck, *Principles of Semiconductor Devices* (free online textbook, University of Colorado): the source of standard values for Nc, Nv and mobilities. https://web.archive.org/web/2021/https://ecee.colorado.edu/~bart/book/book/contents.htm (archived copy)
