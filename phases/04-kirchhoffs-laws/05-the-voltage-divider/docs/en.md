# The Voltage Divider

> Two resistors in a row share the voltage in proportion to their size. Change the ratio and you choose the voltage.

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Phase 04 lessons 01-04 (nodes, KCL, KVL, series and parallel resistors)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Voltage divider | Two (or more) resistors in series whose middle point gives a smaller voltage than the source | A staircase from the top floor to the ground: the landing is partway down |
| Input voltage (Vin) | The voltage you feed into the top of the divider, measured from ground | The height of the top floor |
| Output voltage (Vout) | The voltage at the middle point, measured from ground | The height of the landing |
| Tap / midpoint | The node between the two resistors where you take the output | Where you "tap into" a pipe halfway along |
| Ratio | One number divided by another, like 1/3 | A recipe that says "one part sugar to two parts flour" |
| Load | Whatever you connect to the output that draws current from it | A device that drinks from the tap |
| Loading | The drop in output voltage when a load is connected | The water pressure falling when someone opens a second faucet |
| Unloaded / open-circuit | Nothing connected to the output, so no current leaves the tap | A faucet with the valve closed |
| Source resistance | How much resistance the divider "seems to have" when seen from its output | How narrow the pipe feeding the faucet is |
| Potentiometer (pot) | A resistor with a sliding contact (the wiper) that makes an adjustable divider | A volume knob |
| Wiper | The sliding contact of a potentiometer | A finger sliding along a ruler |
| E12 series | The standard set of 12 resistor values per decade that shops sell | Shoe sizes: you buy the nearest size, not any number you like |

## Learning Objectives

- Derive the divider formula Vout = Vin x R2 / (R1 + R2) from Kirchhoff's voltage law and Ohm's law, step by step
- Compute the output of any two-resistor divider by hand and check it with the code
- Explain why only the ratio of the resistors sets the voltage, while their size sets the current and the wasted power
- Predict how much the output drops when a load is connected, and choose resistors that keep the drop small
- Use a potentiometer as an adjustable divider and pick standard E12 values for a target voltage

## The Problem

You have a 9 V battery and a small chip that reads voltages, but its input can only take up to 3.3 V. Anything above that might damage it. You don't have a 3.3 V battery. What you want is a way to take a fraction of the 9 V: "give me about a third of this".

Or think of a volume knob on an old radio. Turning it does not change the battery. It picks a fraction of the signal and passes only that fraction on to the speaker amplifier.

Or a light sensor whose resistance changes with brightness. Your microcontroller cannot measure resistance directly; it can only measure voltage. You need a circuit that turns "the resistance changed" into "the voltage changed".

All three are solved by the same tiny circuit, made of just two resistors: the **voltage divider**. It is probably the most common two-part circuit in electronics. You will meet it inside sensors, inside amplifiers (Phase 12 and 13), inside the measuring circuit of every multimeter (Phase 06), and in nearly every schematic you read from now on.

## The Physics

Before the formula, picture what is physically going on.

A battery keeps a fixed voltage between its two terminals: every coulomb of charge that travels from the + terminal, through the outside circuit, back to the - terminal, gives up a fixed amount of energy. For a 9 V battery that is 9 joules per coulomb (Phase 01, lesson 06).

Now put two resistors in a row between the terminals. Charge leaving the + terminal must pass through the first resistor, then through the second, then it is back home. There is no other path. So:

1. **The same current flows through both resistors.** Charge cannot pile up at the middle point (that is Kirchhoff's current law, lesson 02): whatever enters the middle node from the top resistor must leave it through the bottom resistor.
2. **Each resistor takes its share of the energy.** Inside a resistor, the moving electrons bump into the atoms of the material and hand over energy as heat. Pushing a current through a bigger resistance costs more energy per coulomb, so the bigger resistor "uses up" more of the voltage.
3. **The shares add up to the whole.** Every coulomb gives up exactly 9 J in total on its trip around the loop, no more and no less (Kirchhoff's voltage law, lesson 03).

So the middle point sits at some height between 0 V and 9 V, and where exactly it sits depends on how the two resistors split the 9 V. That middle height is our output.

The **staircase picture** helps: the top floor is at 9 V, the ground is at 0 V, and each resistor is a flight of stairs. A long (big) flight takes you down more; a short (small) flight takes you down less. The landing between the two flights is the output. What the picture gets wrong: real stairs don't care how many people walk on them, but a divider's landing *moves* when someone draws current from it. That is the "loading" problem, and it gets its own section below.

## The Concept

### The circuit

```
        Vin (+9 V)
          |
         [R1]   top resistor
          |
          +------- Vout  (the tap, measured from ground)
          |
         [R2]   bottom resistor
          |
        ground (0 V)
```

R1 is the top resistor (between the input and the tap). R2 is the bottom resistor (between the tap and ground). Vout is the voltage at the tap, measured from ground, which is the same as the voltage across R2.

### Step 1: find the current

Nothing is connected to the tap yet, so R1 and R2 are in series (lesson 04). Their total resistance is the sum:

```
R_total = R1 + R2
```

Read aloud: "the total resistance is R1 plus R2". Ohm's law (Phase 03, lesson 03) says current equals voltage divided by resistance, so the current around the loop is

```
I = Vin / (R1 + R2)
```

"The current is the input voltage divided by the sum of the two resistances."

### Step 2: find the voltage across each resistor

Ohm's law again, now for each resistor alone. The voltage across a resistor is the current through it times its resistance:

```
V_R1 = I x R1
V_R2 = I x R2
```

### Step 3: check with KVL

Going around the loop, the battery raises the voltage by Vin and the two resistors drop it by V_R1 and V_R2. KVL says these must balance:

```
Vin = V_R1 + V_R2 = I x R1 + I x R2 = I x (R1 + R2)
```

which is exactly Step 1 rearranged. Good, the pieces agree.

### Step 4: put it together

The output is the voltage across R2. Substitute the current from Step 1:

```
Vout = I x R2 = (Vin / (R1 + R2)) x R2

Vout = Vin x R2 / (R1 + R2)
```

Read aloud: **"the output is the input times the bottom resistor, divided by the sum of both resistors."** This is the voltage divider formula. The fraction R2 / (R1 + R2) is always between 0 and 1, so Vout is always somewhere between 0 and Vin. A divider can only make a voltage smaller, never bigger.

### Worked example 1

Vin = 9 V, R1 = 2 kOhm (2000 Ohm), R2 = 1 kOhm (1000 Ohm).

```
I     = 9 V / (2000 + 1000) Ohm = 9 / 3000 = 0.003 A = 3 mA
V_R1  = 0.003 A x 2000 Ohm = 6 V
V_R2  = 0.003 A x 1000 Ohm = 3 V
check: 6 V + 3 V = 9 V
Vout  = 9 x 1000 / 3000 = 3 V
```

R1 is twice as big as R2, so R1 takes twice as much voltage: 6 V against 3 V. The voltage is shared **in proportion to the resistances**.

### Worked example 2

Vin = 12 V, R1 = 10 kOhm, R2 = 4.7 kOhm.

```
R1 + R2 = 14.7 kOhm
fraction = 4.7 / 14.7 = 0.3197
Vout    = 12 x 0.3197 = 3.84 V
I       = 12 V / 14700 Ohm = 0.816 mA
```

Notice that kOhm cancels in the fraction: you can do divider arithmetic in kOhm without converting to ohms, as long as both resistors use the same unit.

### Only the ratio matters (for the voltage)

Multiply both resistors by the same number and the fraction does not change:

```
R1 = 20 Ohm,   R2 = 10 Ohm    -> fraction 10/30 = 1/3   -> 3 V from 9 V
R1 = 2 kOhm,   R2 = 1 kOhm    -> fraction 1/3           -> 3 V
R1 = 200 kOhm, R2 = 100 kOhm  -> fraction 1/3           -> 3 V
```

The output voltage is identical. What changes is the **current** and so the **power** wasted as heat (Phase 03, lesson 05: P = V x I):

```
20 + 10 Ohm:     I = 300 mA,  P = 9 V x 0.3 A    = 2.7 W   (hot! and a 9 V battery dies in an hour)
2k + 1k:         I = 3 mA,    P = 27 mW
200k + 100k:     I = 0.03 mA, P = 0.27 mW
```

So why not always use huge resistors? Because of loading, which is next.

### Loading: when something drinks from the tap

The formula above assumed nothing is connected to the tap. In real life you connect the output to *something*, and that something draws some current. Model it as a load resistor R_L from the tap to ground:

```
        Vin
         |
        [R1]
         |
         +-------+---- Vout
         |       |
        [R2]   [R_L]   the load
         |       |
        ground  ground
```

Now R2 and R_L are in parallel (both connect the tap to ground). From lesson 04, two resistors in parallel act like one smaller resistor:

```
R2 || R_L = R2 x R_L / (R2 + R_L)
```

("R2 parallel R_L is their product over their sum.") The divider now has R1 on top and this smaller combination on the bottom, so:

```
Vout_loaded = Vin x (R2 || R_L) / (R1 + R2 || R_L)
```

### Worked example 3: watching the output sag

Vin = 9 V, R1 = R2 = 10 kOhm. Unloaded, Vout = 9 x 10/20 = 4.5 V.

Connect a 10 kOhm load:

```
R2 || R_L = 10k x 10k / (10k + 10k) = 5 kOhm
Vout      = 9 x 5 / (10 + 5) = 3 V
```

The output fell from 4.5 V to 3 V, a third lower. The load "stole" part of the bottom resistance.

Here is the whole picture for different loads (the code prints the same table):

```
load       R2 || load     Vout     change
1 MOhm     9.90 kOhm      4.478 V  -0.5 %
100 kOhm   9.09 kOhm      4.286 V  -4.8 %
10 kOhm    5 kOhm         3.000 V  -33 %
1 kOhm     0.909 kOhm     0.750 V  -83 %
100 Ohm    99 Ohm         0.088 V  -98 %
```

**Rule of thumb:** a divider holds its voltage well when the load resistance is at least 10 times (better 100 times) bigger than the divider's resistors. That is why you can't make the divider resistors as big as you like: the bigger they are, the bigger the load must be to leave them undisturbed.

### Seeing the divider as a battery with a resistor

There is a neat shortcut. Seen from the tap, the divider behaves exactly like:

```
     a voltage source of        in series with a
     Vin x R2/(R1+R2)            resistor of R1 || R2
        (the unloaded output)      (both resistors "in parallel")

       +---[ R1||R2 ]----- Vout
       |
     (V_open)
       |
     ground
```

For our 10k/10k divider: V_open = 4.5 V and R1 || R2 = 5 kOhm. With a 10 kOhm load, this simple model gives 4.5 x 10/(5 + 10) = 3 V, exactly what the full calculation gave. The code checks this for several loads. Why R1 || R2? If you "switch off" the battery (replace it by a wire), the tap sees R1 going to ground through the battery wire and R2 going to ground directly: two resistors in parallel. In Phase 05 this idea gets a name (Thevenin's theorem) and a proof. For now, just remember: **a divider is a weak voltage source whose internal resistance is R1 || R2**.

### The potentiometer: a divider you can turn

A potentiometer is one long resistive track (say 10 kOhm end to end) with a sliding contact, the **wiper**, that touches the track somewhere along it.

```
   end A (Vin) ---[ upper part ]--+--[ lower part ]--- end B (ground)
                                  |
                                wiper -> Vout
```

The wiper splits the track into an upper part and a lower part that always add up to the full 10 kOhm. At wiper position x (0 at the ground end, 1 at the top end), the lower part is x x 10 kOhm, and

```
Vout = Vin x lower / total = Vin x x
```

With Vin = 5 V: wiper at 25 % gives 1.25 V, at 50 % gives 2.5 V, at 75 % gives 3.75 V. Volume knobs, joystick axes, the "contrast" trimmer on character displays and the position sensor inside hobby servos are all potentiometers wired as dividers.

### Designing a divider with real resistors

Resistors are sold in standard values, not any number you want. The **E12** series has 12 values per decade: 1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2 (and the same times 10, 100, 1000 ...). Designing a divider has three steps:

1. **Ratio:** from Vout/Vin = R2/(R1 + R2), find the ratio R2/R1 you need. For 9 V to 3.3 V: R2/(R1+R2) = 0.367, so R2/R1 = 0.367/0.633 = 0.58.
2. **Size:** choose the current. Too much wastes power; too little makes the divider sensitive to loading. A few hundred microamps to a few milliamps is typical for a sensor input.
3. **Round to E12** and recompute the real output.

The code tries every pair of E12 values and reports the closest one under a current limit. For 9 V to 3.3 V with at most 5 mA it picks 4.7 kOhm on top and 2.7 kOhm on the bottom: 9 x 2.7/7.4 = 3.284 V, about 0.5 % low, drawing 1.2 mA.

## Build It

The code in `code/main.py` does each step with plain Python. Run it:

```
uv run python phases/04-kirchhoffs-laws/05-the-voltage-divider/code/main.py
```

### Step 1: The divider from KVL and Ohm's law

First compute it "the long way", exactly as derived: current, then each voltage, then check that they add up.

```python
def divider_by_kvl(v_in, r_top, r_bottom):
    current = v_in / (r_top + r_bottom)
    v_top = current * r_top
    v_bottom = current * r_bottom
    return current, v_top, v_bottom
```

For 9 V, 2 kOhm and 1 kOhm it prints a current of 3 mA, 6 V across R1, 3 V across R2, and the KVL check 6 + 3 = 9 V. Then the short formula gives the same 3 V:

```python
def divider_output(v_in, r_top, r_bottom):
    return v_in * r_bottom / (r_top + r_bottom)
```

### Step 2: Only the ratio matters

The script scales both resistors by 0.01, 1 and 100. The output stays at 3.000 V every time, while the current goes from 300 mA down to 0.03 mA and the wasted power from 2.7 W down to 0.27 mW.

### Step 3: Loading

To add a load, combine R2 and the load in parallel and reuse the divider function:

```python
def parallel(r_a, r_b):
    return r_a * r_b / (r_a + r_b)


def loaded_output(v_in, r_top, r_bottom, r_load):
    return divider_output(v_in, r_top, parallel(r_bottom, r_load))
```

The printed table shows the 4.5 V output barely moving with a 1 MOhm load and collapsing to 0.088 V with a 100 Ohm load.

### Step 4: The divider as a source plus a resistor

The script computes the open-circuit voltage and R1 || R2, predicts the loaded output with the simple model `v_open * r_load / (r_source + r_load)`, and prints it next to the full calculation. They match to four decimals for every load.

### Step 5: Potentiometer

A 10 kOhm pot on 5 V, wiper at 0, 25, 50, 75 and 100 %. The upper and lower parts always add to 10 kOhm, and Vout goes from 0 V to 5 V in equal steps.

### Step 6: Picking E12 values

```python
def best_e12_pair(v_in, v_target, max_current):
    best = None
    for r_top in e12_values():
        for r_bottom in e12_values():
            current = v_in / (r_top + r_bottom)
            if current > max_current:
                continue
            error = abs(divider_output(v_in, r_top, r_bottom) - v_target)
            if best is None or error < best[0] - 1e-12:
                best = (error, r_top, r_bottom)
    return best
```

A brute-force search over every pair from 10 Ohm to 1 MOhm (a few thousand pairs, instant on any computer). It skips pairs that would draw too much current, then keeps the pair closest to the target. For 9 V to 5 V under 1 mA it finds 12 kOhm and 15 kOhm, which gives exactly 9 x 15/27 = 5.000 V.

## Use It

- **Reading a sensor:** a light-dependent resistor (LDR) in the bottom position and a fixed 10 kOhm resistor on top. In the dark the LDR is around 1 MOhm, so Vout is near Vin; in bright light it falls to around 1 kOhm and Vout drops near 0.45 V on a 5 V supply. A microcontroller's analog input (Phase 17) reads this voltage. The same trick reads thermistors (NTC 10 kOhm parts are the common choice).
- **Measuring a battery:** to measure a 12 V battery with a microcontroller that accepts up to 3.3 V, designers use something like 100 kOhm on top and 33 kOhm on the bottom (fraction 0.248, so 12 V reads as 2.98 V) and draw only 90 microamps. Big resistors here keep the battery drain tiny; a microcontroller input draws almost no current, so loading is not a problem.
- **Setting a regulator's output:** adjustable regulators like the LM317 (Phase 18) set their output voltage with a two-resistor divider in the feedback path. The datasheet formula for its output is, at heart, the divider formula turned around.
- **Inside amplifiers:** the gain of a non-inverting op-amp amplifier (Phase 13) is set by a divider in its feedback path.
- **Where a divider is the wrong tool:** never use a divider to power something that draws a lot of current or a current that changes (a motor, an LED string, a Wi-Fi module). The output sags with the load, as you saw. For power you need a regulator (Phase 18).

## Try It in the Lab

Open the lab task **"Bring 5 V down to 3.3 V"**. A 5 V source feeds two empty slots in series; the node between them is the output. You have six resistors to choose from. Two conditions must hold at the same time:

- the midpoint voltage must land between 3.2 V and 3.4 V;
- the current through the divider must be between 0.5 mA and 5 mA.

Things to think about before you press RUN: What ratio R2/(R1 + R2) do you need? Which pairs in the parts tray have roughly that ratio? Once you have more than one candidate, what does the current condition rule out, and why would a real designer care about both an upper and a lower limit?

## Common Mistakes

- **Swapping R1 and R2.** The formula uses the *bottom* resistor (the one between the tap and ground) in the numerator. If you use the top one you get Vin minus the answer. Quick sanity check: the tap is closer (in voltage) to whichever end has the *smaller* resistor between it and the tap.
- **Forgetting the load.** The formula Vin x R2/(R1+R2) is only true when nothing draws current from the tap. Connect a load comparable to R2 and the answer can be badly wrong.
- **Powering things from a divider.** A divider is for signals and references, not for supplying current. A 5 V-to-3.3 V divider will not run a 3.3 V chip that draws 50 mA.
- **Mixing units.** 10 kOhm and 4700 Ohm in the same fraction gives nonsense unless you convert one of them. Either use ohms everywhere or kOhm everywhere.
- **Ignoring wasted power.** Small resistors give a stiff output but heat up and drain batteries. 10 Ohm + 10 Ohm across 9 V dissipates 4 W, far beyond a normal 1/4 W resistor (Phase 03, lesson 05).
- **Thinking a divider can step voltage up.** The fraction is always below 1. To get a higher voltage you need a boost converter (Phase 18).

## Exercises

1. Vin = 5 V, R1 = 3.3 kOhm, R2 = 6.8 kOhm. Compute the current, the voltage across each resistor, and Vout. Check that the two voltages add to 5 V.
2. A divider has R1 = 4.7 kOhm and R2 = 4.7 kOhm on a 12 V supply. What is Vout? Now a load of 47 kOhm is connected to the output. What is the new Vout, and by what percentage did it drop?
3. You need 2.5 V from a 9 V battery and the divider must draw less than 0.2 mA. Find the ratio, choose the total resistance, and pick E12 values. What output do you actually get?
4. For exercise 2, compute the divider's open-circuit voltage and its equivalent resistance R1 || R2. Use the "source plus resistor" model to predict the output with a 4.7 kOhm load, then check it with the full parallel calculation.
5. (Harder) An NTC thermistor reads 10 kOhm at 25 C and 3.6 kOhm at 50 C. It sits in the bottom position with a fixed 10 kOhm on top, on a 3.3 V supply. Compute Vout at both temperatures. Then swap the thermistor to the top position. Which arrangement gives a voltage that rises with temperature?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Voltage divider | "It cuts the voltage" | Two series resistors that share the input voltage in proportion to their resistances; the tap gives Vin x R2/(R1+R2) when unloaded |
| Divider ratio | "Two to one" | The fraction R2/(R1+R2) that multiplies the input; set only by the ratio of the resistors, not their size |
| Loading | "The voltage dropped when I plugged it in" | A load in parallel with R2 lowers the effective bottom resistance, so the tap voltage falls |
| Source resistance of a divider | "How stiff it is" | R1 parallel R2: the resistance the load sees looking back into the tap |
| Potentiometer | "A knob" | A resistive track with a sliding wiper; wired end-to-end across a voltage, the wiper is an adjustable divider tap |
| E12 values | "Standard resistors" | The 12 preferred values per decade that manufacturers stock; designs are rounded to them and then rechecked |

## Further Reading

- *Practical Electronics for Inventors* (Scherz & Monk), chapter 2 on resistors and voltage dividers, with many practical circuits.
- *The Art of Electronics* (Horowitz & Hill), chapter 1, sections on voltage dividers and "Thevenin equivalent circuits": the classic treatment of why a divider is a source with an internal resistance.
- All About Circuits, *Lessons in Electric Circuits*, Volume I (DC), chapter "Divider Circuits and Kirchhoff's Laws".
- Texas Instruments LM317 datasheet, the "adjustable output voltage" section, to see a divider setting a regulator's output.
