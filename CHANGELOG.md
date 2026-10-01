# Changelog

## 0.2.0 - Unreleased

### Added

- external candidate directory evaluation with `--candidate-dir` and `--candidate-name`;
- optional machine-readable JSON reports;
- a reproducible `requirements.lock` and `environment.snapshot.json` for the Python 3.11/3.12 CI matrix;
- fixture-quality expectations that freeze minimum passing paths and target defect tests;
- Chinese README, contribution, benchmark-contract, task-authoring, result, reproducibility, fixture-quality, and security documentation;
- bounded external-code execution controls: sanitized environment inheritance and per-task timeout;
- JSON result schema.

### Changed

- CI now installs the validated lock snapshot and runs `pip check`;
- CI validates reference/flawed fixture quality from generated JSON results;
- post-release roadmap and documentation now reflect the published v0.1.0 state;
- external candidate results use the same ten canonical tests as repository fixtures.

### Security

- external candidate subprocesses no longer inherit arbitrary host environment variables by default;
- `--inherit-env NAME` provides explicit opt-in environment forwarding;
- external task execution has a default 30-second timeout;
- security documentation explicitly states that these protections are not a sandbox.

### Compatibility

- all ten v0.1.0 task IDs are retained;
- no canonical task, task test, reference implementation, or flawed implementation is removed;
- `--candidate reference`, `--candidate flawed`, and legacy `--candidate bad` remain supported;
- Markdown reports remain supported; JSON output is additive.

## 0.1.0 - 2026-10-01

First public OSS release.

### Benchmark

Includes ten deterministic, offline Python business-logic tasks:

1. order creation API — duplicate-write protection and API semantics;
2. payment reconciliation — deduplication and exact-money rules;
3. user quota — idempotent retries and original-response semantics;
4. payment webhook — retryability and failure atomicity;
5. AI summary validation — structured-output grounding;
6. inventory move atomicity — all-or-nothing multi-step state changes;
7. document authorization — authorization before mutation;
8. optimistic concurrency — stale-write rejection;
9. API contract drift — directional client/server compatibility;
10. unknown write outcome — no blind retry after uncertain external writes.

### OSS foundation

- benchmark manifest and per-task machine-readable metadata;
- benchmark/task JSON schemas;
- strict manifest validation;
- task listing and task-level selection in the evaluator runner;
- reference and deliberately flawed candidates using the same tests;
- Python 3.11 / 3.12 GitHub Actions CI;
- contribution guide and task-authoring guide;
- security policy;
- issue forms and pull-request template;
- changelog, roadmap, and compatibility contract;
- MIT license.
