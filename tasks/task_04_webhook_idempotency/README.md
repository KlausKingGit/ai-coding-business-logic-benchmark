# Payment webhook

**Business background:** A payment provider may redeliver the same event.

**Task / input and output:** POST /webhooks/payment with event_id, payment_id and positive amount_cents; output processed or already_processed.

**Boundary conditions:** Duplicate and conflicting event, bad payload, handler outage and retry.

**Acceptance criteria:** A duplicate succeeds without reprocessing; failed event remains retryable; logs exclude payload secrets.

Run: `python -m pytest -q tasks/task_04_webhook_idempotency/tests`. Inspect `reference_solution.py`, `candidate_bad_example.py`, and `evaluation_notes.md`.
