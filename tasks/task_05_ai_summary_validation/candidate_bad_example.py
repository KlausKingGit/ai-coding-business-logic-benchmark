"""Strict JSON shape, but no comparison to the supplied source facts."""
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
        return Summary.model_validate(json.loads(raw)).model_dump()
    except (json.JSONDecodeError, ValidationError) as exc:
        raise ValueError("invalid summary schema") from exc
