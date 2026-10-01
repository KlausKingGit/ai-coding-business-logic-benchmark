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

## Next release — v0.2.0

The unreleased v0.2.0 candidate now includes:

- [x] external candidate directories;
- [x] reproducible dependency/environment snapshot;
- [x] machine-readable JSON results;
- [x] fixture-quality gates;
- [x] bounded host execution and security guidance;
- [x] comparable result diff and historical-run summaries;
- [x] provider-neutral agent task bundles;
- [x] contributor task scaffold generator;
- [x] containerized execution with stronger isolation and CI smoke validation.

No existing canonical task is removed or weakened in this release candidate.

## Future directions

Only add tooling when real usage justifies it:

- first external task contribution;
- optional thin provider-specific agent wrappers built on the bundle contract;
- task-level timing and performance metadata;
- stronger VM/sandbox integrations for higher-risk code;
- result dashboards only after there is enough real run history to justify them.

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
