import numpy as np

from sim import Circuit

FREQ = 50.0
PEAK = 325.0
SOURCE_OHMS = 1.0
LOAD_OHMS = 10.0
PRIMARY_HENRIES = 10.0
RATIO = 10.0
COUPLING = 0.999


def secondary_voltage(primary_volts, primary_turns, secondary_turns):
    return primary_volts * secondary_turns / primary_turns


def turns_for(primary_volts, secondary_volts, primary_turns):
    return primary_turns * secondary_volts / primary_volts


def reflected_resistance(load_ohms, ratio):
    return ratio**2 * load_ohms


def coupled_coils(peak, freq, source_ohms, load_ohms, l1, l2, coupling, t_stop, dt):
    mutual = coupling * np.sqrt(l1 * l2)
    inductance = np.array([[l1, mutual], [mutual, l2]])
    system = inductance / dt + np.diag([source_ohms, load_ohms])
    solver = np.linalg.inv(system)
    steps = int(round(t_stop / dt))
    t = np.arange(steps + 1) * dt
    currents = np.zeros((steps + 1, 2))
    for n in range(1, steps + 1):
        drive = np.array([peak * np.sin(2 * np.pi * freq * t[n]), 0.0])
        currents[n] = solver @ (inductance / dt @ currents[n - 1] + drive)
    load_current = -currents[:, 1]
    return t, currents[:, 0], load_current, load_ohms * load_current, mutual


def equivalent_circuit(peak, freq, source_ohms, load_ohms, l1, ratio, t_stop, dt):
    c = Circuit()
    c.sine_source("Vs", "in", "0", amplitude=peak, freq=freq)
    c.resistor("Rs", "in", "p", source_ohms)
    c.inductor("Lm", "p", "0", l1)
    c.resistor("Rreflected", "p", "0", reflected_resistance(load_ohms, ratio))
    c.vcvs("E1", "out", "0", "p", "0", 1 / ratio)
    c.resistor("RL", "out", "0", load_ohms)
    run = c.transient(t_stop=t_stop, dt=dt, method="be")
    return np.asarray(run.time), np.asarray(run.v("out")), np.asarray(run.i("Rs"))


def last_cycle(t, values, freq):
    mask = t >= t[-1] - 1 / freq
    return values[mask]


def main():
    print("=== Step 1: The turns ratio sets the voltage ===")
    for primary, secondary in [(1000, 100), (1000, 52), (500, 1000)]:
        print(f"  {primary} : {secondary} turns, 325 V peak in -> {secondary_voltage(325, primary, secondary):6.1f} V peak out")
    print(f"  turns needed for 12 V from 230 V with 1000 primary turns: {turns_for(230, 12, 1000):.1f}")

    print("\n=== Step 2: Power in = power out, so the current ratio is upside down ===")
    v_out, i_out = 12.0, 2.0
    ratio = 230 / 12
    print(f"  load takes {i_out} A at {v_out} V = {v_out * i_out:.0f} W")
    print(f"  primary current = {i_out} / {ratio:.2f} = {i_out / ratio * 1e3:.0f} mA, power {230 * i_out / ratio:.0f} W")

    print("\n=== Step 3: A load seen through a transformer looks n^2 times bigger ===")
    for load, n in [(8, 10), (10, 10), (50, 2)]:
        print(f"  {load} ohm load through {n}:1 -> the source sees {reflected_resistance(load, n):.0f} ohm")

    print("\n=== Step 4: Two coupled coils, simulated from their equations ===")
    l2 = PRIMARY_HENRIES / RATIO**2
    t, i1, i2, v2, mutual = coupled_coils(PEAK, FREQ, SOURCE_OHMS, LOAD_OHMS, PRIMARY_HENRIES, l2, COUPLING, 0.2, 1e-5)
    print(f"  L1 = {PRIMARY_HENRIES} H, L2 = {l2 * 1e3:.0f} mH, k = {COUPLING}, M = {mutual * 1e3:.1f} mH")
    print(f"  turns ratio from sqrt(L1 / L2) = {np.sqrt(PRIMARY_HENRIES / l2):.1f}")
    v2_peak = last_cycle(t, v2, FREQ).max()
    i2_peak = last_cycle(t, i2, FREQ).max()
    i1_swing = np.ptp(last_cycle(t, i1, FREQ)) / 2
    print(f"  secondary peak voltage {v2_peak:.2f} V across {LOAD_OHMS:.0f} ohm (ideal 32.5 V)")
    print(f"  secondary peak current {i2_peak:.3f} A, primary peak current {i1_swing:.3f} A")

    print("\n=== Step 5: The same transformer as an equivalent circuit in our simulator ===")
    ts, v_out_sim, i_primary_sim = equivalent_circuit(PEAK, FREQ, SOURCE_OHMS, LOAD_OHMS, PRIMARY_HENRIES, RATIO, 0.2, 1e-5)
    sim_peak = last_cycle(ts, v_out_sim, FREQ).max()
    sim_primary = np.ptp(last_cycle(ts, i_primary_sim, FREQ)) / 2
    print(f"  ideal transformer + magnetizing inductance + reflected load: secondary peak {sim_peak:.2f} V")
    print(f"  primary peak current {sim_primary:.3f} A")
    difference = np.abs(last_cycle(t, v2, FREQ) - last_cycle(ts, v_out_sim, FREQ)).max()
    print(f"  largest difference between the two secondary waveforms: {difference:.3f} V ({difference / sim_peak * 100:.2f} %)")

    print("\n=== Step 6: Efficiency estimate for a small mains transformer ===")
    out_power, copper_loss, core_loss = 24.0, 1.8, 1.2
    print(f"  output {out_power} W, copper loss {copper_loss} W, core loss {core_loss} W")
    print(f"  efficiency = {out_power / (out_power + copper_loss + core_loss) * 100:.1f} %")


if __name__ == "__main__":
    main()
