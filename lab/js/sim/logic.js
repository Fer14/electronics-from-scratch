// The browser twin of sim/logic.py: gates settle by repeated evaluation, flip-flops move on step().

const OPS = {
  and: (xs) => (xs.every(Boolean) ? 1 : 0),
  or: (xs) => (xs.some(Boolean) ? 1 : 0),
  not: (xs) => 1 - xs[0],
  buf: (xs) => xs[0],
  nand: (xs) => (xs.every(Boolean) ? 0 : 1),
  nor: (xs) => (xs.some(Boolean) ? 0 : 1),
  xor: (xs) => xs.reduce((a, b) => a + b, 0) % 2,
  xnor: (xs) => 1 - (xs.reduce((a, b) => a + b, 0) % 2),
};

export class LogicSettleError extends Error {}

export class LogicCircuit {
  constructor() { this.inputNames = []; this.outputNames = []; this.gates = []; this.flops = []; this.values = {}; }
  inputs(...names) { for (const n of names) if (!this.inputNames.includes(n)) this.inputNames.push(n); }
  outputs(...names) { for (const n of names) if (!this.outputNames.includes(n)) this.outputNames.push(n); }
  gate(op, inputs, output, name) {
    op = op.toLowerCase();
    if (!(op in OPS)) throw new Error(`unknown gate ${op}`);
    this.gates.push({ name: name || `G${this.gates.length + 1}`, op, inputs: op === "not" || op === "buf" ? inputs.slice(0, 1) : [...inputs], output });
  }
  dff(d, q, name, init = 0) { this.flops.push({ name, d, q, init }); this.values[q] = init; }
  evalGate(g) { return OPS[g.op](g.inputs.map((i) => this.values[i] ?? 0)); }
  reset() { this.values = {}; for (const f of this.flops) this.values[f.q] = f.init; }
  settle(inputs = {}) {
    for (const [k, v] of Object.entries(inputs)) this.values[k] = v ? 1 : 0;
    for (let it = 0; it < 4 * this.gates.length + 4; it++) {
      let changed = false;
      for (const g of this.gates) {
        const v = this.evalGate(g);
        if (this.values[g.output] !== v) { this.values[g.output] = v; changed = true; }
      }
      if (!changed) return { ...this.values };
    }
    throw new LogicSettleError("the gates never settle: a feedback loop keeps oscillating");
  }
  step(inputs = {}) {
    this.settle(inputs);
    const captured = {};
    for (const f of this.flops) captured[f.q] = this.values[f.d] ?? 0;
    Object.assign(this.values, captured);
    return this.settle();
  }
  truthTable(inputs = this.inputNames, outputs = this.outputNames) {
    const saved = { ...this.values }, rows = [];
    for (let m = 0; m < 2 ** inputs.length; m++) {
      const assign = {};
      inputs.forEach((name, i) => { assign[name] = (m >> (inputs.length - 1 - i)) & 1; });
      const v = this.settle(assign);
      const row = { ...assign };
      for (const o of outputs) row[o] = v[o] ?? 0;
      rows.push(row);
    }
    this.values = saved;
    return rows;
  }
  gateCount() { return this.gates.filter((g) => g.op !== "buf").length; }
  depth() {
    const sources = new Set([...this.inputNames, ...this.flops.map((f) => f.q)]);
    const driver = new Map(this.gates.map((g) => [g.output, g]));
    const times = new Map(), visiting = new Set();
    const arrival = (sig) => {
      if (sources.has(sig)) return 0;
      if (times.has(sig)) return times.get(sig);
      if (!driver.has(sig)) return 0;
      if (visiting.has(sig)) throw new LogicSettleError(`combinational loop through ${sig}`);
      visiting.add(sig);
      const g = driver.get(sig);
      const t = (g.op === "buf" ? 0 : 1) + Math.max(0, ...g.inputs.map(arrival));
      visiting.delete(sig);
      times.set(sig, t);
      return t;
    };
    const ends = [...this.outputNames, ...this.flops.map((f) => f.d)];
    return Math.max(0, ...ends.map(arrival));
  }
}
