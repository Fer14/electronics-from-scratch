"""Collect every lab task into the web lab.

    uv run python scripts/build_lab.py

Copies phases/*/*/lab/task.json and lab/examples/*/task.json to lab/tasks/<id>.json and
writes lab/tasks/index.json (tasks grouped by phase) for the lab's index page. Invalid
files are reported and skipped; the exit code is 1 if any were skipped.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "lab" / "tasks"
REQUIRED = ("id", "title", "kind", "board", "parts", "goals")


def phase_title(phase_dir):
    readme = phase_dir / "README.md"
    if readme.exists():
        match = re.search(r"^#\s*Phase\s*\d+\s*[:\-–]\s*(.+)$", readme.read_text(), re.M)
        if match:
            return match.group(1).strip()
    return phase_dir.name.split("-", 1)[1].replace("-", " ").capitalize()


KEY_ORDER = ["led", "opamp", "npn", "pnp", "nmos", "pmos", "zener", "diode", "inductor", "capacitor"]
KEY_ALIAS = {"pnp": "npn", "pmos": "nmos", "zener": "diode"}


def key_part(task):
    """The component a task is about, for its icon in the lab's lesson strip."""
    if task["kind"] == "logic":
        return "flipflop" if any(c.get("type") == "dff" for c in task["board"].get("fixed", [])) else "gate"
    if task["kind"] == "chip":
        return "chip"
    comps = list(task["board"].get("fixed", [])) + list(task.get("solution", {}).values()) + list(task.get("parts", []))
    types = {c.get("type") for c in comps}
    for t in KEY_ORDER:
        if t in types:
            return KEY_ALIAS.get(t, t)
    if re.search(r"bulb|lamp|lantern", f"{task['title']} {task.get('story', '')}", re.I):
        return "lamp"
    if "switch" in types:
        return "switch"
    if types & {"pulse_source", "sine_source", "voltage_source", "current_source"}:
        return "source"
    if "battery" in types and "resistor" not in types:
        return "battery"
    return "resistor"


def safe_name(task_id):
    return re.sub(r"[^A-Za-z0-9_.-]", "-", task_id)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    sources = [(p, p.parents[2], p.parents[1].name) for p in sorted(ROOT.glob("phases/*/*/lab/task.json"))]
    sources += [(p, None, p.parent.name) for p in sorted((ROOT / "lab" / "examples").glob("*/task.json"))]
    phases = {}
    seen = {}
    skipped = 0
    for path, phase_dir, lesson in sources:
        rel = path.relative_to(ROOT)
        try:
            task = json.loads(path.read_text())
            missing = [k for k in REQUIRED if k not in task]
            if missing:
                raise ValueError(f"missing {', '.join(missing)}")
            if not task["board"].get("nodes") and task["kind"] != "logic":
                print(f"note  {rel}: no node coordinates, the lab lays it out automatically")
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"skip  {rel}: {exc}")
            skipped += 1
            continue
        name = safe_name(task["id"])
        if name in seen:
            print(f"skip  {rel}: id {task['id']!r} already used by {seen[name]}")
            skipped += 1
            continue
        seen[name] = rel
        (OUT / f"{name}.json").write_text(json.dumps(task, indent=1))
        if phase_dir is None:
            key, number, title = "zz-examples", "ex", "Examples"
        else:
            key, number, title = phase_dir.name, phase_dir.name.split("-", 1)[0], phase_title(phase_dir)
        phases.setdefault(key, {"number": number, "slug": key, "title": title, "tasks": []})
        phases[key]["tasks"].append({"id": name, "title": task["title"], "kind": task["kind"], "key": key_part(task), "lesson": lesson, "source": str(rel)})
    index = {"phases": [phases[k] for k in sorted(phases)]}
    (OUT / "index.json").write_text(json.dumps(index, indent=1))
    total = sum(len(p["tasks"]) for p in index["phases"])
    print(f"{total} tasks in {len(index['phases'])} groups written to {OUT.relative_to(ROOT)}")
    return 1 if skipped else 0


if __name__ == "__main__":
    sys.exit(main())
