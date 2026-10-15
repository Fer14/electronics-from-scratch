import numpy as np

from sim import Circuit


def nodal_system(resistors, current_sources, known):
    unknown_nodes = sorted({n for x, y, _ in resistors for n in (x, y)} - {"0"} - set(known))
    index = {node: k for k, node in enumerate(unknown_nodes)}
    conductance = np.zeros((len(unknown_nodes), len(unknown_nodes)))
    injected = np.zeros(len(unknown_nodes))
    for node_x, node_y, ohms in resistors:
        g = 1.0 / ohms
        for this, other in ((node_x, node_y), (node_y, node_x)):
            if this not in index:
                continue
            conductance[index[this], index[this]] += g
            if other in index:
                conductance[index[this], index[other]] -= g
            elif other in known:
                injected[index[this]] += g * known[other]
    for from_node, to_node, amps in current_sources:
        if to_node in index:
            injected[index[to_node]] += amps
        if from_node in index:
            injected[index[from_node]] -= amps
    return unknown_nodes, conductance, injected


def kcl_residuals(nodes, voltages, resistors, current_sources, known):
    value = dict(known, **{"0": 0.0}, **dict(zip(nodes, voltages)))
    residuals = {}
    for node in nodes:
        leaving = sum((value[node] - value[y if x == node else x]) / ohms
                      for x, y, ohms in resistors if node in (x, y))
        pushed_in = sum(amps for f, t, amps in current_sources if t == node) - sum(
            amps for f, t, amps in current_sources if f == node)
        residuals[node] = leaving - pushed_in
    return residuals


def build_circuit(resistors, current_sources, known):
    circuit = Circuit()
    for k, (node, volts) in enumerate(known.items()):
        circuit.voltage_source(f"V{k + 1}", node, "0", volts)
    for k, (x, y, ohms) in enumerate(resistors):
        circuit.resistor(f"R{k + 1}", x, y, ohms)
    for k, (f, t, amps) in enumerate(current_sources):
        circuit.current_source(f"I{k + 1}", f, t, amps)
    return circuit


def analyse(title, resistors, current_sources, known):
    print(f"\n=== {title} ===")
    nodes, conductance, injected = nodal_system(resistors, current_sources, known)
    print(f"unknown nodes: {nodes}")
    print("conductance matrix (mS):")
    for row in conductance * 1000:
        print("   [" + "  ".join(f"{x:7.3f}" for x in row) + " ]")
    print("injected currents (mA): [" + "  ".join(f"{x:7.3f}" for x in injected * 1000) + " ]")
    voltages = np.linalg.solve(conductance, injected)
    result = build_circuit(resistors, current_sources, known).dc()
    worst = 0.0
    for node, volts in zip(nodes, voltages):
        sim_volts = result.v(node)
        worst = max(worst, abs(volts - sim_volts))
        print(f"  v({node}) by hand-built nodal = {volts:9.4f} V   by sim = {sim_volts:9.4f} V")
    print(f"  largest difference: {worst:.1e} V")
    for node, residual in kcl_residuals(nodes, voltages, resistors, current_sources, known).items():
        print(f"  KCL check at {node}: leaving - pushed in = {residual:.1e} A")


def main():
    analyse(
        "Workhorse: 12 V battery, four resistors, 1 mA source",
        [("a", "b", 1000), ("b", "0", 2000), ("b", "c", 3000), ("c", "0", 1000)],
        [("0", "c", 0.001)],
        {"a": 12.0},
    )
    analyse(
        "Three nodes, two current sources",
        [("n1", "0", 2000), ("n1", "n2", 2000), ("n2", "0", 4000), ("n2", "n3", 1000), ("n3", "0", 4000)],
        [("0", "n1", 0.004), ("n3", "0", 0.002)],
        {},
    )
    analyse(
        "Lab board with the right part (Rs = 1 kOhm)",
        [("a", "0", 2000), ("a", "b", 1000), ("b", "0", 2000)],
        [("0", "a", 0.002)],
        {},
    )


if __name__ == "__main__":
    main()
