# Phase 16: A Computer from Gates

> A computer is an adder, a few registers, a memory and a small state machine, arranged so that numbers in memory decide what the machine does next.

This phase builds a complete computer, the **T8**, from the gates and flip-flops of Phases 14 and 15. It has 8-bit data, 256 bytes of memory shared by program and data, an accumulator, a program counter, two flags and 21 instructions with an encoding of our own. You start with what makes a machine a stored-program computer and write a reference model of the T8 in Python, the specification everything else is checked against. Then, one part per lesson: a 122-gate ALU that adds, subtracts and does logic with zero and carry flags; a RAM made of registers, a decoder and multiplexers (and why real memories use SRAM, DRAM and flash cells instead); a datapath where every register talks over one shared bus; a microcoded control unit whose step counter and table produce every control signal; and a two-pass assembler with labels. In the last lesson all of it runs together: multiplication, a countdown and the Fibonacci sequence execute on the gate-level ALU and step counter, checked against the reference model after every single instruction, and the clock speed follows from the critical path. It comes here because it uses everything from the two previous phases, and because Phase 17's microcontrollers are exactly this kind of machine on one chip.

**Prerequisites:** Phase 14 (Digital Logic), Phase 15 (Sequential Logic)

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [What a Computer Is](01-what-a-computer-is/) | Stored programs, fetch-decode-execute, the T8 specification and instruction set, and a reference model in Python |
| 02 | [The ALU](02-the-alu/) | An 8-bit ALU (ADD, SUB, AND, OR, XOR) with Z, C and N flags, built gate by gate and verified against the reference |
| 03 | [Memory](03-memory/) | A 16-byte RAM from 128 flip-flops, a decoder and read multiplexers; SRAM, DRAM, ROM and flash; the T8's memory model |
| 04 | [The Datapath](04-the-datapath/) | Registers on a shared bus, control signals, register transfers, and LDA/ADD/OUT run by hand cycle by cycle |
| 05 | [The Control Unit](05-the-control-unit/) | The step counter, the T8's microcode as a ROM, and hardwired control equations checked against the table |
| 06 | [Instructions and Assembly](06-instructions-and-assembly/) | The ISA and its bit fields, addressing modes, a two-pass assembler with labels, a disassembler, and two real programs |
| 07 | [Running a Program](07-running-a-program/) | The integrated T8 running programs in lockstep with the reference model, traces, CPI and execution time |

**Labs in this phase:**

- 02 One bit of an ALU (logic)
- 03 Address decoder for a 4-byte memory (logic)
- 05 Decode the MAR_IN control signal (logic)

Run the first lesson:

```
uv run python phases/16-a-computer-from-gates/01-what-a-computer-is/code/main.py
```
