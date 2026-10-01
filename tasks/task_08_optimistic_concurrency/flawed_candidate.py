class ConflictError(RuntimeError):
    pass

class RecordStore:
    def __init__(self, records: dict[str, str]):
        self.records = {
            record_id: {"value": value, "version": 1}
            for record_id, value in records.items()
        }

    def update(self, record_id: str, expected_version: int, value: str) -> dict:
        if record_id not in self.records:
            raise KeyError(record_id)
        if isinstance(expected_version, bool) or not isinstance(expected_version, int) or expected_version <= 0:
            raise ValueError("expected_version must be a positive integer")

        current = self.records[record_id]
        if expected_version > current["version"]:
            raise ConflictError("version conflict")

        current["value"] = value
        current["version"] += 1
        return dict(current)
