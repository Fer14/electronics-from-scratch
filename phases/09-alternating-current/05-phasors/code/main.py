import cmath
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit


def phasor(amplitude, phase_deg):
    return cmath.rect(amplitude, math.radians(phase_deg))


def wave(p, freq, t):
    return np.imag(p * np.exp(1j * 2 * np.pi * freq * t))


def polar_text(p, unit):
    return f"{abs(p):.4g} {unit} at {math.degrees(cmath.phase(p)):7.2f} deg"


def fit_phasor(time, signal, freq):
    omega = 2 * np.pi * freq
    basis = np.column_stack([np.sin(omega * time), np.cos(omega * time)])
    (a_sin, a_cos), *_ = np.linalg.lstsq(basis, signal, rcond=None)
    return complex(a_sin, a_cos)


def main():
    freq = 50.0
    omega = 2 * math.pi * freq
    t = np.arange(0, 0.04, 1e-6)

    print("=== Step 1: Adding two sine waves by adding their phasors ===")
    v1, v2 = phasor(3.0, 0.0), phasor(4.0, 90.0)
    total = v1 + v2
    print(f"  v1 = 3 sin(wt)         -> phasor {v1:.4f} = {polar_text(v1, 'V')}")
    print(f"  v2 = 4 sin(wt + 90)    -> phasor {v2:.4f} = {polar_text(v2, 'V')}")
    print(f"  v1 + v2                -> phasor {total:.4f} = {polar_text(total, 'V')}")
    sampled_sum = wave(v1, freq, t) + wave(v2, freq, t)
    error = np.max(np.abs(sampled_sum - wave(total, freq, t)))
    print(f"  biggest difference between sampled sum and the phasor's wave = {error:.2e} V")
    print(f"  peak of the sum = {sampled_sum.max():.4f} V, not 3 + 4 = 7 V")

    print("\n=== Step 2: Taking a derivative is multiplying by j omega ===")
    v = phasor(10.0, 0.0)
    slope = np.gradient(wave(v, freq, t), t)
    measured = fit_phasor(t, slope, freq)
    print(f"  v = 10 sin(2 pi 50 t), omega = {omega:.2f} rad/s")
    print(f"  phasor of dv/dt from samples = {polar_text(measured, 'V/s')}")
    print(f"  j omega V                    = {polar_text(1j * omega * v, 'V/s')}")

    print("\n=== Step 3: A capacitor's current leads its voltage by 90 deg ===")
    cap = 1e-6
    predicted = 1j * omega * cap * v
    c = Circuit()
    c.sine_source("V1", "a", "0", amplitude=10.0, freq=freq)
    c.capacitor("C1", "a", "0", cap)
    tr = c.transient(t_stop=0.04, dt=1e-5)
    keep = tr.time >= 0.02
    simulated = fit_phasor(tr.time[keep], tr.i("C1")[keep], freq)
    print(f"  I = j omega C V, C = 1 uF: predicted {polar_text(predicted * 1000, 'mA')}")
    print(f"  from the transient simulation:  {polar_text(simulated * 1000, 'mA')}")

    print("\n=== Step 4: An inductor's voltage leads its current by 90 deg ===")
    inductance, current = 0.1, phasor(0.2, 0.0)
    print(f"  V = j omega L I, L = 100 mH, I = 0.2 A at 0 deg -> V = {polar_text(1j * omega * inductance * current, 'V')}")

    print("\n=== Step 5: Series R and C at 1 kHz, solved with phasors ===")
    f_rc, r_ohms, c_farads = 1000.0, 1000.0, 159.15e-9
    w_rc = 2 * math.pi * f_rc
    source = phasor(1.0, 0.0)
    cap_factor = 1 / (1j * w_rc * c_farads)
    i_loop = source / (r_ohms + cap_factor)
    v_r = r_ohms * i_loop
    v_c = cap_factor * i_loop
    print(f"  1 / (j omega C) = {cap_factor:.2f} ohm")
    print(f"  I   = 1 / ({r_ohms:.0f} + ({cap_factor:.1f})) = {polar_text(i_loop * 1000, 'mA')}")
    print(f"  V_R = R I            = {v_r:.4f} V = {polar_text(v_r, 'V')}")
    print(f"  V_C = I / (j omega C) = {v_c:.4f} V = {polar_text(v_c, 'V')}")
    print(f"  V_R + V_C = {v_r + v_c:.4f} V (KVL holds), but |V_R| + |V_C| = {abs(v_r) + abs(v_c):.4f} V")
    rc = Circuit()
    rc.sine_source("V1", "in", "0", amplitude=1.0, freq=f_rc)
    rc.resistor("R1", "in", "out", r_ohms)
    rc.capacitor("C1", "out", "0", c_farads)
    a = rc.ac([f_rc], source="V1")
    sim_vc = complex(a.v("out")[0])
    sim_vr = complex(a.v("in")[0] - a.v("out")[0])
    print(f"  simulator ac(): V_C = {sim_vc:.4f} V, V_R = {sim_vr:.4f} V")

    fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4.5))
    for p, label in ((source, "source"), (v_r, "V_R"), (v_c, "V_C")):
        left.annotate("", xy=(p.real, p.imag), xytext=(0, 0), arrowprops=dict(arrowstyle="->", lw=2))
        left.text(p.real, p.imag, f" {label}")
    left.set_xlim(-0.2, 1.2)
    left.set_ylim(-0.7, 0.7)
    left.set_aspect("equal")
    left.axhline(0, color="gray", lw=0.5)
    left.axvline(0, color="gray", lw=0.5)
    left.set_xlabel("real (V)")
    left.set_ylabel("imaginary (V)")
    left.set_title("phasors at 1 kHz")
    t_ms = np.arange(0, 2e-3, 1e-6)
    for p, label in ((source, "source"), (v_r, "V_R"), (v_c, "V_C")):
        right.plot(1000 * t_ms, wave(p, f_rc, t_ms), label=label)
    right.set_xlabel("time (ms)")
    right.set_ylabel("volts")
    right.legend()
    fig.tight_layout()
    out_path = Path(__file__).parent / "out.png"
    fig.savefig(out_path, dpi=110)
    print(f"\n  plot saved to {out_path.name}")


if __name__ == "__main__":
    main()
