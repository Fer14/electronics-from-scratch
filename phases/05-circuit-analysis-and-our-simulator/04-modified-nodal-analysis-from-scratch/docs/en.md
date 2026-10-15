# Modified Nodal Analysis from Scratch

> Every part writes its own small pattern of numbers into one big table. Add the patterns, solve the table, and you have built the heart of a circuit simulator.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 05 Lesson 01 (Systematic Analysis), Lesson 02 (Nodal Analysis) and Lesson 03 (Mesh Analysis)
**Time:** ~90 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Modified nodal analysis (MNA) | Nodal analysis plus one extra unknown, the current, for every voltage source | A form with one line per node, plus one extra line per battery |
| Stamp | The small fixed pattern of numbers one part adds into the big matrix | A rubber stamp: same shape every time, pressed wherever the part sits |
| Branch current (of a source) | The current flowing through a voltage source, from its plus terminal through the source to its minus terminal | The flow through a pump |
| Augmented system | The bigger matrix you get when you add the extra rows and columns for voltage sources | A spreadsheet with extra rows appended at the bottom |
| Index | The position number of an unknown in the list of unknowns | A seat number |
| Singular matrix | A matrix with no unique solution: some equation is missing or repeated | A puzzle with a clue missing |
| Floating node | A node with no path to ground through any part that can carry DC current | An island with no bridge |
| Netlist parser | Code that reads a text netlist like `R1 a b 1k` and turns it into parts | Reading a recipe card into a shopping list |
| Engineering suffix | A letter after a number that multiplies it: `k` thousand, `m` thousandth, `u` millionth | Writing "5k" for 5000 |
| gmin | A tiny conductance a simulator quietly adds from every node to ground so the matrix never becomes singular | A thread so thin it changes nothing, but keeps the island from drifting away |

## Learning Objectives

- Explain why plain nodal analysis cannot handle a voltage source between two non-ground nodes, and how MNA fixes it with an extra unknown.
- Write the stamps of a resistor, a current source and a voltage source, and say what each entry means physically.
- Assemble the full MNA system for a circuit by hand, adding stamps one part at a time, and solve it.
- Implement a complete MNA solver in NumPy that reads a text netlist, and verify it against our simulator on several circuits.
- Recognise the errors a solver reports for floating nodes and loops of voltage sources.

## The Problem

Lesson 02 left us with an ugly gap. Nodal analysis is wonderful for resistors and current sources, and it can handle a voltage source with one end on ground (the node becomes known). But a battery between two nodes that are both unknown, like this:

```
        a     R1 = 1 kΩ      b                c
   ┌────●────/\/\/\/\────●──[- V2 = 5 V +]──●──┐
   │                                            │
 [V1] 10 V                                   [R2] 2 kΩ
   │                                            │
   └────────────────────────────────────────────┘
                       gnd
```

...broke the method. We do not know the current through V2, and that current appears in the KCL equations of both b and c. Lesson 02 offered the supermesh-like "supernode" trick, and Lesson 03 offered the supermesh trick for current sources in mesh analysis. Both need a human to notice the special case and treat it specially.

A computer program needs a rule with **no special cases**: the same steps for every circuit, whatever its shape. In 1975, Chung-Wen Ho, Albert Ruehli and Pierce Brennan at IBM published exactly that rule. They called it **modified nodal analysis**. It is so simple and so general that half a century later it is still the core of SPICE, LTspice, ngspice, Xyce, the simulators inside chip-design tools, and the simulator in this course's `sim/` folder.

The idea fits in one sentence: *if you do not know the current through a voltage source, make it an unknown, and add the source's own equation to make up for it.*

In this lesson you build it, from an empty matrix to a working solver that reads netlists.

## The Physics

Nothing new physically. MNA uses the same three facts as every other method:

1. **KCL at every node** (charge does not pile up): the currents leaving a node through all its parts add up to zero.
2. **Each part's own rule:** for a resistor, current = `G × (v_x - v_y)` (Ohm's law with conductance `G = 1/R`); for a current source, current = fixed; for a voltage source, `v_plus - v_minus` = fixed.
3. **KVL is built in** because every node has one voltage measured from ground (Lesson 02).

What changes is the bookkeeping. In nodal analysis, every current had to be written in terms of node voltages. A voltage source refuses: its current is not set by its voltage at all (an ideal battery gives 0 A or 10 A at the same 5 V, whatever the circuit wants). So MNA stops trying. It keeps the source's current as its own unknown, called `j`, writes it directly into the KCL of the two nodes it touches, and adds one new row: the source's rule, `v_plus - v_minus = V`.

Each voltage source adds one unknown and one equation. The count stays balanced, and no case is special.

## The Concept

### The unknowns

For a circuit with N nodes besides ground and M voltage sources, the unknowns are:

```
x = [ v_1, v_2, ..., v_N,  j_1, j_2, ..., j_M ]
       node voltages        voltage-source currents
```

Each gets an **index**, its position in this list. Ground has no index: its voltage is 0 by definition and never appears.

For our example circuit above: nodes a, b, c (N = 3) and sources V1, V2 (M = 2). Five unknowns:

```
index:   0    1    2    3     4
x    = [ va,  vb,  vc,  j1,   j2 ]
```

Our convention (the same as SPICE and as `sim`): `j` is the current that flows *into* the source's plus terminal, *through* the source, and *out of* its minus terminal. A battery that is delivering energy pushes current *out* of its plus terminal, so its `j` comes out **negative**. Remember that; it surprises everyone the first time.

### The equations

The system is `A x = z`, five rows by five columns:

- Rows 0 to 2: KCL at nodes a, b, c, written as "current leaving the node through parts = current pushed in by current sources".
- Rows 3 and 4: the rules of V1 and V2.

We start with `A` full of zeros and `z` full of zeros, and let every part press its stamp.

### The resistor stamp

A resistor with conductance `g` between node x and node y. The current leaving x through it is `g × vx - g × vy`. The current leaving y through it is `g × vy - g × vx`. So in the KCL row of x, it adds `+g` in column x and `-g` in column y; in the row of y, `+g` in column y and `-g` in column x:

```
             col x   col y
   row x  [   +g      -g   ]
   row y  [   -g      +g   ]
```

If one end is ground, that row and column simply do not exist; only the one diagonal `+g` survives. This is exactly the "conductance matrix by inspection" of Lesson 02, now produced one resistor at a time.

### The current source stamp

A current source pushing `I` amps from node x, through itself, into node y. It takes `I` out of x and pushes `I` into y. Since the right side `z` holds "current pushed in":

```
   z[x] -= I
   z[y] += I
```

No matrix entries. A current source does not depend on any unknown.

### The voltage source stamp

A voltage source with plus terminal p, minus terminal m, value `V`, and its own index k.

In KCL: its current `j_k` flows *out of* node p into the source (it leaves p), and *out of* the source into node m (it arrives at m). So in row p add `+1` in column k (current leaving), and in row m add `-1` in column k.

Its own rule, row k: `v_p - v_m = V`. So row k gets `+1` in column p, `-1` in column m, and `z[k] = V`.

```
              col p   col m   col k        z
   row p   [                   +1  ]    [     ]
   row m   [                   -1  ]    [     ]
   row k   [   +1      -1          ]    [  V  ]
```

That is the whole trick. Two small additions to the nodal method: a column (the current shows up in KCL) and a row (the voltage rule).

### Assembling our example by hand

Parts: V1 (plus a, minus ground, 10 V, index 3), R1 (a-b, 1 kΩ, g = 1 mS), V2 (plus c, minus b, 5 V, index 4), R2 (c to ground, 2 kΩ, g = 0.5 mS). We work in kΩ, mA, V, so conductances are in mS and currents in mA.

Start from zeros and press each stamp.

**R1 (a-b, 1 mS):** `A[0,0] += 1`, `A[1,1] += 1`, `A[0,1] -= 1`, `A[1,0] -= 1`.

**R2 (c-ground, 0.5 mS):** only `A[2,2] += 0.5`.

**V1 (plus a = 0, minus ground, k = 3, 10 V):** `A[0,3] += 1`, `A[3,0] += 1`, `z[3] = 10`. (The minus side is ground, so its entries vanish.)

**V2 (plus c = 2, minus b = 1, k = 4, 5 V):** `A[2,4] += 1`, `A[1,4] -= 1`, `A[4,2] += 1`, `A[4,1] -= 1`, `z[4] = 5`.

The result:

```
           va    vb    vc    j1    j2          z
row a  [    1    -1     0     1     0  ]    [  0 ]
row b  [   -1     1     0     0    -1  ]    [  0 ]
row c  [    0     0   0.5     0     1  ]    [  0 ]
row V1 [    1     0     0     0     0  ]    [ 10 ]
row V2 [    0    -1     1     0     0  ]    [  5 ]
```

Read each row as a sentence to be sure it is right:

- Row a: "current leaving a through R1 (`va - vb`) plus current leaving a into V1 (`j1`) is zero."
- Row b: "current leaving b through R1 (`vb - va`) minus the current V2 delivers into b... (`-j2`, because j2 flows out of V2's minus terminal, which is b) is zero."
- Row c: "current leaving c through R2 (`0.5 vc`) plus current leaving c into V2's plus terminal (`j2`) is zero."
- Row V1: "`va = 10`."
- Row V2: "`vc - vb = 5`."

### Solving it by hand

Row V1 gives `va = 10 V` at once.
Row V2 gives `vc = vb + 5`.
Row c gives `j2 = -0.5 vc`.
Row b: `-10 + vb - j2 = 0`, so `-10 + vb + 0.5 vc = 0`. Put in `vc = vb + 5`:

```
-10 + vb + 0.5 (vb + 5) = 0
-10 + vb + 0.5 vb + 2.5 = 0
1.5 vb = 7.5
vb = 5 V
```

Then `vc = 10 V`, `j2 = -0.5 × 10 = -5 mA`, and from row a: `j1 = -(va - vb) = -(10 - 5) = -5 mA`.

Interpretation:

- Node b sits at 5 V and V2 lifts node c by another 5 V, to 10 V.
- Both sources have `j = -5 mA`: negative, which by our convention means each one pushes 5 mA *out* of its plus terminal. Both are delivering energy.
- The 5 mA goes a → R1 → b → (through V2, up 5 V) → c → R2 → ground → back to V1. One loop, one current, two batteries in series: 10 V + 5 V = 15 V across a total of 3 kΩ, which is 5 mA. The physics agrees with the matrix.

`sim` reports source currents with the opposite sign (`r.i("V1")` is +5 mA), because for a *source* it is friendlier to report the current it delivers out of its plus terminal. Same physics, different reporting convention. Always check which one a tool uses.

### What can go wrong: singular matrices

The solver needs the rows to be independent. Two classic circuit mistakes make them dependent:

- **A floating node.** A node connected only through a capacitor (in DC, an open), or through nothing at all. Its KCL row is all zeros or just repeats another row: there is no way to tell what its voltage is. Physically: an island with no bridge has no defined height above sea level.
- **A loop of voltage sources.** Two ideal batteries in parallel (or any loop made only of voltage sources). If they disagree (5 V and 6 V in parallel), there is no solution; if they agree, the current split between them is undefined. Physically: two ideal pumps fighting over the same pipe.

NumPy reports these as `LinAlgError: Singular matrix`. Real simulators add a tiny conductance, called **gmin**, from every node to ground (`sim` uses 10⁻¹² S, the conductance of a 1 TΩ resistor) so a floating node quietly sits at 0 V instead of crashing. It changes ordinary answers by parts in a billion. Our from-scratch solver leaves gmin out on purpose, so you can see the error.

### The size of the system

MNA's size is N + M: one row per node plus one per voltage source. Compare with Lesson 01's branch method (one per branch) and pure nodal (N, but cannot handle floating sources). MNA is slightly bigger than nodal but works for every circuit, which is what a program needs.

## Build It

`code/main.py` is a complete DC simulator for resistors, current sources and voltage sources, about a hundred lines, with a netlist parser. It then checks itself against `sim` on four circuits.

### Step 1: reading values with suffixes

Netlists write `4.7k` for 4700 and `100u` for 0.0001. A small table of multipliers does it.

```python
SUFFIXES = {"T": 1e12, "G": 1e9, "MEG": 1e6, "k": 1e3, "m": 1e-3, "u": 1e-6, "n": 1e-9, "p": 1e-12}

def parse_value(text):
    for suffix in sorted(SUFFIXES, key=len, reverse=True):
        if text.endswith(suffix):
            return float(text[: -len(suffix)]) * SUFFIXES[suffix]
    return float(text)
```

(SPICE uses `MEG` for mega because `M` already means milli in its old, case-blind syntax. We keep that tradition.)

### Step 2: reading a netlist

Each line is `NAME node node value`. The first letter of the name says what the part is: R resistor, I current source, V voltage source.

```python
def parse_netlist(text):
    parts = []
    for line in text.strip().splitlines():
        name, node_1, node_2, value = line.split()
        parts.append((name[0].upper(), name, node_1, node_2, parse_value(value)))
    return parts
```

### Step 3: number the unknowns

Every node except ground gets an index, then every voltage source gets the next free index.

```python
def number_unknowns(parts):
    nodes = []
    for _, _, node_1, node_2, _ in parts:
        for node in (node_1, node_2):
            if node not in GROUND and node not in nodes:
                nodes.append(node)
    sources = [name for kind, name, *_ in parts if kind == "V"]
    index = {node: k for k, node in enumerate(nodes)}
    index.update({name: len(nodes) + k for k, name in enumerate(sources)})
    return nodes, sources, index
```

### Step 4: the stamps

Each stamp is a few lines. The helper `add` ignores ground (index `None`), which is how ground's rows and columns "disappear".

```python
def stamp_resistor(matrix, index, node_1, node_2, ohms):
    g = 1.0 / ohms
    a, b = index.get(node_1), index.get(node_2)
    add(matrix, a, a, g)
    add(matrix, b, b, g)
    add(matrix, a, b, -g)
    add(matrix, b, a, -g)


def stamp_current_source(rhs, index, node_from, node_to, amps):
    if node_from in index:
        rhs[index[node_from]] -= amps
    if node_to in index:
        rhs[index[node_to]] += amps


def stamp_voltage_source(matrix, rhs, index, name, plus, minus, volts):
    k, p, m = index[name], index.get(plus), index.get(minus)
    add(matrix, p, k, 1.0)
    add(matrix, m, k, -1.0)
    add(matrix, k, p, 1.0)
    add(matrix, k, m, -1.0)
    rhs[k] += volts
```

### Step 5: assemble and solve

```python
def solve_mna(parts):
    nodes, sources, index = number_unknowns(parts)
    size = len(nodes) + len(sources)
    matrix = np.zeros((size, size))
    rhs = np.zeros(size)
    for kind, name, node_1, node_2, value in parts:
        if kind == "R":
            stamp_resistor(matrix, index, node_1, node_2, value)
        elif kind == "I":
            stamp_current_source(rhs, index, node_1, node_2, value)
        elif kind == "V":
            stamp_voltage_source(matrix, rhs, index, name, node_1, node_2, value)
    solution = np.linalg.solve(matrix, rhs)
    return matrix, rhs, {key: solution[k] for key, k in index.items()}
```

That is a working DC simulator. Everything else in `sim/` (capacitors, diodes, transistors, AC) is more stamps and a few loops around this function.

### Step 6: check against `sim`

For each test netlist, the code builds the same circuit with `sim.Circuit`, solves both, and prints every node voltage side by side. It also converts the source currents to `sim`'s convention (`-j`) before comparing. The four tests are:

1. The floating-battery circuit of this lesson (prints the 5×5 matrix you assembled by hand).
2. The workhorse from Lessons 01 to 03 (vb = 7 V, vc = 2.5 V again).
3. A ladder of six sections with two sources, too big to want to do by hand.
4. A deliberately broken circuit with a floating node, to show the singular-matrix error and how `sim`'s gmin avoids it.

Run it:

```
uv run python phases/05-circuit-analysis-and-our-simulator/04-modified-nodal-analysis-from-scratch/code/main.py
```

The differences with `sim` are a few nanovolts at most (around 10⁻⁹ to 10⁻⁸). They are not exactly zero only because `sim` includes gmin.

## Use It

- **SPICE netlists.** The format you parsed is a tiny subset of real SPICE. In LTspice or ngspice the same circuit is written `V1 a 0 10`, `R1 a b 1k`, `V2 c b 5`, `R2 c 0 2k`, followed by `.op` (operating point). Try it in LTspice: the answer will be vb = 5 V, vc = 10 V, and it will list `I(V1) = -0.005`, the same negative-current convention as our `j`.
- **Our own `sim/`.** Open `sim/stamp.py`: the methods `conductance`, `inject`, `branch` and `branch_voltage` are exactly the three stamps of this lesson, and every element in `sim/elements.py` has a `stamp` method that calls them. You can now read the simulator's core.
- **Bigger circuits.** Chip simulators solve MNA systems with millions of unknowns. The matrix is almost all zeros (each node touches a handful of parts), so they use sparse solvers, but the stamps are identical.
- **Debugging "singular matrix" errors.** When LTspice says "singular matrix" or "node X is floating", you now know what it means: some row has no information. The usual fixes are adding a large resistor (say 100 MΩ) from the floating node to ground, or removing two voltage sources fighting in parallel.

## Try It in the Lab

The lab board is the circuit of this lesson: a 10 V battery on node a, a 1 kΩ resistor from a to b, a floating 5 V battery from b (minus) to c (plus), and an empty slot from c to ground. Pick the resistor so that node c lands between 9.5 V and 10.5 V.

Before you try:

- Node c is always 5 V above node b. So what single loop does all the current follow, and what total voltage drives it?
- Write c's voltage as a formula in the slot resistance `Rs`. (It is a voltage divider in disguise.)

## Common Mistakes

- **Wrong sign of source current.** By the MNA convention, a delivering battery has negative `j`. Many people "fix" this by flipping the stamp, which silently breaks every other source. Keep the convention and translate when you report.
- **Forgetting that ground is not an unknown.** If you give ground an index, the matrix becomes singular (every column sums to zero). Ground must be left out.
- **Stamping the voltage source's row with the wrong order.** Row k says `v_plus - v_minus = V`. Swap plus and minus and every node voltage on that side of the source flips.
- **Two names for one node.** `"B"` and `"b"` are different strings, so they become two nodes. The solver will happily give an answer for a circuit you did not mean (or a singular matrix).
- **Parallel ideal voltage sources.** Two batteries directly in parallel make the system singular. Real batteries have internal resistance (Phase 06), which you must model with a resistor if you want to simulate them in parallel.
- **Confusing `m` and `M`.** In SPICE syntax `1M` is one milli-ohm, not one mega-ohm. Use `MEG`.

## Exercises

1. Assemble the MNA matrix of the workhorse by hand (unknowns va, vb, vc, j1): write the 4×4 matrix and right side. Check it against the matrix the code prints if you add a `print` for that test.
2. Add a current source of 2 mA from ground into node b of this lesson's floating-battery circuit. Predict, then solve with `solve_mna`: what are vb and vc now?
3. Write a netlist for two 9 V batteries in series driving a 1 kΩ resistor, using a floating source for the top battery. What does the solver give for each source's `j`?
4. Write a netlist where two voltage sources of 5 V and 6 V are in parallel. Run it through `solve_mna` and explain the error in one sentence. Then put a 1 Ω resistor in series with one source and run it again: what current flows between them?
5. Harder: add a stamp for a VCVS (a voltage-controlled voltage source, `out_plus - out_minus = gain × (v_cp - v_cm)`). Hint: it is the voltage-source stamp with two more entries in row k. Test it on a gain-of-10 amplifier and compare with `sim`'s `vcvs`. (Lesson 08 uses this part.)

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| MNA | "What SPICE does" | Nodal analysis with every voltage source's current added as an extra unknown and its voltage rule as an extra row |
| Stamp | "Each part adds its bit" | The fixed pattern of matrix and right-side entries that one part contributes |
| Resistor stamp | "+g on the diagonal, -g off" | `+g` at (x,x) and (y,y), `-g` at (x,y) and (y,x) |
| Voltage-source stamp | "The extra row and column" | `±1` linking the source current into KCL of its two nodes, and the row `v_p - v_m = V` |
| Source current sign | "Why is it negative?" | MNA's `j` flows from plus to minus inside the source; a delivering source has negative `j` |
| Singular matrix | "The sim crashed" | The equations do not pin down a unique answer: a floating node or a loop of voltage sources |
| gmin | "Some hidden resistor" | A tiny conductance (here 10⁻¹² S) from every node to ground that keeps the matrix solvable |

## Further Reading

- C.-W. Ho, A. E. Ruehli and P. A. Brennan, "The Modified Nodal Approach to Network Analysis", *IEEE Transactions on Circuits and Systems*, vol. 22, no. 6, pp. 504-509, 1975: the original paper.
- [Erik Cheever, "Analysis of Resistive Circuits", Swarthmore College](https://lpsa.swarthmore.edu/Systems/Electrical/mna/MNA1.html): a clear, free set of pages on the MNA algorithm and its matrix structure.
- [ngspice manual](https://ngspice.sourceforge.io/docs.html): the netlist syntax (element letters, `MEG` suffix, `.op`) used by real SPICE.
- *The Art of Electronics*, Horowitz and Hill, 3rd edition, Appendix J (SPICE primer): how real engineers use a simulator and what to watch out for.
