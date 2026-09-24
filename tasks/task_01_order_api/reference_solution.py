from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class OrderIn(BaseModel):
    order_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    amount: float = Field(gt=0)


class Store:
    def __init__(self) -> None:
        self.orders: dict[str, dict] = {}
        self.fail = False

    def create(self, order: OrderIn) -> dict:
        if self.fail:
            raise OSError("database unavailable")
        if order.order_id in self.orders:
            raise KeyError(order.order_id)
        result = order.model_dump()
        self.orders[order.order_id] = result
        return result


store = Store()


@app.post("/orders", status_code=201)
def create_order(order: OrderIn) -> dict:
    try:
        return store.create(order)
    except KeyError as exc:
        raise HTTPException(409, "order already exists") from exc
    except OSError as exc:
        raise HTTPException(503, "order store unavailable") from exc
