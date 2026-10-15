from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

BETA = 100.0
THERMAL_VOLTAGE = 0.025852
SATURATION_CURRENT = 1e-14


def input_characteristic():
    print("Input side: collector current set by V_BE (collector held at 5 V)")
    print(f"  {'V_BE':>6} {'I_C formula':>13} {'I_C sim':>11} {'I_B sim':>11} {'I_E sim':>11} {'alpha':>7}")
    for vbe in [0.55, 0.60, 0.65, 0.70]:
        circuit = Circuit()
        circuit.voltage_source("VC", "c", "0", 5.0)
        circuit.voltage_source("VB", "b", "0", vbe)
        circuit.npn("Q1", c="c", b="b", e="0", beta=BETA)
        result = circuit.dc()
        formula = SATURATION_CURRENT * np.exp(vbe / THERMAL_VOLTAGE)
        collector, base, emitter = result.i("Q1"), result.i("Q1.b"), result.i("Q1.e")
        print(f"  {vbe:>5.2f}V {formula * 1000:>11.4f}mA {collector * 1000:>9.4f}mA {base * 1e6:>9.3f}uA {emitter * 1000:>9.4f}mA {collector / emitter:>7.4f}")
    print(f"  alpha = I_C / I_E = beta / (beta + 1) = {BETA / (BETA + 1):.4f}")
    print()


def output_curves(base_currents, collector_volts):
    curves = {}
    for base_current in base_currents:
        circuit = Circuit()
        circuit.current_source("IB", "0", "b", base_current)
        circuit.voltage_source("VC", "c", "0", 0.0)
        circuit.npn("Q1", c="c", b="b", e="0", beta=BETA)
        sweep = circuit.sweep("VC", collector_volts)
        curves[base_current] = np.array([float(sweep.i("Q1")[k]) for k in range(len(collector_volts))])
    return curves


def show_output_curves():
    collector_volts = np.array([0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0])
    base_currents = [10e-6, 20e-6, 50e-6]
    curves = output_curves(base_currents, collector_volts)
    print("Output side: collector current versus V_CE for fixed base currents")
    header = "".join(f"{v:>8.2f}" for v in collector_volts)
    print(f"  {'I_B':>7} | V_CE = {header}")
    for base_current, values in curves.items():
        row = "".join(f"{value * 1000:>8.3f}" for value in values)
        print(f"  {base_current * 1e6:>5.0f}uA | I_C mA {row}")
    print("  Above about 0.2-0.3 V the curves go flat at beta x I_B: the active region.")
    print("  Below that the transistor is saturated: it cannot reach beta x I_B.")
    print()
    return collector_volts, curves


def regions():
    print("The four regions, by which junctions are forward biased")
    cases = [("cutoff", 0.0, 5.0), ("active", 0.65, 5.0), ("saturation", 0.75, 0.1), ("reverse active", 0.0, -0.65)]
    for label, vb, vc in cases:
        circuit = Circuit()
        circuit.voltage_source("VB", "b", "0", vb)
        circuit.voltage_source("VC", "c", "0", vc)
        circuit.npn("Q1", c="c", b="b", e="0", beta=BETA)
        result = circuit.dc()
        print(f"  {label:<15} V_BE = {vb:5.2f} V, V_BC = {vb - vc:5.2f} V   I_C = {result.i('Q1') * 1000:9.4f} mA   I_B = {result.i('Q1.b') * 1000:9.4f} mA")
    print()


def biased_with_resistors():
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", 9.0)
    circuit.resistor("RB", "vcc", "b", 180e3)
    circuit.resistor("RC", "vcc", "c", 1000.0)
    circuit.npn("Q1", c="c", b="b", e="0", beta=BETA)
    result = circuit.dc()
    estimate_ib = (9.0 - 0.65) / 180e3
    print("Setting the current with a base resistor: 9 V, R_B = 180 kohm, R_C = 1 kohm")
    print(f"  estimate: I_B = (9 - 0.65) / 180k = {estimate_ib * 1e6:.1f} uA, I_C = beta x I_B = {BETA * estimate_ib * 1000:.2f} mA")
    print(f"  simulator: V_BE = {result.v('b'):.4f} V, I_B = {result.i('Q1.b') * 1e6:.2f} uA, I_C = {result.i('Q1') * 1000:.3f} mA, V_CE = {result.v('c'):.3f} V")
    print(f"  transistor power = V_CE x I_C = {result.p('Q1') * 1000:.1f} mW")
    print()


def plot(collector_volts, curves):
    figure, axis = plt.subplots(figsize=(6, 4))
    fine = np.linspace(0, 10, 201)
    for base_current, _ in curves.items():
        values = output_curves([base_current], fine)[base_current]
        axis.plot(fine, values * 1000, label=f"I_B = {base_current * 1e6:.0f} uA")
    axis.set_xlabel("V_CE (V)")
    axis.set_ylabel("I_C (mA)")
    axis.set_title("NPN output characteristics (beta = 100)")
    axis.legend()
    figure.tight_layout()
    path = Path(__file__).parent / "out.png"
    figure.savefig(path, dpi=120)
    print(f"Saved the output curves to {path.name}")


def main():
    input_characteristic()
    collector_volts, curves = show_output_curves()
    regions()
    biased_with_resistors()
    plot(collector_volts, curves)


if __name__ == "__main__":
    main()
