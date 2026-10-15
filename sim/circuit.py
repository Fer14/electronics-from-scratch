"""The Circuit: a named list of elements on named nodes, plus the analyses that solve it.

    c = Circuit()
    c.voltage_source("V1", "vcc", "0", 9.0)
    c.resistor("R1", "vcc", "a", 470)
    c.led("D1", "a", "0", color="red")
    print(c.dc().table())

Ground is the node "0" (alias "gnd"). DC uses modified nodal analysis with Newton-Raphson
for nonlinear parts (with gmin stepping and source stepping as fallbacks), transient uses
backward Euler for the first step and the trapezoidal rule afterwards (or backward Euler
throughout with method="be"), and AC linearizes every device at the DC operating point and
solves the complex equations at each frequency.
"""
import math

import numpy as np
from scipy.linalg import lu_factor, lu_solve

from .devices import BJT, DIODE_MODELS, MOSFET, Diode, OpAmp, led_saturation_current, LED_IDEALITY
from .elements import (VCCS, VCVS, Capacitor, CurrentSource, Inductor, PulseSource, Resistor, SineSource, Switch,
                       VoltageSource)
from .results import ACResult, DCResult, SweepResult, TransientResult
from .stamp import Stamper, solve

GROUND_NAMES = {"0", "gnd", "GND", "ground"}


class ConvergenceError(RuntimeError):
    pass


class Context:
    def __init__(self, mode, t=0.0, dt=None, method="trap", scale=1.0, gmin=1e-12):
        self.mode = mode
        self.t = t
        self.dt = dt
        self.method = method
        self.scale = scale
        self.gmin = gmin
        self.memory = {}
        self.state = {}
        self.limited = False
        self.x = None
        self.xop = None
        self.omega = 0.0
        self.ac_source = None


class Circuit:
    def __init__(self, title=""):
        self.title = title
        self.elements = {}
        self.node_index = {}
        self.size = 0
        self._dirty = True

    def add(self, element):
        if element.name in self.elements:
            raise ValueError(f"duplicate element name {element.name!r}")
        self.elements[element.name] = element
        self._dirty = True
        return element

    def __getitem__(self, name):
        return self.elements[name]

    def resistor(self, name, a, b, ohms):
        return self.add(Resistor(name, a, b, ohms))

    def capacitor(self, name, a, b, farads, v0=0.0):
        return self.add(Capacitor(name, a, b, farads, v0))

    def inductor(self, name, a, b, henries, i0=0.0):
        return self.add(Inductor(name, a, b, henries, i0))

    def voltage_source(self, name, plus, minus, volts):
        return self.add(VoltageSource(name, plus, minus, volts))

    battery = voltage_source

    def current_source(self, name, a, b, amps):
        return self.add(CurrentSource(name, a, b, amps))

    def pulse_source(self, name, plus, minus, low=0.0, high=5.0, period=1e-3, duty=0.5, delay=0.0, rise=0.0, fall=0.0):
        return self.add(PulseSource(name, plus, minus, low, high, period, duty, delay, rise, fall))

    def sine_source(self, name, plus, minus, amplitude=1.0, freq=50.0, offset=0.0, phase_deg=0.0):
        return self.add(SineSource(name, plus, minus, amplitude, freq, offset, phase_deg))

    def switch(self, name, a, b, closed=True, ron=1e-3, roff=1e12, toggle_at=()):
        return self.add(Switch(name, a, b, closed, ron, roff, toggle_at))

    def vcvs(self, name, plus, minus, cplus, cminus, gain):
        return self.add(VCVS(name, plus, minus, cplus, cminus, gain))

    def vccs(self, name, plus, minus, cplus, cminus, gm):
        return self.add(VCCS(name, plus, minus, cplus, cminus, gm))

    def _junction(self, name, anode, cathode, rs, **law):
        if rs and rs > 0:
            inner = f"{name}.junction"
            hidden = self.add(Resistor(f"{name}.rs", anode, inner, rs))
            hidden.hidden = True
            diode = self.add(Diode(name, inner, cathode, **law))
            diode.node_names_shown = [anode, cathode]
            return diode
        return self.add(Diode(name, anode, cathode, **law))

    def diode(self, name, anode, cathode, Is=None, n=None, rs=None, model=None):
        preset = DIODE_MODELS[(model or "default").lower()]
        return self._junction(name, anode, cathode, preset["rs"] if rs is None else rs,
                              Is=preset["Is"] if Is is None else Is, n=preset["n"] if n is None else n)

    def led(self, name, anode, cathode, color="red", rs=0.0):
        return self._junction(name, anode, cathode, rs, Is=led_saturation_current(color), n=LED_IDEALITY)

    def zener(self, name, anode, cathode, vz=5.1, iz=5e-3, Is=1e-14, n=1.0, nz=1.0, rs=0.0):
        return self._junction(name, anode, cathode, rs, Is=Is, n=n, vz=vz, iz=iz, nz=nz)

    def npn(self, name, c, b, e, beta=100.0, Is=1e-14, beta_r=1.0):
        return self.add(BJT(name, c, b, e, beta, Is, beta_r, polarity=1))

    def pnp(self, name, c, b, e, beta=100.0, Is=1e-14, beta_r=1.0):
        return self.add(BJT(name, c, b, e, beta, Is, beta_r, polarity=-1))

    def nmos(self, name, d, g, s, vth=1.0, k=1e-3, lam=0.0):
        return self.add(MOSFET(name, d, g, s, vth, k, lam, polarity=1))

    def pmos(self, name, d, g, s, vth=1.0, k=1e-3, lam=0.0):
        return self.add(MOSFET(name, d, g, s, abs(vth), k, lam, polarity=-1))

    def opamp(self, name, plus, minus, out, gain=1e5, rails=None):
        return self.add(OpAmp(name, plus, minus, out, gain, rails))

    def nodes(self):
        self._bind()
        return list(self.node_index)

    def index(self, node):
        self._bind()
        node = str(node)
        if node in GROUND_NAMES:
            return -1
        if node not in self.node_index:
            raise KeyError(f"unknown node {node!r}; nodes are {sorted(self.node_index)}")
        return self.node_index[node]

    def _bind(self):
        if not self._dirty:
            return
        self.node_index = {}
        for element in self.elements.values():
            for node in element.node_names:
                node = str(node)
                if node not in GROUND_NAMES and node not in self.node_index:
                    self.node_index[node] = len(self.node_index)
        branch = len(self.node_index)
        for element in self.elements.values():
            element.bind(lambda nd: -1 if str(nd) in GROUND_NAMES else self.node_index[str(nd)], branch)
            branch += element.n_branches
        self.size = branch
        self._dirty = False

    @property
    def is_linear(self):
        return not any(e.nonlinear for e in self.elements.values())

    def _assemble(self, ctx, x, extra_gmin=0.0, dtype=float, matrix=True):
        s = Stamper(self.size, dtype, matrix)
        ctx.x = x
        for element in self.elements.values():
            element.stamp(s, ctx)
        if matrix:
            for i in range(len(self.node_index)):
                s.A[i, i] += ctx.gmin + extra_gmin
        return s

    def _newton(self, ctx, x, extra_gmin=0.0, max_iter=150):
        if self.is_linear:
            s = self._assemble(ctx, x, extra_gmin)
            return solve(s.A, s.b)
        for _ in range(max_iter):
            ctx.limited = False
            s = self._assemble(ctx, x, extra_gmin)
            x_new = solve(s.A, s.b)
            if not np.all(np.isfinite(x_new)):
                raise ConvergenceError("solution blew up")
            settled = np.all(np.abs(x_new - x) <= 1e-6 * np.maximum(np.abs(x_new), np.abs(x)) + 1e-9)
            x = x_new
            if settled and not ctx.limited:
                return x
        raise ConvergenceError("Newton-Raphson did not settle")

    def _operating_point(self, ctx, x0=None):
        self._bind()
        x0 = np.zeros(self.size) if x0 is None else x0
        try:
            ctx.memory = {}
            return self._newton(ctx, x0.copy())
        except ConvergenceError:
            pass
        try:
            ctx.memory = {}
            x = x0.copy()
            for g in np.logspace(-2, -12, 21):
                x = self._newton(ctx, x, extra_gmin=g)
            return self._newton(ctx, x)
        except ConvergenceError:
            pass
        ctx.memory = {}
        x = np.zeros(self.size)
        for scale in np.linspace(0.02, 1.0, 50):
            ctx.scale = scale
            x = self._newton(ctx, x, max_iter=400)
        ctx.scale = 1.0
        return x

    def dc(self):
        ctx = Context("dc")
        x = self._operating_point(ctx)
        return DCResult(self, x, ctx)

    op = dc

    def sweep(self, name, values, attribute=None):
        element = self.elements[name]
        attribute = attribute or next(a for a in ("volts", "amps", "ohms", "farads", "henries") if hasattr(element, a))
        original = getattr(element, attribute)
        ctx = Context("dc")
        rows = []
        x = None
        try:
            for value in values:
                setattr(element, attribute, float(value))
                x = self._operating_point(ctx, x)
                rows.append(x)
        finally:
            setattr(element, attribute, original)
        return SweepResult(self, np.asarray(values, float), np.array(rows), ctx)

    def transient(self, t_stop, dt, method="trap", initial="ic"):
        self._bind()
        if method not in ("trap", "be"):
            raise ValueError("method must be 'trap' or 'be'")
        steps = int(round(t_stop / dt))
        times = np.arange(steps + 1) * dt
        ctx = Context("ic" if initial == "ic" else "dc", t=0.0, dt=dt, method=method)
        x = self._operating_point(ctx)
        for element in self.elements.values():
            element.start(x, ctx)
        out = np.zeros((steps + 1, self.size))
        out[0] = x
        ctx.mode = "tran"
        switches = [e for e in self.elements.values() if isinstance(e, Switch)]
        cache = {}
        for n in range(1, steps + 1):
            x = self._advance(ctx, x, times[n - 1], dt, method if n > 1 else "be", switches, cache, depth=0)
            out[n] = x
        return TransientResult(self, times, out, ctx)

    def _advance(self, ctx, x, t0, dt, method, switches, cache, depth):
        ctx.t, ctx.dt, ctx.method = t0 + dt, dt, method
        try:
            if self.is_linear:
                key = (method, dt, tuple(sw.is_closed(ctx.t) for sw in switches))
                if key not in cache:
                    cache[key] = lu_factor(self._assemble(ctx, x).A + 0.0)
                b = self._assemble(ctx, x, matrix=False).b
                x_new = lu_solve(cache[key], b)
            else:
                x_new = self._newton(ctx, x.copy())
        except ConvergenceError:
            if depth > 10:
                raise
            half = self._advance(ctx, x, t0, dt / 2, "be", switches, cache, depth + 1)
            return self._advance(ctx, half, t0 + dt / 2, dt / 2, "be", switches, cache, depth + 1)
        for element in self.elements.values():
            element.accept(x_new, ctx)
        return x_new

    def ac(self, freqs, source=None):
        self._bind()
        freqs = np.atleast_1d(np.asarray(freqs, float))
        if source is None:
            sources = [e for e in self.elements.values() if isinstance(e, (VoltageSource, CurrentSource))]
            sines = [e for e in sources if isinstance(e, SineSource)]
            if not sources:
                raise ValueError("ac() needs a source")
            source = (sines or sources)[0].name
        op_ctx = Context("dc")
        xop = self._operating_point(op_ctx)
        ctx = Context("ac")
        ctx.xop = xop
        ctx.ac_source = source
        out = np.zeros((len(freqs), self.size), complex)
        for row, f in enumerate(freqs):
            ctx.omega = 2 * math.pi * f
            s = Stamper(self.size, complex)
            ctx.x = xop
            for element in self.elements.values():
                element.stamp_ac(s, ctx)
            for i in range(len(self.node_index)):
                s.A[i, i] += ctx.gmin
            out[row] = solve(s.A, s.b)
        return ACResult(self, freqs, out, ctx, source)
