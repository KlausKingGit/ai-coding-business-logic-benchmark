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
from evaluator.report import write_json_report, write_report
from evaluator.scoring import score

SUMMARY = re.compile(r"(\d+) (passed|failed|error|errors)\b")
FAILED_TEST = re.compile(r"^FAILED\s+.*?::(\S+)", re.MULTILINE)
SAFE_REPORT_NAME = re.compile(r"[^A-Za-z0-9._-]+")
ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
EXTERNAL_ENV_ALLOWLIST = {
    "PATH",
    "HOME",
    "TMPDIR",
    "TMP",
    "TEMP",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "TZ",
    "SYSTEMROOT",
    "WINDIR",
    "PATHEXT",
    "COMSPEC",
}
RESERVED_EXTERNAL_ENV = {"EVAL_CANDIDATE", "EVAL_CANDIDATE_DIR"}


def _safe_report_name(value: str) -> str:
    normalized = SAFE_REPORT_NAME.sub("-", value).strip("-._")
    return normalized or "external"


def _build_candidate_env(
    *,
    candidate_mode: str,
    external_dir: Path | None,
    inherit_env: list[str],
) -> dict[str, str]:
    if candidate_mode != "external":
        if inherit_env:
            raise ValueError("--inherit-env requires --candidate-dir")
        env = os.environ.copy()
        env["EVAL_CANDIDATE"] = candidate_mode
        env.pop("EVAL_CANDIDATE_DIR", None)
        return env

    env = {
        key: value
        for key, value in os.environ.items()
        if key in EXTERNAL_ENV_ALLOWLIST
    }
    for name in inherit_env:
        if not ENV_NAME.fullmatch(name):
            raise ValueError(f"invalid environment variable name: {name!r}")
        if name in RESERVED_EXTERNAL_ENV:
            raise ValueError(f"cannot override reserved environment variable: {name}")
        if name not in os.environ:
            raise ValueError(f"environment variable is not set: {name}")
        env[name] = os.environ[name]

    env["EVAL_CANDIDATE"] = "external"
    if external_dir is None:
        raise ValueError("external candidate directory is required")
    env["EVAL_CANDIDATE_DIR"] = str(external_dir)
    return env


def _timeout_output(exc: subprocess.TimeoutExpired) -> str:
    output = ""
    for value in (exc.stdout, exc.stderr):
        if isinstance(value, bytes):
            output += value.decode(errors="replace")
        elif isinstance(value, str):
            output += value
    return output


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
        "--inherit-env",
        action="append",
        default=[],
        metavar="NAME",
        help="explicitly pass one host environment variable to external candidate code; repeat as needed",
    )
    parser.add_argument(
        "--task-timeout-seconds",
        type=float,
        default=30.0,
        help="maximum pytest runtime per task (default: 30 seconds)",
    )
    parser.add_argument(
        "--task",
        action="append",
        dest="task_ids",
        help="run only this task id; repeat for multiple tasks",
    )
    parser.add_argument("--list-tasks", action="store_true")
    parser.add_argument("--report-dir", type=Path, default=ROOT / "reports")
    parser.add_argument(
        "--json-report",
        type=Path,
        help="optional path for a machine-readable JSON result",
    )
    args = parser.parse_args()

    if args.task_timeout_seconds <= 0:
        parser.error("--task-timeout-seconds must be greater than zero")

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

    try:
        base_env = _build_candidate_env(
            candidate_mode=candidate_mode,
            external_dir=external_dir,
            inherit_env=args.inherit_env,
        )
    except ValueError as exc:
        parser.error(str(exc))

    print(f"Benchmark: {benchmark['benchmark_id']} {benchmark['benchmark_version']}")
    print(f"Candidate: {candidate_label}")
    if external_dir is not None:
        print(f"Candidate directory: {external_dir}")
        print("External candidate environment: sanitized")
    print(f"Task timeout: {args.task_timeout_seconds:g}s")

    rows: list[dict] = []
    infrastructure_error = False

    for task in tasks:
        try:
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
                env=base_env,
                text=True,
                capture_output=True,
                timeout=args.task_timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            infrastructure_error = True
            timeout_message = (
                f"timed out after {args.task_timeout_seconds:g} seconds"
            )
            output = _timeout_output(exc)
            print(f"{task.id}: {timeout_message}")
            if output:
                print(output)
            rows.append(
                {
                    "task": task.id,
                    "passed": 0,
                    "failed": 0,
                    "errors": 1,
                    "score": 0,
                    "failed_tests": [],
                    "infrastructure_error": timeout_message,
                }
            )
            continue

        output = result.stdout + result.stderr
        counts = {kind: int(n) for n, kind in SUMMARY.findall(output)}
        passed = counts.get("passed", 0)
        failed = counts.get("failed", 0)
        errors = counts.get("error", 0) + counts.get("errors", 0)
        row_infrastructure_error: str | None = None

        if result.returncode not in (0, 1) or errors or passed + failed == 0:
            infrastructure_error = True
            row_infrastructure_error = "test collection or execution error"
            print(f"{task.id}: {row_infrastructure_error}\n{output}")

        rows.append(
            {
                "task": task.id,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "score": score(passed, failed),
                "failed_tests": FAILED_TEST.findall(output),
                "infrastructure_error": row_infrastructure_error,
            }
        )
        print(
            f"{task.id}: {passed} passed, {failed} failed, "
            f"{errors} errors, {score(passed, failed)}/100"
        )

    suffix = "" if not args.task_ids else ".selected"
    markdown_target = args.report_dir / f"{report_stem}{suffix}.md"
    write_report(
        candidate_label,
        rows,
        markdown_target,
        benchmark_version=benchmark["benchmark_version"],
    )
    print(f"Report: {markdown_target}")

    if args.json_report is not None:
        write_json_report(
            benchmark_id=benchmark["benchmark_id"],
            benchmark_version=benchmark["benchmark_version"],
            candidate_mode=candidate_mode,
            candidate_name=candidate_label,
            rows=rows,
            target=args.json_report,
        )
        print(f"JSON report: {args.json_report}")

    if infrastructure_error:
        return 2
    if candidate_mode == "reference" and any(row["failed"] for row in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
