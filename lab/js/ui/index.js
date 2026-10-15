// The lab index: tasks grouped by phase, read from tasks/index.json.

const KIND = { dc: "DC", transient: "transient", ac: "AC", logic: "logic", chip: "chip" };

function solvedMap() { try { return JSON.parse(localStorage.getItem("efs-lab:solved") || "{}"); } catch { return {}; } }

async function main() {
  const host = document.querySelector("#phases");
  let index;
  try {
    const res = await fetch("tasks/index.json");
    index = await res.json();
  } catch {
    host.textContent = "No task list yet: run uv run python scripts/build_lab.py";
    return;
  }
  const solved = solvedMap();
  let total = 0, done = 0;
  for (const phase of index.phases) {
    const section = document.createElement("section");
    section.className = "phase";
    const h = document.createElement("h2");
    h.innerHTML = `<span class="num"></span><span class="pt"></span>`;
    h.firstChild.textContent = phase.number;
    h.lastChild.textContent = phase.title;
    section.append(h);
    const list = document.createElement("ul");
    list.className = "task-list";
    for (const t of phase.tasks) {
      total++;
      if (solved[t.id]) done++;
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = `task.html?t=${encodeURIComponent(t.id)}`;
      a.className = solved[t.id] ? "task-link solved" : "task-link";
      a.innerHTML = `<span class="tick" aria-hidden="true"></span><span class="tt"></span><span class="kind"></span>`;
      a.querySelector(".tick").textContent = solved[t.id] ? "✓" : "○";
      a.querySelector(".tt").textContent = t.title;
      a.querySelector(".kind").textContent = KIND[t.kind] || t.kind;
      if (t.lesson) a.title = t.lesson;
      li.append(a);
      list.append(li);
    }
    section.append(list);
    host.append(section);
  }
  document.querySelector("#progress").textContent = `${done} of ${total} tasks solved on this device.`;
}

main();
