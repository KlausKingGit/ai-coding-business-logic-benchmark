# AI summary validation

A manager receives generated JSON: `{"items": [{"customer_id": str, "amount_cents": int, "note": str}]}`. Validate the schema strictly and require the item identities and amounts to match the supplied, precomputed facts exactly. Malformed JSON, extra or missing fields, duplicates, and changed amounts fail with `ValueError`.

Only structured identity and numeric fields are checked against source data. Free-form `note` may still contain an unsupported claim and requires human review. No LLM call is made.

Run `python evaluator/runner.py --candidate reference` or `--candidate bad` from the repository root. See `evaluation_notes.md` for the review checklist.
