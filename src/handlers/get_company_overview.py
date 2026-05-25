import json
from datetime import datetime, timezone, timedelta

from src.services.company_data_client import (
    fetch_company_overview,
    CompanyDataError,
)
from src.repositories.company_repository import (
    get_company_overview,
    save_company_overview,
)


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(body),
    }


def is_stale(item: dict) -> bool:
    updated_at = item.get("updated_at")

    if not updated_at:
        return True

    last_updated = datetime.fromisoformat(updated_at)
    age = datetime.now(timezone.utc) - last_updated

    return age > timedelta(days=30)


def handler(event, context):
    params = event.get("queryStringParameters") or {}
    ticker = params.get("ticker")

    if not ticker:
        return response(400, {"error": "ticker is required"})

    try:
        cached = get_company_overview(ticker)

        if cached and not is_stale(cached):
            return response(200, cached)

        fresh = fetch_company_overview(ticker)
        saved = save_company_overview(fresh)

        return response(200, saved)

    except CompanyDataError as e:
        return response(400, {"error": str(e)})

    except Exception as e:
        print("GET COMPANY OVERVIEW ERROR:", str(e))
        return response(500, {"error": "Failed to get company overview"})