"""Summarize a comparable set of benchmark JSON result files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evaluator.result_io import ResultError, ensure_comparable, load_result


def _expand(paths: list[Path]) -> list[Path]:
    expanded: list[Path] = []
    for path in paths:
        if path.is_dir():
            expanded.extend(sorted(p for p in path.glob("*.json") if p.is_file()))
        else:
            expanded.append(path)
    if not expanded:
        raise ResultError("no JSON result files found")
    return expanded


def build_history(items: list[tuple[Path, dict]]) -> dict:
    benchmark_id, benchmark_version, task_ids = ensure_comparable(items)
    return {
        "schema_version": "1.0",
        "benchmark": {
            "id": benchmark_id,
            "version": benchmark_version,
            "task_ids": task_ids,
        },
        "runs": [
            {
                "source": str(path),
                "candidate": payload["candidate"],
                "environment": payload["environment"],
                "summary": payload["summary"],
            }
            for path, payload in items
        ],
    }


def render_markdown(history: dict) -> str:
    lines = [
        "# Benchmark run history",
        "",
        (
            f"Benchmark: {history['benchmark']['id']} "
            f"{history['benchmark']['version']}"
        ),
        "",
        "| Candidate | Mode | Score | Passed | Failed | Errors | Python |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for run in history["runs"]:
        lines.append(
            f"| {run['candidate']['name']} | {run['candidate']['mode']} | "
            f"{run['summary']['score']} | {run['summary']['passed']} | "
            f"{run['summary']['failed']} | {run['summary']['errors']} | "
            f"{run['environment']['python']} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    try:
        paths = _expand(args.paths)
        items = [(path, load_result(path)) for path in paths]
        history = build_history(items)
    except ResultError as exc:
        parser.error(str(exc))

    markdown = render_markdown(history)
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(history, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
