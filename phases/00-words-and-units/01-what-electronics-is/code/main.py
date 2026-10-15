import numpy as np

THIS_YEAR = 2026
GRAVITY = 9.81

TIMELINE = [
    (-600, "Thales of Miletus notices rubbed amber pulls on light things"),
    (1600, "William Gilbert writes De Magnete and coins the word 'electricus'"),
    (1747, "Benjamin Franklin names the two kinds of charge plus and minus"),
    (1785, "Charles-Augustin de Coulomb measures the force between charges"),
    (1800, "Alessandro Volta stacks zinc, copper and brine: the first battery"),
    (1820, "Hans Christian Oersted sees a current turn a compass needle"),
    (1827, "Georg Ohm publishes how current depends on push and wire"),
    (1831, "Michael Faraday makes a current from a moving magnet"),
    (1882, "Thomas Edison's Pearl Street station sells electricity in New York"),
    (1888, "Nikola Tesla patents the alternating-current induction motor"),
    (1897, "J. J. Thomson discovers the electron"),
    (1904, "John Ambrose Fleming builds the vacuum-tube diode"),
    (1947, "Bardeen, Brattain and Shockley build the first transistor"),
    (1958, "Jack Kilby builds the first integrated circuit"),
    (1971, "Intel 4004: a whole processor with about 2300 transistors"),
]

PHASE_GROUPS = [
    ("Foundations", ["Words and Units", "The Physics Underneath", "Your First Circuits",
                     "Resistance and Ohm's Law", "Kirchhoff's Laws",
                     "Circuit Analysis and Our Simulator", "Sources, Batteries and Measurement"]),
    ("Energy stores and waves", ["Capacitors", "Magnetism and Inductors", "Alternating Current",
                                 "Filters and Resonance"]),
    ("Active parts", ["Semiconductors and Diodes", "Transistors", "Operational Amplifiers"]),
    ("Digital", ["Digital Logic", "Sequential Logic", "A Computer from Gates", "Microcontrollers"]),
    ("Real systems", ["Power Electronics", "Sensors and Signals", "Chip Design",
                      "PCB Design and Manufacturing", "Capstone"]),
]


def years_ago(year):
    return THIS_YEAR - year


def format_year(year):
    return f"{-year} BC" if year < 0 else f"{year} AD" if year < 1000 else str(year)


def text_to_bits(text):
    return "".join(format(ord(letter), "08b") for letter in text)


def energy_of_message(bits, volts, amps, seconds_per_bit):
    ones = bits.count("1")
    return ones * volts * amps * seconds_per_bit


print("Step 1: a timeline of electricity and electronics")
for year, event in TIMELINE:
    print(f"  {format_year(year):>8}  ({years_ago(year):5d} years ago)  {event}")
years = np.array([year for year, _ in TIMELINE])
gaps = np.diff(years)
print(f"  longest quiet gap: {gaps.max()} years, between {format_year(years[gaps.argmax()])} and {years[gaps.argmax() + 1]}")
print(f"  events after 1800: {np.sum(years >= 1800)} of {len(years)}")

print()
print("Step 2: a flashlight moves energy")
cell_volts = 1.5
cells = 2
bulb_amps = 0.25
battery_volts = cell_volts * cells
power_watts = battery_volts * bulb_amps
seconds = 3600
energy_joules = power_watts * seconds
book_lift_joules = 1.0 * GRAVITY * 1.0
print(f"  battery: {cells} cells x {cell_volts} V = {battery_volts:.1f} V")
print(f"  bulb current: {bulb_amps} A")
print(f"  power = {battery_volts:.1f} V x {bulb_amps} A = {power_watts:.2f} W")
print(f"  energy in one hour = {power_watts:.2f} W x {seconds} s = {energy_joules:.0f} J")
print(f"  lifting a 1 kg book by 1 m takes {book_lift_joules:.2f} J")
print(f"  so one hour of flashlight = {energy_joules / book_lift_joules:.0f} book lifts")

print()
print("Step 3: the same light carries information")
message = "HI"
bits = text_to_bits(message)
print(f"  message: {message!r}")
for letter in message:
    print(f"    {letter} -> code {ord(letter):3d} -> bits {format(ord(letter), '08b')}")
pattern = "".join("#" if bit == "1" else "." for bit in bits)
print(f"  light pattern (# on, . off): {pattern}")
led_volts = 2.0
led_amps = 0.02
seconds_per_bit = 0.1
message_energy = energy_of_message(bits, led_volts, led_amps, seconds_per_bit)
print(f"  LED at {led_volts} V and {led_amps} A, {seconds_per_bit} s per bit")
print(f"  {bits.count('1')} 'on' bits use {message_energy * 1000:.1f} mJ in {len(bits) * seconds_per_bit:.1f} s")
print(f"  the flashlight hour used {energy_joules / message_energy:,.0f} times more energy")
print("  electricity cares about how much energy; electronics cares about the pattern")

print()
print("Step 4: a tour of a phone charger, stage by stage")
stages = [
    ("wall socket (Europe)", "230 V alternating, 50 times a second"),
    ("rectifier + capacitor", "about 325 V steady, one direction only"),
    ("switching transistor", "chops it on/off ~100 000 times a second"),
    ("small transformer", "steps the chopped voltage down, isolates you from the mains"),
    ("output rectifier + capacitor", "smooth 5 V steady"),
    ("feedback chip", "measures the 5 V and adjusts the chopping"),
]
for number, (stage, what_happens) in enumerate(stages, start=1):
    print(f"  {number}. {stage:<30} {what_happens}")
output_volts = 5.0
output_amps = 2.0
efficiency = 0.85
output_watts = output_volts * output_amps
input_watts = output_watts / efficiency
print(f"  output: {output_volts} V x {output_amps} A = {output_watts:.1f} W")
print(f"  at {efficiency:.0%} efficiency the wall supplies {input_watts:.2f} W")
print(f"  {input_watts - output_watts:.2f} W becomes heat, which is why chargers feel warm")

print()
print("Step 5: how this course is organized")
phase_number = 0
for group, phases in PHASE_GROUPS:
    print(f"  {group}")
    for phase in phases:
        print(f"    Phase {phase_number:02d}  {phase}")
        phase_number += 1
print(f"  total: {phase_number} phases")
