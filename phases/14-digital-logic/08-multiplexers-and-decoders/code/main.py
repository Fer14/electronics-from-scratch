from itertools import product

from sim.logic import LogicCircuit


def add_mux2(lc, s, a, b, y, tag):
    lc.not_(f"{tag}.ns", s)
    lc.and_(f"{tag}.p", a, f"{tag}.ns")
    lc.and_(f"{tag}.q", b, s)
    lc.or_(y, f"{tag}.p", f"{tag}.q")


def mux2():
    lc = LogicCircuit("2-to-1 mux")
    lc.inputs("s", "a", "b")
    add_mux2(lc, "s", "a", "b", "y", "m")
    lc.outputs("y")
    return lc


def add_mux4(lc, s1, s0, d, y, tag):
    add_mux2(lc, s0, d[0], d[1], f"{tag}.low", f"{tag}.m0")
    add_mux2(lc, s0, d[2], d[3], f"{tag}.high", f"{tag}.m1")
    add_mux2(lc, s1, f"{tag}.low", f"{tag}.high", y, f"{tag}.m2")


def mux4_tree():
    lc = LogicCircuit("4-to-1 mux from three 2-to-1 muxes")
    lc.inputs("s1", "s0", "d0", "d1", "d2", "d3")
    add_mux4(lc, "s1", "s0", ["d0", "d1", "d2", "d3"], "y", "mux")
    lc.outputs("y")
    return lc


def add_decoder2(lc, a1, a0, en, outs):
    lc.not_("na1", a1)
    lc.not_("na0", a0)
    lc.and_(outs[0], en, "na1", "na0")
    lc.and_(outs[1], en, "na1", a0)
    lc.and_(outs[2], en, a1, "na0")
    lc.and_(outs[3], en, a1, a0)


def decoder2():
    lc = LogicCircuit("2-to-4 decoder with enable")
    lc.inputs("en", "a1", "a0")
    add_decoder2(lc, "a1", "a0", "en", ["y0", "y1", "y2", "y3"])
    lc.outputs("y0", "y1", "y2", "y3")
    return lc


def demux4():
    lc = LogicCircuit("1-to-4 demux")
    lc.inputs("a1", "a0", "data")
    add_decoder2(lc, "a1", "a0", "data", ["o0", "o1", "o2", "o3"])
    lc.outputs("o0", "o1", "o2", "o3")
    return lc


def lut2(table):
    lc = LogicCircuit("2-input lookup table")
    lc.inputs("a", "b")
    stored = [lc.constant(f"k{i}", bit) for i, bit in enumerate(table)]
    add_mux4(lc, "a", "b", stored, "y", "lut")
    lc.outputs("y")
    return lc


def column(lc, output):
    return [row[output] for row in lc.truth_table(outputs=[output])]


def main():
    print("=== 2-to-1 multiplexer: y = s'·a + s·b ===")
    m = mux2()
    print(m.format_truth_table())

    print("\n=== 4-to-1 multiplexer built as a tree ===")
    m4 = mux4_tree()
    data = {"d0": 1, "d1": 0, "d2": 0, "d3": 1}
    for s1, s0 in product((0, 1), repeat=2):
        y = m4.evaluate({"s1": s1, "s0": s0, **data})["y"]
        print(f"  select {s1}{s0} -> y = {y}  (d{2 * s1 + s0} = {data[f'd{2 * s1 + s0}']})")
    wrong = 0
    for bits in product((0, 1), repeat=6):
        inputs = dict(zip(m4.input_names, bits))
        wanted = inputs[f"d{2 * inputs['s1'] + inputs['s0']}"]
        wrong += m4.evaluate(inputs)["y"] != wanted
    print(f"  checked all 64 input combinations: {wrong} wrong; gates {m4.gate_count()}, depth {m4.depth()}")

    print("\n=== 2-to-4 decoder ===")
    d = decoder2()
    print(d.format_truth_table())

    print("\n=== 1-to-4 demultiplexer: the data bit goes to the addressed output ===")
    dm = demux4()
    for a1, a0 in product((0, 1), repeat=2):
        out = dm.evaluate({"a1": a1, "a0": a0, "data": 1})
        print(f"  address {a1}{a0}, data 1 -> o0..o3 = {out['o0']} {out['o1']} {out['o2']} {out['o3']}")

    print("\n=== A 4-to-1 mux is a lookup table for any 2-input function ===")
    for name, table in [("AND", [0, 0, 0, 1]), ("XOR", [0, 1, 1, 0]), ("NAND", [1, 1, 1, 0]), ("a' + b (a implies b)", [1, 1, 0, 1])]:
        lut = lut2(table)
        print(f"  stored bits {table} -> truth table {column(lut, 'y')}  = {name}")
    print(f"  a 2-input LUT can be any of 2^(2^2) = {2 ** 4} functions; a 6-input LUT, as in many FPGAs, any of 2^64")


if __name__ == "__main__":
    main()
