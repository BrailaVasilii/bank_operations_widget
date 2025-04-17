import json
from typing import List, Dict, Any


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
    try:
        with open(file_path, "r") as f:
            data = json.load(f)  # Загрузка данных из JSON-файла
            print(f"Tipul datelor citite: {type(data)}")  # Временно добавлено для отладки
            if isinstance(data, list):
                processed_data = []
                for item in data:
                    if isinstance(item, dict):
                        processed_data.append(item)  # Добавление корректного словаря
                    else:
                        processed_data.append({})  # Замена некорректного элемента пустым словарём
                return processed_data
            else:
                return []  # Возврат пустого списка, если корневой элемент не список
    except FileNotFoundError:
        return []  # Возврат пустого списка, если файл не найден
    except json.JSONDecodeError:
        print("Eroare: Nu a reușit decodificarea răspunsului API")
        return []  # Возврат пустого списка при ошибке декодирования JSON
    except Exception as e:
        print(f"O altă eroare la citirea fișierului: {e}")
        return []  # Возврат пустого списка при других ошибках чтения файла
