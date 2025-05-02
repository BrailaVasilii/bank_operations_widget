import pytest
import pandas as pd
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


def test_spending_by_category() -> None:
    data = {
        "Дата операции": ["2023-07-01", "2023-08-01", "2023-09-01"],
        "Категория": ["Супермаркеты", "Супермаркеты", "Развлечения"],
        "Сумма операции": [100, 150, 200],
    }
    transactions_dataframe = pd.DataFrame(data)
    total = spending_by_category(transactions_dataframe, "Супермаркеты", date="2023-10-01")
    assert total == 150


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {
                "Дата операции": ["2023-10-01", "2023-10-02"],
                "Сумма операции": [100, 300],
                "Категория": ["Еда", "Транспорт"],
            },
            {"Воскресенье": 100, "Понедельник": 300},
        ),
    ],
)
def test_spending_by_weekday(data, expected) -> None:
    transactions = pd.DataFrame(data)
    result = spending_by_weekday(transactions, date="2023-10-03")
    assert result == expected


def test_spending_by_workday() -> None:
    data = {
        "Дата операции": ["2023-10-01", "2023-10-02", "2023-10-03"],
        "Категория": ["Еда", "Еда", "Развлечения"],
        "Сумма операции": [100, 200, 300],
    }
    transactions = pd.DataFrame(data)
    result = spending_by_workday(transactions, date="2023-10-03")
    assert result == {"Рабочий": 250.0, "Выходной": 100.0}
