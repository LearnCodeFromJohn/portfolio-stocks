from unittest.mock import patch, Mock

from src.services.company_data_client import fetch_company_overview


def test_fetch_company_overview_parses_alpha_vantage_response(monkeypatch):
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "fake-key")

    fake_response = {
        "Symbol": "AAPL",
        "Name": "Apple Inc",
        "Sector": "TECHNOLOGY",
        "Industry": "CONSUMER ELECTRONICS",
        "MarketCapitalization": "4535749181000",
        "PERatio": "37.43",
        "DividendYield": "0.0034",
        "ProfitMargin": "0.272",
        "Beta": "1.065",
        "Description": "Apple Inc. description here.",
    }

    mock_response = Mock()
    mock_response.json.return_value = fake_response
    mock_response.raise_for_status.return_value = None

    with patch("src.services.company_data_client.requests.get", return_value=mock_response):
        overview = fetch_company_overview("AAPL")

    assert overview["ticker"] == "AAPL"
    assert overview["symbol"] == "AAPL"
    assert overview["name"] == "Apple Inc"
    assert overview["sector"] == "TECHNOLOGY"
    assert overview["market_cap"] == "4535749181000"