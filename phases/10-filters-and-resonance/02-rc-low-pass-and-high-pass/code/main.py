import cmath
import math

import numpy as np

from sim import Circuit

E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]


def low_pass_response(freq, resistance, capacitance):
    z_c = 1 / (1j * 2 * math.pi * freq * capacitance)
    return z_c / (resistance + z_c)


def high_pass_response(freq, resistance, capacitance):
    z_c = 1 / (1j * 2 * math.pi * freq * capacitance)
    return resistance / (resistance + z_c)


def rc_circuit(kind, resistance, capacitance, load=None):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    if kind == "low":
        c.resistor("R1", "in", "out", resistance)
        c.capacitor("C1", "out", "0", capacitance)
    else:
        c.capacitor("C1", "in", "out", capacitance)
        c.resistor("R1", "out", "0", resistance)
    if load:
        c.resistor("Rload", "out", "0", load)
    return c


def nearest_e12(value):
    decade = 10 ** math.floor(math.log10(value))
    candidates = [m * decade for m in E12] + [10 * decade]
    return min(candidates, key=lambda r: abs(math.log(r / value)))


def rise_time_10_90(t, v, final):
    t10 = t[np.argmax(v >= 0.1 * final)]
    t90 = t[np.argmax(v >= 0.9 * final)]
    return t90 - t10


def main():
    r, cap = 1000.0, 100e-9
    fc = 1 / (2 * math.pi * r * cap)
    print("=== Step 1: The low-pass from impedances, H = Z_C / (R + Z_C) = 1 / (1 + j 2 pi f R C) ===")
    print(f"  R = {r:.0f} ohm, C = {cap * 1e9:.0f} nF, fc = {fc:.1f} Hz")
    for freq in [fc / 10, fc / 2, fc, 2 * fc, 10 * fc]:
        h = low_pass_response(freq, r, cap)
        magnitude, angle = cmath.polar(h)
        print(f"  f = {freq:8.1f} Hz: H = {h.real:+.4f} {h.imag:+.4f}j, |H| = {magnitude:.4f}, phase = {math.degrees(angle):6.1f} deg")

    print("\n=== Step 2: The simulator's AC sweep agrees ===")
    freqs = np.logspace(1, 6, 501)
    sweep = rc_circuit("low", r, cap).ac(freqs, source="V1")
    formula = np.array([low_pass_response(f, r, cap) for f in freqs])
    print(f"  largest difference in |H| over 10 Hz .. 1 MHz: {np.abs(sweep.gain('out') - np.abs(formula)).max():.2e}")
    print(f"  cutoff found by the simulator: {sweep.cutoff('out'):.1f} Hz (formula {fc:.1f} Hz)")
    at_fc = rc_circuit("low", r, cap).ac([fc], source="V1")
    print(f"  phase at fc: {at_fc.phase_deg('out')[0]:.1f} deg")

    print("\n=== Step 3: The high-pass, H = R / (R + Z_C) ===")
    sweep_hp = rc_circuit("high", r, cap).ac(freqs, source="V1")
    spot = [fc / 10, fc, 10 * fc]
    spot_gain = rc_circuit("high", r, cap).ac(spot, source="V1").gain("out")
    for freq, simulated in zip(spot, spot_gain):
        h = high_pass_response(freq, r, cap)
        print(f"  f = {freq:8.1f} Hz: |H| = {abs(h):.4f} (sim {simulated:.4f}), "
              f"phase = {math.degrees(cmath.phase(h)):+5.1f} deg")
    print(f"  cutoff found by the simulator: {sweep_hp.cutoff('out'):.1f} Hz")

    print("\n=== Step 4: Design: choose R for a 1 kHz cutoff with C = 10 nF ===")
    target, cap2 = 1000.0, 10e-9
    exact = 1 / (2 * math.pi * target * cap2)
    standard = nearest_e12(exact)
    real_fc = 1 / (2 * math.pi * standard * cap2)
    check = rc_circuit("low", standard, cap2).ac(np.logspace(1, 6, 501), source="V1").cutoff("out")
    print(f"  exact R = 1 / (2 pi f C) = {exact:.0f} ohm, nearest E12 value {standard:.0f} ohm")
    print(f"  with {standard:.0f} ohm: fc = {real_fc:.0f} Hz (simulator {check:.0f} Hz)")

    print("\n=== Step 5: A load on the output moves the cutoff ===")
    for load in [None, 100e3, 10e3, 1e3]:
        sweep_load = rc_circuit("low", r, cap, load).ac(freqs, source="V1")
        label = "no load" if load is None else f"{load / 1000:.0f} k load"
        print(f"  {label:<10}: DC gain {sweep_load.gain('out')[0]:.3f}, cutoff {sweep_load.cutoff('out'):7.1f} Hz")

    print("\n=== Step 6: Time and frequency are two views of one circuit ===")
    c = Circuit()
    c.pulse_source("V1", "in", "0", low=0.0, high=1.0, period=10e-3, duty=0.5)
    c.resistor("R1", "in", "out", r)
    c.capacitor("C1", "out", "0", cap)
    run = c.transient(t_stop=2e-3, dt=1e-7)
    rise = rise_time_10_90(np.asarray(run.time), np.asarray(run.v("out")), 1.0)
    tau = r * cap
    print(f"  tau = R C = {tau * 1e6:.0f} us, fc = 1 / (2 pi tau) = {1 / (2 * math.pi * tau):.1f} Hz")
    print(f"  10-90 % rise time from the simulator: {rise * 1e6:.1f} us (2.2 tau = {2.2 * tau * 1e6:.1f} us, 0.35 / fc = {0.35 / fc * 1e6:.1f} us)")


if __name__ == "__main__":
    main()
