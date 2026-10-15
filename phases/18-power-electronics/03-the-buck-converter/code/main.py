from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

VIN = 12.0
FREQUENCY = 100e3
PERIOD = 1 / FREQUENCY
STEPS = 120
DT = PERIOD / STEPS
INDUCTANCE = 100e-6
CAPACITANCE = 47e-6


def pwm_toggles(duty, cycles):
    on_steps = round(duty * STEPS)
    moments = []
    for k in range(cycles):
        moments += [(k * STEPS + on_steps - 0.5) * DT, ((k + 1) * STEPS - 0.5) * DT]
    return moments


def buck(duty, load_ohms, cycles, from_rest=False, switch_ohms=1e-3, inductor_ohms=0.0):
    vout = duty * VIN
    ripple = (VIN - vout) * duty * PERIOD / INDUCTANCE
    toggles = pwm_toggles(duty, cycles)
    circuit = Circuit()
    circuit.voltage_source("VIN", "vin", "0", VIN)
    circuit.switch("SHIGH", "vin", "sw", closed=True, ron=switch_ohms, toggle_at=toggles)
    circuit.switch("SLOW", "sw", "0", closed=False, ron=switch_ohms, toggle_at=toggles)
    inductor_end = "sw"
    if inductor_ohms:
        circuit.resistor("RDCR", "sw", "lx", inductor_ohms)
        inductor_end = "lx"
    circuit.inductor("L1", inductor_end, "out", INDUCTANCE, i0=0.0 if from_rest else vout / load_ohms - ripple / 2)
    circuit.capacitor("C1", "out", "0", CAPACITANCE, v0=0.0 if from_rest else vout)
    circuit.resistor("RL", "out", "0", load_ohms)
    return circuit.transient(t_stop=cycles * PERIOD, dt=DT)


def buck_with_pulse_source(duty, load_ohms, cycles):
    vout = duty * VIN
    ripple = (VIN - vout) * duty * PERIOD / INDUCTANCE
    circuit = Circuit()
    circuit.pulse_source("VSW", "sw", "0", low=0.0, high=VIN, period=PERIOD, duty=duty)
    circuit.inductor("L1", "sw", "out", INDUCTANCE, i0=vout / load_ohms - ripple / 2)
    circuit.capacitor("C1", "out", "0", CAPACITANCE, v0=vout)
    circuit.resistor("RL", "out", "0", load_ohms)
    return circuit.transient(t_stop=cycles * PERIOD, dt=DT)


def last(result, values, periods=20):
    time = np.asarray(result.time)
    return np.asarray(values)[time >= time[-1] - periods * PERIOD]


def main():
    target, load = 5.0, 5.0
    duty = target / VIN
    ripple_wanted = 0.3 * target / load
    print(f"Design: {VIN:.0f} V -> {target:.0f} V at {target / load:.0f} A, {FREQUENCY / 1e3:.0f} kHz, duty D = Vout / Vin = {duty:.4f}")
    print(f"  L for 30% ripple: (Vin - Vout) D / (f dI) = {(VIN - target) * duty / (FREQUENCY * ripple_wanted) * 1e6:.1f} uH "
          f"-> use {INDUCTANCE * 1e6:.0f} uH")
    ripple = (VIN - target) * duty * PERIOD / INDUCTANCE
    print(f"  ripple current with {INDUCTANCE * 1e6:.0f} uH: {ripple:.3f} A; C for 10 mV: dI / (8 f dV) = "
          f"{ripple / (8 * FREQUENCY * 0.01) * 1e6:.1f} uF -> use {CAPACITANCE * 1e6:.0f} uF")

    print("\nSteady state with ideal switches, compared with the formulas")
    print(f"  {'D':>6s} {'Vout sim':>9s} {'D x Vin':>8s} {'dI sim':>8s} {'dI formula':>10s} {'dV sim':>8s} {'dV formula':>10s}")
    for duty_choice in [0.25, 5 / 12, 0.6]:
        result = buck(duty_choice, load, cycles=100)
        out = last(result, result.v("out"))
        coil = last(result, result.i("L1"), 1)
        one_period = last(result, result.v("out"), 1)
        vout = duty_choice * VIN
        delta_i = (VIN - vout) * duty_choice * PERIOD / INDUCTANCE
        print(f"  {duty_choice:6.4f} {out.mean():7.3f} V {vout:6.3f} V {np.ptp(coil):6.3f} A {delta_i:8.3f} A "
              f"{np.ptp(one_period) * 1e3:6.2f} mV {delta_i / (8 * FREQUENCY * CAPACITANCE) * 1e3:8.2f} mV")

    result = buck(duty, load, cycles=100)
    p_in = last(result, result.p("VIN")).mean()
    p_out = last(result, result.p("RL")).mean()
    print(f"\nPower balance (ideal parts): in {p_in:.3f} W, out {p_out:.3f} W, efficiency {p_out / p_in * 100:.1f}%")
    real = buck(duty, load, cycles=100, switch_ohms=0.05, inductor_ohms=0.1)
    p_in = last(real, real.p("VIN")).mean()
    p_out = last(real, real.p("RL")).mean()
    print(f"With 50 mohm switches and 0.1 ohm inductor resistance: Vout {last(real, real.v('out')).mean():.3f} V, "
          f"efficiency {p_out / p_in * 100:.1f}% (estimate {5 / (5 + 1 ** 2 * 0.15) * 100:.1f}%)")

    pulse = buck_with_pulse_source(duty, load, cycles=100)
    print(f"Switch node as an ideal pulse source instead of two switches: Vout {last(pulse, pulse.v('out')).mean():.3f} V")

    light = buck(duty, 50.0, cycles=100)
    coil = last(light, light.i("L1"))
    print(f"Light load (50 ohm, 0.1 A): inductor current from {coil.min():.3f} A to {coil.max():.3f} A "
          f"(it goes negative: the low switch lets current flow back)")

    start = buck(duty, load, cycles=400, from_rest=True)
    time, out, coil = np.asarray(start.time), np.asarray(start.v("out")), np.asarray(start.i("L1"))
    settled = np.flatnonzero(np.abs(out - target) > 0.05 * target)
    print(f"\nStarting from zero: output peaks at {out.max():.2f} V (overshoot {(out.max() / target - 1) * 100:.0f}%), "
          f"inductor current peaks at {coil.max():.2f} A,")
    print(f"  stays within 5% of {target:.0f} V after {time[settled[-1]] * 1e3:.2f} ms; "
          f"LC resonance 1 / (2 pi sqrt(LC)) = {1 / (2 * np.pi * np.sqrt(INDUCTANCE * CAPACITANCE)):.0f} Hz")

    figure, (top, bottom) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    window = time < 4e-3
    top.plot(time[window] * 1e3, out[window], color="#8a5a2b")
    top.axhline(target, color="black", linestyle="--", linewidth=0.8)
    top.set_ylabel("Vout (V)")
    bottom.plot(time[window] * 1e3, coil[window], color="#555555", linewidth=0.8)
    bottom.set_ylabel("inductor current (A)")
    bottom.set_xlabel("time (ms)")
    figure.tight_layout()
    path = Path(__file__).parent / "buck_startup.png"
    figure.savefig(path, dpi=120)
    print(f"\nSaved {path.name}")


if __name__ == "__main__":
    main()
