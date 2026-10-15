import numpy as np

from sim import Circuit

EPSILON_0 = 8.854e-12


def plate_capacitance(area_m2, gap_m, relative_permittivity=1.0):
    return EPSILON_0 * relative_permittivity * area_m2 / gap_m


def show_plate_examples():
    print("Parallel-plate capacitance C = eps0 * eps_r * A / d")
    examples = [
        ("two 10 cm x 10 cm plates, 1 mm of air", 0.01, 1e-3, 1.0),
        ("same plates, gap shrunk to 0.1 mm", 0.01, 1e-4, 1.0),
        ("same plates, 0.1 mm of polyester film", 0.01, 1e-4, 3.3),
        ("same plates, 0.1 mm of ceramic (X7R-like)", 0.01, 1e-4, 3000.0),
        ("a 1 m x 1 m sheet, 10 um of polyester", 1.0, 10e-6, 3.3),
    ]
    for label, area, gap, eps_r in examples:
        farads = plate_capacitance(area, gap, eps_r)
        print(f"  {label:<45} {farads * 1e9:>12.3f} nF")
    print()


def plate_area_needed(target_farads, gap_m, relative_permittivity):
    return target_farads * gap_m / (EPSILON_0 * relative_permittivity)


def show_area_for_one_microfarad():
    area = plate_area_needed(1e-6, 1e-3, 1.0)
    print(f"Plate area for 1 uF with 1 mm of air: {area:,.0f} m^2 (a square {np.sqrt(area):.0f} m on a side)")
    area = plate_area_needed(1e-6, 5e-6, 3.3)
    print(f"Plate area for 1 uF with 5 um of polyester: {area:.3f} m^2 (rolled up inside a film capacitor)")
    print()


def ramp_with_constant_current(farads, amps=1e-3, t_stop=2e-3):
    circuit = Circuit()
    circuit.current_source("I1", "0", "top", amps)
    circuit.capacitor("C1", "top", "0", farads, v0=0.0)
    result = circuit.transient(t_stop=t_stop, dt=1e-6)
    time = np.asarray(result.time)
    volts = np.asarray(result.v("top"))
    slope = np.polyfit(time, volts, 1)[0]
    return slope, float(np.interp(1e-3, time, volts))


def show_constant_current_ramps():
    print("Pushing a steady 1 mA into different capacitors (simulated)")
    print(f"{'capacitor':>11} {'v after 1 ms (V)':>17} {'slope (V/ms)':>13} {'I / slope (uF)':>15}")
    for farads in (0.47e-6, 1e-6, 2.2e-6, 10e-6):
        slope, volts_at_1ms = ramp_with_constant_current(farads)
        print(f"{farads * 1e6:>9.2f}uF {volts_at_1ms:>17.3f} {slope / 1e3:>13.3f} {1e-3 / slope * 1e6:>15.3f}")
    print()


def show_charge_voltage_table():
    farads = 47e-6
    print("Q = C * V for a 47 uF capacitor")
    for volts in (1.0, 3.3, 5.0, 12.0):
        print(f"  {volts:>5.1f} V  ->  {farads * volts * 1e6:>7.1f} uC")


if __name__ == "__main__":
    show_plate_examples()
    show_area_for_one_microfarad()
    show_constant_current_ramps()
    show_charge_voltage_table()
