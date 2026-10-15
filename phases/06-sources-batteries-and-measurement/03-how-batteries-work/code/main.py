from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sim import Circuit

FARADAY = 96485.0

REDUCTION_POTENTIALS = {
    "Li+ / Li": -3.04,
    "Zn2+ / Zn": -0.76,
    "Fe2+ / Fe": -0.44,
    "2H+ / H2": 0.00,
    "Cu2+ / Cu": 0.34,
    "Ag+ / Ag": 0.80,
}


def cell_voltage(cathode, anode):
    return REDUCTION_POTENTIALS[cathode] - REDUCTION_POTENTIALS[anode]


def amp_hours_per_gram(molar_mass_grams, electrons_per_atom):
    coulombs_per_gram = electrons_per_atom * FARADAY / molar_mass_grams
    return coulombs_per_gram / 3600.0


def terminal_voltage(emf, internal_ohms, load_ohms):
    c = Circuit()
    c.voltage_source("E", "emf", "0", emf)
    c.resistor("Rint", "emf", "plus", internal_ohms)
    c.resistor("RL", "plus", "0", load_ohms)
    r = c.dc()
    return r.v("plus"), r.i("RL")


def discharge(chemistry, load_ohms, step_seconds=60.0):
    used_fraction = 0.0
    seconds = 0.0
    times, volts = [], []
    while used_fraction < 1.0:
        emf = np.interp(used_fraction, chemistry["used"], chemistry["emf"])
        internal = np.interp(used_fraction, chemistry["used"], chemistry["r"])
        v, i = terminal_voltage(float(emf), float(internal), load_ohms)
        if v < chemistry["cutoff"]:
            break
        times.append(seconds / 3600.0)
        volts.append(v)
        used_fraction += i * step_seconds / (chemistry["capacity_ah"] * 3600.0)
        seconds += step_seconds
    return np.array(times), np.array(volts)


ALKALINE_AA = {
    "name": "alkaline AA",
    "capacity_ah": 2.4,
    "cutoff": 1.0,
    "used": [0.0, 0.1, 0.5, 0.8, 0.95, 1.0],
    "emf": [1.58, 1.45, 1.28, 1.15, 1.02, 0.80],
    "r": [0.15, 0.17, 0.25, 0.40, 0.60, 1.00],
}
LITHIUM_ION_18650 = {
    "name": "Li-ion 18650",
    "capacity_ah": 3.0,
    "cutoff": 3.0,
    "used": [0.0, 0.05, 0.2, 0.8, 0.95, 1.0],
    "emf": [4.20, 4.05, 3.85, 3.60, 3.35, 2.80],
    "r": [0.04, 0.04, 0.04, 0.05, 0.07, 0.12],
}

print("Step 1: cell voltage from two half-reactions (standard potentials, 25 C)")
for cathode, anode in [("Cu2+ / Cu", "Zn2+ / Zn"), ("Ag+ / Ag", "Zn2+ / Zn"), ("Cu2+ / Cu", "Fe2+ / Fe"),
                       ("Cu2+ / Cu", "Li+ / Li")]:
    print(f"  {cathode:>10} (+)  against  {anode:<10} (-): "
          f"{REDUCTION_POTENTIALS[cathode]:+.2f} - ({REDUCTION_POTENTIALS[anode]:+.2f}) = {cell_voltage(cathode, anode):.2f} V")
print("  the copper-zinc pair is the classic Daniell cell, about 1.10 V")

print()
print("Step 2: how much charge a gram of metal can give")
for metal, molar_mass, electrons in [("zinc", 65.38, 2), ("lithium", 6.94, 1), ("lead", 207.2, 2)]:
    capacity = amp_hours_per_gram(molar_mass, electrons)
    print(f"  {metal:>8}: {electrons} e- per atom, {molar_mass} g/mol -> {capacity:.3f} Ah per gram")
print(f"  3 g of zinc could in theory give {3 * amp_hours_per_gram(65.38, 2):.2f} Ah")

print()
print("Step 3: capacity, current and runtime")
for label, capacity_mah, current_ma in [("AA in a clock", 2400, 0.1), ("AA in a remote", 2400, 20),
                                         ("AA in a toy car", 2400, 500), ("phone, 4000 mAh", 4000, 400)]:
    hours = capacity_mah / current_ma
    print(f"  {label:<18}: {capacity_mah} mAh / {current_ma} mA = {hours:,.1f} h")
print("  energy in Wh = capacity in Ah * average voltage: "
      f"AA {2.4 * 1.25:.1f} Wh, 18650 {3.0 * 3.6:.1f} Wh")

print()
print("Step 4: discharge curves into a 10 ohm load (simulated minute by minute)")
figure, axis = plt.subplots(figsize=(7, 4))
for cell in [ALKALINE_AA, LITHIUM_ION_18650]:
    hours, volts = discharge(cell, 10.0)
    energy_wh = np.sum(volts**2 / 10.0) * 60.0 / 3600.0
    print(f"  {cell['name']:<13}: starts at {volts[0]:.3f} V, reaches the {cell['cutoff']} V cutoff after "
          f"{hours[-1]:.1f} h, delivered {energy_wh:.2f} Wh")
    axis.plot(hours, volts, label=cell["name"])
axis.set_xlabel("time (h)")
axis.set_ylabel("terminal voltage (V)")
axis.legend()
figure.tight_layout()
figure.savefig(Path(__file__).parent / "out.png", dpi=100)
print("  saved", Path(__file__).parent / "out.png")

print()
print("Step 5: the same alkaline cell, light load versus heavy load")
for load in [10.0, 2.0, 1.0]:
    hours, volts = discharge(ALKALINE_AA, load, step_seconds=30.0)
    charge_ah = np.sum(volts / load) * 30.0 / 3600.0
    print(f"  {load:>4.0f} ohm load: runs {hours[-1]:5.2f} h and delivers {charge_ah:.2f} Ah before 1.0 V")
print("  the heavier the load, the earlier the internal drop pushes the terminals below the cutoff")
