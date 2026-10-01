# Adding a task

A good benchmark task is small enough to understand quickly and sharp enough to distinguish plausible code from correct code.

## 1. Choose one invariant

Start from a concrete failure mode such as:

- an identical retry must return the original response;
- a failed write with unknown outcome must not be blindly retried;
- authorization must be checked before mutation;
- a stale version must not overwrite newer state.

Avoid broad prompts such as "build a production payment system".

## 2. Choose the next stable ID

Use `task_NN_short_slug`. Do not reuse or renumber an existing ID.

## 3. Create canonical files

```text
tasks/task_NN_short_slug/
  README.md
  task.json
  reference_solution.py
  flawed_candidate.py
  evaluation_notes.md
  tests/test_cases.py
```

## 4. Make both candidates informative

The reference should be deliberately small. The flawed candidate should be plausible: ideally it passes the happy path and some edge cases but misses the target invariant.

## 5. Write discriminating tests

At least one test should fail for the flawed candidate for the reason described by the task. Tests must be deterministic and offline.

## 6. Add metadata and register the task

Copy an existing `task.json`, then append the task to `benchmark.json`.

## 7. Validate

```bash
python -m evaluator.manifest
python -m pytest -q
python evaluator/runner.py --candidate reference --task task_NN_short_slug
python evaluator/runner.py --candidate flawed --task task_NN_short_slug
```

## 8. Explain comparability

If you modify an existing task instead of adding one, explain whether old benchmark results remain comparable.
