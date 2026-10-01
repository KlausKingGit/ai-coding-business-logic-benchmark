# v0.1.0 release notes

Released on 2026-10-01 as the first public OSS release of the **AI Coding Business-Logic Benchmark**.

## Scope

The release contains ten deterministic, offline Python tasks that evaluate whether plausible generated code preserves specific backend business invariants.

It also establishes the repository-level OSS contract: stable task IDs, machine-readable metadata, strict manifest validation, transparent scoring, contribution guidance, compatibility rules, and CI on Python 3.11 and 3.12.

## What this release does not claim

This benchmark is intentionally small.

It does not claim to measure overall model intelligence, general software-engineering ability, production readiness, security completeness, or every kind of coding-agent failure.

Individual task fixtures may use in-memory state or simulated failures where that keeps the target invariant easy to inspect and reproduce.

## Release status

All first-release gates were completed:

- [x] ten tasks registered in the canonical manifest;
- [x] each task has reference/flawed candidates, tests, review notes, and task metadata;
- [x] strict manifest validation;
- [x] Python 3.11 CI;
- [x] Python 3.12 CI;
- [x] README / contribution / security / compatibility documentation;
- [x] MIT license;
- [x] release-candidate PR merged to `main`;
- [x] repository description updated to the benchmark positioning;
- [x] repository renamed to `ai-coding-business-logic-benchmark`;
- [x] `v0.1.0` tag created;
- [x] GitHub Release published.

The `v0.1.0` tag points to commit:

`f3419f753082368eb3c0574022600a0c7f52b952`

The published release is:

`v0.1.0 — First OSS Release`

## Post-release note

This file on `main` was updated after publication so it reflects the completed release state rather than the pre-release checklist.

The `v0.1.0` tag remains the immutable release snapshot and is not changed by this documentation housekeeping.
