"""Validate repository-provided reference/flawed fixture quality from JSON reports."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from evaluator.manifest import ROOT, load_benchmark

EXPECTATIONS_PATH = ROOT / "fixture_expectations.json"


class FixtureCheckError(ValueError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FixtureCheckError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FixtureCheckError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise FixtureCheckError(f"{path} must contain a JSON object")
    return value


def _result_map(payload: dict[str, Any], label: str) -> dict[str, dict[str, Any]]:
    rows = payload.get("tasks")
    if not isinstance(rows, list):
        raise FixtureCheckError(f"{label}: tasks must be a list")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise FixtureCheckError(f"{label}: invalid task result")
        if row["id"] in result:
            raise FixtureCheckError(f"{label}: duplicate task result {row['id']}")
        result[row["id"]] = row
    return result


def validate_fixture_results(
    *,
    task_ids: list[str],
    expectations: dict[str, Any],
    reference_payload: dict[str, Any],
    flawed_payload: dict[str, Any],
) -> list[str]:
    problems: list[str] = []

    if expectations.get("schema_version") != "1.0":
        problems.append("fixture expectations: unsupported schema_version")

    expected_tasks = expectations.get("tasks")
    if not isinstance(expected_tasks, dict):
        return problems + ["fixture expectations: tasks must be an object"]

    canonical = set(task_ids)
    configured = set(expected_tasks)
    if configured != canonical:
        missing = sorted(canonical - configured)
        extra = sorted(configured - canonical)
        if missing:
            problems.append("fixture expectations missing: " + ", ".join(missing))
        if extra:
            problems.append("fixture expectations unexpected: " + ", ".join(extra))

    reference = _result_map(reference_payload, "reference report")
    flawed = _result_map(flawed_payload, "flawed report")

    for task_id in task_ids:
        ref = reference.get(task_id)
        bad = flawed.get(task_id)
        config = expected_tasks.get(task_id)

        if ref is None:
            problems.append(f"{task_id}: missing reference result")
            continue
        if bad is None:
            problems.append(f"{task_id}: missing flawed result")
            continue
        if not isinstance(config, dict):
            problems.append(f"{task_id}: invalid fixture expectation")
            continue

        if ref.get("failed") != 0 or ref.get("errors") != 0:
            problems.append(f"{task_id}: reference fixture must pass all tests")

        minimum_passed = config.get("minimum_passed")
        must_fail_tests = config.get("must_fail_tests")
        if not isinstance(minimum_passed, int) or isinstance(minimum_passed, bool) or minimum_passed < 1:
            problems.append(f"{task_id}: minimum_passed must be a positive integer")
            continue
        if (
            not isinstance(must_fail_tests, list)
            or not must_fail_tests
            or not all(isinstance(name, str) and name for name in must_fail_tests)
            or len(must_fail_tests) != len(set(must_fail_tests))
        ):
            problems.append(f"{task_id}: must_fail_tests must be a unique non-empty string list")
            continue

        if bad.get("errors") != 0:
            problems.append(f"{task_id}: flawed fixture has execution/collection errors")

        passed = bad.get("passed")
        if not isinstance(passed, int) or passed < minimum_passed:
            problems.append(
                f"{task_id}: flawed fixture passed {passed!r}; expected at least {minimum_passed}"
            )

        actual_failed = bad.get("failed_tests")
        if not isinstance(actual_failed, list):
            problems.append(f"{task_id}: flawed result missing failed_tests")
            continue
        missing_failures = [name for name in must_fail_tests if name not in actual_failed]
        if missing_failures:
            problems.append(
                f"{task_id}: target defect no longer exposed by "
                + ", ".join(missing_failures)
            )

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-json", type=Path, required=True)
    parser.add_argument("--flawed-json", type=Path, required=True)
    parser.add_argument(
        "--expectations",
        type=Path,
        default=EXPECTATIONS_PATH,
    )
    args = parser.parse_args()

    _, tasks = load_benchmark()
    expectations = _read_json(args.expectations)
    reference_payload = _read_json(args.reference_json)
    flawed_payload = _read_json(args.flawed_json)

    problems = validate_fixture_results(
        task_ids=[task.id for task in tasks],
        expectations=expectations,
        reference_payload=reference_payload,
        flawed_payload=flawed_payload,
    )
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        return 1

    print(f"fixture quality: {len(tasks)} tasks validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
