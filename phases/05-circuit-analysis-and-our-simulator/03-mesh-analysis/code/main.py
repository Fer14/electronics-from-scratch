import numpy as np

from sim import Circuit


def mesh_system(circuit):
    names = [m for m in circuit["meshes"] if m not in circuit["known"]]
    index = {m: k for k, m in enumerate(names)}
    resistance = np.zeros((len(names), len(names)))
    sources = np.zeros(len(names))
    for row_mesh, walk in circuit["meshes"].items():
        if row_mesh not in index:
            continue
        row = index[row_mesh]
        for element, direction in walk:
            if element in circuit["sources"]:
                sources[row] -= direction * circuit["sources"][element][2]
                continue
            ohms = circuit["resistors"][element][2]
            for other_mesh, other_walk in circuit["meshes"].items():
                for other_element, other_direction in other_walk:
                    if other_element != element:
                        continue
                    term = direction * other_direction * ohms
                    if other_mesh in index:
                        resistance[row, index[other_mesh]] += term
                    else:
                        sources[row] -= term * circuit["known"][other_mesh]
    return names, resistance, sources


def branch_current(circuit, mesh_currents, element):
    return sum(direction * mesh_currents[mesh]
               for mesh, walk in circuit["meshes"].items()
               for name, direction in walk if name == element)


def build_sim(circuit):
    sim_circuit = Circuit()
    for name, (plus, minus, volts) in circuit["sources"].items():
        sim_circuit.voltage_source(name, plus, minus, volts)
    for name, (a, b, ohms) in circuit["resistors"].items():
        sim_circuit.resistor(name, a, b, ohms)
    for name, (a, b, amps) in circuit.get("current_sources", {}).items():
        sim_circuit.current_source(name, a, b, amps)
    return sim_circuit


def analyse(title, circuit):
    print(f"\n=== {title} ===")
    names, resistance, sources = mesh_system(circuit)
    print("resistance matrix (kOhm):")
    for row in resistance / 1000:
        print("   [" + "  ".join(f"{x:7.3f}" for x in row) + " ]")
    print("source voltages around each mesh (V): [" + "  ".join(f"{x:7.3f}" for x in sources) + " ]")
    solved = np.linalg.solve(resistance, sources)
    mesh_currents = dict(circuit["known"], **dict(zip(names, solved)))
    for mesh, amps in mesh_currents.items():
        tag = " (fixed by a current source)" if mesh in circuit["known"] else ""
        print(f"  mesh current {mesh} = {amps * 1000:7.3f} mA{tag}")
    result = build_sim(circuit).dc()
    worst = 0.0
    for element in circuit["resistors"]:
        ours = branch_current(circuit, mesh_currents, element)
        theirs = result.i(element)
        worst = max(worst, abs(ours - theirs))
        print(f"  i({element}) from meshes = {ours * 1000:7.3f} mA   sim = {theirs * 1000:7.3f} mA")
    print(f"  largest difference: {worst:.1e} A")
    for node in sorted({n for a, b, _ in circuit["resistors"].values() for n in (a, b)} - {"0"}):
        print(f"  v({node}) from sim = {result.v(node):7.3f} V")


def main():
    two_battery = {
        "resistors": {"R1": ("a", "b", 1000), "R2": ("b", "0", 2000), "R3": ("b", "c", 1000)},
        "sources": {"V1": ("a", "0", 9.0), "V2": ("c", "0", 3.0)},
        "meshes": {
            "m1": [("V1", -1), ("R1", +1), ("R2", +1)],
            "m2": [("R2", -1), ("R3", +1), ("V2", +1)],
        },
        "known": {},
    }
    analyse("Two batteries, two windows", two_battery)

    workhorse = {
        "resistors": {"R1": ("a", "b", 1000), "R2": ("b", "0", 2000), "R3": ("b", "c", 3000), "R4": ("c", "0", 1000)},
        "sources": {"V1": ("a", "0", 12.0)},
        "current_sources": {"I1": ("0", "c", 0.001)},
        "meshes": {
            "m1": [("V1", -1), ("R1", +1), ("R2", +1)],
            "m2": [("R2", -1), ("R3", +1), ("R4", +1)],
            "m3": [("R4", -1)],
        },
        "known": {"m3": -0.001},
    }
    analyse("Workhorse: the current source fixes mesh m3", workhorse)

    transformed = {
        "resistors": {"R1": ("a", "b", 1000), "R2": ("b", "0", 2000), "R3": ("b", "c", 3000), "R4": ("c", "d", 1000)},
        "sources": {"V1": ("a", "0", 12.0), "V2": ("d", "0", 1.0)},
        "meshes": {
            "m1": [("V1", -1), ("R1", +1), ("R2", +1)],
            "m2": [("R2", -1), ("R3", +1), ("R4", +1), ("V2", +1)],
        },
        "known": {},
    }
    analyse("Workhorse after source transformation (1 mA || 1 kOhm -> 1 V + 1 kOhm)", transformed)


if __name__ == "__main__":
    main()
