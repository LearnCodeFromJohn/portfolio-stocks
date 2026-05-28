import json
from decimal import Decimal

from src.repositories.price_repository import get_prices_by_ticker
from src.services.risk_analyzer import generate_risk_report


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
    params = event.get("queryStringParameters") or {}
    ticker = params.get("ticker")

    if not ticker:
        return response(400, {"error": "ticker is required"})

    ticker = ticker.upper()

    prices = get_prices_by_ticker(ticker, limit=5000)

    if not prices:
        return response(404, {
            "error": f"No price data found for {ticker}"
        })

    report = generate_risk_report(ticker, prices)

    return response(200, report)