import os
import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
table = dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))


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