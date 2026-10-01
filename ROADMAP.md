# Roadmap

This roadmap describes possible benchmark growth, not a promise to add every category.

## Foundation

- [x] stable benchmark/task metadata contract;
- [x] contribution path;
- [x] CI;
- [x] compatibility rules;
- [ ] first external task contribution;
- [ ] first tagged benchmark release.

## Candidate task families

- transactional consistency;
- authorization / permission boundaries;
- stale-state and optimistic-concurrency handling;
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
