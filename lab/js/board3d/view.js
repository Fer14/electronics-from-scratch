// Board 3D: the task's circuit built on a real (three.js) breadboard you can orbit, pan and zoom.
//
// Layout comes from layout.js (which reuses the schematic's routing), parts from parts.js. The view
// mirrors the schematic Board's API (render, showVoltages, showReadings, startFlow, stopFlow, setLevel,
// setTime, setState, relayout) so the task page drives all three views the same way.
//
// Performance: holes and current dots are instanced meshes, geometries are shared, there are two
// lights (one casts a soft shadow), and the canvas only redraws when something moves.

import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { partName, partValue } from "../ui/board.js";
import { eng } from "../sim/lab.js";
import { layoutBoard, PITCH, PART_SCALE } from "./layout.js";
import { Materials, readPalette, twoTerminal, to92, dip8, tubeAlong, setOutline, ghostify } from "./parts.js";

const BOARD_T = 0.3;
const reduceMotion = () => { try { return matchMedia("(prefers-reduced-motion: reduce)").matches; } catch { return false; } };

const TEACH = {
  resistor: "Resistor: it limits the current. Read its colour bands from the left: two digits, then the multiplier.",
  lamp: "Bulb: a thin filament that glows when it gets hot. Here it behaves like a resistor.",
  led: "LED: current flows one way only, from the long leg (anode, +) to the short leg. It glows brighter as the current grows.",
  capacitor: "Capacitor: it stores charge. Its voltage cannot jump; it changes as current flows in or out.",
  inductor: "Inductor: a coil of wire. It resists changes in the current through it.",
  diode: "Diode: current passes from the anode to the cathode, the end with the band.",
  zener: "Zener diode: used backwards, it holds about Vz across itself.",
  switch: "Switch: closed joins its two legs, open breaks the path.",
  battery: "Battery pack: the red lead is +, the black lead is −.",
  voltage_source: "Bench supply: holds a fixed voltage between its red (+) and black (−) leads.",
  pulse_source: "Pulse generator: flips between a low and a high voltage, again and again.",
  sine_source: "Signal generator: a smooth sine-wave voltage on its red lead.",
  current_source: "Current source: pushes a fixed current, whatever voltage that takes.",
  npn: "NPN transistor (TO-92, legs E B C): a small base current lets a much larger collector current flow.",
  pnp: "PNP transistor (TO-92, legs E B C): pull the base below the emitter and current flows from emitter to collector.",
  nmos: "N-MOSFET (TO-92, legs S G D): a gate voltage above Vth opens the drain–source channel.",
  pmos: "P-MOSFET (TO-92, legs S G D): pull the gate below the source to open the channel.",
  opamp: "Op-amp (DIP-8, across the channel): pin 2 is −, pin 3 is +, pin 6 is the output. The power pins 4 and 7 are left out here.",
  wire: "Jumper wire: joins two strips, so they become one node.",
  open: "Nothing connected: the two strips stay apart.",
  vcvs: "Controlled voltage source: its voltage follows another voltage in the circuit.",
  vccs: "Controlled current source: its current follows another voltage in the circuit.",
};

export class Board3D {
  constructor(host, task, board) {
    this.host = host;
    this.task = task;
    this.board = board;
    this.onSlot = null;
    this.opts = { labels: true, voltages: true };
    this.state = { volts: null, readings: null, levels: {}, time: null };
    this.running = false;
    this.dirty = true;
    this.host.classList.add("b3d-host");
    this.build();
  }

  build() {
    const host = this.host;
    host.innerHTML = "";
    this.canvasBox = document.createElement("div");
    this.canvasBox.className = "b3d-canvas";
    host.append(this.canvasBox);
    try {
      this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: "low-power" });
    } catch (e) {
      host.innerHTML = `<p class="b3d-fail">This browser cannot draw WebGL, so Board 3D is off. The Schematic and Iso views still work.</p>`;
      this.failed = true;
      return;
    }
    const r = this.renderer;
    r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    r.shadowMap.enabled = true;
    r.shadowMap.type = THREE.PCFSoftShadowMap;
    this.canvasBox.append(r.domElement);
    this.labelBox = document.createElement("div");
    this.labelBox.className = "b3d-labels";
    this.callout = document.createElement("div");
    this.callout.className = "b3d-callout";
    this.callout.hidden = true;
    const tools = document.createElement("div");
    tools.className = "b3d-tools";
    tools.innerHTML = `<button type="button" class="b3d-btn" data-act="reset" title="Reset the camera">reset view</button>
      <label class="b3d-check"><input type="checkbox" data-opt="labels" checked> labels</label>
      <label class="b3d-check"><input type="checkbox" data-opt="voltages" checked> voltages</label>`;
    tools.querySelector("[data-act=reset]").addEventListener("click", () => this.resetCamera());
    tools.querySelectorAll("input[data-opt]").forEach((c) => c.addEventListener("change", () => { this.opts[c.dataset.opt] = c.checked; this.applyOpts(); }));
    const corner = document.createElement("div");
    corner.className = "iso-corner br b3d-state";
    corner.innerHTML = `<span class="iso-key"></span><span class="iso-state"></span>`;
    this.stateText = corner.querySelector(".iso-state");
    const hint = document.createElement("div");
    hint.className = "iso-corner tl b3d-hint";
    hint.textContent = "drag to orbit · right-drag to pan · scroll to zoom";
    host.append(this.labelBox, this.callout, tools, corner, hint);

    this.pal = readPalette();
    this.mats = new Materials(this.pal);
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(34, 1, 0.05, 200);
    this.controls = new OrbitControls(this.camera, r.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.12;
    this.controls.maxPolarAngle = Math.PI / 2 - 0.08;
    this.controls.screenSpacePanning = true;
    this.controls.addEventListener("change", () => { this.dirty = true; this.camMoved = true; this.hideCallout(); });

    this.hemi = new THREE.HemisphereLight(0xffffff, 0xffffff, 1.9);
    this.sun = new THREE.DirectionalLight(0xffffff, 2.2);
    this.sun.castShadow = true;
    this.sun.shadow.mapSize.set(1024, 1024);
    this.sun.shadow.radius = 5;
    this.sun.shadow.bias = -0.0008;
    this.scene.add(this.hemi, this.sun, this.sun.target);

    this.ray = new THREE.Raycaster();
    this.pointer = new THREE.Vector2();
    this.events();
    try { new ResizeObserver(() => this.resize()).observe(host); } catch {}
    try {
      new MutationObserver(() => this.themeChanged()).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
      matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => this.themeChanged());
    } catch {}
    try { new IntersectionObserver((es) => { for (const e of es) this.onscreen = e.isIntersecting; if (this.onscreen) this.dirty = true; }).observe(host); } catch { this.onscreen = true; }
    this.onscreen = true;
    this.clock = performance.now();
    const loop = (now) => { this.frame(now); this.raf = requestAnimationFrame(loop); };
    this.raf = requestAnimationFrame(loop);
  }

  themeChanged() {
    if (this.failed) return;
    this.pal = readPalette();
    this.mats.apply(this.pal);
    if (this.lastChoice) this.relayout();
  }

  size() { return [Math.max(200, this.host.clientWidth), Math.max(200, this.canvasBox.clientHeight || 420)]; }

  resize() {
    if (this.failed || this.host.hidden || !this.host.clientWidth) return;
    const [w, h] = this.size();
    if (this.lastSize && this.lastSize[0] === w && this.lastSize[1] === h) return;
    this.lastSize = [w, h];
    this.renderer.setSize(w, h, false);
    this.renderer.domElement.style.width = "100%";
    this.renderer.domElement.style.height = "100%";
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    if (this.needFit) this.resetCamera();
    this.dirty = true; this.camMoved = true;
  }

  // ---------- scene ----------

  render(choice = {}, focus = null) {
    if (this.failed) return;
    this.stopFlow(true);
    this.lastChoice = choice;
    this.focus = focus;
    this.state = { volts: null, readings: null, levels: {}, time: null };
    const L = layoutBoard(this.task, this.board, choice);
    this.L = L;
    if (this.world) { this.scene.remove(this.world); disposeTree(this.world); }
    this.world = new THREE.Group();
    this.scene.add(this.world);
    const pal = this.pal;
    this.scene.background = new THREE.Color(pal.paper);
    this.hemi.color.set("#ffffff");
    this.hemi.groundColor.set(pal.wash);
    const boundsKey = L.bounds.map((v) => v.toFixed(2)).join(",");
    this.drawBoard(L);
    this.drawParts(L, choice, focus);
    this.drawWires(L);
    this.makeLabels(L);
    this.applyOpts();
    if (boundsKey !== this.boundsKey) { this.boundsKey = boundsKey; this.needFit = true; this.resetCamera(); }
    this.setState((this.task.board.slots || []).some((s) => !choice[s.id]) ? "pick a part, then a glowing slot" : "press RUN");
    this.dirty = true; this.camMoved = true;
  }

  relayout() {
    if (!this.lastChoice || this.failed) return;
    const st = this.state, flow = this.running && this.currentOf ? [this.currentOf, this.scale] : null;
    this.lastSize = null;
    this.resize();
    this.render(this.lastChoice, this.focus);
    if (st.volts) this.showVoltages(st.volts);
    if (st.readings) this.showReadings(st.readings);
    for (const [id, [i, p]] of Object.entries(st.levels)) this.setLevel(id, i, p);
    if (st.time !== null) this.setTime(st.time);
    if (flow) this.startFlow(...flow);
  }

  drawBoard(L) {
    const pal = this.pal, w = this.world;
    const [x0, x1, y0, y1] = L.bounds;
    const cx = (x0 + x1) / 2, cz = (y0 + y1) / 2;
    // paper ground with a faint technical grid
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({ color: pal.paper, roughness: 1 }));
    ground.rotation.x = -Math.PI / 2;
    ground.position.set(cx, -BOARD_T, cz);
    ground.receiveShadow = true;
    w.add(ground);
    const grid = new THREE.GridHelper(80, 160, pal.line, pal.line);
    grid.material.transparent = true;
    grid.material.opacity = 0.45;
    grid.position.set(Math.round(cx), -BOARD_T + 0.002, Math.round(cz));
    w.add(grid);
    // the slab
    const sideMat = new THREE.MeshStandardMaterial({ color: pal.board1, roughness: 0.9 });
    const topMat = new THREE.MeshStandardMaterial({ color: pal.board0, roughness: 0.85 });
    const slab = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0, BOARD_T, y1 - y0), [sideMat, sideMat, topMat, sideMat, sideMat, sideMat]);
    slab.position.set(cx, -BOARD_T / 2, cz);
    slab.castShadow = true;
    slab.receiveShadow = true;
    slab.userData.board = true;
    w.add(slab);
    this.slab = slab;
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(slab.geometry), this.mats.edges);
    slab.add(edges);
    // the centre channels and the rail stripes
    const groove = new THREE.MeshStandardMaterial({ color: pal.board2, roughness: 1 });
    for (const y of L.channels) {
      const g = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0 - 0.1, 0.004, PITCH * 0.7), groove);
      g.position.set(cx, 0.001, y);
      g.receiveShadow = true;
      w.add(g);
    }
    const plus = new THREE.MeshBasicMaterial({ color: pal.clay }), minus = new THREE.MeshBasicMaterial({ color: pal.ink });
    for (const r of L.rails) {
      const s = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0 - 0.35, 0.003, 0.018), r.sign === "+" ? plus : minus);
      s.position.set(cx, 0.002, r.y + (r.sign === "+" ? -0.55 : 0.55) * PITCH);
      w.add(s);
    }
    // the holes (one instanced mesh), tinted toward ink so they read as openings
    const holeColor = new THREE.Color(pal.board0).lerp(new THREE.Color(pal.ink), 0.72);
    const holeGeo = new THREE.BoxGeometry(PITCH * 0.36, 0.004, PITCH * 0.36);
    const holes = new THREE.InstancedMesh(holeGeo, new THREE.MeshBasicMaterial({ color: holeColor }), L.holes.length);
    const m = new THREE.Matrix4();
    L.holes.forEach((h, i) => { m.makeTranslation(h.x, 0.0015, h.y); holes.setMatrixAt(i, m); });
    holes.instanceMatrix.needsUpdate = true;
    w.add(holes);
    // the strip highlight (shown on hover), and the shadow camera fitted to the board
    this.stripGlow = new THREE.Mesh(new THREE.BoxGeometry(1, 0.01, 1), new THREE.MeshBasicMaterial({ color: pal.accent, transparent: true, opacity: 0.38, depthWrite: false }));
    this.stripGlow.visible = false;
    w.add(this.stripGlow);
    const span = Math.max(x1 - x0, y1 - y0);
    this.sun.position.set(cx - span * 0.35, span * 1.3, cz + span * 0.55);
    this.sun.target.position.set(cx, 0, cz);
    const sc = this.sun.shadow.camera;
    sc.left = -span * 0.9; sc.right = span * 0.9; sc.top = span * 0.9; sc.bottom = -span * 0.9; sc.near = 0.1; sc.far = span * 4;
    sc.updateProjectionMatrix();
    this.center = new THREE.Vector3(cx, 0, cz);
    this.span = [x1 - x0, y1 - y0];
  }

  netColor(net) {
    const pal = this.pal;
    if (!this.netColors) this.netColors = {};
    if (net === "GND") return "#3b3537";
    if (net === this.supplyNet) return pal.clay;
    if (!(net in this.netColors)) {
      const cycle = [pal.sage, pal.sand, pal.tint, "#6f8aa0", pal.copper, pal.muted];
      this.netColors[net] = cycle[Object.keys(this.netColors).length % cycle.length];
    }
    return this.netColors[net];
  }

  drawParts(L, choice, focus) {
    const mats = this.mats, w = this.world;
    this.supplyNet = L.supplyNet;
    this.netColors = {};
    const wireMats = { plus: mats.wire(this.pal.clay), minus: mats.wire("#3b3537"), jumper: mats.wire(this.pal.sage) };
    this.items = [];
    this.pickables = [];
    this.handles = {};
    this.ghosts = [];
    const fills = (this.task.board.slots || []).filter((s) => choice[s.id]).map((s) => s.id);
    const accentId = focus && choice[focus] ? focus : fills.length ? fills[fills.length - 1] : null;
    for (const it of L.items) {
      let group = null;
      const comp = it.comp;
      if (it.shape === "two") {
        const [ha, hb] = it.pins.map((p) => p.hole);
        if (!ha || !hb) continue;
        const dx = hb.x - ha.x, dz = hb.y - ha.y;
        const half = Math.max(0.12, Math.hypot(dx, dz) / 2);
        const type = comp ? comp.type : it.type;
        const K = type === "wire" || type === "open" ? 1 : PART_SCALE;
        group = twoTerminal(type, mats, half / K, comp, { lamp: it.lamp, wireMats });
        group.scale.setScalar(K);
        group.position.set((ha.x + hb.x) / 2, 0, (ha.y + hb.y) / 2);
        group.rotation.y = -Math.atan2(dz, dx);
      } else if (it.shape === "three") {
        group = to92(mats, PITCH / 1.4);
        group.scale.setScalar(1.4);
        const c = it.to92 ? it.to92.center : it.center;
        group.position.set(c[0], 0, c[1]);
      } else if (it.dip) {
        group = dip8(mats, it.dip.holes.map((h) => [h.x, h.y]), it.dip.center);
        group.position.set(it.dip.center[0], 0, it.dip.center[1]);
      }
      if (!group) continue;
      if (comp) setOutline(group, mats, !!it.slot && it.id === accentId);
      else { ghostify(group, mats); this.ghosts.push(group); }
      w.add(group);
      group.updateMatrixWorld(true);
      const box = new THREE.Box3().setFromObject(group);
      if (!comp) box.expandByVector(new THREE.Vector3(0.04, 0.06, 0.04));
      const size = box.getSize(new THREE.Vector3()), mid = box.getCenter(new THREE.Vector3());
      const hit = new THREE.Mesh(new THREE.BoxGeometry(Math.max(size.x, 0.3) + 0.08, Math.max(size.y, 0.12) + 0.04, Math.max(size.z, 0.3) + 0.08), new THREE.MeshBasicMaterial({ visible: false }));
      hit.position.copy(mid);
      hit.userData.item = it;
      w.add(hit);
      this.pickables.push(hit);
      const record = { it, group, box, top: new THREE.Vector3(mid.x, box.max.y, mid.z) };
      this.items.push(record);
      if (comp && group.userData.glow) this.handles[it.id] = group.userData.glow;
      if (comp && group.userData.setClosed) this.handles[it.id] = { setClosed: group.userData.setClosed, closed: comp.closed !== false };
      if (!comp) {
        // the empty slot's holes glow
        const ring = new THREE.RingGeometry(0.055, 0.085, 18).rotateX(-Math.PI / 2);
        const mat = new THREE.MeshBasicMaterial({ color: this.pal.accent, transparent: true, opacity: 0.9, depthWrite: false });
        for (const p of it.pins) if (p.hole) { const r = new THREE.Mesh(ring, mat); r.position.set(p.hole.x, 0.006, p.hole.y); w.add(r); }
        group.userData.ringMat = mat;
      }
    }
  }

  drawWires(L) {
    this.wires = [];
    const tiers = [0.1, 0.17, 0.24];
    L.wires.forEach((wr, k) => {
      const color = this.netColor(wr.net);
      const a = new THREE.Vector3(wr.a[0], -0.06, wr.a[1]), b = new THREE.Vector3(wr.b[0], -0.06, wr.b[1]);
      const flat = Math.hypot(wr.a[0] - wr.b[0], wr.a[1] - wr.b[1]);
      let pts;
      if (wr.inner.length) {
        const h = tiers[k % 3] + 0.06 * (wr.net === "GND" ? 0 : 1);
        pts = [a, new THREE.Vector3(a.x, h, a.z), ...wr.inner.map((p) => new THREE.Vector3(p[0], h, p[1])), new THREE.Vector3(b.x, h, b.z), b];
        pts = pts.filter((p, i) => i === 0 || p.distanceTo(pts[i - 1]) > 0.02);
      } else {
        const h = Math.min(0.55, 0.12 + flat * 0.16) + 0.04 * (k % 3);
        pts = [];
        for (let i = 0; i <= 16; i++) {
          const t = i / 16;
          const p = a.clone().lerp(b, t);
          p.y = -0.06 + (h + 0.06) * Math.sin(Math.PI * Math.min(1, Math.max(0, (t - 0.0) / 1))) ** 0.7;
          pts.push(p);
        }
        pts[0] = a; pts[16] = b;
        pts.splice(1, 0, new THREE.Vector3(a.x, 0.03, a.z));
        pts.splice(pts.length - 1, 0, new THREE.Vector3(b.x, 0.03, b.z));
      }
      const tube = tubeAlong(pts, 0.042, this.mats.wire(color), { radial: 7, round: wr.inner.length ? 0.09 : 0.02 });
      this.world.add(tube);
      const curve = tube.userData.curve;
      const len = curve.getLength();
      const samples = curve.getSpacedPoints(Math.max(8, Math.round(len * 24)));
      this.wires.push({ wr, tube, len, samples });
    });
  }

  // ---------- labels ----------

  makeLabels(L) {
    const box = this.labelBox;
    box.innerHTML = "";
    this.labels = [];
    for (const rec of this.items) {
      const it = rec.it, comp = it.comp;
      if (comp && !it.slot && comp.type === "wire") continue;
      const el = document.createElement(it.slot ? "button" : "div");
      el.className = `b3d-label${it.slot ? " slot" : ""}${comp ? "" : " empty"}`;
      if (it.slot) {
        el.type = "button";
        el.dataset.slot = it.slot.id;
        el.setAttribute("aria-label", comp ? `slot ${it.id}, holds ${partName(comp)} ${partValue(comp)}; activate to empty` : `slot ${it.id}, empty; accepts ${(it.slot.accepts || []).join(", ")}`);
        el.addEventListener("click", () => this.onSlot && this.onSlot(it.slot.id));
      }
      const title = comp ? `${it.id}  ${it.lamp ? "bulb " : ""}${partValue(comp) || partName(comp)}` : `${it.id}  ?`;
      el.innerHTML = `<span class="t"></span><span class="r"></span>`;
      el.firstChild.textContent = title;
      box.append(el);
      this.labels.push({ el, rec, reading: el.lastChild, kind: "part" });
    }
    this.nodeTags = {};
    for (const [name, at] of Object.entries(L.nodeTags)) {
      const el = document.createElement("div");
      el.className = "b3d-node";
      box.append(el);
      this.nodeTags[name] = { el, at: new THREE.Vector3(at[0], 0.02, at[1]) };
    }
  }

  applyOpts() {
    this.labelBox.classList.toggle("no-labels", !this.opts.labels);
    this.labelBox.classList.toggle("no-volts", !this.opts.voltages);
    this.camMoved = true; this.dirty = true;
  }

  project(v) {
    const [w, h] = this.size();
    const p = v.clone().project(this.camera);
    return [(p.x * 0.5 + 0.5) * w, (-p.y * 0.5 + 0.5) * h, p.z];
  }

  screenBox(box) {
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) {
      const [sx, sy] = this.project(new THREE.Vector3(x, y, z));
      x0 = Math.min(x0, sx); y0 = Math.min(y0, sy); x1 = Math.max(x1, sx); y1 = Math.max(y1, sy);
    }
    return [x0, y0, x1, y1];
  }

  // Labels sit beside their part, never on it: right, left, above or below, whichever is free.
  placeLabels() {
    if (!this.labels) return;
    const [W, H] = this.size();
    const taken = this.items.map((r) => this.screenBox(r.box));
    const hits = (b) => taken.some((o) => b[0] < o[2] && b[2] > o[0] && b[1] < o[3] && b[3] > o[1]);
    const order = [...this.labels].sort((a, b) => (a.rec.it.slot ? 0 : 1) - (b.rec.it.slot ? 0 : 1));
    for (const lab of order) {
      const el = lab.el;
      const sb = this.screenBox(lab.rec.box);
      const w = el.offsetWidth || 90, h = el.offsetHeight || 30;
      const cy = (sb[1] + sb[3]) / 2, cx = (sb[0] + sb[2]) / 2;
      const spots = [[sb[2] + 6, cy - h / 2], [sb[0] - 6 - w, cy - h / 2], [cx - w / 2, sb[1] - 4 - h], [cx - w / 2, sb[3] + 4],
        [sb[2] + 6, sb[1] - h], [sb[0] - 6 - w, sb[3]], [sb[2] + 26, cy - h / 2], [sb[0] - 26 - w, cy - h / 2]];
      const inside = (s) => s[0] >= 2 && s[1] >= 2 && s[0] + w <= W - 2 && s[1] + h <= H - 2;
      const pick = spots.find((s) => inside(s) && !hits([s[0], s[1], s[0] + w, s[1] + h])) || spots.find(inside) || spots[0];
      const behind = this.project(lab.rec.top)[2] > 1;
      el.style.transform = `translate(${Math.round(pick[0])}px, ${Math.round(pick[1])}px)`;
      el.style.visibility = behind ? "hidden" : "visible";
      taken.push([pick[0], pick[1], pick[0] + w, pick[1] + h]);
    }
    for (const tag of Object.values(this.nodeTags || {})) {
      if (!tag.el.textContent) continue;
      const [sx, sy] = this.project(tag.at);
      const w = tag.el.offsetWidth || 60, h = tag.el.offsetHeight || 16;
      const spots = [[sx + 6, sy - h - 2], [sx - w - 6, sy - h - 2], [sx + 6, sy + 4], [sx - w - 6, sy + 4]];
      const pick = spots.find((s) => !hits([s[0], s[1], s[0] + w, s[1] + h]));
      tag.el.style.visibility = pick ? "visible" : "hidden";
      if (!pick) continue;
      taken.push([pick[0], pick[1], pick[0] + w, pick[1] + h]);
      tag.el.style.transform = `translate(${Math.round(pick[0])}px, ${Math.round(pick[1])}px)`;
    }
  }

  // ---------- camera ----------

  resetCamera() {
    if (!this.center) return;
    const [w, h] = this.size();
    this.camera.aspect = w / h;
    const [sx, sz] = this.span;
    const dir = new THREE.Vector3(-0.22, 0.82, 1).normalize();
    const corners = [];
    for (const x of [-sx / 2, sx / 2]) for (const y of [-BOARD_T, 0.5]) for (const z of [-sz / 2, sz / 2]) corners.push(new THREE.Vector3(x, y, z).add(this.center));
    // move along the view direction until the board's corners fill about 92 % of the canvas, and
    // slide sideways so their projected box is centred (perspective makes the near edge bigger)
    let dist = Math.max(sx, sz) * 1.6;
    const target = this.center.clone();
    for (let k = 0; k < 8; k++) {
      this.camera.position.copy(target).addScaledVector(dir, dist);
      this.camera.lookAt(target);
      this.camera.updateMatrixWorld();
      this.camera.updateProjectionMatrix();
      let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
      for (const c of corners) { const p = c.clone().project(this.camera); x0 = Math.min(x0, p.x); x1 = Math.max(x1, p.x); y0 = Math.min(y0, p.y); y1 = Math.max(y1, p.y); }
      const mid = target.clone().project(this.camera);
      const shifted = new THREE.Vector3((x0 + x1) / 2, (y0 + y1) / 2, mid.z).unproject(this.camera);
      const flat = shifted.sub(target);
      flat.y = 0;
      target.add(flat.multiplyScalar(0.9));
      const ext = Math.max((x1 - x0) / 2, (y1 - y0) / 2 / 0.94);
      dist *= Math.max(0.6, Math.min(1.6, ext / 0.9));
    }
    this.camera.position.copy(target).addScaledVector(dir, dist);
    this.controls.target.copy(target);
    this.controls.minDistance = 1.2;
    this.controls.maxDistance = dist * 3;
    this.camera.near = 0.05; this.camera.far = dist * 10;
    this.camera.updateProjectionMatrix();
    this.controls.update();
    this.needFit = !this.host.clientWidth;
    this.dirty = true; this.camMoved = true;
  }

  // ---------- picking, hover callouts and drops ----------

  events() {
    const c = this.renderer.domElement;
    let down = null;
    c.addEventListener("pointerdown", (e) => { down = [e.clientX, e.clientY]; });
    c.addEventListener("pointerup", (e) => {
      if (!down || e.button !== 0) { down = null; return; }
      const moved = Math.hypot(e.clientX - down[0], e.clientY - down[1]);
      down = null;
      if (moved > 5) return;
      const it = this.pickItem(e.clientX, e.clientY);
      if (it && it.slot && this.onSlot) this.onSlot(it.slot.id);
    });
    let pending = false, last = null;
    c.addEventListener("pointermove", (e) => {
      last = e;
      if (pending || (e.buttons && down)) return;
      pending = true;
      requestAnimationFrame(() => { pending = false; if (last) this.hover(last.clientX, last.clientY); });
    });
    c.addEventListener("pointerleave", () => { last = null; this.hideCallout(); this.renderer.domElement.style.cursor = ""; });
  }

  setPointer(x, y) {
    const r = this.renderer.domElement.getBoundingClientRect();
    if (x < r.left || x > r.right || y < r.top || y > r.bottom) return false;
    this.pointer.set(((x - r.left) / r.width) * 2 - 1, -((y - r.top) / r.height) * 2 + 1);
    this.ray.setFromCamera(this.pointer, this.camera);
    return true;
  }

  pickItem(x, y) {
    if (this.failed || !this.setPointer(x, y)) return null;
    const hit = this.ray.intersectObjects(this.pickables || [], false)[0];
    return hit ? hit.object.userData.item : null;
  }

  // For the tray's drag and drop: the slot under a screen point, if any.
  slotAt(x, y) {
    const it = this.pickItem(x, y);
    return it && it.slot ? it.slot.id : null;
  }

  hover(x, y) {
    if (this.failed || !this.setPointer(x, y)) return;
    const hits = this.ray.intersectObjects([...(this.pickables || []), this.slab].filter(Boolean), false);
    const hit = hits[0];
    const r = this.renderer.domElement.getBoundingClientRect();
    if (!hit) { this.hideCallout(); return; }
    const it = hit.object.userData.item;
    this.renderer.domElement.style.cursor = it && it.slot ? "pointer" : "";
    if (it) {
      this.stripGlow.visible = false;
      this.showCallout(this.teach(it), x - r.left, y - r.top, it.comp ? null : "empty");
      this.dirty = true;
      return;
    }
    // the breadboard itself: light up the strip under the pointer and say what it is
    const p = hit.point;
    const L = this.L;
    let best = null, bd = (PITCH * 0.7) ** 2;
    for (const h of L.holes) { const d = (h.x - p.x) ** 2 + (h.y - p.z) ** 2; if (d < bd) { bd = d; best = h; } }
    if (!best) {
      const onChannel = L.channels.some((cy) => Math.abs(cy - p.z) < PITCH * 0.6);
      this.stripGlow.visible = false;
      this.dirty = true;
      if (onChannel) this.showCallout("Centre channel: it splits the two halves, so a chip can sit across it with each leg in its own strip.", x - r.left, y - r.top);
      else this.hideCallout();
      return;
    }
    const strip = L.strips.get(best.strip);
    const xs = strip.holes.map((h) => h.x), ys = strip.holes.map((h) => h.y);
    const gx0 = Math.min(...xs), gx1 = Math.max(...xs), gy0 = Math.min(...ys), gy1 = Math.max(...ys);
    this.stripGlow.scale.set(gx1 - gx0 + PITCH * 0.7, 1, gy1 - gy0 + PITCH * 0.7);
    this.stripGlow.position.set((gx0 + gx1) / 2, 0.006, (gy0 + gy1) / 2);
    this.stripGlow.visible = true;
    this.dirty = true;
    const net = strip.net && !strip.net.startsWith("__nc") ? strip.net : null;
    const volts = !net || !this.state.volts ? undefined : net === "GND" ? 0 : this.state.volts[net];
    const netText = net ? ` This one is node ${net === "GND" ? "ground (0 V)" : net}${Number.isFinite(volts) ? ` at ${eng(volts, "V")}` : ""}.` : " Nothing uses this one.";
    const text = strip.rail ? `Power rail (${strip.rail === "+" ? "+, red line" : "−, dark line"}): every hole along this line is connected underneath.${netText}`
      : `Breadboard: the five holes in each short row are connected underneath.${netText}`;
    this.showCallout(text, x - r.left, y - r.top);
  }

  teach(it) {
    const comp = it.comp;
    if (!comp) {
      const acc = (it.slot.accepts || []).map((t) => partName({ type: t }));
      return `Empty slot ${it.id}: put ${acc.length ? acc.join(" or ") : "a part"} here. Pick it in the Parts panel, then click this slot or drag the part onto it.`;
    }
    const key = it.lamp ? "lamp" : comp.type;
    const base = TEACH[key] || partName(comp);
    const val = partValue(comp);
    return `${it.id}${val ? ` · ${val}` : ""}. ${base}`;
  }

  showCallout(text, x, y, kind = null) {
    const c = this.callout;
    c.textContent = text;
    c.classList.toggle("empty", kind === "empty");
    c.hidden = false;
    const [W] = this.size();
    const w = c.offsetWidth, h = c.offsetHeight;
    let left = x + 16, top = y + 14;
    if (left + w > W - 6) left = Math.max(6, x - w - 16);
    if (top + h > this.canvasBox.clientHeight - 6) top = Math.max(6, y - h - 14);
    c.style.transform = `translate(${Math.round(left)}px, ${Math.round(top)}px)`;
  }

  hideCallout() {
    if (this.callout) this.callout.hidden = true;
    if (this.stripGlow && this.stripGlow.visible) { this.stripGlow.visible = false; this.dirty = true; }
  }

  // ---------- state shown after RUN ----------

  setState(msg) { if (this.stateText) this.stateText.textContent = msg; }

  showVoltages(volts) {
    this.state.volts = volts;
    for (const [name, tag] of Object.entries(this.nodeTags || {})) {
      const v = volts && volts[name];
      tag.el.textContent = Number.isFinite(v) ? `${name} ${eng(Math.abs(v) < 1e-9 ? 0 : v, "V")}` : "";
    }
    this.camMoved = true; this.dirty = true;
  }

  showReadings(readings) {
    this.state.readings = readings;
    for (const lab of this.labels || []) lab.reading.textContent = readings && readings[lab.rec.it.id] ? readings[lab.rec.it.id] : "";
    this.camMoved = true; this.dirty = true;
  }

  setLit() {}

  // An LED is full at about 15 mA, a bulb at about 1.5 W.
  setLevel(id, amps, watts) {
    this.state.levels[id] = [amps, watts];
    const h = this.handles && this.handles[id];
    if (!h || !h.kind) return;
    let b = 0;
    if (h.kind === "led") b = amps > 1e-4 ? Math.min(1, Math.sqrt(amps / 0.015)) : 0;
    else b = Math.abs(watts) > 0.01 ? Math.min(1, Math.sqrt(Math.abs(watts) / 1.5)) : 0;
    if (h.kind === "led") { h.mats[0].emissiveIntensity = 2.2 * b; h.halo.material.opacity = 0.85 * b; }
    else { h.mats[0].emissiveIntensity = 1.1 * b; h.mats[0].opacity = 0.45 + 0.4 * b; h.mats[1].emissiveIntensity = 4 * b; h.halo.material.opacity = 0.9 * b; }
    this.dirty = true;
  }

  setTime(t) {
    this.state.time = t;
    for (const rec of this.items || []) {
      const c = rec.it.comp;
      if (!c || c.type !== "switch" || !(c.toggle_at || []).length) continue;
      const flips = c.toggle_at.filter((x) => x <= t).length;
      const closed = (c.closed !== false) !== (flips % 2 === 1);
      const h = this.handles[rec.it.id];
      if (h && h.setClosed && h.closed !== closed) { h.closed = closed; h.setClosed(closed); this.dirty = true; }
    }
  }

  // Current dots ride along every jumper; their speed follows the current through it.
  startFlow(currentOf, scale) {
    if (this.failed) return;
    this.stopFlow(true);
    this.currentOf = currentOf;
    this.scale = scale;
    this.running = true;
    this.setState("current flowing · dots move with I");
    const flows = new Map(this.board.flows.map((f) => [f.id, f]));
    const gap = 0.34;
    let total = 0;
    this.dotWires = this.wires.map((w) => {
      const f = w.wr.flow ? flows.get(w.wr.flow) : null;
      const count = f ? Math.max(1, Math.floor(w.len / gap)) : 0;
      total += count;
      return { w, f, count, gap: w.len / Math.max(1, count), phase: Math.random() * gap };
    });
    if (this.dots) { this.world.remove(this.dots); this.dots.geometry.dispose(); }
    if (!total) return;
    const geom = new THREE.SphereGeometry(0.058, 10, 8);
    this.dots = new THREE.InstancedMesh(geom, new THREE.MeshBasicMaterial({ color: this.pal.accent }), total);
    this.dots.frustumCulled = false;
    this.world.add(this.dots);
    this.dirty = true;
  }

  stopFlow(keepState = false) {
    this.running = false;
    if (this.dots && this.world) { this.world.remove(this.dots); this.dots.geometry.dispose(); this.dots = null; }
    if (!keepState) this.currentOf = null;
    this.dirty = true;
  }

  stepDots(dt) {
    if (!this.dots) return;
    const m = new THREE.Matrix4(), hidden = new THREE.Matrix4().makeScale(0, 0, 0);
    let k = 0;
    for (const d of this.dotWires) {
      if (!d.count) continue;
      const amps = (this.currentOf ? this.currentOf(d.f) || 0 : 0) * d.f.sign * d.w.wr.dir;
      const visible = Math.abs(amps) > this.scale * 1e-3 && Math.abs(amps) > 1e-12;
      const speed = this.scale > 0 ? (1.3 * amps) / this.scale : 0;
      d.phase = (((d.phase + speed * dt) % d.gap) + d.gap) % d.gap;
      const S = d.w.samples, n = S.length - 1;
      for (let j = 0; j < d.count; j++, k++) {
        if (!visible) { this.dots.setMatrixAt(k, hidden); continue; }
        const s = ((j * d.gap + d.phase) % d.w.len) / d.w.len * n;
        const i = Math.min(n - 1, Math.floor(s)), f = s - i;
        const p = S[i], q = S[i + 1];
        m.makeTranslation(p.x + (q.x - p.x) * f, p.y + (q.y - p.y) * f, p.z + (q.z - p.z) * f);
        this.dots.setMatrixAt(k, m);
      }
    }
    this.dots.instanceMatrix.needsUpdate = true;
  }

  // ---------- the frame loop: redraw only when something changed or moves ----------

  frame(now) {
    const dt = Math.min(0.05, (now - this.clock) / 1000);
    this.clock = now;
    if (this.failed || this.host.hidden || !this.onscreen || document.hidden || !this.world) return;
    if (!this.lastSize || this.lastSize[0] !== Math.max(200, this.host.clientWidth)) this.resize();
    if (this.controls.update()) this.dirty = true;
    const still = reduceMotion();
    if (this.ghosts.length && !still) {
      const t = now / 1000;
      for (const g of this.ghosts) g.position.y = 0.05 + 0.035 * Math.sin(t * 2.2);
      for (const g of this.ghosts) if (g.userData.ringMat) g.userData.ringMat.opacity = 0.55 + 0.4 * Math.sin(t * 3);
      this.dirty = true;
    }
    if (this.running && this.dots) { this.stepDots(still ? 0 : dt); this.dirty = true; }
    if (!this.dirty) return;
    this.dirty = false;
    this.renderer.render(this.scene, this.camera);
    if (this.camMoved) { this.camMoved = false; this.placeLabels(); }
  }
}

// Free what this render made; shared geometries (parts.js cache) and palette materials stay.
function disposeTree(root) {
  root.traverse((o) => {
    if (o.geometry && !o.geometry.userData.cached) o.geometry.dispose();
    const mats = Array.isArray(o.material) ? o.material : o.material ? [o.material] : [];
    for (const m of mats) if (!m.userData.keep) m.dispose();
  });
}
