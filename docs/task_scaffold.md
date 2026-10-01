# Contributor task scaffold

Generate a non-registered task starting point:

    python -m evaluator.scaffold \
      --output-dir /tmp/task_11_pagination_cursor \
      --task-id task_11_pagination_cursor \
      --title "Pagination cursor" \
      --summary "Preserve cursor progression without skipping or duplicating items." \
      --area pagination \
      --tag pagination \
      --tag cursor

The scaffold creates the canonical task file shape, an intentionally failing placeholder test, and an example fixture-quality entry.

It deliberately does not edit benchmark.json or fixture_expectations.json.

That separation is a safety feature: a generated scaffold is not a benchmark task until its invariant, tests, reference implementation, flawed fixture, limits, and comparability impact have been reviewed.
