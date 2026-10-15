# Series and Parallel Intuition

> In series, parts share one path and split the voltage. In parallel, parts share the voltage and each gets its own path.

**Type:** Build
**Prerequisites:** Phase 02 (Your First Circuits), Lessons 01 (The Closed Loop), 02 (Batteries and Loads) and 03 (Switches, Open and Short Circuits)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Series | Parts connected one after another in a single chain, so the same current passes through each | Beads on one string: to get from one end to the other you pass through every bead |
| Parallel | Parts connected side by side, each between the same two points, so each has its own path | Lanes of a motorway: cars can take any lane, and all lanes start and end at the same towns |
| Branch | One of the separate paths in a parallel arrangement | One lane of the motorway |
| Node | A point where two or more parts connect; all wire joined together without parts in between counts as one node | A road junction |
| Brightness | How much light a bulb gives, which rises with the power it receives | How loud a radio is, which rises with the power to the speaker |
| Shunt | A path placed across a part so that current can go around it | A bypass road around a town |
| Equivalent load | The single load that would draw the same current from the battery as a whole group of loads | Replacing three narrow doors by one wide door that lets the same crowd through |

## Learning Objectives

- Recognise two loads connected in series and two loads connected in parallel, in a schematic and on a real board
- Predict, without formulas, what happens to brightness and battery current when you add bulbs in series or in parallel
- Explain why one failed bulb darkens a whole series string but not a parallel one
- Compute currents, voltages and powers for identical bulbs in series and in parallel, using the previews V = I x R and P = V x I
- Explain why houses are wired in parallel and why cheap decorative lights were long wired in series

## The Problem

You have a 6 V lantern battery and two 6 V bulbs. You want both to light. There are only two ways to connect two bulbs to one battery so that current flows through both, and they give very different results.

Wire them one way and both bulbs glow a dull orange. Unscrew one and the other goes out too. Wire them the other way and both shine at full brightness, each one independent of the other, but the battery is flat twice as fast.

These two arrangements, **series** and **parallel**, are the building blocks of every circuit you will ever see. Christmas lights, car headlights, the sockets in your house, the cells inside a laptop battery, the resistors in a volume control: all are series, parallel or combinations of the two. Phase 04 will give you exact formulas. This lesson gives you the intuition first, so that when the formulas arrive, you already know what answer to expect.

## The Physics

### Series: one path, shared push

Put two bulbs one after another, so that the current leaving the first must go through the second before returning to the battery:

```
        +--------(X)--------(X)--------+
        |        L1          L2        |
      +-+-+                            |
  6 V  ---                             |
      --+--                            |
        |                              |
        +------------------------------+
```

There is only **one path**. From Lesson 01 you know that in a single loop the current is the same at every point. So the same current flows through L1 and through L2. No choice, no splitting.

Now think about energy. Each coulomb leaving the battery's + end carries 6 joules (6 V = 6 J/C). On its way round it must give up all 6 joules before it gets back to the - end, and it passes through two bulbs. Two identical bulbs take equal shares: 3 joules each. So each bulb has **3 V across it**, half the battery voltage.

Half the voltage on a bulb also means about half the current through it (Lesson 02: the load sets the current at a given voltage, and for a resistor-like bulb, half the push gives half the flow). Half the voltage times half the current is **a quarter of the power**. Each bulb glows at roughly a quarter of its rated power: dim, orange, disappointing.

In terms of difficulty: the charge now has to push through two filaments in a row, so the loop is twice as hard to drive. The total resistance is the sum: 12 Ω + 12 Ω = 24 Ω, and the current is 6 V / 24 Ω = 0.25 A.

### Parallel: shared push, separate paths

Now connect each bulb directly across the battery: both top contacts to the + side, both bottom contacts to the - side.

```
        +----------+----------+
        |          |          |
      +-+-+       (X) L1     (X) L2
  6 V  ---         |          |
      --+--        |          |
        |          |          |
        +----------+----------+
```

Each bulb sits between the same two nodes: the top wire, at 6 V, and the bottom wire, at 0 V. So each bulb has the **full 6 V across it**, exactly as if it were alone. Each draws its rated 0.5 A and shines at full brightness.

The battery now has to supply both: 0.5 A for L1 plus 0.5 A for L2, so **1.0 A in total**. The current splits at the top junction (1.0 A comes in, 0.5 A goes down each branch) and joins again at the bottom (0.5 A + 0.5 A = 1.0 A goes back to the battery). No charge is lost at a junction; what goes in comes out. (That bookkeeping rule is Kirchhoff's current law, Phase 04, Lesson 02.)

In terms of difficulty: giving the charge two paths instead of one makes it **easier** for the battery to push current around. Two 12 Ω bulbs in parallel draw the same current as a single 6 Ω load. Adding a parallel branch always makes the total resistance smaller, never bigger, even though you added "more resistance". That sounds backwards at first. Think of supermarket checkouts: opening a second till does not make the queue slower, it doubles how many customers get through per minute.

### Why one dead bulb matters (or not)

When a filament breaks, that bulb becomes an open circuit (Lesson 03).

- **Series**: the broken bulb is in the only path. The whole loop is open, so the current is zero everywhere and **every bulb goes dark**. You cannot tell which one failed by looking.
- **Parallel**: the broken bulb was one of several paths. Its branch carries nothing, but the other branches still connect the + side to the - side, still have 6 V across them, and keep shining exactly as before. The battery simply supplies less total current.

### Real batteries feel the difference

An ideal battery holds its voltage whatever you connect. A real one has a little internal resistance (Lesson 03; Phase 06 covers it fully), so when you draw more current, a little more voltage is lost inside the battery and the bulbs get slightly less. Our lantern battery has about 0.2 Ω inside:

```
1 bulb  (12 Ω):          current = 6 / (0.2 + 12)  = 0.492 A   bulb voltage = 0.492 x 12 = 5.90 V
2 in parallel (like 6 Ω): current = 6 / (0.2 + 6)   = 0.968 A   bulb voltage = 0.968 x 6  = 5.81 V
```

Each bulb now gets 5.81 / 12 = 0.484 A instead of 0.5 A. Barely noticeable with two bulbs, but plug in twenty and the battery's voltage visibly sags. Every source has a limit to how much it can feed in parallel.

### A little history

The first electric street lights of the late 1870s and 1880s were arc lamps, and they were usually wired in **series**: one long loop running from lamp to lamp at thousands of volts. It was cheap in copper, but one failing lamp could darken the street unless it had an automatic bypass, and the high voltage was lethal. When Thomas Edison designed his incandescent lighting system for homes and offices (Pearl Street station, New York, 1882), he chose **parallel** distribution at about 110 V: every lamp across the same two mains wires, each switched on and off independently. That decision is why every socket in your home today is in parallel.

## The Concept

### Recognising the two arrangements

Forget how the wires are drawn on the page; ask about the nodes.

- **Series**: two parts share exactly one node, and **nothing else** connects to that node. All the current leaving one must enter the other.
- **Parallel**: two parts are connected between **the same two nodes**. Whatever voltage is across one is across the other.

```
SERIES (A and B share node m, nothing else touches m)

   x ----[ A ]---- m ----[ B ]---- y

PARALLEL (A and B both go from node x to node y)

        +----[ A ]----+
   x ---+             +--- y
        +----[ B ]----+
```

A useful finger test: put your finger on the + terminal and trace to the - terminal. If every path you can trace goes through both parts, they are in series. If you can trace one path through A only and another through B only, they are in parallel.

### The rules of thumb (identical loads)

| | Series | Parallel |
|---|---|---|
| Current through each part | Same for all; shrinks as you add parts | Each gets its own; unchanged as you add parts |
| Voltage across each part | Battery voltage shared out (n parts: V / n each) | Full battery voltage across every part |
| Brightness of each bulb | Drops fast: 1 / n² of rated power | Stays at full |
| Total current from the battery | Drops (V / (n x R)) | Rises (n x V / R) |
| Total "difficulty" (resistance) | Adds up: n x R | Shrinks: R / n |
| One part fails open | Everything stops | Only that branch stops |
| Battery life | Longer | Shorter |

### Worked example 1: bulbs in series

Identical 6 V 0.5 A bulbs (each 12 Ω hot), 6 V battery. With n bulbs in series:

```
total resistance = n x 12 Ω
current          = 6 V / (n x 12 Ω)
voltage each     = current x 12 Ω = 6 V / n
power each       = voltage each x current
```

```
n = 1:  I = 6 / 12 = 0.500 A   V each = 6.00 V   P each = 6.00 x 0.500 = 3.000 W  (1.000 x rated)
n = 2:  I = 6 / 24 = 0.250 A   V each = 3.00 V   P each = 3.00 x 0.250 = 0.750 W  (0.250 x rated)
n = 3:  I = 6 / 36 = 0.167 A   V each = 2.00 V   P each = 2.00 x 0.167 = 0.333 W  (0.111 x rated)
n = 4:  I = 6 / 48 = 0.125 A   V each = 1.50 V   P each = 1.50 x 0.125 = 0.188 W  (0.062 x rated)
```

Two bulbs in series get a quarter of their power each; four get one sixteenth. (As in Lesson 02, real filaments run cooler at low voltage, their resistance drops, and they end up a bit brighter than this fixed-resistance estimate. The trend is the same.)

### Worked example 2: bulbs in parallel

Same bulbs, same battery, in parallel:

```
voltage each = 6 V        (every bulb is across the battery)
current each = 6 V / 12 Ω = 0.5 A
battery current = n x 0.5 A
```

```
n = 1:  battery gives 0.5 A   (3 W total)
n = 2:  battery gives 1.0 A   (6 W total)
n = 3:  battery gives 1.5 A   (9 W total)
n = 4:  battery gives 2.0 A   (12 W total)
```

Every bulb is at full brightness. The cost is paid by the battery.

### Worked example 3: how long the battery lasts

A 6 V pack of four AA cells holds about 2500 mAh (Lesson 02). Hours = capacity / current:

```
1 bulb:          2500 mAh / 500 mA  = 5.0 h
2 in series:     2500 mAh / 250 mA  = 10.0 h   (but both dim)
2 in parallel:   2500 mAh / 1000 mA = 2.5 h    (both bright)
```

There is no free lunch. Twice the light costs twice the current and half the running time.

### Worked example 4: decorative light strings

Many classic strings of "mini lights" for 120 V mains put around 50 small bulbs in series. Each bulb is rated about 2.5 V, 0.17 A, so it behaves like 2.5 / 0.17 = 14.7 Ω.

```
50 bulbs in series:   total = 50 x 14.7 = 735 Ω
                      current = 120 / 735 = 0.163 A
                      voltage each = 120 / 50 = 2.40 V   (just under rated: long life)
```

Series lets cheap 2.5 V bulbs run straight off mains without any transformer. The weakness: one broken filament would open the loop and darken all 50. Manufacturers solved this with a **shunt**, a tiny coated wire inside each bulb's base, wrapped across the filament's two posts. While the filament is intact the shunt's coating insulates it. When the filament breaks, the full 120 V appears across that one gap (an open circuit, Lesson 03!), which punches through the coating and welds the shunt shut. The dead bulb becomes a plain wire and the rest light up again.

But now 49 bulbs share 120 V:

```
49 bulbs:  current = 120 / (49 x 14.7) = 0.1665 A, voltage each = 2.449 V
48 bulbs:  current = 120 / (48 x 14.7) = 0.1700 A, voltage each = 2.500 V
```

Every failed bulb pushes the others closer to (and then past) their rating, so failures speed up. That is why you are told to replace dead mini bulbs promptly. (This course does not touch mains; these are numbers only.)

### Worked example 5: your home

Every socket in a house is in parallel across the same two supply wires (at 230 V in Europe, about 120 V in North America). Each appliance gets the full voltage and draws its own current. Using current = power / voltage at 230 V:

```
kettle      2200 W / 230 V = 9.57 A    running total  9.57 A
lamp          60 W / 230 V = 0.26 A    running total  9.83 A
television   100 W / 230 V = 0.43 A    running total 10.26 A
fridge       150 W / 230 V = 0.65 A    running total 10.91 A
```

Switching the lamp on or off does not affect the kettle. But the currents **add up** in the wire back to the fuse box, and when the total goes over the circuit breaker's rating (often 16 A or 20 A), the breaker opens the loop (Lesson 03). That is what happens when you run a kettle, a heater and a hair dryer on the same circuit.

## Build It

### Step 1: Bulbs in series

The function returns the current through each bulb, the voltage across each, the power in each, and the battery current (the same as the bulb current in series). An optional `internal_ohms` lets us add a real battery's internal resistance later.

```python
def series_bulbs(battery_volts, bulb_ohms, count, internal_ohms=0.0):
    current = battery_volts / (internal_ohms + bulb_ohms * count)
    volts_each = current * bulb_ohms
    return current, volts_each, current * volts_each, current


for count in range(1, 5):
    amps, volts, watts, battery_amps = series_bulbs(battery_volts, bulb_ohms, count)
```

```
  1 bulb(s): 0.500 A through each, 6.00 V each, 3.000 W each = 1.000 x rated, battery gives 0.500 A
  2 bulb(s): 0.250 A through each, 3.00 V each, 0.750 W each = 0.250 x rated, battery gives 0.250 A
  3 bulb(s): 0.167 A through each, 2.00 V each, 0.333 W each = 0.111 x rated, battery gives 0.167 A
  4 bulb(s): 0.125 A through each, 1.50 V each, 0.188 W each = 0.062 x rated, battery gives 0.125 A
```

### Step 2: Bulbs in parallel

n identical bulbs in parallel draw the same current as one load of R / n (we will prove this in Phase 04, Lesson 04). We find the battery current, then the voltage across the group, then each bulb's share.

```python
def parallel_bulbs(battery_volts, bulb_ohms, count, internal_ohms=0.0):
    combined_ohms = bulb_ohms / count
    battery_current = battery_volts / (internal_ohms + combined_ohms)
    volts_each = battery_current * combined_ohms
    current_each = volts_each / bulb_ohms
    return current_each, volts_each, current_each * volts_each, battery_current
```

```
  1 bulb(s): 0.500 A through each, 6.00 V each, 3.000 W each = 1.000 x rated, battery gives 0.500 A
  2 bulb(s): 0.500 A through each, 6.00 V each, 3.000 W each = 1.000 x rated, battery gives 1.000 A
  4 bulb(s): 0.500 A through each, 6.00 V each, 3.000 W each = 1.000 x rated, battery gives 2.000 A
```

### Step 3: One bulb burns out

We mark which of three bulbs still work with a numpy boolean array. In series, one `False` anywhere opens the loop. In parallel, `np.where` gives each working bulb its 0.5 A and the broken one 0 A.

```python
working = np.array([True, False, True])
series_current = battery_volts / (bulb_ohms * 3) if working.all() else 0.0
parallel_currents = np.where(working, battery_volts / bulb_ohms, 0.0)
```

```
  series:   every bulb carries 0.000 A -> all three dark
  parallel: bulb 1 carries 0.500 A -> lit
  parallel: bulb 2 carries 0.000 A -> dark
  parallel: bulb 3 carries 0.500 A -> lit
  parallel: battery gives 1.000 A
```

### Step 4: A real battery

```python
for count in range(1, 6):
    amps, volts, watts, battery_amps = parallel_bulbs(battery_volts, bulb_ohms, count, internal_ohms=0.2)
```

```
  1 bulb(s): 5.902 V each, 0.492 A each, battery gives 0.492 A
  2 bulb(s): 5.806 V each, 0.484 A each, battery gives 0.968 A
  5 bulb(s): 5.538 V each, 0.462 A each, battery gives 2.308 A
  2 bulbs in series for comparison: 0.248 A each, 2.975 V each
```

The more bulbs in parallel, the more the battery's voltage sags. Two in series still get only about half the voltage each.

### Steps 5 to 7: Battery life, light strings and home wiring

The rest of the script prints the numbers from Worked examples 3, 4 and 5: 5.0 h, 10.0 h and 2.5 h of battery life; the mini-light string with 50, 49 and 48 working bulbs; and the running total of current for four appliances at 230 V.

```python
mini_ohms = 2.5 / 0.17
for count in [50, 49, 48]:
    amps = 120.0 / (mini_ohms * count)
    volts = amps * mini_ohms
```

Run it all:

```
cd electronics_from_scratch
uv run python phases/02-your-first-circuits/04-series-and-parallel-intuition/code/main.py
```

## Use It

**Cars.** Headlights, brake lights and the radio are all in parallel across the 12 V system, so a blown brake bulb does not kill the headlights. Each branch has its own fuse.

**Battery packs.** Cells in series add voltage (Lesson 02): an electric bike pack might stack 13 lithium-ion cells for about 48 V. Cells in parallel add capacity at the same voltage: a laptop pack might put pairs of cells side by side to double the mAh. Many packs do both, written like "13S4P" (13 in series, each position made of 4 in parallel).

**LED strips.** A 12 V LED strip is cut into short segments, typically three LEDs and a resistor in series, and all the segments are in parallel across the 12 V rails. Series inside a segment lets the LEDs share the voltage; parallel between segments means you can cut the strip anywhere along the marked lines.

**Solar panels.** Each silicon cell gives about 0.5 to 0.6 V. A panel strings around 60 cells in series to reach a useful voltage, which is why shading a single cell can drag the whole string down. Panels include bypass diodes, the solar version of the Christmas-light shunt.

**Switches and indicators.** A switch is placed in series with what it controls (it must interrupt the only path). A voltmeter is connected in parallel with what it measures (it must see the same voltage), and an ammeter in series (it must carry the same current). Lesson 07 puts this to work.

## Try It in the Lab

Open the lab task "Two bulbs, both at full brightness". A 6 V battery with 0.2 Ω inside must light two identical 6 V 0.5 A bulbs (12 Ω each when hot). The bulbs' ends are already placed; three gaps between them can each be filled with a wire (closed switch) or left open (open switch). The goals ask for each bulb to carry between 0.45 and 0.55 A.

Before you try:

- Find the arrangement where the bulbs are in series. What current would each get? (Remember the battery's 0.2 Ω.)
- Find the arrangement where each bulb has its own path from the + side to the - side.
- Is there an arrangement that turns some wires into a short circuit across the battery? What would that do?
- Is there an arrangement where one bulb has both of its ends on the same node? What voltage is across it then?

## Common Mistakes

- **Judging by the drawing instead of the nodes.** Two parts drawn side by side on paper are not necessarily in parallel. Check whether they connect between the same two nodes.
- **"Adding a bulb always makes the battery work harder."** In series, adding a bulb makes the loop harder to drive, so the battery current goes **down**. Only in parallel does it go up.
- **"Parallel bulbs share the current, so they are dimmer."** Each parallel branch gets its own full current from the battery; it is the battery's total that grows.
- **"Adding resistance in parallel increases the total resistance."** It always decreases it. Another path is another way through.
- **Forgetting the battery's limits.** Parallel loads assume the source can supply the sum of all their currents. Real batteries sag, and too many loads can trip a fuse or breaker.
- **Expecting series bulbs of different types to share voltage equally.** Only identical loads split it equally. Different loads split it in proportion to their resistances (Phase 04, Lesson 05, the voltage divider).

## Exercises

1. Three identical 4.5 V 0.3 A bulbs are in series on a 4.5 V battery. What is each bulb's hot resistance? What current flows, what voltage does each bulb get, and what fraction of its rated power does each receive?

2. The same three bulbs are put in parallel on the same battery (ideal, no internal resistance). What current flows through each bulb and what current does the battery supply? If the battery holds 1200 mAh, how long does it last?

3. A string of 35 identical mini bulbs runs in series from 120 V. What voltage does each bulb get? If each bulb behaves like 20 Ω, what current flows? If 5 bulbs fail and their shunts close, what voltage does each of the remaining bulbs get now?

4. A house circuit has a 16 A breaker at 230 V. A 2000 W heater is already on. How many 100 W lamps can you add before the breaker trips? Show the currents.

5. (Harder) Use `parallel_bulbs` in `main.py` with `internal_ohms=0.2` to find how many 12 Ω bulbs you can put in parallel on the 6 V battery before each bulb falls below 0.45 A. Then explain, using the idea that the battery loses (battery current x 0.2 Ω) volts inside itself, why the bulbs get dimmer as you add more.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Series | "One after the other", "daisy-chained" | Parts in a single path sharing one node with nothing else attached; same current through each, voltages add up |
| Parallel | "Side by side", "across" | Parts connected between the same two nodes; same voltage across each, currents add up |
| Branch | "A leg of the circuit" | One of the separate paths between two nodes in a parallel arrangement |
| Node | "A junction", "a point" | Everything connected by plain wire with no part in between; one voltage for the whole node |
| Shunt | "A bypass" | A path across a part that lets current go around it, on purpose (or by accident, which is a short) |
| Equivalent resistance | "What the battery sees" | The single resistance that would draw the same current from the source as the whole group |

## Further Reading

- All About Circuits, *Lessons in Electric Circuits*, Volume I (DC), chapter 5 "Series and Parallel Circuits": https://www.allaboutcircuits.com/textbook/direct-current/chpt-5/what-are-series-and-parallel-circuits/
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, sections on resistors in series and parallel and on lamps.
- Khan Academy, "Resistors in series" and "Resistors in parallel" (Physics library, circuits).
- Ben Eater, YouTube channel, for watching real circuits wired on breadboards step by step.
