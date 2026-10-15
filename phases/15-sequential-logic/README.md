# Phase 15: Sequential Logic

> Feed a gate's output back to its input and it starts to remember; add a clock and millions of those memories move in step.

Phase 14's circuits forget everything the moment their inputs change. This phase gives them memory. You start with the physics of feedback: two inverters in a loop hold a bit, three of them oscillate, and the CMOS ring oscillator in our circuit simulator shows the gate delay that sets the rhythm. From there you build latches (set, reset and the forbidden input), then the master-slave flip-flop, which samples its input at one instant per clock tick and makes large systems predictable. Rows of flip-flops become registers with load enables and shift registers, registers that add one become counters, and counters generalise to finite state machines designed from circles and arrows. The phase ends with the numbers that limit every real chip: setup and hold times, critical paths, clock skew and metastability, measured in the analog simulator and turned into a mean time between failures. It comes after Phase 14 because every memory element here is built from its gates, and before Phase 16 because a computer is exactly registers, counters and a state machine wrapped around an adder.

**Prerequisites:** Phase 07 (Capacitors), Phase 12 (Transistors), Phase 14 (Digital Logic)

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [Memory from Feedback](01-memory-from-feedback/) | Bistable loops, ring oscillators (`f = 1 / 2 N tpd`) in gates and in real transistors, and the cross-coupled NOR latch |
| 02 | [Latches](02-latches/) | NOR and NAND SR latches, the forbidden input and its race, gated latches and the transparent D latch `Q+ = en·d + en'·Q` |
| 03 | [Flip-Flops and the Clock](03-flip-flops-and-the-clock/) | Clock period and frequency, the master-slave D flip-flop from two latches, timing diagrams, toggling and synchronous design |
| 04 | [Registers](04-registers/) | n-bit registers, the load-enable multiplexer, shift registers for serial-parallel conversion, register files |
| 05 | [Counters](05-counters/) | Synchronous counter logic (bit i toggles when all lower bits are 1), frequency division, decade counters, ripple counters and their glitches |
| 06 | [Finite State Machines](06-finite-state-machines/) | State diagrams and tables, Moore and Mealy machines, encodings, and a 101 sequence detector checked against a string search |
| 07 | [Timing and Metastability](07-timing-and-metastability/) | Setup and hold constraints, fmax, clock skew, metastability measured in a CMOS latch, MTBF and the two-flip-flop synchronizer |

**Labs in this phase:**

- 02 Build a gated D latch from NAND gates (logic, sequence)
- 04 Give a register bit a load enable (logic, sequence)
- 05 Next-state logic of a 2-bit counter (logic, sequence)
- 06 Next-state logic of a 101 detector (logic, sequence)

Run the first lesson:

```
uv run python phases/15-sequential-logic/01-memory-from-feedback/code/main.py
```
