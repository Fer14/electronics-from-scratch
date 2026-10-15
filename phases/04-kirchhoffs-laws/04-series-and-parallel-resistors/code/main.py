from itertools import combinations_with_replacement


def ohms_text(ohms):
    if ohms >= 1000:
        return f"{ohms / 1000:.4g} kohm"
    return f"{ohms:.4g} ohm"


def series(*parts):
    return ("series", list(parts))


def parallel(*parts):
    return ("parallel", list(parts))


def describe(network):
    if isinstance(network, (int, float)):
        return ohms_text(network)
    kind, parts = network
    joiner = " + " if kind == "series" else " || "
    return "(" + joiner.join(describe(part) for part in parts) + ")"


def reduce_network(network, depth=0):
    if isinstance(network, (int, float)):
        return float(network)
    kind, parts = network
    values = [reduce_network(part, depth + 1) for part in parts]
    if kind == "series":
        result = sum(values)
        working = " + ".join(f"{v:.6g}" for v in values)
    else:
        result = 1.0 / sum(1.0 / v for v in values)
        working = "1 / (" + " + ".join(f"1/{v:.6g}" for v in values) + ")"
    print(f"    {'  ' * depth}{kind:<8} {working} = {ohms_text(result)}")
    return result


supply = 9.0

print("Part 1: series, derived from KVL and KCL")
print("----------------------------------------")
chain = [100.0, 220.0, 330.0]
current = supply / sum(chain)
print(f"  {supply} V across {', '.join(ohms_text(r) for r in chain)} in one path")
print(f"  KCL: one path, so one current I through all of them")
print(f"  KVL: {supply} = I*100 + I*220 + I*330 = I * {sum(chain):.0f}  ->  I = {current * 1000:.3f} mA")
drops = [current * r for r in chain]
for r, drop in zip(chain, drops):
    print(f"    drop across {ohms_text(r):>8}: {drop:.3f} V")
print(f"  sum of drops = {sum(drops):.3f} V, equivalent resistance = V / I = {supply / current:.1f} ohm = 100 + 220 + 330")
print()

print("Part 2: parallel, derived from KVL and KCL")
print("------------------------------------------")
bank = [1000.0, 2200.0, 4700.0]
print(f"  {supply} V directly across {', '.join(ohms_text(r) for r in bank)}, side by side")
print(f"  KVL: each one is between the same two nodes, so each has {supply} V across it")
branch_currents = [supply / r for r in bank]
for r, i in zip(bank, branch_currents):
    print(f"    current through {ohms_text(r):>9}: {supply} / {r:.0f} = {i * 1000:.3f} mA")
total_current = sum(branch_currents)
equivalent = supply / total_current
print(f"  KCL: battery current = {' + '.join(f'{i * 1000:.3f}' for i in branch_currents)} = {total_current * 1000:.3f} mA")
print(f"  equivalent resistance = {supply} / {total_current:.6f} = {equivalent:.1f} ohm")
print(f"  formula 1 / (1/1000 + 1/2200 + 1/4700) = {1 / sum(1 / r for r in bank):.1f} ohm (smaller than the smallest, 1 kohm)")
print()

print("Part 3: shortcuts")
print("-----------------")
a, b = 220.0, 330.0
print(f"  two in parallel, product over sum: {a:.0f}*{b:.0f} / ({a:.0f}+{b:.0f}) = {a * b / (a + b):.1f} ohm")
print(f"  four equal 1 kohm in parallel: 1000 / 4 = {1 / (4 / 1000.0):.0f} ohm")
print(f"  1 kohm || 1 Mohm = {1 / (1 / 1000 + 1 / 1e6):.1f} ohm (the huge one barely matters)")
print(f"  1 kohm + 1 ohm   = {1000 + 1:.0f} ohm (the tiny one barely matters)")
print()

print("Part 4: reduce a network step by step (recursive reducer)")
print("---------------------------------------------------------")
networks = {
    "ladder from lesson 03": series(1000, parallel(3000, series(1000, 2000))),
    "two pairs": parallel(series(100, 220), series(330, 470)),
    "nested": series(47, parallel(100, series(68, parallel(150, 150))), 10),
}
for name, network in networks.items():
    print(f"  {name}: {describe(network)}")
    total = reduce_network(network)
    print(f"    equivalent = {ohms_text(total)}, battery current from {supply} V = {supply / total * 1000:.3f} mA")
    print()

print("Part 5: make a value you do not have from two you do")
print("----------------------------------------------------")
drawer = [100, 220, 330, 470, 680, 1000, 2200, 4700]
for target in [150.0, 1500.0, 400.0]:
    candidates = []
    for first, second in combinations_with_replacement(drawer, 2):
        candidates.append((abs(first + second - target), f"{first} + {second}", first + second))
        both = first * second / (first + second)
        candidates.append((abs(both - target), f"{first} || {second}", both))
    candidates.sort()
    print(f"  target {ohms_text(target)}:")
    for error, recipe, value in candidates[:3]:
        print(f"    {recipe:<12} = {value:8.1f} ohm  (off by {100 * error / target:4.1f} %)")
print()

print("Part 6: the lab circuit")
print("-----------------------")
lab = series(1200, parallel(1000, 470))
print(f"  battery -> S1 -> node a -> (R2 || S2) -> ground with S1 = 1.2 kohm, S2 = 470 ohm")
total = reduce_network(lab)
lab_current = supply / total
node_a = lab_current * (1000 * 470 / (1000 + 470))
print(f"  battery current = {supply} / {total:.1f} = {lab_current * 1000:.3f} mA, v(a) = {node_a:.3f} V")
