# Evaluating external candidates

The benchmark can evaluate code produced outside this repository without modifying the ten canonical tasks or their tests.

## Candidate directory layout

Provide one Python module per task:

```text
my-agent-output/
  task_01_order_api.py
  task_02_payment_reconciliation.py
  task_03_user_quota.py
  task_04_webhook_idempotency.py
  task_05_ai_summary_validation.py
  task_06_inventory_move_atomicity.py
  task_07_document_authorization.py
  task_08_optimistic_concurrency.py
  task_09_api_contract_drift.py
  task_10_unknown_write_outcome.py
```

Each module must expose the public functions/classes expected by that task's existing tests. The task README and reference implementation document that interface.

## Run all tasks

```bash
python evaluator/runner.py \
  --candidate-dir ./my-agent-output \
  --candidate-name my-agent
```

## Run selected tasks

When `--task` is used, only the corresponding candidate files are required:

```bash
python evaluator/runner.py \
  --candidate-dir ./my-agent-output \
  --candidate-name my-agent \
  --task task_08_optimistic_concurrency
```

Repeat `--task` to select multiple tasks.

## Result semantics

A failed assertion is an evaluation result, not a runner failure.

The runner exits non-zero when test collection/execution is invalid or candidate code cannot be loaded. Markdown reports are written to the configured report directory.

External candidate support does not modify benchmark task semantics, reference implementations, flawed fixtures, or canonical tests.
