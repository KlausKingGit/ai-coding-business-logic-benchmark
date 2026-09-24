# Evaluation design

Five small backend contracts expose common AI-generated code errors: overwriting orders, double-counting payments, incomplete retry semantics, marking failed webhooks as done, and trusting structured AI output without checking source facts.

The same tests run against both implementations. Passing a happy path earns partial credit; failing a business invariant reveals the gap. Scores count observed pytest cases only. They do not measure readability, safety beyond tested paths, or production readiness; the task notes provide human review prompts.

Functional correctness asks whether valid input produces the specified output. Business correctness asks whether domain rules survive duplicates, retries, and bad data. Engineering correctness asks whether errors, state changes, and logging remain controlled. A reviewer needs all three views.

The services use process memory and simulated failures. They have no durable unique constraints, multi-worker transactions, or webhook signature verification. Task 05 checks structured identities and amounts, while unrestricted note text remains a human review task.
