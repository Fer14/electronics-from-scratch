import numpy as np

from sim import Circuit
from sim.logic import LogicCircuit, LogicSettleError


def inverter_ring(stages):
    lc = LogicCircuit(f"ring of {stages} inverters")
    names = [f"n{i}" for i in range(stages)]
    for i, name in enumerate(names):
        lc.not_(name, names[i - 1])
    lc.outputs(*names)
    return lc


def nor_latch():
    lc = LogicCircuit("cross-coupled NOR latch")
    lc.inputs("s", "r")
    lc.nor("q", "r", "qb")
    lc.nor("qb", "s", "q")
    lc.outputs("q", "qb")
    return lc


def cmos_ring(stages=3, load=1e-12):
    c = Circuit(f"{stages}-stage CMOS ring oscillator")
    c.voltage_source("VDD", "vdd", "0", 5.0)
    names = [f"n{i}" for i in range(stages)]
    for i, name in enumerate(names):
        c.pmos(f"MP{i}", d=name, g=names[i - 1], s="vdd", vth=1.0, k=1e-3)
        c.nmos(f"MN{i}", d=name, g=names[i - 1], s="0", vth=1.0, k=1e-3)
        c.capacitor(f"C{i}", name, "0", load, v0=5.0 if i % 2 == 0 else 0.0)
    return c


def unit_delay_run(lc, start, steps):
    values = dict(start)
    history = [dict(values)]
    for _ in range(steps):
        values = {**values, **{gate.output: gate.evaluate(values) for gate in lc.gates}}
        history.append(dict(values))
    return history


def main():
    print("=== Two inverters in a loop hold either value ===")
    pair = inverter_ring(2)
    first = pair.settle()
    print(f"  after power-up:          n0 = {first['n0']}, n1 = {first['n1']}")
    kicked = pair.settle({"n1": 1})
    print(f"  kick n1 to 1, let go:    n0 = {kicked['n0']}, n1 = {kicked['n1']}")
    again = pair.settle()
    print(f"  nothing touched:         n0 = {again['n0']}, n1 = {again['n1']}  (it remembers)")
    kicked = pair.settle({"n1": 0})
    print(f"  kick n1 to 0, let go:    n0 = {kicked['n0']}, n1 = {kicked['n1']}")

    print("\n=== Three inverters in a loop never settle ===")
    ring = inverter_ring(3)
    try:
        ring.settle()
        print("  settled (unexpected)")
    except LogicSettleError as error:
        print(f"  settle() says: {error}")
    history = unit_delay_run(ring, {"n0": 1, "n1": 1, "n2": 0}, 12)
    for t, values in enumerate(history):
        print(f"  t = {t:2d}: n0 n1 n2 = {values['n0']} {values['n1']} {values['n2']}")
    rises = [t for t in range(1, len(history)) if history[t]["n0"] == 1 and history[t - 1]["n0"] == 0]
    print(f"  n0 rises at t = {rises}: period = {rises[1] - rises[0]} gate delays = 2 x 3 stages, so f = 1 / (2 N tpd)")

    print("\n=== The same ring with real transistors (sim Circuit, 1 pF per node) ===")
    osc = cmos_ring()
    t = osc.transient(t_stop=100e-9, dt=0.05e-9)
    f = t.frequency("n0")
    tpd = 1 / (2 * 3 * f)
    print(f"  oscillation frequency: {f / 1e6:.0f} MHz")
    print(f"  implied delay per inverter: tpd = 1 / (2 x 3 x f) = {tpd * 1e9:.2f} ns")
    print(f"  compare R_on x C = 250 ohm x 1 pF = {250 * 1e-12 * 1e9:.2f} ns (same order)")
    v = np.asarray(t.v("n0"))
    print(f"  n0 swings between {v[len(v) // 2:].min():.2f} V and {v[len(v) // 2:].max():.2f} V")

    print("\n=== Cross-coupled NOR gates: a memory you can write ===")
    latch = nor_latch()
    for label, s, r in [("set   ", 1, 0), ("hold  ", 0, 0), ("reset ", 0, 1), ("hold  ", 0, 0), ("set   ", 1, 0), ("hold  ", 0, 0)]:
        out = latch.evaluate({"s": s, "r": r})
        print(f"  {label} s={s} r={r} -> q={out['q']} qb={out['qb']}")


if __name__ == "__main__":
    main()
