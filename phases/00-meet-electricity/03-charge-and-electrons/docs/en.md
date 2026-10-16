# Charge and Electrons

> The wire is already full. The battery does not make electricity; it pushes a crowd that was there all along.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 00 (Meet Electricity), Lessons 01 (What Electronics Is) and 02 (What a Circuit Is)
**Time:** ~45 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| atom | The tiny building block that all ordinary matter is made of | One grain of sand in a beach |
| nucleus | The heavy centre of an atom | The sun at the centre of a solar system |
| proton | A heavy particle in the nucleus with a positive charge | A plus sign glued in place |
| neutron | A heavy particle in the nucleus with no charge | A plain bead with no sign on it |
| electron | A very light particle outside the nucleus with a negative charge; the particle that moves in a wire | A minus sign that can sometimes wander off |
| charge | A property of some particles that makes them push or pull on each other; it comes in two kinds, positive and negative | The "N" and "S" of magnets: a label that decides attract or repel |
| neutral | Having as much positive as negative charge, so the object shows no overall charge | A bank account at exactly zero |
| static electricity | Charge that has piled up on an object and stays there, instead of flowing round a loop | The crackle when you pull off a wool jumper |
| free electron | An electron in a metal that is not tied to one atom and can wander through the material | A guest at a party who drifts from room to room |
| coulomb (C) | The unit for an amount of charge: the name for one very big, fixed crowd of electrons' worth of charge | A "dozen", but for an enormous number |
| drift | The slow, overall movement of the electron crowd along a wire | A crowd shuffling forward in a queue |

## Learning Objectives

- Describe an atom in plain words: a heavy positive centre and light negative electrons
- Explain what charge is, name its two kinds, and say which pairs push apart and which pull together
- Explain why most objects are neutral, and what happens when you rub a balloon on your hair
- Say what is actually moving in a wire, and why the battery does not create it
- Explain what a coulomb is, without numbers, as "a name for a very big crowd"
- Explain how electrons can creep slowly while a lamp lights instantly, and what the "full pipe" picture gets wrong

## The Problem

In Lesson 02 we kept talking about "the flow" going round the loop. But a flow of *what*? Nothing drips out of a cut wire. A wire does not get lighter when it carries electricity for a year. You cannot see anything moving, hear it or smell it. Yet something is clearly happening: the lamp lights the moment you close the switch.

Without a picture of what is moving, everything that follows in electronics is a set of rules to memorise. With the right picture, the rules start to make sense on their own. This lesson gives you that picture: **charge**, carried by tiny particles called **electrons**.

## The Physics

### Inside the atom

Everything around you, the desk, the air, your hand, a copper wire, is made of **atoms**. They are absurdly small: a single grain of sand contains more atoms than there are grains of sand on all the beaches of the Earth.

Each atom has two regions:

```
             -                       - electron (light, negative)
         .-------.
       -  |  + +  |  -               + proton (heavy, positive)
          |  + o  |                  o neutron (heavy, no charge)
         '-------'
             -               the heavy centre is the nucleus
```

- In the centre, the **nucleus**: a tight bundle of **protons** and **neutrons**. It holds almost all the atom's weight.
- Around it, the **electrons**: very light particles, nearly two thousand times lighter than a proton.

The drawing is only a cartoon. Real electrons do not circle like little planets, and the atom is mostly empty space. Phase 01 (Lesson 03, Atoms and Electrons) gives a better picture. For electronics, the cartoon is enough: heavy plus in the middle, light minus around it.

### Charge: the property that pushes and pulls

Protons and electrons carry something called **electric charge**. Charge is not a substance you could pour into a cup; it is a property, the way weight is a property. It comes in exactly two kinds, which we call **positive** (+) and **negative** (-):

- protons are positive
- electrons are negative
- neutrons have no charge at all

Charges act on each other without touching:

```
     + and +   push apart
     - and -   push apart
     + and -   pull together
```

Like charges repel, opposite charges attract. This one rule, which Charles-Augustin de Coulomb measured carefully in 1785, is behind every circuit in this course. Phase 01 (Lesson 04, Electric Charge and Coulomb's Law) turns it into a precise law.

The names "positive" and "negative" were chosen by Benjamin Franklin around 1747, long before anyone knew electrons existed. He had to guess which kind was which, and his guess turned out to be the opposite of convenient: the particles that actually move in wires, the electrons, ended up being the "negative" ones. That old choice still affects how we draw the direction of flow, and Lesson 04 explains how.

### Why most things are neutral

An ordinary atom has as many electrons as protons. The plus and the minus balance exactly, and from outside the atom looks as if it had no charge at all. We say it is **neutral**. A table, a wire or your hand is made of trillions of neutral atoms, so it is neutral too. That is why you do not feel electric pushes and pulls from everyday objects all the time.

But electrons are light, and the outermost ones are not held very tightly. Rub a balloon on your hair and a few electrons are scraped off the hair onto the balloon. Now the balloon has a few electrons too many (it is negative) and your hair has a few too few (it is positive). Opposites attract, so your hair stands up towards the balloon. This is **static electricity**: charge that has piled up somewhere and stays there.

Notice what did *not* happen. No charge was made and none was destroyed. Some electrons simply moved from one place to another. This is one of the most solid facts in physics: **charge is never created or destroyed, only moved around**. It is the deep reason a circuit must be a loop, as we saw in Lesson 02.

The Greek word for amber, *elektron*, is where all of this got its name: rubbed amber was the first known source of static electricity, and Thales noticed it around 600 BC.

## The Concept

### What moves in a wire

In most materials, every electron belongs to an atom and stays there. In metals like copper, something special happens: each atom lets go of one or two of its outermost electrons, and those electrons are free to wander through the whole piece of metal. They are called **free electrons**, and there are enormous numbers of them in every wire.

So a copper wire, sitting in a drawer with nothing connected, is already **full of loose electrons**, wandering about at random in every direction. On average they go nowhere, so nothing happens. The wire is still neutral: the free electrons are exactly balanced by the positive atoms they left behind.

Now connect the wire into a loop with a battery. The battery pushes electrons in at one end of the wire and pulls them out at the other. On top of their random wandering, the whole crowd now **drifts** slowly in one direction, round the loop. That drift is the flow we talked about in Lesson 02, and it is what we call an electric **current**. Lesson 04 is about current.

Three consequences:

1. **The battery does not create electrons.** It does not fill the wire with electricity. The wire was full already. The battery only *pushes*.
2. **The electrons are not used up.** They go round and come back. A flat battery still has all its electrons. What it has run out of is the energy to push them (Lesson 06).
3. **The battery and the wire stay neutral.** For every electron pushed out of one end of the battery, one comes back into the other end.

### Why electrons move and protons do not

If charge comes in two kinds, why do we keep talking about electrons moving and never about protons?

- **Protons are locked in.** They sit in the nucleus, held there by forces far stronger than any battery can overcome. In a solid wire the atoms themselves are locked into a rigid pattern, so their nuclei cannot travel either.
- **Electrons are light and, in metals, loose.** A free electron can wander through the whole wire with only a gentle push.

So in a metal wire, the only thing that ever moves is the electron crowd. The positive atoms stay where they are, like the seats in a stadium while the fans move between them. (In salty water and in batteries, whole charged atoms called ions can move too; Phase 06, Lesson 03, How Batteries Work, looks inside.)

### How much charge? The coulomb

We often need to say "how much charge" passed through something, or "how much charge" is stored in a battery. Counting single electrons is hopeless: there are far too many of them, the way counting grains of sand on a beach is hopeless.

So scientists picked a convenient fixed amount and gave it a name: the **coulomb** (C), after Charles-Augustin de Coulomb. One coulomb is simply the charge of a very, very big crowd of electrons: billions of billions of them. Think of it like the word "dozen": nobody counts eggs one by one in a shop, they count dozens. The coulomb is a "dozen" for electrons, only immensely larger.

That is all you need for now. Phase 01 (Lesson 01, Units and Prefixes, and Lesson 04, Electric Charge and Coulomb's Law) gives the exact size of the crowd and the tools to work with numbers that big.

### A feeling for the size of the crowd

It is worth getting a feeling, without numbers, for how many free electrons there are. Think of the smallest bit of copper wire you can see, a speck at the tip of a pin. It already holds more free electrons than there are grains of sand on every beach of the Earth, and more than there are stars in all the galaxies anyone has counted. A whole wire holds unimaginably more.

That is why the crowd picture works so well: there are so many electrons that their flow is perfectly smooth, like water, even though it is made of separate particles. And it is why we need a unit like the coulomb, and the tools for very large and very small numbers that open Phase 01.

### The slow crowd and the fast push

Here is the puzzle that confuses almost everybody. When you flip a light switch, the lamp lights instantly. Yet each electron in the wire drifts astonishingly slowly: if you could watch one, you would see it creep along more slowly than a snail. Phase 01 (Lesson 08, Current as Moving Charge) works out just how slowly. How can both be true?

The answer is that **the wire is already full**. Picture a long tube packed end to end with marbles. Push one more marble into the left end, and at that same moment a marble pops out of the right end. No single marble travelled the length of the tube. Each one only moved a tiny bit. But the *push* travelled the whole length almost instantly.

```
  push in -->  o o o o o o o o o o o o o o o o  --> one pops out at once
               each marble only shifts a little
```

A bicycle chain is another good picture. When you press the pedal, the back wheel turns at the same moment, although each link of the chain only moves a short distance.

So, in a circuit:

- **what travels fast** is the push, and with it, the energy delivered to the lamp
- **what travels slowly** is each individual electron

### What the picture gets wrong

The marble tube and the bicycle chain are useful, but no picture is perfect, and it is worth knowing where they fail.

- **Marbles touch each other; electrons do not.** Electrons push each other through their charge, from a distance, without ever touching. And the push is not passed from one electron to the next like a row of dominoes: it is spread along the whole wire by something called the **electric field**, which Phase 01 (Lesson 05, The Electric Field) introduces.
- **Marbles sit still; electrons do not.** Even with no battery, free electrons are always buzzing about at random, very fast. The drift is a tiny, slow, overall movement on top of that buzzing, like a swarm of bees slowly drifting with the wind while each bee darts around.
- **A chain is rigid; a crowd is not.** In a real wire, the electrons can bunch up a little, and the push takes a (very short) time to spread. For everyday circuits this time is far too short to notice; for very fast signals it matters, and Phase 21 (PCB Design and Manufacturing) deals with it.

Keep the picture, and keep its limits next to it. That is the habit of this whole course.

## Build It

The program for this lesson prints the parts of an atom, the rule for how charges treat each other, a balloon rubbed on hair (with a small made-up count of electrons, so you can see the bookkeeping), and a tiny animation of a crowd of electrons in a wire. Run it from the repository root:

```
uv run python phases/00-meet-electricity/03-charge-and-electrons/code/main.py
```

### Step 1: The particles

A short list holds each particle's name, charge, weight and where it lives, and the program prints it as a table.

### Step 2: Like and unlike

```python
PAIRS = [
    ("+", "+", "push apart"),
    ("-", "-", "push apart"),
    ("+", "-", "pull together"),
]
```

### Step 3: Bookkeeping for the balloon

```python
def object_charge(protons, electrons):
    difference = protons - electrons
    if difference == 0:
        return "neutral: no overall charge"
    if difference > 0:
        return f"positive: {difference} electrons short"
    return f"negative: {-difference} electrons extra"
```

A real balloon would involve far more electrons than this, but the bookkeeping is the same. The balloon gains exactly the electrons the hair loses. Nothing is created; something is moved.

### Step 4: The crowd in the wire

The wire is drawn as a row of `e` characters, one per electron, with one electron marked `@` so we can follow it. At each step every electron moves one place towards the lamp.

```python
def draw_wire(shift):
    cells = []
    for position in range(WIRE_LENGTH):
        cells.append("@" if position == FOLLOWED + shift else "e")
    return "[battery]=" + "".join(cells) + "=[lamp]"
```

```
  step 0: [battery]=eeeee@eeeeeeeeeeeeeeeeee=[lamp]
  step 1: [battery]=eeeeee@eeeeeeeeeeeeeeeee=[lamp]
  step 2: [battery]=eeeeeee@eeeeeeeeeeeeeeee=[lamp]
  step 3: [battery]=eeeeeeee@eeeeeeeeeeeeeee=[lamp]
```

The wire looks full at every step, because it *is* full. Electrons arrive at the lamp end from the very first step, while the one we are following has crept only a few places. Try making the wire longer: the lamp still responds at the first step.

## Use It

- **Static shocks.** Walk across a carpet in rubber-soled shoes and you collect extra electrons. Touch a metal door handle and they jump across in a tiny spark. Harmless to you, but enough to damage a delicate chip, which is why people who repair electronics wear a strap that keeps them connected to a safe point (Phase 21).
- **Photocopiers and laser printers** use static electricity on purpose: a drum is charged in the pattern of the page, and the toner powder sticks to the charged places.
- **Lightning** is static electricity on a gigantic scale: charge separated inside a storm cloud, finally jumping to the ground.
- **Batteries** are labelled with how much charge they can push round a circuit before running flat, using a unit made from the coulomb. Phase 01 (Lesson 01) teaches you to read that label.

## Common Mistakes

- **"The battery is full of electricity that flows out into the wire."** The wire is already full of free electrons. The battery pushes them; it does not fill anything.
- **"A charged phone has more electrons."** A phone's battery stores *energy* in its chemicals. Its total charge stays balanced, charged or flat. "My phone has no charge" really means "my phone has no energy left".
- **"Electrons race round the circuit at the speed of light."** Each electron creeps. The *push* spreads at nearly the speed of light.
- **"Static electricity is a different kind of electricity."** It is the same charge. The difference is only that it stays put, piled up, instead of flowing round a loop.
- **"Positive charge is the thing that moves in a wire."** In metal wires, the movers are electrons, which are negative. The positive atoms stay locked in place. (Lesson 04 explains why diagrams still draw the flow from plus to minus.)

## Exercises

1. **Easy.** For each pair, say whether they push apart or pull together: two electrons; a proton and an electron; two protons; an electron and a neutron (careful!).
2. **Easy.** In the balloon example, change the program so the balloon gains 5 electrons. What does the program say about the hair? Why must it be so?
3. **Medium.** Explain in two or three sentences, without the word "electricity", why a lamp lights instantly even though electrons move slowly.
4. **Medium.** A friend says "if electrons move so slowly, a very long wire should make the lamp light late". Using the marble tube, explain why this is (almost completely) wrong.
5. **Hard.** Find one way in which the bicycle-chain picture of a circuit is better than the marble-tube picture, and one way in which it is worse.

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| charge | "battery level" | A property of particles, in two kinds (+ and -), that makes them push and pull; it is never used up |
| electron | "electricity" | A light, negatively charged particle; in metals some are free to wander |
| neutral | "no electricity in it" | Equal amounts of positive and negative charge, so no overall charge |
| static electricity | "a different electricity" | Charge piled up on an object and staying put |
| coulomb | "a unit of electricity" | The unit of amount of charge: the charge of one fixed, very large crowd of electrons |
| drift | "electrons flying through the wire" | The slow overall movement of the electron crowd along a wire |

## Further Reading

- [SparkFun, "What is Electricity?"](https://learn.sparkfun.com/tutorials/what-is-electricity) — atoms, charge, static and flowing electricity, with good pictures.
- [Wikipedia, "Electric charge"](https://en.wikipedia.org/wiki/Electric_charge) — the two kinds of charge, conservation of charge and the coulomb, for when you want a little more.
- [Wikipedia, "Drift velocity"](https://en.wikipedia.org/wiki/Drift_velocity) — how slowly electrons really move in a wire; Phase 01 does the numbers.
- [The Nobel Prize in Physics 1906: J. J. Thomson](https://www.nobelprize.org/prizes/physics/1906/thomson/facts/) — the discoverer of the electron.
