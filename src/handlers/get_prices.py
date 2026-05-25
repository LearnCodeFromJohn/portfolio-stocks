import json
from decimal import Decimal
from src.repositories.price_repository import get_prices_by_ticker


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(body, default=decimal_default),
    }


def handler(event, context):
    print("EVENT:", json.dumps(event))

    params = event.get("queryStringParameters") or {}
    ticker = params.get("ticker")

    if not ticker:
        return response(400, {"error": "ticker is required", "params": params})

    prices = get_prices_by_ticker(ticker)

    return response(200, {
        "ticker": ticker.upper(),
        "count": len(prices),
        "prices": prices,
    })