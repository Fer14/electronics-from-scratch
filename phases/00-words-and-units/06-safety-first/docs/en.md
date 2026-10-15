# Safety First

> Voltage is the push, current is what hurts, and heat is what burns. Stay at 12 V DC, never short a battery, and never open anything that plugs into the wall.

**Type:** Learn
**Prerequisites:** Phase 00 (Words and Units), Lesson 02 (The Vocabulary), Lesson 03 (Units and SI Prefixes) and Lesson 04 (Scientific Notation and Orders of Magnitude)
**Time:** ~50 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|------|---------------|------------------|
| electric shock | current flowing through your body from one point of contact to another | water finding a path through a leaky roof |
| body resistance | how strongly your body opposes current, mostly decided by your skin | a raincoat: dry, it keeps water out; soaked or torn, it does not |
| let-go threshold | the current at which your hand muscles clamp and you cannot release what you are holding | a hand cramp you cannot undo |
| ventricular fibrillation | the heart's main chambers twitching chaotically instead of pumping; fatal within minutes without help | an orchestra where every player suddenly plays a different song |
| mains | the electricity from wall outlets: 230 V AC in Europe, 120 V AC in North America | the water main under the street, as opposed to a bottle of water |
| AC / DC | alternating current (direction flips many times per second) versus direct current (one direction) | a saw going back and forth versus a car driving one way |
| internal resistance | the small resistance inside a battery that limits how much current it can deliver | the narrow neck of a bottle |
| short circuit | a path with almost no resistance between a source's two terminals (Lesson 02) | pulling the plug out of a full bathtub |
| thermal runaway | heating that causes more heating, until a lithium battery vents or catches fire | a snowball rolling downhill and growing |
| stored charge | charge left in a capacitor after the power is removed | a spring that stays compressed after you let go of the handle |
| RCD / GFCI | a safety switch in a home that cuts the power if current leaks away through a person | a lifeguard who blows the whistle the moment someone slips |

## Learning Objectives

- Explain why current is what harms the body, and why voltage still matters (it is what pushes the current through you)
- Estimate the current through a body for a given voltage and skin condition, using the preview formula I = V / R
- Recall the rough current thresholds: about 1 mA felt, about 10 mA cannot let go, about 100 mA can stop the heart
- Explain why mains (230 V or 120 V AC) is dangerous and why 12 V DC from batteries is the limit for this course
- Explain why shorting a battery is dangerous even at low voltage, and why lithium cells deserve extra respect
- Recognise that capacitors can hold a dangerous charge after unplugging, and that resistors and soldering irons burn
- Follow the safety rules of this course

## The Problem

You will spend the rest of this course building circuits. Most of them will run on a 9 V battery or a USB supply, and most of the time nothing can hurt you. But "most of the time" is not good enough, for two reasons.

First, electricity gives you no warning. You cannot see, hear or smell voltage. A wire at 0 V and a wire at 230 V look identical. The first warning you get is often the injury itself.

Second, the danger does not come only from high voltage. A 3.7 V lithium cell from an old vape or laptop, shorted by a key in your pocket, can deliver tens of amps, get hot enough to burn through cloth, and catch fire. A 12 V car battery cannot shock you through dry skin, but a dropped spanner across its terminals can glow red and weld itself in place. A tiny 1/4 W resistor in the wrong place reaches over 100 °C in seconds.

This lesson builds a picture of why each of these things happens, using numbers from Lessons 03 and 04, and ends with the rules we follow for the whole course. Read it now, and come back to it whenever a lab feels risky.

## The Physics

### What hurts: current

Your nerves and muscles work by tiny electrical signals: ions (charged atoms) moving across the walls of your cells, creating voltages of around 70 mV (you saw this number in Lesson 04's ladder). When an external current flows through your body, it adds its own push to those signals. Muscles in the path contract whether you want them to or not. Nerves fire. The heart, which runs on a precisely timed electrical wave, can lose its rhythm.

What decides how much of this happens is how much charge passes through you per second, which is the current, measured in amperes (A). The Italian physician Luigi Galvani saw this in the 1780s when a frog's leg twitched as he touched its nerve with metal. In the 1950s and 1960s the American engineer Charles Dalziel measured, carefully and on volunteers, how much current people can feel and still let go of. His numbers, and later the international standard IEC 60479, give us the thresholds used in this lesson.

### What pushes: voltage

Voltage (in volts, V) is the electrical push, the "pressure" of Lesson 02. Your body is not a perfect conductor; it resists current. So whether a dangerous current flows depends on two things at once: how hard the source pushes (voltage) and how hard your body resists (resistance, in ohms, Ω).

As a preview of Ohm's law, which we will earn properly in Phase 03, the relationship is:

```
I = V / R
```

Read it as: "the current, in amperes, equals the voltage, in volts, divided by the resistance, in ohms". Double the push and you double the current. Double the resistance and you halve it.

This is the meaning of the old electricians' saying "it's the volts that jolt, but the mils that kill" (mils meaning milliamps). Both matter: no current flows without a push, and no push hurts without the current it drives.

### Where your resistance comes from

Inside, your body is salty water and conducts quite well: around 500 Ω from one hand to the other. The outer layer of your skin, made of dead, dry cells, is a much better insulator. So nearly all your protection comes from your skin, and that protection changes enormously:

```
condition                     rough resistance, hand to hand
dry skin, fingertip touch     ~100 000 Ω  (100 kΩ)
sweaty hands, firm grip       ~ 10 000 Ω  (10 kΩ)
wet hands, full grip          ~  1 000 Ω  (1 kΩ)
cut skin (only the inside)    ~    500 Ω
```

Two orders of magnitude between dry fingertips and wet hands. The real numbers vary from person to person and moment to moment; these are round values to reason with.

There is one more effect, and it is the reason mains is so dangerous: above roughly 50 V, the voltage itself punctures the dry outer layer of skin. The 100 kΩ raincoat tears open, and even a dry hand drops to around 1 000 to 2 000 Ω. At 12 V this does not happen; at 230 V it does, within a fraction of a second.

### The current thresholds

For mains-frequency AC (50 or 60 Hz), flowing hand to hand for about a second, rough thresholds are:

```
current        what happens (AC, 50/60 Hz)
below 1 mA     not felt
1-5 mA         a tingle
5-10 mA        painful, but you can still let go
10-30 mA       muscles lock: you may not be able to let go
30-100 mA      breathing muscles stop, the heart is at risk
above 100 mA   the heart can fibrillate: deadly without immediate help
```

AC is worse than DC at the same current, because the constant reversal keeps re-triggering muscles and nerves. For steady DC the "cannot let go" effect is much weaker (you mostly feel a jolt when contact is made and broken) and the heart can usually tolerate a few times more current before fibrillating, around 150 mA and above for a long contact. "Safer" does not mean safe: DC at high current still burns tissue and stops hearts.

Notice the scale (Lesson 04 thinking): the deadly zone starts around 10^-1 A. A phone charger delivers 10^0 A. Your body can be killed by a tenth of what charges your phone, if something pushes it through you.

### Why a battery short is dangerous even at 1.5 V

Every real battery has a small internal resistance, written r, from the chemistry and the materials inside it (Phase 06, Lesson 02). If you connect a wire straight across its terminals (a short circuit, Lesson 02), the only thing limiting the current is that r:

```
I_short = V / r
```

And all the energy turns to heat inside the battery and the wire. A preview of Phase 03's power rule, P = I^2 x r (read "power equals current squared times resistance"), gives the heat in watts (W, joules per second).

Worked example, an 18650 lithium-ion cell (the cylinder inside laptop packs, power tools and many vapes):

```
V = 3.7 V,  r ≈ 0.04 Ω
I_short = 3.7 / 0.04 = 92.5 A
heat = 92.5^2 x 0.04 = 8556 x 0.04 ≈ 342 W
```

342 W is more than a soldering iron, concentrated inside a cylinder the size of your thumb. Real cells sag a bit under such a load, but the order of magnitude is right. Lithium cells also store a lot of energy in a flammable electrolyte; when they get hot enough, the chemistry starts releasing its own heat (thermal runaway), they vent burning gas, and the fire is very hard to put out. A 1.5 V AA cell shorted by a coin in a pocket gets hot enough to burn skin; a 9 V battery thrown in a drawer with paperclips can start a fire. The voltage is low; the danger is current and heat.

### Why unplugged is not always safe

A capacitor is a part that stores charge (we meet it properly in Phase 07). Its energy is E = ½ x C x V^2 (read "energy in joules equals one half times capacitance in farads times voltage squared"). Unlike a battery, it can release that energy almost instantly. Large capacitors inside anything that plugs into the wall (power supplies, TVs, microwave ovens, camera flashes) can hold hundreds or thousands of volts for minutes, days or longer after unplugging.

```
camera flash:  C = 120 µF = 1.2 x 10^-4 F,  V = 330 V
E = 0.5 x 1.2 x 10^-4 x 330^2 = 0.5 x 1.2 x 10^-4 x 1.089 x 10^5 ≈ 6.5 J
first-touch current through sweaty hands: 330 / 10 000 = 33 mA
```

33 mA is in the "muscles lock" zone, from a part you might pull out of a disposable camera. A microwave oven's capacitor (about 1 µF at 2100 V) would push around 210 mA: in the deadly zone. Never take these apart.

### Heat: the quiet danger

Every part that carries current gets warm, and the power turned into heat in a resistor is P = V^2 / R (another preview of Phase 03). The common through-hole resistor is rated for 1/4 W. Put a 100 Ω resistor straight across 12 V:

```
P = 12^2 / 100 = 144 / 100 = 1.44 W
```

That is almost six times its rating. It will discolour, smoke and can burn a fingertip. Soldering irons sit at 300 to 400 °C, and a lead-acid or lithium battery shorted through a thin wire can make that wire glow.

## The Concept

### Putting the numbers together

Use I = V / R for each voltage and each skin condition. Here is what our script computes:

```
  volts            dry        sweaty           wet   broken skin
    1.5      0.015 mA       0.15 mA        1.5 mA          3 mA
      9       0.09 mA        0.9 mA          9 mA         18 mA
     12       0.12 mA        1.2 mA         12 mA         24 mA   <- course limit
     24       0.24 mA        2.4 mA         24 mA         48 mA
     50        0.5 mA          5 mA         50 mA        100 mA
    120        1.2 mA         12 mA        120 mA        240 mA
    230        2.3 mA         23 mA        230 mA        460 mA
```

Read along the 12 V row. With dry skin, 0.12 mA: below feeling. With wet hands gripping both terminals firmly, the simple model says 12 mA. That sounds alarming, but two things protect you: it is DC (so "cannot let go" barely applies), and at 12 V the skin does not break down, so real low-voltage body resistance is usually higher than our wet-hand round number. In practice, touching both terminals of a 12 V battery is not felt at all with dry hands and is at most a faint tingle with wet ones. That is why 12 V DC sits inside the "safety extra-low voltage" range used by electrical standards for things you are allowed to touch.

Now read the 230 V row. Even the "dry" column, which already understates the danger because the skin breaks down at this voltage, reaches the level you can feel. With realistic broken-down skin (1-2 kΩ) it is 115 to 230 mA: deadly. That is what lives behind every wall outlet.

### The other direction: how much voltage to reach a threshold?

Turn the formula around: V = I x R. How much voltage does it take to push 10 mA ("cannot let go")?

```
dry skin       0.010 A x 100 000 Ω = 1000 V
sweaty hands   0.010 A x  10 000 Ω =  100 V
wet hands      0.010 A x   1 000 Ω =   10 V
broken skin    0.010 A x     500 Ω =    5 V
```

The same threshold needs 1000 V on dry skin but only 5 V through a cut. This is why you never let a circuit's wires touch a wound, never put leads in your mouth to "test" a battery (the tongue is wet and thin), and why bathrooms have stricter electrical rules than living rooms.

### Path matters

Current through one hand (from finger to finger of the same hand) mostly passes through the hand. Current from one hand to the other, or from a hand to the feet, passes through the chest and the heart. That is why professionals working near high voltage keep one hand in their pocket (the "one-hand rule") and stand on insulating mats. You will not need those habits at 12 V, but you should know they exist.

### Home protection devices

Modern homes have a safety switch called an RCD (residual current device) in Europe, or GFCI (ground fault circuit interrupter) in North America. It compares the current going out on one wire with the current coming back on the other. If they differ by more than a few milliamps (typically 30 mA for an RCD, 5 mA for a GFCI), some current must be leaking somewhere, maybe through a person, and it cuts the power within a few hundredths of a second. It is a beautiful use of exactly the idea from this lesson: watch the current, not the voltage.

### The rules of this course

1. **12 V DC is our ceiling.** Use batteries (AA packs, 9 V), USB power (5 V), or a bench supply set to 12 V or less with its current limit turned down. Every lab and simulation in the early phases is designed for this range.
2. **Never open or modify anything that plugs into the wall.** No mains circuits, no opening power supplies, chargers, TVs, microwaves or camera flashes. Not even unplugged: capacitors can still be charged.
3. **Never short a battery.** Keep loose cells in their packaging or a case, away from keys and coins. Use battery holders. If you want a fuse or a current limit, use it.
4. **Respect lithium cells.** Do not puncture, crush, bend or heat them. Do not use a swollen, dented or hot cell. Do not leave lithium cells charging unattended on a soft surface. If one hisses or smokes, get away from it and let it burn out in a safe place; do not breathe the fumes.
5. **Power off before you change the circuit.** Disconnect the battery, then move parts, then reconnect.
6. **If something gets hot, smells or smokes, disconnect first, think later.** Do not grab the hot part. Unplug the battery clip or switch off the supply.
7. **Mind polarity on electrolytic capacitors and wear eye protection when you first power a circuit with them.** A reversed electrolytic can burst (Phase 07).
8. **Soldering irons live in their stand.** 350 °C. Work in a ventilated room and wash your hands after handling solder.
9. **Keep coin cells away from small children.** A swallowed coin cell can cause severe internal burns within hours; that is a chemical and electrical injury from just 3 V.
10. **When in doubt, simulate first.** From Phase 05 on we have our own simulator; check the numbers before you build.

## Build It

`code/main.py` turns the physics above into tables. Everything is one formula, I = V / R, plus the power and energy previews.

### Step 1: Body resistances and thresholds as data

```python
BODY_RESISTANCE = {
    "dry": 100_000.0,
    "sweaty": 10_000.0,
    "wet": 1_000.0,
    "broken skin": 500.0,
}
```

Thresholds are stored as (upper limit, description) pairs, one list for AC and one for DC:

```python
AC_EFFECTS = [
    (0.001, "not felt"),
    (0.005, "a tingle"),
    (0.010, "painful, but you can let go"),
    (0.030, "muscles lock, cannot let go"),
    (0.100, "breathing stops, heart at risk"),
    (np.inf, "heart may fibrillate: deadly"),
]
```

`np.inf` is numpy's infinity: "everything above 100 mA".

### Step 2: Look up the effect of a current

```python
def effect_of(current, effects):
    for limit, description in effects:
        if current < limit:
            return description
    return effects[-1][1]


def body_current(volts, ohms):
    return volts / ohms
```

The script prints the table you saw in The Concept and then the effects (excerpt):

```
  case              current   if DC (battery)                    if AC (mains)
  12 V, dry         0.12 mA   not felt                           not felt
  12 V, wet           12 mA   felt, jolt on touch and release    muscles lock, cannot let go
  230 V, wet         230 mA   heart may fibrillate: deadly       heart may fibrillate: deadly
  but above ~50 V skin breaks down: at 230 V even dry skin falls to ~1-2 kΩ -> 115-230 mA, deadly
```

The "12 V, wet" AC column is the reason household AC at even modest voltages must be treated with care, and the DC column shows why our battery circuits are fine.

### Step 3: Battery shorts

```python
def show_battery_shorts():
    print("=== 4. Short-circuiting a battery: current and heat inside it ===")
    for name, volts, internal_ohms in BATTERIES:
        current = volts / internal_ohms
        heat_watts = current**2 * internal_ohms
        print(f"  {name:<20} {volts:>5g} V, r = {internal_ohms:>6g} Ω  ->  I = {current:8.1f} A, heat = {heat_watts:8.1f} W")
    print()
```

Output:

```
  CR2032 coin cell         3 V, r =     15 Ω  ->  I =      0.2 A, heat =      0.6 W
  9 V PP3 battery          9 V, r =    1.7 Ω  ->  I =      5.3 A, heat =     47.6 W
  AA alkaline cell       1.5 V, r =   0.15 Ω  ->  I =     10.0 A, heat =     15.0 W
  18650 Li-ion cell      3.7 V, r =   0.04 Ω  ->  I =     92.5 A, heat =    342.2 W
  car battery           12.6 V, r =  0.008 Ω  ->  I =   1575.0 A, heat =  19845.0 W
```

The internal resistances are typical values for fresh cells; real ones vary and the voltage sags under such loads, so treat these as upper-end, order-of-magnitude numbers. Notice the pattern: the lower the internal resistance, the more dangerous the short, and it has almost nothing to do with the voltage. The coin cell at 3 V is the gentlest; the 3.7 V lithium cell is hundreds of times fiercer.

### Step 4: Capacitors and resistors

```python
def show_capacitors():
    print("=== 5. Charge left in capacitors after unplugging (touched with sweaty hands, 10 kΩ) ===")
    body_ohms = BODY_RESISTANCE["sweaty"]
    for name, farads, volts in CAPACITORS:
        energy = 0.5 * farads * volts**2
        first_current = volts / body_ohms
        time_constant = body_ohms * farads
        print(
            f"  {name:<24} {farads * 1e6:>6g} µF at {volts:>6g} V: energy = {energy:7.3g} J, "
            f"first touch {first_current * 1000:7.3g} mA, gone after ~5RC = {5 * time_constant:.3g} s"
        )
    print()
```

`time_constant` (R x C, in seconds) is a preview of Phase 07, Lesson 04: a capacitor discharging through a resistance is mostly empty after about five of these. A 12 V breadboard capacitor gives 1.2 mA (not felt); a camera flash gives 33 mA; a microwave capacitor 210 mA.

The last section prints P = V^2 / R for small resistors on 5, 9 and 12 V and flags the ones above their 1/4 W rating.

Run it:

```
cd /home/fer/Escritorio/youtube/electronics_from_scratch
uv run python phases/00-words-and-units/06-safety-first/code/main.py
```

## Use It

- **Electrical standards.** IEC standards call voltages below about 50 V AC or 120 V DC "extra-low voltage", and devices meant to be touched (toys, phone chargers' output, doorbells, garden lights) use safety extra-low voltage, isolated from mains. Our 12 V ceiling sits well inside that.
- **USB chargers.** A phone charger takes 230 V in and gives 5 V out through a transformer that keeps the two sides isolated (Phase 08). You can touch the USB plug's pins safely because of this isolation. Cheap counterfeit chargers sometimes skimp on it, which is why they cause injuries.
- **Battery shipping rules.** Lithium cells must travel with their terminals protected and are banned from checked luggage on planes, because a short or a crushed cell can start a fire in the hold.
- **Fuses and current limits.** A fuse is a deliberately thin wire that melts if the current gets too high (Phase 02, Lesson 03). A lab supply's current limit does the same job electronically. Both protect against the battery-short scenario of this lesson.
- **Datasheets.** Every battery datasheet lists a maximum continuous discharge current, and many lithium cells contain a small protection circuit that disconnects the cell on a short. Every resistor datasheet lists a power rating. Respecting those two numbers prevents most fires on a hobby bench.

## Common Mistakes

- **"Low voltage means harmless."** For shocks, mostly true below 12 V DC with intact skin. For shorts and heat, false: a 3.7 V lithium cell or a 12 V car battery can deliver tens to thousands of amps.
- **"High voltage alone kills."** A static spark from a doorknob can be over 10 000 V but carries so little charge that only a tiny current flows for a microsecond. What matters is how much current flows, for how long, through which path. This is not a reason to play with high voltage; sources that can keep pushing current at high voltage are lethal.
- **"Unplugged means safe."** Capacitors in mains equipment can hold lethal charge long after unplugging.
- **"It's only a resistor."** Small resistors on the wrong supply get hot enough to burn. Calculate the power before you plug in.
- **Licking a 9 V battery to test it.** The tongue is wet and thin-skinned (low resistance), and it is a bad habit. Use a multimeter (Phase 02, Lesson 07).
- **Reaching for a smoking part.** Disconnect power first. A hot resistor or battery stays hot for a while after.
- **Treating the thresholds as exact.** They are rough, vary between people and depend on duration and path. Use them as orders of magnitude and stay far below them.

## Exercises

1. Using I = V / R, compute the current through a body with sweaty hands (10 kΩ) touching a 24 V supply. Which AC zone would that be in? Which DC zone?
2. A 9 V battery has an internal resistance of about 1.7 Ω. Compute its short-circuit current and the heat produced. Why does the battery get hot, not just the wire?
3. A 4.7 µF capacitor in a circuit was charged to 12 V. Compute its stored energy in joules, and the first-touch current through dry skin (100 kΩ). Is it dangerous?
4. You want a resistor to drop 9 V and you have a 1/4 W, 220 Ω part. Compute the power with P = V^2 / R. Will it survive? What is the smallest resistance that keeps the power below half its rating?
5. (Harder) An RCD trips at 30 mA of leakage. For wet hands (1 kΩ) on 230 V, how far above the trip current is the body current? If the RCD takes 40 ms to trip, how much charge passes through the body in that time (charge = current x time, in coulombs)? How many electrons is that, using e = 1.602 x 10^-19 C?

## Key Terms

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| electric shock | "getting zapped by voltage" | current flowing through the body; voltage is what pushes it |
| body resistance | "the body's resistance" | mostly skin resistance; drops 100 times from dry to wet, and breaks down above ~50 V |
| let-go threshold | "you can't let go" | around 10-30 mA AC, when forearm muscles clamp involuntarily |
| fibrillation | "heart attack" | chaotic twitching of the heart's chambers, caused from about 100 mA AC; needs a defibrillator |
| short circuit | "a spark" | near-zero resistance across a source: current limited only by internal resistance, energy becomes heat |
| internal resistance | "battery strength" | the resistance inside a source; low means it can deliver large currents, including into a short |
| extra-low voltage | "safe voltage" | below about 50 V AC / 120 V DC by IEC definitions; our course uses at most 12 V DC |
| RCD / GFCI | "the trip switch" | a device that cuts power when outgoing and returning currents differ by a few mA |

## Further Reading

- [All About Circuits, Volume I, Chapter 3 "Electrical Safety"](https://www.allaboutcircuits.com/textbook/direct-current/chpt-3/importance-electrical-safety/): free, thorough chapter on shock physiology, body resistance and safe practice.
- [OSHA, "Controlling Electrical Hazards" (publication 3075)](https://www.osha.gov/sites/default/files/publications/osha3075.pdf): the US workplace-safety agency's guide, with a table of current effects.
- IEC 60479-1, *Effects of current on human beings and livestock*: the international standard behind the thresholds; summarised on many engineering sites if you cannot access the standard.
- [Battery University, "BU-304a: Safety Concerns with Li-ion"](https://batteryuniversity.com/article/bu-304a-safety-concerns-with-li-ion): why lithium cells fail and how to handle them.
