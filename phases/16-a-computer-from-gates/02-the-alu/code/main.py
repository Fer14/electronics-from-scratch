import random

from sim.logic import LogicCircuit

BITS = 8
OPS = ["ADD", "SUB", "AND", "OR", "XOR"]


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
    lc.gate("buf", ["r7"], "N")
    lc.outputs(*[f"r{i}" for i in range(BITS)], "Z", "C", "N")
    return lc


def reference_alu(op, a, b):
    if op == 0:
        total = a + b
        return total & 0xFF, int(total > 0xFF)
    if op == 1:
        total = a + ((~b) & 0xFF) + 1
        return total & 0xFF, int(total > 0xFF)
    results = {2: a & b, 3: a | b, 4: a ^ b}
    return results[op], 0


def apply(alu, op, a, b):
    inputs = {f"a{i}": (a >> i) & 1 for i in range(BITS)}
    inputs.update({f"b{i}": (b >> i) & 1 for i in range(BITS)})
    inputs.update({"op2": (op >> 2) & 1, "op1": (op >> 1) & 1, "op0": op & 1})
    out = alu.evaluate(inputs)
    result = sum(out[f"r{i}"] << i for i in range(BITS))
    return result, out["Z"], out["C"], out["N"]


def main():
    alu = build_alu()
    print("=== The T8 ALU, gate by gate ===")
    print(f"  {alu.gate_count()} gates: {alu.counts()}")
    print(f"  logic depth (critical path): {alu.depth()} gate delays")

    print("\n=== A few operations ===")
    for op, a, b in [(0, 25, 17), (0, 200, 100), (1, 25, 17), (1, 17, 25), (1, 42, 42), (2, 0b11001100, 0b10101010), (3, 0b11001100, 0b10101010), (4, 0b11001100, 0b10101010)]:
        r, z, c, n = apply(alu, op, a, b)
        print(f"  {OPS[op]:3s} {a:3d} ({a:08b}), {b:3d} ({b:08b}) -> {r:3d} ({r:08b})  Z={z} C={c} N={n}")

    print("\n=== Check against the reference model of Lesson 01 ===")
    rng = random.Random(16)
    special = [0, 1, 127, 128, 254, 255]
    pairs = [(x, y) for x in special for y in special] + [(rng.randrange(256), rng.randrange(256)) for _ in range(300)]
    wrong = 0
    for op in range(5):
        for a, b in pairs:
            r, z, c, n = apply(alu, op, a, b)
            want, want_c = reference_alu(op, a, b)
            wrong += (r, z, c, n) != (want, int(want == 0), want_c, want >> 7)
    print(f"  {5 * len(pairs)} cases (5 operations x {len(pairs)} operand pairs): {wrong} wrong")

    print("\n=== Where the time goes ===")
    tpd = 15e-12
    print(f"  depth {alu.depth()} x {tpd * 1e12:.0f} ps per gate = {alu.depth() * tpd * 1e12:.0f} ps: most of it is the 8-stage carry chain")
    print(f"  with 74HC gates at 8 ns: {alu.depth() * 8} ns, so a breadboard T8 could not clock much faster than ~{1e3 / (alu.depth() * 8 + 20):.0f} MHz")


if __name__ == "__main__":
    main()
