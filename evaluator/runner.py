"""Evaluate either implementation with the same task tests."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evaluator.report import write_report
from evaluator.scoring import score

SUMMARY = re.compile(r"(\d+) (passed|failed|error|errors)\b")
FAILED_TEST = re.compile(r"^FAILED\s+.*?::(\S+)", re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", choices=("reference", "bad"), default="reference")
    args = parser.parse_args()
    display_candidate = "flawed" if args.candidate == "bad" else "reference"
    print(f"Candidate: {display_candidate}")
    rows = []
    infrastructure_error = False
    for task in sorted((ROOT / "tasks").glob("task_*")):
        env = os.environ.copy()
        env["EVAL_CANDIDATE"] = args.candidate
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--disable-warnings", str(task / "tests")],
            cwd=ROOT, env=env, text=True, capture_output=True,
        )
        output = result.stdout + result.stderr
        counts = {kind: int(n) for n, kind in SUMMARY.findall(output)}
        passed = counts.get("passed", 0)
        failed = counts.get("failed", 0)
        errors = counts.get("error", 0) + counts.get("errors", 0)
        if result.returncode not in (0, 1) or errors or passed + failed == 0:
            infrastructure_error = True
            print(f"{task.name}: test collection or execution error\n{output}")
        rows.append({
            "task": task.name, "passed": passed, "failed": failed,
            "errors": errors, "score": score(passed, failed),
            "failed_tests": FAILED_TEST.findall(output),
        })
        print(f"{task.name}: {passed} passed, {failed} failed, {errors} errors, {score(passed, failed)}/100")
    target = ROOT / "reports" / f"{display_candidate}.md"
    write_report(display_candidate, rows, target)
    print(f"Report: {target}")
    if infrastructure_error:
        return 2
    if args.candidate == "reference" and any(row["failed"] for row in rows):
        return 1
    return 0  # In flawed candidate mode, test failures are the expected evaluation result.


if __name__ == "__main__":
    raise SystemExit(main())
