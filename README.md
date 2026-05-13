# Horoscoped V2

FastAPI web app and command-line tools for birth-date astrology and numerology reports. The app calculates tropical zodiac placements, renders natal chart and numerology pages, and pulls structured interpretation text from the `Sign info` markdown files.

## Features

- FastAPI web interface for birth date, birth time, and IANA time zone input.
- Natal report with Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, and Pluto placements.
- Numerology report values derived from the birth date.
- Markdown-backed zodiac interpretation summaries for each body and sign.
- CLI explainers for Sun and Moon sign math.

## Project Structure

- `app.py` - FastAPI routes and report assembly.
- `templates/` - Jinja templates for the web UI.
- `static/` - CSS and browser-side assets.
- `moon_math/`, `sun_math.py`, `julian_day.py` - astronomy and time conversion helpers.
- `sign_interpretations.py` - parser and derived metadata for `Sign info/`.
- `test_*.py` - unittest coverage for natal positions and sign interpretation parsing.

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
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

## CLI Usage

Interactive Sun and Moon report:

```powershell
python main.py
```

Sun sign explainer:

```powershell
python sun_sign_cli.py --date 1990-05-17 --time 14:30 --tz America/New_York
```

Moon sign explainer:

```powershell
python moon_sign_cli.py --date 1990-05-17 --time 14:30 --tz America/New_York
```

## Tests

```powershell
python -m unittest
```

## Notes

- Time zone names must be valid IANA identifiers such as `America/Chicago`.
- On Windows, `tzdata` is included in `requirements.txt` so `zoneinfo` can load IANA time zones.
- The local `venv/`, Python caches, test caches, and generated logs are ignored by Git.
