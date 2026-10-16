# What Electronics Is

> Electricity carries energy from one place to another. Electronics decides what that energy does, and uses it to carry meaning.

**Type:** Learn
**Languages:** Python
**Prerequisites:** None. This is where the course starts.
**Time:** ~40 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| energy | The ability to make something happen: warm something, move something, light something | The fuel in a car's tank |
| electricity | Energy carried from one place to another by tiny particles being pushed along a material, usually a metal wire | A pump pushing water round a garden pipe to turn a little wheel far away |
| electronics | Using electricity in a controlled way, so that one small electrical flow can switch or steer another, usually to handle information | A tap: a small turn of your hand controls a big flow of water |
| information | A pattern that means something to whoever receives it | A message flashed with a torch: long, short, long |
| signal | Something that changes over time in a way that carries information | A traffic light changing colour |
| circuit | A closed path that electricity travels round, coming back to where it started | A running track: you finish where you began |
| component | One part you can buy and put in a circuit: a battery, a lamp, a switch | One Lego brick |
| battery | A component that uses chemistry to push electricity round a circuit | A pump |
| lamp (bulb) | A component that turns electrical energy into light (and some heat) | The light at the end of the pipe |
| switch | A component that opens or closes the path | A drawbridge on the running track |
| transistor | A tiny component in which a small electrical signal controls a much bigger flow | A tap you can turn with one finger that controls a fire hose |
| chip | Many components, often billions of transistors, made together on one small piece of silicon | A whole Lego city built as a single piece |

Do not try to memorise these now. Each one comes back, slowly, in the lessons of this phase. This first lesson is a map: where electricity is, what electronics adds, where the ideas came from, and where the course is going.

## Learning Objectives

- Say in one sentence the difference between electricity and electronics, and give two examples of each
- Explain, without any numbers, what is actually moving in a wire and what is being delivered
- Walk through a flashlight and a phone charger at the level of "this part does this job"
- Place the key moments of the history of electricity on a timeline, from rubbed amber to the chip, and say why each one mattered
- Describe how this course is organised and which phase answers which question

## The Problem

Look around you for one minute and count the things that use electricity. The lights. The phone in your pocket. The fridge humming in the kitchen. The router with its little blinking lights. The oven clock, the car key, the doorbell, the watch on your wrist. Most people pass twenty before the minute is up.

Every one of those objects contains a circuit, and almost all of them contain electronics. Yet for most of us they are closed boxes. When a charger stops working we throw it away. When a tutorial says "put a resistor before the LED" we copy it without knowing why. When an advert says a chip has "billions of transistors", the words pass by without meaning anything.

This course opens the boxes, one at a time, starting from nothing at all: not even the words. By the end you will understand how a circuit works, simulate circuits with a tool you write yourself, build a small computer out of logic gates, and see how chips and circuit boards are designed. This first lesson draws the map.

## The Physics

Everything around you is made of **atoms**, unimaginably small building blocks. Each atom has a heavy centre and, around it, much lighter particles called **electrons**. Electrons carry something called **electric charge**, which makes them push and pull on other charged things. Lesson 03 of this phase looks at electrons and charge in plain words, and Phase 01 (The Physics Underneath) opens the atom properly.

In metals such as copper, some electrons are not tied to any one atom. They wander freely through the metal, like a crowd milling around in a big hall. A copper wire is therefore always full of these loose electrons, even when nothing is connected to it.

Now connect a battery to the two ends of the wire through a lamp. The battery pushes on that crowd. The whole crowd shuffles along together, all the way round the loop, and the push is felt at the lamp almost instantly. The lamp turns some of the energy of that push into light. That is electricity: **energy delivered by pushing a crowd of charged particles round a path**.

Two things are worth noticing right away, because beginners often get them backwards:

1. **The energy travels; the electrons barely move.** The electrons in your desk lamp's wire are mostly the same ones that were there yesterday. What arrives at the lamp is energy, carried by the push. Lesson 03 explains why this is not a contradiction.
2. **The path has to come back.** The crowd can only shuffle along if it has somewhere to go, and the only place it can go is back to the battery. Break the path anywhere and everything stops. That closed path is a **circuit**, and Lesson 02 is all about it.

## The Concept

### Electricity versus electronics

People often use the two words as if they were the same. They are related, and the line between them is blurry, but the difference is worth having in your head.

**Electricity**, in the narrow sense, is about **moving energy**: getting it from where it is produced to where it is used, safely and without wasting much. Power lines, the wiring inside your walls, an electric heater, a kettle, a toaster, a car's starter motor. These things handle a lot of energy, but what they *do* is simple. A kettle is on or off.

**Electronics** is about **control** and **information**. Its central trick is a component in which a small electrical signal controls a larger flow. In the early twentieth century that component was the vacuum tube, a glowing glass valve. Since 1947 it has been the **transistor**. Once one flow can control another, you can build switches that flip other switches, and from those you can build amplifiers, radios, memories, calculators and computers.

```
   ELECTRICITY                        ELECTRONICS
   -----------                        -----------
   moves energy                       moves information
   asks "how much?"                   asks "which pattern?"
   kettle, heater, power line         phone, radio, computer
   big flows, simple behaviour        small flows, rich behaviour
```

The boundary really is blurry, and that is fine. Your phone charger is full of electronics (it has a transistor switching very fast and a small chip that measures and decides), but its *job* is electrical: deliver energy to the battery. An electric car is both at once: huge electric motors, steered by sophisticated electronics. This course teaches both, because you cannot understand the control without understanding the thing being controlled.

### The same light, two jobs

Picture a small torch. Switch it on and leave it on, and it lights the path in front of you. Its job is to deliver energy as light, steadily, for as long as possible. That is electricity at work.

Now use the same torch to send a message across a dark field: on, off, on-on, off. The torch uses hardly any energy for this. What matters is not how much light, but **the pattern** of on and off. Your friend on the other side reads the pattern and understands the message. That is the heart of electronics: the energy is tiny, and the meaning lives in the pattern.

Inside a computer, everything (letters, photos, music) is stored as long patterns of "on" and "off", which we write as 1 and 0. Phase 14 (Digital Logic) builds this up from scratch. For now, keep the picture of the torch: one job is *how much*, the other is *which pattern*.

### A tour of a flashlight

Open an old-style battery flashlight and you find just a few parts:

```
     +-----------------------------------------------+
     |  spring   [ cell ][ cell ]   metal strip      |
     |   ~~~~    (-   +)(-   +)    ============      |
     |                                   |           |
     |                              switch   bulb    |
     +-----------------------------------------------+
```

- **Two cells**, the batteries. They are the **source** of the energy. Each has a plus end and a minus end.
- **A spring** that presses the cells together and touches the minus end of the bottom cell.
- **A metal strip** inside the case, running from the spring up towards the front.
- **A switch** that, when you slide it, closes a gap in that strip.
- **A bulb**, the lamp, which touches the plus end of the top cell and the metal strip.

Follow the path with your finger: out of the battery's plus end, through the bulb, along the strip, through the switch, down to the spring, back into the battery's minus end. A closed loop: a circuit. Slide the switch off and the loop is broken; the bulb goes dark. Lesson 02 draws this loop and names every part of it.

A modern LED flashlight looks the same from outside, but between the battery and the light there is often a tiny chip called a **driver**. It keeps the light steady as the battery runs down, gives you "low, high, blink" modes when you click the button, and may warn you when the battery is nearly empty. Same job (deliver energy), but now electronics decides *how*. That small chip is the difference between an electrical flashlight and an electronic one.

### A tour of a phone charger

A phone charger is small, cheap and everywhere, and it is full of ideas this course will teach you one by one. Here is what happens inside, in plain words. Do not try to understand every stage; just notice that each has one clear job, and which phase explains it.

```
  wall       smooth it     chop it        step it       smooth it     your
 socket --> one way    --> very fast  --> down     --> again     --> phone
                               ^                            |
                               |                            |
                               +---- a small chip checks <--+
                                     "is the output right?"
```

1. **The wall socket** gives a strong push that flips direction back and forth many times a second. This is called alternating current, and Phase 09 (Alternating Current) explains why the whole world chose it.
2. **The first stage** makes the push go in one direction only and smooths it. It uses diodes (Phase 11) and capacitors (Phase 07).
3. **A transistor** switches that push on and off extremely fast. Phase 12 (Transistors) and Phase 18 (Power Electronics) explain why chopping is the efficient way to change voltage.
4. **A small transformer** (Phase 08) steps the push down to a gentle level and, just as important, keeps you separated from the dangerous wall supply: there is no metal path from the socket to the USB plug.
5. **The output stage** smooths the chopped push back into a steady, gentle supply for the phone.
6. **A small chip** watches the output all the time. If the phone asks for more and the output starts to sag, it tells the transistor to stay on a little longer each time. That is electronics watching and correcting electricity.

Modern fast chargers add one more piece: a chip that **talks** to your phone through the cable to agree on how strong a push to deliver. Energy and information, travelling side by side in one cable.

No machine is perfect. A little of the energy taken from the wall turns into heat inside the charger instead of reaching the phone. That is why a charger feels warm in your hand. Phase 18 (Power Electronics) is about keeping that waste small.

### A short history

You do not need history to do electronics, but it helps to know that every idea in this course was once a surprise to somebody, and that many units are named after people. Here are the moments we will keep coming back to.

| Year | Who | What happened | Why it matters to us |
|------|-----|---------------|----------------------|
| ~600 BC | Thales of Miletus | Rubbed amber attracts bits of straw | The Greek word for amber, *elektron*, gave us "electricity" |
| 1600 | William Gilbert | Book *De Magnete*; coins the Latin word *electricus* | First careful experiments telling electric and magnetic effects apart |
| ~1747 | Benjamin Franklin | Names the two kinds of charge "positive" and "negative" | His naming is why current is drawn flowing from plus to minus (Lesson 04) |
| 1785 | Charles-Augustin de Coulomb | Measures the force between charges | The coulomb, the unit of charge, is named after him (Lesson 03) |
| 1800 | Alessandro Volta | Stacks zinc, copper and salty cloth: the first battery | The first steady flow of electricity; the volt is named after him (Lesson 05) |
| 1820 | Hans Christian Oersted | A current makes a compass needle turn | Electricity and magnetism are linked (Phase 08) |
| 1820s | André-Marie Ampère | Studies the forces between currents | The ampere, the unit of current, is named after him (Lesson 04) |
| 1827 | Georg Ohm | Shows how the flow depends on the push and on the wire | Ohm's law and the ohm (Phase 03) |
| 1831 | Michael Faraday | A moving magnet makes a current | Generators and transformers (Phase 08) |
| 1882 | Thomas Edison | Opens a power station in New York | Selling electricity to homes |
| 1888 | Nikola Tesla | Patents the alternating-current motor | Alternating current wins (Phase 09) |
| 1897 | J. J. Thomson | Discovers the electron | At last we know what is moving in the wire (Lesson 03, Phase 01) |
| 1904 | John Ambrose Fleming | The vacuum-tube diode | Electronics is born: a one-way valve for current |
| 1947 | Bardeen, Brattain and Shockley | The first transistor | Small, solid, reliable control (Phase 12) |
| 1958 | Jack Kilby (and Robert Noyce, 1959) | The first integrated circuits | Many components on one chip (Phase 20) |
| 1971 | Intel | The 4004, a whole processor on one chip | A computer's brain on a fingernail |

James Watt does not appear in the table because his famous work was on steam engines, not electricity, but the unit of power, the watt, carries his name. You will meet it in Lesson 06.

Two patterns jump out of that table.

**The long silence.** From Thales to Gilbert is more than two thousand years with almost no progress. Then, after Volta's battery in 1800, discoveries arrive every few years. Why? Before Volta, nobody could make a *steady* flow of electricity; they only had sparks from rubbed amber or glass. A tool that makes an effect steady and repeatable turns a curiosity into a science. Much of this course is about such tools: meters, oscilloscopes and our own simulator, which make invisible things visible.

**The acceleration.** The first chips held a handful of transistors. Chips today hold tens of billions, and that growth, doubling again and again for half a century, is the story of Phase 20 (Chip Design).

### How this course is organised

The course has 23 phases. Think of them as five groups.

```
  Foundations            00 Meet Electricity ......... the big ideas, in words
                         01 The Physics Underneath ... atoms, fields, and the numbers
                         02 Your First Circuits ...... loops, batteries, switches
                         03 Resistance and Ohm's Law . the first real rule
                         04 Kirchhoff's Laws ......... rules for whole circuits
                         05 Circuit Analysis ......... we build our own simulator
                         06 Sources and Measurement .. real batteries, real meters

  Energy stores          07 Capacitors
  and waves              08 Magnetism and Inductors
                         09 Alternating Current
                         10 Filters and Resonance

  Active parts           11 Semiconductors and Diodes
                         12 Transistors
                         13 Operational Amplifiers

  Digital                14 Digital Logic
                         15 Sequential Logic
                         16 A Computer from Gates
                         17 Microcontrollers

  Real systems           18 Power Electronics
                         19 Sensors and Signals
                         20 Chip Design
                         21 PCB Design and Manufacturing
                         22 Capstone
```

This phase, Meet Electricity, is deliberately gentle. It introduces the big ideas (circuit, charge, current, voltage, power, schematic, safety) in plain words, with as few numbers as possible. Phase 01 then opens the box and starts calculating.

Every lesson has the same parts:

- **docs** (what you are reading): the new words first, then the idea, then where it shows up in real life.
- **code/main.py**: a short Python program that prints or computes what the lesson explains. You can run it, change it and run it again. From Phase 05 on, the programs use a circuit simulator that we build ourselves.
- **quiz.json**: a few questions before and after, to check yourself.
- **lab** (in some lessons): an interactive task in the course's web lab, where you drop parts into the empty slots of a small circuit and see whether it works. The first one is in the next lesson.

You do not need to buy anything. Everything runs on a computer. If you later build real circuits, the course stays with small batteries and safe, low voltages, and Lesson 08 (Safety First) explains why.

## Build It

The program for this lesson does not simulate anything yet. It prints the timeline, sorts some everyday objects into "mostly energy" and "mostly information", and prints the map of the course. Run it from the repository root:

```
uv run python phases/00-meet-electricity/01-what-electronics-is/code/main.py
```

### Step 1: The timeline

Each event is a pair: a year and a sentence. Years before Christ are stored as negative numbers, and a small function writes them nicely.

```python
def format_year(year):
    if year < 0:
        return f"{-year} BC"
    return str(year)

for year, event in TIMELINE:
    print(f"  {format_year(year):>7}  {event}")
```

The program also finds the longest quiet gap between two events: the two thousand years between Thales and Gilbert.

### Step 2: Energy or information?

Each everyday object gets a label: `energy`, `information` or `both`. The program groups them and prints each group.

```python
for job, heading in (("energy", "mostly energy"), ("information", "mostly information"), ("both", "both at once")):
    names = [name for name, label in GADGETS if label == job]
    print(f"  {heading:<19} {', '.join(names)}")
```

### Step 3: The torch message

The program turns a short word into a pattern of on and off, using `#` for "light on" and `.` for "light off", so you can see that the meaning lives in the pattern, not in the amount of light.

### Step 4: The course map

The program walks through the five groups and numbers the phases from 00 to 22. Try adding your own gadgets to the list in Step 2 and run it again.

## Use It

Where do the two jobs show up in things you own?

- **Mostly energy:** a toaster, an electric kettle, a heater, the heated seat of a car, a charger. The interesting questions are "how much" and "how hot does it get".
- **Mostly information:** a TV remote (an invisible light blinking a code), a Wi-Fi router, a computer mouse, a digital thermometer.
- **Both at once:** an electric car, an induction hob, a laptop charger that agrees with the laptop on how hard to push before it starts, a drone whose motors are adjusted hundreds of times a second by a tiny computer.

Next time you plug in a modern laptop, remember that before any energy flows, the charger and the laptop exchange messages over the same cable. Energy and information, side by side, in one connector.

## Common Mistakes

- **"Electricity flows out of the battery and gets used up."** What gets used up is energy. The electrons go all the way round the circuit and come back to the battery. A flat battery has not run out of electrons; it has run out of the chemical energy it uses to push them. Lessons 03 and 06 come back to this.
- **"Electrons zoom through the wire at the speed of light."** The *push* travels astonishingly fast. The electrons themselves crawl. Lesson 03 explains how both can be true.
- **"Electronics is just smaller electricity."** The difference is control, not size. A tiny heater is still electrical; a huge radio transmitter is still electronic.
- **"You need to be good at maths to learn electronics."** You need patience and arithmetic. This phase uses almost no maths at all, and later every formula is told as a sentence first.
- **"The history is decoration."** The volt, the ampere, the ohm, the coulomb and the watt are all people. Knowing who did what makes the names much easier to remember.

## Exercises

1. **Easy.** For each of these, decide whether its main job is energy, information or both, and write one sentence why: an electric fan, a calculator, a doorbell, a smartwatch, a street lamp that switches on by itself at dusk.
2. **Easy.** Name one object in your home where you think a small chip controls a bigger flow of energy. What decision is the chip making?
3. **Medium.** Look at the timeline. Which single invention do you think made the most later discoveries possible, and why? (There is no single right answer; the lesson suggests one.)
4. **Medium.** Change the message in `main.py` to your own name and run it. Does a longer name use "more information"? Does it need "more energy"? Are those the same question?
5. **Hard.** Pick any gadget you own and, using the charger tour as a model, guess its stages: where does the energy come from, what changes it, what part decides, and what comes out? Keep your guess; by Phase 18 you will be able to check it.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| electricity | "the stuff in the wires" | Energy delivered by pushing charged particles round a closed path |
| electronics | "small electrical gadgets" | Circuits where one electrical signal controls another, usually to handle information |
| circuit | "the wiring" | A closed path round which charge flows and returns to its source |
| energy | "power" (often confused) | The ability to make something happen; what a battery stores and a lamp uses |
| transistor | "a chip thing" | A component where a small signal controls a larger flow; the building block of modern electronics |
| chip | "the computer bit" | Many transistors and other components made together on one piece of silicon |

## Further Reading

- [SparkFun, "What is Electricity?"](https://learn.sparkfun.com/tutorials/what-is-electricity) — a friendly illustrated introduction to charge, fields and flow, good company for this whole phase.
- [Computer History Museum, "The Silicon Engine" timeline](https://www.computerhistory.org/siliconengine/timeline/) — the story of the transistor and the chip, year by year.
- [The Nobel Prize in Physics 1956](https://www.nobelprize.org/prizes/physics/1956/summary/) — the prize for the invention of the transistor, with background on Bardeen, Brattain and Shockley.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors* (4th ed., McGraw-Hill) — the early chapters give a hands-on introduction to the same ideas, with real parts.
