# Nodal Analysis

> Pick ground, call every other node's voltage an unknown, and balance the currents at each node. That is the whole method.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 04 (Kirchhoff's Laws), especially Lesson 02 (Kirchhoff's Current Law); Phase 05 Lesson 01 (Systematic Analysis)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Node voltage | The voltage of a node measured from ground, written `vb` for node b | The height of a spot measured from sea level |
| Reference node | Another name for ground: the node whose voltage we define as 0 V | Sea level |
| Conductance | How easily a part lets current through; the opposite of resistance, `G = 1 / R` | How wide a door is, instead of how narrow |
| Siemens (S) | The unit of conductance; 1 S is the conductance of a 1 Ω resistor | Doors measured in "people per second per push" |
| Millisiemens (mS) | One thousandth of a siemens; the conductance of a 1 kΩ resistor | |
| Injected current | Current that a source pushes into a node from outside the resistor network | A tap pouring water into a tank |
| Conductance matrix | The table of numbers in nodal analysis: how strongly each node is tied to itself and to each neighbour | A table of how wide every door between rooms is |
| Nodal analysis by inspection | Writing the conductance matrix straight from the drawing, using a pattern, without deriving each equation | Filling a form you already know by heart |
| Grounded voltage source | A voltage source with one terminal at ground, which fixes one node's voltage outright | A water tower: its level is known |
| Floating voltage source | A voltage source between two nodes, neither of which is ground | A pump between two tanks, both of unknown level |
| Supernode | Two nodes joined by a floating voltage source, treated as one big node for KCL | Two rooms joined by an open archway, counted as one area |

## Learning Objectives

- Choose a ground node and name the node voltages that are the unknowns of nodal analysis.
- Write the current in any resistor in terms of the two node voltages at its ends.
- Write KCL at every non-ground node and collect the equations into the form `G v = i`.
- Build the conductance matrix by inspection: sum of conductances on the diagonal, minus the shared conductance off the diagonal.
- Handle grounded voltage sources (a known node) and explain why floating voltage sources need something more.
- Implement a nodal-analysis builder in NumPy and check it against our simulator.

## The Problem

In Lesson 01 you solved the workhorse circuit with four unknown currents and four equations. It worked, but most of the work was bookkeeping: two KCL equations, two KVL equations, careful choice of loops, and avoiding the loop with the current source.

There is a better choice of unknowns. Look at the answer we got: once you knew `vb = 7 V` and `vc = 2.5 V`, every current followed immediately from Ohm's law. `i3 = (7 - 2.5) / 3 kΩ = 1.5 mA`, and so on. The two node voltages were the real information; the four currents were consequences.

So what if the node voltages were the unknowns from the start? Then:

- there is one unknown per node (minus ground), not one per resistor;
- KVL is automatically true, because every voltage is measured from the same ground (we will see why);
- only KCL is left to write, and KCL at a node is easy to read off the drawing.

This is **nodal analysis**, and it is the method behind every circuit simulator. In a circuit with 50 resistors and 20 nodes, it means 19 unknowns instead of 50.

## The Physics

Why does choosing node voltages make KVL disappear? Think of node voltages as heights above sea level. The voltage across any part is the height difference between its two ends: `v_across = v_start - v_end`. Walk around any closed loop and add up the height differences:

```
(v1 - v2) + (v2 - v3) + (v3 - v1) = 0
```

Every height appears once with a plus and once with a minus, so the sum is always zero. KVL is not an extra law we must enforce; it is built into the very idea of "each node has one voltage". Physically, that is energy conservation: a charge that returns to its starting node has the same energy per charge it started with (Phase 01, Lesson 04).

KCL, on the other hand, is a real constraint: it says charge does not pile up. That is what we must write. At each node, the currents leaving through the resistors must equal the currents pushed in by sources.

And the link between voltages and currents is Ohm's law. For a resistor R between node x and node y, the current flowing from x to y is

```
current from x to y = (vx - vy) / R
```

Read it as: "the current through a resistor is the voltage difference across it, divided by its resistance; it flows from the higher node to the lower one." If `vx` is bigger, the result is positive and current flows from x to y. If `vy` is bigger, the result is negative, which simply means the current flows from y to x.

### Conductance: dividing becomes multiplying

Dividing by R over and over is clumsy. Engineers use **conductance**, `G = 1 / R`, measured in **siemens** (S), named after Werner von Siemens. A 1 kΩ resistor has `G = 1 / 1000 Ω = 0.001 S = 1 mS`. A 2 kΩ resistor has 0.5 mS. Big conductance means an easy path, a wide door.

With conductance, Ohm's law becomes `current = G × (vx - vy)`. In the kΩ-mA-V system from Lesson 01, conductances are in mS and `mS × V = mA`.

What the "door" picture gets wrong: a door has a fixed width, but electric current through a resistor depends on both the door width and how hard it is pushed (the voltage difference). A resistor with zero voltage across it carries zero current no matter how wide the door.

## The Concept

### The recipe

```
1. Pick a ground node (0 V). Usually the node with the most connections,
   or the bottom wire where the battery's minus side sits.
2. Name the voltage of every other node: v1, v2, ... (or va, vb, ...).
   If a voltage source connects a node directly to ground, that node's
   voltage is KNOWN. Do not make it an unknown.
3. At every unknown node, write KCL:
     sum over resistors of (v_this - v_neighbour) / R  =  current injected by sources
   "Current leaving through resistors equals current pushed in."
4. Solve the system. Then compute any current you want with Ohm's law.
```

### Our workhorse, by nodal analysis

```
        a      R1 = 1 kΩ      b      R3 = 3 kΩ      c
   ┌────●────/\/\/\/\────●────/\/\/\/\────●──────────┐
   │                     │                 │          │
 [V1] 12 V             [R2] 2 kΩ         [R4] 1 kΩ  (I1) 1 mA, up into c
   │                     │                 │          │
   └─────────────────────┴─────────────────┴──────────┘
                         gnd (0 V)
```

Step 1: ground is the bottom wire.
Step 2: `va = 12 V` (known, the battery fixes it). Unknowns: `vb`, `vc`.
Step 3, KCL at b. Three resistors touch b; the current leaving b through each of them is:

```
through R1 (to a):   (vb - 12) / 1
through R2 (to gnd): (vb - 0)  / 2
through R3 (to c):   (vb - vc) / 3
```

No source pushes current directly into b, so these three add to zero:

```
(vb - 12)/1 + vb/2 + (vb - vc)/3 = 0
```

KCL at c. Two resistors touch c, and the current source pushes 1 mA in:

```
(vc - vb)/3 + vc/1 = 1
```

(Everything in kΩ, mA, V.)

### Tidy the equations

Multiply out and group the terms of each unknown. For node b:

```
vb × (1/1 + 1/2 + 1/3)  -  vc × (1/3)  =  12/1
vb × 1.8333             -  vc × 0.3333 =  12
```

The `12/1` moved to the right side because it is a known number: "current pushed into b from the known 12 V node through R1's conductance" = `12 V × 1 mS = 12 mA`.

For node c:

```
-vb × (1/3)  +  vc × (1/3 + 1/1)  =  1
-vb × 0.3333 +  vc × 1.3333       =  1
```

### Solve

From the second equation, `vc = (1 + 0.3333 vb) / 1.3333 = 0.75 + 0.25 vb`.

Put that in the first:

```
1.8333 vb - 0.3333 × (0.75 + 0.25 vb) = 12
1.8333 vb - 0.25 - 0.08333 vb          = 12
1.75 vb                                = 12.25
vb                                     = 7 V
```

and `vc = 0.75 + 0.25 × 7 = 2.5 V`. The same answer as Lesson 01, with half the unknowns.

### The pattern: conductance matrix by inspection

Write the tidy equations as a matrix:

```
        vb          vc            right side
b  [ 1/1+1/2+1/3   -1/3     ]  [ vb ]   [ 12/1 ]
c  [   -1/3       1/3+1/1   ]  [ vc ] = [  1   ]
```

Look closely and you see a pattern you can use without deriving anything:

- **Diagonal entry (row b, column b):** the sum of the conductances of every resistor touching node b. (1 + 0.5 + 0.333 mS.)
- **Off-diagonal entry (row b, column c):** minus the conductance of the resistor that connects b and c directly. If no resistor connects them, zero.
- **Right side of row b:** the current pushed into b by sources. A current source pointing into b adds its current; one pointing out subtracts it. A resistor to a *known* node (like a, at 12 V) adds `G × v_known`.

The matrix is symmetric (row b, column c equals row c, column b), because the resistor between b and c ties both nodes equally. This is called writing the equations **by inspection**, and once you have done it three times you can do it in your head.

Read the matrix equation `G v = i` out loud: "conductances times node voltages equal injected currents". It is Ohm's law (`I = G V`) for the whole network at once.

### A second example: three nodes, current sources only

```
      I_A = 4 mA                          I_B = 2 mA
     (into n1)                           (out of n3)
         ↑                                    ↓
   n1 ───●────/\/\ 2 kΩ /\/\────●──── n2 ────/\/\ 1 kΩ /\/\────●──── n3
         │                       │                              │
        2 kΩ                    4 kΩ                           4 kΩ
         │                       │                              │
   gnd ──┴───────────────────────┴──────────────────────────────┴──
```

Conductances: 2 kΩ is 0.5 mS, 1 kΩ is 1 mS, 4 kΩ is 0.25 mS.

By inspection:

```
        v1      v2      v3           right side
n1 [  0.5+0.5   -0.5     0    ]     [  4 ]
n2 [   -0.5   0.5+0.25+1  -1  ]     [  0 ]
n3 [    0      -1     1+0.25  ]     [ -2 ]
```

which is

```
[  1.0   -0.5    0.0  ] [v1]   [  4 ]
[ -0.5    1.75  -1.0  ] [v2] = [  0 ]
[  0.0   -1.0    1.25 ] [v3]   [ -2 ]
```

Solve by substitution, the slow and safe way.

From row n1: `1.0 v1 - 0.5 v2 = 4`, so `v1 = 4 + 0.5 v2`.
From row n3: `-1.0 v2 + 1.25 v3 = -2`, so `v3 = (-2 + v2) / 1.25 = -1.6 + 0.8 v2`.
Put both into row n2:

```
-0.5 (4 + 0.5 v2) + 1.75 v2 - 1.0 (-1.6 + 0.8 v2) = 0
-2 - 0.25 v2 + 1.75 v2 + 1.6 - 0.8 v2            = 0
0.7 v2 - 0.4                                      = 0
v2                                                = 0.5714 V
```

Then `v1 = 4 + 0.5 × 0.5714 = 4.2857 V` and `v3 = -1.6 + 0.8 × 0.5714 = -1.1429 V`. (As fractions: 30/7, 4/7 and -8/7 volts.)

A negative node voltage is perfectly normal: current source I_B pulls charge out of n3 faster than the network can refill it from ground, so n3 sits below ground.

### Always check one node

Check KCL at n2 with these numbers. The current leaving n2 through each resistor is:

```
to n1     (2 kΩ, 0.5 mS):  0.5  × (0.5714 - 4.2857)    = -1.8571 mA
to ground (4 kΩ, 0.25 mS): 0.25 × (0.5714 - 0)         =  0.1429 mA
to n3     (1 kΩ, 1 mS):    1.0  × (0.5714 - (-1.1429)) =  1.7143 mA
                                                  sum  =  0.0000 mA
```

No source touches n2, so the sum must be zero, and it is. The negative first term means 1.857 mA actually *arrives* from n1; it splits into 0.143 mA to ground and 1.714 mA onward to n3.

Why bother? Suppose you had copied `v2 = 0.6 V` by mistake. The same check gives `0.5 × (0.6 - 4.2857) + 0.25 × 0.6 + 1.0 × (0.6 + 1.1429) = -1.8429 + 0.15 + 1.7429 = 0.05 mA`: not zero, so you would know immediately that something is wrong. A KCL check at one node costs thirty seconds and catches most mistakes.

### Voltage sources: the grounded kind is easy

In the workhorse, V1 sits between node a and ground, so `va = 12 V` is simply known. In the KCL equations, `va` shows up only as a known number times a conductance, which we move to the right side. Nodal analysis loves grounded voltage sources: each one *removes* an unknown.

### Voltage sources: the floating kind is the problem

Now imagine a battery between two nodes, neither of them ground:

```
   p ───[+ 5 V -]─── q
```

We know `vp - vq = 5 V`, but not `vp` or `vq` separately. And what current flows through the battery? A voltage source, like a current source in Lesson 01, takes whatever current the circuit asks for. That current is unknown, and it appears in the KCL of both p and q. So nodal analysis, as described, gets stuck.

The classic hand trick is the **supernode**: draw a bubble around p, q and the battery, and write KCL for the whole bubble (the battery's unknown current is inside the bubble, so it cancels). Then add the equation `vp - vq = 5` to replace the lost KCL equation. It works, but it is a special case a human must spot. Lesson 04 replaces the trick with a rule a computer can apply blindly: make the battery current an extra unknown. That rule is modified nodal analysis.

## Build It

`code/main.py` builds the conductance matrix from a list of parts, solves it, and compares the result with `sim`.

### Step 1: describe parts as plain data

A resistor is a tuple `(node_x, node_y, ohms)`. A current source is `(from_node, to_node, amps)`, with current flowing from `from_node` through the source into `to_node`. Known nodes (fixed by grounded voltage sources) are a dictionary.

```python
analyse(
    "Workhorse: 12 V battery, four resistors, 1 mA source",
    [("a", "b", 1000), ("b", "0", 2000), ("b", "c", 3000), ("c", "0", 1000)],
    [("0", "c", 0.001)],
    {"a": 12.0},
)
```

### Step 2: fill the conductance matrix by inspection

For every resistor, add its conductance to the diagonal of both of its nodes and subtract it from the two off-diagonal places. If one end is a known node, its contribution `G × v_known` goes to the right side instead. Ground contributes nothing because its voltage is zero.

```python
def nodal_system(resistors, current_sources, known):
    unknown_nodes = sorted({n for x, y, _ in resistors for n in (x, y)} - {"0"} - set(known))
    index = {node: k for k, node in enumerate(unknown_nodes)}
    conductance = np.zeros((len(unknown_nodes), len(unknown_nodes)))
    injected = np.zeros(len(unknown_nodes))
    for node_x, node_y, ohms in resistors:
        g = 1.0 / ohms
        for this, other in ((node_x, node_y), (node_y, node_x)):
            if this not in index:
                continue
            conductance[index[this], index[this]] += g
            if other in index:
                conductance[index[this], index[other]] -= g
            elif other in known:
                injected[index[this]] += g * known[other]
    for from_node, to_node, amps in current_sources:
        if to_node in index:
            injected[index[to_node]] += amps
        if from_node in index:
            injected[index[from_node]] -= amps
    return unknown_nodes, conductance, injected
```

Notice the loop over `(node_x, node_y), (node_y, node_x)`: each resistor is seen once from each end, exactly as KCL at each node sees it.

### Step 3: solve and print

Inside `analyse`:

```python
nodes, conductance, injected = nodal_system(resistors, current_sources, known)
voltages = np.linalg.solve(conductance, injected)
```

The printed matrix (in mS) is `[[1.833, -0.333], [-0.333, 1.333]]`, the same as our hand version, and the voltages are 7 V and 2.5 V.

### Step 4: compare with the simulator

The same circuits are built with `sim.Circuit` and solved with `.dc()`. The code prints both answers side by side and the largest difference (a few nanovolts; the simulator adds a hidden, tiny conductance from every node to ground called gmin, which Lesson 04 explains).

### Step 5: check KCL at every node

For each unknown node, the code adds the currents leaving through resistors and subtracts the injected currents. Every residual prints as zero, which is the check that saved us in the second example.

## Use It

- **SPICE is nodal at heart.** When LTspice or ngspice prints "Node voltages" first and branch currents second, it is because node voltages are the unknowns it solved for. The currents are computed afterwards with Ohm's law, just like you did.
- **Ground choice in real boards.** On a PCB, "ground" is the big copper plane every chip returns to. Designers choose it as the reference because most parts touch it; for nodal analysis that means many entries become zero.
- **Sensor networks.** A thermistor in a divider feeding a microcontroller's ADC input is a two-node nodal problem. The ADC's own input resistance (often tens of kΩ to MΩ, from its datasheet) is just one more conductance on the diagonal.
- **Very large circuits.** In a chip with a million nodes, each node connects to only a handful of neighbours, so almost every entry of the conductance matrix is zero. Simulators store only the non-zero entries ("sparse matrices"), which is why they can handle huge circuits.

## Try It in the Lab

The lab board has a 2 mA current source pushing into node a, a 2 kΩ resistor from a to ground, an empty slot from a to b, and a 2 kΩ resistor from b to ground. Choose the resistor for the slot so that node b sits between 1.5 V and 1.7 V.

Think about it before you try parts at random:

- Write KCL at a and at b with the slot resistor called `Rs`. How many unknowns are there?
- What happens to vb when `Rs` is tiny (almost a wire)? When it is huge (almost an open)?
- Can you solve for vb as a formula in `Rs` and then pick?

## Common Mistakes

- **Sign confusion with current sources.** A source pointing *into* a node adds to that node's right side; pointing *out of* it subtracts. Draw the arrow every time.
- **Making a known node an unknown.** If a battery ties a node to ground, its voltage is known. Treating it as unknown leaves you one equation short.
- **Forgetting the resistors to ground on the diagonal.** A resistor from b to ground appears on b's diagonal but has no off-diagonal partner. Beginners often drop it because "ground isn't an unknown".
- **Adding conductances in series.** On the diagonal you add the conductances of resistors touching that node, each one separately. Two resistors in series between b and c must first be combined (as resistances) or given their own middle node.
- **Mixing R and G.** Putting `3` (kΩ) in the matrix instead of `1/3` (mS). Write a `g = 1 / ohms` line and never touch R again.
- **Not checking.** As you saw above, a copied number can be wrong. One KCL check at one node takes thirty seconds.

## Exercises

1. In the workhorse, change R3 to 1 kΩ. Write the 2×2 conductance matrix by inspection and solve for vb and vc by hand. Check with the code.
2. A single node x has a 5 mA current source pushing into it and three resistors to ground: 1 kΩ, 2 kΩ and 2 kΩ. Use nodal analysis (a 1×1 "matrix") to find vx. (Answer: 2.5 V.)
3. In the three-node example, reverse I_B so it pushes 2 mA *into* n3. Predict which node voltages go up, then compute them with the code.
4. Write the conductance matrix of a ladder: node 1 to node 2 to node 3 in a chain, each link 1 kΩ, each node with 1 kΩ to ground, and a 12 V battery from node 1 to ground. What are v2 and v3? (Hint: v1 is known.)
5. Harder: put a 5 V battery between nodes b and c of the workhorse (plus at b), instead of R3. Solve it with a supernode by hand, then confirm with `sim`. Why can't `nodal_system` from this lesson handle it?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Nodal analysis | "Solve for the node voltages" | KCL at every non-ground node, with currents written as conductance times voltage difference |
| Conductance | "One over R" | The ease of current flow, `G = 1/R`, in siemens; currents are `G × ΔV` |
| Conductance matrix | "The G matrix" | Diagonal: sum of conductances at a node; off-diagonal: minus the conductance between two nodes |
| Injected current | "The right-hand side" | Current pushed into a node by sources, including `G × v_known` from known nodes |
| Grounded voltage source | "A rail" | A source that fixes one node's voltage, removing it from the unknowns |
| Supernode | "Bubble around the battery" | KCL written for a group of nodes joined by a floating voltage source, plus the source's voltage equation |

## Further Reading

- [All About Circuits, Vol. I, "Node Voltage Method"](https://www.allaboutcircuits.com/textbook/direct-current/chpt-10/node-voltage-method/): a free walkthrough of nodal analysis with worked examples.
- *Practical Electronics for Inventors*, Scherz and Monk, 4th edition, Chapter 2 (Theory), section on network analysis.
- [Khan Academy, Electrical Engineering, circuit analysis methods](https://www.khanacademy.org/science/electrical-engineering/ee-circuit-analysis-topic): gentle videos on the node voltage method.
- [MIT OCW 6.002 Circuits and Electronics](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/): the lecture notes on the node method, the workhorse of the course.
