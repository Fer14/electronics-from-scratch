// The browser twin of sim/lab.py: fill the slots, simulate by kind, measure every goal.

import { Circuit, interp, maxOf, minOf } from "./engine.js";
import { LogicCircuit } from "./logic.js";
import { Design, buildBlock } from "./cost.js";

export const TERMINALS = {
  battery: ["plus", "minus"], voltage_source: ["plus", "minus"], pulse_source: ["plus", "minus"], sine_source: ["plus", "minus"],
  current_source: ["from", "to"], resistor: ["a", "b"], capacitor: ["a", "b"], inductor: ["a", "b"], switch: ["a", "b"],
  wire: ["a", "b"], open: ["a", "b"], diode: ["anode", "cathode"], led: ["anode", "cathode"], zener: ["anode", "cathode"],
  npn: ["c", "b", "e"], pnp: ["c", "b", "e"], nmos: ["d", "g", "s"], pmos: ["d", "g", "s"], opamp: ["plus", "minus", "out"],
  vcvs: ["plus", "minus", "cplus", "cminus"], vccs: ["plus", "minus", "cplus", "cminus"],
};
const POSITIONAL = ["a", "b", "c", "d"];
const SLOT_KEYS = new Set(["id", "accepts", "label", "inputs", "output"]);

export const UNITS = {
  voltage: "V", voltage_at_time: "V", peak_voltage: "V", min_voltage: "V", ripple: "V",
  current: "A", current_at_time: "A", peak_current: "A", power: "W",
  time_to_cross: "s", frequency: "Hz", cutoff_frequency: "Hz", gain_db_at: "dB", phase_deg_at: "deg",
  area: "gate units", critical_path: "gate delays", latency: "cycles", throughput: "MACs/cycle",
  bits_moved: "bits/cycle", energy: "units", bits: "bits", gate_count: "gates", depth: "levels",
};

export function place(slot, part) {
  const comp = { ...part, id: slot.id };
  const own = TERMINALS[part.type];
  if (part.type === "gate") { comp.inputs = slot.inputs; comp.output = slot.output; }
  else if (own && own.every((n) => n in slot)) for (const n of own) comp[n] = slot[n];
  else if (own) { const given = POSITIONAL.filter((k) => k in slot).map((k) => slot[k]); own.forEach((n, i) => { if (i < given.length) comp[n] = given[i]; }); }
  else for (const [k, v] of Object.entries(slot)) if (!SLOT_KEYS.has(k)) comp[k] = v;
  return comp;
}

export function components(task, choice) {
  const items = [...(task.board.fixed || [])];
  for (const slot of task.board.slots || []) {
    const part = choice[slot.id];
    if (!part) throw new Error(`slot ${slot.id} is empty`);
    items.push(place(slot, part));
  }
  return items;
}

export function buildCircuit(task, choice) {
  const ground = task.board.ground || "gnd";
  const c = new Circuit();
  for (const comp of components(task, choice)) {
    const n = (k) => (comp[k] === ground ? "0" : comp[k]);
    const id = comp.id;
    switch (comp.type) {
      case "battery": case "voltage_source": c.voltageSource(id, n("plus"), n("minus"), comp.volts ?? 0); break;
      case "pulse_source": c.pulseSource(id, n("plus"), n("minus"), comp); break;
      case "sine_source": c.sineSource(id, n("plus"), n("minus"), comp); break;
      case "current_source": c.currentSource(id, n("from"), n("to"), comp.amps); break;
      case "resistor": c.resistor(id, n("a"), n("b"), comp.ohms); break;
      case "capacitor": c.capacitor(id, n("a"), n("b"), comp.farads, comp.v0 ?? 0); break;
      case "inductor": c.inductor(id, n("a"), n("b"), comp.henries, comp.i0 ?? 0); break;
      case "switch": c.switch(id, n("a"), n("b"), comp.closed ?? true, comp.toggle_at || []); break;
      case "wire": c.switch(id, n("a"), n("b"), true); break;
      case "open": c.switch(id, n("a"), n("b"), false); break;
      case "diode": c.diode(id, n("anode"), n("cathode"), { Is: comp.Is, n: comp.n, model: comp.model }); break;
      case "led": c.led(id, n("anode"), n("cathode"), comp.color || "red"); break;
      case "zener": c.zener(id, n("anode"), n("cathode"), comp.vz ?? 5.1); break;
      case "npn": c.npn(id, n("c"), n("b"), n("e"), { beta: comp.beta }); break;
      case "pnp": c.pnp(id, n("c"), n("b"), n("e"), { beta: comp.beta }); break;
      case "nmos": c.nmos(id, n("d"), n("g"), n("s"), { vth: comp.vth, k: comp.k }); break;
      case "pmos": c.pmos(id, n("d"), n("g"), n("s"), { vth: comp.vth, k: comp.k }); break;
      case "opamp": c.opamp(id, n("plus"), n("minus"), n("out"), comp.gain ?? 1e5, comp.rails || null); break;
      case "vcvs": c.vcvs(id, n("plus"), n("minus"), n("cplus"), n("cminus"), comp.gain); break;
      case "vccs": c.vccs(id, n("plus"), n("minus"), n("cplus"), n("cminus"), comp.gm); break;
      default: throw new Error(`unknown component type ${comp.type} in ${id}`);
    }
  }
  return c;
}

export function buildLogic(task, choice) {
  const lc = new LogicCircuit();
  lc.inputs(...(task.board.inputs || []));
  for (const comp of components(task, choice)) {
    if (comp.type === "gate") lc.gate(comp.op, comp.inputs, comp.output, comp.id);
    else if (comp.type === "dff") lc.dff(comp.d, comp.q, comp.id, comp.init ?? 0);
    else if (comp.type === "wire") lc.gate("buf", (comp.inputs || [comp.a]).slice(0, 1), comp.output ?? comp.b, comp.id);
    else throw new Error(`unknown logic part ${comp.type}`);
  }
  lc.outputs(...(task.board.outputs || []));
  return lc;
}

export function buildDesign(task, choice) {
  const d = new Design();
  for (const comp of components(task, choice)) {
    const params = {};
    for (const [k, v] of Object.entries(comp)) if (!["type", "id", "a", "b", "label"].includes(k)) params[k] = v;
    d.add(comp.id, buildBlock(comp.type, params), comp.a ?? "in", comp.b ?? "out");
  }
  return d;
}

export function transientSettings(task) {
  const sim = task.sim || {};
  const tStop = Number(sim.t_stop ?? 1);
  return [tStop, Number(sim.dt ?? tStop / 2000)];
}

export function acFreqs(task) {
  const sim = task.sim || {};
  const a = Math.log10(sim.f_start ?? 1), b = Math.log10(sim.f_stop ?? 1e6), n = Math.trunc(sim.points ?? 200);
  return [Array.from({ length: n }, (_, i) => 10 ** (a + ((b - a) * i) / (n - 1))), sim.source || null];
}

const gnd = (name, ground) => (name === ground ? "0" : name);

function voltageSeries(t, goal, ground) {
  if (goal.between) { const a = t.v(gnd(goal.between[0], ground)), b = t.v(gnd(goal.between[1], ground)); return a.map((v, i) => v - b[i]); }
  return t.v(gnd(goal.at, ground));
}

function measureDC(r, goal, ground) {
  switch (goal.measure) {
    case "voltage": return goal.between ? r.v(gnd(goal.between[0], ground), gnd(goal.between[1], ground)) : r.v(gnd(goal.at, ground));
    case "current": return r.i(goal.of);
    case "power": return r.p(goal.of);
    default: throw new Error(`measure ${goal.measure} is not available in a dc task`);
  }
}

function measureTransient(t, goal, ground) {
  const last = (a) => a[a.length - 1];
  switch (goal.measure) {
    case "voltage": return last(voltageSeries(t, goal, ground));
    case "voltage_at_time": return interp(goal.time, t.time, voltageSeries(t, goal, ground));
    case "current": return last(t.i(goal.of));
    case "current_at_time": return interp(goal.time, t.time, t.i(goal.of));
    case "power": return last(t.p(goal.of));
    case "time_to_cross": return t.crossingTimes(t.v(gnd(goal.at, ground)), goal.level, goal.direction || "rising")[0] ?? Infinity;
    case "frequency": return t.frequency(gnd(goal.at, ground));
    case "peak_voltage": return maxOf(voltageSeries(t, goal, ground));
    case "min_voltage": return minOf(voltageSeries(t, goal, ground));
    case "ripple": { const v = voltageSeries(t, goal, ground), tail = v.slice(Math.floor(v.length / 2)); return maxOf(tail) - minOf(tail); }
    case "peak_current": return maxOf(t.i(goal.of).map(Math.abs));
    default: throw new Error(`measure ${goal.measure} is not available in a transient task`);
  }
}

function measureAC(a, goal, ground) {
  const node = gnd(goal.at, ground), ref = goal.ref ? gnd(goal.ref, ground) : null;
  switch (goal.measure) {
    case "gain_db_at": return a.gainDbAt(goal.freq, node, ref);
    case "phase_deg_at": return interp(Math.log10(goal.freq), a.freqs.map(Math.log10), a.phaseDeg(node, ref));
    case "cutoff_frequency": return a.cutoff(node, ref);
    default: throw new Error(`measure ${goal.measure} is not available in an ac task`);
  }
}

function measureLogic(lc, goal, task) {
  switch (goal.measure) {
    case "truth_table": {
      const rows = lc.truthTable(task.board.inputs || [], Object.keys(goal.expect));
      let wrong = 0;
      rows.forEach((row, n) => { for (const [o, vals] of Object.entries(goal.expect)) if (row[o] !== vals[n]) wrong++; });
      return wrong;
    }
    case "sequence": {
      lc.reset();
      let wrong = 0;
      goal.steps.forEach((inputs, n) => { lc.step(inputs); for (const [name, vals] of Object.entries(goal.expect)) if ((lc.values[name] ?? 0) !== vals[n]) wrong++; });
      return wrong;
    }
    case "gate_count": return lc.gateCount();
    case "depth": return lc.depth();
    default: throw new Error(`measure ${goal.measure} is not available in a logic task`);
  }
}

function measureChip(d, goal) {
  if (goal.measure === "bits") { const b = d.blocks.get(goal.of).block; return b.params.acc_bits ?? b.params.bits ?? b.bits; }
  if (typeof d[goal.measure] !== "function") throw new Error(`measure ${goal.measure} is not available in a chip task`);
  return d[goal.measure]();
}

export function simulate(task, choice) {
  const kind = task.kind;
  if (["dc", "transient", "ac"].includes(kind)) {
    const c = buildCircuit(task, choice);
    if (kind === "dc") return { circuit: c, result: c.dc() };
    if (kind === "transient") return { circuit: c, result: c.transient(...transientSettings(task)) };
    const [freqs, source] = acFreqs(task);
    return { circuit: c, result: c.ac(freqs, source), op: c.dc() };
  }
  if (kind === "logic") return { result: buildLogic(task, choice) };
  if (kind === "chip") return { result: buildDesign(task, choice) };
  throw new Error(`unknown task kind ${kind}`);
}

export function evaluate(task, choice = task.solution || {}) {
  const ground = task.board.ground || "gnd";
  let model = null, error = null;
  try { model = simulate(task, choice); } catch (e) { error = e.message; }
  const results = (task.goals || []).map((goal) => {
    const label = goal.label || goal.measure;
    if (!model) return { label, goal, value: null, passed: false, error };
    try {
      const r = model.result;
      let value;
      if (task.kind === "dc") value = measureDC(r, goal, ground);
      else if (task.kind === "transient") value = measureTransient(r, goal, ground);
      else if (task.kind === "ac") value = measureAC(r, goal, ground);
      else if (task.kind === "logic") value = measureLogic(r, goal, task);
      else value = measureChip(r, goal);
      const passed = ["truth_table", "sequence"].includes(goal.measure)
        ? value === 0
        : Number.isFinite(value) && value >= (goal.min ?? -Infinity) && value <= (goal.max ?? Infinity);
      return { label, goal, value, passed, error: null };
    } catch (e) {
      return { label, goal, value: null, passed: false, error: e.message };
    }
  });
  return { results, model, error };
}

const PREFIXES = [[1e9, "G"], [1e6, "M"], [1e3, "k"], [1, ""], [1e-3, "m"], [1e-6, "µ"], [1e-9, "n"], [1e-12, "p"]];

export function eng(value, unit) {
  if (value === null || value === undefined) return "n/a";
  if (!Number.isFinite(value)) return value > 0 ? "never" : "n/a";
  if (value === 0) return `0 ${unit}`;
  for (const [s, p] of PREFIXES) if (Math.abs(value) >= s * 0.9995) return `${+(value / s).toPrecision(4)} ${p}${unit}`;
  return `${value.toExponential(2)} ${unit}`;
}

export function formatValue(value, measure) {
  if (value === null || value === undefined) return "n/a";
  if (measure === "truth_table" || measure === "sequence") return value === 0 ? "all rows right" : `${value} wrong`;
  const unit = UNITS[measure] || "";
  if (["V", "A", "W", "s", "Hz"].includes(unit)) return eng(value, unit);
  return `${+Number(value).toPrecision(4)} ${unit}`.trim();
}
