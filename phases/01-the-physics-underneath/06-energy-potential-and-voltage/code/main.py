import numpy as np

ELEMENTARY_CHARGE = 1.602176634e-19
ELECTRON_MASS = 9.109e-31
COULOMB_CONSTANT = 8.988e9
GRAVITY = 9.81


def work_by_constant_force(force, distance):
    return force * distance


def potential_of_point_charge(charge, distance):
    return COULOMB_CONSTANT * charge / distance


def field_of_point_charge(charge, source, point):
    separation = point - source
    distance = np.linalg.norm(separation)
    return COULOMB_CONSTANT * charge * separation / distance**3


def work_along_path(charge, source, path, test_charge=1.0):
    total = 0.0
    for start, end in zip(path[:-1], path[1:]):
        middle = (start + end) / 2
        step = end - start
        force = test_charge * field_of_point_charge(charge, source, middle)
        total += float(np.dot(force, step))
    return total


def straight_path(start, end, steps):
    fractions = np.linspace(0.0, 1.0, steps + 1)[:, None]
    return start + fractions * (end - start)


def detour_path(start, corner, end, steps):
    return np.vstack([straight_path(start, corner, steps), straight_path(corner, end, steps)[1:]])


def speed_from_volts(volts, mass=ELECTRON_MASS, charge=ELEMENTARY_CHARGE):
    return np.sqrt(2 * charge * volts / mass)


print("Step 1: gravity first, lifting a 1 kg book")
mass = 1.0
for height in [1.0, 2.0]:
    energy = mass * GRAVITY * height
    print(f"  lift {mass:.0f} kg by {height:.0f} m: work = {energy:.2f} J, energy per kg = {energy / mass:.2f} J/kg")

print()
print("Step 2: voltage = energy per charge")
for volts in [1.5, 9.0, 230.0]:
    print(f"  {volts:6.1f} V source: 1 C gains {volts:6.1f} J, 0.5 C gains {0.5 * volts:6.2f} J, one electron gains {volts * ELEMENTARY_CHARGE:.3e} J = {volts:.1f} eV")

print()
print("Step 3: uniform field, work = q E d and V = E d")
field = 2000.0
gap = 0.006
charge = 1e-6
force = charge * field
work = work_by_constant_force(force, gap)
print(f"  E = {field:.0f} V/m, gap {gap * 1000:.0f} mm, q = 1 uC")
print(f"  force = {force:.1e} N, work across the gap = {work:.2e} J")
print(f"  work / charge = {work / charge:.1f} J/C = {field * gap:.1f} V = E x d")
for volts, distance in [(12.0, 0.001), (5.0, 0.0001), (1.0, 1e-8)]:
    print(f"  {volts:5.1f} V across {distance * 1e6:7g} um -> E = {volts / distance:12,.0f} V/m")

print()
print("Step 4: potential of a point charge, V = kQ/r")
source_charge = 1e-9
for distance in [0.01, 0.02, 0.05, 0.10]:
    print(f"  Q = 1 nC, r = {distance * 100:3.0f} cm -> V = {potential_of_point_charge(source_charge, distance):6.1f} V")
v_a = potential_of_point_charge(source_charge, 0.01)
v_b = potential_of_point_charge(source_charge, 0.03)
print(f"  voltage from A (1 cm) to B (3 cm) = {v_a:.1f} - {v_b:.1f} = {v_a - v_b:.1f} V")

print()
print("Step 5: the work does not depend on the path")
source = np.array([0.0, 0.0])
point_a = np.array([0.01, 0.0])
point_b = np.array([0.0, 0.03])
paths = {
    "straight A -> B": straight_path(point_a, point_b, 4000),
    "detour via (3 cm, 3 cm)": detour_path(point_a, np.array([0.03, 0.03]), point_b, 4000),
    "detour via (-2 cm, 4 cm)": detour_path(point_a, np.array([-0.02, 0.04]), point_b, 4000),
}
for name, path in paths.items():
    print(f"  work per coulomb, {name:25s} = {work_along_path(source_charge, source, path):.3f} J/C")
print(f"  {'potential difference V_A - V_B':43s} = {v_a - v_b:.3f} V")

print()
print("Step 6: electron-volts and accelerated electrons")
print(f"  1 eV = {ELEMENTARY_CHARGE:.4e} J")
for volts in [1.0, 100.0, 1000.0, 25000.0]:
    speed = speed_from_volts(volts)
    print(f"  electron through {volts:8.0f} V: energy {volts * ELEMENTARY_CHARGE:.3e} J, speed {speed:.3e} m/s ({speed / 3e8 * 100:.1f}% of light)")

print()
print("Step 7: ground is a choice of zero")
potentials_battery_minus = {"battery -": 0.0, "battery +": 9.0, "between lamps": 4.5}
shift = -4.5
potentials_midpoint = {node: value + shift for node, value in potentials_battery_minus.items()}
for node in potentials_battery_minus:
    print(f"  {node:14s} ground at battery -: {potentials_battery_minus[node]:+5.1f} V   ground at midpoint: {potentials_midpoint[node]:+5.1f} V")
difference_one = potentials_battery_minus["battery +"] - potentials_battery_minus["battery -"]
difference_two = potentials_midpoint["battery +"] - potentials_midpoint["battery -"]
print(f"  voltage across the battery: {difference_one:.1f} V vs {difference_two:.1f} V, same either way")
