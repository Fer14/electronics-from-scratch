from sim.logic import LogicCircuit

BITS = 8
SOURCES = ["PC_OUT", "MEM_OUT", "A_OUT", "ALU_OUT"]
OPCODES = {
    "NOP": 0x00, "OUT": 0x01, "HLT": 0x0F, "LDI": 0x10, "LDA": 0x11, "STA": 0x12,
    "ADD": 0x20, "SUB": 0x21, "AND": 0x22, "OR": 0x23, "XOR": 0x24,
    "ADDI": 0x28, "SUBI": 0x29, "ANDI": 0x2A, "ORI": 0x2B, "XORI": 0x2C,
    "JMP": 0x30, "JZ": 0x31, "JNZ": 0x32, "JC": 0x33, "JNC": 0x34,
}
MNEMONICS = {code: name for name, code in OPCODES.items()}
ONE_BYTE = {"NOP", "OUT", "HLT"}


def build_alu():
    lc = LogicCircuit("T8 ALU")
    a = [f"a{i}" for i in range(BITS)]
    b = [f"b{i}" for i in range(BITS)]
    lc.inputs(*a, *b, "op2", "op1", "op0")
    lc.not_("nop2", "op2")
    lc.not_("nop1", "op1")
    lc.not_("nop0", "op0")
    lc.and_("is_arith", "nop2", "nop1")
    lc.and_("sub", "nop2", "nop1", "op0")
    lc.and_("is_and", "nop2", "op1", "nop0")
    lc.and_("is_or", "nop2", "op1", "op0")
    lc.and_("is_xor", "op2", "nop1", "nop0")
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
    lc.and_("C", f"c{BITS}", "is_arith")
    lc.nor("Z", *[f"r{i}" for i in range(BITS)])
    lc.outputs(*[f"r{i}" for i in range(BITS)], "Z", "C")
    return lc


def build_step_counter():
    lc = LogicCircuit("step counter")
    lc.inputs("end")
    lc.constant("one", 1)
    toggle = "one"
    for i in range(3):
        lc.xor(f"d{i}", f"t{i}", toggle)
        lc.dff(f"d{i}", f"t{i}", name=f"T{i}", reset="end")
        if i < 2:
            lc.and_(f"k{i + 1}", toggle, f"t{i}")
            toggle = f"k{i + 1}"
    lc.outputs("t2", "t1", "t0")
    return lc


FETCH = [{"PC_OUT", "MAR_IN"}, {"MEM_OUT", "IR_IN", "PC_INC"}]
POINT = {"PC_OUT", "MAR_IN"}
ADDRESS = {"MEM_OUT", "MAR_IN", "PC_INC"}


def jump_taken(opcode, z, c):
    return {0x30: True, 0x31: z == 1, 0x32: z == 0, 0x33: c == 1, 0x34: c == 0}[opcode]


def microcode(opcode, step, z, c):
    if step < 2:
        return FETCH[step]
    if opcode == 0x01:
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
        tail = [POINT, {"MEM_OUT", "PC_IN", "END"} if jump_taken(opcode, z, c) else {"PC_INC", "END"}]
    else:
        tail = [{"END"}]
    return tail[step - 2] if step - 2 < len(tail) else {"END"}


class T8:
    def __init__(self, memory):
        self.mem = list(memory)
        self.alu = build_alu()
        self.counter = build_step_counter()
        self.reg = {"PC": 0, "MAR": 0, "IR": 0, "A": 0, "B": 0, "OUT": 0, "Z": 0, "C": 0}
        self.outputs = []
        self.cycles = 0
        self.instructions = 0
        self.halted = False

    def step_number(self):
        out = self.counter.evaluate({"end": 0})
        return 4 * out["t2"] + 2 * out["t1"] + out["t0"]

    def alu_outputs(self):
        op = self.reg["IR"] & 0x07
        inputs = {f"a{i}": (self.reg["A"] >> i) & 1 for i in range(BITS)}
        inputs.update({f"b{i}": (self.reg["B"] >> i) & 1 for i in range(BITS)})
        inputs.update({"op2": (op >> 2) & 1, "op1": (op >> 1) & 1, "op0": op & 1})
        out = self.alu.evaluate(inputs)
        return sum(out[f"r{i}"] << i for i in range(BITS)), out["Z"], out["C"]

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

    def run_instruction(self):
        while True:
            step, signals, _ = self.clock()
            if "END" in signals or "HALT" in signals:
                return


def reference_step(state, mem):
    pc, acc, z, c = state
    opcode, operand = mem[pc], mem[(pc + 1) & 0xFF]
    name = MNEMONICS.get(opcode, "NOP")
    pc = (pc + (1 if name in ONE_BYTE else 2)) & 0xFF
    out = None
    if name == "OUT":
        out = acc
    elif name == "LDI":
        acc = operand
    elif name == "LDA":
        acc = mem[operand]
    elif name == "STA":
        mem[operand] = acc
    elif opcode & 0xF0 == 0x20:
        b = operand if opcode & 0x08 else mem[operand]
        op = opcode & 0x07
        total = acc + b if op == 0 else acc + ((~b) & 0xFF) + 1 if op == 1 else {2: acc & b, 3: acc | b, 4: acc ^ b}[op]
        acc, c, z = total & 0xFF, int(op < 2 and total > 0xFF), int(total & 0xFF == 0)
    elif opcode & 0xF0 == 0x30 and jump_taken(opcode, z, c):
        pc = operand
    return (pc, acc, z, c), out, name == "HLT"


def assemble(source):
    lines = []
    for raw in source.splitlines():
        text = raw.split(";")[0].strip()
        if text:
            label, _, rest = text.rpartition(":")
            lines.append((label.strip() or None, rest.split()))
    labels, address = {}, 0
    for label, words in lines:
        if words and words[0] == ".org":
            address = int(words[1], 0)
        if label:
            labels[label] = address
        if words and words[0] != ".org":
            address += len(words) - 1 if words[0] == ".byte" else 1 if words[0] in ONE_BYTE else 2
    memory, address = [0] * 256, 0
    for label, words in lines:
        if not words:
            continue
        if words[0] == ".org":
            address = int(words[1], 0)
            continue
        operands = [labels[w] if w in labels else int(w, 0) for w in words[1:]]
        data = operands if words[0] == ".byte" else [OPCODES[words[0]]] + operands
        memory[address:address + len(data)] = data
        address += len(data)
    return memory, labels


PROGRAMS = {
    "countdown": """
        LDI 5
loop:   OUT
        SUBI 1
        JNZ loop
        OUT
        HLT
""",
    "multiply": """
        LDI 0
        STA result
loop:   LDA y
        ORI 0
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
""",
    "fibonacci": """
        LDI 0
        STA a
        LDI 1
        STA b
loop:   LDA a
        OUT
        ADD b
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
""",
}


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


def main():
    print("=== The first cycles of the multiply program, gate-level ALU and step counter ===")
    memory, labels = assemble(PROGRAMS["multiply"])
    machine = T8(memory)
    for _ in range(16):
        step, signals, bus = machine.clock()
        r = machine.reg
        print(f"  cycle {machine.cycles:2d} T{step}  {', '.join(sorted(signals)):30s} bus={bus:3d}  PC={r['PC']:02X} IR={r['IR']:02X} A={r['A']:3d}")

    print("\n=== Three programs, checked instruction by instruction against the reference model ===")
    for name, source in PROGRAMS.items():
        memory, labels = assemble(source)
        machine, ref_out, ref_mem = lockstep(memory)
        same_memory = machine.mem == ref_mem
        print(f"  {name:9s}: output {machine.outputs}")
        print(f"             reference {ref_out}; same output: {machine.outputs == ref_out}; same final memory: {same_memory}")
        cpi = machine.cycles / machine.instructions
        print(f"             {machine.instructions} instructions, {machine.cycles} clock cycles, {cpi:.2f} cycles per instruction")

    print("\n=== How long would that take on real hardware? ===")
    memory, _ = assemble(PROGRAMS["fibonacci"])
    machine, _, _ = lockstep(memory)
    depth = build_alu().depth()
    for label, gate, overhead in [("74HC chips on a breadboard", 8e-9, 40e-9), ("a modern chip", 15e-12, 100e-12)]:
        period = depth * gate + overhead
        f = 1 / period
        print(f"  {label}: ALU path {depth} x {gate * 1e9:.3g} ns + {overhead * 1e9:.3g} ns of registers and control = {period * 1e9:.3g} ns -> {f / 1e6:.4g} MHz")
        print(f"    Fibonacci: {machine.cycles} cycles = {machine.cycles * period * 1e6:.4g} us")


if __name__ == "__main__":
    main()
