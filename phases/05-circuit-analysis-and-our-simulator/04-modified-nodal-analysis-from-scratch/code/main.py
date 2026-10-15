import numpy as np

from sim import Circuit

GROUND = {"0", "gnd"}
SUFFIXES = {"T": 1e12, "G": 1e9, "MEG": 1e6, "k": 1e3, "m": 1e-3, "u": 1e-6, "n": 1e-9, "p": 1e-12}


def parse_value(text):
    for suffix in sorted(SUFFIXES, key=len, reverse=True):
        if text.endswith(suffix):
            return float(text[: -len(suffix)]) * SUFFIXES[suffix]
    return float(text)


def parse_netlist(text):
    parts = []
    for line in text.strip().splitlines():
        name, node_1, node_2, value = line.split()
        parts.append((name[0].upper(), name, node_1, node_2, parse_value(value)))
    return parts


def number_unknowns(parts):
    nodes = []
    for _, _, node_1, node_2, _ in parts:
        for node in (node_1, node_2):
            if node not in GROUND and node not in nodes:
                nodes.append(node)
    sources = [name for kind, name, *_ in parts if kind == "V"]
    index = {node: k for k, node in enumerate(nodes)}
    index.update({name: len(nodes) + k for k, name in enumerate(sources)})
    return nodes, sources, index


def add(matrix, row, col, value):
    if row is not None and col is not None:
        matrix[row, col] += value


def stamp_resistor(matrix, index, node_1, node_2, ohms):
    g = 1.0 / ohms
    a, b = index.get(node_1), index.get(node_2)
    add(matrix, a, a, g)
    add(matrix, b, b, g)
    add(matrix, a, b, -g)
    add(matrix, b, a, -g)


def stamp_current_source(rhs, index, node_from, node_to, amps):
    if node_from in index:
        rhs[index[node_from]] -= amps
    if node_to in index:
        rhs[index[node_to]] += amps


def stamp_voltage_source(matrix, rhs, index, name, plus, minus, volts):
    k, p, m = index[name], index.get(plus), index.get(minus)
    add(matrix, p, k, 1.0)
    add(matrix, m, k, -1.0)
    add(matrix, k, p, 1.0)
    add(matrix, k, m, -1.0)
    rhs[k] += volts


def solve_mna(parts):
    nodes, sources, index = number_unknowns(parts)
    size = len(nodes) + len(sources)
    matrix = np.zeros((size, size))
    rhs = np.zeros(size)
    for kind, name, node_1, node_2, value in parts:
        if kind == "R":
            stamp_resistor(matrix, index, node_1, node_2, value)
        elif kind == "I":
            stamp_current_source(rhs, index, node_1, node_2, value)
        elif kind == "V":
            stamp_voltage_source(matrix, rhs, index, name, node_1, node_2, value)
    solution = np.linalg.solve(matrix, rhs)
    return matrix, rhs, {key: solution[k] for key, k in index.items()}


def build_sim(parts):
    circuit = Circuit()
    for kind, name, node_1, node_2, value in parts:
        if kind == "R":
            circuit.resistor(name, node_1, node_2, value)
        elif kind == "I":
            circuit.current_source(name, node_1, node_2, value)
        elif kind == "V":
            circuit.voltage_source(name, node_1, node_2, value)
    return circuit


def print_system(parts, matrix, rhs):
    nodes, sources, _ = number_unknowns(parts)
    labels = [f"v{n}" for n in nodes] + [f"j{s}" for s in sources]
    print("  MNA matrix A (conductances in mS) and right side z (mA or V):")
    print("        " + "".join(f"{label:>8s}" for label in labels) + "         z")
    for row, label in enumerate(labels):
        row_scale = 1000.0 if row < len(nodes) else 1.0
        entries = [matrix[row, col] * (1000.0 if col < len(nodes) and row < len(nodes) else 1.0) for col in range(len(labels))]
        print(f"  {label:>5s} [" + "".join(f"{x:8.3f}" for x in entries) + f" ]  [{rhs[row] * row_scale:7.3f} ]")


def compare(title, netlist, show_matrix=False):
    print(f"\n=== {title} ===")
    parts = parse_netlist(netlist)
    matrix, rhs, ours = solve_mna(parts)
    if show_matrix:
        print_system(parts, matrix, rhs)
    result = build_sim(parts).dc()
    nodes, sources, _ = number_unknowns(parts)
    worst = 0.0
    for node in nodes:
        worst = max(worst, abs(ours[node] - result.v(node)))
        print(f"  v({node:>3s}) ours = {ours[node]:10.5f} V   sim = {result.v(node):10.5f} V")
    for name in sources:
        delivered = -ours[name]
        worst = max(worst, abs(delivered - result.i(name)))
        print(f"  {name}: MNA j = {ours[name] * 1000:8.4f} mA, so it delivers {delivered * 1000:8.4f} mA;"
              f" sim i({name}) = {result.i(name) * 1000:8.4f} mA")
    print(f"  largest difference: {worst:.1e}")


def ladder_netlist(sections):
    lines = ["V1 n0 0 10", "V2 m 0 3"]
    for k in range(sections):
        lines.append(f"Rs{k} n{k} n{k + 1} 1k")
        lines.append(f"Rp{k} n{k + 1} 0 2k")
    lines.append(f"Rend n{sections} m 470")
    lines.append("I1 0 n3 500u")
    return "\n".join(lines)


def main():
    compare("Floating 5 V battery (the lesson's hand example)", """
V1 a 0 10
R1 a b 1k
V2 c b 5
R2 c 0 2k
""", show_matrix=True)

    compare("Workhorse from Lessons 01-03", """
V1 a 0 12
R1 a b 1k
R2 b 0 2k
R3 b c 3k
R4 c 0 1k
I1 0 c 1m
""")

    compare("Six-section ladder with two batteries and a current source", ladder_netlist(6))

    print("\n=== A floating node (R3 connects x and y, but nothing ties them to the rest) ===")
    broken = parse_netlist("""
V1 a 0 5
R1 a 0 1k
R3 x y 1k
""")
    try:
        solve_mna(broken)
    except np.linalg.LinAlgError as error:
        print(f"  our solver: numpy says '{error}'")
    result = build_sim(broken).dc()
    print(f"  sim (with gmin from every node to ground): v(x) = {result.v('x'):.3g} V, v(y) = {result.v('y'):.3g} V")


if __name__ == "__main__":
    main()
