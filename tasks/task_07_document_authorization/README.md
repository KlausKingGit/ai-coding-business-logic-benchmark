# Document authorization

A document store allows a document owner or an administrator to rename a document.

Implement:

`rename(actor_id, actor_role, document_id, new_title)`

Rules:

- the document must exist;
- `new_title` must be non-empty after stripping whitespace;
- an `admin` may rename any document;
- a non-admin may rename only a document they own;
- an unauthorized attempt raises `PermissionError`;
- **authorization denial must leave the document unchanged**.

The target invariant is mutation ordering: authorization is a precondition for state change, not a check that may happen afterward.
