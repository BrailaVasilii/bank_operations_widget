import pandas as pd

from src.services import analyze_cashback_categories, get_currency_rate


def main():
    # Пример работы с транзакциями
    transactions = pd.DataFrame(
        [
            {"Дата операции": "2023-10-01", "Сумма операции": 100, "Категория": "Еда"},
            {"Дата операции": "2023-10-03", "Сумма операции": 300, "Категория": "Транспорт"},
        ]
    )
    # Анализ категорий
    cashback_result = analyze_cashback_categories(transactions, year=2023, month=10)

    # Работа с API валют
    forex = get_currency_rate("USD", ["EUR", "RUB"])

    # Возвращаем результат вместо печати
    return {"cashback": cashback_result, "currency_rates": forex}
