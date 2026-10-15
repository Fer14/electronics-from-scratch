# The Breadboard

> A breadboard is a schematic you can push your fingers into. Every hole belongs to a hidden strip of metal; know the strips and you know the circuit.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 00 (Words and Units), Lesson 05 (Reading a Schematic); Phase 02 (Your First Circuits), Lessons 01-04
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| breadboard (solderless) | a plastic block full of holes, with spring metal clips underneath that grab and connect the legs of parts | a pegboard where pegs in the same short row are secretly tied together |
| tie point | one hole of the breadboard | one seat on a bench |
| terminal strip | a group of 5 holes in one row joined by one metal clip | five seats on the same bench: whoever sits there is together |
| power rail (bus) | a long strip of holes along the edge, joined end to end, for the supply | a corridor that runs the whole length of a building, with doors into every room |
| centre gap (ravine) | the groove down the middle that separates the left and right halves of each row | the aisle in a bus between the left and right seats |
| jumper wire | a short wire with bare ends used to join two holes | a bridge between two islands |
| net | everything that is electrically connected together, wherever it physically is | one family, even if the members live in different houses |
| lead (pronounced "leed") | the metal leg of a component | the legs of a table |
| anode / cathode | the two legs of an LED: anode is the plus side (long leg), cathode is the minus side (short leg, flat edge on the body) | the in-door and out-door of a one-way turnstile |
| union-find | a small computer trick for grouping things that are connected | merging friend groups whenever two people turn out to know each other |

## Learning Objectives

- Draw from memory how the holes of a breadboard are connected underneath: rows of five on each side of the centre gap, and the long power rails.
- Translate a schematic into breadboard placements, and a breadboard photo back into a schematic, by thinking in nets instead of holes.
- Spot the three classic mistakes on sight: both legs of a part in the same strip (part shorted out), a missing link back to the supply (open loop), and a wire bridging the plus and minus rails (short circuit).
- Write a Python model of a breadboard that groups holes into nets with union-find and automatically reports shorted parts and open loops.

## The Problem

Up to now our circuits have been drawings and descriptions. To build one for real you need some way to hold the parts and join their legs. You could twist wires together (they come loose), or solder them (permanent, hot, and slow to change). In the early 1970s an engineer called Ronald Portugal designed a better idea for prototyping: a plastic block with rows of holes and springy metal clips inside. Push a leg in and the clip grabs it. Pull it out and it is free again. Nearly every electronics hobbyist and student since has used one.

The name is older. In the 1920s radio amateurs literally built their sets on wooden boards used for slicing bread, hammering nails into the wood and wrapping wires round them. The board was cheap, flat, and in every kitchen. "Breadboarding a circuit" still means building a quick test version.

The catch is that the board is a *hidden* circuit. Its metal clips connect certain holes and not others, and you cannot see them. If you push both legs of a resistor into the same row, the board connects them together and the resistor does nothing. If you forget that the two halves of a row are separate, your circuit has a gap. Most "my circuit doesn't work" questions from beginners are not about electronics at all, they are about the breadboard. This lesson fixes that.

## The Physics

### What is under the holes

Flip a breadboard over and peel off the sticky backing (do it once, on a cheap board, it is worth seeing). Underneath, you see rows of thin metal clips, usually phosphor bronze or nickel-silver plated, sitting in slots. Each clip is a little strip with five pairs of spring fingers. When you push a lead into a hole, it slides between two fingers, which squeeze it from both sides. Metal touching metal under pressure makes an electrical connection.

```
 side view of one clip (5 holes), a lead pushed into the middle hole

   plastic top   ==[ ]====[ ]====[|]====[ ]====[ ]==
                         |   |    |lead
   spring fingers       \ /  \ /  \|/   \ /   \ /
   metal strip    ======+====+====+=====+=====+======
                  one piece of metal joins all five holes
```

Because the whole clip is one piece of metal, all five holes it serves are connected to each other. Any lead pushed into any of those five holes is joined to the others, with a resistance of a few hundredths of an ohm (tiny compared with the resistors you will use, which are hundreds or thousands of ohms).

### The layout

A common "half-size" breadboard has 30 numbered rows and 10 lettered columns, a to j, plus two power rails on each long edge.

```
       L-  L+     a b c d e     f g h i j     R+  R-
        |   |                                  |   |
   1    o   o     o-o-o-o-o     o-o-o-o-o      o   o
   2    o   o     o-o-o-o-o     o-o-o-o-o      o   o
   3    o   o     o-o-o-o-o  |  o-o-o-o-o      o   o
   4    o   o     o-o-o-o-o  |  o-o-o-o-o      o   o
   5    o   o     o-o-o-o-o  |  o-o-o-o-o      o   o
   .    |   |                |                 |   |
   .    |   |      (row strips run across, 5 holes each;
   .    |   |       rails run down the whole length)
  30    o   o     o-o-o-o-o     o-o-o-o-o      o   o
                             ^
                        centre gap
```

The rules, which you should be able to recite:

1. **In the middle area, holes are connected across, in groups of five.** a10, b10, c10, d10 and e10 are one strip. f10, g10, h10, i10 and j10 are another.
2. **The centre gap separates the two halves.** e10 and f10 are *not* connected.
3. **Different rows are not connected.** a10 and a11 are not connected.
4. **The rails run down, along the whole length.** Every hole in the L+ column is one strip, every hole in L- is another. They are usually marked with a red line (+) and a blue or black line (-).
5. **The rails on the left and right are separate** until you join them with a jumper wire.

Counting: 30 rows x 10 holes = 300 holes in the middle, plus 4 rails of 25 holes = 100, for 400 tie points. A "full-size" board has 63 rows and 830 tie points. Some full-size boards split each rail in the middle (look for a break in the red and blue lines); if your circuit works on the top half and not the bottom, that is the first thing to check.

### Why the gap exists

The spacing between holes is 2.54 mm (0.1 inch), and the gap is 7.62 mm (0.3 inch). That is exactly the spacing of the two rows of legs on a standard integrated circuit package, the DIP (dual in-line package). Drop a chip across the gap and each of its legs lands in its own strip, with four free holes next to it for connections. If there were no gap, the chip's opposite legs would be shorted together. You will use chips from Phase 13 onwards, but the board was designed around them from the start.

### Limits of the board

A breadboard is for low-power experiments. The clips are rated around 1 A and up to a few tens of volts, which is far more than we need (this course stays at 12 V DC or less, Phase 00, Lesson 06). Neighbouring strips sit very close, so there is a little capacitance between them (a few picofarads; capacitance is Phase 07). That does not matter for slow circuits but makes breadboards poor for radio frequencies. Clips also wear out: if you force thick leads in, they stretch and stop gripping thin ones.

## The Concept

### Think in nets, not holes

In Phase 00, Lesson 05 you met a **node**: a point in a schematic where parts connect. On a breadboard a node becomes a **net**: the set of all holes that are joined, through strips and jumper wires. Building a circuit is just this:

> For every node in the schematic, choose one net on the board, and put every lead that touches that node into that net.

That is all. The position of parts on the board does not need to look like the schematic. Only the connections matter.

### Example: an LED with a resistor

The circuit we will build:

```
   +9 V ----[ R1 680 ohm ]----+----|>|----+
                              |   D1 LED  |
                            node A      node B
                                          |
   0 V -----------------------------------+
```

An LED (light-emitting diode) lets current through in one direction only, from anode to cathode, and glows when it does. It needs a resistor in series to limit the current; you will see exactly why in Phase 11, Lesson 07. For now, trust the 680 ohm.

There are four nodes: +9 V, A, B and 0 V. Choose a net for each:

| Node | Net on the board | Leads in it |
|---|---|---|
| +9 V | L+ rail | battery plus wire, R1 left leg |
| A | row 10 left strip (a10-e10) | R1 right leg, LED anode |
| B | row 13 left strip (a13-e13) | LED cathode, a jumper wire |
| 0 V | L- rail | battery minus wire, the other end of the jumper |

Placement: battery plus to L+1, battery minus to L-1. R1 from L+10 to c10. LED anode in e10, cathode in e13. A jumper from a13 to L-13.

```
          L-   L+     a    b    c    d    e
row 10    |    o===R1===========o    .    o   R1 from L+10 to c10, LED anode in e10
row 11    |    |                          |
row 12    |    |                         LED
row 13    o====|=wire=o    .    .    .    o   jumper wire from a13 to L-13, LED cathode in e13
        minus   plus
```

Follow the loop with your finger: plus rail, R1, row 10, LED, row 13, jumper, minus rail, battery. Closed.

### The three classic mistakes

**Mistake 1: both legs in the same strip.** Push R1 in with one leg in b10 and the other in d10. Both legs are in the same metal clip, so the clip connects them directly. Current takes the clip (practically zero ohms) instead of the resistor. The resistor is **shorted out**: it is physically there but electrically missing. In the LED circuit this is dangerous for the LED: nothing limits the current any more.

```
   row 10:   a    b    c    d    e
             .    o---R1----o    .      legs in b10 and d10
             ======================     the hidden strip joins them: R1 is bypassed
```

**Mistake 2: forgetting the way back.** Leave out the jumper from row 13 to the minus rail. Row 13 now holds only the LED cathode. A net with a single lead in it is a dead end: no current can flow through that lead, so the loop is open. The LED stays dark and the circuit looks fine at a glance.

**Mistake 3: shorting the supply.** A jumper meant for L- goes into L+ instead (they are right next to each other), or a wire joins the + and - rails. If it connects + to - directly, the battery is short-circuited (Lesson 03): huge current, a hot wire, a damaged battery. Always double-check rail wires before connecting the battery, and connect the battery *last*.

### A rule of thumb for checking

Before powering a board, for every part ask: "Are my two legs in **different** nets?" and for every net ask: "Does this net hold **at least two** leads?" A part with both legs in one net is shorted out. A net with only one lead is a dead end. Then trace the loop from + back to -. These three checks catch nearly every breadboard bug, and they are exactly what our program does.

### Straddling the gap

Some people put an LED with one leg in e10 and the other in f10. That is perfectly fine: e10 and f10 are different strips. Same row *number* is not the same *net*. The gap is your friend: it gives every row two independent nets.

## Build It

We model the board as a set of holes and let a computer work out which holes are joined. The tool for that is **union-find**: start with every hole in its own group, then, each time we learn that two holes are connected (same clip, or a jumper), merge their groups. At the end, two holes are connected exactly when they are in the same group.

### Step 1: Union-find

```python
class UnionFind:
    def __init__(self):
        self.parent = {}

    def add(self, item):
        self.parent.setdefault(item, item)

    def find(self, item):
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != root:
            self.parent[item], item = root, self.parent[item]
        return root

    def union(self, first, second):
        root_first, root_second = self.find(first), self.find(second)
        if root_first != root_second:
            self.parent[root_second] = root_first
```

Each group has one "leader" (the root). `find` walks up to the leader and, on the way back, points everyone directly at it so the next lookup is quick. `union` makes one leader report to the other, merging the groups.

### Step 2: The holes and the hidden strips

```python
ROWS = 30
LEFT_COLUMNS = "abcde"
RIGHT_COLUMNS = "fghij"
RAILS = ["L+", "L-", "R+", "R-"]
RAIL_HOLES = 25


def all_holes():
    holes = [f"{column}{row}" for row in range(1, ROWS + 1) for column in LEFT_COLUMNS + RIGHT_COLUMNS]
    holes += [f"{rail}{index}" for rail in RAILS for index in range(1, RAIL_HOLES + 1)]
    return holes


def internal_strips():
    strips = []
    for row in range(1, ROWS + 1):
        strips.append([f"{column}{row}" for column in LEFT_COLUMNS])
        strips.append([f"{column}{row}" for column in RIGHT_COLUMNS])
    for rail in RAILS:
        strips.append([f"{rail}{index}" for index in range(1, RAIL_HOLES + 1)])
    return strips


def build_board(wires):
    board = UnionFind()
    for hole in all_holes():
        board.add(hole)
    for strip in internal_strips():
        for hole in strip[1:]:
            board.union(strip[0], hole)
    for start, end in wires:
        board.union(start, end)
    return board
```

Each row gives two strips (left and right of the gap), and each rail gives one long strip. Jumper wires are just more unions. The program confirms the layout rules:

```
Breadboard model: 30 rows x 10 columns + 4 rails of 25
  total holes (tie points): 400
  separate metal strips   : 64
  a10 and e10 connected?  : True
  e10 and f10 connected?  : False  (the centre gap)
  a10 and a11 connected?  : False
  L+1 and L+25 connected? : True
```

64 strips: 30 rows x 2 halves = 60, plus 4 rails.

### Step 3: Placing parts and listing nets

A part is a name and a list of legs, each leg in a hole:

```python
good_parts = [
    ("B1", [("plus", "L+1"), ("minus", "L-1")]),
    ("R1", [("a", "L+10"), ("b", "c10")]),
    ("D1", [("anode", "e10"), ("cathode", "e13")]),
]
good_wires = [("a13", "L-13")]
```

```python
def net_names(board, parts):
    names = {}
    for name, legs in parts:
        for leg_name, hole in legs:
            root = board.find(hole)
            names.setdefault(root, []).append(f"{name}.{leg_name}")
    return names
```

For the working circuit it prints three nets, exactly the nodes of the schematic (+9 V, A, and B joined to 0 V through the jumper):

```
  net: B1.plus, R1.a
  net: B1.minus, D1.cathode
  net: R1.b, D1.anode
```

### Step 4: The three checks

```python
def shorted_parts(board, parts):
    return [name for name, legs in parts if board.find(legs[0][1]) == board.find(legs[1][1])]


def lonely_legs(board, parts):
    members = net_names(board, parts)
    return [labels[0] for labels in members.values() if len(labels) == 1]
```

The loop check treats every net as a stop on a map and every part (except the battery) as a road between the two nets its legs are in. Then it searches, stop by stop, for a route from the battery's plus net to its minus net:

```python
def loop_is_closed(board, parts, battery_name):
    battery = dict(parts)[battery_name]
    start = board.find(battery[0][1])
    goal = board.find(battery[1][1])
    if start == goal:
        return False
    edges = {}
    for name, legs in parts:
        if name == battery_name:
            continue
        first, second = board.find(legs[0][1]), board.find(legs[1][1])
        edges.setdefault(first, []).append(second)
        edges.setdefault(second, []).append(first)
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            return True
        for neighbour in edges.get(node, []):
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return False
```

### Step 5: Run it on five boards

`main()` inspects the working circuit and four variations. Run it from the repository root:

```
uv run python phases/02-your-first-circuits/06-the-breadboard/code/main.py
```

Excerpts of the output:

```
=== 2. resistor with both legs in row 10 ===
  net: B1.plus, R1.a, R1.b, D1.anode
  net: B1.minus, D1.cathode
  problem: R1 is shorted: both legs in the same net, current bypasses it

=== 3. forgot the jumper to the minus rail ===
  ...
  problem: B1.minus touches nothing else
  problem: D1.cathode touches nothing else
  problem: OPEN CIRCUIT: no path through the parts from battery + back to battery -

=== 4. jumper pushed into the plus rail by mistake ===
  net: B1.plus, R1.a, D1.cathode
  ...
  problem: OPEN CIRCUIT: no path through the parts from battery + back to battery -

=== 5. LED straddling the centre gap ===
  ...
  ok: closed loop, no shorted parts, every leg has company
```

Case 2 is the scary one: the loop *is* closed, so current flows, but R1 is bypassed and the LED sees the full 9 V. Case 4 is sneaky: R1 and the LED now form a little loop that starts and ends at plus, so no current flows through them at all. Case 5 shows the gap at work: the LED sits in e10 and f10, a jumper takes row 10's right half to the right minus rail, and another joins the right and left minus rails.

Try your own: put the jumper in b12 instead of a13 and predict what the program says before you run it.

## Use It

- **Real boards.** Half-size (400 tie points) and full-size (830 tie points) boards are sold everywhere; they are often ganged on a metal backing plate with screw terminals for the supply. Use solid-core wire around 0.5-0.65 mm diameter (22-24 AWG): stranded wire frays and jams the clips.
- **Colour discipline.** Use red jumpers for the positive supply, black or blue for ground, and other colours for signals. It costs nothing and halves debugging time.
- **Ready-made jumpers and resistor legs.** Trim component leads so parts sit flat; long legs touching each other create accidental connections that no schematic shows.
- **Chips across the gap.** Every DIP chip, from the classic 555 timer to an 8-bit microcontroller like the ATmega328P (the chip on an Arduino Uno), is designed to sit across the centre gap.
- **Software that thinks like our script.** Circuit drawing programs (KiCad, Fritzing) and every circuit simulator do exactly what union-find does: they reduce a picture of wires into a list of nets. That list is called a **netlist**, and you met a tiny one in Phase 00, Lesson 05. Our simulator in Phase 05 starts from a netlist too.

## Try It in the Lab

The lab task "Push in the missing jumper wire" gives you the LED circuit from this lesson already placed on a breadboard: battery on the rails, a 680 ohm resistor from the plus rail to row 10, the LED from row 10 to row 13. One connection is missing between row 13 and the minus rail, and you have three things you could put there. Think about which ones close the loop, and about how much current each one would let the LED have. The goals check that the LED gets a sensible current and that row 13 really is at the minus rail.

## Common Mistakes

- **Putting both legs of a part in one row strip.** The part is shorted out. Every two-legged part should span two different strips: across rows, or across the gap.
- **Assuming the two halves of a row are connected.** They are not; the gap separates them. If you need them joined, add a jumper.
- **Assuming the left and right rails are connected.** They are separate until you join them. Same for split rails on full-size boards.
- **Connecting the battery first.** Build with the power off, check, then connect the supply last. If something gets hot, disconnect immediately.
- **Putting the LED in backwards.** The long leg (anode) goes towards plus. Backwards, it simply stays dark (it blocks current; Phase 11 explains why).
- **Forcing thick leads in.** Leads thicker than about 0.8 mm (for example some power diodes) spread the clip for ever; thin leads in that hole later make intermittent contact. If a circuit works only when you press on it, suspect a tired clip.
- **Trusting a part because it "looks right".** Electricity only follows the metal. When in doubt, check with a multimeter's continuity beep (Lesson 07).

## Exercises

1. **Connected or not?** For each pair, say whether the holes are connected on a bare half-size board: (a) c7 and e7, (b) e7 and f7, (c) c7 and c8, (d) L+3 and L+22, (e) L+3 and R+3.
2. **Count the strips.** A full-size board has 63 rows, 10 columns split by a gap, and 4 rails that are each split into two halves. How many separate metal strips does it have? How many tie points if each rail half has 25 holes?
3. **Place it.** A 9 V battery feeds two resistors in series, 1 kΩ and 2 kΩ, back to minus. Write down a placement (holes for every leg, plus any jumpers) using only rows 5 to 8 and the left rails, then run it through `inspect` by editing `main.py`.
4. **Debug from nets.** A friend's program prints `net: B1.plus, R1.a` / `net: R1.b` / `net: D1.anode, D1.cathode, B1.minus`. Describe in words what is physically wrong on their board and how you would fix it.
5. **Extend the checker.** Add a check that warns when an LED's anode is in the same net as the battery's minus terminal (an LED in backwards, in this simple circuit). Test it on a board where the LED is reversed.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| breadboard | "the board with holes" | a solderless prototyping board whose hidden spring clips join holes in fixed groups |
| row strip | "the row" | five holes on one side of the gap, joined by one clip |
| power rail | "the rail", "the bus" | a long strip along the edge used to distribute the supply; usually red for + and blue for - |
| centre gap | "the ditch", "the ravine" | the groove that splits every row into two independent strips, sized for DIP chips |
| jumper | "a wire" | a short solid wire joining two holes, so two strips become one net |
| net | "a node" | the complete set of points that are electrically the same, through strips and wires |
| shorted out | "it's bypassed" | a part whose two leads are in the same net; no voltage across it, no current through it |
| netlist | "the connection list" | a list of every part and the nets its leads touch; what simulators and PCB tools work from |

## Further Reading

- [Wikipedia, "Breadboard"](https://en.wikipedia.org/wiki/Breadboard) - history from wooden bread boards to Ronald Portugal's solderless design, with photos of the internal clips.
- [SparkFun, "How to Use a Breadboard"](https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard) - photos of the clips inside and of real layouts.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, chapter on building circuits (prototyping, breadboards, wiring practice).
- Ben Eater, the "Build an 8-bit computer" video series - a masterclass in neat breadboard wiring, which you will appreciate more with every phase.
