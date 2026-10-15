from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

SUPPLY_VOLTS = 5.0
RESISTOR_OHMS = 1000.0
CAPACITOR_FARADS = 1e-6
TAU = RESISTOR_OHMS * CAPACITOR_FARADS
PERIOD = 20 * TAU


def small_steps_by_hand(step, steps):
    volts = 0.0
    rows = []
    for index in range(steps + 1):
        current = (SUPPLY_VOLTS - volts) / RESISTOR_OHMS
        rows.append((index * step, current, volts))
        volts += current * step / CAPACITOR_FARADS
    return rows


def show_small_steps():
    print("Charging step by step: every 0.2 ms the current refills the capacitor a little")
    print(f"{'time (ms)':>10} {'current (mA)':>13} {'cap volts (V)':>14} {'formula (V)':>12}")
    for time, current, volts in small_steps_by_hand(0.2e-3, 10):
        exact = SUPPLY_VOLTS * (1 - np.exp(-time / TAU))
        print(f"{time * 1e3:>10.1f} {current * 1e3:>13.3f} {volts:>14.3f} {exact:>12.3f}")
    print()


def simulate_square_wave():
    circuit = Circuit()
    circuit.pulse_source("V1", "in", "0", low=0.0, high=SUPPLY_VOLTS, period=PERIOD, duty=0.5)
    circuit.resistor("R1", "in", "cap", RESISTOR_OHMS)
    circuit.capacitor("C1", "cap", "0", CAPACITOR_FARADS, v0=0.0)
    result = circuit.transient(t_stop=PERIOD, dt=TAU / 1000)
    return np.asarray(result.time), np.asarray(result.v("in")), np.asarray(result.v("cap")), np.asarray(result.i("R1"))


def charging_formula(time):
    return SUPPLY_VOLTS * (1 - np.exp(-time / TAU))


def discharging_formula(time, start_volts):
    return start_volts * np.exp(-time / TAU)


def show_simulation(time, cap_volts, current):
    half = PERIOD / 2
    print("Simulated: 5 V for 10 ms (charging), then 0 V for 10 ms (discharging), R = 1 kOhm, C = 1 uF")
    print(f"{'phase':>12} {'t (ms)':>7} {'sim (V)':>8} {'formula (V)':>12} {'current (mA)':>13}")
    for multiple in (0.5, 1, 2, 3, 5):
        moment = multiple * TAU
        print(f"{'charging':>12} {moment * 1e3:>7.1f} {np.interp(moment, time, cap_volts):>8.3f} "
              f"{charging_formula(moment):>12.3f} {np.interp(moment, time, current) * 1e3:>13.3f}")
    start_volts = charging_formula(half)
    for multiple in (0.5, 1, 2, 3, 5):
        moment = half + multiple * TAU
        print(f"{'discharging':>12} {moment * 1e3:>7.1f} {np.interp(moment, time, cap_volts):>8.3f} "
              f"{discharging_formula(multiple * TAU, start_volts):>12.3f} {np.interp(moment, time, current) * 1e3:>13.3f}")
    print()


def save_plot(time, in_volts, cap_volts, current):
    figure, (top, bottom) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    top.plot(time * 1e3, in_volts, color="#8b5e3c", label="source")
    top.plot(time * 1e3, cap_volts, color="#2f6f4f", label="capacitor")
    top.set_ylabel("volts")
    top.legend()
    bottom.plot(time * 1e3, current * 1e3, color="#b0413e")
    bottom.axhline(0, color="gray", linewidth=0.5)
    bottom.set_ylabel("current (mA)")
    bottom.set_xlabel("time (ms)")
    figure.tight_layout()
    path = Path(__file__).parent / "charge_discharge.png"
    figure.savefig(path, dpi=120)
    print(f"Plot saved to {path.name}")


if __name__ == "__main__":
    show_small_steps()
    time, in_volts, cap_volts, current = simulate_square_wave()
    show_simulation(time, cap_volts, current)
    save_plot(time, in_volts, cap_volts, current)
