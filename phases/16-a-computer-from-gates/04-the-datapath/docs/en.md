# The Datapath

> The datapath is the computer's plumbing: registers, the ALU and memory joined by one shared bus, and nothing moves unless a control signal says so.

**Type:** Build
**Prerequisites:** Phase 15 (Sequential Logic), Lesson 04 (Registers), Phase 16 (A Computer from Gates), Lessons 01-03 (What a Computer Is, The ALU, Memory)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Datapath | All the parts that hold and transform data: registers, ALU, memory, bus | The kitchen: counters, bowls, oven, and the hatch between them |
| Bus | A set of wires shared by many parts, carrying one value at a time | A single-lane bridge: one car at a time, in either direction |
| Bus driver / source | The one part allowed to put its value on the bus in a given cycle | The person speaking in a meeting |
| Control signal | A one-bit wire that tells a part to act: "put your value on the bus", "load from the bus" | A light on a factory machine saying "go" |
| Control word | The set of all control signals active in one clock cycle | The list of jobs for this tick |
| Register transfer | Moving a value from one register to another through the bus in one cycle | Passing a dish through the hatch |
| RTL notation | Writing transfers as `MAR <- PC` ("MAR gets PC") | A recipe line in shorthand |
| MAR | Memory address register: holds the address that memory is looking at | The locker number written on a slip |
| IR | Instruction register: holds the opcode being executed | The current recipe line, pinned up |
| Bus conflict | Two parts trying to drive the bus at the same time | Two people shouting at once |
| Tri-state buffer | An output that can drive 0, 1, or disconnect itself | A tap that can be fully closed, not just hot or cold |
| Micro-step (T-state) | One clock cycle within the execution of an instruction | One beat within a bar of music |

## Learning Objectives

- Draw the T8 datapath and name what each register holds and which control signals it obeys.
- Explain the bus as a one-hot multiplexer and why only one source may drive it per cycle.
- Write instruction execution as register transfers (`MAR <- PC`, `IR <- mem[MAR]`, ...).
- Run LDA, ADD and OUT on the datapath by setting control signals by hand, one clock cycle at a time.
- Explain why fetching an instruction takes two cycles and how many cycles each T8 instruction needs.

## The Problem

Lessons 02 and 03 built the ALU and the memory. Lesson 01 listed the registers. They are islands: nothing connects the memory's data output to the instruction register, or the ALU's result to the accumulator. We need wiring, and we need it to be cheap.

Connecting every part directly to every other part needs a separate 8-wire path for every pair: with 7 parts that is 21 paths, 168 wires, each with its own multiplexer at the receiving end. The classic solution, used in every early computer and still inside many chips, is a single **bus**: 8 shared wires that every part can read and that exactly one part at a time may drive. Then the only question is, in each clock cycle, **who drives the bus and who loads from it**. Those decisions are a handful of control signals. This lesson builds the T8's datapath and drives those signals by hand; Lesson 05 builds the control unit that drives them automatically.

## The Physics

On a breadboard computer, the bus is literally 8 wires, and each register's output connects to them through a **tri-state buffer**: when its enable is off, its output transistors are both off, so the output floats and does not fight the others (Phase 14, Lesson 08). If two enabled buffers drive opposite values, one pulls up and the other pulls down through their on-resistances: a short circuit from supply to ground, tens of milliamps, hot chips and an undefined voltage on the wire. That is a **bus conflict**, and it is a real electrical fault, not just a logic error.

Inside modern chips, tri-state buses are avoided: the bus is a real multiplexer built from gates, where a conflict cannot cause a short. Logically the two are the same: a one-hot select chooses which source reaches the wires. Our simulator builds the multiplexer version and the datapath model refuses (raises an error) if two sources are enabled at once.

## The Concept

### The T8 datapath

```
                                 8-bit bus
   ==================================================================
      ^ |          |           ^ |           |         ^       |
PC_OUT| |PC_IN  MAR_IN   MEM_OUT| |MEM_IN   IR_IN  A_OUT|  A_IN | B_IN     OUT_IN
      | v          v           | v           v         |       v    v         v
    +----+      +-----+     +--------+    +----+     +---+       +---+     +-----+
    | PC |      | MAR |---->| memory |    | IR |     | A |       | B |     | OUT |
    +----+      +-----+ addr| 256 B  |    +----+     +---+       +---+     +-----+
    PC_INC                  +--------+      |          |           |
                                            | op bits  v           v
                                            +------> [    ALU     ] --ALU_OUT--> bus
                                                       |   Z, C
                                                    FLAGS_IN -> [Z][C]
```

Each register is a Phase 15 register with a load enable. Its enable is a control signal named `<register>_IN`. The parts that can **drive** the bus have an output enable named `<part>_OUT`:

| Signal | Effect at the clock edge (or during the cycle, for outputs) |
|---|---|
| `PC_OUT` | the PC drives the bus |
| `MEM_OUT` | memory drives the bus with `mem[MAR]` |
| `A_OUT` | the accumulator drives the bus |
| `ALU_OUT` | the ALU result drives the bus |
| `MAR_IN` | MAR loads the bus |
| `MEM_IN` | memory stores the bus at address MAR |
| `IR_IN` | IR loads the bus |
| `A_IN`, `B_IN`, `OUT_IN` | A, B or OUT loads the bus |
| `PC_IN` | PC loads the bus (a jump) |
| `PC_INC` | PC counts up by one |
| `FLAGS_IN` | Z and C load the ALU's flags |

Some connections bypass the bus because they never need it: the MAR is wired straight to the memory's address input, A and B are wired straight to the ALU's inputs, and the low 3 bits of IR are wired straight to the ALU's operation inputs. The ALU computes all the time; its result only matters in a cycle with `ALU_OUT`.

### The bus is a multiplexer

With four possible sources, each bit of the bus is a 4-input AND-OR multiplexer with one-hot selects, exactly as in Phase 14, Lesson 08:

```
bus_i = PC_OUT·pc_i + MEM_OUT·mem_i + A_OUT·a_i + ALU_OUT·alu_i
```

8 bits times (4 ANDs + 1 OR) = 40 gates. The simulator builds it and shows that enabling each source puts that source's value on the bus. If no source is enabled, the bus reads 0; if two are, the OR mixes their bits, which is garbage. The control unit must guarantee exactly one source whenever some register loads.

### One cycle, one transfer

The rule of a single-bus datapath: **in each clock cycle, one source drives the bus, and any number of registers may load from it at the edge.** So one cycle can copy one value into several places, but can never move two different values. We write transfers in **register transfer notation**:

```
MAR <- PC          "MAR gets the value of PC"   signals: PC_OUT, MAR_IN
IR <- mem[MAR]     "IR gets the byte at address MAR"   signals: MEM_OUT, IR_IN
```

Several things can happen in the same cycle as long as they do not need the bus twice. `PC_INC` uses the PC's own counter, not the bus, so `IR <- mem[MAR], PC <- PC + 1` is a single cycle.

### Fetching an instruction: two cycles

```
T0:  MAR <- PC                       PC_OUT, MAR_IN
T1:  IR <- mem[MAR],  PC <- PC + 1   MEM_OUT, IR_IN, PC_INC
```

Why two cycles and not one? Because the memory reads the address in MAR. The PC's value must first travel over the bus into MAR (one cycle), and only then can memory deliver the byte at that address (the next cycle). The bus can carry only one value per cycle, and here we need two: the address and then the data.

### Executing LDA a: three more cycles

After the fetch, the IR holds `0x11` (LDA) and the PC points at the operand byte.

```
T2:  MAR <- PC                       PC_OUT, MAR_IN       point at the operand
T3:  MAR <- mem[MAR],  PC <- PC + 1  MEM_OUT, MAR_IN, PC_INC   the operand IS the address
T4:  A <- mem[MAR]                   MEM_OUT, A_IN        load the data
```

Look at T3: memory drives the bus with the operand byte (the address `a`), and the same bus value is loaded **into MAR**. That works because MAR loads at the clock edge, after the memory has delivered the value during the cycle (Phase 15: all registers sample at the edge). The next cycle, memory looks at the new address.

### Executing ADD a: four more cycles

```
T2:  MAR <- PC                       PC_OUT, MAR_IN
T3:  MAR <- mem[MAR],  PC <- PC + 1  MEM_OUT, MAR_IN, PC_INC
T4:  B <- mem[MAR]                   MEM_OUT, B_IN        second operand into B
T5:  A <- ALU,  flags <- ALU         ALU_OUT, A_IN, FLAGS_IN
```

In T5 the ALU's result (`A + B`, because IR's low bits are 000) drives the bus and A loads it. A is both an ALU input and the destination in the same cycle. That is safe for the same reason as before: during the cycle A still holds the old value, the ALU computes from it, and A only changes at the edge.

### Executing OUT: one more cycle

```
T2:  OUT <- A                        A_OUT, OUT_IN
```

### The whole run, cycle by cycle

The program at address 0 is `11 10 20 11 01 0F` (LDA 0x10, ADD 0x11, OUT, HLT), with 25 at `0x10` and 17 at `0x11`. Setting the signals by hand, the simulator prints:

```
   0 MAR_IN, PC_OUT               bus=  0 00h  PC=00 MAR=00 IR=00 A=  0 B=  0 OUT=  0
   1 IR_IN, MEM_OUT, PC_INC       bus= 17 11h  PC=01 MAR=00 IR=11 A=  0 B=  0 OUT=  0
   2 MAR_IN, PC_OUT               bus=  1 01h  PC=01 MAR=01 IR=11 A=  0 B=  0 OUT=  0
   3 MAR_IN, MEM_OUT, PC_INC      bus= 16 10h  PC=02 MAR=10 IR=11 A=  0 B=  0 OUT=  0
   4 A_IN, MEM_OUT                bus= 25 19h  PC=02 MAR=10 IR=11 A= 25 B=  0 OUT=  0
   5 MAR_IN, PC_OUT               bus=  2 02h  PC=02 MAR=02 IR=11 A= 25 B=  0 OUT=  0
   6 IR_IN, MEM_OUT, PC_INC       bus= 32 20h  PC=03 MAR=02 IR=20 A= 25 B=  0 OUT=  0
   7 MAR_IN, PC_OUT               bus=  3 03h  PC=03 MAR=03 IR=20 A= 25 B=  0 OUT=  0
   8 MAR_IN, MEM_OUT, PC_INC      bus= 17 11h  PC=04 MAR=11 IR=20 A= 25 B=  0 OUT=  0
   9 B_IN, MEM_OUT                bus= 17 11h  PC=04 MAR=11 IR=20 A= 25 B= 17 OUT=  0
  10 ALU_OUT, A_IN, FLAGS_IN      bus= 42 2Ah  PC=04 MAR=11 IR=20 A= 42 B= 17 OUT=  0
  11 MAR_IN, PC_OUT               bus=  4 04h  PC=04 MAR=04 IR=20 A= 42 B= 17 OUT=  0
  12 IR_IN, MEM_OUT, PC_INC       bus=  1 01h  PC=05 MAR=04 IR=01 A= 42 B= 17 OUT=  0
  13 A_OUT, OUT_IN                bus= 42 2Ah  PC=05 MAR=04 IR=01 A= 42 B= 17 OUT= 42
```

(The register values are shown **after** each clock edge; the script also prints the flags, left out here for width.) Read row 8: the bus carries 0x11, the operand of ADD, which is an address; MAR loads it. Row 9: memory now shows the byte at 0x11, which is 17; B loads it. Row 10: the gate-level ALU computes 25 + 17 = 42 and A loads it. Row 13: the output register shows 42, the same answer as the reference model of Lesson 01, after 14 clock cycles.

### Cycles per instruction

Counting the steps (including the 2 fetch cycles) for every T8 instruction:

```
NOP, OUT, HLT          3 cycles     fetch + 1
LDI n, JMP a, Jcc a    4 cycles     fetch + operand fetch (2)
LDA a, STA a           5 cycles     fetch + operand (2) + memory access (1)
ADDI n ... XORI n      5 cycles     fetch + operand into B (2) + ALU (1)
ADD a ... XOR a        6 cycles     fetch + operand (2) + memory into B (1) + ALU (1)
```

Lesson 05 writes these steps into the control unit's microcode table. A T8 at 1 MHz runs about 200,000 instructions per second. Real processors overlap the steps of consecutive instructions (pipelining) to finish about one instruction per cycle, and use separate buses (or no bus at all, just multiplexers in front of each unit) to move several values per cycle.

## Build It

The script `code/main.py` builds the bus multiplexer and a datapath model that uses the gate-level ALU of Lesson 02.

### Step 1: The ALU and the bus multiplexer

`build_alu` is the same function as in Lesson 02. The bus multiplexer:

```python
SOURCES = ["PC_OUT", "MEM_OUT", "A_OUT", "ALU_OUT"]

def bus_mux():
    lc = LogicCircuit("8-bit bus, 4 sources, one-hot select")
    lc.inputs(*SOURCES, *[f"{src}.{i}" for src in SOURCES for i in range(BITS)])
    for i in range(BITS):
        for src in SOURCES:
            lc.and_(f"{src}.g{i}", f"{src}.{i}", src)
        lc.or_(f"bus{i}", *[f"{src}.g{i}" for src in SOURCES])
    lc.outputs(*[f"bus{i}" for i in range(BITS)])
    return lc
```

### Step 2: The datapath model

The registers are plain integers in a dictionary. The memory is the `Memory` class of Lesson 03. The ALU is the gate-level circuit, evaluated from the current A, B and the low 3 bits of IR:

```python
class Datapath:
    def __init__(self, memory):
        self.mem = memory
        self.alu = build_alu()
        self.reg = {"PC": 0, "MAR": 0, "IR": 0, "A": 0, "B": 0, "OUT": 0, "Z": 0, "C": 0}
```

### Step 3: One source on the bus

```python
    def bus(self, signals):
        drivers = [s for s in SOURCES if s in signals]
        if len(drivers) > 1:
            raise BusConflict(f"two sources drive the bus at once: {drivers}")
        if not drivers:
            return None
        source = drivers[0]
        if source == "PC_OUT":
            return self.reg["PC"]
        if source == "MEM_OUT":
            return self.mem.read(self.reg["MAR"])
        if source == "A_OUT":
            return self.reg["A"]
        return self.alu_outputs()[0]
```

### Step 4: One clock edge

All loads happen together, from values computed **before** the edge, exactly like flip-flops:

```python
    def clock(self, signals):
        value = self.bus(signals)
        result, z, c = self.alu_outputs()
        new = dict(self.reg)
        for name, reg in [("MAR_IN", "MAR"), ("IR_IN", "IR"), ("A_IN", "A"), ("B_IN", "B"), ("OUT_IN", "OUT"), ("PC_IN", "PC")]:
            if name in signals:
                new[reg] = value
        if "PC_INC" in signals:
            new["PC"] = (self.reg["PC"] + 1) & 0xFF
        if "FLAGS_IN" in signals:
            new["Z"], new["C"] = z, c
        if "MEM_IN" in signals:
            self.mem.write(self.reg["MAR"], value)
        self.reg = new
        return value
```

Writing all the new values into `new` and replacing `self.reg` at the end is what makes `MAR <- mem[MAR]` and `A <- A + B` behave correctly.

### Step 5: Drive it by hand

The script lists the 14 control words shown above and calls `dp.clock(signals)` for each, then tries `{"PC_OUT", "A_OUT", "B_IN"}` to show the bus-conflict check.

Run it:

```bash
uv run python phases/16-a-computer-from-gates/04-the-datapath/code/main.py
```

## Use It

- **Breadboard computers** built from 74LS chips use exactly this design: an 8-wire bus, 74LS245 tri-state buffers or 74LS173 registers with tri-state outputs, and LEDs on the bus to watch values move.
- **Early microprocessors** such as the Intel 8080 and the 6502 had a single internal data bus (or two) connecting their registers and ALU, and needed several cycles per instruction for the same reason as the T8.
- **System buses** connect chips on a board: the ISA bus of early PCs, I2C and SPI today (Phase 17), each with rules about who may drive the wires when.
- **Modern processors** replace the shared bus with a "bypass network" of multiplexers so that every unit can receive any result in the next cycle, moving many values per cycle.
- **RTL design**: hardware designers describe chips at the "register transfer level" (Verilog, VHDL), writing transfers like `a <= a + b;` on clock edges, which synthesis turns into gates (Phase 20, Lesson 11).

## Try It in the Lab

This lesson has no lab task; the datapath is easiest to explore in the script. Change the control words: for example, try to run `ADD` without the cycle that loads B, and see what A becomes.

## Common Mistakes

- **Two sources in one cycle.** On a real tri-state bus it is a short circuit; in a multiplexer bus it is garbage data. Every control word must have at most one `_OUT` signal.
- **Expecting a register to change during the cycle.** A loads only at the edge. In the cycle `A <- ALU`, the ALU still sees the old A, which is exactly why it works.
- **Reading memory in the same cycle the address is set.** `MAR <- PC` and `IR <- mem[MAR]` must be separate cycles, because memory uses the MAR value from before the edge.
- **Forgetting PC_INC after reading an operand.** Without it, the next fetch reads the operand byte as an opcode.
- **Confusing the bus value with a register value.** The bus is just wires; it holds nothing between cycles. A value survives only if some register loads it.

## Exercises

1. Write the register transfers and control words for `STA a` (store A at address a), starting after the fetch.
2. Write the transfers for `ADDI n`. Why does it need one cycle less than `ADD a`?
3. Why can't `MAR <- PC` and `IR <- mem[MAR]` be merged into one cycle on this datapath? What extra hardware would allow it?
4. A program runs 1000 instructions: 300 LDA/STA, 400 ADD (memory), 200 ADDI, 100 jumps. Using the cycle counts in this lesson, how many clock cycles does it take? At 4 MHz, how long?
5. In the script, add an `ALU_OUT` and an `A_OUT` in the same control word and observe the error. Then remove the conflict check and look at the bus value the gate-level multiplexer would produce if both were enabled (compute it by hand as a bitwise OR).

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Datapath | "The data side" | Registers, ALU, memory and the interconnect that moves data between them |
| Bus | "The data bus" | Shared wires driven by one selected source per cycle, readable by all |
| Control signal | "Enable line" | A bit that makes a part drive the bus (`_OUT`) or load from it (`_IN`) |
| Control word | "Microinstruction" | All control signals for one clock cycle |
| Register transfer | "`MAR <- PC`" | One cycle moving a value over the bus into one or more registers |
| Bus conflict | "Contention" | More than one source enabled at once |
| Tri-state | "High-Z" | An output that can disconnect itself so others can drive the shared wire |
| T-state | "Micro-step" | One clock cycle inside an instruction; T0 and T1 are the fetch |

## Further Reading

- Albert Paul Malvino and Jerald A. Brown, *Digital Computer Electronics* (3rd ed.), the chapters on the SAP computers, a classic textbook treatment of a bus-based 8-bit computer.
- David Harris and Sarah Harris, *Digital Design and Computer Architecture*, Chapter 7 (Microarchitecture: single-cycle and multicycle processors), for the same ideas on a RISC processor.
- Ben Eater, "Building an 8-bit breadboard computer" videos on the bus, registers and the ALU (YouTube).
- Texas Instruments datasheet *SN74LS245* (octal bus transceivers with 3-state outputs).
