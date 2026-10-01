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
    for key in ("request_required", "response_required"):
        value = contract[key]
        if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
            raise ValueError(f"{key} must be a string list")
    return dict(contract)

def assert_compatible(expected: dict, actual: dict) -> None:
    expected = _normalize(expected)
    actual = _normalize(actual)
    if expected["method"] != actual["method"] or expected["path"] != actual["path"]:
        raise ContractDriftError("endpoint identity changed")
