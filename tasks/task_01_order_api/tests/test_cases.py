import pytest
from fastapi.testclient import TestClient
from shared.candidate import load

candidate = load("task_01_order_api")
app, store = candidate.app, candidate.store


@pytest.fixture
def client():
    store.orders.clear()
    store.fail = False
    yield TestClient(app)
    store.fail = False


BASE = {"order_id": "o1", "customer_id": "c1", "amount_cents": 1250}


def test_create(client):
    r = client.post("/orders", json=BASE)
    assert r.status_code == 201 and r.json() == BASE


def test_duplicate(client):
    client.post("/orders", json=BASE)
    assert client.post("/orders", json=BASE).status_code == 409
    assert len(store.orders) == 1


@pytest.mark.parametrize("change", [{"amount_cents": 0}, {"amount_cents": -1}, {"customer_id": ""}, {"order_id": ""}, {"amount_cents": "bad"}])
def test_invalid(client, change):
    assert client.post("/orders", json=BASE | change).status_code == 422


def test_missing_customer(client):
    assert client.post("/orders", json={"order_id": "o1", "amount_cents": 1}).status_code == 422


def test_store_failure(client):
    store.fail = True
    r = client.post("/orders", json=BASE)
    assert r.status_code == 503 and "database" not in r.text
    assert store.orders == {}


def test_reject_fractional_cents(client):
    assert client.post("/orders", json=BASE | {"amount_cents": 12.5}).status_code == 422
