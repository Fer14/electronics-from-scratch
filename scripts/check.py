import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sim.lab import check as check_task

QUIZ_KEYS = {"id", "stage", "question", "options", "correct", "explanation"}
MAIN_TIMEOUT = 120


def check_lab(lesson):
    task_path = lesson / "lab" / "task.json"
    if not task_path.exists():
        return []
    try:
        task = json.loads(task_path.read_text())
    except json.JSONDecodeError as exc:
        return [f"lab/task.json is not valid JSON: {exc}"]
    for key in ("id", "title", "kind", "board", "parts", "goals", "solution"):
        if key not in task:
            return [f"lab/task.json misses {key!r}"]
    try:
        _, _, problems = check_task(task)
    except Exception as exc:
        return [f"lab: {type(exc).__name__}: {exc}"]
    return [f"lab: {p}" for p in problems]


def check_lesson(lesson):
    errors = []
    for required in ("code/main.py", "docs/en.md", "quiz.json"):
        if not (lesson / required).exists():
            errors.append(f"missing {required}")
    quiz = lesson / "quiz.json"
    if quiz.exists():
        try:
            questions = json.loads(quiz.read_text())
        except json.JSONDecodeError as exc:
            questions = []
            errors.append(f"quiz.json is not valid JSON: {exc}")
        for q in questions:
            if set(q) != QUIZ_KEYS or len(q["options"]) != 4 or not 0 <= q["correct"] < 4 or q["stage"] not in ("pre", "post"):
                errors.append(f"bad quiz question {q.get('id')}")
    main = lesson / "code" / "main.py"
    if main.exists():
        try:
            run = subprocess.run([sys.executable, str(main)], cwd=ROOT, capture_output=True, text=True, timeout=MAIN_TIMEOUT,
                                 env={"MPLBACKEND": "Agg", "PATH": "/usr/bin:/bin", "HOME": str(Path.home()),
                                      "PYTHONPATH": str(ROOT), "OMP_NUM_THREADS": "4", "MKL_NUM_THREADS": "4"})
            if run.returncode:
                errors.append(f"main.py exited {run.returncode}: {run.stderr.strip().splitlines()[-1:]}")
        except subprocess.TimeoutExpired:
            errors.append(f"main.py took longer than {MAIN_TIMEOUT} s")
    errors += check_lab(lesson)
    return errors


def selected_lessons(args):
    every = sorted(p for p in (ROOT / "phases").glob("*/*") if p.is_dir())
    if not args:
        return every
    wanted = [Path(a).resolve() for a in args]
    return [p for p in every if any(p == w or w in p.parents for w in wanted)]


def main():
    lessons = selected_lessons(sys.argv[1:])
    failed = 0
    for lesson in lessons:
        errors = check_lesson(lesson)
        failed += bool(errors)
        print(f"{'FAIL' if errors else 'ok  '}  {lesson.relative_to(ROOT)}")
        for error in errors:
            print(f"      {error}")
    print(f"\n{len(lessons) - failed}/{len(lessons)} lessons pass")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
