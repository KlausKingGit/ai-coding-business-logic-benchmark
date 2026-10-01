# Comparing results and summarizing run history

v0.3 tooling can compare machine-readable results without re-running candidate code.

## Compare two runs

```bash
python -m evaluator.compare \
  reports/baseline.json \
  reports/candidate.json \
  --markdown-output reports/comparison.md \
  --json-output reports/comparison.json
```

The comparison includes aggregate score/count deltas and per-task score deltas.

## Summarize historical runs

Pass JSON files directly or a directory containing JSON reports:

```bash
python -m evaluator.history reports/history \
  --markdown-output reports/history.md \
  --json-output reports/history.json
```

## Comparability guard

By default, result tools refuse to compare runs when any of these differ:

- benchmark id;
- benchmark version;
- evaluated task set.

They also refuse runs containing infrastructure/test-execution errors.

This is intentional. A convenient table is not worth silently presenting non-comparable evidence as if it were comparable.
