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

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python -m pytest -q
python -m evaluator.manifest
python evaluator/runner.py --list-tasks
python evaluator/runner.py --candidate reference
python evaluator/runner.py --candidate flawed
```

The legacy CLI spelling `--candidate bad` remains supported for compatibility.

Run one task:

```bash
python evaluator/runner.py --candidate flawed --task task_10_unknown_write_outcome
```

## Current benchmark

Benchmark version: **0.1.0**

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

The reference candidate must pass all task tests. The flawed candidate must remain plausible enough to pass at least one meaningful path while failing one or more tests that expose the intended business-rule defect.

See [Benchmark contract](docs/benchmark_contract.md). A Chinese companion is available at [基准契约说明](docs/benchmark_contract.zh-CN.md).

## Contributing a task

New task contributions are welcome. Start with [Adding a task](docs/adding_a_task.md) and [CONTRIBUTING.md](CONTRIBUTING.md). Chinese companions are available in [添加任务说明](docs/adding_a_task.zh-CN.md) and [贡献指南](CONTRIBUTING.zh-CN.md).

Task IDs are not renumbered after release.

## Scoring

The included runner reports `round(100 × passed / (passed + failed))`.

Collection errors invalidate a run. Passing tests does not establish production readiness, security, maintainability, or complete semantic correctness.

## CI

GitHub Actions validates manifest/task metadata, the full pytest suite, the reference candidate, and the deliberately flawed candidate as an evaluation fixture on Python 3.11 and 3.12.

## Known limits

The tasks are deliberately compact fixtures. Several use in-memory state and simulated failures. They do not claim durable multi-process guarantees, distributed transactions, real webhook authentication, or exhaustive LLM-output verification.

## Roadmap

Future additions should be driven by concrete contribution needs rather than task-count targets. See [ROADMAP.md](ROADMAP.md).

## License

MIT. See [LICENSE](LICENSE).
