import json
from unittest.mock import patch

from src.handlers.get_prices import handler


def test_get_prices_returns_cached_data_when_fresh():
    event = {
        "queryStringParameters": {
            "ticker": "AAPL"
        }
    }

    cached_prices = [
        {
            "ticker": "AAPL",
            "date": "2099-01-01",
            "price": 100,
            "close": 100,
            "volume": 1000,
        }
    ]

    with patch("src.handlers.get_prices.get_prices_by_ticker") as mock_get, \
         patch("src.handlers.get_prices.fetch_daily_prices") as mock_fetch:

        mock_get.return_value = cached_prices

        response = handler(event, None)
        body = json.loads(response["body"])

        assert response["statusCode"] == 200
        assert body["source"] == "cache"
        assert body["ticker"] == "AAPL"
        assert body["count"] == 1

        mock_fetch.assert_not_called()


def test_get_prices_missing_ticker_returns_400():
    event = {
        "queryStringParameters": {}
    }

    response = handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert body["error"] == "ticker is required"