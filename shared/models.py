"""Shared money convention: integer cents, never binary floating point."""
from decimal import Decimal, InvalidOperation


def cents(value: object) -> int:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("invalid amount") from exc
    if not amount.is_finite() or amount != amount.quantize(Decimal("0.01")):
        raise ValueError("amount must have at most two decimal places")
    return int(amount * 100)
