import numpy as np

from sim import Circuit

CAPACITY_AH = 2.5
R_INTERNAL = 0.06
R_POLARIZATION = 0.04
C_POLARIZATION = 40_000.0
V_MAX = 4.2
V_CUTOFF = 3.0
SOC_POINTS = np.array([0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
OCV_POINTS = np.array([3.00, 3.30, 3.45, 3.55, 3.62, 3.67, 3.72, 3.78, 3.86, 3.95, 4.06, 4.20])


def open_circuit_voltage(soc):
    return float(np.interp(soc, SOC_POINTS, OCV_POINTS))


def solve_cell(soc, v_polarization, charger):
    circuit = Circuit()
    circuit.voltage_source("OCV", "e", "0", open_circuit_voltage(soc))
    circuit.voltage_source("VP", "p", "e", v_polarization)
    circuit.resistor("RINT", "term", "p", R_INTERNAL)
    kind, value = charger
    if kind == "current_in":
        circuit.current_source("CHG", "0", "term", value)
    elif kind == "voltage":
        circuit.voltage_source("CHG", "term", "0", value)
    else:
        circuit.current_source("LOAD", "term", "0", value)
    result = circuit.dc()
    return result.v("term"), result.i("RINT")


def step_state(soc, v_polarization, current_in, dt):
    soc += current_in * dt / (CAPACITY_AH * 3600)
    v_polarization += dt * (current_in / C_POLARIZATION - v_polarization / (R_POLARIZATION * C_POLARIZATION))
    return soc, v_polarization


def discharge(current, dt=30.0):
    soc, v_p, seconds, charge, energy, heat = 1.0, 0.0, 0.0, 0.0, 0.0, 0.0
    while True:
        terminal, _ = solve_cell(soc, v_p, ("load", current))
        if terminal <= V_CUTOFF or soc <= 0:
            break
        charge += current * dt
        energy += terminal * current * dt
        heat += current ** 2 * R_INTERNAL * dt + v_p ** 2 / R_POLARIZATION * dt
        soc, v_p = step_state(soc, v_p, -current, dt)
        seconds += dt
    return seconds, charge / 3600, energy / 3600, heat / 3600, soc


def charge_cc_cv(current, start_soc=0.0, dt=30.0, stop_fraction=0.05):
    soc, v_p, seconds = start_soc, 0.0, 0.0
    log, cc_end, energy = [], None, 0.0
    phase = "CC"
    while True:
        if phase == "CC":
            terminal, i_cell = solve_cell(soc, v_p, ("current_in", current))
            i_in = i_cell
            if terminal >= V_MAX:
                phase, cc_end = "CV", (seconds, soc)
                continue
        else:
            terminal, i_cell = solve_cell(soc, v_p, ("voltage", V_MAX))
            i_in = i_cell
            if i_in <= stop_fraction * CAPACITY_AH:
                break
        if int(seconds) % 600 == 0:
            log.append((seconds, phase, i_in, terminal, soc))
        energy += terminal * i_in * dt
        soc, v_p = step_state(soc, v_p, i_in, dt)
        seconds += dt
    return seconds, soc, cc_end, log, energy / 3600


def main():
    print(f"Cell: {CAPACITY_AH} Ah lithium-ion, R_internal {R_INTERNAL * 1e3:.0f} mohm, "
          f"polarization {R_POLARIZATION * 1e3:.0f} mohm / {C_POLARIZATION:.0f} F (tau {R_POLARIZATION * C_POLARIZATION / 60:.0f} min)")
    print("  open-circuit voltage by state of charge: " +
          ", ".join(f"{int(s * 100)}% {v:.2f} V" for s, v in zip(SOC_POINTS[::2], OCV_POINTS[::2])))

    print(f"\nDischarging from full to the {V_CUTOFF} V cut-off")
    print(f"  {'current':>8s} {'C-rate':>6s} {'time':>8s} {'Ah out':>7s} {'Wh out':>7s} {'heat Wh':>8s} {'left in cell':>12s}")
    for current in [0.5, 2.5, 5.0, 10.0]:
        seconds, amp_hours, watt_hours, heat, soc_left = discharge(current)
        print(f"  {current:6.1f} A {current / CAPACITY_AH:5.1f}C {seconds / 3600:6.2f} h {amp_hours:6.3f} {watt_hours:6.2f} "
              f"{heat:8.3f} {soc_left * 100:10.1f}%")

    current = 0.5 * CAPACITY_AH
    seconds, soc, cc_end, log, energy_in = charge_cc_cv(current)
    print(f"\nCC/CV charge at {current:.2f} A (0.5C) up to {V_MAX} V, stopping when the current falls to 0.05C")
    print(f"  {'time':>7s} {'phase':>5s} {'current':>8s} {'terminal':>9s} {'charge':>7s}")
    for moment, phase, amps, volts, state in log:
        print(f"  {moment / 60:5.0f} min {phase:>5s} {amps:6.3f} A {volts:7.3f} V {state * 100:6.1f}%")
    print(f"  CC phase ended after {cc_end[0] / 60:.0f} min at {cc_end[1] * 100:.1f}% charged;"
          f" total {seconds / 60:.0f} min, finished at {soc * 100:.1f}%")
    _, _, out_energy, _, _ = discharge(current)
    print(f"  energy in {energy_in:.2f} Wh; the same cell gives back about {out_energy:.2f} Wh at 0.5C "
          f"(round trip {out_energy / energy_in * 100:.0f}%)")

    print("\nBuilding a pack from these cells")
    for series, parallel in [(1, 1), (3, 1), (3, 2), (4, 4)]:
        volts = 3.7 * series
        amp_hours = CAPACITY_AH * parallel
        print(f"  {series}S{parallel}P: nominal {volts:4.1f} V, {amp_hours:4.1f} Ah, {volts * amp_hours:5.1f} Wh, "
              f"internal resistance {R_INTERNAL * series / parallel * 1e3:5.1f} mohm")


if __name__ == "__main__":
    main()
