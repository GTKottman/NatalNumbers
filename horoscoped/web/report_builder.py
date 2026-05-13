"""Build template context for natal report pages."""
from __future__ import annotations

from datetime import datetime

from horoscoped.astro.julian_day import julian_day_ut
from horoscoped.astro.moon_math import local_to_utc
from horoscoped.astro.natal_positions import natal_positions
from horoscoped.content.sign_interpretations import (
    PlacementInterpretation,
    build_chart_stat_summary,
    build_chart_theme_summary,
    build_strength_growth_summary,
    placement_lookup,
)

from .numerology import _digit_sum, _reduce, build_numerology_report


def _interpretation_payload(placement: PlacementInterpretation) -> dict[str, object]:
    """Return JSON-safe placement interpretation data for templates."""
    return {
        "body_key": placement.body_key,
        "body_name": placement.body_name,
        "sign": placement.sign,
        "heading_raw": placement.heading_raw,
        "themes_text": placement.themes_text,
        "life_growth_text": placement.life_growth_text,
        "full_text": placement.full_text,
        "summary": placement.summary,
        "strengths": list(placement.strengths),
        "growth_edges": list(placement.growth_edges),
        "life_domains": list(placement.life_domains),
        "keywords": list(placement.keywords),
        "tone_tags": list(placement.tone_tags),
        "stat_scores": [
            {"label": score.label, "value": score.value}
            for score in placement.stat_scores
        ],
    }


def _vibrational(lam: float) -> tuple[int, str]:
    sector = int(lam // 30)
    deg_int = int(lam)
    total = _digit_sum(sector + 1) + _digit_sum(deg_int)
    result = _reduce(total)
    steps = f"sector {sector + 1} + deg digits {_digit_sum(deg_int)} = {total} → {result}"
    return result, steps


def _format_degree_minutes(deg: float) -> str:
    whole = int(deg)
    minutes = round((deg - whole) * 60)
    if minutes == 60:
        whole += 1
        minutes = 0
    return f"{whole}° {minutes:02d}'"


def build_report_context(*, place: str, birth_dt: datetime, timezone: str) -> dict[str, object]:
    utc = local_to_utc(birth_dt, timezone)
    jd = julian_day_ut(utc)
    natal_rows = natal_positions(utc)
    numerology = build_numerology_report(birth_dt)

    total_inf = sum(row.lam for row in natal_rows)
    interpretations = placement_lookup()
    active_interpretations: list[PlacementInterpretation] = []
    planets = []

    for row in natal_rows:
        vib, vib_steps = _vibrational(row.lam)
        influence = round(row.lam / total_inf * 100, 1) if total_inf > 0 else 0.0
        utc_stamp = utc.strftime("%Y-%m-%d %H:%M:%S")
        calc_tex = (
            r"\("
            rf"\lambda={row.lam:.4f}^\circ,\quad "
            rf"s=\left\lfloor\frac{{\lambda}}{{30}}\right\rfloor={row.sector},\quad "
            rf"d=\lambda-{row.sector}\times30={row.degree_in_sign:.4f}^\circ"
            r"\)"
        )
        calc_steps = [
            {
                "label": "UTC time",
                "tex": rf"\(\mathrm{{UTC}}={utc_stamp}\)",
            },
            {
                "label": "Ecliptic longitude",
                "tex": rf"\(\lambda={row.lam:.4f}^\circ\)",
                "note": "Apparent geocentric longitude from PyEphem.",
            },
            {
                "label": "Zodiac sector",
                "tex": (
                    r"\("
                    rf"s=\left\lfloor\frac{{\lambda}}{{30}}\right\rfloor="
                    rf"\left\lfloor\frac{{{row.lam:.4f}}}{{30}}\right\rfloor="
                    rf"{row.sector}\;({row.sign})"
                    r"\)"
                ),
            },
            {
                "label": "Degree inside sign",
                "tex": (
                    r"\("
                    rf"d=\lambda-s\times30={row.lam:.4f}-{row.sector}\times30="
                    rf"{row.degree_in_sign:.4f}^\circ"
                    r"\)"
                ),
            },
        ]
        placement_interpretation = interpretations.get((row.key, row.sign))
        interpretation_payload = None
        if placement_interpretation is not None:
            active_interpretations.append(placement_interpretation)
            interpretation_payload = _interpretation_payload(placement_interpretation)

        planets.append(
            {
                "key": row.key,
                "glyph": row.glyph,
                "name": row.name,
                "label": f"{row.glyph} {row.name}",
                "sign": row.sign,
                "lam": round(row.lam, 6),
                "longitude": f"{row.lam:.2f}°",
                "degree": f"{_format_degree_minutes(row.degree_in_sign)} {row.sign}",
                "degree_decimal": f"{row.degree_in_sign:.2f}°",
                "sector": row.sector,
                "calc_tex": calc_tex,
                "calc_steps": calc_steps,
                "vib": vib,
                "vib_steps": vib_steps,
                "influence": influence,
                "color": row.color,
                "interpretation": interpretation_payload,
            }
        )

    local_str = birth_dt.strftime("%Y-%m-%d %H:%M")
    utc_str = utc.strftime("%Y-%m-%d %H:%M UTC")
    birth_date_long = (
        birth_dt.strftime("%B") + " " + str(birth_dt.day) + ", " + str(birth_dt.year)
    )
    strength_growth_summary = build_strength_growth_summary(active_interpretations)

    return {
        "place": place,
        "local_str": local_str,
        "utc_str": utc_str,
        "birth_date_long": birth_date_long,
        "birth_date_iso": birth_dt.strftime("%Y-%m-%d"),
        "timezone": timezone,
        "birth_dt": birth_dt,
        "planets": planets,
        "numerology": numerology,
        "chart_stat_summary": build_chart_stat_summary(active_interpretations),
        "chart_theme_summary": build_chart_theme_summary(active_interpretations),
        "chart_strengths": strength_growth_summary["strengths"],
        "chart_growth_edges": strength_growth_summary["growth_edges"],
        "jd": jd,
    }
