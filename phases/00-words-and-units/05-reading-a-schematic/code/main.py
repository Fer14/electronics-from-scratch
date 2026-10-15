from collections import defaultdict

TERMINAL_NAMES = {
    "battery": ("plus", "minus"),
    "resistor": ("a", "b"),
    "lamp": ("a", "b"),
    "led": ("anode", "cathode"),
    "diode": ("anode", "cathode"),
    "switch": ("a", "b"),
    "capacitor": ("a", "b"),
}

FLASHLIGHT_SCHEMATIC = r"""
  vcc     S1      lamp_top
   +---o/  o---+
   |           |
  +|          (X) L1
  === B1       |  3 V, 0.3 A lamp
  -|  3 V      |
   |           |
   +-----------+
  gnd
"""

FLASHLIGHT_NETLIST = """
* two AA cells, a slide switch and a small lamp
B1 battery vcc gnd 3V
S1 switch vcc lamp_top closed
L1 lamp lamp_top gnd 10
"""

LED_SCHEMATIC = r"""
  vcc              led_a
   +---[ R1 330 ]---+
   |                |
  +|                V  D1
  === B1           ---  red LED
  -|  5 V           |
   |                |
   +----------------+
  gnd              gnd
"""

LED_NETLIST = """
B1 battery vcc gnd 5V
R1 resistor vcc led_a 330
D1 led led_a gnd red
"""

BROKEN_NETLIST = """
B1 battery vcc gnd 5V
R1 resistor vcc led_a 330
D1 led led_A gnd red
C1 capacitor gnd gnd 100n
"""


def parse_netlist(text):
    parts = []
    for line_number, raw_line in enumerate(text.strip().splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("*"):
            continue
        fields = line.split()
        if len(fields) < 4:
            raise ValueError(f"line {line_number}: expected NAME TYPE NODE NODE [VALUE], got {line!r}")
        name, kind, first_node, second_node = fields[:4]
        if kind not in TERMINAL_NAMES:
            raise ValueError(f"line {line_number}: unknown part type {kind!r}")
        value = fields[4] if len(fields) > 4 else ""
        parts.append({"name": name, "kind": kind, "nodes": (first_node, second_node), "value": value})
    return parts


def build_node_map(parts):
    node_map = defaultdict(list)
    for part in parts:
        for terminal, node in zip(TERMINAL_NAMES[part["kind"]], part["nodes"]):
            node_map[node].append(f"{part['name']}.{terminal}")
    return dict(sorted(node_map.items()))


def find_problems(parts, node_map):
    problems = []
    for node, terminals in node_map.items():
        if len(terminals) == 1:
            problems.append(f"node '{node}' touches only {terminals[0]}: a dangling end, nothing can flow through it")
    for part in parts:
        if part["nodes"][0] == part["nodes"][1]:
            problems.append(f"{part['name']} has both ends on node '{part['nodes'][0]}': it is shorted out and does nothing")
    if "gnd" not in node_map:
        problems.append("no node called 'gnd': this circuit has no reference point")
    return problems


def print_parts(parts):
    print("  parts:")
    for part in parts:
        terminals = TERMINAL_NAMES[part["kind"]]
        links = ", ".join(f"{t} -> {n}" for t, n in zip(terminals, part["nodes"]))
        value = f" [{part['value']}]" if part["value"] else ""
        print(f"    {part['name']:<3} {part['kind']:<9}{value:<9} {links}")


def print_nodes(node_map):
    print("  nodes (who touches whom):")
    for node, terminals in node_map.items():
        print(f"    {node:<9} : {', '.join(terminals)}")


def neighbours(parts, name):
    target = next(part for part in parts if part["name"] == name)
    found = set()
    for part in parts:
        if part["name"] != name and set(part["nodes"]) & set(target["nodes"]):
            found.add(part["name"])
    return sorted(found)


def trace_loop(parts, start_node):
    path = [start_node]
    used = set()
    node = start_node
    while True:
        next_part = next(
            (p for p in parts if p["name"] not in used and node in p["nodes"] and p["kind"] != "battery"),
            None,
        )
        if next_part is None:
            return path, False
        used.add(next_part["name"])
        node = next_part["nodes"][1] if next_part["nodes"][0] == node else next_part["nodes"][0]
        path += [next_part["name"], node]
        battery = next(p for p in parts if p["kind"] == "battery")
        if node == battery["nodes"][1]:
            return path, True


def report(title, schematic, netlist_text):
    print(f"=== {title} ===")
    if schematic:
        print(schematic)
    parts = parse_netlist(netlist_text)
    node_map = build_node_map(parts)
    print_parts(parts)
    print_nodes(node_map)
    for part in parts:
        print(f"  {part['name']} shares a node with: {', '.join(neighbours(parts, part['name'])) or 'nothing'}")
    battery = next((p for p in parts if p["kind"] == "battery"), None)
    if battery is not None:
        path, closed = trace_loop(parts, battery["nodes"][0])
        verdict = "closed loop back to the battery's minus" if closed else "loop is broken"
        print(f"  walk from {battery['name']} plus: {' -> '.join(path)}  ({verdict})")
    problems = find_problems(parts, node_map)
    print(f"  problems found: {len(problems)}")
    for problem in problems:
        print(f"    - {problem}")
    print()


def main():
    report("1. Flashlight", FLASHLIGHT_SCHEMATIC, FLASHLIGHT_NETLIST)
    report("2. Battery, resistor and LED", LED_SCHEMATIC, LED_NETLIST)
    report("3. A netlist with mistakes", "", BROKEN_NETLIST)


if __name__ == "__main__":
    main()
