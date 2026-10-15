import math
import random
from itertools import product

from sim.logic import OPS, LogicCircuit, ripple_adder

VERILOG_MAC = """module mac8 (
    input  wire        clk,
    input  wire        clear,
    input  wire [7:0]  w,
    input  wire [7:0]  x,
    output reg  [23:0] acc
);
    always @(posedge clk) begin
        if (clear) acc <= 24'd0;
        else       acc <= acc + w * x;
    end
endmodule"""


def tokenize(text):
    return [ch for ch in text.replace(" ", "")]


class Synth:
    def __init__(self, lc):
        self.lc = lc
        self.table = {}
        self.count = 0

    def node(self, op, args):
        key = (op, tuple(sorted(args)) if op in ("and", "or", "xor") else tuple(args))
        if key in self.table:
            return self.table[key]
        self.count += 1
        name = f"n{self.count}"
        self.lc.gate(op, list(args), name)
        self.table[key] = name
        return name

    def parse(self, text):
        self.tokens = tokenize(text)
        self.pos = 0
        return self.parse_or()

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse_or(self):
        left = self.parse_xor()
        while self.peek() == "|":
            self.pos += 1
            left = self.node("or", [left, self.parse_xor()])
        return left

    def parse_xor(self):
        left = self.parse_and()
        while self.peek() == "^":
            self.pos += 1
            left = self.node("xor", [left, self.parse_and()])
        return left

    def parse_and(self):
        left = self.parse_not()
        while self.peek() == "&":
            self.pos += 1
            left = self.node("and", [left, self.parse_not()])
        return left

    def parse_not(self):
        if self.peek() == "~":
            self.pos += 1
            return self.node("not", [self.parse_not()])
        if self.peek() == "(":
            self.pos += 1
            inner = self.parse_or()
            self.pos += 1
            return inner
        name = self.tokens[self.pos]
        self.pos += 1
        return self.leaf(name)

    def leaf(self, name):
        return name


class Evaluate(Synth):
    def __init__(self, env):
        self.env = env

    def node(self, op, args):
        return OPS[op](args)

    def leaf(self, name):
        return self.env[name]


def synthesize(outputs, inputs, share=True):
    lc = LogicCircuit("synthesized")
    lc.inputs(*inputs)
    synth = Synth(lc)
    for out, expression in outputs.items():
        if not share:
            synth.table = {}
        result = synth.parse(expression)
        lc.gate("buf", [result], out)
    lc.outputs(*outputs)
    return lc


def equivalent(lc, outputs, inputs):
    for bits in product((0, 1), repeat=len(inputs)):
        env = dict(zip(inputs, bits))
        got = lc.evaluate(env)
        for out, expression in outputs.items():
            if got[out] != Evaluate(env).parse(expression):
                return False
    return True


def nets_of(lc):
    driver = {g.output: g.name for g in lc.gates if g.op != "buf"}
    nets = []
    for g in lc.gates:
        if g.op == "buf":
            continue
        sinks = [h.name for h in lc.gates if h.op != "buf" and g.output in h.inputs]
        if sinks:
            nets.append([g.name] + sinks)
    return nets, list(driver.values())


def hpwl(placement, nets):
    total = 0
    for net in nets:
        xs = [placement[c][0] for c in net]
        ys = [placement[c][1] for c in net]
        total += (max(xs) - min(xs)) + (max(ys) - min(ys))
    return total


def improve(placement, nets, rounds=6):
    cells = sorted(placement)
    best = hpwl(placement, nets)
    for _ in range(rounds):
        improved = False
        for i in range(len(cells)):
            for j in range(i + 1, len(cells)):
                a, b = cells[i], cells[j]
                placement[a], placement[b] = placement[b], placement[a]
                length = hpwl(placement, nets)
                if length < best:
                    best = length
                    improved = True
                else:
                    placement[a], placement[b] = placement[b], placement[a]
        if not improved:
            break
    return best


def dies_per_wafer(die_mm2, wafer_mm=300.0):
    radius = wafer_mm / 2
    return math.pi * radius ** 2 / die_mm2 - math.pi * wafer_mm / math.sqrt(2 * die_mm2)


def poisson_yield(die_mm2, defects_per_cm2):
    return math.exp(-defects_per_cm2 * die_mm2 / 100)


def main():
    print("Step 1: register-transfer level (RTL) in Verilog")
    for line in VERILOG_MAC.splitlines():
        print(f"  | {line}")

    print("\nStep 2: toy synthesis from Boolean expressions to gates")
    inputs = ["a", "b", "c"]
    outputs = {"sum": "a ^ b ^ c", "carry": "(a & b) | ((a ^ b) & c)"}
    for share in (False, True):
        lc = synthesize(outputs, inputs, share)
        label = "with shared subexpressions" if share else "each output on its own"
        print(f"  {label:28s}: {lc.gate_count()} gates, depth {lc.depth()},"
              f" equivalent to the expressions: {equivalent(lc, outputs, inputs)}")
    mux = {"y": "(s & b) | (~s & a)"}
    lc = synthesize(mux, ["a", "b", "s"])
    print(f"  2:1 multiplexer y = (s & b) | (~s & a): {lc.gate_count()} gates, equivalent: {equivalent(lc, mux, ['a', 'b', 's'])}")

    print("\nStep 3: toy placement of a 4-bit ripple adder (20 gates on a 5 x 4 grid)")
    adder = ripple_adder(4)
    nets, cells = nets_of(adder)
    spots = [(x, y) for y in range(4) for x in range(5)]
    rng = random.Random(5)
    rng.shuffle(spots)
    placement = dict(zip(cells, spots))
    start = hpwl(placement, nets)
    final = improve(placement, nets)
    print(f"  {len(cells)} cells, {len(nets)} nets")
    print(f"  random placement: total half-perimeter wirelength {start} grid units")
    print(f"  after greedy swaps: {final} grid units ({(1 - final / start) * 100:.0f}% shorter)")

    print("\nStep 4: dies per 300 mm wafer, yield and cost per good die")
    wafer_cost = 17000.0
    defects = 0.1
    print(f"  wafer cost ${wafer_cost:,.0f}, defect density {defects} per cm^2")
    print(f"  {'die':>8s} {'dies':>6s} {'yield':>7s} {'good':>6s} {'$ per good die':>15s}")
    for area in (10, 50, 100, 200, 400, 800):
        n = dies_per_wafer(area)
        y = poisson_yield(area, defects)
        good = n * y
        print(f"  {area:5d}mm2 {n:6.0f} {y * 100:6.1f}% {good:6.0f} {wafer_cost / good:15.2f}")

    print("\nStep 5: one 800 mm^2 die or four 200 mm^2 chiplets?")
    mono = wafer_cost / (dies_per_wafer(800) * poisson_yield(800, defects))
    chiplet = wafer_cost / (dies_per_wafer(200) * poisson_yield(200, defects))
    packaging = 150.0
    print(f"  monolithic: ${mono:,.2f} of silicon per good chip")
    print(f"  four chiplets: 4 x ${chiplet:,.2f} = ${4 * chiplet:,.2f} of silicon"
          f" + ${packaging:.0f} extra advanced packaging = ${4 * chiplet + packaging:,.2f}")


if __name__ == "__main__":
    main()
