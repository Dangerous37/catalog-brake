import math


def evaluate(data):
    current = data["current"]
    expected = data["expected_pages"]
    limit = data["max_delete_fraction"]
    if type(expected) is not int or not 1 <= expected <= 100000:
        raise ValueError("expected_pages out of range")
    if type(limit) not in (int, float) or not math.isfinite(limit) or not 0 <= limit <= 1:
        raise ValueError("invalid maximum deletion fraction")
    if not isinstance(current, dict):
        raise ValueError("current must map SKUs to records")
    seen, incoming = set(), {}
    for page in data["pages"]:
        number = page["number"]
        if type(number) is not int or not 1 <= number <= expected or number in seen:
            raise ValueError("duplicate or unexpected page")
        seen.add(number)
        rows = page["rows"]
        if not isinstance(rows, dict) or incoming.keys() & rows.keys():
            raise ValueError("invalid page or repeated SKU")
        incoming.update(rows)
    missing = sorted(set(range(1, expected + 1)) - seen)
    absent = sorted(current.keys() - incoming.keys())
    fraction = len(absent) / len(current) if current else 0
    reason = "missing_pages" if missing else "deletion_limit" if fraction > limit else None
    return {"upsert": {k: incoming[k] for k in sorted(incoming) if k not in current or current[k] != incoming[k]},
            "delete": [] if reason else absent, "held": absent if reason else [],
            "reason": reason, "missing_pages": missing}
