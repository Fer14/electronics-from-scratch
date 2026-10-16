# Safety First

> Current is what hurts, voltage is what pushes it, and heat is what burns. Learn with small batteries, never short them, and never touch the wall socket.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 00 (Meet Electricity), Lessons 02 (What a Circuit Is), 04 (Current and Amperes), 05 (Voltage and Volts) and 06 (Power and Watts)
**Time:** ~35 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| electric shock | Current flowing through your body, in at one point and out at another | Water finding a path through a leaky roof |
| skin resistance | How hard your skin makes it for current to get into your body; high when dry, much lower when wet or cut | A raincoat: dry and whole it keeps water out, soaked or torn it does not |
| mains | The electricity from the wall socket: a strong, alternating push | The water main under the street, as opposed to a bottle of water |
| low voltage | A gentle push, like that of the batteries and USB ports used in this course | A garden hose at low pressure |
| short circuit | A shortcut across a source's terminals (Lesson 02); all the energy turns into heat | Pulling the plug out of a full bath |
| lithium battery | The rechargeable battery inside phones, laptops and vapes; it stores a lot of energy and can catch fire if damaged or shorted | A tightly wound spring |
| capacitor | A part that stores charge and can keep it after the power is removed (Phase 07) | A spring that stays compressed after you let go |
| circuit breaker / RCD | A safety switch in a building that cuts the power when something goes wrong, for example when current leaks through a person | A lifeguard who blows the whistle the moment someone slips |
| earth | The safety wire in home wiring that leads to a metal rod in the soil (Lesson 05) | A lightning rod's cable |

## Learning Objectives

- Explain why current through the body is what causes harm, and why voltage still matters
- Explain why dry skin protects you from small batteries, and why the wall socket is dangerous anyway
- Explain why shorting a battery is dangerous even at a low voltage
- Name the extra dangers of lithium batteries and of charged capacitors
- Follow the safety rules of this course

## The Problem

Electricity gives no warning. You cannot see it, hear it or smell it. A wire carrying nothing and a wire connected to the wall socket look exactly the same. Often the first warning is the injury itself.

At the same time, fear is not useful either. Almost everything in this course runs on small batteries or a USB port, or only inside a simulation, and none of that can hurt you if you follow a few simple habits. This lesson explains, calmly and without numbers, *why* some things are dangerous and others are not, so that the rules make sense instead of being a list to obey.

## The Physics

### What hurts: current

Your body runs on electricity of its own. Nerves send tiny electrical signals; muscles contract when those signals arrive; the heart beats in a precisely timed electrical rhythm. When an outside current flows through your body, it adds its own push to those signals. Muscles in its path contract whether you want them to or not. And the heart, if the current crosses the chest, can lose its rhythm.

What decides how bad this is, is **how much current** flows through you (Lesson 04): how much charge passes each second. Roughly, in words:

```
   a tiny current           not felt at all
   a little more            a tingle
   more                     painful, muscles twitch
   more still               muscles lock: you may not be able to let go
   enough through the chest the heart can lose its rhythm, which can kill
```

The surprising thing is how small "enough" is. A current far smaller than what charges your phone, if it passes through your chest, can stop a heart. Phase 01 (Lesson 01, Units and Prefixes) gives you the tools to put numbers on this, and Phase 03 (Resistance and Ohm's Law) shows how to calculate the current.

### What pushes it: voltage

Current does not flow through you on its own. Something has to push it, and that is **voltage** (Lesson 05). Your body is not an easy path: your skin, especially, makes it hard for current to get in. So whether a dangerous current flows depends on two things at once:

- **how hard the source pushes** (its voltage)
- **how hard your body resists** (mostly your skin)

That is the meaning of an old electricians' saying, roughly "the volts push, the amps hurt". Both matter: no current flows without a push, and no push hurts you without the current it drives.

### Your skin, the raincoat

Inside, your body is salty water and conducts fairly well. Nearly all your protection comes from the outer layer of your skin, which is dry and dead and a decent insulator (Lesson 02). Like a raincoat, it works well when dry and whole, and badly when wet, sweaty or cut.

That is why the small batteries of this course are safe to touch. Their push is too gentle to drive a harmful current through dry skin; you will not even feel it. Even with wet hands you would feel at most a faint tingle.

The wall socket is a different world. Its push is so strong that it can force its way through dry skin, as if tearing the raincoat, and then a dangerous current flows easily. It is also alternating (Lesson 04), which is especially good at disturbing muscles and the heart. **The wall socket can kill. Never touch it, and never open anything that plugs into it.**

### The path matters

Current that enters one finger and leaves through another finger of the same hand mostly stays in the hand. Current that enters one hand and leaves through the other, or through the feet, crosses the chest, and the chest is where the heart is. That is why the path through the body matters so much, and why people who work near dangerous voltages keep one hand away from the equipment, so that a mistake cannot send current from one hand to the other.

Water makes every path easier. Wet skin lets current in far more easily, and standing in water or on a wet floor gives the current an easy way out through the feet. That is why bathrooms and kitchens have the strictest electrical rules in a home, and why you never use mains devices with wet hands.

### Why the wall socket's alternating push is extra harmful

Lesson 04 introduced two kinds of current: direct current (DC), always flowing the same way, as from a battery, and alternating current (AC), reversing direction many times a second, as from the wall socket.

For the body, alternating current is the nastier of the two. Every reversal gives nerves and muscles a fresh kick, so muscles can clamp tight and stay clamped (which is how people end up unable to let go of a live wire), and the steady rhythm of the heart is easily thrown off. The wall socket combines a strong push with this alternating kind of current. Phase 09 (Alternating Current) explains why we still use AC for homes: it is wonderful for sending energy over long distances, and handled properly it is perfectly safe.

### Short circuits: danger without a shock

There is a second kind of danger that has nothing to do with touching: **heat**.

From Lesson 02: a short circuit is a bare-metal shortcut straight across a battery. From Lesson 06: power is how fast energy is delivered, and almost all of it ends up as heat. In a short circuit, nothing slows the current except the inside of the battery itself, so the current becomes huge, and all of the battery's power turns into heat in the battery and the wire, very quickly.

The result does not depend much on the voltage. It depends on how much current the battery is *able* to deliver:

- a small AA cell shorted by a coin in your pocket gets hot enough to burn skin
- a square 9 V battery thrown in a drawer with paper clips can start a fire
- a car battery shorted by a spanner can make the spanner glow red and weld it in place
- a lithium battery from a phone, laptop or vape, shorted or punctured, can overheat, hiss and catch fire, and that fire is very hard to put out

So: **safe to touch does not mean safe to short.** Phase 02 (Lesson 03, Switches, Open and Short Circuits) and Phase 06 (Sources, Batteries and Measurement) look at shorts with real numbers.

### Heat from parts that are working normally

Heat is not only a danger in shorts. From Lesson 06, every load turns its energy into heat in the end, and some parts get hot doing their normal job:

- a soldering iron (Phase 21) is meant to be hot enough to melt metal; it lives in its stand
- a small part asked to handle more power than it is built for can get hot enough to burn a fingertip, or smoke; Phase 03 (Lesson 05, Power and Heat) shows how to check this before you build
- chargers and power supplies are warm in normal use; one that is too hot to hold is a warning sign

### Unplugged is not always safe

Some parts store charge, a bit like a spring stays compressed after you let go. The main one is the **capacitor**, which you will meet in Phase 07 (Capacitors). Large capacitors inside things that plug into the wall (power supplies, TVs, microwave ovens, camera flashes) can keep a dangerous charge for a long time after unplugging. This is one more reason to never open those devices.

### If someone gets a shock

You are very unlikely to need this in a course that stays with small batteries, but it is worth knowing:

- **Do not touch the person** while they may still be in contact with the source: the current could pass through you too.
- **Switch off the power** at the plug, the switch or the breaker, if you can do so safely.
- **Call the emergency services.** An electric shock can disturb the heart even if the person seems fine afterwards, so they should always be checked.

### How buildings protect you

Homes have protection built in, and it uses exactly the ideas of this phase. A **fuse** or **circuit breaker** opens the circuit when the current gets too big, which stops shorts from starting fires (Lesson 02). A safety switch called an **RCD** (in North America, a GFCI) compares the current going out to an appliance with the current coming back. If they differ, some current must be leaking somewhere, perhaps through a person, and it cuts the power in a fraction of a second. And the **earth** wire (Lesson 05) gives fault current a safe path away from metal cases you might touch. Phase 06 and Phase 21 come back to earthing.

## The Concept

### Push and path together

Put the two ideas side by side:

| | Dry skin (a hard path) | Wet or cut skin (an easier path) |
|---|---|---|
| **Low push** (batteries, USB) | nothing felt | at most a faint tingle |
| **High push** (wall socket) | dangerous: the push breaks through | very dangerous |

And, separately, the heat danger:

| Source | Push | Can it hurt you through a touch? | Can it hurt you through a short? |
|--------|------|----------------------------------|----------------------------------|
| one AA cell | low | no | it gets hot, can burn |
| a square 9 V battery | low | no | it gets hot, can start a fire |
| a lithium phone or laptop battery | low | no | yes: fire |
| a car battery | low | no | yes: melting metal, burns |
| a wall socket | high | **yes: it can kill** | yes |

### What you will and will not do in this course

| You will | You will not |
|----------|--------------|
| simulate circuits on your computer and in the web lab | open chargers, power supplies, TVs or microwave ovens |
| use AA packs, 9 V batteries and USB power, if you build for real | work on anything connected to the wall socket |
| use battery holders and switches | connect wires straight across batteries |
| disconnect before changing a circuit | touch parts that are smoking or very hot |
| calculate power before you build (from Phase 03 on) | guess and hope |

### The rules of this course

1. **Stay low.** Use batteries (AA packs, a 9 V battery) or USB power, at 12 volts or less. Every lab and simulation in the early phases is designed for this range.
2. **Never open or modify anything that plugs into the wall**, not even when unplugged: capacitors may still be charged.
3. **Never connect a wire straight across a battery.** Keep loose batteries in their packaging or a case, away from keys and coins. Use battery holders.
4. **Respect lithium batteries.** Do not puncture, crush, bend or heat them. Do not use a swollen, dented or hot one. If one hisses or smokes, move away from it.
5. **Disconnect before you change.** Unplug the battery, change the circuit, then reconnect.
6. **If something gets hot, smells or smokes, disconnect first, think later.** Do not grab the hot part.
7. **When in doubt, simulate first.** This course is simulation-first: you can do almost every lesson without touching a real circuit. From Phase 05 on we have our own simulator, and the web lab lets you try circuits that would be dangerous or wasteful to build, safely.

### A calm word

None of this is meant to scare you away. Electricity has been understood and tamed for more than a century; with a few habits, it is one of the safest things you can learn to work with. The habits are short: stay low, never short, never open mains devices, disconnect before you change, and simulate first. Everything else in this course builds on top of them.

### Why this course is simulation-first

Most of what this course teaches can be learned without touching a single real wire. Each lesson's program runs on your computer, the web lab lets you drop parts into a circuit and press RUN, and from Phase 05 on you will have your own circuit simulator. In a simulation you can short a battery, connect a part backwards or push far too much current through a lamp, and see exactly what *would* happen, with nothing getting hot.

That is not a replacement for building real circuits one day, which is great fun. It is a way to make your mistakes where they are free, and to arrive at the bench already knowing what to expect.

## Build It

The program for this lesson prints the ladder of what current does to a body, the push-and-path table, the everyday sources with a verdict for each, and the rules. Run it from the repository root:

```
uv run python phases/00-meet-electricity/08-safety-first/code/main.py
```

### Step 1: Push and path

A small function combines how strong the push is with how easy the path through the skin is:

```python
def push_and_path(push, path_is_easy):
    if push == "high" and path_is_easy:
        return "large current through you: very dangerous"
    if push == "high":
        return "the high push can break through dry skin: still dangerous"
    if path_is_easy:
        return "the push is too small to drive a harmful current through skin"
    return "nothing felt"
```

### Step 2: Everyday sources

Each source is listed with its push, how much current it could deliver into a short, and a verdict. Notice that "safe to touch" and "safe to short" are two different columns: a car battery is gentle on your skin and ferocious in a short.

### Step 3: The rules

The program ends by printing the seven rules. Keep them somewhere you can see them.

## Use It

- **Safety labels.** Chargers and power supplies carry symbols showing they are designed so that the low-voltage side (the USB plug) is safely separated from the mains. That separation is why you can touch a USB plug. Very cheap fake chargers sometimes skip it, which is why they cause injuries.
- **Battery shipping rules.** Lithium batteries must travel with their terminals protected and are not allowed in checked luggage on planes, because a short or a crushed battery can start a fire.
- **Fuses in cars** protect every circuit from shorts. Car batteries cannot shock you, but they can deliver enough current to start a fire in the wiring.
- **Smoke alarms and fire blankets** belong near any bench where real circuits are built, mostly because of lithium batteries.
- **Electricians' habits.** Professionals switch off and test before touching, work with one hand when they must work near live parts, and use tools with insulated handles. You will not need these at 12 volts, but it is good to know they exist.

## Common Mistakes

- **"Low voltage means harmless."** For shocks, mostly true with the batteries of this course. For shorts and heat, false: a small battery shorted can burn, and a lithium battery can catch fire.
- **"Voltage alone kills."** It is the current through you that does the harm. But the voltage decides whether that current can flow, so a high voltage is always a warning sign.
- **"Unplugged means safe."** Capacitors in mains equipment can stay charged long after unplugging.
- **"I'll just test the battery on my tongue."** Your tongue is wet, and wet skin lets current in easily. It is a bad habit even with a 9 V battery. Use a lamp, or a meter (Phase 02, Lesson 07).
- **Grabbing a smoking part.** Disconnect the power first; a hot part stays hot for a while.

- **Ignoring warmth.** A battery, a charger or a part that is getting hotter than usual is telling you something. Disconnect and find out why.

## Exercises

1. **Easy.** In one sentence each: what does the current do to the body, and what does the voltage do?
2. **Easy.** Why can you touch both ends of a 9 V battery with dry fingers and feel nothing?
3. **Medium.** A friend keeps loose AA batteries in the same pocket as their keys. Explain the danger using the words *short circuit*, *current* and *heat*.
4. **Medium.** Explain why a car battery is safe to touch but dangerous to short, using the two tables of this lesson.
5. **Hard.** An RCD compares the current going out to an appliance with the current coming back. Using Lesson 04 (the same current all round a loop), explain why a difference between the two means something is wrong.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| electric shock | "getting zapped by voltage" | Current flowing through the body; voltage is what pushes it |
| skin resistance | "being insulated" | How hard dry skin makes it for current to enter; much lower when wet or cut |
| short circuit | "a spark" | A shortcut across a source: a huge current and fast heating, even at low voltage |
| mains | "the electricity" | The strong alternating push of the wall socket; dangerous to touch |
| RCD / GFCI | "the trip switch" | A safety switch that cuts the power when outgoing and returning currents differ |
| lithium battery | "just a battery" | A battery that stores a lot of energy in a small space; shorted, crushed or punctured it can catch fire |
| capacitor | "a part that is off when unplugged" | A part that stores charge and can keep it after the power is removed (Phase 07) |
| earth | "ground" | The safety wire of home wiring, leading to the soil; not the same as a circuit's ground |

## Further Reading

- [UK Health and Safety Executive, "Electricity at work"](https://www.hse.gov.uk/electricity/index.htm) — practical guidance on electrical hazards and how they are controlled.
- [Wikipedia, "Electrical injury"](https://en.wikipedia.org/wiki/Electrical_injury) — what current does to the body, and why the path through the chest matters.
- [Battery University, "BU-304a: Safety Concerns with Li-ion"](https://batteryuniversity.com/article/bu-304a-safety-concerns-with-li-ion) — why lithium batteries fail and how to handle them.
- [Wikipedia, "Mains electricity"](https://en.wikipedia.org/wiki/Mains_electricity) — what comes out of the wall socket around the world.
