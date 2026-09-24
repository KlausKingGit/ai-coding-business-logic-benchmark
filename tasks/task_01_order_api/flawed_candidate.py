"""Looks typed and handles errors, but duplicates silently overwrite orders."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class OrderIn(BaseModel):
    order_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    amount_cents: int = Field(gt=0, strict=True)


class Store:
    def __init__(self):
        self.orders: dict[str, dict] = {}
        self.fail = False

    def create(self, order: OrderIn) -> dict:
        if self.fail:
            raise OSError("database unavailable")
        result = order.model_dump()
        self.orders[order.order_id] = result  # Missing duplicate check.
        return result


store = Store()


@app.post("/orders", status_code=201)
def create_order(order: OrderIn) -> dict:
    try:
        return store.create(order)
    except OSError as exc:
        raise HTTPException(503, "order store unavailable") from exc
