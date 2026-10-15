from collections import deque

ROWS = 30
LEFT_COLUMNS = "abcde"
RIGHT_COLUMNS = "fghij"
RAILS = ["L+", "L-", "R+", "R-"]
RAIL_HOLES = 25


class UnionFind:
    def __init__(self):
        self.parent = {}

    def add(self, item):
        self.parent.setdefault(item, item)

    def find(self, item):
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != root:
            self.parent[item], item = root, self.parent[item]
        return root

    def union(self, first, second):
        root_first, root_second = self.find(first), self.find(second)
        if root_first != root_second:
            self.parent[root_second] = root_first


def all_holes():
    holes = [f"{column}{row}" for row in range(1, ROWS + 1) for column in LEFT_COLUMNS + RIGHT_COLUMNS]
    holes += [f"{rail}{index}" for rail in RAILS for index in range(1, RAIL_HOLES + 1)]
    return holes


def internal_strips():
    strips = []
    for row in range(1, ROWS + 1):
        strips.append([f"{column}{row}" for column in LEFT_COLUMNS])
        strips.append([f"{column}{row}" for column in RIGHT_COLUMNS])
    for rail in RAILS:
        strips.append([f"{rail}{index}" for index in range(1, RAIL_HOLES + 1)])
    return strips


def build_board(wires):
    board = UnionFind()
    for hole in all_holes():
        board.add(hole)
    for strip in internal_strips():
        for hole in strip[1:]:
            board.union(strip[0], hole)
    for start, end in wires:
        board.union(start, end)
    return board


def net_names(board, parts):
    names = {}
    for name, legs in parts:
        for leg_name, hole in legs:
            root = board.find(hole)
            names.setdefault(root, []).append(f"{name}.{leg_name}")
    return names


def shorted_parts(board, parts):
    return [name for name, legs in parts if board.find(legs[0][1]) == board.find(legs[1][1])]


def lonely_legs(board, parts):
    members = net_names(board, parts)
    return [labels[0] for labels in members.values() if len(labels) == 1]


def loop_is_closed(board, parts, battery_name):
    battery = dict(parts)[battery_name]
    start = board.find(battery[0][1])
    goal = board.find(battery[1][1])
    if start == goal:
        return False
    edges = {}
    for name, legs in parts:
        if name == battery_name:
            continue
        first, second = board.find(legs[0][1]), board.find(legs[1][1])
        edges.setdefault(first, []).append(second)
        edges.setdefault(second, []).append(first)
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            return True
        for neighbour in edges.get(node, []):
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return False


def inspect(title, parts, wires):
    board = build_board(wires)
    print(f"=== {title} ===")
    for labels in net_names(board, parts).values():
        print(f"  net: {', '.join(labels)}")
    battery_short = board.find(dict(parts)["B1"][0][1]) == board.find(dict(parts)["B1"][1][1])
    problems = []
    if battery_short:
        problems.append("SHORT CIRCUIT: battery + and - are in the same net")
    for name in shorted_parts(board, parts):
        if name != "B1":
            problems.append(f"{name} is shorted: both legs in the same net, current bypasses it")
    for label in lonely_legs(board, parts):
        problems.append(f"{label} touches nothing else")
    if not battery_short and not loop_is_closed(board, parts, "B1"):
        problems.append("OPEN CIRCUIT: no path through the parts from battery + back to battery -")
    if problems:
        for problem in problems:
            print(f"  problem: {problem}")
    else:
        print("  ok: closed loop, no shorted parts, every leg has company")
    print()


def main():
    print(f"Breadboard model: {ROWS} rows x {len(LEFT_COLUMNS + RIGHT_COLUMNS)} columns + {len(RAILS)} rails of {RAIL_HOLES}")
    print(f"  total holes (tie points): {len(all_holes())}")
    board = build_board([])
    print(f"  separate metal strips   : {len({board.find(hole) for hole in all_holes()})}")
    print(f"  a10 and e10 connected?  : {board.find('a10') == board.find('e10')}")
    print(f"  e10 and f10 connected?  : {board.find('e10') == board.find('f10')}  (the centre gap)")
    print(f"  a10 and a11 connected?  : {board.find('a10') == board.find('a11')}")
    print(f"  L+1 and L+25 connected? : {board.find('L+1') == board.find('L+25')}")
    print()

    good_parts = [
        ("B1", [("plus", "L+1"), ("minus", "L-1")]),
        ("R1", [("a", "L+10"), ("b", "c10")]),
        ("D1", [("anode", "e10"), ("cathode", "e13")]),
    ]
    good_wires = [("a13", "L-13")]
    inspect("1. working LED circuit", good_parts, good_wires)

    same_row_resistor = [
        ("B1", [("plus", "L+1"), ("minus", "L-1")]),
        ("R1", [("a", "b10"), ("b", "d10")]),
        ("D1", [("anode", "e10"), ("cathode", "e13")]),
    ]
    inspect("2. resistor with both legs in row 10", same_row_resistor, [("a10", "L+10"), ("a13", "L-13")])

    inspect("3. forgot the jumper to the minus rail", good_parts, [])

    inspect("4. jumper pushed into the plus rail by mistake", good_parts, [("a13", "L+13")])

    across_gap = [
        ("B1", [("plus", "L+1"), ("minus", "L-1")]),
        ("R1", [("a", "L+10"), ("b", "c10")]),
        ("D1", [("anode", "e10"), ("cathode", "f10")]),
    ]
    inspect("5. LED straddling the centre gap", across_gap, [("j10", "R-10"), ("R-1", "L-2")])


if __name__ == "__main__":
    main()
