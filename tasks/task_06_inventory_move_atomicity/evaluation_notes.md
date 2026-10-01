# Review notes

The target defect is **partial mutation before a later failure**.

A plausible implementation may:

1. decrement the source;
2. increment the destination;
3. attempt to write an audit/movement record;
4. raise when the record write fails.

That sequence looks straightforward but leaks a successful-looking stock mutation from an operation that actually failed.

Review for:

- all validation before mutation;
- no stock change after a failed movement record;
- no movement record on failure;
- exact success state on a normal move;
- explicit scope: this fixture does not model a real database transaction.
