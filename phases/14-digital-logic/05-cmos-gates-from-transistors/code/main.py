from itertools import product

import numpy as np

from sim import Circuit

VDD = 5.0
VTH = 1.0
K = 1e-3


def inverter(k_p=K):
    c = Circuit("CMOS inverter")
    c.voltage_source("VDD", "vdd", "0", VDD)
    c.voltage_source("VIN", "in", "0", 0.0)
    c.pmos("MP", d="out", g="in", s="vdd", vth=VTH, k=k_p)
    c.nmos("MN", d="out", g="in", s="0", vth=VTH, k=K)
    return c


def transfer_curve(k_p=K):
    vin = np.linspace(0.0, VDD, 501)
    sweep = inverter(k_p).sweep("VIN", vin)
    vout = np.asarray(sweep.v("out"))
    supply = np.abs(np.asarray(sweep.i("VDD")))
    return vin, vout, supply


def switching_point(vin, vout):
    index = int(np.argmin(np.abs(vout - vin)))
    return vin[index]


def unity_gain_points(vin, vout):
    slope = np.gradient(vout, vin)
    steep = np.where(slope < -1.0)[0]
    return vin[steep[0]], vin[steep[-1]]


def nand_gate(a, b):
    c = Circuit("CMOS NAND")
    c.voltage_source("VDD", "vdd", "0", VDD)
    c.voltage_source("VA", "a", "0", a)
    c.voltage_source("VB", "b", "0", b)
    c.pmos("MPA", d="out", g="a", s="vdd", vth=VTH, k=K)
    c.pmos("MPB", d="out", g="b", s="vdd", vth=VTH, k=K)
    c.nmos("MNA", d="out", g="a", s="mid", vth=VTH, k=K)
    c.nmos("MNB", d="mid", g="b", s="0", vth=VTH, k=K)
    return c


def nor_gate(a, b):
    c = Circuit("CMOS NOR")
    c.voltage_source("VDD", "vdd", "0", VDD)
    c.voltage_source("VA", "a", "0", a)
    c.voltage_source("VB", "b", "0", b)
    c.pmos("MPA", d="mid", g="a", s="vdd", vth=VTH, k=K)
    c.pmos("MPB", d="out", g="b", s="mid", vth=VTH, k=K)
    c.nmos("MNA", d="out", g="a", s="0", vth=VTH, k=K)
    c.nmos("MNB", d="out", g="b", s="0", vth=VTH, k=K)
    return c


def gate_table(builder, name):
    print(f"  {name}:  a  b |  Vout     bit | supply current")
    for a, b in product((0, 1), repeat=2):
        r = builder(a * VDD, b * VDD).dc()
        vout = r.v("out")
        bit = 1 if vout > VDD / 2 else 0
        print(f"        {a}  {b} | {vout:5.2f} V   {bit}   | {abs(r.i('VDD')):.1e} A")


def switching_energy(load_farads=1e-12, period=1e-6):
    c = Circuit("inverter driving a load")
    c.voltage_source("VDD", "vdd", "0", VDD)
    c.pulse_source("VIN", "in", "0", low=0.0, high=VDD, period=period, duty=0.5, rise=1e-9, fall=1e-9)
    c.pmos("MP", d="out", g="in", s="vdd", vth=VTH, k=K)
    c.nmos("MN", d="out", g="in", s="0", vth=VTH, k=K)
    c.capacitor("CL", "out", "0", load_farads)
    t = c.transient(t_stop=2 * period, dt=period / 4000)
    time = np.asarray(t.time)
    supply = np.abs(np.asarray(t.i("VDD")))
    second = time >= period
    energy = VDD * np.trapezoid(supply[second], time[second])
    return energy, VDD * load_farads * VDD


def main():
    print("=== CMOS inverter, VDD = 5 V, both transistors Vth = 1 V, k = 1 mA/V^2 ===")
    vin, vout, supply = transfer_curve()
    for v in [0.0, 1.0, 2.0, 2.4, 2.6, 3.0, 4.0, 5.0]:
        n = int(round(v / VDD * (len(vin) - 1)))
        print(f"  Vin = {vin[n]:4.2f} V -> Vout = {vout[n]:5.3f} V, supply current = {supply[n] * 1e3:6.3f} mA")
    vm = switching_point(vin, vout)
    vil, vih = unity_gain_points(vin, vout)
    print(f"  switching point (Vout = Vin): {vm:.2f} V")
    print(f"  slope = -1 points: VIL = {vil:.2f} V, VIH = {vih:.2f} V")
    print(f"  noise margins with VOL = 0, VOH = 5 V: NML = {vil:.2f} V, NMH = {VDD - vih:.2f} V")
    peak = 0.5 * K * (VDD / 2 - VTH) ** 2
    print(f"  peak through-current at Vin = 2.5 V: {supply.max() * 1e3:.3f} mA (hand: 0.5 x 1e-3 x (2.5 - 1)^2 = {peak * 1e3:.3f} mA)")
    print(f"  static current with Vin = 0 V: {supply[0]:.1e} A, with Vin = 5 V: {supply[-1]:.1e} A")

    print("\n=== Weaker PMOS (k = 0.4 mA/V^2) moves the switching point ===")
    vin2, vout2, _ = transfer_curve(k_p=0.4e-3)
    r = np.sqrt(K / 0.4e-3)
    hand = (VDD - VTH + r * VTH) / (1 + r)
    print(f"  switching point: {switching_point(vin2, vout2):.2f} V (hand: {hand:.2f} V)")

    print("\n=== CMOS NAND and NOR from four transistors each ===")
    gate_table(nand_gate, "NAND")
    gate_table(nor_gate, "NOR ")

    print("\n=== Dynamic power: charging the load capacitance ===")
    energy, expected = switching_energy()
    print(f"  energy drawn from VDD per cycle with a 1 pF load: {energy * 1e12:.1f} pJ (C x VDD^2 = {expected * 1e12:.1f} pJ)")
    f = 1e6
    print(f"  at {f / 1e6:.0f} MHz that is {energy * f * 1e6:.1f} uW; the same gate at 1.0 V would use {(1.0 / VDD) ** 2 * 100:.0f} % of it")
    chip = 0.1 * 1e-9 * 1.0 ** 2 * 3e9
    print(f"  a chip with 1 nF of switched capacitance, 10 % activity, 1.0 V, 3 GHz: P = 0.1 x 1e-9 x 1.0^2 x 3e9 = {chip:.1f} W")


if __name__ == "__main__":
    main()
