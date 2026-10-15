import cmath
import math

import numpy as np

from sim import Circuit

FREQS = np.logspace(1, 6, 501)


def rl_low_pass_response(freq, resistance, inductance):
    z_l = 1j * 2 * math.pi * freq * inductance
    return resistance / (resistance + z_l)


def rl_cutoff(resistance, inductance):
    return resistance / (2 * math.pi * inductance)


PART = {"R": "resistor", "L": "inductor", "C": "capacitor"}


def series_then_shunt(series, shunt, dcr=0.0):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    start = "in"
    if dcr:
        c.resistor("Rdcr", "in", "w", dcr)
        start = "w"
    getattr(c, PART[series[0]])("Xseries", start, "out", series[1])
    getattr(c, PART[shunt[0]])("Xshunt", "out", "0", shunt[1])
    return c


def main():
    r, inductance = 100.0, 10e-3
    fc = rl_cutoff(r, inductance)
    print("=== Step 1: RL low-pass, H = R / (R + j 2 pi f L), fc = R / (2 pi L) ===")
    print(f"  R = {r:.0f} ohm, L = {inductance * 1e3:.0f} mH -> fc = {fc:.1f} Hz, tau = L / R = {inductance / r * 1e6:.0f} us")
    for freq in [fc / 10, fc, 10 * fc]:
        h = rl_low_pass_response(freq, r, inductance)
        print(f"  f = {freq:8.1f} Hz: |Z_L| = {2 * math.pi * freq * inductance:8.1f} ohm, |H| = {abs(h):.4f}, "
              f"phase = {math.degrees(cmath.phase(h)):6.1f} deg")

    print("\n=== Step 2: Same cutoff, same curve: RL low-pass vs RC low-pass (simulator) ===")
    rl = series_then_shunt(("L", inductance), ("R", r)).ac(FREQS, source="V1")
    cap = 1 / (2 * math.pi * fc * 1000.0)
    rc = series_then_shunt(("R", 1000.0), ("C", cap)).ac(FREQS, source="V1")
    print(f"  RC partner: R = 1 k, C = {cap * 1e9:.1f} nF")
    print(f"  cutoffs: RL {rl.cutoff('out'):.1f} Hz, RC {rc.cutoff('out'):.1f} Hz")
    print(f"  largest gain difference: {np.abs(rl.gain_db('out') - rc.gain_db('out')).max():.2e} dB")
    hp = series_then_shunt(("R", r), ("L", inductance)).ac(FREQS, source="V1")
    print(f"  RL high-pass (R in series, L to ground): cutoff {hp.cutoff('out'):.1f} Hz, "
          f"gain at fc/10 {hp.gain_db_at(fc / 10, 'out'):.2f} dB, at 10 fc {hp.gain_db_at(10 * fc, 'out'):.2f} dB")

    print("\n=== Step 3: A two-way speaker crossover at 2 kHz with 8 ohm speakers ===")
    speaker, crossover = 8.0, 2000.0
    coil = speaker / (2 * math.pi * crossover)
    cap = 1 / (2 * math.pi * crossover * speaker)
    print(f"  woofer coil L = R / (2 pi f) = {coil * 1e3:.3f} mH, tweeter capacitor C = 1 / (2 pi f R) = {cap * 1e6:.2f} uF")
    woofer = series_then_shunt(("L", coil), ("R", speaker)).ac(FREQS, source="V1")
    tweeter = series_then_shunt(("C", cap), ("R", speaker)).ac(FREQS, source="V1")
    for freq in [200, 1000, 2000, 4000, 20000]:
        w = woofer.gain_db_at(freq, "out")
        t = tweeter.gain_db_at(freq, "out")
        total = 10 ** (w / 10) + 10 ** (t / 10)
        print(f"  {freq:>6} Hz: woofer {w:+7.2f} dB, tweeter {t:+7.2f} dB, total power share {total:.3f}")

    print("\n=== Step 4: Real inductors have wire resistance (DCR) ===")
    for dcr in [0.0, 0.3, 1.0]:
        sweep = series_then_shunt(("L", coil), ("R", speaker), dcr=dcr).ac(FREQS, source="V1")
        print(f"  DCR {dcr:.1f} ohm: woofer gain at 100 Hz {sweep.gain_db_at(100, 'out'):+.2f} dB, "
              f"cutoff {sweep.cutoff('out'):7.1f} Hz")

    print("\n=== Step 5: Cleaning a supply line: no DC drop with an inductor ===")
    load = 5.0
    choke = 100e-6
    ripple = 100e3
    lc = series_then_shunt(("L", choke), ("R", load)).ac([ripple], source="V1")
    print(f"  100 uH in series with a 5 ohm load: fc = {rl_cutoff(load, choke):.0f} Hz")
    print(f"  ripple at 100 kHz: {lc.gain_db('out')[0]:.1f} dB")
    dc = Circuit()
    dc.voltage_source("V1", "in", "0", 5.0)
    dc.inductor("L1", "in", "out", choke)
    dc.resistor("Rload", "out", "0", load)
    op = dc.dc()
    print(f"  DC: load sees {op.v('out'):.3f} V of 5 V, current {op.i('Rload'):.2f} A, nothing lost in the ideal inductor")
    series_r = load / 10
    print(f"  an RC filter would need a series resistor; even {series_r:.1f} ohm drops {5 * series_r / (series_r + load):.2f} V "
          f"and wastes {(5 / (series_r + load)) ** 2 * series_r:.2f} W")


if __name__ == "__main__":
    main()
