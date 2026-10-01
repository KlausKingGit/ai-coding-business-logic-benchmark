# Review notes

The target defect is **mutating first and checking authorization second**.

A function that raises `PermissionError` can still be wrong if it has already changed state.

Review for:

- authorization before assignment;
- owner and admin success paths;
- cross-owner denial with no visible mutation;
- input validation independent from authorization;
- no claim that this tiny owner/admin model is a production IAM system.
