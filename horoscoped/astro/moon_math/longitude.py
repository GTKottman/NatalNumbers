"""Moon mean longitude, pipeline, and sign from Julian Day and UTC."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from horoscoped.astro.julian_day import J2000_JD, julian_day_ut
from horoscoped.astro.tropical_zodiac import TROPICAL_SIGNS

from horoscoped.astro.moon_math.constants import MEAN_L0_DEG, MEAN_MOTION_DEG_PER_DAY
from horoscoped.astro.moon_math.ephemeris import apparent_moon_ecliptic_longitude_deg
from horoscoped.astro.moon_math.time_conversion import local_to_utc


def mean_moon_longitude_deg(jd_ut: float) -> float:
    """Illustrative mean longitude L = L0 + motion * n (n = days since J2000)."""
    n = jd_ut - J2000_JD
    l_deg = MEAN_L0_DEG + MEAN_MOTION_DEG_PER_DAY * n
    return l_deg % 360.0


def longitude_to_sign_index(lambda_deg: float) -> int:
    """Sector index = floor(lambda / 30) on [0, 360) degrees."""
    x = lambda_deg % 360.0
    if x < 0:
        x += 360.0
    return int(x // 30)


def longitude_to_sign_name(lambda_deg: float) -> str:
    return TROPICAL_SIGNS[longitude_to_sign_index(lambda_deg)]


@dataclass(frozen=True)
class MoonLongitude:
    """Intermediate values for explainer UI (matches docs/moon_sign_math_explainer.html)."""

    jd: float
    n: float
    L_mean: float
    lam: float
    mean_to_apparent_deg: float
    sector: int
    sign: str


def moon_longitude_pipeline(utc: datetime) -> MoonLongitude:
    """JD, mean L, apparent lambda, and sector from an aware UTC instant."""
    if utc.tzinfo is None:
        raise ValueError("datetime must be timezone-aware (UTC recommended).")
    utc = utc.astimezone(timezone.utc)
    jd = julian_day_ut(utc)
    n = jd - J2000_JD
    l_mean = mean_moon_longitude_deg(jd)
    lam = apparent_moon_ecliptic_longitude_deg(utc)
    delta = (lam - l_mean + 540.0) % 360.0 - 180.0
    sector = longitude_to_sign_index(lam)
    sign = TROPICAL_SIGNS[sector]
    return MoonLongitude(
        jd=jd,
        n=n,
        L_mean=l_mean,
        lam=lam,
        mean_to_apparent_deg=delta,
        sector=sector,
        sign=sign,
    )


@dataclass(frozen=True)
class MoonSignResult:
    moon_sign: str
    ecliptic_longitude_deg: float
    julian_day_ut: float
    utc_moment: datetime
    mean_longitude_deg: float


def moon_sign_from_birth(naive_local: datetime, iana_tz: str) -> MoonSignResult:
    """Birth local time + zone to Moon sign and intermediate values."""
    utc = local_to_utc(naive_local, iana_tz)
    row = moon_longitude_pipeline(utc)
    return MoonSignResult(
        moon_sign=row.sign,
        ecliptic_longitude_deg=row.lam,
        julian_day_ut=row.jd,
        utc_moment=utc,
        mean_longitude_deg=row.L_mean,
    )
