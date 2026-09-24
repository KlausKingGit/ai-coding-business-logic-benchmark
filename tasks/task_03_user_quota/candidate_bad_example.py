"""Avoids double deduction but returns today's balance for old retries."""
from threading import Lock


class QuotaService:
    def __init__(self, initial: dict[str, int]):
        if any(value < 0 for value in initial.values()):
            raise ValueError("negative initial quota")
        self.quota = initial.copy()
        self.requests: dict[str, tuple[str, int]] = {}
        self.lock = Lock()

    def deduct(self, user_id: str, amount: int, request_id: str) -> int:
        if not user_id or not request_id or type(amount) is not int or amount <= 0:
            raise ValueError("invalid request")
        with self.lock:
            previous = self.requests.get(request_id)
            if previous is not None:
                if previous != (user_id, amount):
                    raise ValueError("request_id reused with different payload")
                return self.quota[user_id]  # Original response was not retained.
            if user_id not in self.quota:
                raise KeyError(user_id)
            if self.quota[user_id] < amount:
                raise ValueError("insufficient quota")
            self.quota[user_id] -= amount
            self.requests[request_id] = (user_id, amount)
            return self.quota[user_id]
