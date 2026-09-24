# AI Coding Evaluation Demo

A compact, offline portfolio case for evaluating generated Python code against real business rules.

## Why I Built This

This project demonstrates how I design and evaluate realistic AI Coding tasks. The focus is real engineering scenarios: business rules, edge cases, validation, error handling, maintainability, safety, and testability.

## What This Demonstrates

Engineering task design, Python/FastAPI, pytest, business-rule validation, AI-generated code review, edge-case design, automated evaluation, and engineering judgment.

## Run in four steps

1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `python -m pip install -r requirements.txt`
4. `python evaluator/runner.py` (writes `report.md`); optionally run `python -m pytest -q`.

Requires Python 3.11+. Everything runs locally without a database server, external API, account, or secret. `candidate_bad_example.py` files are intentionally flawed and are not imported by the reference tests.

## Five-minute reading path

1. Read this page (one minute).
2. Read [order task](tasks/task_01_order_api/README.md) and its reference and bad example (two minutes).
3. Compare [order tests](tasks/task_01_order_api/tests/test_cases.py) with [evaluation notes](tasks/task_01_order_api/evaluation_notes.md) (one minute).
4. Scan the other four task descriptions and [evaluation design](docs/evaluation_design.md) (one minute).

## Tasks and evidence

| Task | Core failure exposed |
|---|---|
| [Order API](tasks/task_01_order_api/README.md) | Duplicate IDs and HTTP error semantics |
| [Payment reconciliation](tasks/task_02_payment_reconciliation/README.md) | One-to-many joins and money precision |
| [User quota](tasks/task_03_user_quota/README.md) | Atomic local deduction and retries |
| [Webhook](tasks/task_04_webhook_idempotency/README.md) | Duplicate delivery and sensitive logging |
| [AI summary](tasks/task_05_ai_summary_validation/README.md) | Schema drift and fabricated facts |

The runner scores passing tests only: `round(100 × passed / (passed + failed))`. Collection errors score as failures. Code quality and production readiness require human review; see each `evaluation_notes.md`. To assess a candidate, replace the relevant reference implementation in an isolated copy, run the same tests, and review the diff against the rubric. Tests establish a minimum contract, not exhaustive correctness.

## Reuse for a hiring review

Each task provides a prompt, reference solution, flawed AI-style candidate, tests, and a short review. This mirrors the work of an AI Coding evaluator: write realistic tasks, define acceptance criteria, identify plausible defects, and explain why a green happy-path run is insufficient. No real customer data or credentials are included.

**GitHub description:** Five offline Python/FastAPI evaluation tasks with reference solutions, flawed AI examples, pytest checks, and transparent scoring.

**Suggested topics:** `ai-coding`, `code-evaluation`, `fastapi`, `pytest`, `python`, `vibe-coding`, `software-testing`.

**Resume (EN):** Designed five realistic AI coding evaluation tasks spanning APIs, payments, idempotency, concurrency, and LLM output validation; delivered reference solutions, defect examples, automated tests, and a reproducible scoring report.

**简历（中文）：** 设计 5 个真实业务场景的 AI 编码评测任务，覆盖 API、回款、幂等、并发与 LLM 输出校验；交付参考实现、缺陷示例、自动化测试和可复现评分报告。
