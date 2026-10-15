from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUTPUT_PATH = Path(__file__).parent / "out.png"

ROOM_KELVIN = 300.0
LAMP_RATED_VOLTS = 12.0
LAMP_RATED_WATTS = 5.0
LAMP_HOT_KELVIN = 2700.0
TUNGSTEN_EXPONENT = 1.2

lamp_hot_ohms = LAMP_RATED_VOLTS**2 / LAMP_RATED_WATTS
lamp_cold_ohms = lamp_hot_ohms / (LAMP_HOT_KELVIN / ROOM_KELVIN) ** TUNGSTEN_EXPONENT
radiation_constant = LAMP_RATED_WATTS / (LAMP_HOT_KELVIN**4 - ROOM_KELVIN**4)


def lamp_resistance(kelvin):
    return lamp_cold_ohms * (kelvin / ROOM_KELVIN) ** TUNGSTEN_EXPONENT


def heat_balance(kelvin, volts):
    electrical_in = volts**2 / lamp_resistance(kelvin)
    radiated_out = radiation_constant * (kelvin**4 - ROOM_KELVIN**4)
    return electrical_in - radiated_out


def lamp_filament_temperature(volts):
    low, high = ROOM_KELVIN, 5000.0
    for _ in range(100):
        middle = (low + high) / 2
        if heat_balance(middle, volts) > 0:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def lamp_current(volts):
    if volts == 0:
        return 0.0
    return volts / lamp_resistance(lamp_filament_temperature(volts))


def thermistor_resistance(celsius, ohms_at_25=10_000.0, beta=3950.0):
    kelvin = celsius + 273.15
    return ohms_at_25 * np.exp(beta * (1 / kelvin - 1 / 298.15))


def diode_current(volts, saturation_amps=1e-14, thermal_volts=0.02585):
    return saturation_amps * (np.exp(volts / thermal_volts) - 1)


print("Step 1: an ordinary resistor - the ratio V / I never changes")
for volts in [1.0, 2.0, 5.0, 10.0]:
    amps = volts / 100.0
    print(f"  V = {volts:5.1f} V  I = {amps * 1000:6.1f} mA  V/I = {volts / amps:6.1f} ohm")

print()
print("Step 2: a 12 V 5 W tungsten lamp")
print(f"  hot resistance (at 12 V)   = 12^2 / 5 = {lamp_hot_ohms:.1f} ohm")
print(f"  cold resistance (at 300 K) = {lamp_cold_ohms:.2f} ohm")
print(f"  ratio hot / cold           = {lamp_hot_ohms / lamp_cold_ohms:.1f}")
print(f"  {'V (V)':>6} {'T (K)':>7} {'I (mA)':>8} {'V/I (ohm)':>10}")
lamp_volts = [0.1, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0]
for volts in lamp_volts:
    kelvin = lamp_filament_temperature(volts)
    amps = lamp_current(volts)
    print(f"  {volts:>6.1f} {kelvin:>7.0f} {amps * 1000:>8.1f} {volts / amps:>10.2f}")

print()
print("Step 3: inrush - the first instant after switch-on the filament is still cold")
inrush = LAMP_RATED_VOLTS / lamp_cold_ohms
steady = LAMP_RATED_VOLTS / lamp_hot_ohms
print(f"  first instant: 12 V / {lamp_cold_ohms:.2f} ohm = {inrush:.2f} A")
print(f"  once hot     : 12 V / {lamp_hot_ohms:.1f} ohm  = {steady:.3f} A")
print(f"  the lamp briefly draws {inrush / steady:.0f} times its normal current")

print()
print("Step 4: static versus dynamic resistance of the lamp at 6 V")
step = 0.01
static = 6.0 / lamp_current(6.0)
dynamic = (2 * step) / (lamp_current(6.0 + step) - lamp_current(6.0 - step))
print(f"  static  V / I        = {static:.2f} ohm")
print(f"  dynamic dV / dI      = {dynamic:.2f} ohm")

print()
print("Step 5: an NTC thermistor (10 kohm at 25 C, B = 3950 K)")
for celsius in [0, 25, 50, 75, 100]:
    print(f"  {celsius:>4} C -> {thermistor_resistance(celsius):9.0f} ohm")

print()
print("Step 6: a silicon diode - no single resistance at all")
print(f"  {'V (V)':>6} {'I':>14} {'V/I':>16}")
for volts in [0.3, 0.5, 0.6, 0.65, 0.7, 0.75]:
    amps = diode_current(volts)
    print(f"  {volts:>6.2f} {amps:>12.3e} A {volts / amps:>12.3e} ohm")
reverse = diode_current(-1.0)
print(f"  reverse -1.00 V -> {reverse * 1e15:.2f} fA (it blocks: about {1.0 / abs(reverse):.1e} ohm)")

print()
print("Step 7: the ohmic test - fit a straight line through the I-V points")
volts_grid = np.array(lamp_volts)
lamp_amps = np.array([lamp_current(v) for v in volts_grid])
resistor_amps = volts_grid / lamp_hot_ohms
for name, amps in [("resistor", resistor_amps), ("lamp", lamp_amps)]:
    slope = np.sum(volts_grid * amps) / np.sum(volts_grid**2)
    worst = np.max(np.abs(amps - slope * volts_grid) / amps) * 100
    print(f"  {name:<9} best straight line misses a point by up to {worst:6.2f} %")

figure, axes = plt.subplots(1, 3, figsize=(12, 3.6))
sweep = np.linspace(0, 12, 61)
axes[0].plot(sweep, sweep / lamp_hot_ohms * 1000, label="28.8 ohm resistor")
axes[0].plot(sweep, [lamp_current(v) * 1000 for v in sweep], label="12 V 5 W lamp")
axes[0].set_xlabel("voltage (V)")
axes[0].set_ylabel("current (mA)")
axes[0].set_title("lamp vs resistor")
axes[0].legend()
temperatures = np.linspace(0, 100, 101)
axes[1].plot(temperatures, thermistor_resistance(temperatures) / 1000)
axes[1].set_xlabel("temperature (C)")
axes[1].set_ylabel("resistance (kohm)")
axes[1].set_title("NTC thermistor")
diode_volts = np.linspace(0, 0.78, 200)
axes[2].plot(diode_volts, diode_current(diode_volts) * 1000)
axes[2].set_xlabel("voltage (V)")
axes[2].set_ylabel("current (mA)")
axes[2].set_title("silicon diode")
figure.tight_layout()
figure.savefig(OUTPUT_PATH, dpi=120)
print()
print(f"saved {OUTPUT_PATH.name}")
