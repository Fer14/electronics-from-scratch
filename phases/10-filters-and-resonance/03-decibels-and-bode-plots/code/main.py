import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

R = 1000.0
C = 100e-9


def voltage_db(ratio):
    return 20 * math.log10(ratio)


def power_db(ratio):
    return 10 * math.log10(ratio)


def db_to_voltage_ratio(db):
    return 10 ** (db / 20)


def dbm(watts):
    return 10 * math.log10(watts / 1e-3)


def low_pass(c, a, b, tag):
    c.resistor(f"R{tag}", a, b, R)
    c.capacitor(f"C{tag}", b, "0", C)


def single_stage():
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    low_pass(c, "in", "out", "1")
    return c


def two_stages(buffered):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    low_pass(c, "in", "mid", "1")
    if buffered:
        c.vcvs("E1", "buf", "0", "mid", "0", 1.0)
        low_pass(c, "buf", "out", "2")
    else:
        low_pass(c, "mid", "out", "2")
    return c


def asymptote_db(freqs, fc):
    return np.where(freqs < fc, 0.0, -20 * np.log10(freqs / fc))


def save_bode(freqs, gain_db, phase, fc, path):
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    top.semilogx(freqs, gain_db, color="saddlebrown", label="simulator")
    top.semilogx(freqs, asymptote_db(freqs, fc), "k--", label="straight-line asymptotes")
    top.axvline(fc, color="gray", linestyle=":")
    top.set_ylabel("gain (dB)")
    top.legend()
    top.grid(True, which="both", alpha=0.3)
    bottom.semilogx(freqs, phase, color="saddlebrown")
    bottom.axvline(fc, color="gray", linestyle=":")
    bottom.set_ylabel("phase (deg)")
    bottom.set_xlabel("frequency (Hz)")
    bottom.grid(True, which="both", alpha=0.3)
    fig.suptitle(f"Bode plot of an RC low-pass, fc = {fc:.0f} Hz")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main():
    print("=== Step 1: Logarithms: how many times you multiply by 10 ===")
    for value in [1, 10, 100, 1000, 0.1, 0.01, 2, 5, 0.5]:
        print(f"  log10({value:>5}) = {math.log10(value):+.3f}   check: 10^{math.log10(value):+.3f} = {10 ** math.log10(value):.3f}")
    print(f"  log10(2 x 5) = {math.log10(10):.3f} = log10(2) + log10(5) = {math.log10(2) + math.log10(5):.3f}")

    print("\n=== Step 2: Voltage ratios in decibels, 20 log10(Vout / Vin) ===")
    for ratio in [10, 2, 1.414, 1, 0.7071, 0.5, 0.1, 0.01, 0.001]:
        print(f"  ratio {ratio:>7}: {voltage_db(ratio):+7.2f} dB")
    print("  power ratios use 10 log10:")
    for ratio in [2, 0.5, 100]:
        print(f"  power ratio {ratio:>5}: {power_db(ratio):+6.2f} dB")
    print("  back from dB to a voltage ratio:")
    for db in [-3, -6, -20, -40, 6]:
        print(f"  {db:+3d} dB = x {db_to_voltage_ratio(db):.4f}")

    print("\n=== Step 3: dB relative to a fixed reference ===")
    for watts in [1e-3, 1.0, 100e-6, 0.5]:
        print(f"  {watts * 1000:8.3f} mW = {dbm(watts):+6.1f} dBm")

    fc = 1 / (2 * math.pi * R * C)
    print(f"\n=== Step 4: Bode plot of the RC low-pass (fc = {fc:.1f} Hz) ===")
    freqs = np.logspace(1, 6, 501)
    sweep = single_stage().ac(freqs, source="V1")
    gain_db = sweep.gain_db("out")
    for f in [fc / 100, fc / 10, fc, 10 * fc, 100 * fc]:
        print(f"  f = {f:9.1f} Hz: {sweep.gain_db_at(f, 'out'):+7.2f} dB, asymptote {asymptote_db(np.array([f]), fc)[0]:+7.2f} dB")
    decade = sweep.gain_db_at(100 * fc, "out") - sweep.gain_db_at(10 * fc, "out")
    octave = sweep.gain_db_at(20 * fc, "out") - sweep.gain_db_at(10 * fc, "out")
    print(f"  slope far above fc: {decade:.2f} dB per decade, {octave:.2f} dB per octave")
    print(f"  largest gap between the curve and the asymptotes: {np.abs(gain_db - asymptote_db(freqs, fc)).max():.2f} dB")

    print("\n=== Step 5: Two stages: dB add up only if the stages do not load each other ===")
    buffered = two_stages(True).ac(freqs, source="V1")
    loaded = two_stages(False).ac(freqs, source="V1")
    for f in [fc, 10 * fc, 100 * fc]:
        one = sweep.gain_db_at(f, "out")
        print(f"  f = {f:9.1f} Hz: one stage {one:+7.2f} dB, two x one = {2 * one:+7.2f} dB, "
              f"buffered {buffered.gain_db_at(f, 'out'):+7.2f} dB, loaded {loaded.gain_db_at(f, 'out'):+7.2f} dB")
    slope = buffered.gain_db_at(100 * fc, "out") - buffered.gain_db_at(10 * fc, "out")
    print(f"  buffered slope: {slope:.1f} dB per decade; buffered cutoff {buffered.cutoff('out'):.0f} Hz, loaded cutoff {loaded.cutoff('out'):.0f} Hz")

    path = Path(__file__).parent / "out.png"
    save_bode(freqs, gain_db, sweep.phase_deg("out"), fc, path)
    print(f"\nBode plot saved to {path.name}")


if __name__ == "__main__":
    main()
