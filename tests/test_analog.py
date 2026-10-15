"""Analog checks: every analysis against a hand-calculated answer."""
import math

import numpy as np

from sim import Circuit


def close(a, b, rel=1e-3, abs_tol=1e-9):
    return abs(a - b) <= rel * abs(b) + abs_tol


def test_voltage_divider():
    c = Circuit()
    c.voltage_source("V1", "vcc", "0", 9.0)
    c.resistor("R1", "vcc", "out", 1000)
    c.resistor("R2", "out", "gnd", 2000)
    r = c.dc()
    assert close(r.v("out"), 6.0)
    assert close(r.i("R1"), 3e-3)
    assert close(r.i("V1"), 3e-3)
    assert close(r.p("R2"), 2000 * 3e-3 ** 2)
    assert close(r.p("V1"), 9 * 3e-3)
    assert close(r.v("vcc", "out"), 3.0)
    assert "R1" in r.table()


def test_current_source():
    c = Circuit()
    c.current_source("I1", "0", "a", 0.002)
    c.resistor("R1", "a", "0", 1000)
    c.resistor("R2", "a", "0", 1000)
    r = c.dc()
    assert close(r.v("a"), 1.0)
    assert close(r.i("R1"), 1e-3)
    assert close(r.p("I1"), 2e-3)


def test_rc_charging():
    R, C, V = 1000.0, 1e-6, 5.0
    c = Circuit()
    c.voltage_source("V1", "in", "0", V)
    c.resistor("R1", "in", "a", R)
    c.capacitor("C1", "a", "0", C)
    t = c.transient(t_stop=5e-3, dt=1e-6)
    exact = V * (1 - np.exp(-t.time / (R * C)))
    assert np.max(np.abs(t.v("a") - exact)) < 1e-3 * V
    assert close(t.i("C1")[0], V / R, rel=1e-2)
    assert close(t.time_to_cross("a", V * (1 - math.exp(-1))), R * C, rel=1e-3)
    be = c.transient(t_stop=5e-3, dt=1e-6, method="be")
    assert np.max(np.abs(be.v("a") - exact)) < 5e-3 * V


def test_rl_current_rise():
    R, L, V = 100.0, 10e-3, 10.0
    c = Circuit()
    c.voltage_source("V1", "in", "0", V)
    c.resistor("R1", "in", "a", R)
    c.inductor("L1", "a", "0", L)
    t = c.transient(t_stop=5 * L / R, dt=L / R / 1000)
    exact = V / R * (1 - np.exp(-t.time * R / L))
    assert np.max(np.abs(t.i("L1") - exact)) < 1e-3 * V / R
    assert close(c.dc().i("L1"), V / R)


def test_lc_oscillation():
    L, C = 1e-3, 1e-6
    c = Circuit()
    c.capacitor("C1", "a", "0", C, v0=1.0)
    c.inductor("L1", "a", "0", L)
    t = c.transient(t_stop=5e-3, dt=1e-7)
    f = 1 / (2 * math.pi * math.sqrt(L * C))
    assert close(t.frequency("a"), f, rel=1e-3)
    assert close(t.v("a")[-2000:].max(), 1.0, rel=1e-2)


def test_rc_low_pass_cutoff():
    R, C = 1000.0, 100e-9
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=1, freq=1000)
    c.resistor("R1", "in", "out", R)
    c.capacitor("C1", "out", "0", C)
    fc = 1 / (2 * math.pi * R * C)
    a = c.ac([fc / 100, fc, fc * 100], source="V1")
    assert abs(a.gain_db("out")[1] + 3.0103) < 1e-3
    assert abs(a.phase_deg("out")[1] + 45) < 1e-3
    assert abs(a.gain_db("out")[2] + 40) < 0.01
    sweep = c.ac(np.logspace(1, 6, 300))
    assert close(sweep.cutoff("out"), fc, rel=1e-3)


def test_diode_forward_drop():
    c = Circuit()
    c.voltage_source("V1", "in", "0", 5.0)
    c.resistor("R1", "in", "a", 430)
    c.diode("D1", "a", "0")
    r = c.dc()
    vd = r.v("a")
    assert 0.6 < vd < 0.75
    i = (5 - vd) / 430
    assert close(r.i("D1"), i, rel=1e-6)
    assert close(i, 1e-14 * (math.exp(vd / 0.025852) - 1), rel=1e-4)
    c2 = Circuit()
    c2.voltage_source("V1", "in", "0", -5.0)
    c2.resistor("R1", "in", "a", 430)
    c2.diode("D1", "a", "0")
    assert abs(c2.dc().i("D1")) < 1e-12
    c3 = Circuit()
    c3.voltage_source("V1", "in", "0", 5.0)
    c3.resistor("R1", "in", "a", 430)
    c3.diode("D1", "a", "0", model="1n4148")
    assert 0.6 < c3.dc().v("a") < 0.9


def test_led_current():
    for color, low, high in (("red", 1.7, 2.0), ("green", 2.0, 2.4), ("blue", 2.8, 3.2), ("white", 2.9, 3.3)):
        c = Circuit()
        c.voltage_source("V1", "vcc", "0", 9.0)
        c.resistor("R1", "vcc", "a", 680)
        c.led("D1", "a", "0", color=color)
        r = c.dc()
        assert low < r.v("a") < high, (color, r.v("a"))
        assert close(r.i("D1"), (9 - r.v("a")) / 680, rel=1e-6)
    c = Circuit()
    c.current_source("I1", "0", "a", 0.01)
    c.led("D1", "a", "0", color="red")
    assert close(c.dc().v("a"), 1.85, rel=1e-4)


def test_zener_regulation():
    outputs = []
    for supply in (9.0, 12.0, 15.0):
        c = Circuit()
        c.voltage_source("V1", "in", "0", supply)
        c.resistor("R1", "in", "z", 470)
        c.zener("Z1", "0", "z", vz=5.1)
        c.resistor("RL", "z", "0", 2200)
        r = c.dc()
        outputs.append(r.v("z"))
        assert r.i("Z1") < 0
    assert all(5.0 < v < 5.25 for v in outputs), outputs
    assert outputs[-1] - outputs[0] < 0.1


def test_npn_switch_saturation():
    c = Circuit()
    c.voltage_source("VCC", "vcc", "0", 5.0)
    c.voltage_source("VIN", "in", "0", 5.0)
    c.resistor("RB", "in", "b", 4700)
    c.resistor("RC", "vcc", "c", 470)
    c.npn("Q1", c="c", b="b", e="0", beta=100)
    r = c.dc()
    assert r.v("c") < 0.2
    assert 0.6 < r.v("b") < 0.8
    assert close(r.i("Q1"), (5 - r.v("c")) / 470, rel=1e-6)
    assert close(r.i("Q1.e"), r.i("Q1") + r.i("Q1.b"), rel=1e-9)
    c["VIN"].volts = 0.0
    r = c.dc()
    assert r.v("c") > 4.99
    c2 = Circuit()
    c2.voltage_source("VCC", "vcc", "0", 10.0)
    c2.voltage_source("VB", "b", "0", 1.7)
    c2.resistor("RE", "e", "0", 1000)
    c2.resistor("RC", "vcc", "c", 2000)
    c2.npn("Q1", c="c", b="b", e="e", beta=100)
    r = c2.dc()
    assert close(r.i("Q1"), r.i("Q1.b") * 100, rel=1e-3)
    assert 0.9e-3 < r.i("Q1") < 1.1e-3


def test_pnp_and_mosfets():
    c = Circuit()
    c.voltage_source("VCC", "vcc", "0", 5.0)
    c.resistor("RB", "b", "0", 4700)
    c.resistor("RC", "c", "0", 470)
    c.pnp("Q1", c="c", b="b", e="vcc")
    assert c.dc().v("c") > 4.8
    c = Circuit()
    c.voltage_source("VDD", "vdd", "0", 5.0)
    c.voltage_source("VG", "g", "0", 2.0)
    c.resistor("RD", "vdd", "d", 1000)
    c.nmos("M1", d="d", g="g", s="0", vth=1.0, k=2e-3)
    r = c.dc()
    assert close(r.i("M1"), 0.5 * 2e-3 * 1.0 ** 2, rel=1e-6)
    c = Circuit()
    c.voltage_source("VDD", "vdd", "0", 5.0)
    c.voltage_source("VIN", "in", "0", 0.0)
    c.pmos("MP", d="out", g="in", s="vdd", vth=1.0, k=1e-3)
    c.nmos("MN", d="out", g="in", s="0", vth=1.0, k=1e-3)
    c.resistor("RL", "out", "0", 1e6)
    assert c.dc().v("out") > 4.9
    c["VIN"].volts = 5.0
    assert c.dc().v("out") < 0.1


def test_opamp_inverting_gain():
    c = Circuit()
    c.voltage_source("V1", "in", "0", 0.2)
    c.resistor("R1", "in", "n", 1000)
    c.resistor("R2", "n", "out", 10000)
    c.opamp("U1", plus="0", minus="n", out="out")
    assert close(c.dc().v("out"), -2.0, rel=1e-3)
    c.elements["V1"].volts = 2.0
    assert close(c.dc().v("out"), -20.0, rel=1e-3)
    c2 = Circuit()
    c2.voltage_source("V1", "in", "0", 2.0)
    c2.resistor("R1", "in", "n", 1000)
    c2.resistor("R2", "n", "out", 10000)
    c2.opamp("U1", plus="0", minus="n", out="out", rails=(-12, 12))
    assert close(c2.dc().v("out"), -12.0, rel=1e-3)
    c2.elements["V1"].volts = 0.5
    assert close(c2.dc().v("out"), -5.0, rel=1e-3)
    a = c.ac([100.0], source="V1")
    assert abs(a.gain_db("out")[0] - 20.0) < 0.01


def test_comparator_and_noninverting():
    c = Circuit()
    c.voltage_source("V1", "in", "0", 1.0)
    c.voltage_source("V2", "ref", "0", 2.5)
    c.opamp("U1", "in", "ref", "out", rails=(0, 5))
    assert c.dc().v("out") < 0.01
    c["V1"].volts = 3.0
    assert c.dc().v("out") > 4.99
    c = Circuit()
    c.voltage_source("V1", "in", "0", 1.5)
    c.resistor("R1", "n", "0", 1000)
    c.resistor("R2", "out", "n", 1000)
    c.opamp("U1", "in", "n", "out", rails=(0, 5))
    assert close(c.dc().v("out"), 3.0, rel=1e-3)


def test_pulse_and_sine_sources():
    c = Circuit()
    c.pulse_source("V1", "in", "0", low=0, high=5, period=1e-3, duty=0.25)
    c.resistor("R1", "in", "0", 1000)
    t = c.transient(t_stop=4e-3, dt=1e-6)
    assert close(np.mean(t.v("in")), 1.25, rel=1e-2)
    assert close(t.frequency("in"), 1000, rel=1e-3)
    c = Circuit()
    c.sine_source("V1", "in", "0", amplitude=2, freq=50, offset=1)
    c.diode("D1", "in", "out")
    c.resistor("RL", "out", "0", 1000)
    t = c.transient(t_stop=0.1, dt=1e-5)
    assert 2.2 < t.v("out").max() < 2.5
    assert t.v("out").min() > -1e-6


def test_switch_toggle_and_sweep():
    c = Circuit()
    c.voltage_source("V1", "in", "0", 5.0)
    c.switch("S1", "in", "a", closed=False, toggle_at=[1e-3])
    c.resistor("R1", "a", "b", 1000)
    c.capacitor("C1", "b", "0", 1e-6)
    t = c.transient(t_stop=3e-3, dt=1e-6)
    assert t.at(0.9e-3, "b") < 1e-6
    assert close(t.at(2e-3, "b"), 5 * (1 - math.exp(-1)), rel=1e-2)
    c = Circuit()
    c.voltage_source("V1", "in", "0", 0.0)
    c.resistor("R1", "in", "a", 100)
    c.diode("D1", "a", "0")
    s = c.sweep("V1", np.linspace(0, 5, 51))
    assert s.i("D1")[0] == 0 or abs(s.i("D1")[0]) < 1e-12
    assert np.all(np.diff(s.v("a")) >= -1e-12)
