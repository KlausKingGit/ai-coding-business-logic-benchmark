# Payment reconciliation

**Business background:** Finance reconciles order and payment CSV exports.

**Task / input and output:** Input CSV columns: orders(order_id,amount), payments(payment_id,order_id,amount). Output order paid/unpaid cents and status plus exceptions.

**Boundary conditions:** Multiple and partial payments, overpayment, orphan, duplicate ID, blank or malformed amount, precision.

**Acceptance criteria:** No duplicate counting; preserve unpaid orders and orphan exceptions; exact cents.

Run: `python -m pytest -q tasks/task_02_payment_reconciliation/tests`. Inspect `reference_solution.py`, `candidate_bad_example.py`, and `evaluation_notes.md`.
