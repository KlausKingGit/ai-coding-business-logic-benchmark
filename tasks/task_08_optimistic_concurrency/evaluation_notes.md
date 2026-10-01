# Review notes

The target defect is **accepting an older expected version**.

The comparison must be exact:

`expected_version == current_version`

Checks such as "reject only future versions" still permit stale writers to overwrite newer state.

Review for:

- exact version equality;
- no mutation on stale or future conflicts;
- version increment only after success;
- clear distinction between missing records, invalid versions, and conflicts.
