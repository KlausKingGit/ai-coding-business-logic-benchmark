import json
import pytest
from shared.candidate import load

validate_summary = load("task_05_ai_summary_validation").validate_summary

FACTS = [{"customer_id": "c1", "amount_cents": 100}]
ITEM = {"customer_id": "c1", "amount_cents": 100, "note": "Late payment"}


def check(item=ITEM, facts=FACTS):
    return validate_summary(json.dumps({"items": [item]}), facts)


def test_valid():
    assert check()["items"][0] == ITEM


@pytest.mark.parametrize("item", [ITEM | {"customer_id": "fiction"}, ITEM | {"amount_cents": 101}, ITEM | {"amount_cents": "100"}, ITEM | {"extra": 1}, {"customer_id": "c1", "amount_cents": 100}])
def test_invalid_item(item):
    with pytest.raises(ValueError):
        check(item)


def test_invalid_json():
    with pytest.raises(ValueError):
        validate_summary("not json", FACTS)


def test_extra_root_field():
    with pytest.raises(ValueError):
        validate_summary(json.dumps({"items": [ITEM], "total": 100}), FACTS)


def test_missing_fact():
    with pytest.raises(ValueError):
        validate_summary(json.dumps({"items": []}), FACTS)


def test_duplicate_fact():
    with pytest.raises(ValueError):
        validate_summary(json.dumps({"items": [ITEM, ITEM]}), FACTS)
