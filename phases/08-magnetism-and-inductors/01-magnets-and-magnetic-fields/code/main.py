from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

MU0 = 4 * np.pi * 1e-7
ELECTRON_CHARGE = 1.602176634e-19
ELECTRON_MASS = 9.109e-31
EARTH_FIELD = 50e-6


def tesla_to_gauss(b):
    return b * 1e4


def dipole_field_on_axis(moment, distance):
    return MU0 / (4 * np.pi) * 2 * moment / distance**3


def dipole_field_at(moment, x, z):
    r = np.sqrt(x**2 + z**2)
    m_dot_r = moment * z
    bx = MU0 / (4 * np.pi) * (3 * x * m_dot_r / r**5)
    bz = MU0 / (4 * np.pi) * (3 * z * m_dot_r / r**5 - moment / r**3)
    return bx, bz


def magnet_moment_from_remanence(remanence, volume):
    return remanence * volume / MU0


def distance_where_field_equals(moment, target_field):
    return (MU0 / (4 * np.pi) * 2 * moment / target_field) ** (1 / 3)


def magnetic_force_on_charge(charge, speed, field, angle_deg=90.0):
    return abs(charge) * speed * field * np.sin(np.radians(angle_deg))


def circle_radius(mass, speed, charge, field):
    return mass * speed / (abs(charge) * field)


def compass_torque(moment, field, angle_deg):
    return moment * field * np.sin(np.radians(angle_deg))


def save_field_plot(moment, path):
    xs = np.linspace(-0.05, 0.05, 41)
    zs = np.linspace(-0.05, 0.05, 41)
    x_grid, z_grid = np.meshgrid(xs, zs)
    inside = np.sqrt(x_grid**2 + z_grid**2) < 0.006
    x_safe = np.where(inside, 0.006, x_grid)
    bx, bz = dipole_field_at(moment, x_safe, np.where(inside, 0.006, z_grid))
    bx = np.where(inside, np.nan, bx)
    bz = np.where(inside, np.nan, bz)
    strength = np.hypot(bx, bz)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.streamplot(x_grid * 100, z_grid * 100, bx, bz, color=np.log10(strength), cmap="copper", density=1.4)
    ax.add_patch(plt.Rectangle((-0.3, -0.6), 0.6, 1.2, color="firebrick"))
    ax.text(0, 0.8, "N", ha="center", fontsize=12)
    ax.text(0, -1.1, "S", ha="center", fontsize=12)
    ax.set_xlabel("x (cm)")
    ax.set_ylabel("z (cm)")
    ax.set_title("Field lines of a small bar magnet")
    ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main():
    print("=== Step 1: Units of magnetic field ===")
    for name, b in [("Earth's field", EARTH_FIELD), ("fridge magnet surface", 5e-3),
                    ("neodymium magnet surface", 0.5), ("MRI scanner", 3.0)]:
        print(f"  {name:<26} {b:>10.6f} T = {tesla_to_gauss(b):>10.1f} gauss")

    print("\n=== Step 2: How strong is a small neodymium cube? ===")
    side = 0.01
    volume = side**3
    remanence = 1.3
    moment = magnet_moment_from_remanence(remanence, volume)
    print(f"  cube side {side * 100:.1f} cm, volume {volume:.1e} m^3, remanence {remanence} T")
    print(f"  magnetic moment m = Br * V / mu0 = {moment:.3f} A*m^2")

    print("\n=== Step 3: The field falls off as 1 / distance^3 ===")
    for d_cm in [1, 2, 5, 10, 20, 50]:
        b = dipole_field_on_axis(moment, d_cm / 100)
        print(f"  {d_cm:>3} cm from the centre: B = {b * 1e6:>12.2f} uT  ({b / EARTH_FIELD:>9.2f} x Earth)")
    d_earth = distance_where_field_equals(moment, EARTH_FIELD)
    print(f"  the magnet matches Earth's 50 uT at {d_earth * 100:.1f} cm")

    print("\n=== Step 4: Force on a moving electron, F = q v B ===")
    speed = 1e6
    field = 0.5
    force = magnetic_force_on_charge(ELECTRON_CHARGE, speed, field)
    radius = circle_radius(ELECTRON_MASS, speed, ELECTRON_CHARGE, field)
    print(f"  electron at {speed:.0e} m/s across {field} T: F = {force:.3e} N")
    print(f"  it curves in a circle of radius {radius * 1e6:.2f} um")
    for angle in [90, 45, 0]:
        f = magnetic_force_on_charge(ELECTRON_CHARGE, speed, field, angle)
        print(f"  angle between velocity and field {angle:>2} deg -> F = {f:.3e} N")

    print("\n=== Step 5: Why a compass needle turns ===")
    needle_moment = 0.05
    for angle in [0, 30, 90, 180]:
        torque = compass_torque(needle_moment, EARTH_FIELD, angle)
        print(f"  needle {angle:>3} deg away from north: torque = {torque * 1e6:.3f} uN*m")

    path = Path(__file__).parent / "out.png"
    save_field_plot(moment, path)
    print(f"\nField-line plot saved to {path.name}")


if __name__ == "__main__":
    main()
