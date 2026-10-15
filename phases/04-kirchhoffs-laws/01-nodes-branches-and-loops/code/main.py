from collections import deque


def find(parent, name):
    while parent[name] != name:
        parent[name] = parent[parent[name]]
        name = parent[name]
    return name


def merge_wire_segments(netlist):
    parent = {}
    for kind, name, end_a, end_b in netlist:
        parent.setdefault(end_a, end_a)
        parent.setdefault(end_b, end_b)
    for kind, name, end_a, end_b in netlist:
        if kind == "wire":
            root_a, root_b = find(parent, end_a), find(parent, end_b)
            if root_a != root_b:
                keep, drop = sorted([root_a, root_b], key=lambda point: (point != "gnd", point))
                parent[drop] = keep
    return {point: find(parent, point) for point in parent}


def branches_of(netlist, node_of):
    return [(name, node_of[end_a], node_of[end_b]) for kind, name, end_a, end_b in netlist if kind != "wire"]


def count_topology(netlist):
    node_of = merge_wire_segments(netlist)
    nodes = sorted(set(node_of.values()))
    branches = branches_of(netlist, node_of)
    loops = len(branches) - len(nodes) + 1
    return nodes, branches, loops


def spanning_tree(nodes, branches, root):
    neighbours = {node: [] for node in nodes}
    for name, node_a, node_b in branches:
        neighbours[node_a].append((name, node_b))
        neighbours[node_b].append((name, node_a))
    came_from = {root: None}
    tree_branches = set()
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for name, other in neighbours[node]:
            if other not in came_from:
                came_from[other] = (name, node)
                tree_branches.add(name)
                queue.append(other)
    return came_from, tree_branches


def path_to_root(came_from, node):
    path = [node]
    while came_from[node] is not None:
        node = came_from[node][1]
        path.append(node)
    return path


def fundamental_loops(nodes, branches, root):
    came_from, tree_branches = spanning_tree(nodes, branches, root)
    loops = []
    for name, node_a, node_b in branches:
        if name in tree_branches:
            continue
        path_a = path_to_root(came_from, node_a)
        path_b = path_to_root(came_from, node_b)
        meeting = next(node for node in path_a if node in path_b)
        up = path_a[: path_a.index(meeting) + 1]
        down = list(reversed(path_b[: path_b.index(meeting)]))
        loops.append((name, up + down + [node_a]))
    return tree_branches, loops


def describe(title, netlist):
    print(title)
    print("-" * len(title))
    node_of = merge_wire_segments(netlist)
    groups = {}
    for point, node in node_of.items():
        groups.setdefault(node, []).append(point)
    nodes, branches, loop_count = count_topology(netlist)
    print(f"  connection points named in the netlist: {len(node_of)}")
    for node in nodes:
        print(f"    node {node:>4} is made of the points {sorted(groups[node])}")
    print(f"  nodes N    = {len(nodes)}")
    print(f"  branches B = {len(branches)}")
    for name, node_a, node_b in branches:
        print(f"    branch {name:>3} joins node {node_a} to node {node_b}")
    print(f"  independent loops L = B - N + 1 = {len(branches)} - {len(nodes)} + 1 = {loop_count}")
    tree, loops = fundamental_loops(nodes, branches, "gnd")
    print(f"  a spanning tree uses branches {sorted(tree)} ({len(tree)} = N - 1 branches)")
    for name, path in loops:
        print(f"    adding {name:>3} closes the loop " + " -> ".join(path))
    print()


single_loop = [
    ("battery", "B1", "vcc", "gnd"),
    ("resistor", "R1", "vcc", "gnd"),
]

drawn_with_many_wires = [
    ("battery", "B1", "p1", "p6"),
    ("wire", "W1", "p1", "p2"),
    ("resistor", "R1", "p2", "p3"),
    ("wire", "W2", "p3", "p4"),
    ("resistor", "R2", "p4", "p5"),
    ("wire", "W3", "p5", "gnd"),
    ("wire", "W4", "p6", "gnd"),
]

ladder = [
    ("battery", "B1", "vcc", "gnd_left"),
    ("resistor", "R1", "vcc", "a"),
    ("resistor", "R2", "a", "gnd_middle"),
    ("resistor", "R3", "a", "b"),
    ("resistor", "R4", "b", "gnd_right"),
    ("wire", "W1", "gnd_left", "gnd"),
    ("wire", "W2", "gnd_middle", "gnd"),
    ("wire", "W3", "gnd_right", "gnd"),
]

bridge = [
    ("battery", "B1", "top", "gnd"),
    ("resistor", "R1", "top", "left"),
    ("resistor", "R2", "top", "right"),
    ("resistor", "R3", "left", "gnd"),
    ("resistor", "R4", "right", "gnd"),
    ("resistor", "R5", "left", "right"),
]

describe("Example 1: one battery, one resistor", single_loop)
describe("Example 2: two resistors drawn with many wire segments", drawn_with_many_wires)
describe("Example 3: a ladder (battery, R1, then R2 and R3+R4 hanging off node a)", ladder)
describe("Example 4: a bridge (five resistors, one battery)", bridge)

print("Summary table")
print(f"  {'circuit':<12}{'N':>4}{'B':>4}{'L':>4}")
for label, netlist in [("single", single_loop), ("many wires", drawn_with_many_wires), ("ladder", ladder), ("bridge", bridge)]:
    nodes, branches, loops = count_topology(netlist)
    print(f"  {label:<12}{len(nodes):>4}{len(branches):>4}{loops:>4}")
