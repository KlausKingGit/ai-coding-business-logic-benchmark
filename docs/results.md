# Machine-readable results

The runner can emit JSON alongside the existing Markdown report.

```bash
python evaluator/runner.py \
  --candidate-dir ./my-agent-output \
  --candidate-name my-agent \
  --json-report reports/my-agent.json
```

## JSON schema

The current result format uses `schema_version: "1.0"` and contains:

- benchmark id and version;
- candidate mode and display name;
- Python/runtime environment metadata;
- aggregate passed/failed/error counts and score;
- one structured result per selected task;
- failed test identifiers.

Example:

```json
{
  "schema_version": "1.0",
  "benchmark": {
    "id": "ai-coding-business-logic",
    "version": "0.2.0"
  },
  "candidate": {
    "mode": "external",
    "name": "my-agent"
  },
  "summary": {
    "tasks": 10,
    "passed": 72,
    "failed": 8,
    "errors": 0,
    "score": 90
  }
}
```

The exact task list remains in `tasks` in the real output.

A non-zero `failed` count is an evaluation result. Infrastructure/collection errors are recorded separately and cause the runner itself to return non-zero.
