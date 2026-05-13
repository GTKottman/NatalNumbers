"""Ephemeris-backed natal chart positions for the report page."""
from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

import ephem

from tropical_zodiac import TROPICAL_SIGNS


BodyFactory = Callable[[], ephem.Body]


@dataclass(frozen=True)
class NatalBody:
    key: str
    glyph: str
    name: str
    factory: BodyFactory
    color: str


@dataclass(frozen=True)
class NatalPosition:
    key: str
    glyph: str
    name: str
    lam: float
    sector: int
    sign: str
    degree_in_sign: float
    color: str


NATAL_BODIES: tuple[NatalBody, ...] = (
    NatalBody("sun", "☉", "Sun", ephem.Sun, "#f5b642"),
    NatalBody("moon", "☽", "Moon", ephem.Moon, "#6b8de3"),
    NatalBody("mercury", "☿", "Mercury", ephem.Mercury, "#8b8f9a"),
    NatalBody("venus", "♀", "Venus", ephem.Venus, "#c47ac0"),
    NatalBody("mars", "♂", "Mars", ephem.Mars, "#d65a4a"),
    NatalBody("jupiter", "♃", "Jupiter", ephem.Jupiter, "#b8863b"),
    NatalBody("saturn", "♄", "Saturn", ephem.Saturn, "#7a6a4f"),
    NatalBody("uranus", "⛢", "Uranus", ephem.Uranus, "#4fb3b8"),
    NatalBody("neptune", "♆", "Neptune", ephem.Neptune, "#4c6edb"),
    NatalBody("pluto", "♇", "Pluto", ephem.Pluto, "#6f4a8e"),
)


def normalize_degrees(value: float) -> float:
    """Normalize an angle to the [0, 360) range."""
    return value % 360.0


def longitude_to_sector(lambda_deg: float) -> int:
    """Map ecliptic longitude to a 30-degree tropical zodiac sector."""
    return int(normalize_degrees(lambda_deg) // 30) % 12


def apparent_ecliptic_longitude_deg(body_factory: BodyFactory, utc: datetime) -> float:
    """Return apparent geocentric ecliptic longitude in degrees."""
    utc = _ensure_utc(utc)
    body = body_factory()
    body.compute(ephem.Date(utc))
    lon_rad = ephem.Ecliptic(body).lon
    return normalize_degrees(math.degrees(lon_rad))


def natal_positions(utc: datetime) -> list[NatalPosition]:
    """Compute the report's natal chart positions for the configured bodies."""
    utc = _ensure_utc(utc)
    positions: list[NatalPosition] = []
    for body in NATAL_BODIES:
        lam = apparent_ecliptic_longitude_deg(body.factory, utc)
        sector = longitude_to_sector(lam)
        positions.append(
            NatalPosition(
                key=body.key,
                glyph=body.glyph,
                name=body.name,
                lam=lam,
                sector=sector,
                sign=TROPICAL_SIGNS[sector],
                degree_in_sign=lam - sector * 30.0,
                color=body.color,
            )
        )
    return positions


def _ensure_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return dt.astimezone(timezone.utc)
