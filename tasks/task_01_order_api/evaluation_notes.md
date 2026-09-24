# Review notes — Order creation API

**Plausible AI failure:** Bad example trusts arbitrary dicts, overwrites orders and returns 200. It has no controlled storage error path.

**Review the candidate against:** No overwrite; correct response body and status; failure leaves store unchanged. Also inspect readable control flow, explicit failure handling, and whether the implementation makes stronger claims than its in-memory scope supports. The automated score is a test pass rate, not a code-quality score.
