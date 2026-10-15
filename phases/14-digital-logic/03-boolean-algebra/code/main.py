from itertools import product

from sim.logic import LogicCircuit


def column(lc, output):
    return [row[output] for row in lc.truth_table(outputs=[output])]


def greenhouse_sop():
    lc = LogicCircuit("a·b + b·c")
    lc.inputs("a", "b", "c")
    lc.and_("ab", "a", "b")
    lc.and_("bc", "b", "c")
    lc.or_("y", "ab", "bc")
    lc.outputs("y")
    return lc


def greenhouse_factored():
    lc = LogicCircuit("b·(a + c)")
    lc.inputs("a", "b", "c")
    lc.or_("a_or_c", "a", "c")
    lc.and_("y", "b", "a_or_c")
    lc.outputs("y")
    return lc


def greenhouse_nand():
    lc = LogicCircuit("NAND(NAND(a,b), NAND(b,c))")
    lc.inputs("a", "b", "c")
    lc.nand("n1", "a", "b")
    lc.nand("n2", "b", "c")
    lc.nand("y", "n1", "n2")
    lc.outputs("y")
    return lc


def de_morgan():
    lc = LogicCircuit("De Morgan")
    lc.inputs("a", "b")
    lc.nand("not_both", "a", "b")
    lc.not_("na", "a")
    lc.not_("nb", "b")
    lc.or_("na_or_nb", "na", "nb")
    lc.nor("neither", "a", "b")
    lc.and_("na_and_nb", "na", "nb")
    lc.outputs("not_both", "na_or_nb", "neither", "na_and_nb")
    return lc


def sum_of_products(names, outputs):
    terms = []
    for bits, out in zip(product((0, 1), repeat=len(names)), outputs):
        if out:
            terms.append("·".join(n if b else n + "'" for n, b in zip(names, bits)))
    return " + ".join(terms)


def karnaugh_map(outputs):
    order = ["00", "01", "11", "10"]
    lines = ["          bc=00 bc=01 bc=11 bc=10"]
    for a in (0, 1):
        cells = [str(outputs[4 * a + int(bc, 2)]) for bc in order]
        lines.append(f"    a={a}     " + "     ".join(cells))
    return "\n".join(lines)


def main():
    print("=== Greenhouse fan, three circuits ===")
    circuits = [greenhouse_sop(), greenhouse_factored(), greenhouse_nand()]
    print(circuits[0].format_truth_table())
    for lc in circuits:
        print(f"  {lc.name:28s} y column = {column(lc, 'y')}  gates = {lc.gate_count()}  {lc.counts()}")
    same = all(column(lc, "y") == column(circuits[0], "y") for lc in circuits)
    print(f"  all three have the same truth table: {same}")

    print("\n=== De Morgan by truth table ===")
    dm = de_morgan()
    print(dm.format_truth_table())
    print(f"  (a·b)' == a' + b' : {column(dm, 'not_both') == column(dm, 'na_or_nb')}")
    print(f"  (a+b)' == a'·b'   : {column(dm, 'neither') == column(dm, 'na_and_nb')}")

    print("\n=== From the truth table back to an expression ===")
    y = column(circuits[0], "y")
    print(f"  sum of minterms: y = {sum_of_products(['a', 'b', 'c'], y)}")
    print("  Karnaugh map:")
    print(karnaugh_map(y))
    print("  groups: column bc=11 -> b·c, row a=1 cols 11,10 -> a·b  =>  y = a·b + b·c = b·(a + c)")


if __name__ == "__main__":
    main()
