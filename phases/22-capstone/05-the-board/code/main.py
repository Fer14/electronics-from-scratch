from sim import Circuit

BOARD_W, BOARD_H = 40.0, 30.0
EDGE_CLEARANCE = 1.0
RHO_COPPER = 1.72e-8
COPPER_M = 35e-6

FOOTPRINTS = {
    "JST_2pin": {"size": (6.0, 5.0), "pads": {"+": (-1.0, 0.0), "-": (1.0, 0.0)}},
    "SOT23": {"size": (3.2, 3.2), "pads": {"1": (-0.95, 1.0), "2": (0.95, 1.0), "3": (0.0, -1.0)}},
    "SOIC8": {"size": (6.0, 5.4), "pads": {"1": (-2.7, -1.905), "2": (-2.7, -0.635), "3": (-2.7, 0.635), "4": (-2.7, 1.905),
                                         "5": (2.7, 1.905), "6": (2.7, 0.635), "7": (2.7, -0.635), "8": (2.7, -1.905)}},
    "0805": {"size": (3.0, 1.8), "pads": {"1": (-0.95, 0.0), "2": (0.95, 0.0)}},
    "LDR_5mm": {"size": (5.5, 4.5), "pads": {"1": (-1.7, 0.0), "2": (1.7, 0.0)}},
    "LED_5mm": {"size": (6.0, 6.0), "pads": {"A": (-1.27, 0.0), "K": (1.27, 0.0)}},
}

PARTS = {
    "BT1": ("JST_2pin", (5.0, 15.0), {"+": "+", "-": "-"}, 0.70),
    "U1": ("SOT23", (13.0, 9.0), {"GND": "1", "OUT": "2", "IN": "3"}, 0.25),
    "C1": ("0805", (13.0, 5.0), {"1": "1", "2": "2"}, 0.01),
    "C2": ("0805", (17.5, 9.0), {"1": "1", "2": "2"}, 0.01),
    "C3": ("0805", (27.5, 10.5), {"1": "1", "2": "2"}, 0.01),
    "U2": ("SOIC8", (24.0, 15.0), {"ADC1": "2", "ADC0": "3", "GND": "4", "PB1": "6", "PB2": "7", "VCC": "8"}, 0.60),
    "LDR1": ("LDR_5mm", (34.0, 6.0), {"1": "1", "2": "2"}, 0.10),
    "R1": ("0805", (34.0, 11.0), {"1": "1", "2": "2"}, 0.005),
    "R2": ("0805", (13.0, 20.0), {"1": "1", "2": "2"}, 0.005),
    "R3": ("0805", (13.0, 23.5), {"1": "1", "2": "2"}, 0.005),
    "C4": ("0805", (17.5, 23.5), {"1": "1", "2": "2"}, 0.01),
    "R4": ("0805", (30.0, 20.0), {"1": "1", "2": "2"}, 0.005),
    "Q1": ("SOT23", (30.0, 24.5), {"B": "1", "E": "2", "C": "3"}, 0.03),
    "R5": ("0805", (36.0, 15.0), {"1": "1", "2": "2"}, 0.005),
    "D1": ("LED_5mm", (36.0, 22.0), {"A": "A", "K": "K"}, 0.05),
}

NETS = {
    "VBAT": ["BT1.+", "U1.IN", "C1.1", "R2.1", "R5.1"],
    "VDD": ["U1.OUT", "C2.1", "C3.1", "U2.VCC"],
    "LDR_PWR": ["U2.PB2", "LDR1.1"],
    "LIGHT": ["LDR1.2", "R1.1", "U2.ADC0"],
    "BAT_SENSE": ["R2.2", "R3.1", "C4.1", "U2.ADC1"],
    "PWM": ["U2.PB1", "R4.1"],
    "BASE": ["R4.2", "Q1.B"],
    "LED_A": ["R5.2", "D1.A"],
    "LED_K": ["D1.K", "Q1.C"],
    "GND": ["BT1.-", "U1.GND", "C1.2", "C2.2", "C3.2", "U2.GND", "R1.2", "R3.2", "C4.2", "Q1.E"],
}

NET_CURRENT_A = {"VBAT": 0.021, "LED_A": 0.019, "LED_K": 0.019, "GND": 0.021, "VDD": 0.002}


def pad_xy(pin):
    ref, name = pin.split(".")
    footprint, (x, y), pin_map, _ = PARTS[ref]
    dx, dy = FOOTPRINTS[footprint]["pads"][pin_map[name]]
    return x + dx, y + dy


def courtyard(ref):
    footprint, (x, y), _, _ = PARTS[ref]
    w, h = FOOTPRINTS[footprint]["size"]
    return x - w / 2, y - h / 2, x + w / 2, y + h / 2


def placement_drc():
    errors = []
    refs = list(PARTS)
    for i, a in enumerate(refs):
        ax0, ay0, ax1, ay1 = courtyard(a)
        if min(ax0, ay0, BOARD_W - ax1, BOARD_H - ay1) < EDGE_CLEARANCE - 1e-9:
            errors.append(f"{a} is closer than {EDGE_CLEARANCE} mm to the board edge")
        for b in refs[i + 1:]:
            bx0, by0, bx1, by1 = courtyard(b)
            if ax0 < bx1 and bx0 < ax1 and ay0 < by1 and by0 < ay1:
                errors.append(f"{a} and {b} overlap")
    return errors


def manhattan(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def mst_length(points):
    in_tree, total = [points[0]], 0.0
    rest = list(points[1:])
    while rest:
        d, q = min((manhattan(p, q), q) for p in in_tree for q in rest)
        total += d
        in_tree.append(q)
        rest.remove(q)
    return total


def ipc_width_mm(current_a, rise_c=10.0):
    area_mil2 = (current_a / (0.048 * rise_c ** 0.44)) ** (1 / 0.725)
    return area_mil2 / (COPPER_M / 25.4e-6) * 0.0254


def trace_ohms(length_mm, width_mm):
    return RHO_COPPER * length_mm * 1e-3 / (width_mm * 1e-3 * COPPER_M)


def led_current(path_ohms):
    c = Circuit()
    c.voltage_source("BAT", "bat_ideal", "0", 4.5)
    c.resistor("R_INT", "bat_ideal", "bt", 0.5)
    c.resistor("T_VBAT", "bt", "vbat", path_ohms["VBAT"])
    c.voltage_source("PB1", "pin", "0", 3.3)
    c.resistor("R4", "pin", "base", 2200)
    c.npn("Q1", c="qc", b="base", e="qe", beta=100)
    c.resistor("T_GND", "qe", "0", path_ohms["GND"])
    c.resistor("R5", "vbat", "r5b", 68)
    c.resistor("T_LED_A", "r5b", "led_a", path_ohms["LED_A"])
    c.led("D1", "led_a", "led_k", color="white")
    c.resistor("T_LED_K", "led_k", "qc", path_ohms["LED_K"])
    return c.dc().i("D1")


def main():
    print(f"Step 1: placement on a {BOARD_W:.0f} x {BOARD_H:.0f} mm board")
    for ref, (footprint, (x, y), _, _) in PARTS.items():
        print(f"  {ref:5s} {footprint:9s} at ({x:4.1f}, {y:4.1f}) mm")
    errors = placement_drc()
    print(f"  placement check: {len(errors)} problems" + ("" if not errors else ": " + "; ".join(errors)))
    c3 = pad_xy("C3.1")
    vcc = pad_xy("U2.VCC")
    print(f"  decoupling C3 to U2 VCC pin: {manhattan(c3, vcc):.2f} mm (rule: under 3 mm)")

    print("\nStep 2: ratsnest length per net (minimum spanning tree, Manhattan)")
    lengths = {}
    for net, pins in NETS.items():
        lengths[net] = mst_length([pad_xy(p) for p in pins])
        print(f"  {net:9s} {len(pins):2d} pins, {lengths[net]:6.1f} mm")
    print(f"  total {sum(lengths.values()):.1f} mm of copper")

    print("\nStep 3: trace widths (IPC-2221 minimum for 10 C rise, our chosen width)")
    widths = {}
    for net in NETS:
        current = NET_CURRENT_A.get(net, 0.001)
        need = ipc_width_mm(current)
        widths[net] = 0.4 if net in NET_CURRENT_A else 0.25
        r = trace_ohms(lengths[net], widths[net])
        print(f"  {net:9s} {current * 1000:5.1f} mA: IPC needs {need:.3f} mm, we use {widths[net]:.2f} mm,"
              f" about {r * 1000:5.1f} mOhm, drop {current * r * 1000:.3f} mV")

    print("\nStep 4: does the copper change the LED current? (simulated)")
    zero = {net: 1e-6 for net in ("VBAT", "GND", "LED_A", "LED_K")}
    real = {net: trace_ohms(lengths[net], widths[net]) for net in zero}
    thin = {net: trace_ohms(lengths[net] * 3, 0.15) for net in zero}
    for name, path in (("ideal wires", zero), ("our traces", real), ("3x longer, 0.15 mm traces", thin)):
        print(f"  {name:26s}: LED {led_current(path) * 1000:.3f} mA")

    print("\nStep 5: bill of materials cost (100 units, typical distributor prices)")
    parts_cost = sum(price for *_, price in PARTS.values())
    board_cost = (30.0 + 100 * (BOARD_W * BOARD_H / 100) * 0.012) / 100
    for ref, (*_, price) in PARTS.items():
        print(f"  {ref:5s} ${price:.3f}")
    print(f"  parts ${parts_cost:.2f} + bare board ${board_cost:.2f} = ${parts_cost + board_cost:.2f} per night light"
          f" (R6: parts under $3: {parts_cost < 3})")


if __name__ == "__main__":
    main()
