import os
import pytest
from src.data_loader import load_operations_from_json, load_operations_from_csv, load_operations_from_xlsx


@pytest.fixture
def data_dir() -> str:
    """Возвращает путь к папке `data`."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "data")


def test_load_operations_from_json(data_dir: str) -> None:
    """Тестирует загрузку операций из JSON-файла."""
    file_path = os.path.join(data_dir, "operations.json")

    # Убедимся, что файл существует
    assert os.path.exists(file_path), f"Файл {file_path} не найден!"

    # Загружаем данные
    operations = load_operations_from_json(file_path)

    # Проверяем важные аспекты данных
    assert len(operations) > 0, "JSON-файл пустой!"
    assert isinstance(operations, list), "Ожидался список операций!"
    assert "description" in operations[0], "Не хватает ключа 'description' в JSON-объектах!"


def test_load_operations_from_csv(data_dir: str) -> None:
    """Тестирует загрузку операций из CSV-файла."""
    file_path = os.path.join(data_dir, "transactions.csv")

    # Убедимся, что CSV-файл существует
    assert os.path.exists(file_path), f"Файл {file_path} не найден!"

    # Загружаем данные
    operations = load_operations_from_csv(file_path)

    # Проверяем важные аспекты данных
    assert len(operations) > 0, "CSV-файл пуст!"
    assert isinstance(operations, list), "Ожидался список операций!"
    assert "description" in operations[0], "Не хватает ключа 'description' в CSV-операциях!"


def test_load_operations_from_xlsx(data_dir: str) -> None:
    """Тестирует загрузку операций из XLSX-файла."""
    file_path = os.path.join(data_dir, "transactions_excel.xlsx")

    # Убедимся, что XLSX-файл существует
    assert os.path.exists(file_path), f"Файл {file_path} не найден!"

    # Загружаем данные
    operations = load_operations_from_xlsx(file_path)

    # Проверяем важные аспекты данных
    assert len(operations) > 0, "XLSX-файл пуст!"
    assert isinstance(operations, list), "Ожидался список операций!"
    assert "description" in operations[0], "Не хватает ключа 'description' в XLSX-операциях!"


def test_load_file_not_found(data_dir: str) -> None:
    """Проверяет обработку ошибки при отсутствии файла."""
    invalid_file = os.path.join(data_dir, "nonexistent.json")

    with pytest.raises(FileNotFoundError):
        load_operations_from_json(invalid_file)
