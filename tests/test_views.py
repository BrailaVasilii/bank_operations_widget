import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
import pandas as pd
from src.views import main_page, events_page


# === Тесты для main_page ===
@pytest.mark.parametrize(
    "datetime_str, expected_greeting",
    [
        ("2023-10-01 09:30:00", "Доброе утро"),
        ("2023-10-01 13:15:00", "Добрый день"),
        ("2023-10-01 19:45:00", "Добрый вечер"),
        ("2023-10-01 02:30:00", "Доброй ночи"),
    ],
)
@patch("src.views.load_transactions")
@patch("src.views.get_currency_rate")
def test_main_page(mock_get_currency_rate, mock_load_transactions, datetime_str, expected_greeting) -> None:
    mock_transactions = {
        "Номер карты": ["1234", "5678", "1234", "9012", "5678"],
        "Сумма операции": [-200, -150, -600, -50, -300],
        "Сумма платежа": [-200, -150, -600, -50, -300],
        "Статус": ["OK", "OK", "OK", "OK", "FAIL"],
    }
    mock_load_transactions.return_value = pd.DataFrame(mock_transactions)
    mock_get_currency_rate.return_value = {"EUR": 0.95, "RUB": 100.5}

    result = main_page(datetime_str)

    assert result["greeting"] == expected_greeting
    assert "total_spent" in result
    assert "top_5_transactions" in result
    assert "currency_rates" in result


@pytest.mark.parametrize(
    "time_filter, expected_days, expected_expenses, expected_income",
    [
        ("W", 7, 200.0, 0.0),  # Неделя: только транзакции за последний день
        ("M", 30, 200.0, 300.0),  # Месяц: включаются 10-дневные транзакции
        ("Y", 365, 300.0, 300.0),  # Год: включается всё за год
        ("ALL", None, 300.0, 300.0),  # Все данные
    ],
)
@patch("src.views.load_transactions")
@patch("src.views.get_currency_rate")
@patch("src.views.get_stock_price")
def test_events_page(
    mock_get_stock_price,
    mock_get_currency_rate,
    mock_load_transactions,
    time_filter,
    expected_days,
    expected_expenses,
    expected_income,
) -> None:
    today = datetime(2023, 10, 1, 10, 0, 0)
    mock_transactions = {
        "Дата операции": [
            (today - timedelta(days=1)).strftime("%d.%m.%Y %H:%M:%S"),
            (today - timedelta(days=10)).strftime("%d.%m.%Y %H:%M:%S"),
            (today - timedelta(days=50)).strftime("%d.%m.%Y %H:%M:%S"),
        ],
        "Сумма операции": [-200, 300, -100],
        "Категория": ["Еда", "Зарплата", "Одежда"],
    }
    mock_load_transactions.return_value = pd.DataFrame(mock_transactions)
    mock_get_currency_rate.return_value = {"EUR": 0.95, "RUB": 100.5}
    mock_get_stock_price.return_value = 4200.5

    result = events_page(today.strftime("%Y-%m-%d %H:%M:%S"), time_filter)

    if expected_days is not None:
        expected_start_date = (today - timedelta(days=expected_days)).strftime("%Y-%m-%d")
        assert result["start_date"] == expected_start_date
    else:
        assert result["start_date"] == "2023-08-12"  # Минимальная дата в моках

    assert result["end_date"] == today.strftime("%Y-%m-%d")
    assert result["expenses"] == expected_expenses
    assert result["income"] == expected_income
    assert result["currency_rates"] == {"EUR": 0.95, "RUB": 100.5}
    assert result["stock_rates"] == {"S&P 500": 4200.5}
