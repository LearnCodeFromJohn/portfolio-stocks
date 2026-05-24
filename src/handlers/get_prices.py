# src/handlers/get_prices.py

import json
from decimal import Decimal
from src.repositories.price_repository import get_prices_by_ticker


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def handler(event, context):
    params = event.get("queryStringParameters") or {}
    ticker = params.get("ticker")

    if not ticker:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "ticker is required"})
        }

    prices = get_prices_by_ticker(ticker)

    return {
        "statusCode": 400,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps({"error": "ticker is required"})
    }