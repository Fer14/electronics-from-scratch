import numpy as np

from sim import Circuit

VZ = 5.1


def zener_regulator(vin, series_ohms, load_ohms):
    circuit = Circuit()
    circuit.voltage_source("VIN", "vin", "0", vin)
    circuit.resistor("RS", "vin", "out", series_ohms)
    circuit.zener("Z1", "0", "out", vz=VZ)
    circuit.resistor("RL", "out", "0", load_ohms)
    result = circuit.dc()
    return {"vout": result.v("out"), "i_in": result.i("RS"), "i_zener": -result.i("Z1"),
            "i_load": result.i("RL"), "p_rs": result.p("RS"), "p_zener": result.p("Z1")}


def follower_regulator(vin, load_ohms):
    circuit = Circuit()
    circuit.voltage_source("VIN", "vin", "0", vin)
    circuit.resistor("RB", "vin", "ref", 1000)
    circuit.zener("Z1", "0", "ref", vz=5.6)
    circuit.npn("Q1", c="vin", b="ref", e="out", beta=100)
    circuit.resistor("RL", "out", "0", load_ohms)
    result = circuit.dc()
    return {"vout": result.v("out"), "i_load": result.i("RL"), "p_q": result.p("Q1"), "i_in": result.i("VIN")}


def feedback_regulator(vin, load_ohms, target=5.0, vref=2.5):
    top = 10_000 * (target / vref - 1)
    circuit = Circuit()
    circuit.voltage_source("VIN", "vin", "0", vin)
    circuit.voltage_source("VREF", "ref", "0", vref)
    circuit.opamp("U1", plus="ref", minus="fb", out="drive", gain=1e4, rails=(0.0, vin))
    circuit.resistor("RB", "drive", "b", 100)
    circuit.npn("Q1", c="vin", b="b", e="out", beta=100)
    circuit.resistor("R1", "out", "fb", top)
    circuit.resistor("R2", "fb", "0", 10_000)
    circuit.resistor("RL", "out", "0", load_ohms)
    soft_start = circuit.sweep("VREF", np.linspace(0.0, vref, 251))
    pick = lambda values: float(np.asarray(values)[-1])
    return {"vout": pick(soft_start.v("out")), "i_load": pick(soft_start.i("RL")),
            "p_q": pick(soft_start.p("Q1")), "i_in": pick(soft_start.i("VIN"))}


def main():
    print(f"Zener shunt regulator: 330 ohm from the input, {VZ} V zener, 1 kohm load")
    print(f"  {'Vin':>6s} {'Vout':>7s} {'I in':>8s} {'I zener':>8s} {'I load':>8s} {'P(RS)':>8s} {'P(zener)':>9s}")
    for vin in [7.0, 9.0, 12.0, 15.0]:
        r = zener_regulator(vin, 330, 1000)
        print(f"  {vin:4.1f} V {r['vout']:5.3f} V {r['i_in'] * 1e3:6.2f} mA {r['i_zener'] * 1e3:6.2f} mA "
              f"{r['i_load'] * 1e3:6.2f} mA {r['p_rs'] * 1e3:6.1f} mW {r['p_zener'] * 1e3:7.1f} mW")

    print("\nThe same zener regulator at 12 V with heavier and heavier loads")
    for load in [10_000, 1_000, 470, 220, 100]:
        r = zener_regulator(12.0, 330, load)
        state = "regulating" if r["i_zener"] > 1e-3 else "OUT OF REGULATION: the zener has no current left"
        print(f"  load {load:6d} ohm: Vout = {r['vout']:5.3f} V, load {r['i_load'] * 1e3:6.2f} mA, "
              f"zener {r['i_zener'] * 1e3:6.2f} mA  {state}")

    print("\nEmitter follower: zener sets the base, the transistor carries the load current")
    for load in [1_000, 100, 22, 10]:
        r = follower_regulator(12.0, load)
        print(f"  load {load:5d} ohm: Vout = {r['vout']:5.3f} V, load {r['i_load'] * 1e3:6.1f} mA, "
              f"transistor heat {r['p_q']:5.2f} W")

    print("\nOp-amp feedback regulator (2.5 V reference, divider sets 5.0 V)")
    for load in [1_000, 100, 22, 10]:
        r = feedback_regulator(12.0, load)
        efficiency = r["vout"] * r["i_load"] / (12.0 * r["i_in"])
        print(f"  load {load:5d} ohm: Vout = {r['vout']:6.4f} V, load {r['i_load'] * 1e3:6.1f} mA, "
              f"transistor heat {r['p_q']:5.2f} W, efficiency {efficiency * 100:5.1f}%")

    print("\nDropout: lowering the input with a 10 ohm load (500 mA)")
    for vin in [9.0, 7.0, 6.0, 5.8, 5.5, 5.2]:
        r = feedback_regulator(vin, 10)
        print(f"  Vin = {vin:4.1f} V: Vout = {r['vout']:6.4f} V  headroom {vin - r['vout']:5.3f} V")

    print("\nEfficiency of any linear regulator is at best Vout / Vin")
    for vin in [5.5, 7.0, 12.0, 24.0]:
        print(f"  {vin:4.1f} V -> 5 V at 1 A: efficiency {5 / vin * 100:5.1f}%, heat {(vin - 5) * 1.0:5.1f} W")


if __name__ == "__main__":
    main()
