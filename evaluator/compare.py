"""Compare two machine-readable benchmark result files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evaluator.result_io import ResultError, ensure_comparable, load_result


def build_comparison(
    baseline: dict,
    candidate: dict,
) -> dict:
    benchmark_id, benchmark_version, ordered_ids = ensure_comparable(
        [
            (Path("<baseline>"), baseline),
            (Path("<candidate>"), candidate),
        ]
    )
    base_rows = {row["id"]: row for row in baseline["tasks"]}
    cand_rows = {row["id"]: row for row in candidate["tasks"]}

    return {
        "schema_version": "1.0",
        "benchmark": {
            "id": benchmark_id,
            "version": benchmark_version,
        },
        "baseline": {
            "candidate": baseline["candidate"],
            "summary": baseline["summary"],
        },
        "candidate": {
            "candidate": candidate["candidate"],
            "summary": candidate["summary"],
        },
        "delta": {
            "score": candidate["summary"]["score"] - baseline["summary"]["score"],
            "passed": candidate["summary"]["passed"] - baseline["summary"]["passed"],
            "failed": candidate["summary"]["failed"] - baseline["summary"]["failed"],
            "errors": candidate["summary"]["errors"] - baseline["summary"]["errors"],
        },
        "tasks": [
            {
                "id": task_id,
                "baseline_score": base_rows[task_id]["score"],
                "candidate_score": cand_rows[task_id]["score"],
                "score_delta": cand_rows[task_id]["score"] - base_rows[task_id]["score"],
                "baseline_passed": base_rows[task_id]["passed"],
                "candidate_passed": cand_rows[task_id]["passed"],
                "baseline_failed": base_rows[task_id]["failed"],
                "candidate_failed": cand_rows[task_id]["failed"],
            }
            for task_id in ordered_ids
        ],
    }


def render_markdown(comparison: dict) -> str:
    base_name = comparison["baseline"]["candidate"]["name"]
    cand_name = comparison["candidate"]["candidate"]["name"]
    lines = [
        f"# Benchmark comparison: {base_name} → {cand_name}",
        "",
        (
            f"Benchmark: {comparison['benchmark']['id']} "
            f"{comparison['benchmark']['version']}"
        ),
        "",
        "| Metric | Baseline | Candidate | Delta |",
        "|---|---:|---:|---:|",
    ]
    for field in ("score", "passed", "failed", "errors"):
        baseline_value = comparison["baseline"]["summary"][field]
        candidate_value = comparison["candidate"]["summary"][field]
        delta = comparison["delta"][field]
        lines.append(
            f"| {field} | {baseline_value} | {candidate_value} | {delta:+d} |"
        )

    lines += [
        "",
        "## Per-task score delta",
        "",
        "| Task | Baseline | Candidate | Delta |",
        "|---|---:|---:|---:|",
    ]
    for row in comparison["tasks"]:
        lines.append(
            f"| {row['id']} | {row['baseline_score']} | "
            f"{row['candidate_score']} | {row['score_delta']:+d} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    try:
        baseline = load_result(args.baseline)
        candidate = load_result(args.candidate)
        comparison = build_comparison(baseline, candidate)
    except ResultError as exc:
        parser.error(str(exc))

    markdown = render_markdown(comparison)
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(comparison, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
