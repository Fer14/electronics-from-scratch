// The 3D view of a task: the same circuit built on an isometric board.
//
// The layout is not invented here: the schematic Board has already routed every wire and placed every
// part on the task's node grid (it records that in board.geo), and this view lifts those positions onto
// the board, one grid step = one world unit. So any task that draws as a schematic also draws in 3D.
//
// The view mirrors the schematic's API (render, showVoltages, showReadings, startFlow, stopFlow) so the
// task page can drive both, plus setLevel (LED and bulb brightness) and setTime (switches that toggle).

import { el, text } from "../ui/svg.js";
import { GRID, MARGIN, partName, partValue } from "../ui/board.js";
import { eng } from "../sim/lab.js";
import { Pen, defs, holePattern } from "./pen.js";
import { drawPart, drawThree, drawOpAmp, halfLength, isLamp } from "./parts.js";

const TRACK_Z = 0.035;
const PK = 1.5; // parts are drawn this much larger than their schematic footprint
const CHAR = 6.7; // width of one 11 px JetBrains Mono glyph
const MATS = ["neutral", "dark", "accent", "metal", "resist", "copper", "board"];
const QUIET = new Set(["wire"]);

const reduceMotion = () => { try { return matchMedia("(prefers-reduced-motion: reduce)").matches; } catch { return false; } };

export class IsoView {
  constructor(host, task, board) {
    this.host = host;
    this.task = task;
    this.board = board;
    this.onSlot = null;
    this.state = { volts: null, readings: null, levels: {}, time: null };
    this.running = false;
    this.lastWidth = 0;
    this.host.classList.add("iso-host");
    this.host.addEventListener("pointerenter", () => this.hold());
    this.host.addEventListener("pointerdown", () => this.hold());
    this.host.addEventListener("focusin", () => this.hold());
    this.host.addEventListener("pointerleave", () => this.release());
    try {
      this.seen = new IntersectionObserver((entries) => { for (const e of entries) this.host.classList.toggle("offscreen", !e.isIntersecting); });
      this.seen.observe(this.host);
    } catch {}
    let pending = null;
    window.addEventListener("resize", () => {
      clearTimeout(pending);
      pending = setTimeout(() => { if (!this.host.hidden && Math.abs(this.width() - this.lastWidth) > 30) this.relayout(); }, 160);
    });
  }

  // Idle motion stops while someone is using the board and comes back a while after they leave.
  hold() { clearTimeout(this.resume); this.host.classList.add("still"); }
  release() { clearTimeout(this.resume); this.resume = setTimeout(() => this.host.classList.remove("still"), 6000); }

  width() {
    const w = this.host.clientWidth || (this.host.parentElement && this.host.parentElement.clientWidth - 20) || 700;
    return Math.max(260, w);
  }

  toWorld([px, py]) {
    const b = this.board;
    return [(px - MARGIN) / GRID + b.minX, (py - MARGIN) / GRID + b.minY];
  }

  // Turn the schematic geometry into world-space items: tracks, sockets and parts.
  layout(choice) {
    const task = this.task, items = [], tracks = [];
    const pts = [];
    for (const g of this.board.geo || []) {
      const comp = g.comp, slot = g.slot;
      const lamp = comp ? isLamp(task, comp) : false;
      if (g.shape === "two") {
        const P = g.pts.map((p) => this.toWorld(p));
        P.forEach((p) => pts.push(p));
        const c = this.toWorld(g.center);
        const d = g.dir;
        const L0 = P[g.leg], L1 = P[g.leg + 1];
        const legLen = Math.hypot(L1[0] - L0[0], L1[1] - L0[1]);
        const type = comp ? comp.type : (slot.accepts || ["resistor"])[0];
        const hl = Math.max(0.2, Math.min(halfLength(type, lamp) * PK, legLen / 2 - 0.06));
        const axis = Math.abs(d[0]) >= Math.abs(d[1]) ? "x" : "y";
        const s = Math.sign(axis === "x" ? d[0] : d[1]) || 1;
        const a = [c[0] - d[0] * hl, c[1] - d[1] * hl], b = [c[0] + d[0] * hl, c[1] + d[1] * hl];
        if (comp && !slot && QUIET.has(comp.type)) { tracks.push(P); continue; }
        tracks.push([...P.slice(0, g.leg + 1), a]);
        tracks.push([b, ...P.slice(g.leg + 1)]);
        items.push({ shape: "two", id: g.id, comp, slot, cx: c[0], cy: c[1], axis, s, hl, lamp, ends: [a, b], flowPts: P });
      } else {
        const wires = g.wires.map((w) => w.map((p) => this.toWorld(p)));
        wires.forEach((w) => { tracks.push(w); w.forEach((p) => pts.push(p)); });
        const c = this.toWorld(g.center);
        pts.push(c);
        items.push({ shape: g.shape, id: g.id, comp, slot, cx: c[0], cy: c[1], pins: g.pins.map((p) => this.toWorld(p)), axis: "x", s: 1, hl: 0.3 });
      }
    }
    for (const name of Object.keys(this.board.uses || {})) {
      const n = this.board.nodes[name];
      if (n) pts.push([n[0], n[1]]);
    }
    if (!pts.length) pts.push([0, 0], [4, 3]);
    const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
    const bounds = [Math.min(...xs) - 0.75, Math.max(...xs) + 0.75, Math.min(...ys) - 0.75, Math.max(...ys) + 0.75];
    return { items, tracks, bounds };
  }

  relayout() {
    if (!this.lastChoice) return;
    const st = this.state, flow = this.running && this.currentOf ? [this.currentOf, this.scale] : null;
    this.render(this.lastChoice, this.focus);
    this.reapply(st, flow);
  }

  reapply(st, flow) {
    if (st.volts) this.showVoltages(st.volts);
    if (st.readings) this.showReadings(st.readings);
    for (const [id, [i, p]] of Object.entries(st.levels)) this.setLevel(id, i, p);
    if (st.time !== null) this.setTime(st.time);
    if (flow) this.startFlow(...flow);
  }

  render(choice = {}, focus = null) {
    this.stopFlow(true);
    this.lastChoice = choice;
    this.focus = focus;
    this.state = { volts: null, readings: null, levels: {}, time: null };
    this.host.innerHTML = "";
    const { items, tracks, bounds } = this.layout(choice);
    this.items = items;
    const [bx0, bx1, by0, by1] = bounds;
    const avail = this.width();
    this.lastWidth = avail;
    const margin = avail < 560 ? 30 : 150;
    const span = (bx1 - bx0 + by1 - by0) * Math.cos(Math.PI / 6);
    const U = Math.max(22, Math.min(64, (avail - 2 * margin) / span));
    const pen = new Pen(U);
    this.pen = pen;

    const svg = el("svg", { class: "iso-svg", role: "img", "aria-label": "3D view of the circuit on a board" }, this.host);
    this.svg = svg;
    const d = defs(svg, MATS);
    holePattern(d, U);
    const L = {
      shadow: el("g", { class: "iso-shadows" }, svg),
      board: el("g", { class: "iso-board" }, svg),
      tracks: el("g", { class: "iso-tracks" }, svg),
      glow: el("g", { class: "iso-glows" }, svg),
      dots: el("g", { class: "iso-dots" }, svg),
      parts: el("g", { class: "iso-parts" }, svg),
      labels: el("g", { class: "iso-labels" }, svg),
    };
    this.layers = L;
    const all = pen.track();

    // the board: a soft halo, the slab, the hole grid and an inset groove
    const zb = -0.3;
    const foot = [[bx0, by0, zb], [bx1, by0, zb], [bx1, by1, zb], [bx0, by1, zb]].map((q) => pen.p(...q));
    el("polygon", { points: foot.map((p) => `${p[0]},${p[1] + U * 0.22}`).join(" "), class: "iso-halo", filter: "url(#iso-blur)" }, L.shadow);
    pen.cuboid(L.board, [bx0, bx1], [by0, by1], [zb, 0], "m-board");
    pen.poly(L.board, [[bx0, by0, 0], [bx1, by0, 0], [bx1, by1, 0], [bx0, by1, 0]], "iso-holes", { fill: "url(#iso-holes)" });
    const i = 0.22;
    pen.poly(L.board, [[bx0 + i, by0 + i, 0], [bx1 - i, by0 + i, 0], [bx1 - i, by1 - i, 0], [bx0 + i, by1 - i, 0]], "groove faint");

    // tracks: raised strips, outline first, then the side, then the top, so crossings stay clean
    const tw = Math.max(3.2, U * 0.1), drop = Math.max(1.4, U * TRACK_Z);
    const poly = (w) => w.map((p) => pen.p(p[0], p[1], TRACK_Z)).map((s) => `${s[0].toFixed(1)},${s[1].toFixed(1)}`).join(" ");
    const shifted = (w) => w.map((p) => pen.p(p[0], p[1], TRACK_Z)).map((s) => `${s[0].toFixed(1)},${(s[1] + drop).toFixed(1)}`).join(" ");
    const usable = tracks.filter((w) => w.length >= 2);
    this.trackList = usable;
    for (const w of usable) { el("polyline", { points: shifted(w), class: "track-line", "stroke-width": tw + 2 }, L.tracks); el("polyline", { points: poly(w), class: "track-line", "stroke-width": tw + 2 }, L.tracks); }
    for (const w of usable) el("polyline", { points: shifted(w), class: "track-side", "stroke-width": tw }, L.tracks);
    for (const w of usable) el("polyline", { points: poly(w), class: "track-top", "stroke-width": tw }, L.tracks);
    for (const [name, n] of Object.entries(this.board.nodes)) {
      const used = this.board.uses[name] || 0;
      if (!used) continue;
      pen.ellipse(L.tracks, n[0], n[1], TRACK_Z + 0.002, used >= 3 ? 0.075 : 0.055, "pad");
    }

    // parts and sockets, back to front
    const fills = (this.task.board.slots || []).filter((s) => choice[s.id]).map((s) => s.id);
    const accentId = focus && choice[focus] ? focus : fills.length ? fills[fills.length - 1] : null;
    this.accentId = accentId;
    const ground = this.task.board.ground || "gnd";
    const drawables = items.map((it) => ({ key: it.cx + it.cy, it }));
    const gn = this.board.nodes[ground];
    if (gn && this.board.uses[ground]) drawables.push({ key: gn[0] + gn[1] + 0.01, ground: gn });
    drawables.sort((a, b) => a.key - b.key);
    this.handles = {};
    this.boxes = [];
    for (const dr of drawables) {
      if (dr.ground) { this.drawGround(pen, L.parts, dr.ground); continue; }
      const it = dr.it;
      it.mat = it.slot && it.id === accentId ? "m-accent" : it.comp && it.comp.type === "resistor" && !it.lamp && !/motor/i.test(it.comp.label || "") ? "m-resist" : "m-neutral";
      const g = el("g", { class: `iso-part${it.slot ? " in-slot" : ""}${it.id === accentId ? " iso-accent" : ""}` }, L.parts);
      const bb = pen.track();
      if (!it.comp) this.drawSocket(pen, g, it);
      else {
        pen.frame(it.cx, it.cy, PK);
        const local = { ...it, hl: it.hl / PK, pins: (it.pins || []).map((q) => [it.cx + (q[0] - it.cx) / PK, it.cy + (q[1] - it.cy) / PK]) };
        if (it.shape === "two") this.handles[it.id] = drawPart(pen, g, local, { glow: L.glow }) || {};
        else if (it.shape === "three") drawThree(pen, g, local);
        else drawOpAmp(pen, g, local);
        pen.unframe();
      }
      pen.box = all;
      if (it.id === accentId) { pen.box = null; this.floatShadow(pen, L.glow, it); pen.box = all; }
      for (const k of [0, 1]) pen.grow(bb[k * 2], bb[k * 2 + 1]);
      if (Number.isFinite(bb[0])) { it.bbox = bb; this.boxes.push(bb); }
      if (it.slot) this.makeTarget(g, it);
    }
    pen.box = all;
    this.placeLabels(pen, L.labels, items, all);

    const pad = 14;
    const vb = [all[0] - pad, all[1] - pad, all[2] - all[0] + 2 * pad, all[3] - all[1] + 2 * pad];
    svg.setAttribute("viewBox", vb.map((v) => v.toFixed(1)).join(" "));
    svg.style.maxWidth = `${Math.ceil(vb[2] * 1.15)}px`;
    this.corners();
    return svg;
  }

  corners() {
    const tl = document.createElement("div");
    tl.className = "iso-corner tl";
    tl.textContent = `FIG_${this.task.id.split("-").slice(0, 2).join("")} · ISO 30°`;
    const br = document.createElement("div");
    br.className = "iso-corner br";
    br.innerHTML = `<span class="iso-key"></span><span class="iso-state"></span>`;
    this.stateText = br.querySelector(".iso-state");
    this.stateText.textContent = (this.task.board.slots || []).length ? "pick a part, then a socket" : "press RUN";
    this.host.append(tl, br);
  }

  setState(msg) { if (this.stateText) this.stateText.textContent = msg; }

  drawGround(pen, layer, [x, y]) {
    const g = el("g", { class: "iso-ground" }, layer);
    let z = TRACK_Z;
    for (const r of [0.24, 0.17, 0.1]) { pen.cuboid(g, [x - r, x + r], [y - r, y + r], [z, z + 0.055], "m-metal"); z += 0.055; }
  }

  drawSocket(pen, g, it) {
    g.classList.add("iso-socket");
    const W = (u, v) => (it.axis === "x" ? [it.cx + it.s * u, it.cy + v] : [it.cx + v, it.cy + it.s * u]);
    const hw = it.shape === "two" ? 0.2 : 0.42, hl = it.shape === "two" ? it.hl : 0.55;
    const corner = [W(-hl, -hw), W(hl, -hw), W(hl, hw), W(-hl, hw)].map((p) => [p[0], p[1], 0.004]);
    pen.poly(g, corner, "socket-well");
    pen.poly(g, corner, "socket-edge");
    if (it.shape === "two") for (const e of it.ends) pen.ellipse(g, e[0], e[1], 0.006, 0.06, "socket-hole");
    const [qx, qy] = pen.p(it.cx, it.cy, 0.01);
    text(g, qx, qy + 5, "?", "socket-q", { "text-anchor": "middle" });
  }

  floatShadow(pen, layer, it) {
    const [x, y] = [it.cx, it.cy];
    const s = pen.ellipse(layer, x, y, 0.01, it.shape === "two" ? Math.max(0.25, it.hl * 0.7) : 0.55, "float-shadow");
    return s;
  }

  makeTarget(g, it) {
    const slot = it.slot;
    g.dataset.slot = slot.id;
    g.setAttribute("tabindex", "0");
    g.setAttribute("role", "button");
    g.setAttribute("aria-label", it.comp ? `slot ${slot.id}, holds ${partName(it.comp)} ${partValue(it.comp)}; activate to empty` : `slot ${slot.id}, empty; accepts ${(slot.accepts || []).join(", ")}`);
    const bb = it.bbox;
    if (bb) el("rect", { x: bb[0] - 6, y: bb[1] - 6, width: bb[2] - bb[0] + 12, height: bb[3] - bb[1] + 12, class: "iso-hit" }, g).dataset.slot = slot.id;
    const fire = () => this.onSlot && this.onSlot(slot.id);
    g.addEventListener("click", fire);
    g.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); fire(); } });
  }

  // Labels sit beside the parts, never on them: try right, left, above and below each part's
  // screen box and take the first spot that hits no other part or label.
  placeLabels(pen, layer, items, all) {
    this.labels = {};
    const taken = this.boxes.slice();
    const hits = (b) => taken.some((o) => b[0] < o[2] && b[2] > o[0] && b[1] < o[3] && b[3] > o[1]);
    // tracks are soft obstacles: a label may cross one, but a clear spot wins
    const samples = [];
    for (const w of this.trackList || []) {
      for (let k = 1; k < w.length; k++) {
        const a = pen.p(w[k - 1][0], w[k - 1][1], TRACK_Z), b = pen.p(w[k][0], w[k][1], TRACK_Z);
        const n = Math.max(1, Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) / 6));
        for (let j = 0; j <= n; j++) samples.push([a[0] + ((b[0] - a[0]) * j) / n, a[1] + ((b[1] - a[1]) * j) / n]);
      }
    }
    const score = (b) => (hits(b) ? 1000 : 0) + samples.filter(([x, y]) => x > b[0] && x < b[2] && y > b[1] && y < b[3]).length;
    const best = (spots, box) => { let pick = null, low = Infinity; for (const s of spots) { const v = score(box(s)); if (v < low) { low = v; pick = s; } if (v === 0) break; } return [pick, low]; };
    const ordered = items.filter((it) => it.bbox).sort((a, b) => (a.slot ? 0 : 1) - (b.slot ? 0 : 1));
    for (const it of ordered) {
      const title = it.comp ? `${it.id}  ${it.lamp ? "bulb " : ""}${partValue(it.comp) || partName(it.comp)}` : `${it.id}  empty`;
      const w = Math.max(title.length, 17) * CHAR, h = 28;
      const [x0, y0, x1, y1] = it.bbox;
      const cy = (y0 + y1) / 2, cx = (x0 + x1) / 2;
      const spots = [
        { x: x1 + 10, y: cy - h / 2, anchor: "start" },
        { x: x0 - 10 - w, y: cy - h / 2, anchor: "end" },
        { x: cx - w / 2, y: y0 - 8 - h, anchor: "middle" },
        { x: cx - w / 2, y: y1 + 8, anchor: "middle" },
        { x: x1 + 10, y: y0 - h, anchor: "start" },
        { x: x0 - 10 - w, y: y1, anchor: "end" },
        { x: x1 + 10, y: y1, anchor: "start" },
        { x: x0 - 10 - w, y: y0 - h, anchor: "end" },
        { x: x1 + 34, y: cy - h / 2, anchor: "start" },
        { x: x0 - 34 - w, y: cy - h / 2, anchor: "end" },
        { x: cx - w / 2, y: y0 - 30 - h, anchor: "middle" },
        { x: cx - w / 2, y: y1 + 30, anchor: "middle" },
      ];
      const [spot] = best(spots, (s) => [s.x, s.y, s.x + w, s.y + h]);
      taken.push([spot.x, spot.y, spot.x + w, spot.y + h]);
      pen.grow(spot.x, spot.y); pen.grow(spot.x + w, spot.y + h);
      const tx = spot.anchor === "start" ? spot.x : spot.anchor === "end" ? spot.x + w : spot.x + w / 2;
      const g = el("g", { class: `iso-label${it.slot ? " slot" : ""}${it.id === this.accentId ? " accent" : ""}` }, layer);
      text(g, tx, spot.y + 11, title, "iso-title", { "text-anchor": spot.anchor });
      const reading = text(g, tx, spot.y + 25, "", "iso-reading", { "text-anchor": spot.anchor });
      this.labels[it.id] = reading;
    }
    // node voltages, shown after RUN, wherever there is room left
    this.nodeTags = {};
    const ground = this.task.board.ground || "gnd";
    for (const [name, n] of Object.entries(this.board.nodes)) {
      if (name === ground || !this.board.uses[name]) continue;
      const [sx, sy] = pen.p(n[0], n[1], TRACK_Z);
      const w = (name.length + 9) * CHAR * 0.92, h = 13;
      const spots = [[sx + 8, sy - 16], [sx - 8 - w, sy - 16], [sx + 8, sy + 4], [sx - 8 - w, sy + 4]];
      const [spot, low] = best(spots, ([x, y]) => [x, y, x + w, y + h]);
      if (!spot || low >= 1000) continue;
      taken.push([spot[0], spot[1], spot[0] + w, spot[1] + h]);
      const right = spot[0] > sx;
      const t = text(layer, right ? spot[0] : spot[0] + w, spot[1] + 10, "", "iso-node", { "text-anchor": right ? "start" : "end" });
      this.nodeTags[name] = { t, box: [spot[0], spot[1], spot[0] + w, spot[1] + h] };
    }
    for (const { box } of Object.values(this.nodeTags)) { pen.grow(box[0], box[1]); pen.grow(box[2], box[3]); }
  }

  showVoltages(volts) {
    this.state.volts = volts;
    for (const [name, { t }] of Object.entries(this.nodeTags || {})) t.textContent = volts && name in volts && Number.isFinite(volts[name]) ? `${name} ${eng(Math.abs(volts[name]) < 1e-9 ? 0 : volts[name], "V")}` : "";
  }

  showReadings(readings) {
    this.state.readings = readings;
    for (const [id, t] of Object.entries(this.labels || {})) t.textContent = readings && readings[id] ? readings[id] : "";
  }

  setLit() {}

  // Brightness follows the current: an LED is full at about 15 mA, a bulb at about 1.5 W.
  setLevel(id, amps, watts) {
    this.state.levels[id] = [amps, watts];
    const h = this.handles && this.handles[id];
    if (!h || !h.kind) return;
    let b = 0;
    if (h.kind === "led") b = amps > 1e-4 ? Math.min(1, Math.sqrt(amps / 0.015)) : 0;
    else if (h.kind === "lamp") b = watts > 0.01 ? Math.min(1, Math.sqrt(Math.abs(watts) / 1.5)) : 0;
    else return;
    if (h.glow) { h.glow.style.opacity = String(b); h.glow.setAttribute("transform-origin", "center"); }
    if (h.lens) h.lens.classList.toggle("lit", b > 0.05);
    if (h.lens) h.lens.style.setProperty("--b", String(b));
    if (h.bulb) { h.bulb.classList.toggle("lit", b > 0.05); h.bulb.style.setProperty("--b", String(b)); }
    if (h.fil) h.fil.classList.toggle("lit", b > 0.05);
  }

  // In a transient, switches with toggle_at flip as the playback clock passes each time.
  setTime(t) {
    this.state.time = t;
    for (const it of this.items || []) {
      const c = it.comp;
      if (!c || c.type !== "switch" || !(c.toggle_at || []).length) continue;
      const flips = c.toggle_at.filter((x) => x <= t).length;
      const closed = (c.closed !== false) !== (flips % 2 === 1);
      const h = this.handles[it.id];
      if (h && h.setClosed && h.closed !== closed) { h.closed = closed; h.setClosed(closed); }
    }
  }

  startFlow(currentOf, scale) {
    this.stopFlow(true);
    this.currentOf = currentOf;
    this.scale = scale;
    this.running = true;
    this.setState("current flowing · dots move with I");
    const pen = this.pen, layer = this.layers.dots;
    layer.innerHTML = "";
    const r = Math.max(2, pen.U * 0.055);
    this.dots = this.board.flows.map((f) => {
      const pts = f.points.map((p) => this.toWorld(p)).map((w) => pen.p(w[0], w[1], TRACK_Z + 0.01));
      const segs = [];
      let total = 0;
      for (let k = 1; k < pts.length; k++) { const l = Math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1]); segs.push(l); total += l; }
      const gap = Math.max(14, pen.U * 0.42);
      const count = Math.max(1, Math.floor(total / gap));
      const circles = Array.from({ length: count }, () => el("circle", { r, class: "iso-dot" }, layer));
      return { flow: f, pts, segs, total, gap: total / count, circles, phase: Math.random() * gap };
    });
    let last = performance.now();
    const tick = (now) => {
      if (!this.running) return;
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      if (!this.host.hidden) {
        for (const d of this.dots) {
          const amps = (this.currentOf(d.flow) || 0) * d.flow.sign;
          const speed = this.scale > 0 ? (pen.U * 2.2 * amps) / this.scale : 0;
          d.phase = (((d.phase + speed * dt) % d.gap) + d.gap) % d.gap;
          const visible = Math.abs(amps) > this.scale * 1e-3 && Math.abs(amps) > 1e-12;
          d.circles.forEach((c, k) => {
            if (!visible) { c.setAttribute("visibility", "hidden"); return; }
            c.setAttribute("visibility", "visible");
            const [x, y] = pointAt(d.pts, d.segs, (k * d.gap + d.phase) % d.total);
            c.setAttribute("cx", x.toFixed(1)); c.setAttribute("cy", y.toFixed(1));
          });
        }
      }
      this.raf = requestAnimationFrame(tick);
    };
    this.raf = requestAnimationFrame(tick);
  }

  stopFlow(keepState = false) {
    this.running = false;
    if (this.raf) cancelAnimationFrame(this.raf);
    this.raf = null;
    if (this.layers) this.layers.dots.innerHTML = "";
    if (!keepState) this.currentOf = null;
  }
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

export { reduceMotion };
