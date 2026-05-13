"""Julian Day (UT), Gregorian calendar (Meeus Astronomical Algorithms 7.1)."""
from __future__ import annotations

from datetime import datetime, timezone

J2000_JD = 2451545.0


def julian_day_ut(dt: datetime) -> float:
    """Julian Day for a timezone-aware instant (converted to UTC internally)."""
    if dt.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    dt_utc = dt.astimezone(timezone.utc)
    y, m, d = dt_utc.year, dt_utc.month, dt_utc.day
    ut = (
        dt_utc.hour
        + dt_utc.minute / 60.0
        + dt_utc.second / 3600.0
        + dt_utc.microsecond / 3_600_000_000.0
    )
    if m <= 2:
        y -= 1
        m += 12
    a = y // 100
    b = 2 - a + a // 4
    jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5
    return jd + ut / 24.0
