import numpy as np

ELEMENTARY_CHARGE = 1.602176634e-19


def find_closed_loop(connections, start, finish):
    neighbours = {}
    for first, second in connections:
        neighbours.setdefault(first, []).append(second)
        neighbours.setdefault(second, []).append(first)
    visited = {start: None}
    frontier = [start]
    while frontier:
        current = frontier.pop(0)
        for nxt in neighbours.get(current, []):
            if nxt not in visited:
                visited[nxt] = current
                frontier.append(nxt)
    if finish not in visited:
        return None
    path = [finish]
    while path[-1] != start:
        path.append(visited[path[-1]])
    return path[::-1]


def describe(name, connections):
    path = find_closed_loop(connections, "battery +", "battery -")
    print(f"  {name}")
    if path is None:
        print("    no path from battery + back to battery -: OPEN loop, no current")
    else:
        print("    closed loop: " + " -> ".join(path) + " -> (inside the battery) -> battery +")
    return path is not None


print("Step 1: is there a closed loop?")
flashlight = [
    ("battery +", "spring"),
    ("spring", "bulb tip"),
    ("bulb tip", "filament"),
    ("filament", "bulb side"),
    ("bulb side", "metal strip"),
    ("metal strip", "switch"),
    ("switch", "battery -"),
]
missing_return = [link for link in flashlight if link != ("metal strip", "switch")]
broken_filament = [link for link in flashlight if link != ("filament", "bulb side")]
one_wire_only = [("battery +", "spring"), ("spring", "bulb tip"), ("bulb tip", "filament")]
results = {}
for name, connections in [
    ("complete flashlight, switch on", flashlight),
    ("switch off (strip not touching switch)", missing_return),
    ("burnt-out bulb (filament broken)", broken_filament),
    ("only one wire to the bulb", one_wire_only),
]:
    results[name] = describe(name, connections)

print()
print("Step 2: how much current flows when the loop closes")
battery_volts = 3.0
bulb_ohms = 10.0
for name, closed in results.items():
    current = battery_volts / bulb_ohms if closed else 0.0
    print(f"  {name:42s} current = {current:.2f} A")

print()
print("Step 3: a ring of segments passing charge along")
current = battery_volts / bulb_ohms
segment_names = ["battery +", "spring", "bulb tip", "filament", "bulb side", "metal strip", "switch", "battery -"]
charge_in_segment = np.full(len(segment_names), 5.0)
passed_through = np.zeros(len(segment_names))
ticks = 10
charge_per_tick = current * 0.1
for _ in range(ticks):
    moving = np.full(len(segment_names), charge_per_tick)
    charge_in_segment = charge_in_segment - moving + np.roll(moving, 1)
    passed_through += moving
for name, passed, held in zip(segment_names, passed_through, charge_in_segment):
    print(f"  {name:12s} charge passed in {ticks * 0.1:.1f} s = {passed:.2f} C   charge sitting there = {held:.2f} C")
print(f"  total free charge in the loop before: {5.0 * len(segment_names):.2f} C, after: {charge_in_segment.sum():.2f} C")
print(f"  charge passed per second at every point: {passed_through[0] / (ticks * 0.1):.2f} A")

print()
print("Step 4: counting the charges that go round")
electrons_per_second = current / ELEMENTARY_CHARGE
print(f"  electrons passing any point each second: {electrons_per_second:.3e}")
seconds_on = 60.0
total_charge = current * seconds_on
print(f"  charge that goes round in {seconds_on:.0f} s: {total_charge:.1f} C")
print(f"  that is {total_charge / ELEMENTARY_CHARGE:.3e} electrons, and every one comes back to the battery")
print(f"  charge piled up anywhere in the loop: {0.0:.1f} C")

print()
print("Step 5: energy delivered while the loop is closed")
power = battery_volts * current
for seconds in [1.0, 60.0, 3600.0]:
    energy = power * seconds
    print(f"  {seconds:6.0f} s on: energy to the bulb = {energy:8.1f} J  (power {power:.2f} W)")
