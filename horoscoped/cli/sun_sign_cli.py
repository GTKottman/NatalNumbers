"""CLI: local birth time + IANA zone, animated explainer math, sun sign."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone

from horoscoped.astro.julian_day import julian_day_ut
from horoscoped.cli.sign_presenters import present_sun
from horoscoped.astro.sun_math import sun_longitude
from zoneinfo import ZoneInfo


def main() -> None:
    p = argparse.ArgumentParser(description="Sun sign from local birth time (explainer math).")
    p.add_argument("--date", required=True, help="YYYY-MM-DD")
    p.add_argument("--time", required=True, help="HH:MM (24h local)")
    p.add_argument("--tz", required=True, help="IANA zone, e.g. America/New_York")
    args = p.parse_args()
    local = datetime.strptime(f"{args.date} {args.time}", "%Y-%m-%d %H:%M")
    local = local.replace(tzinfo=ZoneInfo(args.tz))
    utc = local.astimezone(timezone.utc)
    jd = julian_day_ut(utc)
    row = sun_longitude(jd)
    local_line = f"local = {local.strftime('%Y-%m-%d %H:%M:%S')} ({args.tz})"
    present_sun(utc, local_line, row)


if __name__ == "__main__":
    main()
