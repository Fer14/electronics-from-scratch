from collections import defaultdict

SYMBOLS = [
    ("battery", "a cell or a pack of cells", ["   |  +", " -----   long line = plus", "  ---    short line = minus", "   |  -"]),
    ("wire", "a piece of copper wire", ["  ------------"]),
    ("switch (open)", "a slide or push switch, off", ["  ---o/  o---"]),
    ("switch (closed)", "the same switch, on", ["  ---o---o---"]),
    ("lamp", "a light bulb", ["  ---(X)---    a circle with an X"]),
    ("resistor", "a small striped part (Phase 03)", ["  ---[    ]---  box style", "  ---/\\/\\/---   zigzag style"]),
    ("LED", "a light-emitting diode (Phase 11)", ["  ---|>|---    triangle and bar, arrows for light"]),
    ("ground", "the point we call zero", ["     |", "   -----", "    ---", "     -"]),
    ("junction", "wires really joined", ["  ---*---  a dot: connected", "     |"]),
    ("crossing", "wires passing, not joined", ["     |", "  ---)---  a hop: not connected", "     |"]),
]

FLASHLIGHT = r"""
         S1
   +----o/ o----+
   |            |
  +|           (X) L1  lamp
 ----- B1       |
  ---  battery  |
  -|            |
   +------+-----+
          |
        -----
         ---   ground: our zero
          -
"""

TERMINALS = {"battery": ("plus", "minus"), "switch": ("a", "b"), "lamp": ("a", "b")}

NETLIST = """
B1 battery top gnd
S1 switch top lamp_top
L1 lamp lamp_top gnd
"""


def parse(text):
    parts = []
    for line in text.strip().splitlines():
        name, kind, first, second = line.split()
        parts.append({"name": name, "kind": kind, "nodes": (first, second)})
    return parts


def node_map(parts):
    nodes = defaultdict(list)
    for part in parts:
        for terminal, node in zip(TERMINALS[part["kind"]], part["nodes"]):
            nodes[node].append(f"{part['name']}.{terminal}")
    return dict(nodes)


def walk_loop(parts):
    battery = next(p for p in parts if p["kind"] == "battery")
    start, finish = battery["nodes"]
    steps = [f"start at {battery['name']}'s plus, on '{start}'"]
    node, used = start, {battery["name"]}
    while node != finish:
        part = next(p for p in parts if p["name"] not in used and node in p["nodes"])
        used.add(part["name"])
        node = part["nodes"][1] if part["nodes"][0] == node else part["nodes"][0]
        steps.append(f"through {part['name']} ({part['kind']}) to '{node}'")
    steps.append(f"back into {battery['name']}'s minus: the loop is closed")
    return steps


print("=== the symbols, each with the real thing it stands for ===")
for name, real_object, drawing in SYMBOLS:
    print(f"  {name}: {real_object}")
    for row in drawing:
        print(f"    {row}")

print()
print("=== the flashlight as a schematic ===")
print(FLASHLIGHT)

print("=== the same flashlight as a parts list (a netlist) ===")
parts = parse(NETLIST)
for part in parts:
    print(f"  {part['name']:<3} {part['kind']:<8} connects '{part['nodes'][0]}' and '{part['nodes'][1]}'")

print()
print("=== the junctions (nodes): who touches whom ===")
for node, terminals in node_map(parts).items():
    print(f"  {node:<9} {', '.join(terminals)}")

print()
print("=== reading it wire by wire, following the current ===")
for step in walk_loop(parts):
    print(f"  {step}")
