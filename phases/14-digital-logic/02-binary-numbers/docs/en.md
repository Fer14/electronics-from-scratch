# Binary Numbers

> With only two symbols you can still count to anything: you just need more columns.

**Type:** Learn
**Prerequisites:** Phase 00 (Words and Units), Lesson 04 (Scientific Notation and Orders of Magnitude), Phase 14 (Digital Logic), Lesson 01 (Analog vs Digital)
**Time:** ~70 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Base (radix) | How many different digit symbols a number system uses | Decimal has ten fingers' worth of symbols, 0-9 |
| Place value | Each column of a number is worth a fixed multiple of the next one | In 352, the 3 counts hundreds, the 5 tens, the 2 ones |
| Binary | The base-2 number system, with only digits 0 and 1 | A row of light switches, each up or down |
| Bit | One binary digit | One switch |
| Byte | A group of 8 bits | A row of 8 switches |
| Nibble | 4 bits, half a byte | Half the row |
| MSB / LSB | Most / least significant bit: the leftmost (biggest) and rightmost (smallest) column | The "hundreds" end and the "ones" end of a number |
| Hexadecimal (hex) | Base 16, a short way to write groups of 4 bits | A shorthand: one hex symbol stands for four switches |
| Unsigned | A bit pattern read as a number 0 or greater | A car odometer: never negative |
| Two's complement | The standard way to store negative whole numbers in bits | An odometer rolled back past zero: 0000 becomes 9999, which we agree to read as -1 |
| Overflow | A result too big (or too negative) to fit in the bits available | The odometer rolling over from 99999 to 00000 |
| Carry | The 1 that moves into the next column when a column overflows | "Carry the one" in school addition |

## Learning Objectives

- Explain place value in base 10 and base 2 using the same idea.
- Convert between decimal, binary and hexadecimal by hand, both directions.
- State the range of numbers that n bits can hold, unsigned and signed.
- Encode and decode negative numbers in two's complement and explain why it makes subtraction free.
- Recognise unsigned and signed overflow in 8-bit arithmetic.
- Compute how many bits are needed to tell N different things apart.

## The Problem

Lesson 01 left us with wires that carry only 0 or 1. That is very robust, but a single wire can say only one of two things: yes or no, on or off. A thermometer needs to report 23 °C. A camera pixel needs to report one of 256 brightness levels. A computer needs to add 100 and 50.

So we need a way to represent any number using only 0s and 1s, spread across several wires. And we need a representation that makes arithmetic easy to build out of switches, because in Lesson 07 we will build an adder from gates, and in Phase 16 a whole computer. The way to do it is the same way you already write numbers, just with two symbols instead of ten.

## The Physics

This lesson is mostly about counting, but it has a physical side: each bit of a number is one wire (or one memory cell) with a voltage on it. An 8-bit number travelling across a chip is 8 wires side by side, each LOW or HIGH, which engineers call a **bus**. A 64-bit processor moves numbers on 64 wires at once. Every extra bit is one more wire, one more transistor switch per gate, one more memory cell. That physical cost is why bits are counted carefully, and why the choice of 8, 16, 32 or 64 bits for a number matters in hardware.

## The Concept

### Place value in decimal, slowly

Look at the number 352. You learned at school that it means "three hundreds, five tens and two ones". Written out:

```
352 = 3 x 100 + 5 x 10 + 2 x 1
```

Notice the column values: 1, 10, 100, 1000... each column is worth **ten times** the one to its right. That is because we have ten symbols (0 to 9). When a column passes 9, it wraps back to 0 and adds 1 to the next column: 9 + 1 = 10. Using powers (Phase 00, Lesson 04), the column values are 10^0, 10^1, 10^2, and so on.

### Place value in binary

Binary uses the same rule with **two** symbols. Each column is worth **two times** the one to its right:

```
column value:   128   64   32   16    8    4    2    1
as a power:     2^7  2^6  2^5  2^4  2^3  2^2  2^1  2^0
```

A binary number is a sum of the column values where the digit is 1. Read `1011` out loud as "one eight, no four, one two, one one":

```
1011 = 1 x 8 + 0 x 4 + 1 x 2 + 1 x 1 = 8 + 2 + 1 = 11
```

Check it on a calculator: 8 + 2 + 1 = 11. A longer one, the byte `01100100`:

```
0 x 128 + 1 x 64 + 1 x 32 + 0 x 16 + 0 x 8 + 1 x 4 + 0 x 2 + 0 x 1
= 64 + 32 + 4
= 100
```

To avoid confusion between "binary 10" (two) and "decimal 10" (ten), we sometimes write a small 2 or a `0b` prefix: `0b1011` = 11.

### Counting in binary

Counting is just "add 1, and carry when a column overflows". In binary a column overflows when it passes 1:

```
decimal  binary      what happened
   0     0000
   1     0001
   2     0010        1 + 1 = 10: the ones column wraps, carry into the twos
   3     0011
   4     0100        0011 + 1: two carries in a row
   5     0101
   6     0110
   7     0111
   8     1000        three carries in a row
   9     1001
  ...
  15     1111        the largest 4-bit number
  16    10000        needs a fifth bit
```

A pattern worth spotting: the rightmost bit flips every step, the next one every 2 steps, the next every 4, then every 8. This is exactly what the counter circuit in Phase 15, Lesson 05 will do with flip-flops.

### Decimal to binary: repeated division by 2

To turn 156 into binary, keep dividing by 2 and write down the remainders. Each remainder is the next bit, starting from the right (LSB):

```
156 / 2 = 78   remainder 0     <- bit 0 (LSB)
 78 / 2 = 39   remainder 0     <- bit 1
 39 / 2 = 19   remainder 1     <- bit 2
 19 / 2 =  9   remainder 1     <- bit 3
  9 / 2 =  4   remainder 1     <- bit 4
  4 / 2 =  2   remainder 0     <- bit 5
  2 / 2 =  1   remainder 0     <- bit 6
  1 / 2 =  0   remainder 1     <- bit 7 (MSB)
```

Reading the remainders from the bottom up: 156 = `10011100`. Check by place value: 128 + 16 + 8 + 4 = 156.

Why does it work? Dividing by 2 and taking the remainder asks "is this number odd?", which is exactly the ones bit. Dividing by 2 then shifts every bit one column to the right, so the next remainder is the next bit.

A second method, often faster in your head: subtract the biggest power of two that fits. 156 - 128 = 28 (bit 7 is 1); 64 and 32 do not fit (bits 6 and 5 are 0); 28 - 16 = 12 (bit 4); 12 - 8 = 4 (bit 3); 4 - 4 = 0 (bit 2); bits 1 and 0 are 0. Same answer.

### Hexadecimal: binary in short form

Long rows of 0s and 1s are hard to read and easy to miscopy. Hexadecimal, base 16, fixes this. It needs 16 symbols, so after 0-9 it uses the letters A-F:

```
hex:      0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
decimal:  0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
binary: 0000 0001 0010 0011 0100 0101 0110 0111 1000 1001 1010 1011 1100 1101 1110 1111
```

The magic is that 16 = 2^4, so **one hex digit is exactly 4 bits**. To convert binary to hex, cut the bits into groups of 4 from the right and replace each group:

```
156 = 1001 1100
         9    C     -> 0x9C
```

Check: 9 x 16 + 12 = 144 + 12 = 156. The prefix `0x` marks hex. One byte is always exactly two hex digits, from `0x00` to `0xFF` (255). Programmers use hex for memory addresses, colours (`#FF8000` is orange: red 255, green 128, blue 0) and machine code (Phase 16).

### How big a number fits in n bits?

With n bits there are 2^n different patterns (each bit doubles the count). Read out loud: "n bits give two to the n patterns". Unsigned, they represent 0 to 2^n - 1:

```
bits   patterns          unsigned range
  1    2                 0 .. 1
  4    16                0 .. 15
  8    256               0 .. 255
 16    65,536            0 .. 65,535
 32    4,294,967,296     0 .. about 4.29 billion
```

Turned around: to label N different things you need the smallest n with 2^n at least N. Ten decimal digits need 4 bits (2^3 = 8 is too few, 2^4 = 16 is enough). 26 letters need 5 bits (2^5 = 32). A million colours need 20 bits (2^20 = 1,048,576). A handy fact: 2^10 = 1024 is about a thousand, so every 10 bits multiply the range by about 1000.

### Adding in binary

Binary addition works column by column, exactly like school addition, but the table is tiny:

```
0 + 0 = 0
0 + 1 = 1
1 + 0 = 1
1 + 1 = 10     write 0, carry 1
1 + 1 + 1 = 11 write 1, carry 1   (two bits plus an incoming carry)
```

Example, 6 + 7:

```
  carries:  1 1 0
              0 1 1 0    (6)
            + 0 1 1 1    (7)
            ---------
              1 1 0 1    (13)
```

Column by column from the right: 0+1 = 1 (no carry); 1+1 = 10 (write 0, carry 1); 1+1+carry 1 = 11 (write 1, carry 1); 0+0+carry 1 = 1. Result `1101` = 8 + 4 + 1 = 13. In Lesson 07 we build this exact procedure out of gates; the "write" bit is called the **sum** and the moved bit is the **carry**.

### Overflow: when the answer does not fit

An 8-bit adder has only 8 output wires. 200 + 100 = 300, but 300 needs 9 bits (`1 0010 1100`). The 9th bit falls out as a **carry out** and the 8 wires show `0010 1100` = 44. That is **unsigned overflow**: the result has wrapped around, like an odometer. In math, 300 mod 256 = 44 ("mod" means "the remainder after dividing by").

### Negative numbers: two's complement

How do we store -5 with only 0s and 1s? There are several ideas; the one every modern computer uses is **two's complement**. Start from the odometer picture. An 8-bit counter at `00000000`, rolled back by one, shows `11111111`. We simply agree that `11111111` means -1. Rolling back again gives `11111110` = -2, and so on.

The rule in one sentence: **in n bits, the pattern for a negative number -x is the unsigned pattern of 2^n - x**. For -5 in 8 bits: 256 - 5 = 251 = `11111011`.

An equivalent recipe that is easy by hand: **invert every bit, then add 1**.

```
 5        = 0000 0101
 invert   = 1111 1010
 add 1    = 1111 1011   = -5
```

Another way to read a two's complement number: the MSB counts **negative** 128 instead of +128. So `11111011` = -128 + 64 + 32 + 16 + 8 + 2 + 1 = -128 + 123 = -5. Check it on a calculator.

Properties worth remembering:

- The MSB is 1 for every negative number and 0 for zero and positives, so it works as a **sign bit**.
- The 8-bit range is -128 to +127. There is one more negative than positive, because zero takes one of the "non-negative" patterns.
- There is only one zero (`00000000`), unlike older schemes that also had a "minus zero".

```
pattern     unsigned   two's complement
0000 0000       0            0
0000 0001       1            1
0111 1111     127          127   <- largest positive
1000 0000     128         -128   <- most negative
1111 1011     251           -5
1111 1111     255           -1
```

### Why two's complement wins: subtraction for free

With two's complement, the **same adder** does both addition and subtraction, and the same circuit works for unsigned and signed numbers. To compute 12 - 37, compute 12 + (-37):

```
  37 = 0010 0101   -> invert: 1101 1010 -> add 1: 1101 1011  (-37)

     0000 1100     (12)
   + 1101 1011     (-37)
   -----------
     1110 0111     = -128 + 64 + 32 + 4 + 2 + 1 = -25
```

12 - 37 = -25. Correct. In hardware, "invert every bit" is a row of NOT gates and "add 1" is setting the adder's carry-in to 1. That is why the ALU in Phase 16 subtracts with almost no extra gates.

### Signed overflow

100 + 50 = 150, which fits in 8 unsigned bits (`1001 0110`). But read as signed, that pattern is -128 + 16 + 4 + 2 = -106. Two positive numbers added to a "negative" result: that is **signed overflow**, because +150 is outside -128..+127. The rule a circuit can check: signed overflow happens when two numbers with the same sign produce a result with the other sign. Note the bits are the same in both readings; only our interpretation changes. Processors keep both a carry flag (unsigned overflow) and an overflow flag (signed overflow) so the program can pick the one that matches its meaning.

## Build It

The script `code/main.py` does every conversion of this lesson with small functions, so you can compare its output with your hand calculations.

### Step 1: Decimal to binary

Repeated division by two, collecting remainders, then reversing:

```python
def to_binary(n, width):
    bits = []
    for _ in range(width):
        bits.append(n % 2)
        n = n // 2
    return "".join(str(b) for b in reversed(bits))
```

`%` is Python's remainder operator and `//` is whole-number division. `width` fixes the number of bits so leading zeros are shown.

### Step 2: Binary to decimal

Read from the left: every new bit doubles what we have so far and adds itself. This is place value in disguise (it is called Horner's method).

```python
def from_binary(text):
    value = 0
    for ch in text:
        value = value * 2 + int(ch)
    return value
```

For `1011`: 0 -> 1 -> 2 -> 5 -> 11.

### Step 3: Hexadecimal

The same as binary with 16 instead of 2:

```python
HEX_DIGITS = "0123456789ABCDEF"

def to_hex(n, width):
    digits = []
    for _ in range(width):
        digits.append(HEX_DIGITS[n % 16])
        n = n // 16
    return "".join(reversed(digits))
```

### Step 4: Two's complement

Taking the remainder modulo 2^n turns any whole number, negative ones included, into its n-bit pattern. Going back, a pattern with the MSB set means "subtract 2^n".

```python
def twos_complement(value, width):
    return value % (2 ** width)

def signed_value(pattern, width):
    return pattern - 2 ** width if pattern >= 2 ** (width - 1) else pattern
```

Python's `%` always returns a non-negative remainder, so `-5 % 256` is 251, exactly the pattern we want.

### Step 5: Bits needed

```python
def bits_needed(count):
    bits = 0
    while 2 ** bits < count:
        bits += 1
    return bits
```

Run it:

```bash
uv run python phases/14-digital-logic/02-binary-numbers/code/main.py
```

Part of the output:

```
=== Two's complement, 8 bits ===
      5 -> 00000101 (0x05) -> back to 5
     -5 -> 11111011 (0xFB) -> back to -5
    127 -> 01111111 (0x7F) -> back to 127
   -128 -> 10000000 (0x80) -> back to -128
     -1 -> 11111111 (0xFF) -> back to -1
  100 + 50 = 150, but in 8 bits the pattern is 10010110
    read as unsigned: 150; read as signed: -106 (signed overflow)
  200 + 100 = 300 -> 8-bit pattern 00101100 = 44 (unsigned overflow, carry out = 1)
  -37 by 'invert and add 1': 00100101 -> 11011010 -> 11011011
  12 - 37 as 12 + (-37): 00001100 + 11011011 = 11100111 = -25
```

This lesson is pure counting, so it does not need the circuit simulator yet. From Lesson 03 on, every bit you see here becomes a wire in `sim.logic`.

## Use It

- **Microcontroller registers** (Phase 17) are 8, 16 or 32 bits wide, and datasheets describe them bit by bit: "bit 3 enables the timer". You will read and write them in hex.
- **ADC readings.** A 10-bit analog-to-digital converter returns 0 to 1023. A 12-bit one returns 0 to 4095. With a 3.3 V reference, one step of a 12-bit ADC is 3.3 / 4096 = 0.81 mV.
- **Colours.** Screens store red, green and blue as 8 bits each: 24 bits, 2^24 = 16.7 million colours, written as six hex digits.
- **IPv4 addresses** are 32 bits written as four bytes in decimal (192.168.1.1); IPv6 addresses are 128 bits written in hex.
- **The year 2038 problem.** Many systems count seconds since 1 January 1970 in a signed 32-bit number. Its maximum, 2^31 - 1 = 2,147,483,647 seconds, is reached on 19 January 2038; one second later it overflows to a large negative number. The fix is a 64-bit count.
- **Ariane 5 (1996).** The rocket's guidance software converted a 64-bit value into a 16-bit signed integer. The value was larger than 32,767, the conversion overflowed, and the rocket self-destructed 37 seconds after launch. Overflow is not an academic topic.

## Try It in the Lab

This lesson has no lab task. You will turn these bits into wires and gates from Lesson 03 on.

## Common Mistakes

- **Reading binary from the wrong end.** The rightmost bit is worth 1 (the LSB). In the division method, the first remainder is the LSB, so you read the remainders bottom-up.
- **Dropping leading zeros when the width matters.** `101` and `00000101` are the same unsigned number, but in two's complement `101` as a 3-bit number is -3, while `00000101` is +5. Always know the width.
- **Forgetting the +1 in two's complement.** "Invert the bits" alone gives one's complement: inverting 5 gives `11111010`, which is -6 in two's complement, not -5.
- **Mixing up carry and overflow.** The carry out tells you an unsigned result did not fit. Signed overflow is a different test (same-sign inputs, other-sign result). 255 + 1 sets the carry but not signed overflow (-1 + 1 = 0 is fine); 127 + 1 sets signed overflow but not the carry.
- **Thinking hex is a different kind of number.** Hex, binary and decimal are three ways to write the same number. The hardware only ever has bits.
- **Confusing k with Ki.** In memory sizes, 1 KiB = 1024 bytes (2^10), while 1 kB = 1000 bytes. Disk makers use 1000; operating systems often use 1024.

## Exercises

1. Convert to decimal: `1101`, `10000000`, `0x3F`, `0xA5`.
2. Convert 200 to binary using repeated division, then to hex. Check with place value.
3. How many bits does a counter need to count from 0 to 59 (seconds on a clock)? To store the day of the year (1 to 366)?
4. Write -20 in 8-bit two's complement by "invert and add 1". Then compute 50 + (-20) in binary and check that you get 30. What happens to the 9th bit?
5. For each 8-bit addition, say whether the carry is set and whether signed overflow happens: (a) 0x7F + 0x01, (b) 0xFF + 0x01, (c) 0x80 + 0x80, (d) 0x40 + 0x30. Explain each in one sentence.

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Bit | "A zero or a one" | One binary digit, physically one wire or memory cell at LOW or HIGH |
| Byte | "Eight bits" | 8 bits, 256 patterns, written as two hex digits |
| Hex | "Those numbers with letters" | Base 16, used because one hex digit is exactly 4 bits |
| Two's complement | "How computers do negatives" | n-bit pattern of a negative -x is 2^n - x; the MSB has weight -2^(n-1) |
| Overflow | "The number got too big" | The true result is outside the range the bits can show; the stored bits wrap around |
| Carry | "Carry the one" | The extra bit produced when a column's sum is 2 or more; the carry out of the top column flags unsigned overflow |
| MSB / LSB | "Top bit / bottom bit" | The bit with the largest / smallest place value; in two's complement the MSB is also the sign |

## Further Reading

- Charles Petzold, *Code: The Hidden Language of Computer Hardware and Software* (2nd ed., 2022), chapters on binary numbers and counting with switches.
- Khan Academy, Computing course, "Binary numbers" unit.
- Noam Nisan and Shimon Schocken, *The Elements of Computing Systems* (Nand2Tetris), Chapter 2 (Boolean Arithmetic), for binary and two's complement as hardware sees them.
- All About Circuits, *Digital* textbook (Vol. IV), chapter "Numeration Systems" and "Binary Arithmetic".
