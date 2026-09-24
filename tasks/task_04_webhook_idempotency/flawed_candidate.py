"""Validates payloads but records an event before processing succeeds."""
import logging
from threading import Lock
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
app = FastAPI()


class Event(BaseModel):
    event_id: str = Field(min_length=1)
    payment_id: str = Field(min_length=1)
    amount_cents: int = Field(gt=0)


class Processor:
    def __init__(self):
        self.processed: dict[str, Event] = {}
        self.calls = 0
        self.fail = False
        self.lock = Lock()

    def handle(self, event: Event) -> bool:
        with self.lock:
            old = self.processed.get(event.event_id)
            if old is not None:
                if old != event:
                    raise ValueError("conflicting event")
                return False
            self.processed[event.event_id] = event  # Too early: failed events become duplicates.
            if self.fail:
                logger.error("webhook processing failed for event_id=%s", event.event_id)
                raise RuntimeError("processing failed")
            self.calls += 1
            return True


processor = Processor()


@app.post("/webhooks/payment")
def payment_webhook(event: Event) -> dict:
    try:
        processed = processor.handle(event)
    except ValueError as exc:
        raise HTTPException(409, "event_id conflict") from exc
    except RuntimeError as exc:
        raise HTTPException(503, "processing unavailable") from exc
    return {"status": "processed" if processed else "already_processed"}
