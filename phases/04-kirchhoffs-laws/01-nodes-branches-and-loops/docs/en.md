# Nodes, Branches and Loops

> Before you can apply any law to a circuit, you have to see its shape: which points are really the same point, which parts sit between them, and which closed paths go around.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 02 (Your First Circuits), especially Lesson 01 (The Closed Loop) and Lesson 04 (Series and Parallel Intuition); Phase 03 (Resistance and Ohm's Law), especially Lesson 03 (Ohm's Law)
**Time:** ~50 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Topology | The shape of the connections in a circuit: what is joined to what, ignoring lengths, angles and positions on the page | A subway map: it shows which stations connect, not how far apart they really are |
| Wire segment | One drawn line in a schematic, from one corner or dot to the next | One piece of pipe between two fittings |
| Node | Every point that is joined by plain wire, counted as one single place, no matter how many drawn lines it uses | A town square: you can draw several streets inside it, but it is still one square |
| Element (component) | One part with two ends: a battery, a resistor, a lamp, a switch | One house on a street |
| Branch | One element (or a chain that we choose to treat as one) that connects two nodes | A bridge between two islands |
| Loop | Any closed path you can walk through branches and come back to where you started without visiting a node twice | A walk around the block that ends at your front door |
| Mesh | A loop that has no other branch inside it; one "window" of a flat drawing | One pane of a window frame |
| Independent loop | A loop that contains at least one branch no earlier loop used, so it brings new information | A new street in your walk you have never walked before |
| Ground (reference node) | The one node we agree to call 0 volts, so every other node's voltage is measured from it | Sea level: heights of mountains are measured from it |
| Netlist | A plain text list of every element and the two nodes it connects | A guest list that says who sits next to whom |
| Spanning tree | A set of N - 1 branches that reaches every node without making any loop | The minimum set of bridges you need so that every island is reachable |

## Learning Objectives

- Tell a node from a wire segment, and count the nodes of any schematic correctly even when it is drawn with many lines.
- Identify the branches of a circuit and write it as a netlist.
- Find loops and meshes in a drawing, and explain the difference between them.
- Use the formula L = B - N + 1 to count how many independent loops a circuit has, and say why it works.
- Pick a ground node and explain what choosing it does and does not change.

## The Problem

In Phase 03 every circuit had one battery and one or two resistors, and Ohm's law (V = I × R) was enough. Real circuits do not look like that. Open any gadget's schematic and you see dozens of parts, wires crossing, dots, little ground symbols in five different places. Next lesson you will learn Kirchhoff's current law, which you apply *at each node*. The lesson after that, Kirchhoff's voltage law, which you apply *around each loop*. If you miscount the nodes or the loops, you will write the wrong number of equations: too few and you cannot solve the circuit, too many and you will waste time (or, worse, trust a redundant equation as if it were new information).

Here is the classic beginner trap. Look at this drawing:

```
   p1 ───── p2 ──[ R1 ]── p3 ───── p4
   |                                |
  [B1]                            [ R2 ]
   |                                |
   p6 ──────────── gnd ──────────── p5
```

It has eight named points. A beginner might say "eight nodes". But p1 and p2 are joined by a bare wire, so they are electrically the same place. So are p3 and p4. And p5, gnd and p6 are all one long wire. This circuit has only **three** nodes. Getting that right is what this lesson is about.

## The Physics

Why is a stretch of wire "one point"? Recall from Phase 01 that voltage is energy per unit of charge, and from Phase 03 (Lesson 02, Resistivity and Wires) that a copper wire has a very small resistance: a 10 cm hookup wire has around 0.002 ohms (Ω). By Ohm's law, the voltage difference between the two ends of that wire, carrying even 0.1 amperes (A), is

```
V = I × R = 0.1 A × 0.002 Ω = 0.0002 V = 0.2 mV
```

That is tiny compared with the volts we care about. So in a schematic we make a deliberate simplification: **a drawn wire has zero resistance**, which means zero voltage difference from one end to the other. Every point along it sits at the same voltage. That is the physical reason a whole tangle of drawn wire collapses into one node: a node is a set of points that all share one voltage.

Elements are different. Across a resistor, a battery or a lamp the voltage *can* change, because charges gain or lose energy there. So elements are the "interesting" places, and nodes are the "boring" places between them where nothing happens. Topology is just the bookkeeping of which interesting places touch which boring places.

What the zero-resistance-wire idea gets wrong: real wires do have a little resistance, and at high currents (car starter cables, hundreds of amperes) or very long runs (house wiring, 30 m) the voltage drop along a wire matters. In those cases you draw the wire's resistance as its own little resistor, and then it becomes a branch like any other.

## The Concept

### Nodes: merge everything joined by plain wire

The rule: start at any point, and follow bare wire in every direction (through corners, through dots, along any line) without passing through an element. Everything you can reach is one node. Then start somewhere you have not visited and repeat.

Two details about drawings:

```
     |                    |
  ───●───   joined     ───┼───   NOT joined (crossing without a dot,
     |                    |       in most modern schematics)
```

A dot means wires connect. Two lines crossing without a dot normally mean they just pass over each other. When in doubt, look for the dot.

And the ground symbol:

```
    |
   ─┴─
    ─      every one of these symbols on a page is the SAME node
     ·
```

If a schematic has five ground symbols, all five are one node, as if an invisible wire joined them.

### Branches: the elements between nodes

Once you know the nodes, list each element and the two nodes its ends touch. That list is the **netlist**. For the drawing in The Problem:

```
B1   between node p1 and node gnd
R1   between node p1 and node p3
R2   between node p3 and node gnd
```

Three branches, three nodes. Notice we gave each node one name (p1, p3, gnd) even though the drawing had several names for it. Every circuit simulator, including the one you will build in Phase 05, starts from a netlist exactly like this.

### Loops and meshes

A loop is a closed walk: leave a node through a branch, keep going through branches, come back to the start, never visiting a node twice on the way. In the three-node circuit there is exactly one loop: p1 → R1 → p3 → R2 → gnd → B1 → p1.

Now a bigger example, a **ladder**:

```
   vcc ──[ R1 ]── a ──[ R3 ]── b
    |             |            |
   [B1]          [R2]         [R4]
    |             |            |
   gnd ────────── gnd ──────── gnd
```

Nodes: vcc, a, b, and gnd (the whole bottom line is one node). So N = 4.
Branches: B1, R1, R2, R3, R4. So B = 5.

Loops you can find by eye:

```
Loop A (left window):   vcc → R1 → a → R2 → gnd → B1 → vcc
Loop B (right window):  a → R3 → b → R4 → gnd → R2 → a
Loop C (outside edge):  vcc → R1 → a → R3 → b → R4 → gnd → B1 → vcc
```

Loops A and B are **meshes**: each is one window of the drawing, with no branch inside. Loop C goes around the outside; it has R2 inside it, so it is a loop but not a mesh.

### Why Loop C brings nothing new

Next lessons will turn each loop into an equation. Is Loop C a third independent equation? No. Every branch in Loop C already appears in A or in B. In fact, walking A and then B, the branch R2 is walked once downward (in A) and once upward (in B), and those two walks cancel. What is left is exactly Loop C. So C = A + B, and an equation from C would just be the sum of the equations from A and B. It is redundant.

So the question "how many loops?" really means "how many *independent* loops?", and for that there is a neat formula.

### The formula L = B - N + 1

Read it out loud: *the number of independent loops equals the number of branches, minus the number of nodes, plus one.*

Where does it come from? Build the circuit one branch at a time.

1. Start with the N nodes as separate dots and no branches.
2. To connect N dots into one piece, without making any closed path, you need exactly N - 1 branches. (Two dots need one link. Three dots need two. Each new link connects one new dot.) Such a set of branches is called a **spanning tree**: it spans (reaches) every node, and like a tree it has no loops.
3. Every branch you add beyond those N - 1 joins two nodes that were already connected, so it closes a brand-new loop, and that loop contains a branch (the new one) that no earlier loop had. So each extra branch adds exactly one independent loop.

Number of extra branches = B - (N - 1) = B - N + 1. That is L.

Check it on our examples:

```
one battery, one resistor:   B = 2, N = 2   → L = 2 - 2 + 1 = 1
the three-node drawing:      B = 3, N = 3   → L = 3 - 3 + 1 = 1
the ladder:                  B = 5, N = 4   → L = 5 - 4 + 1 = 2
```

The ladder has 2 independent loops, matching our discovery that Loop C was the sum of A and B. For a flat drawing (no wires crossing), the number of meshes always equals L, which is why counting windows is such a handy shortcut.

The formula assumes the whole circuit is one connected piece. If you had two separate circuits on one page, you would apply it to each piece separately.

### A harder one: the bridge

```
            top
          /     \
       [R1]     [R2]
        /         \
     left ─[R5]─ right
        \         /
       [R3]     [R4]
          \     /
            gnd
   (and battery B1 from top down to gnd, drawn at the side)
```

Nodes: top, left, right, gnd. N = 4.
Branches: B1, R1, R2, R3, R4, R5. B = 6.
L = 6 - 4 + 1 = **3**.

Can you see three windows? Top triangle (R1, R5, R2), bottom triangle (R3, R5, R4), and the window between the battery and the diamond (B1, R1, R3 for example). Three meshes, three independent loops. Notice this circuit is not a simple mix of series and parallel. You will meet it properly in Lesson 07 (The Wheatstone Bridge), and it is the reason we need Kirchhoff's laws at all.

### Choosing ground

Voltage is always a *difference* between two points (Phase 01, Lesson 06). To give each node a single number, we pick one node, call it ground, and say it is 0 V. Every other node's voltage is then "how many volts above ground".

Worked example: a 9 V battery between vcc and gnd, with R1 = 1 kΩ and R2 = 2 kΩ in series. The current is 9 V / 3000 Ω = 3 mA, so R2 has 3 mA × 2000 Ω = 6 V across it.

```
ground = gnd (bottom):   v(gnd) = 0 V,  v(mid) = 6 V,  v(vcc) = 9 V
ground = mid instead:    v(gnd) = -6 V, v(mid) = 0 V,  v(vcc) = 3 V
```

Every voltage *difference* is the same in both choices (vcc minus gnd is 9 V either way). Ground is a bookkeeping choice, like choosing sea level. The usual choice is the battery's minus terminal, or the node with the most connections, because it makes the most voltages positive and simple.

What the "sea level" picture gets wrong: in real equipment, "ground" may also mean a physical connection to the earth through the third pin of a wall plug, for safety. In schematics in this course, ground only means "the node we call zero".

## Build It

The code in `code/main.py` takes a netlist with wires in it, merges the wires into nodes, counts N, B and L, and even finds the independent loops for you. Run it:

```
uv run python phases/04-kirchhoffs-laws/01-nodes-branches-and-loops/code/main.py
```

### Step 1: A netlist with wire segments

Each line is `(kind, name, end_a, end_b)`. Wires are listed like any other element, so the code has to discover that they merge points.

```python
drawn_with_many_wires = [
    ("battery", "B1", "p1", "p6"),
    ("wire", "W1", "p1", "p2"),
    ("resistor", "R1", "p2", "p3"),
    ("wire", "W2", "p3", "p4"),
    ("resistor", "R2", "p4", "p5"),
    ("wire", "W3", "p5", "gnd"),
    ("wire", "W4", "p6", "gnd"),
]
```

This is exactly the eight-point drawing from The Problem.

### Step 2: Merge wire segments into nodes

We use a classic trick called *union-find*. Each point starts as its own group, pointing at itself. Each wire says "these two groups are the same group", so we point one group's leader at the other's. At the end, two points are the same node if following the pointers leads to the same leader. We prefer "gnd" as a leader so the ground node keeps its familiar name.

```python
def find(parent, name):
    while parent[name] != name:
        parent[name] = parent[parent[name]]
        name = parent[name]
    return name


def merge_wire_segments(netlist):
    parent = {}
    for kind, name, end_a, end_b in netlist:
        parent.setdefault(end_a, end_a)
        parent.setdefault(end_b, end_b)
    for kind, name, end_a, end_b in netlist:
        if kind == "wire":
            root_a, root_b = find(parent, end_a), find(parent, end_b)
            if root_a != root_b:
                keep, drop = sorted([root_a, root_b], key=lambda point: (point != "gnd", point))
                parent[drop] = keep
    return {point: find(parent, point) for point in parent}
```

### Step 3: Count N, B and L

Branches are every non-wire element, rewritten in terms of merged nodes.

```python
def count_topology(netlist):
    node_of = merge_wire_segments(netlist)
    nodes = sorted(set(node_of.values()))
    branches = branches_of(netlist, node_of)
    loops = len(branches) - len(nodes) + 1
    return nodes, branches, loops
```

For the eight-point drawing the program prints that gnd is made of the points gnd, p5 and p6, that p1 includes p2, that p3 includes p4, and finally N = 3, B = 3, L = 1.

### Step 4: Find the independent loops with a spanning tree

This is the derivation of L = B - N + 1 turned into code. Starting from ground, a breadth-first search walks outward and keeps the first branch that reaches each new node: those N - 1 branches form the spanning tree. Every branch left over closes one loop: walk from one of its ends up the tree to where the two ends' paths meet, then down to the other end.

```python
def fundamental_loops(nodes, branches, root):
    came_from, tree_branches = spanning_tree(nodes, branches, root)
    loops = []
    for name, node_a, node_b in branches:
        if name in tree_branches:
            continue
        path_a = path_to_root(came_from, node_a)
        path_b = path_to_root(came_from, node_b)
        meeting = next(node for node in path_a if node in path_b)
        up = path_a[: path_a.index(meeting) + 1]
        down = list(reversed(path_b[: path_b.index(meeting)]))
        loops.append((name, up + down + [node_a]))
    return tree_branches, loops
```

For the ladder the output is:

```
a spanning tree uses branches ['B1', 'R2', 'R4'] (3 = N - 1 branches)
  adding  R1 closes the loop vcc -> gnd -> a -> vcc
  adding  R3 closes the loop a -> gnd -> b -> a
```

Read the first loop: from vcc down through B1 to gnd, up through R2 to a, and back to vcc through R1. That is the left window. The second is the right window, except it uses R2 and R4 through ground: from a down R2 to gnd, up R4 to b, back through R3. Different but equally valid choice of two independent loops.

For the bridge the program finds three loops, matching L = 6 - 4 + 1 = 3.

### Step 5: The summary table

```
  circuit        N   B   L
  single         2   2   1
  many wires     3   3   1
  ladder         4   5   2
  bridge         4   6   3
```

Check each row by hand with B - N + 1.

## Use It

- **Every circuit simulator** (SPICE, LTspice, KiCad's simulator, the `sim/` package we build in Phase 05) reads a netlist. When you draw a schematic in KiCad, the program does exactly Step 2: it merges every wire, label and ground symbol into "nets" (KiCad's word for nodes) and writes a netlist file. Our union-find is the same idea.
- **Printed circuit boards** (Phase 21) are drawn from the netlist. A net is one node; the board software checks that every pad on the same net is connected by copper and that no two nets touch. A "short" in a board is literally two nodes accidentally merged.
- **Ground symbols** on real schematics often come in flavours: a plain ground, a chassis ground and an analog ground (AGND) versus digital ground (DGND). Each different symbol is a different node until a designer deliberately connects them, usually at one point.
- **How many equations**: in Phase 05 you will solve circuits with nodal analysis (one equation per node except ground, so N - 1 equations) or mesh analysis (one per independent loop, so L equations). Knowing N and L ahead of time tells you which method is less work. For the bridge: nodal needs 3 equations, mesh needs 3. For a long ladder with 10 rungs, both grow, but you will see how to pick.

## Common Mistakes

- **Counting wire corners as nodes.** A corner in a drawn wire is not a node. Only places separated by elements are different nodes. Always merge first, then count.
- **Treating every ground symbol as a different node.** All identical ground symbols are one node. Forgetting this makes you think a circuit is "open" when it is not.
- **Calling a crossing a connection.** Two wires that cross without a dot are not joined (in modern schematics). Older drawings sometimes used a little hump, a "hop", to make crossings unmistakable.
- **Counting every loop you see as independent.** The outer loop of a ladder is real, but it is the sum of the inner windows. Use L = B - N + 1 to know how many you need.
- **Thinking ground is "where the current goes".** Ground is just the reference for measuring voltage. Current flows around loops and comes back to the battery; it does not disappear into ground.
- **Forgetting the battery is a branch.** Sources are elements with two ends too. Leave the battery out and B is wrong by one, so L is wrong by one.

## Exercises

1. A schematic has a 9 V battery and three resistors all in a single ring, drawn with 10 corners. How many nodes, branches and independent loops does it have?
2. A battery has three resistors connected directly across it, side by side (all three between the same top node and the same bottom node). Find N, B and L. Draw the meshes and check that their count equals L.
3. Write a netlist (in the format of `code/main.py`) for this circuit and run it through `count_topology`: a battery from vcc to gnd, R1 from vcc to a, R2 from a to gnd, R3 from a to gnd, R4 from vcc to gnd. Before running, predict N, B and L.
4. Using the ladder from the lesson, set the battery to 12 V and suppose node voltages (with gnd as ground) are v(vcc) = 12 V, v(a) = 4 V, v(b) = 1 V. Now choose node a as ground instead. Write the new voltage of every node. Which voltage differences changed?
5. (Harder) A cube made of 12 resistors, one on each edge, with a battery connected between two opposite corners. Count the nodes and branches and compute L. Then write its netlist (call the corners c0 to c7) and let `fundamental_loops` list the independent loops for you. Does the count match?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Node | "Each dot in the drawing" | A set of points all joined by plain wire, so all at the same voltage; one node can be drawn with many lines and dots |
| Branch | "A wire" | A two-ended element (source, resistor, lamp) connecting two nodes; wires themselves are not branches |
| Loop | "Any circle in the drawing" | A closed path through branches that visits no node twice |
| Mesh | "Same as loop" | A loop with no branch inside it, one window of a flat drawing |
| Independent loops | "All the loops" | L = B - N + 1 loops, each containing a branch the others do not, so each gives new information |
| Ground | "Where electricity goes away" | The node we choose to call 0 V so other voltages have a reference |
| Netlist | "The schematic" | The text list of elements and the nodes they connect; the schematic is just a drawing of it |

## Further Reading

- *All About Circuits*, Volume I (DC), chapter "Series and Parallel Circuits" and the network analysis chapter: free online textbook with clear pictures of nodes and loops.
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 1: the classic reference, terse but practical about how real engineers read schematics.
- MIT OpenCourseWare 6.002 *Circuits and Electronics* (Anant Agarwal), early lectures on the lumped circuit abstraction: explains why we can treat wires as ideal and circuits as graphs.
- KiCad documentation, the "Eeschema" schematic editor manual: see how a real tool turns wires, labels and ground symbols into nets.
