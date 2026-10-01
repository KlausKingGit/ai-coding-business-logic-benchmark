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
5. include a deliberately flawed implementation that is plausible and passes at least one meaningful path;
6. contain deterministic tests that expose the intended defect;
7. document known limits and avoid production-readiness claims;
8. include `task.json` using the canonical filenames;
9. complete quickly enough for normal CI;
10. use fictional or redistributable data only.

Do not renumber released task IDs.

## Pull requests

A change to benchmark outcomes should explain which invariant changed, why, whether historical scores remain comparable, and whether the benchmark version should change.

Run:

```bash
python -m pytest -q
python -m evaluator.manifest
python evaluator/runner.py --candidate reference
python evaluator/runner.py --candidate flawed
```

## License

By submitting a contribution, you agree that your contribution is licensed under the repository's MIT License.
