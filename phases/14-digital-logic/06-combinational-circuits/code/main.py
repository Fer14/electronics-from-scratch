from itertools import product

from sim.logic import LogicCircuit

SEGMENTS = {
    0: "abcdef", 1: "bc", 2: "abdeg", 3: "abcdg", 4: "bcfg",
    5: "acdfg", 6: "acdefg", 7: "abc", 8: "abcdefg", 9: "abcdfg",
}


def comparator():
    lc = LogicCircuit("2-bit comparator")
    lc.inputs("a1", "a0", "b1", "b0")
    lc.xnor("e1", "a1", "b1")
    lc.xnor("e0", "a0", "b0")
    lc.and_("eq", "e1", "e0")
    lc.not_("nb1", "b1")
    lc.not_("nb0", "b0")
    lc.and_("g1", "a1", "nb1")
    lc.and_("g0", "e1", "a0", "nb0")
    lc.or_("gt", "g1", "g0")
    lc.outputs("eq", "gt")
    return lc


def segment_a():
    lc = LogicCircuit("segment a of a BCD display")
    lc.inputs("A", "B", "C", "D")
    lc.not_("nB", "B")
    lc.not_("nD", "D")
    lc.and_("BD", "B", "D")
    lc.and_("nBnD", "nB", "nD")
    lc.or_("a", "A", "C", "BD", "nBnD")
    lc.outputs("a")
    return lc


def hazard_circuit(with_cover=False):
    lc = LogicCircuit("y = a·b + a'·c" + (" + b·c" if with_cover else ""))
    lc.inputs("a", "b", "c")
    lc.not_("na", "a")
    lc.and_("p", "a", "b")
    lc.and_("q", "na", "c")
    if with_cover:
        lc.and_("r", "b", "c")
        lc.or_("y", "p", "q", "r")
    else:
        lc.or_("y", "p", "q")
    lc.outputs("y")
    return lc


def check_comparator(lc):
    wrong = 0
    for a1, a0, b1, b0 in product((0, 1), repeat=4):
        a, b = 2 * a1 + a0, 2 * b1 + b0
        out = lc.evaluate({"a1": a1, "a0": a0, "b1": b1, "b0": b0})
        wrong += out["eq"] != int(a == b)
        wrong += out["gt"] != int(a > b)
    return wrong


def main():
    print("=== 2-bit magnitude comparator ===")
    cmp2 = comparator()
    print("   A  B | eq gt")
    for a1, a0, b1, b0 in product((0, 1), repeat=4):
        out = cmp2.evaluate({"a1": a1, "a0": a0, "b1": b1, "b0": b0})
        print(f"   {2 * a1 + a0}  {2 * b1 + b0} |  {out['eq']}  {out['gt']}")
    print(f"  checked against Python's == and > for all 16 rows: {check_comparator(cmp2)} wrong")
    print(f"  gates: {cmp2.gate_count()}, logic depth: {cmp2.depth()}")

    print("\n=== Segment 'a' of a 7-segment display, BCD input ABCD ===")
    seg = segment_a()
    wrong = 0
    for digit in range(10):
        bits = dict(zip("ABCD", (int(x) for x in f"{digit:04b}")))
        lit = seg.evaluate(bits)["a"]
        wanted = int("a" in SEGMENTS[digit])
        wrong += lit != wanted
        print(f"  digit {digit} = {digit:04b}: segment a = {lit} (should be {wanted})")
    print(f"  a = A + C + B·D + B'·D' is right for all ten digits: {wrong == 0}; inputs 10-15 are don't-cares")
    minterms = sum(1 for d in range(10) if "a" in SEGMENTS[d])
    print(f"  unsimplified: {minterms} minterms of 4 literals each; simplified: {seg.gate_count()} gates")

    print("\n=== A glitch: y = a·b + a'·c with b = c = 1, a falls from 1 to 0 ===")
    for cover in (False, True):
        lc = hazard_circuit(cover)
        changes = lc.events(before={"a": 1, "b": 1, "c": 1}, after={"a": 0})
        trace = ", ".join(f"t={t}: {w}->{v}" for t, w, v in changes)
        y_values = [v for t, w, v in changes if w == "y"]
        print(f"  {lc.name}")
        print(f"    {trace}")
        print(f"    y changed {len(y_values)} times {'(glitch!)' if y_values else '(clean)'}")

    print("\n=== Delay estimate ===")
    tpd = 8e-9
    for lc in (cmp2, seg):
        print(f"  {lc.name}: depth {lc.depth()} x {tpd * 1e9:.0f} ns = {lc.depth() * tpd * 1e9:.0f} ns worst case")


if __name__ == "__main__":
    main()
