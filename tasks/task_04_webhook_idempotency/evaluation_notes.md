# Review notes — Payment webhook

**Plausible AI failure:** Bad example logs the entire payload and returns an error object for duplicates. It marks events without a failure-safe handler.

**Review the candidate against:** A duplicate succeeds without reprocessing; failed event remains retryable; logs exclude payload secrets. Also inspect readable control flow, explicit failure handling, and whether the implementation makes stronger claims than its in-memory scope supports. The automated score is a test pass rate, not a code-quality score.
