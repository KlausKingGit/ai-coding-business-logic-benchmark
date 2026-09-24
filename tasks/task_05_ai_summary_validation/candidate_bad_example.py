import json


def validate_summary(raw, facts):
    # Parses JSON but trusts the model's invented identities and amounts.
    return json.loads(raw)
