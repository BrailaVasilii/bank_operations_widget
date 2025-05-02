import os

import pytest
from unittest import mock

from _pytest.monkeypatch import MonkeyPatch

from src.data_loader import load_operations_from_json, load_operations_from_csv, load_operations_from_xlsx
from src.operations import (
    filter_operations_by_status,
    filter_operations_by_currency,
    filter_operations_by_description,
    sort_operations_by_date,
    count_operation_categories,
)


@pytest.fixture
def data_dir() -> str:
    """Фикстура для получения пути к папке данных."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "data")


def test_loading_json(data_dir: str) -> None:
    """Тест загрузки операций из JSON-файла."""
    file_path = os.path.join(data_dir, "operations.json")
    operations = load_operations_from_json(file_path)
    assert isinstance(operations, list), "Операции должны быть списком!"
    assert len(operations) > 0, "JSON-файл пустой!"
    assert "description" in operations[0], "Не хватает ключа 'description'!"


def test_loading_csv(data_dir: str) -> None:
    """Тест загрузки операций из CSV-файла."""
    file_path = os.path.join(data_dir, "transactions.csv")
    operations = load_operations_from_csv(file_path)
    assert isinstance(operations, list), "Операции должны быть списком!"
    assert len(operations) > 0, "CSV-файл пуст!"
    assert "description" in operations[0], "Не хватает ключа 'description'!"


def test_loading_xlsx(data_dir: str) -> None:
    """Тест загрузки операций из XLSX-файла."""
    file_path = os.path.join(data_dir, "transactions_excel.xlsx")
    operations = load_operations_from_xlsx(file_path)
    assert isinstance(operations, list), "Операции должны быть списком!"
    assert len(operations) > 0, "XLSX-файл пуст!"
    assert "description" in operations[0], "Не хватает ключа 'description'!"


def test_filter_by_status() -> None:
    """Тест фильтрации по статусу."""
    operations = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
    ]

    filtered = filter_operations_by_status(operations, "EXECUTED")
    assert len(filtered) == 2, "Должно быть 2 операции со статусом EXECUTED!"


def test_filter_by_currency() -> None:
    """Тест фильтрации по валюте."""
    operations = [
        {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "USD"}}},
    ]

    filtered = filter_operations_by_currency(operations, "RUB")
    assert len(filtered) == 1, "Должна быть 1 операция в рублях!"


def test_filter_by_description() -> None:
    """Тест фильтрации по описанию."""
    operations = [
        {"id": 1, "description": "Оплата услуг"},
        {"id": 2, "description": "Перевод на счет"},
        {"id": 3, "description": "Пополнение счета"},
    ]

    filtered = filter_operations_by_description(operations, "счет")
    assert len(filtered) == 2, "Должны быть найдены 2 операции с ключевым словом 'счет'!"


def test_sort_by_date() -> None:
    """Тест сортировки по дате."""
    operations = [
        {"id": 1, "date": "2023-02-01T00:00:00Z"},
        {"id": 2, "date": "2023-01-01T00:00:00Z"},
        {"id": 3, "date": "2023-03-01T00:00:00Z"},
    ]

    sorted_ops = sort_operations_by_date(operations, ascending=True)
    assert sorted_ops[0]["id"] == 2, "Первая операция должна быть самой ранней!"

    sorted_ops_desc = sort_operations_by_date(operations, ascending=False)
    assert sorted_ops_desc[0]["id"] == 3, "Первая операция должна быть самой поздней!"


def test_count_categories() -> None:
    """Тест подсчёта категорий операций."""
    operations = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
    ]

    categories = count_operation_categories(operations)
    assert categories["Перевод организации"] == 2, "Должно быть 2 операции Перевод организации!"
    assert categories["Открытие вклада"] == 1, "Должна быть 1 операция Открытие вклада!"


def test_main_workflow(monkeypatch: MonkeyPatch, data_dir: str) -> None:
    """Тест полного сценария работы main() с имитацией ввода."""
    from src.main import main

    inputs = iter(["1", "EXECUTED", "нет", "нет", "нет"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))  # Имитация ввода с клавиатуры

    mock_json_file = os.path.join(data_dir, "operations.json")

    # Подменяем путь на фиктивный
    with mock.patch("src.data_loader.get_data_file_path", return_value=mock_json_file):
        main()
