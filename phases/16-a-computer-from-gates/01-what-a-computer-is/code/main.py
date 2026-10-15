NAMES = {
    0x00: "NOP", 0x01: "OUT", 0x0F: "HLT",
    0x10: "LDI", 0x11: "LDA", 0x12: "STA",
    0x20: "ADD", 0x21: "SUB", 0x22: "AND", 0x23: "OR", 0x24: "XOR",
    0x28: "ADDI", 0x29: "SUBI", 0x2A: "ANDI", 0x2B: "ORI", 0x2C: "XORI",
    0x30: "JMP", 0x31: "JZ", 0x32: "JNZ", 0x33: "JC", 0x34: "JNC",
}
ONE_BYTE = {0x00, 0x01, 0x0F}
IMMEDIATE = {0x10, 0x28, 0x29, 0x2A, 0x2B, 0x2C}


def describe(opcode, operand):
    name = NAMES.get(opcode, "???")
    if opcode in ONE_BYTE:
        return name
    return f"{name} {operand}" if opcode in IMMEDIATE else f"{name} 0x{operand:02X}"


def alu(op, a, b):
    if op == 0:
        total = a + b
        return total & 0xFF, int(total > 0xFF)
    if op == 1:
        total = a + ((~b) & 0xFF) + 1
        return total & 0xFF, int(total > 0xFF)
    results = {2: a & b, 3: a | b, 4: a ^ b}
    return results[op], 0


def run(memory, max_instructions=1000, trace=False):
    mem = list(memory) + [0] * (256 - len(memory))
    pc, acc, z, c = 0, 0, 0, 0
    outputs = []
    for count in range(1, max_instructions + 1):
        opcode = mem[pc]
        operand = mem[(pc + 1) & 0xFF]
        size = 1 if opcode in ONE_BYTE else 2
        if trace:
            raw = f"{opcode:02X}" if size == 1 else f"{opcode:02X} {operand:02X}"
            print(f"  pc={pc:3d}  fetch {raw:5s}  {describe(opcode, operand):9s}", end="")
        pc = (pc + size) & 0xFF
        group = opcode & 0xF0
        if opcode == 0x0F:
            if trace:
                print("  -> halt")
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
        if trace:
            print(f"  -> A={acc:3d} Z={z} C={c} pc={pc:3d}" + (f"  OUT {acc}" if opcode == 0x01 else ""))
    raise RuntimeError("program did not halt")


def main():
    print("=== The T8 computer: 8-bit data, 256 bytes of memory, one accumulator ===")
    program = [0x11, 0x10, 0x20, 0x11, 0x01, 0x0F]
    memory = program + [0] * (0x10 - len(program)) + [25, 17]
    print("  memory 0x00: " + " ".join(f"{b:02X}" for b in memory[:6]) + "   <- the program")
    print("  memory 0x10: " + " ".join(f"{b:02X}" for b in memory[0x10:0x12]) + "               <- the data (25 and 17)")
    print("\n=== Fetch, decode, execute ===")
    outputs, count, _ = run(memory, trace=True)
    print(f"  output: {outputs}, after {count} instructions")

    print("\n=== A program is just numbers: change one byte ===")
    changed = list(memory)
    changed[2] = 0x21
    outputs, _, _ = run(changed)
    print(f"  byte 2 changed from 0x20 (ADD) to 0x21 (SUB): output {outputs}  (25 - 17)")

    print("\n=== A loop: count down from 5 ===")
    countdown = [0x10, 5, 0x01, 0x29, 1, 0x32, 2, 0x01, 0x0F]
    outputs, count, _ = run(countdown, trace=True)
    print(f"  output: {outputs}, {count} instructions executed for a {len(countdown)}-byte program")


if __name__ == "__main__":
    main()
