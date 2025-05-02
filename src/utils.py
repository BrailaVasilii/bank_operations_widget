import os
import pandas as pd


def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Загружает транзакции из файла Excel. Если файл отсутствует, выбрасывается ошибка.
    """
    # Построение абсолютного пути относительно родительской директории `src`
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Поднимаемся на один уровень выше
    full_path = os.path.join(base_dir, file_path)

    try:
        # Читаем Excel файл
        return pd.read_excel(full_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {full_path} не был найден. Проверьте путь и существование файла.")
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке файла транзакций: {e}")
