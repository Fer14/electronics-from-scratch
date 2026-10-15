import numpy as np

from sim import Circuit

ELECTRON_CHARGE = 1.602e-19
THERMAL_VOLTAGE = 0.025852
SILICON_PERMITTIVITY_F_PER_CM = 11.7 * 8.854e-14
NI = 1.0e10


def built_in_potential(acceptors, donors):
    return THERMAL_VOLTAGE * np.log(acceptors * donors / NI**2)


def depletion_width_cm(acceptors, donors, applied=0.0):
    barrier = built_in_potential(acceptors, donors) - applied
    return np.sqrt(2 * SILICON_PERMITTIVITY_F_PER_CM * barrier / ELECTRON_CHARGE * (1 / acceptors + 1 / donors))


def side_widths_cm(acceptors, donors, applied=0.0):
    total = depletion_width_cm(acceptors, donors, applied)
    into_n = total * acceptors / (acceptors + donors)
    return total - into_n, into_n


def peak_field_v_per_cm(acceptors, donors, applied=0.0):
    barrier = built_in_potential(acceptors, donors) - applied
    return 2 * barrier / depletion_width_cm(acceptors, donors, applied)


def show_built_in():
    print("Built-in potential V_bi = V_T * ln(N_A * N_D / n_i^2)")
    for acceptors, donors in [(1e15, 1e15), (1e17, 1e16), (1e18, 1e18), (1e19, 1e16)]:
        print(f"  N_A = {acceptors:.0e}, N_D = {donors:.0e}  ->  V_bi = {built_in_potential(acceptors, donors):.3f} V")
    print()


def show_depletion(acceptors, donors):
    print(f"Junction with N_A = {acceptors:.0e} (p side) and N_D = {donors:.0e} (n side) per cm^3")
    print(f"  {'applied V':>10} {'barrier V':>10} {'width um':>9} {'into p um':>10} {'into n um':>10} {'peak field kV/cm':>17} {'C nF/cm^2':>10}")
    for applied in [0.6, 0.4, 0.0, -1.0, -5.0, -20.0]:
        width = depletion_width_cm(acceptors, donors, applied)
        into_p, into_n = side_widths_cm(acceptors, donors, applied)
        capacitance = SILICON_PERMITTIVITY_F_PER_CM / width
        barrier = built_in_potential(acceptors, donors) - applied
        print(f"  {applied:>10.1f} {barrier:>10.3f} {width * 1e4:>9.3f} {into_p * 1e4:>10.3f} {into_n * 1e4:>10.3f} "
              f"{peak_field_v_per_cm(acceptors, donors, applied) / 1e3:>17.1f} {capacitance * 1e9:>10.2f}")
    print()


def show_hill_climbers(acceptors, donors):
    barrier = built_in_potential(acceptors, donors)
    print("Fraction of carriers energetic enough to climb the hill, relative to zero bias")
    print("  (each extra 0.0596 V of forward bias multiplies it by 10)")
    for applied in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
        ratio = np.exp(applied / THERMAL_VOLTAGE)
        print(f"  forward V = {applied:.1f} V   hill = {barrier - applied:.3f} V   climbers x {ratio:10.3e}")
    print()


def one_way_street():
    print("Our simulator: 5 V source, 1 kohm resistor, silicon diode")
    for label, anode, cathode in [("forward (anode toward +)", "a", "0"), ("reverse (anode toward ground)", "0", "a")]:
        circuit = Circuit()
        circuit.voltage_source("V1", "in", "0", 5.0)
        circuit.resistor("R1", "in", "a", 1000)
        circuit.diode("D1", anode, cathode, Is=1e-14, n=1.0)
        result = circuit.dc()
        print(f"  {label:<30} V(diode) = {result.v('a'):7.4f} V   I = {result.i('R1') * 1000:10.6f} mA")
    print()


def main():
    show_built_in()
    show_depletion(1e17, 1e16)
    show_hill_climbers(1e17, 1e16)
    one_way_street()


if __name__ == "__main__":
    main()
