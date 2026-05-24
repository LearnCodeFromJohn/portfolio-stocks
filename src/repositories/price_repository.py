# src/repositories/price_repository.py

import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("price_snapshots")


def save_prices(prices):
    for price in prices:
        table.put_item(Item=price)
        
        
def get_prices_by_ticker(ticker: str) -> list[dict]:
    response = table.query(
        KeyConditionExpression=Key("ticker").eq(ticker.upper()),
        ScanIndexForward=False,  # newest dates first
        Limit=100
    )

    return response.get("Items", [])