# How Batteries Work

> A battery is a chemical reaction that has been split in two and forced to pay its electrons through your circuit.

**Type:** Learn
**Prerequisites:** Phase 01 (The Physics Underneath), Phase 06 Lesson 01 (Ideal and Real Sources), Phase 06 Lesson 02 (Internal Resistance)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Cell | One single chemical unit that makes a voltage | One egg in an egg carton |
| Battery | Strictly, several cells joined together; in everyday speech, also one cell | The whole carton |
| Electrode | A piece of material where the chemical reaction happens and electrons enter or leave | A dock where boats load and unload |
| Anode | The electrode that gives electrons away to the outside circuit while the battery discharges (the negative terminal) | The dock where boats leave full |
| Cathode | The electrode that takes electrons in from the outside circuit while the battery discharges (the positive terminal) | The dock where boats arrive |
| Electrolyte | The liquid, gel or paste between the electrodes that lets ions move but not electrons | A turnstile that lets people through but not cars |
| Ion | An atom (or group of atoms) with missing or extra electrons, so it carries charge | A person carrying a token |
| Separator | A porous sheet that keeps the electrodes from touching | A fence with holes small enough only for ions |
| Oxidation | A material losing electrons | Spending money |
| Reduction | A material gaining electrons | Receiving money |
| Redox reaction | A reaction where one material is oxidized and another is reduced at the same time | A payment: someone pays, someone gets paid |
| Capacity | How much charge a battery can deliver before it is empty, in ampere-hours (Ah) or milliampere-hours (mAh) | The size of the fuel tank |
| Energy | Capacity times voltage, in watt-hours (Wh) | How far the tank can take you |
| Cutoff voltage | The voltage below which a device (or a battery's protection) stops using the battery | The fuel gauge's "empty" mark |
| Primary / secondary cell | Use-once battery / rechargeable battery | Disposable camera / phone camera |
| C-rate | Current expressed as a fraction of capacity per hour: 1C empties the battery in 1 hour | Driving speed relative to tank size |

## Learning Objectives

- Explain how a chemical reaction can be split so its electrons are forced through an external wire.
- Compute the voltage of a simple cell from two standard electrode potentials.
- Compute the theoretical capacity of an electrode material from its molar mass and the number of electrons per atom.
- Convert between mAh, Wh and runtime, and explain why capacity shrinks at high current.
- Simulate a discharge curve with our simulator and compare alkaline and lithium-ion cells.

## The Problem

A shop sells an AA alkaline cell for a coin and claims it has "2800 mAh". A drone battery the size of a matchbox claims "850 mAh, 7.4 V, 30C". A car battery says "60 Ah, 12 V". What do these numbers mean? Which of them can light an LED for a week, and which can spin four propellers for five minutes?

To answer, you need to know what is going on inside: where the voltage comes from, where the charge comes from, and why the two run out differently depending on how hard you pull. You also need it to make good decisions: which battery to choose, how long a gadget will last, and why "fully charged" lithium cells must never be shorted.

## The Physics

### Some materials want electrons more than others

Atoms of different elements hold on to their outer electrons with different strength (Phase 01). Zinc holds its two outer electrons loosely. Copper ions hold electrons more tightly than zinc does. Drop a strip of zinc into a solution of copper sulfate (which contains copper ions, Cu2+) and something visible happens: the zinc slowly dissolves and a reddish coat of copper metal grows on it. Each zinc atom hands two electrons to a copper ion:

    Zn  +  Cu2+   ->   Zn2+  +  Cu

Zinc is **oxidized** (it loses electrons). Copper is **reduced** (it gains electrons). Energy is released, but here it is just a little heat in the beaker, because the electrons jump directly from zinc to copper, a fraction of a nanometre away. Nobody can use that energy.

### The trick: split the reaction in two

Now put the zinc in one cup (with zinc sulfate) and a copper strip in another cup (with copper sulfate). Connect the two strips with a wire, and connect the two liquids with a salt bridge (a tube of salty gel that lets ions pass).

```
        e-  ->  ->  ->  wire  ->  ->  e-
     +-----------------[ lamp ]---------------+
     |                                         |
   [Zn]  anode (-)                      (+) cathode  [Cu]
     |   Zn -> Zn2+ + 2e-     Cu2+ + 2e- -> Cu   |
   ~~~~~~~~~~~~~                 ~~~~~~~~~~~~~
   zinc sulfate  <== salt bridge ==>  copper sulfate
                  (ions flow here)
```

The zinc still wants to give its electrons to copper ions. But the only path for electrons is the wire. So electrons leave the zinc, travel through the wire (and through your lamp), and arrive at the copper strip, where copper ions in the liquid pick them up and become copper metal. Inside the liquids, ions drift to keep both cups electrically balanced. The circuit is closed: electrons outside, ions inside.

This is a **cell**: the same redox reaction, split in two, with its electrons forced to take the long way through your circuit. The energy the reaction releases now goes into your lamp instead of into the beaker. This exact arrangement is the Daniell cell, invented in 1836, and it gives about 1.1 V.

### Why the voltage is fixed by the chemistry

How strongly the electrons are pushed depends only on *which* two materials you paired, not on how big the strips are. Chemists measure, for each half-reaction, a number called the **standard electrode potential**, in volts, relative to a reference made of hydrogen. A more negative number means "gives electrons away more eagerly".

| Half-reaction | Standard potential |
|---|---|
| Li+ + e- -> Li | -3.04 V |
| Zn2+ + 2e- -> Zn | -0.76 V |
| Fe2+ + 2e- -> Fe | -0.44 V |
| 2H+ + 2e- -> H2 | 0.00 V (the reference) |
| Cu2+ + 2e- -> Cu | +0.34 V |
| Ag+ + e- -> Ag | +0.80 V |

The cell voltage (at standard conditions, with no current) is the potential of the electrode that receives electrons minus the potential of the one that gives them:

    E_cell = E_cathode - E_anode

Read it: "the cell voltage is how much more the cathode wants electrons than the anode does." For copper and zinc: 0.34 - (-0.76) = 1.10 V.

Lithium sits at the very top of the list (it gives electrons away more eagerly than anything else). That is why lithium cells reach 3 to 4 V per cell while zinc-based cells sit around 1.5 V.

### Where the capacity comes from

Each zinc atom that reacts sends exactly 2 electrons through your circuit. So the total charge a battery can deliver is fixed by how many zinc atoms it contains (and enough of the partner material). Count atoms with chemistry's counting unit, the mole: one mole is 6.022 * 10^23 atoms. One mole of electrons carries a charge called the **Faraday constant**:

    F = 96 485 coulombs per mole of electrons

A mole of zinc weighs 65.38 g. One gram of zinc is 1 / 65.38 = 0.0153 mol of atoms, giving 2 * 0.0153 = 0.0306 mol of electrons, which is 0.0306 * 96 485 = 2952 C.

One ampere-hour is one ampere for one hour: 1 A * 3600 s = 3600 C. So one gram of zinc can give 2952 / 3600 = 0.82 Ah. In formula form:

    capacity per gram (Ah/g) = electrons per atom * F / (molar mass * 3600)

Lithium is far lighter (6.94 g/mol) and gives 1 electron: 1 * 96 485 / (6.94 * 3600) = 3.86 Ah per gram. Light and high-voltage: that is the whole reason phones and electric cars use lithium.

### Why voltage falls as the battery empties

As the reaction runs, the materials near the electrodes change: reactants get used up, products pile up, the electrolyte changes concentration. The pushing strength (the EMF) depends a little on those concentrations, so it drifts down. At the same time, the clogged electrodes raise the internal resistance (Lesson 02). Both effects make the terminal voltage fall over the battery's life. How it falls depends on the chemistry:

- **Alkaline (zinc / manganese dioxide):** starts around 1.55 to 1.6 V and slopes down steadily.
- **Lithium-ion:** starts at 4.2 V when full, drops quickly to a long, fairly flat plateau around 3.6 to 3.8 V, then falls off a cliff near empty.
- **NiMH:** a very flat plateau around 1.2 V.
- **Lead-acid (car battery):** about 2.1 V per cell, six cells for 12.6 V.

### Rechargeable cells run the reaction backwards

In a **secondary** (rechargeable) cell the reaction can be reversed: a charger pushes electrons the other way, rebuilding the original materials. In a lithium-ion cell, lithium ions shuttle back and forth between a graphite anode and a metal-oxide cathode, slipping in between the layers of each material, like books slid into a shelf. In a **primary** cell (alkaline, most coin cells) the reaction cannot be cleanly reversed; trying to charge it can make gas and leak.

## The Concept

### Capacity, energy and runtime

**Capacity** (Ah or mAh) is the charge. Read "2400 mAh" as: "this battery can supply 2400 mA for one hour, or 24 mA for 100 hours, or anything with the same product." Runtime is:

    runtime (hours) = capacity (mAh) / current (mA)

Worked examples with a 2400 mAh AA:

| Device | Current | Runtime |
|---|---|---|
| Wall clock | 0.1 mA | 2400 / 0.1 = 24 000 h (almost 3 years) |
| TV remote (when in use) | 20 mA | 120 h |
| Toy car | 500 mA | 4.8 h, and in practice less (see below) |

**Energy** (Wh) combines capacity with voltage, because each coulomb carries "voltage" joules:

    energy (Wh) = capacity (Ah) * average voltage (V)

A 2.4 Ah alkaline cell averaging 1.25 V holds about 3.0 Wh. A 3.0 Ah lithium-ion 18650 cell averaging 3.6 V holds about 10.8 Wh, more than three AAs in the same size. Comparing batteries by mAh only makes sense when their voltages match.

### The C-rate

Battery people express current relative to capacity. **1C** is the current that would empty the battery in one hour: for a 3000 mAh cell, 1C = 3 A, 2C = 6 A, 0.2C = 600 mA. A drone pack marked "30C" for 850 mAh can deliver 30 * 0.85 = 25.5 A. A C-rate tells you how hard you are working a cell regardless of its size.

### Why capacity shrinks under heavy load

The label capacity is measured at a gentle current. Pull harder and three things happen:

1. **Internal drop.** The I * r drop grows, so the terminal voltage reaches the device's cutoff earlier, while there is still unused chemistry inside.
2. **Slow chemistry.** The reaction at the electrode surface can't keep up; the material near the surface is used up before fresh material can diffuse in. Rest the battery and some voltage "recovers".
3. **Heat.** Losses heat the cell, which wastes energy.

Alkaline cells suffer badly from this. Lithium-ion and NiMH much less. For lead-acid batteries this effect has a classic empirical rule called Peukert's law, but we will simulate it directly instead.

### A discharge simulation

To see a discharge curve we need a model that changes as the battery empties. Let "used" be the fraction of the capacity already spent, from 0 (full) to 1 (empty). We give a table of EMF and internal resistance at a few points of "used" (shaped like real datasheet curves, but simplified) and interpolate between them. Then, minute by minute:

1. Look up EMF and r for the current "used" fraction.
2. Ask the simulator for the terminal voltage and current with the load attached.
3. Stop if the voltage is under the cutoff.
4. Add the charge spent this minute: current * 60 s, divided by the total capacity in coulombs.

This is a small time-stepping loop. In Phase 07 Lesson 08 you will meet the same idea for capacitors.

## Build It

### Step 1: Cell voltage from the table

```python
def cell_voltage(cathode, anode):
    return REDUCTION_POTENTIALS[cathode] - REDUCTION_POTENTIALS[anode]
```

Output:

```
   Cu2+ / Cu (+)  against  Zn2+ / Zn   (-): +0.34 - (-0.76) = 1.10 V
    Ag+ / Ag (+)  against  Zn2+ / Zn   (-): +0.80 - (-0.76) = 1.56 V
   Cu2+ / Cu (+)  against  Fe2+ / Fe   (-): +0.34 - (-0.44) = 0.78 V
   Cu2+ / Cu (+)  against  Li+ / Li    (-): +0.34 - (-3.04) = 3.38 V
```

Real commercial cells use other partners and other conditions (alkaline gel, non-water electrolytes), so their voltages differ from these textbook pairs, but the principle is the same. Silver-zinc pairs really are used: silver-oxide watch cells give about 1.55 V.

### Step 2: Charge per gram

```python
def amp_hours_per_gram(molar_mass_grams, electrons_per_atom):
    coulombs_per_gram = electrons_per_atom * FARADAY / molar_mass_grams
    return coulombs_per_gram / 3600.0
```

Zinc gives 0.820 Ah/g, lithium 3.862 Ah/g, lead 0.259 Ah/g. Lead's poor number is why car batteries are so heavy.

### Step 3: Runtime

Simple division, printed for a clock, a remote, a toy car and a phone. Remember that the toy-car figure is optimistic for alkaline cells.

### Step 4: Discharge into 10 ohm

```python
def discharge(chemistry, load_ohms, step_seconds=60.0):
    used_fraction = 0.0
    seconds = 0.0
    times, volts = [], []
    while used_fraction < 1.0:
        emf = np.interp(used_fraction, chemistry["used"], chemistry["emf"])
        internal = np.interp(used_fraction, chemistry["used"], chemistry["r"])
        v, i = terminal_voltage(float(emf), float(internal), load_ohms)
        if v < chemistry["cutoff"]:
            break
        times.append(seconds / 3600.0)
        volts.append(v)
        used_fraction += i * step_seconds / (chemistry["capacity_ah"] * 3600.0)
        seconds += step_seconds
    return np.array(times), np.array(volts)
```

`terminal_voltage` builds the usual source-plus-r-plus-load circuit in our simulator. Output:

```
  alkaline AA  : starts at 1.557 V, reaches the 1.0 V cutoff after 17.4 h, delivered 2.77 Wh
  Li-ion 18650 : starts at 4.183 V, reaches the 3.0 V cutoff after 7.9 h, delivered 10.90 Wh
```

The plot `out.png` shows the alkaline cell sloping down all the way and the lithium cell sitting on its plateau. The lithium cell runs a shorter time into the same 10 ohm because its higher voltage pushes almost three times more current, but it delivers almost four times the energy.

### Step 5: Light versus heavy load

```
    10 ohm load: runs 17.43 h and delivers 2.18 Ah before 1.0 V
     2 ohm load: runs  2.92 h and delivers 1.75 Ah before 1.0 V
     1 ohm load: runs  1.11 h and delivers 1.28 Ah before 1.0 V
```

Same model, same cell. At 1 ohm (about 1.2 A) only about half of the label capacity comes out before the terminals fall below 1.0 V. The rest is stranded inside, behind the internal resistance. That is the toy-car disappointment, explained by the model from Lesson 02.

Run it:

```bash
uv run python phases/06-sources-batteries-and-measurement/03-how-batteries-work/code/main.py
```

## Use It

| Chemistry | Nominal cell voltage | Typical energy per mass | Rechargeable | Where you find it |
|---|---|---|---|---|
| Alkaline (Zn / MnO2) | 1.5 V | about 100 Wh/kg | No | Remotes, clocks, toys |
| Lithium primary (Li / MnO2), e.g. CR2032 | 3.0 V | about 250 Wh/kg | No | Watches, motherboards, sensors |
| NiMH | 1.2 V | about 60 to 100 Wh/kg | Yes | AA rechargeables, older hybrids |
| Lead-acid | 2.0 V (12 V with 6 cells) | about 30 to 40 Wh/kg | Yes | Cars, backup power |
| Lithium-ion (graphite / metal oxide) | 3.6 to 3.7 V | about 150 to 270 Wh/kg | Yes | Phones, laptops, cars |
| Lithium iron phosphate (LFP) | 3.2 V | about 90 to 160 Wh/kg | Yes | Solar storage, buses, some cars |

These are rough typical ranges; datasheets give exact numbers for each product.

- **Reading a datasheet.** Look for capacity *at a stated current* (for example "2850 mAh at 25 mA to 0.8 V"), a set of discharge curves at several loads, internal resistance, and the operating temperature range.
- **Protection.** Lithium-ion packs include a small protection circuit that disconnects the cell below about 2.5 to 3.0 V and above 4.2 to 4.25 V, and on short circuit. Going outside that window damages the cell or starts a fire.
- **Airline rules.** Spare lithium batteries go in carry-on luggage and are limited by watt-hours (commonly 100 Wh without approval), which is why power banks print their Wh rating.

## Common Mistakes

- **Comparing mAh across voltages.** A 10 000 mAh power bank is rated at its internal 3.7 V cell; at its 5 V USB output it delivers fewer mAh. Compare Wh.
- **Believing the label capacity at any current.** Label capacity is measured gently. Heavy loads get less, sometimes much less.
- **Thinking the battery "stores electrons".** A charged battery has the same number of electrons as an empty one. It stores chemical energy in its materials; electrons are just the currency of the reaction.
- **Mixing up anode and cathode.** During discharge the anode is the negative terminal. During charging of a rechargeable cell the reactions reverse, which is why people prefer to say "negative electrode" and "positive electrode".
- **Charging primary cells.** Alkaline and lithium coin cells are not designed for it and can leak or burst.
- **Storing lithium-ion full and hot.** High charge plus heat ages lithium cells fastest. Store around half charge, cool.

## Exercises

1. Using the table, what voltage would a silver/copper cell give? Which metal is the anode?
2. Aluminium has a molar mass of 26.98 g/mol and gives 3 electrons per atom. What is its theoretical capacity in Ah per gram? Compare it with lithium.
3. A wireless sensor draws 15 microamps when sleeping and 12 mA for 50 ms every 10 s. What is its average current? How long would a 220 mAh CR2032 last (ignoring self-discharge)?
4. A power bank says "10 000 mAh, 3.7 V". How many Wh is that? At 85 % conversion efficiency, how many mAh can it deliver at 5 V?
5. In the script, make the alkaline internal resistance table twice as large and rerun Step 5. How much charge does the 1 ohm load get now? Explain the change in one sentence.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Battery | "Any cell" | Strictly, two or more cells connected; commonly used for one cell too |
| Anode | "The plus end" (wrong) | The electrode that is oxidized and sends electrons out during discharge: the negative terminal |
| Cathode | "The minus end" (wrong) | The electrode that is reduced and receives electrons during discharge: the positive terminal |
| Electrolyte | "The battery acid" | The ion-conducting, electron-blocking material between the electrodes |
| Capacity | "How big the battery is" | Total charge deliverable to a cutoff voltage at a stated current, in Ah |
| Energy | "Same as capacity" | Capacity times voltage, in Wh; the fair way to compare chemistries |
| C-rate | "How fast it charges" | Current divided by capacity per hour; 1C empties the cell in one hour |
| Standard electrode potential | "The voltage of a metal" | Tendency of a half-reaction to gain electrons, versus hydrogen, at standard conditions |

## Further Reading

- Battery University (Cadex), the "BU-1xx" and "BU-2xx" articles on chemistries and discharge: https://batteryuniversity.com/
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., the battery chapter with chemistry comparisons and discharge curves.
- OpenStax *Chemistry 2e*, chapter 17 "Electrochemistry" (galvanic cells, standard potentials, batteries), free: https://openstax.org/details/books/chemistry-2e
- Energizer E91 alkaline and CR2032 lithium datasheets, for real capacity-versus-load curves: https://data.energizer.com/pdfs/e91.pdf and https://data.energizer.com/pdfs/cr2032.pdf
