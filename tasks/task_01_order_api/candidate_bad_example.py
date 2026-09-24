from fastapi import FastAPI

app = FastAPI()
orders = {}


@app.post("/orders")
def create_order(payload: dict) -> dict:
    # Runs on a happy path, but silently overwrites duplicate IDs.
    orders[payload["order_id"]] = payload
    return payload
