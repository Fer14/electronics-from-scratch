from sim import Circuit

HIDDEN_EMF = 1.55
HIDDEN_R = 0.18


def battery_with_load(emf, internal_ohms, load_ohms):
    c = Circuit()
    c.voltage_source("E", "emf", "0", emf)
    c.resistor("Rint", "emf", "plus", internal_ohms)
    c.resistor("RL", "plus", "0", load_ohms)
    return c.dc()


def measure_terminal(load_ohms):
    r = battery_with_load(HIDDEN_EMF, HIDDEN_R, load_ohms)
    return round(r.v("plus"), 3), round(r.i("RL"), 4)


def internal_resistance_from_two_loads(v1, i1, v2, i2):
    return (v1 - v2) / (i2 - i1)


print("Step 1: find a hidden internal resistance with two measurements")
v_open, i_open = measure_terminal(10e6)
v_light, i_light = measure_terminal(10.0)
v_heavy, i_heavy = measure_terminal(2.0)
print(f"  no load (10 Mohm meter only): V = {v_open:.3f} V, I = {i_open * 1000:.4f} mA")
print(f"  10 ohm load:                  V = {v_light:.3f} V, I = {i_light:.4f} A")
print(f"  2 ohm load:                   V = {v_heavy:.3f} V, I = {i_heavy:.4f} A")
r_from_open = (v_open - v_light) / i_light
r_from_two = internal_resistance_from_two_loads(v_light, i_light, v_heavy, i_heavy)
print(f"  r from open and 10 ohm  = ({v_open:.3f} - {v_light:.3f}) / {i_light:.4f} = {r_from_open:.3f} ohm")
print(f"  r from 10 ohm and 2 ohm = ({v_light:.3f} - {v_heavy:.3f}) / ({i_heavy:.4f} - {i_light:.4f}) = {r_from_two:.3f} ohm")
print(f"  the hidden value was {HIDDEN_R} ohm")

print()
print("Step 2: where the energy goes (EMF 9 V, r = 2 ohm)")
print(f"  {'load (ohm)':>10} {'I (A)':>8} {'P load (W)':>11} {'P inside (W)':>13} {'efficiency':>11}")
for load in [100.0, 20.0, 10.0, 4.0, 2.0, 1.0, 0.5]:
    r = battery_with_load(9.0, 2.0, load)
    p_load = r.p("RL")
    p_inside = r.p("Rint")
    print(f"  {load:>10.1f} {r.i('RL'):>8.3f} {p_load:>11.3f} {p_inside:>13.3f} {p_load / (p_load + p_inside):>10.1%}")
print("  efficiency = R_L / (R_L + r): a light load wastes little, a heavy load wastes a lot")

print()
print("Step 3: four AA cells (1.5 V, 0.2 ohm each), three ways, into a 4 ohm load")


def stack_in_series(cells):
    c = Circuit()
    node = "0"
    for k in range(cells):
        top = f"n{k + 1}"
        c.voltage_source(f"E{k}", f"m{k}", node, 1.5)
        c.resistor(f"R{k}", f"m{k}", top, 0.2)
        node = top
    c.resistor("RL", node, "0", 4.0)
    r = c.dc()
    return r.v(node), r.i("RL")


def stack_in_parallel(cells):
    c = Circuit()
    for k in range(cells):
        c.voltage_source(f"E{k}", f"m{k}", "0", 1.5)
        c.resistor(f"R{k}", f"m{k}", "out", 0.2)
    c.resistor("RL", "out", "0", 4.0)
    r = c.dc()
    return r.v("out"), r.i("RL")


def two_by_two():
    c = Circuit()
    for string in range(2):
        c.voltage_source(f"Ea{string}", f"a{string}", "0", 1.5)
        c.resistor(f"Ra{string}", f"a{string}", f"mid{string}", 0.2)
        c.voltage_source(f"Eb{string}", f"b{string}", f"mid{string}", 1.5)
        c.resistor(f"Rb{string}", f"b{string}", "out", 0.2)
    c.resistor("RL", "out", "0", 4.0)
    r = c.dc()
    return r.v("out"), r.i("RL")


for name, (v, i), emf, r_total in [
    ("4 in series      ", stack_in_series(4), 6.0, 0.8),
    ("4 in parallel    ", stack_in_parallel(4), 1.5, 0.05),
    ("2 series x 2 par.", two_by_two(), 3.0, 0.2),
]:
    print(f"  {name}: EMF {emf:.1f} V, r {r_total:.2f} ohm -> V load {v:.3f} V, I {i:.3f} A")
print("  series adds EMF and r; parallel keeps EMF and divides r")

print()
print("Step 4: the same aging cell in a remote (75 ohm) and in a camera (1.5 ohm)")
print(f"  {'r (ohm)':>8} {'V remote (V)':>13} {'V camera (V)':>13}")
for r_aged in [0.15, 0.3, 0.6, 1.0, 1.5]:
    v_remote = battery_with_load(1.5, r_aged, 75.0).v("plus")
    v_camera = battery_with_load(1.5, r_aged, 1.5).v("plus")
    print(f"  {r_aged:>8.2f} {v_remote:>13.3f} {v_camera:>13.3f}")
print("  if the camera needs 1.1 V, the cell is 'dead' for it once r passes about 0.55 ohm,")
print("  but the remote still sees almost 1.5 V")

print()
print("Step 5: starting a car (12.6 V, r = 0.01 ohm, starter = 0.07 ohm, lamps = 1.2 ohm)")
c = Circuit()
c.voltage_source("E", "emf", "0", 12.6)
c.resistor("Rint", "emf", "plus", 0.01)
c.resistor("Rlamps", "plus", "0", 1.2)
before = c.dc()
c.switch("S1", "plus", "st", closed=True)
c.resistor("Rstarter", "st", "0", 0.07)
during = c.dc()
print(f"  lamps only:        V = {before.v('plus'):.2f} V, lamp power {before.p('Rlamps'):.1f} W")
print(f"  while cranking:    V = {during.v('plus'):.2f} V, lamp power {during.p('Rlamps'):.1f} W, "
      f"starter current {during.i('Rstarter'):.0f} A")
