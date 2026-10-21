// The task page: board, parts tray, RUN, goals with measured values, playback and hints.

import { Board, partName, partValue } from "./board.js";
import { el, drawTwoTerminal, drawBJT, drawMOS, drawOpAmp, drawGate, drawBlock, drawFlop } from "./svg.js";
import { evaluate, formatValue, eng } from "../sim/lab.js";
import { maxOf } from "../sim/engine.js";
import { plot } from "./plot.js";
import { IsoView } from "../iso/view.js";
import { lessonStrip, refreshStrip } from "./strip.js";

const $ = (sel) => document.querySelector(sel);
const DRY = new URLSearchParams(location.search).has("check");
const store = {
  get(key, fallback) { try { const v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; } catch { return fallback; } },
  set(key, value) { if (DRY) return; try { localStorage.setItem(key, JSON.stringify(value)); } catch {} },
};

const ISO_KINDS = new Set(["dc", "transient", "ac"]);
const KIND_NAMES = { dc: "DC", transient: "transient", ac: "AC sweep", logic: "logic", chip: "chip" };

function icon(part, kind) {
  const svg = el("svg", { viewBox: "-30 -30 60 60", class: "part-icon", "aria-hidden": "true" });
  const g = el("g", {}, svg);
  if (part.type === "gate") { g.setAttribute("transform", "scale(0.72)"); drawGate(g, part.op, part.op === "not" ? 1 : 2); }
  else if (part.type === "dff") { g.setAttribute("transform", "scale(0.7)"); drawFlop(g); }
  else if (kind === "chip") { g.setAttribute("transform", "scale(0.62)"); drawBlock(g, part, false); }
  else if (part.type === "npn" || part.type === "pnp") { g.setAttribute("transform", "scale(0.85)"); drawBJT(g, part.type === "pnp"); }
  else if (part.type === "nmos" || part.type === "pmos") { g.setAttribute("transform", "scale(0.85)"); drawMOS(g, part.type === "pmos"); }
  else if (part.type === "opamp") { g.setAttribute("transform", "scale(0.55)"); drawOpAmp(g, "minus"); }
  else { g.setAttribute("transform", "scale(1.1)"); drawTwoTerminal(g, part); if (part.type === "led") svg.classList.add(`led-${part.color || "red"}`); }
  return svg;
}

function label(part, kind) {
  if (kind === "chip") {
    const size = part.bits ? `${part.bits} bit` : part.rows ? `${part.rows}×${part.cols}` : "";
    return [part.type.replace(/_/g, " "), [size, part.stages ? `${part.stages} stages` : "", part.acc_bits ? `acc ${part.acc_bits}` : ""].filter(Boolean).join(" · ")];
  }
  if (part.type === "gate") return [`${(part.op || "").toUpperCase()} gate`, ""];
  return [partName(part), partValue(part)];
}

async function loadTask() {
  const params = new URLSearchParams(location.search);
  const src = params.get("src") || (params.get("t") ? `tasks/${params.get("t")}.json` : null);
  if (!src) throw new Error("no task given: open this page from the lab index");
  const res = await fetch(src);
  if (!res.ok) throw new Error(`could not load ${src}`);
  return res.json();
}

class TaskPage {
  constructor(task, Board3D = null) {
    this.task = task;
    this.key = `efs-lab:${task.id}`;
    this.choice = store.get(`${this.key}:choice`, {});
    for (const id of Object.keys(this.choice)) if (!(task.board.slots || []).some((s) => s.id === id)) delete this.choice[id];
    this.selected = null;
    this.hintsShown = 0;
    this.inputs = Object.fromEntries((task.board.inputs || []).map((n) => [n, 0]));
    this.board = new Board($("#board"), task);
    this.board.onSlot = (id) => this.slotClicked(id);
    this.board.onToggle = (name) => this.toggleInput(name);
    this.focus = null;
    this.iso = null;
    if (ISO_KINDS.has(task.kind)) {
      this.iso = new IsoView($("#iso"), task, this.board);
      this.iso.onSlot = (id) => this.slotClicked(id);
    }
    this.b3d = null;
    if (ISO_KINDS.has(task.kind) && Board3D) {
      try {
        this.b3d = new Board3D($("#board3d"), task, this.board);
        this.b3d.onSlot = (id) => this.slotClicked(id);
        if (this.b3d.failed) this.b3d = null;
      } catch (e) { console.warn("Board 3D is off:", e); this.b3d = null; }
    }
    this.views = [this.iso, this.b3d].filter(Boolean);
    this.setupViews();
    this.fillHeader();
    this.fillTray();
    this.fillGoals(null);
    this.fillHints();
    this.redraw();
    $("#run").addEventListener("click", () => this.run());
    $("#reset").addEventListener("click", () => { this.choice = {}; this.save(); this.redraw(); });
    $("#hint").addEventListener("click", () => this.showHint());
  }

  // Schematic | Iso | Board 3D: all views are kept up to date, only one is shown; the choice is remembered.
  setupViews() {
    const bar = $("#view-bar");
    if (!this.iso) { bar.hidden = true; this.view = "schematic"; return; }
    bar.hidden = false;
    const board = bar.querySelector('[data-view="board"]');
    if (board) board.hidden = !this.b3d;
    let saved = null;
    try { saved = localStorage.getItem("efs-lab:view"); } catch {}
    this.view = saved === "schematic" || saved === "iso" ? saved : this.b3d ? "board" : "iso";
    if (this.view === "board" && !this.b3d) this.view = "iso";
    bar.querySelectorAll("button[data-view]").forEach((b) => b.addEventListener("click", () => this.setView(b.dataset.view, true)));
    this.setView(this.view, false);
  }

  setView(view, user) {
    this.view = view;
    if (user && !DRY) { try { localStorage.setItem("efs-lab:view", view); } catch {} }
    document.querySelectorAll("#view-bar button[data-view]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.view === view)));
    $("#board").hidden = view !== "schematic";
    $("#iso").hidden = view !== "iso";
    $("#board3d").hidden = view !== "board";
    if (view === "board" && this.b3d) this.b3d.relayout();
    if (!user) return;
    if (view === "iso") this.iso.relayout();
    else if (view === "schematic") this.board.fit();
  }

  each(method, ...args) {
    this.board[method](...args);
    for (const v of this.views) v[method](...args);
  }

  // Only the views that can show a thing get it (Iso and Board 3D: brightness, time, a status line).
  extra(method, ...args) { for (const v of this.views) if (v[method]) v[method](...args); }

  renderBoards() {
    this.board.render(this.choice);
    for (const v of this.views) v.render(this.choice, this.focus);
  }

  fillHeader() {
    const t = this.task;
    document.title = `${t.title} · Lab`;
    $("#kicker").textContent = `LAB ${t.id} · ${KIND_NAMES[t.kind] || t.kind}`;
    $("#title").textContent = t.title;
    $("#story").textContent = t.story || "";
    if (store.get("efs-lab:solved", {})[t.id]) $("#verdict").innerHTML = `<span class="solved">solved before</span>`;
  }

  fillTray() {
    const tray = $("#tray");
    tray.innerHTML = "";
    this.task.parts.forEach((part, index) => {
      const b = document.createElement("button");
      b.className = "part-chip";
      b.type = "button";
      b.setAttribute("aria-pressed", "false");
      const [name, value] = label(part, this.task.kind);
      b.append(icon(part, this.task.kind));
      const words = document.createElement("span");
      words.className = "part-words";
      words.innerHTML = `<span class="pname"></span><span class="pval"></span>`;
      words.firstChild.textContent = name;
      words.lastChild.textContent = value;
      b.append(words);
      this.dragSource(b, index);
      tray.append(b);
    });
  }

  dragSource(button, index) {
    let start = null, ghost = null;
    button.addEventListener("pointerdown", (ev) => { start = [ev.clientX, ev.clientY]; button.setPointerCapture(ev.pointerId); });
    button.addEventListener("pointermove", (ev) => {
      if (!start) return;
      if (!ghost && Math.hypot(ev.clientX - start[0], ev.clientY - start[1]) > 6) {
        ghost = button.cloneNode(true);
        ghost.classList.add("ghost");
        document.body.append(ghost);
        this.select(index);
      }
      if (ghost) { ghost.style.left = `${ev.clientX - 30}px`; ghost.style.top = `${ev.clientY - 22}px`; }
    });
    button.addEventListener("pointerup", (ev) => {
      if (ghost) {
        ghost.remove();
        ghost = null;
        const target = document.elementFromPoint(ev.clientX, ev.clientY);
        const slot = target && target.closest("[data-slot]");
        if (slot) this.slotClicked(slot.dataset.slot);
        else if (this.b3d && target && target.closest("#board3d")) {
          const id = this.b3d.slotAt(ev.clientX, ev.clientY);
          if (id) this.slotClicked(id);
        }
      } else if (start) {
        this.select(this.selected === index ? null : index);
      }
      start = null;
    });
    button.addEventListener("pointercancel", () => { if (ghost) ghost.remove(); ghost = null; start = null; });
    button.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); this.select(this.selected === index ? null : index); } });
  }

  select(index) {
    this.selected = index;
    document.querySelectorAll(".part-chip").forEach((b, i) => b.setAttribute("aria-pressed", String(i === index)));
    this.say(index === null ? "" : "Now click a slot (a dashed box, or a socket in 3D) to put the part there.");
    $("#board").classList.toggle("placing", index !== null);
    $("#iso").classList.toggle("placing", index !== null);
    $("#board3d").classList.toggle("placing", index !== null);
  }

  say(msg, warn = false) {
    const s = $("#status");
    s.textContent = msg;
    s.classList.toggle("warn", warn);
  }

  slotClicked(id) {
    const slot = this.task.board.slots.find((s) => s.id === id);
    if (this.selected !== null) {
      const part = this.task.parts[this.selected];
      if (slot.accepts && slot.accepts.length && !slot.accepts.includes(part.type)) {
        this.say(`${id} takes ${slot.accepts.map((t) => partName({ type: t })).join(" or ")}, not ${partName(part)}.`, true);
        return;
      }
      this.choice[id] = part;
      this.focus = id;
      this.select(null);
      this.say(`${label(part, this.task.kind).join(" ")} in ${id}.`);
    } else if (this.choice[id]) {
      delete this.choice[id];
      this.say(`${id} emptied.`);
    } else {
      this.say("Pick a part from the tray first.");
      return;
    }
    this.save();
    this.redraw();
  }

  save() { store.set(`${this.key}:choice`, this.choice); }

  redraw() {
    this.stopPlayback();
    this.renderBoards();
    this.fillGoals(null);
    $("#plot").innerHTML = "";
    $("#extra").innerHTML = "";
    if (this.task.kind === "logic") this.liveLogic();
  }

  filled() { return (this.task.board.slots || []).every((s) => this.choice[s.id]); }

  fillGoals(results) {
    const ul = $("#goals");
    ul.innerHTML = "";
    this.task.goals.forEach((goal, i) => {
      const r = results ? results[i] : null;
      const li = document.createElement("li");
      li.className = r ? (r.passed ? "pass" : "fail") : "pending";
      const mark = document.createElement("span");
      mark.className = "mark";
      mark.textContent = r ? (r.passed ? "✓" : "✗") : "○";
      mark.setAttribute("aria-label", r ? (r.passed ? "passed" : "failed") : "not run yet");
      const words = document.createElement("span");
      words.className = "goal-text";
      words.textContent = goal.label || goal.measure;
      const val = document.createElement("span");
      val.className = "measured";
      val.textContent = r ? (r.error ? r.error : formatValue(r.value, goal.measure)) : "";
      li.append(mark, words, val);
      ul.append(li);
    });
    if (!results) $("#verdict").innerHTML = store.get("efs-lab:solved", {})[this.task.id] ? `<span class="solved">solved before</span>` : "";
  }

  fillHints() {
    const hints = this.task.hints || [];
    $("#hints-panel").hidden = hints.length === 0;
    $("#hint").textContent = `Show a hint (${hints.length} left)`;
  }

  showHint() {
    const hints = this.task.hints || [];
    if (this.hintsShown >= hints.length) return;
    const li = document.createElement("li");
    li.textContent = hints[this.hintsShown++];
    $("#hints").append(li);
    const left = hints.length - this.hintsShown;
    $("#hint").textContent = left ? `Show a hint (${left} left)` : "No more hints";
    $("#hint").disabled = left === 0;
  }

  run() {
    if (!this.filled()) {
      const empty = this.task.board.slots.filter((s) => !this.choice[s.id]).map((s) => s.id);
      this.say(`Fill every slot first: ${empty.join(", ")} still empty.`, true);
      return;
    }
    this.stopPlayback();
    this.renderBoards();
    const { results, model, error } = evaluate(this.task, this.choice);
    this.fillGoals(results);
    if (error || !model) { this.say(`The simulation failed: ${error}`, true); return; }
    const ok = results.every((r) => r.passed);
    $("#verdict").innerHTML = ok ? `<span class="solved">All goals met. Solved.</span>` : `<span class="notyet">${results.filter((r) => !r.passed).length} goal(s) not met yet.</span>`;
    if (ok) { const solved = store.get("efs-lab:solved", {}); solved[this.task.id] = true; store.set("efs-lab:solved", solved); refreshStrip(); }
    this.say(ok ? "Every goal passes." : "Look at the measured values and try another part.");
    const kind = this.task.kind;
    if (kind === "dc") this.showDC(model.result);
    else if (kind === "transient") this.showTransient(model.result);
    else if (kind === "ac") this.showAC(model.result);
    else if (kind === "logic") this.showLogic(model.result);
    else this.showChip(model.result);
  }

  nodeNames() { return Object.keys(this.task.board.nodes || {}).filter((n) => n !== (this.task.board.ground || "gnd")); }

  readingsAt(r) {
    const out = {};
    for (const f of this.board.flows) {
      if (f.part) continue;
      try {
        const i = r.i(f.id), p = r.p(f.id);
        out[f.id] = `${eng(Math.abs(i) < 1e-12 ? 0 : i, "A")} · ${eng(Math.abs(p) < 1e-12 ? 0 : p, "W")}`;
        this.board.setLit(f.id, i > 1e-3);
        this.extra("setLevel", f.id, i, p);
      } catch {}
    }
    return out;
  }

  showDC(r) {
    const volts = {};
    for (const n of this.nodeNames()) { try { volts[n] = r.v(n); } catch {} }
    this.each("showVoltages", volts);
    this.each("showReadings", this.readingsAt(r));
    const currents = new Map(this.board.flows.map((f) => [f, safe(() => r.i(f.id))]));
    const scale = Math.max(0, maxOf([...currents.values()].map(Math.abs)));
    this.each("startFlow", (f) => currents.get(f), scale);
  }

  showTransient(t) {
    const n = t.time.length;
    const flows = new Map(this.board.flows.map((f) => [f, safe(() => t.i(f.id), null)]));
    const scale = Math.max(0, ...[...flows.values()].filter(Boolean).map((a) => maxOf(a.map(Math.abs))));
    const nodes = [...new Set(this.task.goals.map((g) => g.at).filter(Boolean))];
    const watch = nodes.length ? nodes : this.nodeNames().slice(0, 2);
    const ground = this.task.board.ground || "gnd";
    const traces = watch.map((nd) => ({ name: `v(${nd})`, y: t.v(nd === ground ? "0" : nd) }));
    const marks = [];
    for (const g of this.task.goals) {
      if (g.level !== undefined) marks.push({ y: g.level });
      if (g.time !== undefined) marks.push({ x: g.time });
    }
    const chart = plot($("#plot"), { x: t.time, series: traces, xLabel: "time", yUnit: "V", marks });
    const box = $("#playback");
    box.hidden = false;
    const slider = $("#scrub"), clock = $("#clock"), play = $("#play");
    slider.max = String(n - 1);
    let index = 0, playing = true, last = performance.now();
    const duration = 6000;
    const show = () => {
      const r = t.at(index);
      const volts = {};
      for (const nd of this.nodeNames()) volts[nd] = safe(() => r.v(nd));
      this.extra("setTime", t.time[index]);
      this.each("showVoltages", volts);
      this.each("showReadings", this.readingsAt(r));
      slider.value = String(index);
      clock.textContent = `t = ${eng(t.time[index], "s")}`;
      chart.setCursor(t.time[index]);
    };
    this.each("startFlow", (f) => { const a = flows.get(f); return a ? a[index] : 0; }, scale);
    const step = (now) => {
      if (playing) {
        index = Math.min(n - 1, index + Math.max(1, Math.round(((now - last) / duration) * n)));
        if (index >= n - 1) { playing = false; play.textContent = "replay"; }
        show();
      }
      last = now;
      this.playRaf = requestAnimationFrame(step);
    };
    play.textContent = "pause";
    play.onclick = () => {
      if (!playing && index >= n - 1) index = 0;
      playing = !playing;
      play.textContent = playing ? "pause" : "play";
    };
    slider.oninput = () => { playing = false; play.textContent = "play"; index = Number(slider.value); show(); };
    show();
    this.playRaf = requestAnimationFrame(step);
  }

  stopPlayback() {
    if (this.playRaf) cancelAnimationFrame(this.playRaf);
    this.playRaf = null;
    this.each("stopFlow");
    const box = $("#playback");
    if (box) box.hidden = true;
  }

  showAC(a) {
    this.extra("setState", "AC sweep · see the plot below");
    const ground = this.task.board.ground || "gnd";
    const nodes = [...new Set(this.task.goals.map((g) => g.at).filter(Boolean))];
    const traces = nodes.map((nd) => ({ name: `gain ${nd}`, y: a.gainDb(nd === ground ? "0" : nd, null) }));
    const marks = [];
    for (const g of this.task.goals) {
      if (g.freq !== undefined) marks.push({ x: g.freq });
      if (g.measure === "gain_db_at" && g.min !== undefined) marks.push({ y: g.min });
      if (g.measure === "gain_db_at" && g.max !== undefined) marks.push({ y: g.max });
    }
    plot($("#plot"), { x: a.freqs, series: traces, xLabel: "frequency", xUnit: "Hz", yUnit: "dB", logX: true, marks });
  }

  liveLogic() {
    if (!this.filled()) { this.board.showLogic(null); return; }
    const { model } = evaluate(this.task, this.choice);
    if (!model) return;
    const lc = model.result;
    try { this.board.showLogic(lc.settle({ ...this.inputs })); } catch (e) { this.say(e.message, true); }
  }

  toggleInput(name) {
    this.inputs[name] = this.inputs[name] ? 0 : 1;
    if (!this.filled()) { this.say("Fill every slot to try the inputs.", true); this.inputs[name] = 0; return; }
    this.liveLogic();
  }

  showLogic(lc) {
    this.liveLogic();
    const goal = this.task.goals.find((g) => g.measure === "truth_table");
    if (!goal) return;
    const inputs = this.task.board.inputs || [];
    const outs = Object.keys(goal.expect);
    const rows = lc.truthTable(inputs, outs);
    const table = document.createElement("table");
    table.className = "truth";
    const head = table.createTHead().insertRow();
    for (const c of [...inputs, ...outs.map((o) => `${o} want`), ...outs.map((o) => `${o} got`)]) { const th = document.createElement("th"); th.textContent = c; head.append(th); }
    const body = table.createTBody();
    const wrongRow = (row, n) => outs.some((o) => row[o] !== goal.expect[o][n]);
    let shown = rows.map((row, n) => [row, n]);
    if (rows.length > 16) {
      const wrong = shown.filter(([row, n]) => wrongRow(row, n));
      shown = wrong.length ? wrong.slice(0, 32) : shown.slice(0, 8);
      const note = document.createElement("p");
      note.className = "table-note";
      note.textContent = wrong.length ? `${wrong.length} of ${rows.length} rows are wrong; the first ones:` : `All ${rows.length} rows are right; the first 8:`;
      $("#extra").append(note);
    }
    for (const [row, n] of shown) {
      const tr = body.insertRow();
      for (const i of inputs) tr.insertCell().textContent = row[i];
      for (const o of outs) tr.insertCell().textContent = goal.expect[o][n];
      for (const o of outs) { const td = tr.insertCell(); td.textContent = row[o]; if (row[o] !== goal.expect[o][n]) td.className = "bad"; }
    }
    $("#extra").append(table);
  }

  showChip(d) {
    const readings = {};
    for (const [id, { block }] of d.blocks) readings[id] = `area ${block.area} · ${block.latency ? "registered" : `delay ${block.delay}`}`;
    this.board.showReadings(readings);
    this.board.startFlow(() => 1, 1);
    const rows = [["area", d.area(), "gate units"], ["critical path", d.critical_path(), "gate delays"], ["latency", d.latency(), "cycles"], ["throughput", d.throughput(), "MACs / cycle"], ["bits moved", d.bits_moved(), "per cycle"]];
    const table = document.createElement("table");
    table.className = "truth";
    for (const [k, v, u] of rows) { const tr = table.insertRow(); tr.insertCell().textContent = k; tr.insertCell().textContent = String(+(+v).toPrecision(6)); tr.insertCell().textContent = u; }
    $("#extra").append(table);
  }
}

function safe(fn, fallback = 0) { try { return fn(); } catch { return fallback; } }

window.addEventListener("error", (ev) => { document.body.dataset.error = ev.message; });

// Board 3D needs three.js from the CDN; if it cannot load, the page keeps the Schematic and Iso views.
async function loadBoard3D(task) {
  if (!ISO_KINDS.has(task.kind)) return null;
  try {
    const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error("three.js took too long")), 10000));
    const mod = await Promise.race([import("../board3d/view.js"), timeout]);
    return mod.Board3D;
  } catch (e) {
    console.warn("Board 3D is off:", e.message);
    return null;
  }
}

loadTask().then(async (task) => {
  lessonStrip(task.id);
  const page = new TaskPage(task, await loadBoard3D(task));
  window.labPage = page; // handy in the console (and for the screenshot checks)
  const params = new URLSearchParams(location.search);
  if (params.has("check")) {
    page.choice = { ...(task.solution || {}) };
    page.redraw();
    page.run();
    const marks = [...document.querySelectorAll("#goals li")].map((li) => li.className);
    document.body.dataset.check = marks.every((m) => m === "pass") ? "pass" : marks.join(",");
  }
}).catch((e) => {
  document.body.dataset.error = e.message;
  $("#title").textContent = "Task not found";
  $("#story").textContent = e.message;
});

