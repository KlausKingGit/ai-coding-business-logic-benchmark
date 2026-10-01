# Security policy

This repository contains offline benchmark fixtures and an evaluation harness, not a production service.

## External candidate code is executable code

`--candidate-dir` imports and executes Python supplied by the evaluator.

Treat external or AI-generated candidate code as untrusted unless you have reviewed it.

The runner applies two bounded protections by default:

- external candidates receive a sanitized environment instead of the full host environment;
- each task has a default 30-second pytest timeout.

These protections reduce accidental exposure and hangs. **They are not a sandbox.**

External candidate code can still attempt to:

- read files accessible to the current OS user;
- write files where the current user has permission;
- consume CPU or memory;
- access the network unless the host environment blocks it;
- spawn child processes where allowed by the operating system.

For code you do not trust, run the benchmark inside a disposable container, VM, CI job, or other sandbox that contains no sensitive credentials or data.

Use `--inherit-env NAME` only when a candidate explicitly requires that variable and you accept that the candidate can read its value.

## Repository hygiene

Do not publish credentials, customer data, private source code, proprietary prompts, or production endpoints in issues, candidate fixtures, or pull requests.

## Reporting a security issue

If you discover a vulnerability in benchmark tooling that could unexpectedly execute code, expose secrets, escape an intended isolation boundary, or affect contributors running the repository, use GitHub private vulnerability reporting/security advisories when available.

Otherwise contact the maintainer privately instead of posting exploit details publicly.

A useful report includes the affected path, reproduction steps, impact, and any safe mitigation you have identified.

## Containerized isolation path

For stronger isolation, use the repository Docker path documented in docs/container_execution.md.

The wrapper disables networking, uses a read-only root filesystem, drops Linux capabilities, enables no-new-privileges, sets resource limits, and mounts the candidate read-only.

This is still not a perfect sandbox. Linux containers share the host kernel, and container/runtime/kernel vulnerabilities remain outside the benchmark's guarantees.
