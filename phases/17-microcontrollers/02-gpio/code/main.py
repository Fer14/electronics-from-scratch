from sim import Circuit

VDD = 3.3
DRIVER_OHMS = 40.0
PULL_UP_OHMS = 35_000.0
INPUT_LEAK_OHMS = 100e6
VIL_FRACTION = 0.3
VIH_FRACTION = 0.6
PIN_CURRENT_LIMIT = 0.020


class GpioPort:
    def __init__(self, name):
        self.name = name
        self.ddr = 0
        self.port = 0
        self.pin_voltages = [0.0] * 8

    def write_ddr(self, value):
        self.ddr = value & 0xFF

    def write_port(self, value):
        self.port = value & 0xFF

    def bit(self, register, number):
        return (register >> number) & 1

    def mode(self, number):
        if self.bit(self.ddr, number):
            return "output-high" if self.bit(self.port, number) else "output-low"
        return "input-pullup" if self.bit(self.port, number) else "input-floating"

    def read_pin_register(self):
        value = 0
        for number in range(8):
            if logic_level(self.pin_voltages[number]) == 1:
                value |= 1 << number
        return value


def logic_level(volts):
    if volts <= VIL_FRACTION * VDD:
        return 0
    if volts >= VIH_FRACTION * VDD:
        return 1
    return None


def add_pin(circuit, port, number, node):
    mode = port.mode(number)
    if mode.startswith("output"):
        circuit.voltage_source(f"DRV{number}", f"drv{number}", "0", VDD if mode == "output-high" else 0.0)
        circuit.resistor(f"RDRV{number}", f"drv{number}", node, DRIVER_OHMS)
    elif mode == "input-pullup":
        circuit.resistor(f"RPU{number}", "vdd", node, PULL_UP_OHMS)
    circuit.resistor(f"RLEAK{number}", node, "0", INPUT_LEAK_OHMS)


def led_on_output(series_ohms):
    port = GpioPort("B")
    port.write_ddr(0b00000001)
    port.write_port(0b00000001)
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", VDD)
    add_pin(circuit, port, 0, "pb0")
    circuit.resistor("R1", "pb0", "a", series_ohms)
    circuit.led("D1", "a", "0", color="red")
    result = circuit.dc()
    return result.v("pb0"), result.i("D1")


def led_sinking(pin_high):
    port = GpioPort("B")
    port.write_ddr(0b00000010)
    port.write_port(0b00000010 if pin_high else 0)
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", VDD)
    add_pin(circuit, port, 1, "pb1")
    circuit.led("D1", "vdd", "k", color="red")
    circuit.resistor("R1", "k", "pb1", 220)
    result = circuit.dc()
    return result.v("pb1"), result.i("D1")


def button_with_pullup(pressed, pullup_enabled):
    port = GpioPort("D")
    port.write_ddr(0)
    port.write_port(0b00000100 if pullup_enabled else 0)
    circuit = Circuit()
    circuit.voltage_source("VDD", "vdd", "0", VDD)
    add_pin(circuit, port, 2, "pd2")
    circuit.switch("SW1", "pd2", "0", closed=pressed)
    result = circuit.dc()
    port.pin_voltages[2] = result.v("pd2")
    current = 0.0 if not pullup_enabled else result.i("RPU2")
    return port, result.v("pd2"), current


def main():
    print(f"Logic thresholds at VDD = {VDD} V: a 0 is below {VIL_FRACTION * VDD:.2f} V, "
          f"a 1 is above {VIH_FRACTION * VDD:.2f} V, in between is undefined")
    for volts in [0.2, 0.9, 1.6, 2.1, 3.3]:
        level = logic_level(volts)
        print(f"  {volts:.1f} V reads as {'undefined' if level is None else level}")

    print(f"\nLED on PB0 (sourcing), driver resistance {DRIVER_OHMS:.0f} ohm")
    print(f"  {'series R':>9s}  {'pin volts':>9s}  {'LED mA':>7s}  verdict")
    for ohms in [1, 47, 100, 220, 470, 1000, 4700]:
        pin_volts, current = led_on_output(ohms)
        verdict = "too much for the pin" if current > PIN_CURRENT_LIMIT else ("dim" if current < 0.001 else "fine")
        print(f"  {ohms:7d} ohm  {pin_volts:7.3f} V  {current * 1e3:7.2f}  {verdict}")

    print("\nLED from VDD into PB1 (sinking, 220 ohm): the LED lights when the pin is LOW")
    for pin_high in [True, False]:
        pin_volts, current = led_sinking(pin_high)
        print(f"  PORTB bit1 = {int(pin_high)}  pin = {pin_volts:.3f} V  LED current = {current * 1e3:.2f} mA")

    print(f"\nButton from PD2 to ground, internal pull-up {PULL_UP_OHMS / 1e3:.0f} kohm")
    for pullup_enabled in [True, False]:
        for pressed in [False, True]:
            port, volts, current = button_with_pullup(pressed, pullup_enabled)
            level = logic_level(volts)
            pin_register = port.read_pin_register()
            print(f"  pull-up {'on ' if pullup_enabled else 'off'}  button {'pressed ' if pressed else 'released'}  "
                  f"pin = {volts:.3f} V  reads {'undefined' if level is None else level}  "
                  f"PIND = {pin_register:08b}  pull-up current = {current * 1e6:.1f} uA")
    print("\nWithout the pull-up, a released button leaves the pin tied to nothing but leakage:")
    print("in a real chip that voltage drifts with noise and touch, so the reading is random.")


if __name__ == "__main__":
    main()
