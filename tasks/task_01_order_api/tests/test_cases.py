import pytest
from fastapi.testclient import TestClient
from tasks.task_01_order_api.reference_solution import app, store


@pytest.fixture
def client():
    store.orders.clear()
    store.fail = False
    yield TestClient(app)
    store.fail = False


BASE = {"order_id": "o1", "customer_id": "c1", "amount": 12.5}


def test_create(client):
    r = client.post("/orders", json=BASE)
    assert r.status_code == 201 and r.json() == BASE


def test_duplicate(client):
    client.post("/orders", json=BASE)
    assert client.post("/orders", json=BASE).status_code == 409
    assert len(store.orders) == 1


@pytest.mark.parametrize("change", [{"amount": 0}, {"amount": -1}, {"customer_id": ""}, {"order_id": ""}, {"amount": "bad"}])
def test_invalid(client, change):
    assert client.post("/orders", json=BASE | change).status_code == 422


def test_missing_customer(client):
    assert client.post("/orders", json={"order_id": "o1", "amount": 1}).status_code == 422


def test_store_failure(client):
    store.fail = True
    r = client.post("/orders", json=BASE)
    assert r.status_code == 503 and "database" not in r.text
    assert store.orders == {}
