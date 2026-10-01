from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

import pytest

from evaluator.runner import _build_candidate_env

ROOT = Path(__file__).resolve().parents[1]


def test_external_environment_does_not_inherit_unrelated_secret(monkeypatch, tmp_path):
    monkeypatch.setenv("BENCHMARK_TEST_SECRET", "do-not-pass")
    monkeypatch.setenv("PATH", os.environ.get("PATH", ""))

    env = _build_candidate_env(
        candidate_mode="external",
        external_dir=tmp_path,
        inherit_env=[],
    )

    assert "BENCHMARK_TEST_SECRET" not in env
    assert env["EVAL_CANDIDATE"] == "external"
    assert env["EVAL_CANDIDATE_DIR"] == str(tmp_path)


def test_external_environment_can_explicitly_inherit_named_variable(monkeypatch, tmp_path):
    monkeypatch.setenv("BENCHMARK_PUBLIC_SETTING", "explicit")

    env = _build_candidate_env(
        candidate_mode="external",
        external_dir=tmp_path,
        inherit_env=["BENCHMARK_PUBLIC_SETTING"],
    )

    assert env["BENCHMARK_PUBLIC_SETTING"] == "explicit"


def test_reserved_external_control_variable_cannot_be_overridden(monkeypatch, tmp_path):
    monkeypatch.setenv("EVAL_CANDIDATE", "attacker-value")

    with pytest.raises(ValueError, match="reserved"):
        _build_candidate_env(
            candidate_mode="external",
            external_dir=tmp_path,
            inherit_env=["EVAL_CANDIDATE"],
        )


def test_external_candidate_timeout_is_runner_error(tmp_path):
    candidate_dir = tmp_path / "candidate"
    candidate_dir.mkdir()
    (candidate_dir / "task_08_optimistic_concurrency.py").write_text(
        "while True:\n    pass\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "evaluator/runner.py",
            "--candidate-dir",
            str(candidate_dir),
            "--task",
            "task_08_optimistic_concurrency",
            "--task-timeout-seconds",
            "0.2",
            "--report-dir",
            str(tmp_path / "reports"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=10,
    )

    assert result.returncode == 2
    assert "timed out after 0.2 seconds" in result.stdout
