# src/services/market_data_client.py

import os
import requests
from decimal import Decimal

class MarketDataError(Exception):
    pass


def fetch_daily_prices(ticker: str) -> list[dict]:
    """
    Fetch daily stock prices from Alpha Vantage.

    Returns:
        List of normalized price records
    """

    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise MarketDataError("Missing API key")

    url = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": api_key,
        "outputsize": "compact",  # last 100 days
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise MarketDataError(f"API request failed: {str(e)}")

    data = response.json()

    # Handle API limit or bad response
    if "Note" in data:
        raise MarketDataError("API rate limit exceeded")

    if "Error Message" in data:
        raise MarketDataError(f"Invalid ticker: {ticker}")

    time_series = data.get("Time Series (Daily)")
    if not time_series:
        raise MarketDataError("Unexpected API response format")

    prices = []

    for date, values in time_series.items():
        try:
            prices.append({
                "ticker": ticker.upper(),
                "date": date,
                "open": Decimal(values["1. open"]),
                "high": Decimal(values["2. high"]),
                "low": Decimal(values["3. low"]),
                "close": Decimal(values["4. close"]),
                "volume": int(values["5. volume"]),
            })
        except (KeyError, ValueError):
            # skip malformed entries
            continue

    return prices