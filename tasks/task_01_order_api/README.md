# Order creation API

A merchant creates an order before taking payment. Implement `POST /orders` with `order_id`, `customer_id`, and positive integer `amount_cents`. Return the created JSON with 201; use 422 for invalid input, 409 for a duplicate ID, and 503 for a simulated store outage. Never expose the internal error text.

Empty IDs, zero or fractional cents, repeated IDs, and store failure are tested. The order must not be overwritten.

Run `python evaluator/runner.py --candidate reference` or `--candidate bad` from the repository root. See `evaluation_notes.md` for the review checklist.
