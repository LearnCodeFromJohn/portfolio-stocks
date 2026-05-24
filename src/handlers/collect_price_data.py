# src/handlers/collect_price_data.py

import json
from src.services.market_data_client import fetch_daily_prices
from src.repositories.price_repository import save_prices


def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    ticker = body.get("ticker")

    if not ticker:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "ticker is required"})
        }

    prices = fetch_daily_prices(ticker)

    save_prices(prices)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps({
            "message": "Prices collected",
            "count": len(prices)
        })
    }