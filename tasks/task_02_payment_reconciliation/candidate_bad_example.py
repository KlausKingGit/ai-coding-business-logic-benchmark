"""Mostly plausible reconciliation; duplicate IDs are counted again."""
from pathlib import Path
import pandas as pd
from shared.models import cents


def reconcile(orders_csv: str | Path, payments_csv: str | Path) -> dict:
    orders = pd.read_csv(orders_csv, dtype=str, keep_default_na=False)
    payments = pd.read_csv(payments_csv, dtype=str, keep_default_na=False)
    if set(orders.columns) != {"order_id", "amount"} or set(payments.columns) != {"payment_id", "order_id", "amount"}:
        raise ValueError("invalid CSV columns")
    totals: dict[str, int] = {}
    exceptions: list[dict] = []
    for row in orders.to_dict("records"):
        oid = row["order_id"].strip()
        try:
            amount = cents(row["amount"])
            if not oid or amount <= 0 or oid in totals:
                raise ValueError()
        except ValueError:
            exceptions.append({"type": "invalid_order", "order_id": oid})
            continue
        totals[oid] = amount
    paid = {oid: 0 for oid in totals}
    for row in payments.to_dict("records"):
        pid, oid = row["payment_id"].strip(), row["order_id"].strip()
        try:
            amount = cents(row["amount"])
            if not pid or amount <= 0:
                raise ValueError()
        except ValueError:
            exceptions.append({"type": "invalid_payment", "payment_id": pid})
            continue
        if oid not in totals:
            exceptions.append({"type": "orphan_payment", "payment_id": pid})
            continue
        paid[oid] += amount  # No payment_id uniqueness check.
    results = []
    for oid, due in totals.items():
        received = paid[oid]
        status = "overpaid" if received > due else "paid" if received == due else "partial" if received else "unpaid"
        if received > due:
            exceptions.append({"type": "overpayment", "order_id": oid})
        results.append({"order_id": oid, "paid_cents": received, "unpaid_cents": max(due - received, 0), "status": status})
    return {"orders": results, "exceptions": exceptions}
