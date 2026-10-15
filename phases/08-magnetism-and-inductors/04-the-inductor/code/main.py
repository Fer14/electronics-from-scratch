import numpy as np

from sim import Circuit, engineering

MU0 = 4 * np.pi * 1e-7


def solenoid_inductance(turns, area, length, relative_permeability=1.0):
    return relative_permeability * MU0 * turns**2 * area / length


def inductor_voltage(inductance, current_change, seconds):
    return inductance * current_change / seconds


def stored_energy(inductance, current):
    return 0.5 * inductance * current**2


def dc_with_part(part):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", 9.0)
    c.resistor("R1", "vcc", "a", 100.0)
    if part == "inductor":
        c.inductor("X", "a", "0", 10e-3)
    elif part == "capacitor":
        c.capacitor("X", "a", "0", 1e-6)
    else:
        c.resistor("X", "a", "0", 100.0)
    result = c.dc()
    return result.v("a"), result.i("R1")


def current_ramp(volts, winding_ohms, inductance, t_stop, dt):
    c = Circuit()
    c.pulse_source("V1", "in", "0", low=0.0, high=volts, period=1.0, duty=0.99)
    c.resistor("Rw", "in", "a", winding_ohms)
    c.inductor("L1", "a", "0", inductance)
    run = c.transient(t_stop=t_stop, dt=dt)
    return np.asarray(run.time), np.asarray(run.i("L1")), np.asarray(run.v("a"))


def current_after_voltage_flip(volts, inductance, flip_time, t_stop, dt):
    c = Circuit()
    c.pulse_source("V1", "in", "0", low=-volts, high=volts, period=2 * flip_time, duty=0.5)
    c.resistor("Rw", "in", "a", 0.01)
    c.inductor("L1", "a", "0", inductance)
    run = c.transient(t_stop=t_stop, dt=dt)
    return np.asarray(run.time), np.asarray(run.i("L1")), np.asarray(run.v("a"))


def main():
    print("=== Step 1: Inductance of a coil, L = mu_r mu0 N^2 A / l ===")
    radius, length = 0.005, 0.02
    area = np.pi * radius**2
    for turns in [50, 100, 200]:
        inductance = solenoid_inductance(turns, area, length)
        print(f"  {turns:>3} turns, radius {radius * 1000:.0f} mm, length {length * 100:.0f} cm, air: L = {inductance * 1e6:7.2f} uH")
    ferrite = solenoid_inductance(100, area, length, 200)
    print(f"  100 turns on a ferrite rod with effective mu_r = 200: L = {ferrite * 1e3:.2f} mH")

    print("\n=== Step 2: The inductor law, v = L di/dt ===")
    for inductance, change, seconds in [(10e-3, 1.0, 1e-3), (10e-3, 1.0, 1e-6), (100e-6, 2.0, 10e-6), (1.0, 0.1, 1.0)]:
        v = inductor_voltage(inductance, change, seconds)
        print(f"  L = {engineering(inductance, 'H'):>8}, current changes {change} A in {engineering(seconds, 's'):>7} -> v = {engineering(v, 'V')}")

    print("\n=== Step 3: Energy stored in the magnetic field, E = 1/2 L I^2 ===")
    for inductance, current in [(10e-3, 1.0), (10e-3, 2.0), (100e-6, 5.0), (1.0, 0.1)]:
        print(f"  L = {engineering(inductance, 'H'):>8} at {current} A: E = {engineering(stored_energy(inductance, current), 'J')}")

    print("\n=== Step 4: At DC an inductor is a wire (9 V, 100 ohm, then the part) ===")
    for part in ["inductor", "capacitor", "resistor"]:
        v_a, i_r1 = dc_with_part(part)
        print(f"  {part:<9} to ground: V(a) = {v_a:6.3f} V, current in R1 = {i_r1 * 1e3:6.2f} mA")

    print("\n=== Step 5: A steady voltage makes the current ramp (1 V across 10 mH) ===")
    t, i_l, v_l = current_ramp(1.0, 0.1, 10e-3, 2e-3, 1e-6)
    for moment in [0.0, 0.5e-3, 1e-3, 2e-3]:
        index = int(round(moment / 1e-6))
        ideal = 1.0 * moment / 10e-3
        print(f"  t = {moment * 1000:3.1f} ms: i = {i_l[index] * 1000:7.2f} mA (ideal ramp V t / L = {ideal * 1000:7.2f} mA), v_L = {v_l[index]:.3f} V")

    print("\n=== Step 6: The current cannot jump, even when the voltage flips ===")
    t, i_l, v_l = current_after_voltage_flip(5.0, 10e-3, 1e-3, 2e-3, 1e-6)
    for moment in [0.999e-3, 1.000e-3, 1.001e-3, 1.5e-3, 2.0e-3]:
        index = int(round(moment / 1e-6))
        print(f"  t = {moment * 1000:6.3f} ms: v_L = {v_l[index]:+6.2f} V, i = {i_l[index] * 1000:7.1f} mA")


if __name__ == "__main__":
    main()
