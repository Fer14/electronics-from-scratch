import numpy as np

from sim import Circuit

SUPPLY = 12.0
WINDING_OHMS = 2.0
WINDING_HENRIES = 1e-3
MOTOR_CONSTANT = 0.02
INERTIA = 1e-5
FRICTION = 1e-6


def loop_torque(turns, field, current, area, angle_deg):
    return turns * field * current * area * np.sin(np.radians(angle_deg))


def rad_per_s_to_rpm(omega):
    return omega * 60 / (2 * np.pi)


def no_load_speed(volts, k, resistance, friction):
    return volts * k / (k**2 + resistance * friction)


def spin_up(volts, load_torque, t_stop, dt):
    steps = int(round(t_stop / dt))
    t = np.arange(steps + 1) * dt
    current = np.zeros(steps + 1)
    speed = np.zeros(steps + 1)
    for n in range(steps):
        back_emf = MOTOR_CONSTANT * speed[n]
        di = (volts - WINDING_OHMS * current[n] - back_emf) / WINDING_HENRIES
        current[n + 1] = current[n] + di * dt
        torque = MOTOR_CONSTANT * current[n + 1] - FRICTION * speed[n] - load_torque
        speed[n + 1] = speed[n] + torque / INERTIA * dt
    return t, current, speed


def stalled_inrush():
    c = Circuit()
    c.pulse_source("V1", "vcc", "0", low=0.0, high=SUPPLY, period=1.0, duty=0.99)
    c.resistor("Rw", "vcc", "x", WINDING_OHMS)
    c.inductor("Lw", "x", "0", WINDING_HENRIES)
    run = c.transient(t_stop=3e-3, dt=1e-6)
    return np.asarray(run.time), np.asarray(run.i("Lw"))


def running_motor_dc(back_emf):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", SUPPLY)
    c.resistor("Rw", "vcc", "x", WINDING_OHMS)
    c.inductor("Lw", "x", "y", WINDING_HENRIES)
    c.voltage_source("Eback", "y", "0", back_emf)
    result = c.dc()
    return result.i("Rw"), result.p("Rw"), back_emf * result.i("Rw")


def generator_into_load(speed, load_ohms):
    c = Circuit()
    c.voltage_source("Egen", "e", "0", MOTOR_CONSTANT * speed)
    c.resistor("Rw", "e", "out", WINDING_OHMS)
    c.resistor("Rload", "out", "0", load_ohms)
    result = c.dc()
    return result.v("out"), result.i("Rload"), result.p("Rload"), result.p("Rw")


def main():
    print("=== Step 1: Torque on a current loop, T = N B I A sin(angle) ===")
    for angle in [90, 45, 0]:
        torque = loop_torque(50, 0.4, 1.0, 0.001, angle)
        print(f"  50 turns, B = 0.4 T, I = 1 A, A = 10 cm^2, angle {angle:>2} deg: T = {torque * 1000:6.2f} mN*m")

    print("\n=== Step 2: The motor's key numbers (12 V, R = 2 ohm, k = 0.02 V*s/rad) ===")
    stall_current = SUPPLY / WINDING_OHMS
    omega0 = no_load_speed(SUPPLY, MOTOR_CONSTANT, WINDING_OHMS, FRICTION)
    print(f"  stall current V / R = {stall_current:.1f} A, stall torque k I = {MOTOR_CONSTANT * stall_current * 1000:.0f} mN*m")
    print(f"  no-load speed = {omega0:.1f} rad/s = {rad_per_s_to_rpm(omega0):.0f} rpm")
    print(f"  no-load current = {FRICTION * omega0 / MOTOR_CONSTANT * 1000:.1f} mA")
    print(f"  electrical time constant L / R = {WINDING_HENRIES / WINDING_OHMS * 1000:.2f} ms")
    print(f"  mechanical time constant J R / k^2 = {INERTIA * WINDING_OHMS / MOTOR_CONSTANT**2 * 1000:.1f} ms")

    print("\n=== Step 3: Spin-up from rest, simulated step by step ===")
    t, current, speed = spin_up(SUPPLY, 0.0, 0.3, 1e-5)
    print(f"  peak current {current.max():.2f} A at t = {t[np.argmax(current)] * 1000:.2f} ms")
    for moment in [0.01, 0.05, 0.1, 0.25]:
        index = int(round(moment / 1e-5))
        print(f"  t = {moment * 1000:5.0f} ms: speed {rad_per_s_to_rpm(speed[index]):6.0f} rpm, "
              f"back-EMF {MOTOR_CONSTANT * speed[index]:5.2f} V, current {current[index]:5.2f} A")

    print("\n=== Step 4: The winding with the rotor held still (our simulator) ===")
    ts, inrush = stalled_inrush()
    for moment in [0.5e-3, 1e-3, 2.5e-3]:
        print(f"  t = {moment * 1000:3.1f} ms: current {np.interp(moment, ts, inrush):5.2f} A (final {stall_current:.1f} A)")

    print("\n=== Step 5: Running under load: back-EMF sets the current (friction ignored) ===")
    for load_torque in [0.005, 0.01, 0.03, 0.06]:
        needed_current = load_torque / MOTOR_CONSTANT
        back_emf = SUPPLY - WINDING_OHMS * needed_current
        current_sim, heat, mechanical = running_motor_dc(back_emf)
        speed_rpm = rad_per_s_to_rpm(back_emf / MOTOR_CONSTANT)
        efficiency = mechanical / (SUPPLY * current_sim) * 100
        print(f"  load {load_torque * 1000:4.0f} mN*m: back-EMF {back_emf:5.2f} V, I = {current_sim:4.2f} A, "
              f"{speed_rpm:5.0f} rpm, heat {heat:5.2f} W, mechanical {mechanical:5.2f} W, efficiency {efficiency:5.1f} %")

    print("\n=== Step 6: The same machine as a generator ===")
    spin = 300.0
    print(f"  spun at {spin:.0f} rad/s ({rad_per_s_to_rpm(spin):.0f} rpm): EMF = k omega = {MOTOR_CONSTANT * spin:.1f} V")
    for load in [1e6, 10.0, 2.0]:
        v_out, i_out, p_load, p_winding = generator_into_load(spin, load)
        brake = MOTOR_CONSTANT * i_out
        print(f"  load {load:>9.0f} ohm: V_out = {v_out:5.2f} V, I = {i_out:5.3f} A, P_load = {p_load:5.2f} W, "
              f"P_winding = {p_winding:5.2f} W, braking torque = {brake * 1000:5.1f} mN*m, P_mech = {brake * spin:5.2f} W")


if __name__ == "__main__":
    main()
