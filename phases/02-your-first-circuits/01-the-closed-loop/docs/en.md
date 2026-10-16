# The Closed Loop

> Current only flows around a complete ring. Break the ring anywhere, and it stops everywhere.

**Type:** Build
**Prerequisites:** Phase 00 (Meet Electricity), Phase 01 (The Physics Underneath), especially Lesson 06 (Energy, Potential and Voltage) and Lesson 08 (Current as Moving Charge)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Circuit | A closed path that charge can travel all the way around, with something that pushes it and something that uses the energy | A circular running track: every runner who leaves the start line comes back to it |
| Closed loop | A circuit with no gaps: you can trace from the battery's + end, through the parts, and back to its - end | A necklace with its clasp fastened |
| Open loop (open circuit) | A path with a gap somewhere, so the ring is not complete | The same necklace with the clasp undone: the beads are all there but the ring is broken |
| Source | The part that pushes charge around the loop and supplies energy (here, a battery) | The pump in a garden fountain |
| Load | The part that takes energy from the moving charge and turns it into something useful (light, heat, motion) | The water wheel that the fountain's stream turns |
| Conductor | A material that lets charge move through it easily, like copper | An open road |
| Insulator | A material that blocks charge, like plastic, air or glass | A wall |
| Terminal | A connection point of a part: where a wire attaches | The two ends of a battery, the two contacts of a bulb |
| Switch | A part that makes or breaks a gap in the loop on purpose | A drawbridge: down, traffic flows; up, it cannot |
| Filament | The thin, coiled wire inside an old-style bulb that glows when current heats it | A toaster wire, much smaller and much hotter |
| Return path | The part of the loop that brings charge back to the source | The road home after a delivery |

## Learning Objectives

- Explain in your own words why a circuit must be a closed loop for current to flow
- Trace the complete path of current in a flashlight, including the return path most people forget
- State and use the fact that the current is the same at every point of a single loop
- Count how many electrons per second pass any point of a loop, given the current
- Write a small Python program that decides whether a list of connections forms a closed loop

## The Problem

You find an old flashlight in a drawer. You put in two fresh AA batteries, slide the switch, and nothing happens. The batteries are new. The bulb looks fine. What is wrong?

To answer this, you need one idea that every electrician, every repair technician and every chip designer carries in their head without thinking about it: **charge only flows around a complete loop**. There must be an unbroken path from one end of the battery, through the bulb, and back to the other end of the battery. A single speck of rust on a spring, a bent metal strip that no longer touches the battery, a filament that snapped when the flashlight was dropped: any one gap anywhere in the ring and the whole thing goes dark.

This sounds obvious once you hear it, but it is the most common thing beginners get wrong. People connect one wire from a battery to a bulb and wonder why it does not light, because it feels like the electricity should "flow out of the battery into the bulb" and be used up there. It does not work like that. Nothing is used up and nothing piles up. The charge goes round and comes back. This lesson is about why.

## The Physics

### What the battery does

From Phase 01, Lesson 06 you know that a **voltage** is a difference in "electrical height" between two points, measured in **volts (V)**. One volt means each coulomb of charge gains or loses one joule of energy moving between the two points (1 V = 1 J/C). A battery keeps one terminal, marked **+**, at a higher electrical potential than the other, marked **-**. A pair of AA cells in a flashlight keeps its + end about 3 V above its - end.

The battery does this with chemistry (how, exactly, is Phase 06, Lesson 03). For now, picture it as a **pump** that lifts charge from the low side to the high side, inside itself. It can only keep doing that if charge keeps arriving at its low side to be lifted. That is the heart of the whole lesson: **a pump with nothing coming back to its inlet stops pumping.**

### What happens when you connect only one wire

Suppose you touch one wire from the battery's + end to the bulb, and leave the other bulb contact hanging in the air. A tiny amount of charge does move for a very short moment: the wire and the bulb get "charged up" to the battery's potential. But this takes a few billionths of a second and involves a minuscule amount of charge. After that, the extra charge at the dead end pushes back against any more charge arriving (like charges repel, Phase 01, Lesson 04). The flow stops. The bulb never notices.

```
      +-------+          wire          +------+
      |  +    |------------------------| bulb |----- (hanging in the air)
      |  3 V  |                        +------+
      |  -    |----- (nothing connected)
      +-------+

      charge has nowhere to go -> no steady current -> no light
```

### What happens when the loop closes

Now connect the second bulb contact back to the battery's - end. The moment the last connection touches, the battery's push is felt all the way around the ring. An **electric field** (Phase 01, Lesson 05) sets up along the wires and through the filament in a tiny fraction of a microsecond, travelling close to the speed of light. Every free electron in the copper and in the filament feels that field and starts to drift. They all start moving at almost the same moment, everywhere in the loop.

This is why the bulb lights "instantly" even though each individual electron drifts incredibly slowly. In a typical flashlight wire with 0.3 A flowing, the electrons creep along at about 0.04 millimetres per second (Phase 01, Lesson 08 showed how to calculate this). An electron leaving the battery would take hours to reach the bulb. It does not need to. The wires are already full of free electrons, like a garden hose that is already full of water: open the tap and water comes out of the far end immediately, even though the water entering the hose takes a while to get there.

### Conventional current and electron flow

A quick reminder from Phase 01. Benjamin Franklin, around 1747, decided to call one kind of charge "positive" and the other "negative" long before anyone knew what was moving inside a wire. Engineers draw current as flowing **from + to -** through the outside circuit. This is called **conventional current**. When J.J. Thomson discovered the electron in 1897, it turned out that the movers in metal wires are electrons, which carry negative charge and drift the opposite way, from - to +. Both descriptions give the same answers for everything in this course. We always use conventional current: out of the battery's + terminal, through the load, and back into the - terminal.

### Every charge comes back

Here is the key physical fact. In a steady circuit, **charge does not pile up anywhere**. If 0.3 coulombs per second leave the battery's + terminal, then 0.3 coulombs per second pass through the spring, 0.3 through the filament, 0.3 through the return strip, and 0.3 enter the battery's - terminal. If more went in than came out somewhere, charge would accumulate there, its repulsion would grow quickly, and it would push back until the flows matched again. This happens in a few nanoseconds; after that the loop is in a steady state.

So the current in a single loop is **the same everywhere**. The bulb does not "use up" current. It uses up **energy**: each coulomb arrives at the bulb with about 3 joules of electrical energy and leaves with almost none, and those 3 joules become light and heat in the filament. The charge itself goes round and round, like the chain on a bicycle. The chain does not get used up; it carries effort from the pedals to the wheel.

### A little history

Before 1800, people could only make electricity in short bursts: rubbing amber, sparks from friction machines, the jolt of a Leyden jar. In the 1780s Luigi Galvani made frog legs twitch when two different metals touched the nerve and the muscle, forming a loop. Alessandro Volta argued the effect came from the two metals, not the frog, and in 1800 he built his **pile**: a stack of zinc and copper discs separated by brine-soaked cloth. For the first time there was a source that gave a **continuous** current, and the only condition was that its two ends be joined by a conducting path. Within weeks, other scientists used Volta's pile to split water into hydrogen and oxygen. The closed loop was the first experiment of the electrical age.

## The Concept

### The rule

Read it as a sentence first: *a steady current flows only if there is a complete, unbroken conducting path from the source's + terminal, through the load, and back to the source's - terminal.*

That path is the **circuit**. The word comes from the Latin *circuitus*, "a going around". Every electronic device ever made, from a flashlight to a phone, is built from such loops, often thousands of them sharing wires.

### The flashlight, traced

Here is a simple flashlight drawn as a schematic (the drawing language from Phase 00, Lesson 07). The battery symbol has a long line for + and a short line for -. The circle with a cross is a bulb. The switch is drawn as a little lever.

```
            spring           bulb tip
     +--------------------------+
     |                          |
   +-+-+                      (X)  bulb (filament inside)
    ---  battery 3 V            |
   --+--                        | bulb side
     |                          |
     +-------o/ o---------------+
           switch    metal strip
```

Follow the conventional current with your finger, starting at the battery's + end (top):

1. Out of the battery's **+** end into the spring.
2. Through the spring into the bulb's tip contact.
3. Through the filament, where the energy turns into light and heat.
4. Out of the bulb's side contact into the metal strip that runs down the body of the flashlight.
5. Through the switch (when it is closed).
6. Back into the battery's **-** end.
7. Inside the battery, the chemistry lifts the charge back up to the + end, and the trip starts again.

Step 4 to 6 is the **return path**, and it is the part people forget. In many flashlights the return path is the metal case itself. In a car, the return path is the car's steel body: only one wire goes to each lamp, and the lamp's metal housing is bolted to the chassis, which leads back to the battery's - terminal. It looks like "one wire", but the loop is still closed. You will meet this idea again as **ground** in Phase 04.

### What breaks a loop

Any of these turns a closed loop into an open one:

| Gap | Where | What you see |
|-----|-------|--------------|
| Switch off | The switch lifts its contact | Nothing, by design |
| Broken filament | Inside the bulb | Bulb looks fine from far away, never lights |
| Corrosion | Battery spring, white crust | Flickers or nothing |
| Battery in backwards | Not a gap, but a different problem | Covered in Lesson 02 |
| Loose wire | Any joint | Works when you shake it, stops when you don't |

Notice that the location of the gap does not matter. A gap right next to the + end, in the middle, or right next to the - end: all give exactly the same result. **Zero current everywhere.** There is no such thing as "the current got as far as the bulb and stopped". In an open loop, no steady current flows anywhere.

### Worked example 1: how much current, how many electrons

Our flashlight runs on two AA cells, about 3 V. The bulb, when hot, behaves like a 10 Ω resistor. (Ω, "ohm", is the unit of resistance: how hard a part makes it for current to get through. Phase 03 is all about it.) As a preview we will earn properly in Phase 03, the current in a simple loop is the voltage divided by the resistance:

```
current = voltage / resistance
I = V / R = 3 V / 10 Ω = 0.3 A
```

Read it aloud: "the current, I, in amperes, equals the voltage, V, in volts, divided by the resistance, R, in ohms."

One ampere is one coulomb per second (Phase 01, Lesson 08). One electron carries 1.602 x 10^-19 coulombs. So the number of electrons passing any point each second is:

```
electrons per second = current / charge of one electron
                     = 0.3 / 1.602e-19
                     = 1.872e18 electrons every second
```

That is 1,872,000,000,000,000,000 electrons per second, and the number is the same at the spring, in the filament, in the metal strip, everywhere in the loop.

### Worked example 2: a minute of light

Leave the flashlight on for 60 seconds. The total charge that goes around:

```
charge = current x time = 0.3 A x 60 s = 18 C
```

That is 18 / 1.602e-19 = 1.123e20 electrons, and **every single one of them** comes back into the battery's - terminal. The battery does not run out of electrons. What it runs out of is the chemical energy it uses to lift them.

How much energy went to the bulb? From Phase 01, Lesson 09, power is voltage times current:

```
power  = V x I = 3 V x 0.3 A = 0.9 W   (0.9 joules every second)
energy = power x time = 0.9 W x 60 s = 54 J
```

54 joules of light and heat, delivered by 18 coulombs of charge, each coulomb having dropped 3 volts (3 joules per coulomb). Check: 18 C x 3 J/C = 54 J. The numbers agree.

### Worked example 3: switch off

Slide the switch to off. The loop is open.

```
current = 0 A          (everywhere in the loop)
electrons per second through the filament = 0
```

What about the bulb's power? It is tempting to write 3 V x 0 A, but careful: the bulb no longer has 3 V across it either. With no current, both ends of the bulb end up at the same potential as the battery's + end, so the voltage across the bulb is 0 V and the power is 0 W. Where did the 3 V go? It sits across the **gap in the switch**. That is a surprising and important fact, and it gets a whole lesson of its own: Lesson 03.

### The bicycle chain picture, and what it gets wrong

The best everyday picture of a closed loop is a bicycle chain. The pedals (the battery) push the chain. The chain moves the rear wheel (the load). The chain itself is not consumed; every link comes back to the pedals. Cut the chain anywhere and the wheel stops, no matter where you cut it.

What the picture gets wrong: a chain is pushed by the link behind it, one link at a time. In a wire, the battery's push is carried by the **electric field**, which reaches every electron in the loop almost at once. Also, a chain pulls (it is under tension on one side and slack on the other), while in a circuit the field pushes charge forward around the whole loop, and the "pressure" is highest at the + end and lowest at the - end. We will look at the water analogy, which is popular and also has limits, in Lesson 05.

## Build It

We will build a tiny "loop checker". We describe a circuit as a list of connections between named points, then search for a path from the battery's + end to its - end. If there is one, the loop is closed.

### Step 1: Is there a closed loop?

We collect, for every point, the list of points it touches. Then we start at "battery +" and visit every point we can reach, remembering where we came from. If "battery -" is reached, we walk back through the "came from" notes to recover the path. This kind of search is called a breadth-first search: it explores everything one step away, then two steps away, and so on.

```python
def find_closed_loop(connections, start, finish):
    neighbours = {}
    for first, second in connections:
        neighbours.setdefault(first, []).append(second)
        neighbours.setdefault(second, []).append(first)
    visited = {start: None}
    frontier = [start]
    while frontier:
        current = frontier.pop(0)
        for nxt in neighbours.get(current, []):
            if nxt not in visited:
                visited[nxt] = current
                frontier.append(nxt)
    if finish not in visited:
        return None
    path = [finish]
    while path[-1] != start:
        path.append(visited[path[-1]])
    return path[::-1]
```

Next we describe four flashlights. The complete flashlight is a chain of seven connections. We make three broken versions by removing one link each: the switch is off, the filament is broken, or only one wire reaches the bulb.

```python
flashlight = [
    ("battery +", "spring"),
    ("spring", "bulb tip"),
    ("bulb tip", "filament"),
    ("filament", "bulb side"),
    ("bulb side", "metal strip"),
    ("metal strip", "switch"),
    ("switch", "battery -"),
]
missing_return = [link for link in flashlight if link != ("metal strip", "switch")]
broken_filament = [link for link in flashlight if link != ("filament", "bulb side")]
one_wire_only = [("battery +", "spring"), ("spring", "bulb tip"), ("bulb tip", "filament")]
```

Running the script prints:

```
  complete flashlight, switch on
    closed loop: battery + -> spring -> bulb tip -> filament -> bulb side -> metal strip -> switch -> battery - -> (inside the battery) -> battery +
  switch off (strip not touching switch)
    no path from battery + back to battery -: OPEN loop, no current
  burnt-out bulb (filament broken)
    no path from battery + back to battery -: OPEN loop, no current
  only one wire to the bulb
    no path from battery + back to battery -: OPEN loop, no current
```

Only the first flashlight lights. One missing link anywhere is enough to stop everything.

### Step 2: Current when the loop is closed

```python
battery_volts = 3.0
bulb_ohms = 10.0
for name, closed in results.items():
    current = battery_volts / bulb_ohms if closed else 0.0
    print(f"  {name:42s} current = {current:.2f} A")
```

The closed flashlight gets 0.30 A. The three broken ones get 0.00 A.

### Step 3: A ring of segments passing charge along

To see "the same current everywhere" with our own eyes, we cut the loop into eight segments, each holding some free charge (5 C each, a made-up round number: real copper holds vastly more free charge). Every tick of 0.1 s, each segment passes a little charge to the next one and receives the same amount from the one before. `np.roll` shifts an array by one place around the ring, which is exactly "receive from the neighbour behind you", including the wrap-around from "battery -" back to "battery +" through the battery.

```python
segment_names = ["battery +", "spring", "bulb tip", "filament", "bulb side", "metal strip", "switch", "battery -"]
charge_in_segment = np.full(len(segment_names), 5.0)
passed_through = np.zeros(len(segment_names))
ticks = 10
charge_per_tick = current * 0.1
for _ in range(ticks):
    moving = np.full(len(segment_names), charge_per_tick)
    charge_in_segment = charge_in_segment - moving + np.roll(moving, 1)
    passed_through += moving
```

Output:

```
  battery +    charge passed in 1.0 s = 0.30 C   charge sitting there = 5.00 C
  filament     charge passed in 1.0 s = 0.30 C   charge sitting there = 5.00 C
  ...
  total free charge in the loop before: 40.00 C, after: 40.00 C
  charge passed per second at every point: 0.30 A
```

Every segment passes 0.30 C in one second, so the current is 0.30 A everywhere, and no segment gains or loses charge. The total is conserved. That is what "every charge returns" means.

### Step 4 and Step 5: Counting electrons and energy

```python
electrons_per_second = current / ELEMENTARY_CHARGE
seconds_on = 60.0
total_charge = current * seconds_on
power = battery_volts * current
for seconds in [1.0, 60.0, 3600.0]:
    energy = power * seconds
```

The script prints 1.872e+18 electrons per second, 18.0 C in a minute (1.123e+20 electrons), and energies of 0.9 J, 54 J and 3240 J for one second, one minute and one hour. Run the whole thing:

```
cd electronics_from_scratch
uv run python phases/02-your-first-circuits/01-the-closed-loop/code/main.py
```

## Use It

**The flashlight.** A classic two-cell incandescent flashlight follows exactly the path we traced. In many designs the barrel is metal and serves as the return path; in plastic ones a long brass strip runs inside the body. When an old flashlight fails, check the loop link by link: are the battery contacts shiny or crusted? Does the strip still press on the battery? Is the filament intact (hold the bulb up to the light)?

**The car.** A car's lamps, radio and starter motor each have one "positive" wire. The negative side of the battery is bolted to the steel body, and every device's metal mounting touches the body. The return path is the car itself. A rusty earth strap is a classic cause of dim headlights.

**Christmas lights and fairy lights.** Many cheap strings put all their bulbs in a single loop. One loose bulb opens the loop and the whole string goes dark. Lesson 04 explains why and what designers do about it.

**Your phone.** A phone circuit board has thousands of tiny loops. Each one still obeys the rule: current leaves the battery's + side, passes through some part, and returns to the - side through copper layers on the board.

**Burglar alarms.** Old alarm systems use the closed-loop idea backwards: a thin wire runs around a window, forming a loop. If a burglar breaks the glass and the wire, the loop opens, the current stops, and the alarm notices the missing current.

## Try It in the Lab

Open the lab task "Close the loop and light the flashlight". You get a 3 V battery and a bulb that behaves like a 10 Ω resistor when hot. There are two gaps in the path: one between the battery's + end and the bulb, and one between the bulb and the battery's - end. You have a few parts to choose from: wires (closed switches), an open switch and a 1 MΩ resistor that stands in for a piece of dry plastic.

Before you try anything, ask yourself:

- Which gap carries the charge to the bulb, and which brings it back?
- What happens to the bulb's current if only one gap is filled with a wire?
- A 1 MΩ "plastic" link does let a tiny current through. How tiny? Would the bulb glow?

The goals ask for a bulb current around 0.3 A and nearly the full 3 V across the bulb.

## Common Mistakes

- **"One wire is enough."** Connecting one wire from the battery to a bulb and expecting light. A load needs two connections, one in and one out, and both must lead back to the source.
- **"The bulb uses up the current."** It uses up energy, not charge. The current going into the bulb equals the current coming out. If you measured both (Lesson 07 shows how), you would read the same number.
- **"Current gets weaker as it goes round."** In a single loop it is the same at every point. What changes around the loop is the voltage (the electrical height), not the current.
- **"The electrons race from the battery to the bulb."** They drift at fractions of a millimetre per second. The push (the field) is what travels fast.
- **"The battery runs out of electrons."** It never does. Every electron that leaves comes back. It runs out of chemical energy.
- **Forgetting the hidden return path.** In cars, metal cases and many devices, the return is the metal body. It still counts as part of the loop, and a bad contact there breaks the circuit just as surely as a cut wire.

## Exercises

1. A torch uses three AA cells (4.5 V) and a bulb that behaves like a 15 Ω resistor when hot. Using the preview I = V / R, what current flows when the loop is closed? What current flows if the filament breaks?

2. For the torch in exercise 1, how many electrons pass through the filament each second? How many pass through the return strip each second? (Use e = 1.602e-19 C.)

3. A loop has a 9 V battery and a load that carries 0.05 A. How much charge goes around in 10 minutes? How much energy is delivered to the load in that time? Check your answer two ways: with power x time and with charge x voltage.

4. Edit `main.py` to add a fifth flashlight in which the metal strip is replaced by the metal case: add the connections ("bulb side", "case") and ("case", "switch") and remove ("bulb side", "metal strip"). Does the checker report a closed loop? Now also remove ("case", "switch"). What happens?

5. (Harder) A friend says: "If I connect the + end of one battery to a bulb, and the other side of the bulb to the - end of a *different* battery, the loop is closed." Draw it. Is there a complete loop? Use the loop checker with points named "battery A +", "battery A -", "battery B +", "battery B -" to test it, and explain the result in terms of what each battery's pump needs.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Circuit | "The wiring" | A closed conducting path around which charge can flow, containing at least a source and a load |
| Closed loop | "It's connected" | No gaps: a path exists from the source's + terminal, through the parts, back to its - terminal |
| Open circuit | "It's broken" / "it's off" | A gap somewhere in the loop; no steady current flows anywhere in that loop |
| Return path | "The negative wire", "ground" | The part of the loop that brings current back to the source; sometimes a metal case or chassis |
| Conventional current | "Current flows from + to -" | The agreed direction of current: out of +, through the load, into -; electrons actually drift the other way |
| Steady state | "Once it's on" | After the first few nanoseconds, when the current is constant and no charge is piling up anywhere |

## Further Reading

- Paul Scherz and Simon Monk, *Practical Electronics for Inventors*, chapter 2 (theory): a friendly treatment of current, voltage and simple circuits.
- All About Circuits, *Lessons in Electric Circuits*, Volume I (DC), chapter 1 "Basic Concepts of Electricity", sections on circuits and open/closed paths: https://www.allaboutcircuits.com/textbook/direct-current/chpt-1/electric-circuits/
- Richard Feynman, *The Feynman Lectures on Physics*, Volume II, chapter 13 (on current and charge conservation): https://www.feynmanlectures.caltech.edu/II_13.html
- Khan Academy, "Circuits" topic in the Physics library (electric current and circuits basics).
