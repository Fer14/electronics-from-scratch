import numpy as np

from sim import Circuit

MOTOR_SUPPLY = 12.0
MOTOR_OHMS = 6.0
PARTS = {
    "logic-level (V_th 1.5 V)": {"vth": 1.5, "k": 5.0},
    "standard (V_th 3.5 V)": {"vth": 3.5, "k": 5.0},
}


def motor_switch(gate_volts, vth, k, gate_ohms=100.0, pulldown_ohms=100e3):
    circuit = Circuit()
    circuit.voltage_source("VM", "vm", "0", MOTOR_SUPPLY)
    circuit.voltage_source("PIN", "pin", "0", gate_volts)
    circuit.resistor("RG", "pin", "g", gate_ohms)
    circuit.resistor("RPD", "g", "0", pulldown_ohms)
    circuit.resistor("RM", "vm", "d", MOTOR_OHMS)
    circuit.nmos("M1", d="d", g="g", s="0", vth=vth, k=k)
    return circuit.dc()


def show_on_resistance():
    print("On-resistance R_DS(on) = 1 / (k (V_GS - V_th)) for two power MOSFETs (k = 5 A/V^2)")
    print(f"  {'V_GS':>5} " + "".join(f"{name:>28}" for name in PARTS))
    for vgs in [2.0, 3.3, 5.0, 10.0]:
        cells = []
        for params in PARTS.values():
            overdrive = vgs - params["vth"]
            cells.append(f"{1000 / (params['k'] * overdrive):>23.1f} mohm" if overdrive > 0 else f"{'off':>28}")
        print(f"  {vgs:>4.1f}V " + "".join(cells))
    print()


def show_motor():
    print(f"A {MOTOR_OHMS:.0f} ohm motor on {MOTOR_SUPPLY:.0f} V, switched from a microcontroller pin")
    print(f"  {'MOSFET':<26} {'pin':>5} {'V_GS':>6} {'motor I':>9} {'V_DS':>7} {'P MOSFET':>10} {'P motor':>9}")
    for name, params in PARTS.items():
        for pin in [3.3, 5.0, 10.0]:
            result = motor_switch(pin, **params)
            print(f"  {name:<26} {pin:>4.1f}V {result.v('g'):>5.2f}V {result.i('RM'):>7.3f} A {result.v('d'):>6.3f}V "
                  f"{result.p('M1'):>8.3f} W {result.p('RM'):>7.2f} W")
    print("  Only the logic-level part is fully on from 3.3 V. The standard part from 3.3 V is OFF; from 5 V it is half on and gets hot.")
    print()


def show_pulldown():
    params = PARTS["logic-level (V_th 1.5 V)"]
    print("Why the 100 kohm pull-down: a floating gate keeps whatever charge it last had")
    for label, gate_ohms in [("pin driving through 100 ohm", 100.0), ("pin through 100 kohm (a bad choice)", 100e3), ("pin through 1 Mohm (a worse one)", 1e6)]:
        result = motor_switch(3.3, gate_ohms=gate_ohms, **params)
        print(f"  {label:<36} V_GS = {result.v('g'):.2f} V   motor current {result.i('RM'):.3f} A   MOSFET power {result.p('M1'):.3f} W")
    print()


def show_gate_charging():
    params = PARTS["logic-level (V_th 1.5 V)"]
    print("The gate is a capacitor: turning on takes time. Gate capacitance 2 nF, pin steps 0 -> 3.3 V")
    for gate_ohms in [10.0, 100.0, 1000.0]:
        circuit = Circuit()
        circuit.voltage_source("VM", "vm", "0", MOTOR_SUPPLY)
        circuit.pulse_source("PIN", "pin", "0", low=0.0, high=3.3, period=20e-6, duty=0.5)
        circuit.resistor("RG", "pin", "g", gate_ohms)
        circuit.capacitor("CG", "g", "0", 2e-9)
        circuit.resistor("RM", "vm", "d", MOTOR_OHMS)
        circuit.nmos("M1", d="d", g="g", s="0", **params)
        result = circuit.transient(t_stop=10e-6, dt=5e-9)
        time = np.asarray(result.time)
        drain = np.asarray(result.v("d"))
        power = np.asarray(result.p("M1"))
        crossing = time[np.argmax(drain < 1.0)] if np.any(drain < 1.0) else float("nan")
        energy = float(np.sum(power[1:] * np.diff(time)))
        print(f"  R_G = {gate_ohms:>6.0f} ohm: tau = {gate_ohms * 2e-9 * 1e9:>6.0f} ns   drain falls below 1 V after {crossing * 1e9:>6.0f} ns   "
              f"switching energy {energy * 1e6:7.3f} uJ")
    print()


def show_flyback():
    params = PARTS["logic-level (V_th 1.5 V)"]
    results = {}
    for protected in [False, True]:
        circuit = Circuit()
        circuit.voltage_source("VM", "vm", "0", MOTOR_SUPPLY)
        circuit.pulse_source("PIN", "g", "0", low=0.0, high=3.3, period=2e-3, duty=0.5, rise=1e-6, fall=1e-6)
        circuit.resistor("RM", "vm", "x", MOTOR_OHMS)
        circuit.inductor("LM", "x", "d", 1e-3, i0=0.0)
        circuit.nmos("M1", d="d", g="g", s="0", **params)
        circuit.zener("ZAV", "0", "d", vz=60.0, nz=5.0)
        if protected:
            circuit.diode("DF", "d", "vm")
        results[protected] = circuit.transient(t_stop=2e-3, dt=5e-7)
    print("Motor winding (6 ohm + 1 mH) switched off after 1 ms; the MOSFET's body avalanches at 60 V")
    for protected, label in [(False, "without flyback diode"), (True, "with flyback diode   ")]:
        result = results[protected]
        time = np.asarray(result.time)
        avalanche = np.asarray(result.p("ZAV"))
        energy = float(np.sum(avalanche[1:] * np.diff(time)))
        print(f"  {label}: drain peaks at {max(result.v('d')):6.2f} V, energy dumped into the MOSFET's avalanche {energy * 1000:6.3f} mJ")
    peak_current = float(np.max(np.asarray(results[False].i("LM"))))
    print(f"  energy stored in the winding at turn-off: 0.5 L I^2 = 0.5 x 1e-3 x {peak_current:.3f}^2 = {0.5e-3 * peak_current**2 * 1000:.3f} mJ")
    print("  (the supply keeps pushing current while the winding empties, so the avalanche absorbs a little more)")


def main():
    show_on_resistance()
    show_motor()
    show_pulldown()
    show_gate_charging()
    show_flyback()


if __name__ == "__main__":
    main()
