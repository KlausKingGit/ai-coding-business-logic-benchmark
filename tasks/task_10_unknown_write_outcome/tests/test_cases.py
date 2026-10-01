import pytest
from shared.candidate import load

ChargeCoordinator = load("task_10_unknown_write_outcome").ChargeCoordinator

class SuccessGateway:
    def __init__(self):
        self.calls = 0
        self.seen = []

    def charge(self, request_id, amount_cents):
        self.calls += 1
        self.seen.append((request_id, amount_cents))
        return {"gateway_id": "g1"}

class TimeoutAfterApplyGateway:
    def __init__(self):
        self.calls = 0
        self.effects = 0

    def charge(self, request_id, amount_cents):
        self.calls += 1
        self.effects += 1
        if self.calls == 1:
            raise TimeoutError("response lost after apply")
        return {"gateway_id": f"g{self.effects}"}

class TimeoutBeforeApplyThenSuccessGateway:
    def __init__(self):
        self.calls = 0
        self.effects = 0

    def charge(self, request_id, amount_cents):
        self.calls += 1
        if self.calls == 1:
            raise TimeoutError("request outcome unknown")
        self.effects += 1
        return {"gateway_id": "g1"}

def test_success():
    gateway = SuccessGateway()
    result = ChargeCoordinator(gateway).charge("r1", 100)
    assert result == {"request_id": "r1", "status": "succeeded", "gateway_id": "g1"}
    assert gateway.calls == 1
    assert gateway.seen == [("r1", 100)]

def test_timeout_after_apply_is_unknown_and_not_retried():
    gateway = TimeoutAfterApplyGateway()
    result = ChargeCoordinator(gateway).charge("r1", 100)
    assert result == {"request_id": "r1", "status": "unknown"}
    assert gateway.calls == 1
    assert gateway.effects == 1

def test_timeout_before_apply_is_still_unknown_and_not_retried():
    gateway = TimeoutBeforeApplyThenSuccessGateway()
    result = ChargeCoordinator(gateway).charge("r1", 100)
    assert result == {"request_id": "r1", "status": "unknown"}
    assert gateway.calls == 1
    assert gateway.effects == 0

@pytest.mark.parametrize("amount", [0, -1, True])
def test_invalid_amount_never_calls_gateway(amount):
    gateway = SuccessGateway()
    with pytest.raises(ValueError):
        ChargeCoordinator(gateway).charge("r1", amount)
    assert gateway.calls == 0

@pytest.mark.parametrize("request_id", ["", "   ", None])
def test_invalid_request_id_never_calls_gateway(request_id):
    gateway = SuccessGateway()
    with pytest.raises(ValueError):
        ChargeCoordinator(gateway).charge(request_id, 100)
    assert gateway.calls == 0
