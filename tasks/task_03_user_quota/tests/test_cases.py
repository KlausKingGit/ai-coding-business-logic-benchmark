from concurrent.futures import ThreadPoolExecutor
import pytest
from shared.candidate import load

QuotaService = load("task_03_user_quota").QuotaService


def test_deduct():
    assert QuotaService({"a": 5}).deduct("a", 2, "r") == 3


def test_exact_balance():
    assert QuotaService({"a": 5}).deduct("a", 5, "r") == 0


def test_insufficient_unchanged():
    s = QuotaService({"a": 5})
    with pytest.raises(ValueError):
        s.deduct("a", 6, "r")
    assert s.quota["a"] == 5


def test_idempotent():
    s = QuotaService({"a": 5})
    assert s.deduct("a", 2, "r") == s.deduct("a", 2, "r") == 3


def test_conflicting_retry():
    s = QuotaService({"a": 5})
    s.deduct("a", 2, "r")
    with pytest.raises(ValueError):
        s.deduct("a", 3, "r")


@pytest.mark.parametrize("amount", [0, -1, True])
def test_invalid_amount(amount):
    with pytest.raises(ValueError):
        QuotaService({"a": 5}).deduct("a", amount, "r")


def test_unknown_user():
    with pytest.raises(KeyError):
        QuotaService({"a": 5}).deduct("x", 1, "r")


def test_concurrent_limit():
    s = QuotaService({"a": 1})
    def call(i):
        try:
            s.deduct("a", 1, str(i))
            return True
        except ValueError:
            return False
    with ThreadPoolExecutor(max_workers=10) as pool:
        assert sum(pool.map(call, range(10))) == 1
    assert s.quota["a"] == 0


def test_retry_returns_original_result():
    s = QuotaService({"a": 10})
    assert s.deduct("a", 2, "r1") == 8
    assert s.deduct("a", 3, "r2") == 5
    assert s.deduct("a", 2, "r1") == 8
    assert s.quota["a"] == 5
