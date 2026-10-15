# What Electronics Is

> Electricity moves energy. Electronics shapes that movement so it carries information.

**Type:** Learn
**Languages:** Python
**Prerequisites:** None. This is where the course starts.
**Time:** ~50 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| electricity | Energy carried from one place to another by tiny charged particles moving through a material | Water in a pipe carrying the push of a pump to a distant water wheel |
| electronics | Using electricity in a controlled way, so that one flow can switch or steer another, usually to handle information | A tap that a person turns on and off to send a message, instead of a hose that just runs |
| energy | The ability to make something happen: heat something, move something, light something | The fuel in a car's tank |
| power | How fast energy is delivered or used | How fast the car burns fuel, not how much fuel it has |
| information | A pattern that means something to whoever receives it | Morse code flashed with a torch |
| signal | A quantity that changes over time in a way that carries information | A traffic light changing colour |
| circuit | A closed path that electricity can travel around and come back to where it started | A running track: you finish where you began |
| component | One part you can buy and put in a circuit (a battery, a lamp, a switch, a resistor) | One Lego brick |
| battery | A component that pushes electricity around a circuit using chemistry | A pump for electric charge |
| switch | A component that opens or closes the path | A drawbridge on the running track |
| mains | The electricity that comes out of the wall socket | The city's water supply |
| transistor | A tiny component where a small electrical signal controls a much bigger flow | A tap you turn with one finger that controls a fire hose |
| integrated circuit (chip) | Many components, often billions, built together on one small piece of silicon | A whole city of Lego built in one piece |

Do not worry about learning these perfectly now. Every one of them comes back, slowly and with numbers, in the next lessons. Lesson 02 is entirely about vocabulary.

## Learning Objectives

- Say in one sentence the difference between electricity and electronics, and give two examples of each
- Explain the two jobs a circuit does: moving energy and moving information
- Walk through what is inside a flashlight and a phone charger, at the level of "this part does this job"
- Place ten key moments of the history of electricity and electronics on a timeline, and say why each mattered
- Describe how this course is organized and what you will be able to build at the end

## The Problem

Look around you right now. Count the things that use electricity: the light in the room, the phone in your pocket, the fridge, the router blinking in the corner, the car key, the watch, the oven clock. Most people find more than twenty within a minute. Every one of them contains a circuit, and almost all of them contain electronics.

And yet, for most people, these objects are black boxes. When a charger stops working, we throw it away. When a recipe online says "use a 220 ohm resistor with your LED", we copy it without knowing why, and if we want a slightly different LED we are stuck. When someone says "this phone has a 4000 mAh battery" or "the chip has 20 billion transistors", the words go past without meaning anything.

This course takes the black box apart. We start from nothing, not even the words, and end up designing a small computer out of logic gates, programming a (virtual) microcontroller, and understanding how chips and circuit boards are made. This first lesson is the map: what electronics is, what it is for, and where we are going.

## The Physics

You will meet the physics properly in Phase 01 (The Physics Underneath). Here is the shortest version, just enough to make the rest of this lesson make sense.

Everything around you is made of atoms. Each atom has a heavy centre (the nucleus) and some very light particles around it called **electrons**. Electrons carry a property called **electric charge**. Charge is what makes them push and pull on each other: two electrons push each other apart, while an electron and a nucleus pull together.

In some materials, mostly metals like copper, some electrons are not tied to any one atom. They wander freely through the metal, like a crowd in a big hall. If you push on that crowd from one end, the whole crowd shifts a little, and the push travels down the wire almost instantly, even though each individual electron moves very slowly (a fraction of a millimetre per second, as you will calculate in Phase 01).

That push, delivered through a wire to a place far away where it does something useful (heats a filament, turns a motor, lights an LED), is what we call **electricity**. A battery or a wall socket is the thing doing the pushing.

Two things are worth noticing already:

1. **Energy moves, the electrons mostly do not.** The electrons in your lamp's wire are the same ones that were there yesterday. What travels from the power station to your lamp is energy, carried by the push.
2. **The path must come back.** The electrons pushed out of one end of a battery have to return to its other end. If the path is broken anywhere, the crowd cannot shift and nothing happens. That closed path is a **circuit**.

## The Concept

### Electricity versus electronics

People often use the two words as if they meant the same thing. They are related, but there is a useful difference.

**Electricity** (or "electrical engineering" in the narrow sense) is about moving **energy**. The questions are: how much energy, how fast, how far, how safely, how cheaply? A power line, an electric heater, a kettle, a car starter motor, the wiring in your house: these are electrical. They are big, they handle lots of energy, and what they do is fairly simple. A kettle is either on or off.

**Electronics** is about **control** and **information**. The defining trick of electronics is a component in which a small electrical signal controls a larger flow. Historically that component was the vacuum tube (from 1904); since 1947 it has been the **transistor**. Once you can make one flow control another, you can build switches that flip other switches, and from those you can build amplifiers, radios, memories, calculators and computers.

Here is a way to remember it:

```
   ELECTRICITY                         ELECTRONICS
   -----------                         -----------
   moves energy                        moves information
   "how much?"                         "which pattern?"
   kettle, heater, power line          phone, radio, computer
   big currents, simple behaviour      tiny currents, rich behaviour
```

The boundary is blurry, and that is fine. Your phone charger is electronic (it has a transistor switching on and off and a chip that measures and decides) but its job is electrical (to deliver energy to the battery). A modern electric car is both: huge electrical motors controlled by sophisticated electronics. In this course we learn both, because you cannot understand the control without understanding the thing being controlled.

### What a circuit does: two jobs

Every circuit you will ever meet does one or both of these two jobs.

**Job 1: move energy.** A battery has energy stored in chemicals. A flashlight bulb turns energy into light (and heat). The circuit is the road the energy travels on.

Let's put numbers on it. Do not worry yet about what the units mean exactly; Lesson 03 (Units and SI Prefixes) explains every one of them, and Phase 01 earns the formulas. For now, read them as a preview.

A common small flashlight uses two AA cells. Each cell gives a push of 1.5 volts (V), and two stacked end to end give

```
   2 cells x 1.5 V = 3.0 V
```

Suppose the bulb lets through a flow (a "current") of 0.25 amperes (A). The rate at which energy is delivered, the **power** in watts (W), is the push times the flow:

```
   power = voltage x current
         = 3.0 V x 0.25 A
         = 0.75 W
```

A watt means one joule (J) of energy every second. In one hour (3600 seconds) the flashlight uses

```
   energy = power x time
          = 0.75 W x 3600 s
          = 2700 J
```

Is 2700 J a lot? Lifting a 1 kg book by 1 metre takes about 9.81 J (its weight times the height). So one hour of flashlight is about 2700 / 9.81 = 275 book lifts. A small amount of energy, delivered steadily, is exactly what a flashlight is for.

**Job 2: move information.** Now imagine you use a small LED (a light-emitting diode, a modern kind of lamp you will study in Phase 11) not to light a room but to send a message, blinking it on and off. Inside a computer, letters are stored as numbers, and numbers as patterns of 0s and 1s (we will build this from scratch in Phase 14). The letter `H` is the number 72, which in binary is `01001000`; the letter `I` is 73, which is `01001001`. If "on" means 1 and "off" means 0, the word `HI` becomes this light pattern:

```
   bits:   0 1 0 0 1 0 0 0   0 1 0 0 1 0 0 1
   light:  . # . . # . . .   . # . . # . . #
```

Suppose the LED needs 2.0 V and 0.02 A when on, and each bit lasts 0.1 s. Only the five `1` bits use energy:

```
   power while on = 2.0 V x 0.02 A = 0.04 W
   energy         = 5 bits x 0.04 W x 0.1 s = 0.02 J
```

The flashlight hour used 2700 J; the message used 0.02 J, that is 135 000 times less. And yet the message is the one that means something. This is the heart of electronics: the energy is tiny, and what matters is the **pattern**. A modern chip moves information using even less: around a millionth of a millionth of a joule per bit.

### A tour of a flashlight

Open an old-style flashlight (a battery one, not a phone) and you find:

```
     +---------------------------------------------+
     |  spring   [ cell ][ cell ]   metal strip    |
     |    ~~~~   (-   +)(-   +)     ===========    |
     |                                    |        |
     |                              switch  bulb   |
     +---------------------------------------------+
```

- **Two cells.** Together they are the battery, the **source** of energy. Each cell has a + end and a - end.
- **A spring** that presses the cells together and touches the - end of the bottom cell.
- **A metal strip** running along the inside of the case, from the spring up to the switch.
- **A switch** that, when slid forward, closes a gap in that strip.
- **A bulb** whose base touches the + end of the top cell, and whose side touches the strip.

Follow the path: + end of the battery, through the bulb, along the metal strip, through the switch, down to the spring, into the - end of the battery. It is a closed loop: a **circuit**. Slide the switch off and the loop is broken; nothing flows and the bulb goes dark. Phase 02 (Your First Circuits) builds exactly this, piece by piece.

A modern LED flashlight looks the same from outside, but inside, between the battery and the LED, there is often a tiny chip called a **driver**. It keeps the LED at the right brightness as the battery runs down, gives you "low / high / strobe" modes when you click the button, and may even warn you when the battery is nearly empty. Same job (move energy), but now with electronics deciding how. That small chip is the difference between an electrical flashlight and an electronic one.

### A tour of a phone charger

A phone charger is a beautiful example because it is small, cheap, everywhere, and full of ideas this course will teach you one at a time. Here is what happens inside, in plain words. Do not try to understand every stage yet; just notice that each one has a clear job.

```
  wall        rectifier       switching        small          output        your
 socket  -->  + capacitor --> transistor -->  transformer --> rectifier --> phone
 230 V AC     ~325 V DC       chops ~100 kHz  steps down      5 V DC
                                   ^                              |
                                   |                              |
                                   +------ feedback chip <--------+
                                          "is it still 5 V?"
```

1. **The wall socket** gives 230 volts in Europe (120 V in North America), and it is **alternating**: the push reverses direction 50 times a second (60 in North America). Phase 09 (Alternating Current) explains why the whole world chose this.
2. **A rectifier and a capacitor** turn the back-and-forth push into a steady one-way push of about 325 V. A rectifier is a set of diodes (Phase 11); a capacitor is a little store of charge (Phase 07).
3. **A switching transistor** chops this high voltage on and off very fast, around a hundred thousand times per second. Phase 12 (Transistors) and Phase 18 (Power Electronics) explain why chopping is the efficient way to do this.
4. **A small transformer** (Phase 08) steps the chopped voltage down and, just as importantly, keeps you physically separated from the dangerous mains: there is no metal path from the wall to the USB plug.
5. **An output rectifier and capacitor** turn the chopped low voltage back into a smooth, steady 5 V.
6. **A feedback chip** measures the output all the time. If the phone draws more and the voltage sags, it tells the switching transistor to stay on a little longer each cycle. This is control: electronics watching and correcting electricity.

Modern fast chargers add one more piece: a chip that **talks** to your phone through the USB cable and negotiates "I can give you 9 V instead of 5 V, do you want it?". Information and energy travel on the same cable.

Numbers again. A charger that gives 5 V at 2 A delivers

```
   output power = 5 V x 2 A = 10 W
```

No machine is perfect. A good small charger is about 85% efficient, which means the output is 85% of what it takes from the wall:

```
   input power = output power / efficiency
               = 10 W / 0.85
               = 11.76 W

   lost as heat = 11.76 W - 10 W = 1.76 W
```

That 1.76 W is why a charger feels warm in your hand. Old chargers from the 1990s used a big heavy transformer at mains frequency and were often only around 50-60% efficient; the switching design is one of the quiet triumphs of modern electronics.

### A tiny history

You do not need history to do electronics, but it helps to know that every idea in this course was once a surprise to someone. Here are the moments we will keep referring back to.

| Year | Who | What happened | Why it matters to us |
|------|-----|---------------|----------------------|
| ~600 BC | Thales of Miletus | Rubbed amber attracts bits of straw | The Greek word for amber, *elektron*, gave us "electricity" |
| 1600 | William Gilbert | Book *De Magnete*; coins the Latin *electricus* | First careful experiments separating electric from magnetic effects |
| ~1747 | Benjamin Franklin | Names the two kinds of charge "positive" and "negative" | His naming is why current is drawn flowing from + to - (Phase 01) |
| 1785 | Charles-Augustin de Coulomb | Measures the force between charges with a torsion balance | The first precise law of electricity (Phase 01, Lesson 02) |
| 1800 | Alessandro Volta | Stacks zinc, copper and brine-soaked cloth: the first battery | First steady flow of electricity; the volt is named after him |
| 1820 | Hans Christian Oersted | A current makes a compass needle turn | Electricity and magnetism are connected (Phase 08) |
| 1820s | André-Marie Ampère | Measures forces between currents | The ampere, unit of current, is named after him |
| 1827 | Georg Ohm | Current depends on the push and on the wire | Ohm's law (Phase 03); the ohm is named after him |
| 1831 | Michael Faraday | A moving magnet makes a current | Generators and transformers (Phase 08) |
| 1882 | Thomas Edison | Pearl Street power station, New York | Selling electricity to homes, with direct current |
| 1888 | Nikola Tesla | Alternating-current induction motor | AC wins the "war of the currents" (Phase 09) |
| 1897 | J. J. Thomson | Discovers the electron | We finally know what is moving (Phase 01) |
| 1904 | John Ambrose Fleming | Vacuum-tube diode | Electronics is born: a one-way valve for current |
| 1947 | Bardeen, Brattain, Shockley | First transistor, at Bell Labs | Small, solid, reliable control of current (Phase 12) |
| 1958 | Jack Kilby (and Robert Noyce, 1959) | First integrated circuits | Many components on one chip (Phase 20) |
| 1971 | Intel | The 4004 processor, about 2300 transistors | A whole computer brain on one chip |

Two patterns jump out of that table.

First, the long silence. From Thales to Gilbert is about 2200 years with very little progress. Then, after Volta's battery in 1800, discoveries come every few years. Why? Because before Volta nobody could make a **steady** flow of electricity; they only had sparks from rubbed amber or glass. A tool that makes an effect steady and repeatable turns a curiosity into a science. Keep that in mind: much of this course is about tools (the multimeter, the oscilloscope, our own simulator) that make invisible things measurable.

Second, the acceleration. The 4004 had about 2300 transistors. Chips today have tens of billions. That growth, roughly doubling every two years for half a century, is called Moore's law, and we look at what it means for chip design in Phase 20.

### How this course is organized

The course has 23 phases. Think of them as five groups.

```
  Foundations            00 Words and Units .......... the language
                         01 The Physics Underneath ... what is really moving
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

Each lesson has the same parts:

- **docs** (what you are reading): words first, then the physics, then the idea with worked numbers.
- **code/main.py**: a short Python program that computes what the lesson explains. You can run it, change numbers and see what happens. From Phase 05 on, the programs use a circuit simulator that we build ourselves, a miniature version of the professional tool SPICE.
- **quiz.json**: a few questions before and after, so you can check yourself.
- **lab** (from Phase 02 on, in most lessons): an interactive task on the course website. You drag components into the empty slots of a small circuit board, press RUN, our simulator solves the circuit, and the task checks whether you met the goal ("make the LED glow without burning it").

You do not need to buy anything. Everything runs on a computer. If you do want to build real circuits later, the course stays at low, safe voltages (12 V or less), and Lesson 06 (Safety First) explains why.

## Build It

The program for this lesson does not simulate a circuit yet. It prints the timeline, works out the flashlight and message numbers from above, tours the charger and lists the course phases. Run it from the repository root:

```
uv run python phases/00-words-and-units/01-what-electronics-is/code/main.py
```

### Step 1: The timeline

We store the events as `(year, description)` pairs, with years before Christ as negative numbers, and print how long ago each one was.

```python
THIS_YEAR = 2026

def years_ago(year):
    return THIS_YEAR - year

def format_year(year):
    return f"{-year} BC" if year < 0 else f"{year} AD" if year < 1000 else str(year)

for year, event in TIMELINE:
    print(f"  {format_year(year):>8}  ({years_ago(year):5d} years ago)  {event}")
years = np.array([year for year, _ in TIMELINE])
gaps = np.diff(years)
```

`np.diff` subtracts each year from the next one, giving the gaps between events. The biggest gap, 2200 years, is the silence between Thales and Gilbert.

### Step 2: The flashlight moves energy

```python
battery_volts = cell_volts * cells
power_watts = battery_volts * bulb_amps
energy_joules = power_watts * seconds
book_lift_joules = 1.0 * GRAVITY * 1.0
```

This prints 3.0 V, 0.75 W, 2700 J and 275 book lifts, the same numbers we worked out by hand.

### Step 3: The same light carries information

```python
def text_to_bits(text):
    return "".join(format(ord(letter), "08b") for letter in text)

def energy_of_message(bits, volts, amps, seconds_per_bit):
    ones = bits.count("1")
    return ones * volts * amps * seconds_per_bit
```

`ord("H")` gives 72, the number a computer uses for the letter H, and `format(72, "08b")` writes it as eight binary digits, `01001000`. The program prints the light pattern `.#..#....#..#..#` and the energy, 20 mJ (millijoules, thousandths of a joule; prefixes like "milli" are Lesson 03).

### Step 4: The charger tour

```python
output_watts = output_volts * output_amps
input_watts = output_watts / efficiency
```

10 W out, 11.76 W in, 1.76 W of heat.

### Step 5: The course map

The program walks through the five groups and numbers the phases from 00 to 22. Try changing `THIS_YEAR`, the bulb current, or the message, and run it again.

## Use It

Where do the two jobs show up in things you own?

- **Mostly energy:** a toaster (about 800-1000 W), an electric kettle (about 2000-3000 W in Europe), a phone charger (5-100 W), the heater in a car seat. They are simple: the interesting questions are "how much power" and "how hot does it get".
- **Mostly information:** a TV remote (the infrared LED blinks a code, using a tiny amount of energy), a Wi-Fi router, a computer mouse, a digital thermometer.
- **Both at once:** an electric car, an induction hob, a laptop power brick that negotiates its voltage over USB, a drone (motor power controlled hundreds of times per second by a small processor).

A real-world number to remember: a USB-C charging port on a modern laptop can deliver up to 100 W in the older standard (20 V at 5 A) and up to 240 W in the newer "extended power range" (48 V at 5 A). Before any of that energy flows, the charger and the laptop exchange messages over the same cable to agree on the voltage. Energy and information, side by side, in one connector.

## Common Mistakes

- **"Electricity flows out of the battery and gets used up."** What gets used up is energy. The charge goes all the way round the circuit and comes back to the battery. A flat battery has not run out of electrons; it has run out of chemical energy to push them with. Phase 01 makes this precise.
- **"Electrons zoom through the wire at the speed of light."** The push travels very fast (a good fraction of the speed of light). The electrons themselves crawl, often less than a millimetre per second. Phase 01, Lesson 06 calculates it.
- **"Electronics is just smaller electricity."** The difference is not size but control. A tiny heater is still electrical; a huge radio transmitter is still electronic.
- **"You need to be good at maths to learn electronics."** You need arithmetic and patience. Every formula in this course is read out as a sentence first, and every calculation is shown step by step.
- **"The history is decoration."** Names like volt, ampere, ohm, coulomb, farad and henry are all people. Knowing who did what makes the units much easier to remember.

## Exercises

1. **Easy.** For each of these, decide whether its main job is energy, information or both: an electric fan, a calculator, a doorbell, a smartwatch, a street lamp with a light sensor. Write one sentence for each.
2. **Easy.** A bicycle light runs on 3 AA cells in a row, each 1.5 V. What is the total push in volts? If its LED draws 0.1 A, what is the power? (Answer: 4.5 V, 0.45 W.)
3. **Medium.** Using the power from exercise 2, how much energy (in joules) does the light use in a 30-minute ride? How many 1 kg book lifts of 1 m is that? (Answer: 0.45 x 1800 = 810 J, about 83 lifts.)
4. **Medium.** Spell the word `OK` in bits (O is 79, K is 75). How many "on" bits are there? With the LED from the lesson (0.04 W while on, 0.1 s per bit), how much energy does it take? Change `message` in `main.py` to check.
5. **Hard.** A laptop charger delivers 65 W to the laptop and is 90% efficient. How much power does it take from the wall, and how much heat does it make? If it runs for 3 hours, how many joules of heat is that? (Answer: 72.2 W in, 7.2 W of heat, about 78 000 J.)

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| electricity | "the stuff in the wires" | The transfer of energy by the push on charged particles in a closed path |
| electronics | "small electrical gadgets" | Circuits where one electrical signal controls another, used to process information |
| circuit | "the wiring" | A closed path around which charge can flow and return to its source |
| power | "how strong it is" | The rate of energy delivery, in joules per second (watts) |
| energy | "power" (often confused) | The total amount of work that can be done, in joules; power x time |
| transistor | "a chip thing" | A component where a small current or voltage controls a larger current; the building block of all modern electronics |
| integrated circuit | "a chip" | Many transistors and other components made together on one piece of silicon |

## Further Reading

- [All About Circuits, Volume I (DC), Chapter 1: Basic Concepts of Electricity](https://www.allaboutcircuits.com/textbook/direct-current/) — a free online textbook written for beginners; good companion for the whole of Phases 00-04.
- Paul Scherz and Simon Monk, *Practical Electronics for Inventors* (4th ed., McGraw-Hill) — Chapter 1 and 2 give a hands-on introduction to the same ideas, with real parts.
- Paul Horowitz and Winfield Hill, *The Art of Electronics* (3rd ed., Cambridge University Press) — the classic reference; too advanced right now, but worth knowing it exists.
- [Computer History Museum, "The Silicon Engine" timeline](https://www.computerhistory.org/siliconengine/timeline/) — the story of the transistor and the integrated circuit, year by year.
