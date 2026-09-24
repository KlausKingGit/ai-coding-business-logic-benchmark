import json
from pydantic import BaseModel, ConfigDict, ValidationError


class Item(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    customer_id: str
    amount_cents: int
    note: str


class Summary(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    items: list[Item]


def validate_summary(raw: str, facts: list[dict]) -> dict:
    try:
        parsed = Summary.model_validate(json.loads(raw))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise ValueError("invalid summary schema") from exc
    expected = {(f["customer_id"], f["amount_cents"]) for f in facts}
    actual = [(i.customer_id, i.amount_cents) for i in parsed.items]
    if len(actual) != len(expected) or set(actual) != expected:
        raise ValueError("summary does not match supplied facts")
    return parsed.model_dump()
