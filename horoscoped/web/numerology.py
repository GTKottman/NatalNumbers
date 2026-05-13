"""Numerology report calculations for the web app."""
from __future__ import annotations

from datetime import datetime

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


def build_numerology_report(date: datetime) -> list[dict[str, object]]:
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
