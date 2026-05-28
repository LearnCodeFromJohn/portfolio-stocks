from decimal import Decimal
from math import sqrt


def calculate_daily_returns(prices: list[dict]) -> list[Decimal]:
    sorted_prices = sorted(prices, key=lambda p: p["date"])

    returns = []

    for i in range(1, len(sorted_prices)):
        previous_close = Decimal(str(sorted_prices[i - 1]["close"]))
        current_close = Decimal(str(sorted_prices[i]["close"]))

        if previous_close == 0:
            continue

        daily_return = (current_close - previous_close) / previous_close
        returns.append(daily_return)

    return returns


def calculate_total_return(prices: list[dict]) -> Decimal:
    sorted_prices = sorted(prices, key=lambda p: p["date"])

    first_close = Decimal(str(sorted_prices[0]["close"]))
    last_close = Decimal(str(sorted_prices[-1]["close"]))

    if first_close == 0:
        return Decimal("0")

    return (last_close - first_close) / first_close


def calculate_volatility(prices: list[dict]) -> Decimal:
    returns = calculate_daily_returns(prices)

    if len(returns) < 2:
        return Decimal("0")

    mean_return = sum(returns) / Decimal(len(returns))

    variance = sum(
        (r - mean_return) ** 2 for r in returns
    ) / Decimal(len(returns) - 1)

    daily_volatility = Decimal(str(sqrt(float(variance))))
    annualized_volatility = daily_volatility * Decimal(str(sqrt(252)))

    return annualized_volatility


def calculate_max_drawdown(prices: list[dict]) -> Decimal:
    sorted_prices = sorted(prices, key=lambda p: p["date"])

    peak = Decimal(str(sorted_prices[0]["close"]))
    max_drawdown = Decimal("0")

    for price in sorted_prices:
        close = Decimal(str(price["close"]))

        if close > peak:
            peak = close

        drawdown = (close - peak) / peak

        if drawdown < max_drawdown:
            max_drawdown = drawdown

    return max_drawdown


def generate_risk_report(ticker: str, prices: list[dict]) -> dict:
    if not prices or len(prices) < 2:
        return {
            "ticker": ticker.upper(),
            "error": "Not enough price data to calculate risk report",
        }

    sorted_prices = sorted(prices, key=lambda p: p["date"])

    latest = sorted_prices[-1]
    first = sorted_prices[0]

    return {
        "ticker": ticker.upper(),
        "start_date": first["date"],
        "end_date": latest["date"],
        "data_points": len(sorted_prices),
        "latest_price": latest["close"],
        "total_return": calculate_total_return(sorted_prices),
        "annualized_volatility": calculate_volatility(sorted_prices),
        "max_drawdown": calculate_max_drawdown(sorted_prices),
    }