from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sim import Circuit

LOADS = [10000.0, 1000.0, 100.0, 10.0, 2.0, 1.0]


def ideal_voltage_source(volts, load_ohms):
    c = Circuit()
    c.voltage_source("V1", "out", "0", volts)
    c.resistor("RL", "out", "0", load_ohms)
    r = c.dc()
    return r.v("out"), r.i("RL")


def real_voltage_source(volts, internal_ohms, load_ohms):
    c = Circuit()
    c.voltage_source("V1", "emf", "0", volts)
    c.resistor("Rint", "emf", "out", internal_ohms)
    c.resistor("RL", "out", "0", load_ohms)
    r = c.dc()
    return r.v("out"), r.i("RL")


def ideal_current_source(amps, load_ohms):
    c = Circuit()
    c.current_source("I1", "0", "out", amps)
    c.resistor("RL", "out", "0", load_ohms)
    r = c.dc()
    return r.v("out"), r.i("RL")


def real_current_source(amps, shunt_ohms, load_ohms):
    c = Circuit()
    c.current_source("I1", "0", "out", amps)
    c.resistor("Rsh", "out", "0", shunt_ohms)
    c.resistor("RL", "out", "0", load_ohms)
    r = c.dc()
    return r.v("out"), r.i("RL")


print("Step 1: an ideal 9 V voltage source keeps 9 V no matter what you connect")
print(f"  {'load (ohm)':>12} {'V out (V)':>10} {'I (A)':>10}")
for load in LOADS:
    v, i = ideal_voltage_source(9.0, load)
    print(f"  {load:>12.0f} {v:>10.3f} {i:>10.4f}")
print("  the current grows without limit as the load shrinks: 9 V / 1 ohm = 9 A")

print()
print("Step 2: a real 9 V source = ideal 9 V in series with 2 ohm inside")
print(f"  {'load (ohm)':>12} {'V out (V)':>10} {'I (A)':>10} {'lost inside (V)':>16}")
for load in LOADS:
    v, i = real_voltage_source(9.0, 2.0, load)
    print(f"  {load:>12.0f} {v:>10.3f} {i:>10.4f} {9.0 - v:>16.3f}")
print("  check by hand for 10 ohm: I = 9 / (2 + 10) = 0.75 A, V = 0.75 * 10 = 7.5 V")

print()
print("Step 3: an ideal 10 mA current source pushes 10 mA no matter what")
print(f"  {'load (ohm)':>12} {'I (mA)':>10} {'V across (V)':>13}")
for load in [1.0, 10.0, 100.0, 1000.0, 10000.0]:
    v, i = ideal_current_source(0.010, load)
    print(f"  {load:>12.0f} {i * 1000:>10.3f} {v:>13.3f}")
print("  the voltage grows without limit as the load grows: 10 mA * 10 kohm = 100 V")

print()
print("Step 4: a real 10 mA current source = ideal 10 mA with 1 kohm in parallel")
print(f"  {'load (ohm)':>12} {'I load (mA)':>12} {'leaks inside (mA)':>18}")
for load in [1.0, 10.0, 100.0, 1000.0, 10000.0]:
    v, i = real_current_source(0.010, 1000.0, load)
    print(f"  {load:>12.0f} {i * 1000:>12.3f} {10.0 - i * 1000:>18.3f}")
print("  check by hand for 1 kohm: the 10 mA splits evenly, 5 mA in the load")

print()
print("Step 5: 9 V with 2 ohm in series looks exactly like 4.5 A with 2 ohm in parallel")
print(f"  {'load (ohm)':>12} {'V (series model)':>17} {'V (parallel model)':>19}")
for load in [1.0, 2.0, 10.0, 100.0]:
    v_series, _ = real_voltage_source(9.0, 2.0, load)
    v_parallel, _ = real_current_source(9.0 / 2.0, 2.0, load)
    print(f"  {load:>12.0f} {v_series:>17.4f} {v_parallel:>19.4f}")
print("  from the outside you cannot tell the two models apart")

print()
print("Step 6: the output line of each source (saved to out.png)")
load_sweep = np.logspace(-1, 4, 200)
curves = {
    "ideal 9 V": [ideal_voltage_source(9.0, rl) for rl in load_sweep],
    "real 9 V, 2 ohm inside": [real_voltage_source(9.0, 2.0, rl) for rl in load_sweep],
    "real 10 mA, 1 kohm inside": [real_current_source(0.010, 1000.0, rl) for rl in load_sweep],
}
figure, axes = plt.subplots(1, 2, figsize=(10, 4))
for name, points in list(curves.items())[:2]:
    volts, amps = zip(*points)
    axes[0].plot(amps, volts, label=name)
axes[0].set_xlim(0, 5)
axes[0].set_xlabel("current drawn (A)")
axes[0].set_ylabel("voltage at the terminals (V)")
axes[0].legend()
volts, amps = zip(*curves["real 10 mA, 1 kohm inside"])
axes[1].plot(np.array(volts), np.array(amps) * 1000, label="real 10 mA, 1 kohm inside")
axes[1].axhline(10, linestyle="--", color="gray", label="ideal 10 mA")
axes[1].set_xlabel("voltage at the terminals (V)")
axes[1].set_ylabel("current delivered (mA)")
axes[1].legend()
figure.tight_layout()
figure.savefig(Path(__file__).parent / "out.png", dpi=100)
print("  saved", Path(__file__).parent / "out.png")
