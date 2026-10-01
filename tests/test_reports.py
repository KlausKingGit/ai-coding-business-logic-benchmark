from __future__ import annotations

import json

from evaluator.report import build_json_report, write_json_report


ROWS = [
    {
        "task": "task_01_example",
        "passed": 3,
        "failed": 1,
        "errors": 0,
        "score": 75,
        "failed_tests": ["test_business_rule"],
    },
    {
        "task": "task_02_example",
        "passed": 2,
        "failed": 0,
        "errors": 0,
        "score": 100,
        "failed_tests": [],
    },
]


def test_build_json_report_has_stable_machine_readable_shape():
    payload = build_json_report(
        benchmark_id="example-benchmark",
        benchmark_version="1.2.3",
        candidate_mode="external",
        candidate_name="agent-a",
        rows=ROWS,
    )

    assert payload["schema_version"] == "1.0"
    assert payload["benchmark"] == {"id": "example-benchmark", "version": "1.2.3"}
    assert payload["candidate"] == {"mode": "external", "name": "agent-a"}
    assert payload["summary"] == {
        "tasks": 2,
        "passed": 5,
        "failed": 1,
        "errors": 0,
        "score": 83,
    }
    assert payload["tasks"][0]["failed_tests"] == ["test_business_rule"]
    assert payload["environment"]["python"]


def test_write_json_report_round_trips(tmp_path):
    target = tmp_path / "nested" / "result.json"

    write_json_report(
        benchmark_id="example-benchmark",
        benchmark_version="1.2.3",
        candidate_mode="reference",
        candidate_name="reference",
        rows=ROWS,
        target=target,
    )

    payload = json.loads(target.read_text(encoding="utf-8"))
    assert payload["candidate"]["mode"] == "reference"
    assert payload["summary"]["score"] == 83
