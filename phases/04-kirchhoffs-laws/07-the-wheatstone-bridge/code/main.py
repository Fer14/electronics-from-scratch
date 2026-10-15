import numpy as np


def divider_output(v_in, r_top, r_bottom):
    return v_in * r_bottom / (r_top + r_bottom)


def bridge_output(v_in, r1, r2, r3, r4):
    v_left = divider_output(v_in, r1, r2)
    v_right = divider_output(v_in, r3, r4)
    return v_left, v_right, v_left - v_right


def balancing_r4(r1, r2, r3):
    return r2 * r3 / r1


def unknown_from_reading(v_in, r1, r2, r3, v_measured):
    v_left = divider_output(v_in, r1, r2)
    v_right = v_left - v_measured
    return r3 * v_right / (v_in - v_right)


def bridge_with_meter(v_in, r1, r2, r3, r4, r_meter):
    g1, g2, g3, g4, gm = 1 / r1, 1 / r2, 1 / r3, 1 / r4, 1 / r_meter
    conductance_matrix = np.array([[g1 + g2 + gm, -gm], [-gm, g3 + g4 + gm]])
    injected = np.array([v_in * g1, v_in * g3])
    v_left, v_right = np.linalg.solve(conductance_matrix, injected)
    return v_left, v_right, (v_left - v_right) / r_meter


def pt100(temperature_c):
    return 100.0 * (1 + 0.00385 * temperature_c)


print("Step 1: a bridge is two dividers side by side")
v_in = 9.0
r1, r2, r3, r4 = 1000.0, 2000.0, 1500.0, 2200.0
v_left, v_right, v_out = bridge_output(v_in, r1, r2, r3, r4)
print(f"  Vin = {v_in} V, left arm R1 = {r1:g} / R2 = {r2:g} Ohm, right arm R3 = {r3:g} / R4 = {r4:g} Ohm")
print(f"  left midpoint  = 9 x {r2:g}/{r1 + r2:g} = {v_left:.4f} V")
print(f"  right midpoint = 9 x {r4:g}/{r3 + r4:g} = {v_right:.4f} V")
print(f"  bridge output (left - right) = {v_out * 1000:.2f} mV")

print()
print("Step 2: the balance condition R1 x R4 = R2 x R3")
r4_balanced = balancing_r4(r1, r2, r3)
v_left, v_right, v_out = bridge_output(v_in, r1, r2, r3, r4_balanced)
print(f"  R4 = R2 x R3 / R1 = {r2:g} x {r3:g} / {r1:g} = {r4_balanced:g} Ohm")
print(f"  left = {v_left:.4f} V, right = {v_right:.4f} V, output = {v_out * 1000:.4f} mV")
for scale in [0.5, 2.0]:
    v_left, v_right, v_out = bridge_output(scale * v_in, r1, r2, r3, r4_balanced)
    print(f"  same resistors on {scale * v_in:g} V: output = {v_out * 1000:.4f} mV (balance does not depend on the supply)")

print()
print("Step 3: sweeping the unknown arm")
r_ref = 1000.0
for r_unknown in [900.0, 950.0, 990.0, 1000.0, 1010.0, 1050.0, 1100.0]:
    _, _, v_out = bridge_output(5.0, r_ref, r_ref, r_ref, r_unknown)
    print(f"  R4 = {r_unknown:7.1f} Ohm: output = {v_out * 1000:+8.2f} mV")

print()
print("Step 4: finding the unknown from a measured output")
for true_value in [1234.0, 870.0]:
    _, _, reading = bridge_output(5.0, r_ref, r_ref, r_ref, true_value)
    rounded_reading = round(reading, 5)
    recovered = unknown_from_reading(5.0, r_ref, r_ref, r_ref, rounded_reading)
    print(f"  meter shows {rounded_reading * 1000:+.2f} mV -> R4 = {recovered:.2f} Ohm (true value {true_value:g} Ohm)")

print()
print("Step 5: sensitivity, a strain gauge in a quarter bridge")
gauge, gauge_factor, v_supply = 350.0, 2.0, 5.0
for microstrain in [100, 500, 1000]:
    delta_r = gauge * gauge_factor * microstrain * 1e-6
    _, _, v_out = bridge_output(v_supply, gauge, gauge, gauge, gauge + delta_r)
    approx = v_supply * delta_r / (4 * gauge)
    single = divider_output(v_supply, gauge, gauge + delta_r)
    print(f"  {microstrain:5d} microstrain: dR = {delta_r:.3f} Ohm, bridge output = {v_out * 1000:+.4f} mV (approx -V dR / 4R = {-approx * 1000:+.4f} mV), single divider reads {single:.5f} V")

print()
print("Step 6: a Pt100 temperature sensor in a bridge balanced at 0 C")
for temperature in [0, 25, 50, 100]:
    _, _, v_out = bridge_output(3.3, 1000.0, 100.0, 1000.0, pt100(temperature))
    print(f"  {temperature:4d} C: Pt100 = {pt100(temperature):7.3f} Ohm, output = {v_out * 1000:+8.3f} mV")

print()
print("Step 7: a real meter between the midpoints (KCL at both midpoints, 2x2 system)")
for r_meter in [1e9, 10e3, 100.0]:
    v_left, v_right, i_meter = bridge_with_meter(5.0, 1000.0, 1000.0, 1000.0, 1050.0, r_meter)
    print(f"  meter resistance {r_meter:>8g} Ohm: left = {v_left:.4f} V, right = {v_right:.4f} V, meter current = {i_meter * 1e6:+9.3f} uA")
v_left, v_right, i_meter = bridge_with_meter(5.0, 1000.0, 1000.0, 1000.0, 1000.0, 100.0)
print(f"  balanced bridge with a 100 Ohm meter: meter current = {abs(i_meter) * 1e6:.3f} uA")
