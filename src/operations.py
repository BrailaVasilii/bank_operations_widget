from typing import List, Dict
import re
from datetime import datetime
from collections import Counter


def filter_operations_by_status(operations: List[Dict], status: str) -> List[Dict]:
    """
    Фильтрует операции по указанному статусу.
    :param operations: список операций
    :param status: статус для фильтрации (например, "EXECUTED")
    :return: список отфильтрованных операций
    """
    return [op for op in operations if op.get("state", "").upper() == status.upper()]


def filter_operations_by_description(operations: List[Dict], search_term: str) -> List[Dict]:
    """
    Фильтрует операции по ключевому слову в описании.
    :param operations: список операций
    :param search_term: ключевое слово для поиска
    :return: список операций, где описание содержит ключевое слово
    """
    regex = re.compile(re.escape(search_term), re.IGNORECASE)
    return [op for op in operations if regex.search(op.get("description", ""))]


def sort_operations_by_date(operations: List[Dict], ascending: bool = True) -> List[Dict]:
    """
    Сортирует операции по дате.
    :param operations: список операций
    :param ascending: сортировка по возрастанию (True) или убыванию (False)
    :return: отсортированный список операций
    """

    def parse_date(date_str: str)-> datetime:
        # Попробуем сначала обработать с дробной частью секунд
        try:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            # Если не получилось, попробуем без дробной части секунд
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

    return sorted(operations, key=lambda x: parse_date(x["date"]), reverse=not ascending)


def filter_operations_by_currency(operations: List[Dict], currency: str) -> List[Dict]:
    """
    Фильтрует операции по указанной валюте.
    :param operations: список операций
    :param currency: код валюты (например, "RUB")
    :return: список операций с указанной валютой
    """
    return [
        operation
        for operation in operations
        if operation.get("operationAmount", {}).get("currency", {}).get("code") == currency
    ]


def count_operation_categories(operations: List[Dict]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям (описаниям) с помощью Counter.
    :param operations: список операций
    :return: словарь с категориями и их количеством
    """
    descriptions = [op.get("description", "Неизвестно") for op in operations]
    return dict(Counter(descriptions))
