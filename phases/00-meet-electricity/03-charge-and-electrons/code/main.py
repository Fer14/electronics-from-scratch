PARTICLES = [
    ("proton", "positive (+)", "heavy", "locked in the centre of the atom"),
    ("neutron", "none", "heavy", "locked in the centre of the atom"),
    ("electron", "negative (-)", "very light", "around the centre; in metals some wander freely"),
]

PAIRS = [
    ("+", "+", "push apart"),
    ("-", "-", "push apart"),
    ("+", "-", "pull together"),
]

WIRE_LENGTH = 24
FOLLOWED = 5


def draw_wire(shift):
    cells = []
    for position in range(WIRE_LENGTH):
        cells.append("@" if position == FOLLOWED + shift else "e")
    return "[battery]=" + "".join(cells) + "=[lamp]"


def object_charge(protons, electrons):
    difference = protons - electrons
    if difference == 0:
        return "neutral: no overall charge"
    if difference > 0:
        return f"positive: {difference} electrons short"
    return f"negative: {-difference} electrons extra"


print("=== what atoms are made of ===")
for name, charge, weight, where in PARTICLES:
    print(f"  {name:<9} charge {charge:<13} {weight:<11} {where}")

print()
print("=== how charges treat each other ===")
for first, second, effect in PAIRS:
    print(f"  {first} and {second}: {effect}")

print()
print("=== a balloon rubbed on your hair (a small made-up count) ===")
print(f"  before rubbing, balloon: {object_charge(100, 100)}")
print(f"  after rubbing,  balloon: {object_charge(100, 103)}")
print(f"  after rubbing,  hair:    {object_charge(100, 97)}")
print("  no charge was created or destroyed: a few electrons simply moved")

print()
print("=== a wire is already full of loose electrons ===")
print("  the battery does not create them; it pushes the whole crowd at once")
print("  follow the electron marked @ while the battery pushes, step by step:")
for step in range(4):
    print(f"  step {step}: {draw_wire(step)}")
print("  the crowd moved at the lamp end from the very first step,")
print("  but the electron we followed has only crept a few places")
