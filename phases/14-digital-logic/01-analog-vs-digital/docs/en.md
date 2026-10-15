# Analog vs Digital

> A digital signal is an analog voltage that has agreed to mean only two things, so that noise has nothing left to change.

**Type:** Learn
**Prerequisites:** Phase 03 (Resistance and Ohm's Law), Phase 12 (Transistors), Lesson 05 (The MOSFET as a Switch), Phase 13 (Operational Amplifiers), Lesson 02 (The Comparator)
**Time:** ~60 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Signal | A voltage (or current) that changes over time to carry information | The needle of a fuel gauge moving as the tank empties |
| Analog | A signal where every value in a range means something different | A dimmer knob: every position is a slightly different brightness |
| Digital | A signal where only a few bands of values are allowed, each with a fixed meaning | A light switch: on or off, nothing in between counts |
| Noise | Small unwanted random changes added to a signal | Static hiss on a radio |
| Bit | One digital value that can only be 0 or 1 | One coin lying heads or tails |
| Logic level | The voltage range that counts as 0 or as 1 | "Below the knee" and "above the shoulder" on a height chart |
| Threshold | The dividing voltage a receiver uses to decide 0 or 1 | The line in a high-jump: over it or not |
| Noise margin | How much noise a 0 or a 1 can take before it is misread | The gap between the edge of a road and the ditch |
| Regeneration | Rebuilding a clean 0 or 1 from a slightly dirty one | A photocopy made from the original, not from a copy of a copy |
| Driver / receiver | The chip that sends a signal / the chip that reads it | The speaker and the listener in a conversation |
| Forbidden zone | The voltage band between "surely 0" and "surely 1" where the meaning is undefined | The no-man's-land between two trenches |

## Learning Objectives

- Explain the difference between an analog and a digital signal with an example of each.
- Explain why noise piles up in a chain of analog stages but not in a chain of digital stages.
- Read the four logic-level numbers on a datasheet (VOH, VOL, VIH, VIL) and compute the two noise margins.
- Decide from a voltage whether a receiver sees a 0, a 1, or "undefined".
- Simulate a 10-stage analog chain and a 10-stage digital chain and compare their errors.

## The Problem

Imagine a microphone in a recording studio. It turns air pressure into a voltage that wiggles up and down a few thousandths of a volt. That wiggle has to travel through a cable to a mixing desk, through an amplifier, through a second cable, onto a tape machine, back off the tape, through another amplifier, and so on. Every one of those steps adds a tiny bit of hiss. After ten copies of a cassette tape, the music is still there but buried in noise. Nothing in the chain knows what the "true" voltage was, so nothing can remove the hiss once it is added.

Now think of a phone call today. Your voice is turned into a stream of numbers, each number into a stream of 0s and 1s, and those 0s and 1s cross dozens of chips, cables, radio links and data centres. Yet the voice at the other end has no added hiss from all those hops. Copy a music file a thousand times and the thousandth copy is identical to the first, bit for bit.

The difference is not magic. Both systems move voltages through wires. The difference is in what the voltage is allowed to mean. This lesson explains that choice. It is the reason almost every chip you will meet from here on is a digital chip, and it is the starting point of the next three phases, which take us from two voltage levels all the way to a working computer.

## The Physics

### Every wire is analog

Physically, there is no such thing as a "digital wire". A wire on a chip or a board has a voltage on it, and that voltage is a real number: 0.03 V, 2.71 V, 4.96 V. Electrons do not know about 0 and 1. What is digital is the agreement between the chip that drives the wire and the chip that reads it.

### Where noise comes from

Noise is any small voltage that sneaks onto a signal without being invited. A few sources you have already met:

- **Thermal noise.** The free electrons in a resistor jiggle because of heat (Phase 01, Lesson 05). Their random motion makes a tiny random voltage across every resistor. It grows with temperature and with resistance.
- **Coupling.** Two wires next to each other form a small capacitor (Phase 07). When one wire jumps from 0 V to 5 V, a little of that jump leaks onto its neighbour. Engineers call this crosstalk.
- **Ground bounce.** Many outputs switching at once pull a big current through the thin ground wire of a chip. That current times the wire's resistance and inductance (Phase 08) makes the chip's "0 V" rise briefly by a few hundred millivolts.
- **Interference.** Motors, radios and power lines create changing fields that induce voltages in any loop of wire (Phase 08, Lesson 03 on Faraday's law).

You cannot remove all of it. You can only make the signal not care.

### Why two levels survive noise

A transistor used as a switch (Phase 12, Lesson 05) has a useful property: its output is either pulled firmly up to the supply or pulled firmly down to ground, almost no matter what the exact input voltage is, as long as the input is clearly on one side of its switching point. If the input is 4.6 V instead of 5.0 V, the output is still pulled all the way down. The small error at the input does not appear at the output. It is erased.

That is the physical heart of digital electronics: a stage with very high gain around its switching point and hard limits (the supply rails) on both sides. You met the same idea in the comparator (Phase 13, Lesson 02): tiny input differences become full-swing outputs. A digital gate is a comparator that is cheap enough to build billions of times on one chip.

## The Concept

### Analog: every value matters

In an analog system, the voltage is a direct copy of the quantity it represents. A temperature sensor may output 10 mV per degree Celsius, so 0.250 V means 25.0 °C and 0.251 V means 25.1 °C. If noise adds 1 mV, the reading becomes wrong by 0.1 °C, and no later stage can tell.

Read this as a sentence first: "the measured value equals the true value plus the noise". In symbols:

```
v_received = v_sent + v_noise
```

Here `v` stands for a voltage in volts (V). After `N` stages, each adding its own noise, the errors add up:

```
v_after_N = v_sent + noise_1 + noise_2 + ... + noise_N
```

Random noise partly cancels itself (sometimes positive, sometimes negative), so the typical total does not grow like `N` but like the square root of `N`. If each stage adds noise with a typical size of 20 mV, then after 10 stages the typical error is about

```
20 mV x sqrt(10) = 20 mV x 3.16 = 63 mV
```

and after 100 stages about `20 mV x 10 = 200 mV`. It never shrinks.

### Digital: only two answers allowed

In a digital system we decide in advance that the wire carries only one of two values. We call them **0** and **1**, or **LOW** and **HIGH**. A single such value is called a **bit** (short for "binary digit"). With a 5 V supply, the simplest agreement is:

```
 5.0 V  +-----------------+
        |                 |
        |    means 1      |
        |                 |
 2.5 V  +---- threshold --+
        |                 |
        |    means 0      |
        |                 |
 0.0 V  +-----------------+
```

The receiver compares the wire against the threshold and decides. Then it does something an analog stage cannot do: it **outputs a brand-new, clean voltage**, 0 V or 5 V, whatever slightly wrong voltage it received. That is **regeneration**.

Worked example. A driver sends 5.0 V (a 1). Noise adds -0.7 V, so the receiver sees 4.3 V. Is 4.3 V above 2.5 V? Yes, so the receiver decides "1" and outputs a fresh 5.0 V to the next stage. The 0.7 V of noise is gone. The next stage sees 5.0 V plus its own new noise, not 5.0 V minus 0.7 V plus new noise.

The noise only wins if a single hop adds more than 2.5 V. That is very unlikely, and when it does happen the result is a wrong bit, which later lessons (and the whole field of error-correcting codes) can detect and fix.

### What the analogy of a light switch gets wrong

We said a digital signal is like a light switch. The picture is good for the meaning (on or off) but wrong in two ways:

1. A real digital wire spends a short time in between while it moves from 0 to 1. That is the **transition**, and it takes nanoseconds, not zero time. During that time the voltage passes through every value in between.
2. The receiver does not have one perfect threshold. Every real chip switches at a slightly different voltage, which changes with temperature and supply. So we cannot use a single line. We need a band.

### Logic levels: four numbers on every datasheet

Because real chips vary, the agreement is written as four guaranteed numbers. A datasheet promises them over the full temperature and supply range.

| Symbol | Read it as | Meaning |
|---|---|---|
| VOH | "V output high" | The driver guarantees a 1 is at least this high |
| VOL | "V output low" | The driver guarantees a 0 is at most this low |
| VIH | "V input high" | The receiver guarantees anything at or above this reads as 1 |
| VIL | "V input low" | The receiver guarantees anything at or below this reads as 0 |

Between VIL and VIH lies the **forbidden zone**: the receiver might read 0, might read 1, might even oscillate. A properly working circuit never parks a wire there; it only passes through quickly during transitions.

```
 driver output                       receiver input
 guarantees                          accepts

 VCC  ---------                      ---------  VCC
      |       |                      |       |
      | "1"   |                      | "1"   |
 VOH  ---------  \                   |       |
                  \  high noise      |       |
                   \ margin NMH      |       |
                    -------------->  ---------  VIH
                                     |forbid-|
                                     |  den  |
                    -------------->  ---------  VIL
                   / low noise       |       |
                  /  margin NML      | "0"   |
 VOL  ---------  /                   |       |
      | "0"   |                      |       |
 GND  ---------                      ---------  GND
```

### Noise margins

The **noise margin** is how much noise a bit can survive. Say it as a sentence: "the high noise margin is how far the worst-case 1 from the driver sits above the lowest voltage the receiver still accepts as 1".

```
NMH = VOH - VIH
NML = VIL - VOL
```

Worked example with a 74HC family chip running at 5 V (the "HC" stands for high-speed CMOS; we meet CMOS in Lesson 05). Typical guaranteed values, rounded, at small output current:

```
VOH = 4.4 V     VOL = 0.1 V      (at 4 mA load it is about 3.98 V and 0.26 V)
VIH = 3.5 V     VIL = 1.5 V
```

Then

```
NMH = 4.4 V - 3.5 V = 0.9 V
NML = 1.5 V - 0.1 V = 1.4 V
```

So a 1 can lose up to 0.9 V and a 0 can gain up to 1.4 V of noise and still be read correctly. The smaller of the two, 0.9 V, is the one that matters: the chain is only as strong as its weakest margin.

Second example, a modern 3.3 V logic standard often called LVCMOS or LVTTL:

```
VOH = 2.4 V     VOL = 0.4 V
VIH = 2.0 V     VIL = 0.8 V
NMH = 2.4 - 2.0 = 0.4 V
NML = 0.8 - 0.4 = 0.4 V
```

Lower supply voltage means smaller margins. Chips still go lower (1.8 V, 1.2 V, under 1 V inside processors) because lower voltage saves a lot of power, as Lesson 05 shows. The price is that board designers must keep noise smaller.

### Deciding what a receiver sees

Given VIL and VIH, any input voltage falls into one of three regions:

```
v <= VIL          -> 0
VIL < v < VIH     -> undefined (forbidden zone)
v >= VIH          -> 1
```

For 74HC at 5 V: 0.8 V reads 0, 4.0 V reads 1, 2.5 V is undefined. Exactly 1.5 V is still guaranteed 0. 3.49 V is undefined; 3.5 V is a guaranteed 1.

### Mixing families: the classic trap

The driver's VOH must be above the receiver's VIH, or a 1 might not be seen. A 3.3 V chip driving a 5 V 74HC input gives at best 3.3 V, often 2.4 V worst case. The 74HC input wants at least 3.5 V for a guaranteed 1. NMH = 2.4 - 3.5 = -1.1 V, a negative margin: the connection is not guaranteed to work at all, even with no noise. This is why "level shifter" chips exist, and why the 74HCT family was made with TTL-style inputs (VIH = 2.0 V) that a 3.3 V output can drive.

### How many levels? Why not ten?

If two levels resist noise, why not use ten levels and store a whole decimal digit on one wire? Because the gap between neighbouring levels shrinks. With 5 V split into 10 bands, each band is 0.5 V wide, so the margin is at most about 0.25 V. With 2 bands, the margin can approach 2.5 V. Two levels also make the circuit simplest: a transistor that is fully on or fully off. Some systems do use more levels where wires are precious: flash memory cells store 3 or 4 bits as 8 or 16 charge levels, and fast network links use 4-level signalling (PAM4). They pay for it with error-correcting codes.

### Sampling: from analog to digital and back

Real-world quantities (sound, temperature, light) are analog. To use digital processing we measure them at regular instants and turn each measurement into a number made of bits. That is the job of an analog-to-digital converter (Phase 17, Lesson 04 and Phase 19, Lessons 04-05). Going back, a digital-to-analog converter makes a voltage again. Between those two converters, all the work happens with bits, and bits can be copied, stored and computed on without degradation.

## Build It

The script `code/main.py` compares an analog chain with a digital chain, then computes noise margins for two logic families and classifies a few voltages.

### Step 1: An analog chain

Each analog stage passes its input to its output and adds random noise. We use a fixed random seed so the result is the same every run.

```python
def run_chains(stages, noise_rms, seed=14):
    rng = np.random.default_rng(seed)
    message = np.array([0, 1, 1, 0, 1, 0, 0, 1] * 25)
    sent = message * 5.0
    analog = sent.copy()
    for _ in range(stages):
        analog = analog + rng.normal(0.0, noise_rms, analog.size)
```

`noise_rms` is the typical size of the noise each stage adds, in volts. The message is 200 bits long, and we send 1 as 5 V and 0 as 0 V.

### Step 2: A digital chain

A digital stage first adds the same kind of noise, then regenerates: it compares with the 2.5 V threshold and outputs a clean 0 V or 5 V.

```python
def regenerate(v, threshold=2.5, vdd=5.0):
    return np.where(v > threshold, vdd, 0.0)

    digital = sent.copy()
    for _ in range(stages):
        digital = regenerate(digital + rng.normal(0.0, noise_rms, digital.size))
```

### Step 3: Compare the errors

The typical error is the root-mean-square difference from what was sent, and a bit is read wrong if it lands on the wrong side of 2.5 V at the end of the chain:

```python
    analog_error = np.sqrt(np.mean((analog - sent) ** 2))
    digital_error = np.sqrt(np.mean((digital - sent) ** 2))
    wrong_analog = int(np.sum((analog > 2.5).astype(int) != message))
    wrong_digital = int(np.sum((digital > 2.5).astype(int) != message))
```

The script runs this for three noise sizes. The output looks like this (numbers come from the fixed seed):

```
After 10 stages with 0.20 V of noise per stage
  analog  chain: typical error 0.59 V  (theory 0.20 x sqrt(10) = 0.63 V), wrong bits 0/200
  digital chain: typical error 0.00 V, wrong bits 0/200
After 10 stages with 0.50 V of noise per stage
  analog  chain: typical error 1.48 V  (theory 0.50 x sqrt(10) = 1.58 V), wrong bits 10/200
  digital chain: typical error 0.00 V, wrong bits 0/200
After 10 stages with 1.00 V of noise per stage
  analog  chain: typical error 2.95 V  (theory 1.00 x sqrt(10) = 3.16 V), wrong bits 35/200
  digital chain: typical error 1.00 V, wrong bits 8/200
```

Read the first block: the analog error (0.59 V) is close to the square-root rule (0.63 V; random numbers never match theory exactly), while the digital error is exactly zero, because each stage throws away the noise before it can accumulate. In the second block the analog chain has drifted so far that 10 of the 200 bits would now be read wrong at the end, while the digital chain is still perfect: a single hop would need noise bigger than 2.5 V, five times its typical size, which practically never happens. Only in the third block, where one hop's noise is already 1 V, does the digital chain start making mistakes (8 of 200), and even then far fewer than the analog chain (35 of 200). Note that "typical error 1.00 V" for the digital chain does not mean every bit is off by 1 V: most bits are perfect and a few are off by the full 5 V.

### Step 4: Noise margins from datasheet numbers

```python
families = {
    "74HC at 5 V": {"VOH": 4.4, "VOL": 0.1, "VIH": 3.5, "VIL": 1.5},
    "LVCMOS 3.3 V": {"VOH": 2.4, "VOL": 0.4, "VIH": 2.0, "VIL": 0.8},
}
for name, lv in families.items():
    nmh = lv["VOH"] - lv["VIH"]
    nml = lv["VIL"] - lv["VOL"]
```

### Step 5: Read a voltage like a receiver

```python
def read_input(v, vil, vih):
    if v <= vil:
        return "0"
    if v >= vih:
        return "1"
    return "undefined"
```

### Step 6: Regeneration with our logic simulator

Our simulator has a digital part, `sim.logic`, that works directly with 0s and 1s instead of voltages: every wire holds a bit, and every gate is assumed to regenerate perfectly. A **buffer** is the simplest gate: its output equals its input. In voltage terms it is two inverting transistor stages (Lesson 05) that restore a clean level. Chaining 10 buffers shows the digital promise in its purest form.

```python
def buffer_chain(stages):
    lc = LogicCircuit("buffer chain")
    lc.inputs("in")
    previous = "in"
    for k in range(1, stages + 1):
        lc.gate("buf", [previous], f"s{k}")
        previous = f"s{k}"
    lc.outputs(previous)
    return lc

chain = buffer_chain(10)
for bit in (0, 1):
    print(chain.evaluate({"in": bit})["s10"])
```

`lc.inputs` names the wires we drive from outside, `lc.gate("buf", [input], output)` adds one gate, and `lc.evaluate({...})` sets the inputs and returns the outputs once every gate has settled. The bit at the end is exactly the bit at the start. From the next lessons on, all gate-level work runs on `sim.logic`.

Run it:

```bash
uv run python phases/14-digital-logic/01-analog-vs-digital/code/main.py
```

## Use It

- **Music and video.** CDs (1982) store sound as 16-bit numbers, 44,100 of them per second per channel. Copying a CD or a file gives an exact copy, which was impossible with tape.
- **Every logic chip datasheet** has a table titled "Recommended operating conditions" with VIH and VIL, and "Electrical characteristics" with VOH and VOL at a stated output current. Look at the datasheet of a 74HC00 (four NAND gates, we will use it in Lesson 04): at VCC = 4.5 V it lists VIH = 3.15 V and VIL = 1.35 V, and the numbers scale with VCC. The 5 V values used above (3.5 V and 1.5 V) are the same 70 % and 30 % of the supply.
- **Microcontrollers** (Phase 17) list the same four numbers for their pins, often as fractions of the supply, like "VIH = 0.7 x VDD".
- **USB, Ethernet, HDMI** carry bits over long cables. They use differential signalling: two wires carry opposite voltages and the receiver looks only at the difference, so noise that hits both wires equally cancels (this is the difference amplifier of Phase 13, Lesson 04, put to work).
- **Level shifters** such as the 74LVC245 or the TXS0108E exist to connect 3.3 V chips to 5 V chips safely.

## Try It in the Lab

This lesson has no lab task. The labs of this phase start in Lesson 03, where you build logic functions out of gates.

## Common Mistakes

- **Thinking digital wires are physically different.** They are ordinary wires carrying ordinary voltages. Digital is an agreement about meaning, plus circuits that enforce it.
- **Using one threshold.** "Anything above 2.5 V is a 1" is a teaching simplification. Real designs must use VIH and VIL and stay out of the forbidden zone.
- **Comparing VOH with VOL, or VIH with VIL, to get a margin.** Margins always compare a driver number with a receiver number: VOH with VIH, VIL with VOL.
- **Forgetting the output current.** VOH and VOL get worse when the output supplies more current, because the output transistor has resistance. A datasheet gives VOH at a stated current; if you draw more, the margin shrinks.
- **Assuming digital means error-free.** Digital means noise does not accumulate. A single big noise spike can still flip a bit. That is why memories, disks and radio links add error-detecting and error-correcting codes.
- **Leaving an input floating.** An unconnected CMOS input sits at an unknown voltage, often inside the forbidden zone. The gate may switch randomly and draw extra current. Every unused input must be tied to a 0 or a 1.

## Exercises

1. A sensor outputs 10 mV per °C. Noise adds 3 mV. What temperature error is that? Would that error grow or shrink after two more analog amplifier stages that each add their own 3 mV of random noise? Estimate the typical total.
2. A logic family has VOH = 4.7 V, VOL = 0.2 V, VIH = 3.3 V, VIL = 1.2 V. Compute NMH and NML. Which one limits the design?
3. A 3.3 V microcontroller with VOH = 2.9 V (at the current you need) drives a 74HCT input with VIH = 2.0 V. What is NMH? Now it drives a 74HC input with VIH = 3.5 V at 5 V. What is NMH, and what does the sign tell you?
4. For 74HC at 5 V, classify 0.4 V, 1.6 V, 3.5 V and 4.9 V as 0, 1 or undefined.
5. In the script, add the case `(50, 1.2)` (50 stages, 1.2 V of noise per stage) to the list. Run it and count how many bits the digital chain gets wrong. Explain why the count is no longer zero, and estimate the probability that one hop flips a bit (hint: the noise has to exceed 2.5 V, about 2.1 times its typical size; a normal distribution exceeds 2.1 times its rms size in one direction about 1.8 % of the time). Why does the count end up close to half of the bits once many flips have happened?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Analog | "Smooth, continuous" | A signal where every value in a range carries a different meaning, so any noise becomes error |
| Digital | "Ones and zeros" | Ordinary voltages agreed to mean only two values, plus circuits that restore them at every stage |
| Bit | "A one or a zero" | The smallest unit of information: one choice between two possibilities |
| Noise margin | "How much noise it can take" | VOH - VIH for a 1 and VIL - VOL for a 0, computed from guaranteed datasheet numbers |
| Regeneration | "It cleans up the signal" | Each stage decides 0 or 1 and outputs a fresh full-swing voltage, discarding the incoming noise |
| Forbidden zone | "The grey area" | Input voltages between VIL and VIH where the receiver's decision is not guaranteed |
| Logic family | "HC, LVC, TTL..." | A set of chips sharing supply voltage and logic levels so they can be wired together safely |

## Further Reading

- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Chapter 10 (Digital Logic), especially the sections on logic levels and noise immunity.
- Texas Instruments, *SN74HC00 Quadruple 2-Input Positive-NAND Gates* datasheet (VIH, VIL, VOH, VOL tables).
- Texas Instruments, *Logic Guide* (SDYU001), for comparing families (TTL, HC, HCT, LVC) and their voltage levels.
- All About Circuits, *Digital* textbook (Vol. IV), chapter "Logic Gates", section "Logic Signal Voltage Levels".
