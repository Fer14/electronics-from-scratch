# Series and Parallel Resistors

> Resistors in one path add up; resistors side by side add their conductances. Both rules are just Kirchhoff's two laws plus Ohm's law, applied once.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 02 (Your First Circuits), especially Lesson 04 (Series and Parallel Intuition); Phase 03 (Resistance and Ohm's Law); Phase 04 Lessons 01 to 03 (Nodes, Branches and Loops; Kirchhoff's Current Law; Kirchhoff's Voltage Law)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Series | Parts connected end to end in a single path, so the same current flows through all of them | Cars driving through three toll booths in a row on a one-lane road |
| Parallel | Parts connected between the same two nodes, so they all have the same voltage across them | Several checkout lanes open side by side in a supermarket |
| Equivalent resistance | The single resistor that would draw the same current from the same voltage as a whole network | Replacing a maze of pipes with one pipe that lets the same amount of water through |
| Conductance | How easily a part lets current through; the inverse of resistance, measured in siemens (S), 1 S = 1 / Ω | Width of a doorway, as opposed to how narrow it is |
| Product over sum | A shortcut for two resistors in parallel: multiply them, divide by their sum | A pocket-calculator trick |
| Network | Any group of resistors connected together with two terminals we look into | A black box with two wires sticking out |
| Reduce (a network) | Replace series or parallel groups by their equivalent, step by step, until one resistor is left | Simplifying a fraction one step at a time |
| `||` | Short notation for "in parallel with": R1 \|\| R2 | The symbol engineers scribble in margins |

## Learning Objectives

- Derive the series rule (resistances add) from KCL and KVL.
- Derive the parallel rule (conductances add) from KVL and KCL.
- Use the product-over-sum shortcut and the "n equal resistors" shortcut.
- Reduce a nested series-parallel network to a single equivalent resistance, step by step, by hand and with a recursive program.
- Build a resistance you do not have from two standard values.

## The Problem

You need a 150 Ω resistor for a circuit and your drawer only has 100, 220, 330, 470, 680, 1 k, 2.2 k and 4.7 kΩ. Can you make 150 Ω from those? (Yes: 220 Ω and 470 Ω side by side give 149.9 Ω.)

Or you are handed a board with seven resistors and a battery, and asked how much current the battery supplies. Writing KCL at every node and KVL around every loop works, but for many circuits there is a faster way: spot pieces that are in series or in parallel, replace each piece by one equivalent resistor, and repeat until one resistor is left. Then a single Ohm's law gives the battery current.

You met the intuition in Phase 02 (Lesson 04): series makes things harder for current, parallel makes it easier. In this lesson you will prove the exact formulas from Kirchhoff's laws, so you know precisely when they apply and when they do not.

## The Physics

Nothing new happens physically in this lesson; that is the point. Every rule here is a consequence of three things you already know:

1. **Ohm's law** (Phase 03, Lesson 03): for a resistor, the voltage across it equals current through it times its resistance, V = I × R. Physically, electrons drifting through a material collide with its atoms, and the push needed (voltage) is proportional to how fast they flow (current).
2. **KCL** (Lesson 02): charge does not pile up at a node, so current in equals current out.
3. **KVL** (Lesson 03): potential is a level, so voltages around a loop add to zero.

Physically, what does putting resistors in series do? Think of a long, thin wire. In Phase 03 (Lesson 02) you saw that resistance grows in proportion to length: R = ρ × L / A (resistivity times length divided by cross-section area). Two 1 m pieces joined end to end are a 2 m wire, with twice the resistance. Series is "making the path longer". Parallel is the opposite: two identical wires side by side are like one wire with twice the cross-section area, so half the resistance. Parallel is "making the path wider". The formulas below generalise this to resistors of different values.

## The Concept

### Series: same current, voltages add

```
            R1         R2         R3
   vcc ───[////]──a──[////]──b──[////]─── gnd
    |                                      |
    └────────────── battery V ─────────────┘
```

Three resistors end to end, in a single path from vcc to gnd.

**Step 1 (KCL):** nodes a and b each have just two branches touching them. Whatever comes in through one must leave through the other. So the same current I flows through R1, R2 and R3. That is the defining property of series.

**Step 2 (Ohm):** the voltages across them are I × R1, I × R2 and I × R3.

**Step 3 (KVL):** around the loop, the battery's rise equals the sum of the drops:

```
V = I×R1 + I×R2 + I×R3 = I × (R1 + R2 + R3)
```

**Step 4:** compare with one single resistor R_eq across the battery: V = I × R_eq. They draw the same current from the same voltage if

```
R_eq = R1 + R2 + R3        (series: resistances add)
```

Read it aloud: *the equivalent resistance of resistors in series is the sum of their resistances.*

Worked example with 9 V and 100 Ω, 220 Ω, 330 Ω:

```
R_eq = 100 + 220 + 330 = 650 Ω
I = 9 V / 650 Ω = 0.013846 A = 13.846 mA
drops: 13.846 mA × 100 Ω = 1.385 V
       13.846 mA × 220 Ω = 3.046 V
       13.846 mA × 330 Ω = 4.569 V
check: 1.385 + 3.046 + 4.569 = 9.000 V  ✓
```

Two consequences: the series total is always **bigger than the biggest** resistor, and the biggest resistor gets the biggest share of the voltage.

### Parallel: same voltage, currents add

```
   vcc ───┬──────────┬──────────┬──────────┐
          |          |          |          |
      [battery V]   [R1]       [R2]       [R3]
          |          |          |          |
   gnd ───┴──────────┴──────────┴──────────┘
```

Three resistors each connected between the same two nodes, vcc and gnd.

**Step 1 (KVL):** take the loop through the battery and R1: the battery's V must equal R1's voltage. Same for R2 and R3. So every resistor has the full V across it. That is the defining property of parallel.

**Step 2 (Ohm):** the currents are V / R1, V / R2 and V / R3.

**Step 3 (KCL):** at node vcc, the current from the battery splits into the three branches:

```
I = V/R1 + V/R2 + V/R3 = V × (1/R1 + 1/R2 + 1/R3)
```

**Step 4:** for a single resistor R_eq, I = V / R_eq = V × (1/R_eq). Same current if

```
1/R_eq = 1/R1 + 1/R2 + 1/R3        (parallel: conductances add)
```

Read it aloud: *one over the equivalent resistance equals the sum of one over each resistance.* Since 1/R is the **conductance** G (in siemens), this says: in parallel, conductances add. More doorways side by side, more total width.

Worked example with 9 V across 1 kΩ, 2.2 kΩ and 4.7 kΩ:

```
I1 = 9 / 1000 = 9.000 mA
I2 = 9 / 2200 = 4.091 mA
I3 = 9 / 4700 = 1.915 mA
total I = 15.006 mA
R_eq = 9 V / 0.015006 A = 599.8 Ω
formula: 1 / (0.001 + 0.000455 + 0.000213) = 1 / 0.001668 = 599.8 Ω  ✓
```

Two consequences: the parallel total is always **smaller than the smallest** resistor (adding a path can only make it easier), and the *smallest* resistor carries the *biggest* current.

### Shortcuts

**Two in parallel, product over sum.** For exactly two resistors, the parallel formula simplifies to

```
R1 || R2 = (R1 × R2) / (R1 + R2)
```

Example: 220 || 330 = 72 600 / 550 = 132 Ω. (Check: 1/220 + 1/330 = 0.004545 + 0.003030 = 0.007576, and 1/0.007576 = 132 Ω.) Warning: this shortcut works for **two only**. For three, use 1/R or apply it twice.

**n equal resistors.** n equal resistors R in series give n × R; in parallel give R / n. Four 1 kΩ in parallel: 250 Ω.

**Very different values.** 1 kΩ in parallel with 1 MΩ (a million ohms) is 999 Ω: the huge one hardly matters, because almost no current goes through it. 1 kΩ in series with 1 Ω is 1001 Ω: the tiny one hardly matters. A good habit is to estimate first: "in series, the big one wins; in parallel, the small one wins".

### What "in series" and "in parallel" really require

Two resistors are in **series** only if *nothing else* connects to the node between them. If a third branch touches that middle node, current can leave there and the two currents differ.

Two resistors are in **parallel** only if *both* their ends are on the *same two nodes*. Being drawn side by side on paper is not enough; check the nodes.

```
   vcc ──[R1]── a ──[R2]── gnd          R1 and R2 in series: a touches only them
                |
               [R3]                     ...unless R3 also touches a. Then R1 and R2
                |                       are NOT in series. But R2 and R3 are both
               gnd                      from a to gnd: they ARE in parallel.
```

This is why you always identify nodes first (Lesson 01).

### Reducing a network step by step

Take the ladder from Lesson 03 (there it had a 12 V battery; here we use 9 V to match the code):

```
   vcc ──[ R1 1k ]── a ──[ R3 1k ]── b
    |                |               |
  [9 V]          [R2 3k]          [R4 2k]
    |                |               |
   gnd ───────────── gnd ─────────── gnd
```

Work from the far end towards the battery:

1. R3 and R4: node b touches only these two, so they are in **series**: 1k + 2k = 3 kΩ. Replace them by one 3 kΩ from a to gnd.
2. That 3 kΩ and R2 (3 kΩ) both go from a to gnd: **parallel**: 3k × 3k / 6k = 1.5 kΩ.
3. R1 and the 1.5 kΩ: node a now touches only these two: **series**: 1k + 1.5k = 2.5 kΩ.

The battery sees 2.5 kΩ, so it supplies 9 V / 2500 Ω = **3.6 mA**. Now work back outwards to get everything else: R1 drops 3.6 mA × 1 kΩ = 3.6 V, so v(a) = 9 - 3.6 = 5.4 V; the two 3 kΩ paths share the current equally, 1.8 mA each; R4 gets 1.8 mA × 2 kΩ = 3.6 V, so v(b) = 3.6 V.

We can write the whole structure in one line:

```
R1 + ( R2 || (R3 + R4) )
```

That bracketed expression is exactly what the code's recursive reducer evaluates.

### When series-parallel is not enough

Some circuits have no pair in series or in parallel at all. The bridge from Lesson 01 (five resistors in a diamond with one across the middle) is the famous example: no node touches only two resistors, and no two resistors share both nodes. For those you must go back to KCL and KVL directly (Lesson 07 handles the balanced case, and Phase 05 the general one).

## Build It

Run the program:

```
uv run python phases/04-kirchhoffs-laws/04-series-and-parallel-resistors/code/main.py
```

### Step 1: Series from the laws

The program applies the derivation literally: one current from KCL, then KVL to find it.

```python
chain = [100.0, 220.0, 330.0]
current = supply / sum(chain)
drops = [current * r for r in chain]
```

It prints 13.846 mA, the three drops, their sum of 9.000 V, and V / I = 650 Ω.

### Step 2: Parallel from the laws

```python
bank = [1000.0, 2200.0, 4700.0]
branch_currents = [supply / r for r in bank]
total_current = sum(branch_currents)
equivalent = supply / total_current
```

Each resistor gets the full 9 V (KVL), the currents add (KCL), and V / I_total = 599.8 Ω, matching 1 / (1/1000 + 1/2200 + 1/4700).

### Step 3: A network as nested lists

We describe a network as a tree: a plain number is one resistor; `series(...)` and `parallel(...)` group smaller networks.

```python
def series(*parts):
    return ("series", list(parts))


def parallel(*parts):
    return ("parallel", list(parts))


ladder = series(1000, parallel(3000, series(1000, 2000)))
```

That line is R1 + (R2 || (R3 + R4)) from The Concept.

### Step 4: The recursive reducer

```python
def reduce_network(network, depth=0):
    if isinstance(network, (int, float)):
        return float(network)
    kind, parts = network
    values = [reduce_network(part, depth + 1) for part in parts]
    if kind == "series":
        result = sum(values)
        ...
    else:
        result = 1.0 / sum(1.0 / v for v in values)
        ...
    print(...)
    return result
```

*Recursive* means the function calls itself: to reduce a group, first reduce each of its parts (which may be groups themselves), then combine them with the series or parallel rule. The innermost groups are reduced first, exactly like working from the far end of the ladder. The output shows each step, indented by depth:

```
        series   1000 + 2000 = 3 kohm
      parallel 1 / (1/3000 + 1/3000) = 1.5 kohm
    series   1000 + 1500 = 2.5 kohm
    equivalent = 2.5 kohm, battery current from 9.0 V = 3.600 mA
```

Compare with the hand reduction above. The program also reduces two other networks; check the "two pairs" one by hand: (100 + 220) || (330 + 470) = 320 || 800 = 256 000 / 1120 = 228.6 Ω.

### Step 5: Making a value from a drawer of parts

```python
for first, second in combinations_with_replacement(drawer, 2):
    candidates.append((abs(first + second - target), f"{first} + {second}", first + second))
    both = first * second / (first + second)
    candidates.append((abs(both - target), f"{first} || {second}", both))
```

Every pair is tried in series and in parallel, and the three closest are printed. For 150 Ω the winner is 220 || 470 = 149.9 Ω (0.1 % off). For 1.5 kΩ, 2.2k || 4.7k = 1498.6 Ω, and 470 + 1000 = 1470 Ω is the best series option.

### Step 6: Check the lab circuit

The last part reduces S1 + (R2 || S2) with one candidate pair and prints the battery current and node voltage. Use it to check your own reasoning for the lab after you have tried it.

## Use It

- **Odd values in real designs.** Standard E12 resistors come in 12 values per decade (Phase 03, Lesson 04). Designers who need, say, 150 Ω exactly and have only E12 on the reel often put two in parallel or series. Precision voltage references sometimes use series pairs to hit a value within 0.1 %.
- **Sharing heat.** Two 1/4 W resistors of 200 Ω in parallel act like one 100 Ω resistor that can handle about 1/2 W, because each one carries half the current and dissipates half the power. Power supplies use banks of parallel resistors for this (Phase 03, Lesson 05).
- **Paralleled LEDs and loads in your house.** Every outlet and lamp in a house is in parallel across the mains, so each gets the full voltage and switching one off does not affect the others. Old Christmas lights were wired in series: one blown bulb broke the single path and the whole string went dark.
- **Multimeter shunts.** An ammeter measures large currents by putting a tiny resistance in parallel with its sensitive meter, so most of the current bypasses it (Phase 06).
- **Thermal and fluid "resistances"** follow the same rules: heat-sink thermal resistances in series add (Phase 18), which is why you meet these formulas far outside electronics.

## Try It in the Lab

Open the lab task for this lesson. A 9 V battery feeds an empty slot S1 to node a. From node a, a fixed 1 kΩ load R2 goes to ground, and a second empty slot S2 sits in parallel with it. Fill both slots so that the battery current through S1 is between 5.6 and 6.3 mA (so the whole network looks like about 1.5 kΩ), the load voltage at node a is between 1.7 and 2.1 V, and S1 stays under 1/4 W.

Think about: what total resistance does 6 mA from 9 V mean? If node a is near 1.9 V and about 6 mA arrives there, what is the resistance of the parallel pair? Which part in parallel with 1 kΩ gives that? And then what is left for S1 in series? Only one combination of the parts meets every goal.

## Common Mistakes

- **Calling two resistors "in series" when a third branch touches the node between them.** Then their currents differ. Check that the middle node has exactly two branches.
- **Calling two resistors "in parallel" because they are drawn side by side.** They must share both nodes. Trace each end.
- **Forgetting the final 1/x in the parallel formula.** 1/1000 + 1/2200 + 1/4700 = 0.001668 is a conductance in siemens. The resistance is 1 / 0.001668 = 599.8 Ω. A quick check: a parallel result must be smaller than the smallest resistor.
- **Using product over sum for three resistors.** (R1 × R2 × R3) / (R1 + R2 + R3) is wrong; it does not even have units of ohms. Pair them up, or use the 1/R form.
- **Reducing from the battery outwards.** Start from the part of the network farthest from the terminals you are looking into, and work inwards.
- **Forgetting to "un-reduce".** The equivalent resistance gives the total current. To find a voltage or current inside the network, go back through your steps in reverse, applying Ohm's law at each stage.

## Exercises

1. Find the equivalent resistance of 470 Ω, 1 kΩ and 2.2 kΩ (a) in series and (b) in parallel. For each case, compute the current drawn from a 5 V supply.
2. Using only 1 kΩ resistors, how would you make 500 Ω, 1.5 kΩ, and 667 Ω? (Hint: the last one uses three.)
3. Reduce this network to one resistor and find the battery current: 12 V across 100 Ω + (330 Ω || 470 Ω) + 220 Ω. Then find the voltage across the 330 Ω resistor.
4. Write the network "1 kΩ in parallel with (2.2 kΩ in series with (4.7 kΩ in parallel with 4.7 kΩ))" using `series` and `parallel` and run `reduce_network` on it. Predict the result by hand first.
5. (Harder) Two resistors in parallel give 120 Ω and in series give 500 Ω. Find both resistances. (Hint: write R1 + R2 = 500 and R1 × R2 / 500 = 120, then think about which two numbers add to 500 and multiply to 60 000.)

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Series | "One after the other on the page" | Connected so that the node between them touches nothing else, which forces the same current through both |
| Parallel | "Side by side" | Both ends connected to the same two nodes, which forces the same voltage across both |
| Equivalent resistance | "The total resistance" | The single resistor that draws the same current from the same voltage as the network, seen from two chosen terminals |
| Conductance | "The opposite of resistance" | G = 1/R in siemens; in parallel, conductances add just as resistances add in series |
| Product over sum | "The parallel formula" | A shortcut valid only for exactly two resistors in parallel |
| Reduce a network | "Simplify the circuit" | Repeatedly replace series or parallel groups by their equivalent until one resistor remains |

## Further Reading

- *All About Circuits*, Volume I (DC), chapters "Series and Parallel Circuits" and "Series-Parallel Combination Circuits": many reduction examples with step-by-step tables.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, 4th ed., Chapter 2 (sections on resistors in series and parallel): practical, with real part values.
- Khan Academy, Electrical Engineering, "Resistors in series" and "Resistors in parallel": short videos deriving the same formulas.
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., section 1.2: the compact engineer's version, including the "big one wins / small one wins" estimation habit.
