"""CLI: local birth time + IANA zone, animated explainer math, moon sign."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone

from moon_math import moon_longitude_pipeline
from sign_presenters import present_moon
from zoneinfo import ZoneInfo


def _parse_local_datetime(date_s: str, time_s: str) -> datetime:
    for tfmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(f"{date_s} {time_s}", f"%Y-%m-%d {tfmt}")
        except ValueError:
            continue
    raise ValueError("time must be HH:MM or HH:MM:SS (24-hour)")


def main() -> None:
    p = argparse.ArgumentParser(description="Moon sign from local birth time (explainer math).")
    p.add_argument("--date", required=True, help="YYYY-MM-DD")
    p.add_argument("--time", required=True, help="HH:MM or HH:MM:SS (24h local)")
    p.add_argument("--tz", required=True, help="IANA zone, e.g. America/New_York")
    args = p.parse_args()
    try:
        local = _parse_local_datetime(args.date.strip(), args.time.strip())
    except ValueError as e:
        raise SystemExit(str(e)) from e
    local = local.replace(tzinfo=ZoneInfo(args.tz))
    utc = local.astimezone(timezone.utc)
    row = moon_longitude_pipeline(utc)
    local_line = f"local = {local.strftime('%Y-%m-%d %H:%M:%S')} ({args.tz})"
    present_moon(utc, local_line, row)


if __name__ == "__main__":
    main()
