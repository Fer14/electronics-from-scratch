import numpy as np

ELECTRON_CHARGE = 1.602176634e-19
GRAVITY = 9.81
JOULES_PER_KWH = 3.6e6
WATER_HEAT_CAPACITY = 4186.0
PRICE_PER_KWH = 0.25


def power(volts, amps):
    return volts * amps


def energy(power_w, seconds):
    return power_w * seconds


def battery_energy_wh(volts, milliamp_hours):
    return volts * milliamp_hours / 1000.0


def print_what_a_joule_is():
    print("=== What one joule feels like ===")
    mass = 0.102
    height = 1.0
    work = mass * GRAVITY * height
    print(f"Lifting {mass * 1000:.0f} g by {height:.0f} m takes {work:.3f} J")
    print(f"A 1 W LED lamp uses 1 J every second, {energy(1.0, 3600):.0f} J every hour")
    print()


def print_power_from_definitions():
    print("=== P = V x I, from the units ===")
    print("volt = joule per coulomb, ampere = coulomb per second")
    print("volt x ampere = (J/C) x (C/s) = J/s = watt")
    devices = [
        ("LED on a 9 V battery", 9.0, 0.020),
        ("USB phone charging", 5.0, 2.0),
        ("car headlight", 12.0, 4.6),
        ("laptop charger output", 20.0, 3.25),
        ("electric kettle", 230.0, 8.7),
    ]
    for label, volts, amps in devices:
        print(f"{label:24s} {volts:6.1f} V x {amps:6.3f} A = {power(volts, amps):8.2f} W")
    print()


def print_electron_bookkeeping():
    print("=== The same power, counted electron by electron ===")
    volts = 9.0
    amps = 0.020
    electrons_per_second = amps / ELECTRON_CHARGE
    energy_per_electron = volts * ELECTRON_CHARGE
    total = electrons_per_second * energy_per_electron
    print(f"Electrons per second          = {electrons_per_second:.3e}")
    print(f"Energy given up per electron  = {energy_per_electron:.3e} J  ({volts:.0f} eV)")
    print(f"Product                       = {total:.3f} W")
    print(f"V x I directly                = {power(volts, amps):.3f} W")
    print()


def print_electricity_bill():
    print("=== A month of household electricity ===")
    appliances = [
        ("fridge (average draw)", 40.0, 24.0),
        ("LED lighting", 60.0, 5.0),
        ("laptop", 45.0, 6.0),
        ("television", 90.0, 3.0),
        ("electric kettle", 2000.0, 0.25),
        ("washing machine", 500.0, 1.0),
        ("router", 10.0, 24.0),
    ]
    days = 30
    names = [name for name, _, _ in appliances]
    watts = np.array([w for _, w, _ in appliances])
    hours_per_day = np.array([h for _, _, h in appliances])
    kwh = watts * hours_per_day * days / 1000.0
    cost = kwh * PRICE_PER_KWH
    for name, w, h, k, c in zip(names, watts, hours_per_day, kwh, cost):
        print(f"{name:22s} {w:7.0f} W x {h:5.2f} h/day x {days} days = {k:6.1f} kWh  -> {c:6.2f} EUR")
    print(f"Total: {kwh.sum():.1f} kWh = {kwh.sum() * JOULES_PER_KWH:.2e} J  -> {cost.sum():.2f} EUR at {PRICE_PER_KWH} EUR/kWh")
    print()


def print_batteries():
    print("=== Energy stored in batteries ===")
    batteries = [
        ("CR2032 coin cell", 3.0, 220.0),
        ("AA alkaline", 1.5, 2500.0),
        ("9 V block", 9.0, 500.0),
        ("phone Li-ion", 3.85, 4500.0),
        ("laptop pack", 11.4, 5000.0),
        ("car battery", 12.0, 60000.0),
    ]
    for label, volts, mah in batteries:
        wh = battery_energy_wh(volts, mah)
        print(f"{label:17s} {volts:5.2f} V x {mah:7.0f} mAh = {wh:7.2f} Wh = {wh * 3600:10.0f} J")
    print()


def print_runtime():
    print("=== How long will it last? ===")
    stored_wh = battery_energy_wh(9.0, 500.0)
    load_w = power(9.0, 0.020)
    hours = stored_wh / load_w
    print(f"9 V block ({stored_wh:.1f} Wh) feeding {load_w:.2f} W lasts about {hours:.0f} hours")
    phone_wh = battery_energy_wh(3.85, 4500.0)
    phone_average_w = 1.2
    print(f"Phone ({phone_wh:.2f} Wh) at {phone_average_w} W average lasts about {phone_wh / phone_average_w:.1f} hours")
    print()


def print_efficiency():
    print("=== Efficiency: where does the energy go? ===")
    cases = [
        ("incandescent bulb", 60.0, 0.02),
        ("LED bulb", 8.0, 0.15),
        ("phone charger", 12.0, 0.85),
        ("electric motor", 100.0, 0.80),
        ("electric heater", 1500.0, 1.00),
    ]
    for label, input_w, useful_fraction in cases:
        useful = input_w * useful_fraction
        wasted = input_w - useful
        print(f"{label:18s} in {input_w:7.1f} W  useful {useful:7.2f} W  wasted as heat {wasted:7.2f} W  efficiency {useful_fraction * 100:5.1f} %")
    print()


def print_kettle():
    print("=== Boiling water with a kettle ===")
    kettle_w = 2000.0
    litres = 1.0
    start_c = 20.0
    end_c = 100.0
    heat_needed = WATER_HEAT_CAPACITY * litres * (end_c - start_c)
    for efficiency in (1.0, 0.85):
        seconds = heat_needed / (kettle_w * efficiency)
        print(f"Efficiency {efficiency * 100:3.0f} %: {heat_needed:.0f} J needed, {seconds:.0f} s = {seconds / 60:.1f} min")
    print(f"Energy in kWh: {heat_needed / JOULES_PER_KWH:.3f} kWh, costing {heat_needed / JOULES_PER_KWH * PRICE_PER_KWH * 100:.1f} cents")
    print()


def main():
    print_what_a_joule_is()
    print_power_from_definitions()
    print_electron_bookkeeping()
    print_electricity_bill()
    print_batteries()
    print_runtime()
    print_efficiency()
    print_kettle()


if __name__ == "__main__":
    main()
