# LEDs

> An LED is a diode whose electrons, when they fall across the band gap, give the energy away as light. The gap sets the colour, the colour sets the voltage, and a resistor sets the current.

**Type:** Build
**Prerequisites:** 11-01 (Why Silicon), 11-04 (The Diode Equation); Phase 03 (Resistance and Ohm's Law), lessons 03-ohms-law and 05-power-and-heat
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| LED (light-emitting diode) | A diode made of a material that turns the energy of recombining electrons into light | A turnstile that rings a bell every time someone passes, and the bell's pitch depends on the step height |
| Photon | A single particle (packet) of light, carrying a fixed amount of energy | One drop of rain: light comes in drops, not a continuous stream |
| Wavelength | The distance between crests of a light wave; for visible light 380-750 nanometres. Shorter wavelength = bluer = more energetic | The spacing between ripples on a pond |
| Nanometre (nm) | One billionth of a metre (10⁻⁹ m) | About the width of 10 atoms side by side |
| Direct band gap | A material where an electron can drop across the gap and emit light easily | A slide straight down into a pool: one smooth move |
| Indirect band gap | A material (like silicon) where the drop also needs a vibration of the crystal, so light is rarely emitted | A slide that ends a step away from the pool: you need an extra shove |
| Forward voltage (V_F) | The voltage across the LED at its rated current | The step height the electrons must climb before falling |
| Current-limiting resistor | The resistor in series with an LED that sets its current | A tap that controls how fast water flows into a funnel |
| Luminous intensity (mcd) | How bright an LED looks in a given direction, in millicandela | How bright a torch looks when pointed at you |
| Efficacy | Light out per electrical watt in, in lumens per watt | Miles per gallon, for light |
| Phosphor | A coating that absorbs blue light and re-emits yellow light; together they look white | Glow-in-the-dark paint powered by a blue lamp |
| Current hogging | When parallel LEDs share a resistor, the one with the lowest V_F takes most of the current | The widest door in a crowded exit gets most of the people |

## Learning Objectives

- Explain how an LED makes light and why silicon diodes do not.
- Relate an LED's colour to its band gap and its forward voltage, using E = 1240 / λ.
- Design the series resistor for any LED and supply, choose a standard value, and check the power.
- Explain why the resistor must drop a good share of the supply.
- Wire LEDs in series correctly, and explain why parallel LEDs need separate resistors.

## The Problem

LEDs are everywhere: indicator lights, phone screens, traffic lights, car headlamps, the bulbs in your ceiling. They are also the first part most beginners destroy. Connect a red LED straight to a 5 V supply and it flashes once, very brightly, and dies. Connect it to a 1.5 V battery and it does nothing at all.

Both outcomes follow from lesson 04: the LED is a diode with an exponential I-V curve. Below its forward voltage almost no current flows; a little above it, the current is enormous. You cannot control an LED by choosing a voltage; you must control its **current**. This lesson shows why the LED behaves that way, why each colour has its own voltage, and how to design the one resistor that makes an LED work.

## The Physics

### Light from recombination

In lesson 03, forward bias pushed electrons from the n side into the p side, where they recombine with holes. Recombination means an electron falls from the conduction band (high shelf) into an empty slot in the valence band (low shelf). It releases an energy roughly equal to the **band gap**, E_g.

Where does that energy go? Two options:

1. It shakes the crystal (heat).
2. It leaves as a **photon**: a single packet of light, carrying exactly that energy.

In silicon, the fall almost always produces heat. Silicon has an **indirect** band gap: the electron at the bottom of the conduction band has a different *momentum* (roughly, direction of motion in the crystal) than the empty slot at the top of the valence band. A photon carries almost no momentum, so it cannot pay for that change; a crystal vibration must take part, which makes light emission millions of times less likely.

Materials like gallium arsenide (GaAs), gallium phosphide mixtures and gallium nitride (GaN) have **direct** band gaps: the electron can fall straight down and emit a photon in one step. Those are LED materials.

What the shelf picture gets wrong: in lesson 01 we said shelves are flat planks. Here we need the fact that, in a real crystal, the "height" of a shelf depends on which way the electron moves. That is precisely the direct/indirect difference. For everything else in this course the flat-plank picture is enough.

### Colour from the gap

A photon's energy and its colour (wavelength) are linked by a fundamental law of nature:

```
E = h × c / λ
```

Read: "the photon energy equals Planck's constant times the speed of light divided by the wavelength". With E in electronvolts and λ (lambda) in nanometres, h × c ≈ 1240 eV·nm, so:

```
E (eV) ≈ 1240 / λ (nm)
```

Worked examples:

- Red light, 630 nm: E = 1240 / 630 = 1.97 eV.
- Green, 525 nm: 1240 / 525 = 2.36 eV.
- Blue, 465 nm: 1240 / 465 = 2.67 eV.
- Infrared (TV remotes), 940 nm: 1240 / 940 = 1.32 eV.

So to get blue light you need a material with a gap of about 2.7 eV, and for red about 2 eV. Engineers tune the gap by mixing elements: aluminium gallium indium phosphide (AlGaInP) for red, orange and yellow; indium gallium nitride (InGaN) for green and blue. The blue InGaN LED was so hard to make that its inventors (Akasaki, Amano and Nakamura) received the 2014 Nobel Prize in Physics: without it there would be no white LEDs.

### Colour sets the voltage

Here is the connection to circuits. For an electron to cross a junction and then fall across a gap of E_g, the barrier picture of lesson 03 says the forward voltage must be roughly E_g / q: about the band gap expressed in volts. So:

| Colour | Photon energy | Typical V_F at 10 mA (our simulator) |
|---|---|---|
| infrared (940 nm) | 1.32 eV | 1.25 V |
| red (630 nm) | 1.97 eV | 1.85 V |
| yellow (590 nm) | 2.10 eV | 2.05 V |
| green (525 nm) | 2.36 eV | 2.20 V |
| blue (465 nm) | 2.67 eV | 3.00 V |
| white (blue + phosphor) | — | 3.10 V |

Red, yellow and green LEDs sit a little *below* their photon energy (heat from the crystal helps a bit), while blue LEDs sit *above* it: the GaN materials have extra resistance and barriers at internal layers. As a rule of thumb, V_F ≈ photon energy in volts, ±0.3 V.

**White LEDs** are blue LEDs coated with a yellow phosphor. Part of the blue light is absorbed and re-emitted as yellow; blue plus yellow looks white to our eyes. That is why a white LED's V_F is the same as a blue one's.

### The LED is still a diode

Electrically, an LED obeys the same Shockley law as lesson 04, just with a different I_S and usually an ideality factor near 2. Our simulator models each colour with n = 2 and an I_S chosen so that the LED carries exactly 10 mA at its V_F. With n = 2 the current rises 10× for every 119 mV, still very steep. The script shows what happens with a red LED connected straight to a supply through only 1 Ω of wiring:

```
supply 1.8 V  ->  LED current       3.5 mA
supply 2.0 V  ->  LED current      58.6 mA
supply 2.5 V  ->  LED current     452.9 mA
supply 3.0 V  ->  LED current     916.4 mA
```

A 0.2 V change takes the LED from dim to overloaded. (Real LEDs would also heat up, which lowers V_F and raises the current further: thermal runaway, then a dead LED.)

## The Concept

### The current-limiting resistor

```
          R
  +Vs ---/\/\/--- a ---|>|--- ground
                       LED
          I = (Vs - V_F) / R
```

The LED keeps its voltage near V_F almost regardless of current (that is what "steep exponential" means). So the resistor gets whatever is left, Vs − V_F, and Ohm's law sets the current:

```
I = (Vs − V_F) / R        so        R = (Vs − V_F) / I
```

Read: "the resistor equals the supply minus the LED voltage, divided by the current you want".

**Worked example**: a red LED (V_F = 1.85 V) on 5 V at 10 mA.

```
R = (5 − 1.85) / 0.010 = 3.15 / 0.010 = 315 Ω
```

Resistors come in standard values (the E12 series: 100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820, ...). Pick the next value **up**, so the current ends a little below target: 330 Ω. The simulator then gives 9.55 mA, with the LED at 1.848 V. (V_F dropped by 2 mV because the current is a little lower: the exponential at work.)

**Check the power.** Resistor: P = I² × R = 0.00955² × 330 = 30 mW. A standard 1/4 W (250 mW) resistor is fine. The LED itself dissipates V_F × I = 1.848 × 0.00955 = 17.6 mW.

The script's full design table for 5 V and 10 mA:

| Colour | V_F | Exact R | E12 pick | Simulated I | P resistor | P LED |
|---|---|---|---|---|---|---|
| infrared | 1.25 V | 375 Ω | 390 Ω | 9.62 mA | 36 mW | 12 mW |
| red | 1.85 V | 315 Ω | 330 Ω | 9.55 mA | 30 mW | 18 mW |
| yellow | 2.05 V | 295 Ω | 330 Ω | 8.96 mA | 27 mW | 18 mW |
| green | 2.20 V | 280 Ω | 330 Ω | 8.51 mA | 24 mW | 19 mW |
| blue | 3.00 V | 200 Ω | 220 Ω | 9.11 mA | 18 mW | 27 mW |
| white | 3.10 V | 190 Ω | 220 Ω | 8.67 mA | 17 mW | 27 mW |

### Why the resistor must take a good share of the voltage

Suppose you have a 2.2 V supply and a red LED. R = (2.2 − 1.85) / 0.01 = 35 Ω; pick 33 Ω. It works, at 10.5 mA. But supplies are never exact. If the supply moves by ±10 %:

```
5 V with 330 ohm   supply -10%:   8.06 mA   nominal:   9.55 mA   +10%:  11.05 mA
2.2 V with 33 ohm  supply -10%:   5.02 mA   nominal:  10.53 mA   +10%:  16.49 mA
```

With 5 V, the resistor drops 3.15 V, so a 0.5 V change in supply changes its voltage by 16 % and the current by about 16 %. With 2.2 V, the resistor only drops 0.35 V; a 0.22 V supply change is 63 % of that, and the current swings from 5 mA to 16.5 mA. Same story for LED-to-LED variation in V_F (datasheets often give V_F as "1.8 V typical, 2.4 V max"). **Rule: let the resistor drop at least a volt or two.**

### LEDs in series

To light several LEDs from one supply, string them in **series** with one resistor. The same current flows through all, so they are equally bright, and their voltages add:

```
          R
  +12 V --/\/\/--|>|--|>|--|>|-- ground
                 red  red  red
  R = (12 − 3 × 1.85) / I
```

For 20 mA: R = (12 − 5.55) / 0.02 = 322 Ω; pick 330 Ω. The simulator gives 19.24 mA, each LED at 1.884 V, and the resistor dissipating 122 mW (still fine for 1/4 W, but getting warm: use a 1/2 W part if the circuit runs hot or enclosed). LED lamps and backlights use long series strings driven by a constant-current circuit for exactly this reason.

### LEDs in parallel: don't share a resistor

Two LEDs in parallel on one resistor seem natural, but their V_F are never exactly equal. Because the current is exponential in voltage, a tiny difference decides who gets everything. The script puts a red (1.85 V) and an orange (1.95 V) LED in parallel on 150 Ω:

```
red gets 18.17 mA, orange gets 2.63 mA
```

A 0.1 V difference gave one LED seven times the current of the other. Even two LEDs of the same colour from the same bag differ by tens of millivolts, and the one that runs hotter gets lower V_F and takes even more. **Give each parallel LED its own resistor.**

### Brightness and current

Light output is roughly proportional to current (more electrons recombining per second = more photons per second). Halving the current roughly halves the light. But our eyes respond to light logarithmically, so half the current looks only a little dimmer. Many modern LEDs are clearly visible at 1-2 mA, which matters for battery-powered gadgets. For dimming, circuits usually switch the LED fully on and off thousands of times a second and vary the on-fraction (PWM, Phase 17) rather than reduce the current, because colour and efficiency stay constant.

### Reverse voltage

LEDs are poor at blocking reverse voltage: datasheets typically allow only **5 V** reverse. Connect one backwards across 12 V and it may be damaged. If an LED will see AC or reversed polarity, put an ordinary diode in anti-parallel or in series.

## Build It

### Step 1: Photon energies

```python
def photon_energy_ev(wavelength_nm):
    return PLANCK_TIMES_LIGHT_EV_NM / wavelength_nm
```

The first block prints each colour's photon energy next to the simulator's V_F, which the package exposes as `LED_COLORS`.

### Step 2: An LED circuit in the simulator

```python
def led_with_resistor(color, supply, ohms):
    circuit = Circuit()
    circuit.voltage_source("V1", "vcc", "0", supply)
    circuit.resistor("R1", "vcc", "a", ohms)
    circuit.led("D1", "a", "0", color=color)
    return circuit.dc()
```

### Step 3: Design with standard values

`show_resistor_design` computes R = (Vs − V_F) / I, rounds it **up** to the next E12 value with `nearest_e12_above`, simulates and prints the current and the power in each part.

### Step 4: The experiments

`show_no_resistor`, `show_supply_sensitivity`, `show_series_string` and `show_parallel_hogging` reproduce each warning of the Concept section with real numbers.

```
uv run python phases/11-semiconductors-and-diodes/07-leds/code/main.py
```

## Use It

- **Indicator LEDs** (3 mm and 5 mm through-hole, 0603 and 0805 surface-mount): typical datasheets list "forward voltage 2.0 V typ, 2.4 V max at 20 mA" (red) or "3.2 V typ, 3.6 V max" (blue/white), maximum continuous current 20-30 mA, reverse voltage 5 V. Modern high-efficiency parts look bright at 2-5 mA.
- **Microcontroller pins**: a 3.3 V pin driving a red LED through 220 Ω gives (3.3 − 1.85)/220 ≈ 6.6 mA, safely below the pin's limit (often 8-20 mA). A blue LED (3.0 V) from a 3.3 V pin barely lights: only 0.3 V is left for the resistor. Phase 12 shows how a transistor lets a pin drive bigger loads.
- **High-power LEDs** (1-3 W, e.g. 350-700 mA) are driven by **constant-current drivers**, not resistors: a resistor would waste too much power and could not compensate for V_F falling as the LED heats.
- **RGB LEDs** combine red, green and blue chips in one package with separate pins; each colour needs its own resistor because each has a different V_F.
- **Efficiency**: a white LED bulb produces 100-150 lumens per watt, about 10 times more than an incandescent bulb, which is why LEDs replaced them.
- **Photodiodes and solar cells** run the LED process backwards: a photon with energy above the gap creates an electron-hole pair that the junction's field separates into current.

## Try It in the Lab

The lab is a USB gadget: a 5 V supply, a green LED and an empty resistor slot. Pick the resistor that gives a bright but safe current and keeps the resistor cool.

Think about: the green LED's forward voltage, what's left for the resistor, the resulting current, and the power the resistor dissipates. After you pass, try the other two parts. Which goal does each one break, and why?

## Common Mistakes

- **No resistor.** The single most common way to destroy an LED (and sometimes the pin driving it).
- **Backwards LED.** The longer leg is the anode (+); the flat side of the rim and the shorter leg are the cathode. A backwards LED simply stays dark at low voltage, but can be damaged above about 5 V reverse.
- **Using the battery voltage the label says.** A "9 V" battery is 9.5 V new and 7 V when tired; USB can be 4.75-5.25 V. Design for the range.
- **Sharing one resistor between parallel LEDs.** Current hogging makes one bright and one dim, and can kill the bright one.
- **Thinking white LEDs are "white material".** They are blue LEDs with phosphor: same 3 V forward voltage as blue.
- **Forgetting the LED's power.** At 20 mA a blue LED dissipates 3 V × 0.02 A = 60 mW, which is fine; at 30 mA in a hot enclosure, near the limit.
- **Expecting an LED to light from a single 1.5 V cell.** Red needs about 1.8 V, blue about 3 V. A single cell needs a boost converter (Phase 18).

## Exercises

1. A yellow LED (V_F = 2.05 V) on a 12 V supply at 15 mA. Compute R, pick an E12 value, and compute the resistor's power. Is a 1/4 W part enough?
2. What wavelength would a photon from a 1.85 eV gap have? Is it visible?
3. You have a 9 V battery and four green LEDs (2.2 V each). Can you put all four in series? If not, what is the best arrangement with resistors?
4. A blue LED with V_F between 2.9 V and 3.4 V (datasheet min and max) is driven from 5 V through 180 Ω. What is the range of currents? Repeat for a 3.6 V supply and 27 Ω. Which design would you trust?
5. Edit `show_parallel_hogging` to give each LED its own 300 Ω resistor from the 5 V supply. How well do they share now?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| LED | "A little light" | A diode of direct-gap semiconductor where recombination emits photons of energy about E_g |
| V_F | "LED voltage" | Forward voltage at rated current; roughly the photon energy in volts (1.2 V infrared to 3.2 V blue/white) |
| Current-limiting resistor | "The LED resistor" | Sets the current: R = (Vs − V_F) / I |
| E = 1240/λ | "Photon energy" | Photon energy in eV from wavelength in nm |
| Direct band gap | "Good for light" | Electron can drop across the gap and emit a photon without needing a lattice vibration |
| Phosphor | "White coating" | Material that converts some blue light to yellow, making white |
| Current hogging | "Uneven sharing" | In parallel, the LED with the lowest V_F takes most of the current, because current is exponential in voltage |

## Further Reading

- *All About Circuits*, Volume III, chapter 3, "Special-purpose diodes" (LEDs and photodiodes). https://www.allaboutcircuits.com/textbook/semiconductors/chpt-3/special-purpose-diodes/
- The Nobel Prize in Physics 2014, popular-science background: "Blue LEDs - filling the world with new light". https://www.nobelprize.org/prizes/physics/2014/popular-information/
- P. Scherz and S. Monk, *Practical Electronics for Inventors*, 4th ed., section on LEDs (resistor calculation, series and parallel strings).
- Kingbright or Lite-On datasheets for a standard 5 mm red LED (e.g. Kingbright L-53HD): forward voltage, maximum current, reverse voltage and intensity curves. https://www.kingbrightusa.com/
