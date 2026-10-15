# The ALU

> The arithmetic logic unit computes every possible answer at once and a multiplexer keeps the one the instruction asked for.

**Type:** Build
**Prerequisites:** Phase 14 (Digital Logic), Lesson 07 (Adders) and Lesson 08 (Multiplexers and Decoders), Phase 16 (A Computer from Gates), Lesson 01 (What a Computer Is)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| ALU | Arithmetic logic unit: the combinational circuit that does a processor's calculations | A pocket calculator without memory |
| Operation code (ALU op) | The bits that tell the ALU which operation to perform | The button you press on the calculator |
| Operand | One of the numbers the ALU works on (A and B) | The numbers you type in |
| Bit slice | The part of the ALU that handles one bit position; the whole ALU is n identical slices | One column of school arithmetic |
| Bitwise operation | AND, OR, XOR applied to each pair of bits separately, with no carries | Comparing two rows of switches position by position |
| Result multiplexer | The selector that keeps the result of the chosen operation | A channel switch picking one of several TV signals |
| Flag | A one-bit output describing the result: zero, carry, negative | Warning lights on a dashboard |
| Zero flag (Z) | 1 when all result bits are 0 | "Tank empty" light |
| Carry flag (C) | The carry out of the top bit of an addition (or "no borrow" for a subtraction) | The odometer rolling over |
| Negative flag (N) | A copy of the top bit of the result: 1 when the result is negative in two's complement | A minus sign on a display |
| Mask | A pattern used with AND, OR or XOR to clear, set or flip chosen bits | A stencil that lets paint through only in certain places |

## Learning Objectives

- Explain how an ALU computes several operations in parallel and selects one with a decoder and a multiplexer.
- Build the T8's 8-bit ALU (ADD, SUB, AND, OR, XOR) gate by gate in `sim.logic`.
- Generate the Z, C and N flags from the result and the carry chain.
- Verify the gate-level ALU against the reference model of Lesson 01 on edge cases and random operands.
- Use bitwise operations with masks to clear, set and flip bits.
- Find the ALU's critical path and relate it to the maximum clock speed of the computer.

## The Problem

Lesson 01's reference model computed `acc + b` with one line of Python. In hardware there is no `+`: there are gates. The T8 needs a circuit that takes two 8-bit numbers and three operation bits from the instruction, and within one clock cycle produces the right 8-bit result and the flags that conditional jumps depend on.

You already have the pieces: the adder/subtractor of Phase 14, Lesson 07 and the multiplexer and decoder of Phase 14, Lesson 08. This lesson puts them together into an ALU and checks it, bit for bit, against the reference model. It also shows where the computer's speed limit comes from: the ALU is almost always the slowest part of a simple processor, and its slowest part is the carry chain.

## The Physics

Physically, the ALU is pure combinational logic: about 120 gates for the T8. When its inputs change, a wave of transitions runs through it, and after the critical-path delay the outputs are valid. Every operation's circuit is powered and switching all the time, even the ones whose result is thrown away by the multiplexer; that wastes some energy (Phase 14, Lesson 05), but it costs no time, because all results are computed in parallel. Real processors sometimes block the inputs of unused units ("operand isolation") to save that power.

## The Concept

### Compute everything, keep one

The simplest way to build a multi-function ALU is not to build a clever circuit that "becomes" an adder or an AND gate on command. It is to build all the operations side by side, feed them the same inputs, and put a multiplexer at the end:

```
             A (8 bits)    B (8 bits)
               |  |           |  |
        +------+--+-----------+--+------+
        |      |  |           |  |      |
     [ADD/SUB] [AND]        [OR]     [XOR]
        |        |            |         |
        +--------+-----+------+---------+
                       |
              [ result multiplexer ] <--- decoded from op2 op1 op0
                       |
                  R (8 bits) ---> [ flag logic ] ---> Z, C, N
```

The T8's ALU operation code is 3 bits, taken straight from the low bits of the opcode (Lesson 01):

```
op2 op1 op0   operation    result
  0   0   0   ADD          A + B
  0   0   1   SUB          A - B
  0   1   0   AND          A AND B (bit by bit)
  0   1   1   OR           A OR B
  1   0   0   XOR          A XOR B
```

### Decoding the operation

A small decoder (Phase 14, Lesson 08) turns the 3 operation bits into one-hot select lines:

```
is_arith = op2'·op1'        ADD or SUB (both use the adder)
sub      = op2'·op1'·op0    SUB only
is_and   = op2'·op1·op0'
is_or    = op2'·op1·op0
is_xor   = op2·op1'·op0'
```

Notice `is_arith` covers two codes: ADD and SUB share the adder, and `sub` only changes how the adder is used.

### The arithmetic part: the adder/subtractor

Exactly the circuit of Phase 14, Lesson 07: each B bit passes through an XOR with `sub` (inverting it for subtraction), the carry into bit 0 is `sub` (the "+1" of two's complement), and 8 full adders ripple the carry from bit 0 to bit 7.

```
for each bit i:
  bx_i = b_i XOR sub
  p_i  = a_i XOR bx_i          (propagate)
  s_i  = p_i XOR c_i           (sum)
  g_i  = a_i AND bx_i          (generate)
  c_(i+1) = g_i OR (p_i AND c_i)
with c_0 = sub
```

### The logic part: bitwise operations

AND, OR and XOR on 8-bit numbers simply apply the gate to each bit position separately. No carries, no interaction between columns:

```
      1100 1100   (204)
  AND 1010 1010   (170)
      ---------
      1000 1000   (136)       1 only where both have 1

      1100 1100
  OR  1010 1010
      ---------
      1110 1110   (238)       1 where either has 1

      1100 1100
  XOR 1010 1010
      ---------
      0110 0110   (102)       1 where they differ
```

One gate per bit per operation: 8 AND, 8 OR and 8 XOR gates.

### The result multiplexer

For each bit i, the result is an AND-OR multiplexer driven by the one-hot select lines (Phase 14, Lesson 08):

```
r_i = is_arith·s_i + is_and·and_i + is_or·or_i + is_xor·xor_i
```

At most one select line is 1, so exactly one candidate passes. (If the operation code is 5, 6 or 7, none is selected and the result is 0. The T8 never uses those codes.)

### The flags

The flags summarise the result for the conditional jumps:

- **Z (zero):** 1 when every result bit is 0. "None of the bits is 1" is a NOR of all eight: `Z = NOR(r0, ..., r7)`.
- **C (carry):** the carry out of bit 7, but only for arithmetic: `C = c8·is_arith`. For ADD it means unsigned overflow; for SUB it means "no borrow", that is `A >= B` as unsigned numbers (Phase 14, Lesson 07). For logic operations C is 0.
- **N (negative):** simply `r7`, the sign bit in two's complement. The T8's jumps do not use it yet, but it costs nothing (a wire), so the ALU provides it.

Worked examples from the simulator:

```
ADD  25, 17   -> 42,  Z=0 C=0 N=0
ADD 200,100   -> 44,  Z=0 C=1 N=0     300 does not fit: carry
SUB  25, 17   ->  8,  Z=0 C=1 N=0     25 >= 17: no borrow
SUB  17, 25   -> 248, Z=0 C=0 N=1     borrow; 248 is -8 in two's complement
SUB  42, 42   ->  0,  Z=1 C=1 N=0     equal: zero, and no borrow
```

Look at the last two lines: one subtraction tells you everything about how two numbers compare. `Z = 1` means equal; `C = 1` means `A >= B`; `C = 0` means `A < B`. That is how processors implement `if a < b`: subtract and test the flags.

### Masks: what the logic operations are for

Bitwise operations look abstract until you need to work with individual bits, which hardware programmers do all the time (every microcontroller register in Phase 17 is a set of control bits):

- **Clear bits with AND.** `A AND 0000 1111` keeps the low 4 bits and clears the high 4. The pattern `0000 1111` is the mask.
- **Set bits with OR.** `A OR 1000 0000` forces bit 7 to 1 and leaves the others.
- **Flip bits with XOR.** `A XOR 0000 0001` flips bit 0 only. `A XOR 1111 1111` flips all bits (the "invert" of two's complement).
- **Test bits with AND.** `A AND 0000 0100` is zero (Z = 1) exactly when bit 2 of A is 0.

### Cost and speed

The simulator counts 122 gates: 3 NOT, 62 AND, 32 XOR, 24 OR, one NOR (for Z) and a buffer (for N). Most are in the 8 slices: per bit, the adder takes 5 gates plus the B-inverting XOR, the logic operations 3, and the multiplexer 5 (4 ANDs and a 4-input OR).

The critical path is 22 gate delays: from the operation bits through the decoder (`sub`), into the first adder's carry, along the whole 8-bit carry chain, into the last sum, through the multiplexer, and finally into the Z NOR. With modern 15 ps gates that is 330 ps; with 74HC chips at about 8 ns per gate, 176 ns, which would limit a breadboard T8 to about 5 MHz. The ALU is the T8's critical path, and its critical path is the carry chain. That is why real processors spend so many gates on carry-lookahead adders.

## Build It

The script `code/main.py` builds the ALU in `sim.logic` and checks it against the reference model.

### Step 1: Decode the operation

```python
lc.not_("nop2", "op2")
lc.not_("nop1", "op1")
lc.not_("nop0", "op0")
lc.and_("is_arith", "nop2", "nop1")
lc.and_("sub", "nop2", "nop1", "op0")
lc.and_("is_and", "nop2", "op1", "nop0")
lc.and_("is_or", "nop2", "op1", "op0")
lc.and_("is_xor", "op2", "nop1", "nop0")
```

### Step 2: The eight slices

Each pass of the loop builds one bit: the adder/subtractor stage, the three logic gates, and the four-way multiplexer.

```python
carry = "sub"
for i in range(BITS):
    lc.xor(f"bx{i}", b[i], "sub")
    lc.xor(f"p{i}", a[i], f"bx{i}")
    lc.xor(f"s{i}", f"p{i}", carry)
    lc.and_(f"g{i}", a[i], f"bx{i}")
    lc.and_(f"t{i}", f"p{i}", carry)
    lc.or_(f"c{i + 1}", f"g{i}", f"t{i}")
    carry = f"c{i + 1}"
    lc.and_(f"and{i}", a[i], b[i])
    lc.or_(f"or{i}", a[i], b[i])
    lc.xor(f"xor{i}", a[i], b[i])
    lc.and_(f"m_s{i}", f"s{i}", "is_arith")
    lc.and_(f"m_and{i}", f"and{i}", "is_and")
    lc.and_(f"m_or{i}", f"or{i}", "is_or")
    lc.and_(f"m_xor{i}", f"xor{i}", "is_xor")
    lc.or_(f"r{i}", f"m_s{i}", f"m_and{i}", f"m_or{i}", f"m_xor{i}")
```

### Step 3: The flags

```python
lc.and_("C", f"c{BITS}", "is_arith")
lc.nor("Z", *[f"r{i}" for i in range(BITS)])
lc.gate("buf", ["r7"], "N")
```

### Step 4: Drive it with numbers

```python
def apply(alu, op, a, b):
    inputs = {f"a{i}": (a >> i) & 1 for i in range(BITS)}
    inputs.update({f"b{i}": (b >> i) & 1 for i in range(BITS)})
    inputs.update({"op2": (op >> 2) & 1, "op1": (op >> 1) & 1, "op0": op & 1})
    out = alu.evaluate(inputs)
    result = sum(out[f"r{i}"] << i for i in range(BITS))
    return result, out["Z"], out["C"], out["N"]
```

### Step 5: Verify against the reference model

The reference `reference_alu` is copied unchanged from Lesson 01. The test uses every pair of "edge" values (0, 1, 127, 128, 254, 255), where carries and sign changes happen, plus 300 random pairs, for each of the 5 operations, and compares result, Z, C and N:

```
  1680 cases (5 operations x 336 operand pairs): 0 wrong
```

Edge values matter: an error in the carry into bit 7 shows up at 127 + 1 or 128 + 128 and nowhere near 25 + 17.

Run it:

```bash
uv run python phases/16-a-computer-from-gates/02-the-alu/code/main.py
```

## Use It

- **74LS181 / 74HC181** was the famous 4-bit ALU chip of the 1970s: 16 logic and 16 arithmetic functions selected by 5 pins, with lookahead carry outputs. Several 1970s minicomputers (including some DEC PDP-11 models) used a few of them side by side.
- **Real processors** have wider ALUs (32 or 64 bits) with more operations: shifts and rotates (a barrel shifter, built from multiplexers), compare, multiply (Phase 20, Lesson 02) and often several ALUs working in parallel.
- **Flags** appear in almost every instruction set: x86 has ZF, CF, SF and OF; ARM has N, Z, C, V. RISC-V deliberately has no flags and compares inside the branch instruction instead.
- **Bit masks** are how firmware sets one control bit without disturbing its neighbours: `PORTB |= (1 << 5)` in C compiles to an OR with the mask `0010 0000`.
- **Critical path.** Processor designers often quote "FO4 delays" (the delay of an inverter driving four copies of itself) per pipeline stage; a fast ALU stage is around 10-20 FO4.

## Try It in the Lab

The lab task "One bit of an ALU" builds a 2-operation slice: `y = a AND b` when `op = 0` and `y = a XOR b` when `op = 1`. The inverter `nop`, the gate that lets the XOR result through when `op = 1`, and the final OR are already placed. Fill three slots: the two candidate results from `a` and `b`, and the gate that lets the first candidate through only while `op = 0`. Parts: AND, OR, XOR, NAND.

Think about: this is a tiny version of the "compute everything, keep one" design. Which slot computes which candidate? What does the gate fed by `x1` and `nop` have to do?

## Common Mistakes

- **Forgetting that the carry flag means "no borrow" after a subtraction.** `SUB 25, 17` gives `C = 1`; `SUB 17, 25` gives `C = 0`. Some processors (x86) store the inverse, "borrow", in their carry flag; check the manual.
- **Setting C for logic operations.** The carry chain still runs during an AND, but its carry out is meaningless; the T8 masks it with `is_arith`.
- **Testing a flag that the instruction does not set.** On the T8 only ALU instructions update the flags (Lesson 01).
- **Assuming the ALU is slow only for big numbers.** The delay is set by the worst case of the circuit, not by the values: every operation must wait for the full critical path because the clock period is fixed.
- **Checking only easy cases.** Errors in adders hide in carries across bit 7 and sign changes. Always test the edge values 0, 1, 127, 128, 255.

## Exercises

1. Compute by hand, with flags: `ADD 127, 1`, `SUB 0, 1`, `AND 0xF0, 0x3C`, `XOR 0xFF, 0x5A`.
2. Using only T8 ALU operations with a mask, write how to (a) clear the low nibble of A, (b) set bit 0, (c) flip bits 7 and 6, (d) test whether bit 3 is 1.
3. After `SUB A, B` on the T8, which flag values mean `A > B`? Write it as a Boolean expression of Z and C.
4. Add an operation 5, "PASS B" (result = B), to the ALU. Which decode line would you add, and how many gates per bit? Modify `build_alu` and check it.
5. The critical path is 22 gate delays. If you replaced the ripple-carry chain with a lookahead adder whose carries all arrive after 4 gate delays, estimate the new depth. What clock frequency would that allow with 15 ps gates, if registers add 60 ps?

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| ALU | "The calculator" | Combinational circuit computing arithmetic and logic results plus flags from two operands and an operation code |
| ALU operation code | "ALU op", "function select" | The bits that choose the operation; on the T8 the low 3 bits of the opcode |
| Bitwise operation | "Logical AND/OR/XOR" | The gate applied separately to each bit pair, no carries |
| Result multiplexer | "Output select" | Chooses which unit's result appears at the ALU output |
| Z flag | "Zero" | NOR of all result bits |
| C flag | "Carry" | Carry out of the top bit: unsigned overflow on ADD, no-borrow on SUB |
| N flag | "Negative", "sign" | The top result bit |
| Mask | "Bit mask" | A constant combined with AND/OR/XOR to clear, set, flip or test chosen bits |

## Further Reading

- David Harris and Sarah Harris, *Digital Design and Computer Architecture*, Chapter 5 (ALUs, flags and the comparison of signed and unsigned numbers).
- Noam Nisan and Shimon Schocken, *The Elements of Computing Systems* (Nand2Tetris), Chapter 2, which builds a different ALU (the Hack ALU) from gates with a clever set of control bits.
- Texas Instruments datasheet *SN74LS181* (4-bit arithmetic logic unit / function generator).
- Ken Shirriff's blog articles on the reverse engineering of real ALUs (for example the 8085 and Z-80 ALUs), for how classic processors actually laid them out in silicon.
