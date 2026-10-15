from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sim import Circuit

OUTPUT_OHMS = 0.005


def bench_supply(volts_set, amps_limit, attach_load):
    constant_voltage = Circuit()
    constant_voltage.voltage_source("Vset", "inner", "0", volts_set)
    constant_voltage.resistor("Rout", "inner", "out", OUTPUT_OHMS)
    attach_load(constant_voltage)
    result = constant_voltage.dc()
    amps = result.i("Rout")
    if amps <= amps_limit:
        return "CV", result.v("out"), amps
    constant_current = Circuit()
    constant_current.current_source("Iset", "0", "out", amps_limit)
    attach_load(constant_current)
    result = constant_current.dc()
    return "CC", result.v("out"), amps_limit


def resistor_load(ohms):
    return lambda c: c.resistor("Rload", "out", "0", ohms)


print("Step 1: a bench supply set to 12 V with a 0.5 A current limit")
print(f"  {'load (ohm)':>10} {'mode':>5} {'V out (V)':>10} {'I (A)':>8}")
for ohms in [1000.0, 100.0, 48.0, 24.0, 20.0, 10.0, 1.0, 0.001]:
    mode, volts, amps = bench_supply(12.0, 0.5, resistor_load(ohms))
    print(f"  {ohms:>10.3f} {mode:>5} {volts:>10.3f} {amps:>8.3f}")
print(f"  crossover load = 12 V / 0.5 A = {12.0 / 0.5:.0f} ohm: above it CV, below it CC")
print("  even a dead short only gets 0.5 A")

print()
print("Step 2: the output rectangle (saved to out.png)")
sweep = np.logspace(-2, 3, 300)
points = [bench_supply(12.0, 0.5, resistor_load(ohms)) for ohms in sweep]
volts = np.array([p[1] for p in points])
amps = np.array([p[2] for p in points])
modes = np.array([p[0] for p in points])
figure, axis = plt.subplots(figsize=(6, 4))
for mode, color in [("CV", "tab:blue"), ("CC", "tab:orange")]:
    chosen = modes == mode
    axis.plot(amps[chosen], volts[chosen], "o", markersize=3, color=color, label=f"{mode} mode")
axis.set_xlabel("output current (A)")
axis.set_ylabel("output voltage (V)")
axis.set_xlim(0, 0.6)
axis.set_ylim(0, 13)
axis.legend()
figure.tight_layout()
figure.savefig(Path(__file__).parent / "out.png", dpi=100)
print(f"  {np.sum(modes == 'CV')} points on the flat CV edge, {np.sum(modes == 'CC')} on the vertical CC edge")
print("  saved", Path(__file__).parent / "out.png")

print()
print("Step 3: a red LED wired straight to the supply set to 5 V")
for limit in [3.0, 0.02]:
    mode, volts, amps = bench_supply(5.0, limit, lambda c: c.led("D1", "out", "0", color="red"))
    print(f"  current limit {limit:>5.2f} A: mode {mode}, LED voltage {volts:.3f} V, LED current {amps * 1000:,.1f} mA")
print("  5 V is far above the LED's ~2 V, so it wants more current than either limit: the supply goes to CC")
print("  a 3 A limit hands the LED 150 times its 20 mA rating (it dies); a 20 mA limit keeps it safe")

print()
print("Step 4: thin leads to a 2 ohm board (5 V set, 0.1 ohm per lead)")


def board_with_leads(volts_set, lead_ohms, board_ohms):
    c = Circuit()
    c.voltage_source("Vset", "plus", "0", volts_set)
    c.resistor("Rlead_plus", "plus", "board_plus", lead_ohms)
    c.resistor("Rboard", "board_plus", "board_minus", board_ohms)
    c.resistor("Rlead_minus", "board_minus", "0", lead_ohms)
    r = c.dc()
    return r.v("board_plus", "board_minus"), r.i("Rboard")


board_volts, board_amps = board_with_leads(5.0, 0.1, 2.0)
print(f"  front panel says 5.000 V, board gets {board_volts:.3f} V at {board_amps:.3f} A")
print(f"  each lead drops {board_amps * 0.1:.3f} V and burns {board_amps**2 * 0.1:.3f} W")
sensed = 5.0 * (2.0 + 2 * 0.1) / 2.0
board_volts, board_amps = board_with_leads(sensed, 0.1, 2.0)
print(f"  remote sensing raises the output to {sensed:.3f} V so the board gets {board_volts:.3f} V")

print()
print("Step 5: load regulation (0.005 ohm output resistance)")
_, no_load, _ = bench_supply(12.0, 3.0, resistor_load(1e9))
_, full_load, full_amps = bench_supply(12.0, 3.0, resistor_load(4.0))
print(f"  no load {no_load:.4f} V, 3 A load {full_load:.4f} V: change {1000 * (no_load - full_load):.1f} mV "
      f"= {100 * (no_load - full_load) / no_load:.3f} %")

print()
print("Step 6: two 12 V outputs in series make a split +12 V / -12 V supply")
c = Circuit()
c.voltage_source("Vtop", "pos", "0", 12.0)
c.voltage_source("Vbottom", "0", "neg", 12.0)
c.resistor("Rpos", "pos", "0", 120.0)
c.resistor("Rneg", "0", "neg", 240.0)
r = c.dc()
print(f"  +rail {r.v('pos'):+.2f} V, -rail {r.v('neg'):+.2f} V, rail to rail {r.v('pos', 'neg'):.2f} V")
print(f"  +rail load {r.i('Rpos') * 1000:.0f} mA, -rail load {r.i('Rneg') * 1000:.0f} mA")
