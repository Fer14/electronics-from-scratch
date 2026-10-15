import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sim import Circuit

GROUND = "0"


def admittance_of(kind, value, omega):
    if kind == "R":
        return 1 / value
    if kind == "C":
        return 1j * omega * value
    return 1 / (1j * omega * value)


class AcNetlist:
    def __init__(self):
        self.parts = []

    def resistor(self, name, a, b, ohms):
        self.parts.append(("R", name, a, b, ohms))

    def capacitor(self, name, a, b, farads):
        self.parts.append(("C", name, a, b, farads))

    def inductor(self, name, a, b, henries):
        self.parts.append(("L", name, a, b, henries))

    def voltage_source(self, name, plus, minus, phasor=1.0):
        self.parts.append(("V", name, plus, minus, phasor))

    def vcvs(self, name, plus, minus, cplus, cminus, gain):
        self.parts.append(("E", name, plus, minus, (cplus, cminus, gain)))

    def nodes(self):
        names = []
        for part in self.parts:
            nodes = [part[2], part[3]] + (list(part[4][:2]) if part[0] == "E" else [])
            for node in nodes:
                if node != GROUND and node not in names:
                    names.append(node)
        return names

    def build(self, freq):
        omega = 2 * math.pi * freq
        nodes = self.nodes()
        index = {node: i for i, node in enumerate(nodes)}
        branches = [p for p in self.parts if p[0] in ("V", "E")]
        size = len(nodes) + len(branches)
        matrix = np.zeros((size, size), complex)
        rhs = np.zeros(size, complex)

        def add(row, col, value):
            if row is not None and col is not None:
                matrix[row, col] += value

        def at(node):
            return None if node == GROUND else index[node]

        for kind, name, a, b, value in self.parts:
            if kind in ("R", "C", "L"):
                admittance = admittance_of(kind, value, omega)
                add(at(a), at(a), admittance)
                add(at(b), at(b), admittance)
                add(at(a), at(b), -admittance)
                add(at(b), at(a), -admittance)
        for k, (kind, name, a, b, value) in enumerate(branches):
            row = len(nodes) + k
            add(at(a), row, 1)
            add(at(b), row, -1)
            add(row, at(a), 1)
            add(row, at(b), -1)
            if kind == "V":
                rhs[row] = value
            else:
                cplus, cminus, gain = value
                add(row, at(cplus), -gain)
                add(row, at(cminus), gain)
        return nodes, matrix, rhs

    def solve(self, freq):
        nodes, matrix, rhs = self.build(freq)
        x = np.linalg.solve(matrix, rhs)
        voltages = {node: x[i] for i, node in enumerate(nodes)}
        voltages[GROUND] = 0j
        return voltages

    def sweep(self, freqs, node):
        return np.array([self.solve(f)[node] for f in freqs])


def describe(netlist):
    sim = Circuit()
    ours = AcNetlist()
    for kind, name, a, b, value in netlist:
        if kind == "V":
            sim.sine_source(name, a, b, amplitude=1.0, freq=1000.0)
            ours.voltage_source(name, a, b, 1.0)
        elif kind == "E":
            sim.vcvs(name, a, b, *value)
            ours.vcvs(name, a, b, *value)
        else:
            method = {"R": "resistor", "C": "capacitor", "L": "inductor"}[kind]
            getattr(sim, method)(name, a, b, value)
            getattr(ours, method)(name, a, b, value)
    return sim, ours


CIRCUITS = {
    "RC low-pass": [("V", "V1", "in", "0", None), ("R", "R1", "in", "out", 1000.0), ("C", "C1", "out", "0", 100e-9)],
    "RLC band-pass": [("V", "V1", "in", "0", None), ("L", "L1", "in", "a", 10e-3), ("C", "C1", "a", "out", 1e-6),
                      ("R", "R1", "out", "0", 10.0)],
    "LC notch": [("V", "V1", "in", "0", None), ("R", "R1", "in", "out", 1000.0), ("C", "C1", "out", "m", 10e-6),
                 ("L", "L1", "m", "w", 1.0), ("R", "Rw", "w", "0", 10.0)],
    "buffered 2-stage": [("V", "V1", "in", "0", None), ("R", "R1", "in", "mid", 1000.0), ("C", "C1", "mid", "0", 100e-9),
                         ("E", "E1", "buf", "0", ("mid", "0", 1.0)), ("R", "R2", "buf", "out", 1000.0),
                         ("C", "C2", "out", "0", 100e-9)],
}


def save_bode(results, path):
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    for name, (freqs, ours) in results.items():
        top.semilogx(freqs, 20 * np.log10(np.abs(ours)), label=name)
        bottom.semilogx(freqs, np.degrees(np.unwrap(np.angle(ours))), label=name)
    top.set_ylabel("gain (dB)")
    top.set_ylim(-80, 5)
    top.legend(fontsize=8)
    top.grid(True, which="both", alpha=0.3)
    bottom.set_ylabel("phase (deg)")
    bottom.set_xlabel("frequency (Hz)")
    bottom.grid(True, which="both", alpha=0.3)
    fig.suptitle("Bode plots from our hand-built complex MNA")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main():
    print("=== Step 1: The complex MNA matrix of the RC low-pass at fc ===")
    _, rc = describe(CIRCUITS["RC low-pass"])
    fc = 1 / (2 * math.pi * 1000 * 100e-9)
    nodes, matrix, rhs = rc.build(fc)
    print(f"  unknowns: {nodes + ['I(V1)']}")
    for row, b in zip(matrix, rhs):
        cells = "  ".join(f"{v.real:+.4f}{v.imag:+.4f}j" for v in row)
        print(f"  [ {cells} ]   rhs {b.real:+.1f}")
    v_out = rc.solve(fc)["out"]
    print(f"  V(out) at fc = {v_out.real:+.4f} {v_out.imag:+.4f}j, |V| = {abs(v_out):.4f}, phase {math.degrees(np.angle(v_out)):.1f} deg")

    print("\n=== Step 2: Our AC analysis against the simulator's, on four circuits ===")
    freqs = np.logspace(0, 6, 601)
    results = {}
    for name, netlist in CIRCUITS.items():
        sim, ours = describe(netlist)
        mine = ours.sweep(freqs, "out")
        theirs = sim.ac(freqs, source="V1").v("out")
        db_error = np.abs(20 * np.log10(np.abs(mine)) - 20 * np.log10(np.abs(theirs))).max()
        phase_error = np.abs(np.degrees(np.angle(mine / theirs))).max()
        results[name] = (freqs, mine)
        print(f"  {name:<17}: max gain difference {db_error:.2e} dB, max phase difference {phase_error:.2e} deg")

    print("\n=== Step 3: Our RC result against the formula 1 / (1 + j f / fc) ===")
    formula = 1 / (1 + 1j * freqs / fc)
    print(f"  largest |difference| over 1 Hz .. 1 MHz: {np.abs(results['RC low-pass'][1] - formula).max():.2e}")

    print("\n=== Step 4: A phasor is a promise about the time domain ===")
    f_test = 1400.0
    _, rlc = describe(CIRCUITS["RLC band-pass"])
    phasor = rlc.solve(f_test)["out"]
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1.0, freq=f_test)
    c.inductor("L1", "in", "a", 10e-3)
    c.capacitor("C1", "a", "out", 1e-6)
    c.resistor("R1", "out", "0", 10.0)
    period = 1 / f_test
    run = c.transient(t_stop=60 * period, dt=period / 500)
    t = np.asarray(run.time)
    v = np.asarray(run.v("out"))
    last = (t >= 50 * period) & (t < 60 * period)
    reference = np.exp(1j * 2 * math.pi * f_test * t[last])
    measured = 2j * np.mean(v[last] * np.conj(reference))
    print(f"  AC phasor at {f_test:.0f} Hz:       |V| = {abs(phasor):.4f}, phase {math.degrees(np.angle(phasor)):+7.2f} deg")
    print(f"  transient, after settling:  |V| = {abs(measured):.4f}, phase {math.degrees(np.angle(measured)):+7.2f} deg")

    path = Path(__file__).parent / "out.png"
    save_bode(results, path)
    print(f"\nBode plots saved to {path.name}")


if __name__ == "__main__":
    main()
