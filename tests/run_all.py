"""Run every test_* function in tests/test_*.py with plain asserts (no pytest needed)."""
import importlib.util
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    passed = failed = 0
    for path in sorted(HERE.glob("test_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name in sorted(n for n in dir(module) if n.startswith("test_")):
            start = time.perf_counter()
            try:
                getattr(module, name)()
                passed += 1
                print(f"ok    {path.stem}.{name}  ({time.perf_counter() - start:.2f} s)")
            except Exception:
                failed += 1
                print(f"FAIL  {path.stem}.{name}")
                traceback.print_exc()
    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
