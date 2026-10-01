from __future__ import annotations

import json

import pytest

from evaluator.scaffold import ScaffoldError, write_scaffold


def test_scaffold_generates_canonical_shape_without_registering(tmp_path):
    output = tmp_path / "task_11_example"
    write_scaffold(
        output_dir=output,
        task_id="task_11_example",
        title="Example task",
        summary="Exercise one narrow invariant.",
        area="example-area",
        tags=["example", "state"],
    )

    expected = {
        "README.md",
        "task.json",
        "reference_solution.py",
        "flawed_candidate.py",
        "evaluation_notes.md",
        "fixture_expectation.example.json",
        "SCaffold_NEXT_STEPS.md",
    }
    assert expected.issubset({path.name for path in output.iterdir()})
    assert (output / "tests" / "test_cases.py").is_file()

    metadata = json.loads((output / "task.json").read_text(encoding="utf-8"))
    assert metadata["id"] == "task_11_example"
    assert metadata["tags"] == ["example", "state"]
    assert "TODO" in (output / "README.md").read_text(encoding="utf-8")
    assert "pytest.fail" in (output / "tests" / "test_cases.py").read_text(
        encoding="utf-8"
    )


def test_scaffold_rejects_existing_canonical_task(tmp_path):
    with pytest.raises(ScaffoldError, match="already exists"):
        write_scaffold(
            output_dir=tmp_path / "existing",
            task_id="task_01_order_api",
            title="Duplicate",
            summary="Should fail.",
            area="api-contract",
            tags=["api"],
        )


def test_scaffold_rejects_nonempty_output(tmp_path):
    output = tmp_path / "task"
    output.mkdir()
    (output / "keep.txt").write_text("keep", encoding="utf-8")

    with pytest.raises(ScaffoldError, match="not empty"):
        write_scaffold(
            output_dir=output,
            task_id="task_11_example",
            title="Example",
            summary="Example summary.",
            area="example-area",
            tags=["example"],
        )
