from __future__ import annotations

import math
import unittest
from datetime import datetime, timezone

import ephem

from natal_positions import NATAL_BODIES, natal_positions
from tropical_zodiac import TROPICAL_SIGNS


class NatalPositionsTest(unittest.TestCase):
    def test_positions_match_direct_pyephem_longitudes(self) -> None:
        utc = datetime(1990, 5, 17, 14, 30, tzinfo=timezone.utc)

        positions = natal_positions(utc)

        self.assertEqual(
            [(p.glyph, p.name) for p in positions],
            [
                ("☉", "Sun"),
                ("☽", "Moon"),
                ("☿", "Mercury"),
                ("♀", "Venus"),
                ("♂", "Mars"),
                ("♃", "Jupiter"),
                ("♄", "Saturn"),
                ("⛢", "Uranus"),
                ("♆", "Neptune"),
                ("♇", "Pluto"),
            ],
        )

        for body_def, position in zip(NATAL_BODIES, positions):
            body = body_def.factory()
            body.compute(ephem.Date(utc))
            expected_lam = math.degrees(ephem.Ecliptic(body).lon) % 360.0
            expected_sector = int(expected_lam // 30) % 12

            self.assertAlmostEqual(position.lam, expected_lam, places=10)
            self.assertEqual(position.sector, expected_sector)
            self.assertEqual(position.sign, TROPICAL_SIGNS[expected_sector])
            self.assertAlmostEqual(
                position.degree_in_sign,
                expected_lam - expected_sector * 30,
                places=10,
            )


if __name__ == "__main__":
    unittest.main()
