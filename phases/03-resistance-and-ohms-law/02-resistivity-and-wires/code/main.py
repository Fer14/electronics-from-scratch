import math

import numpy as np

RESISTIVITY_OHM_METER = {
    "silver": 1.59e-8,
    "copper": 1.68e-8,
    "gold": 2.44e-8,
    "aluminium": 2.65e-8,
    "tungsten": 5.60e-8,
    "iron": 9.70e-8,
    "nichrome": 1.10e-6,
    "graphite": 3.5e-5,
    "pure silicon": 2.3e3,
    "glass": 1e12,
    "PTFE (Teflon)": 1e23,
}

COPPER_TEMPERATURE_COEFFICIENT = 0.00393


def wire_resistance(resistivity, length_m, area_m2):
    return resistivity * length_m / area_m2


def circle_area(diameter_m):
    return math.pi * (diameter_m / 2) ** 2


def awg_diameter_mm(gauge):
    return 0.127 * 92 ** ((36 - gauge) / 39)


def resistance_at_temperature(resistance_at_20c, temperature_c, alpha=COPPER_TEMPERATURE_COEFFICIENT):
    return resistance_at_20c * (1 + alpha * (temperature_c - 20.0))


def length_for_resistance(target_ohms, resistivity, area_m2):
    return target_ohms * area_m2 / resistivity


print("Step 1: resistivity of common materials at 20 C")
for material, rho in RESISTIVITY_OHM_METER.items():
    one_meter_one_mm2 = wire_resistance(rho, 1.0, 1e-6)
    print(f"  {material:15s} rho = {rho:9.2e} ohm m   1 m x 1 mm^2 piece = {one_meter_one_mm2:9.3g} ohm")
ratio = RESISTIVITY_OHM_METER["PTFE (Teflon)"] / RESISTIVITY_OHM_METER["silver"]
print(f"  best insulator / best conductor = {ratio:.1e}  (about {math.log10(ratio):.0f} orders of magnitude)")

print()
print("Step 2: same material, different shapes (copper)")
rho_cu = RESISTIVITY_OHM_METER["copper"]
for length, area_mm2 in [(1.0, 1.0), (2.0, 1.0), (1.0, 2.0), (10.0, 0.5)]:
    ohms = wire_resistance(rho_cu, length, area_mm2 * 1e-6)
    print(f"  L = {length:5.1f} m  A = {area_mm2:4.1f} mm^2  ->  R = {ohms * 1000:7.2f} milliohm")

print()
print("Step 3: the AWG wire gauge table (solid copper)")
print("  AWG  diameter   area      ohm per meter   ohm per 100 m")
for gauge in [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]:
    diameter_mm = awg_diameter_mm(gauge)
    area_m2 = circle_area(diameter_mm / 1000)
    per_meter = wire_resistance(rho_cu, 1.0, area_m2)
    print(f"  {gauge:3d}  {diameter_mm:6.3f} mm  {area_m2 * 1e6:7.4f} mm^2  {per_meter:10.4f}      {per_meter * 100:8.3f}")
diameters = np.array([awg_diameter_mm(g) for g in range(10, 31)])
area_ratio_per_3_gauges = (diameters[:-3] / diameters[3:]) ** 2
print(f"  every 3 gauges the area changes by a factor {area_ratio_per_3_gauges.mean():.3f} (about 2)")

print()
print("Step 4: worked examples")
cord_area = 1.5e-6
cord_length = 2 * 10.0
cord_ohms = wire_resistance(rho_cu, cord_length, cord_area)
print(f"  10 m extension cord, 1.5 mm^2, current goes out and back (20 m): R = {cord_ohms:.3f} ohm")
print(f"    at 10 A the cord itself drops {10 * cord_ohms:.2f} V")
trace_ohms = wire_resistance(rho_cu, 0.050, 0.25e-3 * 35e-6)
print(f"  PCB trace 50 mm long, 0.25 mm wide, 35 um thick: R = {trace_ohms * 1000:.1f} milliohm")
rho_nicr = RESISTIVITY_OHM_METER["nichrome"]
nichrome_area = circle_area(0.4e-3)
per_meter_nicr = wire_resistance(rho_nicr, 1.0, nichrome_area)
print(f"  0.4 mm nichrome wire: {per_meter_nicr:.2f} ohm per meter")
for target in [8.75, 20.0]:
    print(f"    to get {target:5.2f} ohm cut {length_for_resistance(target, rho_nicr, nichrome_area):.3f} m")

print()
print("Step 5: copper gets more resistive when hot")
cold = 10.0
for temperature in [-20, 0, 20, 60, 100]:
    print(f"  a 10.000 ohm copper coil at {temperature:4d} C measures {resistance_at_temperature(cold, temperature):7.3f} ohm")
