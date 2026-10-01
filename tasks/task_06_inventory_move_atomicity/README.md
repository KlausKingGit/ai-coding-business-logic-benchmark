# Inventory move atomicity

A warehouse service moves a positive integer quantity from one SKU bucket to another and records the movement.

Implement:

`move(source_sku, destination_sku, quantity, movement_id)`

Rules:

- source and destination must already exist and be different;
- quantity must be a positive integer (not `bool`);
- source must have enough stock;
- `movement_id` must be non-empty;
- a successful move decrements source stock, increments destination stock, and appends one movement record;
- if recording the movement fails, **no stock change may remain visible**.

The fixture uses in-memory state and a simulated record failure. The point is the all-or-nothing invariant, not a production transaction implementation.

Run:

```bash
python evaluator/runner.py --candidate reference --task task_06_inventory_move_atomicity
python evaluator/runner.py --candidate flawed --task task_06_inventory_move_atomicity
```
