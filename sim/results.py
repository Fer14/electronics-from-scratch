"""Result objects: read voltages, currents and powers out of a solved circuit.

Current directions: resistor, switch, capacitor, inductor from a to b; diode, LED and
zener from anode to cathode; a voltage source reports the current leaving its plus
terminal; a current source reports its own value; transistors report the collector or
drain current (add ".b" or ".e" for a BJT's base or emitter current). Power is what a
part turns into heat (or stores), and what a source delivers.
"""
import math

import numpy as np

from .stamp import node_voltage


def _plain(value):
    if np.ndim(value) == 0:
        value = complex(value) if np.iscomplexobj(value) else float(value)
    return value


def _split(name):
    if "." in name and not name.endswith((".rs", ".junction")):
        base, part = name.rsplit(".", 1)
        return base, part
    return name, None


class _Result:
    def __init__(self, circuit, x, ctx):
        self.circuit = circuit
        self.x = x
        self.ctx = ctx

    def v(self, node, ref=None):
        value = node_voltage(self.x, self.circuit.index(node))
        if ref is not None:
            value = value - node_voltage(self.x, self.circuit.index(ref))
        return _plain(value)

    def _element(self, name):
        base, part = _split(name)
        if base not in self.circuit.elements:
            raise KeyError(f"unknown element {name!r}")
        return self.circuit.elements[base], part

    def i(self, name):
        element, part = self._element(name)
        return _plain(element.current(self.x, self.ctx, part))

    def p(self, name):
        element, _ = self._element(name)
        return _plain(element.power(self.x, self.ctx))


def engineering(value, unit):
    if value == 0 or not math.isfinite(value):
        return f"{value:.4g} {unit}"
    prefixes = [(1e9, "G"), (1e6, "M"), (1e3, "k"), (1, ""), (1e-3, "m"), (1e-6, "u"), (1e-9, "n"), (1e-12, "p")]
    for scale, prefix in prefixes:
        if abs(value) >= scale * 0.9995:
            return f"{value / scale:.4g} {prefix}{unit}"
    return f"{value:.3e} {unit}"


class DCResult(_Result):
    @property
    def voltages(self):
        return {node: float(self.v(node)) for node in self.circuit.node_index if ".junction" not in node}

    @property
    def currents(self):
        return {name: float(self.i(name)) for name, e in self.circuit.elements.items() if not e.hidden}

    def table(self):
        lines = ["node voltages"]
        for node, value in self.voltages.items():
            lines.append(f"  {node:<12} {engineering(value, 'V'):>14}")
        lines.append("parts             current          power")
        for name, element in self.circuit.elements.items():
            if element.hidden:
                continue
            current = float(self.i(name))
            power = float(self.p(name))
            lines.append(f"  {name:<12} {engineering(current, 'A'):>14} {engineering(power, 'W'):>14}")
        return "\n".join(lines)

    def __str__(self):
        return self.table()


class _Series(_Result):
    def __init__(self, circuit, axis, rows, ctx):
        super().__init__(circuit, rows, ctx)
        self.rows = rows


class SweepResult(_Series):
    def __init__(self, circuit, values, rows, ctx):
        super().__init__(circuit, values, rows, ctx)
        self.values = values


class TransientResult(_Series):
    def __init__(self, circuit, time, rows, ctx):
        super().__init__(circuit, time, rows, ctx)
        self.time = time
        self.t = time

    def _with_time(self):
        self.ctx.t = self.time
        return self.ctx

    def i(self, name):
        self._with_time()
        return super().i(name)

    def p(self, name):
        self._with_time()
        return super().p(name)

    def at(self, time, node, ref=None):
        return float(np.interp(time, self.time, self.v(node, ref)))

    def crossing_times(self, node, level, direction="rising", ref=None):
        v = self.v(node, ref) - level
        times = []
        for n in range(1, len(v)):
            a, b = v[n - 1], v[n]
            rising = a < 0 <= b
            falling = a > 0 >= b
            if (direction in ("rising", "any") and rising) or (direction in ("falling", "any") and falling):
                frac = a / (a - b) if a != b else 0.0
                times.append(self.time[n - 1] + frac * (self.time[n] - self.time[n - 1]))
        return times

    def time_to_cross(self, node, level, direction="rising", ref=None):
        times = self.crossing_times(node, level, direction, ref)
        return times[0] if times else math.inf

    def frequency(self, node, ref=None):
        v = self.v(node, ref)
        half = v[len(v) // 4:]
        level = 0.5 * (half.max() + half.min())
        times = [t for t in self.crossing_times(node, level, "rising", ref) if t >= self.time[len(v) // 4]]
        if len(times) < 2:
            return 0.0
        return (len(times) - 1) / (times[-1] - times[0])


class ACResult(_Series):
    def __init__(self, circuit, freqs, rows, ctx, source):
        super().__init__(circuit, freqs, rows, ctx)
        self.freqs = freqs
        self.f = freqs
        self.source = source

    def gain(self, node, ref=None):
        value = self.v(node)
        if ref is not None:
            value = value / self.v(ref)
        return np.abs(value)

    def gain_db(self, node, ref=None):
        return 20 * np.log10(np.maximum(self.gain(node, ref), 1e-300))

    def phase_deg(self, node, ref=None):
        value = self.v(node)
        if ref is not None:
            value = value / self.v(ref)
        return np.degrees(np.unwrap(np.angle(value)))

    def gain_db_at(self, freq, node, ref=None):
        return float(np.interp(math.log10(freq), np.log10(self.freqs), self.gain_db(node, ref)))

    def cutoff(self, node, ref=None, drop_db=3.0103):
        g = self.gain_db(node, ref)
        target = g.max() - drop_db
        peak = int(np.argmax(g))
        logf = np.log10(self.freqs)
        for n in list(range(peak + 1, len(g))):
            if g[n] <= target:
                return float(10 ** np.interp(target, [g[n], g[n - 1]], [logf[n], logf[n - 1]]))
        for n in range(peak - 1, -1, -1):
            if g[n] <= target:
                return float(10 ** np.interp(target, [g[n], g[n + 1]], [logf[n], logf[n + 1]]))
        return math.nan
