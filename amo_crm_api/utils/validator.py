from datetime import datetime, timedelta, timezone


def set_tz(hours: int, minutes: int = 0):
    def replace(t):
        if isinstance(t, datetime):
            delta = timedelta(hours=hours, minutes=minutes)
            return t.replace(tzinfo=timezone(offset=delta)) + delta
        return t
    return replace
