// The lesson strip on a task page: one card per task in the same phase (component icon, number,
// title, a tick when solved), plus the solved/total counter in the header.

import { iconSVG } from "./icons.js";

let index = null, current = null;

function solvedMap() { try { return JSON.parse(localStorage.getItem("efs-lab:solved") || "{}"); } catch { return {}; } }

export async function lessonStrip(taskId) {
  current = taskId;
  try {
    const res = await fetch("tasks/index.json");
    if (!res.ok) return;
    index = await res.json();
  } catch { return; }
  refreshStrip();
}

export function refreshStrip() {
  if (!index) return;
  const solved = solvedMap();
  const all = index.phases.flatMap((p) => p.tasks);
  const pill = document.querySelector("#progress-pill");
  if (pill) {
    const done = all.filter((t) => solved[t.id]).length;
    pill.hidden = false;
    pill.innerHTML = `<span class="pill-n"></span><span class="pill-of"></span>`;
    pill.firstChild.textContent = String(done);
    pill.lastChild.textContent = `/${all.length} solved`;
    pill.title = `${done} of ${all.length} lab tasks solved on this device`;
  }
  const host = document.querySelector("#lesson-strip");
  const phase = index.phases.find((p) => p.tasks.some((t) => t.id === current));
  if (!host || !phase) return;
  host.hidden = false;
  host.innerHTML = "";
  const head = document.createElement("div");
  head.className = "strip-head";
  const done = phase.tasks.filter((t) => solved[t.id]).length;
  head.innerHTML = `<span class="strip-phase"></span><span class="strip-count"></span>`;
  head.firstChild.textContent = phase.number === "ex" ? "Examples" : `Phase ${phase.number} · ${phase.title}`;
  head.lastChild.textContent = `${done}/${phase.tasks.length}`;
  const row = document.createElement("ol");
  row.className = "strip-row";
  phase.tasks.forEach((t, i) => {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.className = `strip-card${t.id === current ? " current" : ""}${solved[t.id] ? " solved" : ""}`;
    a.href = `task.html?t=${encodeURIComponent(t.id)}`;
    if (t.id === current) a.setAttribute("aria-current", "page");
    a.innerHTML = `${iconSVG(t.key || "resistor")}<span class="sc-num"></span><span class="sc-title"></span><span class="sc-tick" aria-hidden="true"></span>`;
    a.querySelector(".sc-num").textContent = String(i + 1).padStart(2, "0");
    a.querySelector(".sc-title").textContent = t.title;
    a.querySelector(".sc-tick").textContent = solved[t.id] ? "✓" : "";
    a.title = t.title + (solved[t.id] ? " (solved)" : "");
    li.append(a);
    row.append(li);
  });
  host.append(head, row);
  const cur = row.querySelector(".current");
  if (cur && row.scrollWidth > row.clientWidth) row.scrollLeft = Math.max(0, cur.parentElement.offsetLeft - 16);
}
