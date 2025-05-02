import pandas as pd
from datetime import datetime, timedelta
from src.utils import load_transactions
from src.services import get_currency_rate, get_stock_price


def main_page(date_str: str) -> dict:
    """
    Возвращает данные для главной страницы:
    - Приветствие,
    - Суммы расходов по картам,
    - Топ-5 транзакций,
    - Курсы валют.
    """
    # Приветствие по времени суток
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    hour = date.hour
    if 6 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 18:
        greeting = "Добрый день"
    elif 18 <= hour < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    # Загрузка данных транзакций
    transactions = load_transactions("data/operations.xls")

    # Проверка наличия необходимых столбцов
    required_columns = {"Номер карты", "Сумма операции", "Сумма платежа", "Статус"}
    if not required_columns.issubset(transactions.columns):
        raise ValueError(f"Отсутствуют необходимые столбцы в данных: {required_columns - set(transactions.columns)}")

    # Удаляем записи с отсутствующими номерами карт
    transactions = transactions.dropna(subset=["Номер карты"])

    # Преобразуем все суммы операций и платежей в абсолютные значения
    transactions["Сумма операции"] = transactions["Сумма операции"].abs()
    transactions["Сумма платежа"] = transactions["Сумма платежа"].abs()

    # Фильтруем только успешные операции
    transactions = transactions[transactions["Статус"] == "OK"]

    # Сумма расходов по картам
    total_spent = transactions.groupby("Номер карты")["Сумма операции"].sum()

    # Топ-5 транзакций по сумме операции
    top_5_transactions = transactions.nlargest(5, "Сумма операции").to_dict(orient="records")

    # Курсы валют (пример с фиксированными валютами)
    currency_rates = get_currency_rate(base="USD", symbols=["EUR", "RUB"])

    # Сформировать ответ
    return {
        "greeting": greeting,
        "total_spent": total_spent.to_dict(),
        "top_5_transactions": top_5_transactions,
        "currency_rates": currency_rates,
    }


def events_page(date_str: str, time_filter: str = "ALL") -> dict:
    """
    Возвращает данные для страницы "События":
    - Фильтрация по временным диапазонам (ALL, W, M, Y),
    - Расходы и поступления,
    - Курсы валют,
    - Курсы акций (значения по умолчанию в случае ошибки API).
    """
    # Загрузка данных транзакций
    transactions = load_transactions("data/operations.xls")

    # Проверка наличия необходимых столбцов
    required_columns = {"Дата операции", "Сумма операции", "Категория"}
    if not required_columns.issubset(transactions.columns):
        raise ValueError(f"Отсутствуют необходимые столбцы в данных: {required_columns - set(transactions.columns)}")

    # Преобразуем колонку с датой в формат datetime
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", dayfirst=True
    )

    # Определяем временной диапазон
    end_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    if time_filter == "W":
        start_date = end_date - timedelta(days=7)
    elif time_filter == "M":
        start_date = end_date - timedelta(days=30)
    elif time_filter == "Y":
        start_date = end_date - timedelta(days=365)
    else:  # time_filter == "ALL"
        start_date = transactions["Дата операции"].min()  # Уже будет в формате datetime

    # Фильтруем транзакции по диапазону дат
    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
    ]

    # Анализируем расходы и доходы
    expenses = abs(filtered_transactions[filtered_transactions["Сумма операции"] < 0]["Сумма операции"].sum())
    income = filtered_transactions[filtered_transactions["Сумма операции"] > 0]["Сумма операции"].sum()

    # Курсы валют
    currency_rates = get_currency_rate(base="USD", symbols=["EUR", "RUB"])

    # Получаем текущую цену акций (или значение по умолчанию)
    sp500_price = get_stock_price("^GSPC")
    if sp500_price is None:  # Если API недоступен, используем фиксированное значение
        sp500_price = 4321.54

    # Сформировать JSON-ответ
    return {
        "time_filter": time_filter,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "expenses": round(float(expenses), 2),  # Преобразуем в float
        "income": round(float(income), 2),
        "currency_rates": currency_rates,
        "stock_rates": {"S&P 500": sp500_price},
    }
