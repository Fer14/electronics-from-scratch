// Places a task's circuit on a breadboard, without any per-task tuning.
//
// The schematic Board has already routed every wire and placed every part on the task's node grid
// (board.geo). This module lifts those positions onto a breadboard lattice (one grid step = four
// holes) and then keeps the breadboard honest: the five holes of a short strip, and the whole length
// of a power rail, are connected underneath, so every strip is claimed by one net only. A part's legs
// go into holes of their own strips, each node gets a strip, and a jumper wire joins a leg's strip to
// its node's strip (no jumper when they already share one). Ground prefers the blue (−) rail.
//
// World axes: x along the board (schematic columns), y along the board (schematic rows), in grid units.
// The 3D view maps (x, y) to three.js (x, z) and lifts things up along +y.

import { GRID, MARGIN } from "../ui/board.js";
import { isLamp } from "../iso/parts.js";

export const PITCH = 0.25; // hole spacing in grid units (a grid step is four holes)
export const PART_SCALE = 1.6; // parts are drawn this much larger than life, like the iso view's parts
const T = 14; // one module: + rail, − rail, five rows, channel, five rows, gap (in pitches)
const HALF_A = [2.5, 3.5, 4.5, 5.5, 6.5];
const HALF_B = [8.5, 9.5, 10.5, 11.5, 12.5];
const CHANNEL = 7.5;
const RAILS = [0, 1]; // + then −

// Half length of each part's body along its axis (grid units); legs go a bit beyond it.
const BODY = { resistor: 0.3, lamp: 0.2, capacitor: 0.14, inductor: 0.3, diode: 0.24, zener: 0.24, led: 0.14, switch: 0.26,
  battery: 0.5, voltage_source: 0.42, pulse_source: 0.42, sine_source: 0.42, current_source: 0.3, vcvs: 0.34, vccs: 0.34, wire: 0.2, open: 0.2 };

export function bodyHalf(type, lamp) { return lamp ? BODY.lamp : BODY[type] ?? 0.28; }

export function layoutBoard(task, board, choice) {
  const ground = task.board.ground || "gnd";
  const netOf = (n) => (n === ground || n === "0" ? "GND" : n);
  const toWorld = ([px, py]) => [(px - MARGIN) / GRID + board.minX, (py - MARGIN) / GRID + board.minY];
  const near = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1]) < 0.02;
  const nodeWorld = {};
  for (const [name, n] of Object.entries(board.nodes)) nodeWorld[name] = [n[0], n[1]];
  const nodeAt = (w) => { for (const [name, p] of Object.entries(nodeWorld)) if (near(p, w)) return name; return null; };

  // 1. items and tracks in world space, as the schematic routed them
  const items = [], tracks = [];
  for (const g of board.geo || []) {
    const comp = g.comp, slot = g.slot;
    const type = comp ? comp.type : g.shape === "two" ? (slot.accepts || ["resistor"])[0] : g.shape === "opamp" ? "opamp" : (slot.accepts || ["npn"]).find((t) => /np|mos/.test(t)) || "npn";
    const lamp = comp ? isLamp(task, comp) : false;
    if (g.shape === "two") {
      const P = g.pts.map(toWorld);
      const L0 = P[g.leg], L1 = P[g.leg + 1];
      const legLen = Math.hypot(L1[0] - L0[0], L1[1] - L0[1]);
      const c = toWorld(g.center), d = g.dir;
      const [na, nb] = g.ends;
      if (comp && !slot && comp.type === "wire") { tracks.push({ pts: P, nets: [na, nb], flow: g.id, dir: 1, from: "node", to: "node", item: null }); continue; }
      const span = Math.max(0.2, Math.min(bodyHalf(type, lamp) * PART_SCALE + 0.12, legLen / 2 - 0.04));
      const a = [c[0] - d[0] * span, c[1] - d[1] * span], b = [c[0] + d[0] * span, c[1] + d[1] * span];
      const it = { shape: "two", id: g.id, comp, slot, type, lamp, center: c, dir: d, span, pins: [{ at: a, net: na }, { at: b, net: nb }] };
      items.push(it);
      tracks.push({ pts: [...P.slice(0, g.leg + 1), a], nets: [na, na], flow: g.id, dir: 1, from: "node", to: 0, item: it });
      tracks.push({ pts: [b, ...P.slice(g.leg + 1)], nets: [nb, nb], flow: g.id, dir: 1, from: 1, to: "node", item: it });
    } else if (g.shape === "three") {
      const wires = g.wires.map((w) => w.map(toWorld));
      const it = { shape: "three", id: g.id, comp, slot, type, center: toWorld(g.center), pins: g.legs.map((net, k) => ({ at: toWorld(g.pins[k]), net })) };
      items.push(it);
      // collector/drain into the part, base/gate into the part, emitter/source out of it
      tracks.push({ pts: wires[0], nets: [g.legs[0], g.legs[0]], flow: g.id, dir: 1, from: "node", to: 0, item: it });
      tracks.push({ pts: wires[1], nets: [g.legs[1], g.legs[1]], flow: `${g.id}.b`, dir: 1, from: "node", to: 1, item: it });
      tracks.push({ pts: wires[2], nets: [g.legs[2], g.legs[2]], flow: g.id, dir: 1, from: 2, to: "node", item: it });
    } else {
      const src = comp || slot;
      const wires = g.wires.map((w) => w.map(toWorld));
      const topNet = nodeAt(wires[0][0]) ?? src.minus, botNet = nodeAt(wires[1][0]) ?? src.plus;
      const topIsPlus = topNet === src.plus && topNet !== src.minus;
      const it = { shape: "opamp", id: g.id, comp, slot, type: "opamp", center: toWorld(g.center), topIsPlus,
        pins: [{ at: toWorld(g.pins[0]), net: topNet }, { at: toWorld(g.pins[1]), net: botNet }, { at: toWorld(g.pins[2]), net: src.out }] };
      items.push(it);
      tracks.push({ pts: wires[0], nets: [topNet, topNet], flow: null, dir: 1, from: "node", to: 0, item: it });
      tracks.push({ pts: wires[1], nets: [botNet, botNet], flow: null, dir: 1, from: "node", to: 1, item: it });
      tracks.push({ pts: wires[2], nets: [src.out, src.out], flow: g.id, dir: 1, from: 2, to: "node", item: it });
    }
  }

  // 2. the lattice: columns along x, modules of rails and two halves along y
  const pts = [];
  for (const it of items) { pts.push(it.center); it.pins.forEach((p) => pts.push(p.at)); }
  for (const t of tracks) t.pts.forEach((p) => pts.push(p));
  for (const name of Object.keys(board.uses || {})) if (nodeWorld[name]) pts.push(nodeWorld[name]);
  if (!pts.length) pts.push([0, 0], [4, 3]);
  const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
  const x0 = Math.min(...xs) - 0.55, x1 = Math.max(...xs) + 0.55;
  const y0 = Math.min(...ys) - 0.3, y1 = Math.max(...ys) + 0.3;
  const cols = Math.max(12, Math.round((x1 - x0) / PITCH) + 1);
  const colX = (i) => x0 + i * PITCH;
  // module offset: a channel under the first op-amp (a DIP must straddle it), else the − rail under ground
  const opamp = items.find((it) => it.shape === "opamp");
  const gnode = nodeWorld[ground] && (board.uses || {})[ground] ? nodeWorld[ground] : null;
  const height = (y1 - y0) / PITCH;
  const modules = Math.max(1, Math.ceil((height + 2) / T));
  let base = y0 - ((modules * T + 2 - height) / 2) * PITCH;
  const align = (target, rowInModule) => {
    const k = (target - base) / PITCH - rowInModule;
    base += (k - Math.round(k / T) * T) * PITCH;
  };
  if (opamp) align(opamp.center[1], CHANNEL);
  else if (gnode) align(gnode[1], RAILS[1]);
  // the modules that cover the circuit after the shift (one more pair of rails closes the last one)
  // (a module whose halves the circuit does not reach is left out; its rails still close the board)
  const first = Math.floor(((y0 - base) / PITCH + 1.5) / T);
  const last = Math.max(first, Math.floor(((y1 - base) / PITCH - 2.5) / T));
  const rowY = (m, r) => base + (m * T + r) * PITCH;

  const holes = [];
  const strips = new Map(); // strip id -> { net, rail, holes: [] }
  const addHole = (x, y, strip, rail) => {
    if (!strips.has(strip)) strips.set(strip, { id: strip, net: null, rail, holes: [] });
    const h = { x, y, strip, rail, used: false, index: holes.length };
    holes.push(h);
    strips.get(strip).holes.push(h);
    return h;
  };
  const channels = [];
  const rails = [];
  for (let m = first; m <= last + 1; m++) {
    RAILS.forEach((r, k) => {
      const y = rowY(m, r);
      rails.push({ y, sign: k === 0 ? "+" : "-", id: `r:${m}:${k}` });
      for (let i = 1; i < cols - 1; i++) if (i % 6 !== 0) addHole(colX(i), y, `r:${m}:${k}`, k === 0 ? "+" : "-");
    });
    if (m > last) break;
    channels.push(rowY(m, CHANNEL));
    for (let i = 1; i < cols - 1; i++) {
      for (const r of HALF_A) addHole(colX(i), rowY(m, r), `a:${m}:${i}`, null);
      for (const r of HALF_B) addHole(colX(i), rowY(m, r), `b:${m}:${i}`, null);
    }
  }
  const bounds = [colX(0) - PITCH * 0.6, colX(cols - 1) + PITCH * 0.6, rowY(first, 0) - PITCH * 1.1, rowY(last + 1, 1) + PITCH * 1.1];
  const holeKey = new Map(holes.map((h) => [`${Math.round(h.x / PITCH * 2)},${Math.round(h.y / PITCH * 2)}`, h]));
  const holeAt = (x, y) => holeKey.get(`${Math.round(x / PITCH * 2)},${Math.round(y / PITCH * 2)}`);

  // the + rails belong to the main supply (a source whose − is ground), the − rails to ground
  const supply = (task.board.fixed || []).find((c) => ["battery", "voltage_source", "pulse_source", "sine_source"].includes(c.type) && netOf(c.minus) === "GND");
  const supplyNet = supply ? netOf(supply.plus) : null;
  const allowed = (h, net) => {
    const s = strips.get(h.strip);
    if (s.net !== null) return s.net === net;
    if (h.rail === "-") return net === "GND";
    if (h.rail === "+") return supplyNet ? net === supplyNet : net !== "GND";
    return true;
  };
  const claim = (h, net) => { h.used = true; strips.get(h.strip).net = net; return h; };
  const nearest = (x, y, test) => {
    let best = null, bd = Infinity;
    for (const h of holes) {
      const d = (h.x - x) ** 2 + (h.y - y) ** 2;
      if (d < bd && test(h)) { bd = d; best = h; }
    }
    return best;
  };
  const findHole = (at, net, exclude = new Set()) => {
    const h = nearest(at[0], at[1], (q) => !q.used && allowed(q, net) && !exclude.has(q.strip))
      || nearest(at[0], at[1], (q) => !q.used) || holes[0];
    return claim(h, net);
  };

  // 3. op-amps first: a DIP-8 straddling the channel, pins 1-4 on the near row, 8-5 on the far row
  const nets = (n) => netOf(n);
  for (const it of items.filter((q) => q.shape === "opamp")) {
    const ch = channels.reduce((b, y) => (Math.abs(y - it.center[1]) < Math.abs(b - it.center[1]) ? y : b), channels[0]);
    const want = [nets(it.pins[it.topIsPlus ? 1 : 0].net), nets(it.pins[it.topIsPlus ? 0 : 1].net), nets(it.pins[2].net)]; // −in, +in, out
    let best = null;
    for (let i = 2; i < cols - 5; i++) {
      const x = colX(i);
      const near4 = [0, 1, 2, 3].map((k) => holeAt(x + k * PITCH, ch + PITCH));
      const far4 = [0, 1, 2, 3].map((k) => holeAt(x + k * PITCH, ch - PITCH));
      if ([...near4, ...far4].some((h) => !h || h.used || strips.get(h.strip).net !== null)) continue;
      const d = Math.abs(x + 1.5 * PITCH - it.center[0]);
      if (!best || d < best.d) best = { d, near4, far4, x };
    }
    if (!best) continue;
    const pinHole = [...best.near4, ...[...best.far4].reverse()]; // pin 1..8
    pinHole.forEach((h, k) => claim(h, `__nc:${it.id}:${k}`));
    const map = { 1: want[0], 2: want[1], 5: want[2] };
    for (const [k, net] of Object.entries(map)) strips.get(pinHole[k].strip).net = net;
    it.dip = { holes: pinHole, center: [best.x + 1.5 * PITCH, ch] };
    // pin order of it.pins is [top, bottom, out]; map onto DIP holes
    const minusHole = pinHole[1], plusHole = pinHole[2], outHole = pinHole[5];
    it.pins[0].hole = it.topIsPlus ? plusHole : minusHole;
    it.pins[1].hole = it.topIsPlus ? minusHole : plusHole;
    it.pins[2].hole = outHole;
  }

  // 4. transistors: TO-92, three legs in a row (E B C left to right, flat face to the viewer)
  for (const it of items.filter((q) => q.shape === "three")) {
    const [cNet, bNet, eNet] = it.pins.map((p) => nets(p.net));
    let best = null;
    for (const h of holes) {
      if (h.rail) continue;
      const row = [h, holeAt(h.x + PITCH, h.y), holeAt(h.x + 2 * PITCH, h.y)];
      if (row.some((q) => !q || q.used || q.rail)) continue;
      if (!allowed(row[0], eNet) || !allowed(row[1], bNet) || !allowed(row[2], cNet)) continue;
      const d = (h.x + PITCH - it.center[0]) ** 2 + (h.y - it.center[1]) ** 2;
      if (!best || d < best.d) best = { d, row };
    }
    if (!best) { it.pins.forEach((p) => { p.hole = findHole(p.at, nets(p.net)); }); continue; }
    claim(best.row[0], eNet); claim(best.row[1], bNet); claim(best.row[2], cNet);
    it.pins[0].hole = best.row[2]; it.pins[1].hole = best.row[1]; it.pins[2].hole = best.row[0];
    it.to92 = { center: [best.row[1].x, best.row[1].y] };
  }

  // 5. two-terminal parts: each leg in its own strip
  for (const it of items.filter((q) => q.shape === "two")) {
    const [pa, pb] = it.pins;
    pa.hole = findHole(pa.at, nets(pa.net));
    pb.hole = findHole(pb.at, nets(pb.net), nets(pa.net) === nets(pb.net) ? new Set() : new Set([pa.hole.strip]));
  }

  // 6. every node used by a wire gets a strip (ground prefers the − rail when one is close)
  const nodeStrip = {};
  const anchor = (name) => {
    if (nodeStrip[name]) return nodeStrip[name];
    const net = nets(name), at = nodeWorld[name] || [0, 0];
    let h = null;
    if (net === "GND") {
      const r = nearest(at[0], at[1], (q) => q.rail === "-" && allowed(q, net));
      if (r && Math.hypot(r.x - at[0], r.y - at[1]) < 0.9) h = r;
    }
    if (!h) {
      // a strip already holding this net (a leg) is the most natural place
      const own = nearest(at[0], at[1], (q) => strips.get(q.strip).net === net);
      if (own && Math.hypot(own.x - at[0], own.y - at[1]) < 0.35) h = own;
    }
    if (!h) h = nearest(at[0], at[1], (q) => !q.used && allowed(q, net)) || holes[0];
    strips.get(h.strip).net = net;
    nodeStrip[name] = h.strip;
    return h.strip;
  };

  // 7. jumpers: from a leg's strip (or a node's strip) to the other end's strip
  const wires = [];
  const freeIn = (strip, toward) => {
    const s = strips.get(strip);
    let best = null, bd = Infinity;
    for (const h of s.holes) { const d = (h.x - toward[0]) ** 2 + (h.y - toward[1]) ** 2; if (!h.used && d < bd) { bd = d; best = h; } }
    if (!best) for (const h of s.holes) { const d = (h.x - toward[0]) ** 2 + (h.y - toward[1]) ** 2; if (d < bd) { bd = d; best = h; } }
    if (best) best.used = true;
    return best;
  };
  for (const t of tracks) {
    const endStrip = (end, name) => (end === "node" ? anchor(name) : t.item.pins[end].hole.strip);
    const sa = endStrip(t.from, t.nets[0]), sb = endStrip(t.to, t.nets[1]);
    if (sa === sb) continue;
    const P = t.pts;
    const inner = P.slice(1, -1);
    const ha = freeIn(sa, P.length > 2 ? P[1] : P[P.length - 1]);
    const hb = freeIn(sb, P.length > 2 ? P[P.length - 2] : P[0]);
    if (!ha || !hb) continue;
    const net = nets(t.nets[0]);
    wires.push({ a: [ha.x, ha.y], b: [hb.x, hb.y], inner, net, flow: t.flow, dir: t.dir, item: t.item, track: t });
  }

  // nodes that only meet in a shared strip still get an anchor for their voltage tag
  const nodeTags = {};
  for (const name of Object.keys(board.uses || {})) {
    if (nets(name) === "GND" || !board.uses[name]) continue;
    const s = nodeStrip[name] ? strips.get(nodeStrip[name]) : [...strips.values()].find((q) => q.net === name);
    if (!s) continue;
    const at = nodeWorld[name] || [0, 0];
    const h = s.holes.reduce((b, q) => ((q.x - at[0]) ** 2 + (q.y - at[1]) ** 2 < (b.x - at[0]) ** 2 + (b.y - at[1]) ** 2 ? q : b), s.holes[0]);
    nodeTags[name] = [h.x, h.y];
  }

  return { supplyNet, items, wires, holes, strips, rails, channels, bounds, pitch: PITCH, nodeTags, netOf: nets, cols, colX };
}
