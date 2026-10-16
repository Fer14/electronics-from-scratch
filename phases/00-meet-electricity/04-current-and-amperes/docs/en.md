# Current and Amperes

> Current is not how much charge there is. It is how much charge passes by, every second.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 00 (Meet Electricity), Lessons 02 (What a Circuit Is) and 03 (Charge and Electrons)
**Time:** ~40 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| current | How much charge flows past one point of a circuit each second | How many people pass through a turnstile each second |
| rate | How much of something happens per second (or per hour, per day) | Kilometres per hour on a speedometer |
| ampere (A), amp | The unit of current, named after André-Marie Ampère | The "litres per second" of electricity |
| through | Current is always measured *through* a part or a wire, at one point | Counting the people passing one gate |
| conventional current | The direction diagrams draw the current: from the plus terminal, round the loop, to the minus terminal | A one-way arrow painted on a road |
| electron flow | The direction electrons actually drift in a metal wire: from minus to plus, opposite to the arrows | The cars that, it turns out, drive the other way |
| direct current (DC) | Current that always flows in the same direction, as from a battery | A river flowing one way |
| alternating current (AC) | Current that keeps reversing direction many times a second, as from a wall socket | A saw going back and forth |
| ammeter | A meter that measures current; the current must pass through it | A turnstile with a counter |

## Learning Objectives

- Define current in your own words, as a rate: charge passing a point each second
- Explain the difference between "how much charge" and "how much current"
- Name the ampere, say what it measures and who it is named after
- Explain why the current is the same at every point of a single loop
- Describe the two directions people talk about (conventional current and electron flow) and why both exist
- Place everyday devices on a rough ladder of current, in words: from a watch to a car starter

## The Problem

"How much electricity does it use?" is a question people ask about everything from phones to fridges. But "how much electricity" is too vague to answer. Do we mean how hard the battery pushes? How much energy it delivers? How much charge is moving?

Electronics needs a separate, precise word for each of these. Lesson 03 gave you **charge**: the electric "stuff", carried by electrons, measured in coulombs. This lesson gives you the next one: **current**, the amount of charge that **moves past a point each second**. Lesson 05 then adds the push (voltage) and Lesson 06 the energy (power).

Current is the quantity that decides how bright a lamp glows, how fast a motor spins, how warm a wire gets, and whether a person who touches something gets hurt (Lesson 08). It is worth getting exactly right.

## The Physics

From Lesson 03: a metal wire is full of free electrons, and when the wire is part of a closed loop with a battery, the whole crowd drifts slowly round.

Now imagine standing at one point of the wire with an impossibly sharp pair of eyes, watching the crowd go by. Every second, a certain amount of charge passes you. If the battery pushes harder, or the path is easier, more charge passes you each second. If the switch is opened, none passes at all.

That amount, **the charge passing a point per second**, is the **current**.

Notice the "per second". Current is a **rate**, like speed. A car's speedometer does not tell you how far you have driven; it tells you how far you go *each hour*. In the same way, current does not tell you how much charge has passed in total; it tells you how much passes *each second*.

## The Concept

### Current is a rate

A good picture is a turnstile at the entrance of a stadium. Count the people going through it:

- "Five thousand people have gone through today" is a **total**. That is like an amount of charge.
- "Two people go through every second" is a **rate**. That is like a current.

If the turnstile stays at two people per second for a minute, the total keeps growing (more and more people inside), but the rate stays the same. A steady current is exactly that: a steady rate of charge going past, while the total that has passed keeps adding up.

So two wires can be compared by their current only if we look at the same amount of time:

- the same charge in half the time means **twice** the current
- twice the charge in the same time also means **twice** the current
- twice the charge in twice the time means **the same** current

### The ampere

The unit of current is the **ampere**, written **A**, and almost always called an **amp**. It is named after André-Marie Ampère, a French physicist who in the 1820s studied how wires carrying current push and pull on each other.

What is one amp? In words: it is the current when **one coulomb of charge passes a point every second**. And a coulomb, from Lesson 03, is the charge of a very big, fixed crowd of electrons. So one amp means: one of those big crowds goes past, every second.

When you see a formula later, current is written with the letter **I**. That comes from the French *intensité du courant*, "intensity of the current", the phrase Ampère's generation used. Do not worry about formulas now; just remember that in electronics, **I means current**.

### How big are everyday currents?

You do not need numbers yet, just a feeling for the ladder, from tiny to huge:

```
   a quartz wristwatch            a tiny trickle (about a millionth of an amp)
   a small LED indicator          a few thousandths of an amp
   a torch bulb                   a fraction of an amp
   a phone charging               about one or two amps
   an electric kettle             around ten amps
   a car's starter motor          hundreds of amps, for a few seconds
```

Electronics spans this whole range, from the trickle in a watch to the torrent in a motor. Talking about "a few thousandths of an amp" all the time is clumsy, so engineers use short prefixes like "milli" (a thousandth). Phase 01 (Lesson 01, Units and Prefixes) teaches them, along with the arithmetic. For now, words are enough.

### What decides how big the current is?

Two things decide how much current flows round a loop:

1. **How hard the source pushes.** A stronger push drives more charge round each second. That push is voltage, the subject of Lesson 05.
2. **How hard the path is to get through.** A thin glowing lamp filament makes it harder than a thick copper wire. That "hardness" is called resistance; Lesson 06 previews it and Phase 03 (Resistance and Ohm's Law) studies it.

So the battery does not "contain" a current. It provides a push, and the whole loop together decides how much current that push produces. The same battery drives a small current through a dim lamp and a large one through a bright lamp, and a dangerously huge one through a short circuit (Lesson 02).

### The river picture and what it gets wrong

A popular picture of current is a river: the current is how much water flows past a bridge each second.

What the river gets right: current is a rate; a wide, easy riverbed carries more flow than a narrow, rocky one; and the water that flows past one bridge also flows past the next.

What the river gets wrong:

- A river runs downhill to the sea and never comes back. A circuit's current goes round a closed loop and returns to the battery.
- River water moves fast; electrons in a wire drift very slowly (Lesson 03), while the push spreads almost instantly.
- A cut river bank spills water. A cut wire spills nothing: the current simply stops, everywhere in the loop at once.

Phase 02 (Lesson 05, The Water Analogy and Its Limits) is a whole lesson on these pictures.

### Current is the same all round one loop

Here is one of the most important facts in all of electronics:

> In a single loop, the current is the same at every point.

```
           ---->  same current  ---->
     +------------------------------------+
     |                                    |
   [bat]                               (lamp)
     |                                    |
     +------------------------------------+
           <----  same current  <----
```

Measure the current just after the battery, just before the lamp, just after the lamp, or on the way back: you get the same value everywhere. Why? Because charge cannot pile up or disappear (Lesson 03). If more charge went into the lamp each second than came out, charge would have to be building up inside the lamp, and it does not.

This means the lamp does **not** "use up" current. Current goes in and the same current comes out. What the lamp takes is **energy**, which the charge hands over as it passes through. Lessons 05 and 06 explain how.

Phase 04 (Kirchhoff's Laws) turns this fact into the first of two great rules for whole circuits, Kirchhoff's current law, which also covers circuits with many branches.

### Current flows *through* things

Because current is about charge passing one point, we always say current flows **through** something: through the lamp, through a wire, through the battery. "The current through the lamp" makes sense. "The current at the battery" is a little sloppy. "The current across the lamp" is wrong; Lesson 05 explains which quantity is "across".

This has a very practical consequence. To measure a current, the current has to pass **through the meter**. So you have to open the loop and put the meter (an **ammeter**) in the gap, so that it becomes part of the path. Phase 02 (Lesson 07, Measuring with a Multimeter) shows how, and why connecting it the wrong way can blow the meter's fuse.

### Two arrows for one event: conventional current and electron flow

Here is a historical quirk that confuses everyone at first, so it is best faced now.

Around 1747, Benjamin Franklin imagined electricity as a single invisible fluid, and he decided that it flowed out of the "positive" side and into the "negative" side. When people later drew current in circuits, they followed him: **the arrow goes from plus to minus**, out of the battery's + terminal, round the loop, into the - terminal. This is called **conventional current**.

Then, in 1897, J. J. Thomson discovered the electron, and it turned out that the particles that actually move in wires are negative. Electrons drift the **other way**: out of the minus terminal, round the loop, into the plus terminal. This is **electron flow**.

```
   conventional current:   +  ---->---->---->  -    how diagrams draw it
   electron flow:          +  ----<----<----<  -    what electrons actually do
```

By the time anyone knew, millions of diagrams, books and rules used Franklin's direction, and it does no harm: a negative charge drifting left has exactly the same effect on the circuit as a positive charge drifting right. So the whole world kept the old arrow. **In this course, as in every textbook, current arrows point from plus to minus outside the battery.** Just remember, in the back of your mind, that the electrons themselves drift the other way. Phase 01 (Lesson 08, Current as Moving Charge) explains why the choice makes no difference to any calculation.

### How people talk about current

Engineers use a handful of everyday phrases for current. They all fit the picture of this lesson:

- **"The lamp draws two amps."** The lamp, connected to its source, lets that much current flow through itself. The source does not force a current on it; the loop as a whole decides.
- **"The battery supplies the current."** The battery pushes, and the current flows through it as well, round the whole loop.
- **"A heavy load."** A load that draws a large current. A kettle is a heavy load; an LED is a light one.
- **"The current through the wire."** Always *through*.
- **"It drains the battery."** A large current, kept up for a long time, uses up the battery's energy quickly (Lesson 06).

When you hear these phrases, translate them back into the crowd picture: how much charge is passing each point, each second.

### One direction or back and forth: DC and AC

A battery always pushes the same way, so its current always flows in the same direction round the loop. That is **direct current**, **DC**.

The electricity in a wall socket is different: its push reverses direction many times every second, so the electrons in the wire rock back and forth instead of drifting round. That is **alternating current**, **AC**. It still delivers energy (a rocking crowd can still warm a lamp), and it has big advantages for sending energy over long distances. Phase 09 (Alternating Current) tells the whole story. Until then, almost everything in this course is DC.

## Build It

The program for this lesson counts "crowds of charge" passing a gate, compares currents, shows that the current is the same all round one loop, draws the two arrows and prints the ladder of everyday currents. Run it from the repository root:

```
uv run python phases/00-meet-electricity/04-current-and-amperes/code/main.py
```

### Step 1: Total versus rate

The program counts crowds of charge passing a gate after one, two and three seconds. The total grows; the rate does not.

```python
def count_at_gate(crowds_per_second, seconds):
    return crowds_per_second * seconds
```

### Step 2: Comparing currents

Current is the amount that passed divided by the time it took. The program compares three pairs of wires:

```python
def current(crowds, seconds):
    return crowds / seconds
```

```
  wire C: 4 crowds in 2 s    wire D: 4 crowds in 1 s
    -> wire D carries the bigger current
  wire E: 2 crowds in 1 s    wire F: 6 crowds in 3 s
    -> the same current in both
```

Wire F passed more charge in total, but it took three times as long, so its current is the same as wire E's.

### Step 3: Round the loop

The program lists five points round the flashlight loop and prints the same current at each, with the reminder that the lamp takes energy, not charge.

### Step 4: The two arrows and the ladder

Finally the program draws conventional current and electron flow side by side, and prints the ladder of everyday currents. Try adding devices you know to the ladder, placing them where you think they belong.

## Use It

- **Chargers** are labelled with the most current they can deliver. A phone charger typically says something like "up to two amps"; a laptop charger more. A phone draws only what it needs, up to that limit.
- **Fuses** are labelled with a current. The fuse in a plug or a car is a thin wire chosen to melt if the current through it goes above its rating, opening the circuit before the wiring overheats (Lesson 02).
- **Wires** are chosen by current. Thin wires are fine for the trickle to an LED; the cable to an electric oven is thick because it carries a large current. Phase 03 (Lesson 02, Resistivity and Wires) explains why.
- **Battery life** depends on current. The smaller the current a device draws, the longer its battery lasts. A watch runs for years on a tiny cell because its current is a tiny trickle. Phase 01 (Lesson 01) shows how to estimate battery life from the label.

## Common Mistakes

- **Confusing current with charge.** Charge is an amount; current is an amount *per second*. A big battery stores a lot; that does not mean it pushes a big current.
- **"The lamp uses up the current."** The same current goes in and comes out. The lamp takes energy.
- **"Current is stronger near the battery."** In one loop, the current is the same everywhere.
- **Saying "current across".** Current flows *through* something. (Voltage is the one that is "across", in Lesson 05.)
- **Thinking conventional current is wrong.** It is a direction everybody agrees to draw. It gives exactly the right answers; it just does not show which way the electrons drift.
- **Measuring current by touching a meter to two points.** The current must pass *through* the meter: open the loop and put the meter in the gap (Phase 02, Lesson 07).

## Exercises

1. **Easy.** Which is a current: "this battery holds a lot of charge" or "a lot of charge passes through this lamp each second"? Explain in one sentence.
2. **Easy.** In a single loop with a battery, a switch and a lamp, you measure the current just before the lamp. Where else in the loop would you get the same reading?
3. **Medium.** Add a pair of wires to Step 2 of `main.py` that passed different total amounts of charge but carry the same current. Run it to check.
4. **Medium.** Draw a battery and a lamp in one loop. Add the conventional-current arrows in one colour and the electron-flow arrows in another.
5. **Hard.** A friend says: "The kettle draws a big current, so it must contain more electrons than the phone." What is wrong with that reasoning? Use the words *rate*, *charge* and *energy* in your answer.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| current | "the electricity flowing" | The amount of charge passing a point each second |
| ampere (amp, A) | "how strong the electricity is" | The unit of current: one coulomb of charge passing each second |
| conventional current | "the wrong direction" | The agreed direction for drawing current: from + round the loop to - |
| electron flow | "the real current" | The actual drift of electrons in a metal, from - to +; same effect, opposite direction |
| DC | "battery electricity" | Current that always flows the same way round the loop |
| AC | "mains electricity" | Current that reverses direction many times a second |

## Further Reading

- [The Physics Classroom, "Electric Current"](https://www.physicsclassroom.com/class/circuits/Lesson-2/Electric-Current) — current as a rate, with the conventional direction explained gently.
- [SparkFun, "Voltage, Current, Resistance, and Ohm's Law"](https://learn.sparkfun.com/tutorials/voltage-current-resistance-and-ohms-law) — current next to voltage and resistance, with a water-tank picture (read the water part with this lesson's caveats in mind).
- [Wikipedia, "Ampere"](https://en.wikipedia.org/wiki/Ampere) — the history of the unit, and how it is defined today by fixing the electron's charge.
