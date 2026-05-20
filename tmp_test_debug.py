"""Temporary debug script for exercising the real assets endpoint."""

from unittest.mock import patch

from src.api_server import app, cache

# Test directly
with patch("src.api_server.load_json_file") as mock_load:
    mock_data = {
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
    }
    mock_load.return_value = mock_data

    client = app.test_client()
    app.testing = True

    # Clear cache before test
    cache.clear()

    response = client.get(
        "/api/real-assets",
        headers={"X-API-KEY": "equity-shield-2024-secure-key"},
        query_string={"page": "1", "per_page": "10"},
    )
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data.decode('utf-8')}")
