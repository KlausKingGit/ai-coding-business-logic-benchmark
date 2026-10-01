class ContractDriftError(RuntimeError):
    pass

_REQUIRED_KEYS = {"method", "path", "request_required", "response_required"}

def _normalize(contract: dict) -> dict:
    if not isinstance(contract, dict) or set(contract) != _REQUIRED_KEYS:
        raise ValueError("contract must contain exactly the required keys")
    if not isinstance(contract["method"], str) or not contract["method"]:
        raise ValueError("method is required")
    if not isinstance(contract["path"], str) or not contract["path"].startswith("/"):
        raise ValueError("path must be absolute")
    result = dict(contract)
    for key in ("request_required", "response_required"):
        value = contract[key]
        if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
            raise ValueError(f"{key} must be a string list")
        if len(value) != len(set(value)):
            raise ValueError(f"{key} must not contain duplicates")
        result[key] = set(value)
    return result

def assert_compatible(expected: dict, actual: dict) -> None:
    expected = _normalize(expected)
    actual = _normalize(actual)

    if expected["method"] != actual["method"] or expected["path"] != actual["path"]:
        raise ContractDriftError("endpoint identity changed")

    new_required_request = actual["request_required"] - expected["request_required"]
    if new_required_request:
        raise ContractDriftError("new required request fields")

    missing_required_response = expected["response_required"] - actual["response_required"]
    if missing_required_response:
        raise ContractDriftError("required response fields removed")
