import math

import numpy as np

from sim import Circuit, engineering

L = 10e-3
C = 1e-6
R = 10.0


def resonant_frequency(inductance, capacitance):
    return 1 / (2 * math.pi * math.sqrt(inductance * capacitance))


def capacitance_for(freq, inductance):
    return 1 / ((2 * math.pi * freq) ** 2 * inductance)


def series_rlc(resistance=R):
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    c.inductor("L1", "in", "a", L)
    c.capacitor("C1", "a", "b", C)
    c.resistor("R1", "b", "0", resistance)
    return c


def ringing(resistance):
    c = Circuit()
    c.capacitor("C1", "top", "0", C, v0=1.0)
    c.inductor("L1", "top", "m", L)
    c.resistor("R1", "m", "0", resistance)
    return c.transient(t_stop=10e-3, dt=1e-6)


def parallel_tank():
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=1000.0)
    c.resistor("Rfeed", "in", "tank", 10e3)
    c.capacitor("C1", "tank", "0", C)
    c.inductor("L1", "tank", "w", L)
    c.resistor("Rdcr", "w", "0", 1.0)
    return c


def main():
    f0 = resonant_frequency(L, C)
    print("=== Step 1: Two reactances that move in opposite directions ===")
    print(f"  L = {L * 1e3:.0f} mH, C = {C * 1e6:.0f} uF, f0 = 1 / (2 pi sqrt(L C)) = {f0:.1f} Hz")
    for freq in [200, 800, f0, 3000, 10000]:
        x_l = 2 * math.pi * freq * L
        x_c = 1 / (2 * math.pi * freq * C)
        print(f"  f = {freq:7.1f} Hz: X_L = {x_l:7.1f} ohm, X_C = {x_c:7.1f} ohm, X_L - X_C = {x_l - x_c:+8.1f} ohm")

    print("\n=== Step 2: Series RLC: the current peaks at f0 (simulator) ===")
    freqs = np.logspace(2, 5, 3001)
    sweep = series_rlc().ac(freqs, source="V1")
    current = sweep.gain("b") / R
    peak = freqs[np.argmax(current)]
    print(f"  peak current {current.max() * 1e3:.2f} mA at {peak:.1f} Hz (hand: 1 V / {R:.0f} ohm = {1 / R * 1e3:.0f} mA at {f0:.1f} Hz)")
    for freq in [f0 / 2, f0, 2 * f0]:
        z = R + 1j * (2 * math.pi * freq * L - 1 / (2 * math.pi * freq * C))
        print(f"  f = {freq:7.1f} Hz: |Z| = {abs(z):7.1f} ohm, current = {1 / abs(z) * 1e3:6.2f} mA")

    print("\n=== Step 3: At resonance the parts see far more than the source voltage ===")
    at_f0 = series_rlc().ac([f0], source="V1")
    v_l = abs(at_f0.v("in")[0] - at_f0.v("a")[0])
    v_c = abs(at_f0.v("a")[0] - at_f0.v("b")[0])
    v_r = abs(at_f0.v("b")[0])
    q = math.sqrt(L / C) / R
    print(f"  source 1.000 V: V_L = {v_l:.3f} V, V_C = {v_c:.3f} V, V_R = {v_r:.3f} V")
    print(f"  quality factor Q = sqrt(L / C) / R = {q:.1f}; V_L and V_C are Q times the source")
    print(f"  V_L and V_C are opposite: V_L + V_C = {abs(at_f0.v('in')[0] - at_f0.v('b')[0]):.2e} V")

    print("\n=== Step 4: Energy sloshing between L and C: ringing ===")
    for resistance in [1.0, 10.0, 50.0, 400.0]:
        run = ringing(resistance)
        v = np.asarray(run.v("top"))
        crossings = [t for t in run.crossing_times("top", 0.0, "falling") if t < 3e-3]
        if len(crossings) >= 2:
            measured = (len(crossings) - 1) / (crossings[-1] - crossings[0])
            text = f"rings at {measured:7.1f} Hz"
        else:
            text = "does not ring (overdamped)"
        print(f"  R = {resistance:5.1f} ohm (Q = {math.sqrt(L / C) / resistance:5.2f}): {text}; "
              f"largest |v| after 2 ms = {np.abs(v[2000:]).max():.3f} V")
    print(f"  undamped prediction: {f0:.1f} Hz")

    print("\n=== Step 5: A parallel LC 'tank' has its HIGHEST impedance at f0 ===")
    tank = parallel_tank().ac(freqs, source="V1")
    g = tank.gain("tank")
    print(f"  fed through 10 k ohm: output peaks at {freqs[np.argmax(g)]:.1f} Hz with gain {g.max():.3f}")
    print(f"  so the tank looks like {10e3 * g.max() / (1 - g.max()):.0f} ohm at f0 (hand: L / (C R_dcr) = {L / (C * 1.0):.0f} ohm)")
    for freq in [f0 / 2, 2 * f0]:
        print(f"  at {freq:7.1f} Hz the gain is only {tank.gain_db_at(freq, 'tank'):.1f} dB")

    print("\n=== Step 6: Tuning: choose C for a target frequency ===")
    for target, inductance in [(1000.0, 10e-3), (50.0, 1.0), (1e6, 100e-6)]:
        cap = capacitance_for(target, inductance)
        print(f"  f0 = {engineering(target, 'Hz'):>9} with L = {engineering(inductance, 'H'):>7} needs C = {engineering(cap, 'F')}")


if __name__ == "__main__":
    main()
