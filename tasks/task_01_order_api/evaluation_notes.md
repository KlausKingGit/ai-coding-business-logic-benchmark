# Order API review

The flawed candidate uses FastAPI validation and returns 201 for a valid order. It misses the duplicate lookup: a second request overwrites the first. `test_duplicate` catches this even though most input checks pass.

Human review checklist:

- Is money represented as positive integer cents, including rejection of fractional cents?
- Is the duplicate check done before mutation?
- Are 409 business conflicts distinct from 503 storage failures?
- Can internal exception details leak to clients?
- Is the success JSON stable?
