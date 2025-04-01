from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.

    Args:
        transactions (list): Список словарей с транзакциями.
        currency_code (str): Код валюты для фильтрации.

    Yields:
        dict: Транзакция, соответствующая заданной валюте.
    """
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генерирует описания транзакций.

    Args:
        transactions (list): Список словарей с транзакциями.

    Yields:
        str: Описание транзакции.
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне.

    Args:
        start (int): Начальное значение диапазона.
        stop (int): Конечное значение диапазона.

    Yields:
        str: Номер банковской карты в формате XXXX XXXX XXXX XXXX.
    """
    for i in range(start, stop + 1):
        yield f"{i:016d}"[:4] + " " + f"{i:016d}"[4:8] + " " + f"{i:016d}"[8:12] + " " + f"{i:016d}"[12:]
