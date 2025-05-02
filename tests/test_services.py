import pytest
from unittest.mock import patch
import pandas as pd
from src.services import investment_bank, get_currency_rate, get_stock_price, analyze_cashback_categories


@pytest.fixture
def transactions_data() -> None:
    """Фикстура с тестовыми данными транзакций."""
    return [
        {"Дата операции": "2023-10-01", "Сумма операции": 112.50},
        {"Дата операции": "2023-10-01", "Сумма операции": 49.75},
    ]


def test_investment_bank(transactions_data) -> None:
    result = investment_bank("2023-10", transactions_data, limit=50)
    assert result == 37.75


def test_get_currency_rate() -> None:
    with patch("src.services.requests.get") as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = {"rates": {"EUR": 0.85, "JPY": 110.25}}
        result = get_currency_rate("USD", ["EUR", "JPY"])
        assert result == {"EUR": 0.85, "JPY": 110.25}


def test_get_stock_price() -> None:
    with patch("src.services.requests.get") as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = {"quoteResponse": {"result": [{"regularMarketPrice": 4500.78}]}}
        result = get_stock_price("^GSPC")
        assert result == 4500.78


@pytest.mark.parametrize(
    "data, year, month, expected",
    [
        (
            [
                {"Дата операции": "2023-10-01", "Сумма операции": 100, "Категория": "Еда"},
                {"Дата операции": "2023-10-02", "Сумма операции": 200, "Категория": "Еда"},
                {"Дата операции": "2023-10-03", "Сумма операции": 300, "Категория": "Транспорт"},
            ],
            2023,
            10,
            {"Еда": 15.0, "Транспорт": 15.0},
        ),
    ],
)
def test_analyze_cashback_categories(data, year, month, expected) -> None:
    df = pd.DataFrame(data)
    result = analyze_cashback_categories(df, year=year, month=month)
    assert result == expected
