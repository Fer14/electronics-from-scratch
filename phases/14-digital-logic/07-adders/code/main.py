import random
from itertools import product

from sim.logic import LogicCircuit


def half_adder():
    lc = LogicCircuit("half adder")
    lc.inputs("a", "b")
    lc.xor("s", "a", "b")
    lc.and_("c", "a", "b")
    lc.outputs("s", "c")
    return lc


def add_full_adder(lc, a, b, cin, s, cout, tag):
    lc.xor(f"{tag}.p", a, b)
    lc.xor(s, f"{tag}.p", cin)
    lc.and_(f"{tag}.g", a, b)
    lc.and_(f"{tag}.t", f"{tag}.p", cin)
    lc.or_(cout, f"{tag}.g", f"{tag}.t")


def full_adder():
    lc = LogicCircuit("full adder")
    lc.inputs("a", "b", "cin")
    add_full_adder(lc, "a", "b", "cin", "s", "cout", "fa")
    lc.outputs("s", "cout")
    return lc


def add_sub(bits):
    lc = LogicCircuit(f"{bits}-bit adder/subtractor")
    a = [f"a{i}" for i in range(bits)]
    b = [f"b{i}" for i in range(bits)]
    lc.inputs(*a, *b, "sub")
    carry = "sub"
    for i in range(bits):
        lc.xor(f"bx{i}", b[i], "sub")
        add_full_adder(lc, a[i], f"bx{i}", carry, f"s{i}", f"c{i + 1}", f"fa{i}")
        carry = f"c{i + 1}"
    lc.xor("v", f"c{bits - 1}", f"c{bits}")
    lc.outputs(*[f"s{i}" for i in range(bits)], f"c{bits}", "v")
    return lc


def drive(bits, x, y, sub=0):
    inputs = {f"a{i}": (x >> i) & 1 for i in range(bits)}
    inputs.update({f"b{i}": (y >> i) & 1 for i in range(bits)})
    inputs["sub"] = sub
    return inputs


def read(out, bits):
    total = sum(out[f"s{i}"] << i for i in range(bits))
    return total, out[f"c{bits}"], out["v"]


def signed(x, bits):
    return x - (1 << bits) if x >> (bits - 1) else x


def main():
    print("=== Half adder ===")
    print(half_adder().format_truth_table())

    print("\n=== Full adder ===")
    fa = full_adder()
    print(fa.format_truth_table())
    wrong = sum(int(2 * r["cout"] + r["s"] != r["a"] + r["b"] + r["cin"]) for r in fa.truth_table())
    print(f"  2 x cout + s == a + b + cin in every row: {wrong == 0}")
    print(f"  gates: {fa.gate_count()}, depth: {fa.depth()}")

    print("\n=== 4-bit adder/subtractor, checked exhaustively ===")
    adder4 = add_sub(4)
    errors = 0
    for x, y, sub in product(range(16), range(16), (0, 1)):
        total, _, _ = read(adder4.evaluate(drive(4, x, y, sub)), 4)
        wanted = (x - y) % 16 if sub else (x + y) % 16
        errors += total != wanted
    print(f"  512 cases (256 additions, 256 subtractions): {errors} wrong")
    for x, y, sub in [(3, 4, 0), (6, 7, 0), (9, 9, 0), (2, 5, 1), (12, 5, 1)]:
        total, carry, overflow = read(adder4.evaluate(drive(4, x, y, sub)), 4)
        op = "-" if sub else "+"
        print(f"  {x:2d} {op} {y:2d}: bits {total:04b} = {total:2d} unsigned / {signed(total, 4):3d} signed, carry {carry}, overflow {overflow}")

    print("\n=== 8-bit adder, 2000 random cases ===")
    adder8 = add_sub(8)
    rng = random.Random(7)
    errors = 0
    for _ in range(2000):
        x, y, sub = rng.randrange(256), rng.randrange(256), rng.randrange(2)
        total, carry, overflow = read(adder8.evaluate(drive(8, x, y, sub)), 8)
        wanted = (x - y) % 256 if sub else (x + y) % 256
        true_signed = signed(x, 8) - signed(y, 8) if sub else signed(x, 8) + signed(y, 8)
        errors += total != wanted or overflow != int(not -128 <= true_signed <= 127)
    print(f"  sums, differences and overflow flags: {errors} wrong")
    total, carry, overflow = read(adder8.evaluate(drive(8, 100, 50)), 8)
    print(f"  100 + 50 -> {total} unsigned, {signed(total, 8)} signed, overflow flag {overflow}")
    total, carry, overflow = read(adder8.evaluate(drive(8, 200, 100)), 8)
    print(f"  200 + 100 -> {total}, carry {carry} (300 does not fit in 8 bits)")

    print("\n=== The carry ripples: 1111 + 0001 ===")
    changes = adder4.events(before=drive(4, 15, 0), after={"b0": 1})
    carries = [(t, w) for t, w, v in changes if w.startswith("c")]
    print("  " + ", ".join(f"{w} at t={t}" for t, w in carries))
    print(f"  last sum bit settles at t = {max(t for t, w, v in changes if w.startswith('s'))}")

    print("\n=== Depth grows with width ===")
    tpd_ns = 8
    for bits in (4, 8, 16, 32):
        depth = add_sub(bits).depth()
        print(f"  {bits:2d}-bit ripple adder/subtractor: depth {depth:3d} gate delays, about {depth * tpd_ns} ns with 74HC gates")


if __name__ == "__main__":
    main()
