# Quota review

The flawed candidate prevents repeated deductions but stores no original response. After another request changes the balance, replaying the first request returns today's balance. `test_retry_returns_original_result` distinguishes these semantics.

Human review checklist:

- Does a retry return the original result, not merely avoid a second deduction?
- Does reuse of a request ID with different arguments fail?
- Could concurrent calls overspend quota?
- Does validation happen before mutation?
- Which guarantees disappear across processes or restarts?
