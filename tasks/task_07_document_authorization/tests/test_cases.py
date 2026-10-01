import pytest
from shared.candidate import load

DocumentStore = load("task_07_document_authorization").DocumentStore

def make_store():
    return DocumentStore({"d1": {"owner_id": "u1", "title": "Original"}})

def test_owner_can_rename():
    store = make_store()
    assert store.rename("u1", "member", "d1", "Updated")["title"] == "Updated"

def test_admin_can_rename_other_users_document():
    store = make_store()
    assert store.rename("admin-user", "admin", "d1", "Reviewed")["title"] == "Reviewed"

def test_unauthorized_rename_leaves_document_unchanged():
    store = make_store()
    with pytest.raises(PermissionError):
        store.rename("u2", "member", "d1", "Hijacked")
    assert store.documents["d1"] == {"owner_id": "u1", "title": "Original"}

@pytest.mark.parametrize("title", ["", "   ", None])
def test_invalid_title_rejected(title):
    store = make_store()
    with pytest.raises(ValueError):
        store.rename("u1", "member", "d1", title)
    assert store.documents["d1"]["title"] == "Original"

def test_unknown_document():
    store = make_store()
    with pytest.raises(KeyError):
        store.rename("u1", "member", "missing", "Title")
