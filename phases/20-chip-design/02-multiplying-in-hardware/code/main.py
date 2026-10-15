from itertools import product
from pathlib import Path

from sim import cost
from sim.lab import evaluate, load_task
from sim.logic import LogicCircuit, array_multiplier, full_adder


def partial_products(x, y, bits):
    return [((x if (y >> j) & 1 else 0) << j) for j in range(bits)]


def half_adder(lc, a, b, s, cout, tag):
    lc.xor(s, a, b)
    lc.and_(cout, a, b)


def trimmed_multiplier(bits):
    lc = LogicCircuit(f"trimmed multiplier {bits}x{bits}")
    a = [f"a{i}" for i in range(bits)]
    b = [f"b{i}" for i in range(bits)]
    lc.inputs(*a, *b)
    for j in range(bits):
        for i in range(bits):
            lc.and_(f"pp{j}_{i}", a[i], b[j])
    row = [f"pp0_{i}" for i in range(bits)] + [None]
    products = ["pp0_0"]
    for j in range(1, bits):
        carry = None
        new_row = []
        for i in range(bits):
            x, y = f"pp{j}_{i}", row[i + 1]
            s, co = f"r{j}c{i}.s", f"r{j}c{i}.co"
            inputs = [n for n in (x, y, carry) if n is not None]
            if len(inputs) == 3:
                full_adder(lc, *inputs, s, co, tag=f"r{j}c{i}")
            else:
                half_adder(lc, *inputs, s, co, tag=f"r{j}c{i}")
            carry = co
            new_row.append(s)
        new_row.append(carry)
        products.append(new_row[0])
        row = new_row
    products += row[1:]
    for k, name in enumerate(products):
        lc.gate("buf", [name], f"p{k}")
    lc.outputs(*[f"p{k}" for k in range(2 * bits)])
    return lc


def multiply_with(lc, bits, x, y):
    inputs = {f"a{i}": (x >> i) & 1 for i in range(bits)}
    inputs.update({f"b{i}": (y >> i) & 1 for i in range(bits)})
    out = lc.evaluate(inputs)
    return sum(out[f"p{k}"] << k for k in range(2 * bits))


def count_correct(lc, bits):
    return sum(1 for x, y in product(range(2 ** bits), repeat=2) if multiply_with(lc, bits, x, y) == x * y)


def main():
    print("Step 1: long multiplication in binary, 13 x 11")
    x, y = 13, 11
    rows = partial_products(x, y, 4)
    for j, row in enumerate(rows):
        bit = (y >> j) & 1
        print(f"  b{j} = {bit}: {row:08b}  ({row})")
    print(f"  sum of the rows: {sum(rows):08b} = {sum(rows)}  (13 x 11 = {x * y})")

    print("\nStep 2: the 4x4 array multiplier from sim.logic")
    full = array_multiplier(4)
    block = cost.multiplier(4)
    print(f"  {full.gate_count()} gates, depth {full.depth()} gate delays"
          f" (sim.cost.multiplier(4): {block.area:.0f} gates, {block.delay} delays)")
    print(f"  correct products: {count_correct(full, 4)} of 256")

    print("\nStep 3: trim it, half adders where an input is always 0")
    trimmed = trimmed_multiplier(4)
    counts = trimmed.counts()
    print(f"  {trimmed.gate_count()} gates, depth {trimmed.depth()} gate delays,"
          f" gate mix {dict((k, v) for k, v in counts.items() if v and k != 'buf')}")
    print(f"  correct products: {count_correct(trimmed, 4)} of 256")

    print("\nStep 4: area grows with the square of the width")
    print(f"  {'bits':>4s} {'adder':>7s} {'multiplier':>11s} {'mult / bits^2':>14s} {'mult / adder':>13s} {'delay':>6s}")
    for bits in (2, 4, 8, 16, 32):
        add, mul = cost.adder(bits), cost.multiplier(bits)
        print(f"  {bits:4d} {add.area:7.0f} {mul.area:11.0f} {mul.area / bits ** 2:14.2f}"
              f" {mul.area / add.area:13.1f} {mul.delay:6d}")

    print("\nStep 5: multipliers per 100,000 gates of silicon")
    budget = 100_000
    base = budget // cost.multiplier(16).area
    for bits in (16, 8, 4):
        count = budget // cost.multiplier(bits).area
        print(f"  {bits:2d}-bit: {count:5.0f} multipliers ({count / base:5.1f}x the 16-bit count)")

    print("\nStep 6: check the lab task")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for result in evaluate(task):
        print(f"  {'PASS' if result['passed'] else 'fail'}  {result['label']}: {result['value']}")


if __name__ == "__main__":
    main()
