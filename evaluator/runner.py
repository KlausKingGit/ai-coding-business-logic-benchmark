"""Evaluate one candidate against the benchmark task tests."""
import argparse, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evaluator.manifest import ManifestError, load_benchmark
from evaluator.report import write_report
from evaluator.scoring import score

SUMMARY = re.compile(r"(\d+) (passed|failed|error|errors)\b")
FAILED_TEST = re.compile(r"^FAILED\s+.*?::(\S+)", re.MULTILINE)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", choices=("reference", "flawed", "bad"), default="reference",
                        help="'bad' is a backward-compatible alias for 'flawed'")
    parser.add_argument("--task", action="append", dest="task_ids",
                        help="run only this task id; repeat for multiple tasks")
    parser.add_argument("--list-tasks", action="store_true")
    parser.add_argument("--report-dir", type=Path, default=ROOT / "reports")
    args = parser.parse_args()
    try:
        benchmark, tasks = load_benchmark()
    except ManifestError as exc:
        parser.error(str(exc))
    if args.list_tasks:
        for task in tasks:
            print(f"{task.id}\t{task.title}")
        return 0
    if args.task_ids:
        wanted = set(args.task_ids)
        known = {task.id for task in tasks}
        unknown = sorted(wanted - known)
        if unknown:
            parser.error("unknown task id(s): " + ", ".join(unknown))
        tasks = [task for task in tasks if task.id in wanted]
    candidate = "reference" if args.candidate == "reference" else "flawed"
    print(f"Benchmark: {benchmark['benchmark_id']} {benchmark['benchmark_version']}")
    print(f"Candidate: {candidate}")
    rows, infrastructure_error = [], False
    for task in tasks:
        env = os.environ.copy()
        env["EVAL_CANDIDATE"] = candidate
        result = subprocess.run([sys.executable, "-m", "pytest", "-q", "--disable-warnings", str(task.path / "tests")],
                                cwd=ROOT, env=env, text=True, capture_output=True)
        output = result.stdout + result.stderr
        counts = {kind: int(n) for n, kind in SUMMARY.findall(output)}
        passed, failed = counts.get("passed", 0), counts.get("failed", 0)
        errors = counts.get("error", 0) + counts.get("errors", 0)
        if result.returncode not in (0, 1) or errors or passed + failed == 0:
            infrastructure_error = True
            print(f"{task.id}: test collection or execution error\n{output}")
        rows.append({"task": task.id, "passed": passed, "failed": failed, "errors": errors,
                     "score": score(passed, failed), "failed_tests": FAILED_TEST.findall(output)})
        print(f"{task.id}: {passed} passed, {failed} failed, {errors} errors, {score(passed, failed)}/100")
    suffix = "" if not args.task_ids else ".selected"
    target = args.report_dir / f"{candidate}{suffix}.md"
    write_report(candidate, rows, target, benchmark_version=benchmark["benchmark_version"])
    print(f"Report: {target}")
    if infrastructure_error:
        return 2
    if candidate == "reference" and any(row["failed"] for row in rows):
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
