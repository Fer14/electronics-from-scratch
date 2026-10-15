import numpy as np

from sim import Circuit

VIN = 5.0
FREQUENCY = 100e3
PERIOD = 1 / FREQUENCY
STEPS = 120
DT = PERIOD / STEPS
INDUCTANCE = 100e-6
CAPACITANCE = 100e-6


def pwm_toggles(duty, cycles):
    on_steps = round(duty * STEPS)
    moments = []
    for k in range(cycles):
        moments += [(k * STEPS + on_steps - 0.5) * DT, ((k + 1) * STEPS - 0.5) * DT]
    return moments


def ideal_gain(duty, load_ohms=None, coil_ohms=0.0):
    gain = 1 / (1 - duty)
    if coil_ohms:
        gain /= 1 + coil_ohms / (load_ohms * (1 - duty) ** 2)
    return gain


def boost(duty, load_ohms, cycles, coil_ohms=0.0, from_rest=False):
    vout = VIN * ideal_gain(duty, load_ohms, coil_ohms)
    i_in = vout ** 2 / load_ohms / VIN
    ripple = VIN * duty * PERIOD / INDUCTANCE
    toggles = pwm_toggles(duty, cycles)
    circuit = Circuit()
    circuit.voltage_source("VIN", "vin", "0", VIN)
    coil_start = "vin"
    if coil_ohms:
        circuit.resistor("RDCR", "vin", "lx", coil_ohms)
        coil_start = "lx"
    circuit.inductor("L1", coil_start, "sw", INDUCTANCE, i0=0.0 if from_rest else i_in - ripple / 2)
    circuit.switch("SLOW", "sw", "0", closed=True, toggle_at=toggles)
    circuit.switch("SHIGH", "sw", "out", closed=False, toggle_at=toggles)
    circuit.capacitor("C1", "out", "0", CAPACITANCE, v0=VIN if from_rest else vout)
    circuit.resistor("RL", "out", "0", load_ohms)
    return circuit.transient(t_stop=cycles * PERIOD, dt=DT)


def last(result, values, periods):
    time = np.asarray(result.time)
    return np.asarray(values)[time >= time[-1] - periods * PERIOD]


def main():
    target, load = 12.0, 24.0
    duty = 1 - VIN / target
    i_out = target / load
    i_in = target * i_out / VIN
    print(f"Design: {VIN:.0f} V -> {target:.0f} V at {i_out:.1f} A ({target * i_out:.0f} W), {FREQUENCY / 1e3:.0f} kHz")
    print(f"  D = 1 - Vin / Vout = {duty:.4f}; input current = Pout / Vin = {i_in:.2f} A")
    delta_i = VIN * duty * PERIOD / INDUCTANCE
    delta_v = i_out * duty * PERIOD / CAPACITANCE
    print(f"  ripple current Vin D / (f L) = {delta_i:.3f} A, output ripple Iout D / (f C) = {delta_v * 1e3:.1f} mV")

    print("\nIdeal synchronous boost: simulation versus Vout = Vin / (1 - D)")
    print(f"  {'D':>6s} {'Vout sim':>9s} {'formula':>8s} {'I in sim':>9s} {'dI sim':>7s} {'dV sim':>8s}")
    for duty_choice in [0.25, 0.5, 7 / 12, 0.75]:
        result = boost(duty_choice, load, cycles=100)
        out = last(result, result.v("out"), 20)
        coil = last(result, result.i("L1"), 20)
        one = last(result, result.v("out"), 1)
        print(f"  {duty_choice:6.4f} {out.mean():7.3f} V {VIN * ideal_gain(duty_choice):6.3f} V {coil.mean():7.3f} A "
              f"{np.ptp(last(result, result.i('L1'), 1)):5.3f} A {np.ptp(one) * 1e3:6.1f} mV")

    result = boost(duty, load, cycles=100)
    p_in = last(result, result.p("VIN"), 20).mean()
    p_out = last(result, result.p("RL"), 20).mean()
    print(f"\nPower balance at D = {duty:.4f}: in {p_in:.3f} W, out {p_out:.3f} W")

    print("\nWith 0.1 ohm of inductor resistance the gain stops growing")
    print(f"  {'D':>5s} {'ideal gain':>10s} {'lossy formula':>13s} {'lossy sim':>9s} {'efficiency':>10s}")
    for duty_choice in [0.5, 0.75, 0.9, 0.95]:
        lossy = ideal_gain(duty_choice, load, 0.1)
        if duty_choice <= 0.9:
            result = boost(duty_choice, load, cycles=300, coil_ohms=0.1)
            sim_gain = last(result, result.v("out"), 20).mean() / VIN
            efficiency = last(result, result.p("RL"), 20).mean() / last(result, result.p("VIN"), 20).mean()
            sim_text = f"{sim_gain:9.3f} {efficiency * 100:9.1f}%"
        else:
            sim_text = f"{'-':>9s} {'-':>10s}"
        print(f"  {duty_choice:5.2f} {ideal_gain(duty_choice):10.2f} {lossy:13.3f} {sim_text}")

    start = boost(duty, load, cycles=600, from_rest=True)
    out, coil = np.asarray(start.v("out")), np.asarray(start.i("L1"))
    print(f"\nSwitching on with the capacitor at Vin (as it is when power is applied): output peaks at {out.max():.2f} V, "
          f"inductor current peaks at {coil.max():.2f} A, after 6 ms Vout = {out[-1]:.2f} V")


if __name__ == "__main__":
    main()
