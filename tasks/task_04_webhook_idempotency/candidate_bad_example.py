from fastapi import FastAPI
import logging

app = FastAPI()
seen = set()


@app.post("/webhooks/payment")
def handle(payload: dict):
    logging.info("webhook payload=%s", payload)  # May expose token or secret.
    if payload["event_id"] in seen:
        return {"error": "duplicate"}  # Wrong success semantics.
    seen.add(payload["event_id"])
    return {"status": "processed"}
