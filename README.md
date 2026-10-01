# AI Coding Business-Logic Benchmark

[中文说明](README.zh-CN.md)

A small, reproducible benchmark for evaluating whether AI-generated Python code preserves backend business rules — not just whether it runs.

This project evolved from an initial five-task evaluation demo into a reusable OSS benchmark that other people can run, extend, review, and maintain.

## What this benchmark measures

The current tasks target failure modes that are easy for plausible code to miss:

- duplicate-write protection and API error semantics;
- payment reconciliation, deduplication, and exact money handling;
- idempotent retries that must return the original response;
- webhook retryability and failure atomicity;
- structured AI output validated against source facts;
- multi-step state changes that must remain atomic on failure;
- authorization checks that must happen before mutation;
- stale writes that must not overwrite newer state;
- API changes that silently break an existing client contract;
- uncertain write outcomes that must not be blindly retried.

Each task contains a human-readable contract, a reference implementation, a deliberately flawed but plausible implementation, the same pytest suite for both implementations, human review notes, and machine-readable task metadata.

## Quick start

Requires Python 3.11+.

For the continuously validated Python 3.11/3.12 environment, install the lock snapshot:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python -m pip check

python -m pytest -q
python -m evaluator.manifest
python evaluator/runner.py --list-tasks
python evaluator/runner.py --candidate reference
python evaluator/runner.py --candidate flawed
```

Use `requirements.txt` when you want the declared compatible dependency ranges rather than the exact CI snapshot. See [Reproducible environment](docs/reproducibility.md).

## Evaluate your own AI-generated code

Put one Python file per task in a candidate directory, then point the runner at it:

```bash
python evaluator/runner.py \
  --candidate-dir ./my-agent-output \
  --candidate-name my-agent \
  --json-report reports/my-agent.json
```

You can evaluate only selected tasks with repeated `--task` arguments. External candidates use the same canonical tests as the repository-provided reference and flawed fixtures.

**External candidate code is executed Python.** The runner sanitizes inherited environment variables and applies a per-task timeout, but it is not a sandbox. Use isolated infrastructure for code you do not trust.

See:

- [Evaluating external candidates](docs/external_candidates.md) / [中文](docs/external_candidates.zh-CN.md)
- [Machine-readable results](docs/results.md) / [中文](docs/results.zh-CN.md)
- [Safe execution](docs/safe_execution.md) / [中文](docs/safe_execution.zh-CN.md)

## Stronger isolation with Docker

For untrusted external candidates, the repository includes a containerized execution path:

    docker build -f containers/Dockerfile -t ai-coding-business-logic-benchmark:local .
    scripts/run_candidate_container.sh ./my-agent-output my-agent

The wrapper disables networking, uses a read-only root filesystem, drops capabilities, enables no-new-privileges, applies resource limits, and mounts candidate code read-only.

See [Containerized execution](docs/container_execution.md) or the [中文说明](docs/container_execution.zh-CN.md).

## Current benchmark

Benchmark version: **0.2.0**

| Task | Primary invariant | Selected tags |
|---|---|---|
| `task_01_order_api` | Duplicate orders must not overwrite stored state | API, validation, duplicate write |
| `task_02_payment_reconciliation` | Repeated payment IDs must not be counted twice | reconciliation, money, deduplication |
| `task_03_user_quota` | Identical retries return the original result | idempotency, retry semantics, concurrency |
| `task_04_webhook_idempotency` | Failed processing remains retryable | webhook, failure atomicity, logging |
| `task_05_ai_summary_validation` | Structured output must match source facts | structured output, schema, grounding |
| `task_06_inventory_move_atomicity` | A failed movement record must not leave stock half-mutated | transaction, atomicity, rollback |
| `task_07_document_authorization` | Authorization denial must happen before mutation | authorization, mutation ordering |
| `task_08_optimistic_concurrency` | A stale version must not overwrite newer state | concurrency, stale state, versioning |
| `task_09_api_contract_drift` | Server changes must preserve the compatibility guarantees an existing client relies on | API contract, compatibility, drift |
| `task_10_unknown_write_outcome` | A timeout after an uncertain write must not trigger a blind retry | partial failure, unknown outcome, retry |

The canonical task order and benchmark version live in [`benchmark.json`](benchmark.json). Each task has its own `task.json`.

## Reproducibility contract

A valid task must have:

```text
tasks/task_NN_slug/
  README.md
  task.json
  reference_solution.py
  flawed_candidate.py
  evaluation_notes.md
  tests/test_cases.py
```

The reference candidate must pass all task tests. The flawed candidate must remain plausible enough to pass meaningful paths while failing the target tests that expose the intended business-rule defect.

See:

- [Benchmark contract](docs/benchmark_contract.md) / [中文](docs/benchmark_contract.zh-CN.md)
- [Fixture quality gates](docs/fixture_quality.md) / [中文](docs/fixture_quality.zh-CN.md)

## Contributing a task

New task contributions are welcome. Start with [Adding a task](docs/adding_a_task.md) and [CONTRIBUTING.md](CONTRIBUTING.md). Chinese companions are available in [添加任务说明](docs/adding_a_task.zh-CN.md) and [贡献指南](CONTRIBUTING.zh-CN.md).

Task IDs are not renumbered after release.

## Scoring and result formats

The included runner reports `round(100 × passed / (passed + failed))`.

Collection/execution errors invalidate a run. Passing tests does not establish production readiness, security, maintainability, or complete semantic correctness.

Markdown reports remain the human-readable default. Use `--json-report` for machine-readable output.

## CI

GitHub Actions validates on Python 3.11 and 3.12:

- locked dependency installation and `pip check`;
- benchmark manifest;
- full pytest suite;
- reference fixture;
- flawed fixture;
- fixture-quality expectations.

## Known limits

The tasks are deliberately compact fixtures. Several use in-memory state and simulated failures. They do not claim durable multi-process guarantees, distributed transactions, real webhook authentication, or exhaustive LLM-output verification.

## Roadmap

Future additions should be driven by concrete contribution needs rather than task-count targets. See [ROADMAP.md](ROADMAP.md).

## License

MIT. See [LICENSE](LICENSE).
