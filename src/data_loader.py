import os
import json
import csv
from typing import List, Dict
import openpyxl


def get_data_file_path(base_dir: str, filename: str) -> str:
    """
    Формирует абсолютный путь к файлу в папке данных.
    """
    file_path = os.path.join(base_dir, "data", filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не существует!")
    return file_path


def load_operations_from_json(file_path: str) -> List[Dict]:
    """
    Загружает операции из JSON-файла.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            operations: List[Dict] = json.load(file)
            return operations
        except json.JSONDecodeError:
            raise ValueError("Ошибка чтения JSON. Проверьте содержимое файла.")


def load_operations_from_csv(file_path: str) -> List[Dict]:
    """
    Загружает операции из CSV-файла.
    """
    operations = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            operations.append(
                {
                    "id": row["id"],
                    "state": row["state"],
                    "date": row["date"],
                    "operationAmount": {
                        "amount": row["amount"],
                        "currency": {"name": row["currency_name"], "code": row["currency_code"]},
                    },
                    "description": row["description"],
                    "from": row.get("from", ""),
                    "to": row["to"],
                }
            )
    return operations


def load_operations_from_xlsx(file_path: str) -> List[Dict]:
    """
    Загружает операции из XLSX-файла.
    """
    operations = []
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    if sheet is None:
        raise ValueError("No active sheet found in the workbook.")

    headers = [cell.value for cell in sheet[1]]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        operation = {headers[i]: row[i] for i in range(len(headers))}
        if operation["id"] is None:
            continue
        operations.append(
            {
                "id": operation["id"],
                "state": operation["state"],
                "date": operation["date"],
                "operationAmount": {
                    "amount": operation["amount"],
                    "currency": {"name": operation["currency_name"], "code": operation["currency_code"]},
                },
                "description": operation["description"],
                "from": operation.get("from", ""),
                "to": operation["to"],
            }
        )
    return operations
