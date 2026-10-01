class ChargeCoordinator:
    def __init__(self, gateway):
        self.gateway = gateway

    def charge(self, request_id: str, amount_cents: int) -> dict:
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("request_id is required")
        if isinstance(amount_cents, bool) or not isinstance(amount_cents, int) or amount_cents <= 0:
            raise ValueError("amount_cents must be a positive integer")

        try:
            result = self.gateway.charge(request_id, amount_cents)
        except TimeoutError:
            return {"request_id": request_id, "status": "unknown"}

        return {
            "request_id": request_id,
            "status": "succeeded",
            "gateway_id": result["gateway_id"],
        }
