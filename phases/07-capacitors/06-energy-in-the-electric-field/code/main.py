import math

import numpy as np

from sim import Circuit

SUPPLY_VOLTS = 9.0
CAPACITOR_FARADS = 100e-6


def stored_energy(farads, volts):
    return 0.5 * farads * volts ** 2


def show_examples():
    print("Energy stored E = 1/2 * C * V^2")
    examples = [
        ("100 uF at 9 V", 100e-6, 9.0),
        ("100 uF at 18 V (double voltage)", 100e-6, 18.0),
        ("200 uF at 9 V (double capacitance)", 200e-6, 9.0),
        ("camera flash, 120 uF at 330 V", 120e-6, 330.0),
        ("supercapacitor, 10 F at 2.7 V", 10.0, 2.7),
    ]
    for label, farads, volts in examples:
        print(f"  {label:<36} {stored_energy(farads, volts):>10.4g} J")
    print(f"  {'AA alkaline cell, 2.5 Ah at 1.2 V':<36} {2.5 * 3600 * 1.2:>10.4g} J")
    print()


def integrate(time, values):
    return float(np.sum(np.diff(time) * (values[1:] + values[:-1]) / 2))


def charge_through(ohms):
    circuit = Circuit()
    circuit.voltage_source("B1", "plus", "0", SUPPLY_VOLTS)
    circuit.resistor("R1", "plus", "top", ohms)
    circuit.capacitor("C1", "top", "0", CAPACITOR_FARADS, v0=0.0)
    tau = ohms * CAPACITOR_FARADS
    result = circuit.transient(t_stop=12 * tau, dt=tau / 1000)
    time = np.asarray(result.time)
    current = np.asarray(result.i("R1"))
    cap_volts = np.asarray(result.v("top"))
    from_battery = integrate(time, SUPPLY_VOLTS * current)
    into_capacitor = integrate(time, cap_volts * current)
    in_resistor = integrate(time, current ** 2 * ohms)
    return from_battery, into_capacitor, in_resistor


def show_half_is_lost():
    print("Charging 100 uF to 9 V through different resistors (simulated, energies in mJ)")
    print(f"{'R (ohm)':>8} {'battery gave':>13} {'capacitor got':>14} {'resistor heat':>14} {'efficiency':>11}")
    for ohms in (10.0, 1000.0, 100e3):
        from_battery, into_capacitor, in_resistor = charge_through(ohms)
        print(f"{ohms:>8.0f} {from_battery * 1e3:>13.3f} {into_capacitor * 1e3:>14.3f} "
              f"{in_resistor * 1e3:>14.3f} {into_capacitor / from_battery * 100:>10.1f}%")
    print(f"Formula: battery gives C*V^2 = {CAPACITOR_FARADS * SUPPLY_VOLTS ** 2 * 1e3:.3f} mJ, "
          f"capacitor keeps 1/2*C*V^2 = {stored_energy(CAPACITOR_FARADS, SUPPLY_VOLTS) * 1e3:.3f} mJ")
    print()


def hold_up_time(farads, load_ohms, start_volts, minimum_volts):
    return load_ohms * farads * math.log(start_volts / minimum_volts)


def show_hold_up():
    farads, load, start, minimum = 220e-6, 100.0, 5.0, 3.0
    print("Hold-up: a 220 uF capacitor keeps a 100 ohm load alive after the supply fails")
    print(f"  usable energy between 5 V and 3 V: {(stored_energy(farads, start) - stored_energy(farads, minimum)) * 1e3:.3f} mJ")
    print(f"  formula: time to fall from 5 V to 3 V = R*C*ln(5/3) = {hold_up_time(farads, load, start, minimum) * 1e3:.2f} ms")
    circuit = Circuit()
    circuit.capacitor("C1", "rail", "0", farads, v0=start)
    circuit.resistor("Rload", "rail", "0", load)
    result = circuit.transient(t_stop=40e-3, dt=10e-6)
    time = np.asarray(result.time)
    volts = np.asarray(result.v("rail"))
    print(f"  simulator: rail at 10 ms = {np.interp(10e-3, time, volts):.3f} V, "
          f"drops below 3 V at {time[int(np.argmax(volts < minimum))] * 1e3:.2f} ms")


if __name__ == "__main__":
    show_examples()
    show_half_is_lost()
    show_hold_up()
