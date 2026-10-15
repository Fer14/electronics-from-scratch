from sim import Circuit

RAILS = (-12.0, 12.0)


def open_loop(differential_volts, gain=1e5):
    circuit = Circuit()
    circuit.voltage_source("VP", "p", "0", differential_volts)
    circuit.opamp("U1", plus="p", minus="0", out="out", gain=gain, rails=RAILS)
    return circuit.dc().v("out")


def show_open_loop():
    print("Open loop: output = A x (V+ - V-), A = 100,000, clipped by the +/-12 V rails")
    for microvolts in [-200.0, -100.0, -50.0, 0.0, 10.0, 50.0, 100.0, 200.0, 1000.0]:
        out = open_loop(microvolts * 1e-6)
        print(f"  V+ - V- = {microvolts:>7.0f} uV  ->  output {out:8.4f} V")
    print("  Only about +/-100 uV of input keeps the output away from the rails. Open loop, an op-amp is a comparator.")
    print()


def follower(source_volts, gain):
    circuit = Circuit()
    circuit.voltage_source("VS", "in", "0", source_volts)
    circuit.opamp("U1", plus="in", minus="out", out="out", gain=gain)
    return circuit.dc().v("out")


def show_follower():
    print("Voltage follower: output tied back to the minus input")
    print(f"  {'open-loop gain A':>17} {'output for 2.000 V in':>22} {'formula A/(1+A) x 2 V':>23} {'V+ - V-':>12}")
    for gain in [10.0, 100.0, 1e3, 1e5, 1e7]:
        out = follower(2.0, gain)
        print(f"  {gain:>17.0e} {out:>20.6f} V {2.0 * gain / (1 + gain):>21.6f} V {(2.0 - out) * 1e6:>9.2f} uV")
    print("  The bigger A, the closer V- gets to V+: the golden rule 'the inputs are equal' is a consequence of feedback.")
    print()


def divider_with_load(load_ohms, buffered):
    circuit = Circuit()
    circuit.voltage_source("VS", "vs", "0", 10.0)
    circuit.resistor("R1", "vs", "mid", 10e3)
    circuit.resistor("R2", "mid", "0", 10e3)
    if buffered:
        circuit.opamp("U1", plus="mid", minus="out", out="out", gain=1e5, rails=RAILS)
        circuit.resistor("RL", "out", "0", load_ohms)
    else:
        circuit.resistor("RL", "mid", "0", load_ohms)
    result = circuit.dc()
    node = "out" if buffered else "mid"
    return result.v(node), result.i("R1"), result


def show_buffer():
    print("A 10 k / 10 k divider from 10 V should give 5 V. Connect a load:")
    print(f"  {'load':>8} {'direct':>9} {'through a follower':>20} {'current drawn from divider':>28}")
    for load in [1e6, 100e3, 10e3, 1e3]:
        direct, _, _ = divider_with_load(load, False)
        buffered, divider_current, result = divider_with_load(load, True)
        print(f"  {load:>7.0f}  {direct:>7.3f} V {buffered:>18.4f} V {divider_current * 1000:>23.4f} mA")
    _, _, result = divider_with_load(1e3, True)
    print(f"  With the 1 k load the follower supplies {result.i('RL') * 1000:.3f} mA from its own output; the divider never notices.")
    print()


def show_input_current():
    circuit = Circuit()
    circuit.voltage_source("VS", "s", "0", 3.0)
    circuit.resistor("RS", "s", "in", 1e6)
    circuit.opamp("U1", plus="in", minus="out", out="out", gain=1e5)
    result = circuit.dc()
    print("Golden rule 2: no current flows into the inputs")
    print(f"  a 3 V source behind 1 Mohm into the follower: output {result.v('out'):.5f} V, current through 1 Mohm {result.i('RS') * 1e9:.4f} nA")


def main():
    show_open_loop()
    show_follower()
    show_buffer()
    show_input_current()


if __name__ == "__main__":
    main()
