from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ELEMENTARY_CHARGE = 1.602176634e-19
ELECTRON_MASS = 9.109e-31
COULOMB_CONSTANT = 8.988e9
EPSILON_0 = 8.854e-12
GRAVITY = 9.81
AIR_BREAKDOWN_FIELD = 3e6
OUTPUT_PATH = Path(__file__).parent / "out.png"


def point_charge_field(charge, source_position, point):
    separation = point - source_position
    distance = np.linalg.norm(separation)
    return COULOMB_CONSTANT * charge / distance**2 * separation / distance


def total_field(sources, point):
    field = np.zeros(2)
    for charge, position in sources:
        field += point_charge_field(charge, position, point)
    return field


def field_on_grid(sources, xs, ys):
    grid_x, grid_y = np.meshgrid(xs, ys)
    field_x = np.zeros_like(grid_x)
    field_y = np.zeros_like(grid_y)
    for charge, position in sources:
        dx = grid_x - position[0]
        dy = grid_y - position[1]
        distance = np.sqrt(dx**2 + dy**2)
        strength = COULOMB_CONSTANT * charge / distance**3
        field_x += strength * dx
        field_y += strength * dy
    return grid_x, grid_y, field_x, field_y


def parallel_plate_field(charge, area):
    return charge / area / EPSILON_0


def fmt(vector):
    clean = np.round(vector, 1) + 0.0
    return f"[{clean[0]:+12,.1f}, {clean[1]:+12,.1f}]"


print("Step 1: field = force per unit charge")
test_charge = 1e-12
force_on_test = np.array([4.5e-8, 0.0])
field = force_on_test / test_charge
print(f"  a {test_charge * 1e12:.0f} pC test charge feels {force_on_test[0]:.1e} N -> E = {field[0]:,.0f} N/C")
print(f"  a 3 pC charge at the same spot feels {3e-12 * field[0]:.2e} N")
print(f"  an electron there feels {-ELEMENTARY_CHARGE * field[0]:.3e} N (opposite way)")

print()
print("Step 2: field of a point charge, E = kQ/r^2")
source_charge = 1e-9
for distance in [0.01, 0.02, 0.05, 0.10]:
    strength = COULOMB_CONSTANT * source_charge / distance**2
    print(f"  Q = 1 nC, r = {distance * 100:3.0f} cm  ->  E = {strength:10,.1f} N/C")

print()
print("Step 3: superposition, field of a dipole")
dipole = [
    (+1e-9, np.array([-0.01, 0.0])),
    (-1e-9, np.array([+0.01, 0.0])),
]
probe_points = {
    "midpoint (0, 0)": np.array([0.0, 0.0]),
    "above (0, 1 cm)": np.array([0.0, 0.01]),
    "right (3 cm, 0)": np.array([0.03, 0.0]),
    "left (-3 cm, 0)": np.array([-0.03, 0.0]),
}
for name, point in probe_points.items():
    field = total_field(dipole, point)
    print(f"  {name:16s} E = {fmt(field)} N/C   |E| = {np.linalg.norm(field):10,.1f} N/C")

print()
print("Step 4: uniform field between two parallel plates")
plate_charge = 1e-9
plate_area = 0.10 * 0.10
uniform = parallel_plate_field(plate_charge, plate_area)
print(f"  +-1 nC on 10 cm x 10 cm plates: sigma = {plate_charge / plate_area:.1e} C/m^2")
print(f"  E = sigma / eps0 = {uniform:,.0f} N/C, the same everywhere between the plates")
electron_force = ELEMENTARY_CHARGE * uniform
electron_acceleration = electron_force / ELECTRON_MASS
print(f"  force on an electron   = {electron_force:.3e} N")
print(f"  electron acceleration  = {electron_acceleration:.3e} m/s^2 = {electron_acceleration / GRAVITY:.2e} g")
print(f"  electron weight        = {ELECTRON_MASS * GRAVITY:.3e} N, ignore it")
gap = 0.005
time_to_cross = np.sqrt(2 * gap / electron_acceleration)
print(f"  time to cross a 5 mm gap from rest = {time_to_cross * 1e9:.1f} ns")

print()
print("Step 5: how much charge until air sparks (E = 3e6 N/C)?")
charge_for_spark = AIR_BREAKDOWN_FIELD * EPSILON_0 * plate_area
print(f"  on 10 cm x 10 cm plates: {charge_for_spark * 1e9:.0f} nC")
radius_for_1uC = np.sqrt(COULOMB_CONSTANT * 1e-6 / AIR_BREAKDOWN_FIELD)
print(f"  near a 1 uC point charge the air breaks down within {radius_for_1uC * 100:.1f} cm")

print()
print("Step 6: field on a grid (numpy) and a quiver plot")
xs = np.linspace(-0.04, 0.04, 21)
ys = np.linspace(-0.03, 0.03, 15)
grid_x, grid_y, field_x, field_y = field_on_grid(dipole, xs, ys)
magnitude = np.sqrt(field_x**2 + field_y**2)
row, col = np.unravel_index(np.argmin(magnitude), magnitude.shape)
print(f"  grid of {magnitude.size} points, strongest |E| = {magnitude.max():,.0f} N/C")
print(f"  weakest |E| = {magnitude.min():,.1f} N/C at ({grid_x[row, col] * 100:+.1f} cm, {grid_y[row, col] * 100:+.1f} cm)")
check = total_field(dipole, np.array([grid_x[7, 10], grid_y[7, 10]]))
print(f"  grid value at the centre matches the loop: {np.allclose(check, [field_x[7, 10], field_y[7, 10]])}")

figure, axes = plt.subplots(figsize=(7, 5))
axes.quiver(grid_x * 100, grid_y * 100, field_x / magnitude, field_y / magnitude, np.log10(magnitude), cmap="viridis")
axes.plot([-1], [0], "o", color="tab:red", markersize=12)
axes.plot([1], [0], "o", color="tab:blue", markersize=12)
axes.set_xlabel("x (cm)")
axes.set_ylabel("y (cm)")
axes.set_title("Field of a dipole: +1 nC (red) and -1 nC (blue)")
axes.set_aspect("equal")
figure.savefig(OUTPUT_PATH, dpi=100, bbox_inches="tight")
plt.close(figure)
print(f"  saved {OUTPUT_PATH.name}")
