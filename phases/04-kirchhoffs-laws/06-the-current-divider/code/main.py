import numpy as np


def two_branch_split(total_current, r_one, r_two):
    i_one = total_current * r_two / (r_one + r_two)
    i_two = total_current * r_one / (r_one + r_two)
    return i_one, i_two


def split_by_voltage(total_current, r_one, r_two):
    r_parallel = r_one * r_two / (r_one + r_two)
    voltage = total_current * r_parallel
    return voltage, voltage / r_one, voltage / r_two


def split_by_conductance(total_current, resistances):
    conductances = 1.0 / np.asarray(resistances, dtype=float)
    shares = conductances / conductances.sum()
    return conductances, shares, total_current * shares


def shunt_for_meter(meter_resistance, meter_full_scale, wanted_full_scale):
    return meter_resistance * meter_full_scale / (wanted_full_scale - meter_full_scale)


def ma(value):
    return f"{value * 1000:.3f} mA"


print("Step 1: two branches, the long way (common voltage, then Ohm's law)")
total, r_one, r_two = 0.030, 100.0, 200.0
voltage, i_one, i_two = split_by_voltage(total, r_one, r_two)
print(f"  I = {ma(total)} into R1 = {r_one:g} Ohm parallel R2 = {r_two:g} Ohm")
print(f"  R1 || R2 = {r_one * r_two / (r_one + r_two):.3f} Ohm, common voltage V = I x (R1 || R2) = {voltage:.3f} V")
print(f"  I1 = V / R1 = {ma(i_one)},  I2 = V / R2 = {ma(i_two)}")
print(f"  KCL check: {ma(i_one)} + {ma(i_two)} = {ma(i_one + i_two)}")

print()
print("Step 2: the current divider formula")
f_one, f_two = two_branch_split(total, r_one, r_two)
print(f"  I1 = I x R2 / (R1 + R2) = {total * 1000:g} mA x {r_two:g} / {r_one + r_two:g} = {ma(f_one)}")
print(f"  I2 = I x R1 / (R1 + R2) = {total * 1000:g} mA x {r_one:g} / {r_one + r_two:g} = {ma(f_two)}")
print("  the SMALLER resistor carries the LARGER current")

print()
print("Step 3: the conductance view, any number of branches")
resistances = [100.0, 220.0, 470.0, 1000.0]
conductances, shares, currents = split_by_conductance(0.050, resistances)
print(f"  I = 50 mA into {len(resistances)} parallel branches")
for r, g, share, i in zip(resistances, conductances, shares, currents):
    print(f"  R = {r:7.1f} Ohm  G = 1/R = {g * 1000:7.3f} mS  share = {share * 100:5.1f} %  I = {ma(i)}")
print(f"  shares add to {shares.sum() * 100:.1f} %, currents add to {ma(currents.sum())}")
print(f"  every branch has the same voltage: " + ", ".join(f"{i * r:.3f} V" for i, r in zip(currents, resistances)))

print()
print("Step 4: a battery with a series resistor feeding two branches")
v_battery, r_series, r_a, r_b = 9.0, 220.0, 330.0, 680.0
r_ab = r_a * r_b / (r_a + r_b)
i_total = v_battery / (r_series + r_ab)
i_a, i_b = two_branch_split(i_total, r_a, r_b)
print(f"  9 V -> {r_series:g} Ohm -> ({r_a:g} Ohm || {r_b:g} Ohm)")
print(f"  parallel part = {r_ab:.2f} Ohm, total = {r_series + r_ab:.2f} Ohm, I_total = {ma(i_total)}")
print(f"  I through {r_a:g} Ohm = {ma(i_a)}, through {r_b:g} Ohm = {ma(i_b)}")
print(f"  KVL check: {i_total * r_series:.3f} V + {i_a * r_a:.3f} V = {i_total * r_series + i_a * r_a:.3f} V")

print()
print("Step 5: extreme branches")
for r_other in [1e6, 1000.0, 100.0, 1.0, 0.01]:
    i_fixed, i_other = two_branch_split(0.010, 100.0, r_other)
    print(f"  10 mA into 100 Ohm || {r_other:>9g} Ohm: 100 Ohm gets {ma(i_fixed)}, the other gets {ma(i_other)}")

print()
print("Step 6: shunts that let a 1 mA meter measure bigger currents")
meter_r, meter_fs = 50.0, 0.001
for wanted in [0.010, 0.100, 1.0]:
    shunt = shunt_for_meter(meter_r, meter_fs, wanted)
    i_meter, i_shunt = two_branch_split(wanted, meter_r, shunt)
    print(f"  full scale {wanted * 1000:6.0f} mA: shunt = {shunt:.4f} Ohm, meter gets {ma(i_meter)}, shunt gets {ma(i_shunt)}")
