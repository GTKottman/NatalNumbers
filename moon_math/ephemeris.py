"""Third-party lunar ephemeris (apparent geocentric ecliptic longitude)."""
from __future__ import annotations

import math
from datetime import datetime, timezone

import ephem


def apparent_moon_ecliptic_longitude_deg(dt_utc: datetime) -> float:
    """Apparent geocentric ecliptic longitude lambda (tropical), via ephem."""
    dt_utc = dt_utc.astimezone(timezone.utc)
    moon = ephem.Moon()
    moon.compute(ephem.Date(dt_utc))
    lon_rad = ephem.Ecliptic(moon).lon
    return math.degrees(lon_rad) % 360.0
