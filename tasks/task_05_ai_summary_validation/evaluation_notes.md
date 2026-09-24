# Review notes — AI summary validation

**Plausible AI failure:** Bad example checks only JSON syntax, so invented customers and modified amounts pass.

**Review the candidate against:** All fact identities and amounts exactly match input; schema admits no extras. Also inspect readable control flow, explicit failure handling, and whether the implementation makes stronger claims than its in-memory scope supports. The automated score is a test pass rate, not a code-quality score.
