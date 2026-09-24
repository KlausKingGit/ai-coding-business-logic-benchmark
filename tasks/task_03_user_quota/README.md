# User quota

**Business background:** A local usage service deducts allowance for requests.

**Task / input and output:** Input initial quota and deduct(user_id, amount, request_id); output remaining integer quota.

**Boundary conditions:** Exact balance, insufficient quota, duplicate and conflicting request IDs, concurrent local calls.

**Acceptance criteria:** Never negative; identical retry deducts once; local calls serialize.

Run: `python -m pytest -q tasks/task_03_user_quota/tests`. Inspect `reference_solution.py`, `candidate_bad_example.py`, and `evaluation_notes.md`.
