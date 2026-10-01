"""Generate a safe contributor scaffold for a new benchmark task."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evaluator.manifest import SLUG, TASK_ID, load_benchmark


class ScaffoldError(ValueError):
    pass


def write_scaffold(
    *,
    output_dir: Path,
    task_id: str,
    title: str,
    summary: str,
    area: str,
    tags: list[str],
) -> None:
    if not TASK_ID.fullmatch(task_id):
        raise ScaffoldError("task id must match task_NN_short_slug")
    if not title.strip() or not summary.strip() or not area.strip():
        raise ScaffoldError("title, summary, and area must be non-empty")
    if not tags or not all(SLUG.fullmatch(tag) for tag in tags):
        raise ScaffoldError("tags must be non-empty lowercase slugs")
    if len(tags) != len(set(tags)):
        raise ScaffoldError("tags must be unique")

    _, existing = load_benchmark()
    if task_id in {task.id for task in existing}:
        raise ScaffoldError(f"task id already exists in benchmark: {task_id}")

    if output_dir.exists() and any(output_dir.iterdir()):
        raise ScaffoldError(f"output directory is not empty: {output_dir}")

    tests_dir = output_dir / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "schema_version": "1.0",
        "id": task_id,
        "title": title.strip(),
        "summary": summary.strip(),
        "area": area.strip(),
        "tags": tags,
        "candidates": {
            "reference": "reference_solution.py",
            "flawed": "flawed_candidate.py",
        },
        "tests": "tests/test_cases.py",
        "review_notes": "evaluation_notes.md",
        "expected": {
            "reference": "pass_all",
            "flawed": "fail_at_least_one",
        },
        "known_limits": [
            "TODO: replace with a deliberate scope limit before contribution."
        ],
    }
    (output_dir / "task.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    (output_dir / "README.md").write_text(
        f"# {title.strip()}\n\n"
        f"{summary.strip()}\n\n"
        "## Business invariant\n\n"
        "TODO: state one narrow observable rule that correct code must preserve.\n\n"
        "## Public interface\n\n"
        "TODO: document the functions/classes the tests will call.\n\n"
        "## Required behavior\n\n"
        "- TODO: happy-path behavior.\n"
        "- TODO: validation/error behavior.\n"
        "- TODO: target edge case that distinguishes plausible from correct code.\n\n"
        "## Known limits\n\n"
        "TODO: document what this small fixture intentionally does not model.\n",
        encoding="utf-8",
    )

    (output_dir / "reference_solution.py").write_text(
        '"""Reference implementation scaffold. Replace before contribution."""\n\n'
        "# TODO: implement the public interface documented in README.md.\n",
        encoding="utf-8",
    )
    (output_dir / "flawed_candidate.py").write_text(
        '"""Plausible flawed implementation scaffold. Replace before contribution."""\n\n'
        "# TODO: implement a realistic candidate that passes meaningful paths\n"
        "# while violating the target business invariant.\n",
        encoding="utf-8",
    )
    (output_dir / "evaluation_notes.md").write_text(
        "# Review notes\n\n"
        "## Target defect\n\n"
        "TODO: explain the exact business-rule defect demonstrated by the flawed fixture.\n\n"
        "## Review checklist\n\n"
        "- TODO: observable invariant.\n"
        "- TODO: why the flawed implementation is plausible.\n"
        "- TODO: known limits.\n",
        encoding="utf-8",
    )
    (tests_dir / "test_cases.py").write_text(
        "import pytest\n\n\n"
        "def test_scaffold_requires_real_discriminating_tests():\n"
        '    pytest.fail("replace scaffold placeholder with real benchmark tests")\n',
        encoding="utf-8",
    )
    (output_dir / "fixture_expectation.example.json").write_text(
        json.dumps(
            {
                task_id: {
                    "minimum_passed": 1,
                    "must_fail_tests": [
                        "TODO_target_test_name"
                    ],
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (output_dir / "SCAFFOLD_NEXT_STEPS.md").write_text(
        "# Scaffold next steps\n\n"
        "1. Replace every TODO and the intentionally failing placeholder test.\n"
        "2. Make the reference implementation pass all task tests.\n"
        "3. Make the flawed implementation plausible and targeted.\n"
        "4. Run the task against both candidates.\n"
        "5. Add the task to benchmark.json only when the task is ready for review.\n"
        "6. Add its quality expectation to fixture_expectations.json.\n"
        "7. Explain historical comparability in the pull request.\n\n"
        "The scaffold generator intentionally does not register the task automatically.\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--area", required=True)
    parser.add_argument("--tag", action="append", dest="tags", required=True)
    args = parser.parse_args()

    try:
        write_scaffold(
            output_dir=args.output_dir,
            task_id=args.task_id,
            title=args.title,
            summary=args.summary,
            area=args.area,
            tags=args.tags,
        )
    except ScaffoldError as exc:
        parser.error(str(exc))

    print(f"Task scaffold: {args.output_dir}")
    print("Not registered in benchmark.json.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
