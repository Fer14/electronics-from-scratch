import cmath
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit


def z_resistor(ohms, freq):
    return complex(ohms, 0.0)


def z_capacitor(farads, freq):
    return 1 / (1j * 2 * math.pi * freq * farads)


def z_inductor(henries, freq):
    return 1j * 2 * math.pi * freq * henries


def series(*impedances):
    return sum(impedances)


def parallel(*impedances):
    return 1 / sum(1 / z for z in impedances)


def polar_text(z, unit):
    return f"{abs(z):9.4g} {unit} at {math.degrees(cmath.phase(z)):7.2f} deg"


def rect_text(z, unit):
    sign = "+" if z.imag >= 0 else "-"
    return f"{z.real:.4g} {sign} j{abs(z.imag):.4g} {unit}"


def measured_impedance(build, freq):
    c = Circuit()
    c.sine_source("V1", "top", "0", amplitude=1.0, freq=freq)
    build(c)
    a = c.ac([freq], source="V1")
    return complex(a.v("top")[0]) / complex(a.i("V1")[0])


def main():
    r, cap, ind = 1000.0, 1e-6, 10e-3

    print("=== Step 1: How R, C and L respond to frequency ===")
    print(f"  {'f (Hz)':>8} {'|Z_R| (ohm)':>12} {'|Z_C| (ohm)':>12} {'|Z_L| (ohm)':>12}")
    for f in (10.0, 100.0, 1000.0, 10_000.0, 100_000.0):
        print(f"  {f:>8.0f} {abs(z_resistor(r, f)):>12.1f} {abs(z_capacitor(cap, f)):>12.2f} {abs(z_inductor(ind, f)):>12.2f}")
    print(f"  (R = 1 kohm, C = 1 uF, L = 10 mH)")

    print("\n=== Step 2: Ohm's law with impedance, V = Z I ===")
    f = 1000.0
    for name, z in (("R = 1 kohm", z_resistor(r, f)), ("C = 1 uF", z_capacitor(cap, f)), ("L = 10 mH", z_inductor(ind, f))):
        current = 1.0 / z
        print(f"  1 V at 1 kHz across {name:<11} Z = {rect_text(z, 'ohm'):<22} I = {polar_text(current * 1000, 'mA')}")

    print("\n=== Step 3: Series R, L and C at 1 kHz ===")
    zs = series(z_resistor(100.0, f), z_inductor(ind, f), z_capacitor(cap, f))
    print(f"  Z = 100 + j{z_inductor(ind, f).imag:.2f} - j{-z_capacitor(cap, f).imag:.2f} = {rect_text(zs, 'ohm')}")
    print(f"    = {polar_text(zs, 'ohm')}")
    print(f"  current from a 1 V source: {polar_text(1 / zs * 1000, 'mA')}")
    sim_zs = measured_impedance(lambda c: (c.resistor("R1", "top", "x", 100.0),
                                           c.inductor("L1", "x", "y", ind),
                                           c.capacitor("C1", "y", "0", cap)), f)
    print(f"  simulator: V / I = {rect_text(sim_zs, 'ohm')}")

    print("\n=== Step 4: R in parallel with C at 1 kHz ===")
    zp = parallel(z_resistor(r, f), z_capacitor(cap, f))
    print(f"  Z = 1 / (1/1000 + 1/({rect_text(z_capacitor(cap, f), 'ohm')})) = {rect_text(zp, 'ohm')}")
    print(f"    = {polar_text(zp, 'ohm')}  (smaller than either part alone)")
    sim_zp = measured_impedance(lambda c: (c.resistor("R1", "top", "0", r), c.capacitor("C1", "top", "0", cap)), f)
    print(f"  simulator: V / I = {rect_text(sim_zp, 'ohm')}")

    print("\n=== Step 5: An impedance divider: L in series, R to ground ===")
    l_div, r_div = 22e-3, 100.0
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=50.0)
    c.inductor("L1", "in", "out", l_div)
    c.resistor("R1", "out", "0", r_div)
    freqs = np.array([50.0, 723.0, 10_000.0])
    a = c.ac(freqs, source="V1")
    for k, fk in enumerate(freqs):
        by_hand = z_resistor(r_div, fk) / series(z_inductor(l_div, fk), z_resistor(r_div, fk))
        print(f"  f = {fk:>7.0f} Hz: hand V(out) = {polar_text(by_hand, 'V')} "
              f"({20 * math.log10(abs(by_hand)):6.2f} dB), simulator {a.gain_db('out')[k]:6.2f} dB")

    sweep = np.logspace(1, 5, 200)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.loglog(sweep, np.full_like(sweep, r), label="resistor 1 kohm")
    ax.loglog(sweep, np.abs(z_capacitor(cap, sweep)), label="capacitor 1 uF")
    ax.loglog(sweep, np.abs(z_inductor(ind, sweep)), label="inductor 10 mH")
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("|Z| (ohm)")
    ax.grid(True, which="both", lw=0.3)
    ax.legend()
    fig.tight_layout()
    out_path = Path(__file__).parent / "out.png"
    fig.savefig(out_path, dpi=110)
    print(f"\n  plot saved to {out_path.name}")


if __name__ == "__main__":
    main()
