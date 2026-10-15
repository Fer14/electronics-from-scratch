// The browser twin of sim/ (Python): modified nodal analysis with Newton-Raphson,
// transient companion models (backward Euler first step, trapezoidal after) and AC sweeps.

export const VT = 0.025852;
const EXP_CAP = 80;
const GROUND = new Set(["0", "gnd", "GND", "ground"]);

export const LED_COLORS = { infrared: 1.25, red: 1.85, orange: 1.95, yellow: 2.05, green: 2.2, blue: 3.0, white: 3.1, uv: 3.2 };
const LED_N = 2.0;
const DIODE_MODELS = {
  default: { Is: 1e-14, n: 1.0, rs: 0 },
  "1n4148": { Is: 2.5e-9, n: 1.75, rs: 0.6 },
  "1n4007": { Is: 7e-9, n: 1.8, rs: 0.04 },
  schottky: { Is: 1e-6, n: 1.05, rs: 0.1 },
};

export class ConvergenceError extends Error {}

function safeExp(u) {
  const c = Math.min(u, EXP_CAP);
  return Math.exp(c) * (1 + Math.max(u - EXP_CAP, 0));
}

function holdBack(vNew, vOld, is, nvt) {
  const knee = nvt * Math.log(nvt / is);
  const base = Math.max(vOld, knee);
  if (vNew > base + 2 * nvt) return [base + nvt * Math.log1p((vNew - base) / nvt), true];
  return [vNew, false];
}

class Stamper {
  constructor(n, complex = false, matrix = true) {
    this.n = n;
    this.complex = complex;
    this.A = matrix ? new Float64Array(n * n) : null;
    this.Ai = complex ? new Float64Array(n * n) : null;
    this.b = new Float64Array(n);
    this.bi = complex ? new Float64Array(n) : null;
  }
  add(r, c, v, vi = 0) {
    if (r < 0 || c < 0 || !this.A) return;
    this.A[r * this.n + c] += v;
    if (this.complex) this.Ai[r * this.n + c] += vi;
  }
  rhs(r, v) { if (r >= 0) this.b[r] += v; }
  conductance(a, b, g, gi = 0) {
    this.add(a, a, g, gi); this.add(b, b, g, gi); this.add(a, b, -g, -gi); this.add(b, a, -g, -gi);
  }
  inject(a, b, amps) { this.rhs(a, -amps); this.rhs(b, amps); }
  branch(a, b, k) { this.add(a, k, 1); this.add(b, k, -1); }
  branchVoltage(k, a, b, c = 1, ci = 0) { this.add(k, a, c, ci); this.add(k, b, -c, -ci); }
  linearized(nodes, v0, currents, jac) {
    for (let i = 0; i < nodes.length; i++) {
      let offset = currents[i];
      for (let j = 0; j < nodes.length; j++) {
        this.add(nodes[i], nodes[j], jac[i][j]);
        offset -= jac[i][j] * v0[j];
      }
      this.rhs(nodes[i], -offset);
    }
  }
}

function solveReal(A0, b0, n) {
  const A = Float64Array.from(A0), b = Float64Array.from(b0);
  for (let k = 0; k < n; k++) {
    let p = k, best = Math.abs(A[k * n + k]);
    for (let i = k + 1; i < n; i++) { const v = Math.abs(A[i * n + k]); if (v > best) { best = v; p = i; } }
    if (best < 1e-300) continue;
    if (p !== k) {
      for (let j = 0; j < n; j++) { const t = A[k * n + j]; A[k * n + j] = A[p * n + j]; A[p * n + j] = t; }
      const t = b[k]; b[k] = b[p]; b[p] = t;
    }
    const d = A[k * n + k];
    for (let i = k + 1; i < n; i++) {
      const f = A[i * n + k] / d;
      if (f === 0) continue;
      for (let j = k; j < n; j++) A[i * n + j] -= f * A[k * n + j];
      b[i] -= f * b[k];
    }
  }
  const x = new Float64Array(n);
  for (let i = n - 1; i >= 0; i--) {
    let s = b[i];
    for (let j = i + 1; j < n; j++) s -= A[i * n + j] * x[j];
    const d = A[i * n + i];
    x[i] = Math.abs(d) < 1e-300 ? 0 : s / d;
  }
  return x;
}

function solveComplex(Ar0, Ai0, br0, bi0, n) {
  const Ar = Float64Array.from(Ar0), Ai = Float64Array.from(Ai0), br = Float64Array.from(br0), bi = Float64Array.from(bi0);
  const swap = (arr, i, j) => { const t = arr[i]; arr[i] = arr[j]; arr[j] = t; };
  for (let k = 0; k < n; k++) {
    let p = k, best = Math.hypot(Ar[k * n + k], Ai[k * n + k]);
    for (let i = k + 1; i < n; i++) { const v = Math.hypot(Ar[i * n + k], Ai[i * n + k]); if (v > best) { best = v; p = i; } }
    if (best < 1e-300) continue;
    if (p !== k) {
      for (let j = 0; j < n; j++) { swap(Ar, k * n + j, p * n + j); swap(Ai, k * n + j, p * n + j); }
      swap(br, k, p); swap(bi, k, p);
    }
    const dr = Ar[k * n + k], di = Ai[k * n + k], dd = dr * dr + di * di;
    for (let i = k + 1; i < n; i++) {
      const xr = Ar[i * n + k], xi = Ai[i * n + k];
      if (xr === 0 && xi === 0) continue;
      const fr = (xr * dr + xi * di) / dd, fi = (xi * dr - xr * di) / dd;
      for (let j = k; j < n; j++) {
        const ar = Ar[k * n + j], ai = Ai[k * n + j];
        Ar[i * n + j] -= fr * ar - fi * ai;
        Ai[i * n + j] -= fr * ai + fi * ar;
      }
      const pr = br[k], pi = bi[k];
      br[i] -= fr * pr - fi * pi;
      bi[i] -= fr * pi + fi * pr;
    }
  }
  const xr = new Float64Array(n), xi = new Float64Array(n);
  for (let i = n - 1; i >= 0; i--) {
    let sr = br[i], si = bi[i];
    for (let j = i + 1; j < n; j++) {
      const ar = Ar[i * n + j], ai = Ai[i * n + j];
      sr -= ar * xr[j] - ai * xi[j];
      si -= ar * xi[j] + ai * xr[j];
    }
    const dr = Ar[i * n + i], di = Ai[i * n + i], dd = dr * dr + di * di;
    if (dd < 1e-300) continue;
    xr[i] = (sr * dr + si * di) / dd;
    xi[i] = (si * dr - sr * di) / dd;
  }
  return [xr, xi];
}

export const maxOf = (a) => { let m = -Infinity; for (const v of a) if (v > m) m = v; return m; };
export const minOf = (a) => { let m = Infinity; for (const v of a) if (v < m) m = v; return m; };

const nv = (x, i) => (i < 0 ? 0 : x[i]);

class Element {
  constructor(name, nodes) { this.name = name; this.nodeNames = nodes; this.n = []; this.k = -1; this.nb = 0; this.nonlinear = false; this.hidden = false; }
  bind(indexOf, first) { this.n = this.nodeNames.map(indexOf); this.k = first; }
  voltage(x, i = 0, j = 1) { return nv(x, this.n[i]) - nv(x, this.n[j]); }
  stampAC(s, ctx) { this.stamp(s, ctx); }
  power(x, ctx) { return this.voltage(x) * this.current(x, ctx); }
  start() {}
  accept() {}
}

class Resistor extends Element {
  constructor(name, a, b, ohms) { super(name, [a, b]); this.ohms = Math.max(ohms, 1e-6); }
  stamp(s) { s.conductance(this.n[0], this.n[1], 1 / this.ohms); }
  current(x) { return this.voltage(x) / this.ohms; }
}

class Switch extends Element {
  constructor(name, a, b, closed = true, toggleAt = []) {
    super(name, [a, b]); this.closed = closed; this.toggleAt = [...toggleAt].sort((p, q) => p - q); this.ron = 1e-3; this.roff = 1e12;
  }
  isClosed(t) { const flips = this.toggleAt.filter((m) => t >= m).length; return this.closed !== (flips % 2 === 1); }
  res(t) { return this.isClosed(t) ? this.ron : this.roff; }
  stamp(s, ctx) { s.conductance(this.n[0], this.n[1], 1 / this.res(ctx.t)); }
  current(x, ctx) { return this.voltage(x) / this.res(ctx.t); }
}

class Capacitor extends Element {
  constructor(name, a, b, farads, v0 = 0) { super(name, [a, b]); this.C = farads; this.v0 = v0; this.nb = 1; }
  stamp(s, ctx) {
    const [a, b] = this.n, k = this.k;
    s.branch(a, b, k);
    if (ctx.mode === "dc") s.add(k, k, 1);
    else if (ctx.mode === "ic") { s.branchVoltage(k, a, b); s.rhs(k, this.v0); }
    else if (ctx.mode === "tran") {
      const st = ctx.state[this.name];
      const g = ctx.method === "be" ? this.C / ctx.dt : (2 * this.C) / ctx.dt;
      s.add(k, k, 1); s.branchVoltage(k, a, b, -g);
      s.rhs(k, ctx.method === "be" ? -g * st.v : -g * st.v - st.i);
    } else { s.add(k, k, 1); s.branchVoltage(k, a, b, 0, -ctx.omega * this.C); }
  }
  current(x) { return x[this.k]; }
  start(x, ctx) { ctx.state[this.name] = { v: this.voltage(x), i: x[this.k] }; }
  accept(x, ctx) { this.start(x, ctx); }
}

class Inductor extends Element {
  constructor(name, a, b, henries, i0 = 0) { super(name, [a, b]); this.L = henries; this.i0 = i0; this.nb = 1; }
  stamp(s, ctx) {
    const [a, b] = this.n, k = this.k;
    s.branch(a, b, k);
    if (ctx.mode === "dc") s.branchVoltage(k, a, b);
    else if (ctx.mode === "ic") { s.add(k, k, 1); s.rhs(k, this.i0); }
    else if (ctx.mode === "tran") {
      const st = ctx.state[this.name];
      const r = ctx.method === "be" ? this.L / ctx.dt : (2 * this.L) / ctx.dt;
      s.branchVoltage(k, a, b); s.add(k, k, -r);
      s.rhs(k, ctx.method === "be" ? -r * st.i : -r * st.i - st.v);
    } else { s.branchVoltage(k, a, b); s.add(k, k, 0, -ctx.omega * this.L); }
  }
  current(x) { return x[this.k]; }
  start(x, ctx) { ctx.state[this.name] = { v: this.voltage(x), i: x[this.k] }; }
  accept(x, ctx) { this.start(x, ctx); }
}

class VoltageSource extends Element {
  constructor(name, plus, minus, volts = 0) { super(name, [plus, minus]); this.volts = volts; this.nb = 1; }
  value() { return this.volts; }
  stamp(s, ctx) {
    const [a, b] = this.n, k = this.k;
    s.branch(a, b, k); s.branchVoltage(k, a, b);
    if (ctx.mode === "ac") s.rhs(k, ctx.acSource === this.name ? 1 : 0);
    else s.rhs(k, ctx.scale * this.value(ctx.t));
  }
  current(x) { return -x[this.k]; }
}

class PulseSource extends VoltageSource {
  constructor(name, plus, minus, o) {
    super(name, plus, minus, o.low ?? 0);
    Object.assign(this, { low: o.low ?? 0, high: o.high ?? 5, period: o.period ?? 1e-3, duty: o.duty ?? 0.5, delay: o.delay ?? 0, rise: o.rise ?? 0, fall: o.fall ?? 0 });
  }
  value(t) {
    if (t < this.delay) return this.low;
    const ph = (t - this.delay) % this.period, on = this.duty * this.period;
    if (this.rise > 0 && ph < this.rise) return this.low + ((this.high - this.low) * ph) / this.rise;
    if (ph < on) return this.high;
    if (this.fall > 0 && ph < on + this.fall) return this.high - ((this.high - this.low) * (ph - on)) / this.fall;
    return this.low;
  }
}

class SineSource extends VoltageSource {
  constructor(name, plus, minus, o) {
    super(name, plus, minus, o.offset ?? 0);
    this.amplitude = o.amplitude ?? 1; this.freq = o.freq ?? 50; this.offset = o.offset ?? 0; this.phase = ((o.phase_deg ?? 0) * Math.PI) / 180;
  }
  value(t) { return this.offset + this.amplitude * Math.sin(2 * Math.PI * this.freq * t + this.phase); }
}

class CurrentSource extends Element {
  constructor(name, a, b, amps) { super(name, [a, b]); this.amps = amps; }
  stamp(s, ctx) {
    if (ctx.mode === "ac") s.inject(this.n[0], this.n[1], ctx.acSource === this.name ? 1 : 0);
    else s.inject(this.n[0], this.n[1], ctx.scale * this.amps);
  }
  current() { return this.amps; }
  power(x) { return -this.voltage(x) * this.amps; }
}

class VCVS extends Element {
  constructor(name, p, m, cp, cm, gain) { super(name, [p, m, cp, cm]); this.gain = gain; this.nb = 1; }
  stamp(s) {
    const [p, m, cp, cm] = this.n;
    s.branch(p, m, this.k); s.branchVoltage(this.k, p, m); s.branchVoltage(this.k, cp, cm, -this.gain);
  }
  current(x) { return -x[this.k]; }
}

class VCCS extends Element {
  constructor(name, p, m, cp, cm, gm) { super(name, [p, m, cp, cm]); this.gm = gm; }
  stamp(s) {
    const [p, m, cp, cm] = this.n;
    s.add(p, cp, this.gm); s.add(p, cm, -this.gm); s.add(m, cp, -this.gm); s.add(m, cm, this.gm);
  }
  current(x) { return this.gm * this.voltage(x, 2, 3); }
  power(x, ctx) { return -this.voltage(x) * this.current(x, ctx); }
}

class Diode extends Element {
  constructor(name, anode, cathode, o = {}) {
    super(name, [anode, cathode]);
    this.nonlinear = true;
    this.Is = o.Is ?? 1e-14; this.nvt = (o.n ?? 1) * VT;
    this.vz = o.vz ?? null; this.iz = o.iz ?? 5e-3; this.nzvt = (o.nz ?? 1) * VT;
  }
  law(v) {
    const e = safeExp(v / this.nvt);
    let i = this.Is * (e - 1), g = (this.Is * e) / this.nvt;
    if (this.vz !== null) {
      const er = safeExp(-(v + this.vz) / this.nzvt);
      i -= this.iz * er; g += (this.iz * er) / this.nzvt;
    }
    return [i, g];
  }
  stamp(s, ctx) {
    if (ctx.mode === "ac") { s.conductance(this.n[0], this.n[1], this.law(this.voltage(ctx.xop))[1]); return; }
    const vNew = this.voltage(ctx.x), vOld = ctx.memory[this.name] ?? 0;
    let v, held;
    if (vNew >= 0 || this.vz === null) [v, held] = holdBack(vNew, vOld, this.Is, this.nvt);
    else {
      const rs = this.iz * Math.exp(-this.vz / this.nzvt);
      let w; [w, held] = holdBack(-vNew, -vOld, rs, this.nzvt); v = -w;
    }
    ctx.memory[this.name] = v;
    ctx.limited = ctx.limited || held;
    const [i, gd] = this.law(v);
    const g = gd + ctx.gmin;
    s.conductance(this.n[0], this.n[1], g);
    s.inject(this.n[0], this.n[1], i - g * v + ctx.gmin * v);
  }
  current(x) { return this.law(this.voltage(x))[0]; }
}

class BJT extends Element {
  constructor(name, c, b, e, o = {}, polarity = 1) {
    super(name, [c, b, e]);
    this.nonlinear = true; this.beta = o.beta ?? 100; this.betaR = o.beta_r ?? 1; this.Is = o.Is ?? 1e-14; this.p = polarity;
  }
  law(vbe, vbc) {
    const ef = safeExp(vbe / VT), er = safeExp(vbc / VT);
    const fw = this.Is * (ef - 1), rv = this.Is * (er - 1), gf = (this.Is * ef) / VT, gr = (this.Is * er) / VT;
    return {
      ic: fw - rv - rv / this.betaR, ib: fw / this.beta + rv / this.betaR,
      dic: [gf, -gr - gr / this.betaR], dib: [gf / this.beta, gr / this.betaR],
    };
  }
  junctions(x) {
    const [vc, vb, ve] = this.n.map((i) => nv(x, i));
    return [this.p * (vb - ve), this.p * (vb - vc)];
  }
  linearize(vbe, vbc) {
    const { ic, ib, dic, dib } = this.law(vbe, vbc);
    const rc = [-dic[1], dic[0] + dic[1], -dic[0]], rb = [-dib[1], dib[0] + dib[1], -dib[0]];
    const re = [0, 1, 2].map((i) => -(rc[i] + rb[i]));
    return [[this.p * ic, this.p * ib, -this.p * (ic + ib)], [rc, rb, re]];
  }
  stamp(s, ctx) {
    if (ctx.mode === "ac") { const [, jac] = this.linearize(...this.junctions(ctx.xop)); s.linearized(this.n, [0, 0, 0], [0, 0, 0], jac); return; }
    const [beN, bcN] = this.junctions(ctx.x), old = ctx.memory[this.name] ?? [0, 0];
    const [vbe, h1] = holdBack(beN, old[0], this.Is, VT), [vbc, h2] = holdBack(bcN, old[1], this.Is, VT);
    ctx.memory[this.name] = [vbe, vbc];
    ctx.limited = ctx.limited || h1 || h2;
    const ve = nv(ctx.x, this.n[2]), vb = ve + this.p * vbe, vc = vb - this.p * vbc;
    const [cur, jac] = this.linearize(vbe, vbc);
    s.linearized(this.n, [vc, vb, ve], cur, jac);
    s.conductance(this.n[1], this.n[2], ctx.gmin);
    s.conductance(this.n[1], this.n[0], ctx.gmin);
  }
  current(x, ctx, part) {
    const { ic, ib } = this.law(...this.junctions(x));
    return part === "b" ? ib : part === "e" ? ic + ib : ic;
  }
  power(x) { const [vbe, vbc] = this.junctions(x); const { ic, ib } = this.law(vbe, vbc); return (vbe - vbc) * ic + vbe * ib; }
}

class MOSFET extends Element {
  constructor(name, d, g, s, o = {}, polarity = 1) {
    super(name, [d, g, s]);
    this.nonlinear = true; this.vth = Math.abs(o.vth ?? 1); this.kp = o.k ?? 1e-3; this.lam = o.lam ?? 0; this.p = polarity;
  }
  law(vgs, vds) {
    const vov = vgs - this.vth, k = this.kp, l = this.lam;
    if (vov <= 0) return [0, 0, 0];
    if (vds < vov) return [k * (vov * vds - 0.5 * vds * vds) * (1 + l * vds), k * vds * (1 + l * vds), k * (vov - vds) * (1 + l * vds) + k * (vov * vds - 0.5 * vds * vds) * l];
    return [0.5 * k * vov * vov * (1 + l * vds), k * vov * (1 + l * vds), 0.5 * k * vov * vov * l];
  }
  channel(vd, vg, vs) {
    const p = this.p;
    if (p * (vd - vs) >= 0) { const [i, gm, gds] = this.law(p * (vg - vs), p * (vd - vs)); return [p * i, gm, gds, false]; }
    const [i, gm, gds] = this.law(p * (vg - vd), p * (vs - vd));
    return [-p * i, gm, gds, true];
  }
  jacobian(vd, vg, vs) {
    const [i, gm, gds, sw] = this.channel(vd, vg, vs);
    const rd = sw ? [gm + gds, -gm, -gds] : [gds, gm, -gm - gds];
    return [[i, 0, -i], [rd, [0, 0, 0], rd.map((v) => -v)]];
  }
  stamp(s, ctx) {
    if (ctx.mode === "ac") { const [, jac] = this.jacobian(...this.n.map((i) => nv(ctx.xop, i))); s.linearized(this.n, [0, 0, 0], [0, 0, 0], jac); return; }
    let [vd, vg, vs] = this.n.map((i) => nv(ctx.x, i));
    let vgs = vg - vs, vds = vd - vs;
    const old = ctx.memory[this.name];
    if (old) {
      const sg = Math.max(-1, Math.min(1, vgs - old[0])), sd = Math.max(-2, Math.min(2, vds - old[1]));
      ctx.limited = ctx.limited || sg !== vgs - old[0] || sd !== vds - old[1];
      vgs = old[0] + sg; vds = old[1] + sd;
    }
    ctx.memory[this.name] = [vgs, vds];
    vg = vs + vgs; vd = vs + vds;
    const [cur, jac] = this.jacobian(vd, vg, vs);
    s.linearized(this.n, [vd, vg, vs], cur, jac);
    s.conductance(this.n[0], this.n[2], ctx.gmin);
  }
  current(x) { const [vd, vg, vs] = this.n.map((i) => nv(x, i)); return this.p * this.channel(vd, vg, vs)[0]; }
  power(x) { const vd = nv(x, this.n[0]), vs = nv(x, this.n[2]); return (vd - vs) * this.p * this.current(x); }
}

class OpAmp extends Element {
  constructor(name, plus, minus, out, gain = 1e5, rails = null) {
    super(name, [plus, minus, out]); this.gain = gain; this.rails = rails; this.nb = 1; this.nonlinear = rails !== null;
  }
  transfer(vd) {
    if (!this.rails) return [this.gain * vd, this.gain];
    const [lo, hi] = this.rails, mid = 0.5 * (lo + hi), half = 0.5 * (hi - lo), u = (this.gain * vd) / half;
    if (Math.abs(u) > 40) return [mid + half * Math.sign(u), 0];
    const th = Math.tanh(u);
    return [mid + half * th, this.gain * (1 - th * th)];
  }
  stamp(s, ctx) {
    const [p, m, o] = this.n, k = this.k;
    s.branch(o, -1, k); s.add(k, o, 1);
    const x = ctx.mode === "ac" ? ctx.xop : ctx.x;
    let vd = this.voltage(x, 0, 1);
    if (this.rails && ctx.mode !== "ac") {
      const old = ctx.memory[this.name], half = 0.5 * (this.rails[1] - this.rails[0]), reach = (4 * half) / this.gain;
      if (old !== undefined && Math.abs(vd - old) > reach && Math.abs(old) < reach) { vd = old + Math.sign(vd - old) * reach; ctx.limited = true; }
      ctx.memory[this.name] = vd;
    }
    const [out, slope] = this.transfer(vd);
    s.branchVoltage(k, p, m, -slope);
    if (ctx.mode !== "ac") s.rhs(k, out - slope * vd);
  }
  current(x) { return -x[this.k]; }
  power(x) { return nv(x, this.n[2]) * this.current(x); }
}

class Context {
  constructor(mode, o = {}) {
    Object.assign(this, { mode, t: 0, dt: null, method: "trap", scale: 1, gmin: 1e-12, memory: {}, state: {}, limited: false, x: null, xop: null, omega: 0, acSource: null }, o);
  }
}

function splitName(name) {
  const i = name.lastIndexOf(".");
  return i > 0 ? [name.slice(0, i), name.slice(i + 1)] : [name, null];
}

class Result {
  constructor(circuit, x, ctx) { this.circuit = circuit; this.x = x; this.ctx = ctx; }
  v(node, ref = null) { let v = nv(this.x, this.circuit.index(node)); if (ref !== null) v -= nv(this.x, this.circuit.index(ref)); return v; }
  element(name) {
    if (this.circuit.elements.has(name)) return [this.circuit.elements.get(name), null];
    const [base, part] = splitName(name);
    if (!this.circuit.elements.has(base)) throw new Error(`unknown element ${name}`);
    return [this.circuit.elements.get(base), part];
  }
  i(name) { const [e, part] = this.element(name); return e.current(this.x, this.ctx, part); }
  p(name) { const [e] = this.element(name); return e.power(this.x, this.ctx); }
}

export class TransientResult {
  constructor(circuit, time, rows, ctx) { this.circuit = circuit; this.time = time; this.rows = rows; this.ctx = ctx; }
  at(n) { return new Result(this.circuit, this.rows[n], { ...this.ctx, t: this.time[n] }); }
  v(node, ref = null) { return this.rows.map((x, n) => this.at(n).v(node, ref)); }
  i(name) { return this.rows.map((x, n) => this.at(n).i(name)); }
  p(name) { return this.rows.map((x, n) => this.at(n).p(name)); }
  crossingTimes(values, level, direction = "rising") {
    const out = [];
    for (let n = 1; n < values.length; n++) {
      const a = values[n - 1] - level, b = values[n] - level;
      const rising = a < 0 && b >= 0, falling = a > 0 && b <= 0;
      if (((direction === "rising" || direction === "any") && rising) || ((direction === "falling" || direction === "any") && falling)) {
        const frac = a !== b ? a / (a - b) : 0;
        out.push(this.time[n - 1] + frac * (this.time[n] - this.time[n - 1]));
      }
    }
    return out;
  }
  timeToCross(node, level, direction = "rising") { const t = this.crossingTimes(this.v(node), level, direction); return t.length ? t[0] : Infinity; }
  frequency(node) {
    const v = this.v(node), q = Math.floor(v.length / 4), half = v.slice(q);
    const level = 0.5 * (maxOf(half) + minOf(half));
    const t = this.crossingTimes(v, level, "rising").filter((x) => x >= this.time[q]);
    return t.length < 2 ? 0 : (t.length - 1) / (t[t.length - 1] - t[0]);
  }
  interp(time, values) { return interp(time, this.time, values); }
}

export function interp(x, xs, ys) {
  if (x <= xs[0]) return ys[0];
  if (x >= xs[xs.length - 1]) return ys[ys.length - 1];
  let lo = 0, hi = xs.length - 1;
  while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (xs[mid] <= x) lo = mid; else hi = mid; }
  return ys[lo] + ((ys[hi] - ys[lo]) * (x - xs[lo])) / (xs[hi] - xs[lo]);
}

export class ACResult {
  constructor(circuit, freqs, re, im, source) { this.circuit = circuit; this.freqs = freqs; this.re = re; this.im = im; this.source = source; }
  phasor(node) { const i = this.circuit.index(node); return this.freqs.map((f, n) => (i < 0 ? [0, 0] : [this.re[n][i], this.im[n][i]])); }
  ratio(node, ref) {
    const a = this.phasor(node);
    if (!ref) return a;
    const b = this.phasor(ref);
    return a.map(([ar, ai], n) => { const [br, bi] = b[n], d = br * br + bi * bi; return [(ar * br + ai * bi) / d, (ai * br - ar * bi) / d]; });
  }
  gainDb(node, ref = null) { return this.ratio(node, ref).map(([r, i]) => 20 * Math.log10(Math.max(Math.hypot(r, i), 1e-300))); }
  phaseDeg(node, ref = null) {
    const raw = this.ratio(node, ref).map(([r, i]) => Math.atan2(i, r));
    const out = [raw[0]];
    for (let n = 1; n < raw.length; n++) {
      let d = raw[n] - raw[n - 1];
      d -= 2 * Math.PI * Math.round(d / (2 * Math.PI));
      out.push(out[n - 1] + d);
    }
    return out.map((p) => (p * 180) / Math.PI);
  }
  gainDbAt(freq, node, ref = null) { return interp(Math.log10(freq), this.freqs.map(Math.log10), this.gainDb(node, ref)); }
  cutoff(node, ref = null) {
    const g = this.gainDb(node, ref), lf = this.freqs.map(Math.log10);
    const peak = g.indexOf(maxOf(g)), target = g[peak] - 3.0103;
    for (let n = peak + 1; n < g.length; n++) if (g[n] <= target) return 10 ** interp(target, [g[n], g[n - 1]], [lf[n], lf[n - 1]]);
    for (let n = peak - 1; n >= 0; n--) if (g[n] <= target) return 10 ** interp(target, [g[n], g[n + 1]], [lf[n], lf[n + 1]]);
    return NaN;
  }
}

export class Circuit {
  constructor() { this.elements = new Map(); this.nodeIndex = new Map(); this.size = 0; this.dirty = true; }
  add(e) { if (this.elements.has(e.name)) throw new Error(`duplicate element ${e.name}`); this.elements.set(e.name, e); this.dirty = true; return e; }
  resistor(n, a, b, ohms) { return this.add(new Resistor(n, a, b, ohms)); }
  capacitor(n, a, b, f, v0 = 0) { return this.add(new Capacitor(n, a, b, f, v0)); }
  inductor(n, a, b, h, i0 = 0) { return this.add(new Inductor(n, a, b, h, i0)); }
  voltageSource(n, p, m, v) { return this.add(new VoltageSource(n, p, m, v)); }
  currentSource(n, a, b, amps) { return this.add(new CurrentSource(n, a, b, amps)); }
  pulseSource(n, p, m, o) { return this.add(new PulseSource(n, p, m, o)); }
  sineSource(n, p, m, o) { return this.add(new SineSource(n, p, m, o)); }
  switch(n, a, b, closed = true, toggleAt = []) { return this.add(new Switch(n, a, b, closed, toggleAt)); }
  vcvs(n, p, m, cp, cm, g) { return this.add(new VCVS(n, p, m, cp, cm, g)); }
  vccs(n, p, m, cp, cm, g) { return this.add(new VCCS(n, p, m, cp, cm, g)); }
  junction(name, anode, cathode, rs, law) {
    if (rs > 0) {
      const inner = `${name}.junction`;
      this.add(new Resistor(`${name}.rs`, anode, inner, rs)).hidden = true;
      return this.add(new Diode(name, inner, cathode, law));
    }
    return this.add(new Diode(name, anode, cathode, law));
  }
  diode(n, a, k, o = {}) {
    const m = DIODE_MODELS[(o.model || "default").toLowerCase()];
    return this.junction(n, a, k, o.rs ?? m.rs, { Is: o.Is ?? m.Is, n: o.n ?? m.n });
  }
  led(n, a, k, color = "red") {
    if (!(color in LED_COLORS)) throw new Error(`unknown LED color ${color}`);
    const nvt = LED_N * VT;
    return this.junction(n, a, k, 0, { Is: 0.01 / Math.expm1(LED_COLORS[color] / nvt), n: LED_N });
  }
  zener(n, a, k, vz = 5.1) { return this.junction(n, a, k, 0, { Is: 1e-14, n: 1, vz, iz: 5e-3, nz: 1 }); }
  npn(n, c, b, e, o = {}) { return this.add(new BJT(n, c, b, e, o, 1)); }
  pnp(n, c, b, e, o = {}) { return this.add(new BJT(n, c, b, e, o, -1)); }
  nmos(n, d, g, s, o = {}) { return this.add(new MOSFET(n, d, g, s, o, 1)); }
  pmos(n, d, g, s, o = {}) { return this.add(new MOSFET(n, d, g, s, o, -1)); }
  opamp(n, p, m, o, gain = 1e5, rails = null) { return this.add(new OpAmp(n, p, m, o, gain, rails)); }

  bind() {
    if (!this.dirty) return;
    this.nodeIndex = new Map();
    for (const e of this.elements.values()) for (const nd of e.nodeNames) if (!GROUND.has(String(nd)) && !this.nodeIndex.has(String(nd))) this.nodeIndex.set(String(nd), this.nodeIndex.size);
    let br = this.nodeIndex.size;
    for (const e of this.elements.values()) { e.bind((nd) => (GROUND.has(String(nd)) ? -1 : this.nodeIndex.get(String(nd))), br); br += e.nb; }
    this.size = br;
    this.dirty = false;
  }
  index(node) {
    this.bind();
    node = String(node);
    if (GROUND.has(node)) return -1;
    if (!this.nodeIndex.has(node)) throw new Error(`unknown node ${node}`);
    return this.nodeIndex.get(node);
  }
  get isLinear() { return ![...this.elements.values()].some((e) => e.nonlinear); }
  assemble(ctx, x, extraGmin = 0) {
    const s = new Stamper(this.size);
    ctx.x = x;
    for (const e of this.elements.values()) e.stamp(s, ctx);
    for (let i = 0; i < this.nodeIndex.size; i++) s.A[i * this.size + i] += ctx.gmin + extraGmin;
    return s;
  }
  newton(ctx, x, extraGmin = 0, maxIter = 150) {
    if (this.isLinear) { const s = this.assemble(ctx, x, extraGmin); return solveReal(s.A, s.b, this.size); }
    for (let it = 0; it < maxIter; it++) {
      ctx.limited = false;
      const s = this.assemble(ctx, x, extraGmin);
      const xn = solveReal(s.A, s.b, this.size);
      if (!xn.every(Number.isFinite)) throw new ConvergenceError("solution blew up");
      let settled = true;
      for (let i = 0; i < xn.length; i++) if (Math.abs(xn[i] - x[i]) > 1e-6 * Math.max(Math.abs(xn[i]), Math.abs(x[i])) + 1e-9) { settled = false; break; }
      x = xn;
      if (settled && !ctx.limited) return x;
    }
    throw new ConvergenceError("Newton-Raphson did not settle");
  }
  operatingPoint(ctx, x0 = null) {
    this.bind();
    x0 = x0 || new Float64Array(this.size);
    try { ctx.memory = {}; return this.newton(ctx, Float64Array.from(x0)); } catch (e) { if (!(e instanceof ConvergenceError)) throw e; }
    try {
      ctx.memory = {};
      let x = Float64Array.from(x0);
      for (let k = 0; k < 21; k++) x = this.newton(ctx, x, 10 ** (-2 - k * 0.5));
      return this.newton(ctx, x);
    } catch (e) { if (!(e instanceof ConvergenceError)) throw e; }
    ctx.memory = {};
    let x = new Float64Array(this.size);
    for (let k = 0; k < 50; k++) { ctx.scale = 0.02 + (0.98 * k) / 49; x = this.newton(ctx, x, 0, 400); }
    ctx.scale = 1;
    return x;
  }
  dc() { const ctx = new Context("dc"); return new Result(this, this.operatingPoint(ctx), ctx); }
  transient(tStop, dt, method = "trap") {
    this.bind();
    const steps = Math.round(tStop / dt);
    const time = Array.from({ length: steps + 1 }, (_, n) => n * dt);
    const ctx = new Context("ic", { dt, method });
    let x = this.operatingPoint(ctx);
    for (const e of this.elements.values()) e.start(x, ctx);
    const rows = [x];
    ctx.mode = "tran";
    for (let n = 1; n <= steps; n++) {
      x = this.advance(ctx, x, time[n - 1], dt, n > 1 ? method : "be", 0);
      rows.push(x);
    }
    return new TransientResult(this, time, rows, ctx);
  }
  advance(ctx, x, t0, dt, method, depth) {
    Object.assign(ctx, { t: t0 + dt, dt, method });
    let xn;
    try { xn = this.newton(ctx, Float64Array.from(x)); } catch (e) {
      if (!(e instanceof ConvergenceError) || depth > 10) throw e;
      const half = this.advance(ctx, x, t0, dt / 2, "be", depth + 1);
      return this.advance(ctx, half, t0 + dt / 2, dt / 2, "be", depth + 1);
    }
    for (const e of this.elements.values()) e.accept(xn, ctx);
    return xn;
  }
  ac(freqs, source = null) {
    this.bind();
    if (!source) {
      const srcs = [...this.elements.values()].filter((e) => e instanceof VoltageSource || e instanceof CurrentSource);
      const sines = srcs.filter((e) => e instanceof SineSource);
      source = (sines[0] || srcs[0]).name;
    }
    const xop = this.operatingPoint(new Context("dc"));
    const ctx = new Context("ac", { xop, acSource: source });
    const re = [], im = [];
    for (const f of freqs) {
      ctx.omega = 2 * Math.PI * f;
      ctx.x = xop;
      const s = new Stamper(this.size, true);
      for (const e of this.elements.values()) e.stampAC(s, ctx);
      for (let i = 0; i < this.nodeIndex.size; i++) s.A[i * this.size + i] += ctx.gmin;
      const [xr, xi] = solveComplex(s.A, s.Ai, s.b, s.bi, this.size);
      re.push(xr); im.push(xi);
    }
    return new ACResult(this, freqs, re, im, source);
  }
}
