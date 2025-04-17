import os
from unittest.mock import patch, MagicMock
import requests
import json
from src.external_api import convert_currency_to_rub
from typing import Any


def test_convert_currency_to_rub_success() -> None:
    """Тестирует успешную конвертацию валюты в рубли."""
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "timestamp": 1681780800,
        "base": "USD",
        "date": "2023-04-17",
        "rates": {"RUB": 80.0},
    }
    with patch("requests.get", return_value=mock_response):
        os.environ["EXCHANGE_RATES_API_KEY"] = "test_api_key"
        result: float = convert_currency_to_rub({"currency": "USD", "amount": 10})
        assert abs(result - 800.0) < 1e-6
        del os.environ["EXCHANGE_RATES_API_KEY"]


def test_convert_currency_to_rub_no_api_key() -> None:
    """Тестирует конвертацию при отсутствии API-ключа."""
    original_api_key: Any = os.environ.get("EXCHANGE_RATES_API_KEY")
    result: float  # type: ignore
    try:
        if "EXCHANGE_RATES_API_KEY" in os.environ:
            del os.environ["EXCHANGE_RATES_API_KEY"]
        result = convert_currency_to_rub({"currency": "USD", "amount": 10})
        assert abs(result - 10.0) < 1e-6
    finally:
        if original_api_key is not None:
            os.environ["EXCHANGE_RATES_API_KEY"] = original_api_key
        elif "EXCHANGE_RATES_API_KEY" in os.environ:
            del os.environ["EXCHANGE_RATES_API_KEY"]


def test_convert_currency_to_rub_invalid_amount() -> None:
    """Тестирует обработку некорректной суммы."""
    result: float = convert_currency_to_rub({"currency": "USD", "amount": "abc"})
    assert result == 0.0


def test_convert_currency_to_rub_missing_currency() -> None:
    """Тестирует обработку отсутствующей валюты."""
    result: float = convert_currency_to_rub({"amount": 10})
    assert result == 0.0


def test_convert_currency_to_rub_missing_amount() -> None:
    """Тестирует обработку отсутствующей суммы."""
    result: float = convert_currency_to_rub({"currency": "USD"})
    assert result == 0.0


def test_convert_currency_to_rub_request_exception() -> None:
    """Тестирует обработку ошибки при запросе к API."""
    result: float  # type: ignore
    with patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error")):
        os.environ["EXCHANGE_RATES_API_KEY"] = "test_api_key"
        result = convert_currency_to_rub({"currency": "USD", "amount": 10})
        assert abs(result - 10.0) < 1e-6  # Возвращается исходная сумма
        del os.environ["EXCHANGE_RATES_API_KEY"]


def test_convert_currency_to_rub_json_decode_error() -> None:
    """Тестирует обработку ошибки декодирования JSON."""
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = json.JSONDecodeError("Error decoding JSON", "invalid json", 0)
    result: float  # type: ignore
    with patch("requests.get", return_value=mock_response):
        os.environ["EXCHANGE_RATES_API_KEY"] = "test_api_key"
        result = convert_currency_to_rub({"currency": "USD", "amount": 10})
        assert abs(result - 0.0) < 1e-6


def test_convert_currency_to_rub_no_rub_rate() -> None:
    """Тестирует обработку отсутствия курса RUB в ответе API."""
    mock_response: MagicMock = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "timestamp": 1681780800,
        "base": "USD",
        "date": "2023-04-17",
        "rates": {"EUR": 0.9},
    }
    result: float  # type: ignore
    with patch("requests.get", return_value=mock_response):
        os.environ["EXCHANGE_RATES_API_KEY"] = "test_api_key"
        result = convert_currency_to_rub({"currency": "USD", "amount": 10})
        assert abs(result - 10.0) < 1e-6  # Возвращается исходная сумма
        del os.environ["EXCHANGE_RATES_API_KEY"]


def test_convert_currency_to_rub_unexpected_error() -> None:
    """Тестирует обработку неожиданной ошибки."""
    result: float  # type: ignore
    with patch("requests.get", side_effect=Exception("Unexpected error")):
        os.environ["EXCHANGE_RATES_API_KEY"] = "test_api_key"
        result = convert_currency_to_rub({"currency": "USD", "amount": 10})
        assert abs(result - 0.0) < 1e-6
        del os.environ["EXCHANGE_RATES_API_KEY"]


def test_convert_currency_to_rub_no_api_key_explicit() -> None:
    """Тестирует конвертацию при отсутствии API-ключа (тест явный)."""
    original_api_key: Any = os.environ.get("EXCHANGE_RATES_API_KEY")
    result_eur: float  # type: ignore
    result_rub: float  # type: ignore
    try:
        if "EXCHANGE_RATES_API_KEY" in os.environ:
            del os.environ["EXCHANGE_RATES_API_KEY"]
        result_eur = convert_currency_to_rub({"currency": "EUR", "amount": 20})  # Используем другую валюту
        assert abs(result_eur - 20.0) < 1e-6
        result_rub = convert_currency_to_rub({"currency": "RUB", "amount": 100})
        assert abs(result_rub - 100.0) < 1e-6
    finally:
        if original_api_key is not None:
            os.environ["EXCHANGE_RATES_API_KEY"] = original_api_key
        elif "EXCHANGE_RATES_API_KEY" in os.environ:
            del os.environ["EXCHANGE_RATES_API_KEY"]
