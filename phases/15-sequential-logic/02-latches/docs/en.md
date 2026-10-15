# Latches

> A latch is a bit of memory with a door: while the door is open the bit follows its input, when it closes the bit stays.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lessons 03-04 (Boolean Algebra, Logic Gates), Phase 15 (Sequential Logic), Lesson 01 (Memory from Feedback)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Latch | A feedback circuit that stores one bit and has inputs to change it | A light switch with separate on and off buttons |
| SR latch | A latch with a Set input and a Reset input | "On" and "off" buttons |
| Active-low | An input that does its job when it is 0, not 1 (often written with a bar or a trailing `'` or `n`) | A dead-man's handle: the action happens when you let go |
| Forbidden state | An input combination that breaks the latch's promises | Pressing "on" and "off" at the same time |
| Race | Two signals changing at once, where the result depends on which one wins | Two people reaching for the last biscuit |
| Gated latch | A latch with an enable that decides when the other inputs are listened to | A door that only accepts letters while the letterbox flap is open |
| Enable (en) | The input that opens the door | Holding the letterbox flap open |
| D latch | A gated latch with a single data input D | A notepad where you can only write while the cover is open |
| Transparent | The output follows the input immediately | A window: you see whatever is outside right now |
| Opaque (hold) | The output ignores the input and keeps its value | A photograph: it shows what was there when the shutter closed |
| Next state (Q+) | The value the stored bit will have after the inputs act | Tomorrow's balance in your bank account |

## Learning Objectives

- Build and operate an SR latch from NOR gates and an S'R' latch from NAND gates.
- Explain why the input S = R = 1 (or S' = R' = 0) is forbidden and show the race it causes.
- Add an enable to make a gated SR latch, then a gated D latch with no forbidden input.
- Write the next-state equation of a D latch, `Q+ = EN·D + EN'·Q`, and recognise it as a multiplexer.
- Explain transparency and why it is a problem when latches feed each other.

## The Problem

Lesson 01 found the basic memory element: two inverters in a loop, or two cross-coupled NOR gates. The NOR version could be set and reset. But a computer register needs something more convenient: "here is a data bit; store it now". It should not need two separate set and reset wires that you must never press together, and it should store the data only at the moment you say so, ignoring the data wire the rest of the time.

The **latch** family fixes these problems one at a time: first the SR latch, then a gate that decides when to listen, and finally the D latch, which takes a single data bit and an enable. The D latch is the building block of the flip-flop (Lesson 03), the register (Lesson 04) and every state machine in this phase.

## The Physics

A latch is the bistable loop of Lesson 01 with extra transistors that can overpower it. Writing a latch is a tug-of-war: the input stage must pull a node hard enough to cross the switching point of the loop's inverter; once it does, positive feedback takes over and finishes the job, snapping both nodes to their rails. If the push is too weak or too short, the loop drifts back to its old state, or worse, hovers near the middle for a while before deciding (metastability, Lesson 07). So a latch has timing requirements: the input must be held long enough for the loop to complete the change. On a datasheet this appears as a minimum pulse width and, for gated latches, setup and hold times around the closing of the enable.

## The Concept

### The NOR SR latch, again

Lesson 01 built it as two equations:

```
q  = NOR(r, qb)
qb = NOR(s, q)
```

Its behaviour, summarised as a **characteristic table** (what happens to `q`):

```
 s r | q next      action
 0 0 | q (keep)    hold
 0 1 | 0           reset
 1 0 | 1           set
 1 1 | 0, qb = 0   forbidden
```

The first three rows are what we want. The last row needs explaining.

### Why s = r = 1 is forbidden

With both inputs at 1, both NOR gates have a 1 on an input, so both output 0: `q = 0` and `qb = 0`. The latch's promise that `qb` is the opposite of `q` is broken. That alone is a reason to avoid it, but the real trouble comes next.

Suppose both inputs return to 0 **at the same instant**. Now each NOR sees 0 on its outside input and 0 from the other gate, so each wants to output 1. If the gates are perfectly identical, both outputs rise together. Now each sees a 1 from the other and wants to output 0. Both fall together. And so on:

```
t = 0: q = 0, qb = 0
t = 1: q = 1, qb = 1
t = 2: q = 0, qb = 0
t = 3: q = 1, qb = 1
...
```

That is what our simulator prints with equal one-unit delays for both gates. In a real circuit the two gates are never perfectly equal: one is a few picoseconds faster, its output wins, and the latch falls into one of its two states, but **which** one depends on tiny manufacturing differences and noise. This is a **race**, and its result is unpredictable. A memory that you cannot predict is useless, so the rule is simply: never let s and r be 1 together.

### The NAND S'R' latch: active-low inputs

Two NAND gates make the mirror-image latch:

```
q  = NAND(sn, qb)
qb = NAND(rn, q)
```

A NAND with one input at 1 is an inverter of its other input, so with `sn = rn = 1` the two gates form the bistable loop and hold. Pulling `sn` to 0 forces `q = 1` (a NAND with any 0 input outputs 1): that sets the latch. Pulling `rn` to 0 resets it. The inputs work when they are **0**, so they are called **active-low** and named with a bar, a `'`, or an `n`: S', R', `sn`, `rn`.

```
 sn rn | q next     action
  1  1 | q (keep)   hold
  1  0 | 0          reset
  0  1 | 1          set
  0  0 | q = qb = 1 forbidden
```

Active-low signals are very common in real chips (`RESET'`, `CS'` for chip select, `OE'` for output enable) because in older logic families pulling a line low was stronger and faster than pulling it high, and because a disconnected input with a pull-up resistor sits safely at "inactive".

### Adding a door: the gated SR latch

We want the latch to listen only when we allow it. Put two NAND gates in front of the NAND latch, each combining one input with an enable `en`:

```
sn = NAND(s, en)
rn = NAND(r, en)
```

- **en = 0:** both NANDs output 1 whatever `s` and `r` are. The latch sees `sn = rn = 1` and holds. The door is closed.
- **en = 1:** each front NAND is an inverter, so `sn = s'` and `rn = r'`. The latch is set by `s = 1` and reset by `r = 1`. The door is open.

The forbidden input still exists (`s = r = 1` while `en = 1`), so we take one more step.

### The gated D latch

Most of the time we do not want separate set and reset at all. We want: "store this data bit `d`". So generate `s` and `r` from one bit: `s = d` and `r = d'`. They are always opposites, so the forbidden combination can never occur.

```
          steering gates                 NAND S'R' latch
        +-------------+               +--------------------+
 d -----| NAND(d, en) |---- sn ------>|                    |
   |    +-------------+               | q  = NAND(sn, qb)  |---- q
   |                                  |                    |
 [NOT]  +-------------+               | qb = NAND(rn, q)   |---- qb
   |    | NAND(nd,en) |---- rn ------>|                    |
   nd --|             |               +--------------------+
        +-------------+
 en ------ goes to both steering gates
```

As equations, the five gates are:

```
nd = NOT d
sn = NAND(d, en)
rn = NAND(nd, en)
q  = NAND(sn, qb)
qb = NAND(rn, q)
```

Check the four cases by hand:

```
 en d | sn rn | effect on the NAND latch | q
  0 0 |  1  1 | hold                      | old q
  0 1 |  1  1 | hold                      | old q
  1 0 |  1  0 | reset                     | 0
  1 1 |  0  1 | set                       | 1
```

When `en = 1`, `q` equals `d`: the latch is **transparent**, like a window. When `en = 0`, `q` keeps whatever `d` was at the moment `en` fell: the latch is **opaque**, like a photograph taken when the shutter closed.

Our simulator runs this sequence:

```
 en d | q
  1 1 | 1     transparent: q follows d
  1 0 | 0
  1 1 | 1
  0 1 | 1     en falls with d = 1: stores 1
  0 0 | 1     d changes, q does not
  0 1 | 1
  0 0 | 1
  1 0 | 0     transparent again
  0 1 | 0     stores 0, ignores d = 1
```

### The next-state equation

A compact way to describe any memory element is its **next-state equation**: the stored value after the inputs act, `Q+`, written as a function of the inputs and the current value `Q`. For the D latch, say it in words: "if the enable is on, the next value is d; otherwise it is the current value". In Boolean algebra:

```
Q+ = en·d + en'·Q
```

Look closely: that is exactly a **2-to-1 multiplexer** (Phase 14, Lesson 08) with select `en`, choosing between the old value `Q` and the new data `d`. A D latch is "a mux whose output is fed back into one of its own inputs". Many chip libraries build latches exactly that way, with a transmission-gate mux and two inverters.

For the SR latch, the next-state equation is `Q+ = s + r'·Q`, valid when `s·r = 0`. Check: `s = 1` gives 1 (set); `r = 1, s = 0` gives `0 + 0 = 0` (reset); `s = r = 0` gives `Q` (hold).

### The trouble with transparency

Transparency is a feature when you want to see the input right away. It is a problem when the output of a latch feeds, through some logic, back into the input of the same or another latch with the same enable. While `en = 1` the signal runs straight through all the transparent latches and around the loop, possibly many times, and what gets stored when `en` falls depends on exact gate delays.

Example: a 1-bit "toggle" made of a D latch whose `d` is `NOT q`. While `en = 1`, `q` follows `d = q'`, so it flips, then flips again, and again: a ring oscillator (Lesson 01) for as long as `en` is high. When `en` falls, the stored value is whatever the oscillation happened to be at that instant.

The cure, in Lesson 03, is to make sure the door is never open on both sides at once: two latches in series with opposite enables. That is the edge-triggered flip-flop.

## Build It

The script `code/main.py` builds every latch of this lesson in `sim.logic` and drives it with input sequences.

### Step 1: The two SR latches

```python
def nor_sr_latch():
    lc = LogicCircuit("NOR SR latch")
    lc.inputs("s", "r")
    lc.nor("q", "r", "qb")
    lc.nor("qb", "s", "q")
    lc.outputs("q", "qb")
    return lc


def nand_sr_latch():
    lc = LogicCircuit("NAND S'R' latch")
    lc.inputs("sn", "rn")
    lc.nand("q", "sn", "qb")
    lc.nand("qb", "rn", "q")
    lc.outputs("q", "qb")
    return lc
```

### Step 2: Drive a sequence

A latch must be driven step by step, because the same circuit object keeps its stored values between calls. `run` applies each input dictionary in turn and records the outputs.

```python
def run(lc, sequence, names):
    rows = []
    for inputs in sequence:
        out = lc.evaluate(inputs)
        rows.append({**inputs, **{n: out[n] for n in names}})
    return rows
```

### Step 3: The forbidden input

With `s = r = 1` the script prints `q = 0, qb = 0`. Then it releases both inputs at once and steps every gate with one unit of delay, using the same `unit_delay_run` as Lesson 01:

```python
history = unit_delay_run(nor, {"s": 0, "r": 0, "q": 0, "qb": 0}, 6)
```

```
    t = 0: q = 0, qb = 0
    t = 1: q = 1, qb = 1
    t = 2: q = 0, qb = 0
    ...
```

### Step 4: The gated D latch

```python
def d_latch():
    lc = LogicCircuit("gated D latch")
    lc.inputs("en", "d")
    lc.not_("nd", "d")
    lc.nand("sn", "d", "en")
    lc.nand("rn", "nd", "en")
    lc.nand("q", "sn", "qb")
    lc.nand("qb", "rn", "q")
    lc.outputs("q", "qb")
    return lc
```

The script drives the nine-step sequence shown above and checks the two promises automatically:

```
  q == d whenever en = 1: True; q unchanged whenever en = 0: True
  gates: 5 (4 NAND + 1 NOT); no forbidden input is possible
```

Run it:

```bash
uv run python phases/15-sequential-logic/02-latches/code/main.py
```

## Use It

- **74HC75** contains four transparent D latches (pairs share an enable); **74HC373** has eight, with tri-state outputs, and was the classic way to hold an address on a microprocessor bus.
- **74HC279** contains four S'R' latches, used for switch debouncing.
- **Address latches.** Older microprocessors such as the Intel 8085 and 8088 sent the low address bits and the data on the same pins, one after the other. An external '373 latch grabbed the address while the ALE ("address latch enable") pulse was high, then held it while the pins carried data.
- **Latch-based design.** Some high-performance processors use pairs of latches on opposite clock phases instead of flip-flops, because it lets logic "borrow time" across the boundary. It is harder to design and verify.
- **Synthesis warnings.** In hardware description languages, forgetting to assign an output in every branch of an `if` makes the tool infer a latch by accident. Chip designers treat "latch inferred" warnings as bugs.

## Try It in the Lab

The lab task "Build a gated D latch from NAND gates" has the inverter for `d` and the two cross-coupled NAND gates already wired. Fill the two steering slots: one combines `d` with `en` into `sn`, the other combines `nd` with `en` into `rn`. Parts: NAND, AND, NOR and OR. The checker drives eight steps (`en` and `d` changing) and compares `q` after each step.

Think about: when must `sn` be 0? When must both `sn` and `rn` be 1? Which gate gives 0 only when all its inputs are 1?

## Common Mistakes

- **Using s = r = 1.** It makes `q` and `qb` equal and leads to an unpredictable race when released. A D latch avoids it by construction.
- **Mixing up active-low inputs.** On a NAND latch the inputs act when they are 0. Driving `sn` to 1 to "set" does nothing.
- **Treating a latch as edge-triggered.** A latch is level-sensitive: it follows its input for the whole time `en` is 1, not just at the moment `en` rises. Glitches on `d` while `en = 1` go straight to `q`.
- **Changing d just as en falls.** The latch needs `d` stable for a short time before and after the closing edge (setup and hold, Lesson 07), or it may store either value or go metastable.
- **Building loops through transparent latches.** A path from a latch's output back to its own input, while it is transparent, oscillates or races. Use flip-flops (Lesson 03) for loops.

## Exercises

1. Trace the NAND S'R' latch for (sn, rn) = (1, 0), (1, 1), (0, 1), (1, 1), (0, 0), (1, 1). Write q and qb after each step. Which step is forbidden, and what is q after it?
2. Derive the next-state equation `Q+ = s + r'·Q` from the SR latch's characteristic table (treat the forbidden row as a don't-care) using a Karnaugh map with variables s, r, Q.
3. Draw a D latch built from a 2-to-1 multiplexer whose output is fed back to one of its inputs. Which input of the mux gets `d`, which gets `q`, and what drives the select?
4. A D latch has `en = 1` for 20 ns. During that time `d` glitches from 1 to 0 and back for 3 ns. What does `q` do? Would it matter if the glitch happened while `en = 0`?
5. Two D latches are connected in a loop through an inverter (latch A's `q` goes through a NOT into latch B's `d`, and B's `q` goes into A's `d`). Both share the same enable. What happens while the enable is 1? Now give B the inverted enable. What happens on each change of the enable? (This is the idea of Lesson 03.)

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| SR latch | "Set-reset latch" | Cross-coupled NORs (or NANDs with active-low inputs) that set, reset or hold one bit |
| Forbidden state | "Don't press both" | s = r = 1 (or sn = rn = 0): outputs stop being complements and release causes a race |
| Active-low | "Bar", "n" | A signal that is asserted when it is 0 |
| Gated latch | "Latch with enable" | A latch whose inputs only act while `en` = 1 |
| D latch | "Transparent latch" | A gated latch storing a single data bit: `Q+ = en·d + en'·Q` |
| Transparent | "Follows the input" | While enabled, the output equals the input after a gate delay |
| Level-sensitive | "Not edge-triggered" | Responds during the whole time the enable is active, not at an instant |
| Next-state equation | "Q plus" | The stored value after the inputs act, as a function of inputs and current state |

## Further Reading

- David Harris and Sarah Harris, *Digital Design and Computer Architecture*, Chapter 3, sections on SR latches and D latches.
- M. Morris Mano and Michael D. Ciletti, *Digital Design*, Chapter 5 (Synchronous Sequential Logic), sections on latches and characteristic equations.
- Texas Instruments datasheets *SN74HC75* (4-bit bistable latches) and *SN74HC373* (octal transparent D-type latches).
- Ben Eater, "SR latch" and "D latch" videos (YouTube), for these circuits built on a breadboard.
