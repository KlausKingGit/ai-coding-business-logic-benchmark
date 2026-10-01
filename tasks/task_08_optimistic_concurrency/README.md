# Optimistic concurrency

A record store exposes versioned updates:

`update(record_id, expected_version, value)`

Every record starts at version 1.

Rules:

- the record must exist;
- `expected_version` must be a positive integer (not `bool`);
- the update is allowed only when `expected_version` exactly equals the current version;
- success stores the new value and increments the version by one;
- a stale or future version raises `ConflictError`;
- a conflict leaves the record unchanged.

The target defect is accepting a stale write after another update has already advanced the record.
