from itertools import product

from sim.logic import LogicCircuit

STATES = {"A": (0, 0), "B": (0, 1), "C": (1, 0), "D": (1, 1)}
NAMES = {code: name for name, code in STATES.items()}
TRANSITIONS = {
    ("A", 0): "A", ("A", 1): "B",
    ("B", 0): "C", ("B", 1): "B",
    ("C", 0): "A", ("C", 1): "D",
    ("D", 0): "C", ("D", 1): "B",
}


def detector():
    lc = LogicCircuit("Moore detector for 101")
    lc.inputs("x")
    lc.not_("nx", "x")
    lc.not_("ns0", "s0")
    lc.and_("p", "s0", "nx")
    lc.and_("r", "s1", "ns0", "x")
    lc.or_("n1", "p", "r")
    lc.dff("x", "s0", name="S0")
    lc.dff("n1", "s1", name="S1")
    lc.and_("z", "s1", "s0")
    lc.outputs("s1", "s0", "z")
    return lc


def table_from_transitions():
    rows = []
    for (s1, s0), x in product(STATES.values(), (0, 1)):
        nxt = STATES[TRANSITIONS[(NAMES[(s1, s0)], x)]]
        rows.append((s1, s0, x, nxt[0], nxt[1]))
    return rows


def reference(bits):
    return [int(k >= 2 and bits[k - 2:k + 1] == [1, 0, 1]) for k in range(len(bits))]


def main():
    print("=== State table of the 101 detector (A = 00, B = 01, C = 10, D = 11) ===")
    print("  s1 s0 x | s1+ s0+   from -> to")
    for s1, s0, x, n1, n0 in table_from_transitions():
        print(f"   {s1}  {s0} {x} |  {n1}   {n0}     {NAMES[(s1, s0)]} --x={x}--> {NAMES[(n1, n0)]}")
    print("  s0+ column equals x; s1+ is 1 only on rows 010, 101, 110 -> s1+ = s0·x' + s1·s0'·x")

    print("\n=== Check the gate-level next-state logic against the table ===")
    lc = detector()
    wrong = 0
    for s1, s0, x, n1, n0 in table_from_transitions():
        values = lc.settle({"s1": s1, "s0": s0, "x": x})
        wrong += values["n1"] != n1 or x != n0
    print(f"  8 rows, {wrong} wrong")
    print(f"  gates {lc.gate_count()}, flip-flops {lc.counts()['dff']}, depth {lc.depth()}")

    print("\n=== Run it on an input stream ===")
    stream = [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1]
    lc = detector()
    lc.reset()
    states, outputs = [], []
    for bit in stream:
        out = lc.step({"x": bit})
        states.append(NAMES[(out["s1"], out["s0"])])
        outputs.append(out["z"])
    print(f"  x     : {' '.join(map(str, stream))}")
    print(f"  state : {' '.join(states)}")
    print(f"  z     : {' '.join(map(str, outputs))}")
    print(f"  string search says: {' '.join(map(str, reference(stream)))}")
    print(f"  match: {outputs == reference(stream)}; found {sum(outputs)} occurrences, overlapping ones included")

    print("\n=== One-hot encoding of the same machine needs 4 flip-flops ===")
    print("  binary: 2 flip-flops, next-state logic as above")
    print("  one-hot: A=0001 B=0010 C=0100 D=1000; each next-state bit is an OR of the arrows into that state:")
    for target in "ABCD":
        sources = [f"{s}·{'x' if x else 'x' + chr(39)}" for (s, x), t in TRANSITIONS.items() if t == target]
        print(f"    {target}+ = {' + '.join(sources)}")


if __name__ == "__main__":
    main()
