HEX_DIGITS = "0123456789ABCDEF"


def to_binary(n, width):
    bits = []
    for _ in range(width):
        bits.append(n % 2)
        n = n // 2
    return "".join(str(b) for b in reversed(bits))


def from_binary(text):
    value = 0
    for ch in text:
        value = value * 2 + int(ch)
    return value


def to_hex(n, width):
    digits = []
    for _ in range(width):
        digits.append(HEX_DIGITS[n % 16])
        n = n // 16
    return "".join(reversed(digits))


def place_values(text):
    width = len(text)
    terms = [f"{ch}x{2 ** (width - 1 - i)}" for i, ch in enumerate(text)]
    return " + ".join(terms)


def twos_complement(value, width):
    return value % (2 ** width)


def signed_value(pattern, width):
    return pattern - 2 ** width if pattern >= 2 ** (width - 1) else pattern


def bits_needed(count):
    bits = 0
    while 2 ** bits < count:
        bits += 1
    return bits


def main():
    print("=== Counting in binary with 4 bits ===")
    for n in range(16):
        print(f"  {n:2d} = {to_binary(n, 4)} = 0x{to_hex(n, 1)}")

    print("\n=== Binary to decimal by place value ===")
    for text in ["1011", "01100100", "11111111"]:
        print(f"  {text} = {place_values(text)} = {from_binary(text)}")

    print("\n=== Decimal to binary by repeated division ===")
    n = 156
    steps = []
    while n > 0:
        steps.append(f"{n} / 2 = {n // 2} remainder {n % 2}")
        n //= 2
    for step in steps:
        print(f"  {step}")
    print(f"  read remainders bottom-up: 156 = {to_binary(156, 8)}")

    print("\n=== Hexadecimal ===")
    for n in [156, 255, 4096, 48879]:
        width = 4 if n > 255 else 2
        print(f"  {n:5d} = 0x{to_hex(n, width)} = {to_binary(n, 4 * width)}")

    print("\n=== Unsigned range for n bits ===")
    for width in [1, 4, 8, 16, 32]:
        print(f"  {width:2d} bits: 0 .. {2 ** width - 1}")

    print("\n=== Two's complement, 8 bits ===")
    for value in [5, -5, 127, -128, -1]:
        pattern = twos_complement(value, 8)
        print(f"  {value:5d} -> {to_binary(pattern, 8)} (0x{to_hex(pattern, 2)}) -> back to {signed_value(pattern, 8)}")
    a, b = 100, 50
    raw = a + b
    wrapped = raw % 256
    print(f"  {a} + {b} = {raw}, but in 8 bits the pattern is {to_binary(wrapped, 8)}")
    print(f"    read as unsigned: {wrapped}; read as signed: {signed_value(wrapped, 8)} (signed overflow)")
    print(f"  200 + 100 = 300 -> 8-bit pattern {to_binary(300 % 256, 8)} = {300 % 256} (unsigned overflow, carry out = 1)")
    x = 37
    inverted = (~x) & 0xFF
    print(f"  -37 by 'invert and add 1': {to_binary(x, 8)} -> {to_binary(inverted, 8)} -> {to_binary((inverted + 1) & 0xFF, 8)}")
    print(f"  12 - 37 as 12 + (-37): {to_binary(12, 8)} + {to_binary((inverted + 1) & 0xFF, 8)} = {to_binary((12 + inverted + 1) & 0xFF, 8)} = {signed_value((12 + inverted + 1) & 0xFF, 8)}")

    print("\n=== Bits needed ===")
    for count in [2, 10, 26, 100, 256, 1000, 1_000_000]:
        print(f"  {count:8d} different values need {bits_needed(count):2d} bits")


if __name__ == "__main__":
    main()
