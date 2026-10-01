# v0.1.0 release candidate

This is the proposed first public release of the AI Coding Business-Logic Benchmark.

## Scope

The release contains ten deterministic, offline Python tasks that evaluate whether plausible generated code preserves specific backend business invariants.

It also establishes the repository-level OSS contract: stable task IDs, machine-readable metadata, strict manifest validation, transparent scoring, contribution guidance, compatibility rules, and CI on Python 3.11 and 3.12.

## What this release does not claim

This benchmark is intentionally small.

It does not claim to measure overall model intelligence, general software-engineering ability, production readiness, security completeness, or every kind of coding-agent failure.

Individual task fixtures may use in-memory state or simulated failures where that keeps the target invariant easy to inspect and reproduce.

## Release gates

Before creating the `v0.1.0` tag / GitHub Release:

- [x] ten tasks registered in the canonical manifest;
- [x] each task has reference/flawed candidates, tests, review notes, and task metadata;
- [x] strict manifest validation;
- [x] Python 3.11 CI;
- [x] Python 3.12 CI;
- [x] README / contribution / security / compatibility documentation;
- [x] MIT license;
- [ ] release-candidate PR merged to `main`;
- [ ] repository description updated to the benchmark positioning;
- [ ] repository rename decision finalized;
- [ ] `v0.1.0` tag created;
- [ ] GitHub Release published.

The unchecked items require an explicit release decision; this release-candidate branch does not perform them.
