from sim.logic import LogicCircuit

BITS = 8
SOURCES = ["PC_OUT", "MEM_OUT", "A_OUT", "ALU_OUT"]
LOADS = ["MAR_IN", "MEM_IN", "IR_IN", "A_IN", "B_IN", "OUT_IN", "PC_IN", "FLAGS_IN", "PC_INC"]


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


def bus_mux():
    lc = LogicCircuit("8-bit bus, 4 sources, one-hot select")
    lc.inputs(*SOURCES, *[f"{src}.{i}" for src in SOURCES for i in range(BITS)])
    for i in range(BITS):
        for src in SOURCES:
            lc.and_(f"{src}.g{i}", f"{src}.{i}", src)
        lc.or_(f"bus{i}", *[f"{src}.g{i}" for src in SOURCES])
    lc.outputs(*[f"bus{i}" for i in range(BITS)])
    return lc


class Memory:
    def __init__(self, contents=()):
        self.cells = list(contents) + [0] * (256 - len(contents))

    def read(self, address):
        return self.cells[address & 0xFF]

    def write(self, address, value):
        self.cells[address & 0xFF] = value & 0xFF


class BusConflict(RuntimeError):
    pass


class Datapath:
    def __init__(self, memory):
        self.mem = memory
        self.alu = build_alu()
        self.reg = {"PC": 0, "MAR": 0, "IR": 0, "A": 0, "B": 0, "OUT": 0, "Z": 0, "C": 0}

    def alu_outputs(self):
        op = self.reg["IR"] & 0x07
        inputs = {f"a{i}": (self.reg["A"] >> i) & 1 for i in range(BITS)}
        inputs.update({f"b{i}": (self.reg["B"] >> i) & 1 for i in range(BITS)})
        inputs.update({"op2": (op >> 2) & 1, "op1": (op >> 1) & 1, "op0": op & 1})
        out = self.alu.evaluate(inputs)
        return sum(out[f"r{i}"] << i for i in range(BITS)), out["Z"], out["C"]

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


def show(dp, step, signals, value):
    r = dp.reg
    regs = f"PC={r['PC']:02X} MAR={r['MAR']:02X} IR={r['IR']:02X} A={r['A']:3d} B={r['B']:3d} OUT={r['OUT']:3d} Z={r['Z']} C={r['C']}"
    shown = "  -    " if value is None else f"{value:3d} {value:02X}h"
    print(f"  {step:2d} {', '.join(sorted(signals)):28s} bus={shown}  {regs}")


def main():
    print("=== The bus is a multiplexer: one-hot source select, 8 bits wide ===")
    mux = bus_mux()
    values = {"PC_OUT": 5, "MEM_OUT": 0x11, "A_OUT": 42, "ALU_OUT": 99}
    for chosen in SOURCES:
        inputs = {src: int(src == chosen) for src in SOURCES}
        for src in SOURCES:
            inputs.update({f"{src}.{i}": (values[src] >> i) & 1 for i in range(BITS)})
        out = mux.evaluate(inputs)
        print(f"  {chosen:8s} enabled -> bus = {sum(out[f'bus{i}'] << i for i in range(BITS)):3d}")
    print(f"  {mux.gate_count()} gates for 4 sources x 8 bits")

    print("\n=== Running LDA 0x10, ADD 0x11, OUT by setting control signals by hand ===")
    mem = Memory([0x11, 0x10, 0x20, 0x11, 0x01, 0x0F] + [0] * 10 + [25, 17])
    dp = Datapath(mem)
    program = [
        {"PC_OUT", "MAR_IN"}, {"MEM_OUT", "IR_IN", "PC_INC"},
        {"PC_OUT", "MAR_IN"}, {"MEM_OUT", "MAR_IN", "PC_INC"}, {"MEM_OUT", "A_IN"},
        {"PC_OUT", "MAR_IN"}, {"MEM_OUT", "IR_IN", "PC_INC"},
        {"PC_OUT", "MAR_IN"}, {"MEM_OUT", "MAR_IN", "PC_INC"}, {"MEM_OUT", "B_IN"}, {"ALU_OUT", "A_IN", "FLAGS_IN"},
        {"PC_OUT", "MAR_IN"}, {"MEM_OUT", "IR_IN", "PC_INC"},
        {"A_OUT", "OUT_IN"},
    ]
    for step, signals in enumerate(program):
        value = dp.clock(signals)
        show(dp, step, signals, value)
    print(f"  output register: {dp.reg['OUT']} after {len(program)} clock cycles")

    print("\n=== What happens if two sources drive the bus ===")
    try:
        dp.clock({"PC_OUT", "A_OUT", "B_IN"})
    except BusConflict as error:
        print(f"  {error}")


if __name__ == "__main__":
    main()
