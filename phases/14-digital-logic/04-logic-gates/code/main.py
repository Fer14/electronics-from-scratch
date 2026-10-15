from sim.logic import LogicCircuit

TWO_INPUT_GATES = ["and", "or", "nand", "nor", "xor", "xnor"]


def all_gates():
    lc = LogicCircuit("the basic gates")
    lc.inputs("a", "b")
    lc.not_("not_a", "a")
    for op in TWO_INPUT_GATES:
        lc.gate(op, ["a", "b"], op)
    lc.outputs("not_a", *TWO_INPUT_GATES)
    return lc


def from_nand_only():
    lc = LogicCircuit("NOT, AND, OR from NAND")
    lc.inputs("a", "b")
    lc.nand("not_a", "a", "a")
    lc.nand("t", "a", "b")
    lc.nand("and_ab", "t", "t")
    lc.nand("na", "a", "a")
    lc.nand("nb", "b", "b")
    lc.nand("or_ab", "na", "nb")
    lc.outputs("not_a", "and_ab", "or_ab")
    return lc


def from_nor_only():
    lc = LogicCircuit("NOT, OR, AND from NOR")
    lc.inputs("a", "b")
    lc.nor("not_a", "a", "a")
    lc.nor("t", "a", "b")
    lc.nor("or_ab", "t", "t")
    lc.nor("na", "a", "a")
    lc.nor("nb", "b", "b")
    lc.nor("and_ab", "na", "nb")
    lc.outputs("not_a", "or_ab", "and_ab")
    return lc


def xor_from_nands():
    lc = LogicCircuit("XOR from four NANDs")
    lc.inputs("a", "b")
    lc.nand("n1", "a", "b")
    lc.nand("n2", "a", "n1")
    lc.nand("n3", "b", "n1")
    lc.nand("y", "n2", "n3")
    lc.outputs("y")
    return lc


def column(lc, output):
    return [row[output] for row in lc.truth_table(outputs=[output])]


def main():
    print("=== Truth tables of the basic gates (rows: ab = 00, 01, 10, 11) ===")
    gates = all_gates()
    for name in ["not_a"] + TWO_INPUT_GATES:
        print(f"  {name:6s} {column(gates, name)}")

    print("\n=== NAND is universal ===")
    nand_only = from_nand_only()
    print(f"  NOT a from NAND(a, a)          : {column(nand_only, 'not_a')}  (expected {column(gates, 'not_a')})")
    print(f"  a AND b from NAND then NAND    : {column(nand_only, 'and_ab')}  (expected {column(gates, 'and')})")
    print(f"  a OR b from NAND(a', b')        : {column(nand_only, 'or_ab')}  (expected {column(gates, 'or')})")
    print(f"  NAND gates used: {nand_only.counts()['nand']}")

    print("\n=== NOR is universal too ===")
    nor_only = from_nor_only()
    print(f"  NOT a  : {column(nor_only, 'not_a')}")
    print(f"  a OR b : {column(nor_only, 'or_ab')}")
    print(f"  a AND b: {column(nor_only, 'and_ab')}")

    print("\n=== XOR from four NANDs ===")
    xor4 = xor_from_nands()
    print(xor4.format_truth_table(outputs=["n1", "n2", "n3", "y"]))
    print(f"  matches XOR: {column(xor4, 'y') == column(gates, 'xor')}")
    print(f"  logic depth: {xor4.depth()} gate delays (a single XOR gate: 1)")

    print("\n=== Watching the signal ripple through, one time unit per gate ===")
    changes = xor4.events(before={"a": 0, "b": 0}, after={"a": 1})
    for time, wire, value in changes:
        print(f"  t = {time}: {wire} -> {value}")
    tpd_ns = 8
    print(f"  with a 74HC00 at 5 V (about {tpd_ns} ns per gate), y settles after about {xor4.depth() * tpd_ns} ns in the worst case")


if __name__ == "__main__":
    main()
