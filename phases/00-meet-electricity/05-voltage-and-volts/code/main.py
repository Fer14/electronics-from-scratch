BATTERY_VOLTS = 9

LOOP = [
    ("battery -", 0),
    ("battery +", BATTERY_VOLTS),
    ("top wire, before the switch", BATTERY_VOLTS),
    ("top of the lamp", BATTERY_VOLTS),
    ("bottom of the lamp", 0),
    ("bottom wire, back to battery -", 0),
]

EVERYDAY_VOLTAGES = [
    ("one AA cell", "1.5 volts", "safe to handle"),
    ("a USB port", "5 volts", "safe to handle"),
    ("a square 9 V battery", "9 volts", "safe to handle, but never short it"),
    ("a car battery", "12 volts", "safe to touch, dangerous to short"),
    ("a wall socket", "230 volts (120 in North America)", "dangerous: never touch"),
]


def bar(volts):
    return "#" * (volts * 3)


def heights_from(reference_name, loop):
    zero = dict(loop)[reference_name]
    return [(name, level - zero) for name, level in loop]


print(f"=== a {BATTERY_VOLTS} V battery and a lamp: the height of each point above ground ===")
print("  ground = the battery's minus side, the point we agree to call zero")
for name, level in LOOP:
    print(f"  {name:<32} {level:>2} V  {bar(level)}")
print("  the battery lifts the charge up; the charge falls back down through the lamp")

print()
print("=== voltage is always between two points ===")
levels = dict(LOOP)
pairs = [("top of the lamp", "bottom of the lamp"), ("battery +", "top of the lamp"), ("battery +", "battery -")]
for high, low in pairs:
    print(f"  from {low} up to {high}: {levels[high] - levels[low]} V")
print("  along a plain wire the height does not change, so the voltage between its ends is zero")

print()
print("=== choosing a different zero ===")
for reference in ("battery -", "battery +"):
    print(f"  heights measured from '{reference}':")
    for name, level in heights_from(reference, LOOP[:2] + LOOP[3:5]):
        print(f"    {name:<22} {level:>3} V")
print("  the labels change, but the voltage across the lamp is the same either way")

print()
print("=== an open switch: no current, but the push is still there ===")
print(f"  across the open gap: {BATTERY_VOLTS} V    current: none")

print()
print("=== everyday voltages ===")
for source, size, note in EVERYDAY_VOLTAGES:
    print(f"  {source:<22} {size:<33} {note}")
