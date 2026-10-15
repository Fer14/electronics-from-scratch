from sim import Circuit

BETA = 100.0
SUPPLY = 5.0
PIN_HIGH = 3.3


def led_driver(base_ohms, pin_volts=PIN_HIGH, led_ohms=150.0):
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", SUPPLY)
    circuit.voltage_source("PIN", "pin", "0", pin_volts)
    circuit.resistor("RB", "pin", "b", base_ohms)
    circuit.resistor("RLED", "vcc", "a", led_ohms)
    circuit.led("D1", "a", "c", color="red")
    circuit.npn("Q1", c="c", b="b", e="0", beta=BETA)
    return circuit.dc()


def show_design():
    led_volts, saturation_volts, target = 1.85, 0.1, 0.020
    led_ohms = (SUPPLY - led_volts - saturation_volts) / target
    minimum_base = target / BETA
    overdriven_base = target / 10
    base_ohms = (PIN_HIGH - 0.7) / overdriven_base
    print("Design by hand: red LED at 20 mA from 5 V, switched by a 3.3 V pin")
    print(f"  R_LED = (5 - 1.85 - 0.1) / 0.020 = {led_ohms:.1f} ohm  -> use 150 ohm")
    print(f"  minimum base current = I_C / beta = {minimum_base * 1e3:.2f} mA; with a forced beta of 10: {overdriven_base * 1e3:.1f} mA")
    print(f"  R_B = (3.3 - 0.7) / {overdriven_base:.3f} = {base_ohms:.0f} ohm  -> use 1 kohm (2.6 mA, within a pin's limit)")
    print()


def show_sweep():
    print("Sweeping the base resistor (pin at 3.3 V)")
    print(f"  {'R_B':>8} {'I_B':>9} {'I_C':>9} {'V_CE':>7} {'I_C/I_B':>8} {'P transistor':>13} {'state':>12}")
    for base_ohms in [100.0, 330.0, 1000.0, 4700.0, 10000.0, 47000.0, 100000.0]:
        result = led_driver(base_ohms)
        base = result.i("Q1.b")
        collector = result.i("Q1")
        vce = result.v("c")
        state = "saturated" if vce < 0.3 else "active"
        print(f"  {base_ohms:>7.0f}  {base * 1000:>7.3f}mA {collector * 1000:>7.2f}mA {vce:>6.3f}V {collector / base:>8.1f} "
              f"{result.p('Q1') * 1000:>10.2f}mW {state:>12}")
    print()


def show_on_off():
    print("The same switch with the pin LOW (0 V) and HIGH (3.3 V), R_B = 1 kohm")
    for label, volts in [("LOW ", 0.0), ("HIGH", PIN_HIGH)]:
        result = led_driver(1000.0, pin_volts=volts)
        print(f"  pin {label}: LED current {result.i('D1') * 1000:8.4f} mA   V_CE {result.v('c'):5.3f} V   "
              f"transistor power {result.p('Q1') * 1000:6.2f} mW   pin current {result.i('RB') * 1000:6.3f} mA")
    print()


def show_beta_spread():
    print("Robustness: the same 1 kohm design with transistors of different beta")
    for beta in [50.0, 100.0, 300.0]:
        circuit = Circuit()
        circuit.voltage_source("VCC", "vcc", "0", SUPPLY)
        circuit.voltage_source("PIN", "pin", "0", PIN_HIGH)
        circuit.resistor("RB", "pin", "b", 1000.0)
        circuit.resistor("RLED", "vcc", "a", 150.0)
        circuit.led("D1", "a", "c", color="red")
        circuit.npn("Q1", c="c", b="b", e="0", beta=beta)
        result = circuit.dc()
        print(f"  beta {beta:>4.0f}: LED current {result.i('D1') * 1000:6.2f} mA, V_CE {result.v('c'):.3f} V")
    print("  Saturated switches do not care about beta; amplifiers do.")
    print()


def motor_turn_off():
    circuit = Circuit()
    circuit.voltage_source("VCC", "vcc", "0", 12.0)
    circuit.pulse_source("PIN", "pin", "0", low=0.0, high=PIN_HIGH, period=4e-3, duty=0.5)
    circuit.resistor("RB", "pin", "b", 220.0)
    circuit.resistor("RM", "vcc", "m", 60.0)
    circuit.inductor("LM", "m", "c", 10e-3, i0=0.0)
    circuit.npn("Q1", c="c", b="b", e="0", beta=BETA)
    unprotected = circuit.transient(t_stop=4e-3, dt=1e-6)
    circuit.diode("DF", "c", "vcc")
    protected = circuit.transient(t_stop=4e-3, dt=1e-6)
    print("Switching an inductive load (relay or motor coil: 60 ohm, 10 mH) from 12 V")
    print(f"  without flyback diode: collector peaks at {max(unprotected.v('c')):10.1f} V when the transistor turns off")
    print(f"  with flyback diode:    collector peaks at {max(protected.v('c')):10.2f} V (one diode drop above 12 V)")
    print("  (a real transistor would break down long before the unprotected value)")


def main():
    show_design()
    show_sweep()
    show_on_off()
    show_beta_spread()
    motor_turn_off()


if __name__ == "__main__":
    main()
