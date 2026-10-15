from itertools import product
from pathlib import Path

from sim import cost
from sim.lab import evaluate, load_task
from sim.logic import LogicCircuit, full_adder, ripple_adder

GATE_DELAY_PS = 20.0


def count_gates(lc):
    return sum(1 for gate in lc.gates if gate.op != "buf")


def longest_path(lc):
    driver = {gate.output: gate for gate in lc.gates}
    memo = {}

    def depth(signal):
        if signal not in driver:
            return 0
        if signal not in memo:
            gate = driver[signal]
            own = 0 if gate.op == "buf" else 1
            memo[signal] = own + max(depth(i) for i in gate.inputs)
        return memo[signal]

    return max(depth(name) for name in lc.output_names)


def add_with(lc, bits, x, y):
    inputs = {f"a{i}": (x >> i) & 1 for i in range(bits)}
    inputs.update({f"b{i}": (y >> i) & 1 for i in range(bits)})
    out = lc.evaluate(inputs)
    return sum(out[f"s{i}"] << i for i in range(bits)) + (out["cout"] << bits)


def carry_select_adder(bits):
    half = bits // 2
    lc = LogicCircuit(f"carry-select {bits}-bit")
    a = [f"a{i}" for i in range(bits)]
    b = [f"b{i}" for i in range(bits)]
    lc.inputs(*a, *b)
    lc.constant("zero", 0)
    lc.constant("one", 1)
    carry = "zero"
    for i in range(half):
        out = f"lo.c{i + 1}"
        full_adder(lc, a[i], b[i], carry, f"s{i}", out, tag=f"lo{i}")
        carry = out
    select = carry
    for guess in ("zero", "one"):
        c = guess
        for i in range(half, bits):
            out = f"{guess}.c{i + 1}"
            full_adder(lc, a[i], b[i], c, f"{guess}.s{i}", out, tag=f"{guess}{i}")
            c = out
    lc.not_("nsel", select)
    picks = [(f"s{i}", f"zero.s{i}", f"one.s{i}") for i in range(half, bits)]
    picks.append(("cout", f"zero.c{bits}", f"one.c{bits}"))
    for name, if_zero, if_one in picks:
        lc.and_(f"{name}.z", if_zero, "nsel")
        lc.and_(f"{name}.o", if_one, select)
        lc.or_(name, f"{name}.z", f"{name}.o")
    lc.outputs(*[f"s{i}" for i in range(bits)], "cout")
    return lc


def main():
    print("Step 1: one full adder, built from five gates")
    fa = LogicCircuit("full adder")
    fa.inputs("a", "b", "cin")
    full_adder(fa, "a", "b", "cin", "s", "cout")
    fa.outputs("s", "cout")
    print(fa.format_truth_table())

    print("\nStep 2: our own cost model, by hand, compared with sim.logic")
    print(f"  full adder: {count_gates(fa)} gates (sim.logic says {fa.gate_count()}),"
          f" longest path {longest_path(fa)} gates (sim.logic says {fa.depth()})")

    print("\nStep 3: ripple-carry adders grow linearly in area and in delay")
    print(f"  {'bits':>4s} {'gates':>6s} {'depth':>6s} {'sim.cost':>12s} {'period':>9s} {'max clock':>10s}")
    for bits in (4, 8, 16, 32, 64):
        lc = ripple_adder(bits)
        block = cost.adder(bits)
        depth = longest_path(lc)
        period_ps = depth * GATE_DELAY_PS
        print(f"  {bits:4d} {count_gates(lc):6d} {depth:6d} {block.area:5.0f}/{block.delay:<5d}"
              f" {period_ps:6.0f} ps {1e6 / period_ps:7.0f} MHz")

    print("\nStep 4: check the 4-bit adder on all 256 pairs")
    adder4 = ripple_adder(4)
    wrong = sum(1 for x, y in product(range(16), repeat=2) if add_with(adder4, 4, x, y) != x + y)
    print(f"  {256 - wrong} of 256 sums correct")
    print(f"  example: 11 + 6 = {add_with(adder4, 4, 11, 6)}")

    print("\nStep 5: watch the carry ripple (0111 + 0000 -> 0111 + 0001)")
    before = {f"a{i}": (7 >> i) & 1 for i in range(4)} | {f"b{i}": 0 for i in range(4)}
    after = {"b0": 1}
    last_change = {}
    for time, name, value in adder4.events(before, after):
        if name in adder4.output_names:
            last_change[name] = (time, value)
    for name in adder4.output_names:
        if name in last_change:
            time, value = last_change[name]
            print(f"  {name:4s} settles to {value} after {time} gate delays")

    print("\nStep 6: spend area to buy speed (8-bit carry-select vs ripple)")
    ripple8 = ripple_adder(8)
    select8 = carry_select_adder(8)
    wrong = sum(1 for x, y in product(range(256), repeat=2) if add_with(select8, 8, x, y) != x + y)
    for name, lc in (("ripple", ripple8), ("carry-select", select8)):
        print(f"  {name:12s}: {count_gates(lc):3d} gates, longest path {longest_path(lc):2d} gate delays")
    print(f"  carry-select checked on all 65536 pairs: {65536 - wrong} correct")
    ratio_area = count_gates(select8) / count_gates(ripple8)
    ratio_speed = longest_path(ripple8) / longest_path(select8)
    print(f"  {ratio_area:.2f}x the area for {ratio_speed:.2f}x the speed")

    print("\nStep 7: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for result in evaluate(task):
        print(f"  {'PASS' if result['passed'] else 'fail'}  {result['label']}: {result['value']}")


if __name__ == "__main__":
    main()
