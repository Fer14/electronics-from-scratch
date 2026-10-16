// The isometric parts. Each drawer gets a placed item:
//   { cx, cy }  centre on the board (world units), axis "x" or "y", s = +1/-1 (direction from terminal a to b),
//   hl = half length along the axis, comp = the component, mat = body material class.
// and paints its solid back to front into g. Glows go into ctx.glow (a layer under the parts).

import { el } from "../ui/svg.js";
import { shade } from "./pen.js";

const BAND = ["#1b1b1b", "#7a4a27", "#c8372d", "#e57b26", "#ecc433", "#3b8c4a", "#2f63b8", "#7a4fb0", "#8b8b8b", "#f4f4f2"];
const GOLD = "#c7a23f", SILVER = "#c2c2c2";

export function bandColors(ohms) {
  if (!(ohms > 0) || !Number.isFinite(ohms)) return [BAND[0], BAND[0], BAND[0], GOLD];
  let e = Math.floor(Math.log10(ohms)) - 1;
  let m = Math.round(ohms / 10 ** e);
  if (m >= 100) { m = Math.round(m / 10); e += 1; }
  const mult = e === -1 ? GOLD : e === -2 ? SILVER : e < -2 ? SILVER : BAND[Math.min(9, e)];
  return [BAND[Math.floor(m / 10)], BAND[m % 10], mult, GOLD];
}

// (u along the axis, v across it) -> world (x, y)
function W(it, u, v) { return it.axis === "x" ? [it.cx + it.s * u, it.cy + v] : [it.cx + v, it.cy + it.s * u]; }

function range(it, u0, u1, v0, v1) {
  const a = W(it, u0, v0), b = W(it, u1, v1);
  return [[Math.min(a[0], b[0]), Math.max(a[0], b[0])], [Math.min(a[1], b[1]), Math.max(a[1], b[1])]];
}

function box(pen, g, it, u0, u1, v0, v1, z0, z1, mat) {
  const [xr, yr] = range(it, u0, u1, v0, v1);
  pen.cuboid(g, xr, yr, [z0, z1], mat);
}

// Coloured stripes painted on the visible long faces of a box (resistor bands, a diode's cathode ring).
function band(pen, g, it, u0, u1, hw, z0, z1, color) {
  const [xr, yr] = range(it, u0, u1, -hw, hw);
  const e = 0.002;
  pen.poly(g, [[xr[0], yr[0], z1 + e], [xr[1], yr[0], z1 + e], [xr[1], yr[1], z1 + e], [xr[0], yr[1], z1 + e]], "band", { fill: color });
  if (it.axis === "x") pen.poly(g, [[xr[0], yr[1] + e, z0], [xr[1], yr[1] + e, z0], [xr[1], yr[1] + e, z1], [xr[0], yr[1] + e, z1]], "band", { fill: color.startsWith("#") ? shade(color, 0.84) : color });
  else pen.poly(g, [[xr[1] + e, yr[0], z0], [xr[1] + e, yr[1], z0], [xr[1] + e, yr[1], z1], [xr[1] + e, yr[0], z1]], "band", { fill: color.startsWith("#") ? shade(color, 0.7) : color });
}

// Thin metal leads from the body down to the ends where the tracks stop.
function leads(pen, g, it, uBody, zBody) {
  for (const sgn of [-1, 1]) {
    const a = W(it, sgn * uBody, 0), b = W(it, sgn * (uBody + 0.05), 0), c = W(it, sgn * it.hl, 0);
    pen.line(g, [[a[0], a[1], zBody], [b[0], b[1], 0.03], [c[0], c[1], 0.03]], "lead");
  }
}

function resistor(pen, g, it) {
  const hb = Math.min(0.31, it.hl - 0.05), hw = 0.085, z0 = 0.09, z1 = 0.26;
  leads(pen, g, it, hb, (z0 + z1) / 2);
  box(pen, g, it, -hb, hb, -hw, hw, z0, z1, it.mat);
  const colors = bandColors(it.comp.ohms);
  const at = [-0.66, -0.42, -0.18, 0.5];
  colors.forEach((c, k) => band(pen, g, it, at[k] * hb, at[k] * hb + 0.13 * hb, hw, z0, z1, c));
}

function lamp(pen, g, it, ctx) {
  const [x, y] = W(it, 0, 0);
  for (const sgn of [-1, 1]) { const c = W(it, sgn * it.hl, 0); pen.line(g, [[x, y, 0.03], [c[0], c[1], 0.03]], "lead"); }
  const glow = el("g", { class: "iso-glow lamp-glow" }, ctx.glow);
  const [gx, gy] = pen.p(x, y, 0.42);
  el("circle", { cx: gx, cy: gy, r: pen.u * 0.9, fill: "url(#iso-glow)" }, glow);
  pen.cylinder(g, x, y, 0.13, 0.02, 0.17, it.mat);
  pen.cylinder(g, x, y, 0.1, 0.17, 0.24, "m-metal");
  const bulb = pen.sphere(g, x, y, 0.42, 0.22, "iso-bulb");
  const [fx, fy] = pen.p(x, y, 0.4);
  const u = pen.u, zz = [];
  for (let k = 0; k <= 8; k++) zz.push(`${(fx - u * 0.07 + (u * 0.14 * k) / 8).toFixed(1)} ${(fy - u * 0.03 + (k % 2 ? -u * 0.025 : u * 0.025)).toFixed(1)}`);
  const fil = el("path", { d: `M ${fx - u * 0.06} ${fy + u * 0.17} L ${fx - u * 0.07} ${fy - u * 0.03} L ${zz.join(" L ")} L ${fx + u * 0.06} ${fy + u * 0.17}`, class: "iso-filament" }, g);
  return { glow, bulb, fil, kind: "lamp" };
}

function motor(pen, g, it) {
  const [x, y] = W(it, 0, 0);
  for (const sgn of [-1, 1]) { const c = W(it, sgn * it.hl, 0); pen.line(g, [[x, y, 0.03], [c[0], c[1], 0.03]], "lead"); }
  pen.cylinder(g, x, y, 0.24, 0.02, 0.42, it.mat);
  pen.cylinder(g, x, y, 0.09, 0.42, 0.47, "m-metal");
  pen.cylinder(g, x, y, 0.025, 0.47, 0.62, "m-metal");
  return {};
}

function capacitor(pen, g, it) {
  const [x, y] = W(it, 0, 0);
  for (const sgn of [-1, 1]) { const a = W(it, sgn * 0.07, 0), c = W(it, sgn * it.hl, 0); pen.line(g, [[a[0], a[1], 0.03], [c[0], c[1], 0.03]], "lead"); }
  const r = 0.15;
  pen.cylinder(g, x, y, r, 0.02, 0.5, it.mat);
  const [cx, cy] = pen.p(x, y, 0.5);
  const k = pen.u * 0.07;
  el("path", { d: `M ${cx - k} ${cy} L ${cx + k} ${cy} M ${cx} ${cy - k * 0.58} L ${cx} ${cy + k * 0.58}`, class: "groove" }, g);
  // the minus stripe on the side that faces the viewer
  const [sx, sy] = pen.p(x, y, 0.47);
  el("rect", { x: sx + r * pen.u * 0.25, y: sy, width: r * pen.u * 0.3, height: 0.4 * pen.u, class: "iso-stripe" }, g);
  return {};
}

function inductor(pen, g, it) {
  const [x, y] = W(it, 0, 0);
  for (const sgn of [-1, 1]) { const a = W(it, sgn * 0.1, 0), c = W(it, sgn * it.hl, 0); pen.line(g, [[a[0], a[1], 0.03], [c[0], c[1], 0.03]], "lead"); }
  pen.cylinder(g, x, y, 0.19, 0.02, 0.1, "m-dark");
  pen.cylinder(g, x, y, it.mat === "m-accent" ? 0.18 : 0.175, 0.1, 0.3, it.mat === "m-accent" ? "m-accent" : "m-copper");
  pen.cylinder(g, x, y, 0.19, 0.3, 0.38, "m-dark");
  return {};
}

function diode(pen, g, it) {
  const hb = Math.min(0.2, it.hl - 0.06), hw = 0.06, z0 = 0.07, z1 = 0.19;
  leads(pen, g, it, hb, (z0 + z1) / 2);
  box(pen, g, it, -hb, hb, -hw, hw, z0, z1, it.mat === "m-accent" ? "m-accent" : "m-dark");
  band(pen, g, it, hb * 0.5, hb * 0.78, hw, z0, z1, it.comp.type === "zener" ? "#9fb7d9" : "#d9d7d0");
  return {};
}

function led(pen, g, it, ctx) {
  const [x, y] = W(it, 0, 0);
  for (const sgn of [-1, 1]) { const a = W(it, sgn * 0.05, 0), c = W(it, sgn * it.hl, 0); pen.line(g, [[a[0], a[1], 0.03], [c[0], c[1], 0.03]], "lead"); }
  const glow = el("g", { class: `iso-glow led-glow led-${it.comp.color || "red"}` }, ctx.glow);
  const [gx, gy] = pen.p(x, y, 0.26);
  el("circle", { cx: gx, cy: gy, r: pen.u * 0.75, fill: "url(#iso-glow)" }, glow);
  const lens = el("g", { class: `iso-led led-${it.comp.color || "red"}` }, g);
  pen.cylinder(lens, x, y, 0.14, 0.02, 0.06, "m-lens");
  pen.cylinder(lens, x, y, 0.115, 0.06, 0.22, "m-lens");
  pen.dome(lens, x, y, 0.115, 0.22, 0.13, "face m-lens f0 dome");
  const [hx, hy] = pen.p(x - 0.03, y - 0.05, 0.28);
  el("ellipse", { cx: hx, cy: hy, rx: pen.u * 0.035, ry: pen.u * 0.05, class: "iso-shine" }, lens);
  return { glow, lens, kind: "led" };
}

function battery(pen, g, it) {
  const hb = Math.min(0.48, it.hl - 0.04), hw = 0.27, z1 = 0.4;
  box(pen, g, it, -hb, hb, -hw, hw, 0.01, z1, it.mat === "m-accent" ? "m-accent" : "m-dark");
  // the wrap label around the middle, and the two snaps on the + end
  const [xr, yr] = range(it, -hb * 0.45, hb * 0.55, -hw - 0.002, hw + 0.002);
  pen.poly(g, [[xr[0], yr[0], z1 + 0.002], [xr[1], yr[0], z1 + 0.002], [xr[1], yr[1], z1 + 0.002], [xr[0], yr[1], z1 + 0.002]], "face m-neutral f0");
  if (it.axis === "x") pen.poly(g, [[xr[0], yr[1], 0.01], [xr[1], yr[1], 0.01], [xr[1], yr[1], z1], [xr[0], yr[1], z1]], "face m-neutral f1");
  else pen.poly(g, [[xr[1], yr[0], 0.01], [xr[1], yr[1], 0.01], [xr[1], yr[1], z1], [xr[1], yr[0], z1]], "face m-neutral f2");
  const plus = W(it, -hb * 0.75, -0.1), minus = W(it, -hb * 0.75, 0.1);
  const back = (p, q) => (p[0] + p[1] <= q[0] + q[1] ? [p, q] : [q, p]);
  const [first, second] = back(plus, minus);
  for (const p of [first, second]) {
    const isPlus = p === plus;
    pen.cylinder(g, p[0], p[1], isPlus ? 0.055 : 0.07, z1, z1 + 0.07, "m-metal");
  }
  const mid = W(it, hb * 0.05, 0);
  const volts = it.comp.volts ?? 0;
  pen.engrave(g, mid[0], mid[1], z1 + 0.004, it.axis, `${+volts.toPrecision(3)}V`, Math.max(8, pen.u * 0.2));
  return {};
}

function source(pen, g, it) {
  const hb = Math.min(0.38, it.hl - 0.04), hw = 0.3, z1 = 0.32;
  box(pen, g, it, -hb, hb, -hw, hw, 0.01, z1, it.mat);
  const z = z1 + 0.003, t = it.comp.type;
  const glyph = [];
  const at = (u, v) => { const p = W(it, u, v); return [p[0], p[1], z]; };
  if (t === "sine_source") for (let k = 0; k <= 16; k++) { const u = -0.2 + (0.4 * k) / 16; glyph.push(at(u, -0.08 * Math.sin((k / 16) * 2 * Math.PI))); }
  else if (t === "pulse_source") for (const [u, v] of [[-0.2, 0.06], [-0.1, 0.06], [-0.1, -0.08], [0.04, -0.08], [0.04, 0.06], [0.14, 0.06], [0.14, -0.08], [0.2, -0.08]]) glyph.push(at(u, v));
  else if (t === "current_source" || t === "vccs") { pen.line(g, [at(-0.16, 0), at(0.16, 0)], "groove strong"); pen.line(g, [at(0.08, -0.06), at(0.16, 0), at(0.08, 0.06)], "groove strong"); }
  else { pen.line(g, [at(-0.2, 0), at(-0.1, 0)], "groove strong"); pen.line(g, [at(-0.15, -0.05), at(-0.15, 0.05)], "groove strong"); pen.line(g, [at(0.1, 0), at(0.2, 0)], "groove strong"); }
  if (glyph.length) pen.line(g, glyph, "groove strong");
  if (t === "vcvs" || t === "vccs") { const d = [at(0, -0.2), at(0.12, 0), at(0, 0.2), at(-0.12, 0)]; pen.poly(g, d, "groove"); }
  return {};
}

function switchPart(pen, g, it) {
  const hb = Math.min(0.3, it.hl - 0.04), hw = 0.13;
  const pa = -hb * 0.72, pb = hb * 0.72;
  for (const sgn of [-1, 1]) { const a = W(it, sgn * hb * 0.72, 0), c = W(it, sgn * it.hl, 0); pen.line(g, [[a[0], a[1], 0.03], [c[0], c[1], 0.03]], "lead"); }
  box(pen, g, it, -hb, hb, -hw, hw, 0.01, 0.07, it.mat);
  const A = W(it, pa, 0), B = W(it, pb, 0);
  const ordered = A[0] + A[1] <= B[0] + B[1] ? [A, B] : [B, A];
  for (const p of ordered) pen.cylinder(g, p[0], p[1], 0.04, 0.07, 0.15, "m-metal");
  const lever = el("g", { class: "iso-lever" }, g);
  const len = pb - pa;
  const draw = (closed) => {
    lever.innerHTML = "";
    const ang = closed ? 0 : (34 * Math.PI) / 180;
    const end = W(it, pa + len * Math.cos(ang) * (closed ? 1.04 : 1), 0);
    const z = 0.15 + len * Math.sin(ang);
    pen.line(lever, [[A[0], A[1], 0.15], [end[0], end[1], z]], "lever-edge");
    pen.line(lever, [[A[0], A[1], 0.15], [end[0], end[1], z]], `lever ${it.mat === "m-accent" ? "accent" : ""}`);
    const [kx, ky] = pen.p(end[0], end[1], z);
    el("circle", { cx: kx, cy: ky, r: Math.max(2.2, pen.u * 0.05), class: `lever-knob ${it.mat === "m-accent" ? "accent" : ""}` }, lever);
  };
  draw(it.comp.closed !== false);
  return { setClosed: draw, kind: "switch" };
}

function jumper(pen, g, it) {
  const a = W(it, -it.hl, 0), b = W(it, it.hl, 0);
  const h = 0.12;
  const pts = [[a[0], a[1], 0.03], [a[0], a[1], h], [b[0], b[1], h], [b[0], b[1], 0.03]];
  pen.line(g, pts, "jumper-edge");
  pen.line(g, pts, `jumper ${it.mat === "m-accent" ? "accent" : ""}`);
  return {};
}

function openGap(pen, g, it) {
  for (const sgn of [-1, 1]) { const a = W(it, sgn * 0.08, 0), c = W(it, sgn * it.hl, 0); pen.line(g, [[a[0], a[1], 0.03], [c[0], c[1], 0.03]], "lead"); }
  return {};
}

function generic(pen, g, it) {
  const hb = Math.min(0.3, it.hl - 0.04);
  box(pen, g, it, -hb, hb, -0.16, 0.16, 0.01, 0.2, it.mat);
  return {};
}

export function isLamp(task, comp) {
  if (comp.type !== "resistor") return false;
  if (/bulb|lamp/i.test(comp.label || "")) return true;
  const story = `${task.title} ${task.story || ""}`;
  if (!/bulb|lamp|lantern/i.test(story)) return false;
  const named = [...(task.board.fixed || [])].some((c) => c.type === "resistor" && /^L\d*$/.test(c.id));
  if (named) return /^L\d*$/.test(comp.id);
  return (task.board.slots || []).some((s) => s.id === comp.id);
}

export function drawPart(pen, g, it, ctx) {
  const t = it.comp.type;
  if (t === "resistor") {
    if (it.lamp) return lamp(pen, g, it, ctx);
    if (/motor/i.test(it.comp.label || "")) return motor(pen, g, it);
    resistor(pen, g, it);
    return {};
  }
  if (t === "capacitor") return capacitor(pen, g, it);
  if (t === "inductor") return inductor(pen, g, it);
  if (t === "diode" || t === "zener") return diode(pen, g, it);
  if (t === "led") return led(pen, g, it, ctx);
  if (t === "battery") return battery(pen, g, it);
  if (["voltage_source", "pulse_source", "sine_source", "current_source", "vcvs", "vccs"].includes(t)) return source(pen, g, it);
  if (t === "switch") return switchPart(pen, g, it);
  if (t === "wire") return jumper(pen, g, it);
  if (t === "open") return openGap(pen, g, it);
  return generic(pen, g, it);
}

// The natural half length of each part along its axis (clamped later to the room on the board).
export function halfLength(type, lamp) {
  if (lamp) return 0.34;
  return { battery: 0.5, voltage_source: 0.42, pulse_source: 0.42, sine_source: 0.42, current_source: 0.42, vcvs: 0.42, vccs: 0.42,
    resistor: 0.36, capacitor: 0.3, inductor: 0.32, diode: 0.28, zener: 0.28, led: 0.24, switch: 0.36, wire: 0.3, open: 0.3 }[type] ?? 0.34;
}

// Transistors (TO-92 style) and op-amps (DIP-8) are drawn at their body centre with legs to their pins.
export function drawThree(pen, g, it) {
  const { cx, cy, pins } = it;
  const mat = it.mat === "m-accent" ? "m-accent" : "m-dark";
  const z0 = 0.16, z1 = 0.46;
  // legs, painted first because they sit behind the body on screen
  for (const p of pins) pen.line(g, [[cx, cy, z0 + 0.02], [p[0], p[1], 0.03]], "lead");
  pen.cuboid(g, [cx - 0.15, cx + 0.15], [cy - 0.1, cy + 0.1], [z0, z1], mat);
  const [ex, ey] = pen.p(cx + 0.15, cy, (z0 + z1) / 2);
  el("line", { x1: ex, y1: ey - pen.u * 0.05, x2: ex, y2: ey + pen.u * 0.05, class: "groove" }, g);
  return {};
}

export function drawOpAmp(pen, g, it) {
  const { cx, cy, pins } = it;
  const mat = it.mat === "m-accent" ? "m-accent" : "m-dark";
  for (const p of pins) pen.line(g, [[Math.max(cx - 0.36, Math.min(cx + 0.36, p[0])), cy + (p[1] < cy ? -0.18 : p[1] > cy ? 0.18 : 0), 0.08], [p[0], p[1], 0.03]], "lead");
  for (let k = 0; k < 4; k++) {
    const x = cx - 0.27 + k * 0.18;
    pen.cuboid(g, [x - 0.03, x + 0.03], [cy - 0.27, cy + 0.27], [0.02, 0.09], "m-metal");
  }
  pen.cuboid(g, [cx - 0.4, cx + 0.4], [cy - 0.22, cy + 0.22], [0.07, 0.22], mat);
  const [nx, ny] = pen.p(cx - 0.4, cy, 0.22);
  el("path", { d: `M ${nx + pen.u * 0.06} ${ny - pen.u * 0.03} a ${pen.u * 0.07} ${pen.u * 0.05} 0 0 1 ${pen.u * 0.06} ${pen.u * 0.06}`, class: "groove strong" }, g);
  pen.ellipse(g, cx - 0.3, cy - 0.12, 0.222, 0.025, "groove-dot");
  return {};
}
