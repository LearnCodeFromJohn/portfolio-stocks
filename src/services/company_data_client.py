# src/services/market_data_client.py

import os
import requests
# from decimal import Decimal

class CompanyDataError(Exception):
    pass

def fetch_company_overview(ticker: str) -> dict:
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise MarketDataError("Missing API key")

    response = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "OVERVIEW",
            "symbol": ticker.upper(),
            "apikey": api_key,
        },
        timeout=10,
    )

    response.raise_for_status()
    data = response.json()

    if not data or "Symbol" not in data:
        raise MarketDataError(f"No company overview found for {ticker}")

    return {
        "ticker": data.get("Symbol"),
        "symbol": data.get("Symbol"),
        "name": data.get("Name"),
        "sector": data.get("Sector"),
        "industry": data.get("Industry"),
        "market_cap": data.get("MarketCapitalization"),
        "pe_ratio": data.get("PERatio"),
        "dividend_yield": data.get("DividendYield"),
        "profit_margin": data.get("ProfitMargin"),
        "beta": data.get("Beta"),
        "description": data.get("Description"),
        "source": "alpha_vantage",
    }