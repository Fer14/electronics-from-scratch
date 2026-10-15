from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

THRESHOLD = 1.0
TRANSCONDUCTANCE_PARAMETER = 2e-3
OXIDE_PERMITTIVITY = 3.9 * 8.854e-12


def gate_capacitance():
    thickness = 10e-9
    width, length = 10e-6, 1e-6
    per_area = OXIDE_PERMITTIVITY / thickness
    total = per_area * width * length
    print("The gate is a capacitor: metal (or polysilicon) / 10 nm of SiO2 / silicon")
    print(f"  C per area = eps_ox / t_ox = {OXIDE_PERMITTIVITY:.3e} / {thickness:.0e} = {per_area * 1e3:.2f} fF per square micrometre")
    print(f"  a 10 um x 1 um gate: C = {total * 1e15:.1f} fF")
    charge_per_volt = total
    electrons = charge_per_volt * 1.0 / 1.602e-19
    print(f"  1 V above threshold pulls about {electrons:.0f} electrons into the channel")
    print()


def square_law(vgs, vds):
    overdrive = vgs - THRESHOLD
    if overdrive <= 0:
        return 0.0
    if vds < overdrive:
        return TRANSCONDUCTANCE_PARAMETER * (overdrive * vds - 0.5 * vds * vds)
    return 0.5 * TRANSCONDUCTANCE_PARAMETER * overdrive**2


def nmos_current(vgs, vds):
    circuit = Circuit()
    circuit.voltage_source("VG", "g", "0", vgs)
    circuit.voltage_source("VD", "d", "0", vds)
    circuit.nmos("M1", d="d", g="g", s="0", vth=THRESHOLD, k=TRANSCONDUCTANCE_PARAMETER)
    return circuit.dc().i("M1")


def show_transfer():
    print(f"Transfer curve: drain current versus V_GS (V_DS = 5 V, V_th = {THRESHOLD} V, k = {TRANSCONDUCTANCE_PARAMETER * 1e3:.0f} mA/V^2)")
    print(f"  {'V_GS':>5} {'formula':>10} {'simulator':>10}")
    for vgs in [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]:
        print(f"  {vgs:>4.1f}V {square_law(vgs, 5.0) * 1000:>8.3f}mA {nmos_current(vgs, 5.0) * 1000:>8.3f}mA")
    print("  Doubling the overdrive (V_GS - V_th) from 1 V to 2 V multiplies the current by 4: a square law, not an exponential.")
    print()


def show_output():
    drain_volts = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
    print("Output curves: drain current versus V_DS for fixed V_GS")
    print("  V_GS | " + "".join(f"{v:>8.2f}" for v in drain_volts))
    for vgs in [2.0, 3.0, 4.0]:
        row = "".join(f"{nmos_current(vgs, vds) * 1000:>8.3f}" for vds in drain_volts)
        print(f"  {vgs:>3.0f} V | {row}  mA")
    print("  Each curve rises (triode: the channel acts like a resistor) then flattens once V_DS > V_GS - V_th (saturation).")
    print()


def show_resistor_mode():
    print("Small V_DS: the channel is a resistor whose value the gate sets, R = 1 / (k (V_GS - V_th))")
    for vgs in [1.5, 2.0, 3.0, 5.0]:
        vds = 0.01
        simulated = vds / nmos_current(vgs, vds)
        print(f"  V_GS = {vgs:.1f} V: formula {1 / (TRANSCONDUCTANCE_PARAMETER * (vgs - THRESHOLD)):7.1f} ohm   simulator {simulated:7.1f} ohm")
    print()


def show_no_gate_current():
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", 10.0)
    circuit.voltage_source("VG", "g", "0", 3.0)
    circuit.resistor("RD", "vdd", "d", 1000.0)
    circuit.nmos("M1", d="d", g="g", s="0", vth=THRESHOLD, k=TRANSCONDUCTANCE_PARAMETER)
    result = circuit.dc()
    print("Steady gate current is zero: 3 V on the gate, 10 V supply, 1 kohm drain resistor")
    print(f"  gate current {result.i('VG') * 1e9:.3f} nA, drain current {result.i('M1') * 1000:.3f} mA, V_DS = {result.v('d'):.3f} V")
    print()


def show_pmos():
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", 5.0)
    circuit.voltage_source("VG", "g", "0", 2.0)
    circuit.pmos("M2", d="d", g="g", s="vdd", vth=THRESHOLD, k=TRANSCONDUCTANCE_PARAMETER)
    circuit.resistor("RD", "d", "0", 1000.0)
    result = circuit.dc()
    print("PMOS: source at +5 V, gate at 2 V (V_SG = 3 V), 1 kohm from drain to ground")
    print(f"  current through the load {result.i('RD') * 1000:.3f} mA, drain at {result.v('d'):.3f} V")
    print()


def plot():
    vds = np.linspace(0, 5, 101)
    figure, axis = plt.subplots(figsize=(6, 4))
    for vgs in [2.0, 3.0, 4.0]:
        axis.plot(vds, [square_law(vgs, v) * 1000 for v in vds], label=f"V_GS = {vgs:.0f} V")
    axis.plot(vds, [0.5 * TRANSCONDUCTANCE_PARAMETER * v * v * 1000 for v in vds], "k--", label="edge of saturation")
    axis.set_ylim(0, 10)
    axis.set_xlabel("V_DS (V)")
    axis.set_ylabel("I_D (mA)")
    axis.set_title("NMOS output characteristics")
    axis.legend()
    figure.tight_layout()
    path = Path(__file__).parent / "out.png"
    figure.savefig(path, dpi=120)
    print(f"Saved the output curves to {path.name}")


def main():
    gate_capacitance()
    show_transfer()
    show_output()
    show_resistor_mode()
    show_no_gate_current()
    show_pmos()
    plot()


if __name__ == "__main__":
    main()
