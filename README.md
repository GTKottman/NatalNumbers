# Horoscoped V2

FastAPI web app and command-line tools for birth-date astrology and numerology reports. The app calculates tropical zodiac placements, renders natal chart and numerology pages, and pulls structured interpretation text from packaged markdown files.

## Features

- FastAPI web interface for birth date, birth time, and IANA time zone input.
- Natal report with Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, and Pluto placements.
- Numerology report values derived from the birth date.
- Markdown-backed zodiac interpretation summaries for each body and sign.
- CLI explainers for Sun and Moon sign math.

## Project Structure

- `horoscoped/web/` - FastAPI app, report assembly, Jinja templates, and static assets.
- `horoscoped/astro/` - astronomy, zodiac, Julian Day, Sun, Moon, and natal position helpers.
- `horoscoped/content/` - parser and derived metadata for packaged sign interpretation markdown.
- `horoscoped/data/` - packaged sign interpretation files and reference data.
- `horoscoped/cli/` - command-line entry points and Rich presenters.
- `docs/` - standalone explainers and supporting documentation.
- `tests/` - unittest coverage for calculations, interpretation parsing, and web routes.

## Setup

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS or Linux:

```bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the Web App

```powershell
uvicorn horoscoped.web.app:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

## CLI Usage

Interactive Sun and Moon report:

```powershell
python -m horoscoped.cli.main
```

Sun sign explainer:

```powershell
python -m horoscoped.cli.sun_sign_cli --date 1990-05-17 --time 14:30 --tz America/New_York
```

Moon sign explainer:

```powershell
python -m horoscoped.cli.moon_sign_cli --date 1990-05-17 --time 14:30 --tz America/New_York
```

## Tests

```powershell
python -m unittest discover -s tests
```

## Notes

- Time zone names must be valid IANA identifiers such as `America/Chicago`.
- On Windows, `tzdata` is included in `requirements.txt` so `zoneinfo` can load IANA time zones.
- The local `venv/`, Python caches, test caches, and generated logs are ignored by Git.
