# Evaluation report: bad

Score = round(100 × passed / (passed + failed)). Collection errors invalidate the run.
Only observed test outcomes are scored; human review remains necessary.

| Task | Passed | Failed | Errors | Score |
|---|---:|---:|---:|---:|
| task_01_order_api | 9 | 1 | 0 | 90/100 |
| task_02_payment_reconciliation | 8 | 2 | 0 | 80/100 |
| task_03_user_quota | 10 | 1 | 0 | 91/100 |
| task_04_webhook_idempotency | 8 | 1 | 0 | 89/100 |
| task_05_ai_summary_validation | 6 | 4 | 0 | 60/100 |

## Failed tests

### task_01_order_api
- `test_duplicate`

### task_02_payment_reconciliation
- `test_duplicate_payment_not_counted`
- `test_invalid_first_payment_id_still_reserved`

### task_03_user_quota
- `test_retry_returns_original_result`

### task_04_webhook_idempotency
- `test_failure_retry`

### task_05_ai_summary_validation
- `test_invalid_item[item0]`
- `test_invalid_item[item1]`
- `test_missing_fact`
- `test_duplicate_fact`
