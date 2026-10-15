import numpy as np

from sim import Circuit

AMBIENT = 40.0
TJ_MAX = 125.0
THETA_JC = 5.0
THETA_CS = 0.5
THETA_JA_BARE = 50.0
CAP_DIE = 0.05
CAP_CASE = 2.0
CAP_SINK = 30.0


def steady_junction(power, theta_sa=None):
    circuit = Circuit()
    circuit.voltage_source("TAMB", "amb", "0", AMBIENT)
    circuit.current_source("P", "0", "j", power)
    if theta_sa is None:
        circuit.resistor("RJA", "j", "amb", THETA_JA_BARE)
        result = circuit.dc()
        return result.v("j"), None, None
    circuit.resistor("RJC", "j", "c", THETA_JC)
    circuit.resistor("RCS", "c", "s", THETA_CS)
    circuit.resistor("RSA", "s", "amb", theta_sa)
    result = circuit.dc()
    return result.v("j"), result.v("c"), result.v("s")


def heating_curve(power, theta_sa, t_stop=3000.0, dt=1.0):
    circuit = Circuit()
    circuit.voltage_source("TAMB", "amb", "0", AMBIENT)
    circuit.current_source("P", "0", "j", power)
    circuit.resistor("RJC", "j", "c", THETA_JC)
    circuit.resistor("RCS", "c", "s", THETA_CS)
    circuit.resistor("RSA", "s", "amb", theta_sa)
    circuit.capacitor("CDIE", "j", "0", CAP_DIE, v0=AMBIENT)
    circuit.capacitor("CCASE", "c", "0", CAP_CASE, v0=AMBIENT)
    circuit.capacitor("CSINK", "s", "0", CAP_SINK, v0=AMBIENT)
    result = circuit.transient(t_stop=t_stop, dt=dt)
    return np.asarray(result.time), np.asarray(result.v("j")), np.asarray(result.v("s"))


def step_response(power, theta_sa, t_stop, dt):
    circuit = Circuit()
    circuit.voltage_source("TAMB", "amb", "0", 0.0)
    circuit.current_source("P", "0", "j", power)
    circuit.resistor("RJC", "j", "c", THETA_JC)
    circuit.resistor("RCS", "c", "s", THETA_CS)
    circuit.resistor("RSA", "s", "amb", theta_sa)
    circuit.capacitor("CDIE", "j", "0", CAP_DIE, v0=0.0)
    circuit.capacitor("CCASE", "c", "0", CAP_CASE, v0=0.0)
    circuit.capacitor("CSINK", "s", "0", CAP_SINK, v0=0.0)
    result = circuit.transient(t_stop=t_stop, dt=dt)
    return np.asarray(result.time), np.asarray(result.v("j"))


def mosfet_temperature(current, r_on_25=0.02, alpha=0.005, theta_ja=40.0, rounds=200):
    temperature = AMBIENT
    for count in range(1, rounds + 1):
        r_on = r_on_25 * (1 + alpha * (temperature - 25))
        new_temperature = AMBIENT + theta_ja * current ** 2 * r_on
        if abs(new_temperature - temperature) < 0.01 or new_temperature > 2000:
            return new_temperature, count, r_on
        temperature = new_temperature
    return temperature, rounds, r_on


def loop_gain(current, r_on_25=0.02, alpha=0.005, theta_ja=40.0):
    return theta_ja * current ** 2 * r_on_25 * alpha


def main():
    power = (12 - 5) * 0.5
    print(f"A linear regulator dropping 12 V to 5 V at 0.5 A dissipates {power:.1f} W; ambient {AMBIENT:.0f} C, "
          f"maximum junction {TJ_MAX:.0f} C")
    tj, _, _ = steady_junction(power)
    print(f"  no heatsink (theta_JA = {THETA_JA_BARE:.0f} K/W): Tj = {tj:.1f} C  {'OK' if tj < TJ_MAX else 'TOO HOT'}")
    budget = (TJ_MAX - AMBIENT) / power - THETA_JC - THETA_CS
    print(f"  largest heatsink thermal resistance allowed: ({TJ_MAX:.0f} - {AMBIENT:.0f}) / {power} - {THETA_JC} - {THETA_CS}"
          f" = {budget:.1f} K/W")
    for theta_sa in [30.0, 15.0, 8.0]:
        tj, tc, ts = steady_junction(power, theta_sa)
        print(f"  heatsink {theta_sa:4.1f} K/W: junction {tj:6.1f} C, case {tc:6.1f} C, heatsink {ts:6.1f} C  "
              f"{'OK' if tj < TJ_MAX else 'TOO HOT'}")

    print("\nWarming up after switch-on (15 K/W heatsink, thermal capacities 0.05, 2 and 30 J/K)")
    time, junction, sink = heating_curve(power, 15.0)
    final = junction[-1]
    for moment in [1, 10, 60, 300, 600, 1200, 3000]:
        index = min(np.searchsorted(time, moment), len(time) - 1)
        print(f"  t = {moment:5d} s: junction {junction[index]:6.1f} C, heatsink {sink[index]:6.1f} C")
    rise = final - AMBIENT
    reach = time[np.argmax(junction >= AMBIENT + 0.95 * rise)]
    print(f"  95% of the final rise after {reach:.0f} s; heatsink time constant theta_SA x C = {15 * CAP_SINK:.0f} s")

    print("\nShort power pulses (superposition of two step responses), 50 W, 15 K/W heatsink")
    dt = 1e-3
    time, step = step_response(50.0, 15.0, t_stop=2.0, dt=dt)
    for width in [0.001, 0.01, 0.1, 1.0]:
        shift = int(round(width / dt))
        pulse = step.copy()
        pulse[shift:] -= step[:len(step) - shift]
        print(f"  {width * 1e3:6.0f} ms pulse: peak junction rise {pulse.max():6.2f} K "
              f"(steady 50 W would give {50 * (THETA_JC + THETA_CS + 15):.0f} K)")

    print("\nA MOSFET carrying DC: on-resistance grows with temperature (20 mohm at 25 C, +0.5%/K, theta_JA 40 K/W)")
    for current in [5.0, 10.0, 14.0, 16.0]:
        gain = loop_gain(current)
        temperature, rounds, r_on = mosfet_temperature(current)
        if gain >= 1:
            verdict = "loop gain >= 1: no balance point, thermal runaway"
        elif temperature > 175:
            verdict = "balances, but above a 175 C maximum"
        else:
            verdict = "fine"
        print(f"  {current:4.1f} A: loop gain {gain:4.2f}, after {rounds:3d} rounds Tj = {min(temperature, 2000):7.1f} C, "
              f"R_on {r_on * 1e3:6.1f} mohm  {verdict}")


if __name__ == "__main__":
    main()
