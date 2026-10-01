# Benchmark contract

The benchmark is designed around deterministic evidence, stable task identity, and explicit limits.

## Task identity

A released task ID is stable. Do not renumber tasks to make the directory list prettier. The canonical order is the order in `benchmark.json`.

## Candidate roles

Each task has two repository-provided candidates:

- **reference** — expected to pass all task tests;
- **flawed** — deliberately plausible and expected to fail at least one targeted test.

The flawed candidate should not be maximally broken. If it fails every meaningful path, it is less useful as an evaluation fixture.

## Test contract

Tests should encode observable behavior from the task contract and prefer business invariants over implementation details.

Examples:

- did a duplicate request mutate state?
- did a retry return the original result?
- did a failed webhook become permanently marked as done?
- did structured output introduce a fact not present in source data?

## Offline and deterministic by default

Tasks must not require network access, live APIs, external accounts, credentials, or time-sensitive data.

## Scoring

The default score is `round(100 × passed / (passed + failed))`. Collection or execution errors invalidate the run.

The score does not measure readability, production security, latency, architecture quality, or untested semantics.

## Versioning

`benchmark_version` follows semantic-versioning intent:

- patch: documentation/infrastructure changes with no intended benchmark-outcome change;
- minor: additive tasks or backward-compatible evaluation features;
- major: incompatible task semantics, scoring rules, or manifest-contract changes.

Before 1.0, compatibility-sensitive changes should still be called out explicitly in `CHANGELOG.md`.

## Historical comparability

A change that makes old and new scores non-comparable must say so. Do not silently edit a core invariant and continue presenting prior scores as the same benchmark.
