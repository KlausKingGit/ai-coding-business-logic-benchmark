# Payment webhook

A payment provider may redeliver an event. Implement `POST /webhooks/payment` with `event_id`, `payment_id`, and positive integer `amount_cents`. Return `processed` for first success and `already_processed` for an identical retry. A conflicting event ID returns 409; invalid input returns 422.

Simulated processing failure returns 503 and leaves the event retryable. Logs must not contain arbitrary payload fields. The in-memory processor is an evaluation fixture; a real endpoint would also authenticate the sender and persist processing state.

Run `python evaluator/runner.py --candidate reference` or `--candidate bad` from the repository root. See `evaluation_notes.md` for the review checklist.
