import numpy as np

from sim import Circuit


def esr_step(esr_ohms, farads=1000e-6, start_volts=5.0, load_amps=1.0):
    circuit = Circuit()
    circuit.capacitor("C1", "inner", "0", farads, v0=start_volts)
    circuit.resistor("ESR", "inner", "out", esr_ohms)
    circuit.current_source("Iload", "out", "0", load_amps)
    result = circuit.transient(t_stop=0.5e-3, dt=1e-6)
    time = np.asarray(result.time)
    volts = np.asarray(result.v("out"))
    return float(np.interp(2e-6, time, volts)), float(volts[-1])


def show_esr():
    print("ESR: a 1000 uF capacitor at 5 V suddenly asked for 1 A")
    print(f"{'ESR (ohm)':>10} {'output right away (V)':>22} {'after 0.5 ms (V)':>17}")
    for esr in (0.01, 0.1, 1.0):
        right_away, later = esr_step(esr)
        print(f"{esr:>10.2f} {right_away:>22.3f} {later:>17.3f}")
    print("  The instant drop is I * ESR; the slow slide is I * t / C = 0.5 V in 0.5 ms")
    print()


def leakage_after(leak_ohms, farads=100e-6, start_volts=10.0, seconds=60.0):
    circuit = Circuit()
    circuit.capacitor("C1", "top", "0", farads, v0=start_volts)
    circuit.resistor("Rleak", "top", "0", leak_ohms)
    result = circuit.transient(t_stop=seconds, dt=seconds / 2000)
    return float(np.asarray(result.v("top"))[-1])


def show_leakage():
    print("Leakage: a 100 uF capacitor charged to 10 V and left alone for 60 s")
    electrolytic_amps = max(0.01 * 100 * 10, 3.0) * 1e-6
    models = [
        ("aluminium electrolytic (0.01*C*V rule)", 10.0 / electrolytic_amps),
        ("good electrolytic (0.5 uA)", 10.0 / 0.5e-6),
        ("film capacitor (about 10 GOhm)", 10e9),
    ]
    for label, leak_ohms in models:
        print(f"  {label:<40} R_leak = {leak_ohms:>9.2e} ohm -> {leakage_after(leak_ohms):.3f} V")
    print()


def ceramic_dc_bias(nominal_farads, applied_volts, rated_volts):
    fraction_of_rating = applied_volts / rated_volts
    return nominal_farads * max(0.2, 1 - 0.75 * fraction_of_rating ** 1.5)


def show_dc_bias():
    print("Class II ceramic (X5R/X7R) loses capacitance under DC voltage (illustrative curve)")
    nominal, rated = 10e-6, 6.3
    for volts in (0.0, 1.8, 3.3, 5.0):
        effective = ceramic_dc_bias(nominal, volts, rated)
        print(f"  10 uF / 6.3 V part at {volts:>3.1f} V behaves like {effective * 1e6:>5.2f} uF")
    print()


def show_tolerance():
    print("Tolerance: tau = 10 kOhm (1%) * 10 uF (+/-20%)")
    for c_factor, r_factor, label in ((0.8, 0.99, "smallest"), (1.0, 1.0, "nominal"), (1.2, 1.01, "largest")):
        tau = 10e3 * r_factor * 10e-6 * c_factor
        print(f"  {label:<9} tau = {tau * 1e3:6.1f} ms")


if __name__ == "__main__":
    show_esr()
    show_leakage()
    show_dc_bias()
    show_tolerance()
