"""Run all reference-solution tests and write a reproducible report."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evaluator.report import write_report
from evaluator.scoring import score


COUNT = re.compile(r"(\d+) (passed|failed|error|errors)")


def main() -> int:
    rows = []
    for task in sorted((ROOT / "tasks").glob("task_*")):
        result = subprocess.run([sys.executable, "-m", "pytest", "-q", str(task / "tests")], cwd=ROOT, text=True, capture_output=True)
        output = result.stdout + result.stderr
        counts = {kind: int(n) for n, kind in COUNT.findall(output)}
        passed = counts.get("passed", 0)
        failed = counts.get("failed", 0) + counts.get("error", 0) + counts.get("errors", 0)
        if result.returncode and not failed:
            failed = 1  # Collection or execution failure is never scored as success.
        rows.append({"task": task.name, "passed": passed, "failed": failed, "score": score(passed, failed)})
        print(f"{task.name}: {passed} passed, {failed} failed, {score(passed, failed)}/100")
        if result.returncode:
            print(output)
    target = ROOT / "report.md"
    write_report(rows, target)
    print(f"Report: {target}")
    return 1 if any(row["failed"] for row in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
