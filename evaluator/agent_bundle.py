"""Export provider-neutral task bundles for AI coding agents."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evaluator.manifest import ManifestError, TaskSpec, load_benchmark


class BundleError(ValueError):
    pass


def build_prompt(task: TaskSpec) -> str:
    contract = (task.path / "README.md").read_text(encoding="utf-8").strip()
    tags = ", ".join(task.metadata["tags"])
    return (
        f"# Agent task: {task.id} — {task.title}\n\n"
        "Implement the task as a standalone Python module.\n\n"
        "## Output contract\n\n"
        f"- Write the complete implementation to: candidate/{task.id}.py\n"
        "- Preserve the public functions/classes required by the task contract.\n"
        "- Do not modify benchmark tests or benchmark metadata.\n"
        "- Do not depend on network access, secrets, or external services.\n"
        "- Keep scope limited to the stated task.\n\n"
        "The benchmark reference implementation is intentionally not included in this bundle.\n\n"
        f"Area: {task.metadata['area']}\n"
        f"Tags: {tags}\n\n"
        "## Public task contract\n\n"
        f"{contract}\n"
    )


def build_manifest(benchmark: dict, tasks: list[TaskSpec]) -> dict:
    return {
        "schema_version": "1.0",
        "benchmark": {
            "id": benchmark["benchmark_id"],
            "version": benchmark["benchmark_version"],
        },
        "candidate_directory": "candidate",
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "prompt": f"prompts/{task.id}.md",
                "candidate": f"candidate/{task.id}.py",
            }
            for task in tasks
        ],
    }


def write_bundle(output_dir: Path, benchmark: dict, tasks: list[TaskSpec]) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise BundleError(f"output directory is not empty: {output_dir}")

    prompts = output_dir / "prompts"
    candidate = output_dir / "candidate"
    prompts.mkdir(parents=True, exist_ok=True)
    candidate.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest(benchmark, tasks)
    (output_dir / "bundle.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    for task in tasks:
        (prompts / f"{task.id}.md").write_text(
            build_prompt(task),
            encoding="utf-8",
        )

    task_lines = "\n".join(
        f"- {task.id} -> candidate/{task.id}.py" for task in tasks
    )
    (output_dir / "README.md").write_text(
        "# AI coding agent bundle\n\n"
        f"Benchmark: {benchmark['benchmark_id']} "
        f"{benchmark['benchmark_version']}\n\n"
        "This bundle is provider-neutral. Feed each file in prompts/ to the "
        "coding agent of your choice and save its Python output to the matching "
        "path in candidate/.\n\n"
        "The bundle intentionally excludes repository reference/flawed "
        "implementations.\n\n"
        "## Expected outputs\n\n"
        f"{task_lines}\n\n"
        "## Evaluate\n\n"
        "From the benchmark repository, run:\n\n"
        "    python evaluator/runner.py --candidate-dir /path/to/this-bundle/candidate "
        "--candidate-name my-agent --json-report reports/my-agent.json\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--task",
        action="append",
        dest="task_ids",
        help="export only this task id; repeat for multiple tasks",
    )
    args = parser.parse_args()

    try:
        benchmark, tasks = load_benchmark()
    except ManifestError as exc:
        parser.error(str(exc))

    if args.task_ids:
        wanted = set(args.task_ids)
        known = {task.id for task in tasks}
        unknown = sorted(wanted - known)
        if unknown:
            parser.error("unknown task id(s): " + ", ".join(unknown))
        tasks = [task for task in tasks if task.id in wanted]

    try:
        write_bundle(args.output_dir, benchmark, tasks)
    except BundleError as exc:
        parser.error(str(exc))

    print(f"Agent bundle: {args.output_dir}")
    print(f"Tasks: {len(tasks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
