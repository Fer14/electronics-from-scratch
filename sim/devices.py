"""Nonlinear devices: diode, LED, zener, BJT, MOSFET and the op-amp with rails.

Each device gives, at a guessed set of terminal voltages, the current flowing into each
terminal and how fast those currents change with each terminal voltage (the Jacobian).
Newton-Raphson replaces the device by that straight-line model, solves, and repeats.

Exponential junctions can jump to absurd currents when a guess overshoots, so each
junction voltage is held back: once a junction conducts well, a voltage step is shrunk
to the step that would give the current the straight-line model predicted. Any held-back
step marks the iteration as not converged yet.
"""
import math

import numpy as np

from .elements import Element
from .stamp import node_voltage

THERMAL_VOLTAGE = 0.025852
EXP_CAP = 80.0

LED_COLORS = {
    "infrared": 1.25,
    "red": 1.85,
    "orange": 1.95,
    "yellow": 2.05,
    "green": 2.2,
    "blue": 3.0,
    "white": 3.1,
    "uv": 3.2,
}
LED_IDEALITY = 2.0
LED_REFERENCE_CURRENT = 0.010

DIODE_MODELS = {
    "default": {"Is": 1e-14, "n": 1.0, "rs": 0.0},
    "1n4148": {"Is": 2.5e-9, "n": 1.75, "rs": 0.6},
    "1n4007": {"Is": 7e-9, "n": 1.8, "rs": 0.04},
    "schottky": {"Is": 1e-6, "n": 1.05, "rs": 0.1},
}


def safe_exp(u):
    u = np.asarray(u, dtype=float)
    capped = np.minimum(u, EXP_CAP)
    return np.exp(capped) * (1.0 + np.maximum(u - EXP_CAP, 0.0))


def turn_on_voltage(saturation_current, nvt):
    return nvt * math.log(nvt / saturation_current)


def hold_back(v_new, v_old, saturation_current, nvt, knee=None):
    if knee is None:
        knee = turn_on_voltage(saturation_current, nvt)
    base = max(v_old, knee)
    if v_new > base + 2.0 * nvt:
        return base + nvt * math.log1p((v_new - base) / nvt), True
    return v_new, False


def led_saturation_current(color):
    if color not in LED_COLORS:
        raise ValueError(f"unknown LED color {color!r}; choose from {sorted(LED_COLORS)}")
    nvt = LED_IDEALITY * THERMAL_VOLTAGE
    return LED_REFERENCE_CURRENT / math.expm1(LED_COLORS[color] / nvt)


class Diode(Element):
    nonlinear = True
    terminals = ("anode", "cathode")

    def __init__(self, name, anode, cathode, Is=1e-14, n=1.0, vz=None, iz=5e-3, nz=1.0):
        super().__init__(name, [anode, cathode])
        self.Is = float(Is)
        self.nvt = n * THERMAL_VOLTAGE
        self.vz = vz
        self.iz = iz
        self.nzvt = nz * THERMAL_VOLTAGE

    def reverse_knee(self):
        return self.vz + self.nzvt * math.log(self.nzvt / self.iz)

    def law(self, v):
        e = safe_exp(v / self.nvt)
        i = self.Is * (e - 1.0)
        g = self.Is * e / self.nvt
        if self.vz is not None:
            er = safe_exp(-(v + self.vz) / self.nzvt)
            i = i - self.iz * er
            g = g + self.iz * er / self.nzvt
        return i, g

    def junction_voltage(self, x, ctx):
        v_new = float(self.voltage(x))
        v_old = ctx.memory.get(self.name, 0.0)
        if v_new >= 0 or self.vz is None:
            v, held = hold_back(v_new, v_old, self.Is, self.nvt)
        else:
            w, held = hold_back(-v_new, -v_old, None, self.nzvt, knee=self.reverse_knee())
            v = -w
        ctx.memory[self.name] = v
        ctx.limited |= held
        return v

    def stamp(self, s, ctx):
        if ctx.mode == "ac":
            v = float(self.voltage(ctx.xop))
            s.conductance(self.n[0], self.n[1], float(self.law(v)[1]))
            return
        v = self.junction_voltage(ctx.x, ctx)
        i, g = self.law(v)
        i, g = float(i), float(g) + ctx.gmin
        s.conductance(self.n[0], self.n[1], g)
        s.inject(self.n[0], self.n[1], i - g * v + ctx.gmin * v)

    def current(self, x, ctx, part=None):
        return self.law(self.voltage(x))[0]


class BJT(Element):
    nonlinear = True
    terminals = ("c", "b", "e")

    def __init__(self, name, c, b, e, beta=100.0, Is=1e-14, beta_r=1.0, polarity=1):
        super().__init__(name, [c, b, e])
        self.beta = float(beta)
        self.beta_r = float(beta_r)
        self.Is = float(Is)
        self.polarity = polarity

    def law(self, vbe, vbc):
        vt = THERMAL_VOLTAGE
        ef, er = safe_exp(vbe / vt), safe_exp(vbc / vt)
        forward, reverse = self.Is * (ef - 1.0), self.Is * (er - 1.0)
        gf, gr = self.Is * ef / vt, self.Is * er / vt
        ic = forward - reverse - reverse / self.beta_r
        ib = forward / self.beta + reverse / self.beta_r
        dic = (gf, -gr - gr / self.beta_r)
        dib = (gf / self.beta, gr / self.beta_r)
        return ic, ib, dic, dib

    def junctions(self, x):
        p = self.polarity
        vc, vb, ve = (node_voltage(x, i) for i in self.n)
        return p * (vb - ve), p * (vb - vc)

    def linearize(self, vbe, vbc):
        p = self.polarity
        ic, ib, dic, dib = self.law(vbe, vbc)
        ic, ib = float(ic), float(ib)
        dic, dib = [float(v) for v in dic], [float(v) for v in dib]
        row_c = [-dic[1], dic[0] + dic[1], -dic[0]]
        row_b = [-dib[1], dib[0] + dib[1], -dib[0]]
        row_e = [-(row_c[i] + row_b[i]) for i in range(3)]
        currents = [p * ic, p * ib, -p * (ic + ib)]
        return currents, [row_c, row_b, row_e]

    def stamp(self, s, ctx):
        if ctx.mode == "ac":
            currents, jac = self.linearize(*[float(v) for v in self.junctions(ctx.xop)])
            s.linearized(self.n, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], jac)
            return
        vbe_new, vbc_new = (float(v) for v in self.junctions(ctx.x))
        old = ctx.memory.get(self.name, (0.0, 0.0))
        vbe, held_be = hold_back(vbe_new, old[0], self.Is, THERMAL_VOLTAGE)
        vbc, held_bc = hold_back(vbc_new, old[1], self.Is, THERMAL_VOLTAGE)
        ctx.memory[self.name] = (vbe, vbc)
        ctx.limited |= held_be or held_bc
        p = self.polarity
        ve = float(node_voltage(ctx.x, self.n[2]))
        vb = ve + p * vbe
        vc = vb - p * vbc
        currents, jac = self.linearize(vbe, vbc)
        s.linearized(self.n, [vc, vb, ve], currents, jac)
        s.conductance(self.n[1], self.n[2], ctx.gmin)
        s.conductance(self.n[1], self.n[0], ctx.gmin)

    def current(self, x, ctx, part=None):
        ic, ib, _, _ = self.law(*self.junctions(x))
        if part == "b":
            return ib
        if part == "e":
            return ic + ib
        return ic

    def power(self, x, ctx):
        vbe, vbc = self.junctions(x)
        ic, ib, _, _ = self.law(vbe, vbc)
        return (vbe - vbc) * ic + vbe * ib


class MOSFET(Element):
    nonlinear = True
    terminals = ("d", "g", "s")

    def __init__(self, name, d, g, s, vth=1.0, k=1e-3, lam=0.0, polarity=1):
        super().__init__(name, [d, g, s])
        self.vth = float(vth)
        self.kp = float(k)
        self.lam = float(lam)
        self.polarity = polarity

    def law(self, vgs, vds):
        vov = vgs - self.vth
        if vov <= 0:
            return 0.0, 0.0, 0.0
        if vds < vov:
            i = self.kp * (vov * vds - 0.5 * vds * vds) * (1 + self.lam * vds)
            gm = self.kp * vds * (1 + self.lam * vds)
            gds = self.kp * (vov - vds) * (1 + self.lam * vds) + self.kp * (vov * vds - 0.5 * vds * vds) * self.lam
            return i, gm, gds
        i = 0.5 * self.kp * vov * vov * (1 + self.lam * vds)
        return i, self.kp * vov * (1 + self.lam * vds), 0.5 * self.kp * vov * vov * self.lam

    def terminal_voltages(self, x):
        vd, vg, vs = (node_voltage(x, i) for i in self.n)
        return vd, vg, vs

    def channel(self, vd, vg, vs):
        p = self.polarity
        if p * (vd - vs) >= 0:
            i, gm, gds = self.law(p * (vg - vs), p * (vd - vs))
            return p * i, gm, gds, False
        i, gm, gds = self.law(p * (vg - vd), p * (vs - vd))
        return -p * i, gm, gds, True

    def jacobian(self, vd, vg, vs):
        i, gm, gds, swapped = self.channel(vd, vg, vs)
        if not swapped:
            row_d = [gds, gm, -gm - gds]
        else:
            row_d = [gm + gds, -gm, -gds]
        row_s = [-v for v in row_d]
        return [i, 0.0, -i], [row_d, [0.0, 0.0, 0.0], row_s]

    def stamp(self, s, ctx):
        if ctx.mode == "ac":
            _, jac = self.jacobian(*(float(v) for v in self.terminal_voltages(ctx.xop)))
            s.linearized(self.n, [0.0] * 3, [0.0] * 3, jac)
            return
        vd, vg, vs = (float(v) for v in self.terminal_voltages(ctx.x))
        vgs, vds = vg - vs, vd - vs
        old = ctx.memory.get(self.name)
        if old is not None:
            step_gs = max(-1.0, min(1.0, vgs - old[0]))
            step_ds = max(-2.0, min(2.0, vds - old[1]))
            ctx.limited |= step_gs != vgs - old[0] or step_ds != vds - old[1]
            vgs, vds = old[0] + step_gs, old[1] + step_ds
        ctx.memory[self.name] = (vgs, vds)
        vg, vd = vs + vgs, vs + vds
        currents, jac = self.jacobian(vd, vg, vs)
        s.linearized(self.n, [vd, vg, vs], currents, jac)
        s.conductance(self.n[0], self.n[2], ctx.gmin)

    def current(self, x, ctx, part=None):
        vd, vg, vs = self.terminal_voltages(x)
        values = np.vectorize(lambda a, b, c: self.channel(a, b, c)[0])(vd, vg, vs)
        return self.polarity * values if np.ndim(values) else self.polarity * float(values)

    def power(self, x, ctx):
        vd, _, vs = self.terminal_voltages(x)
        return (vd - vs) * self.polarity * self.current(x, ctx)


class OpAmp(Element):
    n_branches = 1
    terminals = ("plus", "minus", "out")

    def __init__(self, name, plus, minus, out, gain=1e5, rails=None):
        super().__init__(name, [plus, minus, out])
        self.gain = float(gain)
        self.rails = tuple(float(r) for r in rails) if rails is not None else None
        self.nonlinear = rails is not None

    def transfer(self, vd):
        if self.rails is None:
            return self.gain * vd, self.gain
        lo, hi = self.rails
        mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
        u = self.gain * vd / half
        if abs(u) > 40:
            return mid + half * math.copysign(1.0, u), 0.0
        th = math.tanh(u)
        return mid + half * th, self.gain * (1.0 - th * th)

    def stamp(self, s, ctx):
        p, m, o = self.n
        k = self.k
        s.branch(o, -1, k)
        s.add(k, o, 1.0)
        x = ctx.xop if ctx.mode == "ac" else ctx.x
        vd = float(self.voltage(x, 0, 1))
        if self.rails is not None and ctx.mode != "ac":
            old = ctx.memory.get(self.name)
            half = 0.5 * (self.rails[1] - self.rails[0])
            reach = 4.0 * half / self.gain
            if old is not None and abs(vd - old) > reach and abs(old) < reach:
                vd = old + math.copysign(reach, vd - old)
                ctx.limited = True
            ctx.memory[self.name] = vd
        out, slope = self.transfer(vd)
        s.branch_voltage(k, p, m, -slope)
        if ctx.mode != "ac":
            s.rhs(k, out - slope * vd)

    def current(self, x, ctx, part=None):
        return -x[..., self.k]

    def power(self, x, ctx):
        return node_voltage(x, self.n[2]) * self.current(x, ctx)
