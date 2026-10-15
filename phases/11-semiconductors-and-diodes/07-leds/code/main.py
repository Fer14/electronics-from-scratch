from sim import Circuit, LED_COLORS

PLANCK_TIMES_LIGHT_EV_NM = 1239.84
COLORS = ["infrared", "red", "yellow", "green", "blue", "white"]
TYPICAL_WAVELENGTH_NM = {"infrared": 940, "red": 630, "yellow": 590, "green": 525, "blue": 465}


def photon_energy_ev(wavelength_nm):
    return PLANCK_TIMES_LIGHT_EV_NM / wavelength_nm


def led_with_resistor(color, supply, ohms):
    circuit = Circuit()
    circuit.voltage_source("V1", "vcc", "0", supply)
    circuit.resistor("R1", "vcc", "a", ohms)
    circuit.led("D1", "a", "0", color=color)
    return circuit.dc()


def show_photons():
    print("Photon energy E = 1240 / wavelength(nm) eV, compared with the LED's forward voltage at 10 mA")
    for color, wavelength in TYPICAL_WAVELENGTH_NM.items():
        print(f"  {color:<9} {wavelength:>4} nm   photon {photon_energy_ev(wavelength):.2f} eV   forward voltage {LED_COLORS[color]:.2f} V")
    print()


def show_resistor_design(supply, target_amps):
    print(f"Designing the series resistor: {supply} V supply, target {target_amps * 1000:.0f} mA")
    print(f"  {'color':<9} {'V_F':>5} {'R = (Vs-VF)/I':>14} {'E12 pick':>9} {'sim I':>9} {'sim V_F':>8} {'P resistor':>11} {'P LED':>8}")
    for color in COLORS:
        forward = LED_COLORS[color]
        exact = (supply - forward) / target_amps
        pick = nearest_e12_above(exact)
        result = led_with_resistor(color, supply, pick)
        print(f"  {color:<9} {forward:>5.2f} {exact:>12.1f} ohm {pick:>7.0f} ohm {result.i('D1') * 1000:>7.2f} mA "
              f"{result.v('a'):>7.3f} V {result.p('R1') * 1000:>8.1f} mW {result.p('D1') * 1000:>6.1f} mW")
    print()


def nearest_e12_above(ohms):
    series = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
    decade = 1.0
    while decade * 10 <= ohms:
        decade *= 10
    for step in series + [10.0]:
        if step * decade >= ohms:
            return step * decade
    return 10.0 * decade


def show_no_resistor():
    print("What if you skip the resistor? Red LED straight across a supply (tiny 1 ohm wiring resistance)")
    for supply in [1.8, 2.0, 2.5, 3.0]:
        result = led_with_resistor("red", supply, 1.0)
        print(f"  supply {supply:.1f} V  ->  LED current {result.i('D1') * 1000:9.1f} mA")
    print("  A typical small LED is rated for 20-30 mA. Anything above about 2 V would destroy it.")
    print()


def show_supply_sensitivity():
    print("Why the resistor must take a good share of the voltage: red LED, current when the supply moves by 10 %")
    for label, supply_nominal, ohms in [("5 V with 330 ohm", 5.0, 330.0), ("2.2 V with 33 ohm", 2.2, 33.0)]:
        low = led_with_resistor("red", supply_nominal * 0.9, ohms).i("D1")
        mid = led_with_resistor("red", supply_nominal, ohms).i("D1")
        high = led_with_resistor("red", supply_nominal * 1.1, ohms).i("D1")
        print(f"  {label:<18} supply -10%: {low * 1000:6.2f} mA   nominal: {mid * 1000:6.2f} mA   +10%: {high * 1000:6.2f} mA")
    print()


def show_series_string():
    circuit = Circuit()
    circuit.voltage_source("V1", "vcc", "0", 12.0)
    circuit.resistor("R1", "vcc", "a", 330.0)
    circuit.led("D1", "a", "b", color="red")
    circuit.led("D2", "b", "c", color="red")
    circuit.led("D3", "c", "0", color="red")
    result = circuit.dc()
    print("Three red LEDs in series from 12 V through 330 ohm")
    print(f"  current {result.i('R1') * 1000:.2f} mA through all three; each LED {result.v('a', 'b'):.3f} V; resistor {result.p('R1') * 1000:.1f} mW")
    print()


def show_parallel_hogging():
    circuit = Circuit()
    circuit.voltage_source("V1", "vcc", "0", 5.0)
    circuit.resistor("R1", "vcc", "a", 150.0)
    circuit.led("D1", "a", "0", color="red")
    circuit.led("D2", "a", "0", color="orange")
    result = circuit.dc()
    print("Two LEDs in parallel sharing one 150 ohm resistor (red V_F 1.85 V, orange V_F 1.95 V)")
    print(f"  red gets {result.i('D1') * 1000:.2f} mA, orange gets {result.i('D2') * 1000:.2f} mA: a 0.1 V difference steals most of the current")
    print()


def main():
    show_photons()
    show_resistor_design(5.0, 0.010)
    show_no_resistor()
    show_supply_sensitivity()
    show_series_string()
    show_parallel_hogging()


if __name__ == "__main__":
    main()
