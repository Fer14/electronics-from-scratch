"""Check lab tasks (lab/task.json, see LAB_FORMAT.md) with our simulator.

    uv run python -m sim.lab phases/11-semiconductors-and-diodes/07-leds/lab/task.json

fills the slots with the task's reference solution, simulates, and prints every goal
with its measured value. It then tries every other offered part in each slot (keeping the
rest of the solution) and reports which of them fail, because a good task makes every
wrong choice fail at least one goal.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

from .circuit import Circuit, ConvergenceError
from .cost import Design, build as build_block
from .logic import LogicCircuit, LogicSettleError

TERMINALS = {
    "battery": ("plus", "minus"),
    "voltage_source": ("plus", "minus"),
    "pulse_source": ("plus", "minus"),
    "sine_source": ("plus", "minus"),
    "current_source": ("from", "to"),
    "resistor": ("a", "b"),
    "capacitor": ("a", "b"),
    "inductor": ("a", "b"),
    "switch": ("a", "b"),
    "wire": ("a", "b"),
    "open": ("a", "b"),
    "diode": ("anode", "cathode"),
    "led": ("anode", "cathode"),
    "zener": ("anode", "cathode"),
    "npn": ("c", "b", "e"),
    "pnp": ("c", "b", "e"),
    "nmos": ("d", "g", "s"),
    "pmos": ("d", "g", "s"),
    "opamp": ("plus", "minus", "out"),
    "vcvs": ("plus", "minus", "cplus", "cminus"),
    "vccs": ("plus", "minus", "cplus", "cminus"),
}
POSITIONAL = ("a", "b", "c", "d")
SLOT_KEYS = {"id", "accepts", "label", "inputs", "output"}
UNITS = {
    "voltage": "V", "voltage_at_time": "V", "peak_voltage": "V", "min_voltage": "V", "ripple": "V",
    "current": "A", "current_at_time": "A", "peak_current": "A", "power": "W",
    "time_to_cross": "s", "frequency": "Hz", "cutoff_frequency": "Hz",
    "gain_db_at": "dB", "phase_deg_at": "deg",
    "area": "gate units", "critical_path": "gate delays", "latency": "cycles", "throughput": "MACs/cycle",
    "bits_moved": "bits/cycle", "energy": "units", "bits": "bits", "gate_count": "gates", "depth": "levels",
}


def load_task(path):
    return json.loads(Path(path).read_text())


def place(slot, part):
    component = {k: v for k, v in part.items()}
    component["id"] = slot["id"]
    own = TERMINALS.get(part["type"])
    if part["type"] == "gate":
        component["inputs"] = slot["inputs"]
        component["output"] = slot["output"]
    elif own and all(name in slot for name in own):
        for name in own:
            component[name] = slot[name]
    elif own:
        given = [slot[k] for k in POSITIONAL if k in slot]
        for name, node in zip(own, given):
            component[name] = node
    else:
        for key, value in slot.items():
            if key not in SLOT_KEYS:
                component[key] = value
    return component


def components(task, choice):
    board = task["board"]
    items = list(board.get("fixed", []))
    for slot in board.get("slots", []):
        part = choice.get(slot["id"])
        if part is None:
            raise ValueError(f"slot {slot['id']} is empty")
        items.append(place(slot, part))
    return items


def _node(name, ground):
    return "0" if name == ground else name


def build_circuit(task, choice):
    ground = task["board"].get("ground", "gnd")
    c = Circuit(task.get("title", ""))
    for comp in components(task, choice):
        kind, cid = comp["type"], comp["id"]
        n = lambda key: _node(comp[key], ground)
        if kind in ("battery", "voltage_source"):
            c.voltage_source(cid, n("plus"), n("minus"), comp.get("volts", 0.0))
        elif kind == "pulse_source":
            c.pulse_source(cid, n("plus"), n("minus"), comp.get("low", 0.0), comp.get("high", 5.0),
                           comp.get("period", 1e-3), comp.get("duty", 0.5), comp.get("delay", 0.0),
                           comp.get("rise", 0.0), comp.get("fall", 0.0))
        elif kind == "sine_source":
            c.sine_source(cid, n("plus"), n("minus"), comp.get("amplitude", 1.0), comp.get("freq", 50.0),
                          comp.get("offset", 0.0), comp.get("phase_deg", 0.0))
        elif kind == "current_source":
            c.current_source(cid, n("from"), n("to"), comp["amps"])
        elif kind == "resistor":
            c.resistor(cid, n("a"), n("b"), comp["ohms"])
        elif kind == "capacitor":
            c.capacitor(cid, n("a"), n("b"), comp["farads"], comp.get("v0", 0.0))
        elif kind == "inductor":
            c.inductor(cid, n("a"), n("b"), comp["henries"], comp.get("i0", 0.0))
        elif kind == "switch":
            c.switch(cid, n("a"), n("b"), comp.get("closed", True), toggle_at=comp.get("toggle_at", ()))
        elif kind == "wire":
            c.switch(cid, n("a"), n("b"), True)
        elif kind == "open":
            c.switch(cid, n("a"), n("b"), False)
        elif kind == "diode":
            c.diode(cid, n("anode"), n("cathode"), Is=comp.get("Is"), n=comp.get("n"), model=comp.get("model"))
        elif kind == "led":
            c.led(cid, n("anode"), n("cathode"), color=comp.get("color", "red"))
        elif kind == "zener":
            c.zener(cid, n("anode"), n("cathode"), vz=comp.get("vz", 5.1))
        elif kind in ("npn", "pnp"):
            getattr(c, kind)(cid, n("c"), n("b"), n("e"), beta=comp.get("beta", 100.0))
        elif kind in ("nmos", "pmos"):
            getattr(c, kind)(cid, n("d"), n("g"), n("s"), vth=comp.get("vth", 1.0), k=comp.get("k", 1e-3))
        elif kind == "opamp":
            c.opamp(cid, n("plus"), n("minus"), n("out"), gain=comp.get("gain", 1e5), rails=comp.get("rails"))
        elif kind == "vcvs":
            c.vcvs(cid, n("plus"), n("minus"), n("cplus"), n("cminus"), comp["gain"])
        elif kind == "vccs":
            c.vccs(cid, n("plus"), n("minus"), n("cplus"), n("cminus"), comp["gm"])
        else:
            raise ValueError(f"unknown component type {kind!r} in {cid}")
    return c


def build_logic(task, choice):
    board = task["board"]
    lc = LogicCircuit(task.get("title", ""))
    lc.inputs(*board.get("inputs", []))
    for comp in components(task, choice):
        if comp["type"] == "gate":
            lc.gate(comp["op"], comp["inputs"], comp["output"], name=comp["id"])
        elif comp["type"] == "dff":
            lc.dff(comp["d"], comp["q"], name=comp["id"], init=comp.get("init", 0))
        elif comp["type"] == "wire":
            lc.gate("buf", comp.get("inputs", [comp.get("a")])[:1], comp.get("output", comp.get("b")), name=comp["id"])
        else:
            raise ValueError(f"unknown logic part {comp['type']!r}")
    lc.outputs(*board.get("outputs", []))
    return lc


def build_design(task, choice):
    design = Design(task.get("title", ""))
    for comp in components(task, choice):
        params = {k: v for k, v in comp.items() if k not in ("type", "id", "a", "b", "label")}
        design.add(comp["id"], build_block(comp["type"], **params), comp.get("a", "in"), comp.get("b", "out"))
    return design


def _voltage(result, goal):
    ground = goal.get("_ground", "gnd")
    if "between" in goal:
        a, b = (_node(x, ground) for x in goal["between"])
        return result.v(a, b)
    return result.v(_node(goal["at"], ground))


def measure_dc(c, goal, ground):
    r = c.dc()
    kind = goal["measure"]
    if kind == "voltage":
        return float(_voltage(r, {**goal, "_ground": ground}))
    if kind == "current":
        return float(r.i(goal["of"]))
    if kind == "power":
        return float(r.p(goal["of"]))
    raise ValueError(f"measure {kind!r} is not available in a dc task")


def transient_settings(task):
    sim = task.get("sim", {})
    t_stop = float(sim.get("t_stop", 1.0))
    dt = float(sim.get("dt", t_stop / 2000))
    return t_stop, dt


def measure_transient(t, goal, ground):
    kind = goal["measure"]
    g = {**goal, "_ground": ground}
    if kind in ("voltage_at_time", "voltage"):
        v = _voltage(t, g)
        return float(v[-1]) if kind == "voltage" else float(_interp(t, goal["time"], v))
    if kind in ("current_at_time", "current"):
        i = t.i(goal["of"])
        return float(i[-1]) if kind == "current" else float(_interp(t, goal["time"], i))
    if kind == "power":
        return float(t.p(goal["of"])[-1])
    if kind == "time_to_cross":
        node = _node(goal["at"], ground)
        return float(t.time_to_cross(node, goal["level"], goal.get("direction", "rising")))
    if kind == "frequency":
        return float(t.frequency(_node(goal["at"], ground)))
    if kind == "peak_voltage":
        return float(_voltage(t, g).max())
    if kind == "min_voltage":
        return float(_voltage(t, g).min())
    if kind == "ripple":
        v = _voltage(t, g)
        tail = v[len(v) // 2:]
        return float(tail.max() - tail.min())
    if kind == "peak_current":
        return float(abs(t.i(goal["of"])).max())
    raise ValueError(f"measure {kind!r} is not available in a transient task")


def _interp(t, time, values):
    return np.interp(time, t.time, values)


def ac_settings(task):
    sim = task.get("sim", {})
    freqs = np.logspace(math.log10(sim.get("f_start", 1.0)), math.log10(sim.get("f_stop", 1e6)), int(sim.get("points", 200)))
    return freqs, sim.get("source")


def measure_ac(a, goal, ground):
    kind = goal["measure"]
    node = _node(goal["at"], ground)
    ref = _node(goal["ref"], ground) if goal.get("ref") else None
    if kind == "gain_db_at":
        return a.gain_db_at(goal["freq"], node, ref)
    if kind == "phase_deg_at":
            return float(np.interp(math.log10(goal["freq"]), np.log10(a.freqs), a.phase_deg(node, ref)))
    if kind == "cutoff_frequency":
        return a.cutoff(node, ref)
    raise ValueError(f"measure {kind!r} is not available in an ac task")


def measure_logic(lc, goal, task):
    kind = goal["measure"]
    if kind == "truth_table":
        rows = lc.truth_table(task["board"].get("inputs"), list(goal["expect"]))
        return sum(1 for n, row in enumerate(rows) for out, values in goal["expect"].items() if row[out] != values[n])
    if kind == "sequence":
        lc.reset()
        wrong = 0
        for n, inputs in enumerate(goal["steps"]):
            lc.step(inputs)
            wrong += sum(int(lc.values.get(name, 0) != values[n]) for name, values in goal["expect"].items())
        return wrong
    if kind == "gate_count":
        return lc.gate_count()
    if kind == "depth":
        return lc.depth()
    raise ValueError(f"measure {kind!r} is not available in a logic task")


def measure_chip(design, goal):
    kind = goal["measure"]
    if kind == "bits":
        block = design.blocks[goal["of"]][0]
        return block.params.get("acc_bits", block.params.get("bits", block.bits))
    return float(getattr(design, kind)())


def evaluate(task, choice=None):
    choice = choice if choice is not None else task.get("solution", {})
    kind = task["kind"]
    ground = task["board"].get("ground", "gnd")
    results = []
    try:
        if kind in ("dc", "transient", "ac"):
            model = build_circuit(task, choice)
            if kind == "transient":
                model = model.transient(*transient_settings(task))
            elif kind == "ac":
                freqs, source = ac_settings(task)
                model = model.ac(freqs, source)
        elif kind == "logic":
            model = build_logic(task, choice)
        elif kind == "chip":
            model = build_design(task, choice)
        else:
            raise ValueError(f"unknown task kind {kind!r}")
        error = None
    except (ConvergenceError, LogicSettleError, ValueError) as exc:
        model, error = None, str(exc)
    for goal in task.get("goals", []):
        label = goal.get("label", goal["measure"])
        if model is None:
            results.append({"label": label, "measure": goal["measure"], "value": None, "passed": False, "error": error})
            continue
        try:
            if kind == "dc":
                value = measure_dc(model, goal, ground)
            elif kind == "transient":
                value = measure_transient(model, goal, ground)
            elif kind == "ac":
                value = measure_ac(model, goal, ground)
            elif kind == "logic":
                value = measure_logic(model, goal, task)
            else:
                value = measure_chip(model, goal)
            if goal["measure"] in ("truth_table", "sequence"):
                passed = value == 0
            else:
                passed = math.isfinite(value) and goal.get("min", -math.inf) <= value <= goal.get("max", math.inf)
            results.append({"label": label, "measure": goal["measure"], "value": value, "passed": bool(passed), "error": None})
        except (ConvergenceError, LogicSettleError, KeyError, ValueError) as exc:
            results.append({"label": label, "measure": goal["measure"], "value": None, "passed": False, "error": str(exc)})
    return results


def alternatives(task):
    solution = task.get("solution", {})
    report = {}
    for slot in task["board"].get("slots", []):
        accepted = set(slot.get("accepts", []))
        rows = []
        for part in task.get("parts", []):
            if accepted and part["type"] not in accepted:
                continue
            if part == solution.get(slot["id"]):
                continue
            outcome = evaluate(task, {**solution, slot["id"]: part})
            failed = [r["label"] for r in outcome if not r["passed"]]
            rows.append({"part": part, "fails": failed})
        report[slot["id"]] = rows
    return report


def check(task):
    goals = evaluate(task)
    others = alternatives(task)
    problems = []
    if "solution" not in task:
        problems.append("task has no solution")
    problems += [f"solution fails goal: {g['label']}" + (f" ({g['error']})" if g["error"] else "") for g in goals if not g["passed"]]
    for slot, rows in others.items():
        if not any(row["fails"] for row in rows):
            problems.append(f"slot {slot}: no wrong part fails any goal")
    return goals, others, problems


def describe(part):
    details = ", ".join(f"{k}={v}" for k, v in part.items() if k != "type")
    return f"{part['type']}({details})"


def format_value(value, measure):
    if value is None:
        return "n/a"
    if measure in ("truth_table", "sequence"):
        return "all rows right" if value == 0 else f"{value} wrong"
    from .results import engineering
    unit = UNITS.get(measure, "")
    if unit in ("V", "A", "W", "s", "Hz"):
        return engineering(float(value), unit)
    return f"{value:.4g} {unit}".strip()


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: python -m sim.lab path/to/task.json [...]")
        return 2
    status = 0
    for path in argv:
        task = load_task(path)
        goals, others, problems = check(task)
        print(f"{task.get('id', path)}  [{task['kind']}]  {task.get('title', '')}")
        print("  reference solution:")
        for g in goals:
            mark = "pass" if g["passed"] else "FAIL"
            extra = f"  ({g['error']})" if g["error"] else ""
            print(f"    {mark}  {g['label']}: {format_value(g['value'], g['measure'])}{extra}")
        for slot, rows in others.items():
            print(f"  slot {slot}, other parts:")
            for row in rows:
                verdict = "fails: " + "; ".join(row["fails"]) if row["fails"] else "PASSES every goal"
                print(f"    {describe(row['part'])} -> {verdict}")
        if problems:
            status = 1
            print("  problems:")
            for p in problems:
                print(f"    - {p}")
        else:
            print("  task ok")
    return status


if __name__ == "__main__":
    sys.exit(main())
