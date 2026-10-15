# Running a Program

> Put the ALU, the memory, the datapath, the control unit and the assembler together, press "run", and a pile of gates computes Fibonacci numbers.

**Type:** Build
**Prerequisites:** Phase 16 (A Computer from Gates), Lessons 01-06
**Time:** ~80 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Integration | Joining separately built and tested parts into one working system | Assembling a car from an engine, a gearbox and a body that were each tested alone |
| Lockstep comparison | Running two models side by side and comparing their state after every step | Two people solving the same sum line by line and checking each line |
| Trace | A record of what the machine did, cycle by cycle or instruction by instruction | A flight recorder |
| Cycles per instruction (CPI) | The average number of clock cycles one instruction takes | Average number of steps a dancer needs per move |
| Instructions per second | How many instructions the machine completes each second: clock frequency / CPI | Moves per minute |
| Execution time | Total cycles times the clock period | How long the whole dance lasts |
| Benchmark | A program used to measure and compare performance | A standard test lap on a race track |
| Pipelining | Overlapping the steps of several instructions, like an assembly line | A car wash where the next car enters while the previous one is being dried |
| Cache | A small fast memory near the processor holding recently used data | A notepad on your desk instead of the filing cabinet down the hall |
| Bring-up | The first time a new machine is switched on and made to run | The first test drive |

## Learning Objectives

- Combine the gate-level ALU, the step counter, the datapath, the microcode and the memory into one working T8.
- Assemble programs with the assembler of Lesson 06 and run them on the hardware model.
- Verify the machine in lockstep against the reference model of Lesson 01, after every instruction.
- Read a cycle-by-cycle trace and connect each line to the microcode.
- Compute cycles per instruction, clock frequency from the critical path, and execution time.
- Explain what real processors add to this design (pipelining, caches, more registers) and why.

## The Problem

Six lessons have produced six parts: a reference model (Lesson 01), an ALU made of 122 gates (Lesson 02), a memory (Lesson 03), a datapath with a bus (Lesson 04), a microcoded control unit with a step counter (Lesson 05) and an assembler (Lesson 06). Each one was tested alone. That is necessary but not sufficient: the classic way for a hardware project to fail is that every part works and the whole does not, because two parts disagree about some detail (does `PC_INC` happen before or after the read? Do loads set the flags?).

This lesson integrates everything into one machine, runs real programs on it and checks it against the reference model **after every single instruction**. If the gates and the specification ever disagree, the check stops at the first instruction where they differ, which is exactly how professional processor verification is done. Then we ask how fast this machine would be on real hardware.

## The Physics

Nothing new physically: the T8 is a synchronous circuit with one clock. Its speed is set by the slowest path that must complete in one cycle. In the T8 that is: a register's clock-to-output delay, through the ALU's 22 gate levels (Lesson 02), onto the bus multiplexer, into a register's setup time (Phase 15, Lesson 07). Its power is mostly switching power (Phase 14, Lesson 05), spent every cycle by the clock and by the ALU, which recomputes every cycle even when no instruction uses it. Real machines measure exactly these things in the lab during **bring-up**: the maximum clock at which the chip still runs a test program correctly, and the current it draws.

## The Concept

### The whole machine

```
             +-------------------- control unit --------------------+
             |  step counter (gates) --T--> microcode(IR, T, Z, C)  |
             +----------------------------+--------------------------+
                                          | 15 control signals
   +--------------------------------------v-----------------------------------+
   |                               8-bit bus                                  |
   +----+--------+---------+--------+--------+--------+--------+--------------+
        |        |         |        |        |        |        |
      [PC]    [MAR]-->[ memory ]  [IR]      [A]      [B]     [OUT] --> outputs
                       256 bytes    |        |        |
                                    | op     v        v
                                    +----> [ ALU: 122 gates ] --> Z, C
```

Every cycle, the machine does the same three things:

1. Read the step number from the gate-level step counter.
2. Look up the control word for (IR, step, Z, C) in the microcode.
3. Apply it to the datapath at the clock edge: one source drives the bus, the selected registers load, the PC may count, the flags may load, memory may store. Then the step counter counts (or resets, if `END` was set).

### Reading a trace

The first 16 cycles of the multiply program (Lesson 06) on the integrated machine:

```
  cycle  1 T0  MAR_IN, PC_OUT                 bus=  0  PC=00 IR=00 A=  0
  cycle  2 T1  IR_IN, MEM_OUT, PC_INC         bus= 16  PC=01 IR=10 A=  0
  cycle  3 T2  MAR_IN, PC_OUT                 bus=  1  PC=01 IR=10 A=  0
  cycle  4 T3  A_IN, END, MEM_OUT, PC_INC     bus=  0  PC=02 IR=10 A=  0
  cycle  5 T0  MAR_IN, PC_OUT                 bus=  2  PC=02 IR=10 A=  0
  cycle  6 T1  IR_IN, MEM_OUT, PC_INC         bus= 18  PC=03 IR=12 A=  0
  cycle  7 T2  MAR_IN, PC_OUT                 bus=  3  PC=03 IR=12 A=  0
  cycle  8 T3  MAR_IN, MEM_OUT, PC_INC        bus=130  PC=04 IR=12 A=  0
  cycle  9 T4  A_OUT, END, MEM_IN             bus=  0  PC=04 IR=12 A=  0
  cycle 10 T0  MAR_IN, PC_OUT                 bus=  4  PC=04 IR=12 A=  0
  cycle 11 T1  IR_IN, MEM_OUT, PC_INC         bus= 17  PC=05 IR=11 A=  0
  cycle 12 T2  MAR_IN, PC_OUT                 bus=  5  PC=05 IR=11 A=  0
  cycle 13 T3  MAR_IN, MEM_OUT, PC_INC        bus=129  PC=06 IR=11 A=  0
  cycle 14 T4  A_IN, END, MEM_OUT             bus=  7  PC=06 IR=11 A=  7
  cycle 15 T0  MAR_IN, PC_OUT                 bus=  6  PC=06 IR=11 A=  7
  cycle 16 T1  IR_IN, MEM_OUT, PC_INC         bus= 43  PC=07 IR=2B A=  7
```

Translate it line by line:

- Cycles 1-4 are `LDI 0`: fetch (the bus carries opcode 16 = `0x10`), point at the operand, load it (0) into A, END.
- Cycles 5-9 are `STA result`: the opcode 18 = `0x12`, then the operand 130 = `0x82` (the address of `result`) goes into MAR, and in cycle 9 A drives the bus and memory stores it.
- Cycles 10-14 are `LDA y`: opcode 17 = `0x11`, address 129 = `0x81`, and in cycle 14 memory delivers 7 (the value of y), which A loads.
- Cycle 16 fetches opcode 43 = `0x2B`: `ORI 0`, the flag-setting trick of Lesson 06.

Every line matches the microcode table of Lesson 05. A trace like this is the main debugging tool of hardware designers, usually viewed as waveforms.

### Lockstep verification

For each program, the script runs the reference model of Lesson 01 one instruction at a time, and the T8 hardware model one instruction at a time (as many cycles as each instruction needs), and after every instruction compares the programmer-visible state: PC, A, Z and C. At the end it also compares the outputs and all 256 bytes of memory.

```
  countdown: output [5, 4, 3, 2, 1, 0]
             reference [5, 4, 3, 2, 1, 0]; same output: True; same final memory: True
             18 instructions, 70 clock cycles, 3.89 cycles per instruction
  multiply : output [42]
             reference [42]; same output: True; same final memory: True
             71 instructions, 342 clock cycles, 4.82 cycles per instruction
  fibonacci: output [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
             reference [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]; same output: True; same final memory: True
             131 instructions, 611 clock cycles, 4.66 cycles per instruction
```

220 instructions, about a thousand clock cycles, and the gate-level machine never disagrees with the specification. If it did, the check would raise an error naming the first instruction where the state differs, which is the most useful single fact when debugging hardware.

### Counting cycles by hand

Check the countdown's 70 cycles using the cycle counts of Lesson 05:

```
LDI 5                       1 x 4 =  4
OUT        (6 times)        6 x 3 = 18
SUBI 1     (5 times)        5 x 5 = 25
JNZ loop   (5 times)        5 x 4 = 20
HLT                         1 x 3 =  3
                            total   70 cycles
```

Instructions: `1 + 6 + 5 + 5 + 1 = 18`. Cycles per instruction: `CPI = 70 / 18 = 3.89`. The multiply program has a higher CPI (4.82) because it uses more 5- and 6-cycle memory instructions.

### How fast is it?

Say it as a sentence first: "execution time equals the number of instructions, times the cycles per instruction, times the clock period". In symbols:

```
time = instructions x CPI x T = cycles x T
```

The clock period must cover the critical path. The ALU alone is 22 gate delays (Lesson 02); add an allowance for the register's clock-to-Q and setup times, the bus multiplexer and the control unit (Phase 15, Lesson 07):

- **Built from 74HC chips on a breadboard:** `22 x 8 ns + 40 ns = 216 ns`, so `f = 4.6 MHz`. Fibonacci takes `611 x 216 ns = 132 us`.
- **Built on a modern chip:** `22 x 15 ps + 100 ps = 430 ps`, so `f = 2.3 GHz`. Fibonacci takes `611 x 0.43 ns = 0.26 us`.

The same 611 cycles; only the technology changed. To make the machine itself faster, there are exactly three knobs in the formula: fewer instructions (a richer instruction set, like a multiply instruction), fewer cycles per instruction (better microarchitecture), or a shorter clock period (a shorter critical path or faster transistors).

### What real processors add

The T8 is complete: it can, given enough memory and time, compute anything any computer can (Turing's universality, Lesson 01). Real processors add features for **speed** and **convenience**:

- **Pipelining.** While one instruction executes, the next is decoded and the one after is fetched, like an assembly line. The ideal CPI approaches 1. Phase 20, Lesson 05 cuts the critical path with pipeline registers.
- **Separate paths instead of one bus**, so several values move per cycle, and separate instruction and data memories (Harvard style) or caches, so the fetch does not compete with loads.
- **More registers.** With 16 or 32 registers, most values stay inside the processor and fewer loads and stores are needed.
- **A stack and call/return instructions**, so programs can be split into functions.
- **Hardware multipliers and shifters**, so `6 x 7` takes one instruction, not 71.
- **Interrupts**, so external events can pause the program (Phase 17, Lesson 05).
- **Caches** (Phase 20, Lesson 07), because main memory is roughly a hundred times slower than the processor.

A microcontroller in Phase 17 is a processor of this kind, with memory and input/output devices on the same chip. You now know what is inside it.

## Build It

The script `code/main.py` contains the whole machine. Every piece comes from an earlier lesson of this phase.

### Step 1: The parts

`build_alu` (Lesson 02) and `build_step_counter` (Lesson 05) are gate-level `sim.logic` circuits. `microcode(opcode, step, z, c)` is the table of Lesson 05. `assemble` is a compact version of the assembler of Lesson 06, and `reference_step` executes one instruction of the reference model of Lesson 01.

### Step 2: One clock cycle of the T8

```python
    def clock(self):
        step = self.step_number()
        signals = microcode(self.reg["IR"], step, self.reg["Z"], self.reg["C"])
        drivers = [s for s in SOURCES if s in signals]
        assert len(drivers) <= 1, f"bus conflict {drivers}"
        result, z, c = self.alu_outputs()
        bus = {"PC_OUT": self.reg["PC"], "MEM_OUT": self.mem[self.reg["MAR"]], "A_OUT": self.reg["A"], "ALU_OUT": result}.get(drivers[0] if drivers else None, 0)
        new = dict(self.reg)
        for name, reg in [("MAR_IN", "MAR"), ("IR_IN", "IR"), ("A_IN", "A"), ("B_IN", "B"), ("OUT_IN", "OUT"), ("PC_IN", "PC")]:
            if name in signals:
                new[reg] = bus
        if "PC_INC" in signals:
            new["PC"] = (self.reg["PC"] + 1) & 0xFF
        if "FLAGS_IN" in signals:
            new["Z"], new["C"] = z, c
        if "MEM_IN" in signals:
            self.mem[self.reg["MAR"]] = bus
        if "OUT_IN" in signals:
            self.outputs.append(bus)
        self.reg = new
        self.cycles += 1
        if "HALT" in signals:
            self.halted = True
        self.counter.step({"end": int("END" in signals)})
        if "END" in signals or "HALT" in signals:
            self.instructions += 1
        return step, signals, bus
```

This is Lesson 04's `Datapath.clock`, with the control word now coming from the microcode instead of from a hand-written list, and the step counter advancing at the same edge.

### Step 3: One instruction

```python
    def run_instruction(self):
        while True:
            step, signals, _ = self.clock()
            if "END" in signals or "HALT" in signals:
                return
```

### Step 4: Lockstep

```python
def lockstep(memory, limit=5000):
    machine = T8(memory)
    ref_mem = list(memory)
    state = (0, 0, 0, 0)
    ref_out = []
    for _ in range(limit):
        state, out, halted = reference_step(state, ref_mem)
        if out is not None:
            ref_out.append(out)
        machine.run_instruction()
        mine = (machine.reg["PC"], machine.reg["A"], machine.reg["Z"], machine.reg["C"])
        if not halted and mine != state:
            raise AssertionError(f"mismatch after instruction {machine.instructions}: {mine} vs {state}")
        if halted:
            break
    return machine, ref_out, ref_mem
```

### Step 5: Programs and timing

The three programs are stored as assembly text in `PROGRAMS`. The script assembles each one, runs it in lockstep, prints the outputs, cycles and CPI, and finally converts the Fibonacci cycle count into time for two technologies using the ALU's depth.

Run it:

```bash
uv run python phases/16-a-computer-from-gates/07-running-a-program/code/main.py
```

## Use It

- **Processor verification** in industry is lockstep comparison at scale: the hardware design (in simulation, in an FPGA, or the real chip) runs millions of random and directed programs, and every instruction's result is compared with an instruction set simulator.
- **Breadboard and FPGA computers**: building a small computer like the T8 from 74HC chips, or in an FPGA with a hardware description language, is a classic university lab and hobby project.
- **Benchmarks** such as CoreMark (for microcontrollers) and SPEC (for servers) measure the instructions x CPI x period product on standard programs.
- **Performance counters**: modern processors count cycles and instructions in hardware registers; tools like `perf` on Linux read them and report instructions per cycle (IPC = 1 / CPI). A good desktop core reaches an IPC of 2-4 on ordinary code.
- **Microcontrollers** (Phase 17) such as the AVR in an Arduino Uno execute most instructions in 1-2 cycles at 16 MHz, about 100 times faster per clock than the T8, thanks to pipelining, 32 registers and a separate program memory.

## Try It in the Lab

This lesson has no lab task. The lab of this phase is the script itself: write a new program in `PROGRAMS`, run it on the T8 and watch the lockstep check confirm that the gates agree with the specification.

## Common Mistakes

- **Testing parts only in isolation.** Integration bugs come from disagreements between parts. Always test the whole machine against the specification.
- **Comparing only the final output.** A program can produce the right output for the wrong reason. Lockstep comparison after every instruction finds the first divergence.
- **Forgetting the fetch cycles when counting time.** Every instruction pays 2 cycles of fetch on the T8. A NOP is not free.
- **Confusing clock frequency with speed.** A 100 MHz processor with CPI 1 beats a 300 MHz processor with CPI 5 on the same instructions.
- **Ignoring the instruction count.** A machine with a multiply instruction can run a program in a tenth of the instructions; the instruction set matters as much as the hardware.

## Exercises

1. Using the cycle counts of Lesson 05, compute by hand the 342 cycles of the multiply program. (Hint: count each instruction type in the 71 executed instructions.)
2. Write a T8 program that adds the numbers 1 to 10, add it to `PROGRAMS`, and run it. How many cycles and what CPI do you get? Is the CPI higher or lower than for Fibonacci, and why?
3. Suppose a pipelined T8 achieved a CPI of 1.2 with a 30 % longer clock period. Would the Fibonacci program run faster or slower than now? By what factor?
4. Introduce a deliberate bug: in `microcode`, remove `PC_INC` from the not-taken conditional jump. Run the script. At which instruction does the lockstep check fail, and what does the error message tell you?
5. A multiply instruction `MUL a` (A = A x mem[a], low 8 bits) would need a hardware multiplier. If it took 8 cycles, how many cycles would the multiply program need for 6 x 7? Compare with 342.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Integration | "Putting it all together" | Connecting separately verified blocks and verifying the whole system |
| Lockstep verification | "Co-simulation" | Running the design and a reference model together and comparing state after every step |
| Trace | "Waveform", "log" | A cycle-by-cycle record of control signals, bus values and registers |
| CPI | "Cycles per instruction" | Total cycles / instructions executed; IPC is its inverse |
| Execution time | "Run time" | instructions x CPI x clock period |
| Critical path | "The slow path" | The longest register-to-register delay; sets the minimum clock period |
| Pipelining | "Instruction overlap" | Splitting instruction execution into stages that work on different instructions at once |
| Bring-up | "First silicon" | The first runs of a new machine, finding its maximum working speed and its bugs |

## Further Reading

- David A. Patterson and John L. Hennessy, *Computer Organization and Design*, Chapter 1 (the performance equation) and Chapter 4 (the processor, including pipelining).
- Noam Nisan and Shimon Schocken, *The Elements of Computing Systems* (Nand2Tetris), Chapter 5 (Computer Architecture), where the Hack computer is assembled from its parts and tested with programs.
- Albert Paul Malvino and Jerald A. Brown, *Digital Computer Electronics*, for the complete SAP-1 to SAP-3 bus computers, the textbook ancestors of breadboard designs.
- Ben Eater, "Building an 8-bit breadboard computer" (YouTube), the full series ending with the computer running programs, for a real-chip version of this lesson.
