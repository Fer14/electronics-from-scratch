from sim import Circuit

ZENER_VOLTS = 5.1
SERIES_OHMS = 220.0


def zener_curve(reverse_volts, dynamic_ohms=0.0):
    circuit = Circuit()
    circuit.voltage_source("V1", "k", "0", reverse_volts)
    circuit.zener("Z1", "0", "k", vz=ZENER_VOLTS, rs=dynamic_ohms)
    result = circuit.dc()
    return -result.i("Z1")


def show_curve():
    print(f"Zener diode ({ZENER_VOLTS} V), reverse current as the reverse voltage rises")
    print(f"  {'reverse V':>9} {'ideal-ish':>12} {'with 10 ohm dynamic resistance':>32}")
    for volts in [1.0, 3.0, 4.5, 4.9, 5.0, 5.05, 5.1, 5.15, 5.2]:
        sharp = zener_curve(volts)
        soft = zener_curve(volts, 10.0)
        print(f"  {volts:>9.2f} {sharp * 1000:>9.4f} mA {soft * 1000:>29.4f} mA")
    print()


def regulator(input_volts, load_ohms, series_ohms=SERIES_OHMS, dynamic_ohms=0.0):
    circuit = Circuit()
    circuit.voltage_source("V1", "in", "0", input_volts)
    circuit.resistor("RS", "in", "out", series_ohms)
    circuit.zener("Z1", "0", "out", vz=ZENER_VOLTS, rs=dynamic_ohms)
    if load_ohms is not None:
        circuit.resistor("RL", "out", "0", load_ohms)
    return circuit.dc()


def describe(result, has_load):
    out = result.v("out")
    series = result.i("RS")
    zener = -result.i("Z1")
    load = result.i("RL") if has_load else 0.0
    return out, series, zener, load, result.p("Z1"), result.p("RS")


def show_design():
    low, high, max_load, min_zener = 10.0, 14.0, 0.020, 0.002
    worst = (low - ZENER_VOLTS) / (max_load + min_zener)
    print("Design: input 10-14 V, output 5.1 V, load 0-20 mA, keep at least 2 mA in the zener")
    print(f"  R_S <= (V_in,min - V_Z) / (I_load,max + I_Z,min) = ({low} - {ZENER_VOLTS}) / {max_load + min_zener} = {worst:.1f} ohm  -> pick {SERIES_OHMS:.0f} ohm")
    no_load_current = (high - ZENER_VOLTS) / SERIES_OHMS
    print(f"  worst zener power: 14 V in, no load: I = {no_load_current * 1000:.1f} mA, P = {no_load_current * ZENER_VOLTS * 1000:.0f} mW")
    print(f"  worst resistor power: P = {(high - ZENER_VOLTS) ** 2 / SERIES_OHMS * 1000:.0f} mW")
    print()


def show_load_regulation():
    print("Load regulation at 12 V input (R_S = 220 ohm)")
    print(f"  {'load':>9} {'V_out':>8} {'I_RS':>9} {'I_zener':>9} {'I_load':>9} {'P_zener':>9}")
    for load in [None, 2000.0, 500.0, 255.0, 200.0, 150.0, 100.0]:
        out, series, zener, load_current, zener_power, _ = describe(regulator(12.0, load), load is not None)
        label = "none" if load is None else f"{load:.0f} ohm"
        print(f"  {label:>9} {out:>7.3f}V {series * 1000:>7.2f}mA {zener * 1000:>7.2f}mA {load_current * 1000:>7.2f}mA {zener_power * 1000:>7.1f}mW")
    print("  Below about 200 ohm the load wants more than the resistor can deliver: the zener lets go and V_out falls.")
    print()


def show_line_regulation():
    print("Line regulation with a 500 ohm load (about 10 mA)")
    for dynamic in [0.0, 10.0]:
        outputs = [regulator(volts, 500.0, dynamic_ohms=dynamic).v("out") for volts in [10.0, 12.0, 14.0]]
        change = (outputs[-1] - outputs[0]) * 1000
        print(f"  dynamic resistance {dynamic:>4.0f} ohm: V_out at 10/12/14 V = {outputs[0]:.3f} / {outputs[1]:.3f} / {outputs[2]:.3f} V   ({change:.1f} mV for 4 V of input change)")
    estimate = 4.0 * 10.0 / (10.0 + SERIES_OHMS) * 1000
    print(f"  estimate with r_z = 10 ohm: delta V_out = delta V_in x r_z / (r_z + R_S) = 4 x 10 / 230 = {estimate:.0f} mV")
    print()


def show_compare_divider():
    print("Why not just a voltage divider? 12 V -> 5.1 V with 220 ohm over 163 ohm")
    for load in [None, 1000.0, 500.0, 255.0]:
        circuit = Circuit()
        circuit.voltage_source("V1", "in", "0", 12.0)
        circuit.resistor("R1", "in", "out", 220.0)
        circuit.resistor("R2", "out", "0", 163.0)
        if load is not None:
            circuit.resistor("RL", "out", "0", load)
        divider = circuit.dc().v("out")
        zener = regulator(12.0, load).v("out")
        label = "none" if load is None else f"{load:.0f} ohm"
        print(f"  load {label:>9}: divider {divider:.3f} V   zener regulator {zener:.3f} V")
    print()


def main():
    show_curve()
    show_design()
    show_load_regulation()
    show_line_regulation()
    show_compare_divider()


if __name__ == "__main__":
    main()
