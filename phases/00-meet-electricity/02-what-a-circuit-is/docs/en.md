# What a Circuit Is

> Out and back again. Electricity only does anything when its path makes a complete loop.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 00 (Meet Electricity), Lesson 01 (What Electronics Is)
**Time:** ~45 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| circuit | A path for electricity that leaves a source and comes all the way back to it | A running track: you end where you started |
| closed loop | A circuit with no gaps, so the flow can go round | A track with every section in place |
| open circuit | A circuit with a gap somewhere, so nothing flows anywhere in it | A drawbridge that has been raised |
| short circuit | An accidental shortcut that lets the flow rush from one side of the source to the other without passing through anything useful | A hole in a dam: the water rushes through the hole instead of turning the mill |
| source | The part that gives energy and does the pushing, such as a battery | A pump |
| load | The part that takes energy and turns it into something useful: light, heat, motion, sound | A water wheel turned by the flow |
| battery | A source that pushes using chemistry; it has a plus end (+) and a minus end (-) | A pump with an outlet and an inlet |
| lamp (bulb) | A load that glows when electricity flows through it | A water wheel that glows instead of turning |
| switch | A part that opens or closes a gap in the loop on purpose | A drawbridge you can raise and lower |
| wire | A thin strip of metal, usually wrapped in plastic, that carries the flow from one part to the next | A pipe |
| conductor | A material that lets electricity through easily, such as copper and most metals | An open road |
| insulator | A material that almost completely blocks electricity, such as plastic, rubber, glass or dry wood | A wall across the road |
| terminal | A metal point on a part where a wire can be connected | The two ends of a battery |

## Learning Objectives

- Explain in your own words what a circuit is, and why the path must go out and come back
- Name the four parts of the simplest circuit (battery, wire, lamp, switch) and say what each one does
- Tell a source from a load in any simple device
- Recognise an open circuit (switch off, broken wire, burnt-out lamp) and say what it does to the flow
- Explain why a short circuit is dangerous, even with a small battery
- Close the loop in the course's first lab task

## The Problem

Take a battery and a small lamp. Touch one wire from the lamp to the battery's plus end. Nothing happens. You might think the lamp needs more time, or a bigger battery, or a different lamp. None of that is the problem. The lamp is waiting for the electricity to have a way **back**.

Almost every "it doesn't work" in electronics, from a beginner's first project to a professional's broken circuit board, comes down to the same question: is the path complete? Is there a loop from the source, through the thing we want to power, and back to the source? A single loose wire, a switch left off, a cracked solder joint, and the whole thing goes dark.

This lesson builds the most important picture in the course, the picture every later lesson stands on: the **circuit**, a closed loop.

## The Physics

Lesson 01 gave you the starting picture. A metal wire is full of loose electrons, tiny particles that can wander through the metal. A battery pushes on them. The push moves the whole crowd along at once, and that moving crowd carries energy to the lamp.

Now ask: where does the crowd *go*?

Imagine a ring-shaped corridor packed with people, shoulder to shoulder. If someone at one point pushes gently, the whole ring can shuffle round, because every person has space to step into: the space the person in front just left. Now imagine the corridor is not a ring but a dead end. Push, and the people at the far end are squashed against the wall. Very quickly the crowd pushes back as hard as you push, and everyone stops.

Electricity behaves like the ring. Electrons cannot pile up in one place or vanish into thin air: the electrons pushed out of one end of the battery must be replaced by electrons coming back in at the other end. If there is a ring of metal from one end of the battery to the other, the crowd can circulate, and it keeps carrying energy round for as long as the battery can push. If there is a gap anywhere, the crowd shifts for a tiny moment, gets squashed against the gap, and stops. Lesson 03 looks at the electrons more closely, and Phase 01 (The Physics Underneath) explains *why* they cannot pile up.

That is why the word **circuit** comes from the same root as "circle": the path has to go round and come back.

## The Concept

### The four parts of the simplest circuit

Here is the flashlight from Lesson 01, drawn as a picture rather than as a schematic (we learn the proper symbols in Lesson 07):

```
           wire                      switch
     +--------------------------------o/ o---------+
     |                                             |
  +--+--+                                        .-+-.
  |  +  |                                       ( lamp )
  | bat |                                        '-+-'
  |  -  |                                          |
  +--+--+                                          |
     |                                             |
     +---------------------------------------------+
                         wire
```

- **The battery** is the **source**. It has two terminals, plus (+) and minus (-). It gives energy and pushes the flow round.
- **The wires** are the path. They connect each part to the next and, ideally, do nothing else.
- **The lamp** is the **load**. It takes energy and turns it into light (and some heat).
- **The switch** is the control. It opens and closes a gap in the path on purpose.

Follow the loop with your finger: from the battery's plus terminal, along the top wire, through the switch, down through the lamp, along the bottom wire, and back into the battery's minus terminal. You end where you started. That is a **closed loop**, and the lamp is on.

Every circuit in this course, however big, is made of loops like this one. A phone has millions of them. But each loop follows the same rule: out of the source, through something, back to the source.

### Source and load

Every circuit has at least one part that **gives** energy and at least one that **takes** it.

| Source (gives energy) | Load (takes energy) | What the load makes |
|-----------------------|---------------------|---------------------|
| battery | lamp, LED | light |
| wall socket | heater, toaster, kettle | heat |
| solar panel | motor, fan | motion |
| phone charger | phone battery (while charging) | stored chemical energy |
| bicycle dynamo | bicycle light | light |

Notice the last-but-one row. A phone battery is a *load* while it charges and a *source* when you unplug it. "Source" and "load" are jobs, not kinds of object.

A useful habit: whenever you look at a device, ask "where does the energy come from, and where does it go?". The answer gives you the source and the load, and between them, the loop.

### Conductors and insulators

Why are wires made of metal and wrapped in plastic? Because materials come in two broad families.

A **conductor** lets electricity through easily. Metals like copper, aluminium, silver and gold are conductors, because they are full of loose electrons. Salty water, and your body, conduct too, less well but enough to matter (Lesson 08).

An **insulator** almost completely blocks electricity. Plastic, rubber, glass, ceramic, dry wood and air are insulators: their electrons are held tightly and cannot wander.

A wire is a conductor wrapped in an insulator. The copper inside carries the flow; the plastic outside keeps the flow where we want it and stops it leaking into your fingers or into the wire next to it.

The picture is not perfectly black and white. There is a fascinating family in between, the **semiconductors** such as silicon, which make all of modern electronics possible. Phase 01 (Lesson 07, Conductors, Insulators and Semiconductors) and Phase 11 (Semiconductors and Diodes) are about them.

### The open circuit

An **open circuit** is a loop with a gap in it. The gap can be on purpose or by accident:

- a switch turned off (on purpose)
- a wire that has come loose or broken (accident)
- a lamp whose thin glowing wire has burnt through (accident)
- a strip of plastic, or air, where a wire should be (an insulator is as good as a gap)

The surprising thing about an open circuit is that **one gap stops everything, everywhere in the loop**. The lamp does not get "a bit less". It does not matter whether the gap is next to the battery or next to the lamp, or on the top wire or the bottom one. Since the crowd cannot circulate, it stops all the way round at once.

```
     +-----------------------o/ o-------+
     |                    gap here      |
   [bat]                              (lamp)    nothing flows anywhere
     |                                  |
     +----------------------------------+
```

That is also why one switch is enough to control a lamp, and why a wall switch only needs to break one of the wires going to the ceiling light.

One more thing about an open gap, which we only mention now and study in Lesson 05 and in Phase 02: even though nothing flows, the battery is still *pushing*. The push is still there, waiting across the gap. That is why an "off" light switch at home is still dangerous inside.

### The short circuit: a first warning

A **short circuit** (or just "a short") is the opposite problem. Instead of a gap, there is a **shortcut**: a path of bare metal straight from one side of the source to the other, that skips the load.

```
     +----------------------------------+
     |                                  |
   [bat]========= bare wire ========  (lamp)
     |                                  |
     +----------------------------------+

     the flow rushes through the shortcut instead of the lamp
```

Electricity takes the easiest path it is offered. A lamp is a little hard to get through: that is how it takes energy. A bare wire is very easy. So almost all the flow rushes through the shortcut, the lamp goes dark, and the battery is pushing as hard as it can through nothing but metal. All the energy turns into heat in the battery and the wire. Batteries get hot, swell, leak and, with the lithium batteries in phones and laptops, can even catch fire.

Two things to remember:

- **"Short" does not mean the wire is short.** It means it is a shortcut around the load. A long wire can make a short circuit.
- **Never connect a wire straight across a battery.** Not even a small one, not even "just to see". Lesson 08 (Safety First) explains why even a small battery can be dangerous, and Phase 02 (Lesson 03, Switches, Open and Short Circuits) and Phase 06 (Sources, Batteries and Measurement) look at shorts in detail, with numbers.

### Three states of one loop

Put together, any simple loop is in one of three states:

| State | What the path is like | What flows | The lamp | The battery |
|-------|-----------------------|------------|----------|-------------|
| closed loop | complete, through the load | a steady, sensible flow | on | working normally |
| open circuit | a gap somewhere | nothing at all | off | fine, resting |
| short circuit | a shortcut around the load | far too much | dark | hot, in danger |

Learn to ask which of these three you are looking at. It is the first question an electronics engineer asks when something does not work.

### What a circuit is not

Two common misunderstandings are worth clearing up now.

**The battery does not "send out" electricity that the lamp "eats".** The electrons are not food. They go round and round, out of one terminal and back into the other. What the lamp takes is **energy**, handed over by the push. When the battery is flat, all its electrons are still there; it has simply run out of chemical energy to push with.

**The flow does not go out on one wire and stop at the lamp.** It goes all the way round. There is just as much flow in the wire coming back from the lamp as in the wire going to it. Lesson 04 (Current and Amperes) turns that into a precise idea.

## Build It

The program for this lesson describes a loop as a list of pieces, from the battery's plus end back to its minus end, and checks whether every piece lets the flow through. Run it from the repository root:

```
uv run python phases/00-meet-electricity/02-what-a-circuit-is/code/main.py
```

### Step 1: Which pieces conduct?

A small dictionary says, for each kind of piece, whether the flow can pass through it.

```python
CONDUCTS = {
    "wire": True,
    "closed switch": True,
    "lamp": True,
    "open switch": False,
    "cut wire": False,
    "plastic strip": False,
    "burnt-out lamp": False,
}
```

### Step 2: Look for the first gap

The function walks along the loop and stops at the first piece that does not conduct.

```python
def first_gap(path):
    for position, piece in enumerate(path):
        if not CONDUCTS[piece]:
            return position, piece
    return None
```

If there is no gap, the loop is closed and the lamp is on. If there is one, it is an open circuit, and the program says exactly where the gap is.

### Step 3: Six scenarios

The program tries the flashlight with the switch on, the switch off, a loose wire, a plastic strip in the gap, a burnt-out lamp and, finally, a bare wire straight across the battery. The last one prints the short-circuit warning:

```
=== a wire straight across the battery ===
  a bare wire joins the battery's + and - directly
  the flow takes that easy shortcut instead of going through the lamp
  lamp: dark   battery: gets hot, a short circuit (never do this)
```

### Step 4: Who does what

The program ends by printing the job of each part: source, load, path and control. Try adding a motor or a bell to that list, or invent a new scenario with two gaps.

## Use It

- **A fuse** is a deliberately weak piece of wire inside the loop. If a short circuit happens, the huge flow melts it and creates an open circuit on purpose, which stops everything before anything catches fire. Your home has fuses or circuit breakers for exactly this reason. Phase 02 meets them properly.
- **A light switch at home** is the drawbridge of this lesson: it makes an open circuit when you turn it off.
- **Old fairy lights** were wired as one long loop through every bulb. When one bulb burnt out, it made a gap, and the whole string went dark. Finding the dead bulb was a famous Christmas chore. Modern strings avoid this with a different wiring, which you will understand in Phase 02 (Lesson 04, Series and Parallel Intuition).
- **Battery packs** come with plastic caps, tape on the terminals or a plastic tab you pull out before first use. All of these are insulators, placed there to stop accidental short circuits and open the loop until you are ready.

## Try It in the Lab

The course's web lab has its first task here: **Close the loop**. A battery and a lamp are already wired up, but the top wire has a gap in it and the lamp is dark. You have three pieces to choose from: an empty gap, a strip of plastic and a piece of wire. Drop one into the gap and press RUN.

In the lab the lamp is drawn as a resistor box (a rectangle), because a glowing lamp behaves like one; you will meet resistors in Phase 03. Before you try, follow the loop with your finger and ask, for each piece: would the crowd of electrons be able to get past it?

## Common Mistakes

- **Connecting only one wire.** A lamp touched to only one battery terminal stays dark. Electricity needs a way out *and* a way back.
- **Thinking the flow stops at the lamp.** It goes all the way round. The wire coming back from the lamp carries just as much as the wire going to it.
- **Thinking a gap "far away" doesn't matter.** One gap anywhere in the loop stops the flow everywhere in the loop.
- **Thinking plastic or air can close a gap if it is thin.** At the gentle pushes of everyday batteries, insulators are as good as a gap. (Huge pushes, like lightning, are another story, for later.)
- **Thinking a short circuit is a small or short wire.** It is any shortcut around the load, whatever its length, and it is dangerous.
- **Testing whether a battery is alive by shorting it with a wire.** Never. Use a lamp, or a meter (Phase 02, Lesson 07).

## Exercises

1. **Easy.** For each of these, name the source and the load: a bicycle light, an electric fan, a doorbell, a laptop running on its battery, a laptop charging while switched off.
2. **Easy.** A torch does not light. List four different gaps that could be causing an open circuit.
3. **Medium.** Draw (as a picture, like the one in this lesson) a battery, a switch and a lamp in one loop. Then draw where you would place a second switch so that *either* switch can turn the lamp off.
4. **Medium.** In `main.py`, add a new scenario where the switch is closed but the bottom wire is a "plastic strip". Predict the output before running it.
5. **Hard.** A friend says: "The lamp went dark because the short circuit used up all the electricity before it reached the lamp." What is right and what is wrong in that sentence? Rewrite it correctly in your own words.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| circuit | "the wiring" | A complete loop from a source, through one or more parts, back to the source |
| open circuit | "it's off" or "it's broken" | A gap in the loop: nothing flows anywhere in it |
| short circuit | "a short wire" or "a spark" | A shortcut around the load that lets far too much flow through, turning the energy into heat |
| source | "where the electricity comes from" | The part that gives energy and pushes the flow; the flow also returns to it |
| load | "the thing that uses the electricity" | The part that takes energy and turns it into light, heat, motion or sound |
| conductor | "metal" | A material that lets charge move through it easily |
| insulator | "plastic" | A material in which charge can hardly move at all |

## Further Reading

- [SparkFun, "What is a Circuit?"](https://learn.sparkfun.com/tutorials/what-is-a-circuit) — a short illustrated tutorial on loops, open circuits and short circuits.
- [The Physics Classroom, "What is an Electric Circuit?"](https://www.physicsclassroom.com/class/circuits/Lesson-2/What-is-an-Electric-Circuit) and ["Requirements of a Circuit"](https://www.physicsclassroom.com/class/circuits/Lesson-2/Requirements-of-a-Circuit) — gentle pages, with simple experiments, on why the loop must be complete.
- [Wikipedia, "Short circuit"](https://en.wikipedia.org/wiki/Short_circuit) — what happens in a short and how fuses and breakers protect against it.
