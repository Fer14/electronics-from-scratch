import math

import numpy as np

COLOR_DIGITS = {
    "black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4,
    "green": 5, "blue": 6, "violet": 7, "grey": 8, "white": 9,
}
MULTIPLIER_EXTRA = {"gold": -1, "silver": -2}
TOLERANCE_PERCENT = {
    "brown": 1.0, "red": 2.0, "green": 0.5, "blue": 0.25, "violet": 0.1,
    "grey": 0.05, "gold": 5.0, "silver": 10.0, "none": 20.0,
}

E6 = [1.0, 1.5, 2.2, 3.3, 4.7, 6.8]
E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
       3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]


def multiplier_power(color):
    if color in MULTIPLIER_EXTRA:
        return MULTIPLIER_EXTRA[color]
    return COLOR_DIGITS[color]


def decode_bands(bands):
    *digit_bands, multiplier_band, tolerance_band = bands
    digits = 0
    for color in digit_bands:
        digits = digits * 10 + COLOR_DIGITS[color]
    ohms = digits * 10 ** multiplier_power(multiplier_band)
    return ohms, TOLERANCE_PERCENT[tolerance_band]


def encode_bands(ohms, significant_digits=2, tolerance_band="gold"):
    power = math.floor(math.log10(ohms)) - (significant_digits - 1)
    digits = round(ohms / 10**power)
    if digits >= 10**significant_digits:
        digits //= 10
        power += 1
    color_by_digit = {value: name for name, value in COLOR_DIGITS.items()}
    color_by_power = {**color_by_digit, -1: "gold", -2: "silver"}
    digit_colors = [color_by_digit[int(c)] for c in str(digits)]
    return digit_colors + [color_by_power[power], tolerance_band]


def format_ohms(ohms):
    for limit, suffix in [(1e6, "M"), (1e3, "k")]:
        if ohms >= limit:
            text = f"{ohms / limit:g}"
            return text.replace(".", suffix) if "." in text else text + suffix
    text = f"{ohms:g}"
    return text.replace(".", "R") if "." in text else text + "R"


def decode_smd(code):
    if "R" in code:
        return float(code.replace("R", "."))
    return int(code[:-1]) * 10 ** int(code[-1])


def series_values(series, decades=(1, 10, 100, 1000, 10000, 100000)):
    return np.array([value * decade for decade in decades for value in series])


def nearest_standard(target_ohms, series=E12):
    values = series_values(series, decades=(0.1, 1, 10, 100, 1000, 10000, 100000, 1000000))
    ratios = np.abs(np.log(values / target_ohms))
    return float(values[np.argmin(ratios)])


print("Step 1: decode color bands")
examples = [
    ["brown", "black", "red", "gold"],
    ["yellow", "violet", "red", "gold"],
    ["red", "red", "brown", "gold"],
    ["orange", "orange", "gold", "silver"],
    ["brown", "black", "black", "brown", "brown"],
    ["yellow", "violet", "black", "brown", "brown"],
]
for bands in examples:
    ohms, tolerance = decode_bands(bands)
    low, high = ohms * (1 - tolerance / 100), ohms * (1 + tolerance / 100)
    print(f"  {'-'.join(bands):36s} -> {ohms:>10,.1f} ohm ({format_ohms(ohms):>4s})  +/-{tolerance:g}%  "
          f"[{low:,.1f} .. {high:,.1f}]")

print()
print("Step 2: encode values as bands (4-band, 5% gold)")
for ohms in [10, 220, 470, 1000, 4700, 10000, 47000, 1000000, 3.3]:
    print(f"  {format_ohms(ohms):>5s} -> {'-'.join(encode_bands(ohms))}")

print()
print("Step 3: SMD codes printed on tiny surface-mount resistors")
for code in ["103", "472", "221", "1002", "4R7", "000"]:
    print(f"  '{code}' -> {decode_smd(code):,} ohm")

print()
print("Step 4: the E-series are geometric")
for name, series in [("E6", E6), ("E12", E12), ("E24", E24)]:
    count = len(series)
    ideal = [round(10 ** (k / count), 2) for k in range(count)]
    print(f"  {name:3s} step = 10^(1/{count}) = {10 ** (1 / count):.3f}")
    print(f"      ideal : {ideal}")
    print(f"      real  : {series}")
ratios = np.array(E12[1:] + [10.0]) / np.array(E12)
print(f"  E12 neighbour ratios: {np.round(ratios, 3).tolist()}")

print()
print("Step 5: why 10% parts come in 12 values per decade")
for name, series, tolerance in [("E6", E6, 20), ("E12", E12, 10), ("E24", E24, 5)]:
    values = np.array(series + [10.0])
    upper_edges = values[:-1] * (1 + tolerance / 100)
    lower_edges = values[1:] * (1 - tolerance / 100)
    gaps_percent = (lower_edges - upper_edges) / values[:-1] * 100
    worst = int(np.argmax(gaps_percent))
    print(f"  {name:3s} with +/-{tolerance:2d}%: worst gap between neighbours {max(gaps_percent.max(), 0):4.1f}% "
          f"(between {values[worst]:g} and {values[worst + 1]:g}); "
          f"{int(np.sum(gaps_percent <= 1e-9))} of {len(series)} neighbour pairs touch or overlap")

print()
print("Step 6: pick the nearest E12 value for a calculated resistance")
for supply, target_ma in [(9.0, 9.0), (12.0, 2.5), (5.0, 10.0), (3.3, 1.0), (24.0, 15.0)]:
    exact = supply / (target_ma / 1000)
    chosen = nearest_standard(exact)
    actual_ma = supply / chosen * 1000
    print(f"  {supply:4.1f} V for {target_ma:4.1f} mA: exact {exact:7,.0f} ohm -> E12 {format_ohms(chosen):>4s} "
          f"({'-'.join(encode_bands(chosen))}) gives {actual_ma:5.2f} mA")
