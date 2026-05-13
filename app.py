"""Natal Numbers FastAPI webapp."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from julian_day import julian_day_ut
from moon_math import local_to_utc
from natal_positions import natal_positions
from sign_interpretations import (
    PlacementInterpretation,
    build_chart_stat_summary,
    build_chart_theme_summary,
    build_strength_growth_summary,
    placement_lookup,
)
from timezone_converter import IANA_TIMEZONE_LIST

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Natal Numbers")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# ---------------------------------------------------------------------------
# Numerology helpers
# ---------------------------------------------------------------------------

def _digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))


def _reduce(n: int) -> int:
    while n > 9 and n not in (11, 22, 33):
        n = _digit_sum(n)
    return n


def _reduction_path(n: int) -> list[int]:
    path = [n]
    while n > 9 and n not in (11, 22, 33):
        n = _digit_sum(n)
        path.append(n)
    return path


def _format_reduction(path: list[int]) -> str:
    return " → ".join(str(part) for part in path)


def _digit_expression(n: int) -> str:
    digits = [int(d) for d in str(abs(n))]
    return " + ".join(str(digit) for digit in digits) + f" = {sum(digits)}"


def _life_path(date: datetime) -> tuple[int, str]:
    m = _reduce(date.month)
    d = _reduce(date.day)
    y = _reduce(_digit_sum(date.year))
    raw = m + d + y
    result = _reduce(raw)
    steps = (
        f"{date.month}→{m}  +  {date.day}→{d}  +  "
        f"{date.year}→{_digit_sum(date.year)}→{y}  =  {raw}→{result}"
    )
    return result, steps


def _destiny(date: datetime) -> tuple[int, str]:
    total = _digit_sum(date.year) + _digit_sum(date.month) + _digit_sum(date.day)
    result = _reduce(total)
    return result, f"digit sum of full date = {total} → {result}"


def _soul_urge(date: datetime) -> tuple[int, str]:
    v = _reduce(date.month)
    result = _reduce(v + _reduce(date.day))
    return result, f"vowel reduction of birth numbers = {result}"


def _personality(date: datetime) -> tuple[int, str]:
    c = _reduce(date.day + date.month)
    result = _reduce(c)
    return result, f"consonant reduction = {result}"


def _maturity(life: int, destiny: int) -> tuple[int, str]:
    result = _reduce(life + destiny)
    return result, f"Life Path {life} + Destiny {destiny} = {life + destiny} → {result}"


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


def _numerology_item(
    *,
    item_id: str,
    label: str,
    value: int,
    steps: str,
    method: str,
    components: list[dict[str, str]],
    calculation: list[str],
    interpretation: list[str],
) -> dict[str, object]:
    return {
        "id": item_id,
        "label": label,
        "value": value,
        "steps": steps,
        "method": method,
        "components": components,
        "calculation": calculation,
        "interpretation": interpretation,
    }


def _build_numerology_report(date: datetime) -> list[dict[str, object]]:
    month_path = _reduction_path(date.month)
    day_path = _reduction_path(date.day)
    year_digit_sum = _digit_sum(date.year)
    year_path = _reduction_path(year_digit_sum)

    life_num, life_steps = _life_path(date)
    destiny_num, destiny_steps = _destiny(date)
    soul_num, soul_steps = _soul_urge(date)
    personality_num, personality_steps = _personality(date)
    maturity_num, maturity_steps = _maturity(life_num, destiny_num)

    life_raw = month_path[-1] + day_path[-1] + year_path[-1]
    life_path = _reduction_path(life_raw)
    destiny_total = (
        _digit_sum(date.year)
        + _digit_sum(date.month)
        + _digit_sum(date.day)
    )
    destiny_path = _reduction_path(destiny_total)
    soul_month = _reduce(date.month)
    soul_day = _reduce(date.day)
    soul_raw = soul_month + soul_day
    soul_path = _reduction_path(soul_raw)
    personality_raw = date.month + date.day
    personality_path = _reduction_path(personality_raw)
    maturity_raw = life_num + destiny_num
    maturity_path = _reduction_path(maturity_raw)

    return [
        _numerology_item(
            item_id="life-path",
            label="Life Path",
            value=life_num,
            steps=life_steps,
            method=(
                "Reduce the month, day, and year separately, add those "
                "reduced parts, then reduce the sum."
            ),
            components=[
                {
                    "label": "Month",
                    "source": str(date.month),
                    "digits": _digit_expression(date.month),
                    "reduction": _format_reduction(month_path),
                },
                {
                    "label": "Day",
                    "source": str(date.day),
                    "digits": _digit_expression(date.day),
                    "reduction": _format_reduction(day_path),
                },
                {
                    "label": "Year",
                    "source": str(date.year),
                    "digits": _digit_expression(date.year),
                    "reduction": _format_reduction(year_path),
                },
            ],
            calculation=[
                (
                    f"Reduced parts: {month_path[-1]} + {day_path[-1]} "
                    f"+ {year_path[-1]} = {life_raw}"
                ),
                f"Final reduction: {_format_reduction(life_path)}",
                f"Life Path = {life_num}",
            ],
            interpretation=[
                "This is the core path number, derived from the full birth date.",
                "It shows the primary pattern that the other numerology values orbit.",
            ],
        ),
        _numerology_item(
            item_id="destiny",
            label="Destiny",
            value=destiny_num,
            steps=destiny_steps,
            method=(
                "Add the digit sums of the year, month, and day, then reduce "
                "the combined total."
            ),
            components=[
                {
                    "label": "Year digit sum",
                    "source": str(date.year),
                    "digits": _digit_expression(date.year),
                    "reduction": str(_digit_sum(date.year)),
                },
                {
                    "label": "Month digit sum",
                    "source": str(date.month),
                    "digits": _digit_expression(date.month),
                    "reduction": str(_digit_sum(date.month)),
                },
                {
                    "label": "Day digit sum",
                    "source": str(date.day),
                    "digits": _digit_expression(date.day),
                    "reduction": str(_digit_sum(date.day)),
                },
            ],
            calculation=[
                (
                    f"Combined digit sums: {_digit_sum(date.year)} + "
                    f"{_digit_sum(date.month)} + {_digit_sum(date.day)} "
                    f"= {destiny_total}"
                ),
                f"Final reduction: {_format_reduction(destiny_path)}",
                f"Destiny = {destiny_num}",
            ],
            interpretation=[
                "This number emphasizes the full date as one combined signature.",
                "Master numbers 11, 22, and 33 are preserved when they appear.",
            ],
        ),
        _numerology_item(
            item_id="soul-urge",
            label="Soul Urge",
            value=soul_num,
            steps=soul_steps,
            method=(
                "Use the reduced month and reduced day as the inner-date "
                "components, then reduce their sum."
            ),
            components=[
                {
                    "label": "Reduced month",
                    "source": str(date.month),
                    "digits": _digit_expression(date.month),
                    "reduction": str(soul_month),
                },
                {
                    "label": "Reduced day",
                    "source": str(date.day),
                    "digits": _digit_expression(date.day),
                    "reduction": str(soul_day),
                },
            ],
            calculation=[
                f"Inner-date sum: {soul_month} + {soul_day} = {soul_raw}",
                f"Final reduction: {_format_reduction(soul_path)}",
                f"Soul Urge = {soul_num}",
            ],
            interpretation=[
                "This app derives Soul Urge from the birth numbers available in the report.",
                "It highlights the month-and-day pattern before the year is considered.",
            ],
        ),
        _numerology_item(
            item_id="personality",
            label="Personality",
            value=personality_num,
            steps=personality_steps,
            method=(
                "Add the raw birth month and day, then reduce the result to "
                "the displayed number."
            ),
            components=[
                {
                    "label": "Birth month",
                    "source": str(date.month),
                    "digits": _digit_expression(date.month),
                    "reduction": str(date.month),
                },
                {
                    "label": "Birth day",
                    "source": str(date.day),
                    "digits": _digit_expression(date.day),
                    "reduction": str(date.day),
                },
            ],
            calculation=[
                f"Month plus day: {date.month} + {date.day} = {personality_raw}",
                f"Final reduction: {_format_reduction(personality_path)}",
                f"Personality = {personality_num}",
            ],
            interpretation=[
                "This number focuses on the visible month-and-day combination.",
                "It gives a compact counterpart to the deeper full-date calculations.",
            ],
        ),
        _numerology_item(
            item_id="maturity",
            label="Maturity",
            value=maturity_num,
            steps=maturity_steps,
            method=(
                "Combine the already-derived Life Path and Destiny values, "
                "then reduce their sum."
            ),
            components=[
                {
                    "label": "Life Path",
                    "source": str(life_num),
                    "digits": str(life_num),
                    "reduction": str(life_num),
                },
                {
                    "label": "Destiny",
                    "source": str(destiny_num),
                    "digits": str(destiny_num),
                    "reduction": str(destiny_num),
                },
            ],
            calculation=[
                f"Life Path plus Destiny: {life_num} + {destiny_num} = {maturity_raw}",
                f"Final reduction: {_format_reduction(maturity_path)}",
                f"Maturity = {maturity_num}",
            ],
            interpretation=[
                "This is a synthesis number built from two major report values.",
                "It shows how the core path and full-date signature combine.",
            ],
        ),
    ]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {"timezones": IANA_TIMEZONE_LIST},
    )


@app.get("/numerology", response_class=HTMLResponse)
async def numerology_detail(
    request: Request,
    birth_date: str = "",
) -> HTMLResponse:
    errors: list[str] = []
    birth_dt: Optional[datetime] = None

    try:
        date_part = datetime.strptime(birth_date.strip(), "%Y-%m-%d").date()
        birth_dt = datetime(date_part.year, date_part.month, date_part.day)
    except ValueError:
        errors.append("Use a valid birth date in YYYY-MM-DD format.")

    numerology = _build_numerology_report(birth_dt) if birth_dt else []
    birth_date_long = (
        birth_dt.strftime("%B") + " " + str(birth_dt.day) + ", " + str(birth_dt.year)
        if birth_dt
        else ""
    )

    return templates.TemplateResponse(
        request,
        "numerology_detail.html",
        {
            "birth_date": birth_date,
            "birth_date_long": birth_date_long,
            "errors": errors,
            "numerology": numerology,
        },
        status_code=422 if errors else 200,
    )


@app.post("/report", response_class=HTMLResponse)
async def report(
    request: Request,
    place: str = Form(default=""),
    birth_date: str = Form(...),
    birth_time: str = Form(...),
    timezone: str = Form(...),
) -> HTMLResponse:
    errors: list[str] = []

    if timezone not in IANA_TIMEZONE_LIST:
        errors.append(f"Unknown IANA time zone: {timezone!r}")

    birth_dt: Optional[datetime] = None
    if not errors:
        try:
            date_part = datetime.strptime(birth_date.strip(), "%Y-%m-%d").date()
            time_part = None
            for fmt in ("%H:%M:%S", "%H:%M"):
                try:
                    time_part = datetime.strptime(birth_time.strip(), fmt).time()
                    break
                except ValueError:
                    continue
            if time_part is None:
                errors.append("Birth time must be HH:MM or HH:MM:SS (24-hour).")
            else:
                birth_dt = datetime(
                    date_part.year, date_part.month, date_part.day,
                    time_part.hour, time_part.minute, time_part.second,
                )
        except ValueError as exc:
            errors.append(f"Could not parse date: {exc}")

    if errors:
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "timezones": IANA_TIMEZONE_LIST,
                "errors": errors,
                "prefill": {
                    "place": place,
                    "birth_date": birth_date,
                    "birth_time": birth_time,
                    "timezone": timezone,
                },
            },
            status_code=422,
        )

    utc = local_to_utc(birth_dt, timezone)
    jd = julian_day_ut(utc)
    natal_rows = natal_positions(utc)

    numerology = _build_numerology_report(birth_dt)

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
    birth_date_long = birth_dt.strftime("%B") + " " + str(birth_dt.day) + ", " + str(birth_dt.year)
    strength_growth_summary = build_strength_growth_summary(active_interpretations)

    return templates.TemplateResponse(
        request,
        "report.html",
        {
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
        },
    )
