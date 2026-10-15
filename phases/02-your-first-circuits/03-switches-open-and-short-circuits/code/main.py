CLOSED_SWITCH_OHMS = 0.01
OPEN_SWITCH_OHMS = 1e12


def series_loop(battery_volts, internal_ohms, part_ohms):
    total_ohms = internal_ohms + sum(part_ohms.values())
    current = battery_volts / total_ohms
    drops = {name: current * ohms for name, ohms in part_ohms.items()}
    return current, drops


def parallel(first_ohms, second_ohms):
    return 1.0 / (1.0 / first_ohms + 1.0 / second_ohms)


battery_volts = 9.0
internal_ohms = 1.5
lamp_ohms = 30.0

print("Step 1: the two states of a switch in a 9 V lamp loop")
print(f"  battery {battery_volts:.1f} V with {internal_ohms:.1f} ohm inside, lamp {lamp_ohms:.0f} ohm when hot")
for state, switch_ohms in [("closed", CLOSED_SWITCH_OHMS), ("open", OPEN_SWITCH_OHMS)]:
    current, drops = series_loop(battery_volts, internal_ohms, {"switch": switch_ohms, "lamp": lamp_ohms})
    print(f"  switch {state:6s}: current = {current:.3e} A, across switch = {drops['switch']:6.3f} V, across lamp = {drops['lamp']:6.3f} V")

print()
print("Step 2: a wire dropped across the lamp (a short circuit)")
wire_ohms = 0.01
shorted_ohms = parallel(lamp_ohms, wire_ohms)
current, drops = series_loop(battery_volts, internal_ohms, {"switch": CLOSED_SWITCH_OHMS, "lamp with wire across": shorted_ohms})
lamp_volts = drops["lamp with wire across"]
print(f"  lamp and wire together behave like {shorted_ohms:.4f} ohm")
print(f"  current from battery = {current:.2f} A")
print(f"  voltage across the lamp = {lamp_volts:.3f} V, lamp current = {lamp_volts / lamp_ohms * 1000:.2f} mA (dark)")
print(f"  heat inside the battery = {current ** 2 * internal_ohms:.1f} W, heat in the wire = {lamp_volts ** 2 / wire_ohms:.2f} W")

print()
print("Step 3: a 0.01 ohm wire straight across different batteries")
batteries = [
    ("CR2032 coin cell", 3.0, 15.0),
    ("9 V alkaline", 9.0, 1.5),
    ("AA alkaline", 1.5, 0.15),
    ("18650 lithium-ion", 3.7, 0.03),
    ("12 V car battery", 12.6, 0.01),
]
for name, volts, ohms in batteries:
    short_current = volts / (ohms + CLOSED_SWITCH_OHMS)
    heat = short_current ** 2 * ohms
    print(f"  {name:18s} {volts:5.1f} V, {ohms:5.2f} ohm inside -> {short_current:8.1f} A, {heat:9.1f} W of heat inside")

print()
print("Step 4: a 1 A fuse in the loop")
fuse_rating = 1.0
fuse_melting_i2t = 0.5
for label, amps in [("normal (lamp on)", series_loop(battery_volts, internal_ohms, {"lamp": lamp_ohms})[0]), ("short across lamp", current)]:
    if amps <= fuse_rating:
        print(f"  {label:18s} {amps:5.2f} A -> fuse stays whole")
    else:
        print(f"  {label:18s} {amps:5.2f} A -> fuse melts in about {fuse_melting_i2t / amps ** 2 * 1000:.0f} ms, loop opens, current 0 A")

print()
print("Step 5: open versus short, side by side")
for label, gap_ohms in [("open (gap)", OPEN_SWITCH_OHMS), ("normal lamp", lamp_ohms), ("short (wire)", CLOSED_SWITCH_OHMS)]:
    amps = battery_volts / (internal_ohms + gap_ohms)
    volts = amps * gap_ohms
    watts = amps * volts
    print(f"  {label:12s} current {amps:9.3e} A   voltage across it {volts:6.3f} V   power in it {watts:7.3f} W")
