import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit


def sine(t, amplitude, freq, phase_deg=0.0):
    return amplitude * np.sin(2 * np.pi * freq * t + np.radians(phase_deg))


def rising_zero_crossings(time, signal):
    below = signal[:-1] < 0
    above = signal[1:] >= 0
    hits = np.where(below & above)[0]
    fraction = -signal[hits] / (signal[hits + 1] - signal[hits])
    return time[hits] + fraction * (time[hits + 1] - time[hits])


def measure_frequency(time, signal):
    crossings = rising_zero_crossings(time, signal)
    periods = np.diff(crossings)
    return 1.0 / periods.mean()


def measure_lag_deg(time, reference, delayed, freq):
    t_ref = rising_zero_crossings(time, reference)
    t_del = rising_zero_crossings(time, delayed)
    lag_s = t_del[-1] - t_ref[t_ref <= t_del[-1]][-1]
    return 360.0 * lag_s * freq, lag_s


def main():
    print("=== Step 1: Samples of a 10 V, 50 Hz sine wave over one period ===")
    amplitude, freq = 10.0, 50.0
    period = 1.0 / freq
    for step in range(9):
        t = step * period / 8
        angle_deg = 360.0 * t / period
        print(f"  t = {1000 * t:5.2f} ms   angle = {angle_deg:5.1f} deg   v = {sine(t, amplitude, freq):7.3f} V")

    print("\n=== Step 2: Frequency, period and angular frequency ===")
    for f in (50.0, 60.0, 440.0, 1000.0):
        omega = 2 * math.pi * f
        print(f"  f = {f:7.1f} Hz   T = {1000 / f:7.3f} ms   omega = 2 pi f = {omega:9.2f} rad/s")
    print(f"  1 radian = {math.degrees(1):.4f} deg,  90 deg = {math.radians(90):.4f} rad")

    print("\n=== Step 3: Measure an unknown frequency from samples ===")
    time = np.arange(0, 0.1, 1e-6)
    mystery = sine(time, 3.0, 137.0, phase_deg=20.0)
    print(f"  measured frequency = {measure_frequency(time, mystery):.3f} Hz (true value 137 Hz)")

    print("\n=== Step 4: Phase difference between two sine waves ===")
    leader = sine(time, 5.0, 50.0)
    follower = sine(time, 5.0, 50.0, phase_deg=-60.0)
    lag_deg, lag_s = measure_lag_deg(time, leader, follower, 50.0)
    print(f"  time shift = {1000 * lag_s:.4f} ms of a {1000 / 50:.0f} ms period")
    print(f"  phase      = 360 x {1000 * lag_s:.4f} / 20 = {lag_deg:.2f} deg (the follower lags)")

    print("\n=== Step 5: A resistor and a capacitor shift the phase (simulated) ===")
    r_ohms, c_farads, f_test = 1000.0, 159.15e-9, 1000.0
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=f_test)
    c.resistor("R1", "in", "out", r_ohms)
    c.capacitor("C1", "out", "0", c_farads)
    t = c.transient(t_stop=10e-3, dt=1e-6)
    settled = t.time >= 6e-3
    time_s, v_in, v_out = t.time[settled], t.v("in")[settled], t.v("out")[settled]
    out_amplitude = (v_out.max() - v_out.min()) / 2
    lag_deg, lag_s = measure_lag_deg(time_s, v_in, v_out, f_test)
    print(f"  R = {r_ohms:.0f} ohm, C = {c_farads * 1e9:.2f} nF, f = {f_test:.0f} Hz, input amplitude 1.000 V")
    print(f"  output amplitude = {out_amplitude:.4f} V")
    print(f"  output lags the input by {1e6 * lag_s:.1f} us = {lag_deg:.1f} deg")

    fig, (top, bottom) = plt.subplots(2, 1, figsize=(8, 6))
    window = time < 0.04
    top.plot(1000 * time[window], leader[window], label="leader, phase 0 deg")
    top.plot(1000 * time[window], follower[window], label="follower, phase -60 deg")
    top.set_xlabel("time (ms)")
    top.set_ylabel("volts")
    top.legend()
    bottom.plot(1000 * time_s, v_in, label="input")
    bottom.plot(1000 * time_s, v_out, label="capacitor voltage")
    bottom.set_xlabel("time (ms)")
    bottom.set_ylabel("volts")
    bottom.legend()
    fig.tight_layout()
    out_path = Path(__file__).parent / "out.png"
    fig.savefig(out_path, dpi=110)
    print(f"\n  plot saved to {out_path.name}")


if __name__ == "__main__":
    main()
