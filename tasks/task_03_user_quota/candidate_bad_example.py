class QuotaService:
    def __init__(self, initial):
        self.quota = initial

    def deduct(self, user_id, amount, request_id):
        self.quota[user_id] -= amount  # Duplicates and concurrent calls both deduct.
        return self.quota[user_id]
