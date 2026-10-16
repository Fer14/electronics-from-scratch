from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BADGE = "https://img.shields.io/badge/{}-{}-793e4d?style=flat-square&labelColor=fafaf5"


def phases():
    for phase in sorted((ROOT / "phases").iterdir()):
        if not phase.is_dir():
            continue
        lines = (phase / "README.md").read_text().splitlines()
        title = lines[0].removeprefix("# ").split(": ", 1)[1]
        motto = next(l for l in lines if l.startswith("> ")).removeprefix("> ")
        lessons = []
        for lesson in sorted(p for p in phase.iterdir() if p.is_dir()):
            lessons.append((lesson, (lesson / "docs" / "en.md").read_text().splitlines()[0].removeprefix("# ")))
        yield phase, title, motto, lessons


def main():
    data = list(phases())
    total = sum(len(l) for *_, l in data)
    labs = len(list((ROOT / "phases").glob("*/*/lab/task.json")))
    table = "\n".join(f"| {p.name[:2]} | [{t}](phases/{p.name}/) | {len(l)} | {m} |" for p, t, m, l in data)
    contents = []
    for phase, title, motto, lessons in data:
        rows = "\n".join(f"| {l.name[:2]} | [{name}](phases/{phase.name}/{l.name}/) |" for l, name in lessons)
        contents.append(f"""<a id="phase-{phase.name[:2]}"></a>
<details>
<summary><strong>Phase {phase.name[:2]} · {title}</strong> · {len(lessons)} lessons</summary>

> {motto}

| # | Lesson |
|---|---|
{rows}

</details>""")
    contents = "\n\n".join(contents)
    readme = f"""<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/readme/header-dark.svg">
    <img src="assets/readme/header-light.svg" alt="Electronics from Scratch" width="840">
  </picture>
</p>

Learn electronics from absolute zero. Start with what a volt and an ampere really are, work up through resistors, capacitors, diodes, transistors and op-amps, build a computer out of logic gates, design the arithmetic inside an AI chip, and finish by designing a real printed circuit board. Every idea is simulated with a circuit simulator you build yourself, and almost every phase has hands-on tasks in the interactive lab.

> {total} lessons. {len(data)} phases. {labs} lab tasks. Python and NumPy, no prior knowledge.

<p align="center">
  <a href="LICENSE"><img src="{BADGE.format('license', 'MIT')}" alt="MIT License"></a>
  <a href="#contents"><img src="{BADGE.format('lessons', total)}" alt="{total} lessons"></a>
  <a href="#contents"><img src="{BADGE.format('phases', len(data))}" alt="{len(data)} phases"></a>
  <a href="#the-lab"><img src="{BADGE.format('labs', labs)}" alt="{labs} labs"></a>
</p>

## Phases

| # | Phase | Lessons | What it is about |
|---|---|---|---|
{table}

## Every lesson has the same shape

```
NN-lesson-name/
├── code/main.py   from-scratch implementation, runnable from the repo root
├── docs/en.md     Words You'll Meet · The Physics · The Concept · Build It · Use It · Exercises
├── quiz.json      questions to check yourself before and after
└── lab/task.json  a hands-on task for the interactive lab (most lessons from Phase 02 on)
```

## Our own simulator

`sim/` is a small circuit simulator written for this course in plain Python and NumPy. It does DC operating points, transient (time) simulation and AC frequency sweeps, plus gate-level logic and a cost model for chip design. Phase 05 builds its core, modified nodal analysis, from scratch; Phases 07 and 10 build transient and AC analysis by hand and compare them with `sim`.

```python
from sim import Circuit

c = Circuit()
c.voltage_source("V1", "vcc", "0", 9.0)
c.resistor("R1", "vcc", "a", 680)
c.led("D1", "a", "0", color="red")
print(c.dc().i("D1"))
```

<a id="the-lab"></a>

## The lab

`lab/` is a static web page: every task is a small circuit with empty slots. Drop a part in each slot, press RUN, and the simulator checks the goals. Nothing to install:

```bash
uv run python scripts/build_lab.py
cd lab && python -m http.server 8000
```

Then open http://localhost:8000. `uv run python -m sim.lab phases/03-resistance-and-ohms-law/03-ohms-law/lab/task.json` checks a task from the terminal.

## Local setup

```bash
git clone https://github.com/Fer14/electronics-from-scratch.git
cd electronics-from-scratch
uv sync
uv run python phases/00-meet-electricity/01-what-electronics-is/code/main.py
```

No uv? `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` works too.

Check that every lesson runs: `uv run python scripts/check.py`

<a id="contents"></a>

## Contents

{contents}

## Contributing

New lessons follow [LESSON_TEMPLATE.md](LESSON_TEMPLATE.md) and lab tasks follow [LAB_FORMAT.md](LAB_FORMAT.md). Run `uv run python scripts/check.py` before opening a pull request.

## License

[MIT](LICENSE). Part of the THOTH series, alongside [Classic ML from Scratch](https://github.com/Fer14/classic-ml-from-scratch) and [Deep Learning from Scratch](https://github.com/Fer14/deep-learning-from-scratch). Structure inspired by [AI Engineering from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch).
"""
    (ROOT / "README.md").write_text(readme)


if __name__ == "__main__":
    main()
