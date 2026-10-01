# Review notes

The target defect is **treating endpoint existence as contract compatibility**.

A client can still break when the method/path stay unchanged but:

- the server requires a new request field the client never sends;
- the server stops guaranteeing a response field the client reads.

Review for the correct directional set relationships:

- `actual.request_required - expected.request_required` must be empty;
- `expected.response_required - actual.response_required` must be empty.

Removing request requirements and adding response fields are compatible in this small model.
