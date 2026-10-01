"""Load and validate the benchmark manifest using only the standard library."""
from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_PATH = ROOT / "benchmark.json"
TASK_ID = re.compile(r"^task_\d{2}_[a-z0-9_]+$")
REQUIRED_TASK_FILES = (
    "README.md", "task.json", "reference_solution.py", "flawed_candidate.py",
    "evaluation_notes.md", "tests/test_cases.py",
)

@dataclass(frozen=True)
class TaskSpec:
    id: str
    title: str
    path: Path
    metadata: dict[str, Any]

class ManifestError(ValueError):
    pass

def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestError(f"missing manifest file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ManifestError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value

def _text(value: Any, field: str, path: Path) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{path.relative_to(ROOT)}: {field} must be non-empty text")
    return value

def load_benchmark(path: Path = BENCHMARK_PATH) -> tuple[dict[str, Any], list[TaskSpec]]:
    benchmark = _read_json(path)
    if benchmark.get("schema_version") != "1.0":
        raise ManifestError("benchmark.json: unsupported schema_version")
    _text(benchmark.get("benchmark_id"), "benchmark_id", path)
    _text(benchmark.get("benchmark_version"), "benchmark_version", path)
    tasks = benchmark.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ManifestError("benchmark.json: tasks must be a non-empty list")
    seen: set[str] = set()
    specs: list[TaskSpec] = []
    for item in tasks:
        if not isinstance(item, dict):
            raise ManifestError("benchmark.json: each task entry must be an object")
        task_id = _text(item.get("id"), "id", path)
        title = _text(item.get("title"), "title", path)
        if not TASK_ID.fullmatch(task_id):
            raise ManifestError(f"benchmark.json: invalid task id {task_id!r}")
        if task_id in seen:
            raise ManifestError(f"benchmark.json: duplicate task id {task_id}")
        seen.add(task_id)
        task_path = ROOT / "tasks" / task_id
        for relative in REQUIRED_TASK_FILES:
            if not (task_path / relative).is_file():
                raise ManifestError(f"{task_id}: missing {relative}")
        metadata_path = task_path / "task.json"
        metadata = _read_json(metadata_path)
        if metadata.get("schema_version") != "1.0":
            raise ManifestError(f"{task_id}: unsupported task schema_version")
        if metadata.get("id") != task_id or metadata.get("title") != title:
            raise ManifestError(f"{task_id}: manifest/task metadata mismatch")
        tags = metadata.get("tags")
        if not isinstance(tags, list) or not tags or len(tags) != len(set(tags)):
            raise ManifestError(f"{task_id}: tags must be a non-empty unique list")
        if metadata.get("candidates") != {"reference": "reference_solution.py", "flawed": "flawed_candidate.py"}:
            raise ManifestError(f"{task_id}: candidates mapping must use canonical filenames")
        if metadata.get("tests") != "tests/test_cases.py":
            raise ManifestError(f"{task_id}: tests must be tests/test_cases.py")
        if metadata.get("review_notes") != "evaluation_notes.md":
            raise ManifestError(f"{task_id}: review_notes must be evaluation_notes.md")
        if metadata.get("expected") != {"reference": "pass_all", "flawed": "fail_at_least_one"}:
            raise ManifestError(f"{task_id}: expected outcomes must use the benchmark contract")
        specs.append(TaskSpec(task_id, title, task_path, metadata))
    on_disk = {p.name for p in (ROOT / "tasks").glob("task_*") if p.is_dir()}
    unregistered = sorted(on_disk - seen)
    if unregistered:
        raise ManifestError("task directories missing from benchmark.json: " + ", ".join(unregistered))
    return benchmark, specs

def main() -> int:
    benchmark, tasks = load_benchmark()
    print(f"{benchmark['benchmark_id']} {benchmark['benchmark_version']}: {len(tasks)} tasks")
    for task in tasks:
        print(f"- {task.id}: {task.title}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
