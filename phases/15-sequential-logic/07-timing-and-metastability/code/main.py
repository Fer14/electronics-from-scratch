import math

import numpy as np

from sim import Circuit, engineering
from sim.logic import ripple_adder


def fmax(tcq, tlogic, tsetup, skew=0.0):
    period = tcq + tlogic + tsetup - skew
    return period, 1 / period


def latch_resolution(imbalance, vdd=5.0, load=1e-12):
    c = Circuit("cross-coupled inverters")
    c.voltage_source("VDD", "vdd", "0", vdd)
    for i, (node, other) in enumerate([("q", "qb"), ("qb", "q")]):
        c.pmos(f"MP{i}", d=node, g=other, s="vdd", vth=1.0, k=1e-3, lam=0.02)
        c.nmos(f"MN{i}", d=node, g=other, s="0", vth=1.0, k=1e-3, lam=0.02)
    c.capacitor("C0", "q", "0", load, v0=vdd / 2 + imbalance)
    c.capacitor("C1", "qb", "0", load, v0=vdd / 2 - imbalance)
    t = c.transient(t_stop=40e-9, dt=0.02e-9)
    return t.time_to_cross("q", 0.8 * vdd)


def mtbf(t_resolve, tau, window, f_clk, f_data):
    return math.exp(t_resolve / tau) / (window * f_clk * f_data)


def main():
    print("=== Setup-time budget: register -> 8-bit ripple adder -> register ===")
    depth = ripple_adder(8).depth()
    for family, gate, tcq, tsetup in [("74HC-like parts at 5 V", 8e-9, 15e-9, 5e-9), ("a modern chip", 15e-12, 40e-12, 25e-12)]:
        tlogic = depth * gate
        period, f = fmax(tcq, tlogic, tsetup)
        print(f"  {family}: tcq {engineering(tcq, 's')} + logic {depth} x {engineering(gate, 's')} = {engineering(tlogic, 's')} + setup {engineering(tsetup, 's')}")
        print(f"    minimum period {engineering(period, 's')}  ->  f_max = {engineering(f, 'Hz')}")

    print("\n=== Clock skew changes the budget ===")
    tcq, tlogic, tsetup = 40e-12, 270e-12, 25e-12
    for skew in [0.0, 20e-12, -20e-12]:
        period, f = fmax(tcq, tlogic, tsetup, skew)
        side = "capture clock late" if skew > 0 else ("capture clock early" if skew < 0 else "no skew")
        print(f"  skew {engineering(skew, 's'):>8s} ({side:19s}): period {engineering(period, 's')}, f_max {engineering(f, 'Hz')}")
    thold, tmin_logic = 15e-12, 10e-12
    for skew in [0.0, 60e-12]:
        slack = tcq + tmin_logic - (thold + skew)
        print(f"  hold check with skew {engineering(skew, 's'):>6s}: tcq + t_min - (t_hold + skew) = {engineering(slack, 's')} -> {'ok' if slack >= 0 else 'HOLD VIOLATION'}")

    print("\n=== Metastability: two CMOS inverters released near their balance point ===")
    imbalances = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
    times = [latch_resolution(d) for d in imbalances]
    for d, t in zip(imbalances, times):
        print(f"  start {engineering(d, 'V'):>8s} away from balance -> resolves in {engineering(t, 's')}")
    slope = np.polyfit(np.log(imbalances), times, 1)[0]
    tau = -slope
    print(f"  every factor 10 closer adds {engineering(tau * math.log(10), 's')}: tau = {engineering(tau, 's')}")
    gm = 1e-3 * (2.5 - 1.0)
    print(f"  estimate tau = C / (gm_n + gm_p) = 1 pF / ({gm * 1e3:.1f} mS + {gm * 1e3:.1f} mS) = {engineering(1e-12 / (2 * gm), 's')}")

    print("\n=== How often does a flip-flop fail to resolve in time? ===")
    rng = np.random.default_rng(15)
    window = 0.2e-9
    offsets = rng.uniform(-5e-9, 5e-9, 2_000_000)
    for t_res in [0.5e-9, 1.0e-9, 1.5e-9]:
        needed = tau * np.log((window / 2) / np.maximum(np.abs(offsets), 1e-30))
        fails = int(np.sum(needed > t_res))
        predicted = len(offsets) * (window / 10e-9) * math.exp(-t_res / tau)
        print(f"  allow {engineering(t_res, 's')}: {fails} of {len(offsets)} random edges unresolved (formula: {predicted:.0f})")

    print("\n=== MTBF of one flip-flop vs a two-flip-flop synchronizer ===")
    f_clk, f_data, w = 100e6, 1e6, 0.2e-9
    one = mtbf(5e-9, tau, w, f_clk, f_data)
    two = mtbf(5e-9 + 10e-9, tau, w, f_clk, f_data)
    year = 365.25 * 24 * 3600
    print(f"  f_clk = 100 MHz, data changes 1 million times per second, tau = {engineering(tau, 's')}, window = 0.2 ns")
    print(f"  one flip-flop, 5 ns to resolve:          MTBF = {one:.3g} s = {one / 3600:.3g} hours")
    print(f"  two flip-flops, 5 ns + a full 10 ns cycle: MTBF = {two:.3g} s = {two / year:.3g} years")


if __name__ == "__main__":
    main()
