# Why Alternating Current

> The wall socket pushes back and forth fifty times a second because a back-and-forth push is the only kind a transformer can change, and changing the voltage is what makes long wires cheap.

**Type:** Learn
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Lesson 05 (Power and Heat); Phase 05 (Circuit Analysis and Our Simulator); Phase 08 (Magnetism and Inductors), Lessons 03 (Faraday's Law and Induction) and 06 (Transformers)
**Time:** ~50 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Direct current (DC) | Current that always flows the same way round the circuit | A river that always runs downhill in one direction |
| Alternating current (AC) | Current that flows one way, stops, flows the other way, stops, and repeats | A saw going back and forth: it never travels anywhere, yet it cuts |
| Waveform | The shape you get when you draw a voltage or current against time | The trace an ECG machine draws of your heartbeat |
| Cycle | One full repeat of the back-and-forth pattern | One full stroke of the saw, forward and back |
| Period (T) | How long one cycle takes, in seconds | The time between two ticks of a pendulum swinging the same way |
| Frequency (f) | How many cycles happen in one second | Beats per minute of a song, but counted per second |
| Hertz (Hz) | The unit of frequency: one cycle per second | "50 Hz" means 50 full back-and-forth swings each second |
| Mains | The electricity that comes out of the wall socket | The water that comes out of the tap: someone far away pushes it to you |
| Grid | The network of power stations, lines and transformers that feeds the mains | The road network, from motorways down to the street outside your house |
| Transmission line | The long, high-voltage wires that carry power between regions | Motorways for electrical energy |
| Distribution | The lower-voltage wiring that carries power the last few kilometres to buildings | Local streets after you leave the motorway |
| Line loss | Energy turned into heat in the wires on the way, instead of reaching the user | Water leaking from a long hose before it reaches the garden |
| Transformer | A device of two coils on an iron core that changes an AC voltage up or down | A gearbox: trades speed (voltage) for force (current) |
| Step up / step down | Make the voltage higher / lower with a transformer | Shifting gear up for the motorway, down for town |
| Generator | A machine that turns spinning motion into electrical energy | A bicycle dynamo, scaled up to the size of a building |

## Learning Objectives

- Describe the difference between direct current and alternating current, and sketch the waveform of each.
- Explain, with numbers, why sending the same power at a higher voltage wastes far less energy in the wires (loss goes as one over voltage squared).
- Explain why the transformer, which only works with changing current, made AC the winner for power grids.
- Summarise the "war of the currents" (Edison, Westinghouse, Tesla, the Ganz engineers) and why HVDC is coming back today.
- State the mains voltage and frequency where you live, and convert a frequency into a period.

## The Problem

Imagine you run a small power station by a river, and the town you want to supply is 10 kilometres away. The town needs 12 kilowatts (12 kW, that is 12,000 watts: think of six electric kettles running at once). Your two wires, the one going to the town and the one coming back, have a total resistance of 0.8 ohm. That is not much: it is about what 10 km of thick copper cable has.

The houses expect 240 volts. So the obvious plan is: generate 240 V, send it down the wires, done. Let us see how that goes. To deliver 12,000 W at 240 V, the current has to be 12,000 / 240 = 50 amperes. Fifty amperes through 0.8 ohm heats the wires with 50 x 50 x 0.8 = 2,000 watts. One sixth of everything the town wanted is being used to warm the countryside. Worse, the 50 A also loses 50 x 0.8 = 40 volts across the wires, so the houses get only 200 V and their lights are dim.

Now the trick that runs the modern world: send the power at 24,000 V instead. Same 12,000 W, but the current is only 12,000 / 24,000 = 0.5 A. The wires now waste 0.5 x 0.5 x 0.8 = 0.2 W. Not 2,000 W: two tenths of one watt. The only catch is that nobody wants 24,000 V inside a kitchen, so near the town you have to bring the voltage back down. The machine that does that, the transformer, only works when the current keeps changing direction. That is the whole reason your wall socket gives you alternating current. This lesson tells that story with numbers.

## The Physics

### What "alternating" means physically

In a battery circuit (Phase 02), the battery pushes charges round the loop in one direction, always. The voltage across the battery has a fixed sign: the `+` terminal is always higher than the `-` terminal. We call that **direct current**, DC.

At a wall socket, the two holes swap roles all the time. For a hundredth of a second one hole is "higher" than the other, then the other one is higher for the next hundredth of a second, and so on. The charges in the wires of your lamp do not travel from the power station to your house. They shuffle a tiny distance one way, then the same distance back, fifty times a second. **Alternating current**, AC, is that shuffling.

```
   DC (battery)                      AC (wall socket)
 V                                 V
 |  ___________________            |   _       _       _
 |                                 |  / \     / \     / \
 |                                 | /   \   /   \   /   \
 +-------------------- t           +-------\-/-----\-/-----\--- t
                                   |        V       V
```

Does the shuffling deliver energy if the charges never get anywhere? Yes. Think of a saw: the blade goes back and forth and ends up where it started, but the wood still gets cut. The energy is handed from charge to charge through the electric field (Phase 01, Lesson 05), and the lamp filament gets hot whether the charges move left or right: what heats it is the current, and the heat does not care about the direction. (In Lesson 03 you will see exactly how to compare "how much heating" an AC current gives with a DC one.)

### Where AC comes from

You met the generator in Phase 08, Lesson 07: a coil spinning inside a magnetic field. As the coil turns, the magnetic flux through it grows, shrinks, reverses, and grows again. Faraday's law (Phase 08, Lesson 03) says the induced voltage is set by how fast the flux changes, and a steadily spinning coil makes that voltage swing smoothly up and down in the shape of a **sine wave** (Lesson 02 of this phase). So a spinning generator gives you AC naturally. Getting DC out of it needs extra parts (a commutator, or the diodes of Phase 11).

### Where the heat in the wires comes from

From Phase 03, Lesson 05: a resistor that carries current I has power turned into heat equal to

```
P = I x I x R      (read: "power equals current times current times resistance")
```

with P in watts (W), I in amperes (A) and R in ohms. The current appears **twice**. Double the current and the wires get four times hotter. That square is the hero of this story.

And from Phase 01, Lesson 09, the power delivered to a load is

```
P = V x I          (read: "power equals voltage times current")
```

So, for a fixed power the town needs, the current is I = P / V. Put that into the heat formula:

```
loss = (P / V) x (P / V) x R = P^2 x R / V^2
```

Read it aloud: "the loss in the wires equals the power squared times the wire resistance, divided by the voltage squared". Multiply the voltage by 10 and the loss drops by 10 x 10 = 100. Multiply by 100 and it drops by 10,000.

### Why the transformer needs AC

You built the transformer in Phase 08, Lesson 06: two coils wound on the same iron core. A current in the first coil (the primary) makes a magnetic field in the core. If that field **changes**, Faraday's law induces a voltage in the second coil (the secondary). The voltage is scaled by the ratio of the number of turns: a coil with 10 times fewer turns gives 10 times less voltage, and (because energy is conserved) can deliver about 10 times more current.

The key word is **changes**. A steady DC current makes a steady field, and a steady field induces nothing. A transformer on a battery just sits there as a thick piece of wire (which, by the way, will get very hot). Feed it AC and the field is always changing, so the transformer works all the time. Until the 1960s, when power transistors and later thyristors and IGBTs appeared, there was no practical, efficient way to change a DC voltage up or down at power-station scale. AC plus transformers was the only option, and it was a very good one.

## The Concept

### The problem in one table

Let us redo the opening story for several transmission voltages. The town always needs 12,000 W; the line always has 0.8 ohm in total.

| Line voltage | Current I = P / V | Loss = I x I x R | Loss as % of 12 kW | Voltage lost in wires = I x R |
|---|---|---|---|---|
| 240 V | 12,000 / 240 = 50 A | 50 x 50 x 0.8 = 2,000 W | 16.7 % | 50 x 0.8 = 40 V |
| 2,400 V | 5 A | 5 x 5 x 0.8 = 20 W | 0.17 % | 4 V |
| 24,000 V | 0.5 A | 0.5 x 0.5 x 0.8 = 0.2 W | 0.0017 % | 0.4 V |
| 240,000 V | 0.05 A | 0.002 W | 0.000017 % | 0.04 V |

Every factor of 10 in voltage buys a factor of 100 in loss. Real grids carry power hundreds of kilometres at 110,000 to 765,000 volts for exactly this reason.

You could also cut the loss by making the wires thicker (smaller R). But copper is heavy and expensive: to cut the loss by 100 at 240 V you would need wires 100 times thicker in cross-section. Raising the voltage is almost free by comparison: it needs better insulation and taller pylons, not more metal.

### The loss of a fixed load

The table above cheats a little: it assumes the town always takes exactly 12 kW at whatever voltage reaches it. Real loads behave more like resistors. A 12 kW, 240 V town behaves roughly like one resistor of

```
R_town = V^2 / P = 240 x 240 / 12,000 = 4.8 ohm
```

(from P = V x I and I = V / R, so P = V x V / R).

Connect that 4.8 ohm load straight to a 240 V source through the 0.8 ohm of line:

```
   plant                 0.4 ohm (wire there)          town
   +240 V o----------------/\/\/\-------------------o
          |                                          |
         ---  generator                            [4.8 ohm]  the town as one resistor
          -                                          |
          |                                          |
   0 V    o----------------/\/\/\-------------------o
                         0.4 ohm (wire back)
```

The total resistance in the loop is 0.4 + 4.8 + 0.4 = 5.6 ohm (Phase 04: series resistances add). The current is 240 / 5.6 = 42.86 A. The town gets 42.86 x 42.86 x 4.8 = 8,816 W instead of 12,000 W, the wires burn 42.86 x 42.86 x 0.8 = 1,469 W, and the houses see 42.86 x 4.8 = 205.7 V.

### What a transformer does to a load

Now put a step-up transformer at the plant and a step-down transformer at the town. Say the step-down has a **turns ratio** of 10:1 (ten turns on the line side for every turn on the house side). Then:

- the house side voltage is 1/10 of the line side voltage;
- the house side current is 10 times the line side current (energy in = energy out for an ideal transformer).

Seen from the line, how big does the 4.8 ohm town look? Call the house voltage V_h and the house current I_h, so V_h / I_h = 4.8 ohm. On the line side, the voltage is 10 x V_h and the current is I_h / 10. Their ratio is

```
(10 x V_h) / (I_h / 10) = 100 x (V_h / I_h) = 100 x 4.8 ohm = 480 ohm
```

Read it: "a load behind an n-to-1 step-down transformer looks n squared times bigger from the line". This is called the **reflected** resistance, and it lets us simulate the whole thing with resistors only: plant source, 0.4 ohm, a 480 ohm "town as seen through the transformer", 0.4 ohm back.

With the plant at 2,400 V (the 240 V of the generator stepped up by 10): current = 2,400 / (480 + 0.8) = 4.992 A. The wires waste 4.992 x 4.992 x 0.8 = 19.9 W. The town receives 4.992 x 4.992 x 480 = 11,960 W. The house voltage is 4.992 x 480 / 10 = 239.6 V. Much better. With a 100:1 ratio and 24,000 V on the line, the town gets 11,999.6 W and the houses see 240.0 V.

### The same problem inside your house

Line loss is not only a power-station problem. Say an electric oven of 3,000 W sits at the end of 20 m of household cable. The current must go there and come back, so there are 40 m of copper; for a common 2.5 mm^2 cable, that is about 0.27 ohm (Phase 03, Lesson 02: R = resistivity x length / area = 1.7e-8 x 40 / 2.5e-6 = 0.27 ohm).

- At 230 V, the current is 3,000 / 230 = 13.0 A. The cable wastes 13.0 x 13.0 x 0.27 = 46 W and drops 13.0 x 0.27 = 3.5 V.
- At 120 V (American mains), the current would be 3,000 / 120 = 25 A. The same cable would waste 25 x 25 x 0.27 = 169 W, almost four times more, and drop 6.8 V.

That is one reason why American houses use thicker cables for big appliances, and why large American appliances (ovens, dryers) are connected to 240 V instead of 120 V.

### The war of the currents (a short history)

- **1882.** Thomas Edison opens the Pearl Street Station in New York: DC at about 110 V. It works, but the losses we just computed limit each station to customers within roughly a mile or two. A city would need a power station every few blocks.
- **1881-1885.** Lucien Gaulard and John Gibbs in Europe show AC "secondary generators" (early transformers). In 1885, at the Ganz works in Budapest, Károly Zipernowsky, Ottó Bláthy and Miksa Déri build closed iron-core transformers connected in parallel: the design every grid still uses.
- **1886.** William Stanley, working for George Westinghouse, lights the town of Great Barrington, Massachusetts with a transformer-based AC system.
- **1888.** Nikola Tesla patents the AC induction motor (and Galileo Ferraris in Italy independently studies the rotating magnetic field). Westinghouse buys Tesla's patents. Now AC can drive factories, not only light bulbs.
- **Late 1880s.** Edison's camp campaigns hard against AC, stressing (correctly) that high-voltage AC can kill, and (with much exaggeration and some grim publicity stunts) that it is uniquely deadly. This is the "war of the currents".
- **1891.** A 175 km three-phase AC line carries power from Lauffen to the electrical exhibition in Frankfurt, Germany, at high voltage with good efficiency.
- **1893-1896.** Westinghouse lights the Chicago World's Fair with AC, then builds the Niagara Falls hydroelectric plant, which starts sending AC power to Buffalo, about 40 km away, in 1896. AC has won.

**Today, a twist.** Modern power electronics (Phase 18) can now convert DC voltages efficiently, so very long lines and undersea cables increasingly use **high-voltage DC** (HVDC), which avoids some AC problems you will meet in this phase (energy sloshing back and forth in the capacitance and inductance of long cables). Inside your devices, almost everything runs on low-voltage DC: the charger turns the AC from the wall into DC. AC dominates the middle of the system: generation, transformers and distribution.

### Why 50 or 60 hertz?

The frequency f is how many full cycles happen each second; the unit is the **hertz** (Hz), one cycle per second. The **period** T is how long one cycle lasts. They are reciprocals:

```
T = 1 / f      (read: "the period is one divided by the frequency")
```

At f = 50 Hz, T = 1 / 50 = 0.02 s = 20 milliseconds (ms). At 60 Hz, T = 1 / 60 = 0.01667 s = 16.67 ms. In each cycle the current flows one way and then the other, so the direction flips 2 x 50 = 100 times per second at 50 Hz.

Early systems used anything from about 25 Hz to over 130 Hz. Engineers settled on a compromise:

- **Too low** (say 25 Hz): light bulbs visibly flicker, and transformers must be bigger and heavier (a transformer's iron core must be larger the slower the field changes, for the same power).
- **Too high** (say 400 Hz): long lines and motors behave worse, because, as you will see in Lesson 06, inductances "resist" faster changes more strongly.

North America standardised on 60 Hz, most of the rest of the world on 50 Hz. Japan is split in two: eastern Japan (Tokyo) uses 50 Hz with equipment originally bought from Germany, western Japan (Osaka) uses 60 Hz with American equipment, and they still need special converter stations to share power. Aircraft use 400 Hz precisely because the transformers become lighter.

### What AC costs us

AC is not free:

- A sine wave of "230 V" actually peaks at about 325 V. Insulation must survive the peak (Lesson 03 explains the 230 V figure).
- With capacitors and inductors in the circuit, current and voltage get out of step, and some energy sloshes back and forth without doing work (Lesson 07, power factor).
- All generators on a grid must spin in lock-step at exactly the same frequency.
- You need new mathematics to analyse AC circuits quickly. That is what Lessons 04 to 06 build: complex numbers, phasors and impedance.

## Build It

The script `code/main.py` redoes the numbers above: first with the formula, then with our simulator, then a small table of mains systems.

### Step 1: Loss by formula

```python
TOWN_POWER_W = 12_000.0
LINE_RESISTANCE_EACH_WIRE = 0.4
HOUSE_VOLTAGE = 240.0


def loss_by_formula(power_w, voltage_v, line_resistance_total):
    current = power_w / voltage_v
    loss = current**2 * line_resistance_total
    drop = current * line_resistance_total
    return current, loss, drop
```

`current**2` is Python for "current squared". For 240 V the function returns 50 A, 2,000 W and 40 V, exactly as computed by hand. The script loops over 240 V, 2,400 V, 24,000 V and 240,000 V and prints one row per voltage.

### Step 2: Simulate the line with a fixed load

```python
def send_power(source_volts, turns_ratio):
    load_resistance = HOUSE_VOLTAGE**2 / TOWN_POWER_W
    load_seen_by_line = load_resistance * turns_ratio**2
    c = Circuit()
    c.voltage_source("V1", "plant", "0", source_volts)
    c.resistor("Rgo", "plant", "town", LINE_RESISTANCE_EACH_WIRE)
    c.resistor("Rload", "town", "back", load_seen_by_line)
    c.resistor("Rreturn", "back", "0", LINE_RESISTANCE_EACH_WIRE)
    r = c.dc()
    line_current = r.i("Rgo")
    line_loss = r.p("Rgo") + r.p("Rreturn")
    delivered = r.p("Rload")
    house_volts = r.v("town", "back") / turns_ratio
    return line_current, line_loss, delivered, house_volts
```

The transformers are not simulated as coils: we use the reflected resistance `load_resistance * turns_ratio**2` you derived above. A DC operating point is good enough here, because at any single instant a resistor obeys Ohm's law whether the source is AC or DC, and (as Lesson 03 will justify) "240 V AC" is defined so that it heats a resistor exactly like 240 V DC.

Expected output, Step 2:

```
  send at     240 V (step-down   1:1): line current  42.857 A, line loss   1469.39 W, delivered    8816.3 W, house sees  205.7 V
  send at    2400 V (step-down  10:1): line current   4.992 A, line loss     19.93 W, delivered   11960.1 W, house sees  239.6 V
  send at   24000 V (step-down 100:1): line current   0.500 A, line loss      0.20 W, delivered   11999.6 W, house sees  240.0 V
```

### Step 3: Mains around the world

The last block prints voltage, frequency, period (1000 / f in milliseconds) and how many times per second the current reverses (2 x f). It ends with a fun number: at 50 Hz the grid completes 50 x 60 x 60 x 24 = 4,320,000 cycles a day.

Run it:

```
uv run python phases/09-alternating-current/01-why-alternating-current/code/main.py
```

## Use It

- **Your street.** A typical European chain: generator at around 10-25 kV, stepped up to 220-400 kV for transmission, down to 10-30 kV for regional distribution, and down again to 230 V (400 V between phases) by the grey transformer box or pole-top "can" near your house.
- **The phone charger.** It takes 230 V or 120 V AC, turns it into DC, chops it at tens of kilohertz, sends it through a tiny high-frequency transformer (high frequency means a much smaller core) and rectifies it again to 5 V DC. You will build pieces of this in Phases 11 and 18.
- **The doorbell or halogen transformer.** A small iron-core transformer turning 230 V AC into 8-12 V AC. It only works on AC: connect it to a 12 V battery and nothing useful happens.
- **HVDC links.** Undersea cables such as those between Norway and the UK or Germany, and very long overland lines in China and Brazil, use DC at hundreds of kilovolts, converted at each end with power electronics.
- **Labels on appliances.** Look at a laptop power brick: "Input 100-240 V ~ 50/60 Hz". The `~` symbol means AC. A battery-powered device shows a line with dashes underneath, the symbol for DC.

## Common Mistakes

- **"AC charges travel from the power station to my house."** They do not. They wiggle back and forth by far less than a millimetre. Energy travels through the field; charges stay roughly where they are.
- **"Higher voltage means more power is lost."** The opposite. For the same delivered power, higher voltage means lower current, and loss depends on current squared.
- **Using the wrong voltage in P = V^2 / R.** The formula `loss = V^2 / R_line` uses the voltage **across the wire**, not the transmission voltage. Using the line voltage here gives absurd answers (24,000^2 / 0.8 = 720 MW!). Compute the current first, then I x I x R.
- **Thinking a transformer works on DC.** It needs a changing magnetic field. On DC it is just a coil of wire with low resistance, and it will draw a huge current.
- **Mixing up frequency and period.** 50 Hz is "50 cycles per second"; the period is 1/50 of a second, 20 ms, not 50 ms.
- **Thinking AC is less dangerous because it "keeps changing direction".** Mains AC at 50-60 Hz is particularly good at disturbing the heart rhythm. Revisit Phase 00, Lesson 08. In this course we stay at low voltage.

## Exercises

1. **Period.** What is the period of a 400 Hz aircraft supply, in milliseconds? How many times per second does its current change direction?
2. **Loss table.** A farm 3 km away needs 6 kW. The line resistance (both wires) is 1.5 ohm. Compute the line current and the loss at 230 V and at 11,000 V. What percentage of 6 kW is lost in each case?
3. **Reflected load.** A 2 kW, 230 V heater sits behind a 50:1 step-down transformer. What is the heater's resistance? What resistance does the high-voltage line "see"?
4. **Thicker wire vs higher voltage.** In the 240 V example, the loss was 2,000 W. By how much would you need to reduce the line resistance to cut the loss to 20 W while keeping 240 V? Copper resistance is inversely proportional to cross-section area (Phase 03, Lesson 02): how much more copper is that?
5. **Simulator.** Modify `send_power` so the plant runs at 6,000 V with a 25:1 step-down. Predict the line current and the delivered power by hand before running it.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| AC | "The electricity from the wall" | Current and voltage that reverse direction periodically, at the wall usually as a 50 or 60 Hz sine wave |
| DC | "Battery electricity" | Current that flows in one direction only; voltage with a fixed sign |
| Frequency | "How fast it wiggles" | Number of complete cycles per second, in hertz |
| Period | "One wiggle" | Duration of one complete cycle, T = 1 / f |
| Transformer | "The box that changes the voltage" | Two magnetically coupled coils; changes AC voltage by the turns ratio and current by its inverse |
| Line loss | "Power lost on the way" | Heat I x I x R in the wires; falls as 1 / V^2 for a fixed delivered power |
| Reflected resistance | "What the load looks like from the other side" | A load R behind an n:1 step-down transformer appears as n^2 x R to the source side |
| HVDC | "DC power lines" | High-voltage DC transmission using power electronics converters, used for very long or undersea links |

## Further Reading

- [All About Circuits, Vol. II (AC), Chapter 1: Basic AC Theory](https://www.allaboutcircuits.com/textbook/alternating-current/chpt-1/what-is-alternating-current-ac/) — a free, gentle introduction to what AC is and why it is used.
- *The Art of Electronics*, Horowitz & Hill, 3rd ed., Chapter 1 (sections on signals and on transformers) — the engineer's view, short and practical.
- [Wikipedia: War of the currents](https://en.wikipedia.org/wiki/War_of_the_currents) and [Utility frequency](https://en.wikipedia.org/wiki/Utility_frequency) — well-sourced overviews of the history and of why 50 and 60 Hz were chosen.
- [Khan Academy: Electrical engineering, AC analysis](https://www.khanacademy.org/science/electrical-engineering/ee-circuit-analysis-topic) — short videos that will also cover the next lessons of this phase.
