from __future__ import annotations

from pathlib import Path

import pytest

from evaluator.compare import build_comparison
from evaluator.history import build_history
from evaluator.result_io import ResultError, ensure_comparable


def result(name: str, scores: list[tuple[str, int, int]]) -> dict:
    rows = []
    passed = failed = 0
    for task_id, p, f in scores:
        passed += p
        failed += f
        total = p + f
        rows.append(
            {
                "id": task_id,
                "passed": p,
                "failed": f,
                "errors": 0,
                "score": round(100 * p / total),
                "failed_tests": [],
                "infrastructure_error": None,
            }
        )
    total = passed + failed
    return {
        "schema_version": "1.0",
        "benchmark": {"id": "bench", "version": "0.2.0"},
        "candidate": {"mode": "external", "name": name},
        "environment": {
            "python": "3.12.14",
            "implementation": "CPython",
            "platform": "linux",
        },
        "summary": {
            "tasks": len(rows),
            "passed": passed,
            "failed": failed,
            "errors": 0,
            "score": round(100 * passed / total),
        },
        "tasks": rows,
    }


def test_comparison_computes_aggregate_and_task_deltas():
    baseline = result("a", [("task_01_x", 8, 2), ("task_02_x", 5, 5)])
    candidate = result("b", [("task_01_x", 9, 1), ("task_02_x", 7, 3)])

    comparison = build_comparison(baseline, candidate)

    assert comparison["delta"]["score"] == 15
    assert comparison["tasks"][0]["score_delta"] == 10
    assert comparison["tasks"][1]["score_delta"] == 20


def test_history_keeps_input_order():
    first = result("first", [("task_01_x", 8, 2)])
    second = result("second", [("task_01_x", 9, 1)])

    history = build_history(
        [(Path("first.json"), first), (Path("second.json"), second)]
    )

    assert [run["candidate"]["name"] for run in history["runs"]] == [
        "first",
        "second",
    ]


def test_comparability_rejects_different_benchmark_version():
    first = result("first", [("task_01_x", 8, 2)])
    second = result("second", [("task_01_x", 8, 2)])
    second["benchmark"]["version"] = "0.3.0"

    with pytest.raises(ResultError, match="version differs"):
        ensure_comparable(
            [(Path("first.json"), first), (Path("second.json"), second)]
        )


def test_comparability_rejects_different_task_sets():
    first = result("first", [("task_01_x", 8, 2)])
    second = result("second", [("task_02_x", 8, 2)])

    with pytest.raises(ResultError, match="task set differs"):
        ensure_comparable(
            [(Path("first.json"), first), (Path("second.json"), second)]
        )


def test_comparability_rejects_infrastructure_errors():
    first = result("first", [("task_01_x", 8, 2)])
    first["summary"]["errors"] = 1
    first["tasks"][0]["errors"] = 1

    with pytest.raises(ResultError, match="infrastructure"):
        ensure_comparable([(Path("first.json"), first)])
