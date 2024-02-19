from datetime import datetime, timedelta, timezone


def set_tz(t):
    if isinstance(t, datetime):
        delta = timedelta(hours=5)
        return t.replace(tzinfo=timezone(offset=delta)) + delta
    return t
