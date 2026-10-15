// A small line plot in SVG: time traces for transients, Bode magnitude for AC sweeps.

import { el, text } from "./svg.js";
import { eng } from "../sim/lab.js";
import { maxOf, minOf } from "../sim/engine.js";

const W = 520, HGT = 210, L = 58, R = 14, T = 14, B = 34;

function niceTicks(lo, hi, n = 5) {
  if (!(hi > lo)) { hi = lo + 1; lo -= 1; }
  const raw = (hi - lo) / n, mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 5, 10].map((m) => m * mag).find((s) => s >= raw);
  const out = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + step * 1e-9; v += step) out.push(+v.toPrecision(12));
  return out;
}

export function plot(host, { x, series, xLabel, yUnit, xUnit = "s", logX = false, marks = [] }) {
  host.innerHTML = "";
  const svg = el("svg", { viewBox: `0 0 ${W} ${HGT}`, class: "plot-svg", role: "img", "aria-label": "plot" }, host);
  const fx = logX ? (v) => Math.log10(v) : (v) => v;
  const xs = x.map(fx);
  const x0 = minOf(xs), x1 = maxOf(xs);
  let y0 = Infinity, y1 = -Infinity;
  for (const s of series) for (const v of s.y) if (Number.isFinite(v)) { y0 = Math.min(y0, v); y1 = Math.max(y1, v); }
  for (const m of marks) if (m.y !== undefined) { y0 = Math.min(y0, m.y); y1 = Math.max(y1, m.y); }
  if (y1 - y0 < 1e-12) { y0 -= 1; y1 += 1; }
  const pad = (y1 - y0) * 0.08; y0 -= pad; y1 += pad;
  const sx = (v) => L + ((fx(v) - x0) / (x1 - x0 || 1)) * (W - L - R);
  const sy = (v) => T + (1 - (v - y0) / (y1 - y0)) * (HGT - T - B);
  const grid = el("g", { class: "plot-grid" }, svg);
  for (const v of niceTicks(y0, y1)) {
    el("line", { x1: L, x2: W - R, y1: sy(v), y2: sy(v), class: "grid-line" }, grid);
    text(grid, L - 6, sy(v) + 3, yUnit === "dB" ? `${+v.toPrecision(3)}` : eng(v, yUnit).replace(" ", ""), "axis", { "text-anchor": "end" });
  }
  const xt = logX ? niceTicks(x0, x1).filter((v) => Number.isInteger(v)).map((v) => 10 ** v) : niceTicks(x0, x1);
  for (const v of xt) {
    el("line", { x1: sx(v), x2: sx(v), y1: T, y2: HGT - B, class: "grid-line" }, grid);
    text(grid, sx(v), HGT - B + 14, eng(v, xUnit).replace(" ", ""), "axis", { "text-anchor": "middle" });
  }
  text(svg, W - R, HGT - 4, xLabel, "axis", { "text-anchor": "end" });
  el("rect", { x: L, y: T, width: W - L - R, height: HGT - T - B, class: "plot-frame" }, svg);
  for (const m of marks) {
    if (m.y !== undefined) el("line", { x1: L, x2: W - R, y1: sy(m.y), y2: sy(m.y), class: "mark-line" }, svg);
    if (m.x !== undefined && Number.isFinite(m.x)) el("line", { x1: sx(m.x), x2: sx(m.x), y1: T, y2: HGT - B, class: "mark-line" }, svg);
  }
  series.forEach((s, k) => {
    const step = Math.max(1, Math.floor(x.length / 900));
    const pts = [];
    for (let i = 0; i < x.length; i += step) if (Number.isFinite(s.y[i])) pts.push(`${sx(x[i]).toFixed(1)},${sy(s.y[i]).toFixed(1)}`);
    el("polyline", { points: pts.join(" "), class: `trace trace-${k}` }, svg);
    text(svg, W - R - 8 - k * 110, T + 14, s.name, `legend trace-${k}-text`, { "text-anchor": "end" });
  });
  const cursor = el("line", { x1: L, x2: L, y1: T, y2: HGT - B, class: "cursor", visibility: "hidden" }, svg);
  return {
    setCursor(v) {
      if (v === null) { cursor.setAttribute("visibility", "hidden"); return; }
      cursor.setAttribute("visibility", "visible");
      cursor.setAttribute("x1", sx(v)); cursor.setAttribute("x2", sx(v));
    },
  };
}
