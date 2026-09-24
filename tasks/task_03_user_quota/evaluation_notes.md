# Review notes — User quota

**Plausible AI failure:** Bad example deducts before checking and ignores request_id; concurrent and repeated requests can both charge.

**Review the candidate against:** Never negative; identical retry deducts once; local calls serialize. Also inspect readable control flow, explicit failure handling, and whether the implementation makes stronger claims than its in-memory scope supports. The automated score is a test pass rate, not a code-quality score.
