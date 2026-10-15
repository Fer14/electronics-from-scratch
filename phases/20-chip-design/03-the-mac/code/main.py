import math
from pathlib import Path

import numpy as np

from sim import cost
from sim.lab import evaluate, load_task
from sim.logic import LogicCircuit, full_adder


def accumulator_bits(value_bits, terms):
    largest = terms * (2 ** value_bits - 1) ** 2
    return math.ceil(math.log2(largest + 1))


def wrapping_dot(w, x, acc_bits):
    acc = 0
    for wi, xi in zip(w, x):
        acc = (acc + int(wi) * int(xi)) % (2 ** acc_bits)
    return acc


def build_mac(bits, acc_bits):
    lc = LogicCircuit(f"MAC {bits}-bit, {acc_bits}-bit accumulator")
    a = [f"a{i}" for i in range(bits)]
    b = [f"b{i}" for i in range(bits)]
    lc.inputs(*a, *b)
    lc.constant("zero", 0)
    row = []
    for i in range(bits):
        lc.and_(f"pp0_{i}", a[i], b[0])
        row.append(f"pp0_{i}")
    row.append("zero")
    product = [row[0]]
    for j in range(1, bits):
        carry = "zero"
        new_row = []
        for i in range(bits):
            lc.and_(f"pp{j}_{i}", a[i], b[j])
            out = f"m{j}c{i}"
            full_adder(lc, f"pp{j}_{i}", row[i + 1], carry, f"m{j}s{i}", out, tag=f"m{j}fa{i}")
            carry = out
            new_row.append(f"m{j}s{i}")
        new_row.append(carry)
        product.append(new_row[0])
        row = new_row
    product += row[1:]
    acc_q = [f"acc{k}" for k in range(acc_bits)]
    acc_d = [f"sum{k}" for k in range(acc_bits)]
    carry = "zero"
    for k in range(acc_bits):
        addend = product[k] if k < len(product) else "zero"
        out = f"ac{k + 1}"
        full_adder(lc, acc_q[k], addend, carry, acc_d[k], out, tag=f"acc_fa{k}")
        carry = out
    lc.register("ACC", acc_d, acc_q)
    lc.outputs(*acc_q)
    return lc


def run_mac(lc, bits, acc_bits, pairs):
    lc.reset()
    for wi, xi in pairs:
        inputs = {f"a{i}": (int(wi) >> i) & 1 for i in range(bits)}
        inputs.update({f"b{i}": (int(xi) >> i) & 1 for i in range(bits)})
        lc.step(inputs)
    return sum(lc.values[f"acc{k}"] << k for k in range(acc_bits))


def main():
    rng = np.random.default_rng(7)

    print("Step 1: a dot product is a loop of multiply-accumulates")
    w = rng.integers(0, 16, size=8)
    x = rng.integers(0, 16, size=8)
    acc = 0
    for step, (wi, xi) in enumerate(zip(w, x), start=1):
        acc += int(wi) * int(xi)
        print(f"  step {step}: acc += {wi:2d} x {xi:2d} -> {acc}")
    print(f"  numpy dot product: {int(np.dot(w, x))}")

    print("\nStep 2: how many MACs real layers need")
    for name, rows, cols, batch in (("small layer 512 x 512, 1 input", 512, 512, 1),
                                    ("4096 x 4096 layer, 1 input", 4096, 4096, 1),
                                    ("4096 x 4096 layer, 64 inputs", 4096, 4096, 64)):
        print(f"  {name:32s}: {rows * cols * batch:>13,d} MACs")

    print("\nStep 3: accumulator width needed so the sum can never overflow (unsigned inputs)")
    print(f"  {'inputs':>6s} {'terms':>6s} {'product bits':>12s} {'accumulator bits':>16s}")
    for value_bits in (4, 8):
        for terms in (1, 16, 256, 4096):
            print(f"  {value_bits:4d}-b {terms:6d} {2 * value_bits:12d} {accumulator_bits(value_bits, terms):16d}")

    print("\nStep 4: what overflow does to an 8-bit dot product of length 256")
    w8 = rng.integers(0, 256, size=256)
    x8 = rng.integers(0, 256, size=256)
    exact = int(np.dot(w8, x8))
    for acc_bits in (16, 20, 24):
        got = wrapping_dot(w8, x8, acc_bits)
        verdict = "correct" if got == exact else f"wrong by {exact - got:,d}"
        print(f"  {acc_bits}-bit accumulator: {got:>12,d}  (exact {exact:,d}) -> {verdict}")

    print("\nStep 5: a clocked gate-level MAC (4-bit inputs) in sim.logic")
    w4 = rng.integers(0, 16, size=12)
    x4 = rng.integers(0, 16, size=12)
    exact4 = int(np.dot(w4, x4))
    for acc_bits in (8, 12):
        mac = build_mac(4, acc_bits)
        got = run_mac(mac, 4, acc_bits, zip(w4, x4))
        print(f"  {acc_bits:2d}-bit accumulator: {mac.gate_count()} gates + {len(mac.flops)} flip-flops,"
              f" result after 12 clock cycles {got} (exact {exact4})")

    print("\nStep 6: where the area of an 8-bit MAC goes (sim.cost)")
    for acc_bits in (16, 24, 32):
        block = cost.mac(8, acc_bits)
        m, a, r = cost.multiplier(8).area, cost.adder(acc_bits).area, cost.register(acc_bits).area
        print(f"  acc {acc_bits}: total {block.area:4.0f} = multiplier {m:.0f} + adder {a:.0f} + register {r:.0f}"
              f"  (multiplier is {m / block.area * 100:4.1f}%), path {block.delay} gate delays")

    print("\nStep 7: MACs per million gates")
    for bits in (4, 8, 16):
        block = cost.mac(bits)
        print(f"  {bits:2d}-bit MAC with {block.params['acc_bits']}-bit accumulator: {block.area:5.0f} gates,"
              f" {1_000_000 // block.area:5.0f} per million gates")

    print("\nStep 8: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for part in task["parts"]:
        results = evaluate(task, {"S1": part})
        line = ", ".join(f"{r['label']}: {r['value']:.0f}" for r in results)
        print(f"  acc_bits {part['acc_bits']}: {line} -> {'PASS' if all(r['passed'] for r in results) else 'fail'}")


if __name__ == "__main__":
    main()
