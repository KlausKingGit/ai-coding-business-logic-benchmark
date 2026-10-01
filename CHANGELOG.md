# Changelog

## 0.2.0 - 2026-10-01

### Added

- external candidate directory evaluation with --candidate-dir and --candidate-name;
- optional machine-readable JSON reports and result schema;
- comparable result diff and historical-run summaries;
- comparison/history JSON schemas;
- provider-neutral agent task bundles with machine-readable bundle manifest;
- contributor task scaffold generator that does not auto-register unfinished tasks;
- a reproducible requirements.lock and environment.snapshot.json for the Python 3.11/3.12 CI matrix;
- fixture-quality expectations that freeze minimum passing paths and target defect tests;
- bilingual English/Chinese documentation for core usage, contribution, results, reproducibility, fixture quality, agent bundles, scaffolding, container isolation, and security;
- bounded external-code execution controls: sanitized environment inheritance and per-task timeout;
- containerized external-candidate execution with network disabled, read-only root filesystem, dropped capabilities, no-new-privileges, resource limits, and read-only candidate mount;
- GitHub Actions container smoke validation.

### Changed

- CI installs the validated lock snapshot and runs pip check;
- CI validates reference/flawed fixture quality from generated JSON results;
- external candidate results use the same ten canonical tests as repository fixtures;
- provider-specific agent integrations are kept outside the benchmark core through a provider-neutral bundle contract;
- result comparison refuses different benchmark versions, different task sets, or infrastructure-error runs.

### Security

- external candidate subprocesses do not inherit arbitrary host environment variables by default;
- --inherit-env NAME provides explicit opt-in environment forwarding for direct host execution;
- external task execution has a default 30-second timeout;
- the Docker wrapper disables networking, drops capabilities, enables no-new-privileges, applies PID/memory/CPU/file-descriptor limits, and uses a bounded tmpfs;
- documentation explicitly states that containers provide stronger isolation but are not a perfect sandbox.

### Compatibility

- all ten v0.1.0 task IDs are retained;
- no canonical task, task test, reference implementation, or flawed implementation is removed or changed;
- --candidate reference, --candidate flawed, and legacy --candidate bad remain supported;
- Markdown reports remain supported; JSON output is additive;
- v0.1.0 tag/release remains unchanged.

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
