# Changelog

## 0.1.0 - Release candidate

First public OSS release candidate.

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

### Compatibility

- the original five task IDs and test semantics are retained;
- `--candidate bad` remains available as a compatibility alias for `--candidate flawed`;
- no earlier public benchmark release is claimed: the temporary 0.2.0/0.3.0 development labels were never released and are intentionally collapsed into this first 0.1.0 candidate.
