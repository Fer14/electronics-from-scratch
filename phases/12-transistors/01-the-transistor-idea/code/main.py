from sim import Circuit

SUPPLY = 10.0
LOAD_OHMS = 1000.0


def ideal_valve(control_volts, transconductance, load_ohms=LOAD_OHMS):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", SUPPLY)
    circuit.voltage_source("VIN", "in", "0", control_volts)
    circuit.resistor("RL", "vcc", "out", load_ohms)
    circuit.vccs("G1", "out", "0", "in", "0", transconductance)
    circuit.resistor("RIN", "in", "0", 1e6)
    return circuit.dc()


def real_transistor(base_emitter_volts, load_ohms=LOAD_OHMS):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", SUPPLY)
    circuit.voltage_source("VIN", "b", "0", base_emitter_volts)
    circuit.resistor("RL", "vcc", "out", load_ohms)
    circuit.npn("Q1", c="out", b="b", e="0", beta=100)
    return circuit.dc()


def show_valve():
    gm = 0.005
    print(f"An ideal 'valve': output current = {gm * 1000:.0f} mA per volt of control voltage, load {LOAD_OHMS:.0f} ohm, supply {SUPPLY:.0f} V")
    print(f"  {'control V':>9} {'control I':>10} {'load I':>9} {'V out':>7} {'control power':>14} {'load power':>11}")
    for volts in [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]:
        result = ideal_valve(volts, gm)
        load_current = result.i("RL")
        control_current = result.i("RIN")
        print(f"  {volts:>8.1f}V {control_current * 1e6:>8.1f}uA {load_current * 1000:>7.2f}mA {result.v('out'):>6.2f}V "
              f"{volts * control_current * 1e6:>11.2f}uW {result.p('RL') * 1000:>9.1f}mW")
    print("  At 3 V the ideal model pushes the output to -5 V, below its own ground: impossible for a real part.")
    print("  A real transistor runs out of voltage at about 0 V instead (it 'saturates').")
    print()


def show_amplification():
    gm = 0.005
    low = ideal_valve(0.9, gm).v("out")
    high = ideal_valve(1.1, gm).v("out")
    gain = (high - low) / 0.2
    print("Amplification: wiggle the control between 0.9 V and 1.1 V")
    print(f"  output moves from {low:.2f} V to {high:.2f} V: voltage gain = {gain:.1f} (= -gm x R_L = -{gm} x {LOAD_OHMS:.0f})")
    print()


def show_switch():
    gm = 0.005
    print("Switching: only two control levels")
    for label, volts in [("OFF (0 V)", 0.0), ("ON  (2 V)", 2.0)]:
        result = ideal_valve(volts, gm)
        print(f"  {label}: load current {result.i('RL') * 1000:5.2f} mA, output {result.v('out'):5.2f} V")
    print()


def show_real_transistor():
    print("A real NPN transistor in the same place: control = base-emitter voltage")
    print(f"  {'V_BE':>6} {'base I':>11} {'collector I':>12} {'V out':>7} {'I_C / I_B':>9}")
    for volts in [0.50, 0.55, 0.60, 0.62, 0.64, 0.66, 0.70, 0.72, 0.75]:
        result = real_transistor(volts)
        collector = result.i("Q1")
        base = result.i("Q1.b")
        ratio = collector / base if base > 0 else float("nan")
        print(f"  {volts:>5.2f}V {base * 1e6:>9.3f}uA {collector * 1000:>10.4f}mA {result.v('out'):>6.2f}V {ratio:>9.1f}")
    print("  A few microamps into the base control milliamps in the collector, 100 times more.")
    print("  From 0.72 V the load cannot pass more than about 10 mA: the transistor saturates and the ratio collapses.")
    print()


def main():
    show_valve()
    show_amplification()
    show_switch()
    show_real_transistor()


if __name__ == "__main__":
    main()
