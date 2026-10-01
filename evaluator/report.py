from __future__ import annotations

import json
from pathlib import Path
import platform
import sys

from evaluator.scoring import score


def write_report(
    candidate: str,
    rows: list[dict],
    target: Path,
    *,
    benchmark_version: str | None = None,
) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# Evaluation report: {candidate} candidate", ""]
    if benchmark_version:
        lines += [f"Benchmark version: {benchmark_version}", ""]
    lines += [
        "Score = round(100 × passed / (passed + failed)). Collection errors invalidate the run.",
        "Only observed test outcomes are scored; human review remains necessary.",
        "",
        "| Task | Passed | Failed | Errors | Score |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['task']} | {row['passed']} | {row['failed']} | "
            f"{row['errors']} | {row['score']}/100 |"
        )
    lines += ["", "## Failed tests", ""]
    for row in rows:
        lines.append(f"### {row['task']}")
        infrastructure_error = row.get("infrastructure_error")
        if infrastructure_error:
            lines.append(f"- Infrastructure error: {infrastructure_error}")
        lines.extend(f"- `{name}`" for name in row["failed_tests"])
        if not row["failed_tests"] and not infrastructure_error:
            lines.append("- None")
        lines.append("")
    target.write_text("\n".join(lines), encoding="utf-8")


def build_json_report(
    *,
    benchmark_id: str,
    benchmark_version: str,
    candidate_mode: str,
    candidate_name: str,
    rows: list[dict],
) -> dict:
    passed = sum(row["passed"] for row in rows)
    failed = sum(row["failed"] for row in rows)
    errors = sum(row["errors"] for row in rows)

    return {
        "schema_version": "1.0",
        "benchmark": {
            "id": benchmark_id,
            "version": benchmark_version,
        },
        "candidate": {
            "mode": candidate_mode,
            "name": candidate_name,
        },
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": sys.platform,
        },
        "summary": {
            "tasks": len(rows),
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "score": score(passed, failed),
        },
        "tasks": [
            {
                "id": row["task"],
                "passed": row["passed"],
                "failed": row["failed"],
                "errors": row["errors"],
                "score": row["score"],
                "failed_tests": list(row["failed_tests"]),
                "infrastructure_error": row.get("infrastructure_error"),
            }
            for row in rows
        ],
    }


def write_json_report(
    *,
    benchmark_id: str,
    benchmark_version: str,
    candidate_mode: str,
    candidate_name: str,
    rows: list[dict],
    target: Path,
) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = build_json_report(
        benchmark_id=benchmark_id,
        benchmark_version=benchmark_version,
        candidate_mode=candidate_mode,
        candidate_name=candidate_name,
        rows=rows,
    )
    target.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
