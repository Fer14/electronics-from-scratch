E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]


def divider_output(v_in, r_top, r_bottom):
    return v_in * r_bottom / (r_top + r_bottom)


def divider_by_kvl(v_in, r_top, r_bottom):
    current = v_in / (r_top + r_bottom)
    v_top = current * r_top
    v_bottom = current * r_bottom
    return current, v_top, v_bottom


def parallel(r_a, r_b):
    return r_a * r_b / (r_a + r_b)


def loaded_output(v_in, r_top, r_bottom, r_load):
    return divider_output(v_in, r_top, parallel(r_bottom, r_load))


def e12_values(low=10.0, high=1e6):
    values = []
    decade = 1.0
    while decade <= high:
        for base in E12:
            value = round(base * decade, 6)
            if low <= value <= high:
                values.append(value)
        decade *= 10
    return values


def best_e12_pair(v_in, v_target, max_current):
    best = None
    for r_top in e12_values():
        for r_bottom in e12_values():
            current = v_in / (r_top + r_bottom)
            if current > max_current:
                continue
            error = abs(divider_output(v_in, r_top, r_bottom) - v_target)
            if best is None or error < best[0] - 1e-12:
                best = (error, r_top, r_bottom)
    return best


def ohms(value):
    if value >= 1e6:
        return f"{value / 1e6:g} MOhm"
    if value >= 1e3:
        return f"{value / 1e3:g} kOhm"
    return f"{value:g} Ohm"


print("Step 1: the divider from KVL and Ohm's law")
v_in, r_top, r_bottom = 9.0, 2000.0, 1000.0
current, v_top, v_bottom = divider_by_kvl(v_in, r_top, r_bottom)
print(f"  Vin = {v_in} V, R1 = {ohms(r_top)}, R2 = {ohms(r_bottom)}")
print(f"  loop current I = Vin / (R1 + R2) = {current * 1000:.3f} mA")
print(f"  V across R1 = I * R1 = {v_top:.3f} V")
print(f"  V across R2 = I * R2 = {v_bottom:.3f} V")
print(f"  KVL check: {v_top:.3f} V + {v_bottom:.3f} V = {v_top + v_bottom:.3f} V (equals Vin)")
print(f"  formula Vin * R2 / (R1 + R2) = {divider_output(v_in, r_top, r_bottom):.3f} V")

print()
print("Step 2: only the ratio matters for the output voltage")
for scale in [0.01, 1, 100]:
    a, b = r_top * scale, r_bottom * scale
    out = divider_output(v_in, a, b)
    i = v_in / (a + b)
    print(f"  R1 = {ohms(a):>10}, R2 = {ohms(b):>10}:  Vout = {out:.3f} V, current = {i * 1000:9.4f} mA, power = {v_in * i * 1000:9.3f} mW")

print()
print("Step 3: loading the divider")
v_in, r_top, r_bottom = 9.0, 10000.0, 10000.0
print(f"  unloaded: 9 V with two {ohms(r_top)} resistors gives {divider_output(v_in, r_top, r_bottom):.3f} V")
for r_load in [1e6, 100e3, 10e3, 1e3, 100.0]:
    out = loaded_output(v_in, r_top, r_bottom, r_load)
    print(f"  load {ohms(r_load):>9}: R2 || Rload = {ohms(round(parallel(r_bottom, r_load), 1)):>12}, Vout = {out:.3f} V ({100 * (out - 4.5) / 4.5:+.1f} %)")

print()
print("Step 4: the divider seen from the output (source voltage and source resistance)")
v_open = divider_output(v_in, r_top, r_bottom)
r_source = parallel(r_top, r_bottom)
print(f"  open-circuit output = {v_open:.3f} V, equivalent resistance R1 || R2 = {ohms(r_source)}")
for r_load in [100e3, 10e3, 1e3]:
    simple = v_open * r_load / (r_source + r_load)
    full = loaded_output(v_in, r_top, r_bottom, r_load)
    print(f"  load {ohms(r_load):>9}: simple model {simple:.4f} V, full circuit {full:.4f} V")

print()
print("Step 5: a potentiometer as an adjustable divider")
pot_total = 10000.0
for position in [0.0, 0.25, 0.5, 0.75, 1.0]:
    lower = pot_total * position
    upper = pot_total - lower
    out = 5.0 * lower / pot_total
    print(f"  wiper at {position * 100:5.1f} %: upper {ohms(upper):>9}, lower {ohms(lower):>9}, Vout = {out:.3f} V")

print()
print("Step 6: designing with standard E12 values")
for v_target, max_current in [(3.3, 0.005), (5.0, 0.001), (1.2, 0.0005)]:
    error, a, b = best_e12_pair(9.0, v_target, max_current)
    out = divider_output(9.0, a, b)
    print(f"  9 V -> {v_target} V, current under {max_current * 1000:g} mA: R1 = {ohms(a)}, R2 = {ohms(b)}, Vout = {out:.3f} V, current = {9.0 / (a + b) * 1000:.3f} mA")
