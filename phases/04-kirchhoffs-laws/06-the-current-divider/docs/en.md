# The Current Divider

> When current reaches a fork, it splits in inverse proportion to resistance: the easier path gets the bigger share.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Phase 04 lessons 01-05 (nodes, KCL, KVL, series and parallel resistors, the voltage divider)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Current divider | Two or more resistors in parallel that share an incoming current | A river splitting into several channels around islands |
| Branch | One of the parallel paths the current can take | One of the checkout lines in a supermarket |
| Total current (I) | The current arriving at the fork, before it splits | All the shoppers arriving at the checkouts |
| Branch current (I1, I2, ...) | The part of the total that goes through one branch | The shoppers in one line |
| Common voltage | The single voltage that every parallel branch has across it | Every checkout line starts at the same entrance and ends at the same exit |
| Conductance (G) | 1 divided by resistance; how *easily* current flows. Unit: siemens (S) | The width of a doorway instead of its narrowness |
| Siemens (S) | The unit of conductance. 1 S = 1/Ohm; 1 mS = one thousandth of a siemens | "Doorway width" units |
| Current source | A source that pushes a fixed current, whatever voltage that needs | A conveyor belt that delivers exactly 10 boxes per minute, no matter what |
| Shunt | A low resistance placed in parallel with something to carry most of the current around it | A bypass road around a narrow village street |
| Full scale | The largest value a meter can show (needle at the end of the dial) | The top mark on a measuring jug |

## Learning Objectives

- Derive the two-branch current divider formula I1 = I x R2 / (R1 + R2) from KCL and Ohm's law
- Explain why the smaller resistance carries the larger current, and how extreme branches (a short, an open) behave
- Use conductance G = 1/R to split a current among any number of parallel branches
- Solve a mixed circuit (battery, series resistor, parallel branches) by combining the voltage and current dividers
- Design a shunt resistor that lets a sensitive meter measure a bigger current

## The Problem

In the last lesson, resistors in **series** shared a **voltage**. The mirror-image situation is just as common: resistors in **parallel** sharing a **current**.

Picture a car's dashboard with three lamps wired in parallel to the same supply. Together they draw 1.5 A. You'd like to know how much of that goes through each lamp, to pick the right fuse or wire for each one. Or picture an old needle meter that reads full scale at only 1 mA, and you need it to measure currents of 100 mA. You can't push 100 mA through it; the coil would burn. But if you put a low-value resistor beside it, most of the current takes the easy path and only a safe, known fraction goes through the meter. The meter's reading is then simply multiplied by a fixed factor.

Both need the same answer: **when a current meets parallel paths, how does it split?** By the end of this lesson you will compute it in one line, for two branches or for twenty.

## The Physics

Remember what happens at a node (lesson 02): charge cannot pile up there, so every bit of charge that arrives must leave. If 30 mA arrive at a fork with two exits, the two exits together carry 30 mA. That is Kirchhoff's current law.

But KCL alone does not say *how* the 30 mA splits. That depends on the paths. Here is the key physical fact: **the two ends of every parallel branch are the same two nodes**. So the electrical "push", the voltage, across each branch is the same. Each branch sees the same voltage V, and each branch responds with its own current according to Ohm's law, I = V / R.

A branch with low resistance lets a big current through for that voltage. A branch with high resistance lets a small current through. The current doesn't "choose" the easy path; there is just more of it flowing where the path is easier. And it is not "all through the easy path" either: every path carries some current, unless its resistance is infinite (an open circuit).

The **river picture**: a river meets an island and splits into a wide channel and a narrow channel. More water goes through the wide one, but the narrow one still carries some. Both channels have the same drop in height from where the river splits to where it joins again. What the picture gets wrong: in a river the water level adjusts slowly and can flood; in a circuit the split settles almost instantly and is fixed by the resistances alone.

## The Concept

### The circuit

```
              I (total)
              |
       +------+------+       node A (top)
       |             |
      [R1]          [R2]
       | I1          | I2
       +------+------+       node B (bottom)
              |
              I (total)
```

A total current I arrives at node A, splits into I1 through R1 and I2 through R2, and the two parts join again at node B.

### Step 1: KCL at the top node

Current in equals current out:

```
I = I1 + I2
```

"The total current equals the sum of the branch currents."

### Step 2: both branches share one voltage

Both resistors connect A to B, so both have the same voltage V across them. Ohm's law for each one:

```
I1 = V / R1
I2 = V / R2
```

### Step 3: find that common voltage

The two parallel resistors act like one resistor R1 || R2 (lesson 04):

```
R1 || R2 = R1 x R2 / (R1 + R2)
```

so the common voltage is the total current times that combined resistance:

```
V = I x R1 x R2 / (R1 + R2)
```

### Step 4: put it together

Substitute V into I1 = V / R1. The R1 on top cancels the R1 on the bottom:

```
I1 = I x R1 x R2 / (R1 + R2) / R1

I1 = I x R2 / (R1 + R2)
I2 = I x R1 / (R1 + R2)
```

Read aloud: **"the current through R1 is the total current times the *other* resistor, divided by the sum."** Notice the swap compared with the voltage divider: in the voltage divider, a resistor's share of the *voltage* has *its own* resistance on top; in the current divider, a branch's share of the *current* has the *other* resistance on top. That is the formula's way of saying "the smaller resistor takes the larger current".

### Worked example 1

I = 30 mA, R1 = 100 Ohm, R2 = 200 Ohm.

The long way:

```
R1 || R2 = 100 x 200 / 300 = 66.67 Ohm
V        = 0.030 A x 66.67 Ohm = 2.0 V
I1       = 2.0 V / 100 Ohm = 0.020 A = 20 mA
I2       = 2.0 V / 200 Ohm = 0.010 A = 10 mA
check:     20 + 10 = 30 mA
```

The short way:

```
I1 = 30 mA x 200 / 300 = 20 mA
I2 = 30 mA x 100 / 300 = 10 mA
```

R1 is half of R2, so R1 carries twice the current. In parallel, **current is shared in inverse proportion to resistance**.

### Worked example 2: extreme branches

10 mA arrive at 100 Ohm in parallel with something else. What happens as "something else" changes?

```
other branch     100 Ohm gets     other gets
1 MOhm           9.999 mA         0.001 mA     (almost an open circuit)
1 kOhm           9.091 mA         0.909 mA
100 Ohm          5.000 mA         5.000 mA     (equal resistors, equal split)
1 Ohm            0.099 mA         9.901 mA
0.01 Ohm         0.001 mA         9.999 mA     (almost a short circuit)
```

Two limits worth remembering (Phase 02, lesson 03):

- An **open** branch (infinite resistance) carries nothing; the other branch takes everything.
- A **short** branch (zero resistance) takes everything; the other branch carries nothing, because the voltage across both is zero. This is why shorting out a component "kills" it: it doesn't burn, it just stops getting any current.

### The conductance view

Resistance says how hard it is to push current. Its upside-down twin, **conductance**, says how easy it is:

```
G = 1 / R
```

"Conductance is one over resistance." Its unit is the siemens (S). A 100 Ohm resistor has G = 1/100 = 0.01 S = 10 mS. A 1 kOhm resistor has G = 1 mS.

Ohm's law in conductance form is I = G x V ("current is conductance times voltage"). In parallel all branches share V, so each branch current is just its conductance times the same V. That means:

```
I_k = I x G_k / (G1 + G2 + ... + Gn)
```

"Each branch gets a share of the total equal to its conductance divided by the sum of all conductances." This works for any number of branches, and it looks exactly like the voltage divider, with G in place of R. Conductances in parallel simply add, the way resistances in series add.

### Worked example 3: four branches

50 mA into 100, 220, 470 and 1000 Ohm in parallel.

```
G:     10.000 mS   4.545 mS   2.128 mS   1.000 mS     sum = 17.673 mS
share: 10/17.673   4.545/17.673   ...
     = 56.6 %      25.7 %     12.0 %     5.7 %
I:     28.29 mA    12.86 mA   6.02 mA    2.83 mA      sum = 50 mA
V = I_k x R_k = 2.829 V for every branch
```

The common voltage check (every branch has 2.829 V across it) is the best way to catch an arithmetic slip.

### Worked example 4: a battery, a series resistor, two branches

Most real circuits mix series and parallel. Here a 9 V battery feeds a 220 Ohm resistor and then a 330 Ohm || 680 Ohm pair:

```
  +9V ---[220]---+--------+
                 |        |
               [330]    [680]
                 |        |
  0V ------------+--------+
```

Work from the outside in:

```
330 || 680       = 330 x 680 / 1010 = 222.18 Ohm
total resistance = 220 + 222.18     = 442.18 Ohm
I_total          = 9 V / 442.18 Ohm = 20.35 mA
I_330 = 20.35 mA x 680 / 1010 = 13.70 mA
I_680 = 20.35 mA x 330 / 1010 = 6.65 mA
```

KVL check around the loop through the 330 Ohm branch: 20.35 mA x 220 Ohm = 4.478 V on the series resistor, plus 13.70 mA x 330 Ohm = 4.522 V on the branch, adds up to 9.000 V. Both dividers, voltage and current, used together.

### The shunt: a current divider on purpose

A needle meter movement is a coil with some resistance (say 50 Ohm) that shows full scale at 1 mA. To read 10 mA at full scale, put a **shunt** resistor Rs in parallel so that, at 10 mA total, exactly 1 mA goes through the meter and 9 mA through the shunt. Same voltage across both:

```
1 mA x 50 Ohm = 9 mA x Rs     ->  Rs = 50 / 9 = 5.556 Ohm
```

In general: Rs = R_meter x I_meter / (I_wanted - I_meter). For 100 mA full scale, Rs = 50 x 1 / 99 = 0.505 Ohm; for 1 A, about 0.050 Ohm. The bigger the range, the smaller the shunt. Multimeters (Phase 06) measure current exactly this way: a tiny, precise shunt resistor, and a circuit that measures the small voltage across it.

### Voltage divider and current divider side by side

The two dividers are mirror images. Keep this table in your head:

```
                     voltage divider             current divider
connection           series                      parallel
what is shared       one current                 one voltage
what is split        the voltage                 the current
share of R1          Vin x R1 / (R1 + R2)        I x R2 / (R1 + R2)
bigger resistor gets the bigger share            the smaller share
natural unit         resistance R (adds)         conductance G (adds)
```

### Battery or current source?

In the formulas above, the total current I was given. That is exactly what an ideal **current source** does: it delivers a fixed current no matter what you connect. With a battery, the total current is not fixed. It depends on everything in the circuit.

Try it with a 6 V battery and a single 300 Ohm resistor: I = 6/300 = 20 mA. Now add a second 300 Ohm resistor in parallel. The combination is 150 Ohm, so the battery now delivers 6/150 = 40 mA, and each resistor still gets 20 mA. Adding a branch to a battery doesn't steal current from the first branch; it makes the battery work harder. (A real battery has some internal resistance, so it sags a little; Phase 06 deals with that.)

Now do the same with a 20 mA current source. One 300 Ohm resistor: all 20 mA through it, V = 6 V. Add a second 300 Ohm in parallel: the source still delivers 20 mA, now split 10 + 10, and the voltage falls to 3 V. Here adding a branch *does* steal current from the first.

So the current divider formula is always right about the **ratio** of the split, but the **total** it splits depends on what drives the parallel group. Find the total first, then split it.

## Build It

Run the script:

```
uv run python phases/04-kirchhoffs-laws/06-the-current-divider/code/main.py
```

### Step 1: The long way

```python
def split_by_voltage(total_current, r_one, r_two):
    r_parallel = r_one * r_two / (r_one + r_two)
    voltage = total_current * r_parallel
    return voltage, voltage / r_one, voltage / r_two
```

Combine, find the common voltage, apply Ohm's law to each branch. For 30 mA into 100 Ohm || 200 Ohm the script prints V = 2.000 V, I1 = 20 mA, I2 = 10 mA and the KCL check 20 + 10 = 30 mA.

### Step 2: The formula

```python
def two_branch_split(total_current, r_one, r_two):
    i_one = total_current * r_two / (r_one + r_two)
    i_two = total_current * r_one / (r_one + r_two)
    return i_one, i_two
```

Same answers in one line each, with the "other resistor on top" swap clearly visible.

### Step 3: Conductances for many branches

```python
def split_by_conductance(total_current, resistances):
    conductances = 1.0 / np.asarray(resistances, dtype=float)
    shares = conductances / conductances.sum()
    return conductances, shares, total_current * shares
```

NumPy turns the list of resistances into an array, takes 1/R of every element at once, and normalizes so the shares add to 1. The script prints the four-branch table above and confirms that every branch has the same 2.829 V across it.

### Step 4: Mixed series and parallel

The battery + 220 Ohm + (330 || 680) example: combine the parallel pair, find the total current with Ohm's law, split it with `two_branch_split`, and check KVL.

### Step 5: Extreme branches

The script splits 10 mA between 100 Ohm and a second branch that goes from 1 MOhm (nearly open) to 0.01 Ohm (nearly short), printing the table from worked example 2.

### Step 6: Shunts

```python
def shunt_for_meter(meter_resistance, meter_full_scale, wanted_full_scale):
    return meter_resistance * meter_full_scale / (wanted_full_scale - meter_full_scale)
```

For a 50 Ohm, 1 mA meter it computes the shunts for 10 mA, 100 mA and 1 A full scale, then runs the current divider to confirm the meter gets exactly 1.000 mA each time.

## Use It

- **Current-sense resistors:** power supplies, battery chargers and motor drivers measure current with a small resistor (often 0.01 to 0.1 Ohm, e.g. the 2512-size "current sense" parts sold by Vishay, Yageo and others) in the current path. Sometimes it is in series and sometimes it is a shunt in parallel with a measuring circuit; either way the current divider tells you what fraction each path gets.
- **Analog ammeters:** classic panel meters (for example "0-1 mA" moving-coil meters) are sold with separate shunts stamped "100 mA" or "10 A": exactly the calculation of Step 6.
- **LEDs in parallel (a warning):** it is tempting to drive several LEDs in parallel from one resistor. Real LEDs are not resistors; their current depends steeply on voltage (Phase 11), so the brightest one hogs most of the current. The current divider with real resistors is well-behaved; with diodes it is not. Each LED gets its own resistor.
- **Ground paths on a circuit board:** when a current has two ways back to the battery (a thin trace and a wide copper area), it splits by conductance just like here. Most of it takes the wide, low-resistance path. Phase 21 builds on this.

## Try It in the Lab

Open the lab task **"Protect the meter with a shunt"**. A current source pushes 10 mA into node A. A fixed 1 kOhm resistor RM stands in for a delicate meter that reads full scale at 1 mA and must not get more. One empty slot sits in parallel with it, and the tray has five resistors.

Goals: the meter must get between 0.85 mA and 1.0 mA, and the shunt must stay under 1/4 W.

Think first: what share of the 10 mA should the meter get? Using "same voltage across both branches", how small should the shunt be compared with 1 kOhm? The exact answer is not a standard value. Which way should you round so the meter stays safe, and what happens to the reading if you round the other way?

## Common Mistakes

- **Using the voltage-divider form.** Writing I1 = I x R1 / (R1 + R2) gives the current of the *other* branch. Sanity check: the smaller resistor must get the bigger current.
- **Applying the two-branch formula to three branches.** I x R2/(R1+R2) is only for two branches. For more, use conductances, or combine all the others into one equivalent resistor first.
- **Forgetting that the source matters.** The split ratio depends only on the branch resistances, but the *total* current depends on the whole circuit. If a battery feeds the parallel pair, adding a branch lowers the total resistance and increases the total current. Only with an ideal current source does the total stay fixed.
- **Believing "all the current takes the easy path".** Only a true short takes all of it. Every finite resistance carries some current, I = V/R.
- **Mixing up conductance units.** 1/1000 Ohm is 0.001 S = 1 mS, not 1 kS.
- **Forgetting the shunt's power.** At large currents a tiny shunt still gets hot: 10 A through 0.01 Ohm is P = I^2 x R = 1 W.

## Exercises

1. 12 mA arrive at 1 kOhm in parallel with 2 kOhm. Find each branch current with the formula, then check by finding the common voltage.
2. 100 mA split between 10 Ohm, 22 Ohm and 47 Ohm in parallel. Compute the conductances, the share of each branch, and the branch currents. Verify that the voltage across each branch is the same.
3. A 5 V supply feeds a 100 Ohm series resistor, then 150 Ohm in parallel with 330 Ohm. Find the total current, each branch current, and check KVL.
4. A meter movement has 200 Ohm resistance and reads full scale at 50 microamps. What shunt makes it read 10 mA at full scale? How much power does the shunt dissipate at full scale?
5. (Harder) You want a branch to get exactly one third of a total current, and the other branch is a fixed 1.5 kOhm resistor. What resistance must the first branch have? Now there are three branches: 1.5 kOhm, 1 kOhm and an unknown R. What R makes the 1 kOhm branch carry exactly half of the total?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Current divider | "The current splits" | Parallel branches share one voltage, so a total current I splits as I1 = I x R2/(R1+R2) for two branches |
| Inverse proportion | "The small one takes more" | Branch current is proportional to 1/R: halve the resistance and that branch's share of the voltage-driven current doubles |
| Conductance | "The opposite of resistance" | G = 1/R in siemens; parallel conductances add, and each branch gets I x G_k / sum(G) |
| Shunt | "A bypass resistor" | A low resistance in parallel with something sensitive, sized so a known small fraction of the current goes through that something |
| Full scale | "The max of the meter" | The current (or voltage) that moves the needle to the end of its dial |
| Current source | "A source that fixes the current" | An idealized source that delivers a set current no matter what voltage is needed; it makes the total current of a divider constant |

## Further Reading

- All About Circuits, *Lessons in Electric Circuits*, Volume I (DC), chapter "Divider Circuits and Kirchhoff's Laws", section on current divider circuits.
- *Practical Electronics for Inventors* (Scherz & Monk), chapter 2, the parts on parallel resistors and current division.
- *The Art of Electronics* (Horowitz & Hill), chapter 1, for the conductance view and quick mental arithmetic with parallel resistors.
- A current-sense resistor datasheet (for example Vishay's WSL series), to see real shunt values, power ratings and tolerances.
