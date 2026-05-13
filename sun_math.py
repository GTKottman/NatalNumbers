"""Pure sun-sign math from Julian Day through ecliptic longitude (see sun_sign_math explainer)."""
from __future__ import annotations

import math
from dataclasses import dataclass

from julian_day import J2000_JD
from tropical_zodiac import TROPICAL_SIGNS


def _norm360(x: float) -> float:
    return x % 360.0


@dataclass(frozen=True)
class SunLongitude:
    jd: float
    n: float  # days since J2000
    L: float  # mean longitude (deg)
    g: float  # mean anomaly (deg), for equation of center
    lam: float  # apparent ecliptic longitude λ (deg)
    sign: str
    sector: int  # 0..11


def sun_longitude(jd: float) -> SunLongitude:
    n = jd - J2000_JD
    L = _norm360(280.460 + 0.9856474 * n)
    g = math.radians(_norm360(357.5291 + 0.98560028 * n))
    lam = _norm360(L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g))
    sector = int(lam // 30) % 12
    return SunLongitude(
        jd=jd,
        n=n,
        L=L,
        g=math.degrees(g),
        lam=lam,
        sign=TROPICAL_SIGNS[sector],
        sector=sector,
    )
