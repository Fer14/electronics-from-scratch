import math

from sim import Circuit

FULL_SCALE_AMPS = 0.001
COIL_OHMS = 200.0


def needle_percent(coil_amps):
    return 100.0 * coil_amps / FULL_SCALE_AMPS


def multiplier_for(volts_range):
    return volts_range / FULL_SCALE_AMPS - COIL_OHMS


def shunt_for(amps_range):
    return COIL_OHMS * FULL_SCALE_AMPS / (amps_range - FULL_SCALE_AMPS)


def analog_voltmeter_reading(measured_volts, volts_range):
    c = Circuit()
    c.voltage_source("Vx", "x", "0", measured_volts)
    c.resistor("Rmult", "x", "coil", multiplier_for(volts_range))
    c.resistor("Rcoil", "coil", "0", COIL_OHMS)
    return c.dc().i("Rcoil")


def analog_ammeter_reading(measured_amps, amps_range):
    c = Circuit()
    c.current_source("Ix", "0", "top", measured_amps)
    c.resistor("Rshunt", "top", "0", shunt_for(amps_range))
    c.resistor("Rcoil", "top", "0", COIL_OHMS)
    r = c.dc()
    return r.i("Rcoil"), r.v("top")


def analog_ohmmeter_reading(unknown_ohms, battery_volts=1.5):
    c = Circuit()
    c.voltage_source("B", "b", "0", battery_volts)
    c.resistor("Rzero", "b", "coil", battery_volts / FULL_SCALE_AMPS - COIL_OHMS)
    c.resistor("Rcoil", "coil", "probe", COIL_OHMS)
    c.resistor("Rx", "probe", "0", unknown_ohms)
    return c.dc().i("Rcoil")


LADDER = [9e6, 900e3, 90e3, 10e3]
RANGES = {"200 mV": 0, "2 V": 1, "20 V": 2, "200 V": 3}
ADC_FULL_SCALE = 0.2
COUNTS = 2000


def adc_counts(volts):
    return round(volts / ADC_FULL_SCALE * COUNTS)


def digital_voltmeter_reading(measured_volts, range_name):
    c = Circuit()
    c.voltage_source("Vx", "n0", "0", measured_volts)
    for k, ohms in enumerate(LADDER):
        bottom = "0" if k == len(LADDER) - 1 else f"n{k + 1}"
        c.resistor(f"R{k}", f"n{k}", bottom, ohms)
    r = c.dc()
    tap = RANGES[range_name]
    tap_volts = measured_volts if tap == 0 else r.v(f"n{tap}")
    ratio = sum(LADDER) / sum(LADDER[tap:])
    counts = adc_counts(tap_volts)
    if abs(counts) >= COUNTS:
        return tap_volts, "OL"
    step = ADC_FULL_SCALE / COUNTS * ratio
    decimals = max(0, round(-math.log10(step)))
    return tap_volts, f"{counts * step:.{decimals}f}"


print("Step 1: the moving-coil movement on its own")
print(f"  full scale: {FULL_SCALE_AMPS * 1000:.1f} mA through a {COIL_OHMS:.0f} ohm coil")
print(f"  so full scale is only {FULL_SCALE_AMPS * COIL_OHMS:.2f} V across the coil")

print()
print("Step 2: a voltmeter = movement + big series resistor (the multiplier)")
for volts_range in [1.0, 10.0, 100.0]:
    multiplier = multiplier_for(volts_range)
    coil_amps = analog_voltmeter_reading(volts_range, volts_range)
    half = analog_voltmeter_reading(volts_range / 2, volts_range)
    print(f"  {volts_range:>5.0f} V range: multiplier {multiplier:>8.0f} ohm, total {volts_range / FULL_SCALE_AMPS:>8.0f} ohm, "
          f"needle at {needle_percent(coil_amps):.1f}% for {volts_range:.0f} V and {needle_percent(half):.1f}% for half")
print(f"  sensitivity = 1 / {FULL_SCALE_AMPS} A = {1 / FULL_SCALE_AMPS:.0f} ohm per volt")

print()
print("Step 3: an ammeter = movement + small parallel resistor (the shunt)")
for amps_range in [0.01, 0.1, 1.0]:
    coil_amps, burden = analog_ammeter_reading(amps_range, amps_range)
    print(f"  {amps_range * 1000:>6.0f} mA range: shunt {shunt_for(amps_range):>8.4f} ohm, "
          f"needle at {needle_percent(coil_amps):.1f}%, voltage across the meter {burden * 1000:.0f} mV")

print()
print("Step 4: an ohmmeter = movement + battery + zero-adjust resistor")
print(f"  {'unknown R (ohm)':>16} {'needle (%)':>11}")
for unknown in [0.0, 150.0, 500.0, 1500.0, 4500.0, 15000.0, 150000.0]:
    print(f"  {unknown:>16.0f} {needle_percent(analog_ohmmeter_reading(unknown)):>11.1f}")
print("  0 ohm is full scale, 1500 ohm is exactly half: the scale is backwards and squashed")

print()
print("Step 5: a digital voltmeter = 10 Mohm divider ladder + a 2000-count, 200 mV converter")
for measured, range_name in [(0.1234, "200 mV"), (1.5, "2 V"), (12.0, "20 V"), (12.0, "200 V"), (230.0, "200 V")]:
    tap_volts, shown = digital_voltmeter_reading(measured, range_name)
    print(f"  measure {measured:>8.4f} V on {range_name:>6}: converter sees {tap_volts * 1000:8.3f} mV, display {shown}")
print("  12 V on the 200 V range loses a digit; 230 V is more than 1999 counts, so the meter shows OL")

print()
print("Step 6: digital current ranges use a shunt and measure its voltage")
for amps, shunt_ohms in [(0.150, 1.0), (0.015, 10.0), (2.5, 0.01)]:
    c = Circuit()
    c.current_source("Ix", "0", "top", amps)
    c.resistor("Rshunt", "top", "0", shunt_ohms)
    burden = c.dc().v("top")
    print(f"  {amps * 1000:>7.1f} mA through a {shunt_ohms:>5} ohm shunt: {burden * 1000:.0f} mV burden voltage")
