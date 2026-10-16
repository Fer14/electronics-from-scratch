CONDUCTS = {
    "wire": True,
    "closed switch": True,
    "lamp": True,
    "open switch": False,
    "cut wire": False,
    "plastic strip": False,
    "burnt-out lamp": False,
}

SCENARIOS = [
    ("the flashlight, switch on", ["wire", "closed switch", "wire", "lamp", "wire"], False),
    ("the flashlight, switch off", ["wire", "open switch", "wire", "lamp", "wire"], False),
    ("a wire has come loose", ["wire", "closed switch", "cut wire", "lamp", "wire"], False),
    ("a plastic strip in the gap", ["wire", "plastic strip", "wire", "lamp", "wire"], False),
    ("the lamp has burnt out", ["wire", "closed switch", "wire", "burnt-out lamp", "wire"], False),
    ("a wire straight across the battery", ["wire", "closed switch", "wire", "lamp", "wire"], True),
]


def first_gap(path):
    for position, piece in enumerate(path):
        if not CONDUCTS[piece]:
            return position, piece
    return None


def describe(path, shorted):
    print("  path: battery + -> " + " -> ".join(path) + " -> battery -")
    gap = first_gap(path)
    if shorted:
        print("  a bare wire joins the battery's + and - directly")
        print("  the flow takes that easy shortcut instead of going through the lamp")
        print("  lamp: dark   battery: gets hot, a short circuit (never do this)")
    elif gap is None:
        print("  the path goes out and comes back: a closed loop")
        print("  lamp: ON")
    else:
        position, piece = gap
        print(f"  the path is broken at piece {position + 1} ({piece}): an open circuit")
        print("  lamp: OFF    battery: fine, nothing flows anywhere in the loop")


def roles(parts):
    for name, role, job in parts:
        print(f"  {name:<8} {role:<8} {job}")


for title, path, shorted in SCENARIOS:
    print(f"=== {title} ===")
    describe(path, shorted)
    print()

print("=== who does what ===")
roles([
    ("battery", "source", "gives energy, pushes the flow round the loop"),
    ("lamp", "load", "takes energy and turns it into light and heat"),
    ("wire", "path", "carries the flow from one part to the next"),
    ("switch", "control", "opens or closes the loop"),
])
