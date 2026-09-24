# User quota

A local service deducts a positive integer allowance via `deduct(user_id, amount, request_id)` and returns the remaining quota. Reject insufficient balance, invalid amounts, and request IDs reused with different arguments.

An identical retry returns the *original response* and changes nothing, even if later requests have changed the current balance. Calls within one process serialize; this exercise does not promise durability or coordination between workers.

Run `python evaluator/runner.py --candidate reference` or `--candidate bad` from the repository root. See `evaluation_notes.md` for the review checklist.
