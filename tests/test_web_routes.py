from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from horoscoped.web.app import app


class WebRoutesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_index_renders(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Get Your Free Math Report", response.text)

    def test_numerology_validation_error_renders(self) -> None:
        response = self.client.get("/numerology", params={"birth_date": "not-a-date"})

        self.assertEqual(response.status_code, 422)
        self.assertIn("Use a valid birth date", response.text)

    def test_report_validation_error_renders(self) -> None:
        response = self.client.post(
            "/report",
            data={
                "place": "Chicago, USA",
                "birth_date": "1990-05-17",
                "birth_time": "14:30",
                "timezone": "Not/AZone",
            },
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn("Unknown IANA time zone", response.text)

    def test_report_renders_with_selected_birthplace(self) -> None:
        response = self.client.post(
            "/report",
            data={
                "place": "Chicago, USA",
                "birth_date": "1990-05-17",
                "birth_time": "14:30",
                "timezone": "America/Chicago",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Chicago, USA", response.text)
        self.assertIn("America/Chicago", response.text)

    def test_static_assets_remain_available(self) -> None:
        css_response = self.client.get("/static/style.css")
        js_response = self.client.get("/static/orbital.js")
        picker_response = self.client.get("/static/location-picker.js")

        self.assertEqual(css_response.status_code, 200)
        self.assertEqual(js_response.status_code, 200)
        self.assertEqual(picker_response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
