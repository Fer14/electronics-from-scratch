from dataclasses import dataclass, field

from sim import Circuit


@dataclass
class Part:
    ref: str
    footprint: str
    x: float
    y: float
    pads: dict = field(default_factory=dict)

    def pad_position(self, pad):
        dx, dy = self.pads[pad]
        return self.x + dx, self.y + dy


FOOTPRINTS = {
    "USB_power_2pin": {"1": (0.0, -1.25), "2": (0.0, 1.25)},
    "Button_6mm": {"1": (-3.25, 0.0), "2": (3.25, 0.0)},
    "R_0805": {"1": (-0.95, 0.0), "2": (0.95, 0.0)},
    "LED_0805": {"A": (-0.95, 0.0), "K": (0.95, 0.0)},
}

NETLIST = {
    "VBUS": [("J1", "1"), ("SW1", "1")],
    "SW_OUT": [("SW1", "2"), ("R1", "1")],
    "LED_A": [("R1", "2"), ("D1", "A")],
    "GND": [("D1", "K"), ("J1", "2")],
}


def make_parts(positions):
    return {ref: Part(ref, fp, x, y, dict(FOOTPRINTS[fp])) for ref, (fp, x, y) in positions.items()}


def manhattan(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def minimum_spanning_tree(points):
    in_tree = [0]
    edges = []
    while len(in_tree) < len(points):
        best = None
        for i in in_tree:
            for j in range(len(points)):
                if j in in_tree:
                    continue
                d = manhattan(points[i], points[j])
                if best is None or d < best[0]:
                    best = (d, i, j)
        edges.append(best)
        in_tree.append(best[2])
    return edges


def ratsnest(parts, netlist):
    report = {}
    for net, pins in netlist.items():
        points = [parts[ref].pad_position(pad) for ref, pad in pins]
        edges = minimum_spanning_tree(points)
        report[net] = sum(d for d, _, _ in edges)
    return report


def simulate_schematic():
    c = Circuit()
    c.voltage_source("J1", "vbus", "0", 5.0)
    c.switch("SW1", "vbus", "sw_out", closed=True)
    c.resistor("R1", "sw_out", "led_a", 330)
    c.led("D1", "led_a", "0", color="red")
    return c.dc()


def main():
    print("Step 1: the schematic works before we draw any copper")
    r = simulate_schematic()
    print(f"  LED anode voltage      = {r.v('led_a'):.3f} V")
    print(f"  LED current            = {r.i('D1') * 1000:.2f} mA")
    print(f"  resistor power         = {r.p('R1') * 1000:.2f} mW")

    print("\nStep 2: the netlist (which pins must be joined by copper)")
    for net, pins in NETLIST.items():
        print(f"  {net:7s}: " + ", ".join(f"{ref}.{pad}" for ref, pad in pins))

    tidy = make_parts({
        "J1": ("USB_power_2pin", 2.0, 5.0),
        "SW1": ("Button_6mm", 8.0, 2.0),
        "R1": ("R_0805", 14.0, 4.0),
        "D1": ("LED_0805", 14.0, 7.0),
    })
    messy = make_parts({
        "J1": ("USB_power_2pin", 2.0, 5.0),
        "SW1": ("Button_6mm", 16.0, 9.0),
        "R1": ("R_0805", 3.0, 10.0),
        "D1": ("LED_0805", 18.0, 1.0),
    })

    print("\nStep 3: pad positions in the tidy placement (mm)")
    for part in tidy.values():
        for pad in part.pads:
            x, y = part.pad_position(pad)
            print(f"  {part.ref}.{pad:2s} at ({x:5.2f}, {y:5.2f}) mm")

    print("\nStep 4: ratsnest length per net (Manhattan, mm)")
    tidy_report = ratsnest(tidy, NETLIST)
    messy_report = ratsnest(messy, NETLIST)
    print(f"  {'net':8s} {'tidy':>8s} {'messy':>8s}")
    for net in NETLIST:
        print(f"  {net:8s} {tidy_report[net]:8.2f} {messy_report[net]:8.2f}")
    total_tidy = sum(tidy_report.values())
    total_messy = sum(messy_report.values())
    print(f"  {'total':8s} {total_tidy:8.2f} {total_messy:8.2f}")
    print(f"  the messy placement needs {total_messy / total_tidy:.2f}x more copper")

    print("\nStep 5: what that copper costs in resistance (0.25 mm wide, 35 um thick)")
    rho = 1.72e-8
    area = 0.25e-3 * 35e-6
    for name, total in (("tidy", total_tidy), ("messy", total_messy)):
        resistance = rho * total * 1e-3 / area
        print(f"  {name:5s}: {total:6.2f} mm of trace -> {resistance * 1000:.1f} mOhm in total")


if __name__ == "__main__":
    main()
