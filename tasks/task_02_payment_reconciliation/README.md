# Payment reconciliation

Finance imports `orders.csv` (`order_id,amount`) and `payments.csv` (`payment_id,order_id,amount`). Return each order's paid and unpaid integer cents, payment status, and an exception list. Keep unpaid orders and orphan payments visible; handle partial, multiple, and excess payments.

**Business rule:** the first occurrence of a nonempty `payment_id` reserves that ID, even if its amount is invalid. Every later occurrence is a duplicate and is not counted. This is a chosen business policy, not a technical necessity. Blank IDs and invalid amounts are exceptions. Decimal input has at most two places.

Run `python evaluator/runner.py --candidate reference` or `--candidate bad` from the repository root. See `evaluation_notes.md` for the review checklist.
