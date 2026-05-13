"""Naive local wall time plus IANA zone to UTC."""
from __future__ import annotations

from datetime import datetime, timezone


def _zoneinfo_or_pytz():
    try:
        from zoneinfo import ZoneInfo

        return ("zoneinfo", ZoneInfo)
    except ImportError:
        pass
    import pytz

    return ("pytz", pytz)


def local_to_utc(naive_local: datetime, iana_tz: str) -> datetime:
    """Interpret naive local wall time in `iana_tz` and return UTC."""
    kind, tzmod = _zoneinfo_or_pytz()
    if naive_local.tzinfo is not None:
        return naive_local.astimezone(timezone.utc)
    if kind == "zoneinfo":
        ZoneInfo = tzmod
        return naive_local.replace(tzinfo=ZoneInfo(iana_tz)).astimezone(timezone.utc)
    pytz = tzmod
    tz = pytz.timezone(iana_tz)
    return tz.localize(naive_local).astimezone(timezone.utc)
