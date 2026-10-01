# Changelog

## 0.3.0 - Unreleased

### Added

- task 09: directional API contract compatibility / drift detection;
- task 10: uncertain write outcome with no blind retry.

### Compatibility

- tasks 01–08 are unchanged;
- the benchmark runner and metadata contract are unchanged;
- the release is additive, so earlier task-level results remain comparable.

## 0.2.0 - Unreleased

### Added

- task 06: inventory move atomicity;
- task 07: authorization-before-mutation;
- task 08: optimistic concurrency / stale-write rejection.

### Compatibility

- tasks 01–05 are unchanged;
- the runner and manifest contract remain backward-compatible with 0.1.0;
- this release is additive, so earlier task-level results remain comparable.

## 0.1.0 - Unreleased

### Added

- formal benchmark manifest and per-task metadata;
- machine-readable benchmark/task schemas;
- manifest validation and task discovery;
- task filtering and listing in the evaluator runner;
- GitHub Actions CI for Python 3.11 and 3.12;
- contribution, security, issue, and pull-request guidance;
- MIT license;
- benchmark contract and task-authoring documentation.

### Compatibility

- the original five task IDs and tests are retained;
- `--candidate bad` remains available as an alias for `--candidate flawed`.
