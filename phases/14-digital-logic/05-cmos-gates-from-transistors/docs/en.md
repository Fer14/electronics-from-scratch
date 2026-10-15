# CMOS Gates from Transistors

> Pair every switch that pulls up with one that pulls down, and make sure only one of them is ever on: that is CMOS.

**Type:** Build
**Prerequisites:** Phase 12 (Transistors), Lesson 04 (The MOSFET) and Lesson 05 (The MOSFET as a Switch), Phase 14 (Digital Logic), Lessons 01-04
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| NMOS | A MOSFET that turns on when its gate is high compared with its source | A tap that opens when you push the handle up |
| PMOS | A MOSFET that turns on when its gate is low compared with its source | A tap that opens when you pull the handle down |
| CMOS | "Complementary MOS": logic built from NMOS and PMOS in matched pairs | A see-saw: when one end is up the other is down |
| Pull-up network | The transistors that connect the output to the supply | A hand lifting the output to 1 |
| Pull-down network | The transistors that connect the output to ground | A hand pushing the output to 0 |
| Threshold voltage (Vth) | The gate-to-source voltage at which a MOSFET starts to conduct | The minimum push needed before a door starts to open |
| Voltage transfer curve (VTC) | A graph of output voltage against input voltage | A map of how a gate reacts to every possible input |
| Switching point (VM) | The input voltage where the output equals the input | The balance point of a see-saw |
| Static power | Power drawn while nothing changes | A car engine idling |
| Dynamic power | Power drawn because outputs switch and charge capacitances | Fuel burned each time you accelerate |
| Load capacitance | The capacitance of the wires and inputs an output must charge | A bucket you must fill every time you say "1" |
| Leakage | The tiny current that flows through a transistor that is "off" | A tap that drips even when closed |

## Learning Objectives

- Explain how an NMOS and a PMOS behave as voltage-controlled switches.
- Build a CMOS inverter in the simulator and plot its voltage transfer curve.
- Find the switching point and the unity-gain points (VIL, VIH) of an inverter and compute its noise margins.
- Build CMOS NAND and NOR gates from four transistors each and explain the series/parallel duality.
- Explain why a CMOS gate draws almost no current when idle, and compute dynamic power with `P = α C V^2 f`.
- Explain why NAND is preferred over NOR on real chips.

## The Problem

Lesson 04 treated gates as black boxes that "just compute". A processor has billions of them on a chip the size of a fingernail, running billions of times per second, on a battery. If each gate wasted even one microampere while idle, a billion gates would waste a thousand amperes. The phone would melt.

Early logic families did waste power. Resistor-transistor logic (RTL) and transistor-transistor logic (TTL) used resistors to pull outputs up, so current flowed whenever an output was low. A 1970s TTL gate drew a few milliamperes all the time. The breakthrough that made today's chips possible was CMOS, invented by Frank Wanlass at Fairchild in 1963: a way of building gates that, once settled, draw essentially no current at all. This lesson builds CMOS gates from the MOSFET models in our simulator and measures why they work so well.

## The Physics

### The MOSFET as a switch, revisited

Phase 12 introduced the MOSFET: a channel between **drain** (d) and **source** (s) whose conductivity is controlled by the voltage on the **gate** (g). The gate is insulated by a thin oxide layer, so it draws no steady current, like the plate of a capacitor.

An **NMOS** conducts when its gate is above its source by more than the threshold voltage `Vth`. In our simulator, with `Vth = 1 V`, an NMOS with its source on ground is:

```
gate at 0 V  ->  Vgs = 0 V  < 1 V   ->  OFF (open switch)
gate at 5 V  ->  Vgs = 5 V  > 1 V   ->  ON  (closed switch, a few hundred ohms)
```

A **PMOS** is the mirror image. Its channel carries holes instead of electrons (Phase 11, Lesson 02), and it conducts when its gate is **below** its source by more than `Vth`. With its source on the 5 V supply:

```
gate at 0 V  ->  Vsg = 5 V  > 1 V   ->  ON
gate at 5 V  ->  Vsg = 0 V  < 1 V   ->  OFF
```

So for the same gate voltage, an NMOS and a PMOS do opposite things. That opposite behaviour is the "complementary" in CMOS.

The NMOS is good at pulling a node **down** to ground: as the drain falls toward 0 V, its `Vgs` stays at 5 V and it stays strongly on. It is bad at pulling up: an NMOS trying to pull a node toward 5 V turns itself off when the node reaches `5 V - Vth = 4 V`. The PMOS is the opposite: good at pulling up, bad at pulling down. So in CMOS, **NMOS transistors always sit in the pull-down network and PMOS transistors in the pull-up network.**

### How much current flows

Our simulator uses the classic square-law model. Say it in words first: "when the transistor is on and its drain voltage is large enough (saturation), the current is half of k times the square of how far the gate voltage exceeds the threshold". In symbols, with `k` in amperes per volt squared (A/V^2):

```
saturation (Vds >= Vgs - Vth):   I = 0.5 x k x (Vgs - Vth)^2
linear     (Vds <  Vgs - Vth):   I = k x ((Vgs - Vth) x Vds - 0.5 x Vds^2)
off        (Vgs <= Vth):         I = 0
```

With `k = 1 mA/V^2`, `Vgs = 5 V` and a small `Vds`, the linear formula is about `k x (Vgs - Vth) x Vds`, so the transistor acts like a resistor of `1 / (k x (Vgs - Vth)) = 1 / (0.001 x 4) = 250 Ω`. That is the "on resistance" that charges and discharges the output.

### Electrons are faster than holes

In silicon, electrons move about two to three times more easily than holes (their mobility is higher). A PMOS of the same size as an NMOS therefore conducts about 2-3 times less current. Chip designers compensate by making PMOS transistors wider. This fact explains why NAND gates are preferred to NOR gates, as we will see.

## The Concept

### The CMOS inverter

Put one PMOS from the supply to the output and one NMOS from the output to ground, and tie both gates to the input:

```
            VDD (5 V)
              |
           s  |
        +--o|[  PMOS (MP)
        |  d  |
  in ---+     +------- out
        |  d  |
        +---|[  NMOS (MN)
           s  |
              |
             GND
```

(The `o` on the PMOS gate is the same "invert" bubble as on a gate symbol: it turns on with a low gate.)

- **in = 0 V:** the PMOS is on (`Vsg = 5 V`), the NMOS is off (`Vgs = 0 V`). The output is connected to 5 V through about 250 Ω and to nothing else. Output = 5 V, a logic 1.
- **in = 5 V:** the PMOS is off, the NMOS is on. Output = 0 V, a logic 0.

In both settled states, **one of the two transistors is off**, so there is no path from the supply to ground. No current flows (apart from tiny leakage). That is the whole secret of CMOS: the static power is essentially zero.

Compare with a resistor pull-up (like the "NMOS with a resistor" inverter in Phase 12): with in = 5 V, the NMOS pulls the output low, and current `5 V / R` flows through the resistor the whole time. With R = 1 kΩ that is 5 mA, 25 mW, per gate, forever.

### The voltage transfer curve

What happens between 0 and 5 V? Sweep the input slowly and record the output. Our simulator gives (both transistors `Vth = 1 V`, `k = 1 mA/V^2`):

```
 Vin (V) | Vout (V) | supply current
 --------+----------+---------------
   0.00  |  5.000   |  0.000 mA       NMOS off
   1.00  |  5.000   |  0.000 mA       NMOS just at threshold
   2.00  |  4.732   |  0.500 mA       both on, output starts to fall
   2.40  |  4.175   |  0.980 mA
   2.60  |  0.825   |  0.980 mA       the steep part
   3.00  |  0.268   |  0.500 mA
   4.00  |  0.000   |  0.000 mA       PMOS off
   5.00  |  0.000   |  0.000 mA
```

Drawn as a graph:

```
 Vout
 5 V |*********.
     |          *.
     |            *
     |            |
 2.5 |- - - - - - + - - - - -    switching point VM = 2.5 V
     |            |
     |            *
     |             '*.
 0 V +------------+---*********--- Vin
     0           2.5            5 V
```

Check the Vin = 2.00 V row by hand. The NMOS has `Vgs = 2 V`, so `Vgs - Vth = 1 V`; its drain (the output) is high, so it is in saturation: `I = 0.5 x 0.001 x 1^2 = 0.5 mA`. The same current must flow through the PMOS, which has `Vsg = 5 - 2 = 3 V`, overdrive 2 V, and is in its linear region with a small `Vsd`:

```
0.001 x (2 x Vsd - 0.5 x Vsd^2) = 0.0005
Vsd^2 - 4 Vsd + 1 = 0
Vsd = 2 - sqrt(3) = 0.268 V
Vout = 5 - 0.268 = 4.732 V
```

which is exactly the table's value.

Three features of this curve make it a good logic gate:

1. **Flat ends.** For inputs near 0 V the output is exactly 5 V, and for inputs near 5 V exactly 0 V. Small input errors produce no output error: that is regeneration (Lesson 01) in transistor form.
2. **A steep middle.** Around 2.5 V a tiny input change swings the output by volts. The slope there is the inverter's gain. With ideal transistors (no channel-length modulation) the curve is vertical at exactly 2.5 V.
3. **Current only in the middle.** The supply current peaks at the switching point, where both transistors are on: `0.5 x 0.001 x (2.5 - 1)^2 = 1.125 mA`. At either end it is about `10^-11 A`, the simulator's small leakage conductance.

### Switching point and noise margins

The **switching point** `VM` is where `Vout = Vin`. For matched transistors (same `k` and `Vth`), symmetry gives `VM = VDD / 2 = 2.5 V`.

Lesson 01 defined VIL and VIH as datasheet guarantees. For a single gate, a natural choice is the two input voltages where the curve's slope is exactly -1: below VIL the gate attenuates disturbances (slope flatter than -1), between VIL and VIH it amplifies them. The simulator finds `VIL = 2.13 V` and `VIH = 2.87 V`. With `VOL = 0 V` and `VOH = 5 V`:

```
NML = VIL - VOL = 2.13 - 0 = 2.13 V
NMH = VOH - VIH = 5 - 2.87 = 2.13 V
```

Real 74HC parts guarantee less (1.5 V and 3.5 V, Lesson 01) because they must cover every chip, every temperature and every supply from 2 V to 6 V.

### When the PMOS is weaker

If the PMOS conducts less (`k_p` smaller than `k_n`, because holes are slower), the NMOS wins the tug-of-war earlier and the switching point moves down. Setting the two saturation currents equal:

```
0.5 k_n (VM - Vth)^2 = 0.5 k_p (VDD - VM - Vth)^2
```

Take square roots and let `r = sqrt(k_n / k_p)`:

```
r (VM - Vth) = VDD - VM - Vth
VM = (VDD - Vth + r x Vth) / (1 + r)
```

With `k_p = 0.4 mA/V^2`: `r = sqrt(1 / 0.4) = 1.58`, so `VM = (5 - 1 + 1.58) / 2.58 = 2.16 V`. The simulator agrees. This is why designers make the PMOS about 2-3 times wider: to bring the switching point back to the middle and balance rise and fall times.

### NAND from four transistors

The rule for any CMOS gate is: **the pull-down network conducts exactly when the output should be 0, and the pull-up network is its dual**, with series and parallel swapped and NMOS replaced by PMOS. Then exactly one network conducts for every input, and there is never a static path from supply to ground.

A NAND output is 0 only when `a = 1` **and** `b = 1`. "And" in switches means series (Lesson 03). So the pull-down is two NMOS in series. The dual pull-up is two PMOS in parallel:

```
              VDD
          +----+----+
          |         |
   a --o|[ MPA     o|[ MPB -- b         two PMOS in parallel
          |         |
          +----+----+
               |
               +---------- out
               |
         a ---|[ MNA                    two NMOS in series
               |
              mid
               |
         b ---|[ MNB
               |
              GND
```

Check all four rows. Remember: an NMOS is on when its gate is 1, a PMOS when its gate is 0.

```
 a b | MNA MNB | series path? | MPA MPB | parallel path? | out
 0 0 | off off |     no       | on  on  |     yes        |  1
 0 1 | off on  |     no       | on  off |     yes        |  1
 1 0 | on  off |     no       | off on  |     yes        |  1
 1 1 | on  on  |     yes      | off off |     no         |  0
```

Exactly one path conducts in each row, and the output column is NAND. The simulator measures 5.00 V, 5.00 V, 5.00 V and 0.00 V, with supply currents around `10^-11 A` in every row.

### NOR from four transistors

NOR is 0 when `a = 1` **or** `b = 1`: the pull-down is two NMOS in **parallel**, and the pull-up two PMOS in **series**.

```
              VDD
               |
         a --o|[ MPA
               |
              mid
               |
         b --o|[ MPB
               |
               +---------- out
          +----+----+
   a ---|[ MNA     |[ MNB --- b
          |         |
          +----+----+
              GND
```

### Why AND and OR cost more

A single CMOS stage always inverts: a high input can only turn on NMOS transistors, which pull the output down. So the natural gates are NOT, NAND and NOR. An AND gate is a NAND followed by an inverter: 4 + 2 = 6 transistors and two stages of delay. Transistor counts:

```
gate   transistors   built as
NOT        2         1 PMOS + 1 NMOS
NAND2      4         2 PMOS parallel + 2 NMOS series
NOR2       4         2 PMOS series + 2 NMOS parallel
AND2       6         NAND2 + NOT
OR2        6         NOR2 + NOT
XOR2      8-12       depends on the design
```

This is the real reason Lesson 04's NAND-only designs matter.

### Why NAND beats NOR

In a NAND, the slow PMOS transistors are in **parallel**, and the fast NMOS transistors are in series. In a NOR, the slow PMOS are in **series**, which doubles their resistance on top of their weakness. To pull up as fast as an inverter, a NOR2's PMOS must be about twice as wide again, so a NOR is bigger and slower than a NAND with the same number of inputs. Standard cell libraries (Phase 20) therefore have fast, compact NANDs, and synthesis tools prefer them. Gates with many inputs are avoided for the same reason: four transistors in series are slow, so a wide AND is usually built as a tree of smaller gates.

### Dynamic power: the cost of switching

If CMOS draws no current when idle, where does a processor's 50 W go? Into **switching**. Every gate output drives a load capacitance `C`: the gates of the next transistors and the wires. Charging it from 0 to `VDD` takes energy `C x VDD^2` from the supply (Phase 07, Lesson 06: half is stored in the capacitor, half is burned in the PMOS while charging; when the output falls, the stored half is burned in the NMOS). So each full 0-1-0 cycle of an output costs `C VDD^2`.

The simulator confirms it. An inverter driving a 1 pF load, switched once per microsecond, draws 25.5 pJ from the supply per cycle, against `C x VDD^2 = 1e-12 x 5^2 = 25 pJ` (the extra half picojoule is the brief through-current while both transistors are on during the 1 ns input edge).

For a whole chip, say it as a sentence first: "the switching power equals the fraction of gates that switch each cycle, times the total switched capacitance, times the supply voltage squared, times the clock frequency". In symbols:

```
P = α x C x VDD^2 x f
```

where `α` (alpha) is the **activity factor**, the fraction of the capacitance that switches per clock cycle. Example: a chip with 1 nF of total switched capacitance, 10 % activity, at 1.0 V and 3 GHz:

```
P = 0.1 x 1e-9 F x (1.0 V)^2 x 3e9 Hz = 0.3 W
```

The `VDD^2` is why chips run at ever lower voltages: going from 5 V to 1 V divides switching energy by 25. It is also why phones lower their voltage and clock when idle ("dynamic voltage and frequency scaling").

### Leakage: why "off" is not quite off

In modern chips with transistors only a few nanometres long, an "off" transistor still leaks a little current, and billions of them leak a lot: leakage can be a third of a processor's power. That is why idle parts of a chip are not just stopped but completely disconnected from the supply ("power gating"). Our simulator models leakage only as a tiny `10^-12 S` conductance, which is why it prints currents around `10^-11 A`.

## Build It

The script `code/main.py` builds CMOS gates out of the simulator's `nmos` and `pmos` devices and measures them.

### Step 1: A CMOS inverter

```python
VDD = 5.0
VTH = 1.0
K = 1e-3

def inverter(k_p=K):
    c = Circuit("CMOS inverter")
    c.voltage_source("VDD", "vdd", "0", VDD)
    c.voltage_source("VIN", "in", "0", 0.0)
    c.pmos("MP", d="out", g="in", s="vdd", vth=VTH, k=k_p)
    c.nmos("MN", d="out", g="in", s="0", vth=VTH, k=K)
    return c
```

The PMOS has its source on `vdd` and the NMOS its source on ground, exactly as in the drawing.

### Step 2: Sweep the input

`Circuit.sweep(name, values)` re-solves the DC operating point for every value of one source. We sweep `VIN` from 0 to 5 V in 10 mV steps and read the output voltage and the supply current.

```python
def transfer_curve(k_p=K):
    vin = np.linspace(0.0, VDD, 501)
    sweep = inverter(k_p).sweep("VIN", vin)
    vout = np.asarray(sweep.v("out"))
    supply = np.abs(np.asarray(sweep.i("VDD")))
    return vin, vout, supply
```

### Step 3: Switching point and unity-gain points

```python
def switching_point(vin, vout):
    index = int(np.argmin(np.abs(vout - vin)))
    return vin[index]

def unity_gain_points(vin, vout):
    slope = np.gradient(vout, vin)
    steep = np.where(slope < -1.0)[0]
    return vin[steep[0]], vin[steep[-1]]
```

`np.gradient` estimates the slope between neighbouring points; the first and last points steeper than -1 are VIL and VIH. Output:

```
  switching point (Vout = Vin): 2.50 V
  slope = -1 points: VIL = 2.13 V, VIH = 2.87 V
  noise margins with VOL = 0, VOH = 5 V: NML = 2.13 V, NMH = 2.13 V
  peak through-current at Vin = 2.5 V: 1.125 mA (hand: 0.5 x 1e-3 x (2.5 - 1)^2 = 1.125 mA)
  static current with Vin = 0 V: 1.5e-11 A, with Vin = 5 V: 1.0e-11 A
```

With `k_p = 0.4 mA/V^2` the script reports a switching point of 2.16 V, matching the hand formula.

### Step 4: NAND and NOR

```python
def nand_gate(a, b):
    c = Circuit("CMOS NAND")
    c.voltage_source("VDD", "vdd", "0", VDD)
    c.voltage_source("VA", "a", "0", a)
    c.voltage_source("VB", "b", "0", b)
    c.pmos("MPA", d="out", g="a", s="vdd", vth=VTH, k=K)
    c.pmos("MPB", d="out", g="b", s="vdd", vth=VTH, k=K)
    c.nmos("MNA", d="out", g="a", s="mid", vth=VTH, k=K)
    c.nmos("MNB", d="mid", g="b", s="0", vth=VTH, k=K)
    return c
```

`nor_gate` swaps the arrangement: the PMOS in series through a node `mid`, the NMOS in parallel. The script runs a DC analysis for each of the four input combinations:

```
  NAND:  a  b |  Vout     bit | supply current
        0  0 |  5.00 V   1   | 1.3e-11 A
        0  1 |  5.00 V   1   | 1.5e-11 A
        1  0 |  5.00 V   1   | 1.8e-11 A
        1  1 |  0.00 V   0   | 1.5e-11 A
```

The voltages are clean rails and the static currents are tens of picoamperes, the simulator's leakage floor.

### Step 5: Dynamic energy

We drive the inverter with a square wave and a 1 pF load, run a transient simulation for two periods and integrate the supply current over the second period (the first one includes the start-up).

```python
def switching_energy(load_farads=1e-12, period=1e-6):
    c = Circuit("inverter driving a load")
    c.voltage_source("VDD", "vdd", "0", VDD)
    c.pulse_source("VIN", "in", "0", low=0.0, high=VDD, period=period, duty=0.5, rise=1e-9, fall=1e-9)
    c.pmos("MP", d="out", g="in", s="vdd", vth=VTH, k=K)
    c.nmos("MN", d="out", g="in", s="0", vth=VTH, k=K)
    c.capacitor("CL", "out", "0", load_farads)
    t = c.transient(t_stop=2 * period, dt=period / 4000)
    time = np.asarray(t.time)
    supply = np.abs(np.asarray(t.i("VDD")))
    second = time >= period
    energy = VDD * np.trapezoid(supply[second], time[second])
    return energy, VDD * load_farads * VDD
```

Energy is voltage times charge, and charge is the time integral of current; `np.trapezoid` does that integral. The script prints 25.5 pJ against the formula's 25.0 pJ.

Run it:

```bash
uv run python phases/14-digital-logic/05-cmos-gates-from-transistors/code/main.py
```

## Use It

- **74HC and 74LVC chips** are CMOS. The 74HC00 datasheet lists a quiescent supply current of at most a few microamperes for the whole chip (four gates), and a "power dissipation capacitance" CPD of around 20 pF per gate, which you plug into `P = CPD x VCC^2 x f` to get its dynamic power.
- **Microcontrollers** (Phase 17) sleep at a few microamperes because their CMOS logic draws almost nothing when the clock is stopped.
- **Processors** run at 0.7-1.2 V cores and change voltage and frequency hundreds of times per second to trade speed against power.
- **The CD4000 series** (RCA, 1968) was the first popular CMOS logic family; it could run from 3 to 15 V, and its very low power made digital watches and pocket calculators practical.
- **Latch-up and ESD.** Real CMOS chips have protection diodes on every input. Driving an input above VDD or below ground can forward-bias them and, in bad cases, trigger latch-up, a short circuit inside the chip. Never drive a powered-off CMOS chip's inputs.

## Try It in the Lab

The lab task "Pick the pull-up of a CMOS inverter" shows two copies of the same inverter with its NMOS pull-down already placed. One has its input held at 0 V, the other at 5 V. For each, choose the pull-up from a PMOS, an NMOS, a 1 kΩ resistor and a 100 kΩ resistor. The goals: the first output above 4.5 V, the second below 0.5 V, and the battery delivering less than 1 µA.

Think about: which part is on when its gate is at 0 V and off when its gate is at 5 V? For a resistor pull-up, how much current flows when the NMOS below it is on?

## Common Mistakes

- **Putting an NMOS in the pull-up.** An NMOS can only pull its source up to `VG - Vth`, so its "1" is weak (4 V instead of 5 V with `Vth = 1 V`), and it is slow. NMOS pulls down, PMOS pulls up.
- **Forgetting the PMOS source goes to VDD.** A PMOS is on when its gate is low **relative to its source**. If you put the source on the output, the transistor behaves very differently.
- **Making both networks conduct at once.** If the pull-up and pull-down are not exact duals, some input will turn both on and short the supply through the transistors. Always check every row.
- **Thinking CMOS draws no power at all.** It draws almost none when idle. Every switching event costs `C VDD^2`, and at GHz rates that is most of a chip's power.
- **Driving CMOS inputs slowly.** An input that lingers in the middle region keeps both transistors on and wastes current (the 1.125 mA peak above). This is why slow or noisy signals go through a Schmitt-trigger input (Phase 13, Lesson 02).

## Exercises

1. An NMOS with `k = 2 mA/V^2` and `Vth = 0.7 V` has its gate at 3.3 V and its source on ground. Estimate its on-resistance for small `Vds`.
2. In the inverter table, check the row Vin = 3.00 V by hand: which transistor is in saturation, which in the linear region, and what is Vout? (Answer: 0.268 V, the mirror of the 2.00 V row.)
3. Draw the transistor diagram of a 3-input NAND. How many transistors does it need? Which ones are in series?
4. With `k_n = 1 mA/V^2`, `k_p = 0.5 mA/V^2`, `Vth = 1 V` and `VDD = 5 V`, compute the switching point. How wide must the PMOS be, relative to now, to bring it back to 2.5 V?
5. A microcontroller core has 200 pF of switched capacitance with 15 % activity. Compute its dynamic power at 3.3 V and 48 MHz, and at 1.8 V and 48 MHz. What fraction of power is saved by the lower voltage?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| CMOS | "The chip technology" | Logic where an NMOS pull-down network and its dual PMOS pull-up network never conduct at the same time once settled |
| Pull-up / pull-down network | "The top and bottom halves" | PMOS switches to VDD and NMOS switches to ground, arranged as series/parallel duals |
| Voltage transfer curve | "The VTC" | Output voltage versus input voltage; flat ends regenerate, the steep middle gives gain |
| Switching point | "VM" | The input voltage where Vout = Vin; VDD/2 for matched transistors |
| Static power | "Idle power" | Power with no switching; nearly zero in CMOS apart from leakage |
| Dynamic power | "Switching power" | `α C VDD^2 f`: energy spent charging and discharging load capacitance |
| Leakage | "Off current" | Current through transistors that are nominally off; significant in nanometre chips |

## Further Reading

- Neil H. E. Weste and David Money Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*, Chapters 1-2 (CMOS logic, the inverter DC transfer characteristic) and Chapter 5 (power).
- Jan M. Rabaey, Anantha Chandrakasan and Borivoje Nikolić, *Digital Integrated Circuits: A Design Perspective*, Chapter 5 (the CMOS inverter).
- Texas Instruments application report SCAA035, *CMOS Power Consumption and CPD Calculation*.
- MIT OpenCourseWare 6.002 *Circuits and Electronics* (Agarwal and Lang), lectures on the MOSFET switch and the CMOS inverter.
