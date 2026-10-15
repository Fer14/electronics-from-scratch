// node lab/js/cli.mjs task.json [...]: prints the goal values of the solution and of every
// single-slot alternative as JSON, so scripts/compare_lab.py can compare them with sim/.
import { readFileSync } from "node:fs";
import { evaluate } from "./sim/lab.js";

const out = {};
for (const path of process.argv.slice(2)) {
  const task = JSON.parse(readFileSync(path, "utf8"));
  const runs = [{ slot: null, part: null, choice: task.solution || {} }];
  for (const slot of task.board.slots || []) {
    for (const part of task.parts || []) {
      if (slot.accepts && slot.accepts.length && !slot.accepts.includes(part.type)) continue;
      if (JSON.stringify(part) === JSON.stringify(task.solution?.[slot.id])) continue;
      runs.push({ slot: slot.id, part, choice: { ...task.solution, [slot.id]: part } });
    }
  }
  out[path] = runs.map((r) => ({ slot: r.slot, part: r.part, results: evaluate(task, r.choice).results.map((g) => ({ value: Number.isFinite(g.value) ? g.value : g.value === null ? null : String(g.value), passed: g.passed })) }));
}
console.log(JSON.stringify(out));
