OPCODES = {
    "NOP": 0x00, "OUT": 0x01, "HLT": 0x0F,
    "LDI": 0x10, "LDA": 0x11, "STA": 0x12,
    "ADD": 0x20, "SUB": 0x21, "AND": 0x22, "OR": 0x23, "XOR": 0x24,
    "ADDI": 0x28, "SUBI": 0x29, "ANDI": 0x2A, "ORI": 0x2B, "XORI": 0x2C,
    "JMP": 0x30, "JZ": 0x31, "JNZ": 0x32, "JC": 0x33, "JNC": 0x34,
}
MNEMONICS = {code: name for name, code in OPCODES.items()}
ONE_BYTE = {"NOP", "OUT", "HLT"}


class AssemblyError(ValueError):
    pass


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
    memory = [0] * 256
    listing = []
    address = 0
    for number, label, words in lines:
        if not words:
            continue
        head = words[0].upper()
        if head == ".ORG":
            address = int(words[1], 0)
            continue
        if head == ".BYTE":
            data = [value_of(w, labels, number) for w in words[1:]]
        else:
            data = [OPCODES[head]]
            if head not in ONE_BYTE:
                if len(words) != 2:
                    raise AssemblyError(f"line {number}: {head} needs exactly one operand")
                data.append(value_of(words[1], labels, number))
        for offset, byte in enumerate(data):
            memory[address + offset] = byte
        listing.append((address, data, (label + ": " if label else "") + " ".join(words)))
        address += len(data)
    return memory, labels, listing


def disassemble(memory, start, end):
    out, address = [], start
    while address < end:
        opcode = memory[address]
        name = MNEMONICS.get(opcode, f".byte {opcode}")
        if name in OPCODES and name not in ONE_BYTE:
            out.append((address, f"{name} {memory[address + 1]:#04x}"))
            address += 2
        else:
            out.append((address, name))
            address += 1
    return out


def run(memory, max_instructions=10000):
    mem = list(memory)
    pc, acc, z, c, outputs = 0, 0, 0, 0, []
    for count in range(1, max_instructions + 1):
        opcode, operand = mem[pc], mem[(pc + 1) & 0xFF]
        name = MNEMONICS.get(opcode, "NOP")
        pc = (pc + (1 if name in ONE_BYTE or opcode not in MNEMONICS else 2)) & 0xFF
        if name == "HLT":
            return outputs, count, mem
        if name == "OUT":
            outputs.append(acc)
        elif name == "LDI":
            acc = operand
        elif name == "LDA":
            acc = mem[operand]
        elif name == "STA":
            mem[operand] = acc
        elif opcode & 0xF0 == 0x20:
            b = operand if opcode & 0x08 else mem[operand]
            op = opcode & 0x07
            if op == 0:
                total = acc + b
            elif op == 1:
                total = acc + ((~b) & 0xFF) + 1
            else:
                total = {2: acc & b, 3: acc | b, 4: acc ^ b}[op]
            acc, c, z = total & 0xFF, int(op < 2 and total > 0xFF), int(total & 0xFF == 0)
        elif opcode & 0xF0 == 0x30:
            if {"JMP": True, "JZ": z == 1, "JNZ": z == 0, "JC": c == 1, "JNC": c == 0}[name]:
                pc = operand
    raise RuntimeError("program did not halt")


MULTIPLY = """
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
"""

FIBONACCI = """
; print Fibonacci numbers until the next one does not fit in 8 bits
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

        .org 0x80
a:      .byte 0
b:      .byte 0
next:   .byte 0
"""


def show_listing(listing):
    for address, data, text in listing:
        print(f"  {address:02X}: {' '.join(f'{b:02X}' for b in data):8s}  {text}")


def main():
    print("=== Assembling the multiply program ===")
    memory, labels, listing = assemble(MULTIPLY)
    show_listing(listing)
    print(f"  labels: {', '.join(f'{k}={v:#04x}' for k, v in labels.items())}")
    outputs, count, final = run(memory)
    print(f"  run on the reference model: output {outputs}, {count} instructions, result cell = {final[labels['result']]}")

    print("\n=== Disassembling the first bytes back into instructions ===")
    for address, text in disassemble(memory, 0, 12):
        print(f"  {address:02X}: {text}")

    print("\n=== Fibonacci ===")
    memory, labels, listing = assemble(FIBONACCI)
    used = max(a + len(d) for a, d, _ in listing if a < 0x80)
    print(f"  program: {used} bytes of code")
    outputs, count, _ = run(memory)
    print(f"  output: {outputs}")
    print(f"  {count} instructions executed")

    print("\n=== The assembler catches mistakes ===")
    for bad in ["        LDA nowhere\n        HLT", "        LDI 300\n        HLT", "        MUL 3\n        HLT", "x: .byte 1\nx: .byte 2"]:
        try:
            assemble(bad)
        except AssemblyError as error:
            print(f"  {error}")


if __name__ == "__main__":
    main()
