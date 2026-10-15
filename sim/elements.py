"""Linear elements and independent sources.

Every element knows its terminals, how many branch-current unknowns it needs, how to
write itself into the equations for each analysis (dc, ic, tran, ac), and how to report
its current and power from a solution vector.

Analysis modes:
  dc    steady state: capacitors are open, inductors are shorts
  ic    the instant t = 0 of a transient: capacitors hold v0, inductors carry i0
  tran  one time step: capacitors and inductors become companion models
  ac    small-signal phasors at angular frequency ctx.omega
"""
import math

import numpy as np

from .stamp import node_voltage


class Element:
    nonlinear = False
    n_branches = 0
    terminals = ("a", "b")
    hidden = False

    def __init__(self, name, nodes):
        self.name = name
        self.node_names = list(nodes)
        self.n = []
        self.k = -1

    def bind(self, index_of, first_branch):
        self.n = [index_of(node) for node in self.node_names]
        self.k = first_branch

    def voltage(self, x, i=0, j=1):
        return node_voltage(x, self.n[i]) - node_voltage(x, self.n[j])

    def stamp(self, s, ctx):
        raise NotImplementedError

    def stamp_ac(self, s, ctx):
        self.stamp(s, ctx)

    def current(self, x, ctx, part=None):
        raise NotImplementedError

    def power(self, x, ctx):
        return self.voltage(x) * self.current(x, ctx)

    def start(self, x, ctx):
        pass

    def accept(self, x, ctx):
        pass


class Resistor(Element):
    def __init__(self, name, a, b, ohms):
        super().__init__(name, [a, b])
        if ohms < 0:
            raise ValueError(f"{name}: resistance cannot be negative, got {ohms}")
        self.ohms = float(ohms)

    @property
    def effective_ohms(self):
        return max(self.ohms, 1e-6)

    def stamp(self, s, ctx):
        s.conductance(self.n[0], self.n[1], 1.0 / self.effective_ohms)

    def current(self, x, ctx, part=None):
        return self.voltage(x) / self.effective_ohms


class Switch(Element):
    def __init__(self, name, a, b, closed=True, ron=1e-3, roff=1e12, toggle_at=()):
        super().__init__(name, [a, b])
        self.closed = bool(closed)
        self.ron = ron
        self.roff = roff
        self.toggle_at = sorted(toggle_at or ())

    def is_closed(self, t):
        flips = sum(1 for moment in self.toggle_at if t >= moment)
        return self.closed != (flips % 2 == 1)

    def resistance(self, t):
        return self.ron if self.is_closed(t) else self.roff

    def stamp(self, s, ctx):
        s.conductance(self.n[0], self.n[1], 1.0 / self.resistance(ctx.t))

    def current(self, x, ctx, part=None):
        t = np.asarray(ctx.t)
        r = np.vectorize(self.resistance)(t) if t.ndim else self.resistance(float(t))
        return self.voltage(x) / r


class Capacitor(Element):
    n_branches = 1

    def __init__(self, name, a, b, farads, v0=0.0):
        super().__init__(name, [a, b])
        self.farads = float(farads)
        self.v0 = float(v0)

    def stamp(self, s, ctx):
        a, b, k = self.n[0], self.n[1], self.k
        s.branch(a, b, k)
        if ctx.mode == "dc":
            s.add(k, k, 1.0)
        elif ctx.mode == "ic":
            s.branch_voltage(k, a, b)
            s.rhs(k, self.v0)
        elif ctx.mode == "tran":
            state = ctx.state[self.name]
            g = self.farads / ctx.dt if ctx.method == "be" else 2.0 * self.farads / ctx.dt
            s.add(k, k, 1.0)
            s.branch_voltage(k, a, b, -g)
            history = -g * state["v"] if ctx.method == "be" else -g * state["v"] - state["i"]
            s.rhs(k, history)
        else:
            s.add(k, k, 1.0)
            s.branch_voltage(k, a, b, -1j * ctx.omega * self.farads)

    def current(self, x, ctx, part=None):
        return x[..., self.k]

    def start(self, x, ctx):
        ctx.state[self.name] = {"v": float(self.voltage(x)), "i": float(x[self.k])}

    accept = start


class Inductor(Element):
    n_branches = 1

    def __init__(self, name, a, b, henries, i0=0.0):
        super().__init__(name, [a, b])
        self.henries = float(henries)
        self.i0 = float(i0)

    def stamp(self, s, ctx):
        a, b, k = self.n[0], self.n[1], self.k
        s.branch(a, b, k)
        if ctx.mode == "dc":
            s.branch_voltage(k, a, b)
        elif ctx.mode == "ic":
            s.add(k, k, 1.0)
            s.rhs(k, self.i0)
        elif ctx.mode == "tran":
            state = ctx.state[self.name]
            r = self.henries / ctx.dt if ctx.method == "be" else 2.0 * self.henries / ctx.dt
            s.branch_voltage(k, a, b)
            s.add(k, k, -r)
            history = -r * state["i"] if ctx.method == "be" else -r * state["i"] - state["v"]
            s.rhs(k, history)
        else:
            s.branch_voltage(k, a, b)
            s.add(k, k, -1j * ctx.omega * self.henries)

    def current(self, x, ctx, part=None):
        return x[..., self.k]

    def start(self, x, ctx):
        ctx.state[self.name] = {"v": float(self.voltage(x)), "i": float(x[self.k])}

    accept = start


class VoltageSource(Element):
    n_branches = 1
    terminals = ("plus", "minus")

    def __init__(self, name, plus, minus, volts=0.0):
        super().__init__(name, [plus, minus])
        self.volts = float(volts)

    def value(self, t):
        return self.volts

    def stamp(self, s, ctx):
        a, b, k = self.n[0], self.n[1], self.k
        s.branch(a, b, k)
        s.branch_voltage(k, a, b)
        if ctx.mode == "ac":
            s.rhs(k, 1.0 if ctx.ac_source == self.name else 0.0)
        else:
            s.rhs(k, ctx.scale * self.value(ctx.t))

    def current(self, x, ctx, part=None):
        return -x[..., self.k]


class PulseSource(VoltageSource):
    def __init__(self, name, plus, minus, low=0.0, high=5.0, period=1e-3, duty=0.5, delay=0.0, rise=0.0, fall=0.0):
        super().__init__(name, plus, minus, low)
        self.low, self.high = float(low), float(high)
        self.period, self.duty, self.delay = float(period), float(duty), float(delay)
        self.rise, self.fall = float(rise), float(fall)

    def value(self, t):
        if t < self.delay:
            return self.low
        phase = (t - self.delay) % self.period
        on_time = self.duty * self.period
        if self.rise > 0 and phase < self.rise:
            return self.low + (self.high - self.low) * phase / self.rise
        if phase < on_time:
            return self.high
        if self.fall > 0 and phase < on_time + self.fall:
            return self.high - (self.high - self.low) * (phase - on_time) / self.fall
        return self.low


class SineSource(VoltageSource):
    def __init__(self, name, plus, minus, amplitude=1.0, freq=50.0, offset=0.0, phase_deg=0.0):
        super().__init__(name, plus, minus, offset)
        self.amplitude, self.freq = float(amplitude), float(freq)
        self.offset, self.phase = float(offset), math.radians(phase_deg)

    def value(self, t):
        return self.offset + self.amplitude * math.sin(2 * math.pi * self.freq * t + self.phase)


class CurrentSource(Element):
    terminals = ("from", "to")

    def __init__(self, name, a, b, amps):
        super().__init__(name, [a, b])
        self.amps = float(amps)

    def stamp(self, s, ctx):
        if ctx.mode == "ac":
            s.inject(self.n[0], self.n[1], 1.0 if ctx.ac_source == self.name else 0.0)
        else:
            s.inject(self.n[0], self.n[1], ctx.scale * self.amps)

    def current(self, x, ctx, part=None):
        return self.amps + 0.0 * x[..., 0].real

    def power(self, x, ctx):
        return -self.voltage(x) * self.current(x, ctx)


class VCVS(Element):
    n_branches = 1
    terminals = ("plus", "minus", "cplus", "cminus")

    def __init__(self, name, plus, minus, cplus, cminus, gain):
        super().__init__(name, [plus, minus, cplus, cminus])
        self.gain = float(gain)

    def stamp(self, s, ctx):
        p, m, cp, cm = self.n
        s.branch(p, m, self.k)
        s.branch_voltage(self.k, p, m)
        s.branch_voltage(self.k, cp, cm, -self.gain)

    def current(self, x, ctx, part=None):
        return -x[..., self.k]

    def power(self, x, ctx):
        return self.voltage(x) * self.current(x, ctx)


class VCCS(Element):
    terminals = ("plus", "minus", "cplus", "cminus")

    def __init__(self, name, plus, minus, cplus, cminus, gm):
        super().__init__(name, [plus, minus, cplus, cminus])
        self.gm = float(gm)

    def stamp(self, s, ctx):
        p, m, cp, cm = self.n
        for row, sign in ((p, 1.0), (m, -1.0)):
            s.add(row, cp, sign * self.gm)
            s.add(row, cm, -sign * self.gm)

    def current(self, x, ctx, part=None):
        return self.gm * self.voltage(x, 2, 3)

    def power(self, x, ctx):
        return -self.voltage(x) * self.current(x, ctx)
