# Reconciliation review

The bad candidate handles multiple payments, orphan records, and exact cents. It omits payment ID uniqueness, so a repeated payment is counted twice. `test_duplicate_payment_not_counted` and `test_invalid_first_payment_id_still_reserved` expose the rule violation.

Human review checklist:

- Does aggregation avoid multiplying an order when it has several payments?
- Are orphan payments retained in exceptions?
- Does money arithmetic avoid float drift?
- Does the first occurrence reserve a payment ID even when its amount is invalid?
- Are blank fields rejected without stopping the whole file?
