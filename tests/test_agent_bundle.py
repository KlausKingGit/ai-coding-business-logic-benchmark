from __future__ import annotations

import json

import pytest

from evaluator.agent_bundle import BundleError, build_prompt, write_bundle
from evaluator.manifest import load_benchmark


def test_bundle_exports_selected_contract_without_reference_solution(tmp_path):
    benchmark, tasks = load_benchmark()
    selected = [task for task in tasks if task.id == "task_08_optimistic_concurrency"]

    output = tmp_path / "bundle"
    write_bundle(output, benchmark, selected)

    manifest = json.loads((output / "bundle.json").read_text(encoding="utf-8"))
    assert manifest["benchmark"]["version"] == benchmark["benchmark_version"]
    assert [task["id"] for task in manifest["tasks"]] == [
        "task_08_optimistic_concurrency"
    ]

    prompt = (
        output / "prompts" / "task_08_optimistic_concurrency.md"
    ).read_text(encoding="utf-8")
    assert "Optimistic concurrency" in prompt
    assert "candidate/task_08_optimistic_concurrency.py" in prompt
    assert "reference_solution.py" not in prompt
    assert (output / "candidate").is_dir()


def test_bundle_refuses_nonempty_output_directory(tmp_path):
    benchmark, tasks = load_benchmark()
    output = tmp_path / "bundle"
    output.mkdir()
    (output / "keep.txt").write_text("do not overwrite", encoding="utf-8")

    with pytest.raises(BundleError, match="not empty"):
        write_bundle(output, benchmark, tasks[:1])


def test_prompt_contains_public_contract_and_no_solution_source():
    _, tasks = load_benchmark()
    prompt = build_prompt(tasks[0])

    assert "# Agent task:" in prompt
    assert "Public task contract" in prompt
    assert "reference implementation is intentionally not included" in prompt
