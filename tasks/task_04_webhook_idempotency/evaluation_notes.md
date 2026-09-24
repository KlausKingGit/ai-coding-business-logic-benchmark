# Webhook review

The bad candidate validates the payload and suppresses ordinary duplicates. It marks an event as processed before simulated work succeeds. `test_failure_retry` verifies both the failed state and the later retry's side effect.

Human review checklist:

- Is an event recorded only after successful processing?
- Can a retry repeat a side effect after a partial failure?
- Are payload secrets excluded from logs?
- Are identical duplicates successful while conflicting payloads are rejected?
- What persistence and sender authentication would a real integration require?
