import numpy as np

ELECTRON_CHARGE = 1.602e-19
ELECTRON_MASS = 9.109e-31
COPPER_FREE_ELECTRONS_PER_M3 = 8.5e28
COPPER_MEAN_FREE_TIME = 2.5e-14


def drift_speed(current_amps, area_m2, electrons_per_m3=COPPER_FREE_ELECTRONS_PER_M3):
    return current_amps / (electrons_per_m3 * ELECTRON_CHARGE * area_m2)


def simulate_average_drift(push, mean_free_time, steps=4000, dt=0.01, electrons=5000, seed=0):
    rng = np.random.default_rng(seed)
    velocity = rng.normal(0.0, 1.0, electrons)
    drift_history = []
    collision_probability = dt / mean_free_time
    for step in range(steps):
        velocity += push * dt
        collided = rng.random(electrons) < collision_probability
        velocity[collided] = rng.normal(0.0, 1.0, collided.sum())
        if step >= steps // 2:
            drift_history.append(velocity.mean())
    return float(np.mean(drift_history))


def resistance_from_measurement(volts, amps):
    return volts / amps


def conductivity_from_collisions(electrons_per_m3, mean_free_time):
    return electrons_per_m3 * ELECTRON_CHARGE**2 * mean_free_time / ELECTRON_MASS


print("Step 1: how slowly electrons really drift")
area_one_mm2 = 1e-6
for current in [0.01, 0.1, 1.0, 10.0]:
    speed = drift_speed(current, area_one_mm2)
    print(f"  {current:6.2f} A in a 1 mm^2 copper wire -> drift speed {speed * 1000:8.4f} mm/s")
seconds_for_one_meter = 1.0 / drift_speed(1.0, area_one_mm2)
print(f"  at 1 A an electron needs {seconds_for_one_meter:,.0f} s (~{seconds_for_one_meter / 3600:.1f} hours) to drift 1 m")

print()
print("Step 2: a toy crowd of electrons that keep bumping into the lattice")
print("  push = how hard the electric field accelerates them (arbitrary units)")
print("  mean free time = average time between collisions (arbitrary units)")
for mean_free_time in [1.0, 0.5]:
    for push in [0.0, 0.5, 1.0, 2.0]:
        drift = simulate_average_drift(push, mean_free_time)
        print(f"  mean free time {mean_free_time:3.1f}  push {push:3.1f} -> average drift {drift:6.3f}"
              f"   (prediction push x time = {push * mean_free_time:5.3f})")
print("  doubling the push doubles the drift; halving the time between bumps halves it")

print()
print("Step 3: resistance is volts per amp")
measurements = [
    ("short copper hook-up wire", 0.002, 0.1),
    ("1 m of thin nichrome wire", 4.5, 0.5),
    ("a resistor from the kit", 9.0, 0.009),
    ("your dry skin, hand to hand", 9.0, 0.000009),
]
for name, volts, amps in measurements:
    ohms = resistance_from_measurement(volts, amps)
    print(f"  {name:30s} {volts:7.3f} V / {amps:10.6f} A = {ohms:12,.2f} ohm")

print()
print("Step 4: copper's conductivity from the collision picture")
sigma = conductivity_from_collisions(COPPER_FREE_ELECTRONS_PER_M3, COPPER_MEAN_FREE_TIME)
print(f"  n = {COPPER_FREE_ELECTRONS_PER_M3:.2e} free electrons per m^3, tau = {COPPER_MEAN_FREE_TIME:.1e} s")
print(f"  conductivity sigma = n e^2 tau / m = {sigma:.3e} siemens per meter")
print(f"  measured value for copper at 20 C  = 5.96e+07 siemens per meter")
print(f"  resistivity rho = 1 / sigma = {1 / sigma:.3e} ohm meter")
