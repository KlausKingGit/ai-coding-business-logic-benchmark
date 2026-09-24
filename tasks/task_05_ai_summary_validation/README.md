# AI summary validation

**Business background:** A manager reads a generated note about precomputed exceptions.

**Task / input and output:** Input JSON string with items[{customer_id,amount_cents,note}] and supplied facts; output validated JSON or ValueError.

**Boundary conditions:** Invalid JSON, missing/extra fields, type mismatch, invented or duplicated facts.

**Acceptance criteria:** All fact identities and amounts exactly match input; schema admits no extras.

Run: `python -m pytest -q tasks/task_05_ai_summary_validation/tests`. Inspect `reference_solution.py`, `candidate_bad_example.py`, and `evaluation_notes.md`.
