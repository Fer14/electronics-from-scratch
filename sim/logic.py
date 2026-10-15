"""Gate-level digital logic: gates, D flip-flops, registers and a clocked simulation.

    lc = LogicCircuit()
    lc.inputs("a", "b", "cin")
    lc.xor("p", "a", "b")
    lc.xor("s", "p", "cin")
    lc.and_("g", "a", "b")
    lc.and_("t", "p", "cin")
    lc.or_("cout", "g", "t")
    lc.outputs("s", "cout")
    for row in lc.truth_table():
        print(row)

Signals are named wires holding 0 or 1. Combinational gates settle by repeated evaluation
(so feedback loops such as an SR latch keep their memory between calls). Flip-flops only
change on step(), which is one rising clock edge: every flip-flop copies its D input at the
same instant, then the gates settle again. events() replays an input change with a delay
of one time unit per gate, which shows glitches and the critical path.
"""
from itertools import product

OPS = {
    "and": lambda xs: int(all(xs)),
    "or": lambda xs: int(any(xs)),
    "not": lambda xs: 1 - xs[0],
    "buf": lambda xs: xs[0],
    "nand": lambda xs: 1 - int(all(xs)),
    "nor": lambda xs: 1 - int(any(xs)),
    "xor": lambda xs: sum(xs) % 2,
    "xnor": lambda xs: 1 - sum(xs) % 2,
}


class Gate:
    def __init__(self, name, op, inputs, output):
        if op not in OPS:
            raise ValueError(f"unknown gate {op!r}; choose from {sorted(OPS)}")
        self.name, self.op, self.inputs, self.output = name, op, list(inputs), output
        if op in ("not", "buf"):
            self.inputs = self.inputs[:1]

    def evaluate(self, values):
        return OPS[self.op]([values.get(i, 0) for i in self.inputs])


class FlipFlop:
    def __init__(self, name, d, q, init=0, enable=None, reset=None):
        self.name, self.d, self.q, self.init = name, d, q, int(init)
        self.enable, self.reset = enable, reset


class LogicSettleError(RuntimeError):
    pass


class LogicCircuit:
    def __init__(self, name=""):
        self.name = name
        self.input_names = []
        self.output_names = []
        self.gates = []
        self.flops = []
        self.values = {}
        self.constants = {}
        self.cycle = 0

    def inputs(self, *names):
        for name in names:
            if name not in self.input_names:
                self.input_names.append(name)
        return list(names)

    input = inputs

    def outputs(self, *names):
        for name in names:
            if name not in self.output_names:
                self.output_names.append(name)
        return list(names)

    output = outputs

    def constant(self, name, value):
        self.constants[name] = int(value)
        self.values[name] = int(value)
        return name

    def gate(self, op, inputs, output, name=None):
        if isinstance(inputs, str):
            inputs = [inputs]
        gate = Gate(name or f"G{len(self.gates) + 1}", op.lower(), inputs, output)
        self.gates.append(gate)
        return output

    def and_(self, output, *inputs):
        return self.gate("and", inputs, output)

    def or_(self, output, *inputs):
        return self.gate("or", inputs, output)

    def not_(self, output, a):
        return self.gate("not", [a], output)

    def nand(self, output, *inputs):
        return self.gate("nand", inputs, output)

    def nor(self, output, *inputs):
        return self.gate("nor", inputs, output)

    def xor(self, output, *inputs):
        return self.gate("xor", inputs, output)

    def xnor(self, output, *inputs):
        return self.gate("xnor", inputs, output)

    def dff(self, d, q, name=None, init=0, enable=None, reset=None):
        flop = FlipFlop(name or f"F{len(self.flops) + 1}", d, q, init, enable, reset)
        self.flops.append(flop)
        self.values[q] = flop.init
        return q

    def register(self, name, d_bits, q_bits, init=0, enable=None, reset=None):
        if len(d_bits) != len(q_bits):
            raise ValueError("register needs as many D wires as Q wires")
        for bit, (d, q) in enumerate(zip(d_bits, q_bits)):
            self.dff(d, q, f"{name}[{bit}]", (init >> bit) & 1, enable, reset)
        return list(q_bits)

    def reset(self):
        self.values = dict(self.constants)
        for flop in self.flops:
            self.values[flop.q] = flop.init
        self.cycle = 0

    def settle(self, inputs=None):
        for name, value in (inputs or {}).items():
            self.values[name] = int(value)
        for _ in range(4 * len(self.gates) + 4):
            changed = False
            for gate in self.gates:
                value = gate.evaluate(self.values)
                if self.values.get(gate.output) != value:
                    self.values[gate.output] = value
                    changed = True
            if not changed:
                return dict(self.values)
        raise LogicSettleError("the gates never settle: a feedback loop keeps oscillating")

    def evaluate(self, inputs=None):
        values = self.settle(inputs)
        names = self.output_names or list(values)
        return {name: values.get(name, 0) for name in names}

    def step(self, inputs=None):
        self.settle(inputs)
        captured = {}
        for flop in self.flops:
            if flop.reset is not None and self.values.get(flop.reset, 0):
                captured[flop.q] = flop.init
            elif flop.enable is None or self.values.get(flop.enable, 0):
                captured[flop.q] = self.values.get(flop.d, 0)
        self.values.update(captured)
        self.cycle += 1
        return self.evaluate()

    def run(self, steps):
        return [self.step(inputs) for inputs in steps]

    def truth_table(self, inputs=None, outputs=None):
        inputs = list(inputs or self.input_names)
        outputs = list(outputs or self.output_names)
        rows = []
        saved = dict(self.values)
        for bits in product((0, 1), repeat=len(inputs)):
            values = self.settle(dict(zip(inputs, bits)))
            rows.append({**dict(zip(inputs, bits)), **{o: values.get(o, 0) for o in outputs}})
        self.values = saved
        return rows

    def format_truth_table(self, inputs=None, outputs=None):
        rows = self.truth_table(inputs, outputs)
        columns = list(rows[0]) if rows else []
        lines = [" ".join(f"{c:>4}" for c in columns)]
        lines += [" ".join(f"{row[c]:>4}" for c in columns) for row in rows]
        return "\n".join(lines)

    def gate_count(self):
        return len([g for g in self.gates if g.op != "buf"])

    def counts(self):
        tally = {}
        for gate in self.gates:
            tally[gate.op] = tally.get(gate.op, 0) + 1
        tally["dff"] = len(self.flops)
        return tally

    def arrival_times(self):
        sources = set(self.input_names) | set(self.constants) | {f.q for f in self.flops}
        driver = {g.output: g for g in self.gates}
        times = {s: 0 for s in sources}
        visiting = set()

        def arrival(signal):
            if signal in times:
                return times[signal]
            if signal not in driver:
                return 0
            if signal in visiting:
                raise LogicSettleError(f"combinational loop through {signal!r}")
            visiting.add(signal)
            gate = driver[signal]
            delay = 0 if gate.op == "buf" else 1
            times[signal] = delay + max((arrival(i) for i in gate.inputs), default=0)
            visiting.discard(signal)
            return times[signal]

        for gate in self.gates:
            arrival(gate.output)
        return times

    def depth(self):
        times = self.arrival_times()
        ends = list(self.output_names) + [f.d for f in self.flops]
        return max((times.get(e, 0) for e in ends), default=0)

    def events(self, before, after, delay=1, horizon=None):
        self.settle(before)
        horizon = horizon or 4 * len(self.gates) + 4
        changes = []
        current = dict(self.values)
        for name, value in after.items():
            if current.get(name) != int(value):
                current[name] = int(value)
                changes.append((0, name, int(value)))
        time = 0
        while time < horizon:
            scheduled = {}
            for gate in self.gates:
                value = gate.evaluate(current)
                if current.get(gate.output) != value:
                    scheduled[gate.output] = value
            if not scheduled:
                break
            time += delay
            for name, value in scheduled.items():
                current[name] = value
                changes.append((time, name, value))
        self.values = current
        return changes


def full_adder(lc, a, b, cin, s, cout, tag="fa"):
    lc.xor(f"{tag}.p", a, b)
    lc.xor(s, f"{tag}.p", cin)
    lc.and_(f"{tag}.g", a, b)
    lc.and_(f"{tag}.t", f"{tag}.p", cin)
    lc.or_(cout, f"{tag}.g", f"{tag}.t")
    return s, cout


def ripple_adder(bits):
    lc = LogicCircuit(f"ripple adder {bits}-bit")
    a = [f"a{i}" for i in range(bits)]
    b = [f"b{i}" for i in range(bits)]
    lc.inputs(*a, *b)
    lc.constant("zero", 0)
    carry = "zero"
    for i in range(bits):
        out = f"c{i + 1}" if i < bits - 1 else "cout"
        full_adder(lc, a[i], b[i], carry, f"s{i}", out, tag=f"fa{i}")
        carry = out
    lc.outputs(*[f"s{i}" for i in range(bits)], "cout")
    return lc


def array_multiplier(bits):
    lc = LogicCircuit(f"array multiplier {bits}x{bits}")
    a = [f"a{i}" for i in range(bits)]
    b = [f"b{i}" for i in range(bits)]
    lc.inputs(*a, *b)
    lc.constant("zero", 0)
    row = []
    for i in range(bits):
        lc.and_(f"pp0_{i}", a[i], b[0])
        row.append(f"pp0_{i}")
    row.append("zero")
    products = [row[0]]
    for j in range(1, bits):
        carry = "zero"
        new_row = []
        for i in range(bits):
            lc.and_(f"pp{j}_{i}", a[i], b[j])
            out_carry = f"r{j}c{i}"
            full_adder(lc, f"pp{j}_{i}", row[i + 1], carry, f"r{j}s{i}", out_carry, tag=f"r{j}fa{i}")
            carry = out_carry
            new_row.append(f"r{j}s{i}")
        new_row.append(carry)
        products.append(new_row[0])
        row = new_row
    products += row[1:]
    for k, name in enumerate(products):
        lc.gate("buf", [name], f"p{k}")
    lc.outputs(*[f"p{k}" for k in range(2 * bits)])
    return lc
