from sim import Circuit

RAILS = (-12.0, 12.0)


def non_inverting(input_volts, feedback_ohms, ground_ohms, gain=1e5, rails=RAILS):
    circuit = Circuit()
    circuit.voltage_source("VIN", "in", "0", input_volts)
    circuit.opamp("U1", plus="in", minus="n", out="out", gain=gain, rails=rails)
    circuit.resistor("RF", "out", "n", feedback_ohms)
    circuit.resistor("RG", "n", "0", ground_ohms)
    return circuit.dc()


def inverting(input_volts, feedback_ohms, input_ohms, gain=1e5, rails=RAILS):
    circuit = Circuit()
    circuit.voltage_source("VIN", "in", "0", input_volts)
    circuit.resistor("RI", "in", "n", input_ohms)
    circuit.resistor("RF", "n", "out", feedback_ohms)
    circuit.opamp("U1", plus="0", minus="n", out="out", gain=gain, rails=rails)
    return circuit.dc()


def show_non_inverting():
    print("Non-inverting amplifier: gain = 1 + R_F / R_G")
    for feedback, ground in [(9e3, 1e3), (47e3, 4.7e3), (1e3, 1e9)]:
        result = non_inverting(0.3, feedback, ground)
        ideal = 1 + feedback / ground
        print(f"  R_F = {feedback:>7.0f}, R_G = {ground:>10.0f}: ideal gain {ideal:7.3f}   0.3 V in -> {result.v('out'):.5f} V out"
              f"   V- = {result.v('n'):.6f} V   input current {result.i('VIN') * 1e9:.4f} nA")
    print()


def show_inverting():
    print("Inverting amplifier: gain = -R_F / R_I, and the minus input is a 'virtual ground'")
    for feedback, input_ohms in [(10e3, 10e3), (100e3, 10e3), (22e3, 4.7e3)]:
        result = inverting(0.5, feedback, input_ohms)
        print(f"  R_F = {feedback:>6.0f}, R_I = {input_ohms:>6.0f}: ideal gain {-feedback / input_ohms:7.3f}   0.5 V in -> {result.v('out'):8.5f} V out"
              f"   V- = {result.v('n') * 1e6:7.2f} uV   source current {result.i('VIN') * 1e6:7.3f} uA")
    print(f"  The source always sees R_I: 0.5 V / 10 k = 50 uA, whatever the gain.")
    print()


def show_finite_gain():
    print("How exact is 'gain = 1 + R_F/R_G'? Closed-loop gain = A / (1 + A B), with B = R_G / (R_F + R_G) = 0.1")
    for gain in [100.0, 1e3, 1e4, 1e5, 1e6]:
        result = non_inverting(1.0, 9e3, 1e3, gain=gain, rails=None)
        formula = gain / (1 + gain * 0.1)
        print(f"  A = {gain:>9.0f}: simulated {result.v('out'):8.5f}   formula {formula:8.5f}   error vs ideal 10: {(10 - result.v('out')) / 10 * 100:7.4f} %")
    print()


def show_saturation():
    print("Gain 10 with +/-12 V rails: the output cannot leave the rails")
    for volts in [0.5, 1.0, 1.1, 1.5, -1.5]:
        result = non_inverting(volts, 9e3, 1e3)
        print(f"  input {volts:5.2f} V -> output {result.v('out'):8.4f} V (ideal {10 * volts:6.2f} V)")
    print()


def show_loading():
    print("Input resistance: a sensor with 100 kohm internal resistance, 1 V open-circuit")
    circuit = Circuit()
    circuit.voltage_source("VS", "s", "0", 1.0)
    circuit.resistor("RS", "s", "in", 100e3)
    circuit.opamp("U1", plus="in", minus="n", out="out", gain=1e5, rails=RAILS)
    circuit.resistor("RF", "out", "n", 9e3)
    circuit.resistor("RG", "n", "0", 1e3)
    print(f"  non-inverting x10: output {circuit.dc().v('out'):.4f} V   (input resistance essentially infinite)")
    circuit = Circuit()
    circuit.voltage_source("VS", "s", "0", 1.0)
    circuit.resistor("RS", "s", "a", 100e3)
    circuit.resistor("RI", "a", "n", 10e3)
    circuit.resistor("RF", "n", "out", 100e3)
    circuit.opamp("U1", plus="0", minus="n", out="out", gain=1e5, rails=RAILS)
    print(f"  inverting x(-10) with R_I = 10 k: output {circuit.dc().v('out'):.4f} V   (the sensor's 100 k adds to R_I: gain -100k/110k)")


def main():
    show_non_inverting()
    show_inverting()
    show_finite_gain()
    show_saturation()
    show_loading()


if __name__ == "__main__":
    main()
