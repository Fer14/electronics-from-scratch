"""Check that the web lab's JavaScript simulator agrees with sim/ on every task.

    uv run python scripts/compare_lab.py [task.json ...]

Runs the reference solution and every single-slot alternative of each task through both
simulators (Python here, JavaScript through node) and fails when a goal's pass/fail
differs or a measured value differs by more than 1%.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sim.lab import evaluate, load_task


def python_runs(task):
    solution = task.get("solution", {})
    runs = [(None, None, solution)]
    for slot in task["board"].get("slots", []):
        accepted = set(slot.get("accepts", []))
        for part in task.get("parts", []):
            if accepted and part["type"] not in accepted:
                continue
            if part == solution.get(slot["id"]):
                continue
            runs.append((slot["id"], part, {**solution, slot["id"]: part}))
    return [[(g["value"], g["passed"]) for g in evaluate(task, choice)] for _, _, choice in runs]


def number(value):
    if isinstance(value, (int, float)) and math.isfinite(value):
        return float(value)
    return None


def same(a, b):
    a, b = number(a), number(b)
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= 0.01 * max(abs(a), abs(b)) + 1e-12


def main():
    paths = sys.argv[1:] or [str(p) for p in sorted(ROOT.glob("phases/*/*/lab/task.json")) + sorted(ROOT.glob("lab/examples/*/task.json"))]
    js = json.loads(subprocess.run(["node", str(ROOT / "lab/js/cli.mjs"), *paths], capture_output=True, text=True, check=True).stdout)
    bad = 0
    for path in paths:
        task = load_task(path)
        py = python_runs(task)
        jr = js[path]
        problems = []
        for n, (prun, jrun) in enumerate(zip(py, jr)):
            for (pv, pp), j in zip(prun, jrun["results"]):
                if pp != j["passed"] or not same(pv, j["value"]):
                    who = "solution" if n == 0 else f"{jrun['slot']}={jrun['part']}"
                    problems.append(f"{who}: python {pv} ({pp}) vs js {j['value']} ({j['passed']})")
        if len(py) != len(jr):
            problems.append(f"python ran {len(py)} variants, js {len(jr)}")
        bad += bool(problems)
        print(f"{'FAIL' if problems else 'ok  '}  {task.get('id', path)}")
        for p in problems:
            print(f"      {p}")
    print(f"\n{len(paths) - bad}/{len(paths)} tasks agree")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
