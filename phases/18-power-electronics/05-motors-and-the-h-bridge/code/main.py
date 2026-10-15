import numpy as np

from sim import Circuit

VBAT = 12.0
R_ARMATURE = 2.0
L_ARMATURE = 1e-3
K_MOTOR = 0.02
INERTIA = 1e-5
FRICTION = 1e-5
WIRING_OHMS = 0.01
PWM_HZ = 20e3
PWM_STEPS = 100

STATES = {
    "forward": {"S1": True, "S2": False, "S3": False, "S4": True},
    "reverse": {"S1": False, "S2": True, "S3": True, "S4": False},
    "brake": {"S1": False, "S2": True, "S3": False, "S4": True},
    "coast": {"S1": False, "S2": False, "S3": False, "S4": False},
    "shoot-through": {"S1": True, "S2": True, "S3": False, "S4": False},
}


def add_motor(circuit, a, b, load_torque=0.0):
    circuit.resistor("RA", a, "m1", R_ARMATURE)
    circuit.inductor("LA", "m1", "m2", L_ARMATURE)
    circuit.vcvs("EMF", "m2", b, "omega", "0", K_MOTOR)
    circuit.vccs("TORQUE", "0", "omega", a, "m1", K_MOTOR / R_ARMATURE)
    circuit.capacitor("J", "omega", "0", INERTIA)
    circuit.resistor("FRICTION", "omega", "0", 1 / FRICTION)
    if load_torque:
        circuit.current_source("TLOAD", "omega", "0", load_torque)


def steady_speed(volts, load_torque=0.0):
    return (K_MOTOR * volts - R_ARMATURE * load_torque) / (K_MOTOR ** 2 + FRICTION * R_ARMATURE)


def start_up(volts, load_torque=0.0):
    circuit = Circuit()
    circuit.voltage_source("VBAT", "a", "0", volts)
    add_motor(circuit, "a", "0", load_torque)
    result = circuit.transient(t_stop=0.3, dt=50e-6)
    return np.asarray(result.time), np.asarray(result.v("omega")), np.asarray(result.i("RA"))


def h_bridge_dc(state):
    closed = STATES[state]
    circuit = Circuit()
    circuit.voltage_source("VBAT", "bat", "0", VBAT)
    circuit.resistor("RWIRE", "bat", "vcc", WIRING_OHMS)
    circuit.switch("S1", "vcc", "a", closed=closed["S1"])
    circuit.switch("S2", "a", "0", closed=closed["S2"])
    circuit.switch("S3", "vcc", "b", closed=closed["S3"])
    circuit.switch("S4", "b", "0", closed=closed["S4"])
    circuit.resistor("RMOTOR", "a", "b", R_ARMATURE)
    result = circuit.dc()
    return result.i("RMOTOR"), result.i("RWIRE")


def braking(state, seconds=0.2):
    closed = STATES[state]
    omega0 = steady_speed(VBAT)
    circuit = Circuit()
    circuit.voltage_source("VBAT", "vcc", "0", VBAT)
    for name, (top, bottom) in {"S1": ("vcc", "a"), "S2": ("a", "0"), "S3": ("vcc", "b"), "S4": ("b", "0")}.items():
        circuit.switch(name, top, bottom, closed=closed[name])
        circuit.diode(f"D{name}", bottom, top)
    circuit.resistor("RA", "a", "m1", R_ARMATURE)
    circuit.inductor("LA", "m1", "m2", L_ARMATURE, i0=FRICTION * omega0 / K_MOTOR)
    circuit.vcvs("EMF", "m2", "b", "omega", "0", K_MOTOR)
    circuit.vccs("TORQUE", "0", "omega", "a", "m1", K_MOTOR / R_ARMATURE)
    circuit.capacitor("J", "omega", "0", INERTIA, v0=omega0)
    circuit.resistor("FRICTION", "omega", "0", 1 / FRICTION)
    result = circuit.transient(t_stop=seconds, dt=200e-6)
    return np.asarray(result.time), np.asarray(result.v("omega"))


def pwm_drive(duty, periods=40):
    period = 1 / PWM_HZ
    dt = period / PWM_STEPS
    on_steps = round(duty * PWM_STEPS)
    toggles = []
    for k in range(periods):
        toggles += [(k * PWM_STEPS + on_steps - 0.5) * dt, ((k + 1) * PWM_STEPS - 0.5) * dt]
    omega0 = steady_speed(duty * VBAT)
    circuit = Circuit()
    circuit.voltage_source("VBAT", "vcc", "0", VBAT)
    circuit.switch("S1", "vcc", "a", closed=True, toggle_at=toggles)
    circuit.switch("S2", "a", "0", closed=False, toggle_at=toggles)
    circuit.switch("S4", "b", "0", closed=True)
    circuit.resistor("RA", "a", "m1", R_ARMATURE)
    circuit.inductor("LA", "m1", "m2", L_ARMATURE, i0=FRICTION * omega0 / K_MOTOR)
    circuit.vcvs("EMF", "m2", "b", "omega", "0", K_MOTOR)
    circuit.vccs("TORQUE", "0", "omega", "a", "m1", K_MOTOR / R_ARMATURE)
    circuit.capacitor("J", "omega", "0", INERTIA, v0=omega0)
    circuit.resistor("FRICTION", "omega", "0", 1 / FRICTION)
    result = circuit.transient(t_stop=periods * period, dt=dt)
    time = np.asarray(result.time)
    tail = time >= time[-1] - 10 * period
    current = np.asarray(result.i("RA"))[tail]
    return np.asarray(result.v("a"))[tail].mean(), current.mean(), np.ptp(current), np.asarray(result.v("omega"))[tail].mean()


def rpm(omega):
    return omega * 60 / (2 * np.pi)


def main():
    print(f"Motor: R = {R_ARMATURE} ohm, L = {L_ARMATURE * 1e3:.0f} mH, k = {K_MOTOR} V s/rad (= N m/A), "
          f"J = {INERTIA:g} kg m^2, friction {FRICTION:g} N m s")
    print(f"  stall current {VBAT / R_ARMATURE:.1f} A, stall torque {K_MOTOR * VBAT / R_ARMATURE:.3f} N m, "
          f"no-load speed {steady_speed(VBAT):.0f} rad/s ({rpm(steady_speed(VBAT)):.0f} rpm)")
    print(f"  mechanical time constant J R / k^2 = {INERTIA * R_ARMATURE / K_MOTOR ** 2 * 1e3:.0f} ms, "
          f"electrical L / R = {L_ARMATURE / R_ARMATURE * 1e3:.1f} ms")

    time, omega, current = start_up(VBAT)
    print(f"\nSwitching 12 V straight onto the motor")
    for moment in [0.001, 0.01, 0.05, 0.1, 0.3]:
        index = np.searchsorted(time, moment)
        print(f"  t = {moment * 1e3:5.0f} ms: speed {omega[index]:6.1f} rad/s ({rpm(omega[index]):5.0f} rpm), "
              f"current {current[index]:5.2f} A, back-EMF {K_MOTOR * omega[index]:5.2f} V")
    print(f"  peak current {current.max():.2f} A")

    print("\nA load torque slows the motor and raises the current")
    for load in [0.0, 0.02, 0.05]:
        time, omega, current = start_up(VBAT, load)
        print(f"  load {load:4.2f} N m: speed {omega[-1]:6.1f} rad/s (formula {steady_speed(VBAT, load):6.1f}), "
              f"current {current[-1]:5.2f} A")

    print("\nH-bridge states (DC, motor stalled so it is just its 2 ohm winding)")
    for state, closed in STATES.items():
        motor, supply = h_bridge_dc(state)
        switches = " ".join(name for name, on in closed.items() if on) or "none"
        print(f"  {state:13s} closed: {switches:12s} motor current {motor:7.2f} A, battery current {supply:8.2f} A")

    print("\nStopping a motor spinning at full speed (with the switches' body diodes)")
    for state in ["coast", "brake"]:
        time, omega = braking(state)
        index = np.searchsorted(time, 0.05)
        print(f"  {state:6s}: speed after 50 ms {omega[index]:6.1f} rad/s, after 200 ms {omega[-1]:6.1f} rad/s")

    print(f"\nSpeed control with {PWM_HZ / 1e3:.0f} kHz PWM on the left leg (S4 kept closed)")
    print(f"  {'duty':>5s} {'avg V(a)':>9s} {'avg I':>7s} {'ripple I':>9s} {'speed':>8s} {'formula':>8s}")
    for duty in [0.25, 0.5, 0.75]:
        volts, amps, ripple, speed = pwm_drive(duty)
        print(f"  {duty:5.2f} {volts:7.2f} V {amps:5.3f} A {ripple * 1e3:6.1f} mA {speed:6.1f} {steady_speed(duty * VBAT):8.1f}")


if __name__ == "__main__":
    main()
