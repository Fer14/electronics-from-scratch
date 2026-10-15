# The Control Unit

> The control unit is a state machine whose state is "which step of which instruction", and whose outputs are the control signals that make the datapath move.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lesson 08 (Multiplexers and Decoders), Phase 15 (Sequential Logic), Lessons 05-06 (Counters, Finite State Machines), Phase 16 (A Computer from Gates), Lesson 04 (The Datapath)
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Control unit | The part of a processor that decides, every cycle, which control signals are on | The conductor of an orchestra |
| Step counter | A counter that numbers the cycles within one instruction: T0, T1, T2, ... | The beat count within a bar |
| T-state | One value of the step counter, one clock cycle of an instruction | Beat 1, beat 2, beat 3 |
| Microcode | A table that lists the control word for every (instruction, step, flags) combination | A choreography sheet: on beat 3 of move X, raise the left arm |
| Microinstruction | One row of that table: the control word for one step | One line of the choreography |
| Control ROM | A read-only memory that stores the microcode | The printed choreography sheet |
| Hardwired control | Control signals computed by gates directly, without a table | A dancer who knows the moves by heart |
| END | A control signal that resets the step counter, finishing the instruction | "Back to the start of the bar" |
| HALT | A control signal that stops the clock | The final chord |
| Instruction decoder | Logic that turns the opcode into "kind of instruction" lines | Reading the title of a dance to know which choreography to use |
| Conditional microcode | Steps that depend on a flag, used for conditional jumps | "If the audience claps, take a bow; otherwise leave" |

## Learning Objectives

- Explain the control unit as a finite state machine whose state is (opcode in IR, step counter).
- Write the T8's microcode: the control word of every step of every instruction, including the flag-dependent steps of conditional jumps.
- Build the step counter with an END reset in `sim.logic` and watch it count through instructions.
- Store the microcode as a ROM, and compute its size from the address and word widths.
- Derive hardwired equations for control signals and verify them against the microcode for every case.
- Compare microcoded and hardwired control.

## The Problem

In Lesson 04 we made the T8 run three instructions by typing 14 control words by hand. A real computer has to produce those control words by itself, every cycle, for whatever instruction it has just fetched, at millions of cycles per second.

What does the control unit know? Only two things: the opcode in the IR (which instruction this is) and how many cycles have passed since this instruction started (which step it is at). From those, plus the flags for conditional jumps, it must produce 15 control signals. That is a combinational function of a few inputs, plus a counter. In other words, a finite state machine (Phase 15, Lesson 06), with the IR and a step counter as its state. This lesson builds it two ways: as a table (microcode) and as gates (hardwired), and checks that both agree.

## The Physics

The control unit is ordinary synchronous logic: a 3-bit counter (Phase 15, Lesson 05), a decoder, and either a ROM or a few dozen gates. Its timing matters, though: the control signals must settle at the start of each cycle before the datapath can use them, so the control unit's delay adds to the critical path. A microcode ROM read can be slow (a ROM is a decoder plus a large OR array, Lesson 03), which is one reason fast processors use hardwired control for common instructions. Glitches on control signals during a cycle are harmless as long as every register samples only at the clock edge (Phase 15, Lesson 03), which is another reason the T8 is strictly synchronous: a glitch on `MEM_IN` in an asynchronous memory would write garbage.

## The Concept

### What the control unit has to do

```
                +---------------+
  clk --------->| step counter  |---- T (3 bits) ---+
       END ---->| (reset)       |                   |
                +---------------+                   v
                                           +------------------+
  IR (opcode, 8 bits) -------------------->|                  |
  flags Z, C ----------------------------->|  control logic   |----> 15 control signals
                                           |  (ROM or gates)  |      PC_OUT, MEM_OUT, ...
                                           +------------------+      END, HALT
```

The step counter starts at 0 for every instruction and counts up each clock. When the last step of an instruction asserts `END`, the counter resets to 0 at that edge, and the next cycle begins the fetch of the next instruction. `HALT` stops the clock.

### The fetch steps are the same for everyone

Steps T0 and T1 are the fetch, and they cannot depend on the opcode, because at T0 and T1 the new opcode is not in the IR yet: it is being loaded at the end of T1.

```
T0:  PC_OUT, MAR_IN               MAR <- PC
T1:  MEM_OUT, IR_IN, PC_INC       IR <- mem[MAR], PC <- PC + 1
```

From T2 on, the IR holds the opcode and the control logic can look at it.

### The microcode of the T8

Each line is one clock cycle. Writing them follows directly from the register transfers of Lesson 04:

```
NOP          T2: END
OUT          T2: A_OUT, OUT_IN, END
HLT          T2: HALT
LDI n        T2: PC_OUT, MAR_IN                   point at the operand
             T3: MEM_OUT, A_IN, PC_INC, END       A <- n
LDA a        T2: PC_OUT, MAR_IN
             T3: MEM_OUT, MAR_IN, PC_INC          MAR <- a
             T4: MEM_OUT, A_IN, END               A <- mem[a]
STA a        T2: PC_OUT, MAR_IN
             T3: MEM_OUT, MAR_IN, PC_INC
             T4: A_OUT, MEM_IN, END               mem[a] <- A
ADD..XOR a   T2: PC_OUT, MAR_IN
             T3: MEM_OUT, MAR_IN, PC_INC
             T4: MEM_OUT, B_IN                    B <- mem[a]
             T5: ALU_OUT, A_IN, FLAGS_IN, END     A <- A op B
ADDI..XORI n T2: PC_OUT, MAR_IN
             T3: MEM_OUT, B_IN, PC_INC            B <- n
             T4: ALU_OUT, A_IN, FLAGS_IN, END
JMP a        T2: PC_OUT, MAR_IN
             T3: MEM_OUT, PC_IN, END              PC <- a
Jcc a        T2: PC_OUT, MAR_IN
             T3 if taken:     MEM_OUT, PC_IN, END
             T3 if not taken: PC_INC, END         skip the operand byte
```

Three design points worth noticing:

1. **The ALU operation is not in the microcode.** All five ALU instructions share the same steps; the ALU reads its operation directly from the IR's low 3 bits (Lesson 01's encoding). One microcode routine serves five instructions.
2. **Conditional jumps are the only steps that depend on flags.** Taken: load the PC from the operand. Not taken: just step the PC past the operand. Either way the instruction takes 4 cycles.
3. **END is on the last useful step**, so no cycle is wasted. NOP takes 3 cycles; ADD with a memory operand takes 6.

### Control words as numbers

Give each of the 15 signals a bit position:

```
bit:  14    13   12     11      10    9      8     7    6     5      4      3       2      1       0
     HALT  END PC_INC FLAGS_IN PC_IN OUT_IN B_IN  A_IN IR_IN MEM_IN MAR_IN ALU_OUT A_OUT MEM_OUT PC_OUT
```

Then each step is a 15-bit number, printed in hex by the script:

```
  11 LDA  (5 cycles)
      T0: 0011  PC_OUT, MAR_IN
      T1: 1042  MEM_OUT, IR_IN, PC_INC
      T2: 0011  PC_OUT, MAR_IN
      T3: 1012  MEM_OUT, MAR_IN, PC_INC
      T4: 2082  MEM_OUT, A_IN, END
```

Check `T0 = 0011`: `PC_OUT` is bit 0 (value 1) and `MAR_IN` is bit 4 (value 16); 1 + 16 = 17 = 0x11. Check `T4 = 2082`: `MEM_OUT` (bit 1, 2) + `A_IN` (bit 7, 128) + `END` (bit 13, 8192) = 8322 = 0x2082.

### Microcode in a ROM

A ROM (Lesson 03) is a lookup table: an address goes in, a stored word comes out. Make the address the concatenation of everything the control unit looks at:

```
ROM address = opcode (8 bits) | step (3 bits) | Z (1 bit) | C (1 bit)  = 13 bits
ROM word    = the 15 control bits
```

`2^13 = 8192` words of 15 bits: 122,880 bits. Only 392 of those words are used by the 21 instructions (counting each flag combination separately); the rest can hold anything, for example "END", so an undefined opcode behaves like NOP. Real microcoded machines compress this by decoding the opcode to a short "microprogram start address" first, but the idea is the same.

The beauty of microcode is that changing the instruction set is a change of table, not of wiring. Fixing a bug in the microcode of a running processor is literally a firmware update; Intel and AMD ship microcode updates for exactly that.

### The step counter

The step counter is the synchronous counter of Phase 15, Lesson 05, with the `END` signal on its synchronous reset. It counts every clock and returns to 0 at the edge where `END = 1`. For two LDA instructions in a row (5 steps each, END on T4), the simulator shows:

```
  two LDA instructions in a row: T-states [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
```

A 3-to-8 decoder (Phase 14, Lesson 08) turns its 3 bits into one-hot step lines `t0..t7`, which hardwired control uses.

### Hardwired control: equations instead of a table

Each control signal is a Boolean function of the step lines, the instruction kind and the flags. Read the microcode table column by column instead of row by row. Where does `MAR_IN` appear?

- in T0 of every instruction,
- in T2 of every two-byte instruction,
- in T3 of instructions whose operand is an address (LDA, STA, and the memory ALU instructions).

So, with decoder lines `two` (two-byte instruction) and `mem` (memory operand):

```
MAR_IN = t0 + t2·two + t3·mem
```

Where does `A_IN` appear? In T3 of LDI, T4 of LDA, T5 of the memory ALU instructions and T4 of the immediate ALU instructions:

```
A_IN = t3·LDI + t4·LDA + t5·ALUm + t4·ALUi
```

The instruction-kind lines come from a small decoder on the opcode bits, made easy by the encoding of Lesson 01. For example, `ALUm` is "high nibble is 2 and bit 3 is 0", and `two` is "the high nibble is not 0".

The script builds both equations in `sim.logic` (8 gates), feeds them every combination of instruction, step and flags, and compares with the microcode table:

```
  1008 checks over all instructions, steps and flags: 0 wrong; 8 gates
```

Do this for all 15 signals and you have a hardwired control unit: no ROM, a few dozen gates, and faster. The price: changing an instruction means redesigning logic.

### Microcoded versus hardwired

```
                 microcoded (ROM)                    hardwired (gates)
flexibility      change the table                    redesign the logic
speed            a ROM read every cycle              a few gate delays
size             grows with instructions x steps     grows with the number of distinct conditions
typical use      complex instruction sets (x86's     simple instruction sets (RISC-V, ARM cores),
                 rare complex instructions)          and the common instructions of every CPU
```

Historically, microcode was invented by Maurice Wilkes in 1951 to make complex control units systematic. IBM's System/360 (1964) used it so that machines of very different speeds could run the same instruction set. The RISC movement of the 1980s returned to hardwired control with simple instructions. Modern x86 processors decode most instructions in hardware and fall back to microcode only for the complicated ones.

### The control unit as a state machine

Put the pieces into the shape of Phase 15, Lesson 06:

- **State:** the step counter (3 bits) and, from T2 on, the opcode in the IR. (Strictly the IR is part of the datapath, but the control unit reads it as part of its state.)
- **Inputs:** the flags Z and C.
- **Next-state logic:** step + 1, or 0 when `END`.
- **Output logic:** the microcode ROM or the hardwired equations. Outputs depend on the state (and, for conditional jumps, on the flags), so it is a Moore machine with a little Mealy flavour at the jump step.

## Build It

The script `code/main.py` writes the microcode, packs it into control words, builds the step counter and checks hardwired equations against the table.

### Step 1: Signals and shared steps

```python
SIGNALS = ["PC_OUT", "MEM_OUT", "A_OUT", "ALU_OUT", "MAR_IN", "MEM_IN", "IR_IN", "A_IN",
           "B_IN", "OUT_IN", "PC_IN", "FLAGS_IN", "PC_INC", "END", "HALT"]
FETCH = [{"PC_OUT", "MAR_IN"}, {"MEM_OUT", "IR_IN", "PC_INC"}]
POINT = {"PC_OUT", "MAR_IN"}
ADDRESS = {"MEM_OUT", "MAR_IN", "PC_INC"}
```

`POINT` points MAR at the operand byte; `ADDRESS` replaces MAR with the operand (an address) and steps the PC past it.

### Step 2: The microcode

```python
def steps_for(opcode, z=0, c=0):
    if opcode == 0x00:
        tail = [{"END"}]
    elif opcode == 0x01:
        tail = [{"A_OUT", "OUT_IN", "END"}]
    elif opcode == 0x0F:
        tail = [{"HALT"}]
    elif opcode == 0x10:
        tail = [POINT, {"MEM_OUT", "A_IN", "PC_INC", "END"}]
    elif opcode == 0x11:
        tail = [POINT, ADDRESS, {"MEM_OUT", "A_IN", "END"}]
    elif opcode == 0x12:
        tail = [POINT, ADDRESS, {"A_OUT", "MEM_IN", "END"}]
    elif 0x20 <= opcode <= 0x24:
        tail = [POINT, ADDRESS, {"MEM_OUT", "B_IN"}, {"ALU_OUT", "A_IN", "FLAGS_IN", "END"}]
    elif 0x28 <= opcode <= 0x2C:
        tail = [POINT, {"MEM_OUT", "B_IN", "PC_INC"}, {"ALU_OUT", "A_IN", "FLAGS_IN", "END"}]
    elif 0x30 <= opcode <= 0x34:
        last = {"MEM_OUT", "PC_IN", "END"} if jump_taken(opcode, z, c) else {"PC_INC", "END"}
        tail = [POINT, last]
    else:
        tail = [{"END"}]
    return FETCH + tail


def microcode(opcode, step, z, c):
    steps = steps_for(opcode, z, c)
    return steps[step] if step < len(steps) else set()
```

`microcode(opcode, step, z, c)` is exactly what a ROM would return for that address.

### Step 3: Control words

```python
def control_word(signals):
    return sum(1 << SIGNALS.index(s) for s in signals)
```

### Step 4: The step counter

```python
def step_counter():
    lc = LogicCircuit("3-bit step counter with END reset")
    lc.inputs("end")
    toggle = "one"
    lc.constant("one", 1)
    for i in range(3):
        lc.xor(f"d{i}", f"t{i}", toggle)
        lc.dff(f"d{i}", f"t{i}", name=f"T{i}", reset="end")
        if i < 2:
            lc.and_(f"k{i + 1}", toggle, f"t{i}")
            toggle = f"k{i + 1}"
    lc.outputs("t2", "t1", "t0")
    return lc
```

The same counter as Phase 15, Lesson 05, always enabled (the constant `one`), with `reset="end"`.

### Step 5: Hardwired equations

```python
def hardwired():
    lc = LogicCircuit("hardwired MAR_IN and A_IN")
    lc.inputs("t0", "t1", "t2", "t3", "t4", "t5", "ldi", "lda", "alum", "alui", "two", "mem")
    lc.and_("m2", "t2", "two")
    lc.and_("m3", "t3", "mem")
    lc.or_("MAR_IN", "t0", "m2", "m3")
    lc.and_("a3", "t3", "ldi")
    lc.and_("a4", "t4", "lda")
    lc.and_("a5", "t5", "alum")
    lc.and_("a4i", "t4", "alui")
    lc.or_("A_IN", "a3", "a4", "a5", "a4i")
    lc.outputs("MAR_IN", "A_IN")
    return lc
```

The check loops over all 21 instructions, steps 0 to 5 and the four flag combinations, sets one step line, computes the instruction-kind lines with `classes(opcode)`, and compares both signals with the microcode.

Run it:

```bash
uv run python phases/16-a-computer-from-gates/05-the-control-unit/code/main.py
```

## Use It

- **Breadboard computers** often store microcode in EEPROM chips (such as the 28C16), with the opcode and step counter on the address pins and the control lines on the data pins, exactly the ROM layout of this lesson.
- **x86 processors** decode simple instructions in hardware but run complex ones (string moves, some floating-point and system instructions) from a microcode ROM, which can be patched at boot by a microcode update.
- **IBM System/360** used microcode so that cheap and expensive models could run the same programs.
- **RISC processors** (RISC-V, ARM) use hardwired control, made simple by fixed-length instructions with regular fields, the same idea as the T8's ALU bits taken straight from the opcode.
- **FPGA soft processors** often implement control as a small ROM in block RAM, because changing the table is easier than re-synthesising logic.

## Try It in the Lab

The lab task "Decode the MAR_IN control signal" gives you the step lines `t0`, `t2`, `t3` and the instruction-kind lines `two` and `mem`. The final OR with `t0` is fixed. Fill the three slots so that `mar_in = t0 + t2·two + t3·mem` for all 32 input combinations. Parts: AND, OR, XOR, NAND.

Think about: each of the three conditions is "this step and this kind of instruction". How are the conditions combined?

## Common Mistakes

- **Making the fetch steps depend on the opcode.** At T0 and T1 the IR still holds the previous instruction. Fetch must be identical for all.
- **Forgetting END.** Without it the step counter runs into empty steps, wasting cycles, or wraps around and executes nonsense.
- **Forgetting PC_INC on the not-taken jump.** The PC would then point at the operand byte and execute it as an opcode.
- **Two _OUT signals in one microinstruction.** The control unit, not the datapath, is responsible for avoiding bus conflicts. Check every row of the table.
- **Changing flags with loads.** Only `FLAGS_IN` (in the ALU steps) updates Z and C, which is what the instruction set promises (Lesson 01).

## Exercises

1. Write the hardwired equation for `PC_INC` from the microcode table. Which steps and instruction kinds does it involve? Where do the flags enter?
2. Write the hardwired equation for `MEM_OUT`. How many product terms does it have?
3. Add a new instruction `SHL` (opcode `0x05`, one byte) that doubles A using the ALU: what steps would it need with the existing datapath? (Hint: you can use ADD if B holds a copy of A. Which transfer puts A into B?)
4. The T8's microcode ROM has 13 address bits. If the opcode were first decoded to a 5-bit "routine number" (there are only about 10 different routines), how many address bits and how many words would the ROM need?
5. Count the cycles for this program: `LDI 5`, `SUBI 1`, `JNZ` back to the `SUBI` (taken 4 times, then not taken), `HLT`. At 1 MHz, how long does it run?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Control unit | "The controller" | Step counter plus logic that produces every control signal from opcode, step and flags |
| Step counter | "T-state counter", "ring counter" | Counts cycles within an instruction; reset by END |
| Microcode | "Microprogram" | The table of control words for each instruction step |
| Microinstruction | "Control word" | One row of microcode: the signals for one cycle |
| Control ROM | "Microcode store" | ROM addressed by opcode, step and flags, outputting control words |
| Hardwired control | "Random logic control" | Each control signal as a Boolean equation of step lines, instruction kind and flags |
| END / HALT | "Next instruction" / "stop" | Reset the step counter / stop the clock |
| Instruction decoder | "Decode logic" | Turns the opcode into instruction-kind lines (two-byte, memory operand, ALU, ...) |

## Further Reading

- Maurice V. Wilkes, "The Best Way to Design an Automatic Calculating Machine" (1951), the original proposal of microprogramming.
- David A. Patterson and John L. Hennessy, *Computer Organization and Design*, the chapter on the processor (datapath and control), and their discussion of microprogramming versus hardwired control.
- Albert Paul Malvino and Jerald A. Brown, *Digital Computer Electronics*, chapters on the SAP-1 and SAP-2 controller-sequencers.
- Ben Eater, "8-bit computer control logic" videos (YouTube), building microcode in EEPROMs.
