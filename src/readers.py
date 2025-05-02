import pandas as pd
import logging
import json
from typing import List, Dict, Any, Hashable

# Конфигурация логгера (должна быть выполнена только один раз в модуле)
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


def read_csv_transactions(file_path: str) -> List[Dict[Hashable, Any]]:
    """
    Читает транзакции из CSV-файла.

    Args:
        file_path (str): Путь к CSV-файлу.

    Returns:
        list: Список словарей, где каждый словарь представляет транзакцию.
              Возвращает пустой список, если файл пуст или не существует.
    Raises:
        FileNotFoundError: Если файл не существует.
    """
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            return []
        else:
            return df.to_dict(orient="records")

    except FileNotFoundError:
        logging.error(f"CSV-файл не найден: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Ошибка при чтении CSV-файла: {e}")
        empty_list: List[Dict[Hashable, Any]] = []
        return empty_list


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает транзакции из Excel-файла.

    Args:
        file_path (str): Путь к Excel-файлу.

    Returns:
        list: Список словарей, где каждый словарь представляет транзакцию.
              Возвращает пустой список, если файл пуст или не существует.
    Raises:
        FileNotFoundError: Если файл не существует.
    """
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            return []
        else:
            # Явно преобразуем ключи в str.
            return [{str(k): v for k, v in record.items()} for record in df.to_dict(orient="records")]
    except FileNotFoundError:
        logging.error(f"Excel-файл не найден: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Ошибка при чтении Excel-файла: {e}")
        return []


def read_operations_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает операции из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        list: Список словарей, где каждый словарь представляет операцию.
              Возвращает пустой список, если файл пуст или не существует.
    Raises:
        FileNotFoundError: Если файл не существует.
        json.JSONDecodeError: Если JSON-файл недействителен.
    """

    empty_list: List[Dict[str, Any]] = []
    try:
        with open(file_path, "r") as f:
            data: List[Dict[str, Any]] = json.load(f)
        return data
    except FileNotFoundError:
        logging.error(f"JSON-файл не найден: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка при декодировании JSON из файла {file_path}: {e}")
        return empty_list
    except Exception as e:
        logging.error(f"Ошибка при чтении JSON-файла: {e}")
        return empty_list
