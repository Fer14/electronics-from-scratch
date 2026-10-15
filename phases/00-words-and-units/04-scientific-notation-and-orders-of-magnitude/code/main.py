import math

import numpy as np

ELEMENTARY_CHARGE = 1.602176634e-19

ENGINEERING_PREFIXES = {
    -15: "f",
    -12: "p",
    -9: "n",
    -6: "µ",
    -3: "m",
    0: "",
    3: "k",
    6: "M",
    9: "G",
    12: "T",
}


def split_scientific(value):
    if value == 0:
        return 0.0, 0
    exponent = math.floor(math.log10(abs(value)))
    mantissa = value / 10**exponent
    if abs(mantissa) >= 10:
        mantissa /= 10
        exponent += 1
    return mantissa, exponent


def split_engineering(value):
    if value == 0:
        return 0.0, 0
    mantissa, exponent = split_scientific(value)
    engineering_exponent = 3 * math.floor(exponent / 3)
    return value / 10**engineering_exponent, engineering_exponent


def with_prefix(value, unit, digits=3):
    mantissa, exponent = split_engineering(value)
    prefix = ENGINEERING_PREFIXES.get(exponent)
    if prefix is None:
        return f"{value:.{digits - 1}e} {unit}"
    return f"{mantissa:.{digits}g} {prefix}{unit}"


def multiply_scientific(first, second):
    m1, e1 = split_scientific(first)
    m2, e2 = split_scientific(second)
    raw_mantissa = m1 * m2
    raw_exponent = e1 + e2
    mantissa, shift = split_scientific(raw_mantissa)
    return raw_mantissa, raw_exponent, mantissa, raw_exponent + shift


def divide_scientific(top, bottom):
    m1, e1 = split_scientific(top)
    m2, e2 = split_scientific(bottom)
    raw_mantissa = m1 / m2
    raw_exponent = e1 - e2
    mantissa, shift = split_scientific(raw_mantissa)
    return raw_mantissa, raw_exponent, mantissa, raw_exponent + shift


def order_of_magnitude(value):
    return round(math.log10(abs(value)))


def show_notations():
    print("=== 1. Three ways to write the same number ===")
    samples = [
        ("LED current", 0.020, "A"),
        ("quartz watch current", 0.0000015, "A"),
        ("pull-up resistor", 47000.0, "Ω"),
        ("Wi-Fi frequency", 2_400_000_000.0, "Hz"),
        ("charge of one electron", ELEMENTARY_CHARGE, "C"),
    ]
    for name, value, unit in samples:
        m_sci, e_sci = split_scientific(value)
        m_eng, e_eng = split_engineering(value)
        print(f"  {name}")
        print(f"    plain decimal : {value:.12g} {unit}")
        print(f"    scientific    : {m_sci:.4g} x 10^{e_sci} {unit}")
        print(f"    engineering   : {m_eng:.4g} x 10^{e_eng} {unit}  ->  {with_prefix(value, unit)}")
    print()


def show_arithmetic():
    print("=== 2. Multiplying and dividing in scientific notation ===")
    current = 0.015
    resistance = 680.0
    raw_m, raw_e, m, e = multiply_scientific(current, resistance)
    print("  Voltage across a 680 Ω resistor carrying 15 mA (preview: V = I x R)")
    print(f"    (1.5 x 10^-2 A) x (6.8 x 10^2 Ω) = {raw_m:.4g} x 10^{raw_e} = {m:.4g} x 10^{e} V")
    print(f"    check with plain floats: {current * resistance:.4g} V")

    charge_per_second = 0.001
    raw_m, raw_e, m, e = divide_scientific(charge_per_second, ELEMENTARY_CHARGE)
    print("  Electrons per second in a 1 mA current")
    print(f"    (1 x 10^-3 C/s) / (1.602 x 10^-19 C) = {raw_m:.4g} x 10^{raw_e} = {m:.4g} x 10^{e} electrons/s")
    print(f"    check with plain floats: {charge_per_second / ELEMENTARY_CHARGE:.4e} electrons/s")

    energy = 3.7 * 3.0
    seconds_in_hour = 3600.0
    raw_m, raw_e, m, e = multiply_scientific(energy, seconds_in_hour)
    print("  Energy in a 3.7 V, 3 Ah phone battery (preview: Wh x 3600 = J)")
    print(f"    (1.11 x 10^1 Wh) x (3.6 x 10^3 s/h) = {raw_m:.4g} x 10^{raw_e} = {m:.4g} x 10^{e} J")
    print()


def show_ladder(title, unit, entries):
    print(f"=== {title} ===")
    values = np.array([value for _, value in entries])
    exponents = np.log10(values)
    for (name, value), exponent in zip(entries, exponents):
        bar = "#" * int(round(exponent - exponents.min())) + "#"
        print(f"  {name:<34} {with_prefix(value, unit):>12}   10^{order_of_magnitude(value):>3}  {bar}")
    span = exponents.max() - exponents.min()
    print(f"  span: about {span:.0f} orders of magnitude (largest / smallest = {values.max() / values.min():.1e})")
    print()


def show_ladders():
    currents = [
        ("leakage of a good capacitor", 1e-9),
        ("quartz wristwatch", 1.5e-6),
        ("TV remote, idle", 2e-6),
        ("red indicator LED", 0.010),
        ("phone charging (USB)", 2.0),
        ("electric kettle (230 V)", 9.0),
        ("car starter motor", 200.0),
        ("lightning stroke (typical)", 30000.0),
    ]
    show_ladder("3a. Currents in the world", "A", currents)
    voltages = [
        ("nerve signal inside a cell", 0.07),
        ("silicon diode drop", 0.65),
        ("AA cell", 1.5),
        ("USB port", 5.0),
        ("car battery", 12.0),
        ("European mains outlet", 230.0),
        ("long-distance power line", 400000.0),
        ("lightning cloud to ground", 1e8),
    ]
    show_ladder("3b. Voltages in the world", "V", voltages)
    resistances = [
        ("1 m of thick copper cable", 0.005),
        ("hot filament of a 6 V lamp", 30.0),
        ("human body, wet hands", 1000.0),
        ("typical breadboard resistor", 10000.0),
        ("human body, dry skin", 100000.0),
        ("multimeter input", 1e7),
        ("glass insulator", 1e12),
    ]
    show_ladder("3c. Resistances in the world", "Ω", resistances)


def show_fermi():
    print("=== 4. A Fermi estimate: electrons through a phone cable in one night ===")
    charging_current = 1.0
    charging_hours = 8.0
    seconds = charging_hours * 3600.0
    total_charge = charging_current * seconds
    electrons = total_charge / ELEMENTARY_CHARGE
    rough_seconds = 3e4
    rough_electrons = 1.0 * rough_seconds / 1.6e-19
    print(f"  current ~ {charging_current:g} A, time ~ {charging_hours:g} h = {seconds:.3g} s")
    print(f"  charge  = current x time = {total_charge:.3g} C")
    print(f"  electrons = {total_charge:.3g} C / {ELEMENTARY_CHARGE:.4g} C = {electrons:.2e}")
    print(f"  head-only version: 1 x 3 x 10^4 / 1.6 x 10^-19 = {rough_electrons:.1e}")
    print(f"  order of magnitude: 10^{order_of_magnitude(electrons)}")
    print()


def show_python_formatting():
    print("=== 5. Python float formatting ===")
    value = 0.000047
    print(f"  value = {value!r}")
    print(f"  f'{{value:e}}'    -> {value:e}")
    print(f"  f'{{value:.2e}}'  -> {value:.2e}")
    print(f"  f'{{value:.3g}}'  -> {value:.3g}")
    print(f"  f'{{value:.6f}}'  -> {value:.6f}")
    print(f"  with_prefix      -> {with_prefix(value, 'F')}")
    print(f"  4.7e3 == 4700    -> {4.7e3 == 4700}")
    print(f"  0.1 + 0.2        -> {0.1 + 0.2!r}")
    print(f"  math.isclose     -> {math.isclose(0.1 + 0.2, 0.3)}")
    print()


def main():
    show_notations()
    show_arithmetic()
    show_ladders()
    show_fermi()
    show_python_formatting()


if __name__ == "__main__":
    main()
