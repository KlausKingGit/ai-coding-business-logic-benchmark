import pytest
from shared.candidate import load

candidate = load("task_08_optimistic_concurrency")
RecordStore = candidate.RecordStore
ConflictError = candidate.ConflictError

def test_update_current_version():
    store = RecordStore({"r1": "v1"})
    assert store.update("r1", 1, "v2") == {"value": "v2", "version": 2}

def test_stale_update_rejected_and_unchanged():
    store = RecordStore({"r1": "v1"})
    store.update("r1", 1, "v2")
    with pytest.raises(ConflictError):
        store.update("r1", 1, "stale")
    assert store.records["r1"] == {"value": "v2", "version": 2}

def test_future_version_rejected_and_unchanged():
    store = RecordStore({"r1": "v1"})
    with pytest.raises(ConflictError):
        store.update("r1", 2, "future")
    assert store.records["r1"] == {"value": "v1", "version": 1}

@pytest.mark.parametrize("version", [0, -1, True])
def test_invalid_version(version):
    store = RecordStore({"r1": "v1"})
    with pytest.raises(ValueError):
        store.update("r1", version, "x")
    assert store.records["r1"] == {"value": "v1", "version": 1}

def test_missing_record():
    store = RecordStore({"r1": "v1"})
    with pytest.raises(KeyError):
        store.update("missing", 1, "x")
