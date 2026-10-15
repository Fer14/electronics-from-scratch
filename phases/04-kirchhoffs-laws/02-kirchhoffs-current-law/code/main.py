import numpy as np


def milliamps(amps):
    return f"{round(amps * 1000, 9) + 0.0:8.3f} mA"


def current_through(resistor, voltages):
    name, node_from, node_to, ohms = resistor
    return (voltages[node_from] - voltages[node_to]) / ohms


def leaving_current_at(node, branches, branch_currents):
    total = 0.0
    for (name, node_from, node_to, _), current in zip(branches, branch_currents):
        if node_from == node:
            total += current
        if node_to == node:
            total -= current
    return total


print("Part 1: a junction with five wires")
print("-----------------------------------")
known = {"wire 1 (in)": 0.120, "wire 2 (in)": 0.045, "wire 3 (out)": -0.080, "wire 4 (out)": -0.030}
for name, amps in known.items():
    print(f"  {name:<14} {milliamps(abs(amps))} {'arriving' if amps > 0 else 'leaving'}")
arriving = sum(amps for amps in known.values() if amps > 0)
leaving = -sum(amps for amps in known.values() if amps < 0)
unknown = arriving - leaving
print(f"  total arriving  = {milliamps(arriving)}")
print(f"  total leaving   = {milliamps(leaving)} (not counting wire 5)")
print(f"  KCL: wire 5 must carry {milliamps(unknown)} {'out of' if unknown > 0 else 'into'} the junction")
print()

print("Part 2: what if KCL were broken by just 1 mA?")
print("----------------------------------------------")
mismatch = 0.001
node_capacitance = 10e-12
seconds = [1e-9, 1e-6, 1e-3]
for t in seconds:
    piled_charge = mismatch * t
    voltage = piled_charge / node_capacitance
    print(f"  after {t:8.0e} s: extra charge {piled_charge:9.2e} C, node voltage would rise by {voltage:12.4g} V")
print("  a real node holds only ~10 pF, so even 1 mA of imbalance would push its voltage")
print("  up by about a hundred thousand volts per millisecond. The voltage adjusts almost instantly until")
print("  the currents balance. That balance is Kirchhoff's current law.")
print()

print("Part 3: use KCL to find the unknown node voltage")
print("------------------------------------------------")
supply = 9.0
r_feed, r_left, r_right = 1000.0, 2000.0, 6000.0
print(f"  battery {supply} V from vcc to gnd")
print(f"  R1 = {r_feed:.0f} ohm from vcc to a, R2 = {r_left:.0f} ohm from a to gnd, R3 = {r_right:.0f} ohm from a to gnd")


def imbalance_at_a(v_a):
    arriving = (supply - v_a) / r_feed
    leaving = v_a / r_left + v_a / r_right
    return arriving - leaving


low, high = 0.0, supply
for step in range(40):
    middle = (low + high) / 2
    if imbalance_at_a(middle) > 0:
        low = middle
    else:
        high = middle
v_a_search = (low + high) / 2
print("  guessing v(a) and checking 'in minus out' at node a:")
for guess in [3.0, 5.0, 5.4, 6.0, 8.0]:
    print(f"    v(a) = {guess:4.1f} V -> in - out = {milliamps(imbalance_at_a(guess))}")
print(f"  bisection search (40 halvings) finds v(a) = {v_a_search:.6f} V")

v_a_algebra = (supply / r_feed) / (1 / r_feed + 1 / r_left + 1 / r_right)
print(f"  algebra: v(a) = (9/1000) / (1/1000 + 1/2000 + 1/6000) = {v_a_algebra:.6f} V")
print()

print("Part 4: check KCL at every node of the solved circuit")
print("-----------------------------------------------------")
voltages = {"vcc": supply, "a": v_a_algebra, "gnd": 0.0}
resistors = [("R1", "vcc", "a", r_feed), ("R2", "a", "gnd", r_left), ("R3", "a", "gnd", r_right)]
resistor_currents = [current_through(resistor, voltages) for resistor in resistors]
battery_current = resistor_currents[0]
branches = resistors + [("B1", "gnd", "vcc", None)]
branch_currents = resistor_currents + [battery_current]
for (name, node_from, node_to, ohms), current in zip(branches, branch_currents):
    label = f"{ohms:.0f} ohm" if ohms else "battery"
    print(f"  {name} ({label:>9}) carries {milliamps(current)} from {node_from} to {node_to}")
for node in ["vcc", "a", "gnd"]:
    print(f"  node {node:>3}: sum of currents leaving = {round(leaving_current_at(node, branches, branch_currents), 15) + 0.0:+.3e} A")
print()

print("Part 5: the same check written as a matrix (incidence matrix)")
print("-------------------------------------------------------------")
nodes = ["vcc", "a", "gnd"]
incidence = np.zeros((len(nodes), len(branches)))
for column, (name, node_from, node_to, _) in enumerate(branches):
    incidence[nodes.index(node_from), column] = 1
    incidence[nodes.index(node_to), column] = -1
print("  rows = nodes, columns = branches, +1 = branch leaves node, -1 = branch enters node")
print("         " + "".join(f"{name:>6}" for name, *_ in branches))
for node, row in zip(nodes, incidence):
    print(f"  {node:>5}  " + "".join(f"{value:6.0f}" for value in row))
print(f"  incidence @ currents = {np.round(incidence @ np.array(branch_currents), 15) + 0.0} A")
print("  every entry is zero (up to rounding): KCL holds at every node")
