"""Horoscoped FastAPI web app."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from horoscoped.timezone_converter import IANA_TIMEZONE_LIST

from .numerology import build_numerology_report
from .report_builder import build_report_context

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Natal Numbers")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


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

    numerology = build_numerology_report(birth_dt) if birth_dt else []
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
                    date_part.year,
                    date_part.month,
                    date_part.day,
                    time_part.hour,
                    time_part.minute,
                    time_part.second,
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

    return templates.TemplateResponse(
        request,
        "report.html",
        build_report_context(place=place, birth_dt=birth_dt, timezone=timezone),
    )
