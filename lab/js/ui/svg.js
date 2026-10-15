// Tiny SVG helpers and the standard schematic symbols, drawn in a local frame.
// Two-terminal symbols run along the x axis from -H (terminal a) to +H (terminal b).

export const NS = "http://www.w3.org/2000/svg";
export const H = 22;

export function el(tag, attrs = {}, parent = null) {
  const node = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) if (v !== undefined && v !== null) node.setAttribute(k, v);
  if (parent) parent.appendChild(node);
  return node;
}

export function text(parent, x, y, content, cls = "lbl", attrs = {}) {
  const t = el("text", { x, y, class: cls, ...attrs }, parent);
  t.textContent = content;
  return t;
}

const line = (g, x1, y1, x2, y2, cls = "sym") => el("line", { x1, y1, x2, y2, class: cls }, g);
const path = (g, d, cls = "sym") => el("path", { d, class: cls }, g);

function resistor(g) {
  const pts = [[-H, 0], [-14, 0]];
  for (let i = 0; i < 6; i++) pts.push([-12 + i * 5 + 2.5, i % 2 ? 6 : -6]);
  pts.push([16, 0], [H, 0]);
  el("polyline", { points: pts.map((p) => p.join(",")).join(" "), class: "sym" }, g);
}

function capacitor(g) {
  line(g, -H, 0, -4, 0); line(g, 4, 0, H, 0);
  line(g, -4, -12, -4, 12, "sym plate"); line(g, 4, -12, 4, 12, "sym plate");
}

function inductor(g) {
  line(g, -H, 0, -16, 0); line(g, 16, 0, H, 0);
  path(g, "M -16 0 a 4 4 0 0 1 8 0 a 4 4 0 0 1 8 0 a 4 4 0 0 1 8 0 a 4 4 0 0 1 8 0");
}

function battery(g) {
  line(g, -H, 0, -4, 0); line(g, 4, 0, H, 0);
  line(g, -4, -14, -4, 14, "sym plate"); line(g, 4, -7, 4, 7, "sym plate thick");
  text(g, -12, -10, "+", "pol"); text(g, 12, -10, "−", "pol");
}

function sourceCircle(g, inner) {
  line(g, -H, 0, -15, 0); line(g, 15, 0, H, 0);
  el("circle", { cx: 0, cy: 0, r: 15, class: "sym fillbg" }, g);
  inner(g);
}

function voltageSource(g) { sourceCircle(g, (s) => { text(s, -7, 4, "+", "pol"); text(s, 7, 4, "−", "pol"); }); }
function pulseSource(g) { sourceCircle(g, (s) => path(s, "M -9 4 H -4 V -5 H 2 V 4 H 8 V -5", "sym thin")); }
function sineSource(g) { sourceCircle(g, (s) => path(s, "M -9 0 C -6 -10 -2 -10 0 0 C 2 10 6 10 9 0", "sym thin")); }
function currentSource(g) {
  sourceCircle(g, (s) => { line(s, -8, 0, 7, 0, "sym thin"); path(s, "M 3 -4 L 8 0 L 3 4", "sym thin"); });
}

function diamond(g, inner) {
  line(g, -H, 0, -15, 0); line(g, 15, 0, H, 0);
  path(g, "M -15 0 L 0 -15 L 15 0 L 0 15 Z", "sym fillbg");
  inner(g);
}

function vcvs(g) { diamond(g, (s) => { text(s, -7, 4, "+", "pol"); text(s, 7, 4, "−", "pol"); }); }
function vccs(g) { diamond(g, (s) => { line(s, -8, 0, 7, 0, "sym thin"); path(s, "M 3 -4 L 8 0 L 3 4", "sym thin"); }); }

function diodeBody(g, cls = "sym fillbg") {
  line(g, -H, 0, -8, 0); line(g, 8, 0, H, 0);
  path(g, "M -8 -9 L 8 0 L -8 9 Z", cls);
}

function diode(g) { diodeBody(g); line(g, 8, -9, 8, 9, "sym plate"); }

function led(g, color) {
  diodeBody(g, "sym led-body");
  line(g, 8, -9, 8, 9, "sym plate");
  for (const dx of [-2, 5]) {
    line(g, dx, -11, dx + 6, -19, "sym thin");
    path(g, `M ${dx + 2} -18 L ${dx + 6} -19 L ${dx + 5.5} -15`, "sym thin");
  }
  g.dataset.color = color || "red";
}

function zener(g) { diodeBody(g); path(g, "M 4 -11 L 8 -9 L 8 9 L 12 11", "sym plate"); }

function switchSym(g, closed) {
  line(g, -H, 0, -10, 0); line(g, 10, 0, H, 0);
  el("circle", { cx: -10, cy: 0, r: 2.4, class: "sym fillink" }, g);
  el("circle", { cx: 10, cy: 0, r: 2.4, class: "sym fillink" }, g);
  if (closed) line(g, -10, 0, 10, -1.5); else line(g, -10, 0, 8, -10);
}

function wire(g) { line(g, -H, 0, H, 0); }
function open(g) { line(g, -H, 0, -6, 0); line(g, 6, 0, H, 0); }

export const TWO_TERMINAL = {
  resistor, capacitor, inductor, battery, voltage_source: voltageSource, pulse_source: pulseSource,
  sine_source: sineSource, current_source: currentSource, diode, led, zener,
  switch: (g, c) => switchSym(g, c.closed !== false), wire, open, vcvs, vccs,
};

export function drawTwoTerminal(g, comp) {
  const fn = TWO_TERMINAL[comp.type];
  if (fn) fn(g, comp.type === "led" ? comp.color : comp);
  else { el("rect", { x: -H, y: -10, width: 2 * H, height: 20, class: "sym fillbg" }, g); text(g, 0, 4, comp.type, "tiny", { "text-anchor": "middle" }); }
}

export function drawBJT(g, pnp) {
  el("circle", { cx: 2, cy: 0, r: 21, class: "sym thin fillbg" }, g);
  line(g, -24, 0, -7, 0);
  line(g, -7, -12, -7, 12, "sym plate");
  path(g, "M -7 -6 L 10 -15 L 10 -26");
  path(g, "M -7 6 L 10 15 L 10 26");
  if (pnp) path(g, "M -1 12 L -6 6.5 L 1 5", "sym thin fillink");
  else path(g, "M 2 9 L 9 14.5 L 1 15.5", "sym thin fillink");
}

export function drawMOS(g, pmos) {
  el("circle", { cx: 2, cy: 0, r: 21, class: "sym thin fillbg" }, g);
  line(g, pmos ? -24 : -24, 0, pmos ? -15 : -11, 0);
  if (pmos) el("circle", { cx: -13, cy: 0, r: 2.4, class: "sym thin fillbg" }, g);
  line(g, -11, -11, -11, 11, "sym plate");
  line(g, -5, -13, -5, 13, "sym plate");
  path(g, "M -5 -9 L 10 -9 L 10 -26");
  path(g, "M -5 9 L 10 9 L 10 26");
  if (pmos) path(g, "M 4 -12 L 8 -9 L 4 -6", "sym thin");
  else path(g, "M 0 6 L -4 9 L 0 12", "sym thin");
}

export function drawOpAmp(g, topSign) {
  path(g, "M -30 -32 L -30 32 L 34 0 Z", "sym fillbg");
  line(g, -44, -16, -30, -16); line(g, -44, 16, -30, 16); line(g, 34, 0, 48, 0);
  text(g, -22, -11, topSign === "plus" ? "+" : "−", "pol");
  text(g, -22, 21, topSign === "plus" ? "−" : "+", "pol");
}

const GATE_BODY = {
  and: "M -24 -18 H 4 A 18 18 0 0 1 4 18 H -24 Z",
  or: "M -24 -18 Q -12 0 -24 18 Q 8 18 24 0 Q 8 -18 -24 -18 Z",
  buf: "M -20 -16 L 18 0 L -20 16 Z",
};

export function drawGate(g, op, nInputs) {
  const base = { and: "and", nand: "and", or: "or", nor: "or", xor: "or", xnor: "or", not: "buf", buf: "buf" }[op] || "and";
  path(g, GATE_BODY[base], "sym fillbg");
  if (op === "xor" || op === "xnor") path(g, "M -30 -18 Q -18 0 -30 18", "sym");
  const bubble = ["nand", "nor", "xnor", "not"].includes(op);
  const tip = base === "buf" ? 18 : 22 + (base === "or" ? 2 : 0);
  if (bubble) el("circle", { cx: tip + 4, cy: 0, r: 4, class: "sym fillbg" }, g);
  line(g, bubble ? tip + 8 : tip, 0, 36, 0);
  const pins = gatePins(nInputs);
  const edge = base === "or" ? -19 : base === "buf" ? -20 : -24;
  for (const y of pins) line(g, -36, y, op === "xor" || op === "xnor" ? -27 : edge, y);
}

export function gatePins(n) {
  if (n <= 1) return [0];
  return Array.from({ length: n }, (_, i) => (i - (n - 1) / 2) * (28 / (n - 1)));
}

export function drawFlop(g) {
  el("rect", { x: -24, y: -28, width: 48, height: 56, rx: 2, class: "sym fillbg" }, g);
  text(g, -19, -8, "D", "tiny"); text(g, 12, -8, "Q", "tiny");
  path(g, "M -24 8 L -16 14 L -24 20", "sym thin");
  line(g, -36, -12, -24, -12); line(g, 24, -12, 36, -12);
  line(g, -36, 14, -24, 14, "sym thin");
  text(g, -34, 26, "clk", "tiny");
}

export function drawBlock(g, comp, slotted) {
  if (comp.type === "register") {
    el("rect", { x: -14, y: -20, width: 28, height: 40, rx: 2, class: "sym fillbg" }, g);
    path(g, "M -14 10 L -7 15 L -14 20", "sym thin");
    line(g, -H - 18, 0, -14, 0); line(g, 14, 0, H + 18, 0);
    text(g, 0, -2, "reg", "tiny", { "text-anchor": "middle" });
    return;
  }
  if (comp.type === "wire") { line(g, -H - 18, 0, H + 18, 0); return; }
  el("rect", { x: -40, y: -17, width: 80, height: 34, rx: 3, class: "sym fillbg" }, g);
  text(g, 0, -2, comp.type.replace(/_/g, " "), "tiny", { "text-anchor": "middle" });
  text(g, 0, 11, blockSize(comp), "tiny muted", { "text-anchor": "middle" });
}

export function blockSize(c) {
  if (c.rows) return `${c.rows}×${c.cols} · ${c.bits} bit`;
  if (c.words) return `${c.words} × ${c.bits} bit`;
  if (c.stages) return `${c.bits} bit · ${c.stages} stages`;
  if (c.type === "gates") return `${c.area} gates · depth ${c.depth}`;
  if (c.type === "mux") return `${c.inputs}:1 · ${c.bits} bit`;
  if (c.bits) return `${c.bits} bit`;
  return "";
}
