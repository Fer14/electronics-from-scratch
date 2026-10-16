# Power and Watts

> Energy is how much. Power is how fast. And the push times the flow tells you how fast.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 00 (Meet Electricity), Lessons 04 (Current and Amperes) and 05 (Voltage and Volts)
**Time:** ~45 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| energy | The ability to make something happen: light, heat, motion, sound; an *amount* | The fuel in a car's tank |
| power | How fast energy is delivered or used; a *rate* | How fast the engine burns the fuel |
| watt (W) | The unit of power, named after James Watt | The "fuel per second" of electricity |
| kilowatt-hour (kWh) | An amount of energy: what a thousand watts uses if it runs for one hour; what your electricity bill counts | One "tankful" on the energy bill |
| rating | The power (or voltage, or current) a device is designed for, printed on its label | The "max load" sign in a lift |
| heat | Energy that ends up warming things; every load makes some | The warmth of a phone charger in your hand |
| resistance | How hard a part makes it for current to get through; a preview, studied in Phase 03 | How narrow a doorway is for a crowd |

## Learning Objectives

- Tell energy (an amount) from power (a rate), and use each word correctly
- Name the watt and say what it measures
- Say in a sentence how volts, amps and watts connect, and use it in one simple example
- Explain energy as power kept up over time, and what a kilowatt-hour on the electricity bill is
- Explain why every load ends up making heat
- Say, as a preview, what resistance is and which phase studies it

## The Problem

Light bulbs are sold by watts. So are kettles, microwaves, chargers and solar panels. The electricity bill counts kilowatt-hours. A phone advert talks about a "big battery" and "fast charging". A laptop charger says it delivers so many watts.

Behind all of these are two ideas that everyday language mixes up all the time: **energy** and **power**. "This battery has more power", "the power is out", "save power": usually the word people mean is *energy*. In electronics each word means one exact thing, and mixing them up leads to wrong answers.

This lesson separates the two, introduces the **watt**, and then, for the first time in the course, shows how the ideas of the last two lessons connect: how the push (volts) and the flow (amps) together decide the power (watts).

## The Physics

From Lesson 05: as charge goes round the loop, the battery gives each bit of it some energy, and the lamp takes that energy and turns it into light and heat. From Lesson 04: current tells us how much charge goes round each second.

Put those two together. Each bit of charge carries some energy (set by the voltage), and a certain amount of charge passes every second (set by the current). So every second, a certain amount of energy is delivered to the lamp. **How much energy arrives each second is the power.**

Where does the energy go in the end? Almost all of it becomes **heat**, sooner or later. A lamp's light warms whatever it shines on. A motor's motion is eventually slowed by friction, which makes heat. Even a computer, which seems to "think", turns essentially all the energy it takes into heat; that is why it has a fan. Phase 01 (Lesson 09, Energy and Power) follows the energy step by step, and Phase 18 (Lesson 07, Heat and Thermal Design) is about getting rid of the heat.

## The Concept

### Energy is an amount, power is a rate

The cleanest picture is a car:

- **Energy** is the fuel in the tank: *how much* there is.
- **Power** is how fast the engine burns it: *how quickly* it is used.

A big tank does not make a car fast. A powerful engine empties even a big tank quickly. In the same way:

- a phone battery stores an **amount of energy**; a bigger battery lasts longer
- a fast charger delivers energy at a higher **rate**, a higher power; it fills the battery sooner

The same pairing appeared in Lesson 04: charge is an amount, current is a rate. Power is to energy what current is to charge.

### The watt

The unit of power is the **watt**, written **W**, named after James Watt, the Scottish engineer whose improved steam engines powered the Industrial Revolution in the late eighteenth century. (He worked on engines, not electricity, but power is power, whether it comes from steam or a battery.)

How big is a watt? In words: it is a modest amount of power, about what you use when you slowly lift a small apple up onto a table, once every second. Everyday devices, roughly:

```
   a small LED indicator      a tiny fraction of a watt
   a phone charging           a few watts to a few tens of watts
   an LED room bulb           around ten watts
   a laptop                   a few tens of watts
   a microwave oven           around a thousand watts
   an electric kettle         two to three thousand watts
```

Anything that heats things quickly (kettles, ovens, hair dryers, heaters) needs a lot of power. Anything that only handles information (an LED indicator, a chip in a remote control) needs very little.

### How volts, amps and watts connect

Now we have all three ideas, each defined on its own:

- **voltage** (volts): how much energy each bit of charge carries round the loop, the push
- **current** (amps): how much charge passes each second, the flow
- **power** (watts): how much energy is delivered each second

Read the first two together and the third follows: if each bit of charge carries a certain energy, and a certain amount of charge passes each second, then the energy delivered each second is the two multiplied together. In a sentence:

> **The power in watts is the voltage in volts multiplied by the current in amps.**

Or, written short:

```
   watts = volts x amps
```

This is the only formula in this phase, and it is worth reading slowly. It says the push and the flow matter **equally**. Double the push with the same flow, and the power doubles. Double the flow with the same push, and the power doubles too.

One example. A lamp in a car (cars run on about 12 volts) draws a current of 2 amps. Its power is

```
   watts = 12 volts x 2 amps = 24 watts
```

Twenty-four watts: the lamp turns energy into light and heat at that rate, every second it is on. (The proper unit for the energy itself, the joule, arrives in Phase 01.)

The same rule explains "fast charging". A charger that agrees with the phone to push harder (more volts), or to deliver a bigger flow (more amps), delivers more watts through the same cable, so the battery fills sooner.

Phase 01 (Lesson 09, Energy and Power) shows exactly where this formula comes from, and Phase 03 (Lesson 05, Power and Heat) uses it to keep parts from burning.

### Power in the height picture

Lesson 05 pictured voltage as height: the battery lifts charge up, and the charge falls back down through the lamp. Power fits that picture nicely. Think of a waterfall turning a water wheel at its foot:

- a **taller** waterfall (more volts) gives each drop more energy to hand over
- **more water** going over each second (more amps) means more drops handing it over

The power of the wheel depends on both: the height *and* the flow. A tiny trickle down a huge cliff can give the same power as a wide river over a small step. That is the sentence "watts are volts multiplied by amps", told as a waterfall.

### Reading a label, in words

Most appliances have a small label or plate, often on the back or underneath. It usually gives two things:

- the **voltage** it is designed for (the push it expects from the wall socket or the charger)
- its **power** in watts (how fast it uses energy when it is on)

From those two, an engineer can work out the current it draws, and so choose a cable and a fuse that can carry it. You will do that arithmetic in Phase 01 (Lesson 09) and Phase 02 (Lesson 02, Batteries and Loads). For now, just get used to looking for the watts: they tell you, at a glance, whether something is a light load like a phone charger or a heavy one like a kettle.

### Energy: power kept up over time

If power is how fast energy is used, then the total energy used depends on two things: how big the power is, and **how long** it is kept up. A lamp left on for two hours uses twice the energy of the same lamp on for one hour. A lamp twice as powerful uses in one hour what the small lamp uses in two.

```
   small lamp, 1 hour      #
   small lamp, 2 hours     ##
   small lamp, 3 hours     ###
   double lamp, 1 hour     ##
```

That is what your electricity bill measures. It counts **kilowatt-hours** (kWh): one kilowatt-hour is the energy used by something drawing a thousand watts for one hour, like a microwave oven running for an hour, or an LED bulb running for about four days. You do not pay for watts (how fast); you pay for kilowatt-hours (how much).

Phase 01 (Lesson 01, Units and Prefixes, and Lesson 09, Energy and Power) introduces the joule, the proper unit of energy, and does the arithmetic of bills and batteries.

### Where the energy goes

Every load is a converter: energy comes in electrically and leaves in some other form.

| Load | Energy goes into | What is wasted (as heat) |
|------|------------------|--------------------------|
| an old filament bulb | a little light, mostly heat | most of it |
| an LED bulb | mostly light | a small part |
| a motor | motion | some, in the windings and the bearings |
| a speaker | sound | almost all of it |
| a heater or a kettle | heat, on purpose | nothing: heat is the goal |
| a charger | energy stored in the phone's battery | a little, which is why it feels warm |
| a computer chip | moving information | essentially all of it, in the end |

"Wasted" does not mean "destroyed". Energy never disappears; it only changes form. It means it ends up as heat we did not want. How much of the incoming energy ends up as the thing we wanted is called **efficiency**. An LED bulb is far more efficient than a filament bulb, which is why it needs so many fewer watts for the same light. Phase 01 (Lesson 09, Energy and Power) and Phase 18 (Power Electronics) put numbers on efficiency.

### What the fuel picture gets wrong

The car picture (energy is fuel, power is how fast it burns) is excellent for separating the two words, but it has one important flaw. Fuel travels *inside* the car. Electrical energy is not carried *inside* the electrons like fuel in a tank, and the electrons do not arrive at the lamp "full" and leave "empty": they creep along slowly and the energy arrives almost instantly (Lesson 03). The energy is passed along by the push itself, through the electric and magnetic effects around the wire. Phase 01 (Lesson 05, The Electric Field) and Phase 08 (Magnetism and Inductors) build this better picture. For now, keep the fuel picture for the words, and remember its limit.

### A preview: resistance

One question is left open. What decides how much current flows through a lamp? The battery sets the push. But two different lamps on the same battery can draw very different currents: one glows brightly, another dimly.

The answer is that every part makes it more or less **hard** for current to get through it. A thin glowing filament makes it hard; a thick copper wire makes it very easy. That property is called **resistance**. For the same push, more resistance means less current, and so less power. The lamp's resistance is also where its energy is turned into heat and light.

Resistance is the subject of a whole phase: Phase 03 (Resistance and Ohm's Law), which also gives the famous rule connecting push, flow and resistance. Until then, "how hard it is to get through" is all you need. It also explains the short circuit of Lesson 02: a bare wire has almost no resistance, so the current becomes huge, and so does the power turned into heat inside the battery.

## Build It

The program for this lesson computes the power of the car lamp, shows what doubling the push or the flow does, draws energy as power kept up over time, and prints the ladder of everyday power. Run it from the repository root:

```
uv run python phases/00-meet-electricity/06-power-and-watts/code/main.py
```

### Step 1: Watts from volts and amps

```python
def watts(volts, amps):
    return volts * amps
```

```
  a 12 V lamp drawing 2 A
  watts = volts x amps = 12 x 2 = 24 W
```

### Step 2: Doubling

The program doubles the push, then the flow, and shows the power doubling each time. The two count equally.

### Step 3: Energy builds up over time

```python
def energy_bar(power_units, hours):
    return "#" * (power_units * hours)
```

Each `#` is the energy of a small lamp running for one hour. The bar grows with time, and a lamp twice as powerful fills it twice as fast.

### Step 4: The ladder

Finally the program prints how much power everyday things use, in words. Try changing the lamp's volts and amps in Step 1 and predict the result before you run it.

## Use It

- **Light bulbs** are labelled in watts: the rate at which they use energy. An LED bulb gives as much light as an old filament bulb for far fewer watts, because the old bulb turned most of its energy into heat instead of light.
- **Chargers** are labelled in watts, or in volts and amps from which you can work out the watts. A higher-watt charger can fill a battery faster, if the device agrees to take it.
- **Electricity bills** count kilowatt-hours: energy, not power. A heater left on all night costs more than a kettle boiled once, although the kettle draws more watts, because the heater runs for much longer.
- **Ratings.** Every part has a maximum power it can safely turn into heat. Small resistors are rated for a fraction of a watt, and Phase 03 shows how to check you stay below it.

## Common Mistakes

- **"This battery has more power."** It has more *energy*. Power is how fast energy is delivered.
- **"Turn it off to save power."** Strictly, you save *energy*. Power is the rate while it is on.
- **Thinking only the voltage matters.** A high voltage with a tiny current can be a small power; a low voltage with a large current can be a big one. It is the product that counts.
- **Paying attention to watts on the bill.** The bill counts kilowatt-hours: power multiplied by how long.
- **Thinking energy "disappears" in a load.** It changes form: to light, motion, sound, and in the end almost all to heat.
- **Mixing "watts" and "watt-hours".** Watts are a rate (how fast). Watt-hours and kilowatt-hours are an amount (how much).

- **Thinking a bigger battery means a faster device.** A bigger battery stores more energy and lasts longer; how fast the device uses energy (its power) is a separate question.

## Exercises

1. **Easy.** Energy or power? "How fast the kettle heats the water", "how much the battery can store", "what the electricity bill counts", "what is printed on a light bulb".
2. **Easy.** Using the sentence "watts are volts multiplied by amps", find the power of a 6 volt lamp that draws 1 amp. (Answer: 6 watts.)
3. **Medium.** Two lamps run on the same battery. One draws twice the current of the other. Which one uses more power, and how much more?
4. **Medium.** A small lamp is on for four hours. A lamp four times as powerful is on for one hour. Which uses more energy? Change Step 3 of `main.py` to check.
5. **Hard.** Explain, using power, why a short circuit across a battery makes the battery hot, even though nothing "useful" is connected. Which phases look at this with real numbers?

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| energy | "power" | An amount: what is stored, delivered or used in total |
| power | "how strong it is" | A rate: how fast energy is delivered or used |
| watt (W) | "how much electricity" | The unit of power; watts equal volts multiplied by amps |
| kilowatt-hour (kWh) | "units of power" | An amount of energy: a thousand watts kept up for one hour |
| resistance | "what slows electricity down" | How hard a part makes it for current to pass; studied in Phase 03 |

## Further Reading

- [SparkFun, "Electric Power"](https://learn.sparkfun.com/tutorials/electric-power) — power, energy and the volts-times-amps rule, with everyday examples.
- [The Physics Classroom, "Electric Power Revisited"](https://www.physicsclassroom.com/class/circuits/Lesson-3/Power-Revisited) — power in circuits, for when you are ready for a little more algebra.
- [Wikipedia, "Kilowatt-hour"](https://en.wikipedia.org/wiki/Kilowatt-hour) — the unit on the electricity bill and how it relates to watts.
- [Wikipedia, "Watt"](https://en.wikipedia.org/wiki/Watt) — the unit and its namesake, James Watt.
