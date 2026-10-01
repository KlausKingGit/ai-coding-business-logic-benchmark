# Roadmap

This roadmap describes possible benchmark growth, not a promise to add every category.

## Foundation

- [x] stable benchmark/task metadata contract;
- [x] contribution path;
- [x] CI;
- [x] compatibility rules;
- [x] first additive task pack;
- [ ] first external task contribution;
- [ ] first tagged benchmark release.

## Covered task families

- duplicate writes and API semantics;
- reconciliation and exact money;
- idempotent retries;
- webhook failure atomicity;
- structured-output grounding;
- transactional atomicity;
- authorization-before-mutation;
- stale-state / optimistic concurrency.

## Candidate task families

- API contract drift;
- partial failure and unknown outcomes;
- retry after uncertain writes;
- pagination / cursor correctness;
- durable idempotency versus in-memory idempotency.

## Later tooling

Only add tooling when contributors need it:

- machine-readable JSON evaluation output;
- benchmark-result comparison;
- task-level timing metadata;
- optional adapters for evaluating externally generated patches.

Prefer a small transparent runner over a large benchmark platform.
