# Phase 14: Digital Logic

> Two voltage levels, three Boolean operations and a handful of gates: enough to build anything that computes.

Until now every voltage in the course could take any value. This phase makes a deliberate choice: a wire may only mean 0 or 1. You will see why that choice beats noise (each gate regenerates a clean level instead of passing errors along), how numbers become rows of bits (binary, hexadecimal, two's complement), and how Boolean algebra describes and simplifies every decision a circuit can make. Then you open the gates themselves: NAND, NOR, XOR and friends, and the CMOS transistor pairs inside them that draw almost no power when idle, simulated with the MOSFET models from Phase 12. With those parts you design real combinational circuits step by step (comparators, a display decoder, adders that add and subtract, multiplexers and decoders) and check every one against ordinary arithmetic with our logic simulator, `sim.logic`. It comes here because transistors (Phase 12) and comparators (Phase 13) are exactly what a gate is made of, and because Phases 15 and 16 need these blocks to add memory and then build a whole computer.

**Prerequisites:** Phase 02 (Your First Circuits), Phase 12 (Transistors), Phase 13 (Operational Amplifiers), Lesson 02 (The Comparator)

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [Analog vs Digital](01-analog-vs-digital/) | Why two levels beat noise, regeneration, logic levels VOH/VOL/VIH/VIL, noise margins, and an analog chain against a digital chain |
| 02 | [Binary Numbers](02-binary-numbers/) | Place value in base 2, conversions to decimal and hex, unsigned ranges, two's complement, carry and overflow |
| 03 | [Boolean Algebra](03-boolean-algebra/) | AND, OR, NOT, truth tables, the laws, De Morgan, sum of products and Karnaugh maps |
| 04 | [Logic Gates](04-logic-gates/) | The seven gates and their symbols, NAND and NOR universality, XOR from four NANDs, delay, depth and real 74HC chips |
| 05 | [CMOS Gates from Transistors](05-cmos-gates-from-transistors/) | The CMOS inverter and its transfer curve, NAND and NOR from four MOSFETs, near-zero static power and `α C V^2 f` |
| 06 | [Combinational Circuits](06-combinational-circuits/) | The design flow from spec to verified gates, a 2-bit comparator, a 7-segment segment with don't-cares, critical paths and glitches |
| 07 | [Adders](07-adders/) | Half and full adders, ripple-carry adders, subtraction with two's complement, carry and overflow flags, carry-lookahead |
| 08 | [Multiplexers and Decoders](08-multiplexers-and-decoders/) | 2-to-1 and 4-to-1 muxes, decoders with enable, demuxes, and the mux as a lookup table (the heart of an FPGA) |

**Labs in this phase:**

- 03 Greenhouse fan from NAND gates (logic)
- 04 Build XOR from four NAND gates (logic)
- 05 Pick the pull-up of a CMOS inverter (dc)
- 06 Are two 2-bit numbers equal? (logic)
- 07 Finish the full adder (logic)
- 08 Build a 2-to-1 multiplexer (logic)

Run the first lesson:

```
uv run python phases/14-digital-logic/01-analog-vs-digital/code/main.py
```
