"""Debug test for the real assets endpoint."""

import json
import unittest
from unittest.mock import patch

from src.api_server import app, cache


class ApiServerTestCase(unittest.TestCase):
    """Test case for the real assets endpoint."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.headers = {"X-API-KEY": "equity-shield-2024-secure-key"}
        self.mock_data = {
            "MSFT": {
                "market_cap": 1000.0,
                "revenue": 500.0,
                "last_updated": "2023-01-01",
            },
            "GOOG": {
                "market_cap": 2000.0,
                "revenue": 800.0,
                "last_updated": "2023-01-01",
            },
            "JPM": {
                "market_cap": 3000.0,
                "revenue": 1200.0,
                "last_updated": "2023-01-01",
            },
            "BAC": {
                "market_cap": 2500.0,
                "revenue": 1000.0,
                "last_updated": "2023-01-01",
            },
            "C": {
                "market_cap": 1800.0,
                "revenue": 900.0,
                "last_updated": "2023-01-01",
            },
            "PLD": {
                "market_cap": 1500.0,
                "revenue": 600.0,
                "last_updated": "2023-01-01",
            },
            "AMT": {
                "market_cap": 1700.0,
                "revenue": 700.0,
                "last_updated": "2023-01-01",
            },
            "SPG": {
                "market_cap": 1600.0,
                "revenue": 650.0,
                "last_updated": "2023-01-01",
            },
        }

    def test_get_real_assets(self):
        """Test real assets endpoint with pagination and filtering."""
        cache.clear()

        with patch("src.api_server.load_json_file") as mock_load:
            mock_load.return_value = self.mock_data

            response = self.app.get(
                "/api/real-assets",
                headers=self.headers,
                query_string={"page": "1", "per_page": "10"},
            )
            if response.status_code != 200:
                print(f"Response data: {response.data.decode('utf-8')}")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, dict)
            self.assertIn("data", data)
            self.assertIn("page", data)
            self.assertIn("per_page", data)
            self.assertIn("total", data)


if __name__ == "__main__":
    unittest.main()
