import numpy as np

ELECTRON_CHARGE = 1.602176634e-19
COPPER_FREE_ELECTRONS = 8.5e28
SPEED_OF_LIGHT = 2.998e8
CABLE_VELOCITY_FACTOR = 0.66
FERMI_SPEED_COPPER = 1.57e6


def current_from_charge(charge_c, time_s):
    return charge_c / time_s


def electrons_per_second(current_a):
    return current_a / ELECTRON_CHARGE


def drift_velocity(current_a, area_m2, carrier_density=COPPER_FREE_ELECTRONS):
    return current_a / (carrier_density * ELECTRON_CHARGE * area_m2)


def print_basic_currents():
    print("=== Current is charge per second ===")
    examples = [
        ("10 C through a lamp in 5 s", 10.0, 5.0),
        ("0.06 C through an LED in 3 s", 0.06, 3.0),
        ("14 400 C out of a phone battery in 2 h", 14400.0, 7200.0),
    ]
    for label, charge, seconds in examples:
        current = current_from_charge(charge, seconds)
        print(f"{label:40s} I = {current:8.3f} A")
    print()


def print_electron_counts():
    print("=== How many electrons pass each second? ===")
    examples = [
        ("quartz watch", 1.5e-6),
        ("red LED", 0.020),
        ("phone charging", 2.0),
        ("electric kettle", 8.7),
        ("car starter motor", 150.0),
    ]
    for label, current in examples:
        count = electrons_per_second(current)
        print(f"{label:18s} I = {current:9.2e} A  ->  {count:9.2e} electrons per second")
    print()


def print_drift_speeds():
    print("=== Drift speed in copper wire ===")
    cases = [
        ("LED wire, 0.02 A, 0.2 mm^2", 0.02, 0.2e-6),
        ("lamp cord, 1 A, 1 mm^2", 1.0, 1.0e-6),
        ("kettle cord, 8.7 A, 1.5 mm^2", 8.7, 1.5e-6),
        ("starter cable, 150 A, 25 mm^2", 150.0, 25e-6),
    ]
    for label, current, area in cases:
        v = drift_velocity(current, area)
        hours_per_metre = 1.0 / v / 3600.0
        print(f"{label:30s} v = {v * 1000:8.4f} mm/s  ->  {hours_per_metre:7.2f} hours to move 1 m")
    print()


def print_speed_comparison():
    print("=== Three very different speeds ===")
    drift = drift_velocity(1.0, 1.0e-6)
    signal = CABLE_VELOCITY_FACTOR * SPEED_OF_LIGHT
    print(f"Drift speed (1 A in 1 mm^2 copper) = {drift:.2e} m/s")
    print(f"Random thermal-quantum speed       = {FERMI_SPEED_COPPER:.2e} m/s")
    print(f"Signal speed in a typical cable    = {signal:.2e} m/s")
    print(f"Signal is {signal / drift:.1e} times faster than the drift")
    distance = 2.0
    print(f"Over a {distance:.0f} m lamp cord: signal arrives in {distance / signal * 1e9:.1f} ns, an electron needs {distance / drift / 3600:.1f} hours")
    print()


def simulate_counting(seed=7):
    print("=== Counting charges that cross a line (toy wire) ===")
    rng = np.random.default_rng(seed)
    wire_length = 1.0
    charges_per_metre = 2000
    drift = 0.05
    duration = 4.0
    positions = np.sort(rng.uniform(-wire_length, 0.0, charges_per_metre))
    final_positions = positions + drift * duration
    crossed = int(np.sum((positions < 0.0) & (final_positions >= 0.0)))
    measured_rate = crossed / duration
    predicted_rate = charges_per_metre * drift
    print(f"Charges per metre of wire   = {charges_per_metre}")
    print(f"Drift speed                 = {drift} m/s for {duration} s")
    print(f"Charges that crossed x = 0  = {crossed}")
    print(f"Measured rate               = {measured_rate:.1f} charges per second")
    print(f"Predicted (density x speed) = {predicted_rate:.1f} charges per second")
    print()


def simulate_random_walk(seed=11):
    print("=== Fast random motion, slow average drift ===")
    rng = np.random.default_rng(seed)
    electrons = 100000
    steps = 400
    random_speed = 1
    drift_per_step = 0.01
    kicks = (2 * rng.integers(0, 2, size=(steps, electrons), dtype=np.int8) - 1) * random_speed
    displacement = kicks.sum(axis=0, dtype=np.int32) + drift_per_step * steps
    print(f"Each step an electron moves {random_speed} unit left or right at random")
    print(f"Plus a tiny push of {drift_per_step} units per step from the field")
    print(f"Average displacement after {steps} steps = {displacement.mean():.3f} units")
    print(f"Expected from the push alone        = {drift_per_step * steps:.3f} units")
    print(f"Typical size of one electron's wander = {displacement.std():.1f} units")
    print()


def print_ac_wiggle():
    print("=== AC preview: electrons wiggle in place ===")
    rms_current = 1.0
    frequency = 50.0
    area = 1.0e-6
    peak_current = rms_current * np.sqrt(2.0)
    peak_speed = drift_velocity(peak_current, area)
    amplitude = peak_speed / (2 * np.pi * frequency)
    print(f"Peak current {peak_current:.3f} A at {frequency:.0f} Hz in 1 mm^2 copper")
    print(f"Peak drift speed = {peak_speed:.2e} m/s")
    print(f"Electrons swing back and forth by about {amplitude * 1e6:.2f} micrometres")
    print()


def print_charge_in_wire():
    print("=== How much movable charge is already inside a wire? ===")
    volume = 1.0 * 1.0e-6
    electrons = COPPER_FREE_ELECTRONS * volume
    charge = electrons * ELECTRON_CHARGE
    print(f"Free electrons in 1 m of 1 mm^2 copper = {electrons:.2e}")
    print(f"Their total charge                    = {charge:.0f} C")
    print(f"At 1 A, replacing all of them takes   = {charge / 1.0 / 3600:.1f} hours")
    print()


def main():
    print_basic_currents()
    print_electron_counts()
    print_drift_speeds()
    print_speed_comparison()
    print_charge_in_wire()
    simulate_counting()
    simulate_random_walk()
    print_ac_wiggle()


if __name__ == "__main__":
    main()
