import pytest
import pandas as pd
from unittest.mock import patch
from src.utils import load_transactions


def test_load_transactions_success(tmp_path: pytest.TempPathFactory) -> None:
    # Создаем временный тестовый файл Excel
    file_path = tmp_path / "transactions.xlsx"
    df = pd.DataFrame({"Дата операции": ["2023-10-01"], "Сумма операции": [200]})
    df.to_excel(file_path, index=False)

    # Загружаем транзакции через функцию
    result = load_transactions(str(file_path))
    assert not result.empty
    assert list(result.columns) == ["Дата операции", "Сумма операции"]


def test_load_transactions_file_not_found() -> None:
    # Проверяем, что вызывается FileNotFoundError при отсутствии файла
    with pytest.raises(FileNotFoundError, match=r"Файл .* не был найден\. Проверьте путь и существование файла\."):
        load_transactions("non_existing_file.xlsx")


@patch("src.utils.pd.read_excel", side_effect=RuntimeError("Ошибка чтения файла"))
def test_load_transactions_runtime_error(mock_read_excel) -> None:
    # Проверяем, что RuntimeError обрабатывается корректно
    with pytest.raises(RuntimeError, match=r"Ошибка при загрузке файла транзакций: Ошибка чтения файла"):
        load_transactions("example.xlsx")
