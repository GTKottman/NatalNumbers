"""Rich Live explainer panels for Sun and Moon sign math."""
from __future__ import annotations

import sys
import time
from datetime import datetime

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from horoscoped.astro.moon_math.constants import MEAN_L0_DEG, MEAN_MOTION_DEG_PER_DAY
from horoscoped.astro.moon_math.longitude import MoonLongitude
from horoscoped.astro.sun_math import SunLongitude

console = Console(legacy_windows=False)


def ensure_utf8_stdout() -> None:
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass


def present_sun(utc: datetime, local_line: str, row: SunLongitude) -> None:
    ensure_utf8_stdout()
    steps = [
        (
            "1 | local -> UTC",
            f"{local_line}\nUTC = {utc.strftime('%Y-%m-%d %H:%M:%S')} UTC",
        ),
        ("2 | Julian Day", f"JD = {row.jd:.6f}"),
        ("3 | days since J2000", f"n = JD - 2451545.0 = {row.n:.6f}"),
        ("4 | mean longitude", f"L = 280.460 deg + 0.9856474 deg * n = {row.L:.4f} deg"),
        (
            "5 | equation of center",
            f"lambda = L + 1.915*sin(g) + 0.020*sin(2g)   |   g ~ {row.g:.4f} deg",
        ),
        ("6 | apparent lambda", f"lambda = {row.lam:.4f} deg"),
        (
            "7 | zodiac sector",
            f"floor(lambda / 30) = {row.sector}  ->  {row.sector * 30} deg .. {row.sector * 30 + 30} deg",
        ),
    ]
    _typewriter_panel(steps, "[magenta]Sun sign math[/]")
    tbl = Table(title="Result", show_header=False, border_style="magenta")
    tbl.add_row("lambda", f"{row.lam:.4f} deg")
    tbl.add_row("sector", str(row.sector))
    tbl.add_row("Sun sign", f"[bold yellow]{row.sign}[/]")
    _pulse_table(tbl)


def present_moon(utc: datetime, local_line: str, row: MoonLongitude) -> None:
    ensure_utf8_stdout()
    steps = [
        (
            "1 | local -> UTC",
            f"{local_line}\nUTC = {utc.strftime('%Y-%m-%d %H:%M:%S')} UTC",
        ),
        ("2 | Julian Day", f"JD = {row.jd:.6f}"),
        ("3 | days since J2000", f"n = JD - 2451545.0 = {row.n:.6f}"),
        (
            "4 | mean longitude",
            f"L = {MEAN_L0_DEG:.6f} deg + {MEAN_MOTION_DEG_PER_DAY:.6f} deg * n = {row.L_mean:.4f} deg",
        ),
        (
            "5 | apparent lambda (ephemeris)",
            f"lambda = {row.lam:.4f} deg  |  mean->apparent (short arc) = {row.mean_to_apparent_deg:+.4f} deg",
        ),
        (
            "6 | zodiac sector",
            f"floor(lambda / 30) = {row.sector}  ->  {row.sector * 30} deg .. {row.sector * 30 + 30} deg",
        ),
    ]
    _typewriter_panel(steps, "[magenta]Moon sign math[/]")
    tbl = Table(title="Result", show_header=False, border_style="magenta")
    tbl.add_row("mean L", f"{row.L_mean:.4f} deg")
    tbl.add_row("lambda", f"{row.lam:.4f} deg")
    tbl.add_row("sector", str(row.sector))
    tbl.add_row("Moon sign", f"[bold yellow]{row.sign}[/]")
    _pulse_table(tbl)


def _typewriter_panel(steps: list[tuple[str, str]], panel_title: str) -> None:
    acc: list[str] = []
    with Live(console=console, refresh_per_second=20, transient=False) as live:
        for title, body in steps:
            line = body
            shown = ""
            for i in range(1, len(line) + 1):
                shown = line[:i]
                block = "\n\n".join(acc + [f"[bold cyan]{title}[/]\n{shown}"])
                live.update(Panel(block, title=panel_title, border_style="blue"))
                time.sleep(0.018)
            acc.append(f"[bold cyan]{title}[/]\n{line}")
            live.update(Panel("\n\n".join(acc), title=panel_title, border_style="blue"))
            time.sleep(0.35)


def _pulse_table(tbl: Table) -> None:
    with Live(tbl, console=console, refresh_per_second=6, transient=False) as live:
        for i in range(6):
            tbl.border_style = "yellow" if i % 2 else "magenta"
            live.update(tbl)
            time.sleep(0.25)
