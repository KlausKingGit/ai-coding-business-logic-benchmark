# Roadmap

This roadmap describes benchmark evolution, not a target task count.

## Foundation

- [x] stable benchmark/task metadata contract;
- [x] contribution path;
- [x] CI;
- [x] compatibility rules;
- [x] ten-task first release;
- [x] first tagged benchmark release (`v0.1.0`);
- [x] Chinese documentation entry points;
- [ ] first external task contribution.

## v0.2 — External Evaluation Harness

Optimization sequence:

1. [x] evaluate external candidate directories without changing the ten canonical tasks;
2. [x] record a reproducible dependency/environment snapshot;
3. [x] emit machine-readable JSON results;
4. [x] enforce stronger fixture-quality gates for reference/flawed candidates;
5. [x] document and enforce bounded handling of external candidate code.

No existing task is planned for removal as part of this optimization cycle.

## Covered task families

- duplicate writes and API semantics;
- reconciliation and exact money;
- idempotent retries;
- webhook failure atomicity;
- structured-output grounding;
- transactional atomicity;
- authorization-before-mutation;
- stale-state / optimistic concurrency;
- API contract compatibility / drift;
- uncertain write outcome / no blind retry.

## Later tooling

Only add tooling when contributors need it:

- result comparison and historical-run summaries;
- optional adapters for AI coding agents;
- task-level timing metadata;
- stronger OS/container sandbox integrations.

Prefer a small transparent runner over a large benchmark platform.
