# Instructions and Assembly

> Machine code is numbers for the machine; assembly language is the same numbers with names for people, and an assembler is the small program that translates one into the other.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lesson 02 (Binary Numbers), Phase 16 (A Computer from Gates), Lessons 01 and 05 (What a Computer Is, The Control Unit)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Instruction set architecture (ISA) | The full list of instructions a processor understands, with their encodings and effects | The vocabulary and grammar of a language |
| Machine code | A program as the raw bytes the processor executes | A message in Morse code |
| Assembly language | Machine code written with readable names (mnemonics) and labels | The same message written in letters |
| Mnemonic | The short name of an instruction, such as `LDA` | An abbreviation like "Rd." for "Road" |
| Assembler | A program that turns assembly text into machine code | A translator |
| Label | A name for an address, written `name:` | A bookmark with a title |
| Directive | A line that tells the assembler something rather than producing an instruction (`.org`, `.byte`) | A note to the typesetter, not part of the text |
| Two-pass assembly | Reading the program twice: first to find label addresses, then to produce bytes | Numbering the pages of a book before writing its index |
| Listing | A printout showing each address, its bytes and the source line | A bilingual edition with both languages side by side |
| Disassembler | A program that turns machine code back into assembly | A translator working in the other direction |
| Addressing mode | How an instruction finds its operand: immediate (the number itself) or direct (an address) | "Take 5 apples" versus "take the apples in box 5" |
| Encoding | The bit pattern chosen for each instruction | The spelling of each word |

## Learning Objectives

- Read and write T8 assembly language with mnemonics, labels, comments and directives.
- Explain immediate and direct addressing and the opcode bit fields of the T8.
- Build a two-pass assembler in Python that resolves labels and reports errors.
- Build a disassembler and use it to check the assembler.
- Write and run two real programs: multiplication by repeated addition and the Fibonacci sequence.

## The Problem

In Lesson 01 we wrote programs as bytes: `11 10 20 11 01 0F`. That works for 6 bytes, but imagine a 100-byte program. Every jump target is an absolute address; insert one instruction near the top, and every jump below it points to the wrong place. One wrong digit and the program executes data. This is how the first programmers worked, toggling binary into front-panel switches, and it was miserable.

The fix, invented in the late 1940s, was to let the computer do the bookkeeping. Write `LDA x` instead of `11 80`, `loop:` instead of remembering that the loop starts at `0x04`, and let a program, the **assembler**, translate it. This lesson writes an assembler for the T8. It is our first piece of real systems software: a program whose job is to make other programs.

## The Physics

There is no new physics in an assembler; it is software. But the encoding it produces is a hardware decision, and a good one saves gates. Lesson 05 showed that because the low 3 bits of every T8 ALU opcode are the ALU operation, five instructions share one microcode routine and the ALU needs no decoder of its own. Real instruction sets are full of such choices: RISC-V puts the register numbers in the same bit positions in every instruction format, so the register file can be read before the instruction is even fully decoded. The ISA is the contract between the hardware designers and the software writers, and it is designed for both.

## The Concept

### The T8 instruction set, as a programmer sees it

```
mnemonic   operand   encoding  effect                         flags
NOP        -         00        nothing                        -
OUT        -         01        OUT = A                        -
HLT        -         0F        stop                           -
LDI        n         10 n      A = n                          -
LDA        a         11 a      A = mem[a]                     -
STA        a         12 a      mem[a] = A                     -
ADD        a         20 a      A = A + mem[a]                 Z, C
SUB        a         21 a      A = A - mem[a]                 Z, C (C = no borrow)
AND        a         22 a      A = A AND mem[a]               Z (C = 0)
OR         a         23 a      A = A OR mem[a]                Z (C = 0)
XOR        a         24 a      A = A XOR mem[a]               Z (C = 0)
ADDI..XORI n         28-2C n   the same with the number n     as above
JMP        a         30 a      PC = a                         -
JZ / JNZ   a         31 / 32   PC = a if Z = 1 / Z = 0        -
JC / JNC   a         33 / 34   PC = a if C = 1 / C = 0        -
```

The opcode's bit fields, for the ALU group:

```
  bit:  7 6 5 4 | 3 | 2 1 0
        0 0 1 0 | i | op        i = 1: operand is a number (immediate)
        group 2 |   | ALU op    i = 0: operand is an address (direct)
```

So `ADD` is `0010 0 000` = `0x20`, `SUBI` is `0010 1 001` = `0x29`, and `XOR` is `0010 0 100` = `0x24`.

### Two addressing modes

The same arithmetic can take its operand in two ways:

- **Immediate:** the operand byte **is** the value. `ADDI 5` adds 5. Good for constants.
- **Direct:** the operand byte is an **address**, and the value is read from memory there. `ADD 0x80` adds whatever is stored at `0x80`. Good for variables.

`LDI` and `LDA` are the same pair for loading. The jumps take an address, the place to go. Real processors have many more modes (register, indirect, indexed, relative), which let programs walk through arrays and call functions; the T8 keeps just these two.

### Assembly language syntax

Our assembler accepts lines of this shape:

```
label:  MNEMONIC operand   ; comment
```

- Everything after `;` is a comment and is ignored.
- A **label** is a name followed by `:`. It stands for the address where that line's bytes start.
- An operand is a number (`5`, `0x80`, `0b1010`) or a label.
- **Directives** start with a dot: `.org 0x80` moves the current address (where the next bytes go), and `.byte 6` places a raw data byte.

### Two passes

The difficulty is **forward references**. In

```
        JZ done
        ...
done:   LDA result
```

the `JZ` needs the address of `done` before the assembler has reached `done`. The classic solution is to read the program twice:

1. **First pass.** Walk through the lines, keeping a running address. Do not produce bytes; just add each line's size (0 for `.org`, 1 for `NOP`/`OUT`/`HLT`, 2 for others, n for `.byte` with n values) and record each label's address in a **symbol table**.
2. **Second pass.** Walk through again, now producing bytes: look up the opcode for each mnemonic, and turn each operand into a byte, looking labels up in the symbol table.

The first pass works because the **size** of every instruction is known from its mnemonic alone, without knowing the value of its operand. That is one more reason simple instruction sets have fixed, predictable sizes.

### A program: multiplication

The T8 has no multiply instruction. Multiplying `x` by `y` means adding `x` to a running total `y` times:

```
; result = x * y by repeated addition
        LDI 0
        STA result
loop:   LDA y          ; any multiplications left?
        ORI 0          ; set Z from A (loads do not set flags)
        JZ done
        SUBI 1
        STA y
        LDA result
        ADD x
        STA result
        JMP loop
done:   LDA result
        OUT
        HLT

        .org 0x80
x:      .byte 6
y:      .byte 7
result: .byte 0
```

Read it in words: set the result to 0. Then repeat: if `y` is zero, stop; otherwise decrease `y`, and add `x` to the result. Notice the `ORI 0` trick. On the T8 only ALU instructions update the flags (Lesson 01), so after `LDA y` the Z flag still describes an older result. OR-ing with 0 leaves A unchanged but sets Z according to A. Real programmers learn these idioms for every processor.

The assembler's listing:

```
  00: 10 00     LDI 0
  02: 12 82     STA result
  04: 11 81     loop: LDA y
  06: 2B 00     ORI 0
  08: 31 16     JZ done
  0A: 29 01     SUBI 1
  0C: 12 81     STA y
  0E: 11 82     LDA result
  10: 20 80     ADD x
  12: 12 82     STA result
  14: 30 04     JMP loop
  16: 11 82     done: LDA result
  18: 01        OUT
  19: 0F        HLT
  80: 06        x: .byte 6
  81: 07        y: .byte 7
  82: 00        result: .byte 0
  labels: loop=0x04, done=0x16, x=0x80, y=0x81, result=0x82
```

Check a few bytes by hand. `STA result`: STA is `0x12`, and `result` is at `0x82`, so `12 82`. `JZ done`: JZ is `0x31` and `done` is at `0x16`, so `31 16`, a forward reference resolved by the first pass. `JMP loop`: `30 04`, a backward reference. Running it on the reference model of Lesson 01 gives the output `[42]` after 71 instructions: 6 x 7 = 42.

Count the instructions to see the cost of multiplying in software: 2 at the start, then 9 per pass of the loop (7 passes), then a final pass that exits after 3, then 3 at the end: `2 + 7 x 9 + 3 + 3 = 71`. The time grows with `y`: 6 x 200 would take over 1,800 instructions. That is why real processors have multiplier hardware (Phase 20, Lesson 02).

### A program: Fibonacci

The Fibonacci sequence starts 0, 1, and each number is the sum of the previous two: 0, 1, 1, 2, 3, 5, 8, ... This program prints them until the next one would not fit in 8 bits, using the carry flag to detect the overflow:

```
        LDI 0
        STA a
        LDI 1
        STA b
loop:   LDA a
        OUT
        ADD b          ; A = a + b, C = 1 if it overflowed
        JC last
        STA next
        LDA b
        STA a
        LDA next
        STA b
        JMP loop
last:   LDA b
        OUT
        HLT
```

Output: `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]`. When `a = 144` and `b = 233`, the sum 377 does not fit in a byte, the ALU sets C (Lesson 02), the program jumps to `last`, prints 233 and stops. Using the carry flag this way is how 8-bit processors built 16- and 32-bit arithmetic: add the low bytes, then add the high bytes plus the carry.

### Errors the assembler catches

An assembler is also the first line of defence against typing mistakes:

```
  line 1: undefined label or bad number 'nowhere'
  line 1: 300 does not fit in one byte
  line 1: unknown instruction 'MUL'
  line 2: label 'x' defined twice
```

It cannot catch logic errors (a loop that never ends, a wrong address) but it catches everything that is not valid T8 code.

### Disassembly

A **disassembler** reads bytes and prints mnemonics: the reverse of assembly. It needs to know where instructions start, because the same byte can be an opcode or an operand. Starting at address 0 and stepping by each instruction's size, it reproduces the program (with numbers instead of label names, which are lost in machine code):

```
  00: LDI 0x00
  02: STA 0x82
  04: LDA 0x81
  06: ORI 0x00
  08: JZ 0x16
  0A: SUBI 0x01
```

Debuggers use disassemblers to show what a processor is executing.

## Build It

The script `code/main.py` is a complete T8 assembler, disassembler and (to test the programs) the reference model of Lesson 01.

### Step 1: Parse lines

```python
def parse(source):
    lines = []
    for number, raw in enumerate(source.splitlines(), start=1):
        text = raw.split(";")[0].strip()
        if not text:
            continue
        label = None
        if ":" in text:
            label, text = (part.strip() for part in text.split(":", 1))
        words = text.replace(",", " ").split()
        lines.append((number, label, words))
    return lines
```

Each line becomes (line number, label or `None`, list of words). Comments and blank lines disappear.

### Step 2: Sizes and values

```python
def size_of(words, number):
    if not words:
        return 0
    head = words[0].upper()
    if head == ".BYTE":
        return len(words) - 1
    if head == ".ORG":
        return 0
    if head not in OPCODES:
        raise AssemblyError(f"line {number}: unknown instruction {words[0]!r}")
    return 1 if head in ONE_BYTE else 2


def value_of(token, labels, number):
    if token in labels:
        return labels[token]
    try:
        value = int(token, 0)
    except ValueError:
        raise AssemblyError(f"line {number}: undefined label or bad number {token!r}") from None
    if not 0 <= value <= 255:
        raise AssemblyError(f"line {number}: {value} does not fit in one byte")
    return value
```

`int(token, 0)` understands decimal, `0x..` hex and `0b..` binary.

### Step 3: Two passes

```python
def assemble(source):
    lines = parse(source)
    labels, address = {}, 0
    for number, label, words in lines:
        if words and words[0].upper() == ".ORG":
            address = int(words[1], 0)
        if label:
            if label in labels:
                raise AssemblyError(f"line {number}: label {label!r} defined twice")
            labels[label] = address
        address += size_of(words, number)
```

That is the first pass: only addresses. The second pass (in the script) walks the same lines, writes `OPCODES[head]` and the operand value into a 256-byte memory image, and records each line for the listing.

### Step 4: Run the programs

The `run` function is the reference model from Lesson 01, slightly compacted. The assembled memory image goes straight into it.

Run it:

```bash
uv run python phases/16-a-computer-from-gates/06-instructions-and-assembly/code/main.py
```

## Use It

- **Every processor family has an assembler**: GNU `as` for x86, ARM and RISC-V; `avr-as` for the AVR microcontrollers of Phase 17. Compilers for C and other languages usually generate assembly text and hand it to the assembler.
- **Startup code** of microcontrollers (the first instructions after reset: set up the stack, copy initial data to RAM) is often written in assembly.
- **Reverse engineering and security**: disassemblers such as objdump, Ghidra and IDA turn machine code back into assembly to analyse malware or old software.
- **Retro computing**: 6502 and Z80 assemblers are still used to write games for the Commodore 64, NES and ZX Spectrum, whose processors are close cousins of the T8.
- **Instruction set design**: the RISC-V specification is a public document listing every instruction's encoding and meaning, exactly like the table above but with about 50 base instructions.

## Try It in the Lab

This lesson has no lab task. Write your own T8 programs in the script, assemble them and run them on the reference model; in Lesson 07 they will run on the gate-level machine.

## Common Mistakes

- **Using `LDA` when you meant `LDI`.** `LDA 5` loads the byte at address 5; `LDI 5` loads the number 5.
- **Testing flags after a load.** Loads do not set Z or C on the T8. Use an ALU operation such as `ORI 0` first.
- **Putting data where the program runs.** Without `.org` (or a `HLT` and a jump around it), data placed after the code may be executed. Keep code and data apart.
- **Forgetting that operands are one byte.** Numbers above 255 do not fit; the assembler reports them.
- **Off-by-one loop counts.** Decide whether the loop tests before or after the body, and trace the first and last pass by hand.

## Exercises

1. Hand-assemble: `LDI 0x20`, `ADDI 3`, `STA 0x90`, `JNZ 0x00`, `HLT`. Write the bytes and the address of each instruction.
2. Disassemble by hand the bytes `10 0A 29 03 33 02 0F` starting at address 0. What does this program compute, and when does it stop? (Careful: what does C mean after SUBI?)
3. Write a T8 program that outputs the numbers 10, 9, ..., 1 and halts. Assemble it with the script and run it.
4. Write a T8 program that computes the sum 1 + 2 + ... + 10 and outputs it. How many instructions does it execute?
5. Extend the assembler with a directive `.word` that stores a 16-bit number as two bytes (low byte first). Then write a T8 program that adds two 16-bit numbers stored with `.word`, using `ADD` for the low bytes, `JNC` to skip an `ADDI 1` on the high byte, and `ADD` for the high bytes.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| ISA | "Instruction set" | The contract between hardware and software: instructions, encodings, registers, flags |
| Machine code | "Binary", "object code" | The bytes the processor actually fetches and executes |
| Assembly language | "Assembler", "asm" | One line per instruction, with mnemonics and labels for readability |
| Mnemonic | "Op name" | The readable name of an opcode, such as `ADDI` |
| Label | "Symbol" | A name that stands for an address, resolved by the assembler |
| Directive | "Pseudo-op" | An assembler command such as `.org` or `.byte` that does not become an instruction |
| Two-pass assembler | "Classic assembler" | First pass collects label addresses, second pass emits bytes |
| Immediate / direct | "Addressing modes" | Operand is the value itself / operand is the address of the value |

## Further Reading

- Noam Nisan and Shimon Schocken, *The Elements of Computing Systems* (Nand2Tetris), Chapter 6 (Assembler), which builds an assembler for the Hack computer.
- David A. Patterson and Andrew Waterman, *The RISC-V Reader: An Open Architecture Atlas*, for a real, modern instruction set and its encodings.
- Andrew S. Tanenbaum and Todd Austin, *Structured Computer Organization*, the chapters on the instruction set architecture level and assembly language.
- Kathleen Booth's 1947 work on "contracted notation" for the ARC computers at Birkbeck College, often credited as the first assembly language.
