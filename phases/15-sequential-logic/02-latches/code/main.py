from sim.logic import LogicCircuit


def nor_sr_latch():
    lc = LogicCircuit("NOR SR latch")
    lc.inputs("s", "r")
    lc.nor("q", "r", "qb")
    lc.nor("qb", "s", "q")
    lc.outputs("q", "qb")
    return lc


def nand_sr_latch():
    lc = LogicCircuit("NAND S'R' latch")
    lc.inputs("sn", "rn")
    lc.nand("q", "sn", "qb")
    lc.nand("qb", "rn", "q")
    lc.outputs("q", "qb")
    return lc


def d_latch():
    lc = LogicCircuit("gated D latch")
    lc.inputs("en", "d")
    lc.not_("nd", "d")
    lc.nand("sn", "d", "en")
    lc.nand("rn", "nd", "en")
    lc.nand("q", "sn", "qb")
    lc.nand("qb", "rn", "q")
    lc.outputs("q", "qb")
    return lc


def unit_delay_run(lc, start, steps):
    values = dict(start)
    history = [dict(values)]
    for _ in range(steps):
        values = {**values, **{gate.output: gate.evaluate(values) for gate in lc.gates}}
        history.append(dict(values))
    return history


def run(lc, sequence, names):
    rows = []
    for inputs in sequence:
        out = lc.evaluate(inputs)
        rows.append({**inputs, **{n: out[n] for n in names}})
    return rows


def show(rows):
    keys = list(rows[0])
    print("  " + " ".join(f"{k:>3}" for k in keys))
    for row in rows:
        print("  " + " ".join(f"{row[k]:>3}" for k in keys))


def main():
    print("=== NOR SR latch: set, hold, reset, hold ===")
    nor = nor_sr_latch()
    show(run(nor, [{"s": 1, "r": 0}, {"s": 0, "r": 0}, {"s": 0, "r": 1}, {"s": 0, "r": 0}], ["q", "qb"]))

    print("\n=== The forbidden input s = r = 1 ===")
    out = nor.evaluate({"s": 1, "r": 1})
    print(f"  s = r = 1: q = {out['q']}, qb = {out['qb']}  (both 0: q and qb are no longer opposites)")
    print("  now release both inputs at the same instant, every gate 1 time unit:")
    history = unit_delay_run(nor, {"s": 0, "r": 0, "q": 0, "qb": 0}, 6)
    for t, values in enumerate(history):
        print(f"    t = {t}: q = {values['q']}, qb = {values['qb']}")
    print("  with perfectly equal gates the latch never decides; real gates differ slightly, so it falls")
    print("  to a random side after a while. That is why s = r = 1 is forbidden.")

    print("\n=== NAND S'R' latch: active-low inputs ===")
    nand = nand_sr_latch()
    show(run(nand, [{"sn": 0, "rn": 1}, {"sn": 1, "rn": 1}, {"sn": 1, "rn": 0}, {"sn": 1, "rn": 1}], ["q", "qb"]))

    print("\n=== Gated D latch: transparent while en = 1, holds while en = 0 ===")
    latch = d_latch()
    sequence = [
        {"en": 1, "d": 1}, {"en": 1, "d": 0}, {"en": 1, "d": 1},
        {"en": 0, "d": 1}, {"en": 0, "d": 0}, {"en": 0, "d": 1}, {"en": 0, "d": 0},
        {"en": 1, "d": 0}, {"en": 0, "d": 1},
    ]
    rows = run(latch, sequence, ["q"])
    show(rows)
    held = all(rows[i]["q"] == rows[i - 1]["q"] for i, inputs in enumerate(sequence) if i and inputs["en"] == 0)
    follows = all(row["q"] == row["d"] for row in rows if row["en"] == 1)
    print(f"  q == d whenever en = 1: {follows}; q unchanged whenever en = 0: {held}")
    print(f"  gates: {latch.gate_count()} ({latch.counts()['nand']} NAND + 1 NOT); no forbidden input is possible")


if __name__ == "__main__":
    main()
