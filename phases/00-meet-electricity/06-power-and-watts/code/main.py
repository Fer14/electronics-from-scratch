EVERYDAY_POWER = [
    ("a small LED indicator", "a tiny fraction of a watt"),
    ("a phone charging", "a few watts to a few tens of watts"),
    ("an LED room bulb", "around ten watts"),
    ("a laptop", "a few tens of watts"),
    ("a microwave oven", "around a thousand watts"),
    ("an electric kettle", "two to three thousand watts"),
]


def watts(volts, amps):
    return volts * amps


def energy_bar(power_units, hours):
    return "#" * (power_units * hours)


print("=== power: how fast energy is delivered ===")
volts, amps = 12, 2
print(f"  a {volts} V lamp drawing {amps} A")
print(f"  watts = volts x amps = {volts} x {amps} = {watts(volts, amps)} W")

print()
print("=== double the push or double the flow ===")
print(f"  {volts} V and {amps} A      -> {watts(volts, amps)} W")
print(f"  {2 * volts} V and {amps} A      -> {watts(2 * volts, amps)} W   (twice the push, twice the power)")
print(f"  {volts} V and {2 * amps} A      -> {watts(volts, 2 * amps)} W   (twice the flow, twice the power)")

print()
print("=== energy: power kept up over time ===")
print("  each # is one 'hour of a small lamp'")
for hours in (1, 2, 3):
    print(f"  small lamp on for {hours} hour(s): {energy_bar(1, hours)}")
print(f"  a lamp twice as powerful, on for 1 hour: {energy_bar(2, 1)}")
print("  the stronger lamp uses in 1 hour as much energy as the small lamp uses in 2 hours")

print()
print("=== how much power do everyday things use? ===")
for device, size in EVERYDAY_POWER:
    print(f"  {device:<24} {size}")
