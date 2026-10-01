"""Evaluate one candidate against the benchmark task tests."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evaluator.manifest import ManifestError, load_benchmark
from evaluator.report import write_report
from evaluator.scoring import score

SUMMARY = re.compile(r"(\d+) (passed|failed|error|errors)\b")
FAILED_TEST = re.compile(r"^FAILED\s+.*?::(\S+)", re.MULTILINE)
SAFE_REPORT_NAME = re.compile(r"[^A-Za-z0-9._-]+")


def _safe_report_name(value: str) -> str:
    normalized = SAFE_REPORT_NAME.sub("-", value).strip("-._")
    return normalized or "external"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--candidate",
        choices=("reference", "flawed", "bad"),
        default=None,
        help="'bad' is a backward-compatible alias for 'flawed'",
    )
    source.add_argument(
        "--candidate-dir",
        type=Path,
        help="directory containing external candidate files named <task_id>.py",
    )
    parser.add_argument(
        "--candidate-name",
        help="display/report name for --candidate-dir runs",
    )
    parser.add_argument(
        "--task",
        action="append",
        dest="task_ids",
        help="run only this task id; repeat for multiple tasks",
    )
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

    external_dir: Path | None = None
    if args.candidate_dir is not None:
        external_dir = args.candidate_dir.expanduser().resolve()
        if not external_dir.is_dir():
            parser.error(f"candidate directory not found: {external_dir}")
        candidate_mode = "external"
        candidate_label = args.candidate_name or external_dir.name or "external"
        report_stem = f"external-{_safe_report_name(candidate_label)}"
    else:
        if args.candidate_name:
            parser.error("--candidate-name requires --candidate-dir")
        requested = args.candidate or "reference"
        candidate_mode = "reference" if requested == "reference" else "flawed"
        candidate_label = candidate_mode
        report_stem = candidate_mode

    print(f"Benchmark: {benchmark['benchmark_id']} {benchmark['benchmark_version']}")
    print(f"Candidate: {candidate_label}")
    if external_dir is not None:
        print(f"Candidate directory: {external_dir}")

    rows: list[dict] = []
    infrastructure_error = False

    for task in tasks:
        env = os.environ.copy()
        env["EVAL_CANDIDATE"] = candidate_mode
        if external_dir is not None:
            env["EVAL_CANDIDATE_DIR"] = str(external_dir)
        else:
            env.pop("EVAL_CANDIDATE_DIR", None)

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "--disable-warnings",
                str(task.path / "tests"),
            ],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
        )
        output = result.stdout + result.stderr
        counts = {kind: int(n) for n, kind in SUMMARY.findall(output)}
        passed = counts.get("passed", 0)
        failed = counts.get("failed", 0)
        errors = counts.get("error", 0) + counts.get("errors", 0)

        if result.returncode not in (0, 1) or errors or passed + failed == 0:
            infrastructure_error = True
            print(f"{task.id}: test collection or execution error\n{output}")

        rows.append(
            {
                "task": task.id,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "score": score(passed, failed),
                "failed_tests": FAILED_TEST.findall(output),
            }
        )
        print(
            f"{task.id}: {passed} passed, {failed} failed, "
            f"{errors} errors, {score(passed, failed)}/100"
        )

    suffix = "" if not args.task_ids else ".selected"
    target = args.report_dir / f"{report_stem}{suffix}.md"
    write_report(
        candidate_label,
        rows,
        target,
        benchmark_version=benchmark["benchmark_version"],
    )
    print(f"Report: {target}")

    if infrastructure_error:
        return 2
    if candidate_mode == "reference" and any(row["failed"] for row in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
