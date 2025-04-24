import unittest
import os
import pandas as pd
from src.readers import read_csv_transactions, read_excel_transactions, read_operations_json
import json
import logging


# Конфигурация логгера для тестов
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Определение константы для пути к директории с тестовыми данными
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Названия тестовых файлов
EMPTY_CSV_FILE = os.path.join(TEST_DATA_DIR, "empty.csv")
EMPTY_EXCEL_FILE = os.path.join(TEST_DATA_DIR, "empty.xlsx")
TRANSACTIONS_CSV_FILE = os.path.join(TEST_DATA_DIR, "transactions.csv")
TRANSACTIONS_EXCEL_FILE = os.path.join(TEST_DATA_DIR, "transactions.xlsx")
OPERATIONS_JSON_FILE = os.path.join(TEST_DATA_DIR, "operations.json")


def create_test_files() -> None:
    """
    Создает тестовые файлы, необходимые для тестирования функций чтения.
    """
    os.makedirs(TEST_DATA_DIR, exist_ok=True)

    # Создает пустой CSV-файл
    with open(EMPTY_CSV_FILE, "w", newline="") as f:
        f.write("")

    # Создает пустой Excel-файл
    df_empty = pd.DataFrame()
    df_empty.to_excel(EMPTY_EXCEL_FILE, index=False)

    # Создает CSV-файл с транзакциями
    transactions_data = {
        "id": [1, 2, 3],
        "user_id": [101, 102, 101],
        "amount": [100.00, -50.00, 25.00],
        "type": ["deposit", "withdrawal", "deposit"],
    }
    df_transactions = pd.DataFrame(transactions_data)
    df_transactions.to_csv(TRANSACTIONS_CSV_FILE, index=False)

    # Создает Excel-файл с транзакциями
    df_transactions.to_excel(TRANSACTIONS_EXCEL_FILE, index=False)

    # Создает JSON-файл с операциями
    operations_data = [
        {"operation_id": "op1", "user_id": 101, "details": "Deposit of 100"},
        {"operation_id": "op2", "user_id": 102, "details": "Withdrawal of 50"},
    ]
    with open(OPERATIONS_JSON_FILE, "w") as f:
        json.dump(operations_data, f)


class TestReaders(unittest.TestCase):
    """
    Класс для тестирования функций из модуля readers.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Метод класса, который выполняется один раз перед всеми тестами в классе.
        Создает необходимые тестовые файлы.
        """
        create_test_files()

    def test_read_csv_transactions_success(self) -> None:
        """
        Тестирует успешное чтение транзакций из CSV-файла.
        """
        transactions = read_csv_transactions(TRANSACTIONS_CSV_FILE)
        self.assertEqual(len(transactions), 3)
        self.assertEqual(transactions[0]["id"], 1)
        self.assertEqual(transactions[0]["user_id"], 101)
        self.assertEqual(transactions[0]["amount"], 100.00)
        self.assertEqual(transactions[0]["type"], "deposit")

    def test_read_csv_transactions_empty_file(self) -> None:
        """
        Тестирует чтение из пустого CSV-файла.
        """
        transactions = read_csv_transactions(EMPTY_CSV_FILE)
        self.assertEqual(transactions, [])

    def test_read_csv_transactions_file_not_found(self) -> None:
        """
        Тестирует сценарий, когда CSV-файл не существует.
        """
        with self.assertRaises(FileNotFoundError):
            read_csv_transactions("non_existent.csv")

    def test_read_excel_transactions_success(self) -> None:
        """
        Тестирует успешное чтение транзакций из Excel-файла.
        """
        transactions = read_excel_transactions(TRANSACTIONS_EXCEL_FILE)
        self.assertEqual(len(transactions), 3)
        self.assertEqual(transactions[0]["id"], 1)
        self.assertEqual(transactions[0]["user_id"], 101)
        self.assertEqual(transactions[0]["amount"], 100.00)
        self.assertEqual(transactions[0]["type"], "deposit")

    def test_read_excel_transactions_empty_file(self) -> None:
        """
        Тестирует чтение из пустого Excel-файла.
        """
        transactions = read_excel_transactions(EMPTY_EXCEL_FILE)
        self.assertEqual(transactions, [])

    def test_read_excel_transactions_file_not_found(self) -> None:
        """
        Тестирует сценарий, когда Excel-файл не существует.
        """
        with self.assertRaises(FileNotFoundError):
            read_excel_transactions("non_existent.xlsx")

    def test_read_operations_json_success(self) -> None:
        """
        Тестирует успешное чтение операций из JSON-файла.
        """
        operations = read_operations_json(OPERATIONS_JSON_FILE)
        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0]["operation_id"], "op1")
        self.assertEqual(operations[0]["user_id"], 101)
        self.assertEqual(operations[0]["details"], "Deposit of 100")

    def test_read_operations_json_empty_file(self) -> None:
        """
        Тестирует чтение из пустого JSON-файла.
        """
        empty_json_file = os.path.join(TEST_DATA_DIR, "empty.json")
        with open(empty_json_file, "w") as f:
            f.write("[]")

        operations = read_operations_json(empty_json_file)
        self.assertEqual(operations, [])
        os.remove(empty_json_file)

    def test_read_operations_json_file_not_found(self) -> None:
        """
        Тестирует сценарий, когда JSON-файл не существует.
        """
        with self.assertRaises(FileNotFoundError):
            read_operations_json("non_existent.json")

    def test_read_operations_json_invalid_json(self) -> None:
        """
        Тестирует сценарий, когда JSON-файл содержит недействительные данные JSON.
        """
        invalid_json_file = os.path.join(TEST_DATA_DIR, "invalid.json")
        with open(invalid_json_file, "w") as f:
            f.write("invalid json data")

        operations = read_operations_json(invalid_json_file)
        self.assertEqual(operations, [])
        os.remove(invalid_json_file)
