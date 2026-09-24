import pytest
from fastapi.testclient import TestClient
from shared.candidate import load

candidate = load("task_04_webhook_idempotency")
app, processor = candidate.app, candidate.processor

E = {"event_id": "e1", "payment_id": "p1", "amount_cents": 100}


@pytest.fixture
def client():
    processor.processed.clear()
    processor.calls = 0
    processor.fail = False
    yield TestClient(app)
    processor.fail = False


def test_process(client):
    assert client.post("/webhooks/payment", json=E).json() == {"status": "processed"}


def test_duplicate_success(client):
    client.post("/webhooks/payment", json=E)
    r = client.post("/webhooks/payment", json=E)
    assert r.status_code == 200 and r.json()["status"] == "already_processed"
    assert processor.calls == 1


def test_conflict(client):
    client.post("/webhooks/payment", json=E)
    assert client.post("/webhooks/payment", json=E | {"amount_cents": 200}).status_code == 409


@pytest.mark.parametrize("change", [{"event_id": ""}, {"payment_id": ""}, {"amount_cents": 0}, {"amount_cents": -1}])
def test_invalid(client, change):
    assert client.post("/webhooks/payment", json=E | change).status_code == 422


def test_missing_field(client):
    assert client.post("/webhooks/payment", json={"event_id": "e1"}).status_code == 422


def test_failure_retry(client, caplog):
    processor.fail = True
    r = client.post("/webhooks/payment", json=E | {"secret": "DO_NOT_LOG"})
    assert r.status_code == 503 and "DO_NOT_LOG" not in caplog.text
    assert processor.calls == 0
    assert processor.processed == {}
    processor.fail = False
    assert client.post("/webhooks/payment", json=E).json() == {"status": "processed"}
    assert processor.calls == 1
