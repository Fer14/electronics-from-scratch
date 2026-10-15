# Doping: n-type and p-type

> Add one phosphorus atom per million silicon atoms and you get a million times more free electrons. Add boron instead and you get a million empty seats that drift around like positive charges.

**Type:** Learn
**Prerequisites:** 11-01 (Why Silicon); Phase 03 (Resistance and Ohm's Law), lesson 02-resistivity-and-wires
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Doping | Adding a tiny, controlled amount of another element to a pure semiconductor | A pinch of salt in a big pot of soup: tiny amount, big change in taste |
| Dopant | The foreign atom that is added | The salt itself |
| Donor | A dopant atom with one more outer electron than silicon (phosphorus, arsenic); it gives that electron away | A guest who brings a spare chair to a full party: one extra person ends up standing and wandering |
| Acceptor | A dopant atom with one fewer outer electron than silicon (boron); it grabs an electron from a neighbour | A guest who arrives without a chair and takes one from the next table, leaving that table with an empty seat |
| Hole | A missing electron in the valence band; it moves when neighbouring electrons hop into it and behaves like a positive charge | The empty seat in a full cinema row: people shift one seat over and the empty seat walks the other way |
| n-type | Silicon doped with donors: most carriers are electrons (Negative) | A street full of wandering pedestrians |
| p-type | Silicon doped with acceptors: most carriers are holes (Positive) | A car park almost full, with a few empty spaces that "move" as cars shuffle |
| Majority carrier | The carrier type there is lots of (electrons in n-type, holes in p-type) | The home team crowd in a stadium |
| Minority carrier | The other type, of which there are very few | The handful of away fans |
| Concentration | How many of something per unit volume (here, per cubic centimetre) | People per square metre in a crowd |
| Mobility | How easily a carrier drifts when pushed by an electric field | How fast you can walk through a crowd: easy in a thin crowd, slow in a dense one |
| Compensation | Having both donors and acceptors; they cancel each other partly | Mixing sugar and lemon: the taste depends on which one wins and by how much |
| Ionized | An atom that has lost or gained an electron and so carries a net charge | A person who gave away a coin is now "one coin short" |

## Learning Objectives

- Explain what a donor and an acceptor do, using the bond picture and the band picture.
- Describe a hole as a moving vacancy and explain why it behaves like a positive carrier.
- Use the mass-action law (n × p = n_i²) to find the minority carrier concentration.
- Compute the resistivity of doped silicon from the doping level.
- Explain why doped silicon is stable with temperature while pure silicon is not.

## The Problem

Lesson 01 ended with bad news. Pure silicon is a poor conductor whose conductivity doubles every 10 °C or so. You cannot build a predictable circuit on a material that changes its mind every time the sun comes through the window.

Engineers needed two things: a way to set silicon's conductivity to *whatever value they want*, and a way to make it insensitive to temperature. And for diodes and transistors they need something stranger still: two *different kinds* of silicon, one where current is carried by negative charges and one where it seems to be carried by positive charges, sitting side by side in the same crystal.

All three are achieved by the same trick: sprinkle in a very small number of foreign atoms. This lesson shows why that works, introduces the "hole" (the single most important idea in semiconductor electronics), and gives you the numbers.

## The Physics

### Silicon's bonds, revisited

Each silicon atom has 4 outer (valence) electrons and shares them with 4 neighbours, forming 4 covalent bonds. In the flat drawings below, each `=` is a bond holding a pair of electrons.

```
    Si = Si = Si = Si
    ||   ||   ||   ||
    Si = Si = Si = Si
    ||   ||   ||   ||
    Si = Si = Si = Si
```

Every bond complete means the valence band is full. As we saw, that carries no current.

### Donors: atoms with one electron too many

Phosphorus (P) sits one column to the right of silicon in the periodic table: it has **5** outer electrons. If a phosphorus atom takes the place of a silicon atom in the crystal, 4 of its electrons form the 4 bonds. The **fifth** has no bond to join.

```
    Si = Si = Si = Si
    ||   ||   ||   ||
    Si =  P = Si = Si        P has 5 outer electrons: 4 in bonds,
    ||   ||   ||   ||        1 left over  ->  e-  (loosely held)
    Si = Si = Si = Si
```

That spare electron is held very weakly, by about 0.045 eV. Compare with kT ≈ 0.026 eV at room temperature: the thermal shoves easily knock it loose. At room temperature essentially **every** phosphorus atom has released its extra electron into the conduction band. The phosphorus atom is left with one more proton than electrons: a fixed **positive ion** stuck in the crystal. It cannot move; only the released electron moves.

Because phosphorus *donates* an electron, it is called a **donor**. Silicon doped with donors has many free electrons (negative carriers), so it is called **n-type**.

In the band picture, the donor adds a few new shelves just below the conduction band, each holding one electron. The step from those shelves up into the conduction band is tiny, so they empty at once.

```
   conduction band   ==========================   <- donated electrons land here
                      - - - - - - - - - - - - -   <- donor shelves, 0.045 eV below
                              gap 1.12 eV
   valence band      ##########################
```

### Acceptors: atoms with one electron too few

Boron (B) sits one column to the *left* of silicon: **3** outer electrons. In the crystal it forms 3 complete bonds and one bond that is missing an electron.

```
    Si = Si = Si = Si
    ||   ||   ||   ||
    Si =  B - Si = Si        one bond has only one electron:  "-"
    ||   ||   ||   ||        an empty place an electron could fill
    Si = Si = Si = Si
```

An electron from a neighbouring silicon-silicon bond can hop into that gap with very little energy (again about 0.045 eV). When it does, the boron atom becomes a fixed **negative ion** (it gained an electron), and the neighbouring bond is now the one with a missing electron. Boron *accepts* an electron, so it is an **acceptor**. Silicon doped with acceptors is **p-type**.

### The hole: a moving vacancy

Now the key idea. After that hop, there is a bond somewhere in the crystal with one electron missing. Call that missing electron a **hole**. What happens when you apply a voltage?

Picture a cinema row with exactly one empty seat. Everyone is told "shift one seat toward the left exit if the seat to your left is free". The person right of the empty seat moves into it. Now the empty seat is one place to the right. The next person moves in, and so on. Each person moved only one seat to the left, but **the empty seat travelled all the way to the right**.

The script prints exactly this:

```
step 0:  [ee_eeeee]   empty seat at position 2
step 1:  [eee_eeee]   empty seat at position 3
step 2:  [eeee_eee]   empty seat at position 4
...
step 5:  [eeeeeee_]   empty seat at position 7
```

The electrons (negative) moved left, which is exactly what a positive charge moving right would look like from outside. So instead of tracking billions of valence electrons each shuffling one place, we track **one** imaginary particle, the hole, that:

- carries a charge of **+q** (plus 1.602 × 10⁻¹⁹ coulombs),
- moves in the direction of the electric field (the way positive charges are pushed),
- moves somewhat more slowly than a free electron (each hop requires an electron to jump between bonds), roughly 3 times slower in silicon.

What the analogy gets wrong: in the cinema, the empty seat moves only because people move, and you could still say "it's really the people moving". In a crystal, this is also true, but the hole picture is not just a bookkeeping trick: measurements such as the Hall effect (which reveals the sign of the carriers) really show positive carriers in p-type material. The hole is as real a particle as the physics needs it to be.

In the band picture: a hole is an empty slot in the nearly full valence band. Because the band is no longer completely full, it can carry current (recall from lesson 01 that only partly filled bands conduct).

### Majority and minority carriers

Even in n-type silicon, heat still occasionally breaks a silicon bond and makes an electron-hole pair. So n-type silicon has **lots** of electrons (the majority carriers) and **a few** holes (the minority carriers). P-type is the other way around.

How few? There is a beautiful rule, the **mass-action law**:

```
n × p = n_i²
```

Read: "the number of free electrons times the number of holes, per cubic centimetre, always equals the square of the intrinsic concentration" (at a given temperature, in equilibrium). `n` is the electron concentration, `p` the hole concentration, and `n_i` ≈ 1 × 10¹⁰ per cm³ for silicon at 300 K.

Why? Electrons and holes are constantly created (by heat) and destroyed (when a free electron falls into a hole, called *recombination*). The creation rate depends only on temperature. The destruction rate is proportional to how often an electron meets a hole, n × p. In balance, n × p is fixed, and in pure silicon (n = p = n_i) it equals n_i². Adding more electrons does not change the creation rate but makes holes get "eaten" faster, so the hole count falls.

What the analogy gets wrong: think of a dance hall where couples form when a free dancer meets a partner. Bring in many extra men and women without partners get snapped up quickly, so there are fewer single women. The analogy is fine as far as it goes, but in silicon "creation" and "destruction" are quantum processes with energy exchange, not choices.

## The Concept

### How many carriers? Worked example

Dope silicon with **N_D = 1 × 10¹⁶ donors per cm³**. Silicon has 5 × 10²² atoms per cm³, so that is 1 phosphorus atom per 5 million silicon atoms. Purity at the level of a few grains of salt in a bathtub.

1. Every donor releases its electron, so n ≈ N_D = **1 × 10¹⁶ per cm³**. (The thermal electrons, ~10¹⁰, are negligible.)
2. Mass-action law: p = n_i² / n = (10¹⁰)² / 10¹⁶ = 10²⁰ / 10¹⁶ = **1 × 10⁴ per cm³**.

So in this piece there are 10¹² times more electrons than holes. Compared to pure silicon, electrons went up a million times and holes went **down** a million times.

The general formula, used in the code, also works when the doping is comparable to n_i:

```
n = (N_D - N_A)/2 + sqrt( ((N_D - N_A)/2)² + n_i² ),     p = n_i² / n
```

Read: "electrons equal half the net doping plus the square root of (half the net doping, squared, plus n_i squared)". It comes from combining n × p = n_i² with **charge neutrality** (the total charge in the piece must be zero: n + N_A = p + N_D). When N_D is much larger than n_i, the square root is almost exactly N_D/2 and n ≈ N_D.

### Resistivity of doped silicon

From lesson 01: conductivity σ = q (n μn + p μp) and resistivity ρ = 1/σ. In doped silicon one term dominates. For n-type with 1 × 10¹⁶ donors:

```
μn at that doping ≈ 1185 cm²/(V·s)       (dopants slightly slow electrons down)
σ = 1.602e-19 × 1e16 × 1185 = 1.90  siemens per cm
ρ = 1 / 1.90 = 0.527 ohm·cm
```

Compare with pure silicon at 3.3 × 10⁵ Ω·cm (with the measured n_i). Doping one atom in five million lowered the resistivity by a factor of **600,000**.

**Mobility falls with doping.** The ionized dopant atoms are charged bumps that scatter carriers. The code uses a standard empirical formula (fitted to measurements) where electron mobility drops from about 1414 in pure silicon to about 100 at 10¹⁹ per cm³. Holes are always slower: about 470 at low doping.

Results from the script (n-type):

| Donors per cm³ | 1 dopant per … Si atoms | n | p | ρ (Ω·cm) |
|---|---|---|---|---|
| 10¹⁴ | 500 million | 1.0 × 10¹⁴ | 1.0 × 10⁶ | 44.5 |
| 10¹⁵ | 50 million | 1.0 × 10¹⁵ | 1.0 × 10⁵ | 4.58 |
| 10¹⁶ | 5 million | 1.0 × 10¹⁶ | 1.0 × 10⁴ | 0.527 |
| 10¹⁷ | 500,000 | 1.0 × 10¹⁷ | 1.0 × 10³ | 0.087 |
| 10¹⁸ | 50,000 | 1.0 × 10¹⁸ | 100 | 0.023 |

For p-type, the same doping gives a resistivity about 2.5-3 times higher, because holes are slower: 13.5 Ω·cm at 10¹⁵ boron atoms versus 4.58 Ω·cm for phosphorus.

### A worked bar of silicon

A bar of n-type silicon, 10 mm long, 1 mm wide and 0.1 mm thick, doped with 10¹⁵ donors per cm³. Using R = ρ × L / A from Phase 03 (in centimetres: L = 1 cm, A = 0.1 cm × 0.01 cm = 0.001 cm²):

```
R = 4.583 Ω·cm × 1 cm / 0.001 cm² = 4583 Ω
```

That is a perfectly usable resistor, made of silicon. In fact, chips make resistors exactly this way: a strip of doped silicon whose length and doping set the value.

### Compensation

You can put both donors and acceptors in the same region. They cancel: each acceptor captures one donor's electron. What matters is the **net** doping. With 1 × 10¹⁶ donors and 3 × 10¹⁵ acceptors, the net is 7 × 10¹⁵ donors, so n = 7 × 10¹⁵ and p = n_i²/n ≈ 1.4 × 10⁴. The region is n-type, just less strongly.

This is how chips are made: start with a lightly doped p-type wafer and "overdope" small regions with donors to turn them n-type, then overdope smaller regions inside those with acceptors to turn them back p-type. The transistors of Phase 12 are built exactly like this.

### Why doping fixes the temperature problem

In pure silicon, every carrier comes from heat, so carriers grow exponentially with temperature. In doped silicon, the carriers come from dopant atoms, and they are **already all released** at room temperature. Heat cannot release more of them. The script compares:

```
 T (C)    pure n_i     doped n
   -40    1.37e+07   1.000e+16
    25    8.66e+09   1.000e+16
   125    3.19e+12   1.000e+16
   250    2.37e+14   1.001e+16
   350    2.26e+15   1.049e+16
```

The doped piece keeps n = 10¹⁶ until the thermal carriers become comparable to the dopants, around 300-400 °C for this doping. (Real silicon's resistance still rises somewhat with temperature, because hot crystals scatter carriers more and mobility drops; we kept mobility fixed to isolate the effect of carrier number.)

Below about -200 °C the opposite happens: there is not enough heat even to release the dopants' loosely held electrons ("freeze-out"), and conductivity drops again. Ordinary electronics never goes that cold.

### Charge bookkeeping: a doped piece is neutral

A common confusion: "n-type silicon has extra electrons, so it must be negatively charged". No. Each released electron left behind a positive phosphorus ion. The piece as a whole is exactly neutral. N-type means "the **mobile** charges are mostly negative", not "the material is negative". This bookkeeping is what makes the pn junction in the next lesson work: when the mobile carriers leave a region, the fixed ions stay behind and **then** the region is charged.

```
    n-type region:                        p-type region:
    (+) fixed donor ions                  (-) fixed acceptor ions
     e- mobile electrons, same number     h+ mobile holes, same number
     net charge: zero                     net charge: zero
```

## Build It

The script `code/main.py` uses plain Python and NumPy.

### Step 1: The moving vacancy

```python
def hole_walk(seats, steps):
    row = list(seats)
    frames = ["".join(row)]
    for _ in range(steps):
        gap = row.index("_")
        if gap + 1 < len(row):
            row[gap], row[gap + 1] = row[gap + 1], row[gap]
        frames.append("".join(row))
    return frames
```

Each step swaps the empty seat `_` with the electron on its right, which is the same as "the electron moves one seat left". The printout shows the vacancy walking right.

### Step 2: n_i with temperature

We reuse the shape of lesson 01's formula but pin it to the measured value, 1 × 10¹⁰ per cm³ at 300 K:

```python
def intrinsic_density(kelvin):
    shape = (kelvin / 300.0) ** 1.5 * np.exp(-SILICON_GAP_EV / (2 * BOLTZMANN_EV * kelvin))
    shape_at_300 = np.exp(-SILICON_GAP_EV / (2 * BOLTZMANN_EV * 300.0))
    return MEASURED_NI_300 * shape / shape_at_300
```

### Step 3: Carriers from doping

```python
def carrier_densities(donors, acceptors, kelvin=300.0):
    ni = intrinsic_density(kelvin)
    net = donors - acceptors
    if net >= 0:
        electrons = net / 2 + np.sqrt((net / 2) ** 2 + ni**2)
        holes = ni**2 / electrons
    else:
        holes = -net / 2 + np.sqrt((net / 2) ** 2 + ni**2)
        electrons = ni**2 / holes
    return electrons, holes
```

This is the neutrality-plus-mass-action formula. The mass-action check prints `n x p = 1.000e+20` and `n_i^2 = 1.000e+20`.

### Step 4: Mobility and resistivity

```python
def electron_mobility(total_doping):
    return 68.5 + (1414 - 68.5) / (1 + (total_doping / 9.2e16) ** 0.711)
```

The form "minimum + (maximum - minimum) / (1 + (N/N_ref)^α)" is a widely used empirical fit (Caughey-Thomas). Resistivity then follows from σ = q(nμn + pμp).

### Step 5: Run it

```
uv run python phases/11-semiconductors-and-diodes/02-doping-n-and-p/code/main.py
```

Try changing the donor list, or set acceptors and donors together to explore compensation.

## Use It

- **Wafer datasheets** quote resistivity rather than doping. A common wafer spec is "p-type, boron, 1-10 Ω·cm", which by our table means about 1.5 × 10¹⁵ to 1.5 × 10¹⁶ acceptors per cm³.
- **Common dopants.** Donors: phosphorus, arsenic, antimony. Acceptors: boron (almost always). They are introduced by *ion implantation* (firing dopant ions into the wafer with an accelerator and then heating to repair the crystal) or by *diffusion* from a hot gas.
- **Heavily doped contacts.** Where a metal wire touches silicon, the silicon is doped very heavily (10²⁰ per cm³ and above, written n⁺ or p⁺) so the contact behaves like a plain resistor. You will see n⁺ and p⁺ in transistor cross-sections in Phase 12.
- **Hall-effect sensors.** The magnetic field sensors in phones and brushless motors are slabs of lightly doped semiconductor. The sign of the Hall voltage reveals whether the carriers are electrons or holes.
- **On-chip resistors.** A strip of doped silicon or polysilicon, typically with a "sheet resistance" of tens to thousands of ohms per square, set by the doping.

## Common Mistakes

- **"n-type silicon is negatively charged."** It is neutral. The mobile electrons are balanced by fixed positive donor ions.
- **"Holes are protons" or "holes are positrons".** A hole is the absence of an electron in an otherwise full band. It behaves as a +q carrier; there is no new particle flying around.
- **"Adding donors adds holes too."** It removes them. Mass action: more electrons means fewer holes, n × p stays n_i².
- **"More doping = more mobility."** The opposite: dopant ions scatter carriers. More doping gives more carriers but each moves more slowly; the net effect is still lower resistivity.
- **Forgetting that the dopant ion stays put.** Only the electron (or hole) moves. This immobile charge is the key to the depletion region in lesson 03.
- **Thinking you need lots of dopant.** One part in a million is "heavy" doping for many devices. Purity of the starting silicon must be far better than that, or the impurities would dominate.

## Exercises

1. Silicon is doped with 5 × 10¹⁵ boron atoms per cm³. What are p and n at 300 K? Is it n-type or p-type?
2. Using the table, estimate the resistance of a cube of n-type silicon 1 cm on a side with 10¹⁷ donors per cm³.
3. A region has 2 × 10¹⁷ donors and 5 × 10¹⁷ acceptors. What type is it, and what are the majority and minority concentrations?
4. In the script, raise the temperature in `show_temperature_stability` until doped n is 10 % above N_D. Roughly what temperature is that? Repeat with 10¹⁴ donors. Why is lightly doped silicon more sensitive?
5. Extend `hole_walk` so the field can point either way (a `direction` argument). Then add a second empty seat and show that two holes move independently.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Donor | "n-dopant" | Atom with 5 outer electrons (P, As, Sb) that releases one into the conduction band, leaving a fixed + ion |
| Acceptor | "p-dopant" | Atom with 3 outer electrons (B) that captures a valence electron, leaving a hole and a fixed − ion |
| Hole | "a positive charge" | An empty slot in the valence band that moves opposite to electrons and acts as a +q carrier |
| Majority carrier | "the carriers" | The abundant type: electrons in n-type, holes in p-type |
| Minority carrier | "leakage carriers" | The rare type: p = n_i²/N_D in n-type; they become important in diodes and BJTs |
| Mass-action law | "n p = n_i squared" | In equilibrium the product of electron and hole concentrations depends only on material and temperature |
| n⁺ / p⁺ | "heavily doped" | Regions doped around 10¹⁹-10²¹ per cm³, used for contacts and emitters |

## Further Reading

- *All About Circuits*, Volume III, "Solid-state device theory: Electrons and holes" and "Band theory of solids". https://www.allaboutcircuits.com/textbook/semiconductors/chpt-2/electrons-and-holes/
- B. Van Zeghbroeck, *Principles of Semiconductor Devices*, chapter 2 (carrier densities, mobility models). https://web.archive.org/web/2021/https://ecee.colorado.edu/~bart/book/book/contents.htm (archived copy)
- HyperPhysics (Georgia State University), "Intrinsic Semiconductors" and "Doped Semiconductors": short pages with the carrier-density numbers. http://hyperphysics.phy-astr.gsu.edu/hbase/Solids/intrin.html
- D. M. Caughey and R. E. Thomas, "Carrier mobilities in silicon empirically related to doping and field", *Proceedings of the IEEE*, 1967: origin of the mobility formula used here.
