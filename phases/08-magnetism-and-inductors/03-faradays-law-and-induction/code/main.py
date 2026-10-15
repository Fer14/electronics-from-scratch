import numpy as np

from sim import Circuit

MU0 = 4 * np.pi * 1e-7
G = 9.81


def flux(field, area, angle_deg=0.0):
    return field * area * np.cos(np.radians(angle_deg))


def average_emf(turns, flux_before, flux_after, seconds):
    return -turns * (flux_after - flux_before) / seconds


def motional_emf(field, length, speed):
    return field * length * speed


def rotating_coil_flux(turns_area_field, omega, t):
    return turns_area_field * np.cos(omega * t)


def numerical_derivative(values, t):
    return np.gradient(values, t)


def dipole_flux_through_loop(moment, loop_radius, z):
    return MU0 * moment * loop_radius**2 / (2 * (loop_radius**2 + z**2) ** 1.5)


def falling_magnet_emf(moment, loop_radius, turns, drop_height, duration, steps):
    t = np.linspace(0, duration, steps)
    z = drop_height - 0.5 * G * t**2
    linked = turns * dipole_flux_through_loop(moment, loop_radius, z)
    return t, z, -numerical_derivative(linked, t)


def lamp_on_generator(peak_volts, freq, lamp_ohms):
    c = Circuit()
    c.sine_source("Vgen", "a", "0", amplitude=peak_volts, freq=freq)
    c.resistor("Rlamp", "a", "0", lamp_ohms)
    run = c.transient(t_stop=4 / freq, dt=1 / freq / 2000)
    current = np.asarray(run.i("Rlamp"))
    voltage = np.asarray(run.v("a"))
    last_cycle = np.asarray(run.time) >= 3 / freq
    return current[last_cycle].max(), np.mean((voltage * current)[last_cycle])


def main():
    print("=== Step 1: Magnetic flux, Phi = B * A * cos(angle) ===")
    area = 0.02 * 0.02
    for angle in [0, 60, 90]:
        print(f"  B = 0.3 T through 2 cm x 2 cm at {angle:>2} deg: Phi = {flux(0.3, area, angle) * 1e6:7.2f} uWb")

    print("\n=== Step 2: Faraday's law, EMF = -N dPhi/dt ===")
    before, after = flux(0.0, area), flux(0.3, area)
    for seconds in [0.5, 0.05, 0.005]:
        emf = average_emf(200, before, after, seconds)
        print(f"  200 turns, field 0 -> 0.3 T in {seconds * 1000:>5.0f} ms: EMF = {emf:8.2f} V")
    print(f"  field 0.3 -> 0 T in 50 ms: EMF = {average_emf(200, after, before, 0.05):+.2f} V (sign flips)")

    print("\n=== Step 3: Motional EMF of a rod sliding on rails, EMF = B L v ===")
    for speed in [1, 2, 5]:
        print(f"  B = 0.5 T, L = 10 cm, v = {speed} m/s: EMF = {motional_emf(0.5, 0.1, speed):.2f} V")

    print("\n=== Step 4: A coil spinning in a field makes a sine wave ===")
    turns, field, coil_area, freq = 100, 0.1, 0.01, 50
    omega = 2 * np.pi * freq
    t = np.linspace(0, 2 / freq, 4001)
    linked = rotating_coil_flux(turns * field * coil_area, omega, t)
    emf = -numerical_derivative(linked, t)
    predicted_peak = turns * field * coil_area * omega
    print(f"  N = {turns}, B = {field} T, A = {coil_area * 1e4:.0f} cm^2, f = {freq} Hz, omega = {omega:.2f} rad/s")
    print(f"  peak EMF from the numerical derivative: {emf.max():.2f} V")
    print(f"  peak EMF predicted N B A omega:          {predicted_peak:.2f} V")
    for fraction in [0.0, 0.25, 0.5, 0.75]:
        index = round(fraction / freq / (t[1] - t[0]))
        print(f"  at t = {t[index] * 1000:4.1f} ms: flux linkage {linked[index] * 1e3:7.2f} mWb-turns, EMF {emf[index]:7.2f} V")

    print("\n=== Step 5: A magnet falling through a coil (Lenz's law) ===")
    t, z, emf = falling_magnet_emf(moment=1.035, loop_radius=0.015, turns=50, drop_height=0.10,
                                   duration=0.2, steps=20001)
    centre = np.argmin(np.abs(z))
    first = np.argmax(np.abs(emf[:centre]))
    second = centre + np.argmax(np.abs(emf[centre:]))
    print(f"  magnet crosses the coil at t = {t[centre] * 1000:.1f} ms at {G * t[centre]:.2f} m/s")
    print(f"  approaching: peak EMF {emf[first] * 1000:+7.1f} mV at t = {t[first] * 1000:.1f} ms")
    print(f"  leaving:     peak EMF {emf[second] * 1000:+7.1f} mV at t = {t[second] * 1000:.1f} ms")
    print(f"  EMF exactly at the centre: {emf[centre] * 1000:+.2f} mV")

    print("\n=== Step 6: Our generator lights a 100 ohm lamp (simulator) ===")
    peak_current, average_power = lamp_on_generator(predicted_peak, freq, 100.0)
    print(f"  peak current {peak_current:.3f} A (hand: {predicted_peak / 100:.3f} A)")
    print(f"  average power {average_power:.2f} W (hand: {predicted_peak**2 / 2 / 100:.2f} W)")


if __name__ == "__main__":
    main()
