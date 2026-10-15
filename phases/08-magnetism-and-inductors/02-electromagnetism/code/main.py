import numpy as np

from sim import Circuit

MU0 = 4 * np.pi * 1e-7


def field_around_long_wire(current, distance):
    return MU0 * current / (2 * np.pi * distance)


def biot_savart_straight_wire(current, distance, half_length, pieces):
    edges = np.linspace(-half_length, half_length, pieces + 1)
    centres = (edges[:-1] + edges[1:]) / 2
    piece_length = edges[1] - edges[0]
    r_squared = centres**2 + distance**2
    contributions = MU0 / (4 * np.pi) * current * piece_length * distance / r_squared**1.5
    return contributions.sum()


def field_on_axis_of_loop(current, radius, z):
    return MU0 * current * radius**2 / (2 * (radius**2 + z**2) ** 1.5)


def biot_savart_loop_on_axis(current, radius, z, pieces):
    angles = np.linspace(0, 2 * np.pi, pieces, endpoint=False)
    step = 2 * np.pi / pieces
    positions = np.stack([radius * np.cos(angles), radius * np.sin(angles), np.zeros(pieces)], axis=1)
    pieces_dl = np.stack([-np.sin(angles), np.cos(angles), np.zeros(pieces)], axis=1) * radius * step
    point = np.array([0.0, 0.0, z])
    to_point = point - positions
    distances = np.linalg.norm(to_point, axis=1)[:, None]
    contributions = MU0 / (4 * np.pi) * current * np.cross(pieces_dl, to_point) / distances**3
    return contributions.sum(axis=0)[2]


def solenoid_field(turns, length, current, relative_permeability=1.0):
    return relative_permeability * MU0 * (turns / length) * current


def force_on_wire(field, current, length):
    return field * current * length


def force_per_metre_between_wires(current_a, current_b, separation):
    return MU0 * current_a * current_b / (2 * np.pi * separation)


def relay_coil_current(supply_volts, series_ohms, coil_ohms):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", supply_volts)
    c.resistor("R1", "vcc", "coil", series_ohms)
    c.resistor("Rcoil", "coil", "0", coil_ohms)
    result = c.dc()
    return result.i("Rcoil"), result.v("coil"), result.p("R1")


def main():
    print("=== Step 1: Field around a long straight wire, B = mu0 I / (2 pi r) ===")
    for current, distance in [(1, 0.01), (10, 0.01), (10, 0.02), (100, 0.05)]:
        b = field_around_long_wire(current, distance)
        print(f"  I = {current:>4} A at r = {distance * 100:>4.1f} cm -> B = {b * 1e6:>8.1f} uT")

    print("\n=== Step 2: Check the formula by adding up tiny pieces of wire ===")
    exact = field_around_long_wire(10, 0.01)
    for pieces in [10, 100, 1000, 100000]:
        summed = biot_savart_straight_wire(10, 0.01, 1.0, pieces)
        print(f"  {pieces:>6} pieces of a 2 m wire: B = {summed * 1e6:.3f} uT (formula {exact * 1e6:.3f} uT)")

    print("\n=== Step 3: A single loop, at its centre and along its axis ===")
    for z in [0.0, 0.01, 0.02, 0.05]:
        formula = field_on_axis_of_loop(2.0, 0.02, z)
        summed = biot_savart_loop_on_axis(2.0, 0.02, z, 360)
        print(f"  loop R = 2 cm, I = 2 A, z = {z * 100:>3.0f} cm: formula {formula * 1e6:7.2f} uT, sum {summed * 1e6:7.2f} uT")

    print("\n=== Step 4: Solenoid, B = mu0 (N / l) I ===")
    turns, length, current = 500, 0.05, 0.5
    air = solenoid_field(turns, length, current)
    print(f"  {turns} turns over {length * 100:.0f} cm with {current} A: n = {turns / length:.0f} turns/m")
    print(f"  air core: B = {air * 1e3:.2f} mT")
    for mu_r in [10, 100]:
        print(f"  core with effective mu_r = {mu_r:>3}: B = {solenoid_field(turns, length, current, mu_r) * 1e3:.1f} mT")

    print("\n=== Step 5: Forces on wires ===")
    print(f"  5 cm of wire, 2 A, across 0.2 T: F = {force_on_wire(0.2, 2, 0.05) * 1e3:.1f} mN")
    per_metre = force_per_metre_between_wires(10, 10, 0.01)
    print(f"  two wires 1 cm apart, 10 A each: {per_metre * 1e3:.2f} mN per metre")
    print(f"  definition check, 1 A each, 1 m apart: {force_per_metre_between_wires(1, 1, 1):.1e} N per metre")

    print("\n=== Step 6: Driving a relay coil (our simulator) ===")
    for series in [100, 470, 1000]:
        i_coil, v_coil, p_series = relay_coil_current(24.0, series, 400.0)
        status = "pulls in" if 0.025 <= i_coil <= 0.035 else "out of range"
        print(f"  24 V, series {series:>4} ohm, coil 400 ohm: I = {i_coil * 1e3:5.1f} mA, "
              f"V_coil = {v_coil:5.2f} V, P_series = {p_series * 1e3:5.0f} mW -> {status}")


if __name__ == "__main__":
    main()
