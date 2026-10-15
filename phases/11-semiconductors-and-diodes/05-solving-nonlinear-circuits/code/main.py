from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

THERMAL_VOLTAGE = 0.025852
SATURATION_CURRENT = 1e-14
SOURCE_VOLTS = 5.0
RESISTOR_OHMS = 1000.0


def diode_current(volts):
    return SATURATION_CURRENT * (np.exp(volts / THERMAL_VOLTAGE) - 1.0)


def diode_slope(volts):
    return SATURATION_CURRENT * np.exp(volts / THERMAL_VOLTAGE) / THERMAL_VOLTAGE


def mismatch(volts):
    return (SOURCE_VOLTS - volts) / RESISTOR_OHMS - diode_current(volts)


def mismatch_slope(volts):
    return -1.0 / RESISTOR_OHMS - diode_slope(volts)


def naive_fixed_point(start, steps):
    volts = start
    history = [volts]
    for _ in range(steps):
        amps = diode_current(volts)
        volts = SOURCE_VOLTS - amps * RESISTOR_OHMS
        history.append(volts)
    return history


def log_fixed_point(start, tolerance=1e-9, limit=100):
    volts = start
    history = [volts]
    for _ in range(limit):
        amps = (SOURCE_VOLTS - volts) / RESISTOR_OHMS
        new_volts = THERMAL_VOLTAGE * np.log(amps / SATURATION_CURRENT + 1.0)
        history.append(new_volts)
        if abs(new_volts - volts) < tolerance:
            break
        volts = new_volts
    return history


def bisection(low, high, tolerance=1e-9, limit=200):
    history = []
    for _ in range(limit):
        middle = 0.5 * (low + high)
        history.append(middle)
        if mismatch(middle) > 0:
            low = middle
        else:
            high = middle
        if high - low < tolerance:
            break
    return history


KNEE_VOLTS = THERMAL_VOLTAGE * np.log(THERMAL_VOLTAGE / SATURATION_CURRENT)


def hold_back(new_volts, old_volts):
    base = max(old_volts, KNEE_VOLTS)
    if new_volts > base + 2 * THERMAL_VOLTAGE:
        return base + THERMAL_VOLTAGE * np.log(1 + (new_volts - base) / THERMAL_VOLTAGE)
    return new_volts


def newton(start, tolerance=1e-9, limit=300, careful=False):
    volts = start
    history = [volts]
    for _ in range(limit):
        proposal = volts - mismatch(volts) / mismatch_slope(volts)
        if careful:
            proposal = hold_back(proposal, volts)
        step = proposal - volts
        volts = proposal
        history.append(volts)
        if abs(step) < tolerance:
            break
    return history


def show_methods():
    print(f"Circuit: {SOURCE_VOLTS} V source -> {RESISTOR_OHMS:.0f} ohm -> silicon diode -> ground")
    print("Unknown: the diode voltage V. Equation: (5 - V)/1000 = I_S (e^(V/V_T) - 1)")
    print()
    print("1) Naive guess-and-repeat: V -> diode current -> V = 5 - I R")
    for step, volts in enumerate(naive_fixed_point(0.6, 4)):
        print(f"   step {step}: V = {volts:.6g} V")
    print("   It explodes: each pass makes the error bigger.")
    print()
    history = log_fixed_point(0.0)
    print(f"2) Rearranged guess-and-repeat: V -> resistor current -> V = V_T ln(I/I_S + 1)   ({len(history) - 1} steps)")
    for step, volts in enumerate(history[:6]):
        print(f"   step {step}: V = {volts:.9f} V")
    print(f"   final: V = {history[-1]:.9f} V")
    print()
    history = bisection(0.0, SOURCE_VOLTS)
    print(f"3) Bisection between 0 V and 5 V: {len(history)} halvings to reach 1 nV, V = {history[-1]:.9f} V")
    print()
    history = newton(0.6)
    print(f"4) Plain Newton-Raphson from V = 0.6 V ({len(history) - 1} steps)")
    for step, volts in enumerate(history):
        if step <= 3 or step >= len(history) - 4:
            print(f"   step {step:>3}: V = {volts:.12f} V   current mismatch = {abs(mismatch(volts)):.3e} A")
        elif step == 4:
            print("   ...      (each step only 25.85 mV lower: crawling down the exponential wall)")
    print()
    for start in [0.0, 0.6, 0.8]:
        plain = newton(start)
        careful = newton(start, careful=True)
        print(f"5) Start at {start:.1f} V: plain Newton {len(plain) - 1:>3} steps, Newton with junction hold-back {len(careful) - 1:>2} steps")
    print()
    history = newton(0.6, careful=True)
    print(f"6) Newton with hold-back from 0.6 V, step by step")
    for step, volts in enumerate(history):
        print(f"   step {step}: V = {volts:.12f} V   current mismatch = {abs(mismatch(volts)):.3e} A")
    print()
    return history[-1]


def diode_companion(volts):
    conductance = diode_slope(volts)
    equivalent_current = diode_current(volts) - conductance * volts
    return conductance, equivalent_current


def solve_two_diode_network(tolerance=1e-9, limit=100):
    nodes = {"in": 0, "a": 1, "b": 2}
    resistors = [("in", "a", 1000.0), ("a", "b", 2200.0)]
    diode_anodes = ["a", "b"]
    size = len(nodes) + 1
    guess = np.zeros(size)
    junctions = {anode: 0.6 for anode in diode_anodes}
    print("Two-diode network solved by hand-built Newton + modified nodal analysis")
    print(f"  {'iter':>4} {'V(in)':>9} {'V(a)':>12} {'V(b)':>12} {'largest change':>15}")
    for iteration in range(1, limit + 1):
        matrix = np.zeros((size, size))
        right = np.zeros(size)
        for first, second, ohms in resistors:
            g = 1.0 / ohms
            i, j = nodes[first], nodes[second]
            matrix[i, i] += g
            matrix[j, j] += g
            matrix[i, j] -= g
            matrix[j, i] -= g
        for anode in diode_anodes:
            k = nodes[anode]
            junction = hold_back(guess[k], junctions[anode]) if iteration > 1 else junctions[anode]
            junctions[anode] = junction
            conductance, equivalent_current = diode_companion(junction)
            matrix[k, k] += conductance
            right[k] -= equivalent_current
        source_row = len(nodes)
        matrix[nodes["in"], source_row] += 1.0
        matrix[source_row, nodes["in"]] += 1.0
        right[source_row] = SOURCE_VOLTS
        new_guess = np.linalg.solve(matrix, right)
        change = np.max(np.abs(new_guess[:3] - guess[:3]))
        held = any(abs(junctions[a] - new_guess[nodes[a]]) > tolerance for a in diode_anodes)
        guess = new_guess
        print(f"  {iteration:>4} {guess[0]:>9.4f} {guess[1]:>12.8f} {guess[2]:>12.8f} {change:>15.3e}")
        if change < tolerance and not held:
            break
    return {"in": guess[0], "a": guess[1], "b": guess[2]}


def simulate_two_diode_network():
    circuit = Circuit()
    circuit.voltage_source("V1", "in", "0", SOURCE_VOLTS)
    circuit.resistor("R1", "in", "a", 1000.0)
    circuit.diode("D1", "a", "0", Is=SATURATION_CURRENT, n=1.0)
    circuit.resistor("R2", "a", "b", 2200.0)
    circuit.diode("D2", "b", "0", Is=SATURATION_CURRENT, n=1.0)
    return circuit.dc()


def compare(single_answer):
    circuit = Circuit()
    circuit.voltage_source("V1", "in", "0", SOURCE_VOLTS)
    circuit.resistor("R1", "in", "a", RESISTOR_OHMS)
    circuit.diode("D1", "a", "0", Is=SATURATION_CURRENT, n=1.0)
    result = circuit.dc()
    print("Single diode: ours versus the simulator")
    print(f"  ours      V = {single_answer:.9f} V   I = {(SOURCE_VOLTS - single_answer) / RESISTOR_OHMS * 1000:.6f} mA")
    print(f"  simulator V = {result.v('a'):.9f} V   I = {result.i('R1') * 1000:.6f} mA")
    print()
    ours = solve_two_diode_network()
    simulated = simulate_two_diode_network()
    print("Two-diode network: ours versus the simulator")
    for node in ["a", "b"]:
        print(f"  V({node}) ours = {ours[node]:.9f} V   simulator = {simulated.v(node):.9f} V   difference = {abs(ours[node] - simulated.v(node)):.1e} V")
    print(f"  D1 current = {simulated.i('D1') * 1000:.4f} mA, D2 current = {simulated.i('D2') * 1000:.4f} mA")
    print()


def plot_load_line(answer):
    volts = np.linspace(0.0, 0.8, 400)
    figure, (left, right) = plt.subplots(1, 2, figsize=(10, 4))
    left.plot(volts, (SOURCE_VOLTS - volts) / RESISTOR_OHMS * 1000, label="resistor: (5 - V)/1k")
    left.plot(volts, diode_current(volts) * 1000, label="diode: I_S e^(V/V_T)")
    left.plot([answer], [(SOURCE_VOLTS - answer) / RESISTOR_OHMS * 1000], "o", label="operating point")
    left.set_ylim(0, 8)
    left.set_xlabel("diode voltage V (volts)")
    left.set_ylabel("current (mA)")
    left.set_title("load line: where both parts agree")
    left.legend()
    for label, history in [("Newton with hold-back", newton(0.6, careful=True)), ("plain Newton", newton(0.6)), ("rearranged repeat", log_fixed_point(0.0)), ("bisection", bisection(0.0, SOURCE_VOLTS))]:
        errors = [max(abs(v - answer), 1e-16) for v in history]
        right.semilogy(range(len(errors)), errors, marker=".", label=label)
    right.set_xlabel("iteration")
    right.set_ylabel("error in V (volts)")
    right.set_title("how fast each method closes in")
    right.legend()
    figure.tight_layout()
    path = Path(__file__).parent / "out.png"
    figure.savefig(path, dpi=120)
    print(f"Saved the load line and convergence plot to {path.name}")


def main():
    answer = show_methods()
    compare(answer)
    plot_load_line(answer)


if __name__ == "__main__":
    main()
