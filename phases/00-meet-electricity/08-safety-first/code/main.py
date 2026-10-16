SOURCES = [
    ("one AA cell", "low", "small", "safe to touch; never short it"),
    ("a square 9 V battery", "low", "medium", "safe to touch; never short it, keep away from keys and coins"),
    ("a USB port", "low", "limited by the port", "safe to touch"),
    ("a phone or laptop lithium battery", "low", "very large", "safe to touch; never puncture, crush or short it: it can catch fire"),
    ("a car battery", "low", "enormous", "safe to touch; a short can melt metal and burn you"),
    ("a wall socket", "high", "large", "DANGEROUS: never touch, never open anything that plugs in"),
]

BODY_EFFECTS = [
    "a tiny current: not felt at all",
    "a little more: a tingle",
    "more: painful, muscles start to twitch",
    "more still: muscles lock and you may not be able to let go",
    "enough through the chest: the heart can lose its rhythm, which can kill",
]

RULES = [
    "Stay with batteries and USB power, at 12 volts or less.",
    "Never open or modify anything that plugs into the wall, even unplugged.",
    "Never connect a wire straight across a battery.",
    "Treat lithium batteries with respect: no punctures, no crushing, no shorts.",
    "Disconnect the battery before you change a circuit.",
    "If something gets hot, smells or smokes: disconnect first, think later.",
    "When in doubt, simulate first.",
]


def push_and_path(push, path_is_easy):
    if push == "high" and path_is_easy:
        return "large current through you: very dangerous"
    if push == "high":
        return "the high push can break through dry skin: still dangerous"
    if path_is_easy:
        return "the push is too small to drive a harmful current through skin"
    return "nothing felt"


print("=== what hurts is current; what pushes it is voltage ===")
for step, effect in enumerate(BODY_EFFECTS, start=1):
    print(f"  {'>' * step:<6} {effect}")

print()
print("=== push x path: when does a dangerous current flow through a person? ===")
for push in ("low", "high"):
    for path_is_easy, skin in ((False, "dry skin"), (True, "wet skin")):
        print(f"  {push:<4} push, {skin:<9} -> {push_and_path(push, path_is_easy)}")

print()
print("=== everyday sources ===")
print(f"  {'source':<34} {'push':<5} {'current into a short':<21} verdict")
for name, push, deliver, verdict in SOURCES:
    print(f"  {name:<34} {push:<5} {deliver:<21} {verdict}")

print()
print("=== the rules of this course ===")
for number, rule in enumerate(RULES, start=1):
    print(f"  {number}. {rule}")
