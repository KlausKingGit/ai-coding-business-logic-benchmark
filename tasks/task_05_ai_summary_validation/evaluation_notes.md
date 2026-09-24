# AI summary review

The flawed candidate validates JSON shape but never compares it to supplied facts. Tests for invented identities, changed amounts, missing facts, and duplicates fail. Schema-valid output alone is insufficient.

Human review checklist:

- Are `customer_id` and `amount_cents` checked against deterministic source data?
- Are extra fields, missing fields, and wrong types rejected?
- Does malformed JSON produce a controlled failure?
- Could free-form `note` assert unsupported facts? A person must review its content.
- Is the output contract small enough to inspect quickly?
