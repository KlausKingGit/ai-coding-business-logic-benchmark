# Roadmap

This roadmap describes possible benchmark growth, not a promise to add every category.

## Foundation

- [x] stable benchmark/task metadata contract;
- [x] contribution path;
- [x] CI;
- [x] compatibility rules;
- [x] ten-task first-release scope;
- [x] first-release candidate assembled;
- [ ] first tagged benchmark release;
- [ ] first external task contribution.

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

## Candidate task families

Future tasks should be added because they represent a useful, discriminating invariant — not to increase task count.

Possible families:

- pagination / cursor correctness;
- durable idempotency versus in-memory idempotency;
- retry budgets and bounded backoff;
- state-machine transition legality;
- cross-resource consistency.

## Later tooling

Only add tooling when contributors need it:

- machine-readable JSON evaluation output;
- benchmark-result comparison;
- task-level timing metadata;
- optional adapters for evaluating externally generated patches.

Prefer a small transparent runner over a large benchmark platform.
