// Isometric drawing primitives: a 30° projection with no perspective, solids painted with
// three face tones (top lightest) plus a line tone, written as plain SVG elements.
//
// World axes: x and y lie on the board (x = schematic columns, y = schematic rows), z points up.
// One world unit is one schematic grid step.

import { el } from "../ui/svg.js";

export const COS = Math.cos(Math.PI / 6);
export const SIN = 0.5;
const RX = Math.SQRT2 * COS; // a horizontal circle of radius r projects to an ellipse r·RX wide
const RY = Math.SQRT2 * SIN; // and r·RY tall

const fmt = (pts) => pts.map((p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(" ");

export class Pen {
  constructor(unit) {
    this.U = unit;
    this.box = null;
    this.f = null; // an optional local frame { cx, cy, k }: parts are drawn k times larger around their centre
  }

  get u() { return this.U * (this.f ? this.f.k : 1); }
  frame(cx, cy, k) { this.f = { cx, cy, k }; }
  unframe() { this.f = null; }

  // Start collecting the screen bounding box of everything drawn until the next call.
  track() { const b = [Infinity, Infinity, -Infinity, -Infinity]; this.box = b; return b; }
  grow(x, y) { const b = this.box; if (!b) return; if (x < b[0]) b[0] = x; if (y < b[1]) b[1] = y; if (x > b[2]) b[2] = x; if (y > b[3]) b[3] = y; }

  p(x, y, z = 0) {
    const f = this.f;
    if (f) { x = f.cx + (x - f.cx) * f.k; y = f.cy + (y - f.cy) * f.k; z *= f.k; }
    const s = [(x - y) * COS * this.U, (x + y) * SIN * this.U - z * this.U];
    this.grow(s[0], s[1]);
    return s;
  }

  poly(g, pts3, cls, attrs = {}) { return el("polygon", { points: fmt(pts3.map((q) => this.p(...q))), class: cls, ...attrs }, g); }
  line(g, pts3, cls, attrs = {}) { return el("polyline", { points: fmt(pts3.map((q) => this.p(...q))), class: cls, ...attrs }, g); }

  // A box: the +y face (lower left on screen), the +x face (lower right) and the top.
  cuboid(g, [x0, x1], [y0, y1], [z0, z1], mat) {
    this.poly(g, [[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]], `face ${mat} f1`);
    this.poly(g, [[x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [x1, y0, z1]], `face ${mat} f2`);
    this.poly(g, [[x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], `face ${mat} f0`);
  }

  // A vertical cylinder standing on z0.
  cylinder(g, x, y, r, z0, z1, mat, { top = true } = {}) {
    const [cx, cy1] = this.p(x, y, z1);
    const cy0 = cy1 + (z1 - z0) * this.u;
    const rx = r * RX * this.u, ry = r * RY * this.u;
    this.grow(cx - rx, cy1 - ry); this.grow(cx + rx, cy0 + ry);
    const d = `M ${cx - rx} ${cy1} L ${cx - rx} ${cy0} A ${rx} ${ry} 0 0 0 ${cx + rx} ${cy0} L ${cx + rx} ${cy1} A ${rx} ${ry} 0 0 1 ${cx - rx} ${cy1} Z`;
    el("path", { d, class: `face ${mat} side`, fill: `url(#iso-g-${mat.replace("m-", "")})` }, g);
    if (top) el("ellipse", { cx, cy: cy1, rx, ry, class: `face ${mat} f0` }, g);
    return { cx, cy: cy1, rx, ry };
  }

  // A half dome on top of a cylinder (an LED lens).
  dome(g, x, y, r, z, h, cls) {
    const [cx, cy] = this.p(x, y, z);
    const rx = r * RX * this.u, ry = r * RY * this.u, hh = h * this.u;
    this.grow(cx - rx, cy - hh - ry); this.grow(cx + rx, cy + ry);
    const d = `M ${cx - rx} ${cy} A ${rx} ${ry} 0 0 0 ${cx + rx} ${cy} A ${rx} ${hh + ry * 0.4} 0 0 0 ${cx - rx} ${cy} Z`;
    return el("path", { d, class: cls }, g);
  }

  ellipse(g, x, y, z, r, cls) {
    const [cx, cy] = this.p(x, y, z);
    const rx = r * RX * this.u, ry = r * RY * this.u;
    this.grow(cx - rx, cy - ry); this.grow(cx + rx, cy + ry);
    return el("ellipse", { cx, cy, rx, ry, class: cls }, g);
  }

  sphere(g, x, y, z, r, cls) {
    const [cx, cy] = this.p(x, y, z);
    const R = r * RX * this.u; // a sphere projects to a circle of radius r·√1.5
    this.grow(cx - R, cy - R); this.grow(cx + R, cy + R);
    return el("circle", { cx, cy, r: R, class: cls }, g);
  }

  // Text lying flat on a horizontal face, running along world +x (axis "x") or world -y (axis "y").
  engrave(g, x, y, z, axis, str, size, cls = "iso-engrave") {
    const [sx, sy] = this.p(x, y, z);
    const m = axis === "x" ? [COS, SIN, -COS, SIN] : [COS, -SIN, COS, SIN];
    const t = el("text", { x: 0, y: 0, class: cls, "font-size": size, "text-anchor": "middle", "dominant-baseline": "central",
      transform: `matrix(${m.map((v) => v.toFixed(4)).join(" ")} ${sx.toFixed(1)} ${sy.toFixed(1)})` }, g);
    t.textContent = str;
    return t;
  }
}

export function defs(svg, mats) {
  const d = el("defs", {}, svg);
  for (const m of mats) {
    const g = el("linearGradient", { id: `iso-g-${m}`, x1: 0, y1: 0, x2: 1, y2: 0 }, d);
    el("stop", { offset: 0, style: `stop-color: var(--iso-${m}1)` }, g);
    el("stop", { offset: 0.42, style: `stop-color: var(--iso-${m}1)` }, g);
    el("stop", { offset: 0.62, style: `stop-color: var(--iso-${m}2)` }, g);
    el("stop", { offset: 1, style: `stop-color: var(--iso-${m}2)` }, g);
  }
  const glow = el("radialGradient", { id: "iso-glow" }, d);
  el("stop", { offset: 0, style: "stop-color: var(--glow, #ffd36b); stop-opacity: 0.95" }, glow);
  el("stop", { offset: 0.35, style: "stop-color: var(--glow, #ffd36b); stop-opacity: 0.45" }, glow);
  el("stop", { offset: 1, style: "stop-color: var(--glow, #ffd36b); stop-opacity: 0" }, glow);
  const blur = el("filter", { id: "iso-blur", x: "-20%", y: "-20%", width: "140%", height: "140%" }, d);
  el("feGaussianBlur", { stdDeviation: 7 }, blur);
  return d;
}

// A dot grid lying on the board's top face (the breadboard holes), as a pattern mapped into the projection.
export function holePattern(defsNode, unit, step = 0.25) {
  const U = unit;
  const p = el("pattern", { id: "iso-holes", patternUnits: "userSpaceOnUse", width: step, height: step,
    patternTransform: `matrix(${COS * U} ${SIN * U} ${-COS * U} ${SIN * U} 0 0)` }, defsNode);
  el("rect", { x: step / 2 - 0.035, y: step / 2 - 0.035, width: 0.07, height: 0.07, rx: 0.012, class: "iso-hole" }, p);
  return p;
}

export function shade(hex, k) {
  const n = parseInt(hex.slice(1), 16);
  const c = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => Math.round(v * k));
  return `rgb(${c.join(",")})`;
}
