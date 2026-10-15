from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal as scipy_signal

from sim import Circuit

RATE = 1000.0


def moving_average(x, taps):
    kernel = np.ones(taps) / taps
    return np.convolve(x, kernel, mode="full")[:len(x)]


def exponential_average(x, alpha):
    y = np.empty_like(x)
    state = x[0]
    for index, value in enumerate(x):
        state = state + alpha * (value - state)
        y[index] = state
    return y


def windowed_sinc(cutoff_hz, taps, rate=RATE):
    n = np.arange(taps) - (taps - 1) / 2
    ideal = 2 * cutoff_hz / rate * np.sinc(2 * cutoff_hz / rate * n)
    window = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(taps) / (taps - 1))
    kernel = ideal * window
    return kernel / kernel.sum()


def fir(x, kernel):
    return np.convolve(x, kernel, mode="full")[:len(x)]


def gain_at(kernel, frequency, rate=RATE):
    n = np.arange(len(kernel))
    return abs(np.sum(kernel * np.exp(-2j * np.pi * frequency * n / rate)))


def median_filter(x, width):
    half = width // 2
    padded = np.pad(x, half, mode="edge")
    return np.array([np.median(padded[i:i + width]) for i in range(len(x))])


def rc_step_from_sim(ohms, farads, seconds, dt):
    circuit = Circuit()
    circuit.pulse_source("VIN", "in", "0", low=0.0, high=1.0, period=4 * seconds, duty=0.5, delay=0.0)
    circuit.resistor("R1", "in", "out", ohms)
    circuit.capacitor("C1", "out", "0", farads, v0=0.0)
    result = circuit.transient(t_stop=seconds, dt=dt)
    return np.asarray(result.time), np.asarray(result.v("out"))


def main():
    dt = 1 / RATE
    seconds = 4.0
    t = np.arange(int(seconds * RATE)) * dt
    clean = 1.0 + 0.5 * np.sin(2 * np.pi * 1.0 * t)
    generator = np.random.default_rng(21)
    noisy = clean + 0.2 * generator.normal(0, 1, len(t)) + 0.3 * np.sin(2 * np.pi * 50 * t)
    noisy[2000] += 5.0

    print(f"A 1 Hz sensor signal sampled at {RATE:.0f} samples/s, with white noise (0.2 RMS), 50 Hz hum (0.3) and one spike")
    print(f"  RMS error of the raw samples: {np.sqrt(np.mean((noisy - clean) ** 2)):.3f}")

    print("\nMoving average: gain at a few frequencies (formula |sin(pi f N / fs) / (N sin(pi f / fs))|)")
    for taps in [5, 20, 50]:
        kernel = np.ones(taps) / taps
        row = []
        for frequency in [1, 25, 50, 100]:
            formula = abs(np.sin(np.pi * frequency * taps / RATE) / (taps * np.sin(np.pi * frequency / RATE)))
            row.append(f"{frequency:3d} Hz {gain_at(kernel, frequency):.3f} ({formula:.3f})")
        print(f"  N = {taps:2d}: " + ", ".join(row))
    print("  N = 20 spans exactly one 50 Hz period, so it has a perfect null at 50 Hz and every multiple")

    rc_ohms, rc_farads = 10_000, 10e-6
    tau = rc_ohms * rc_farads
    alpha = dt / (tau + dt)
    print(f"\nExponential average y += alpha (x - y) as the digital twin of an RC (tau = {tau * 1e3:.0f} ms)")
    print(f"  alpha = dt / (tau + dt) = {alpha:.5f}")
    sim_time, sim_out = rc_step_from_sim(rc_ohms, rc_farads, 0.5, dt)
    step = np.ones(len(sim_time))
    step[0] = 0.0
    ema_out = exponential_average(step, alpha)
    for moment in [0.01, 0.1, 0.2, 0.5]:
        index = int(round(moment / dt))
        print(f"  t = {moment * 1e3:4.0f} ms: RC in sim {sim_out[index]:.4f}, EMA {ema_out[index]:.4f}, "
              f"exact 1 - e^(-t/RC) = {1 - np.exp(-moment / tau):.4f}")

    kernel = windowed_sinc(10.0, 201)
    check = scipy_signal.firwin(201, 10.0, window="hamming", fs=RATE)
    print(f"\nWindowed-sinc FIR low-pass: 201 taps, cutoff 10 Hz, Hamming window "
          f"(largest difference from scipy.signal.firwin: {np.max(np.abs(kernel - check)):.2e})")
    for frequency in [1, 5, 10, 20, 50, 100]:
        gain = gain_at(kernel, frequency)
        print(f"  {frequency:4d} Hz: gain {gain:.4f} ({20 * np.log10(gain + 1e-15):7.1f} dB)")

    print("\nCleaning the noisy record (error measured after each filter's start-up, delay removed)")
    results = {
        "moving average N = 20": (moving_average(noisy, 20), (20 - 1) / 2),
        "moving average N = 100": (moving_average(noisy, 100), (100 - 1) / 2),
        "exponential, tau = 20 ms": (exponential_average(noisy, dt / (0.02 + dt)), 20.0),
        "windowed-sinc FIR, 10 Hz": (fir(noisy, kernel), 100.0),
        "median of 5 then FIR": (fir(median_filter(noisy, 5), kernel), 100.0),
    }
    settled = slice(500, len(t) - 300)
    print(f"  {'filter':26s} {'delay':>9s} {'RMS error':>10s} {'largest error':>14s}")
    for name, (output, delay_samples) in results.items():
        shift = int(round(delay_samples))
        aligned = np.roll(output, -shift)
        error = aligned[settled] - clean[settled]
        print(f"  {name:26s} {delay_samples * dt * 1e3:6.1f} ms {np.sqrt(np.mean(error ** 2)):10.4f} {np.max(np.abs(error)):14.4f}")

    figure, axis = plt.subplots(figsize=(9, 4))
    window = (t > 1.5) & (t < 2.5)
    axis.plot(t[window], noisy[window], color="#cccccc", linewidth=0.6, label="raw samples")
    axis.plot(t[window], np.roll(results["windowed-sinc FIR, 10 Hz"][0], -100)[window], color="#8a5a2b", label="FIR, delay removed")
    axis.plot(t[window], clean[window], color="black", linestyle="--", linewidth=0.8, label="true signal")
    axis.set_xlabel("time (s)")
    axis.legend(loc="upper right")
    figure.tight_layout()
    path = Path(__file__).parent / "filtering.png"
    figure.savefig(path, dpi=120)
    print(f"\nSaved {path.name}")


if __name__ == "__main__":
    main()
