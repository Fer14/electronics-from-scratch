// The browser twin of sim/cost.py: area in gate units, delay in gate delays, latency in cycles.

const FLOP = 6, ACT = 0.25;

const block = (kind, area, delay, bits, o = {}) => {
  const b = { kind, area, delay, bits, latency: o.latency ?? 0, ops: o.ops ?? 0, params: o.params ?? {} };
  b.energy = o.energy ?? ACT * area;
  b.stage = b.latency ? Math.ceil(b.delay / b.latency) : b.delay;
  return b;
};

const adder = (n) => block("adder", 5 * n, 2 * n + 1, n + 1, { params: { bits: n } });
const multiplier = (n) => block("multiplier", n * n + 5 * n * (n - 1), n === 1 ? 1 : 6 * (n - 1), 2 * n, { ops: 1, params: { bits: n } });
const register = (n) => block("register", FLOP * n, 0, n, { latency: 1, params: { bits: n } });
const mac = (n, acc) => {
  acc = acc || 2 * n + 8;
  const m = multiplier(n), a = adder(acc), r = register(acc);
  return block("mac", m.area + a.area + r.area, m.delay + a.delay, acc, { latency: 1, ops: 1, params: { bits: n, acc_bits: acc } });
};
const mux = (k, n) => block("mux", 3 * n * (k - 1), 2 * Math.ceil(Math.log2(Math.max(k, 2))), n, { params: { inputs: k, bits: n } });

export const BUILDERS = {
  adder: (p) => adder(p.bits),
  multiplier: (p) => multiplier(p.bits),
  register: (p) => register(p.bits),
  pipelined_multiplier: (p) => {
    const s = p.stages ?? 2, m = multiplier(p.bits);
    return block("pipelined_multiplier", m.area + s * register(2 * p.bits).area, m.delay, 2 * p.bits, { latency: s, ops: 1, params: { bits: p.bits, stages: s } });
  },
  mac: (p) => mac(p.bits, p.acc_bits),
  mux: (p) => mux(p.inputs, p.bits),
  register_file: (p) => { const r = mux(p.words, p.bits); return block("register_file", FLOP * p.words * p.bits + r.area, r.delay, p.bits, { params: { words: p.words, bits: p.bits } }); },
  sram: (p) => { const w = p.width ?? 32; return block("sram", p.bits, 2 * Math.ceil(Math.log2(Math.max(p.bits, 2))), w, { latency: 1, energy: 10 * w, params: { bits: p.bits, width: w } }); },
  dram: (p) => { const w = p.width ?? 64; return block("dram", 0, 0, w, { latency: 100, energy: 200 * w, params: { width: w } }); },
  systolic_array: (p) => {
    const c = mac(p.bits, p.acc_bits);
    return block("systolic_array", p.rows * p.cols * c.area, c.delay, p.cols * c.bits, { latency: 1, ops: p.rows * p.cols, params: { rows: p.rows, cols: p.cols, bits: p.bits, acc_bits: c.params.acc_bits } });
  },
  wire: (p) => block("wire", 0, Math.trunc(p.length ?? 1), p.bits ?? 0, { energy: 2 * (p.bits ?? 0) * (p.length ?? 1), params: { bits: p.bits, length: p.length ?? 1 } }),
  gates: (p) => block("gates", p.area, Math.trunc(p.depth), p.bits ?? 0, { params: { area: p.area, depth: p.depth, bits: p.bits ?? 0 } }),
};

export function buildBlock(kind, params) {
  if (!(kind in BUILDERS)) throw new Error(`unknown block ${kind}`);
  return BUILDERS[kind](params);
}

export class Design {
  constructor() { this.blocks = new Map(); }
  add(name, b, a = "in", to = "out") { this.blocks.set(name, { block: b, a, b: to }); }
  sum(key) { let s = 0; for (const { block } of this.blocks.values()) s += block[key]; return s; }
  area() { return this.sum("area"); }
  throughput() { return this.sum("ops"); }
  bits_moved() { return this.sum("bits"); }
  energy() { return this.sum("energy"); }
  incoming() {
    const inc = new Map();
    for (const [name, { block, a, b }] of this.blocks) {
      if (!inc.has(b)) inc.set(b, []);
      if (!inc.has(a)) inc.set(a, []);
      inc.get(b).push({ name, block, a });
    }
    return inc;
  }
  arrivals() {
    const inc = this.incoming(), times = new Map(), visiting = new Set();
    const arrival = (node) => {
      if (times.has(node)) return times.get(node);
      if (visiting.has(node)) throw new Error(`combinational loop through ${node}: put a register in the loop`);
      visiting.add(node);
      let best = 0;
      for (const { block, a } of inc.get(node) || []) best = Math.max(best, block.latency ? block.stage : arrival(a) + block.delay);
      visiting.delete(node);
      times.set(node, best);
      return best;
    };
    for (const node of inc.keys()) arrival(node);
    return times;
  }
  critical_path() {
    const t = this.arrivals();
    let worst = Math.max(0, ...t.values());
    for (const { block, a } of this.blocks.values()) if (block.latency) worst = Math.max(worst, t.get(a) + block.stage);
    return worst;
  }
  latency() {
    const inc = this.incoming(), memo = new Map();
    const cycles = (node, path) => {
      if (memo.has(node)) return memo.get(node);
      let best = 0;
      for (const { block, a } of inc.get(node) || []) { if (path.has(a)) continue; best = Math.max(best, cycles(a, new Set([...path, a])) + block.latency); }
      memo.set(node, best);
      return best;
    };
    return Math.max(0, ...[...inc.keys()].map((n) => cycles(n, new Set([n]))));
  }
}
