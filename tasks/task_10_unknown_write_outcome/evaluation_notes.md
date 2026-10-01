# Review notes

The target defect is **retrying a write whose first outcome is unknown**.

A timeout is transport evidence, not proof that the external system did nothing.

The strongest test simulates:

1. gateway applies the charge;
2. response is lost and the caller receives `TimeoutError`;
3. a blind retry applies the charge again.

Review for:

- no retry after the timeout;
- explicit `unknown` status;
- stable request identity forwarded to the gateway;
- input validation before any external call;
- no claim that this fixture implements reconciliation or durable idempotency.
