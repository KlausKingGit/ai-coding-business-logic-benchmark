from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from shared.candidate import load

ROOT = Path(__file__).resolve().parents[1]


def test_loader_imports_external_candidate(tmp_path, monkeypatch):
    (tmp_path / "task_99_example.py").write_text("VALUE = 42\n", encoding="utf-8")
    monkeypatch.setenv("EVAL_CANDIDATE", "external")
    monkeypatch.setenv("EVAL_CANDIDATE_DIR", str(tmp_path))

    module = load("task_99_example")

    assert module.VALUE == 42


def test_loader_reports_missing_external_file(tmp_path, monkeypatch):
    monkeypatch.setenv("EVAL_CANDIDATE", "external")
    monkeypatch.setenv("EVAL_CANDIDATE_DIR", str(tmp_path))

    with pytest.raises(FileNotFoundError, match="task_99_missing.py"):
        load("task_99_missing")


def test_runner_evaluates_external_candidate_directory(tmp_path):
    candidate_dir = tmp_path / "candidate"
    candidate_dir.mkdir()
    source = ROOT / "tasks" / "task_08_optimistic_concurrency" / "reference_solution.py"
    (candidate_dir / "task_08_optimistic_concurrency.py").write_text(
        source.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    report_dir = tmp_path / "reports"
    json_report = tmp_path / "result.json"

    result = subprocess.run(
        [
            sys.executable,
            "evaluator/runner.py",
            "--candidate-dir",
            str(candidate_dir),
            "--candidate-name",
            "test-agent",
            "--task",
            "task_08_optimistic_concurrency",
            "--report-dir",
            str(report_dir),
            "--json-report",
            str(json_report),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        env={k: v for k, v in os.environ.items() if k not in {"EVAL_CANDIDATE", "EVAL_CANDIDATE_DIR"}},
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Candidate: test-agent" in result.stdout
    assert "task_08_optimistic_concurrency" in result.stdout
    assert (report_dir / "external-test-agent.selected.md").is_file()

    payload = json.loads(json_report.read_text(encoding="utf-8"))
    assert payload["candidate"] == {"mode": "external", "name": "test-agent"}
    assert payload["summary"]["tasks"] == 1
    assert payload["summary"]["score"] == 100
