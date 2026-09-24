# AI Coding Evaluation Demo

Five offline Python tasks for reviewing generated code against backend business rules. Each task has a prompt, reference implementation, plausible flawed candidate, shared tests, and a human review checklist.

## Example: How the evaluator catches an AI-style bug

**Bad candidate (Task 03):**

```python
if request_id in self.requests:
    return self.quota[user_id]
```

This looks reasonable: it avoids charging twice. But after `r1` reduces quota from 10 to 8 and `r2` reduces it to 5, replaying `r1` must return its original result **8**, not the current balance **5**. A retry is the same operation, including its response. The bad candidate passes ordinary deduction, insufficient-balance, and immediate-retry cases; `test_retry_returns_original_result` exposes the missing response history.

```bash
python evaluator/runner.py --candidate bad
# task_03_user_quota: 10 passed, 1 failed, 0 errors, 91/100
```

## Candidate comparison

Observed with the same tests for both candidates (see [reference report](reports/reference.md) and [bad report](reports/bad.md)):

| Task | Reference | Bad candidate | Defect caught |
|---|---:|---:|---|
| [Order API](tasks/task_01_order_api/README.md) | 10/10 | 9/10 | Duplicate overwrite |
| [Reconciliation](tasks/task_02_payment_reconciliation/README.md) | 10/10 | 8/10 | Repeated payment ID |
| [Quota](tasks/task_03_user_quota/README.md) | 11/11 | 10/11 | Retry returns current balance |
| [Webhook](tasks/task_04_webhook_idempotency/README.md) | 9/9 | 8/9 | Failed event marked done |
| [AI summary](tasks/task_05_ai_summary_validation/README.md) | 10/10 | 6/10 | Structured facts unchecked |

## Run locally

Requires Python 3.11+. No database, external API, account, or secret.

1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `python -m pip install -r requirements.txt`
4. Run `python -m pytest -q`, then `python evaluator/runner.py --candidate reference` and `python evaluator/runner.py --candidate bad`.

The runner writes `reports/reference.md` or `reports/bad.md`. The default `pytest` run uses the reference; `EVAL_CANDIDATE=bad python -m pytest -q` runs the identical tests against the flawed candidate. Bad-mode test failures are expected, so the runner exits successfully when evaluation completed without collection errors. A reference-mode failure or any collection error yields a nonzero exit code. Scores are `round(100 × passed / (passed + failed))`; they do not automate code-quality judgment.

## Why I built this

AI Coding review needs more than code that runs. These tasks check domain rules, validation, error paths, state changes, and testability. The flawed implementations pass some tests while failing targeted checks, which makes the assessment closer to reviewing a real generated patch. Read [evaluation design](docs/evaluation_design.md) for the scoring boundary and [common failures](docs/common_ai_coding_failures.md) for examples.

**Five-minute reading path:** this page (one minute), [Quota task](tasks/task_03_user_quota/README.md) plus its [two implementations](tasks/task_03_user_quota/reference_solution.py) and [bad candidate](tasks/task_03_user_quota/candidate_bad_example.py) (two minutes), [quota tests](tasks/task_03_user_quota/tests/test_cases.py) and [review notes](tasks/task_03_user_quota/evaluation_notes.md) (one minute), then the two reports (one minute).

**GitHub description:** Five offline Python/FastAPI evaluation tasks with reference and flawed AI-style implementations, shared pytest checks, and transparent scoring.

**Suggested topics:** `ai-coding`, `code-evaluation`, `fastapi`, `pytest`, `python`, `vibe-coding`, `software-testing`.

**Resume (EN):** Designed five realistic AI coding evaluation tasks covering APIs, payments, idempotency, concurrency, and structured LLM output; ran shared tests against reference and flawed implementations to expose business-rule defects.

**简历（中文）：** 设计 5 个真实业务场景的 AI 编码评测任务，用同一套测试对照参考实现与部分正确的错误实现，识别订单、回款、幂等、并发和结构化摘要中的业务缺陷。
