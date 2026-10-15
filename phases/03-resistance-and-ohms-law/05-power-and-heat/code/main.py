import numpy as np


def power_from_voltage_and_current(volts, amps):
    return volts * amps


def power_from_current(amps, ohms):
    return amps**2 * ohms


def power_from_voltage(volts, ohms):
    return volts**2 / ohms


def energy_joules(watts, seconds):
    return watts * seconds


def temperature_rise(watts, kelvin_per_watt):
    return watts * kelvin_per_watt


print("Step 1: power is energy per charge times charge per second")
charge_per_second = 0.5
energy_per_charge = 12.0
print(f"  a battery lifts each coulomb by {energy_per_charge} J (that is {energy_per_charge} V)")
print(f"  {charge_per_second} C pass every second (that is {charge_per_second} A)")
print(f"  energy delivered per second = {energy_per_charge} J/C * {charge_per_second} C/s = "
      f"{energy_per_charge * charge_per_second} J/s = {energy_per_charge * charge_per_second} W")

print()
print("Step 2: three formulas, one answer")
volts = 12.0
ohms = 100.0
amps = volts / ohms
print(f"  12 V across 100 ohm -> I = V / R = {amps:.3f} A")
print(f"  P = V * I     = {power_from_voltage_and_current(volts, amps):.3f} W")
print(f"  P = I^2 * R   = {power_from_current(amps, ohms):.3f} W")
print(f"  P = V^2 / R   = {power_from_voltage(volts, ohms):.3f} W")

print()
print("Step 3: same voltage, different resistors")
print(f"  {'R (ohm)':>10} {'I (mA)':>10} {'P (W)':>10}")
for resistance in [10, 47, 100, 220, 1000, 10000]:
    current = volts / resistance
    print(f"  {resistance:>10} {current * 1000:>10.2f} {power_from_voltage(volts, resistance):>10.4f}")
print("  at fixed voltage, a SMALLER resistor burns MORE power")

print()
print("Step 4: same current, different resistors")
fixed_current = 0.02
print(f"  {'R (ohm)':>10} {'V (V)':>10} {'P (W)':>10}")
for resistance in [10, 47, 100, 220, 1000]:
    print(f"  {resistance:>10} {fixed_current * resistance:>10.2f} {power_from_current(fixed_current, resistance):>10.4f}")
print("  at fixed current, a BIGGER resistor burns MORE power")

print()
print("Step 5: power over time is energy")
heater_watts = power_from_voltage(230.0, 26.45)
for minutes in [1, 10, 60]:
    joules = energy_joules(heater_watts, minutes * 60)
    print(f"  a {heater_watts:.0f} W kettle element running {minutes:>2} min uses {joules:>10.0f} J = {joules / 3.6e6:.3f} kWh")

print()
print("Step 6: how hot does it get? temperature rise = power * thermal resistance")
ambient_celsius = 25.0
packages = {"1/4 W through-hole": 250.0, "1/2 W through-hole": 150.0, "0603 surface-mount": 400.0, "5 W ceramic": 30.0}
dissipated = 0.144
print(f"  dissipating {dissipated} W (12 V across 1 kohm) in ambient air at {ambient_celsius} C")
for name, kelvin_per_watt in packages.items():
    rise = temperature_rise(dissipated, kelvin_per_watt)
    print(f"  {name:<22} {kelvin_per_watt:>6.0f} K/W -> rise {rise:6.1f} K -> body at {ambient_celsius + rise:6.1f} C")

print()
print("Step 7: the lab question - which resistor heats with 1 W to 2 W from 12 V?")
candidates = np.array([47.0, 100.0, 220.0])
powers = volts**2 / candidates
for resistance, watts in zip(candidates, powers):
    verdict = "OK" if 1.0 <= watts <= 2.0 else "out of range"
    print(f"  {resistance:>5.0f} ohm -> {watts:.3f} W  {verdict}")
