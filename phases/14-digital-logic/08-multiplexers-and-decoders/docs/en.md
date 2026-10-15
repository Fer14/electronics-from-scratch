# Multiplexers and Decoders

> A multiplexer chooses one of many inputs; a decoder chooses one of many outputs. Together they route every bit inside a computer.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lesson 03 (Boolean Algebra), Lesson 04 (Logic Gates) and Lesson 06 (Combinational Circuits)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Multiplexer (mux) | A circuit that copies one of several data inputs to its single output, chosen by select bits | A TV remote choosing which channel reaches the screen |
| Select input | The bits that choose which input (or output) is used | The channel number you type |
| Data input | An input whose value is passed through, not interpreted | The programmes on each channel |
| Decoder | A circuit with n input bits and 2^n outputs, exactly one of which is 1 | A hotel switchboard ringing exactly one room for a room number |
| One-hot | A group of wires where exactly one is 1 | A row of lift buttons where only your floor is lit |
| Enable | An input that switches a whole block on or off | The master switch of a power strip |
| Demultiplexer (demux) | The opposite of a mux: one data input sent to one of several outputs | A railway switch sending a train down one of several tracks |
| Encoder | The opposite of a decoder: a one-hot input turned into its binary number | Reading which lift button is lit and saying the floor number |
| Lookup table (LUT) | A small memory whose stored bits are a truth table, read by a mux | A times-table chart: look up the row and read the answer |
| FPGA | A chip made of thousands of programmable LUTs and wires | A box of Lego that rebuilds itself into any circuit you describe |
| Bus | A group of wires that carries a multi-bit value | A multi-lane road carrying one convoy |

## Learning Objectives

- Build a 2-to-1 multiplexer from gates and explain it as "AND to gate, OR to combine".
- Build a 4-to-1 multiplexer as a tree of 2-to-1 muxes and verify it on all 64 input combinations.
- Build a 2-to-4 decoder with enable and a 1-to-4 demultiplexer, and explain why decoders select memory locations.
- Use a multiplexer as a lookup table that implements any function of its select inputs.
- Count the gates and logic depth of mux and decoder designs.

## The Problem

Inside a computer, data has to go to the right place. The adder needs its second number from one of several registers. The result has to go back into exactly one of them. When the processor reads memory, address 1000 must activate memory cell 1000 and no other. All of this is routing: picking which wire talks to which.

You could imagine a mechanical rotary switch for each choice, but a processor makes billions of such choices per second, so the switches must be gates. Two small circuits do almost all of this work. The multiplexer selects **from** many sources. The decoder selects **one of many** destinations. In Phase 16 the whole datapath of our computer is held together by them, and FPGAs, chips that can become any circuit, are built mostly from multiplexers.

## The Physics

A multiplexer is just a combinational circuit of AND and OR gates (or their CMOS NAND forms), so the physics is that of Lessons 04-06: each gate adds a few nanoseconds of delay, and wide muxes have more levels. On chips, muxes are also built from **transmission gates**: an NMOS and a PMOS in parallel acting as a bidirectional switch. When its control is on, it connects two wires with a few hundred ohms; when off, it disconnects them. A 2-to-1 mux is then two such switches and one inverter, only 6 transistors. Their limitation is that they do not regenerate the signal (they are switches, not gates), so long chains of them need buffers.

Older board-level designs also used **tri-state** outputs: an output that can be 0, 1 or disconnected ("high impedance"). Many chips can share one bus wire if exactly one of them drives it at a time, chosen by a decoder. That is a multiplexer spread across several chips. Inside modern chips, ordinary gate multiplexers are preferred because a mistake with tri-state outputs can short a 1 driver against a 0 driver.

## The Concept

### The 2-to-1 multiplexer

**Spec.** Inputs `a`, `b` and a select `s`. Output `y = a` when `s = 0`, `y = b` when `s = 1`.

The idea in two steps:

1. **Gate.** An AND gate with one input held at 1 copies its other input; with one input at 0 it outputs 0. So `a·s'` is "a, but only while s is 0", and `b·s` is "b, but only while s is 1".
2. **Combine.** At any moment at most one of those two terms can be non-zero, so an OR simply passes whichever one is open.

```
y = s'·a + s·b
```

```
           +--------+
  a -------|  AND   |---- p --+
     +-----|        |         |
     |     +--------+         +---[ OR ]---- y
  s -+-[NOT]                  |
     |                        |
     |     +--------+         |
  b -|-----|  AND   |---- q --+
     +-----|        |
           +--------+
```

(The NOT output feeds the top AND; `s` itself feeds the bottom AND.)

Truth table, 8 rows (inputs s, a, b):

```
 s a b | y
 0 0 0 | 0     s = 0: y copies a
 0 0 1 | 0
 0 1 0 | 1
 0 1 1 | 1
 1 0 0 | 0     s = 1: y copies b
 1 0 1 | 1
 1 1 0 | 0
 1 1 1 | 1
```

Four gates, depth 3. (You met this exact function in Lesson 06 as the example with a glitch. In a clocked design that glitch is harmless; when it matters, the consensus term `a·b` removes it.)

A schematic usually draws a mux as a trapezoid, wide on the input side:

```
         +\
  a --0--| \
         |  |---- y
  b --1--| /
         +/
          |
          s
```

### Wider data: one mux per bit

To choose between two 8-bit numbers `A` and `B`, use eight 2-to-1 muxes side by side, all with the same select wire. Engineers draw it as one mux with a slash and "8" on the wires. This is how the input of the adder in Phase 16 picks "register B" or "a number from memory".

### More inputs: the 4-to-1 multiplexer

With 4 data inputs `d0..d3` we need 2 select bits `s1 s0`: the binary number `s1 s0` names the input to pass. Two ways to build it:

**As a sum of products.** One AND per input, each enabled by its own select pattern (a minterm of the select bits, Lesson 03), then one 4-input OR:

```
y = s1'·s0'·d0 + s1'·s0·d1 + s1·s0'·d2 + s1·s0·d3
```

**As a tree of 2-to-1 muxes.** First let `s0` choose between `d0`/`d1` and between `d2`/`d3`; then let `s1` choose between the two winners.

```
 d0 --0\
        |-- low --0\
 d1 --1/            |
        s0          |-- y
 d2 --0\            |
        |-- high -1/
 d3 --1/            s1
        s0
```

Check select `10` (s1 = 1, s0 = 0): the first level gives `low = d0`, `high = d2`; the second level with `s1 = 1` passes `high`, so `y = d2`. Correct: binary 10 is 2.

In general, a `2^k`-to-1 mux needs `k` select bits. The tree has `2^k - 1` small muxes in `k` levels, so its depth grows with `k`, the logarithm of the number of inputs. Our simulator's 4-to-1 tree has 12 gates and depth 5; the verification over all `2^6 = 64` input combinations finds 0 wrong rows.

### The decoder

**Spec.** A 2-to-4 decoder has 2 address inputs `a1 a0` and 4 outputs `y0..y3`. Exactly the output whose number equals the address is 1; the others are 0. The outputs are **one-hot**.

Each output is the minterm of its own address:

```
y0 = a1'·a0'      y1 = a1'·a0      y2 = a1·a0'      y3 = a1·a0
```

An **enable** input `en` ANDed into every output turns the whole decoder off: with `en = 0` all outputs are 0.

```
 en a1 a0 | y0 y1 y2 y3
  0  x  x |  0  0  0  0
  1  0  0 |  1  0  0  0
  1  0  1 |  0  1  0  0
  1  1  0 |  0  0  1  0
  1  1  1 |  0  0  0  1
```

An n-to-2^n decoder needs `2^n` AND gates of `n` inputs each (plus `n` inverters). A 3-to-8 decoder has 8 outputs; a 10-to-1024 decoder would select one of 1024 memory rows. That is the job of the **row decoder** in every memory chip (Phase 16, Lesson 03): the address bits arrive, and exactly one row of memory cells is switched on. Large decoders are built in stages (pre-decoding pairs of bits, then combining), for the same speed reasons as wide adders.

Decoders with enables also chain: to make a 3-to-8 decoder from two 2-to-4 decoders, send the top address bit to the enables: `en_low = a2'` and `en_high = a2`.

### The demultiplexer

A demux sends one data bit to one of several outputs. Look at the decoder with enable again: if you put the **data** on the enable input, the addressed output equals the data and all others are 0. So **a decoder with enable is a demultiplexer**: no new circuit is needed.

```
 data = 1, address 10 -> o0 o1 o2 o3 = 0 0 1 0
 data = 0, address 10 -> o0 o1 o2 o3 = 0 0 0 0
```

### The encoder

The reverse of a decoder takes a one-hot input and outputs its number. For 4 inputs `i0..i3`, the 2-bit output is `b1 = i2 + i3` and `b0 = i1 + i3`. If more than one input can be 1 (several keys pressed), a **priority encoder** outputs the number of the highest one: keyboards and interrupt controllers (Phase 17) use them.

### A multiplexer can compute anything

Here is a surprising and important fact. Take a 4-to-1 mux, connect your two variables `a` and `b` to its **select** inputs, and connect the four **data** inputs to fixed 0s and 1s. The mux output for `a b` is whichever constant sits at input number `ab`. So the four constants are, in order, the **truth table** of the function.

```
 stored bits (d0 d1 d2 d3)     function of a, b
       0  0  0  1              AND
       0  1  1  0              XOR
       1  1  1  0              NAND
       1  1  0  1              a' + b   ("a implies b")
```

The simulator builds exactly this and prints each truth table, which matches the stored bits. With 4 stored bits there are `2^4 = 16` possible functions of 2 inputs, and the mux can be any of them, just by changing the stored bits. This structure is a **lookup table** (LUT). In general, a `2^k`-to-1 mux with stored bits is a LUT of k inputs, able to compute any of the `2^(2^k)` functions of k variables.

That is how an **FPGA** (field-programmable gate array) works. It contains tens of thousands to millions of small LUTs (commonly 4 or 6 inputs) whose stored bits are loaded from a configuration file at power-up, plus programmable wiring between them (also made of multiplexers). Change the file and the same chip becomes a different circuit. Phase 20, Lesson 09 compares FPGAs with custom chips.

### Muxes versus decoders

```
               multiplexer                     decoder / demux
inputs         many data + k select bits       k address bits (+ data/enable)
outputs        one                             2^k, one-hot
answers        "which source do I listen to?"  "which destination do I talk to?"
used for       choosing operands, LUTs         selecting memory rows, chip selects, writing registers
```

## Build It

The script `code/main.py` builds each block in `sim.logic`, reusing small builder functions the way a hardware designer reuses modules.

### Step 1: A reusable 2-to-1 mux

```python
def add_mux2(lc, s, a, b, y, tag):
    lc.not_(f"{tag}.ns", s)
    lc.and_(f"{tag}.p", a, f"{tag}.ns")
    lc.and_(f"{tag}.q", b, s)
    lc.or_(y, f"{tag}.p", f"{tag}.q")
```

This adds four gates to any circuit `lc`. The `tag` prefix keeps inner wire names unique when we place several muxes.

### Step 2: A 4-to-1 mux as a tree

```python
def add_mux4(lc, s1, s0, d, y, tag):
    add_mux2(lc, s0, d[0], d[1], f"{tag}.low", f"{tag}.m0")
    add_mux2(lc, s0, d[2], d[3], f"{tag}.high", f"{tag}.m1")
    add_mux2(lc, s1, f"{tag}.low", f"{tag}.high", y, f"{tag}.m2")
```

The script checks it on all 64 combinations of `s1, s0, d0..d3` against the rule "y equals input number `2·s1 + s0`":

```
  checked all 64 input combinations: 0 wrong; gates 12, depth 5
```

### Step 3: Decoder and demux

```python
def add_decoder2(lc, a1, a0, en, outs):
    lc.not_("na1", a1)
    lc.not_("na0", a0)
    lc.and_(outs[0], en, "na1", "na0")
    lc.and_(outs[1], en, "na1", a0)
    lc.and_(outs[2], en, a1, "na0")
    lc.and_(outs[3], en, a1, a0)
```

The decoder passes `en` as its enable; the demux passes its data bit in the same place. The script prints the decoder's truth table (one-hot outputs when `en = 1`, all zeros when `en = 0`) and the demux routing the data bit to the addressed output.

### Step 4: The lookup table

`lc.constant(name, value)` creates a wire permanently at 0 or 1. We store four constants and feed them to the 4-to-1 mux, with the function's inputs `a` and `b` on the select lines:

```python
def lut2(table):
    lc = LogicCircuit("2-input lookup table")
    lc.inputs("a", "b")
    stored = [lc.constant(f"k{i}", bit) for i, bit in enumerate(table)]
    add_mux4(lc, "a", "b", stored, "y", "lut")
    lc.outputs("y")
    return lc
```

```
  stored bits [0, 1, 1, 0] -> truth table [0, 1, 1, 0]  = XOR
  stored bits [1, 1, 0, 1] -> truth table [1, 1, 0, 1]  = a' + b (a implies b)
```

Run it:

```bash
uv run python phases/14-digital-logic/08-multiplexers-and-decoders/code/main.py
```

## Use It

- **74HC157** (four 2-to-1 muxes with a shared select), **74HC153** (two 4-to-1 muxes) and **74HC151** (one 8-to-1 mux) are the classic mux chips.
- **74HC138** is a 3-to-8 decoder with three enable inputs and active-low outputs. In 1980s computers it chose which chip (ROM, RAM, I/O) answered each address range. **74HC139** has two 2-to-4 decoders.
- **Analog multiplexers** such as the CD4051 pass analog voltages using transmission gates; microcontrollers use the same idea to share one ADC among many pins (Phase 17, Lesson 04).
- **FPGAs** from AMD (Xilinx), Intel (Altera) and Lattice are built from 4- or 6-input LUTs. A 6-input LUT is a 64-to-1 mux with 64 stored bits.
- **Memory chips** contain row decoders (one word line on) and column multiplexers (pick the bits of the addressed word), which is exactly a decoder plus a mux around an array of cells.

## Try It in the Lab

The lab task "Build a 2-to-1 multiplexer" has the inverter `ns = s'` already placed. Slot S1 receives `a` and `ns`, slot S2 receives `b` and `s`, and slot S3 combines their outputs into `y`. The parts are AND, OR and NOR. The output must copy `a` when `s = 0` and `b` when `s = 1`, in all 8 rows.

Think about: which gate can act as a "door" that lets a signal through only when a control input is 1? Once at most one of the two doors is open, which gate passes whichever one is open?

## Common Mistakes

- **Swapping the select polarity.** Make sure `s = 0` really selects input 0. A mux with `s'` and `s` exchanged works perfectly but selects the wrong input, a bug that passes casual testing when both inputs happen to be equal.
- **Wrong select bit order.** In a 4-to-1 mux, `s1` is the high bit. Wiring `s0` to the last level instead of the first still gives a valid mux, but input numbering is permuted.
- **Forgetting the enable.** A decoder without enable always drives one output. When chaining decoders or using one as a demux, the enable is essential.
- **Two drivers on one wire.** Connecting two gate outputs together to "combine" them is not an OR: if one drives 1 and the other 0, they fight and current flows. Use a gate (or a mux) to combine signals.
- **Confusing mux and demux.** A mux has many inputs and one output; a demux has one input and many outputs.

## Exercises

1. How many select bits does a 32-to-1 multiplexer need? How many 2-to-1 muxes in a tree, and how many levels?
2. Write the sum-of-products expression for an 8-to-1 multiplexer with select bits `s2 s1 s0`. How many AND gates, and how many inputs does each have?
3. Show how to build a 3-to-8 decoder from two 2-to-4 decoders with enable. What goes to each enable?
4. What stored bits turn a 4-to-1 mux LUT (select `a b`) into NOR? Into "output = b" (ignoring a)?
5. Build a full adder's sum and carry from two 8-to-1 muxes used as 3-input LUTs (select bits `a b cin`). List the 8 stored bits for each. How does that compare in gate count with the 5-gate full adder of Lesson 07, and why do FPGAs still win for flexibility?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Multiplexer | "Mux", "selector" | Copies the data input numbered by the select bits to the output: `y = s'·a + s·b` for 2 inputs |
| Decoder | "Address decoder" | n inputs, 2^n one-hot outputs, each output a minterm of the inputs |
| Demultiplexer | "Demux" | A decoder with the data on its enable: routes one bit to one of many outputs |
| Encoder | "Priority encoder" | Turns a one-hot (or highest set) input into its binary number |
| Enable | "EN", "chip select" | An input that turns all outputs of a block off when inactive |
| Lookup table | "LUT" | A mux whose data inputs are stored constants, so it computes any function of its select bits |
| FPGA | "Programmable logic" | A chip of many LUTs and programmable routing, configured by a bitstream |
| One-hot | "Only one wire high" | A code where exactly one of n wires is 1 |

## Further Reading

- M. Morris Mano and Michael D. Ciletti, *Digital Design*, Chapter 4 sections on decoders, encoders and multiplexers.
- Texas Instruments datasheets *SN74HC138* (3-to-8 decoder/demultiplexer) and *SN74HC157* (quad 2-to-1 data selector/multiplexer).
- AMD (Xilinx), *7 Series FPGAs Configurable Logic Block User Guide* (UG474), for how 6-input LUTs and multiplexers form an FPGA's logic.
- Ben Eater, videos on building RAM and the bus of an 8-bit breadboard computer (YouTube), for decoders and tri-state buses in real chips.
