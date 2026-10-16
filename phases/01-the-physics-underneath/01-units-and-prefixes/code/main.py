import re

import numpy as np

PREFIXES = {"p": 1e-12, "n": 1e-9, "u": 1e-6, "µ": 1e-6, "m": 1e-3, "": 1.0, "k": 1e3, "M": 1e6, "G": 1e9}
PREFIX_NAMES = [("p", "pico", -12), ("n", "nano", -9), ("µ", "micro", -6), ("m", "milli", -3),
                ("", "(none)", 0), ("k", "kilo", 3), ("M", "mega", 6), ("G", "giga", 9)]
UNITS = ["Hz", "Ah", "Wh", "V", "A", "Ω", "W", "J", "C", "F", "H", "s"]

BASE_ORDER = ["kg", "m", "s", "A"]
DIMENSIONS = {
    "s": np.array([0, 0, 1, 0]),
    "A": np.array([0, 0, 0, 1]),
    "N": np.array([1, 1, -2, 0]),
    "J": np.array([1, 2, -2, 0]),
    "W": np.array([1, 2, -3, 0]),
    "C": np.array([0, 0, 1, 1]),
    "V": np.array([1, 2, -3, -1]),
    "Ω": np.array([1, 2, -3, -2]),
    "F": np.array([-1, -2, 4, 2]),
    "H": np.array([1, 2, -2, -2]),
    "Hz": np.array([0, 0, -1, 0]),
}


def parse_quantity(text):
    match = re.fullmatch(r"\s*([0-9]*\.?[0-9]+)\s*(\S*)\s*", text)
    number, rest = float(match.group(1)), match.group(2)
    if rest in UNITS:
        return number, rest
    prefix, unit = rest[0], rest[1:]
    return number * PREFIXES[prefix], unit


def parse_resistor_code(code):
    for letter, multiplier in (("R", 1.0), ("k", 1e3), ("M", 1e6)):
        if letter in code:
            whole, fraction = code.split(letter)
            return float(f"{whole or 0}.{fraction or 0}") * multiplier
    return float(code)


def engineering(value, unit):
    if value == 0:
        return f"0 {unit}"
    exponent = int(np.floor(np.log10(abs(value)) / 3) * 3)
    exponent = max(-12, min(9, exponent))
    symbol = {-12: "p", -9: "n", -6: "µ", -3: "m", 0: "", 3: "k", 6: "M", 9: "G"}[exponent]
    return f"{value / 10 ** exponent:g} {symbol}{unit}"


def base_units(vector):
    parts = [f"{base}^{power}" for base, power in zip(BASE_ORDER, vector) if power != 0]
    return " ".join(parts) if parts else "no unit"


def dimension_name(vector):
    for name, dims in DIMENSIONS.items():
        if np.array_equal(dims, vector):
            return name
    return base_units(vector)


def combine(first, operator, second):
    if operator == "x":
        return DIMENSIONS[first] + DIMENSIONS[second]
    return DIMENSIONS[first] - DIMENSIONS[second]


def battery_summary(name, milliamp_hours, volts):
    amp_hours = milliamp_hours / 1000
    coulombs = amp_hours * 3600
    watt_hours = amp_hours * volts
    joules = watt_hours * 3600
    return name, amp_hours, coulombs, watt_hours, joules


print("Step 1: the prefixes")
for symbol, name, power in PREFIX_NAMES:
    print(f"  {symbol or '-':>2}  {name:<7} 10^{power:<4} = {10.0 ** power:g}")

print()
print("Step 2: converting labels into base units")
labels = ["4.7 kΩ", "20 mA", "100 nF", "330 Ω", "2.2 MΩ", "10 µH", "16 MHz", "3.3 V", "47 pF", "500 mW"]
for label in labels:
    value, unit = parse_quantity(label)
    base = f"{value:.12g} {unit}"
    print(f"  {label:>8} = {base:<14} = {engineering(value, unit)}")

print()
print("Step 3: the resistor shorthand where the letter is the decimal point")
for code in ["4k7", "2R2", "1M5", "470R", "10k", "0R1"]:
    ohms = parse_resistor_code(code)
    print(f"  {code:>5} -> {ohms:g} Ω -> {engineering(ohms, 'Ω')}")

print()
print("Step 4: arithmetic with prefixes")
volts = 5.0
ohms, _ = parse_quantity("4.7 kΩ")
amps = volts / ohms
print(f"  5 V / 4.7 kΩ = 5 / 4700 = {amps:.6f} A = {engineering(amps, 'A')}")
amps, _ = parse_quantity("20 mA")
watts = 3.3 * amps
print(f"  3.3 V x 20 mA = 3.3 x 0.02 = {watts:.3f} W = {engineering(watts, 'W')}")
resistance, _ = parse_quantity("10 kΩ")
capacitance, _ = parse_quantity("100 nF")
seconds = resistance * capacitance
print(f"  10 kΩ x 100 nF = 10000 x 0.0000001 = {seconds:.6f} s = {engineering(seconds, 's')}")

print()
print("Step 5: unit sanity checks in base units (kg, m, s, A)")
for name in ["J", "W", "C", "V", "Ω", "F", "H"]:
    print(f"  {name:>2} = {base_units(DIMENSIONS[name])}")
checks = [("V", "x", "A"), ("V", "/", "A"), ("A", "x", "s"), ("W", "x", "s"), ("V", "x", "C"),
          ("Ω", "x", "F"), ("H", "/", "Ω"), ("V", "/", "Ω"), ("C", "/", "V")]
for first, operator, second in checks:
    print(f"  {first} {operator} {second:<2} -> {dimension_name(combine(first, operator, second))}")
wrong = combine("V", "/", "A")
print(f"  someone writes power = V / I: units come out as {dimension_name(wrong)}, not W, so the formula is wrong")

print()
print("Step 6: batteries in mAh and Wh")
batteries = [
    battery_summary("AA rechargeable", 2500, 1.2),
    battery_summary("phone battery", 4000, 3.85),
    battery_summary("power bank", 20000, 3.7),
    battery_summary("CR2032 coin cell", 225, 3.0),
]
print(f"  {'battery':<18} {'Ah':>6} {'coulombs':>9} {'Wh':>7} {'joules':>9}")
for name, amp_hours, coulombs, watt_hours, joules in batteries:
    print(f"  {name:<18} {amp_hours:6.3f} {coulombs:9.0f} {watt_hours:7.2f} {joules:9.0f}")
led_amps = 0.020
print(f"  a 20 mA LED on the AA cell: 2500 mAh / 20 mA = {2.5 / led_amps:.0f} hours (ideal)")
print(f"  a 0.01 mA watch on the coin cell: 225 mAh / 0.01 mA = {225 / 0.01:.0f} hours = {225 / 0.01 / 24 / 365:.1f} years")
airline_limit = 100.0
power_bank_wh = batteries[2][3]
print(f"  power bank {power_bank_wh:.0f} Wh vs airline cabin limit {airline_limit:.0f} Wh: {'allowed' if power_bank_wh <= airline_limit else 'not allowed'}")
print("  mAh alone cannot compare an AA cell with a phone battery; Wh can, because it includes the voltage")
