from sim import Circuit


def voltage_amplifier(signal_volts, load_ohms=900):
    circuit = Circuit()
    circuit.voltage_source("VS", "s", "0", signal_volts)
    circuit.resistor("RS", "s", "in", 1000)
    circuit.resistor("RIN", "in", "0", 9000)
    circuit.vcvs("E1", "x", "0", "in", "0", 50.0)
    circuit.resistor("ROUT", "x", "out", 100)
    circuit.resistor("RL", "out", "0", load_ohms)
    return circuit


def transconductance_stage(input_volts, rc_ohms=2000, gm=0.04):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", 10.0)
    circuit.voltage_source("VIN", "in", "0", input_volts)
    circuit.resistor("RC", "vcc", "out", rc_ohms)
    circuit.vccs("G1", "out", "0", "in", "0", gm)
    return circuit


def inverting_amplifier(gain, input_volts=0.1):
    circuit = Circuit()
    circuit.voltage_source("VIN", "in", "0", input_volts)
    circuit.resistor("R1", "in", "n", 1000)
    circuit.resistor("R2", "n", "out", 10000)
    circuit.vcvs("E1", "out", "0", "0", "n", gain)
    return circuit


def follower_output_resistance(gain, rout=100.0, test_amps=1e-3):
    circuit = Circuit()
    circuit.voltage_source("VIN", "in", "0", 0.0)
    circuit.vcvs("E1", "x", "0", "in", "out", gain)
    circuit.resistor("ROUT", "x", "out", rout)
    circuit.current_source("ITEST", "0", "out", test_amps)
    return circuit.dc().v("out") / test_amps


def main():
    print("=== Example 1: voltage amplifier model (Rin = 9 kOhm, A = 50, Rout = 100 Ohm) ===")
    result = voltage_amplifier(0.1).dc()
    v_in, v_out = result.v("in"), result.v("out")
    print(f"  v(in)  = {v_in * 1000:7.3f} mV   (hand: 100 mV x 9/10 = 90 mV)")
    print(f"  v(out) = {v_out:7.4f} V    (hand: 50 x 90 mV x 900/1000 = 4.05 V)")
    print(f"  overall voltage gain = {v_out / 0.1:.2f}   (the box says 50)")
    input_power = result.p("RIN")
    load_power = result.p("RL")
    print(f"  power into the input = {input_power * 1e6:.3f} uW, power into the load = {load_power * 1000:.3f} mW,"
          f" power gain = {load_power / input_power:,.0f}")
    for load in (100, 900, 10000, 1e6):
        gain = voltage_amplifier(0.1, load).dc().v("out") / 0.1
        print(f"    with RL = {load:>9,.0f} Ohm the overall gain is {gain:6.2f}")

    print("\n=== Example 2: transistor-like stage (VCCS gm = 40 mS, RC = 2 kOhm, VCC = 10 V) ===")
    outputs = {}
    for v_in_mv in (0.0, 10.0, 20.0):
        outputs[v_in_mv] = transconductance_stage(v_in_mv / 1000).dc().v("out")
        print(f"  v(in) = {v_in_mv:4.1f} mV  ->  G1 pulls {0.04 * v_in_mv:5.2f} mA  ->  v(out) = {outputs[v_in_mv]:6.3f} V")
    gain = (outputs[20.0] - outputs[10.0]) / 0.010
    print(f"  small-signal gain = {gain:.1f}   (hand: -gm x RC = {-0.04 * 2000:.1f})")

    print("\n=== Example 3: feedback around a huge gain (R1 = 1 kOhm, R2 = 10 kOhm) ===")
    for open_loop in (10.0, 100.0, 1e3, 1e4, 1e5, 1e6):
        closed = inverting_amplifier(open_loop).dc().v("out") / 0.1
        formula = -(open_loop * 10 / 11) / (1 + open_loop / 11)
        print(f"  A = {open_loop:>9,.0f}:  gain = {closed:9.5f}   formula = {formula:9.5f}   ideal -R2/R1 = -10")

    print("\n=== Thevenin resistance of a follower, found with a test source (Rout = 100 Ohm) ===")
    for open_loop in (1.0, 10.0, 1e3, 1e5):
        r_th = follower_output_resistance(open_loop)
        print(f"  A = {open_loop:>9,.0f}:  test source gives Rth = {r_th:12.6f} Ohm,"
              f" Rout/(1+A) = {100 / (1 + open_loop):12.6f} Ohm")
    print("  'Turning off' E1 instead would give 100 Ohm for every A: wrong, the source reacts to the test current.")


if __name__ == "__main__":
    main()
