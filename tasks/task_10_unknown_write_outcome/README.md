# Unknown write outcome

A coordinator sends a charge request to an external gateway.

Implement:

`ChargeCoordinator.charge(request_id, amount_cents)`

Rules:

- `request_id` must be non-empty;
- `amount_cents` must be a positive integer (not `bool`);
- a normal gateway response returns `status = "succeeded"`;
- if the gateway times out, the coordinator cannot know whether the write happened;
- a timeout therefore returns `status = "unknown"`;
- **the coordinator must not automatically retry the write after that timeout**.

The test gateway can simulate a timeout *after* applying the effect. Blind retry then creates a duplicate effect, which is the defect this task targets.

The fixture does not prescribe how a production system should reconcile unknown outcomes; it only establishes that uncertainty is not equivalent to safe retryability.
