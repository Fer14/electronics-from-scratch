import numpy as np

E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]


def tolerance_range(nominal_ohms, tolerance):
    return nominal_ohms * (1 - tolerance), nominal_ohms * (1 + tolerance)


def derated_power(rated_watts, ambient_celsius, knee_celsius=70.0, zero_celsius=155.0):
    if ambient_celsius <= knee_celsius:
        return rated_watts
    if ambient_celsius >= zero_celsius:
        return 0.0
    return rated_watts * (zero_celsius - ambient_celsius) / (zero_celsius - knee_celsius)


def max_safe_voltage(ohms, rated_watts, limiting_volts):
    power_limited_volts = np.sqrt(rated_watts * ohms)
    return min(power_limited_volts, limiting_volts), power_limited_volts


def resistance_at(nominal_ohms, ppm_per_kelvin, celsius, reference_celsius=25.0):
    return nominal_ohms * (1 + ppm_per_kelvin * 1e-6 * (celsius - reference_celsius))


print("Step 1: the E12 series covers every decade with 10% steps")
for decade in [100, 1000]:
    values = [round(v * decade) for v in E12]
    print(f"  {decade:>5} ohm decade: {values}")
print("  each value at +/-10% just about touches its neighbours:")
for low, high in zip(E12[:4], E12[1:5]):
    print(f"    {low * 1000:>5.0f} ohm +10% = {low * 1100:>6.0f}   {high * 1000:>5.0f} ohm -10% = {high * 900:>6.0f}")

print()
print("Step 2: what a tolerance band promises")
for tolerance in [0.01, 0.05, 0.10]:
    low, high = tolerance_range(4700, tolerance)
    print(f"  4.7 kohm +/-{tolerance * 100:.0f}% -> anything from {low:.0f} ohm to {high:.0f} ohm")

print()
print("Step 3: worst case current through 1 kohm +/-5% on a 9 V battery that can sag to 7.5 V")
resistor_low, resistor_high = tolerance_range(1000, 0.05)
battery_low, battery_high = 7.5, 9.6
print(f"  nominal : {9.0 / 1000 * 1000:.2f} mA")
print(f"  minimum : {battery_low:.1f} V / {resistor_high:.0f} ohm = {battery_low / resistor_high * 1000:.2f} mA")
print(f"  maximum : {battery_high:.1f} V / {resistor_low:.0f} ohm = {battery_high / resistor_low * 1000:.2f} mA")

print()
print("Step 4: a bag of 10 000 real resistors (simulated, 5% parts)")
rng = np.random.default_rng(7)
bag = 1000 * (1 + rng.normal(0, 0.05 / 3, size=10_000))
print(f"  mean {bag.mean():.1f} ohm, smallest {bag.min():.1f} ohm, largest {bag.max():.1f} ohm")
print(f"  share within +/-1%: {np.mean(np.abs(bag - 1000) <= 10) * 100:.1f} %")
print(f"  share within +/-5%: {np.mean(np.abs(bag - 1000) <= 50) * 100:.1f} %")
currents = 9.0 / bag * 1000
print(f"  current on 9 V: from {currents.min():.2f} mA to {currents.max():.2f} mA")

print()
print("Step 5: power derating - a 1/4 W resistor in hot air")
for ambient in [25, 70, 85, 100, 125, 155]:
    print(f"  ambient {ambient:>3} C -> may dissipate {derated_power(0.25, ambient):.3f} W")

print()
print("Step 6: voltage rating - big resistors hit a voltage limit before a power limit")
limiting_volts = 250.0
critical_ohms = limiting_volts**2 / 0.25
print(f"  1/4 W part with a 250 V limiting voltage: critical resistance = 250^2 / 0.25 = {critical_ohms:.0f} ohm")
for ohms in [100, 10_000, 250_000, 1_000_000, 10_000_000]:
    allowed, from_power = max_safe_voltage(ohms, 0.25, limiting_volts)
    limit = "power" if from_power < limiting_volts else "voltage"
    print(f"  {ohms:>10} ohm: power allows {from_power:8.1f} V, limit is {allowed:6.1f} V ({limit}-limited)")

print()
print("Step 7: temperature coefficient - resistance drifts with temperature")
for name, ppm in [("carbon film", -500), ("metal film", 50), ("precision foil", 2)]:
    hot = resistance_at(10_000, ppm, 85)
    print(f"  10 kohm {name:<15} {ppm:>5} ppm/K at 85 C -> {hot:9.1f} ohm ({(hot / 10_000 - 1) * 100:+.3f} %)")

print()
print("Step 8: the lab question - USB keep-alive load on 5 V")
for ohms in [100, 150, 220, 330]:
    current = 5.0 / ohms
    power = 5.0**2 / ohms
    current_ok = current >= 0.020
    power_ok = power <= 0.15
    verdict = "OK" if current_ok and power_ok else ("too little current" if not current_ok else "too hot")
    print(f"  {ohms:>4} ohm: {current * 1000:6.1f} mA, {power:.3f} W  {verdict}")
