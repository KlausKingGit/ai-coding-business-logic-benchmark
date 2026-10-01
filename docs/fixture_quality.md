# Fixture quality gates

The repository-provided flawed candidates are intended to be **plausible but wrong in a targeted way**.

A useful flawed fixture should not simply fail everything.

## Frozen expectations

`fixture_expectations.json` records, for every canonical task:

- the minimum number of tests the flawed candidate must continue to pass;
- the specific test(s) that must continue to fail because they expose the intended defect.

The reference candidate must continue to pass every test.

## CI validation

CI runs reference and flawed candidates once, emits JSON reports, and then validates those reports with:

```bash
python -m evaluator.fixture_check \
  --reference-json reference.json \
  --flawed-json flawed.json
```

This catches two important regressions:

1. a flawed fixture becomes too broken and stops representing plausible generated code;
2. a flawed fixture accidentally stops demonstrating the business-rule defect the task was created to test.

The quality file is separate from `task.json`, so the released task metadata contract does not need a breaking schema change.
