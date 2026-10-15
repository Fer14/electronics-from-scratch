import math
from dataclasses import dataclass
from pathlib import Path

from sim.lab import evaluate, load_task

RULES = {
    "min_trace_width": 0.15,
    "min_clearance": 0.15,
    "min_drill": 0.30,
    "min_annular_ring": 0.15,
    "edge_clearance": 0.30,
}

VOLTAGE_CLEARANCE_OUTER = [(30, 0.10), (100, 0.60), (300, 1.25), (500, 2.50)]


@dataclass
class Capsule:
    kind: str
    name: str
    net: str
    start: tuple
    end: tuple
    radius: float


def trace(name, net, start, end, width):
    return Capsule("trace", name, net, start, end, width / 2)


def pad(name, net, centre, size):
    return Capsule("pad", name, net, centre, centre, size / 2)


def via(name, net, centre, drill, diameter):
    item = Capsule("via", name, net, centre, centre, diameter / 2)
    item.drill = drill
    return item


def point_segment_distance(p, a, b):
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    length2 = dx * dx + dy * dy
    if length2 == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / length2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def segments_cross(a, b, c, d):
    def side(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    d1, d2 = side(c, d, a), side(c, d, b)
    d3, d4 = side(a, b, c), side(a, b, d)
    return d1 * d2 < 0 and d3 * d4 < 0


def segment_distance(a, b, c, d):
    if segments_cross(a, b, c, d):
        return 0.0
    return min(point_segment_distance(a, c, d), point_segment_distance(b, c, d),
               point_segment_distance(c, a, b), point_segment_distance(d, a, b))


def gap(x, y):
    return segment_distance(x.start, x.end, y.start, y.end) - x.radius - y.radius


def voltage_clearance(volts):
    for limit, clearance in VOLTAGE_CLEARANCE_OUTER:
        if volts <= limit:
            return clearance
    return None


def drc(items, board_w, board_h, net_volts):
    errors = []
    for item in items:
        if item.kind == "trace" and 2 * item.radius < RULES["min_trace_width"] - 1e-9:
            errors.append(f"{item.name}: width {2 * item.radius:.2f} mm < {RULES['min_trace_width']} mm")
        if item.kind == "via":
            if item.drill < RULES["min_drill"] - 1e-9:
                errors.append(f"{item.name}: drill {item.drill:.2f} mm < {RULES['min_drill']} mm")
            ring = item.radius - item.drill / 2
            if ring < RULES["min_annular_ring"] - 1e-9:
                errors.append(f"{item.name}: annular ring {ring:.2f} mm < {RULES['min_annular_ring']} mm")
        for x, y in (item.start, item.end):
            edge = min(x, y, board_w - x, board_h - y) - item.radius
            if edge < RULES["edge_clearance"] - 1e-9:
                errors.append(f"{item.name}: {edge:.2f} mm from the board edge < {RULES['edge_clearance']} mm")
                break
    for i, x in enumerate(items):
        for y in items[i + 1:]:
            if x.net == y.net:
                continue
            needed = max(RULES["min_clearance"], voltage_clearance(abs(net_volts[x.net] - net_volts[y.net])))
            g = gap(x, y)
            if g < needed - 1e-9:
                errors.append(f"{x.name} ({x.net}) to {y.name} ({y.net}): gap {g:.2f} mm < {needed:.2f} mm")
    return errors


def first_layout():
    return [
        pad("J1.1", "VIN", (2.0, 4.0), 1.7),
        pad("J1.2", "GND", (2.0, 6.54), 1.7),
        trace("T1", "VIN", (2.0, 4.0), (12.0, 4.0), 0.5),
        trace("T2", "SIG", (4.0, 4.4), (12.8, 4.4), 0.10),
        trace("T3", "GND", (2.0, 6.54), (12.0, 6.54), 0.5),
        via("V1", "SIG", (12.8, 4.4), 0.20, 0.45),
        trace("T4", "VIN", (12.0, 4.0), (12.0, 0.2), 0.5),
    ]


def fixed_layout():
    return [
        pad("J1.1", "VIN", (2.0, 4.0), 1.7),
        pad("J1.2", "GND", (2.0, 6.54), 1.7),
        trace("T1", "VIN", (2.0, 4.0), (12.0, 4.0), 0.5),
        trace("T2", "SIG", (4.0, 5.27), (11.0, 5.27), 0.20),
        trace("T3", "GND", (2.0, 6.54), (12.0, 6.54), 0.5),
        via("V1", "SIG", (11.0, 5.27), 0.30, 0.60),
        trace("T4", "VIN", (12.0, 4.0), (12.0, 1.0), 0.5),
    ]


def main():
    net_volts = {"VIN": 12.0, "GND": 0.0, "SIG": 3.3}

    print("Step 1: the rules of our pretend low-cost fab (mm)")
    for name, value in RULES.items():
        print(f"  {name:18s} {value:.2f} mm")
    print("  voltage clearance on uncoated outer layers (simplified IPC-2221):")
    for limit, clearance in VOLTAGE_CLEARANCE_OUTER:
        print(f"    up to {limit:3d} V -> {clearance:.2f} mm")

    print("\nStep 2: a gap measured between two capsules")
    a = trace("A", "VIN", (0.0, 0.0), (10.0, 0.0), 0.5)
    b = trace("B", "GND", (0.0, 0.6), (10.0, 0.6), 0.5)
    print(f"  centre lines 0.60 mm apart, both 0.50 mm wide -> copper gap {gap(a, b):.2f} mm")

    print("\nStep 3: DRC of the first layout")
    errors = drc(first_layout(), 20.0, 10.0, net_volts)
    for error in errors:
        print(f"  ERROR {error}")
    print(f"  {len(errors)} violations")

    print("\nStep 4: DRC of the fixed layout")
    errors = drc(fixed_layout(), 20.0, 10.0, net_volts)
    for error in errors:
        print(f"  ERROR {error}")
    print(f"  {len(errors)} violations")

    print("\nStep 5: an electrical rule, decoupling (the lab task)")
    task = load_task(Path(__file__).parent.parent / "lab" / "task.json")
    for part in task["parts"]:
        result = evaluate(task, {"S1": part})[0]
        verdict = "PASS" if result["passed"] else "fail"
        print(f"  {part['farads'] * 1e6:6.0f} uF: lowest vdd {result['value']:.3f} V -> {verdict}")


if __name__ == "__main__":
    main()
