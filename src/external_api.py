# src/external_api.py
import os
import requests
import json
from typing import Dict, Any, Optional

EXCHANGE_RATES_API_URL: str = "https://api.apilayer.com/exchangerates_data/latest"


def convert_currency_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму в рубли, используя внешний API.

    Args:
        transaction: Словарь с информацией о транзакции, содержащий ключи 'currency' (валюта)
                     и 'amount' (сумма).

    Returns:
        Сумма в рублях (float). Возвращает 0.0 в случае отсутствия необходимых данных
        или ошибок преобразования.
    """
    currency: Optional[str] = transaction.get("currency")
    amount_str: Optional[Any] = transaction.get("amount")

    if not currency or amount_str is None:
        return 0.0

    try:
        amount: float = float(amount_str)
    except ValueError:
        return 0.0

    if currency == "RUB":
        return amount

    api_key: Optional[str] = os.environ.get("EXCHANGE_RATES_API_KEY")
    if not api_key:
        print("API ключ для курсов валют не установлен. Возвращается исходная сумма.")
        return amount

    headers: Dict[str, str] = {"apikey": api_key}
    params: Dict[str, str] = {"symbols": "RUB", "base": currency.upper()}

    try:
        response: requests.Response = requests.get(EXCHANGE_RATES_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
        rates: Optional[Dict[str, float]] = data.get("rates")
        if rates and "RUB" in rates:
            return amount * float(rates["RUB"])
        else:
            print(f"Не удалось найти курс RUB для {currency}.")
            return amount
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return amount
    except json.JSONDecodeError:
        print("Ошибка декодирования ответа курса валют.")
        return 0.0
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return 0.0
