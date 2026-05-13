from datetime import datetime

from julian_day import julian_day_ut
from moon_math import local_to_utc, moon_longitude_pipeline
from sign_presenters import present_moon, present_sun
from sun_math import sun_longitude
from timezone_converter import IANA_TIMEZONE_LIST


def _parse_local_datetime(date_str: str, time_str: str) -> datetime:
    date_str = date_str.strip()
    time_str = time_str.strip()
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    t = None
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            t = datetime.strptime(time_str, fmt).time()
            break
        except ValueError:
            continue
    if t is None:
        raise ValueError("Time must be HH:MM or HH:MM:SS using 24-hour clock.")
    return datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)


def main() -> None:
    if not IANA_TIMEZONE_LIST:
        print("Could not load IANA time zones. Install tzdata (and use Python 3.9+) or pytz.")
        return

    print(
        "Sun and Moon signs from birth date, time, and time zone "
        "(same UTC instant for both; see explainers in the repo)."
    )
    print()
    place = input("Birth city, country (optional, for your records only): ").strip()
    date_s = input("Birth date (YYYY-MM-DD): ").strip()
    time_s = input("Birth time, 24-hour (HH:MM or HH:MM:SS): ").strip()
    tz = input("IANA time zone (e.g. America/Chicago): ").strip()

    if not tz:
        print()
        print("IANA time zone is required so local clock time can be converted to UTC.")
        return

    if tz not in IANA_TIMEZONE_LIST:
        print()
        print(f"Unknown IANA time zone: {tz!r}.")
        print("Use the exact name from the IANA database (region/city).")
        return

    try:
        birth_local = _parse_local_datetime(date_s, time_s)
    except ValueError as e:
        print()
        print(f"Could not parse date or time: {e}")
        return

    utc = local_to_utc(birth_local, tz)
    jd = julian_day_ut(utc)
    sun_row = sun_longitude(jd)
    moon_row = moon_longitude_pipeline(utc)
    print()
    local_line = f"local = {birth_local.isoformat()} ({tz})"
    if place:
        local_line = f"place = {place}\n{local_line}"
    present_sun(utc, local_line, sun_row)
    present_moon(utc, local_line, moon_row)


if __name__ == "__main__":
    main()
