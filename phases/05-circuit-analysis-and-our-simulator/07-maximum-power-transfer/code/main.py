from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

V_TH = 12.0 * 6000 / (3000 + 6000)
R_TH = 3000 * 6000 / (3000 + 6000)


def source_with_load(load_ohms):
    circuit = Circuit()
    circuit.voltage_source("V1", "a", "0", 12.0)
    circuit.resistor("R1", "a", "p", 3000)
    circuit.resistor("R2", "p", "0", 6000)
    circuit.resistor("RL", "p", "0", load_ohms)
    return circuit


def formula_power(load_ohms):
    return V_TH ** 2 * load_ohms / (R_TH + load_ohms) ** 2


def main():
    print(f"Source: 12 V, 3 kOhm over 6 kOhm.  Vth = {V_TH:.3f} V, Rth = {R_TH / 1000:.3f} kOhm")
    print(f"Predicted maximum: RL = Rth = {R_TH / 1000:.3f} kOhm, P_max = Vth^2 / (4 Rth) = {V_TH ** 2 / (4 * R_TH) * 1000:.3f} mW")

    print(f"\n{'RL':>10s} {'P_load sim':>12s} {'P_load formula':>15s} {'eff. (Thevenin)':>16s} {'eff. (real divider)':>20s}")
    for load in (500, 1000, 2000, 4000, 10000, 100000):
        result = source_with_load(load).dc()
        load_power = result.p("RL")
        battery_power = result.p("V1")
        print(f"{load:9.0f}Ohm {load_power * 1000:10.3f}mW {formula_power(load) * 1000:13.3f}mW"
              f" {load / (load + R_TH) * 100:14.1f} % {load_power / battery_power * 100:18.1f} %")

    loads = np.logspace(2, 6, 401)
    powers = np.array([source_with_load(r).dc().p("RL") for r in loads])
    best = loads[np.argmax(powers)]
    print(f"\nSweep of {len(loads)} loads from 100 Ohm to 1 MOhm:")
    print(f"  largest load power {powers.max() * 1000:.4f} mW at RL = {best:.0f} Ohm (Rth = {R_TH:.0f} Ohm)")
    print(f"  RL = Rth/2 gives {formula_power(R_TH / 2) * 1000:.4f} mW and RL = 2 Rth gives {formula_power(2 * R_TH) * 1000:.4f} mW: the curve is symmetric on a log axis")

    efficiency = loads / (loads + R_TH)
    figure, power_axis = plt.subplots(figsize=(8, 4.5))
    power_axis.semilogx(loads, powers * 1000, color="#8a5a2b", label="load power (sim)")
    power_axis.axvline(R_TH, color="gray", linestyle="--", linewidth=1)
    power_axis.plot([best], [powers.max() * 1000], "o", color="#8a5a2b")
    power_axis.set_xlabel("load resistance RL (Ohm)")
    power_axis.set_ylabel("load power (mW)")
    efficiency_axis = power_axis.twinx()
    efficiency_axis.semilogx(loads, efficiency * 100, color="#4a6b3a", label="efficiency (Thevenin)")
    efficiency_axis.set_ylabel("efficiency (%)")
    figure.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    power_axis.set_title("Maximum power at RL = Rth, where efficiency is 50 %")
    figure.tight_layout()
    output = Path(__file__).parent / "out.png"
    figure.savefig(output, dpi=120)
    print(f"\nPlot saved to {output}")


if __name__ == "__main__":
    main()
