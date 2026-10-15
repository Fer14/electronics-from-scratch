from sim import Circuit


def build_workhorse(v1_volts, i1_amps):
    circuit = Circuit()
    circuit.voltage_source("V1", "a", "0", v1_volts)
    circuit.resistor("R1", "a", "b", 1000)
    circuit.resistor("R2", "b", "0", 2000)
    circuit.resistor("R3", "b", "c", 3000)
    circuit.resistor("R4", "c", "0", 1000)
    circuit.current_source("I1", "0", "c", i1_amps)
    return circuit


def parallel(*resistances):
    return 1.0 / sum(1.0 / r for r in resistances)


def hand_contributions():
    lower_b = parallel(2.0, 3.0 + 1.0)
    vb_battery = 12.0 * lower_b / (1.0 + lower_b)
    vc_battery = vb_battery * 1.0 / (3.0 + 1.0)
    r1_r2 = parallel(1.0, 2.0)
    seen_from_c = parallel(1.0, 3.0 + r1_r2)
    vc_source = 1.0 * seen_from_c
    vb_source = vc_source * r1_r2 / (3.0 + r1_r2)
    return {"b": (vb_battery, vb_source), "c": (vc_battery, vc_source)}


def main():
    both = build_workhorse(12.0, 0.001).dc()
    battery_only = build_workhorse(12.0, 0.0).dc()
    source_only = build_workhorse(0.0, 0.001).dc()
    hand = hand_contributions()

    print("Node voltages: contribution of each source, their sum, and the full solution")
    print(f"  {'node':4s} {'V1 alone':>10s} {'I1 alone':>10s} {'sum':>10s} {'both on':>10s}   hand (V1, I1)")
    for node in ("a", "b", "c"):
        first, second = battery_only.v(node), source_only.v(node)
        hand_text = "" if node == "a" else f"  ({hand[node][0]:.3f}, {hand[node][1]:.3f})"
        print(f"  {node:4s} {first:9.4f}V {second:9.4f}V {first + second:9.4f}V {both.v(node):9.4f}V {hand_text}")

    print("\nResistor currents (positive from first node to second)")
    print(f"  {'part':4s} {'V1 alone':>10s} {'I1 alone':>10s} {'sum':>10s} {'both on':>10s}")
    for name in ("R1", "R2", "R3", "R4"):
        first, second = battery_only.i(name) * 1000, source_only.i(name) * 1000
        print(f"  {name:4s} {first:8.4f}mA {second:8.4f}mA {first + second:8.4f}mA {both.i(name) * 1000:8.4f}mA")

    print("\nTransfer coefficients (one unit of each source, the other off)")
    per_volt = build_workhorse(1.0, 0.0).dc()
    per_milliamp = build_workhorse(0.0, 0.001).dc()
    coefficients = {node: (per_volt.v(node), per_milliamp.v(node)) for node in ("b", "c")}
    for node, (k_v, k_i) in coefficients.items():
        print(f"  v{node} = {k_v:.4f} x V1 + {k_i:.4f} kOhm x I1(mA)")

    print("\nPredictions from the coefficients, checked by a fresh simulation")
    for v1, i1_ma in ((9.0, 1.0), (12.0, -1.0), (6.0, 2.0)):
        predicted = coefficients["b"][0] * v1 + coefficients["b"][1] * i1_ma
        simulated = build_workhorse(v1, i1_ma / 1000).dc().v("b")
        print(f"  V1 = {v1:4.1f} V, I1 = {i1_ma:4.1f} mA: predicted vb = {predicted:.4f} V, simulated vb = {simulated:.4f} V")

    print("\nPower does not superpose (resistor R4)")
    true_power = both.p("R4")
    wrong_sum = battery_only.p("R4") + source_only.p("R4")
    cross_term = 2 * battery_only.v("c") * source_only.v("c") / 1000
    print(f"  true power                    = {true_power * 1000:.3f} mW")
    print(f"  power(V1 alone) + power(I1 alone) = {wrong_sum * 1000:.3f} mW   (wrong)")
    print(f"  missing cross term 2ab/R       = {cross_term * 1000:.3f} mW")
    print(f"  wrong sum + cross term         = {(wrong_sum + cross_term) * 1000:.3f} mW")


if __name__ == "__main__":
    main()
