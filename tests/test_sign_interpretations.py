from __future__ import annotations

import re
import unittest
from pathlib import Path

from horoscoped.content.sign_interpretations import (
    BODY_DOC_FILES,
    SIGN_INFO_DIR,
    load_interpretation_documents,
    placement_lookup,
)
from horoscoped.astro.tropical_zodiac import TROPICAL_SIGNS


class SignInterpretationsTest(unittest.TestCase):
    def test_all_report_bodies_have_all_twelve_signs(self) -> None:
        docs = load_interpretation_documents()

        self.assertEqual(set(docs), set(BODY_DOC_FILES))
        for body_key, document in docs.items():
            with self.subTest(body=body_key):
                self.assertEqual(tuple(document.placements), TROPICAL_SIGNS)

        self.assertEqual(len(placement_lookup()), len(BODY_DOC_FILES) * len(TROPICAL_SIGNS))

    def test_each_placement_keeps_source_text_and_derived_fields(self) -> None:
        for document in load_interpretation_documents().values():
            for sign, placement in document.placements.items():
                with self.subTest(body=document.body_key, sign=sign):
                    self.assertTrue(placement.themes_text)
                    self.assertTrue(placement.life_growth_text)
                    self.assertEqual(
                        placement.full_text,
                        f"{placement.themes_text}\n\n{placement.life_growth_text}",
                    )
                    self.assertTrue(placement.summary)
                    self.assertTrue(placement.strengths)
                    self.assertTrue(placement.growth_edges)
                    self.assertTrue(placement.life_domains)
                    self.assertTrue(placement.keywords)
                    self.assertEqual(len(placement.stat_scores), 6)
                    for score in placement.stat_scores:
                        self.assertGreaterEqual(score.value, 10)
                        self.assertLessEqual(score.value, 96)

    def test_parser_preserves_original_placement_paragraphs(self) -> None:
        for body_key, filename in BODY_DOC_FILES.items():
            source_file = SIGN_INFO_DIR / filename
            source_text = source_file.read_text(encoding="utf-8")
            document = load_interpretation_documents()[body_key]

            for sign, placement in document.placements.items():
                with self.subTest(body=body_key, sign=sign):
                    original = _source_section_text(source_text, placement.heading_raw)
                    self.assertEqual(placement.full_text, original)


def _source_section_text(source_text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n\n(?P<body>.*?)(?=\n## |\n---|\Z)"
    match = re.search(pattern, source_text, flags=re.MULTILINE | re.DOTALL)
    if match is None:
        raise AssertionError(f"Could not find section {heading!r} in {Path()}")
    return match.group("body").strip()


if __name__ == "__main__":
    unittest.main()
