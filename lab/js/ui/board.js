// Draws a task's board on a grid and animates current as dots moving along the wires.

import { el, text, H, drawTwoTerminal, drawBJT, drawMOS, drawOpAmp, drawGate, gatePins, drawFlop, drawBlock } from "./svg.js";
import { place, eng } from "../sim/lab.js";

export const GRID = 72;
const MARGIN = 56;

export function partValue(p) {
  switch (p.type) {
    case "resistor": return eng(p.ohms, "Ω");
    case "capacitor": return eng(p.farads, "F");
    case "inductor": return eng(p.henries, "H");
    case "battery": case "voltage_source": return eng(p.volts ?? 0, "V");
    case "current_source": return eng(p.amps, "A");
    case "pulse_source": return `${eng(p.high ?? 5, "V")} · ${eng(1 / (p.period ?? 1e-3), "Hz")}`;
    case "sine_source": return `${eng(p.amplitude ?? 1, "V")} · ${eng(p.freq ?? 50, "Hz")}`;
    case "led": return `${p.color || "red"}`;
    case "zener": return `${p.vz ?? 5.1} V`;
    case "diode": return (p.model || "si").toUpperCase();
    case "npn": case "pnp": return `β ${p.beta ?? 100}`;
    case "nmos": case "pmos": return `Vth ${p.vth ?? 1} V`;
    case "opamp": return p.rails ? `${p.rails[0]}…${p.rails[1]} V` : "";
    case "switch": return p.closed === false ? "open" : "closed";
    case "gate": return (p.op || "").toUpperCase();
    case "vcvs": return `${p.gain}·v(${p.cplus},${p.cminus})`;
    case "vccs": return `${eng(p.gm, "S")}·v(${p.cplus},${p.cminus})`;
    default: return "";
  }
}

export function partName(p) {
  const names = { battery: "battery", voltage_source: "source", pulse_source: "pulse", sine_source: "sine", current_source: "current source",
    resistor: "resistor", capacitor: "capacitor", inductor: "inductor", diode: "diode", led: "LED", zener: "zener", switch: "switch",
    wire: "wire", open: "nothing", vcvs: "controlled voltage source", vccs: "controlled current source", npn: "NPN", pnp: "PNP", nmos: "N-MOSFET", pmos: "P-MOSFET", opamp: "op-amp", gate: "gate", dff: "flip-flop" };
  return names[p.type] || p.type.replace(/_/g, " ");
}

const SOURCE_TYPES = new Set(["battery", "voltage_source", "pulse_source", "sine_source", "vcvs"]);
const THREE = new Set(["npn", "pnp", "nmos", "pmos"]);
const CHIP = new Set(["adder", "multiplier", "mac", "register", "pipelined_multiplier", "mux", "register_file", "sram", "dram", "systolic_array", "gates"]);

export class Board {
  constructor(host, task) {
    this.host = host;
    this.task = task;
    this.nodes = { ...autoLayout(task), ...(task.board.nodes || {}) };
    this.ground = task.board.ground || "gnd";
    const xs = Object.values(this.nodes).map((p) => p[0]), ys = Object.values(this.nodes).map((p) => p[1]);
    this.minX = Math.min(0, ...xs); this.minY = Math.min(0, ...ys);
    this.maxX = Math.max(...xs, 1); this.maxY = Math.max(...ys, 1);
    this.flows = [];
    this.dots = [];
    this.running = false;
    this.onSlot = null;
    this.logicValues = null;
  }

  px(name) {
    const p = this.nodes[name];
    if (!p) return [MARGIN, MARGIN];
    return [MARGIN + (p[0] - this.minX) * GRID, MARGIN + (p[1] - this.minY) * GRID];
  }

  render(choice = {}, highlight = null) {
    this.host.innerHTML = "";
    const w = (this.maxX - this.minX) * GRID + 2 * MARGIN + 90, h = (this.maxY - this.minY) * GRID + 2 * MARGIN;
    this.svg = el("svg", { viewBox: `0 0 ${w} ${h}`, class: "board-svg", role: "img", "aria-label": "schematic" }, this.host);
    this.layers = {
      wires: el("g", { class: "wires" }, this.svg),
      parts: el("g", { class: "parts" }, this.svg),
      dots: el("g", { class: "dots" }, this.svg),
      nodes: el("g", { class: "nodes" }, this.svg),
      labels: el("g", { class: "labels" }, this.svg),
    };
    this.flows = [];
    this.nodeLabels = {};
    this.partLabels = {};
    this.uses = {};
    this.partGroups = {};
    const items = [];
    const fixed = [...(this.task.board.fixed || [])];
    fixed.sort((p, q) => SOURCE_TYPES.has(p.type) - SOURCE_TYPES.has(q.type));
    this.segments = [];
    this.labelBoxes = [];
    this.loops = 0;
    for (const comp of fixed) items.push({ comp, slot: null });
    for (const slot of this.task.board.slots || []) items.push({ comp: choice[slot.id] ? place(slot, choice[slot.id]) : null, slot });
    for (const item of items) this.drawItem(item, highlight);
    this.drawNodes();
    this.fitted = false;
    this.fit();
    return this.svg;
  }

  fit() {
    try {
      const bb = this.svg.getBBox();
      if (bb.width > 0) this.svg.setAttribute("viewBox", `${bb.x - 24} ${bb.y - 30} ${bb.width + 90} ${bb.height + 54}`);
    } catch {}
  }

  touch(node) { this.uses[node] = (this.uses[node] || 0) + 1; }

  wire(points, cls = "wire", net = null) {
    for (let i = 1; i < points.length; i++) this.segments.push({ A: points[i - 1], B: points[i], net });
    el("polyline", { points: points.map((p) => p.join(",")).join(" "), class: cls }, this.layers.wires);
  }

  overlaps(P, Q, net = null) {
    const vertical = Math.abs(P[0] - Q[0]) < 1, horizontal = Math.abs(P[1] - Q[1]) < 1;
    const span = (a, b, c, d) => Math.min(Math.max(a, b), Math.max(c, d)) - Math.max(Math.min(a, b), Math.min(c, d));
    return this.segments.some(({ A, B, net: other }) => {
      if (net !== null && other === net) return false;
      if (vertical && Math.abs(A[0] - B[0]) < 1 && Math.abs(A[0] - P[0]) < 1) return span(P[1], Q[1], A[1], B[1]) > 4;
      if (horizontal && Math.abs(A[1] - B[1]) < 1 && Math.abs(A[1] - P[1]) < 1) return span(P[0], Q[0], A[0], B[0]) > 4;
      return false;
    });
  }

  symbolLeg(pts) {
    let leg = 0;
    const len = (j) => Math.hypot(pts[j + 1][0] - pts[j][0], pts[j + 1][1] - pts[j][1]);
    for (let i = 1; i < pts.length - 1; i++) if (len(i) > len(leg) + 1) leg = i;
    return leg;
  }

  clear(pts, netA, netB) {
    const leg = this.symbolLeg(pts);
    for (let i = 1; i < pts.length; i++) {
      const net = i - 1 < leg ? netA : i - 1 > leg ? netB : null;
      if (this.overlaps(pts[i - 1], pts[i], net)) return false;
    }
    return true;
  }

  choose(P, Q, preferH, netA, netB) {
    const width = (this.maxX - this.minX) * GRID + 2 * MARGIN;
    const first = this.route(P, Q, preferH);
    const options = [first, this.route(P, Q, !preferH)];
    const awayX = P[0] > width * 0.6 ? 1 : -1;
    for (const k of [1, -1, 2, -2]) {
      const ox = k * awayX * GRID * 1.2, oy = k * GRID * 1.2;
      options.push([P, [P[0] + ox, P[1]], [P[0] + ox, Q[1]], Q]);
      options.push([P, [P[0], P[1] + oy], [Q[0], P[1] + oy], Q]);
      options.push([P, [Q[0] + ox, P[1]], [Q[0] + ox, Q[1]], Q]);
    }
    const tidy = (pts) => pts.filter((p, i) => i === 0 || Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]) > 0.5);
    const ok = options.map(tidy).find((pts) => this.clear(pts, netA, netB) && pts.every((p) => p[0] > 4 && p[1] > 4));
    return ok || tidy(first);
  }

  route(P, Q, preferH = true) {
    if (Math.abs(P[0] - Q[0]) < 1 || Math.abs(P[1] - Q[1]) < 1) return [P, Q];
    return preferH ? [P, [Q[0], P[1]], Q] : [P, [P[0], Q[1]], Q];
  }

  drawItem({ comp, slot }, highlight) {
    const kind = this.task.kind;
    const shown = comp || (slot ? { ...slot, type: "slot" } : null);
    if (!shown) return;
    if (kind === "logic") return this.drawLogicItem(comp, slot);
    if (THREE.has(shown.type)) return this.drawThree(comp, slot);
    if (shown.type === "opamp") return this.drawOpAmpItem(comp, slot);
    const ends = this.endpoints(shown, slot);
    if (!ends) return;
    this.drawTwo(comp, slot, ends, highlight);
  }

  endpoints(comp, slot) {
    const order = { battery: ["plus", "minus"], voltage_source: ["plus", "minus"], pulse_source: ["plus", "minus"], sine_source: ["plus", "minus"],
      current_source: ["from", "to"], vcvs: ["plus", "minus"], vccs: ["plus", "minus"], diode: ["anode", "cathode"], led: ["anode", "cathode"], zener: ["anode", "cathode"] }[comp.type];
    if (order && comp[order[0]] !== undefined) return [comp[order[0]], comp[order[1]]];
    if (comp.a !== undefined) return [comp.a, comp.b];
    const src = slot || comp;
    for (const pair of [["plus", "minus"], ["anode", "cathode"], ["from", "to"], ["c", "e"], ["d", "s"]]) if (src[pair[0]] !== undefined) return [src[pair[0]], src[pair[1]]];
    return null;
  }

  drawTwo(comp, slot, [a, b], highlight) {
    const P = this.px(a), Q = this.px(b);
    this.touch(a); this.touch(b);
    const chip = this.task.kind === "chip";
    const dx = Q[0] - P[0], dy = Q[1] - P[1];
    const pts = this.choose(P, Q, Math.abs(dx) >= Math.abs(dy), a, b);
    const leg = this.symbolLeg(pts);
    const L0 = pts[leg], L1 = pts[leg + 1];
    const legLen = Math.hypot(L1[0] - L0[0], L1[1] - L0[1]) || 1;
    const dir = [(L1[0] - L0[0]) / legLen, (L1[1] - L0[1]) / legLen];
    const center = [(L0[0] + L1[0]) / 2, (L0[1] + L1[1]) / 2];
    const half = chip ? (comp && comp.type === "register" ? 14 : comp && comp.type === "wire" ? H + 18 : 40) : H;
    const angle = (Math.atan2(dir[1], dir[0]) * 180) / Math.PI;
    const leadIn = chip && comp && comp.type !== "wire" && comp.type !== "register" ? half : chip ? H + 18 : H;
    const sIn = [center[0] - dir[0] * leadIn, center[1] - dir[1] * leadIn], eIn = [center[0] + dir[0] * leadIn, center[1] + dir[1] * leadIn];
    this.wire([...pts.slice(0, leg + 1), sIn], "wire", a);
    this.wire([eIn, ...pts.slice(leg + 1)], "wire", b);
    this.segments.push({ A: sIn, B: eIn, net: null });
    const upright = Math.abs(angle) > 90 && !(comp && ["battery", "diode", "led", "zener", "current_source", "vcvs", "vccs", "voltage_source"].includes(comp.type)) ? angle + 180 : angle;
    const g = el("g", { transform: `translate(${center[0]},${center[1]}) rotate(${upright})`, class: "part" }, this.layers.parts);
    const id = slot ? slot.id : comp.id;
    this.partGroups[id] = g;
    if (!comp) {
      this.drawEmptySlot(g, slot, chip ? 44 : 26);
    } else {
      if (slot) g.classList.add("filled");
      if (chip && CHIP.has(comp.type) || (chip && comp.type === "wire")) drawBlock(g, comp, !!slot);
      else drawTwoTerminal(g, comp);
      if (comp.type === "led") g.classList.add(`led-${comp.color || "red"}`);
      if (slot) this.makeSlotTarget(g, slot, chip ? 46 : 28, true);
    }
    const rot = upright === angle ? angle : upright;
    g.querySelectorAll(".pol").forEach((t) => t.setAttribute("transform", `rotate(${-rot} ${t.getAttribute("x")} ${Number(t.getAttribute("y")) - 4})`));
    const width = (this.maxX - this.minX) * GRID + 2 * MARGIN;
    const side = leg > 0 && pts.length === 4 ? Math.sign(pts[1][0] - pts[0][0]) || 1 : center[0] > width * 0.6 ? -1 : 1;
    const first = Math.abs(dir[0]) > 0.5 ? [0, leg > 0 && pts.length === 4 ? Math.sign(pts[1][1] - pts[0][1]) || -1 : -1] : [side, 0];
    const off = chip ? 30 : 24;
    const titleText = comp ? `${id}${partValue(comp) && !chip ? "  " + partValue(comp) : ""}` : `${id} ?`;
    const placeAt = (normal, shift = 0) => {
      const lp = [center[0] + normal[0] * (off + 4), center[1] + normal[1] * off + (normal[1] < 0 ? -2 : 4) + shift];
      const anchor = normal[0] > 0 ? "start" : normal[0] < 0 ? "end" : "middle";
      const w = Math.max(titleText.length * 7, 150);
      const x0 = anchor === "start" ? lp[0] : anchor === "end" ? lp[0] - w : lp[0] - w / 2;
      const y0 = normal[1] < 0 ? lp[1] - 24 : lp[1] - 12;
      return { lp, anchor, normal, box: [x0, y0, x0 + w, y0 + 30] };
    };
    const hits = (b) => this.labelBoxes.some((o) => b[0] < o[2] && b[2] > o[0] && b[1] < o[3] && b[3] > o[1]);
    const flip = [-first[0], -first[1]];
    const vertical = first[1] === 0;
    const spots = [placeAt(first), placeAt(flip)];
    if (vertical) for (const shift of [40, -40, 70, -70]) spots.push(placeAt(first, shift), placeAt(flip, shift));
    const spot = spots.find((c) => !hits(c.box)) || spots[0];
    this.labelBoxes.push(spot.box);
    const { lp, anchor, normal } = spot;
    const label = el("g", {}, this.layers.labels);
    const quiet = comp && !slot && comp.type === "wire";
    if (!quiet) text(label, lp[0], lp[1], titleText, slot ? "lbl accent" : "lbl", { "text-anchor": anchor });
    const reading = text(label, lp[0], lp[1] + (normal[1] < 0 ? -13 : 14), "", "reading", { "text-anchor": anchor });
    if (quiet) reading.classList.add("quiet");
    this.partLabels[id] = reading;
    if (comp && comp.type !== "open") {
      const sign = SOURCE_TYPES.has(comp.type) ? -1 : 1;
      this.flows.push({ id, points: pts, sign, part: null });
    }
  }

  drawEmptySlot(g, slot, half) {
    g.classList.add("slot");
    el("rect", { x: -half, y: -13, width: 2 * half, height: 26, rx: 5, class: "slot-box" }, g);
    text(g, 0, 5, "?", "slot-q", { "text-anchor": "middle" });
    this.makeSlotTarget(g, slot, half + 6, false);
  }

  makeSlotTarget(g, slot, half, filled) {
    const hit = el("rect", { x: -half, y: -22, width: 2 * half, height: 44, class: "slot-hit" }, g);
    g.dataset.slot = slot.id;
    hit.dataset.slot = slot.id;
    g.setAttribute("tabindex", "0");
    g.setAttribute("role", "button");
    g.setAttribute("aria-label", filled ? `slot ${slot.id}, filled; activate to empty` : `slot ${slot.id}, empty; accepts ${(slot.accepts || []).join(", ")}`);
    const fire = () => this.onSlot && this.onSlot(slot.id);
    g.addEventListener("click", fire);
    g.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); fire(); } });
  }

  drawThree(comp, slot) {
    const src = comp || slot;
    const isBJT = (comp ? comp.type : (slot.accepts || [])[0] || "npn").match(/np|pn/) && !(comp && /mos/.test(comp.type));
    const top = isBJT ? "c" : "d", mid = isBJT ? "b" : "g", bot = isBJT ? "e" : "s";
    const T = this.px(src[top] ?? src.a), M = this.px(src[mid] ?? src.b), B = this.px(src[bot] ?? src.c);
    [src[top], src[mid], src[bot]].forEach((n) => n && this.touch(n));
    const flip = T[1] > B[1];
    const cx = (Math.abs(T[0] - B[0]) < 1 ? T[0] : (T[0] + B[0]) / 2) - 10, cy = (T[1] + B[1]) / 2;
    const mirror = M[0] > cx + 10;
    const g = el("g", { transform: `translate(${cx + (mirror ? 20 : 0)},${cy}) scale(${mirror ? -1 : 1},${flip ? -1 : 1})`, class: "part" }, this.layers.parts);
    const pin = (x, y) => [cx + (mirror ? 20 - x : x), cy + (flip ? -y : y)];
    const pT = pin(10, -26), pM = pin(-24, 0), pB = pin(10, 26);
    this.wire(this.route(T, pT, false), "wire", src[top] ?? src.a);
    this.wire(this.route(M, pM, true), "wire", src[mid] ?? src.b);
    this.wire(this.route(pB, B, false), "wire", src[bot] ?? src.c);
    const id = slot ? slot.id : comp.id;
    if (!comp) {
      this.drawEmptySlot(g, slot, 24);
    } else {
      if (slot) { g.classList.add("filled"); this.makeSlotTarget(g, slot, 28, true); }
      if (/mos/.test(comp.type)) drawMOS(g, comp.type === "pmos"); else drawBJT(g, comp.type === "pnp");
    }
    const label = el("g", {}, this.layers.labels);
    const lx = cx + (mirror ? -30 : 40);
    const anchor = mirror ? "end" : "start";
    text(label, lx, cy - 4, comp ? `${id}  ${partName(comp)}` : `${id} ?`, slot ? "lbl accent" : "lbl", { "text-anchor": anchor });
    this.partLabels[id] = text(label, lx, cy + 11, "", "reading", { "text-anchor": anchor });
    if (comp) {
      const p = comp.type === "pnp" || comp.type === "pmos" ? -1 : 1;
      const bipolar = comp.type === "npn" || comp.type === "pnp";
      this.flows.push({ id, part: null, points: [...this.route(T, pT, false), [pin(10, 0)[0], cy], ...this.route(pB, B, false)], sign: p });
      if (bipolar) this.flows.push({ id: `${id}.b`, part: "b", points: [...this.route(M, pM, true), [cx + (mirror ? 20 : 0), cy]], sign: p });
    }
  }

  drawOpAmpItem(comp, slot) {
    const src = comp || slot;
    const Pp = this.px(src.plus), Pm = this.px(src.minus), O = this.px(src.out);
    [src.plus, src.minus, src.out].forEach((n) => n && this.touch(n));
    const inX = Math.max(Pp[0], Pm[0]);
    const cx = Math.max(inX + 80, O[0] - 72), cy = O[1];
    const topSign = Pp[1] < Pm[1] ? "plus" : Pp[1] > Pm[1] ? "minus" : "minus";
    const g = el("g", { transform: `translate(${cx},${cy})`, class: "part" }, this.layers.parts);
    const topPin = [cx - 44, cy - 16], botPin = [cx - 44, cy + 16], outPin = [cx + 48, cy];
    const [tNode, bNode] = topSign === "plus" ? [Pp, Pm] : [Pm, Pp];
    const elbow = (N, pinP) => { const mx = Math.min(pinP[0] - 14, Math.max(N[0], pinP[0] - 30)); return [N, [mx, N[1]], [mx, pinP[1]], pinP]; };
    this.wire(elbow(tNode, topPin), "wire", topSign === "plus" ? src.plus : src.minus);
    this.wire(elbow(bNode, botPin), "wire", topSign === "plus" ? src.minus : src.plus);
    this.wire([outPin, O], "wire", src.out);
    const id = slot ? slot.id : comp.id;
    if (!comp) this.drawEmptySlot(g, slot, 30);
    else { if (slot) { g.classList.add("filled"); this.makeSlotTarget(g, slot, 40, true); } drawOpAmp(g, topSign); }
    const label = el("g", {}, this.layers.labels);
    text(label, cx, cy + 50, comp ? `${id}  op-amp ${partValue(comp)}` : `${id} ?`, slot ? "lbl accent" : "lbl", { "text-anchor": "middle" });
    this.partLabels[id] = text(label, cx, cy + 64, "", "reading", { "text-anchor": "middle" });
    if (comp) this.flows.push({ id, part: null, points: [outPin, O], sign: 1 });
  }

  drawLogicItem(comp, slot) {
    const src = comp || slot;
    const isFlop = comp ? comp.type === "dff" : !!(slot && slot.d);
    const inputs = isFlop ? [src.d] : src.inputs || [];
    const out = isFlop ? src.q : src.output;
    const O = this.px(out);
    const ins = inputs.map((n) => this.px(n));
    inputs.forEach((n) => this.touch(n)); this.touch(out);
    const maxIn = Math.max(...ins.map((p) => p[0]), O[0] - 140);
    const cx = Math.max(maxIn + 60, O[0] - Math.min(72, (O[0] - maxIn) / 2 + 18)), cy = O[1];
    const g = el("g", { transform: `translate(${cx},${cy})`, class: "part" }, this.layers.parts);
    const pins = isFlop ? [-12] : gatePins(comp && comp.op === "not" ? 1 : inputs.length);
    const outY = isFlop ? -12 : 0;
    const used = comp && comp.op === "not" ? inputs.slice(0, 1) : inputs;
    used.forEach((n, i) => {
      const N = this.px(n), pin = [cx - 36, cy + pins[i]];
      const mx = Math.min(pin[0] - 12, Math.max(N[0] + 12, (N[0] + pin[0]) / 2));
      this.wire(Math.abs(N[1] - pin[1]) < 1 ? [N, pin] : [N, [mx, N[1]], [mx, pin[1]], pin], `wire net net-${css(n)}`);
    });
    const pinOut = [cx + 36, cy + outY];
    let outPath;
    if (O[0] < pinOut[0] - 1) {
      const below = MARGIN + (this.maxY - this.minY) * GRID + 26 + 14 * (this.loops = (this.loops || 0) + 1);
      outPath = [pinOut, [pinOut[0] + 14, pinOut[1]], [pinOut[0] + 14, below], [O[0] - 16, below], [O[0] - 16, O[1]], O];
    } else outPath = Math.abs(pinOut[1] - O[1]) < 1 ? [pinOut, O] : [pinOut, [O[0], pinOut[1]], O];
    this.wire(outPath, `wire net net-${css(out)}`);
    const id = slot ? slot.id : comp.id;
    if (!comp) this.drawEmptySlot(g, slot, 26);
    else {
      if (slot) { g.classList.add("filled"); this.makeSlotTarget(g, slot, 34, true); }
      if (comp.type === "dff") drawFlop(g); else drawGate(g, comp.op, pins.length);
    }
    const label = el("g", {}, this.layers.labels);
    text(label, cx, cy - (isFlop ? 36 : 26), comp ? `${id}${comp.op ? "  " + comp.op.toUpperCase() : ""}` : `${id} ?`, slot ? "lbl accent" : "lbl", { "text-anchor": "middle" });
  }

  drawNodes() {
    const kind = this.task.kind;
    const inputs = new Set(this.task.board.inputs || []), outputs = new Set(this.task.board.outputs || []);
    for (const name of Object.keys(this.nodes)) {
      const [x, y] = this.px(name);
      if (kind === "logic" && inputs.has(name)) {
        const g = el("g", { class: "logic-in", tabindex: "0", role: "button", "aria-label": `input ${name}` }, this.layers.nodes);
        el("rect", { x: x - 34, y: y - 12, width: 34, height: 24, rx: 4, class: "in-box" }, g);
        text(g, x - 28, y + 4, name, "lbl");
        const v = text(g, x - 8, y + 4, "0", "bit", { "text-anchor": "middle" });
        this.nodeLabels[name] = v;
        g.addEventListener("click", () => this.onToggle && this.onToggle(name));
        g.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); this.onToggle && this.onToggle(name); } });
        continue;
      }
      if (kind === "logic" && outputs.has(name)) {
        el("circle", { cx: x + 12, cy: y, r: 10, class: `lamp lamp-${css(name)}` }, this.layers.nodes);
        el("line", { x1: x, y1: y, x2: x + 2, y2: y, class: "wire" }, this.layers.wires);
        text(this.layers.labels, x + 28, y + 4, name, "lbl");
        this.nodeLabels[name] = text(this.layers.labels, x + 12, y + 4, "", "bit", { "text-anchor": "middle" });
        continue;
      }
      if (name === this.ground && kind !== "logic" && kind !== "chip") {
        const g = el("g", { class: "ground" }, this.layers.nodes);
        el("line", { x1: x, y1: y, x2: x, y2: y + 10, class: "wire" }, g);
        el("line", { x1: x - 12, y1: y + 10, x2: x + 12, y2: y + 10, class: "sym" }, g);
        el("line", { x1: x - 7, y1: y + 15, x2: x + 7, y2: y + 15, class: "sym" }, g);
        el("line", { x1: x - 2.5, y1: y + 20, x2: x + 2.5, y2: y + 20, class: "sym" }, g);
      }
      const junction = (this.uses[name] || 0) >= 3 || kind === "chip";
      el("circle", { cx: x, cy: y, r: junction ? 3.6 : 2.4, class: junction ? "node junction" : "node" }, this.layers.nodes);
      if (name !== this.ground || kind === "chip") {
        const t = text(this.layers.labels, x - 6, y - 8, name, "node-name", { "text-anchor": "end" });
        this.nodeLabels[name] = t;
      }
    }
  }

  showVoltages(volts) {
    for (const [name, t] of Object.entries(this.nodeLabels)) {
      if (this.task.kind === "logic" || this.task.kind === "chip") continue;
      t.textContent = volts && name in volts ? `${name} ${eng(volts[name], "V")}` : name;
      t.classList.toggle("live", !!volts);
    }
  }

  showReadings(readings) {
    for (const [id, t] of Object.entries(this.partLabels)) t.textContent = readings && readings[id] && !t.classList.contains("quiet") ? readings[id] : "";
    if (!this.fitted) { this.fitted = true; this.fit(); }
  }

  showLogic(values) {
    this.logicValues = values;
    for (const [name, t] of Object.entries(this.nodeLabels)) t.textContent = values ? String(values[name] ?? 0) : t.textContent;
    this.svg.querySelectorAll(".net").forEach((n) => n.classList.remove("high"));
    if (!values) return;
    for (const [name, v] of Object.entries(values)) {
      if (v) this.svg.querySelectorAll(`.net-${css(name)}`).forEach((n) => n.classList.add("high"));
      const lamp = this.svg.querySelector(`.lamp-${css(name)}`);
      if (lamp) lamp.classList.toggle("on", !!v);
    }
  }

  setLit(id, on) {
    const g = this.partGroups[id];
    if (g && g.querySelector(".led-body")) g.classList.toggle("lit", !!on);
  }

  startFlow(currentOf, scale) {
    this.stopFlow();
    this.layers.dots.innerHTML = "";
    this.dots = this.flows.map((f) => {
      const segs = [];
      let total = 0;
      for (let i = 1; i < f.points.length; i++) { const l = Math.hypot(f.points[i][0] - f.points[i - 1][0], f.points[i][1] - f.points[i - 1][1]); segs.push(l); total += l; }
      const count = Math.max(1, Math.floor(total / 22));
      const circles = Array.from({ length: count }, () => el("circle", { r: 2.4, class: "dot" }, this.layers.dots));
      return { flow: f, segs, total, circles, phase: Math.random() * 18 };
    });
    this.currentOf = currentOf;
    this.scale = scale;
    this.running = true;
    let last = performance.now();
    const tick = (now) => {
      if (!this.running) return;
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      for (const d of this.dots) {
        const amps = this.currentOf(d.flow) * d.flow.sign;
        const speed = this.scale > 0 ? (110 * amps) / this.scale : 0;
        d.phase = (((d.phase + speed * dt) % 22) + 22) % 22;
        const visible = Math.abs(amps) > this.scale * 1e-3 && Math.abs(amps) > 1e-12;
        d.circles.forEach((c, k) => {
          if (!visible) { c.setAttribute("visibility", "hidden"); return; }
          c.setAttribute("visibility", "visible");
          const [x, y] = pointAt(d.flow.points, d.segs, (k * 22 + d.phase) % d.total);
          c.setAttribute("cx", x); c.setAttribute("cy", y);
        });
      }
      this.raf = requestAnimationFrame(tick);
    };
    this.raf = requestAnimationFrame(tick);
  }

  stopFlow() {
    this.running = false;
    if (this.raf) cancelAnimationFrame(this.raf);
    if (this.layers) this.layers.dots.innerHTML = "";
  }
}

function autoLayout(task) {
  const given = task.board.nodes || {};
  const items = [...(task.board.fixed || []), ...(task.board.slots || [])];
  if (task.kind === "logic") {
    const level = new Map();
    for (const n of task.board.inputs || []) level.set(n, 0);
    const outOf = (it) => it.output ?? it.q;
    const insOf = (it) => it.inputs ?? (it.d ? [it.d] : []);
    for (const it of items) if (it.q) level.set(it.q, 0);
    for (let pass = 0; pass < items.length + 2; pass++) {
      for (const it of items) {
        if (it.q || !outOf(it)) continue;
        const l = 1 + Math.max(0, ...insOf(it).map((n) => level.get(n) ?? 0));
        if ((level.get(outOf(it)) ?? -1) < l) level.set(outOf(it), Math.min(l, 60));
      }
    }
    for (const it of items) for (const n of insOf(it)) if (!level.has(n)) level.set(n, 0);
    const columns = new Map();
    for (const [n, l] of level) { if (!columns.has(l)) columns.set(l, []); columns.get(l).push(n); }
    const pos = {};
    const feeds = new Map(items.map((it) => [outOf(it), insOf(it)]));
    for (const l of [...columns.keys()].sort((a, b) => a - b)) {
      const nets = columns.get(l);
      if (l > 0) {
        const bary = (n) => { const ys = (feeds.get(n) || []).map((m) => (pos[m] ? pos[m][1] : 0)); return ys.length ? ys.reduce((a, b) => a + b, 0) / ys.length : 0; };
        nets.sort((a, b) => bary(a) - bary(b));
      }
      nets.forEach((n, i) => { pos[n] = [1 + l * 2.4, 0.6 + i * 1.3]; });
    }
    for (const n of Object.keys(given)) delete pos[n];
    return pos;
  }
  const names = [];
  for (const it of items) for (const [k, v] of Object.entries(it)) if (typeof v === "string" && !["id", "type", "color", "label", "model"].includes(k) && !names.includes(v)) names.push(v);
  const missing = names.filter((n) => !(n in given));
  const cols = Math.max(2, Math.ceil(Math.sqrt(missing.length)));
  return Object.fromEntries(missing.map((n, i) => [n, [1 + (i % cols) * 3, 1 + Math.floor(i / cols) * 2.5]]));
}

function pointAt(points, segs, s) {
  for (let i = 0; i < segs.length; i++) {
    if (s <= segs[i] || i === segs.length - 1) {
      const f = segs[i] ? Math.min(1, s / segs[i]) : 0;
      return [points[i][0] + (points[i + 1][0] - points[i][0]) * f, points[i][1] + (points[i + 1][1] - points[i][1]) * f];
    }
    s -= segs[i];
  }
  return points[0];
}

export function css(name) { return String(name).replace(/[^a-zA-Z0-9_-]/g, "_"); }
