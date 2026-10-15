from sim import Circuit

METERS = {
    "ideal meter": None,
    "DMM, 10 Mohm": 10e6,
    "analog 20 kohm/V on 10 V": 200e3,
    "analog 1 kohm/V on 10 V": 10e3,
}


def divider_reading(top_ohms, bottom_ohms, meter_ohms, volts=10.0):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", volts)
    c.resistor("R1", "vcc", "mid", top_ohms)
    c.resistor("R2", "mid", "0", bottom_ohms)
    if meter_ohms is not None:
        c.resistor("Rmeter", "mid", "0", meter_ohms)
    return c.dc().v("mid")


def predicted_reading(open_volts, thevenin_ohms, meter_ohms):
    return open_volts * meter_ohms / (meter_ohms + thevenin_ohms)


def solve_two_readings(reading_a, meter_a, reading_b, meter_b):
    thevenin_ohms = (reading_b - reading_a) / (reading_a / meter_a - reading_b / meter_b)
    open_volts = reading_a * (meter_a + thevenin_ohms) / meter_a
    return open_volts, thevenin_ohms


print("Step 1: measuring the middle of a 1 Mohm / 1 Mohm divider on 10 V (true value 5 V)")
for name, meter in METERS.items():
    reading = divider_reading(1e6, 1e6, meter)
    print(f"  {name:<26}: reads {reading:.3f} V, error {100 * (reading - 5.0) / 5.0:+6.1f} %")

print()
print("Step 2: the same meters on a 1 kohm / 1 kohm divider (true value 5 V)")
for name, meter in METERS.items():
    reading = divider_reading(1e3, 1e3, meter)
    print(f"  {name:<26}: reads {reading:.4f} V, error {100 * (reading - 5.0) / 5.0:+7.3f} %")

print()
print("Step 3: the Thevenin view predicts every reading")
for top, bottom in [(1e6, 1e6), (1e3, 1e3), (100e3, 47e3)]:
    open_volts = 10.0 * bottom / (top + bottom)
    thevenin = top * bottom / (top + bottom)
    simulated = divider_reading(top, bottom, 10e6)
    print(f"  {top:>9.0f} / {bottom:>9.0f} ohm: V_th {open_volts:.4f} V, R_th {thevenin:>9.0f} ohm, "
          f"predicted {predicted_reading(open_volts, thevenin, 10e6):.4f} V, simulated {simulated:.4f} V")

print()
print("Step 4: undo the error with two readings from meters of known resistance")
reading_dmm = round(divider_reading(1e6, 1e6, 10e6), 3)
reading_analog = round(divider_reading(1e6, 1e6, 200e3), 3)
open_volts, thevenin = solve_two_readings(reading_dmm, 10e6, reading_analog, 200e3)
print(f"  DMM (10 Mohm) reads {reading_dmm} V, analog (200 kohm) reads {reading_analog} V")
print(f"  solving both: hidden V_th = {open_volts:.3f} V, hidden R_th = {thevenin / 1000:.0f} kohm (true: 5 V, 500 kohm)")

print()
print("Step 5: an ammeter's burden: 3.3 V across a 33 ohm load (true current 100 mA)")
for name, meter_ohms in [("ideal ammeter", 0.0), ("mA range, 1.5 ohm", 1.5), ("10 A range, 0.06 ohm", 0.06)]:
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", 3.3)
    if meter_ohms == 0.0:
        c.resistor("Rload", "vcc", "0", 33.0)
    else:
        c.resistor("Rmeter", "vcc", "x", meter_ohms)
        c.resistor("Rload", "x", "0", 33.0)
    r = c.dc()
    current = r.i("Rload")
    print(f"  {name:<22}: {current * 1000:7.2f} mA, error {100 * (current - 0.1) / 0.1:+5.2f} %")

print()
print("Step 6: measuring a resistor with a voltmeter (10 Mohm) and an ammeter (1 ohm), 10 V source")


def measure_resistor(true_ohms, voltmeter_across_resistor_only):
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", 10.0)
    c.resistor("Ram", "vcc", "x", 1.0)
    c.resistor("Rx", "x", "0", true_ohms)
    if voltmeter_across_resistor_only:
        c.resistor("Rvm", "x", "0", 10e6)
        r = c.dc()
        return r.v("x") / r.i("Ram")
    c.resistor("Rvm", "vcc", "0", 10e6)
    r = c.dc()
    return r.v("vcc") / r.i("Ram")


for true_ohms in [10.0, 1e6]:
    across = measure_resistor(true_ohms, True)
    around = measure_resistor(true_ohms, False)
    print(f"  true {true_ohms:>9.0f} ohm: voltmeter across R only -> {across:>12.2f} ohm ({100 * (across / true_ohms - 1):+.4f} %), "
          f"voltmeter across both -> {around:>12.2f} ohm ({100 * (around / true_ohms - 1):+.4f} %)")
print("  small resistors: put the voltmeter right across them; large ones: across the ammeter too")
