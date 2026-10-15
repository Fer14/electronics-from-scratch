import numpy as np

from sim import Circuit

SUPPLY = 12.0
TOP_OHMS = 100e3
BOTTOM_OHMS = 10e3
EMITTER_OHMS = 200.0
COLLECTOR_OHMS = 2200.0
THERMAL_VOLTAGE = 0.025852


def common_emitter(beta=100.0, collector_ohms=COLLECTOR_OHMS, bypass=None, amplitude=0.0, freq=1000.0):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", SUPPLY)
    circuit.sine_source("VIN", "in", "0", amplitude=amplitude, freq=freq, offset=0.0)
    circuit.capacitor("CIN", "in", "b", 10e-6)
    circuit.resistor("R1", "vcc", "b", TOP_OHMS)
    circuit.resistor("R2", "b", "0", BOTTOM_OHMS)
    circuit.resistor("RC", "vcc", "c", collector_ohms)
    circuit.resistor("RE", "e", "0", EMITTER_OHMS)
    if bypass:
        circuit.capacitor("CE", "e", "0", bypass)
    circuit.npn("Q1", c="c", b="b", e="e", beta=beta)
    return circuit


def fixed_bias(beta):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", SUPPLY)
    circuit.resistor("RB", "vcc", "b", 750e3)
    circuit.resistor("RC", "vcc", "c", COLLECTOR_OHMS)
    circuit.npn("Q1", c="c", b="b", e="0", beta=beta)
    return circuit.dc()


def show_bias_by_hand():
    thevenin_volts = SUPPLY * BOTTOM_OHMS / (TOP_OHMS + BOTTOM_OHMS)
    thevenin_ohms = TOP_OHMS * BOTTOM_OHMS / (TOP_OHMS + BOTTOM_OHMS)
    emitter_current = (thevenin_volts - 0.66) / (EMITTER_OHMS + thevenin_ohms / 101)
    print("Biasing by hand (beta = 100, V_BE about 0.66 V)")
    print(f"  divider Thevenin: V_TH = 12 x 10k / 110k = {thevenin_volts:.3f} V, R_TH = 100k || 10k = {thevenin_ohms:.0f} ohm")
    print(f"  I_E = (V_TH - V_BE) / (R_E + R_TH / (beta + 1)) = ({thevenin_volts:.3f} - 0.66) / ({EMITTER_OHMS:.0f} + {thevenin_ohms / 101:.0f}) = {emitter_current * 1000:.3f} mA")
    print(f"  V_C = 12 - I_C x R_C = {SUPPLY - emitter_current * 0.99 * COLLECTOR_OHMS:.2f} V")
    print()


def show_bias_simulated():
    result = common_emitter().dc()
    print("Operating point from the simulator")
    print(f"  V_B = {result.v('b'):.4f} V   V_E = {result.v('e'):.4f} V   V_BE = {result.v('b', 'e'):.4f} V")
    print(f"  I_C = {result.i('Q1') * 1000:.4f} mA   V_C = {result.v('c'):.3f} V   V_CE = {result.v('c', 'e'):.3f} V")
    print()
    return result


def show_beta_sensitivity():
    print("Why the divider + emitter resistor: what happens when beta changes (transistors vary 2-3x)")
    print(f"  {'beta':>5} {'fixed bias: I_C':>17} {'V_C':>7} {'divider + R_E: I_C':>20} {'V_C':>7}")
    for beta in [50.0, 100.0, 200.0, 300.0]:
        fixed = fixed_bias(beta)
        stable = common_emitter(beta=beta).dc()
        print(f"  {beta:>5.0f} {fixed.i('Q1') * 1000:>14.3f} mA {fixed.v('c'):>6.2f}V {stable.i('Q1') * 1000:>17.3f} mA {stable.v('c'):>6.2f}V")
    print()


def show_gain(operating_point):
    collector_current = operating_point.i("Q1")
    emitter_resistance = THERMAL_VOLTAGE / collector_current
    print("Small-signal voltage gain at 1 kHz")
    print(f"  r_e = V_T / I_C = 25.85 mV / {collector_current * 1000:.3f} mA = {emitter_resistance:.2f} ohm")
    estimate = COLLECTOR_OHMS / (EMITTER_OHMS + emitter_resistance)
    ac = common_emitter(amplitude=1.0).ac([1000.0], source="VIN")
    gain = abs(ac.v("c")[0])
    print(f"  estimate  |A| = R_C / (R_E + r_e) = 2200 / {EMITTER_OHMS + emitter_resistance:.1f} = {estimate:.2f}  ({20 * np.log10(estimate):.2f} dB)")
    print(f"  simulator |A| = {gain:.2f}  ({20 * np.log10(gain):.2f} dB), phase {ac.phase_deg('c')[0]:.1f} degrees (inverting)")
    bypassed = common_emitter(amplitude=1.0, bypass=470e-6).ac([1000.0], source="VIN")
    gain_bypassed = abs(bypassed.v("c")[0])
    print(f"  with R_E bypassed by 470 uF: estimate R_C / r_e = {COLLECTOR_OHMS / emitter_resistance:.1f}, simulator {gain_bypassed:.1f}")
    print()


def show_gain_versus_beta():
    print("Gain versus beta (R_E not bypassed: the gain hardly depends on the transistor)")
    for beta in [50.0, 100.0, 300.0]:
        gain = abs(common_emitter(beta=beta, amplitude=1.0).ac([1000.0], source="VIN").v("c")[0])
        bypassed = abs(common_emitter(beta=beta, amplitude=1.0, bypass=470e-6).ac([1000.0], source="VIN").v("c")[0])
        print(f"  beta {beta:>4.0f}: degenerated gain {gain:6.2f}   bypassed gain {bypassed:7.1f}")
    print()


def show_waveforms():
    print("Time domain: 1 kHz sine at the input, collector swing")
    for amplitude in [0.05, 0.2, 0.5]:
        result = common_emitter(amplitude=amplitude).transient(t_stop=5e-3, dt=5e-6, initial="dc")
        time = np.asarray(result.time)
        collector = np.asarray(result.v("c"))[time > 3e-3]
        swing = collector.max() - collector.min()
        print(f"  input {amplitude * 1000:>4.0f} mV peak: collector between {collector.min():6.3f} V and {collector.max():6.3f} V, "
              f"swing {swing:6.3f} V peak-to-peak, ratio {swing / (2 * amplitude):5.2f}")
    print("  At 0.5 V peak the output would need 10 V of swing around 8.8 V: the top flattens at 12 V, where the transistor cuts off.")


def main():
    show_bias_by_hand()
    operating_point = show_bias_simulated()
    show_beta_sensitivity()
    show_gain(operating_point)
    show_gain_versus_beta()
    show_waveforms()


if __name__ == "__main__":
    main()
