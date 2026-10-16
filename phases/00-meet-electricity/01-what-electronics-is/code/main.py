TIMELINE = [
    (-600, "Thales of Miletus notices that rubbed amber pulls on bits of straw"),
    (1600, "William Gilbert writes De Magnete and coins the word 'electricus'"),
    (1747, "Benjamin Franklin names the two kinds of charge plus and minus"),
    (1785, "Charles-Augustin de Coulomb measures the force between charges"),
    (1800, "Alessandro Volta stacks zinc, copper and salty cloth: the first battery"),
    (1820, "Hans Christian Oersted sees a current turn a compass needle"),
    (1827, "Georg Ohm shows how the flow depends on the push and the wire"),
    (1831, "Michael Faraday makes a current with a moving magnet"),
    (1882, "Thomas Edison opens a power station in New York"),
    (1888, "Nikola Tesla patents the alternating-current motor"),
    (1897, "J. J. Thomson discovers the electron"),
    (1904, "John Ambrose Fleming builds the vacuum-tube diode"),
    (1947, "Bardeen, Brattain and Shockley build the first transistor"),
    (1958, "Jack Kilby builds the first integrated circuit"),
    (1971, "Intel puts a whole processor on one chip"),
]

GADGETS = [
    ("kettle", "energy"),
    ("toaster", "energy"),
    ("heater", "energy"),
    ("TV remote", "information"),
    ("Wi-Fi router", "information"),
    ("digital thermometer", "information"),
    ("electric car", "both"),
    ("laptop charger", "both"),
    ("LED flashlight with modes", "both"),
]

PHASE_GROUPS = [
    ("Foundations", ["Meet Electricity", "The Physics Underneath", "Your First Circuits",
                     "Resistance and Ohm's Law", "Kirchhoff's Laws",
                     "Circuit Analysis and Our Simulator", "Sources, Batteries and Measurement"]),
    ("Energy stores and waves", ["Capacitors", "Magnetism and Inductors", "Alternating Current",
                                 "Filters and Resonance"]),
    ("Active parts", ["Semiconductors and Diodes", "Transistors", "Operational Amplifiers"]),
    ("Digital", ["Digital Logic", "Sequential Logic", "A Computer from Gates", "Microcontrollers"]),
    ("Real systems", ["Power Electronics", "Sensors and Signals", "Chip Design",
                      "PCB Design and Manufacturing", "Capstone"]),
]


def format_year(year):
    if year < 0:
        return f"{-year} BC"
    return str(year)


def longest_gap(timeline):
    pairs = zip(timeline, timeline[1:])
    return max(((after[0] - before[0], before[0], after[0]) for before, after in pairs))


def torch_pattern(word):
    bits = "".join(format(ord(letter), "08b") for letter in word)
    return "".join("#" if bit == "1" else "." for bit in bits)


print("Step 1: a timeline of electricity and electronics")
for year, event in TIMELINE:
    print(f"  {format_year(year):>7}  {event}")
gap, start, end = longest_gap(TIMELINE)
print(f"  the longest quiet stretch: {gap} years, from {format_year(start)} to {format_year(end)}")
print("  after Volta's battery, discoveries come every few years")

print()
print("Step 2: energy or information?")
for job, heading in (("energy", "mostly energy"), ("information", "mostly information"), ("both", "both at once")):
    names = [name for name, label in GADGETS if label == job]
    print(f"  {heading:<19} {', '.join(names)}")

print()
print("Step 3: the same torch, used to send a message")
message = "HI"
print(f"  message: {message}")
print(f"  pattern (# light on, . light off): {torch_pattern(message)}")
print("  the torch hardly uses any energy for this: the meaning is in the pattern")

print()
print("Step 4: how this course is organised")
phase_number = 0
for group, phases in PHASE_GROUPS:
    print(f"  {group}")
    for phase in phases:
        print(f"    Phase {phase_number:02d}  {phase}")
        phase_number += 1
print(f"  {phase_number} phases in total")
