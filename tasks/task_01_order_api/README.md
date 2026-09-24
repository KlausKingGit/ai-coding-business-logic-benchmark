# Order creation API

**Business background:** A merchant creates an order before taking payment.

**Task / input and output:** POST /orders with order_id, customer_id and positive amount; returns 201 JSON. Duplicate ID returns 409, invalid input 422, storage outage 503 without internals.

**Boundary conditions:** Empty IDs, zero/negative amount, duplicate order, store failure.

**Acceptance criteria:** No overwrite; correct response body and status; failure leaves store unchanged.

Run: `python -m pytest -q tasks/task_01_order_api/tests`. Inspect `reference_solution.py`, `candidate_bad_example.py`, and `evaluation_notes.md`.
