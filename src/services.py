import requests
import pandas as pd
import json
from typing import Dict, Any, List


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму инвестиций через округление трат.
    """
    total_savings = 0.0
    for transaction in transactions:
        if transaction["Дата операции"].startswith(month):
            amount = transaction["Сумма операции"]
            total_savings += limit - (amount % limit) if amount % limit != 0 else 0.0
    return round(total_savings, 2)


def get_currency_rate(base: str, symbols: List[str]) -> Dict[str, float]:
    """
    Получает курсы валют с API для заданной базовой валюты и списка валют.
    """
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        rates = response.json().get("rates", {})
        # Удаляем валюты, если они отсутствуют в ответе API
        return {symbol: rates.get(symbol, 0.0) for symbol in symbols}
    except requests.RequestException as e:
        print(f"Ошибка API: {e}")
        return {symbol: 0.0 for symbol in symbols}  # Default значения


def get_stock_price(stock_symbol: str) -> float:
    """
    Получает текущую цену акции через Yahoo Finance API.
    """
    url = "https://query1.finance.yahoo.com/v7/finance/quote"
    try:
        response = requests.get(url, params={"symbols": stock_symbol})
        response.raise_for_status()
        result = response.json()
        price = result.get("quoteResponse", {}).get("result", [{}])[0].get("regularMarketPrice", None)
        return float(price) if price is not None else 0.0
    except (requests.RequestException, IndexError, KeyError) as e:
        print(f"Ошибка API для {stock_symbol}: {e}")
        return 0.0


def analyze_cashback_categories(data: pd.DataFrame, year: int, month: int) -> Dict[str, float]:
    """
    Анализирует, сколько можно заработать повышенного кешбэка по категориям.
    """
    data["Дата операции"] = pd.to_datetime(data["Дата операции"])
    filtered = data[(data["Дата операции"].dt.year == year) & (data["Дата операции"].dt.month == month)]
    cashback_by_category = filtered.groupby("Категория")["Сумма операции"].sum() * 0.05
    return cashback_by_category.round(2).to_dict()


def simple_search(data: pd.DataFrame, query: str) -> List[Dict[str, Any]]:
    """
    Выполняет поиск по строке в колонках "Описание" и "Категория".
    """
    filtered = data[
        data["Описание"].str.contains(query, case=False, na=False)
        | data["Категория"].str.contains(query, case=False, na=False)
    ]
    return json.loads(filtered.to_json(orient="records", force_ascii=False))


def search_phone_numbers(data: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Находит транзакции с телефонными номерами в строке "Описание".
    """
    phone_pattern = r"\+7\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}"
    filtered = data[data["Описание"].str.contains(phone_pattern, regex=True, na=False)]
    return json.loads(filtered.to_json(orient="records", force_ascii=False))


def search_person_transfers(data: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Находит транзакции перевода физическим лицам.
    """
    pattern = r"[А-ЯЁ][а-яё]+\s[А-ЯЁ]\."
    filtered = data[(data["Категория"] == "Переводы") & (data["Описание"].str.contains(pattern, regex=True, na=False))]
    return json.loads(filtered.to_json(orient="records", force_ascii=False))
