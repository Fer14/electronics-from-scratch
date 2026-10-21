// Low-poly breadboard parts for the Board 3D view, in the lab's palette.
//
// Every builder returns a THREE.Group in a local frame: the part's axis is +x (from pin a to pin b),
// up is +y, the board's top face is y = 0 and the pin holes sit at x = ±L. Geometries are cached and
// shared between parts; materials come from one palette so a theme switch only recolours them.

import * as THREE from "three";
import { bandColors } from "../iso/parts.js";

const geoCache = new Map();
function geo(key, make) {
  if (!geoCache.has(key)) { const g = make(); g.userData.cached = true; geoCache.set(key, g); }
  return geoCache.get(key);
}

export const LED_COLORS = { red: "#e2483d", orange: "#ee8a2b", yellow: "#e8c62c", green: "#3cb563", blue: "#3d7fe0", white: "#f4f1e6", infrared: "#8a2b2b", uv: "#8a5ce0" };

// The palette reads the page's CSS variables, so the 3D view follows the light and dark themes.
export function readPalette() {
  const cs = getComputedStyle(document.documentElement);
  const v = (name, fallback) => (cs.getPropertyValue(name).trim() || fallback);
  return {
    paper: v("--paper", "#fbf7f6"), card: v("--card", "#fffdfc"), ink: v("--ink", "#3a2529"), muted: v("--muted", "#8f7a7e"),
    accent: v("--accent", "#793e4d"), tint: v("--tint", "#bb8190"), wash: v("--wash", "#efe1e5"), line: v("--line-strong", "#dccfcf"),
    sage: v("--sage", "#5f7a5a"), clay: v("--clay", "#b5654a"), sand: v("--sand", "#c9a227"),
    board0: v("--iso-board0", "#f8f2f1"), board1: v("--iso-board1", "#e9dfde"), board2: v("--iso-board2", "#d7cbca"),
    hole: v("--iso-line", "#3a3936"), edge: v("--iso-line", "#3a3936"),
    dark: v("--iso-dark1", "#3d3b39"), dark2: v("--iso-dark2", "#2a2927"), metal: v("--iso-metal1", "#c8c7c2"), metal0: v("--iso-metal0", "#f3f3f0"),
    resist: v("--iso-resist0", "#efe5cf"), copper: v("--iso-copper1", "#c4834f"), neutral: v("--iso-neutral0", "#ffffff"),
    dot: v("--accent", "#793e4d"),
  };
}

export class Materials {
  constructor(pal) {
    this.m = {};
    this.edges = new THREE.LineBasicMaterial({ color: pal.edge, transparent: true, opacity: 0.55 });
    this.edgesAccent = new THREE.LineBasicMaterial({ color: pal.accent });
    this.edges.userData.keep = this.edgesAccent.userData.keep = true;
    this.apply(pal);
  }

  get(name, make) {
    if (!this.m[name]) { this.m[name] = make(); this.m[name].userData.keep = true; }
    return this.m[name];
  }

  std(name, color, extra = {}) {
    return this.get(name, () => new THREE.MeshStandardMaterial({ color, roughness: 0.72, metalness: 0, flatShading: true, ...extra }));
  }

  apply(pal) {
    this.pal = pal;
    const set = { body: pal.dark2, dark: pal.dark, metal: pal.metal, resist: pal.resist, copper: pal.copper, neutral: pal.neutral,
      sage: pal.sage, clay: pal.clay, sand: pal.sand, accent: pal.accent, tint: pal.tint, ink: pal.ink, card: pal.card, board: pal.board0, boardSide: pal.board1 };
    for (const [k, c] of Object.entries(set)) {
      const mat = this.std(k, c, k === "metal" ? { roughness: 0.38 } : {});
      mat.color.set(c);
    }
    this.edges.color.set(pal.edge);
    this.edgesAccent.color.set(pal.accent);
    if (this.m.ghost) this.m.ghost.color.set(pal.accent);
  }

  ghost() { return this.get("ghost", () => new THREE.MeshBasicMaterial({ color: this.pal.accent, transparent: true, opacity: 0.42, depthWrite: false })); }
  band(color) { return this.get(`band:${color}`, () => new THREE.MeshStandardMaterial({ color, roughness: 0.6, flatShading: true })); }
  wire(color) { return this.get(`wire:${color}`, () => new THREE.MeshStandardMaterial({ color, roughness: 0.55 })); }
  led(color) {
    return new THREE.MeshStandardMaterial({ color, roughness: 0.25, transparent: true, opacity: 0.82, emissive: new THREE.Color(color), emissiveIntensity: 0, flatShading: true });
  }
}

// A mesh, optionally with a crisp outline in the illustration style.
function mesh(g, geometry, material, { outline = true, shadow = true } = {}) {
  const m = new THREE.Mesh(geometry, material);
  m.castShadow = shadow;
  m.receiveShadow = false;
  g.add(m);
  if (outline) {
    const key = `edges:${geometry.uuid}`;
    const eg = geo(key, () => new THREE.EdgesGeometry(geometry, 32));
    const lines = new THREE.LineSegments(eg, null);
    lines.userData.outline = true;
    m.add(lines);
  }
  return m;
}

// A thin metal lead (or any tube) along a polyline with softly rounded corners.
export function tubeAlong(points, radius, material, { radial = 5, round = 0.05, outline = false } = {}) {
  const path = new THREE.CurvePath();
  const P = points.map((p) => (p.isVector3 ? p : new THREE.Vector3(...p)));
  let cur = P[0].clone();
  for (let i = 1; i < P.length; i++) {
    const a = P[i - 1], b = P[i], c = P[i + 1];
    if (!c) { path.add(new THREE.LineCurve3(cur, b.clone())); break; }
    const ab = b.clone().sub(a), bc = c.clone().sub(b);
    const r = Math.min(round, ab.length() / 2, bc.length() / 2);
    const p1 = b.clone().sub(ab.normalize().multiplyScalar(r));
    const p2 = b.clone().add(bc.normalize().multiplyScalar(r));
    if (cur.distanceTo(p1) > 1e-4) path.add(new THREE.LineCurve3(cur, p1));
    path.add(new THREE.QuadraticBezierCurve3(p1, b.clone(), p2));
    cur = p2;
  }
  const len = path.getLength();
  const g = new THREE.TubeGeometry(path, Math.max(8, Math.round(len * 40)), radius, radial, false);
  const m = new THREE.Mesh(g, material);
  m.castShadow = true;
  m.userData.curve = path;
  return m;
}

const lead = (mats, pts) => tubeAlong(pts, 0.014, mats.std("metal"), { radial: 4, round: 0.04 });
const DOWN = -0.06; // legs end a little inside the hole

// Axial parts (resistor, diode, inductor): body lifted over the board, legs bent down at ±L.
function axialLegs(g, mats, L, half, y) {
  for (const s of [-1, 1]) g.add(lead(mats, [[s * half * 0.98, y, 0], [s * L, y, 0], [s * L, DOWN, 0]]));
}

// Standing parts (LED, capacitor, bulb): two legs from under the body, splayed out to ±L.
function standingLegs(g, mats, L, y, gap = 0.05) {
  for (const s of [-1, 1]) g.add(lead(mats, [[s * gap, y, 0], [s * gap, Math.min(y, 0.1), 0], [s * L, 0.05, 0], [s * L, DOWN, 0]]));
}

function cylX(r, len, seg = 10) { return geo(`cylx:${r}:${len}:${seg}`, () => new THREE.CylinderGeometry(r, r, len, seg).rotateZ(Math.PI / 2)); }
function cylY(r, h, seg = 12) { return geo(`cyly:${r}:${h}:${seg}`, () => new THREE.CylinderGeometry(r, r, h, seg)); }
function box(w, h, d) { return geo(`box:${w}:${h}:${d}`, () => new THREE.BoxGeometry(w, h, d)); }

function resistor(mats, L, comp) {
  const g = new THREE.Group();
  const y = 0.13, half = Math.min(0.3, L - 0.05);
  const k = half / 0.3;
  axialLegs(g, mats, L, half, y);
  const body = new THREE.Group();
  mesh(body, cylX(0.075, 0.42), mats.std("resist"));
  for (const s of [-1, 1]) { const cap = mesh(body, cylX(0.095, 0.14), mats.std("resist")); cap.position.x = s * 0.23; }
  const colors = bandColors(comp ? comp.ohms : 1000);
  const at = [-0.2, -0.11, -0.04, 0.17];
  colors.forEach((c, i) => {
    const r = Math.abs(at[i]) > 0.15 ? 0.099 : 0.079;
    const b = mesh(body, cylX(r, 0.035), mats.band(c), { outline: false });
    b.position.x = at[i];
  });
  body.scale.x = k;
  body.position.y = y;
  g.add(body);
  return g;
}

function diode(mats, L, comp) {
  const g = new THREE.Group();
  const y = 0.11, half = Math.min(0.22, L - 0.05);
  axialLegs(g, mats, L, half, y);
  const zener = comp && comp.type === "zener";
  const body = mesh(g, cylX(0.065, half * 2), zener ? mats.std("sand") : mats.std("body"));
  body.position.y = y;
  const band = mesh(g, cylX(0.068, 0.05), zener ? mats.std("body") : mats.std("metal"), { outline: false });
  band.position.set(half * 0.68, y, 0);
  return g;
}

function inductor(mats, L) {
  const g = new THREE.Group();
  const y = 0.14, half = Math.min(0.28, L - 0.05);
  axialLegs(g, mats, L, half, y);
  const core = mesh(g, cylX(0.06, half * 2), mats.std("dark"));
  core.position.y = y;
  const ring = geo("coil", () => new THREE.TorusGeometry(0.075, 0.03, 6, 12).rotateY(Math.PI / 2));
  const n = 6;
  for (let i = 0; i < n; i++) { const r = mesh(g, ring, mats.std("copper"), { outline: false }); r.position.set(-half * 0.8 + (i * 1.6 * half) / (n - 1), y, 0); }
  return g;
}

function capacitor(mats, L) {
  const g = new THREE.Group();
  const y0 = 0.07, h = 0.38;
  standingLegs(g, mats, L, y0);
  const can = mesh(g, cylY(0.14, h, 14), mats.std("sage"));
  can.position.y = y0 + h / 2;
  const stripe = mesh(g, box(0.07, h * 0.9, 0.02), mats.std("card"), { outline: false });
  stripe.position.set(-0.04, y0 + h / 2, 0.135);
  const top = mesh(g, cylY(0.12, 0.012, 14), mats.std("metal"), { outline: false });
  top.position.y = y0 + h + 0.006;
  return g;
}

function ledPart(mats, L, comp) {
  const g = new THREE.Group();
  const color = LED_COLORS[(comp && comp.color) || "red"] || LED_COLORS.red;
  const mat = mats.led(color);
  const y0 = 0.14;
  standingLegs(g, mats, L, y0);
  const flange = mesh(g, cylY(0.15, 0.04, 14), mat);
  flange.position.y = y0 + 0.02;
  const barrel = mesh(g, cylY(0.13, 0.18, 14), mat);
  barrel.position.y = y0 + 0.13;
  const dome = mesh(g, geo("dome", () => new THREE.SphereGeometry(0.13, 14, 7, 0, Math.PI * 2, 0, Math.PI / 2)), mat);
  dome.position.y = y0 + 0.22;
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTexture(), color, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending }));
  halo.scale.set(0.9, 0.9, 1);
  halo.position.y = y0 + 0.2;
  g.add(halo);
  g.userData.glow = { kind: "led", mats: [mat], halo };
  return g;
}

function lampPart(mats, L) {
  const g = new THREE.Group();
  standingLegs(g, mats, L, 0.06, 0.06);
  const socket = mesh(g, box(0.32, 0.08, 0.3), mats.std("dark"));
  socket.position.y = 0.06;
  const base = mesh(g, cylY(0.09, 0.14, 12), mats.std("metal"));
  base.position.y = 0.17;
  const glassMat = new THREE.MeshStandardMaterial({ color: "#fff6dc", roughness: 0.15, transparent: true, opacity: 0.45, emissive: new THREE.Color("#ffcf5a"), emissiveIntensity: 0, depthWrite: false });
  const glass = mesh(g, geo("bulb", () => new THREE.SphereGeometry(0.2, 16, 12)), glassMat, { outline: false });
  glass.position.y = 0.42;
  const filMat = new THREE.MeshStandardMaterial({ color: "#5b4a3a", emissive: new THREE.Color("#ffb020"), emissiveIntensity: 0 });
  const fil = new THREE.Mesh(geo("fil", () => new THREE.TorusGeometry(0.06, 0.008, 4, 12, Math.PI)), filMat);
  fil.position.y = 0.36;
  g.add(fil);
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTexture(), color: "#ffd36b", transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending }));
  halo.scale.set(1.4, 1.4, 1);
  halo.position.y = 0.42;
  g.add(halo);
  g.userData.glow = { kind: "lamp", mats: [glassMat, filMat], halo };
  return g;
}

function switchPart(mats, L, comp) {
  const g = new THREE.Group();
  const half = Math.min(0.26, L - 0.04);
  for (const s of [-1, 1]) g.add(lead(mats, [[s * half * 0.8, 0.04, 0], [s * L, 0.04, 0], [s * L, DOWN, 0]]));
  const base = mesh(g, box(half * 2, 0.08, 0.26), mats.std("dark"));
  base.position.y = 0.06;
  for (const s of [-1, 1]) { const post = mesh(g, cylY(0.035, 0.08, 8), mats.std("metal")); post.position.set(s * half * 0.7, 0.14, 0); }
  const hinge = new THREE.Group();
  hinge.position.set(-half * 0.7, 0.19, 0);
  const lever = mesh(hinge, box(half * 1.55, 0.028, 0.07), mats.std("metal"));
  lever.position.x = half * 0.77;
  const knob = mesh(hinge, box(0.08, 0.06, 0.1), mats.std("clay"));
  knob.position.set(half * 1.5, 0.03, 0);
  g.add(hinge);
  const setClosed = (closed) => { hinge.rotation.z = closed ? 0 : 0.6; };
  setClosed(!comp || comp.closed !== false);
  g.userData.setClosed = setClosed;
  return g;
}

// Batteries and bench sources lie on the board; their red and black snap leads go into the holes.
function batteryPack(mats, L, comp, wireMats) {
  const g = new THREE.Group();
  const half = Math.min(0.5, Math.max(0.3, L - 0.14));
  const holder = mesh(g, box(half * 2, 0.16, 0.5), mats.std("ink"));
  holder.position.y = 0.08;
  for (const z of [-0.12, 0.12]) {
    const cell = mesh(g, cylX(0.1, half * 1.7, 12), mats.std("sand"));
    cell.position.set(0, 0.2, z);
    const tip = mesh(g, cylX(0.045, 0.04, 8), mats.std("metal"), { outline: false });
    tip.position.set(z > 0 ? -half * 0.87 : half * 0.87, 0.2, z);
  }
  // + at the a end (x = -L), − at the b end
  g.add(tubeAlong([[-half, 0.12, 0.18], [-half - 0.08, 0.14, 0.18], [-L, 0.12, 0], [-L, DOWN, 0]], 0.03, wireMats.plus, { round: 0.08 }));
  g.add(tubeAlong([[half, 0.12, 0.18], [half + 0.08, 0.14, 0.18], [L, 0.12, 0], [L, DOWN, 0]], 0.03, wireMats.minus, { round: 0.08 }));
  return g;
}

function benchSource(mats, L, comp, wireMats) {
  const g = new THREE.Group();
  const half = Math.min(0.42, Math.max(0.26, L - 0.14));
  const type = comp ? comp.type : "voltage_source";
  const bodyMat = type === "current_source" ? mats.std("sage") : mats.std("card");
  const body = mesh(g, box(half * 2, 0.26, 0.48), bodyMat);
  body.position.y = 0.13;
  const face = mesh(g, box(half * 1.2, 0.01, 0.26), mats.std("ink"), { outline: false });
  face.position.set(-half * 0.25, 0.265, -0.04);
  const accent = type === "pulse_source" ? "sand" : type === "sine_source" ? "sage" : type === "current_source" ? "card" : "clay";
  const knob = mesh(g, cylY(0.07, 0.07, 10), mats.std(accent));
  knob.position.set(half * 0.62, 0.3, 0.05);
  if (type === "current_source") {
    const arrow = mesh(g, geo("arrow", () => new THREE.ConeGeometry(0.06, 0.16, 8).rotateZ(-Math.PI / 2)), mats.std("ink"));
    arrow.position.set(-half * 0.25, 0.32, -0.04);
  }
  g.add(tubeAlong([[-half, 0.1, 0.1], [-half - 0.08, 0.1, 0.1], [-L, 0.1, 0], [-L, DOWN, 0]], 0.03, wireMats.plus, { round: 0.08 }));
  g.add(tubeAlong([[half, 0.1, 0.1], [half + 0.08, 0.1, 0.1], [L, 0.1, 0], [L, DOWN, 0]], 0.03, wireMats.minus, { round: 0.08 }));
  return g;
}

function controlled(mats, L) {
  const g = new THREE.Group();
  const half = Math.min(0.3, L - 0.06);
  axialLegs(g, mats, L, half, 0.06);
  const b = mesh(g, box(half * 2, 0.12, 0.3), mats.std("body"));
  b.position.y = 0.1;
  return g;
}

function jumperPart(mats, L, wireMat) {
  const g = new THREE.Group();
  g.add(tubeAlong([[-L, DOWN, 0], [-L, 0.12, 0], [L, 0.12, 0], [L, DOWN, 0]], 0.03, wireMat, { round: 0.08 }));
  return g;
}

function openPart(mats, L) {
  const g = new THREE.Group();
  for (const s of [-1, 1]) { const cap = mesh(g, cylY(0.05, 0.03, 8), mats.std("tint")); cap.position.set(s * L, 0.015, 0); }
  return g;
}

export function twoTerminal(type, mats, L, comp, ctx) {
  if (ctx.lamp) return lampPart(mats, L);
  switch (type) {
    case "resistor": return resistor(mats, L, comp);
    case "diode": case "zener": return diode(mats, L, comp);
    case "led": return ledPart(mats, L, comp);
    case "capacitor": return capacitor(mats, L);
    case "inductor": return inductor(mats, L);
    case "switch": return switchPart(mats, L, comp);
    case "battery": return batteryPack(mats, L, comp, ctx.wireMats);
    case "voltage_source": case "pulse_source": case "sine_source": case "current_source": return benchSource(mats, L, comp, ctx.wireMats);
    case "vcvs": case "vccs": return controlled(mats, L);
    case "wire": return jumperPart(mats, L, ctx.wireMats.jumper);
    case "open": return openPart(mats, L);
    default: return resistor(mats, L, comp);
  }
}

// TO-92: legs at x = -p, 0, +p (E B C), flat face toward +z (the viewer).
export function to92(mats, p) {
  const g = new THREE.Group();
  const y0 = 0.2, h = 0.34;
  const half = geo("to92", () => {
    const shape = new THREE.Shape();
    shape.moveTo(-0.15, 0);
    shape.absarc(0, 0, 0.15, Math.PI, 0, true);
    shape.lineTo(-0.15, 0);
    return new THREE.ExtrudeGeometry(shape, { depth: h, bevelEnabled: false, curveSegments: 6 }).rotateX(Math.PI / 2).translate(0, h, 0);
  });
  const body = mesh(g, half, mats.std("body"));
  body.rotation.y = Math.PI;
  body.position.set(0, y0, 0.02);
  for (const k of [-1, 0, 1]) g.add(lead(mats, [[k * 0.07, y0 + 0.01, 0], [k * 0.07, 0.12, 0], [k * p, 0.05, 0], [k * p, DOWN, 0]]));
  return g;
}

// DIP-8 over the channel: pin k (0..7) hole positions are given in local coordinates.
export function dip8(mats, holes, center) {
  const g = new THREE.Group();
  const w = 4 * 0.25 - 0.05, d = Math.abs(holes[0][1] - holes[7][1]) - 0.12;
  const body = mesh(g, box(w, 0.13, d), mats.std("body"));
  body.position.y = 0.16;
  const notch = mesh(g, geo("notch", () => new THREE.CylinderGeometry(0.05, 0.05, 0.012, 10, 1, false, 0, Math.PI)), mats.std("dark"), { outline: false });
  notch.rotation.y = Math.PI / 2;
  notch.position.set(-w / 2, 0.226, 0);
  const dot = mesh(g, cylY(0.025, 0.006, 8), mats.std("card"), { outline: false });
  dot.position.set(-w / 2 + 0.08, 0.228, d / 2 - 0.08);
  for (const [x, z] of holes.map(([hx, hz]) => [hx - center[0], hz - center[1]])) {
    const s = Math.sign(z) || 1;
    g.add(tubeAlong([[x, 0.14, s * (d / 2 - 0.02)], [x, 0.14, s * (d / 2 + 0.03)], [x, DOWN, z]], 0.016, mats.std("metal"), { radial: 4, round: 0.03 }));
  }
  return g;
}

let glowTex = null;
function glowTexture() {
  if (glowTex) return glowTex;
  const c = document.createElement("canvas");
  c.width = c.height = 64;
  const x = c.getContext("2d");
  const grd = x.createRadialGradient(32, 32, 0, 32, 32, 32);
  grd.addColorStop(0, "rgba(255,255,255,1)");
  grd.addColorStop(0.35, "rgba(255,255,255,0.45)");
  grd.addColorStop(1, "rgba(255,255,255,0)");
  x.fillStyle = grd;
  x.fillRect(0, 0, 64, 64);
  glowTex = new THREE.CanvasTexture(c);
  return glowTex;
}

// Outline colour for a whole part: accent for parts the learner placed, ink for the fixed ones.
export function setOutline(group, mats, accent) {
  group.traverse((o) => { if (o.userData.outline) o.material = accent ? mats.edgesAccent : mats.edges; });
}

// A see-through copy of a part, for an empty slot.
export function ghostify(group, mats) {
  const ghost = mats.ghost();
  group.traverse((o) => {
    if (o.isMesh) { o.material = ghost; o.castShadow = false; }
    if (o.isSprite) o.visible = false;
    if (o.userData.outline) o.visible = false;
  });
  return group;
}
