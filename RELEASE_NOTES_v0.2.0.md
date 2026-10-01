# v0.2.0 release notes

v0.2.0 turns the original benchmark corpus into an **external evaluation harness** while retaining all ten canonical v0.1.0 tasks.

## External candidate evaluation

Users can evaluate their own AI-generated Python implementations with:

```bash
python evaluator/runner.py \
  --candidate-dir ./my-agent-output \
  --candidate-name my-agent \
  --json-report reports/my-agent.json
```

The external candidate modules are exercised by the same canonical tests used for the repository fixtures.

## Reproducibility

- `requirements.txt` continues to declare compatible dependency ranges.
- `requirements.lock` captures the validated Python 3.11/3.12 dependency graph.
- `environment.snapshot.json` records the CI environment used to validate that lock.
- CI installs the lock and runs `pip check`.

## Machine-readable results

The runner can emit JSON containing:

- benchmark id/version;
- candidate mode/name;
- runtime environment;
- aggregate score/counts;
- per-task results and failed-test identifiers;
- infrastructure-error state.

The result contract is documented by `schemas/result.schema.json`.

## Fixture quality gates

Repository flawed fixtures now have frozen quality expectations:

- a minimum number of normal paths must remain passing;
- specific target defect tests must remain failing;
- reference fixtures must remain fully passing.

This prevents a flawed candidate from silently becoming either too broken or accidentally correct.

## External-code safety

External candidate execution now:

- uses a sanitized child environment by default;
- supports explicit `--inherit-env NAME` opt-in;
- applies a per-task timeout (30 seconds by default);
- records timeout/infrastructure errors in reports.

These controls are bounded protections, **not a sandbox**. Untrusted code should still run inside an external isolation boundary.

## Chinese documentation

v0.2 adds Chinese companion documentation for the README, contributing flow, benchmark contract, task authoring, external candidates, results, reproducibility, fixture quality, and security guidance.

## Compatibility

- all ten v0.1.0 tasks are retained;
- task IDs are unchanged;
- canonical task tests and business invariants are unchanged;
- existing reference/flawed CLI modes remain supported;
- Markdown report output remains supported;
- JSON reporting and external candidates are additive harness features.


## Result comparison and history

v0.2 can compare two valid JSON runs and summarize a directory of comparable historical runs without re-executing candidate code.

Comparison refuses different benchmark versions, different evaluated task sets, and runs containing infrastructure errors.

## Provider-neutral agent bundles

The agent-bundle exporter creates one public-contract prompt per selected task plus a machine-readable output mapping and candidate directory.

Reference/flawed source is intentionally excluded from exported prompts, and the benchmark core remains independent from vendor SDKs or API credentials.

## Contributor scaffold

The scaffold generator creates the canonical task file shape, task metadata, placeholder reference/flawed files, review notes, a deliberately failing test placeholder, and a fixture-quality example.

It intentionally does not edit benchmark.json or fixture_expectations.json, so a generated draft cannot silently become a canonical benchmark task.

## Containerized isolation

The Docker path provides a stronger execution boundary for untrusted candidate code:

- network disabled;
- read-only root filesystem;
- all Linux capabilities dropped;
- no-new-privileges;
- PID, memory, CPU, file-descriptor, and tmpfs limits;
- candidate mount read-only;
- host UID/GID execution.

GitHub Actions performs a real container smoke test using task_08_optimistic_concurrency and verifies a 100/100 JSON result.

This is stronger isolation, not a guarantee of perfect sandboxing.
