import numpy as np

from sim import Circuit


def build_workhorse():
    circuit = Circuit()
    circuit.voltage_source("V1", "a", "0", 12.0)
    circuit.resistor("R1", "a", "b", 1000)
    circuit.resistor("R2", "b", "0", 2000)
    circuit.resistor("R3", "b", "c", 3000)
    circuit.resistor("R4", "c", "0", 1000)
    circuit.current_source("I1", "0", "c", 0.001)
    return circuit


def solve_branch_currents():
    branch_matrix = np.array([
        [1.0, -1.0, -1.0, 0.0],
        [0.0, 0.0, 1.0, -1.0],
        [1.0, 2.0, 0.0, 0.0],
        [0.0, 2.0, -3.0, -1.0],
    ])
    right_side = np.array([0.0, -1.0, 12.0, 0.0])
    return np.linalg.solve(branch_matrix, right_side)


def main():
    print("Branch current method, solved with numpy (kOhm, mA, V)")
    branch_currents_ma = solve_branch_currents()
    for name, value in zip(("i1 (R1)", "i2 (R2)", "i3 (R3)", "i4 (R4)"), branch_currents_ma):
        print(f"  {name:8s} = {value:7.3f} mA")
    print(f"  vb = 2 kOhm x i2 = {2 * branch_currents_ma[1]:.3f} V")
    print(f"  vc = 1 kOhm x i4 = {1 * branch_currents_ma[3]:.3f} V")

    print("\nSame circuit, solved by our simulator")
    result = build_workhorse().dc()
    print(result.table())
    for node in ("a", "b", "c"):
        print(f"  v({node}) = {result.v(node):7.3f} V")
    for name in ("R1", "R2", "R3", "R4"):
        print(f"  i({name}) = {result.i(name) * 1000:7.3f} mA")

    print("\nKirchhoff checks on the simulator's answer")
    kcl_b = result.i("R1") - result.i("R2") - result.i("R3")
    kcl_c = result.i("R3") + 0.001 - result.i("R4")
    kvl_outer = 12.0 - 1000 * result.i("R1") - 3000 * result.i("R3") - 1000 * result.i("R4")
    print(f"  KCL at b: in - out = {kcl_b:.2e} A")
    print(f"  KCL at c: in - out = {kcl_c:.2e} A")
    print(f"  KVL outer loop: 12 V - drops = {kvl_outer:.2e} V")

    print("\nPower budget")
    burned = sum(result.p(name) for name in ("R1", "R2", "R3", "R4"))
    delivered_by_battery = 12.0 * result.i("R1")
    delivered_by_current_source = result.v("c") * 0.001
    print(f"  burned in resistors      = {burned * 1000:.3f} mW")
    print(f"  delivered by V1          = {delivered_by_battery * 1000:.3f} mW")
    print(f"  delivered by I1          = {delivered_by_current_source * 1000:.3f} mW")
    print(f"  delivered - burned       = {(delivered_by_battery + delivered_by_current_source - burned) * 1000:.2e} mW")

    agreement = np.allclose(branch_currents_ma / 1000, [result.i(n) for n in ("R1", "R2", "R3", "R4")])
    print(f"\nHand method and simulator agree: {agreement}")


if __name__ == "__main__":
    main()
