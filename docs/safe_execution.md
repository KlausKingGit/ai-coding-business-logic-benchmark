# Safe execution of external candidates

External candidates are Python programs. Evaluating them is code execution.

## Default runner protections

When `--candidate-dir` is used:

1. the child pytest process receives a sanitized environment rather than the complete host environment;
2. each task is terminated if its pytest process exceeds `--task-timeout-seconds` (30 seconds by default).

You can intentionally pass a host variable with:

```bash
python evaluator/runner.py \
  --candidate-dir ./candidate \
  --inherit-env MY_PUBLIC_SETTING
```

Reserved benchmark control variables cannot be overridden through this mechanism.

## What these protections do not provide

This runner is **not a security sandbox**.

It does not currently enforce:

- filesystem isolation;
- network isolation;
- memory limits;
- CPU quotas beyond wall-clock timeout;
- syscall filtering;
- process-tree containment.

For untrusted candidate code, use an external isolation boundary such as a disposable container, VM, restricted CI worker, or dedicated sandbox with no secrets.

## Recommended trust model

- Repository reference/flawed fixtures: trusted project code.
- Code you generated and reviewed yourself: run according to your own risk tolerance.
- Third-party or unknown candidate code: isolate it before evaluation.
