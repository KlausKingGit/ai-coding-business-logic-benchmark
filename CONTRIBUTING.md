# Contributing

[中文贡献指南](CONTRIBUTING.zh-CN.md)

Contributions are welcome if they make the benchmark more reproducible, discriminating, or maintainable.

## Good contributions

- a new task built around one narrow business invariant;
- a test that catches a realistic false-positive implementation;
- a fix to benchmark infrastructure or documentation;
- a clarification that removes ambiguity without silently changing the intended contract.

For a substantial task, opening a **Task proposal** issue first is encouraged.

## Task acceptance criteria

A task should:

1. use a stable ID such as `task_11_pagination_cursor`;
2. isolate one or a small number of closely related business invariants;
3. run offline with no account, credential, paid API, or network dependency;
4. include a reference implementation that passes all tests;
5. include a deliberately flawed implementation that is plausible and passes meaningful non-target paths;
6. contain deterministic tests that expose the intended defect;
7. add a fixture-quality expectation defining target failing tests and a minimum passing baseline;
8. document known limits and avoid production-readiness claims;
9. include `task.json` using the canonical filenames;
10. complete quickly enough for normal CI;
11. use fictional or redistributable data only.

Do not renumber released task IDs.

See [Fixture quality gates](docs/fixture_quality.md) for the repository-provided reference/flawed baseline.

## Pull requests

A change to benchmark outcomes should explain which invariant changed, why, whether historical scores remain comparable, and whether the benchmark version should change.

Run:

```bash
python -m pytest -q
python -m evaluator.manifest
python evaluator/runner.py --candidate reference --json-report /tmp/reference.json
python evaluator/runner.py --candidate flawed --json-report /tmp/flawed.json
python -m evaluator.fixture_check --reference-json /tmp/reference.json --flawed-json /tmp/flawed.json
```

## License

By submitting a contribution, you agree that your contribution is licensed under the repository's MIT License.
