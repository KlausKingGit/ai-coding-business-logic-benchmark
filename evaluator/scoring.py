def score(passed: int, failed: int) -> int:
    """Transparent test score. No subjective quality claims are automated."""
    total = passed + failed
    return round(100 * passed / total) if total else 0
