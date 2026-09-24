# Common AI coding failures

1. **Happy path only:** order creation works once but a duplicate overwrites it.
2. **Missing edge cases:** zero-value payment is accepted.
3. **Incorrect exception handling:** duplicate order returns 500 instead of 409.
4. **Over-broad try/except:** `except Exception: return {}` hides a storage outage.
5. **Missing idempotency:** a webhook retry credits twice.
6. **Hidden state bugs:** shared test data leaks between requests.
7. **Data duplication after joins:** order amount is multiplied by payment rows.
8. **Incorrect money calculations:** `0.1 + 0.2` is compared as a float.
9. **Invalid API status codes:** creation returns 200 or validation returns 500.
10. **Hallucinated fields:** an AI summary invents a customer ID.
11. **Missing validation:** negative quota deduction increases the balance.
12. **Security-sensitive logging:** a full webhook payload records a secret.
13. **Incomplete tests:** only one successful order is asserted.
14. **Overengineering:** a broker and distributed lock are added to an offline example.
15. **Runs but violates business rules:** duplicate payment IDs are counted twice.
