import pytest
from shared.candidate import load

candidate = load("task_09_api_contract_drift")
assert_compatible = candidate.assert_compatible
ContractDriftError = candidate.ContractDriftError

BASE = {
    "method": "POST",
    "path": "/orders",
    "request_required": ["order_id", "amount_cents"],
    "response_required": ["order_id", "amount_cents", "status"],
}

def test_identical_contract_is_compatible():
    assert assert_compatible(BASE, dict(BASE)) is None

def test_removing_request_requirement_is_compatible():
    actual = BASE | {"request_required": ["order_id"]}
    assert assert_compatible(BASE, actual) is None

def test_adding_response_field_is_compatible():
    actual = BASE | {"response_required": BASE["response_required"] + ["created_at"]}
    assert assert_compatible(BASE, actual) is None

def test_new_required_request_field_is_breaking():
    actual = BASE | {"request_required": BASE["request_required"] + ["currency"]}
    with pytest.raises(ContractDriftError):
        assert_compatible(BASE, actual)

def test_removed_required_response_field_is_breaking():
    actual = BASE | {"response_required": ["order_id", "status"]}
    with pytest.raises(ContractDriftError):
        assert_compatible(BASE, actual)

@pytest.mark.parametrize("change", [
    {"method": "PUT"},
    {"path": "/v2/orders"},
])
def test_endpoint_identity_change_is_breaking(change):
    with pytest.raises(ContractDriftError):
        assert_compatible(BASE, BASE | change)

def test_invalid_contract_shape():
    with pytest.raises(ValueError):
        assert_compatible(BASE, {"method": "POST"})
