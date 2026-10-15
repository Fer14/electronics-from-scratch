from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

PEAK_VOLTS = 12.0
FREQUENCY = 50.0
LOAD_OHMS = 1000.0
STOP_TIME = 0.1
TIME_STEP = 2e-5


def half_wave(capacitance):
    circuit = Circuit()
    circuit.sine_source("V1", "ac", "0", amplitude=PEAK_VOLTS, freq=FREQUENCY, offset=0.0)
    circuit.diode("D1", "ac", "out")
    circuit.resistor("RL", "out", "0", LOAD_OHMS)
    if capacitance:
        circuit.capacitor("C1", "out", "0", capacitance, v0=0.0)
    return circuit.transient(t_stop=STOP_TIME, dt=TIME_STEP)


def full_wave_bridge(capacitance):
    circuit = Circuit()
    circuit.sine_source("V1", "ac1", "ac2", amplitude=PEAK_VOLTS, freq=FREQUENCY, offset=0.0)
    circuit.diode("D1", "ac1", "out")
    circuit.diode("D2", "ac2", "out")
    circuit.diode("D3", "0", "ac1")
    circuit.diode("D4", "0", "ac2")
    circuit.resistor("RL", "out", "0", LOAD_OHMS)
    if capacitance:
        circuit.capacitor("C1", "out", "0", capacitance, v0=0.0)
    return circuit.transient(t_stop=STOP_TIME, dt=TIME_STEP)


def last_cycle(time, values):
    window = time >= STOP_TIME - 1.0 / FREQUENCY
    return values[window]


def summarize(label, result, diode="D1"):
    time = np.asarray(result.time)
    output = np.asarray(result.v("out"))
    diode_current = np.asarray(result.i(diode))
    cycle = last_cycle(time, output)
    peak_current = np.max(last_cycle(time, diode_current))
    print(f"  {label:<34} peak {cycle.max():6.2f} V   min {cycle.min():6.2f} V   ripple {cycle.max() - cycle.min():6.3f} V   "
          f"average {cycle.mean():6.2f} V   peak diode current {peak_current * 1000:6.1f} mA")
    return cycle


def ripple_estimate(capacitance, pulses_per_second):
    load_current = (PEAK_VOLTS - 0.75) / LOAD_OHMS
    return load_current / (pulses_per_second * capacitance)


def show_estimates():
    print("Hand estimates (diode drop about 0.75 V, load current about (12 - 0.75)/1000 = 11.25 mA)")
    for capacitance in [100e-6, 470e-6]:
        print(f"  C = {capacitance * 1e6:4.0f} uF   half-wave ripple ~ I/(f C) = {ripple_estimate(capacitance, 50):5.3f} V"
              f"   full-wave ripple ~ I/(2 f C) = {ripple_estimate(capacitance, 100):5.3f} V")
    print()


def plot(results):
    figure, axes = plt.subplots(len(results), 1, figsize=(9, 2.4 * len(results)), sharex=True)
    for axis, (label, result) in zip(axes, results):
        time = np.asarray(result.time) * 1000
        axis.plot(time, np.asarray(result.v("out")), label="output")
        axis.set_title(label)
        axis.set_ylabel("volts")
        axis.set_ylim(-1, 13)
    axes[-1].set_xlabel("time (ms)")
    figure.tight_layout()
    path = Path(__file__).parent / "out.png"
    figure.savefig(path, dpi=110)
    print(f"Saved the waveforms to {path.name}")


def main():
    print(f"Input: sine wave, {PEAK_VOLTS} V peak, {FREQUENCY:.0f} Hz; load {LOAD_OHMS:.0f} ohm; last 20 ms of {STOP_TIME * 1000:.0f} ms")
    print()
    show_estimates()
    print("Simulated")
    runs = []
    for label, maker, capacitance in [
        ("half-wave, no capacitor", half_wave, 0.0),
        ("half-wave, 100 uF", half_wave, 100e-6),
        ("half-wave, 470 uF", half_wave, 470e-6),
        ("full-wave bridge, no capacitor", full_wave_bridge, 0.0),
        ("full-wave bridge, 100 uF", full_wave_bridge, 100e-6),
        ("full-wave bridge, 470 uF", full_wave_bridge, 470e-6),
    ]:
        result = maker(capacitance)
        summarize(label, result)
        runs.append((label, result))
    print()
    plot([runs[0], runs[2], runs[3], runs[5]])


if __name__ == "__main__":
    main()
