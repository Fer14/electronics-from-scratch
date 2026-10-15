import numpy as np

ELECTRON_CHARGE = 1.602e-19
ELECTRON_MASS = 9.109e-31
COPPER_FREE_ELECTRONS_PER_M3 = 8.5e28
COPPER_MEAN_FREE_TIME = 2.5e-14


def current_from_drift(volts, length_m, area_m2, electrons_per_m3, mean_free_time):
    field = volts / length_m
    drift = ELECTRON_CHARGE * field * mean_free_time / ELECTRON_MASS
    return electrons_per_m3 * ELECTRON_CHARGE * area_m2 * drift


def current(volts, ohms):
    return volts / ohms


def voltage(amps, ohms):
    return amps * ohms


def resistance(volts, amps):
    return volts / amps


def fit_resistance(volts, amps):
    slope, intercept = np.polyfit(amps, volts, 1)
    return slope, intercept


def ascii_iv_plot(curves, v_max, i_max, width=50, height=12):
    grid = [[" "] * width for _ in range(height)]
    for symbol, ohms in curves:
        for column in range(width):
            v = v_max * column / (width - 1)
            row = round((current(v, ohms) / i_max) * (height - 1))
            if 0 <= row < height:
                grid[height - 1 - row][column] = symbol
    lines = [f"  {i_max * 1000:5.1f} mA |" + "".join(grid[0])]
    lines += ["           |" + "".join(r) for r in grid[1:]]
    lines.append("     0 mA  +" + "-" * width)
    lines.append(f"            0 V{' ' * (width - 8)}{v_max:.0f} V")
    return "\n".join(lines)


print("Step 1: Ohm's law from the drift picture")
length = 1.0
area = 0.1e-6
for volts in [0.01, 0.02, 0.04, 0.08]:
    amps = current_from_drift(volts, length, area, COPPER_FREE_ELECTRONS_PER_M3, COPPER_MEAN_FREE_TIME)
    print(f"  1 m of 0.1 mm^2 copper, {volts * 1000:4.0f} mV applied -> {amps * 1000:7.2f} mA   V/I = {volts / amps:.4f} ohm")
predicted = ELECTRON_MASS * length / (COPPER_FREE_ELECTRONS_PER_M3 * ELECTRON_CHARGE**2 * COPPER_MEAN_FREE_TIME * area)
print(f"  formula R = m L / (n e^2 tau A) = {predicted:.4f} ohm, the same for every voltage")

print()
print("Step 2: a bench measurement of a 1 kohm resistor")
rng = np.random.default_rng(3)
supply_volts = np.arange(0.0, 10.5, 1.0)
true_ohms = 1000.0
measured_ma = (supply_volts / true_ohms) * 1000 + rng.normal(0, 0.02, supply_volts.size)
print("   V (V)   I (mA)   V/I (ohm)")
for v, i_ma in zip(supply_volts, measured_ma):
    ratio = f"{v / (i_ma / 1000):8.0f}" if v > 0 else "     ---"
    print(f"  {v:6.1f}  {i_ma:7.3f}  {ratio}")
slope, intercept = fit_resistance(supply_volts, measured_ma / 1000)
print(f"  best straight line V = R I + b: R = {slope:.1f} ohm, b = {intercept * 1000:.1f} mV")

print()
print("Step 3: the I-V graph of three resistors (steeper line = smaller resistance)")
print(ascii_iv_plot([("a", 500.0), ("b", 1000.0), ("c", 2000.0)], v_max=10.0, i_max=0.020))
print("  a = 500 ohm, b = 1 kohm, c = 2 kohm")

print()
print("Step 4: the three forms of Ohm's law")
print(f"  I = V / R : 9 V across 1 kohm          -> {current(9.0, 1000.0) * 1000:.1f} mA")
print(f"  I = V / R : 5 V across 220 ohm         -> {current(5.0, 220.0) * 1000:.1f} mA")
print(f"  V = I R   : 20 mA through 330 ohm      -> {voltage(0.020, 330.0):.2f} V")
print(f"  V = I R   : 2 A through 0.05 ohm wire  -> {voltage(2.0, 0.05):.2f} V")
print(f"  R = V / I : 12 V gives 0.5 A           -> {resistance(12.0, 0.5):.1f} ohm")
print(f"  R = V / I : 3.3 V gives 1.5 mA         -> {resistance(3.3, 0.0015):.0f} ohm")

print()
print("Step 5: design a resistor for a target current")
for supply, target_ma in [(9.0, 9.0), (5.0, 10.0), (12.0, 2.5)]:
    ohms = resistance(supply, target_ma / 1000)
    print(f"  {supply:4.1f} V supply, want {target_ma:4.1f} mA -> R = {ohms:,.0f} ohm")
