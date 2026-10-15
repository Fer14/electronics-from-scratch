supply = 12.0
node_voltages = {"gnd": 0.0, "vcc": 12.0, "a": 7.2, "b": 4.8}
branches = {
    "B1": ("battery", "vcc", "gnd", None),
    "R1": ("resistor", "vcc", "a", 1000.0),
    "R2": ("resistor", "a", "gnd", 3000.0),
    "R3": ("resistor", "a", "b", 1000.0),
    "R4": ("resistor", "b", "gnd", 2000.0),
}


def voltage_across(name, voltages):
    kind, plus_end, minus_end, ohms = branches[name]
    return voltages[plus_end] - voltages[minus_end]


def walk_loop(start, steps, voltages):
    position = start
    total_change = 0.0
    lines = []
    for name in steps:
        kind, end_a, end_b, ohms = branches[name]
        next_position = end_b if position == end_a else end_a
        change = voltages[next_position] - voltages[position]
        total_change += change
        word = "rise" if change > 0 else "drop"
        lines.append(f"    {position:>3} -> {next_position:<3} through {name}: {word} of {abs(change):5.2f} V")
        position = next_position
    return position, total_change, lines


def report_loop(title, start, steps, voltages):
    end, total, lines = walk_loop(start, steps, voltages)
    print(f"  {title}")
    for line in lines:
        print(line)
    print(f"    back at {end}: total change = {round(total, 12) + 0.0:+.3f} V")


print("Part 1: the height picture of one coulomb going round")
print("-----------------------------------------------------")
charge = 1.0
energy_from_battery = charge * supply
print(f"  the battery lifts {charge:.0f} C of charge by {supply:.0f} V, giving it {energy_from_battery:.0f} J of energy")
for name in ["R1", "R2"]:
    drop = voltage_across(name, node_voltages)
    print(f"  through {name} it falls {drop:.1f} V and gives {charge * drop:.1f} J to the resistor as heat")
left = energy_from_battery - charge * voltage_across("R1", node_voltages) - charge * voltage_across("R2", node_voltages)
print(f"  energy left when it is back at the battery's minus terminal: {left:.1f} J")
print()

print("Part 2: currents from Ohm's law, then KVL around every loop")
print("-----------------------------------------------------------")
for name, (kind, end_a, end_b, ohms) in branches.items():
    v = voltage_across(name, node_voltages)
    if ohms:
        print(f"  {name}: {v:5.2f} V across {ohms:6.0f} ohm -> {v / ohms * 1000:5.2f} mA from {end_a} to {end_b}")
    else:
        print(f"  {name}: battery, {v:5.2f} V from {end_a} (plus) to {end_b} (minus)")
print()
report_loop("left window: gnd -> B1 -> R1 -> R2 -> gnd", "gnd", ["B1", "R1", "R2"], node_voltages)
report_loop("right window: a -> R3 -> R4 -> R2 -> a", "a", ["R3", "R4", "R2"], node_voltages)
report_loop("outer loop: gnd -> B1 -> R1 -> R3 -> R4 -> gnd", "gnd", ["B1", "R1", "R3", "R4"], node_voltages)
report_loop("same right window, walked the other way", "a", ["R2", "R4", "R3"], node_voltages)
print()

print("Part 3: KVL catches a wrong meter reading")
print("------------------------------------------")
readings = {"R3": 2.4, "R4": 5.3, "R2": 7.2}
print("  a student measures each resistor of the right window with a voltmeter:")
for name, volts in readings.items():
    print(f"    across {name}: {volts:.1f} V")
loop_sum = -readings["R3"] - readings["R4"] + readings["R2"]
print(f"  walking a -> R3 -> b -> R4 -> gnd -> R2 -> a: -{readings['R3']:.1f} - {readings['R4']:.1f} + {readings['R2']:.1f} = {loop_sum:+.1f} V")
print("  the loop does not close to zero, so at least one reading is wrong (R4 is really 4.8 V)")
print()
print("  if instead we describe the circuit with node voltages, KVL can never fail:")
scrambled = {"gnd": 0.0, "vcc": 3.0, "a": -1.7, "b": 8.25}
report_loop("right window with made-up node voltages", "a", ["R3", "R4", "R2"], scrambled)
print("  every walk adds v(next) - v(here), and those terms cancel in pairs around any loop.")
print("  node voltages satisfy KVL automatically; what picks the right ones is KCL plus Ohm's law.")
print()

print("Part 4: use KVL to find the missing drop")
print("----------------------------------------")
battery = 9.0
known_drops = {"lamp": 3.2, "resistor": 4.1}
missing = battery - sum(known_drops.values())
print(f"  a {battery} V battery drives a lamp, a resistor and a motor in one loop")
for name, drop in known_drops.items():
    print(f"    {name:<9} drops {drop:.1f} V")
print(f"  KVL: rise = sum of drops -> motor drops {battery} - {' - '.join(f'{d:.1f}' for d in known_drops.values())} = {missing:.1f} V")
print()

print("Part 5: use KVL to choose a series resistor")
print("-------------------------------------------")
load_ohms = 1000.0
target_load_volts = 3.0
needed_drop = battery - target_load_volts
current = target_load_volts / load_ohms
ideal_series = needed_drop / current
print(f"  load {load_ohms:.0f} ohm should get {target_load_volts:.1f} V from {battery:.1f} V")
print(f"  KVL: the series resistor must drop {battery:.1f} - {target_load_volts:.1f} = {needed_drop:.1f} V")
print(f"  Ohm on the load: current = {target_load_volts:.1f} / {load_ohms:.0f} = {current * 1000:.1f} mA")
print(f"  Ohm on the series resistor: R = {needed_drop:.1f} / {current:.3f} = {ideal_series:.0f} ohm")
e12 = [1000, 1200, 1500, 1800, 2200, 2700, 3300, 3900, 4700]
print("  nearby standard (E12) values:")
for series in e12:
    load_volts = battery * load_ohms / (load_ohms + series)
    series_volts = battery - load_volts
    print(f"    {series:5d} ohm -> load {load_volts:4.2f} V + series {series_volts:4.2f} V = {load_volts + series_volts:.2f} V")
