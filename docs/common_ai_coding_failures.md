# Common AI coding failures

1. **Happy path only:** an order succeeds once but a second request overwrites it.
2. **Missing edge cases:** zero-cent orders pass a truthiness check.
3. **Incorrect exception handling:** a duplicate order returns 500 instead of 409.
4. **Over-broad try/except:** `except Exception: return {}` hides a store outage.
5. **Missing idempotency:** a webhook retry credits twice.
6. **Hidden state bugs:** a retry returns current quota rather than its original response.
7. **Data duplication after joins:** an order total is multiplied by payment rows.
8. **Incorrect money calculations:** binary floats make exact equality unreliable.
9. **Invalid API status codes:** a successful creation returns 200 rather than 201.
10. **Hallucinated structured fields:** generated JSON invents a customer ID. Free-form notes still need human review.
11. **Missing validation:** a negative deduction increases quota.
12. **Security-sensitive logging:** logging the whole webhook payload records a secret.
13. **Incomplete tests:** a 200 retry response is accepted without checking processing happened.
14. **Overengineering:** a broker and distributed lock are added to an offline example.
15. **Runs but violates business rules:** a repeated payment ID is counted twice.
