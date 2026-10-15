import numpy as np


def series_bulbs(battery_volts, bulb_ohms, count, internal_ohms=0.0):
    current = battery_volts / (internal_ohms + bulb_ohms * count)
    volts_each = current * bulb_ohms
    return current, volts_each, current * volts_each, current


def parallel_bulbs(battery_volts, bulb_ohms, count, internal_ohms=0.0):
    combined_ohms = bulb_ohms / count
    battery_current = battery_volts / (internal_ohms + combined_ohms)
    volts_each = battery_current * combined_ohms
    current_each = volts_each / bulb_ohms
    return current_each, volts_each, current_each * volts_each, battery_current


battery_volts = 6.0
bulb_ohms = 12.0
rated_power = 3.0

print("Step 1: identical 6 V 0.5 A bulbs (12 ohm hot) in SERIES on a 6 V battery")
for count in range(1, 5):
    amps, volts, watts, battery_amps = series_bulbs(battery_volts, bulb_ohms, count)
    print(f"  {count} bulb(s): {amps:.3f} A through each, {volts:.2f} V each, {watts:.3f} W each = {watts / rated_power:5.3f} x rated, battery gives {battery_amps:.3f} A")

print()
print("Step 2: the same bulbs in PARALLEL")
for count in range(1, 5):
    amps, volts, watts, battery_amps = parallel_bulbs(battery_volts, bulb_ohms, count)
    print(f"  {count} bulb(s): {amps:.3f} A through each, {volts:.2f} V each, {watts:.3f} W each = {watts / rated_power:5.3f} x rated, battery gives {battery_amps:.3f} A")

print()
print("Step 3: one of three bulbs burns out")
working = np.array([True, False, True])
series_current = battery_volts / (bulb_ohms * 3) if working.all() else 0.0
print(f"  series:   every bulb carries {series_current:.3f} A -> all three dark")
parallel_currents = np.where(working, battery_volts / bulb_ohms, 0.0)
for index, amps in enumerate(parallel_currents, start=1):
    print(f"  parallel: bulb {index} carries {amps:.3f} A -> {'lit' if amps > 0 else 'dark'}")
print(f"  parallel: battery gives {parallel_currents.sum():.3f} A")

print()
print("Step 4: a real battery (0.2 ohm inside) and more bulbs in parallel")
for count in range(1, 6):
    amps, volts, watts, battery_amps = parallel_bulbs(battery_volts, bulb_ohms, count, internal_ohms=0.2)
    print(f"  {count} bulb(s): {volts:.3f} V each, {amps:.3f} A each, battery gives {battery_amps:.3f} A")
amps, volts, watts, battery_amps = series_bulbs(battery_volts, bulb_ohms, 2, internal_ohms=0.2)
print(f"  2 bulbs in series for comparison: {amps:.3f} A each, {volts:.3f} V each")

print()
print("Step 5: battery life, 4 x AA (2500 mAh)")
for label, battery_amps in [("1 bulb", 0.5), ("2 in series", 0.25), ("2 in parallel", 1.0)]:
    print(f"  {label:14s} battery current {battery_amps:.2f} A -> about {2500.0 / (battery_amps * 1000.0):.1f} h")

print()
print("Step 6: a string of 50 mini bulbs (2.5 V, 0.17 A) in series on 120 V")
mini_ohms = 2.5 / 0.17
for count in [50, 49, 48]:
    amps = 120.0 / (mini_ohms * count)
    volts = amps * mini_ohms
    print(f"  {count} bulbs still in the loop: {amps:.4f} A, {volts:.3f} V per bulb, {amps * volts / (2.5 * 0.17):.3f} x rated power")

print()
print("Step 7: home wiring is parallel (230 V)")
appliances = [("kettle", 2200.0), ("lamp", 60.0), ("television", 100.0), ("fridge", 150.0)]
total = 0.0
for name, watts in appliances:
    amps = watts / 230.0
    total += amps
    print(f"  {name:10s} {watts:6.0f} W at 230 V -> {amps:5.2f} A, running total {total:5.2f} A")
