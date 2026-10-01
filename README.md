# AI Coding Business-Logic Benchmark

A small, reproducible benchmark for evaluating whether AI-generated Python code preserves backend business rules — not just whether it runs.

This repository started as a five-task evaluation demo. The repository name is retained for continuity, but the project is now organized as a reusable OSS benchmark that other people can run, extend, review, and maintain.

## What this benchmark measures

The current tasks target failure modes that are easy for plausible code to miss:

- duplicate-write protection and API error semantics;
- payment reconciliation, deduplication, and exact money handling;
- idempotent retries that must return the original response;
- webhook retryability and failure atomicity;
- structured AI output validated against source facts;
- multi-step state changes that must remain atomic on failure;
- authorization checks that must happen before mutation;
- stale writes that must not overwrite newer state.

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
python evaluator/runner.py --candidate flawed --task task_03_user_quota
```

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

See [Benchmark contract](docs/benchmark_contract.md).

## Contributing a task

New task contributions are welcome. Start with [Adding a task](docs/adding_a_task.md) and [CONTRIBUTING.md](CONTRIBUTING.md). Task IDs are not renumbered after release.

## Scoring

The included runner reports `round(100 × passed / (passed + failed))`.

Collection errors invalidate a run. Passing tests does not establish production readiness, security, maintainability, or complete semantic correctness.

## CI

GitHub Actions validates manifest/task metadata, the full pytest suite, the reference candidate, and the deliberately flawed candidate as an evaluation fixture.

## Known limits

The tasks are deliberately compact fixtures. Several use in-memory state and simulated failures. They do not claim durable multi-process guarantees, distributed transactions, real webhook authentication, or exhaustive LLM-output verification.

## Roadmap

Potential future task families include API contract drift, partial-failure / unknown-outcome semantics, pagination/cursor correctness, and durable idempotency. See [ROADMAP.md](ROADMAP.md).

## License

MIT. See [LICENSE](LICENSE).
