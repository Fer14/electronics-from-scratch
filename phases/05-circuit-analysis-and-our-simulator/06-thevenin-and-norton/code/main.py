from sim import Circuit


def divider(circuit, sources_on=1.0):
    circuit.voltage_source("V1", "a", "0", 12.0 * sources_on)
    circuit.resistor("R1", "a", "p", 6000)
    circuit.resistor("R2", "p", "0", 3000)


def workhorse_without_r4(circuit, sources_on=1.0):
    circuit.voltage_source("V1", "a", "0", 12.0 * sources_on)
    circuit.resistor("R1", "a", "b", 1000)
    circuit.resistor("R2", "b", "0", 2000)
    circuit.resistor("R3", "b", "p", 3000)
    circuit.current_source("I1", "0", "p", 0.001 * sources_on)


def thevenin(network):
    open_circuit = Circuit()
    network(open_circuit)
    v_open = open_circuit.dc().v("p")
    shorted = Circuit()
    network(shorted)
    shorted.voltage_source("VSHORT", "p", "0", 0.0)
    i_short = -shorted.dc().i("VSHORT")
    return v_open, v_open / i_short, i_short


def dead_source_resistance(network, test_amps=0.001):
    dead = Circuit()
    network(dead, sources_on=0.0)
    dead.current_source("ITEST", "0", "p", test_amps)
    return dead.dc().v("p") / test_amps


def load_voltage_original(network, load):
    original = Circuit()
    network(original)
    original.resistor("RL", "p", "0", load)
    return original.dc().v("p")


def load_voltage_thevenin(v_th, r_th, load):
    equivalent = Circuit()
    equivalent.voltage_source("VTH", "t", "0", v_th)
    equivalent.resistor("RTH", "t", "p", r_th)
    equivalent.resistor("RL", "p", "0", load)
    return equivalent.dc().v("p")


def load_voltage_norton(i_n, r_n, load):
    equivalent = Circuit()
    equivalent.current_source("IN", "0", "p", i_n)
    equivalent.resistor("RN", "p", "0", r_n)
    equivalent.resistor("RL", "p", "0", load)
    return equivalent.dc().v("p")


def study(title, network, loads):
    print(f"\n=== {title} ===")
    v_th, r_th, i_short = thevenin(network)
    r_dead = dead_source_resistance(network)
    print(f"  open-circuit voltage   Voc = {v_th:8.4f} V        (= Vth)")
    print(f"  short-circuit current  Isc = {i_short * 1000:8.4f} mA       (= In)")
    print(f"  Rth = Voc / Isc            = {r_th / 1000:8.4f} kOhm")
    print(f"  Rth with sources dead      = {r_dead / 1000:8.4f} kOhm")
    print(f"  {'load':>10s} {'original':>11s} {'Thevenin':>11s} {'Norton':>11s} {'formula':>11s}")
    for load in loads:
        formula = v_th * load / (r_th + load)
        print(f"  {load:9.0f}Ohm"
              f" {load_voltage_original(network, load):10.5f}V"
              f" {load_voltage_thevenin(v_th, r_th, load):10.5f}V"
              f" {load_voltage_norton(i_short, r_th, load):10.5f}V"
              f" {formula:10.5f}V")
    return v_th, r_th


def main():
    study("Divider: 12 V, 6 kOhm over 3 kOhm, port across the 3 kOhm", divider,
          (100, 1000, 2000, 6000, 20000, 1e6))
    v_th, r_th = study("Workhorse seen from the terminals of R4 (node c and ground)", workhorse_without_r4,
                       (100, 1000, 3667, 10000, 1e6))
    print(f"\n  With R4 = 1 kOhm back in place: vc = {v_th:.4f} x 1 / ({r_th / 1000:.4f} + 1) = "
          f"{v_th * 1000 / (r_th + 1000):.4f} V  (Lessons 01-05 found 2.5 V)")
    print(f"  Hand values: Vth = 35/3 = {35 / 3:.4f} V, Rth = 11/3 = {11 / 3:.4f} kOhm, In = 35/11 = {35 / 11:.4f} mA")


if __name__ == "__main__":
    main()
