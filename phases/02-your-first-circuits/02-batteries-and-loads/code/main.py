import numpy as np


def stack_voltage(cell_volts, cells_in_series):
    return cell_volts * cells_in_series


def hot_resistance(rated_volts, rated_amps):
    return rated_volts / rated_amps


def verdict(power_ratio):
    if power_ratio < 0.25:
        return "barely glows"
    if power_ratio < 0.8:
        return "dim"
    if power_ratio <= 1.2:
        return "about right"
    if power_ratio <= 2.0:
        return "overdriven, short life"
    return "burns out quickly"


def led_current(applied_volts, series_ohms, forward_drop=2.0):
    if applied_volts <= forward_drop:
        return 0.0
    return (applied_volts - forward_drop) / series_ohms


print("Step 1: making voltage by stacking cells in series")
cells = [
    ("alkaline AA", 1.5, 2),
    ("alkaline AA", 1.5, 4),
    ("NiMH rechargeable AA", 1.2, 4),
    ("lithium-ion cell", 3.7, 1),
    ("coin cell CR2032", 3.0, 1),
    ("inside a 9 V battery", 1.5, 6),
    ("lead-acid car cell", 2.1, 6),
]
for name, volts, count in cells:
    print(f"  {count} x {name:22s} {volts:.1f} V each -> {stack_voltage(volts, count):5.1f} V")

print()
print("Step 2: loads, their ratings and how they behave when hot")
loads = [
    ("flashlight bulb", 3.0, 0.3),
    ("lantern bulb", 6.0, 0.5),
    ("car side-light bulb", 12.0, 0.42),
    ("small 12 V heater pad", 12.0, 2.0),
]
for name, volts, amps in loads:
    print(f"  {name:22s} rated {volts:5.1f} V {amps:5.2f} A -> {volts * amps:5.2f} W, behaves like {hot_resistance(volts, amps):6.1f} ohm")

print()
print("Step 3: matching the lantern bulb (6 V, 0.5 A, 12 ohm) to different batteries")
bulb_ohms = hot_resistance(6.0, 0.5)
rated_power = 6.0 * 0.5
battery_volts = np.array([1.5, 3.0, 6.0, 9.0, 12.0])
currents = battery_volts / bulb_ohms
powers = battery_volts * currents
for volts, amps, watts in zip(battery_volts, currents, powers):
    ratio = watts / rated_power
    print(f"  {volts:5.1f} V battery: {amps:5.3f} A, {watts:6.2f} W = {ratio:5.2f} x rated -> {verdict(ratio)}")

print()
print("Step 4: polarity matters for an LED (red, about 2.0 V drop, 150 ohm in series)")
supply = 5.0
for label, applied in [("battery the right way round", supply), ("battery reversed", -supply)]:
    amps = led_current(applied, 150.0)
    print(f"  {label:28s} LED current = {amps * 1000:5.1f} mA -> {'lit' if amps > 0 else 'dark'}")

print()
print("Step 5: how long does the battery last?")
budgets = [
    ("2 x AA (2500 mAh) + flashlight bulb", 2500.0, 3.0, 0.3),
    ("9 V battery (550 mAh) + red LED at 20 mA", 550.0, 9.0, 0.02),
    ("4 x AA (2500 mAh) + lantern bulb", 2500.0, 6.0, 0.5),
]
for label, capacity_mah, volts, amps in budgets:
    hours = capacity_mah / (amps * 1000.0)
    energy_wh = capacity_mah / 1000.0 * volts
    print(f"  {label:42s} {energy_wh:5.2f} Wh stored, about {hours:5.1f} h of use")
