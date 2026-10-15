"""A cost model for chip design: area, delay, latency, bits moved and energy.

Units are deliberately simple so they can be checked by hand:
  area     one logic gate = 1 unit, one flip-flop = 6 units, one SRAM bit = 1 unit
  delay    one gate = 1 unit of delay; a path's delay is the number of gates in a row
  latency  clock cycles from input to output (how many registers the data crosses)
  energy   one gate switching = 1 unit; a quarter of the gates switch each cycle,
           moving a bit along one unit of wire costs 2, reading a bit from SRAM costs 10,
           from DRAM 200

The adder and multiplier numbers are the ones you get by counting the gates of the
gate-level builders in sim.logic (ripple_adder, array_multiplier); tests check that.

A Design is a graph: nodes are places where data sits, every block carries data from node
a to node b. Blocks with latency end in a register: the timing path stops there, and the
clock period has to fit the slowest stretch of gates between two registers.
"""
import math
from dataclasses import dataclass, field

FLOP_AREA = 6
SRAM_BIT_AREA = 1
ACTIVITY = 0.25
WIRE_ENERGY_PER_BIT = 2.0
SRAM_ENERGY_PER_BIT = 10.0
DRAM_ENERGY_PER_BIT = 200.0


@dataclass
class Block:
    kind: str
    area: float
    delay: int
    bits: int = 0
    latency: int = 0
    ops: float = 0.0
    energy: float = None
    params: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.energy is None:
            self.energy = ACTIVITY * self.area

    @property
    def stage_delay(self):
        return math.ceil(self.delay / self.latency) if self.latency else self.delay


def adder(bits):
    return Block("adder", 5 * bits, 2 * bits + 1, bits + 1, params={"bits": bits})


def multiplier(bits):
    area = bits * bits + 5 * bits * (bits - 1)
    delay = 1 if bits == 1 else 6 * (bits - 1)
    return Block("multiplier", area, delay, 2 * bits, ops=1, params={"bits": bits})


def register(bits):
    return Block("register", FLOP_AREA * bits, 0, bits, latency=1, params={"bits": bits})


def pipelined_multiplier(bits, stages):
    base = multiplier(bits)
    area = base.area + stages * register(2 * bits).area
    return Block("pipelined_multiplier", area, base.delay, 2 * bits, latency=stages, ops=1,
                 params={"bits": bits, "stages": stages})


def mac(bits, acc_bits=None):
    acc_bits = acc_bits or 2 * bits + 8
    m, a, r = multiplier(bits), adder(acc_bits), register(acc_bits)
    return Block("mac", m.area + a.area + r.area, m.delay + a.delay, acc_bits, latency=1, ops=1,
                 params={"bits": bits, "acc_bits": acc_bits})


def mux(inputs, bits):
    levels = math.ceil(math.log2(max(inputs, 2)))
    return Block("mux", 3 * bits * (inputs - 1), 2 * levels, bits, params={"inputs": inputs, "bits": bits})


def register_file(words, bits):
    storage = FLOP_AREA * words * bits
    read = mux(words, bits)
    return Block("register_file", storage + read.area, read.delay, bits, params={"words": words, "bits": bits})


def sram(bits, width=32):
    levels = math.ceil(math.log2(max(bits, 2)))
    return Block("sram", SRAM_BIT_AREA * bits, 2 * levels, width, latency=1,
                 energy=SRAM_ENERGY_PER_BIT * width, params={"bits": bits, "width": width})


def dram(width=64):
    return Block("dram", 0, 0, width, latency=100, energy=DRAM_ENERGY_PER_BIT * width, params={"width": width})


def systolic_array(rows, cols, bits, acc_bits=None):
    cell = mac(bits, acc_bits)
    return Block("systolic_array", rows * cols * cell.area, cell.delay, cols * cell.bits, latency=1,
                 ops=rows * cols, params={"rows": rows, "cols": cols, "bits": bits, "acc_bits": cell.params["acc_bits"]})


def wire(bits, length=1):
    return Block("wire", 0, int(length), bits, energy=WIRE_ENERGY_PER_BIT * bits * length,
                 params={"bits": bits, "length": length})


def gates(area, depth, bits=0):
    return Block("gates", area, int(depth), bits, params={"area": area, "depth": depth, "bits": bits})


def from_logic(lc):
    return gates(lc.gate_count() + FLOP_AREA * len(lc.flops), lc.depth(), len(lc.output_names))


BUILDERS = {
    "adder": lambda p: adder(p["bits"]),
    "multiplier": lambda p: multiplier(p["bits"]),
    "register": lambda p: register(p["bits"]),
    "pipelined_multiplier": lambda p: pipelined_multiplier(p["bits"], p.get("stages", 2)),
    "mac": lambda p: mac(p["bits"], p.get("acc_bits")),
    "mux": lambda p: mux(p["inputs"], p["bits"]),
    "register_file": lambda p: register_file(p["words"], p["bits"]),
    "sram": lambda p: sram(p["bits"], p.get("width", 32)),
    "dram": lambda p: dram(p.get("width", 64)),
    "systolic_array": lambda p: systolic_array(p["rows"], p["cols"], p["bits"], p.get("acc_bits")),
    "wire": lambda p: wire(p["bits"], p.get("length", 1)),
    "gates": lambda p: gates(p["area"], p["depth"], p.get("bits", 0)),
}


def build(kind, **params):
    if kind not in BUILDERS:
        raise ValueError(f"unknown block {kind!r}; choose from {sorted(BUILDERS)}")
    return BUILDERS[kind](params)


class Design:
    def __init__(self, name=""):
        self.name = name
        self.blocks = {}

    def add(self, name, block, a="in", b="out"):
        if name in self.blocks:
            raise ValueError(f"duplicate block {name!r}")
        self.blocks[name] = (block, a, b)
        return block

    def chain(self, *named_blocks, start="in", end="out"):
        node = start
        for i, (name, block) in enumerate(named_blocks):
            nxt = end if i == len(named_blocks) - 1 else f"{name}.out"
            self.add(name, block, node, nxt)
            node = nxt
        return self

    def area(self):
        return sum(block.area for block, _, _ in self.blocks.values())

    def throughput(self):
        return sum(block.ops for block, _, _ in self.blocks.values())

    def bits_moved(self):
        return sum(block.bits for block, _, _ in self.blocks.values())

    def energy(self):
        return sum(block.energy for block, _, _ in self.blocks.values())

    def _incoming(self):
        incoming = {}
        for name, (block, a, b) in self.blocks.items():
            incoming.setdefault(b, []).append((name, block, a))
            incoming.setdefault(a, [])
        return incoming

    def arrivals(self):
        incoming = self._incoming()
        times = {}
        visiting = set()

        def arrival(node):
            if node in times:
                return times[node]
            if node in visiting:
                raise ValueError(f"combinational loop through {node!r}: put a register in the loop")
            visiting.add(node)
            best = 0
            for _, block, a in incoming.get(node, []):
                best = max(best, block.stage_delay if block.latency else arrival(a) + block.delay)
            visiting.discard(node)
            times[node] = best
            return best

        for node in incoming:
            arrival(node)
        return times

    def critical_path(self):
        times = self.arrivals()
        worst = max(times.values(), default=0)
        for block, a, _ in self.blocks.values():
            if block.latency:
                worst = max(worst, times[a] + block.stage_delay)
        return worst

    def latency(self):
        incoming = self._incoming()
        memo = {}

        def cycles(node, path):
            if node in memo:
                return memo[node]
            best = 0
            for _, block, a in incoming.get(node, []):
                if a in path:
                    continue
                best = max(best, cycles(a, path | {a}) + block.latency)
            memo[node] = best
            return best

        return max((cycles(node, {node}) for node in incoming), default=0)

    def max_clock_mhz(self, gate_delay_ps=20.0):
        path = max(self.critical_path(), 1)
        return 1e6 / (path * gate_delay_ps)

    def report(self):
        lines = [f"design {self.name}".rstrip()]
        lines.append(f"  {'block':<14}{'kind':<22}{'area':>10}{'delay':>8}{'latency':>9}")
        for name, (block, _, _) in self.blocks.items():
            lines.append(f"  {name:<14}{block.kind:<22}{block.area:>10.0f}{block.delay:>8}{block.latency:>9}")
        lines.append(f"  total area     {self.area():.0f} gate units")
        lines.append(f"  critical path  {self.critical_path()} gate delays")
        lines.append(f"  latency        {self.latency()} cycles")
        lines.append(f"  throughput     {self.throughput():g} MACs per cycle")
        lines.append(f"  bits moved     {self.bits_moved()} per cycle")
        lines.append(f"  energy         {self.energy():.1f} units per cycle")
        return "\n".join(lines)

    def __str__(self):
        return self.report()
