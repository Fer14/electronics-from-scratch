import numpy as np

from sim import Circuit

BATTERY_VOLTS = 9.0
RESISTOR_OHMS = 1000.0
CAPACITOR_FARADS = 100e-6
T_STOP = 0.6
DT = 1e-4


def build_charging_circuit():
    circuit = Circuit()
    circuit.voltage_source("B1", "plus", "0", BATTERY_VOLTS)
    circuit.resistor("R1", "plus", "top", RESISTOR_OHMS)
    circuit.capacitor("C1", "top", "0", CAPACITOR_FARADS, v0=0.0)
    return circuit


def charge_moved(time, current):
    steps = np.diff(time)
    return np.concatenate([[0.0], np.cumsum(steps * (current[1:] + current[:-1]) / 2)])


def value_at(time, values, moment):
    return float(np.interp(moment, time, values))


def show_charging():
    result = build_charging_circuit().transient(t_stop=T_STOP, dt=DT)
    time = np.asarray(result.time)
    capacitor_volts = np.asarray(result.v("top"))
    current = np.asarray(result.i("R1"))
    charge = charge_moved(time, current)
    print("Charging a 100 uF capacitor from a 9 V battery through 1 kOhm")
    print(f"{'time (ms)':>10} {'current (mA)':>13} {'charge moved (uC)':>18} {'cap voltage (V)':>16} {'Q / V (uF)':>11}")
    for moment in (0.001, 0.05, 0.1, 0.2, 0.3, 0.5):
        q = value_at(time, charge, moment)
        v = value_at(time, capacitor_volts, moment)
        print(f"{moment * 1e3:>10.0f} {value_at(time, current, moment) * 1e3:>13.3f} "
              f"{q * 1e6:>18.1f} {v:>16.3f} {q / v * 1e6:>11.2f}")
    print(f"Total charge pushed onto the top plate: {charge[-1] * 1e6:.1f} uC")
    print(f"Charge a full 9 V needs on 100 uF:      {CAPACITOR_FARADS * BATTERY_VOLTS * 1e6:.1f} uC")
    print()


def show_holding():
    circuit = Circuit()
    circuit.capacitor("C1", "top", "0", CAPACITOR_FARADS, v0=BATTERY_VOLTS)
    circuit.resistor("Rmeter", "top", "0", 10e6)
    result = circuit.transient(t_stop=10.0, dt=1e-2)
    time = np.asarray(result.time)
    capacitor_volts = np.asarray(result.v("top"))
    print("Battery removed: the charged capacitor watched by a 10 MOhm voltmeter")
    for moment in (0.0, 1.0, 5.0, 10.0):
        print(f"  after {moment:>4.0f} s the capacitor still shows {value_at(time, capacitor_volts, moment):.3f} V")
    print()


def show_electron_count():
    electron_charge = 1.602e-19
    stored = CAPACITOR_FARADS * BATTERY_VOLTS
    print(f"900 uC is {stored / electron_charge:.2e} electrons moved from one plate to the other")


if __name__ == "__main__":
    show_charging()
    show_holding()
    show_electron_count()
