# Reproducible environment

The repository keeps two dependency views for different purposes.

## Compatible ranges

`requirements.txt` is the human-maintained compatibility declaration. It expresses the dependency ranges the project intends to support.

## Validated lock snapshot

`requirements.lock` records the exact dependency set used by the validated GitHub Actions matrix.

Install it with:

```bash
python -m pip install -r requirements.lock
python -m pip check
```

The accompanying `environment.snapshot.json` records the CI provider, runner image, Python patch versions, and the Python-specific NumPy resolution observed when the snapshot was captured.

## Why NumPy has markers

The successful CI resolution differed by Python minor version:

- Python 3.11.16 → NumPy 2.4.6
- Python 3.12.14 → NumPy 2.5.3

The lock file preserves that actual validated resolution with environment markers instead of pretending one installation was used everywhere.

## Supported reproduction boundary

The lock snapshot is currently defined for Python 3.11 and 3.12 because those are the versions continuously validated by CI.

A future Python minor version should be added to CI first, then captured in a new environment snapshot before it is described as reproducible.

The benchmark task semantics are independent from these package pins; updating a lock file must not silently change a task invariant or historical comparability.
