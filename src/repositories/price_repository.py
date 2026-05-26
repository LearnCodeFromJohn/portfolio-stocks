import os
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("PRICE_TABLE_NAME", "price_snapshots"))


def get_prices_by_ticker(ticker: str, limit: int = 5000) -> list[dict]:
    response = table.query(
        KeyConditionExpression=Key("ticker").eq(ticker.upper()),
        ScanIndexForward=False,  # newest first
        Limit=limit,
    )

    return response.get("Items", [])


def save_missing_prices(prices: list[dict], existing_dates: set[str]) -> int:
    saved_count = 0

    with table.batch_writer() as batch:
        for price in prices:
            if price["date"] not in existing_dates:
                batch.put_item(Item=price)
                saved_count += 1

    return saved_count