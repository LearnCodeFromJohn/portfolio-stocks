import os
import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("COMPANY_OVERVIEWS_TABLE", "company_overviews"))


def get_company_overview(ticker: str) -> dict | None:
    response = table.get_item(
        Key={
            "ticker": ticker.upper()
        }
    )

    return response.get("Item")


def save_company_overview(overview: dict) -> dict:
    item = {
        **overview,
        "ticker": overview["ticker"].upper(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    table.put_item(Item=item)

    return item