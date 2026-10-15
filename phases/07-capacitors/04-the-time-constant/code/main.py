import math

import numpy as np

from sim import Circuit

SUPPLY_VOLTS = 5.0


def show_tau_table():
    print("How far a charging capacitor gets after whole numbers of tau")
    print(f"{'time':>6} {'charged (%)':>12} {'still missing (%)':>18}")
    for multiple in range(1, 6):
        charged = 1 - math.exp(-multiple)
        print(f"{multiple:>4} t {charged * 100:>12.1f} {(1 - charged) * 100:>18.1f}")
    print()


def time_to_reach(threshold, supply, tau):
    return tau * math.log(supply / (supply - threshold))


def simulate_rc(ohms, farads, t_stop):
    circuit = Circuit()
    circuit.voltage_source("V1", "in", "0", SUPPLY_VOLTS)
    circuit.resistor("R1", "in", "cap", ohms)
    circuit.capacitor("C1", "cap", "0", farads, v0=0.0)
    result = circuit.transient(t_stop=t_stop, dt=t_stop / 5000)
    return np.asarray(result.time), np.asarray(result.v("cap"))


def first_crossing(time, volts, threshold):
    index = int(np.argmax(volts >= threshold))
    if volts[index] < threshold:
        return float("nan")
    if index == 0:
        return float(time[0])
    t0, t1, v0, v1 = time[index - 1], time[index], volts[index - 1], volts[index]
    return float(t0 + (threshold - v0) * (t1 - t0) / (v1 - v0))


def show_crossings():
    print("Simulated time to cross thresholds vs the formula t = tau * ln(V / (V - Vth))")
    print(f"{'R':>8} {'C':>8} {'tau (ms)':>9} {'Vth (V)':>8} {'sim (ms)':>9} {'formula (ms)':>13}")
    for ohms, farads in ((10e3, 100e-9), (4.7e3, 1e-6), (100e3, 10e-6)):
        tau = ohms * farads
        time, volts = simulate_rc(ohms, farads, 6 * tau)
        for threshold in (2.5, SUPPLY_VOLTS * (1 - math.exp(-1)), 4.5):
            print(f"{ohms / 1e3:>6.1f}k {farads * 1e6:>6.2f}u {tau * 1e3:>9.3f} {threshold:>8.2f} "
                  f"{first_crossing(time, volts, threshold) * 1e3:>9.3f} {time_to_reach(threshold, SUPPLY_VOLTS, tau) * 1e3:>13.3f}")
    print()


def show_rise_time():
    tau = 1e-3
    t10 = time_to_reach(0.1 * SUPPLY_VOLTS, SUPPLY_VOLTS, tau)
    t90 = time_to_reach(0.9 * SUPPLY_VOLTS, SUPPLY_VOLTS, tau)
    print(f"10%-90% rise time for tau = 1 ms: {(t90 - t10) * 1e3:.3f} ms (about 2.2 tau)")
    print(f"Half-way point for tau = 1 ms:    {time_to_reach(0.5 * SUPPLY_VOLTS, SUPPLY_VOLTS, tau) * 1e3:.3f} ms (about 0.69 tau)")
    print()


def design_reset_delay(delay, threshold, farads):
    tau = delay / math.log(SUPPLY_VOLTS / (SUPPLY_VOLTS - threshold))
    return tau / farads


def show_design():
    farads = 100e-9
    ohms = design_reset_delay(5e-3, 2.5, farads)
    print(f"Reset delay design: 5 ms to reach 2.5 V with 100 nF needs R = {ohms / 1e3:.1f} kOhm")
    time, volts = simulate_rc(68e3, farads, 40e-3)
    print(f"With the nearest standard value 68 kOhm the simulator crosses 2.5 V at {first_crossing(time, volts, 2.5) * 1e3:.2f} ms")


if __name__ == "__main__":
    show_tau_table()
    show_crossings()
    show_rise_time()
    show_design()
