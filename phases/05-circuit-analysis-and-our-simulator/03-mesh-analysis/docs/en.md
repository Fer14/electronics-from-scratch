# Mesh Analysis

> Imagine a current circling inside every window of the drawing. Where two windows share a wire, their currents subtract. Balance the voltages around each window and you are done.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 04 (Kirchhoff's Laws), especially Lesson 01 (Nodes, Branches and Loops) and Lesson 03 (Kirchhoff's Voltage Law); Phase 05 Lesson 01 (Systematic Analysis) and Lesson 02 (Nodal Analysis)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Mesh | A loop of the drawing with nothing inside it; one "window pane" | One pane in a window frame |
| Mesh current | An imagined current that circles around one mesh, always in the same direction | A toy train running around one small track |
| Planar circuit | A circuit you can draw on paper with no wires crossing | A city map with no bridges or tunnels |
| Shared branch | A branch that belongs to two meshes at once (the wire between two window panes) | The wooden bar between two panes, touched by both |
| Resistance matrix | The table of numbers in mesh analysis: resistance around each mesh and resistance shared between meshes | A table of how much each pair of tracks share |
| Clockwise | Turning the same way as the hands of a clock | |
| Supermesh | Two meshes that share a current source, merged for KVL | Two rooms with a turnstile between them, counted as one big room |
| Source transformation | Swapping a current source with a parallel resistor for a voltage source with a series resistor (or back), without changing what the rest of the circuit sees | Swapping a tap for a tank of the right height and pipe |

## Learning Objectives

- Identify the meshes of a planar circuit and assign one clockwise mesh current to each.
- Write the current in a shared branch as the difference of two mesh currents.
- Write KVL around each mesh with Ohm's law, and collect the equations into `R i = v`.
- Build the resistance matrix by inspection: sum around the mesh on the diagonal, minus shared resistance off the diagonal.
- Handle a current source on an outer edge (a known mesh current) and know when you need a supermesh.
- Implement a mesh solver in NumPy and check it against our simulator.

## The Problem

Nodal analysis (Lesson 02) chose node voltages as unknowns and needed only KCL. There is a mirror-image method that chooses *currents* as unknowns and needs only KVL. Why learn both?

- Some circuits have few loops but many nodes: a long chain of resistors in series with a couple of sources. Nodal analysis needs one unknown per node; mesh analysis needs one per window, which can be far fewer.
- Many textbook problems, exam questions and older engineering notes use mesh currents. You should be able to read them.
- Mesh analysis makes you think in *currents circulating in loops*, which is exactly how power engineers think about current returning to its source and how PCB designers think about "current loops" that radiate noise (Phase 21).

Here is the scenario that makes it natural. Two batteries (say a 9 V battery and a 3 V coin cell) feed a network of three resistors. You want to know the current through the resistor between them. Two windows, two unknowns, done.

## The Physics

Physically, there is no such thing as a "mesh current". Electrons in a wire do not know which window they belong to. So why does the method work?

Look at any branch of a planar circuit. It is either on the outside edge of the drawing (it belongs to exactly one window) or between two windows (it belongs to exactly two). Now imagine each window has its own circulating current. In an outside branch, the real current equals that window's current. In a shared branch, the two circulating currents pass through in opposite directions (one going down, its neighbour going up, if both circulate clockwise), so the real current is their *difference*.

And here is the beautiful part: **KCL is then automatically true at every node.** Each mesh current enters a node and leaves it again (it is a closed circle), so it contributes zero net current to every node it touches. Add up any number of such circles and every node still balances. So mesh analysis builds KCL in, exactly as nodal analysis built KVL in. What remains is KVL around each window: the energy rises (batteries) must equal the energy drops (resistors), which is energy conservation (Phase 01, Lesson 04).

What the "toy train" picture gets wrong: real current in a shared branch is one single flow, not two trains passing through each other. The mesh currents are bookkeeping, a clever choice of unknowns, not physical objects.

## The Concept

### The recipe

```
1. Check the circuit is planar (drawn with no crossings).
2. Find the windows (meshes). Give each a mesh current, all clockwise.
3. For each mesh, walk around clockwise and write KVL:
     sum of battery rises along the walk = sum of resistor drops
   A resistor drop is R x (this mesh current - neighbour mesh current)
   if the resistor is shared, or R x (this mesh current) if not.
4. Solve. Real branch currents are mesh currents (outer branches)
   or differences of mesh currents (shared branches).
```

Choosing *all* clockwise is not required, but it makes the pattern below work every time.

### First example: two batteries, two windows

```
        a     R1 = 1 kΩ      b      R3 = 1 kΩ      c
   ┌────●────/\/\/\/\────────●────/\/\/\/\────────●────┐
   │                         │                         │
  +│        ⟳ i1             │          ⟳ i2          +│
 [V1] 9 V                 [R2] 2 kΩ                 [V2] 3 V
  -│                         │                        -│
   │                         │                         │
   └─────────────────────────┴─────────────────────────┘
                            gnd
```

Two windows: the left one (V1, R1, R2) with mesh current `i1`, and the right one (R2, R3, V2) with mesh current `i2`. Both clockwise.

**Mesh 1, walking clockwise** from the bottom-left corner: up through V1 from its minus to its plus side (a rise of 9 V), right through R1 (a drop of `1 × i1`), down through R2. In R2, mesh 1 flows down and mesh 2 flows up, so the real downward current is `i1 - i2`, and the drop is `2 × (i1 - i2)`. Back to the start. KVL:

```
9 = 1 × i1 + 2 × (i1 - i2)
9 = 3 i1 - 2 i2
```

**Mesh 2, walking clockwise** from the bottom of R2: up through R2 (here mesh 2 flows up, so from mesh 2's point of view the current is `i2 - i1`, drop `2 × (i2 - i1)`), right through R3 (drop `1 × i2`), down through V2 from its plus side to its minus side. Going from plus to minus is a *drop* of 3 V. KVL (rises = drops, and there are no rises in this walk):

```
0 = 2 × (i2 - i1) + 1 × i2 + 3
-3 = -2 i1 + 3 i2
```

In kΩ, mA and V, the two equations are:

```
 3 i1 - 2 i2 =  9
-2 i1 + 3 i2 = -3
```

### Solve by elimination

Multiply the first equation by 3 and the second by 2, then add them so `i2` cancels:

```
 9 i1 - 6 i2 =  27
-4 i1 + 6 i2 =  -6
---------------------
 5 i1        =  21      so  i1 = 4.2 mA
```

Back into the first: `3 × 4.2 - 2 i2 = 9`, so `12.6 - 9 = 2 i2`, `i2 = 1.8 mA`.

Now the real branch currents:

- R1 (outer, only mesh 1): 4.2 mA from a to b.
- R3 (outer, only mesh 2): 1.8 mA from b to c, and on through V2 into its plus side. So the 9 V battery is *charging* the 3 V battery. (A real coin cell may not like that; Phase 06 will explain why.)
- R2 (shared): `i1 - i2 = 4.2 - 1.8 = 2.4 mA` downward.

Node b: `vb = 2 kΩ × 2.4 mA = 4.8 V`. Check by KCL at b: in 4.2 mA, out 2.4 + 1.8 = 4.2 mA. It balances, as it must.

### The pattern: resistance matrix by inspection

Write the system as a matrix:

```
       i1        i2          right side
m1 [ 1 + 2      -2    ]     [  9 ]
m2 [  -2       2 + 1  ]     [ -3 ]
```

It mirrors the nodal pattern:

- **Diagonal (row m1, column m1):** the total resistance around mesh 1 (`R1 + R2 = 3 kΩ`).
- **Off-diagonal (row m1, column m2):** minus the resistance shared by mesh 1 and mesh 2 (`-R2 = -2 kΩ`). Zero if they share nothing.
- **Right side of row m1:** the sum of source voltages that push current clockwise around mesh 1 (a rise when you walk clockwise counts plus; a drop counts minus).

Written short: `R i = v`. Read it: "resistances times loop currents equal the source voltages around each loop". Ohm's law (`V = R I`) for the whole network, the mirror of `G v = i`.

The minus signs on the off-diagonal appear only because all meshes go clockwise: in a shared branch, two clockwise currents always pass in opposite directions.

### Current sources: the easy case and the hard case

Our workhorse from Lessons 01 and 02 has a current source:

```
        a      R1 = 1 kΩ      b      R3 = 3 kΩ      c
   ┌────●────/\/\/\/\────●────/\/\/\/\────●──────────┐
   │                     │                 │          │
 [V1] 12 V   ⟳ i1      [R2] 2 kΩ  ⟳ i2   [R4] 1 kΩ ⟳ i3 (I1) 1 mA up
   │                     │                 │          │
   └─────────────────────┴─────────────────┴──────────┘
```

Three windows. The third window is bounded by R4 and the current source I1 only, and I1 is on the *outside* edge. The only mesh current flowing through I1 is `i3`. So `i3` is not unknown: it is set by I1. Clockwise in window 3 means *down* the right edge, while I1 pushes 1 mA *up*. So `i3 = -1 mA`.

**The easy case:** a current source on an outer edge simply fixes one mesh current. One fewer unknown.

Now write KVL for meshes 1 and 2, as before:

```
mesh 1:  12 = 1 × i1 + 2 × (i1 - i2)                 →  3 i1 - 2 i2 = 12
mesh 2:   0 = 2 × (i2 - i1) + 3 × i2 + 1 × (i2 - i3)  → -2 i1 + 6 i2 = i3 = -1
```

The R4 term `1 × (i2 - i3)` is the shared-branch rule again, and the known `i3` moved to the right side. By substitution: from the first, `i1 = (12 + 2 i2) / 3 = 4 + 0.6667 i2`. Into the second: `-8 - 1.3333 i2 + 6 i2 = -1`, so `4.6667 i2 = 7`, `i2 = 1.5 mA`, and `i1 = 4 + 1 = 5 mA`.

Branch currents: R1 carries 5 mA, R2 carries `5 - 1.5 = 3.5 mA` down, R3 carries 1.5 mA, R4 carries `i2 - i3 = 1.5 - (-1) = 2.5 mA` down. Exactly the answers of Lessons 01 and 02. Three methods, one circuit, one truth.

**The hard case:** a current source on a *shared* branch, between two windows. Then it does not fix one mesh current; it fixes their *difference* (`i_left - i_right = I_source`), and the voltage across it is unknown. The fix, called a **supermesh**, is to write KVL around the big loop formed by both windows *skipping* the current source branch, and use `i_left - i_right = I_source` as the second equation. It works, but again it needs a human to spot it. Lesson 04's modified nodal analysis never needs such tricks, which is one reason simulators use it.

### Another trick: source transformation

A current source `I` with a resistor `R` in parallel behaves, for the rest of the circuit, exactly like a voltage source `V = I × R` with the same resistor `R` in series. In the workhorse, I1 (1 mA) in parallel with R4 (1 kΩ) can be replaced by a 1 V battery in series with 1 kΩ. Then the circuit has only voltage sources and two meshes, and you get the same 3 i1 - 2 i2 = 12, -2 i1 + 6 i2 = -1. Lesson 06 proves why this works.

### Nodal or mesh?

| Situation | Better choice |
|---|---|
| Many components in series, few nodes in total | Mesh |
| Many components in parallel, many loops | Nodal |
| Current sources | Nodal (they go straight to the right side) |
| Voltage sources | Mesh (they go straight to the right side) |
| Circuit cannot be drawn without crossings (non-planar) | Nodal only; meshes are not defined |
| Writing a simulator | Nodal, extended (Lesson 04) |

## Build It

`code/main.py` describes each mesh as a list of the elements it walks through, builds the resistance matrix from that description, solves it, and compares the branch currents with `sim`.

### Step 1: describe meshes by what they walk through

Each mesh is a list of `(element, direction)`. Direction `+1` means the clockwise walk goes through the element from its first node to its second; `-1` means the other way. For a voltage source, the first node is its plus side, so walking through it with direction `-1` (minus to plus) is a rise.

```python
two_battery = {
    "resistors": {"R1": ("a", "b", 1000), "R2": ("b", "0", 2000), "R3": ("b", "c", 1000)},
    "sources": {"V1": ("a", "0", 9.0), "V2": ("c", "0", 3.0)},
    "meshes": {
        "m1": [("V1", -1), ("R1", +1), ("R2", +1)],
        "m2": [("R2", -1), ("R3", +1), ("V2", +1)],
    },
    "known": {},
}
```

### Step 2: build R and v

For every resistor, look at every pair of meshes that pass through it. If both walk it the same way, they add (`+R`); if opposite ways, they subtract (`-R`). That one rule produces both the diagonal sums and the negative off-diagonals.

```python
def mesh_system(circuit):
    names = [m for m in circuit["meshes"] if m not in circuit["known"]]
    index = {m: k for k, m in enumerate(names)}
    resistance = np.zeros((len(names), len(names)))
    sources = np.zeros(len(names))
    for row_mesh, walk in circuit["meshes"].items():
        if row_mesh not in index:
            continue
        row = index[row_mesh]
        for element, direction in walk:
            if element in circuit["sources"]:
                sources[row] -= direction * circuit["sources"][element][2]
                continue
            ohms = circuit["resistors"][element][2]
            for other_mesh, other_walk in circuit["meshes"].items():
                for other_element, other_direction in other_walk:
                    if other_element != element:
                        continue
                    term = direction * other_direction * ohms
                    if other_mesh in index:
                        resistance[row, index[other_mesh]] += term
                    else:
                        sources[row] -= term * circuit["known"][other_mesh]
    return names, resistance, sources
```

A source walked with direction `-1` (minus to plus) adds its volts to the right side: a rise.

### Step 3: branch currents from mesh currents

The real current in an element (in its own first-to-second direction) is the sum of `direction × mesh current` over the meshes that walk through it.

```python
def branch_current(circuit, mesh_currents, element):
    return sum(direction * mesh_currents[mesh]
               for mesh, walk in circuit["meshes"].items()
               for name, direction in walk if name == element)
```

### Step 4: compare with the simulator

The same circuit is built with `sim.Circuit`, and the code prints our mesh currents, our branch currents and the simulator's `r.i(...)` side by side. For the workhorse, mesh m3 is listed under `"known"` with -1 mA.

The code also solves the source-transformed workhorse (1 V battery in series with R4). Look at its output carefully: node b and node c come out exactly as before (7 V and 2.5 V), and so do the currents in R1, R2 and R3. But the current in the transformed R4 is 1.5 mA, not 2.5 mA. A source transformation keeps everything *outside* the swapped pair identical; what happens *inside* the pair is different. Keep that in mind when you use it.

## Use It

- **Power distribution.** A battery feeding a motor through long cables is one big mesh. The cable resistance (a few milliohms per meter) shows up on the diagonal; the motor's resistance next to it. Engineers estimate voltage loss in cables exactly like this.
- **Current loops and noise.** In PCB design (Phase 21), every signal current returns to its source through ground. The *area* of that loop decides how much it radiates or picks up interference. Thinking in mesh currents is thinking in loops.
- **Kelvin (four-wire) measurement.** To measure a 1 mΩ shunt resistor, instruments force current through one mesh and sense voltage through another, so the wire resistance in the forcing mesh does not spoil the reading. You will meet this in Phase 06.
- **Exam-style hand analysis.** Datasheets of op-amps and regulators often show "typical application" circuits with two or three loops. Mesh analysis gets you the currents in a few lines.

## Try It in the Lab

The lab board is the two-battery circuit of this lesson: a 9 V battery on the left, a 3 V battery on the right, 1 kΩ resistors from each battery to the middle node b, and an empty slot from b to ground. Pick the resistor for the slot so that the current through the right resistor (from b toward the 3 V battery) is between 1.6 and 2.0 mA.

Things to think about:

- If the slot were a short (0 Ω), node b would be at ground. Which way would current flow in the right resistor then?
- If the slot were an open (nothing), what single loop is left, and what current flows?
- Write the 2×2 resistance matrix with the slot as `Rs`. Which entries depend on `Rs`?

## Common Mistakes

- **Mixing clockwise and counter-clockwise.** If one mesh goes the other way, the off-diagonal sign flips. Allowed, but it breaks the by-inspection pattern. Stay clockwise.
- **Getting battery signs backwards.** Walking from minus to plus is a rise (positive on the right side); plus to minus is a drop. Mark the plus side on every battery before you start.
- **Using the mesh current as the branch current in a shared branch.** The real current there is the difference of the two mesh currents.
- **Trying meshes on a non-planar circuit.** If you cannot draw it without crossings, "the windows" do not exist. Use nodal analysis.
- **Writing KVL through a current source.** The voltage across a current source is unknown. Either its mesh current is known (outer edge) or you need a supermesh.

## Exercises

1. In the two-battery circuit, swap V2 for a 9 V battery (same orientation). Write the resistance matrix and solve. What current flows in R3 now, and in which direction? (Hint: by symmetry, think before you compute.)
2. Change R2 to 1 kΩ in the two-battery circuit. Solve for i1 and i2 by hand and check vb. (Answer: vb = 4 V.)
3. A single loop has a 12 V battery and resistors of 1, 2 and 3 kΩ in series. Mesh analysis gives a 1×1 "matrix". What is it, and what is the current?
4. Three windows in a row: a 10 V battery on the far left, and three shared/outer resistors as follows: R1 = 1 kΩ (outer, top of mesh 1), Ra = 1 kΩ (shared 1-2), R2 = 1 kΩ (outer, top of mesh 2), Rb = 1 kΩ (shared 2-3), R3 = 1 kΩ (outer, top of mesh 3), R4 = 1 kΩ (right edge of mesh 3). Write the 3×3 resistance matrix by inspection and solve with NumPy.
5. Harder: move the workhorse's 1 mA current source so it sits *in series with R3* (between b and c, pointing toward c), and remove R3. Draw it: is the source on an outer edge or on a branch shared by two windows? Decide whether you need a supermesh, then solve. Confirm with `sim`.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Mesh analysis | "Loop currents" | KVL around every window of a planar circuit, with one circulating current per window as the unknowns |
| Mesh current | "The current in the loop" | A bookkeeping current; real branch currents are one mesh current or a difference of two |
| Resistance matrix | "The R matrix" | Diagonal: total resistance around a mesh; off-diagonal: minus the shared resistance |
| Planar | "Flat" | Drawable without crossings; required for meshes to exist |
| Supermesh | "Skip the current source" | KVL around two meshes merged, plus an equation saying their difference equals the source current |
| Source transformation | "Swap I for V" | A current source with parallel R is equivalent to a voltage source `I × R` with series R |

## Further Reading

- [All About Circuits, Vol. I, "Mesh Current Method"](https://www.allaboutcircuits.com/textbook/direct-current/chpt-10/mesh-current-method/): a free, step-by-step treatment with several examples.
- *Practical Electronics for Inventors*, Scherz and Monk, 4th edition, Chapter 2: network theorems and loop methods.
- Agarwal and Lang, *Foundations of Analog and Digital Electronic Circuits* (the MIT 6.002 textbook), Chapter 3: node and loop methods side by side.
- [Khan Academy, Electrical Engineering, circuit analysis methods](https://www.khanacademy.org/science/electrical-engineering/ee-circuit-analysis-topic): videos on the mesh current method.
