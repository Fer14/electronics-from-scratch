import numpy as np

from sim import Circuit

SUPPLY = 12.0
BETA = 100.0
THERMAL_VOLTAGE = 0.025852
FREQ = 1000.0


def add_bias_network(circuit):
    circuit.voltage_source("VCC", "vcc", "0", SUPPLY)
    circuit.resistor("R1", "vcc", "b", 100e3)
    circuit.resistor("R2", "b", "0", 10e3)
    circuit.resistor("RC", "vcc", "c", 2200.0)
    circuit.resistor("RE", "e", "0", 200.0)
    circuit.capacitor("CE", "e", "0", 470e-6)


def full_amplifier(amplitude=1.0):
    circuit = Circuit()
    add_bias_network(circuit)
    circuit.sine_source("VIN", "in", "0", amplitude=amplitude, freq=FREQ, offset=0.0)
    circuit.capacitor("CIN", "in", "b", 10e-6)
    circuit.npn("Q1", c="c", b="b", e="e", beta=BETA)
    return circuit


def operating_point():
    result = full_amplifier().dc()
    return result.i("Q1"), result


def small_signal_model(gm, r_pi):
    circuit = Circuit()
    circuit.sine_source("VIN", "in", "0", amplitude=1.0, freq=FREQ, offset=0.0)
    circuit.capacitor("CIN", "in", "b", 10e-6)
    circuit.resistor("R1", "b", "0", 100e3)
    circuit.resistor("R2", "b", "0", 10e3)
    circuit.resistor("RPI", "b", "e", r_pi)
    circuit.vccs("GM", "c", "e", "b", "e", gm)
    circuit.resistor("RC", "c", "0", 2200.0)
    circuit.resistor("RE", "e", "0", 200.0)
    circuit.capacitor("CE", "e", "0", 470e-6)
    return circuit


def show_parameters():
    collector, result = operating_point()
    gm = collector / THERMAL_VOLTAGE
    r_pi = BETA / gm
    print("Operating point (bypassed common-emitter amplifier from lesson 06)")
    print(f"  I_C = {collector * 1000:.4f} mA, V_C = {result.v('c'):.3f} V")
    print("Small-signal parameters")
    print(f"  g_m  = I_C / V_T  = {collector * 1000:.4f} mA / 25.852 mV = {gm * 1000:.2f} mA/V")
    print(f"  r_pi = beta / g_m = 100 / {gm:.5f} = {r_pi:.0f} ohm")
    print(f"  r_e  = 1 / g_m    = {1 / gm:.2f} ohm")
    print()
    return gm, r_pi


def compare_models(gm, r_pi):
    frequencies = [10.0, 100.0, 1000.0, 10000.0]
    full = full_amplifier().ac(frequencies, source="VIN")
    model = small_signal_model(gm, r_pi).ac(frequencies, source="VIN")
    print("Voltage gain |v_c / v_in|: full nonlinear transistor versus the linear small-signal model")
    for k, freq in enumerate(frequencies):
        print(f"  {freq:>7.0f} Hz   transistor {abs(full.v('c')[k]):7.2f}   model {abs(model.v('c')[k]):7.2f}")
    print(f"  mid-band prediction by hand: -g_m x R_C = -{gm:.5f} x 2200 = {-gm * 2200:.1f}")
    print()


def show_input_resistance(r_pi):
    bias = 100e3 * 10e3 / 110e3
    parallel = 1 / (1 / bias + 1 / r_pi)
    print("What the signal source sees (input resistance at mid-band)")
    print(f"  R_in = R1 || R2 || r_pi = 9091 || {r_pi:.0f} = {parallel:.0f} ohm")
    full = full_amplifier().ac([1000.0], source="VIN")
    current = full.i("CIN")[0]
    print(f"  simulator: v_in / i_in = {1 / abs(current):.0f} ohm")
    print()


def harmonic_ratio(signal, time, freq, harmonic):
    window = time >= time[-1] - 4.0 / freq
    values = signal[window] - signal[window].mean()
    t = time[window]
    fundamental = abs(np.sum(values * np.exp(-2j * np.pi * freq * t)))
    other = abs(np.sum(values * np.exp(-2j * np.pi * harmonic * freq * t)))
    return other / fundamental


def show_distortion():
    print("How small is 'small'? Input amplitude versus distortion (2nd harmonic / fundamental)")
    print(f"  {'input':>7} {'output p-p':>11} {'gain':>7} {'2nd harmonic':>13} {'estimate v/(4 V_T)':>19}")
    for amplitude in [0.001, 0.003, 0.010, 0.020]:
        result = full_amplifier(amplitude).transient(t_stop=8e-3, dt=2e-6, initial="dc")
        time = np.asarray(result.time)
        collector = np.asarray(result.v("c"))
        tail = collector[time >= 4e-3]
        swing = tail.max() - tail.min()
        ratio = harmonic_ratio(collector, time, FREQ, 2)
        print(f"  {amplitude * 1000:>5.0f}mV {swing:>9.3f} V {swing / (2 * amplitude):>7.1f} {ratio * 100:>11.2f} % {amplitude / (4 * THERMAL_VOLTAGE) * 100:>17.2f} %")
    print("  The exponential bends the output: keep the base-emitter signal well below V_T (26 mV) for a clean copy.")


def main():
    gm, r_pi = show_parameters()
    compare_models(gm, r_pi)
    show_input_resistance(r_pi)
    show_distortion()


if __name__ == "__main__":
    main()
