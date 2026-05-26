import os
import requests
from decimal import Decimal


class MarketDataError(Exception):
    pass


def fetch_daily_prices(ticker: str) -> list[dict]:
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")

    if not api_key:
        raise MarketDataError("Missing ALPHA_VANTAGE_API_KEY")

    outputsize = "compact"

    response = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker.upper(),
            "apikey": api_key,
            "outputsize": outputsize,
        },
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()

    if "Note" in data:
        raise MarketDataError("Alpha Vantage rate limit exceeded")

    if "Error Message" in data:
        raise MarketDataError(f"Invalid ticker: {ticker}")

    time_series = data.get("Time Series (Daily)")

    if not time_series:
        print("ALPHA VANTAGE RESPONSE:", data)
        raise MarketDataError("Unexpected API response format")

    prices = []

    for date, values in time_series.items():
        close_price = Decimal(values["4. close"])

        prices.append({
            "ticker": ticker.upper(),
            "date": date,
            "price": close_price,
            "open": Decimal(values["1. open"]),
            "high": Decimal(values["2. high"]),
            "low": Decimal(values["3. low"]),
            "close": close_price,
            "volume": int(values["5. volume"]),
        })

    return prices