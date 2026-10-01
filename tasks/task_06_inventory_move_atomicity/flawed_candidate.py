class InventoryService:
    def __init__(self, stock: dict[str, int]):
        self.stock = dict(stock)
        self.movements: list[dict] = []
        self.fail_record = False

    def _record(self, movement: dict) -> None:
        if self.fail_record:
            raise RuntimeError("movement store unavailable")
        self.movements.append(dict(movement))

    def move(self, source_sku: str, destination_sku: str, quantity: int, movement_id: str) -> dict:
        if not source_sku or not destination_sku or source_sku == destination_sku:
            raise ValueError("source and destination must be distinct non-empty SKUs")
        if source_sku not in self.stock or destination_sku not in self.stock:
            raise KeyError("unknown SKU")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("quantity must be a positive integer")
        if not movement_id:
            raise ValueError("movement_id is required")
        if self.stock[source_sku] < quantity:
            raise ValueError("insufficient stock")

        movement = {
            "movement_id": movement_id,
            "source_sku": source_sku,
            "destination_sku": destination_sku,
            "quantity": quantity,
        }
        self.stock[source_sku] -= quantity
        self.stock[destination_sku] += quantity
        self._record(movement)
        return dict(movement)
