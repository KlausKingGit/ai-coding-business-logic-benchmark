# Roadmap

This roadmap describes benchmark evolution, not a target task count.

## Foundation

- [x] stable benchmark/task metadata contract;
- [x] contribution path;
- [x] CI;
- [x] compatibility rules;
- [x] ten-task first release;
- [x] first tagged benchmark release (v0.1.0);
- [x] Chinese documentation entry points;
- [ ] first external task contribution.

## v0.2 — External Evaluation Harness

- [x] evaluate external candidate directories;
- [x] reproducible dependency/environment snapshot;
- [x] machine-readable JSON results;
- [x] fixture-quality gates;
- [x] bounded handling and security guidance for external candidate code.

## v0.3 — Tooling and Integrations

Optimization sequence:

1. [x] comparable result diff and historical-run summaries;
2. [x] provider-neutral agent task bundles / adapters;
3. [x] contributor task scaffold generator;
4. [x] containerized execution path for stronger isolation.

No existing canonical task is planned for removal or weakening in this cycle.

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

Prefer a small transparent benchmark and harness over a large platform.
