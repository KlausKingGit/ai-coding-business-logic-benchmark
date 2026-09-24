from io import StringIO
import pytest
from shared.candidate import load

reconcile = load("task_02_payment_reconciliation").reconcile

O = "order_id,amount\na,10.00\nb,5.00\nc,2.00\n"
P = "payment_id,order_id,amount\np1,a,3.00\np2,a,7.00\np3,b,6.00\np4,x,1.00\n"


def run(o=O, p=P):
    return reconcile(StringIO(o), StringIO(p))


def test_multiple_payments():
    assert run()["orders"][0] == {"order_id": "a", "paid_cents": 1000, "unpaid_cents": 0, "status": "paid"}


def test_overpayment():
    assert run()["orders"][1]["status"] == "overpaid"


def test_unpaid():
    assert run()["orders"][2]["unpaid_cents"] == 200


def test_orphan():
    assert any(x["type"] == "orphan_payment" for x in run()["exceptions"])


def test_partial():
    assert run(p="payment_id,order_id,amount\np1,a,2.00\n")["orders"][0]["status"] == "partial"


def test_duplicate_payment_not_counted():
    result = run(p="payment_id,order_id,amount\np1,a,2.00\np1,a,2.00\n")
    assert result["orders"][0]["paid_cents"] == 200


def test_empty_amount():
    assert any(x["type"] == "invalid_payment" for x in run(p="payment_id,order_id,amount\np1,a,\n")["exceptions"])


def test_decimal_precision():
    assert run(o="order_id,amount\na,0.30\n", p="payment_id,order_id,amount\np1,a,0.10\np2,a,0.20\n")["orders"][0]["status"] == "paid"


def test_bad_columns():
    with pytest.raises(ValueError):
        run(o="id,amount\na,1.00\n")


def test_invalid_first_payment_id_still_reserved():
    result = run(p="payment_id,order_id,amount\np1,a,\np1,a,2.00\n")
    assert result["orders"][0]["paid_cents"] == 0
    assert [x["type"] for x in result["exceptions"]] == ["invalid_payment", "duplicate_or_missing_payment_id"]
