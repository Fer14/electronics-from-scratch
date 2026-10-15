# Switches, Open and Short Circuits

> An open circuit has the full voltage and no current. A short circuit has huge current and no voltage. One is harmless, the other starts fires.

**Type:** Build
**Prerequisites:** Phase 02 (Your First Circuits), Lessons 01 (The Closed Loop) and 02 (Batteries and Loads); Phase 00 (Words and Units), Lesson 06 (Safety First)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| Switch | A part with two metal contacts that you can push together (closed, on) or pull apart (open, off) | A drawbridge: down lets traffic cross, up stops it |
| Closed switch | The contacts touch; the switch behaves like a short piece of wire | A drawbridge that is down |
| Open switch | The contacts are apart with air between them; no current can cross | A drawbridge that is up |
| Open circuit | A loop with a gap somewhere, so no current flows | A road with a missing bridge |
| Short circuit | An accidental path with almost no resistance that lets current bypass the load | A shortcut through a field that everyone takes instead of the road with the toll booth |
| Internal resistance | The small resistance hidden inside every real battery, which limits how much current it can give | A pump whose own pipes are a little narrow |
| Fuse | A thin wire in a holder that melts and opens the loop if the current gets too big | A tripwire that breaks to stop a runaway cart |
| Circuit breaker | A switch that opens itself when the current is too large, and can be reset | A fuse you can re-arm with a lever |
| Contact | The metal surfaces in a switch that touch to let current pass | Two hands clasping |
| Voltage across | The voltage between the two ends of one part, measured from one terminal to the other | The height difference between the top and bottom of one step |

## Learning Objectives

- Describe what a switch does in terms of closing and opening a loop
- State the two rules: an open circuit has zero current but can have full voltage across the gap; a short circuit has near-zero voltage across it but can carry a huge current
- Explain why a short circuit is dangerous and where the energy goes
- Use the idea of a battery's internal resistance to estimate short-circuit current
- Explain how a fuse protects a circuit, and estimate whether it blows

## The Problem

Your bedside lamp has a switch. Flick it and the lamp goes off. Simple. But what exactly is happening inside that switch? Is the electricity "waiting" at the switch, piled up behind the gap? Is there still voltage there? Could you get a shock from a switched-off lamp?

Now picture a different accident. You are carrying a 9 V battery in your pocket with some coins. A few minutes later your pocket is uncomfortably hot. Nothing was switched on. What happened?

Both stories are about the two extreme states a circuit can be in: **open**, where the loop is broken and nothing flows, and **short**, where the loop is closed through a path with almost no resistance and far too much flows. Every safety rule about batteries, every fuse in your house and every "check for shorts" step before switching on a new board comes from these two ideas. This lesson builds them from what you already know.

## The Physics

### Inside a switch

A switch is two pieces of metal (contacts) and a mechanism that pushes them together or pulls them apart.

- **Closed (on)**: the contacts touch firmly. Copper or silver contacts have a tiny resistance, typically a few thousandths of an ohm (milliohms, written mΩ). For our purposes, a closed switch is just a short piece of wire.
- **Open (off)**: the contacts are separated by a few millimetres of air. Air is an excellent insulator at low voltages: its resistance across a small gap is far beyond a million million ohms. For our purposes, an open switch is a gap where no current flows.

That is all a switch is: a deliberate, movable gap in the loop.

### Where does the voltage go when the switch is open?

This is the surprising part, so let us go slowly.

Take a 9 V battery, a lamp and a switch, all in one loop:

```
         +-----o/ o------+
         |    switch     |
       +-+-+            (X) lamp
   9 V  ---              |
       --+--             |
         |               |
         +---------------+
```

With the switch open, no current flows (Lesson 01). Now think about electrical height (potential, from Phase 01, Lesson 04). The bottom of the battery is at 0 V. Its top is 9 V higher. The wire from the battery's top to the left contact of the switch carries no current, so there is no reason for any voltage to be lost along it: the left contact sits at 9 V. On the other side, the right contact of the switch connects through the lamp to the bottom of the battery. No current flows through the lamp either, and a lamp with no current has no voltage across it (we will see why in Phase 03: no current, no drop). So the right contact sits at 0 V.

```
   left contact:   9 V
   right contact:  0 V
   voltage across the open switch = 9 V - 0 V = 9 V
   voltage across the lamp        = 0 V - 0 V = 0 V
```

**The whole battery voltage appears across the open gap.** This is why you can get a shock from the contacts of a switched-off mains switch if you open it up, and why electricians switch off the supply at the main board, not at the wall switch, before working on a light fitting. The gap blocks current, but the push is still there, waiting on both sides.

Charge is not "piling up" behind the gap in any meaningful amount. When the switch first opened, a tiny amount of charge shifted to set up these potentials, and then everything stopped. The wire on the left is simply sitting at 9 V, like a ball resting on a shelf: it has height but is not moving.

### Shorts: when the load is bypassed

Now take the same loop, with the switch closed and the lamp shining. Drop a paperclip across the lamp's two terminals.

```
         +-----o--o------+-------+
         |    switch     |       |
       +-+-+            (X)    paperclip
   9 V  ---              |       |
       --+--             |       |
         |               |       |
         +---------------+-------+
```

Charge arriving at the top of the lamp now has two paths back to the battery: through the filament (30 Ω when hot) or through the paperclip (perhaps 0.01 Ω). Current splits between paths in proportion to how easy they are (Phase 04, Lesson 06 will make this exact). The paperclip is 3000 times easier, so nearly all of the current goes through it. The lamp goes dark.

But that is the harmless part. The dangerous part is what happens to the **total** current. Before the paperclip, the battery was pushing charge through a 30 Ω filament. Now it is pushing through a 0.01 Ω paperclip. If the battery could hold its 9 V perfectly, the current would be 9 / 0.01 = 900 A, enough to melt the paperclip and set the battery on fire. In practice, something else limits it.

### Internal resistance: the battery's own limit

Every real battery has some resistance **inside** it: the chemistry, the electrolyte paste and the internal connections all resist the flow a little. We call it the **internal resistance** and draw it as a small resistor in series with an ideal battery. You will study it properly in Phase 06, Lesson 02; here we just need the idea.

```
     real battery
   +-------------------+
   |  ideal 9 V   r    |
   |  --||---/\/\/\----+---- + terminal
   |         1.5 Ω     |
   +-------------------+---- - terminal
```

For a 9 V alkaline battery, r is around 1.5 Ω (it varies between brands and rises as the battery empties). With a dead short across the terminals, the only real resistance left in the loop is r (plus the paperclip's tiny bit):

```
short-circuit current = battery voltage / (internal resistance + wire resistance)
                      = 9 V / (1.5 Ω + 0.01 Ω)
                      = 5.96 A
```

Compare that with the 0.29 A the lamp normally draws: twenty times more. And where does the energy go? Power is voltage times current, and for a resistor it can be written as current squared times resistance (P = I x I x R, a preview from Phase 03, Lesson 05):

```
heat inside the battery = I x I x r = 5.96 x 5.96 x 1.5 = 53 W
```

53 watts of heat inside a small 9 V battery, about as much as a soldering iron. The battery gets hot in seconds, can leak, swell or rupture. That is the pocket-full-of-coins story: the coins touch both terminals of the 9 V battery and form a short.

### Open and short are opposites

Put the two extreme states side by side for our 9 V battery with 1.5 Ω inside:

| State | Resistance of the "gap" | Current | Voltage across the gap | Power in the gap |
|-------|-------------------------|---------|------------------------|------------------|
| Open (air gap) | about 10^12 Ω | 9e-12 A, effectively 0 | 9.000 V, the full battery voltage | 0 W |
| Normal lamp | 30 Ω | 0.286 A | 8.57 V | 2.45 W |
| Short (wire) | 0.01 Ω | 5.96 A | 0.060 V, almost zero | 0.36 W |

Read the table slowly. An open circuit has **voltage without current**. A short circuit has **current without voltage**. Neither delivers useful power: the open circuit because nothing flows, the short circuit because there is almost no voltage across it. In the short case, the power goes somewhere you do not want it: into the battery's internal resistance, as heat (53 W).

## The Concept

### The two rules

Read them aloud:

1. *An open circuit carries no current, and the full source voltage can appear across the gap.*
2. *A short circuit has almost no voltage across it, and the current is limited only by whatever small resistance is left in the loop, usually the source's own internal resistance.*

### Different batteries, different dangers

How dangerous a short is depends mostly on the internal resistance. A battery designed to deliver big currents has a small r, which also means it delivers a huge current into a short. Here are typical values (they vary between brands; these are reasonable round figures) and the current through a 0.01 Ω wire across each one:

```
battery              voltage   r inside    short current          heat inside the battery
CR2032 coin cell     3.0 V     15 Ω        3.0 / 15.01 =   0.2 A    0.2 x 0.2 x 15   =    0.6 W
9 V alkaline         9.0 V     1.5 Ω       9.0 / 1.51  =   6.0 A    5.96 x 5.96 x 1.5 =  53   W
AA alkaline          1.5 V     0.15 Ω      1.5 / 0.16  =   9.4 A    9.4 x 9.4 x 0.15 =   13   W
18650 lithium-ion    3.7 V     0.03 Ω      3.7 / 0.04  =  92.5 A    92.5 x 92.5 x 0.03 = 257 W
12 V car battery    12.6 V     0.01 Ω     12.6 / 0.02  = 630   A    630 x 630 x 0.01  = 3969 W
```

The coin cell is fairly safe to short (it is still bad for it). The lithium-ion cell and the car battery are not: hundreds of amps can weld a spanner to the terminals, melt wires and start fires. (Swallowed coin cells are still very dangerous for a different reason: the current flows through body tissue and causes chemical burns.) This is why lithium-ion batteries in phones and laptops carry protection circuits, and why you should never carry loose lithium cells in a pocket.

### Where else does the heat go?

In a short, every part of the loop gets current squared times its resistance as heat. The battery's internal resistance gets most of it. The shorting wire gets I x I x 0.01 = 5.96 x 5.96 x 0.01 = 0.36 W, which sounds small, but a thin wire with high current can still get very hot because it is tiny and cannot shed heat fast. In house wiring, where the source (the grid) has very low internal resistance, it is the wires that would overheat and set walls on fire. That is what fuses and breakers are for.

### Fuses: an intentional weak link

A **fuse** is a short piece of thin wire, chosen so that it melts when the current goes above a set value. It sits in series with the circuit it protects. While the current is normal, it is just another bit of wire. When a short happens, the fuse is the thinnest, hottest part of the loop, so it melts first, and **turns the short circuit into an open circuit**. The current drops to zero, and the expensive or dangerous parts survive.

A rough way to think about how fast a fuse melts: the heat it gets depends on current squared times time. Fuse datasheets give a number called the "melting I²t" (current squared times time) in A²s. If a small 1 A fast fuse melts at about 0.5 A²s:

```
time to melt ≈ melting I²t / (current x current)

normal lamp current, 0.29 A:   below the 1 A rating, the fuse stays whole
short-circuit current, 5.92 A: 0.5 / (5.92 x 5.92) = 0.5 / 35.0 = 0.014 s = 14 ms
```

The fuse opens the loop in about a hundredth of a second, long before the battery has time to heat up. (This I²t rule works for big overloads. Near the rated current, real fuses behave differently, and their datasheets show full curves; we keep the simple version.)

Thomas Edison's lighting companies used fuses from the early 1880s, and Edison patented one in 1890: early electric lighting needed something to stop shorted wiring from burning down the newly electrified buildings. Modern homes mostly use **circuit breakers**, which do the same job with a mechanism (a bimetal strip that bends with heat, plus an electromagnet that trips on sudden large currents) and can be reset with a lever instead of replaced.

### Kinds of switches, briefly

You will meet many switches. They all do the same thing (open or close a gap), but differ in how:

- **Toggle and slide switches** stay where you put them.
- **Push buttons** (momentary) are closed only while you press them, like a doorbell.
- **Reed switches** close when a magnet comes near (door alarms).
- **Relays** are switches moved by an electromagnet, so one circuit can switch another (Phase 08).
- **Transistors** are switches with no moving parts, controlled by a voltage or current (Phase 12). Your computer contains billions of them.

Throughout this course, the lab's `switch` part is ideal: closed it is a perfect wire, open it is a perfect gap. That is why the lab hints say "a wire is a closed switch".

## Build It

We will model a 9 V battery with internal resistance as a loop of resistors in a row, and compute what happens for each switch state and for a short.

### Step 1: A switch in a loop

For a single loop of parts one after another, the preview rule is: total resistance is the sum of all the resistances, current = voltage / total, and the voltage across each part is current x that part's resistance.

```python
CLOSED_SWITCH_OHMS = 0.01
OPEN_SWITCH_OHMS = 1e12


def series_loop(battery_volts, internal_ohms, part_ohms):
    total_ohms = internal_ohms + sum(part_ohms.values())
    current = battery_volts / total_ohms
    drops = {name: current * ohms for name, ohms in part_ohms.items()}
    return current, drops


battery_volts = 9.0
internal_ohms = 1.5
lamp_ohms = 30.0
for state, switch_ohms in [("closed", CLOSED_SWITCH_OHMS), ("open", OPEN_SWITCH_OHMS)]:
    current, drops = series_loop(battery_volts, internal_ohms, {"switch": switch_ohms, "lamp": lamp_ohms})
```

Output:

```
  switch closed: current = 2.856e-01 A, across switch =  0.003 V, across lamp =  8.569 V
  switch open  : current = 9.000e-12 A, across switch =  9.000 V, across lamp =  0.000 V
```

Closed: 0.286 A, and the lamp gets 8.57 V (a little is lost inside the battery: 0.286 x 1.5 = 0.43 V). Open: 9 picoamps, which is zero for every practical purpose, and the **full 9 V sits across the switch**.

### Step 2: A wire across the lamp

Two paths side by side (in parallel) combine into one equivalent resistance. We will derive this formula in Phase 04, Lesson 04; for now trust it:

```python
def parallel(first_ohms, second_ohms):
    return 1.0 / (1.0 / first_ohms + 1.0 / second_ohms)


wire_ohms = 0.01
shorted_ohms = parallel(lamp_ohms, wire_ohms)
current, drops = series_loop(battery_volts, internal_ohms, {"switch": CLOSED_SWITCH_OHMS, "lamp with wire across": shorted_ohms})
lamp_volts = drops["lamp with wire across"]
```

```
  lamp and wire together behave like 0.0100 ohm
  current from battery = 5.92 A
  voltage across the lamp = 0.059 V, lamp current = 1.97 mA (dark)
  heat inside the battery = 52.6 W, heat in the wire = 0.35 W
```

The lamp is dark (2 mA instead of 286 mA), the battery current jumped twentyfold, and the battery is heating itself at 53 W.

### Step 3: Shorting different batteries

```python
for name, volts, ohms in batteries:
    short_current = volts / (ohms + CLOSED_SWITCH_OHMS)
    heat = short_current ** 2 * ohms
```

The output matches the table in The Concept: 0.2 A for the coin cell up to 630 A and about 4 kW for the car battery.

### Step 4: A fuse

```python
fuse_rating = 1.0
fuse_melting_i2t = 0.5
if amps <= fuse_rating:
    print(f"  {label:18s} {amps:5.2f} A -> fuse stays whole")
else:
    print(f"  {label:18s} {amps:5.2f} A -> fuse melts in about {fuse_melting_i2t / amps ** 2 * 1000:.0f} ms, loop opens, current 0 A")
```

```
  normal (lamp on)    0.29 A -> fuse stays whole
  short across lamp   5.92 A -> fuse melts in about 14 ms, loop opens, current 0 A
```

### Step 5: Open, normal and short side by side

```python
for label, gap_ohms in [("open (gap)", OPEN_SWITCH_OHMS), ("normal lamp", lamp_ohms), ("short (wire)", CLOSED_SWITCH_OHMS)]:
    amps = battery_volts / (internal_ohms + gap_ohms)
    volts = amps * gap_ohms
    watts = amps * volts
```

```
  open (gap)   current 9.000e-12 A   voltage across it  9.000 V   power in it   0.000 W
  normal lamp  current 2.857e-01 A   voltage across it  8.571 V   power in it   2.449 W
  short (wire) current 5.960e+00 A   voltage across it  0.060 V   power in it   0.355 W
```

Run it:

```
cd electronics_from_scratch
uv run python phases/02-your-first-circuits/03-switches-open-and-short-circuits/code/main.py
```

## Use It

**Battery storage rules.** Tape over the terminals of 9 V and lithium batteries before throwing them in a drawer or recycling bin. Airlines require spare lithium-ion batteries in carry-on luggage with terminals protected, precisely because a short in a suitcase can start a fire.

**Fuses in devices.** Open a car's fuse box: each circuit (radio, lights, wipers) has its own fuse, colour-coded by rating (for blade fuses, 10 A is red, 15 A blue, 20 A yellow). Multimeters have fuses on their current inputs (Lesson 07 tells the classic story of blowing one). Many power supplies and chargers have a small glass fuse inside.

**Polyfuses.** USB ports and many small boards use a resettable fuse (a PTC, "polyfuse") whose resistance shoots up when it gets hot, limiting the current, and returns to normal when it cools.

**Battery protection circuits.** Every phone battery pack contains a tiny circuit with transistor switches that opens the loop within milliseconds if it senses a short or an overload.

**Testing for shorts.** Before powering a new circuit board, technicians measure the resistance between the supply's + and - points (with power off, see Lesson 07). If it reads nearly 0 Ω, there is a short, maybe a blob of solder bridging two pins. Better to find it with a meter than with smoke.

**Light switches at home.** A wall switch interrupts only one wire to the lamp. That is enough to stop the current (one gap opens the whole loop), but parts of the fitting can still be connected to mains. Always switch off at the breaker before touching wiring. This course never works with mains (Phase 00, Lesson 06).

## Try It in the Lab

Open the lab task "Clip across the lamp without starting a fire". A 6 V battery with 0.5 Ω of internal resistance (drawn as a separate resistor, R_int) lights a 12 Ω lamp. Two test clips hang across the lamp's terminals, and you must clip one of three things between them: an open switch (a gap), a closed switch (a wire) or a second 12 Ω lamp.

Before you choose, predict for each option:

- What current would flow through the lamp? Would it stay lit?
- What voltage would appear across the lamp (and across the clips)?
- How much current would the battery have to supply? Compare 6 V / 0.5 Ω with the normal current.

The goals ask that the lamp keeps 0.4 to 0.55 A and 5.5 to 6.5 V, and that the battery delivers less than 0.6 A. One of the three options passes, one obviously fails, and one fails in a less obvious way.

## Common Mistakes

- **"No current means no voltage."** Across an open switch, the full source voltage can appear even though no current flows. Open circuits can still shock you.
- **"A short circuit has a huge voltage."** It is the other way round: a short has almost no voltage across it, and huge current through it.
- **"The short goes through the load."** A short bypasses the load. The load goes dark or stops; the danger is in the rest of the loop (battery, wires).
- **Assuming a battery limits its own current safely.** Low-resistance batteries (lithium-ion, lead-acid) can deliver tens to hundreds of amps into a short.
- **Replacing a blown fuse with a bigger one (or a piece of wire).** The fuse blew for a reason. A bigger fuse lets the wires become the weak link instead, which is how fires start.
- **Thinking "off" at a switch means "safe" for the whole fitting.** A switch opens one point of the loop; other parts may still be at full voltage.

## Exercises

1. A 4.5 V battery (internal resistance 0.5 Ω) lights a lamp that behaves like 15 Ω. What current flows with the switch closed? What voltage appears across the switch when it is open? (Use the series rule from Step 1.)

2. The same battery is shorted by a 0.01 Ω wire. What current flows, and how many watts of heat appear inside the battery? By what factor is the current larger than in normal use?

3. A circuit draws 0.8 A normally and has a 2 A fuse with a melting I²t of 2 A²s. A short makes the current 20 A. Does the fuse blow in normal use? How long does it take to melt during the short?

4. Change `internal_ohms` in `main.py` to 0.05 Ω (a much stronger battery) and run it again. What happens to the short-circuit current and to the heat inside the battery? What happens to the normal lamp current? Explain why a strong battery is more dangerous to short but makes almost no difference to the lamp.

5. (Harder) In the lab circuit (6 V, R_int = 0.5 Ω, 12 Ω lamp), work out by hand the lamp current, the lamp voltage and the battery current for each of the three options. For the second lamp in parallel, use `parallel(12, 12)` to find the combined resistance first. Which goal does each wrong option fail?

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Open circuit | "It's off", "the wire's broken" | A gap in the loop; zero current, but the source voltage can appear across the gap |
| Short circuit | "It shorted out" | An unintended near-zero-resistance path; nearly zero voltage across it and a large current, limited only by what resistance is left |
| Closed switch | "On" | Contacts touching: behaves like a wire with milliohms of resistance |
| Open switch | "Off" | Contacts apart: behaves like a gap with enormous resistance |
| Internal resistance | "The battery's limit" | The small resistance inside a real source that limits its maximum current and turns into heat when it is loaded heavily |
| Fuse | "The fuse blew" | A deliberate weak link that melts and opens the loop when the current is too high for too long |
| Circuit breaker | "The breaker tripped" | A resettable switch that opens itself on overcurrent |

## Further Reading

- All About Circuits, *Lessons in Electric Circuits*, Volume I (DC), chapter 1 section "Electric Circuits" (open and closed paths) and chapter 12 section "Fuses": https://www.allaboutcircuits.com/textbook/direct-current/chpt-12/fuses/
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd edition, chapter 1 (sources, internal resistance and the idea of an ideal switch).
- Littelfuse, *Fuseology* application guide, for how real fuses are rated (I²t, time-current curves).
- Battery University, "Safety concerns with Li-ion" (BU-304a): https://batteryuniversity.com/article/bu-304a-safety-concerns-with-li-ion
