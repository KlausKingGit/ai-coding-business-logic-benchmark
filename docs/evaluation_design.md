# Evaluation design

These five tasks reflect routine backend failures rather than puzzles: HTTP contracts, payment aggregation, quota state, webhook delivery, and generated summaries. A program that starts can still overwrite an order, double charge a user, or invent a customer. Tests therefore assert outcomes and error paths, not merely importability.

- **Functional correctness:** Does the feature produce the specified output on valid input?
- **Business correctness:** Do domain rules hold, including duplicates, insufficient balance, and exact money?
- **Engineering correctness:** Are failures controlled, state updates atomic within the stated scope, logs safe, and code maintainable?

Automated scoring deliberately measures only test pass rate. A human must inspect architecture, readability, security, and whether tests omit important behavior. These examples use process memory; real deployments need persistent unique constraints, transactions, and multi-worker coordination. The webhook example does not authenticate senders, so it is a local evaluation exercise, not a deployable payment integration.
