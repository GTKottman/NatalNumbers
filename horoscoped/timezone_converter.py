# IANA zones: zoneinfo (3.9+) uses system data; on Windows install `tzdata` or use pytz fallback.
try:
    from zoneinfo import available_timezones

    IANA_TIMEZONE_LIST = sorted(available_timezones())
except ImportError:
    IANA_TIMEZONE_LIST = []

if not IANA_TIMEZONE_LIST:
    try:
        import pytz

        IANA_TIMEZONE_LIST = sorted(pytz.all_timezones)
    except ImportError:
        IANA_TIMEZONE_LIST = []
