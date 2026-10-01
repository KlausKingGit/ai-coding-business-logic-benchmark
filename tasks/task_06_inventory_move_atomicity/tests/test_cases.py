import pytest
from shared.candidate import load

InventoryService = load("task_06_inventory_move_atomicity").InventoryService

def test_move_success():
    service = InventoryService({"a": 5, "b": 1})
    movement = service.move("a", "b", 2, "m1")
    assert movement["movement_id"] == "m1"
    assert service.stock == {"a": 3, "b": 3}
    assert service.movements == [movement]

@pytest.mark.parametrize("quantity", [0, -1, True])
def test_invalid_quantity(quantity):
    service = InventoryService({"a": 5, "b": 1})
    with pytest.raises(ValueError):
        service.move("a", "b", quantity, "m1")
    assert service.stock == {"a": 5, "b": 1}

def test_insufficient_stock_is_unchanged():
    service = InventoryService({"a": 1, "b": 1})
    with pytest.raises(ValueError):
        service.move("a", "b", 2, "m1")
    assert service.stock == {"a": 1, "b": 1}
    assert service.movements == []

def test_unknown_sku():
    service = InventoryService({"a": 5, "b": 1})
    with pytest.raises(KeyError):
        service.move("a", "missing", 1, "m1")

def test_same_sku_rejected():
    service = InventoryService({"a": 5})
    with pytest.raises(ValueError):
        service.move("a", "a", 1, "m1")

def test_record_failure_is_atomic():
    service = InventoryService({"a": 5, "b": 1})
    service.fail_record = True
    with pytest.raises(RuntimeError):
        service.move("a", "b", 2, "m1")
    assert service.stock == {"a": 5, "b": 1}
    assert service.movements == []
