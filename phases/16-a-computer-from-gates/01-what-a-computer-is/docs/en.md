# What a Computer Is

> A computer is a machine that reads its own instructions from memory, one after another, and the instructions are just numbers like any other data.

**Type:** Learn
**Prerequisites:** Phase 14 (Digital Logic), all lessons, Phase 15 (Sequential Logic), Lessons 03-06 (Flip-Flops and the Clock, Registers, Counters, Finite State Machines)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Computer | A machine that follows a list of instructions stored in its own memory | A cook following a recipe written in a notebook the cook can also write in |
| Program | The list of instructions | The recipe |
| Instruction | One small step the machine knows how to do (add, load, jump...) | "Add two eggs" |
| Stored-program computer | A computer whose program sits in the same memory as its data | A notebook holding both the recipe and the shopping list |
| Memory | A numbered array of storage cells, each holding one byte | A street of numbered mailboxes |
| Address | The number of a memory cell | A house number |
| Register | A small, fast storage place inside the processor (Phase 15, Lesson 04) | The cook's hands, holding what is being worked on right now |
| Accumulator (A) | The main register where results are collected | A mixing bowl |
| Program counter (PC) | The register holding the address of the next instruction | A bookmark in the recipe |
| ALU | Arithmetic logic unit: the circuit that adds, subtracts and does logic | The cook's knife and whisk |
| Fetch-decode-execute | The cycle every processor repeats: get an instruction, work out what it means, do it | Read the next line, understand it, do it |
| Opcode | The number that says which instruction it is | The verb of a recipe line ("add", "stir") |
| Operand | The extra number an instruction works on (a value or an address) | "two eggs", "the large bowl" |
| Jump | An instruction that changes the program counter, so the next instruction comes from elsewhere | "Go back to step 3" |
| Flag | A one-bit register remembering something about the last result, like "it was zero" | A note on the fridge saying "the bowl is empty" |

## Learning Objectives

- Explain what makes a machine a stored-program computer.
- Name the parts of a simple processor (ALU, registers, program counter, memory, control unit, bus) and say what each does.
- Describe the fetch-decode-execute cycle and step through it by hand for a three-instruction program.
- Read the instruction set of the T8, the 8-bit computer we build in this phase.
- Explain why a program is just data, and use a reference model in Python to run programs on the T8.

## The Problem

Everything in Phases 14 and 15 was a machine built for one job: an adder adds, a counter counts, a detector detects 101. To make it do something else, you rebuild it. Early electronic machines were like that too: ENIAC (1945) was "programmed" by plugging cables and setting switches, and changing the program took days.

The idea that changed everything is simple to say. Put the instructions in memory, as numbers, next to the data. Build one fixed machine that reads an instruction, does it, and moves on to the next. Then to change what the machine does, you just change some numbers in memory: no wiring at all. That machine is a **computer**. Every phone, laptop, washing machine controller and car engine unit works this way.

This phase builds one, from the gates of Phase 14 and the registers and state machines of Phase 15, in seven steps. This first lesson shows what we are going to build and gives us a **reference model**: a short Python program that behaves exactly like the finished machine, so that every hardware piece we build later can be checked against it.

## The Physics

A computer adds no new physics. It is a large synchronous circuit (Phase 15, Lesson 03): registers made of flip-flops, combinational logic between them, one clock. What is new is **organisation**. A handful of registers, one adder-based ALU, a memory and a small state machine are arranged so that the state machine reads numbers from memory and uses them to decide which registers load what on each clock edge. The same hardware then performs any computation you can describe as a list of small steps. The physical limits are the ones you already know: the critical path through the ALU sets the clock speed (Phase 15, Lesson 07), and every switching node costs `C V^2` of energy (Phase 14, Lesson 05).

## The Concept

### A short history

- **1830s:** Charles Babbage designs the Analytical Engine, a mechanical computer with a "mill" (ALU) and a "store" (memory), programmed with punched cards. Ada Lovelace writes the first published program for it. It was never completed.
- **1936:** Alan Turing describes a theoretical machine that reads and writes symbols on a tape following a table of rules, and shows that one universal machine can imitate any other. This is the mathematical idea of a general-purpose computer.
- **1945:** John von Neumann's *First Draft of a Report on the EDVAC* describes a stored-program computer: one memory holding both instructions and data, a processing unit, a control unit and input/output. This organisation is still called the **von Neumann architecture**.
- **1948:** The Manchester "Baby" runs the first stored program on 21 June 1948: 32 words of memory, 7 instructions.
- **1971:** The Intel 4004 puts a whole 4-bit processor on one chip (about 2,300 transistors).

### The parts of a processor

```
                 +-------------------------------------------+
                 |               control unit                |
                 |  (a state machine reading the opcode)     |
                 +--+--------+--------+--------+--------+----+
                    | control signals: "load A", "PC out", ...
     +--------------v--------v--------v--------v--------v-----------+
     |                          bus (8 wires)                        |
     +---+--------+--------+--------+--------+--------+--------+----+
         |        |        |        |        |        |        |
       [ PC ]  [ MAR ]  [ memory ] [ IR ]  [ A ]    [ B ]   [ OUT ]
                           256 B             |        |
                                           [   ALU   ]
                                              flags
```

- **Memory** holds the program and the data, 256 cells of 8 bits each in our machine.
- The **program counter (PC)** holds the address of the next byte of the program to read. It is a counter with a load input (Phase 15, Lesson 05): it counts up through the program and can be loaded with a new address for a jump.
- The **memory address register (MAR)** holds the address memory is currently looking at.
- The **instruction register (IR)** holds the opcode of the instruction being executed.
- The **accumulator (A)** holds the working value; **B** holds the second operand for the ALU.
- The **ALU** computes A + B, A - B, A AND B, and so on (Lesson 02), and sets **flags**: Z (the result was zero) and C (there was a carry out).
- The **output register (OUT)** holds a number for the outside world, like a display.
- The **bus** is a set of 8 shared wires that moves one byte at a time between these parts (Lesson 04).
- The **control unit** is a finite state machine (Phase 15, Lesson 06) that, on each clock cycle, decides which part puts its value on the bus and which part loads it (Lesson 05).

### Fetch, decode, execute

The control unit repeats the same cycle forever:

1. **Fetch.** Send the PC to memory, read the byte at that address into the IR, and add 1 to the PC.
2. **Decode.** Look at the opcode in the IR and work out which steps the instruction needs.
3. **Execute.** Do those steps: maybe read an operand byte, maybe use the ALU, maybe store a result, maybe change the PC.

Then fetch again, from wherever the PC now points. Because the PC normally just counts up, instructions are executed in order. A **jump** instruction loads a new value into the PC, so the next fetch comes from somewhere else. A **conditional jump** loads the PC only if a flag is set: that one feature is what lets a computer make decisions and repeat loops.

### The T8: our machine

We call the machine we build the **T8** (for "tiny, 8-bit"). Its specification:

```
data width        8 bits (values 0-255, or -128..127 in two's complement)
memory            256 bytes, addresses 0x00-0xFF, program and data together
registers         A (accumulator), B (ALU operand), PC, MAR, IR, OUT
flags             Z (last ALU result was zero), C (last ALU operation carried out)
instruction size  1 byte (opcode only) or 2 bytes (opcode + operand)
start             PC = 0, A = 0, flags = 0
```

Its instruction set (the full list of what it can do):

| Opcode | Mnemonic | Bytes | What it does |
|---|---|---|---|
| `00` | `NOP` | 1 | nothing |
| `01` | `OUT` | 1 | OUT = A (show A on the output) |
| `0F` | `HLT` | 1 | stop the clock |
| `10` | `LDI n` | 2 | A = n (load an immediate number) |
| `11` | `LDA a` | 2 | A = memory[a] (load from address a) |
| `12` | `STA a` | 2 | memory[a] = A (store to address a) |
| `20`-`24` | `ADD/SUB/AND/OR/XOR a` | 2 | A = A op memory[a]; sets Z and C |
| `28`-`2C` | `ADDI/SUBI/ANDI/ORI/XORI n` | 2 | A = A op n; sets Z and C |
| `30` | `JMP a` | 2 | PC = a |
| `31` | `JZ a` | 2 | PC = a if Z = 1 |
| `32` | `JNZ a` | 2 | PC = a if Z = 0 |
| `33` | `JC a` | 2 | PC = a if C = 1 |
| `34` | `JNC a` | 2 | PC = a if C = 0 |

The encoding is ours, chosen to make the hardware simple:

- The **high 4 bits** of the opcode say which group the instruction is in: `0` control, `1` load/store, `2` ALU, `3` jumps.
- In the ALU group, the **low 3 bits** are exactly the ALU operation code (0 ADD, 1 SUB, 2 AND, 3 OR, 4 XOR), so the IR's bits can drive the ALU directly. Bit 3 says "the operand is a number" (`28`-`2C`) rather than "the operand is an address" (`20`-`24`).
- Only ALU instructions change the flags. Loads and stores do not. (So `LDA` followed by `JZ` tests the flags of the **last ALU operation**, not of the loaded value; a common beginner trap, and true of many real processors.)

For subtraction, C means "no borrow": `C = 1` when `A >= operand` as unsigned numbers, exactly the adder/subtractor carry of Phase 14, Lesson 07.

### Running a program by hand

Here is a complete program, written as bytes in memory. It adds the numbers at addresses `0x10` and `0x11` and shows the result:

```
address  bytes   instruction   meaning
0x00     11 10   LDA 0x10      A = memory[0x10]
0x02     20 11   ADD 0x11      A = A + memory[0x11]
0x04     01      OUT           show A
0x05     0F      HLT           stop
...
0x10     19                    the number 25
0x11     11                    the number 17
```

Fetch-decode-execute, step by step:

```
PC = 0x00: fetch 11 -> LDA, read operand 10 -> A = memory[0x10] = 25, PC = 0x02
PC = 0x02: fetch 20 -> ADD, read operand 11 -> A = 25 + memory[0x11] = 25 + 17 = 42, Z = 0, C = 0, PC = 0x04
PC = 0x04: fetch 01 -> OUT: the output shows 42, PC = 0x05
PC = 0x05: fetch 0F -> HLT: stop
```

Notice that the data bytes `0x11` (17) and the opcode `0x11` (LDA) are the **same number**. Memory does not know which bytes are instructions. Only the PC decides: whatever byte the PC points at is treated as an opcode. If a program jumped to address `0x10` by mistake, the machine would happily execute 25 as an instruction. This is both the power and the danger of the stored-program idea.

### A program is just data

Change byte 2 of the program from `0x20` (ADD) to `0x21` (SUB), and the same machine now computes 25 - 17 = 8. No rewiring. Programs can even write into their own instruction bytes ("self-modifying code"); early programmers used this trick, and today it is mostly forbidden by the operating system for safety.

### A loop

Conditional jumps make loops. This 9-byte program counts down from 5 to 0:

```
address  bytes   instruction
0x00     10 05   LDI 5         A = 5
0x02     01      OUT           show A          <- loop starts here
0x03     29 01   SUBI 1        A = A - 1, sets Z when A reaches 0
0x05     32 02   JNZ 0x02      if Z = 0, go back to 0x02
0x07     01      OUT           show the final 0
0x08     0F      HLT
```

It executes 18 instructions and outputs 5, 4, 3, 2, 1, 0. A tiny program can do a lot of work because the PC goes back.

### The plan for this phase

```
Lesson 02  the ALU         8-bit add/sub/and/or/xor with flags, gate by gate in sim.logic
Lesson 03  memory          RAM from registers, a decoder and multiplexers
Lesson 04  the datapath    registers on a shared bus, moved by control signals
Lesson 05  the control unit the state machine that issues those signals: microcode
Lesson 06  instructions    an assembler that turns text into T8 machine code
Lesson 07  running         the whole machine running real programs, checked against this lesson's model
```

The Python model in this lesson's script (`run`) is the **specification**: every later lesson's hardware must produce the same results, cycle after cycle. Real chip teams work exactly like this: an "instruction set simulator" written first, and the hardware verified against it.

## Build It

The script `code/main.py` is the T8 reference model.

### Step 1: Names and sizes

```python
NAMES = {
    0x00: "NOP", 0x01: "OUT", 0x0F: "HLT",
    0x10: "LDI", 0x11: "LDA", 0x12: "STA",
    0x20: "ADD", 0x21: "SUB", 0x22: "AND", 0x23: "OR", 0x24: "XOR",
    0x28: "ADDI", 0x29: "SUBI", 0x2A: "ANDI", 0x2B: "ORI", 0x2C: "XORI",
    0x30: "JMP", 0x31: "JZ", 0x32: "JNZ", 0x33: "JC", 0x34: "JNC",
}
ONE_BYTE = {0x00, 0x01, 0x0F}
```

### Step 2: The ALU in one function

```python
def alu(op, a, b):
    if op == 0:
        total = a + b
        return total & 0xFF, int(total > 0xFF)
    if op == 1:
        total = a + ((~b) & 0xFF) + 1
        return total & 0xFF, int(total > 0xFF)
    results = {2: a & b, 3: a | b, 4: a ^ b}
    return results[op], 0
```

`& 0xFF` keeps the low 8 bits (what fits on 8 wires); the carry is whether the true total went above 255. Subtraction is done exactly as the hardware will do it: add the inverted operand plus one (Phase 14, Lesson 07).

### Step 3: The fetch-decode-execute loop

```python
def run(memory, max_instructions=1000, trace=False):
    mem = list(memory) + [0] * (256 - len(memory))
    pc, acc, z, c = 0, 0, 0, 0
    outputs = []
    for count in range(1, max_instructions + 1):
        opcode = mem[pc]
        operand = mem[(pc + 1) & 0xFF]
        size = 1 if opcode in ONE_BYTE else 2
        pc = (pc + size) & 0xFF
        group = opcode & 0xF0
        if opcode == 0x0F:
            return outputs, count, mem
        if opcode == 0x01:
            outputs.append(acc)
        elif opcode == 0x10:
            acc = operand
        elif opcode == 0x11:
            acc = mem[operand]
        elif opcode == 0x12:
            mem[operand] = acc
        elif group == 0x20:
            b = operand if opcode & 0x08 else mem[operand]
            acc, c = alu(opcode & 0x07, acc, b)
            z = int(acc == 0)
        elif group == 0x30:
            taken = {0x30: True, 0x31: z == 1, 0x32: z == 0, 0x33: c == 1, 0x34: c == 0}[opcode]
            if taken:
                pc = operand
    raise RuntimeError("program did not halt")
```

(The real script also prints a trace line per instruction when `trace=True`.) Look at how the decoding uses the bit fields: `opcode & 0xF0` is the group, `opcode & 0x08` the "immediate" bit, `opcode & 0x07` the ALU operation. The `max_instructions` limit stops a program that loops forever.

### Step 4: Run the examples

```
  pc=  0  fetch 11 10  LDA 0x10   -> A= 25 Z=0 C=0 pc=  2
  pc=  2  fetch 20 11  ADD 0x11   -> A= 42 Z=0 C=0 pc=  4
  pc=  4  fetch 01     OUT        -> A= 42 Z=0 C=0 pc=  5  OUT 42
  pc=  5  fetch 0F     HLT        -> halt
  output: [42], after 4 instructions
```

Then the same program with one byte changed outputs `[8]`, and the countdown outputs `[5, 4, 3, 2, 1, 0]` in 18 instructions.

Run it:

```bash
uv run python phases/16-a-computer-from-gates/01-what-a-computer-is/code/main.py
```

## Use It

- **Every processor** follows fetch-decode-execute, from an 8-bit AVR in an Arduino (Phase 17) to a 64-bit server CPU. Modern ones overlap the steps of many instructions at once (pipelining), but the model is the same.
- **Instruction set simulators**: QEMU, Spike (for RISC-V) and the simulators shipped with microcontroller tools are big versions of this lesson's `run`, used to test software before hardware exists and to check hardware against.
- **Historic 8-bit processors** such as the 6502 (Apple II, Commodore 64, NES) and the Z80 had an accumulator, a PC, flags and instructions very much like the T8's, with about 3,500 and 8,500 transistors.
- **Harvard architecture.** Many microcontrollers (AVR, PIC) keep program and data in separate memories, so a fetch and a data access can happen in the same cycle. The T8 uses the von Neumann single memory, which is simpler.
- **Security.** "A program is just data" is why a buffer overflow can make a computer run an attacker's bytes as instructions. Modern systems mark memory pages as non-executable to block this.

## Try It in the Lab

This lesson has no lab task. The labs of this phase start in Lesson 02, where you build a slice of the T8's ALU.

## Common Mistakes

- **Confusing an address with the value stored there.** `LDA 0x10` loads the **contents** of cell 0x10 (25), not the number 0x10 (16). `LDI 16` would load 16.
- **Forgetting that the PC moves before the instruction executes.** After fetching a 2-byte instruction at 0x02, the PC is already 0x04. A jump target is an absolute address, not a distance.
- **Testing flags after a load.** On the T8 only ALU instructions set Z and C. To test whether a loaded value is zero, do an ALU operation first, such as `ORI 0` or `ADDI 0`.
- **Letting the PC run into data.** Without a `HLT` or a jump, the PC continues into the data bytes and executes them as instructions.
- **Thinking 8 bits limits the computer to small numbers.** Bigger numbers are handled in pieces with the carry flag, the same way you add long numbers digit by digit.

## Exercises

1. Write the bytes of a T8 program that loads 100 from address `0x20`, subtracts the value at `0x21` (30), stores the result at `0x22` and halts. Check it by hand.
2. In the countdown program, what happens if `JNZ 0x02` is changed to `JNZ 0x00`? Trace the first two passes. What does the program output?
3. Byte `0x29` appears as an opcode (SUBI). Suppose a program accidentally jumps to an address holding the data byte 41 (= `0x29`). What will the T8 do next?
4. Why does `SUBI 1` from A = 5 set C = 1 on the T8? What would C be after `SUBI 6` from A = 5, and what is A then (as unsigned and as signed)?
5. Write a T8 program (as bytes) that outputs 0, 2, 4, 6, 8 and halts, using `ADDI`, `OUT` and a conditional jump. How many instructions does it execute? Run it with the script's `run` function to check.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Stored-program computer | "Von Neumann machine" | Instructions are numbers in the same memory as data, read and executed one after another |
| Program counter | "PC", "instruction pointer" | The register holding the address of the next instruction byte |
| Instruction register | "IR" | The register holding the opcode being executed |
| Accumulator | "A" | The register that receives ALU results in an accumulator machine |
| Fetch-decode-execute | "The instruction cycle" | Read the opcode at PC, work out its steps, carry them out, repeat |
| Opcode / operand | "The instruction and its argument" | The byte that names the operation / the byte it works on (a number or an address) |
| Flags | "Status bits" | One-bit registers (Z, C) set by the ALU and tested by conditional jumps |
| Instruction set | "ISA" | The complete list of instructions a processor understands and how they are encoded |

## Further Reading

- John von Neumann, *First Draft of a Report on the EDVAC* (1945), the document that described the stored-program organisation.
- Charles Petzold, *Code: The Hidden Language of Computer Hardware and Software* (2nd ed.), chapters on automation and the first processors.
- Noam Nisan and Shimon Schocken, *The Elements of Computing Systems* (Nand2Tetris), Chapters 4-5 (machine language and computer architecture).
- Ben Eater, "Building an 8-bit breadboard computer" video series (YouTube), a different small computer of the same family, built from 74LS chips.
