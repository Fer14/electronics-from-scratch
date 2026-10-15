from sim import engineering
from sim.logic import LogicCircuit


def add_d_latch(lc, en, d, q, tag):
    lc.not_(f"{tag}.nd", d)
    lc.nand(f"{tag}.sn", d, en)
    lc.nand(f"{tag}.rn", f"{tag}.nd", en)
    lc.nand(q, f"{tag}.sn", f"{tag}.qb")
    lc.nand(f"{tag}.qb", f"{tag}.rn", q)


def master_slave(feedback=False):
    lc = LogicCircuit("master-slave D flip-flop" + (" with d = NOT q" if feedback else ""))
    lc.inputs("clk") if feedback else lc.inputs("clk", "d")
    lc.not_("nclk", "clk")
    if feedback:
        lc.not_("d", "q")
    add_d_latch(lc, "nclk", "d", "m", "master")
    add_d_latch(lc, "clk", "m", "q", "slave")
    lc.outputs("m", "q")
    return lc


def single_latch_toggle():
    lc = LogicCircuit("one latch with d = NOT q")
    lc.inputs("clk")
    lc.not_("d", "q")
    add_d_latch(lc, "clk", "d", "q", "only")
    lc.outputs("q")
    return lc


def waveform(values):
    return "".join("‾" if v else "_" for v in values)


def main():
    print("=== Master-slave D flip-flop built from two NAND D latches ===")
    ff = master_slave()
    clk = [0, 1] * 6
    d = [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1]
    m_trace, q_trace = [], []
    ff.evaluate({"clk": 0, "d": 0})
    ff.evaluate({"clk": 1, "d": 0})
    for c, data in zip(clk, d):
        out = ff.evaluate({"clk": c, "d": data})
        m_trace.append(out["m"])
        q_trace.append(out["q"])
    print(f"  clk {waveform(clk)}")
    print(f"  d   {waveform(d)}")
    print(f"  m   {waveform(m_trace)}   master: follows d while clk = 0")
    print(f"  q   {waveform(q_trace)}   slave:  changes only when clk rises")
    sampled = [d[i - 1] for i in range(1, len(clk)) if clk[i] == 1 and clk[i - 1] == 0]
    q_after = [q_trace[i] for i in range(1, len(clk)) if clk[i] == 1 and clk[i - 1] == 0]
    print(f"  d just before each rising edge: {sampled}")
    print(f"  q just after each rising edge:  {q_after}")
    print(f"  gates: {ff.gate_count()}")

    print("\n=== The same behaviour from sim.logic's built-in flip-flop ===")
    lc = LogicCircuit("built-in dff")
    lc.inputs("d")
    lc.dff("d", "q")
    lc.outputs("q")
    edge_d = [0, 1, 1, 0, 1, 0]
    q_values = [lc.step({"d": value})["q"] for value in edge_d]
    print(f"  d at each edge: {edge_d}")
    print(f"  q after edge:   {q_values}")
    print(f"  matches the gate-level flip-flop: {q_values == q_after}")

    print("\n=== Toggle: d = NOT q ===")
    try:
        single_latch_toggle().evaluate({"clk": 1})
        print("  one transparent latch: settled (unexpected)")
    except Exception as error:
        print(f"  one transparent latch with clk = 1: {error}")
    toggle = master_slave(feedback=True)
    toggle.evaluate({"clk": 0})
    toggle.evaluate({"clk": 1})
    q_seen = []
    for c in [0, 1] * 5:
        q_seen.append(toggle.evaluate({"clk": c})["q"])
    print(f"  master-slave flip-flop: clk {waveform([0, 1] * 5)}")
    print(f"                          q   {waveform(q_seen)}   one toggle per rising edge, half the clock frequency")

    print("\n=== A clock in numbers ===")
    for f in [1e3, 16e6, 3.2e9]:
        period = 1 / f
        print(f"  f = {engineering(f, 'Hz'):>9s} -> period {engineering(period, 's'):>9s}, high for {engineering(period / 2, 's')} at 50 % duty")


if __name__ == "__main__":
    main()
