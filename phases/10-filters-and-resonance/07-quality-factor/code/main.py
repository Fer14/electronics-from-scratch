import math

import numpy as np

from sim import Circuit

L = 10e-3
C = 1e-6
F0 = 1 / (2 * math.pi * math.sqrt(L * C))
FREQS = np.logspace(math.log10(F0) - 1, math.log10(F0) + 1, 8001)


def series_band_pass(resistance):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=F0)
    c.inductor("L1", "in", "a", L)
    c.capacitor("C1", "a", "out", C)
    c.resistor("R1", "out", "0", resistance)
    return c


def measured_bandwidth(resistance):
    g = series_band_pass(resistance).ac(FREQS, source="V1").gain_db("out")
    target = g.max() - 3.0103
    peak = int(np.argmax(g))
    logf = np.log10(FREQS)
    low = 10 ** np.interp(target, g[:peak + 1], logf[:peak + 1])
    high = 10 ** np.interp(target, g[peak:][::-1], logf[peak:][::-1])
    return low, high


def q_from_parts(resistance):
    return math.sqrt(L / C) / resistance


def ring_down(resistance, cycles=40):
    c = Circuit()
    c.capacitor("C1", "top", "0", C, v0=1.0)
    c.inductor("L1", "top", "m", L)
    c.resistor("R1", "m", "0", resistance)
    period = 1 / F0
    run = c.transient(t_stop=cycles * period, dt=period / 400)
    v = np.asarray(run.v("top"))
    t = np.asarray(run.time)
    peaks = [n for n in range(1, len(v) - 1) if v[n] > v[n - 1] and v[n] >= v[n + 1] and v[n] > 0]
    return t[peaks], v[peaks]


def main():
    print(f"=== Step 1: Three ways to get Q for L = 10 mH, C = 1 uF (f0 = {F0:.1f} Hz) ===")
    print("      R    Q = sqrt(L/C)/R    f_low     f_high    BW       Q = f0 / BW")
    for resistance in [1.0, 3.3, 10.0, 33.0, 100.0]:
        low, high = measured_bandwidth(resistance)
        bw = high - low
        print(f"  {resistance:6.1f}   {q_from_parts(resistance):9.2f}       {low:8.1f}  {high:8.1f}  {bw:7.1f}   {F0 / bw:9.2f}")

    print("\n=== Step 2: Q as stored energy over energy lost per cycle (R = 10 ohm, 1 V drive) ===")
    resistance = 10.0
    current = 1.0 / resistance
    stored = 0.5 * L * current**2
    lost_per_cycle = 0.5 * current**2 * resistance / F0
    print(f"  peak current {current * 1000:.0f} mA, energy sloshing between L and C = 1/2 L I^2 = {stored * 1e6:.1f} uJ")
    print(f"  heat per cycle = (1/2 I^2 R) x T = {lost_per_cycle * 1e6:.2f} uJ")
    print(f"  Q = 2 pi x stored / lost = {2 * math.pi * stored / lost_per_cycle:.2f}")

    print("\n=== Step 3: Ringing: high Q rings for about Q cycles ===")
    for resistance in [1.0, 10.0, 33.0]:
        times, peaks = ring_down(resistance, cycles=150 if resistance == 1.0 else 40)
        q = q_from_parts(resistance)
        ratio = peaks[1] / peaks[0]
        below = np.where(peaks < math.exp(-math.pi))[0]
        cycles = int(below[0]) if len(below) else len(peaks)
        print(f"  R = {resistance:5.1f} ohm, Q = {q:6.2f}: each peak is {ratio:.4f} of the one before "
              f"(e^(-pi/Q) = {math.exp(-math.pi / q):.4f}); falls below 4.3 % after {cycles} cycles")

    print("\n=== Step 4: Selectivity: a neighbour 10 % above f0 ===")
    neighbour = 1.1 * F0
    for resistance in [1.0, 10.0, 100.0]:
        g = series_band_pass(resistance).ac([F0, neighbour], source="V1").gain_db("out")
        print(f"  Q = {q_from_parts(resistance):6.2f}: wanted {g[0]:+6.2f} dB, neighbour {g[1]:+7.2f} dB, rejection {g[0] - g[1]:5.1f} dB")

    print("\n=== Step 5: A tank's impedance at resonance grows with Q ===")
    for dcr in [10.0, 1.0, 0.1]:
        q = q_from_parts(dcr)
        print(f"  coil resistance {dcr:4.1f} ohm: Q = {q:6.1f}, tank impedance Q x sqrt(L/C) = {q * math.sqrt(L / C) / 1000:7.1f} k ohm")


if __name__ == "__main__":
    main()
