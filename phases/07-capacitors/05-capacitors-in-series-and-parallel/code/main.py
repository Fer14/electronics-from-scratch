import math

import numpy as np

from sim import Circuit

SUPPLY_VOLTS = 5.0
RESISTOR_OHMS = 1000.0


def parallel(*capacitors):
    return sum(capacitors)


def series(*capacitors):
    return 1.0 / sum(1.0 / c for c in capacitors)


def show_formulas():
    print("Combining capacitors (all values in uF)")
    print(f"  1 + 2.2 in parallel          = {parallel(1, 2.2):.3f}")
    print(f"  4.7 and 10 in series         = {series(4.7, 10):.3f}")
    print(f"  two 10 in series             = {series(10, 10):.3f}")
    print(f"  three 1 in parallel          = {parallel(1, 1, 1):.3f}")
    print(f"  (1 || 1) in series with 2    = {series(parallel(1, 1), 2):.3f}")
    print()


def first_crossing(time, volts, threshold):
    index = int(np.argmax(volts >= threshold))
    t0, t1, v0, v1 = time[index - 1], time[index], volts[index - 1], volts[index]
    return float(t0 + (threshold - v0) * (t1 - t0) / (v1 - v0))


def measured_capacitance(circuit):
    result = circuit.transient(t_stop=20e-3, dt=2e-6)
    time = np.asarray(result.time)
    volts = np.asarray(result.v("top"))
    half_time = first_crossing(time, volts, SUPPLY_VOLTS / 2)
    return half_time / math.log(2) / RESISTOR_OHMS


def rc_with_parallel_pair(c1, c2):
    circuit = Circuit()
    circuit.voltage_source("V1", "in", "0", SUPPLY_VOLTS)
    circuit.resistor("R1", "in", "top", RESISTOR_OHMS)
    circuit.capacitor("C1", "top", "0", c1, v0=0.0)
    circuit.capacitor("C2", "top", "0", c2, v0=0.0)
    return circuit


def rc_with_series_pair(c1, c2):
    circuit = Circuit()
    circuit.voltage_source("V1", "in", "0", SUPPLY_VOLTS)
    circuit.resistor("R1", "in", "top", RESISTOR_OHMS)
    circuit.capacitor("C1", "top", "mid", c1, v0=0.0)
    circuit.capacitor("C2", "mid", "0", c2, v0=0.0)
    return circuit


def show_measured():
    print("Measuring the combination with the simulator: time to reach half the supply = 0.693 * R * C")
    measured = measured_capacitance(rc_with_parallel_pair(1e-6, 2.2e-6))
    print(f"  1 uF || 2.2 uF : measured {measured * 1e6:.3f} uF, formula {parallel(1, 2.2):.3f} uF")
    measured = measured_capacitance(rc_with_series_pair(4.7e-6, 10e-6))
    print(f"  4.7 uF + 10 uF in series: measured {measured * 1e6:.3f} uF, formula {series(4.7, 10):.3f} uF")
    print()


def show_series_voltage_split():
    c1, c2 = 1e-6, 2e-6
    circuit = Circuit()
    circuit.voltage_source("V1", "in", "0", 9.0)
    circuit.resistor("R1", "in", "top", 100.0)
    circuit.capacitor("C1", "top", "mid", c1, v0=0.0)
    circuit.capacitor("C2", "mid", "0", c2, v0=0.0)
    result = circuit.transient(t_stop=5e-3, dt=1e-6)
    v_top = float(np.asarray(result.v("top"))[-1])
    v_mid = float(np.asarray(result.v("mid"))[-1])
    print("1 uF on top of 2 uF in series, charged from 9 V")
    print(f"  across the 1 uF: {v_top - v_mid:.3f} V (formula 9 * 2 / 3 = {9 * c2 / (c1 + c2):.3f} V)")
    print(f"  across the 2 uF: {v_mid:.3f} V (formula 9 * 1 / 3 = {9 * c1 / (c1 + c2):.3f} V)")
    print(f"  charge on each: {c1 * (v_top - v_mid) * 1e6:.3f} uC and {c2 * v_mid * 1e6:.3f} uC")


if __name__ == "__main__":
    show_formulas()
    show_measured()
    show_series_voltage_split()
