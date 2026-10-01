"""Shared validation helpers for machine-readable benchmark results."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ResultError(ValueError):
    """Raised when a result file cannot be compared safely."""


def load_result(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ResultError(f"result file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ResultError(f"invalid JSON in {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise ResultError(f"{path}: top-level result must be an object")
    if payload.get("schema_version") != "1.0":
        raise ResultError(f"{path}: unsupported result schema_version")

    benchmark = payload.get("benchmark")
    if (
        not isinstance(benchmark, dict)
        or not isinstance(benchmark.get("id"), str)
        or not benchmark["id"]
        or not isinstance(benchmark.get("version"), str)
        or not benchmark["version"]
    ):
        raise ResultError(f"{path}: invalid benchmark metadata")

    candidate = payload.get("candidate")
    if (
        not isinstance(candidate, dict)
        or not isinstance(candidate.get("mode"), str)
        or not isinstance(candidate.get("name"), str)
        or not candidate["name"]
    ):
        raise ResultError(f"{path}: invalid candidate metadata")

    summary = payload.get("summary")
    if not isinstance(summary, dict):
        raise ResultError(f"{path}: summary must be an object")
    for field in ("tasks", "passed", "failed", "errors", "score"):
        value = summary.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ResultError(f"{path}: summary.{field} must be a non-negative integer")

    rows = payload.get("tasks")
    if not isinstance(rows, list):
        raise ResultError(f"{path}: tasks must be a list")

    seen: set[str] = set()
    passed = failed = errors = 0
    for row in rows:
        if not isinstance(row, dict):
            raise ResultError(f"{path}: task result must be an object")
        task_id = row.get("id")
        if not isinstance(task_id, str) or not task_id:
            raise ResultError(f"{path}: task result id must be non-empty text")
        if task_id in seen:
            raise ResultError(f"{path}: duplicate task result {task_id}")
        seen.add(task_id)

        for field in ("passed", "failed", "errors", "score"):
            value = row.get(field)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ResultError(
                    f"{path}: {task_id}.{field} must be a non-negative integer"
                )
        if row["score"] > 100:
            raise ResultError(f"{path}: {task_id}.score must be <= 100")

        failed_tests = row.get("failed_tests")
        if not isinstance(failed_tests, list) or not all(
            isinstance(name, str) for name in failed_tests
        ):
            raise ResultError(f"{path}: {task_id}.failed_tests must be a string list")

        infrastructure_error = row.get("infrastructure_error")
        if infrastructure_error is not None and not isinstance(infrastructure_error, str):
            raise ResultError(
                f"{path}: {task_id}.infrastructure_error must be text or null"
            )

        passed += row["passed"]
        failed += row["failed"]
        errors += row["errors"]

    if summary["tasks"] != len(rows):
        raise ResultError(f"{path}: summary.tasks does not match task result count")
    if summary["passed"] != passed or summary["failed"] != failed or summary["errors"] != errors:
        raise ResultError(f"{path}: summary counts do not match task results")

    return payload


def task_ids(payload: dict[str, Any]) -> list[str]:
    return [row["id"] for row in payload["tasks"]]


def ensure_comparable(
    payloads: list[tuple[Path, dict[str, Any]]],
    *,
    require_valid_runs: bool = True,
) -> tuple[str, str, list[str]]:
    if not payloads:
        raise ResultError("at least one result is required")

    first_path, first = payloads[0]
    benchmark_id = first["benchmark"]["id"]
    benchmark_version = first["benchmark"]["version"]
    ids = task_ids(first)
    id_set = set(ids)

    for path, payload in payloads:
        if payload["benchmark"]["id"] != benchmark_id:
            raise ResultError(
                f"{path}: benchmark id differs from {first_path}"
            )
        if payload["benchmark"]["version"] != benchmark_version:
            raise ResultError(
                f"{path}: benchmark version differs from {first_path}"
            )
        if set(task_ids(payload)) != id_set:
            raise ResultError(
                f"{path}: task set differs from {first_path}"
            )
        if require_valid_runs and payload["summary"]["errors"] != 0:
            raise ResultError(
                f"{path}: run has infrastructure/test execution errors"
            )
        if require_valid_runs and any(
            row.get("infrastructure_error") for row in payload["tasks"]
        ):
            raise ResultError(
                f"{path}: run contains infrastructure_error entries"
            )

    return benchmark_id, benchmark_version, ids
