"""Structured interpretation data derived from packaged sign markdown files."""
from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from horoscoped.astro.tropical_zodiac import TROPICAL_SIGNS


PACKAGE_DIR = Path(__file__).resolve().parents[1]
SIGN_INFO_DIR = PACKAGE_DIR / "data" / "sign_info"

BODY_DOC_FILES: dict[str, str] = {
    "sun": "sun_sign_zodiac_summaries.md",
    "moon": "moon_sign_zodiac_summaries.md",
    "mercury": "mercury_sign_zodiac_summaries.md",
    "venus": "venus_sign_zodiac_summaries.md",
    "mars": "mars_sign_zodiac_summaries.md",
    "jupiter": "jupiter_sign_zodiac_summaries.md",
    "saturn": "saturn_sign_zodiac_summaries.md",
    "uranus": "uranus_sign_zodiac_summaries.md",
    "neptune": "neptune_sign_zodiac_summaries.md",
    "pluto": "pluto_sign_zodiac_summaries.md",
}

BODY_DISPLAY_NAMES = {key: key.title() for key in BODY_DOC_FILES}

STAT_ORDER = (
    "Drive",
    "Stability",
    "Connection",
    "Insight",
    "Expression",
    "Growth Pressure",
)

STAT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Drive": (
        "action", "initiative", "courage", "confidence", "leadership", "competition",
        "adventure", "assertion", "will", "bravery", "pioneering", "strength",
        "independence", "freedom", "ambition",
    ),
    "Stability": (
        "steady", "steadiness", "stability", "routine", "reliable", "persistence",
        "patience", "discipline", "structure", "commitment", "security", "grounding",
        "practical", "responsibility", "long-term", "consistency",
    ),
    "Connection": (
        "relationship", "relationships", "family", "home", "belonging", "empathy",
        "care", "nurture", "partnership", "community", "friendship", "compassion",
        "cooperation", "fairness", "harmony", "love",
    ),
    "Insight": (
        "learning", "questions", "analysis", "research", "intuition", "truth",
        "psychology", "strategy", "perception", "discernment", "wisdom", "meaning",
        "knowledge", "systems", "awareness", "mystery",
    ),
    "Expression": (
        "communication", "writing", "speaking", "teaching", "creativity", "art",
        "performance", "self-expression", "voice", "storytelling", "beauty",
        "design", "music", "ideas", "sharing",
    ),
    "Growth Pressure": (
        "growth", "lessons", "challenge", "challenges", "pressure", "fear",
        "blocked", "tested", "transformation", "shadow", "control", "maturity",
        "boundaries", "healing", "releasing", "learn", "learning",
    ),
}

BODY_BASE_STATS: dict[str, dict[str, int]] = {
    "sun": {"Drive": 16, "Expression": 14, "Stability": 8},
    "moon": {"Connection": 18, "Insight": 10, "Stability": 8},
    "mercury": {"Insight": 18, "Expression": 16, "Drive": 6},
    "venus": {"Connection": 18, "Expression": 14, "Stability": 8},
    "mars": {"Drive": 20, "Growth Pressure": 10, "Expression": 6},
    "jupiter": {"Drive": 10, "Insight": 16, "Expression": 10},
    "saturn": {"Stability": 20, "Growth Pressure": 16, "Insight": 8},
    "uranus": {"Insight": 16, "Expression": 12, "Drive": 10},
    "neptune": {"Insight": 16, "Connection": 12, "Expression": 10},
    "pluto": {"Growth Pressure": 20, "Insight": 14, "Drive": 8},
}

SIGN_BASE_STATS: dict[str, dict[str, int]] = {
    "Aries": {"Drive": 18, "Expression": 6},
    "Taurus": {"Stability": 18, "Connection": 6},
    "Gemini": {"Insight": 12, "Expression": 14},
    "Cancer": {"Connection": 18, "Stability": 8},
    "Leo": {"Expression": 18, "Drive": 8},
    "Virgo": {"Insight": 14, "Stability": 12},
    "Libra": {"Connection": 16, "Expression": 8},
    "Scorpio": {"Insight": 14, "Growth Pressure": 14},
    "Sagittarius": {"Drive": 12, "Insight": 14},
    "Capricorn": {"Stability": 18, "Drive": 8},
    "Aquarius": {"Insight": 16, "Connection": 8},
    "Pisces": {"Connection": 12, "Insight": 14, "Expression": 8},
}

STRENGTH_TAXONOMY: dict[str, tuple[str, ...]] = {
    "Leadership": ("leadership", "leader", "initiative", "pioneering", "authority"),
    "Creative expression": ("creativity", "art", "performance", "music", "storytelling", "self-expression"),
    "Communication": ("communication", "writing", "speaking", "teaching", "language", "voice"),
    "Emotional intelligence": ("emotional", "empathy", "compassion", "sensitivity", "nurture"),
    "Practical mastery": ("practical", "systems", "details", "work", "craftsmanship", "organization"),
    "Relationship skill": ("relationship", "partnership", "diplomacy", "fairness", "cooperation", "harmony"),
    "Resilience": ("resilience", "survive", "survival", "strength", "discipline", "maturity"),
    "Insight and research": ("research", "psychology", "truth", "strategy", "analysis", "investigative"),
    "Expansion and meaning": ("travel", "philosophy", "meaning", "faith", "education", "worldview"),
    "Innovation": ("technology", "innovation", "future", "reform", "unconventional", "originality"),
    "Healing": ("healing", "caregiving", "recovery", "repair", "transformation"),
    "Grounded building": ("stability", "security", "commitment", "long-term", "patience", "building"),
}

GROWTH_EDGE_TAXONOMY: dict[str, tuple[str, ...]] = {
    "Patience and pacing": ("patience", "slow down", "rushing", "reacting", "follow-through"),
    "Healthy boundaries": ("boundaries", "losing themselves", "other people's needs", "care does not"),
    "Self-trust": ("trust themselves", "trust their voice", "doubting", "confidence slowly"),
    "Flexibility": ("adapt", "let go", "risk", "familiar", "rigid"),
    "Self-criticism": ("self-criticism", "perfect", "perfection", "mistakes", "unworthy"),
    "Emotional openness": ("vulnerability", "guarded", "emotional openness", "feelings"),
    "Control and power": ("control", "domination", "obsession", "manipulation", "revenge"),
    "Conflict honesty": ("conflict", "decisiveness", "avoidance", "peace built on avoidance"),
    "Grounding and discernment": ("grounding", "discernment", "fantasy", "escapism", "confusion"),
    "Humility and tact": ("humility", "tact", "certainty", "forced on others", "details"),
    "Rest and softness": ("rest", "softness", "productivity", "achievement", "status"),
    "Connection without distance": ("distant", "emotionally connected", "unique", "belonging"),
}

DOMAIN_TAXONOMY: dict[str, tuple[str, ...]] = {
    "Career and purpose": ("career", "work", "leadership", "management", "achievement", "authority"),
    "Relationships": ("relationship", "partnership", "love", "friendship", "social"),
    "Home and family": ("home", "family", "ancestry", "belonging"),
    "Creativity": ("creativity", "art", "music", "performance", "storytelling", "design"),
    "Learning and communication": ("learning", "writing", "speaking", "teaching", "questions", "information"),
    "Healing and psychology": ("healing", "psychology", "therapy", "trauma", "emotional"),
    "Money and security": ("money", "financial", "resources", "security", "stability", "possessions"),
    "Spirituality and meaning": ("spiritual", "faith", "meaning", "philosophy", "dreams", "intuition"),
    "Systems and technology": ("systems", "technology", "science", "reform", "community"),
}

BODY_GROWTH_FALLBACKS: dict[str, str] = {
    "sun": "Balanced confidence",
    "moon": "Emotional regulation",
    "mercury": "Mental focus",
    "venus": "Relationship balance",
    "mars": "Intentional action",
    "jupiter": "Measured expansion",
    "saturn": "Patient maturity",
    "uranus": "Grounded change",
    "neptune": "Clear boundaries",
    "pluto": "Healthy power",
}

SIGN_GROWTH_FALLBACKS: dict[str, str] = {
    "Aries": "Patience and pacing",
    "Taurus": "Flexibility",
    "Gemini": "Consistent focus",
    "Cancer": "Healthy boundaries",
    "Leo": "Humility and openness",
    "Virgo": "Self-acceptance",
    "Libra": "Clear decisions",
    "Scorpio": "Control and trust",
    "Sagittarius": "Tact and commitment",
    "Capricorn": "Rest and softness",
    "Aquarius": "Emotional connection",
    "Pisces": "Grounding and discernment",
}


@dataclass(frozen=True)
class StatScore:
    label: str
    value: int


@dataclass(frozen=True)
class PlacementInterpretation:
    body_key: str
    body_name: str
    sign: str
    heading_raw: str
    source_file: str
    themes_text: str
    life_growth_text: str
    full_text: str
    summary: str
    strengths: tuple[str, ...]
    growth_edges: tuple[str, ...]
    life_domains: tuple[str, ...]
    keywords: tuple[str, ...]
    tone_tags: tuple[str, ...]
    stat_scores: tuple[StatScore, ...]


@dataclass(frozen=True)
class BodyInterpretationDocument:
    body_key: str
    body_name: str
    source_file: str
    intro_markdown: str
    closing_note_markdown: str
    placements: dict[str, PlacementInterpretation]


def placement_lookup() -> dict[tuple[str, str], PlacementInterpretation]:
    """Return placement interpretations keyed by normalized body key and sign."""
    docs = load_interpretation_documents()
    return {
        (doc.body_key, sign): placement
        for doc in docs.values()
        for sign, placement in doc.placements.items()
    }


@lru_cache(maxsize=1)
def load_interpretation_documents() -> dict[str, BodyInterpretationDocument]:
    """Parse all sign information files into lossless structured documents."""
    return {
        body_key: _parse_body_document(body_key, SIGN_INFO_DIR / filename)
        for body_key, filename in BODY_DOC_FILES.items()
    }


def build_chart_theme_summary(
    placements: list[PlacementInterpretation],
    *,
    limit: int = 8,
) -> list[dict[str, object]]:
    """Aggregate recurring domains and keywords across the active chart."""
    counts: dict[str, int] = {}
    for placement in placements:
        for label in (*placement.life_domains, *placement.keywords):
            counts[label] = counts.get(label, 0) + 1

    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
    if not ranked:
        return []

    max_count = max(count for _, count in ranked)
    return [
        {
            "label": label,
            "count": count,
            "weight": round(count / max_count * 100),
        }
        for label, count in ranked
    ]


def build_chart_stat_summary(
    placements: list[PlacementInterpretation],
) -> list[dict[str, object]]:
    """Average placement stat scores into chart-level bars."""
    if not placements:
        return []

    totals = {label: 0 for label in STAT_ORDER}
    for placement in placements:
        for score in placement.stat_scores:
            totals[score.label] += score.value

    return [
        {
            "label": label,
            "value": round(totals[label] / len(placements)),
        }
        for label in STAT_ORDER
    ]


def build_strength_growth_summary(
    placements: list[PlacementInterpretation],
    *,
    limit: int = 6,
) -> dict[str, list[str]]:
    """Pick the most repeated strengths and growth edges for chart summaries."""
    return {
        "strengths": _rank_repeated_labels(
            label for placement in placements for label in placement.strengths
        )[:limit],
        "growth_edges": _rank_repeated_labels(
            label for placement in placements for label in placement.growth_edges
        )[:limit],
    }


def _parse_body_document(body_key: str, source_file: Path) -> BodyInterpretationDocument:
    body_name = BODY_DISPLAY_NAMES[body_key]
    text = source_file.read_text(encoding="utf-8").strip()
    sections = re.split(r"^##\s+", text, flags=re.MULTILINE)
    intro = _strip_h1(sections[0]).strip()

    placements: dict[str, PlacementInterpretation] = {}
    closing_note = ""
    for raw_section in sections[1:]:
        heading, _, section_body = raw_section.partition("\n")
        heading = heading.strip()
        section_body = section_body.strip()
        if heading == "Closing Note":
            closing_note = section_body.strip()
            continue

        sign = _sign_from_heading(body_key, heading)
        paragraphs = _paragraphs(section_body)
        if len(paragraphs) < 2:
            raise ValueError(f"{source_file} section {heading!r} needs two paragraphs")

        themes_text = paragraphs[0]
        life_growth_text = "\n\n".join(paragraphs[1:])
        full_text = f"{themes_text}\n\n{life_growth_text}"
        placements[sign] = _build_placement(
            body_key=body_key,
            body_name=body_name,
            sign=sign,
            heading_raw=heading,
            source_file=str(source_file),
            themes_text=themes_text,
            life_growth_text=life_growth_text,
            full_text=full_text,
        )

    missing = set(TROPICAL_SIGNS) - set(placements)
    if missing:
        raise ValueError(f"{source_file} is missing signs: {sorted(missing)}")

    return BodyInterpretationDocument(
        body_key=body_key,
        body_name=body_name,
        source_file=str(source_file),
        intro_markdown=intro,
        closing_note_markdown=closing_note,
        placements=placements,
    )


def _build_placement(
    *,
    body_key: str,
    body_name: str,
    sign: str,
    heading_raw: str,
    source_file: str,
    themes_text: str,
    life_growth_text: str,
    full_text: str,
) -> PlacementInterpretation:
    growth_edges = _taxonomy_matches(full_text, GROWTH_EDGE_TAXONOMY, limit=4)
    if not growth_edges:
        growth_edges = _fallback_growth_edges(body_key, sign)

    return PlacementInterpretation(
        body_key=body_key,
        body_name=body_name,
        sign=sign,
        heading_raw=heading_raw,
        source_file=source_file,
        themes_text=themes_text,
        life_growth_text=life_growth_text,
        full_text=full_text,
        summary=_summary_sentence(themes_text),
        strengths=tuple(_taxonomy_matches(full_text, STRENGTH_TAXONOMY, limit=4)),
        growth_edges=tuple(growth_edges),
        life_domains=tuple(_taxonomy_matches(full_text, DOMAIN_TAXONOMY, limit=4)),
        keywords=tuple(_keywords(full_text)),
        tone_tags=tuple(_tone_tags(body_key, sign, full_text)),
        stat_scores=tuple(_stat_scores(body_key, sign, full_text)),
    )


def _sign_from_heading(body_key: str, heading: str) -> str:
    body_name = BODY_DISPLAY_NAMES[body_key]
    for sign in TROPICAL_SIGNS:
        if heading == f"{sign} {body_name}" or heading == f"{body_name} in {sign}":
            return sign
    raise ValueError(f"Could not identify sign from heading {heading!r}")


def _strip_h1(text: str) -> str:
    return re.sub(r"^#\s+.*(?:\n|$)", "", text, count=1).strip()


def _paragraphs(text: str) -> list[str]:
    return [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", text.strip())
        if paragraph.strip() and paragraph.strip() != "---"
    ]


def _summary_sentence(text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return sentences[0] if sentences else text.strip()


def _taxonomy_matches(
    text: str,
    taxonomy: dict[str, tuple[str, ...]],
    *,
    limit: int,
) -> list[str]:
    lowered = text.lower()
    ranked: list[tuple[int, str]] = []
    for label, keywords in taxonomy.items():
        matches = sum(1 for keyword in keywords if keyword in lowered)
        if matches:
            ranked.append((matches, label))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [label for _, label in ranked[:limit]]


def _fallback_growth_edges(body_key: str, sign: str) -> list[str]:
    labels = [
        BODY_GROWTH_FALLBACKS.get(body_key, "Integration"),
        SIGN_GROWTH_FALLBACKS.get(sign, "Integration"),
    ]
    return list(dict.fromkeys(labels))


def _keywords(text: str, *, limit: int = 6) -> list[str]:
    lowered = text.lower()
    candidates = {
        keyword
        for keywords in (
            *STAT_KEYWORDS.values(),
            *STRENGTH_TAXONOMY.values(),
            *GROWTH_EDGE_TAXONOMY.values(),
            *DOMAIN_TAXONOMY.values(),
        )
        for keyword in keywords
        if " " not in keyword and keyword in lowered
    }
    return sorted(candidates, key=lambda keyword: (-lowered.count(keyword), keyword))[:limit]


def _tone_tags(body_key: str, sign: str, text: str) -> list[str]:
    tags = [BODY_DISPLAY_NAMES[body_key], sign]
    if "traditional" in text.lower():
        tags.append("Traditional dignity note")
    if body_key in {"uranus", "neptune", "pluto"}:
        tags.append("Generational")
    if body_key in {"sun", "moon", "mercury", "venus", "mars"}:
        tags.append("Personal")
    return tags


def _stat_scores(body_key: str, sign: str, text: str) -> list[StatScore]:
    lowered = text.lower()
    scores: dict[str, int] = {label: 28 for label in STAT_ORDER}

    for label, value in BODY_BASE_STATS.get(body_key, {}).items():
        scores[label] += value
    for label, value in SIGN_BASE_STATS.get(sign, {}).items():
        scores[label] += value

    for label, keywords in STAT_KEYWORDS.items():
        matches = sum(lowered.count(keyword) for keyword in keywords)
        scores[label] += min(matches * 7, 28)

    return [
        StatScore(label=label, value=max(10, min(96, scores[label])))
        for label in STAT_ORDER
    ]


def _rank_repeated_labels(labels: object) -> list[str]:
    counts: dict[str, int] = {}
    for label in labels:
        counts[str(label)] = counts.get(str(label), 0) + 1
    return [
        label
        for label, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]
