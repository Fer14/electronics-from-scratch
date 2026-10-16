LOOP_POINTS = ["leaving the battery's +", "before the switch", "into the lamp", "out of the lamp", "back into the battery's -"]

EVERYDAY_CURRENTS = [
    ("a quartz wristwatch", "a tiny trickle, a millionth of an amp or so"),
    ("a small LED indicator", "a few thousandths of an amp"),
    ("a torch bulb", "a fraction of an amp"),
    ("a phone charging from a charger", "about one or two amps"),
    ("an electric kettle", "around ten amps"),
    ("a car's starter motor", "hundreds of amps, for a few seconds"),
]


def count_at_gate(crowds_per_second, seconds):
    return crowds_per_second * seconds


def current(crowds, seconds):
    return crowds / seconds


def compare(first, second):
    (first_name, first_crowds, first_seconds), (second_name, second_crowds, second_seconds) = first, second
    print(f"  {first_name}: {first_crowds} crowds in {first_seconds} s    {second_name}: {second_crowds} crowds in {second_seconds} s")
    first_current = current(first_crowds, first_seconds)
    second_current = current(second_crowds, second_seconds)
    if first_current == second_current:
        return "    -> the same current in both"
    bigger = first_name if first_current > second_current else second_name
    return f"    -> {bigger} carries the bigger current"


print("=== current is charge passing a point each second ===")
print("  picture a gate in the wire and count the crowds of charge going through")
for seconds in (1, 2, 3):
    print(f"  after {seconds} second(s): {count_at_gate(2, seconds)} crowds counted")
print("  the count keeps growing, but the rate stays the same: that steady rate is the current")

print()
print("=== comparing currents ===")
print(compare(("wire A", 3, 1), ("wire B", 6, 1)))
print(compare(("wire C", 4, 2), ("wire D", 4, 1)))
print(compare(("wire E", 2, 1), ("wire F", 6, 3)))
print("  what matters is how much passes per second, not how much has passed in total")

print()
print("=== the same current all round one loop ===")
for point in LOOP_POINTS:
    print(f"  {point:<28} the same current")
print("  the lamp takes energy, not charge: what goes in comes out")

print()
print("=== two arrows for one event ===")
print("  conventional current:  + ---->---->---->  -   (how diagrams draw it)")
print("  electrons drift:       + ----<----<----<  -   (what electrons actually do)")

print()
print("=== how big are everyday currents? ===")
for device, size in EVERYDAY_CURRENTS:
    print(f"  {device:<32} {size}")
