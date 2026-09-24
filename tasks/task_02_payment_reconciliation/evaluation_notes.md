# Review notes — Payment reconciliation

**Plausible AI failure:** Bad example inner-joins away unpaid/orphan rows and aggregates floating values; it never checks duplicate payment IDs.

**Review the candidate against:** No duplicate counting; preserve unpaid orders and orphan exceptions; exact cents. Also inspect readable control flow, explicit failure handling, and whether the implementation makes stronger claims than its in-memory scope supports. The automated score is a test pass rate, not a code-quality score.
