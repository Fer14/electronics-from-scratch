from pathlib import Path

from sim import cost
from sim.lab import evaluate, load_task
from sim.logic import LogicCircuit, full_adder

GATE_DELAY_PS = 20.0


def describe(design):
    path = design.critical_path()
    period = path * GATE_DELAY_PS
    return (f"area {design.area():5.0f} gates, critical path {path:3d} gate delays = {period:5.0f} ps"
            f" -> {design.max_clock_mhz():6.0f} MHz, latency {design.latency()} cycles")


def mac_datapath(split):
    d = cost.Design("MAC datapath")
    d.add("R_IN", cost.register(16), "in", "operands")
    d.add("MUL", cost.multiplier(8), "operands", "product")
    if split:
        d.add("R_MID", cost.register(16), "product", "product_q")
        d.add("ADD", cost.adder(24), "product_q", "sum")
    else:
        d.add("ADD", cost.adder(24), "product", "sum")
    d.add("ACC", cost.register(24), "sum", "acc")
    return d


def accumulator(registers_in_loop, bits=8):
    lc = LogicCircuit(f"accumulator with {registers_in_loop} register(s) in the loop")
    x = [f"x{i}" for i in range(bits)]
    lc.inputs(*x)
    lc.constant("zero", 0)
    acc = [f"acc{i}" for i in range(bits)]
    total = [f"sum{i}" for i in range(bits)]
    carry = "zero"
    for i in range(bits):
        full_adder(lc, acc[i], x[i], carry, total[i], f"k{i + 1}", tag=f"fa{i}")
        carry = f"k{i + 1}"
    stage = total
    for r in range(registers_in_loop):
        q = acc if r == registers_in_loop - 1 else [f"mid{r}_{i}" for i in range(bits)]
        lc.register(f"R{r}", stage, q)
        stage = q
    lc.outputs(*acc)
    return lc


def run_accumulator(lc, values, bits=8):
    lc.reset()
    seen = []
    for v in values:
        lc.step({f"x{i}": (v >> i) & 1 for i in range(bits)})
        seen.append(sum(lc.values[f"acc{i}"] << i for i in range(bits)))
    return seen


def main():
    print("Step 1: an 8-bit MAC datapath, unpipelined")
    print("  " + describe(mac_datapath(split=False)))

    print("\nStep 2: one pipeline register between the multiplier and the adder")
    print("  " + describe(mac_datapath(split=True)))

    print("\nStep 3: pipelining the multiplier itself (sim.cost.pipelined_multiplier)")
    for stages in (1, 2, 3, 4, 6):
        block = cost.pipelined_multiplier(8, stages)
        d = cost.Design("multiplier")
        d.add("R_IN", cost.register(16), "in", "x")
        d.add("MUL", block, "x", "out")
        print(f"  {stages} stage(s): stage delay {block.stage_delay:2d} gate delays,"
              f" {d.max_clock_mhz():5.0f} MHz, multiplier area {block.area:5.0f} gates")

    print("\nStep 4: the accumulator loop cannot be pipelined away")
    loop = cost.Design("loop without a register")
    loop.add("ADD", cost.adder(24), "acc", "acc")
    try:
        loop.critical_path()
    except ValueError as error:
        print(f"  no register in the loop: {error}")
    for regs in (1, 2):
        d = cost.Design("loop")
        d.add("ADD", cost.adder(24), "acc", "sum")
        node = "sum"
        for r in range(regs):
            nxt = "acc" if r == regs - 1 else f"q{r}"
            d.add(f"R{r}", cost.register(24), node, nxt)
            node = nxt
        print(f"  {regs} register(s) in the loop: critical path {d.critical_path()} gate delays")

    print("\nStep 5: what the extra loop register does to the answer (gate level)")
    values = [5, 3, 10, 1, 7, 2]
    running = [sum(values[: n + 1]) for n in range(len(values))]
    print(f"  inputs              {values}")
    print(f"  running sum wanted  {running}")
    for regs in (1, 2):
        print(f"  {regs} register(s) give   {run_accumulator(accumulator(regs), values)}")
    print("  with two registers the loop keeps two separate sums: odd steps and even steps")

    print("\nStep 6: throughput and latency of the pipelined MAC")
    for name, design in (("unpipelined", mac_datapath(False)), ("2-stage", mac_datapath(True))):
        period_ns = design.critical_path() * GATE_DELAY_PS / 1000
        macs_per_s = 1 / (period_ns * 1e-9)
        print(f"  {name:12s}: one MAC every {period_ns:.2f} ns = {macs_per_s / 1e9:.2f} GMAC/s,"
              f" first result after {design.latency()} cycles = {design.latency() * period_ns:.2f} ns")

    print("\nStep 7: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    wire, register = task["parts"]
    for choice in ((wire, wire, wire), (wire, register, register), (register, wire, register),
                   (register, register, register), (register, register, wire)):
        picked = dict(zip(("S1", "S2", "S3"), choice))
        results = evaluate(task, picked)
        names = "/".join("reg" if p["type"] == "register" else "wire" for p in choice)
        verdict = "PASS" if all(r["passed"] for r in results) else "fail"
        print(f"  S1/S2/S3 = {names:14s}: path {results[0]['value']:3.0f}, area {results[1]['value']:4.0f} -> {verdict}")


if __name__ == "__main__":
    main()
