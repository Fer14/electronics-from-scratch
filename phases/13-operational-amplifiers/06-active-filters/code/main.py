import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

FREQS = np.logspace(1, 5, 401)


def inverting_low_pass():
    circuit = Circuit()
    circuit.sine_source("VIN", "in", "0", amplitude=1.0, freq=1000.0)
    circuit.resistor("RI", "in", "n", 1e3)
    circuit.resistor("RF", "n", "out", 10e3)
    circuit.capacitor("CF", "n", "out", 15.9e-9)
    circuit.opamp("U1", plus="0", minus="n", out="out", gain=1e5)
    return circuit


def passive_two_stage(r, c):
    circuit = Circuit()
    circuit.sine_source("VIN", "in", "0", amplitude=1.0, freq=1000.0)
    circuit.resistor("R1", "in", "a", r)
    circuit.capacitor("C1", "a", "0", c)
    circuit.resistor("R2", "a", "out", r)
    circuit.capacitor("C2", "out", "0", c)
    return circuit


def sallen_key_low_pass(r, c_feedback, c_ground):
    circuit = Circuit()
    circuit.sine_source("VIN", "in", "0", amplitude=1.0, freq=1000.0)
    circuit.resistor("R1", "in", "a", r)
    circuit.resistor("R2", "a", "p", r)
    circuit.capacitor("C1", "a", "out", c_feedback)
    circuit.capacitor("C2", "p", "0", c_ground)
    circuit.opamp("U1", plus="p", minus="out", out="out", gain=1e5)
    return circuit


def sallen_key_high_pass(r_feedback, r_ground, c):
    circuit = Circuit()
    circuit.sine_source("VIN", "in", "0", amplitude=1.0, freq=1000.0)
    circuit.capacitor("C1", "in", "a", c)
    circuit.capacitor("C2", "a", "p", c)
    circuit.resistor("R1", "a", "out", r_feedback)
    circuit.resistor("R2", "p", "0", r_ground)
    circuit.opamp("U1", plus="p", minus="out", out="out", gain=1e5)
    return circuit


def gains_at(result, points):
    return [result.gain_db_at(f, "out") for f in points]


def show_first_order():
    result = inverting_low_pass().ac(FREQS, source="VIN")
    corner = 1 / (2 * math.pi * 10e3 * 15.9e-9)
    print("First-order active low-pass: inverting amp, gain -R_F/R_I = -10, with C_F = 15.9 nF across R_F")
    print(f"  pass-band gain {result.gain_db_at(10.0, 'out'):.2f} dB (20 log 10 = 20 dB)")
    print(f"  cutoff: simulated {result.cutoff('out'):.0f} Hz, formula 1 / (2 pi R_F C_F) = {corner:.0f} Hz")
    print(f"  at 10 kHz: {result.gain_db_at(10e3, 'out'):.2f} dB   at 100 kHz: {result.gain_db_at(100e3, 'out'):.2f} dB (20 dB less per decade)")
    print()


def show_second_order():
    r = 10e3
    print("Second-order low-pass filters aimed at 1 kHz (R = 10 k)")
    designs = [
        ("passive RC-RC, C = 15.9 nF", passive_two_stage(r, 15.9e-9)),
        ("Sallen-Key Q 0.707 (22.5 n / 11.25 n)", sallen_key_low_pass(r, 22.5e-9, 11.25e-9)),
        ("Sallen-Key Q 2.0 (63.7 n / 3.98 n)", sallen_key_low_pass(r, 63.7e-9, 3.98e-9)),
    ]
    points = [100.0, 500.0, 1000.0, 2000.0, 10000.0]
    header = "".join(f"{p:>9.0f}Hz" for p in points)
    print(f"  {'design':<40}{header}   cutoff (-3 dB)")
    curves = []
    for label, circuit in designs:
        result = circuit.ac(FREQS, source="VIN")
        cells = "".join(f"{g:>9.2f}dB" for g in gains_at(result, points))
        print(f"  {label:<40}{cells}   {result.cutoff('out'):8.0f} Hz")
        curves.append((label, result))
    print("  The passive filter droops early (its second RC loads the first); Sallen-Key with Q = 0.707 is flat, then falls 40 dB/decade.")
    print(f"  Q = 0.707 design: f0 = 1 / (2 pi R sqrt(C1 C2)) = {1 / (2 * math.pi * r * math.sqrt(22.5e-9 * 11.25e-9)):.0f} Hz, Q = sqrt(C1/C2)/2 = {math.sqrt(2) / 2:.3f}")
    print()
    return curves


def show_high_pass():
    result = sallen_key_high_pass(11.25e3, 22.5e3, 10e-9).ac(FREQS, source="VIN")
    f0 = 1 / (2 * math.pi * 10e-9 * math.sqrt(22.5e3 * 11.25e3))
    print("Sallen-Key high-pass (swap every R and C), C = 10 nF, R1 = 11.25 k (to output), R2 = 22.5 k (to ground)")
    print(f"  f0 = 1 / (2 pi C sqrt(R1 R2)) = {f0:.0f} Hz")
    for f in [100.0, 500.0, 1000.0, 10e3]:
        print(f"  {f:>6.0f} Hz: {result.gain_db_at(f, 'out'):7.2f} dB")
    print()


def show_transient_check():
    circuit = Circuit()
    circuit.sine_source("VSIG", "s", "0", amplitude=1.0, freq=200.0)
    circuit.sine_source("VHUM", "in", "s", amplitude=1.0, freq=5000.0)
    circuit.resistor("R1", "in", "a", 10e3)
    circuit.resistor("R2", "a", "p", 10e3)
    circuit.capacitor("C1", "a", "out", 22.5e-9)
    circuit.capacitor("C2", "p", "0", 11.25e-9)
    circuit.opamp("U1", plus="p", minus="out", out="out", gain=1e5)
    result = circuit.transient(t_stop=20e-3, dt=5e-6)
    time = np.asarray(result.time)
    out = np.asarray(result.v("out"))[time > 10e-3]
    t = time[time > 10e-3]
    low = 2 * abs(np.mean(out * np.exp(-2j * np.pi * 200 * t)))
    high = 2 * abs(np.mean(out * np.exp(-2j * np.pi * 5000 * t)))
    print("Time domain: 1 V at 200 Hz plus 1 V at 5 kHz into the Q = 0.707 Sallen-Key low-pass")
    print(f"  output: {low:.3f} V at 200 Hz, {high:.4f} V at 5 kHz  (5 kHz is attenuated {20 * math.log10(high):.1f} dB)")


def plot(curves):
    figure, axis = plt.subplots(figsize=(7, 4))
    for label, result in curves:
        axis.semilogx(FREQS, result.gain_db("out"), label=label)
    axis.set_ylim(-60, 10)
    axis.set_xlabel("frequency (Hz)")
    axis.set_ylabel("gain (dB)")
    axis.set_title("second-order low-pass filters at 1 kHz")
    axis.grid(True, which="both", alpha=0.3)
    axis.legend(fontsize=8)
    figure.tight_layout()
    path = Path(__file__).parent / "out.png"
    figure.savefig(path, dpi=120)
    print(f"Saved the Bode plot to {path.name}")


def main():
    show_first_order()
    curves = show_second_order()
    show_high_pass()
    show_transient_check()
    plot(curves)


if __name__ == "__main__":
    main()
