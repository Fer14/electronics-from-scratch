import numpy as np

from sim import Circuit

VIN = 12.0
FREQUENCY = 50e3
PERIOD = 1 / FREQUENCY
CYCLES = 200
STEPS = 120


def pwm_toggles(duty, cycles=CYCLES, steps=STEPS):
    on_steps = round(duty * steps)
    dt = PERIOD / steps
    moments = []
    for k in range(cycles):
        moments += [(k * steps + on_steps - 0.5) * dt, ((k + 1) * steps - 0.5) * dt]
    return moments


def add_half_bridge(circuit, duty, node="sw"):
    toggles = pwm_toggles(duty)
    circuit.switch("SHIGH", "vin", node, closed=True, toggle_at=toggles)
    circuit.switch("SLOW", node, "0", closed=False, toggle_at=toggles)


def tail(result, values, periods=10):
    time = np.asarray(result.time)
    return np.asarray(values)[time >= time[-1] - periods * PERIOD]


def chopper_into_heater(duty, load_ohms=10.0):
    circuit = Circuit()
    circuit.voltage_source("VIN", "vin", "0", VIN)
    circuit.switch("S1", "vin", "out", closed=True, toggle_at=pwm_toggles(duty))
    circuit.resistor("RL", "out", "0", load_ohms)
    result = circuit.transient(t_stop=CYCLES * PERIOD, dt=PERIOD / STEPS)
    return {"v_avg": tail(result, result.v("out")).mean(), "p_in": tail(result, result.p("VIN")).mean(),
            "p_load": tail(result, result.p("RL")).mean()}


def filtered(kind, duty, load_ohms=5.0):
    circuit = Circuit()
    circuit.voltage_source("VIN", "vin", "0", VIN)
    add_half_bridge(circuit, duty)
    target = duty * VIN * (load_ohms / (load_ohms + 1.0) if kind == "rc" else 1.0)
    if kind == "rc":
        circuit.resistor("RF", "sw", "out", 1.0)
    else:
        ripple = (VIN - target) * duty * PERIOD / 100e-6
        circuit.inductor("LF", "sw", "out", 100e-6, i0=target / load_ohms - ripple / 2)
    circuit.capacitor("CF", "out", "0", 1000e-6 if kind == "rc" else 100e-6, v0=target)
    circuit.resistor("RL", "out", "0", load_ohms)
    result = circuit.transient(t_stop=CYCLES * PERIOD, dt=PERIOD / STEPS)
    out = tail(result, result.v("out"), 50)
    p_in = tail(result, result.p("VIN"), 50).mean()
    p_load = tail(result, result.p("RL"), 50).mean()
    return {"v_avg": out.mean(), "ripple": out.max() - out.min(), "p_in": p_in, "p_load": p_load,
            "efficiency": p_load / p_in}


def inductive_kick(with_diode):
    current = 1.2
    circuit = Circuit()
    circuit.voltage_source("VIN", "vin", "0", VIN)
    circuit.switch("S1", "vin", "sw", closed=True, toggle_at=[11e-9])
    circuit.capacitor("CPAR", "sw", "0", 100e-12, v0=VIN)
    circuit.inductor("L1", "sw", "out", 100e-6, i0=current)
    circuit.resistor("RL", "out", "0", VIN / current)
    if with_diode:
        circuit.diode("D1", "0", "sw")
    result = circuit.transient(t_stop=2e-6, dt=2e-9)
    sw = np.asarray(result.v("sw"))
    return sw.min(), current * np.sqrt(100e-6 / 100e-12)


def main():
    print(f"An ideal switch chopping {VIN:.0f} V into a 10 ohm heater at {FREQUENCY / 1e3:.0f} kHz")
    print(f"  {'duty':>5s} {'avg V':>7s} {'P in':>7s} {'P heater':>9s} {'lost':>9s}  D x V^2/R")
    for duty in [0.25, 0.5, 0.75]:
        r = chopper_into_heater(duty)
        print(f"  {duty:5.2f} {r['v_avg']:5.2f} V {r['p_in']:5.2f} W {r['p_load']:7.2f} W {(r['p_in'] - r['p_load']) * 1e3:6.2f} mW"
              f"  {duty * VIN ** 2 / 10:5.2f} W")

    print("\nSmoothing the chopped voltage for a 5 ohm electronic load")
    for kind, duty in [("rc", 0.5), ("lc", 5 / 12)]:
        r = filtered(kind, duty)
        name = "1 ohm + 1000 uF (RC)" if kind == "rc" else "100 uH + 100 uF (LC)"
        print(f"  {name:22s} duty {duty:5.3f}: Vout = {r['v_avg']:5.3f} V, ripple {r['ripple'] * 1e3:6.1f} mV, "
              f"P in {r['p_in']:6.2f} W, P load {r['p_load']:5.2f} W, efficiency {r['efficiency'] * 100:5.1f}%")

    print("\nOpening a switch while 1.2 A flows in a 100 uH inductor (100 pF of stray capacitance)")
    lowest, estimate = inductive_kick(False)
    print(f"  no freewheel path: the switch node swings to {lowest:8.1f} V  (estimate -I sqrt(L/C) = {-estimate:.0f} V)")
    lowest, _ = inductive_kick(True)
    print(f"  with a freewheel diode: the switch node only reaches {lowest:6.2f} V")
    print(f"  energy stored in the inductor: 1/2 L I^2 = {0.5 * 100e-6 * 1.2 ** 2 * 1e6:.0f} uJ")

    print("\nMaking 5 V at 1 A from different inputs")
    print(f"  {'Vin':>5s} {'linear eff':>10s} {'linear heat':>11s} {'90% switcher heat':>18s}")
    for vin in [7.0, 12.0, 24.0, 48.0]:
        print(f"  {vin:3.0f} V {5 / vin * 100:8.1f}% {vin - 5:9.1f} W {5 / 0.9 - 5:16.2f} W")


if __name__ == "__main__":
    main()
