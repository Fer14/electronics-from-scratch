// Small illustrated component icons for the lesson strip and the index (48 × 48 SVG strings).
// Drawn in the lab's isometric style: dark outline, two or three flat tones, one highlight.

const O = `stroke="var(--iso-line)" stroke-width="1.3" stroke-linejoin="round" stroke-linecap="round"`;
const LEG = `stroke="var(--iso-metal2)" stroke-width="2" stroke-linecap="round" fill="none"`;

const ICONS = {
  resistor: `<path d="M6 30 L13 26 M35 18 L42 14" ${LEG}/>
    <path d="M12 22 l6-3.5 l4 1 l8-4.6 l4 1 l6 -3.4 v6 l-6 3.4 l-4 -1 l-8 4.6 l-4 -1 l-6 3.5 z" fill="var(--iso-resist0)" ${O}/>
    <path d="M16 20.2 v6 M19.5 19.6 v6 M23 18.5 v6 M31 14 v6" stroke="#7a4a27" stroke-width="2.2"/>
    <path d="M23 18.5 v6" stroke="#1b1b1b" stroke-width="2.2"/><path d="M31 14 v6" stroke="#c7a23f" stroke-width="2.2"/>`,
  led: `<path d="M20 34 v8 M28 34 v6" ${LEG}/>
    <path d="M14 33 a10 4 0 0 0 20 0 v-3 a10 4 0 0 0 -20 0 z" fill="#c8372d" ${O}/>
    <path d="M16 30 v-12 a8 8 0 0 1 16 0 v12 a8 3.2 0 0 1 -16 0 z" fill="#e2483d" ${O}/>
    <path d="M19.5 16 a4.5 4.5 0 0 1 4 -3.6" stroke="#fff" stroke-width="2" fill="none" opacity=".75"/>`,
  capacitor: `<path d="M21 37 v6 M27 37 v6" ${LEG}/>
    <path d="M14 12 v24 a10 4 0 0 0 20 0 v-24 z" fill="var(--sage)" ${O}/>
    <ellipse cx="24" cy="12" rx="10" ry="4" fill="var(--iso-metal1)" ${O}/>
    <path d="M18 16 v20" stroke="#fff" stroke-width="3" opacity=".55"/>`,
  inductor: `<path d="M5 30 l6-3 M37 18 l6-3" ${LEG}/>
    <path d="M11 27 l26 -13" stroke="var(--iso-dark1)" stroke-width="6" stroke-linecap="round"/>
    ${[0, 1, 2, 3, 4].map((k) => `<ellipse cx="${14 + k * 5.5}" cy="${25.5 - k * 2.75}" rx="2.6" ry="5" fill="var(--iso-copper1)" ${O}/>`).join("")}`,
  diode: `<path d="M5 31 l8-4 M35 17 l8-4" ${LEG}/>
    <path d="M12 23 l22 -11 a3 3 0 0 1 2 6 l-22 11 a3 3 0 0 1 -2 -6 z" fill="var(--iso-dark1)" ${O}/>
    <path d="M28 15 l2.5 -1.2 l2.5 5 l-2.5 1.2 z" fill="var(--iso-metal0)"/>`,
  switch: `<path d="M10 34 v6 M38 34 v6" ${LEG}/>
    <path d="M8 26 l16 -8 l16 8 l-16 8 z" fill="var(--iso-dark0)" ${O}/><path d="M8 26 v4 l16 8 v-4 z" fill="var(--iso-dark1)" ${O}/><path d="M24 34 v4 l16 -8 v-4 z" fill="var(--iso-dark2)" ${O}/>
    <path d="M15 26 L33 14" stroke="var(--iso-metal1)" stroke-width="3" stroke-linecap="round"/><rect x="31" y="10" width="6" height="5" rx="1" fill="var(--clay)" ${O}/>`,
  battery: `<path d="M38 30 c4 2 4 8 0 10 M34 32 c3 3 1 8 -2 9" stroke="#3b3537" stroke-width="2.4" fill="none" stroke-linecap="round"/>
    <path d="M38 30 c5 0 6 5 4 8" stroke="var(--clay)" stroke-width="2.4" fill="none" stroke-linecap="round"/>
    <path d="M6 24 l18 -9 l18 9 l-18 9 z" fill="var(--iso-dark0)" ${O}/><path d="M6 24 v6 l18 9 v-6 z" fill="var(--iso-dark1)" ${O}/><path d="M24 33 v6 l18 -9 v-6 z" fill="var(--iso-dark2)" ${O}/>
    <path d="M12 23 l14 -7 M18 26 l14 -7" stroke="var(--sand)" stroke-width="5" stroke-linecap="round"/>`,
  source: `<path d="M6 24 l18 -9 l18 9 l-18 9 z" fill="var(--iso-neutral0)" ${O}/><path d="M6 24 v8 l18 9 v-8 z" fill="var(--iso-neutral1)" ${O}/><path d="M24 33 v8 l18 -9 v-8 z" fill="var(--iso-neutral2)" ${O}/>
    <path d="M13 23 l9 -4.5 l7 3.5 l-9 4.5 z" fill="var(--iso-dark1)"/><path d="M15 22.5 q2 -3 4 -1 t4 -1" stroke="var(--sand)" stroke-width="1.4" fill="none"/>
    <ellipse cx="32" cy="25" rx="3" ry="1.6" fill="var(--clay)" ${O}/>`,
  npn: `<path d="M17 32 v10 M24 33 v10 M31 32 v10" ${LEG}/>
    <path d="M14 14 h20 v16 a10 4 0 0 1 -20 0 z" fill="var(--iso-dark1)" ${O}/><path d="M14 14 a10 4 0 0 0 20 0 a10 4 0 0 0 -20 0" fill="var(--iso-dark0)" ${O}/>
    <path d="M17 18 v10" stroke="#fff" stroke-width="1.6" opacity=".35"/>`,
  nmos: `<path d="M17 32 v10 M24 33 v10 M31 32 v10" ${LEG}/>
    <path d="M14 14 h20 v16 a10 4 0 0 1 -20 0 z" fill="var(--iso-dark1)" ${O}/><path d="M14 14 a10 4 0 0 0 20 0 a10 4 0 0 0 -20 0" fill="var(--iso-dark0)" ${O}/>
    <text x="24" y="27" text-anchor="middle" font-family="var(--mono)" font-size="7" fill="#fff" opacity=".7">FET</text>`,
  opamp: `${[0, 1, 2, 3].map((k) => `<path d="M${10 + k * 7} ${30 + k * -3.5} v5 M${17 + k * 7} ${37 + k * -3.5} v4" ${LEG}/>`).join("")}
    <path d="M8 24 l24 -12 l10 5 l-24 12 z" fill="var(--iso-dark0)" ${O}/><path d="M8 24 v5 l10 5 v-5 z" fill="var(--iso-dark1)" ${O}/><path d="M18 29 v5 l24 -12 v-5 z" fill="var(--iso-dark2)" ${O}/>
    <circle cx="14" cy="24.5" r="1.4" fill="#fff" opacity=".7"/><text x="25" y="23" font-family="var(--mono)" font-size="5.5" fill="#fff" opacity=".7" transform="rotate(-26 25 23)">741</text>`,
  lamp: `<path d="M20 40 v4 M28 40 v4" ${LEG}/>
    <path d="M18 30 h12 v8 a6 2.4 0 0 1 -12 0 z" fill="var(--iso-metal1)" ${O}/>
    <circle cx="24" cy="20" r="11" fill="#fff3c4" fill-opacity=".85" ${O}/><path d="M20 30 l1 -10 q3 -4 6 0 l1 10" stroke="#e0901a" stroke-width="1.4" fill="none"/>
    <path d="M17 16 a7 7 0 0 1 5 -4.5" stroke="#fff" stroke-width="2" fill="none"/>`,
  gate: `<path d="M5 18 h8 M5 30 h8 M37 24 h6" ${LEG}/>
    <path d="M12 12 h12 a12 12 0 0 1 0 24 h-12 z" fill="var(--iso-neutral0)" ${O}/><circle cx="18" cy="24" r="2" fill="var(--accent)"/>`,
  flipflop: `<path d="M5 18 h7 M5 30 h7 M36 18 h7" ${LEG}/>
    <rect x="12" y="10" width="24" height="28" rx="2" fill="var(--iso-neutral0)" ${O}/><path d="M12 26 l5 4 l-5 4" ${O} fill="none"/>
    <text x="17" y="21" font-family="var(--mono)" font-size="7" fill="var(--ink)">D</text><text x="27" y="21" font-family="var(--mono)" font-size="7" fill="var(--ink)">Q</text>`,
  chip: `${[0, 1, 2, 3, 4].map((k) => `<path d="M${13 + k * 5.5} 9 v-4 M${13 + k * 5.5} 43 v-4 M9 ${13 + k * 5.5} h-4 M43 ${13 + k * 5.5} h-4" ${LEG}/>`).join("")}
    <rect x="9" y="9" width="30" height="30" rx="3" fill="var(--iso-dark1)" ${O}/><rect x="16" y="16" width="16" height="16" rx="1.5" fill="var(--iso-accent1)" ${O}/>`,
};
ICONS.zener = ICONS.diode;
ICONS.pnp = ICONS.npn;
ICONS.pmos = ICONS.nmos;

export function iconSVG(key, cls = "comp-icon") {
  const body = ICONS[key] || ICONS.resistor;
  return `<svg class="${cls}" viewBox="0 0 48 48" aria-hidden="true">${body}</svg>`;
}
