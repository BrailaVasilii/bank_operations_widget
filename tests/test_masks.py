# tests/test_masks.py
import pytest
import os
import shutil
import logging
import time
import tempfile
from src.masks import get_mask_account, get_mask_card_number, logger_masks
from src.utils import read_json_file, logger as logger_utils
from logging import Logger, Handler


def clear_log_handlers(logger_obj: Logger) -> None:
    """Удаляет и закрывает все файловые обработчики, с обработкой ошибок."""
    handlers_to_remove: list[Handler] = []
    for handler in logger_obj.handlers:
        if isinstance(handler, logging.FileHandler):
            try:
                handler.close()
            except Exception as e:
                print(f"Ошибка при закрытии обработчика лога: {e}")  # Логируем ошибку
            handlers_to_remove.append(handler)
    for handler in handlers_to_remove:
        logger_obj.removeHandler(handler)
    logger_obj.propagate = False
    logger_obj.disabled = True


def remove_dir_with_retry(log_dir: str) -> None:
    """
    Attempts to remove a directory multiple times with a delay and error handling.
    """
    for attempt in range(5):  # Retry up to 5 times
        try:
            # Remove files within the directory first
            if os.path.exists(log_dir):
                for filename in os.listdir(log_dir):
                    filepath = os.path.join(log_dir, filename)
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                shutil.rmtree(log_dir)
            if not os.path.exists(log_dir):
                break  # Exit loop if rmtree was successful
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error removing directory {log_dir}: {e}")
            if attempt < 4:  # Wait before retrying
                time.sleep(0.5)
            else:
                raise  # Raise the exception after the final attempt


def test_log_directory_creation() -> None:
    """Тестирует создание директории logs и запись в файлы."""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = os.path.join(temp_dir, "logs")  # Create "logs" inside temp dir
        masks_log_file = os.path.join(log_dir, "masks.log")
        utils_log_file = os.path.join(log_dir, "utils.log")

        print(f"log_dir: {log_dir}")  # Debug: Print log_dir value

        # Убедимся, что директории logs нет перед тестом
        if os.path.exists(log_dir):
            shutil.rmtree(log_dir)
        assert not os.path.exists(log_dir)
        print(f"After initial check, os.path.exists(log_dir): {os.path.exists(log_dir)}")  # Debug

        # Create the log directory *before* calling the functions
        os.makedirs(log_dir, exist_ok=True)  # Create the directory

        # Очищаем логгеры перед вызовом функций
        clear_log_handlers(logger_masks)
        clear_log_handlers(logger_utils)

        # Reconfigure loggers to use the temporary directory
        for logger_obj in [logger_masks, logger_utils]:
            for handler in logger_obj.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.close()
            logger_obj.handlers.clear()  # Clear existing handlers
            file_handler = logging.FileHandler(masks_log_file if logger_obj == logger_masks else utils_log_file)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )  # Or use your existing formatter
            file_handler.setFormatter(formatter)
            logger_obj.addHandler(file_handler)
            logger_obj.setLevel(logging.DEBUG)  # Or your desired level
            if logger_obj == logger_masks:
                logger_masks.propagate = True
            if logger_obj == logger_utils:
                logger_utils.propagate = True

        # Вызываем функции, которые должны создать директорию и записать логи
        get_mask_card_number("1234567812345678")
        read_json_file("nonexistent.json")

        # Проверяем, что директория и файлы логов были созданы
        assert os.path.exists(log_dir)
        print(f"After function calls, os.path.exists(log_dir): {os.path.exists(log_dir)}")  # Debug
        assert os.path.exists(masks_log_file)
        assert os.path.exists(utils_log_file)

        # Очищаем логгеры после проверки.
        clear_log_handlers(logger_masks)
        clear_log_handlers(logger_utils)
        logging.shutdown()

        # Удаляем директорию и файлы
        remove_dir_with_retry(log_dir)

        # Проверяем, что директория удалена
        assert not os.path.exists(log_dir)


# Остальная часть вашего тестового файла остается без изменений.
@pytest.mark.parametrize(
    "card_number, expected_result",
    [
        ("1234567812345678", "1234 56** **** 5678"),
        ("123456781234", "1234 56** **** 1234"),
        ("", " ** **** "),
    ],
)
def test_get_mask_card_number(card_number: str, expected_result: str) -> None:
    assert get_mask_card_number(card_number) == expected_result


@pytest.mark.parametrize(
    "account_number, expected_result",
    [
        ("12345678901234567890", "**7890"),
        ("1234", "**1234"),
        ("", "**"),
    ],
)
def test_get_mask_account(account_number: str, expected_result: str) -> None:
    assert get_mask_account(account_number) == expected_result


@pytest.mark.parametrize(
    "card_number, expected_result",
    [
        ("1234abc812345678", "Некорректный номер карты"),
        ("1234 5678 1234 5678", "Некорректный номер карты"),
        ("1234-5678-1234-5678", "Некорректный номер карты"),
        ("12345678901234567", "1234 56** **** 4567"),  # Длина > 16
        ("123456789012345", "1234 56** **** 2345"),  # Длина < 16
        ("1234567890123456", "1234 56** **** 3456"),  # Длина == 16
    ],
)
def test_get_mask_card_number_invalid_format(card_number: str, expected_result: str) -> None:
    assert get_mask_card_number(card_number) == expected_result


@pytest.mark.parametrize(
    "account_number, expected_result",
    [
        ("abc1234567890", "Некорректный номер счета"),
        ("12 34 56 78", "Некорректный номер счета"),
        ("12-34-56-78", "Некорректный номер счета"),
        ("123", "**123"),  # Длина < 4
        ("1234", "**1234"),  # Длина == 4
        ("12345", "**2345"),  # Длина > 4
    ],
)
def test_get_mask_account_invalid_format(account_number: str, expected_result: str) -> None:
    assert get_mask_account(account_number) == expected_result
