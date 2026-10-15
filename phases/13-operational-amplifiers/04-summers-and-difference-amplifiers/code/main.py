import math

from sim import Circuit

RAILS = (-12.0, 12.0)


def inverting_summer(inputs, input_ohms, feedback_ohms):
    circuit = Circuit()
    for k, (volts, ohms) in enumerate(zip(inputs, input_ohms)):
        circuit.voltage_source(f"V{k}", f"in{k}", "0", volts)
        circuit.resistor(f"R{k}", f"in{k}", "sum", ohms)
    circuit.resistor("RF", "sum", "out", feedback_ohms)
    circuit.opamp("U1", plus="0", minus="sum", out="out", gain=1e5, rails=RAILS)
    return circuit.dc()


def show_mixer():
    inputs = [0.5, -0.2, 0.3]
    result = inverting_summer(inputs, [10e3, 10e3, 10e3], 10e3)
    print("Audio mixer: three inputs, all 10 kohm, feedback 10 kohm -> out = -(V1 + V2 + V3)")
    print(f"  inputs {inputs} V -> output {result.v('out'):.5f} V   (ideal {-sum(inputs):.3f} V)")
    print(f"  summing node sits at {result.v('sum') * 1e6:.2f} uV: each input's current is V_k / 10 k, independent of the others")
    weights = inverting_summer([1.0, 1.0, 1.0], [10e3, 20e3, 40e3], 10e3)
    print(f"  weighted: 1 V into 10 k, 20 k, 40 k -> {weights.v('out'):.4f} V   (ideal -(1 + 0.5 + 0.25) = -1.75 V)")
    print()


def show_dac():
    print("A 4-bit digital-to-analogue converter: bits of 5 V into 10 k, 20 k, 40 k, 80 k; feedback 5 k")
    ohms = [10e3, 20e3, 40e3, 80e3]
    for code in [0, 1, 2, 5, 8, 15]:
        bits = [(code >> (3 - k)) & 1 for k in range(4)]
        result = inverting_summer([5.0 * b for b in bits], ohms, 5e3)
        print(f"  code {code:>2} = {''.join(str(b) for b in bits)}  ->  output {result.v('out'):8.4f} V   (ideal {-code * 5.0 / 16:7.4f} V)")
    print()


def difference_amplifier(v1, v2, r1=10e3, r2=10e3, r3=10e3, r4=10e3):
    circuit = Circuit()
    circuit.voltage_source("V1", "a", "0", v1)
    circuit.voltage_source("V2", "b", "0", v2)
    circuit.resistor("R1", "b", "n", r1)
    circuit.resistor("R2", "n", "out", r2)
    circuit.resistor("R3", "a", "p", r3)
    circuit.resistor("R4", "p", "0", r4)
    circuit.opamp("U1", plus="p", minus="n", out="out", gain=1e5, rails=RAILS)
    return circuit.dc()


def show_difference():
    print("Difference amplifier, four 10 k resistors: out = V1 - V2")
    for v1, v2 in [(5.2, 5.0), (1.0, 0.0), (0.0, 1.0), (3.0, 3.0)]:
        result = difference_amplifier(v1, v2)
        print(f"  V1 = {v1:.1f} V, V2 = {v2:.1f} V -> output {result.v('out'):8.5f} V")
    print()


def show_mismatch():
    print("Common-mode rejection: both inputs at 5 V (no difference). Ideal output 0 V.")
    for error in [0.0, 0.001, 0.01, 0.05]:
        result = difference_amplifier(5.0, 5.0, r4=10e3 * (1 + error))
        differential = difference_amplifier(5.001, 5.0, r4=10e3 * (1 + error)).v("out") - result.v("out")
        common_gain = abs(result.v("out")) / 5.0
        cmrr = differential / 0.001 / common_gain if common_gain > 1e-9 else float("inf")
        cmrr_db = f"{20 * math.log10(cmrr):6.1f} dB" if cmrr != float("inf") else "   ideal"
        print(f"  R4 off by {error * 100:4.1f} %: output {result.v('out') * 1000:8.3f} mV   CMRR {cmrr_db}")
    print("  A 1 % resistor error lets 5 V of common-mode voltage leak through as about 25 mV of fake signal.")
    print()


def show_bridge():
    print("Reading a strain-gauge bridge: two dividers from 5 V, 120 ohm gauges, one gauge stretched by 0.2 %")
    gauge = 120.0
    stretched = 120.0 * 1.002
    v1 = 5.0 * stretched / (gauge + stretched)
    v2 = 2.5
    result = difference_amplifier(v1, v2, r1=1e3, r2=100e3, r3=1e3, r4=100e3)
    print(f"  bridge outputs {v1:.5f} V and {v2:.5f} V, difference {(v1 - v2) * 1000:.3f} mV")
    print(f"  difference amp with gain 100 (1 k / 100 k): output {result.v('out'):.4f} V")


def main():
    show_mixer()
    show_dac()
    show_difference()
    show_mismatch()
    show_bridge()


if __name__ == "__main__":
    main()
