# src/utils.py
import logging
import json
from typing import List, Dict, Any
import os

# Настройка логирования для модуля utils
logger = logging.getLogger(__name__)
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
file_handler = logging.FileHandler(os.path.join(logs_dir, "utils.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными о финансовых транзакциях.

    Args:
        file_path: Путь к JSON-файлу.

    Returns:
        Список словарей с данными о транзакциях. Возвращает пустой список,
        если файл не найден, пустой или содержит не список.
        Некорректные элементы списка (не словари) заменяются на пустые словари.
    """
    logger.debug(f"Чтение JSON-файла: {file_path}")
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            logger.debug(f"Тип прочитанных данных: {type(data)}")
            if isinstance(data, list):
                processed_data = []
                for item in data:
                    if isinstance(item, dict):
                        processed_data.append(item)
                        logger.debug(f"Добавлен корректный элемент: {item}")
                    else:
                        processed_data.append({})
                        logger.warning(f"Некорректный элемент (не словарь) заменен на пустой словарь: {item}")
                logger.info(f"Файл успешно прочитан. Обработано {len(processed_data)} элементов.")
                return processed_data
            else:
                logger.warning("Корневой элемент файла не является списком. Возвращен пустой список.")
                return []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        return []
    except Exception as e:
        logger.critical(f"Непредвиденная ошибка при чтении файла {file_path}: {e}")
        return []
