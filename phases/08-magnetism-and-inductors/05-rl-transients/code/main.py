from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

SUPPLY = 10.0
INDUCTANCE = 0.1
RESISTANCE = 100.0


def time_constant(inductance, resistance):
    return inductance / resistance


def rise_current(final_current, tau, t):
    return final_current * (1 - np.exp(-t / tau))


def decay_current(start_current, tau, t):
    return start_current * np.exp(-t / tau)


def simulate_rl_square(volts, inductance, resistance, period, t_stop, dt):
    c = Circuit()
    c.pulse_source("V1", "in", "0", low=0.0, high=volts, period=period, duty=0.5)
    c.inductor("L1", "in", "x", inductance)
    c.resistor("R1", "x", "0", resistance)
    return c.transient(t_stop=t_stop, dt=dt)


def simulate_switch_off(with_diode, t_stop, dt):
    steady = SUPPLY / RESISTANCE
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", SUPPLY)
    c.switch("S1", "vcc", "a", closed=True, toggle_at=(1e-3,))
    c.inductor("L1", "a", "x", INDUCTANCE, i0=steady)
    c.resistor("Rcoil", "x", "0", RESISTANCE)
    c.resistor("Rleak", "a", "0", 10e3)
    if with_diode:
        c.diode("D1", "0", "a")
    return c.transient(t_stop=t_stop, dt=dt)


def save_plot(run, tau, path):
    t = np.asarray(run.time)
    fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    axes[0].plot(t * 1e3, np.asarray(run.v("in")), color="gray", label="source (V)")
    axes[0].plot(t * 1e3, np.asarray(run.v("x")), color="saddlebrown", label="v across R1 (V)")
    axes[0].legend()
    axes[0].set_ylabel("volts")
    axes[1].plot(t * 1e3, np.asarray(run.i("L1")) * 1e3, color="saddlebrown", label="simulator")
    axes[1].plot(t * 1e3, np.where(t < 6e-3, rise_current(SUPPLY / RESISTANCE, tau, t) * 1e3, np.nan), "k:", label="formula (rise)")
    axes[1].set_ylabel("inductor current (mA)")
    axes[1].set_xlabel("time (ms)")
    axes[1].legend()
    fig.suptitle("RL circuit driven by a 10 V square wave, tau = 1 ms")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main():
    tau = time_constant(INDUCTANCE, RESISTANCE)
    final = SUPPLY / RESISTANCE
    print("=== Step 1: The time constant tau = L / R ===")
    print(f"  L = {INDUCTANCE * 1e3:.0f} mH, R = {RESISTANCE:.0f} ohm -> tau = {tau * 1e3:.3f} ms")
    print(f"  final current V / R = {final * 1e3:.1f} mA")
    for multiple in [1, 2, 3, 4, 5]:
        i = rise_current(final, tau, multiple * tau)
        print(f"  after {multiple} tau: i = {i * 1e3:6.2f} mA ({i / final * 100:5.1f} % of the final value)")

    print("\n=== Step 2: Rise, simulated vs formula ===")
    run = simulate_rl_square(SUPPLY, INDUCTANCE, RESISTANCE, period=12e-3, t_stop=10e-3, dt=1e-6)
    t = np.asarray(run.time)
    current = np.asarray(run.i("L1"))
    for moment in [0.5e-3, 1e-3, 2e-3, 3e-3, 5e-3]:
        simulated = np.interp(moment, t, current)
        print(f"  t = {moment * 1e3:3.1f} ms: simulator {simulated * 1e3:6.2f} mA, formula {rise_current(final, tau, moment) * 1e3:6.2f} mA")
    crossing = run.time_to_cross("x", 0.632 * SUPPLY, "rising")
    print(f"  v across R1 reaches 63.2 % (6.32 V) at t = {crossing * 1e3:.3f} ms (tau = {tau * 1e3:.3f} ms)")

    print("\n=== Step 3: Decay after the source drops to 0 V at t = 6 ms ===")
    start = np.interp(6e-3, t, current)
    for after in [0.0, 1e-3, 2e-3, 3e-3]:
        simulated = np.interp(6e-3 + after, t, current)
        print(f"  {after * 1e3:3.1f} ms after: simulator {simulated * 1e3:6.2f} mA, formula {decay_current(start, tau, after) * 1e3:6.2f} mA")
    print(f"  the voltage across L1 just after the drop: {np.interp(6e-3 + 2e-6, t, np.asarray(run.v('in', 'x'))):.2f} V")

    print("\n=== Step 4: Opening a switch in series with the coil ===")
    for with_diode in [False, True]:
        kick = simulate_switch_off(with_diode, t_stop=6e-3, dt=1e-6)
        kt = np.asarray(kick.time)
        v_a = np.asarray(kick.v("a"))
        i_l = np.asarray(kick.i("L1"))
        label = "with flyback diode   " if with_diode else "without a diode      "
        decay_at = kt[np.argmax((kt > 1e-3) & (i_l < 0.368 * final))]
        print(f"  {label} lowest V(a) = {v_a.min():9.2f} V, current falls to 36.8 % "
              f"{(decay_at - 1e-3) * 1e6:7.1f} us after opening")
    print(f"  energy that must go somewhere: 1/2 L I^2 = {0.5 * INDUCTANCE * final**2 * 1e3:.2f} mJ")

    path = Path(__file__).parent / "out.png"
    save_plot(run, tau, path)
    print(f"\nPlot saved to {path.name}")


if __name__ == "__main__":
    main()
